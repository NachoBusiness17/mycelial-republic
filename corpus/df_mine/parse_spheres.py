# Parses Dwarf Fortress READ-ONLY raws into df_spheres.json + df_bestiary.json.
# Stratum: SPHERES + MEGABEASTS (closes the fleet OWED item: wiki renders spheres as image only).
# Sources:
#   data/vanilla/vanilla_creatures*/objects/*.txt  -> [SPHERE:X] census + boss roster
#   data/init/globals.lua                          -> canonical sphere list (random_sphere_adjective keys),
#                                                     evil_spheres / good_spheres
#   data/vanilla/vanilla_procedural/.../creatures.lua -> regiontype sphere sets for FB/titan generation
import json, re
from pathlib import Path

DF = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Dwarf Fortress")
OUT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent\corpus\df_mine")

CREATURE_DIRS = ["vanilla_creatures", "vanilla_creatures_extinct"]
TAG_RE = re.compile(r"\[([A-Z_0-9]+)(?::([^\]]*))?\]")

# ---- 1. canonical sphere data from globals.lua -------------------------------
globals_lua = (DF / "data" / "init" / "globals.lua").read_text(encoding="utf-8", errors="replace")

def lua_string_list(name):
    m = re.search(name + r"\s*=\s*\{(.*?)\}", globals_lua, re.S)
    return re.findall(r'"([A-Z_]+)"', m.group(1)) if m else []

evil_spheres = lua_string_list("evil_spheres")
good_spheres = lua_string_list("good_spheres")

m = re.search(r"random_sphere_adjective\s*=\s*\{(.*?)\n\}", globals_lua, re.S)
canonical_spheres = sorted(re.findall(r"^\s*([A-Z_]+)=\{", m.group(1), re.M)) if m else []

# ---- 2. procedural generator sphere sets (forgotten beasts / titans) ---------
creatures_lua = (DF / "data" / "vanilla" / "vanilla_procedural" / "scripts" /
                 "generators" / "creatures.lua").read_text(encoding="utf-8", errors="replace")
region_spheres = {}
rt = re.search(r"regiontypes\s*=\s*\{(.*?)\n\}\n", creatures_lua, re.S)
if rt:
    for name, body in re.findall(r"^\s{4}([A-Z_]+)=\{\s*spheres=\{(.*?)\}", rt.group(1), re.S | re.M):
        region_spheres[name] = sorted(set(re.findall(r"([A-Z_]+)=true", body)))

# ---- 3. creature raw scan ----------------------------------------------------
NOTABLE = {
    "NODEFEAT", "TRAPAVAIL", "BUILDINGDESTROYER", "LARGE_PREDATOR", "NOFEAR", "NOPAIN",
    "NOEXERT", "NOSTUN", "PARALYZEIMMUNE", "FIREIMMUNE", "FIREIMMUNE_SUPER", "WEBIMMUNE",
    "CAN_LEARN", "CAN_SPEAK", "POWER", "ITEM_THIEF", "CURIOUSBEAST_ITEM",
    "CURIOUSBEAST_GUZZLER", "FANCIFUL", "DOES_NOT_EXIST", "AMPHIBIOUS", "AQUATIC",
    "FLIER", "NOBREATHE", "BONECARN", "TRAINABLE", "PET_EXOTIC", "MOUNT_EXOTIC",
    "LAIR", "NOEMOTION", "LARGE_ROAMING", "VERMIN_HUNTER", "MEGABEAST", "SEMIMEGABEAST",
    "TITAN", "FEATURE_BEAST", "UNIQUE_DEMON", "DEMON",
}

def parse_creature_block(token, lines):
    rec = {"token": token, "name": None, "classes": [], "difficulty": None,
           "spheres": [], "size_cm3": None, "biomes": [], "attacks": [], "notable": []}
    interaction = None
    attack = None
    for ln in lines:
        for m in TAG_RE.finditer(ln):
            tag, args = m.group(1), m.group(2)
            a = args.split(":") if args is not None else []
            if tag == "NAME" and rec["name"] is None and a:
                rec["name"] = a[0]
            elif tag == "CASTE_NAME" and rec["name"] is None and a:
                rec["name"] = a[0]
            elif tag in ("MEGABEAST", "SEMIMEGABEAST", "TITAN", "FEATURE_BEAST",
                         "UNIQUE_DEMON", "DEMON"):
                if tag not in rec["classes"]:
                    rec["classes"].append(tag)
                if tag not in rec["notable"]:
                    rec["notable"].append(tag)
            elif tag == "DIFFICULTY" and a:
                rec["difficulty"] = int(a[0]) if a[0].isdigit() else a[0]
            elif tag == "SPHERE" and a:
                s = a[0].upper()
                if s not in rec["spheres"]:
                    rec["spheres"].append(s)
            elif tag == "BODY_SIZE" and len(a) >= 3 and a[2].isdigit():
                sz = int(a[2])  # last BODY_SIZE = adult size
                if rec["size_cm3"] is None or sz > rec["size_cm3"]:
                    rec["size_cm3"] = sz
            elif tag == "BIOME" and a and a[0] not in rec["biomes"]:
                rec["biomes"].append(a[0])
            elif tag == "ATTACK" and a:
                attack = {"type": a[0], "verb": None, "special": []}
                rec["attacks"].append(attack)
            elif tag == "ATTACK_VERB" and attack is not None:
                attack["verb"] = ":".join(a)
            elif tag == "ATTACK_SPECIAL" and attack is not None:
                attack["special"].append(a[0] if a else "")
            elif tag == "SPECIALATTACK":
                rec["attacks"].append({"type": "SPECIALATTACK", "args": a})
            elif tag == "CAN_DO_INTERACTION":
                interaction = {"type": "INTERACTION", "id": a[0] if a else None,
                               "adv_name": None, "flow": None, "verb": None,
                               "usage_hint": None}
                rec["attacks"].append(interaction)
            elif tag == "CDI" and interaction is not None and a:
                if a[0] == "ADV_NAME":
                    interaction["adv_name"] = ":".join(a[1:])
                elif a[0] == "FLOW":
                    interaction["flow"] = a[1] if len(a) > 1 else None
                elif a[0] == "VERB":
                    interaction["verb"] = ":".join(a[1:])
                elif a[0] == "USAGE_HINT":
                    interaction["usage_hint"] = a[1] if len(a) > 1 else None
            elif tag in NOTABLE and tag not in rec["notable"]:
                rec["notable"].append(tag)
    return rec

creatures = []
sphere_usage = {}
by_creature = {}
occurrences = 0
for d in CREATURE_DIRS:
    for f in sorted((DF / "data" / "vanilla" / d / "objects").glob("*.txt")):
        cur_tok, cur_lines = None, []
        def flush():
            global occurrences
            if cur_tok is None:
                return
            rec = parse_creature_block(cur_tok, cur_lines)
            creatures.append(rec)
            for s in rec["spheres"]:
                sphere_usage[s] = sphere_usage.get(s, 0) + 1
                occurrences += 1
            if rec["spheres"]:
                by_creature.setdefault(rec["name"] or rec["token"], []).extend(rec["spheres"])
        text = f.read_text(encoding="utf-8", errors="replace")
        for ln in text.splitlines():
            m0 = re.match(r"\[CREATURE:([A-Z_0-9]+)\]", ln.strip())
            if m0:
                flush()
                cur_tok, cur_lines = m0.group(1), []
            elif cur_tok is not None:
                cur_lines.append(ln)
        flush()

def flush():  # rebind as plain function for module-level use
    pass

# ---- 4. assemble deliverables ------------------------------------------------
seen_spheres = sorted(set(sphere_usage) | set(canonical_spheres))

spheres_doc = {
    "source": "Dwarf Fortress install (READ-ONLY): data/vanilla/vanilla_creatures*/objects/*.txt + data/init/globals.lua + vanilla_procedural generators",
    "spheres": seen_spheres,
    "canonical_sphere_count": len(canonical_spheres),
    "canonical_source": "globals.lua random_sphere_adjective keys ('-- mods can add more')",
    "evil_spheres": evil_spheres,
    "good_spheres": good_spheres,
    "usage": dict(sorted(sphere_usage.items())),
    "sphere_occurrences_total": occurrences,
    "by_creature": dict(sorted(by_creature.items())),
    "generator_region_spheres": region_spheres,
}

CLASS_RANK = {"MEGABEAST": "megabeast", "TITAN": "titan", "SEMIMEGABEAST": "semimegabeast",
              "FEATURE_BEAST": "feature_beast", "UNIQUE_DEMON": "unique_demon", "DEMON": "demon"}

def best_class(rec):
    for c in ("MEGABEAST", "TITAN", "SEMIMEGABEAST", "FEATURE_BEAST", "UNIQUE_DEMON", "DEMON"):
        if c in rec["classes"]:
            return CLASS_RANK[c]
    return "boss_difficulty" if rec["difficulty"] is not None else None

roster = []
difficulty_rated = []
for rec in creatures:
    cls = best_class(rec)
    if cls in CLASS_RANK.values():
        entry = {"name": rec["name"] or rec["token"], "token": rec["token"], "class": cls}
        if rec["difficulty"] is not None:
            entry["difficulty"] = rec["difficulty"]
        entry["spheres"] = rec["spheres"]
        entry["size_cm3"] = rec["size_cm3"]
        entry["attacks"] = [a for a in rec["attacks"]
                            if a["type"] != "INTERACTION"
                            and (a.get("verb") or a.get("args") or a.get("special"))
                            or (a["type"] == "INTERACTION"
                                and (a.get("usage_hint") == "ATTACK" or a.get("flow")))]
        entry["biomes"] = rec["biomes"]
        entry["notable"] = [t for t in rec["notable"] if t not in rec["classes"]]
        roster.append(entry)
    elif rec["difficulty"] is not None:
        difficulty_rated.append({"name": rec["name"] or rec["token"], "token": rec["token"],
                                 "difficulty": rec["difficulty"], "size_cm3": rec["size_cm3"],
                                 "biomes": rec["biomes"]})

bestiary_doc = {
    "source": "Dwarf Fortress install (READ-ONLY): data/vanilla/vanilla_creatures/objects/*.txt",
    "note": "TITAN and FEATURE_BEAST classes are 100% procedurally generated in vanilla (see procedural_templates); only fixed bosses are raw-written creatures.",
    "roster": sorted(roster, key=lambda r: (r["class"], r["name"])),
    "difficulty_rated_wildlife": sorted(difficulty_rated, key=lambda r: (-r["difficulty"], r["name"])),
    "procedural_templates": {
        "forgotten_beast": {
            "class": "feature_beast", "difficulty": 10, "min_size_cm3": 10000000,
            "base_spheres": ["CAVERNS"], "plus": "WATER if aquatic layer, + 1 random evil sphere",
            "biomes": ["SUBTERRANEAN_WATER (layer 0)", "SUBTERRANEAN_CHASM"],
            "skills": "wrestling/bite/grasp/stance/melee/dodging 6, situational_awareness 6",
            "flags": ["NO_GENDER", "CARNIVORE", "LARGE_PREDATOR", "is_evil"],
        },
        "titan": {
            "class": "titan", "difficulty": 10, "min_size_cm3": 10000000,
            "spheres": "regiontype sphere set + 1 evil sphere (evil region) or 1 good sphere (good region); none otherwise",
            "region_spheres": region_spheres,
            "lair": "SHRINE:100", "flags": ["NO_GENDER", "NO_DRINK", "NO_EAT", "NO_SLEEP",
                                            "LARGE_PREDATOR (or BENIGN if good)"],
        },
        "demon": {
            "class": "demon", "difficulty": "variable", "biome": "SUBTERRANEAN_CHASM depth 5",
            "flags": ["LARGE_ROAMING", "LARGE_PREDATOR", "force_goo", "intangible_flier option",
                      "fixed_temp 10040", "brimstone odor", "fire_immune"],
            "unique_demon": {"flags": ["UNIQUE_DEMON", "SPREAD_EVIL_SPHERES_IF_RULER",
                                       "CAN_LEARN", "CAN_SPEAK"], "skills_at": 14},
        },
    },
}

(OUT / "df_spheres.json").write_text(json.dumps(spheres_doc, indent=2), encoding="utf-8")
(OUT / "df_bestiary.json").write_text(json.dumps(bestiary_doc, indent=2), encoding="utf-8")

print("canonical spheres:", len(canonical_spheres))
print("seen sphere tokens (union):", len(seen_spheres))
print("[SPHERE:] occurrences in creature raws:", occurrences)
print("roster size:", len(roster))
for r in roster:
    print(" -", r["class"], "|", r["name"], "| spheres:", r["spheres"], "| size:", r["size_cm3"],
          "| diff:", r.get("difficulty"), "| biomes:", r["biomes"])
print("usage:", json.dumps(sphere_usage, indent=0))
print("region_spheres:", json.dumps(region_spheres))
print("evil:", evil_spheres)
print("good:", good_spheres)
