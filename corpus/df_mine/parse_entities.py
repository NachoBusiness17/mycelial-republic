# Parses DF entity_default.txt (READ-ONLY source) into df_entities.json.
# Stratum: civilizations, ethics, values, positions, punishments.
import json, re
from pathlib import Path

SRC = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Dwarf Fortress\data\vanilla\vanilla_entities\objects\entity_default.txt")
OUT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent\corpus\df_mine\df_entities.json")

text = SRC.read_text(encoding="utf-8", errors="replace")
lines = text.splitlines()

# tokenize [TAG:arg...] per line, keep indentation depth
toks = []  # (depth, tag, args)
for ln in lines:
    stripped = ln.strip()
    depth = (len(ln) - len(ln.lstrip())) // 1
    for m in re.finditer(r"\[([A-Z_0-9]+)(?::([^\]]*))?\]", stripped):
        tag = m.group(1)
        args = m.group(2).split(":") if m.group(2) is not None else []
        toks.append((depth, tag, args))

entities = []
cur = None
pos = None
style = None

def flush_pos():
    global pos
    if pos is not None and cur is not None:
        cur["positions"].append(pos)
        pos = None

for depth, tag, args in toks:
    if tag == "ENTITY" and depth == 0:
        flush_pos()
        cur = {"id": args[0], "ethics": {}, "values": None, "variable_values": None,
               "positions": [], "variable_positions": False, "site_variable_positions": False,
               "banditry": None, "local_banditry": False, "punishment_flags": [], "creature": [], "religion": [], "site_type": None}
        entities.append(cur)
        continue
    if cur is None:
        continue
    if depth == 1:
        if tag == "POSITION":
            flush_pos()
            pos = {"id": args[0], "name": None, "name_male": None, "name_female": None,
                   "number": None, "succession": None, "appointed_by": [], "replaced_by": None,
                   "responsibilities": [], "precedence": None, "squad": None, "execution_skill": None,
                   "flags": [], "requirements": {}}
            continue
        flush_pos()
        if tag == "ETHIC":
            cur["ethics"][args[0]] = args[1]
        elif tag == "VALUE":
            if cur["values"] is None:
                cur["values"] = {}
            cur["values"][args[0]] = int(args[1])
        elif tag == "VARIABLE_VALUE":
            cur["variable_values"] = {"scope": args[0], "min": int(args[1]), "max": int(args[2])}
        elif tag == "VARIABLE_POSITIONS":
            cur["variable_positions"] = args[0] if args else True
        elif tag == "SITE_VARIABLE_POSITIONS":
            cur["site_variable_positions"] = args[0] if args else True
        elif tag == "BANDITRY":
            cur["banditry"] = int(args[0])
        elif tag == "LOCAL_BANDITRY":
            cur["local_banditry"] = True
        elif tag == "CREATURE":
            cur["creature"].append(args[0])
        elif tag == "RELIGION":
            cur["religion"].append(args[0])
        elif tag == "DEFAULT_SITE_TYPE":
            cur["site_type"] = args[0]
        elif tag in ("PUNISHMENT_EXCLUSIVE", "EXECUTION_STYLE", "CRIMINAL"):
            cur["punishment_flags"].append({"tag": tag, "args": args})
        continue
    # depth >= 2: inside POSITION or TISSUE_STYLE blocks
    if depth >= 2 and cur is not None:
        if tag == "POSITION":
            flush_pos()
            pos = {"id": args[0], "name": None, "name_male": None, "name_female": None,
                   "number": None, "succession": None, "appointed_by": [], "replaced_by": None,
                   "responsibilities": [], "precedence": None, "squad": None, "execution_skill": None,
                   "flags": [], "requirements": {}}
            continue
        if pos is not None:
            if tag == "NAME" and len(args) >= 1:
                pos["name"] = ":".join(args)
            elif tag == "NAME_MALE":
                pos["name_male"] = ":".join(args)
            elif tag == "NAME_FEMALE":
                pos["name_female"] = ":".join(args)
            elif tag == "NUMBER":
                pos["number"] = args[0] if args else "1"
            elif tag == "SUCCESSION":
                pos["succession"] = ":".join(args)
            elif tag == "APPOINTED_BY":
                pos["appointed_by"].append(args[0])
            elif tag == "REPLACED_BY":
                pos["replaced_by"] = args[0]
            elif tag == "RESPONSIBILITY":
                pos["responsibilities"].append(args[0])
            elif tag == "PRECEDENCE":
                pos["precedence"] = int(args[0])
            elif tag == "SQUAD":
                pos["squad"] = ":".join(args)
            elif tag == "EXECUTION_SKILL":
                pos["execution_skill"] = args[0]
            elif tag in ("REQUIRED_BOXES", "REQUIRED_CABINETS", "REQUIRED_RACKS", "REQUIRED_STANDS",
                          "REQUIRED_OFFICE", "REQUIRED_BEDROOM", "REQUIRED_DINING", "REQUIRED_TOMB",
                          "DEMAND_MAX", "MANDATE_MAX", "REQUIRES_POPULATION"):
                pos["requirements"][tag] = int(args[0]) if args else True
            elif tag == "REQUIRES_MARKET":
                pos["requirements"]["REQUIRES_MARKET"] = True
            else:
                pos["flags"].append(tag)
flush_pos()

# punishment summary per entity
PUNISH_TOKENS = {"PUNISH_CAPITAL", "PUNISH_SERIOUS", "PUNISH_EXILE", "PUNISH_REPRIMAND"}
CRIME_ACTS = {"TREASON","OATH_BREAKING","LYING","VANDALISM","TRESPASSING","THEFT","ASSAULT","SLAVERY",
              "KILL_ENTITY_MEMBER","TORTURE_AS_EXAMPLE"}
for e in entities:
    e["punishments"] = {act: resp for act, resp in e["ethics"].items() if resp in PUNISH_TOKENS}
    e["enforcement_positions"] = [
        p["id"] for p in e["positions"]
        if "LAW_ENFORCEMENT" in p["responsibilities"] or "EXECUTIONS" in p["responsibilities"]
    ]

doc = {
    "source": str(SRC),
    "source_readonly": True,
    "mined": "2026-09-25",
    "entity_count": len(entities),
    "ethic_response_categories": sorted({r for e in entities for r in e["ethics"].values()}),
    "ethic_acts": sorted({a for e in entities for a in e["ethics"]}),
    "note_tokens_absent": ["PUNISHMENT_EXCLUSIVE", "EXECUTION_STYLE"],
    "note": "Punishment is encoded solely as ETHIC response values plus executor positions (SHERIFF/CAPTAIN_OF_THE_GUARD: LAW_ENFORCEMENT; HAMMERER: EXECUTIONS + EXECUTION_SKILL:HAMMER); elites escape via [PUNISHMENT_EXEMPTION]. PLAINS humans and EVIL goblins use VARIABLE_POSITIONS/VARIABLE_VALUE instead of fixed values and offices.",
    "entities": entities,
}
OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

pos_total = sum(len(e["positions"]) for e in entities)
print(f"entities={len(entities)} ethic_lines={sum(len(e['ethics']) for e in entities)} "
      f"position_blocks={pos_total} response_categories={len(doc['ethic_response_categories'])}")
for e in entities:
    print(f"  {e['id']}: ethics={len(e['ethics'])} values={'VARIABLE' if e['values'] is None else len(e['values'])} "
          f"positions={len(e['positions'])} crimes_punished={len(e['punishments'])} enforcers={e['enforcement_positions']}")
