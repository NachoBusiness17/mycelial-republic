#!/usr/bin/env python3
"""_build_keeper_voice.py — THE KEEPER'S VOICE, file-fed.

Knock-out #10 (2026-09-07): the maze-keeper orphan (watch/maze_world/Modelfile,
qwen2.5:32b world-bible, orphaned whole per O4) is LOOTED as a FILE-FED narrator
per the orphan salon verdict (watch/SELF_STEAL_ORPHANS_20260906.md). The
resident-weights form is DISPUTED -> retired: prompts/laws are stripped to filed
artifacts, the narrator composes from data only, zero model calls.

Emits:
  state/keeper_world/world.json          — the world-bible as structured data
                                           (cast, laws, history w/ receipt paths)
  dashboard/static/keeper_voice_data.json — projection the page fetches
                                           (world + per-slab aggregates + chunks)

House laws: $0, no network, dark style bg #070d0c / cyan #7cf5ff / amber #e8c96a.
"""
import csv, json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELFILE = os.path.join(ROOT, "watch", "maze_world", "Modelfile")
MANIFEST = os.path.join(ROOT, "state", "shadow_work", "chunk_manifest.json")
SLAB_DIR = os.path.join(ROOT, "state", "shadow_work")
OUT_WORLD = os.path.join(ROOT, "state", "keeper_world", "world.json")
OUT_DATA = os.path.join(ROOT, "dashboard", "static", "keeper_voice_data.json")

MOD_SRC = "watch/maze_world/Modelfile"
MAN_SRC = "state/shadow_work/chunk_manifest.json"

def parse_modelfile():
    raw = open(MODELFILE, encoding="utf-8").read()
    m = re.search(r'SYSTEM\s+"""(.*?)"""', raw, re.S)
    sys_block = m.group(1).strip()
    base = os.path.basename(MODELFILE)
    frm = re.search(r"^FROM\s+(\S+)", raw, re.M).group(1)

    def section(name, nxt):
        pat = re.escape(name) + r"[^:]*:\s*(.*?)(?=\n\s*THE (?:WORLD|CAST|HISTORY|LAWS|ROLE)|\Z)"
        mm = re.search(pat, sys_block, re.S)
        return mm.group(1).strip() if mm else ""

    world_txt = section("THE WORLD", None)
    cast_txt = section("THE CAST", None)
    hist_txt = section("THE HISTORY", None)
    laws_txt = section("THE LAWS", None)
    role_txt = section("YOUR ROLE", None)

    cast = []
    for nm, role in re.findall(r"((?:The\s+)?[A-Z][A-Za-z]+(?:s)?)\s+\(([^)]+)\)", cast_txt):
        cast.append({"name": nm, "role": role.strip(), "src": MOD_SRC})

    laws = [{"text": ln.lstrip("- ").strip(), "src": MOD_SRC}
            for ln in laws_txt.splitlines() if ln.strip().startswith("-")]

    history = [
        {"beat": "The dream came first.", "when": "2023", "src": MOD_SRC},
        {"beat": "Then a napkin (March).", "when": "the napkin month", "src": MOD_SRC},
        {"beat": "Then five bodies of the machine: the Mirror, the Field, the Kit, the Rebuild, and the living Agent.", "when": "the five bodies", "src": MOD_SRC},
        {"beat": "Once, 49 million tokens burned in a day, and from those ashes the phoenix rose.", "when": "the burn", "src": MOD_SRC},
        {"beat": "There have been four slayings of great dragons tonight, each one a wrong belief.", "when": "the night of the build", "src": MOD_SRC},
        # the 09-06 night, filed with real receipts
        {"beat": "THE RUN: the model itself was mapped as a volumetric world — 9,305 reasoning parts carved into 50 slabs, 72 chunks vision-gated, and the keeper's own walls were walked.",
         "when": "2026-09-06", "src": "watch/SELF_STEAL_SHADOW_WORK_20260906.md"},
        {"beat": "THE AMNESIA CURE: the registry auto-heal landed — the recurring wipe-amnesia class closed at the loader; missing or shrunken registries heal from the newest seal, 18/18 falsifier checks PASS.",
         "when": "2026-09-06", "src": "watch/inbox/REGISTRY_AUTOHEAL_20260906.md"},
        {"beat": "THE ORPHAN TRIAL: the orphan salon gathered what never made it in — the keeper was found orphaned whole, verdict LOOT: rewire as a file-fed narrator; the resident-weights form stood DISPUTED and was retired.",
         "when": "2026-09-06", "src": "watch/SELF_STEAL_ORPHANS_20260906.md"},
    ]
    return {
        "schema": "keeper_world/v1",
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "provenance": {
            "modelfile": MOD_SRC,
            "base_model": frm,
            "orphan_entry": "watch/SELF_STEAL_ORPHANS_20260906.md",
            "lineage_finding": "research/orphan_registry/maze_lineage.md",
            "salon_verdict": "LOOT as file-fed narrator candidate; resident-weights form DISPUTED — strip prompts/laws to filed artifacts",
            "form": "file-fed (deterministic templates over this file; no model calls)",
        },
        "world": {"name": "The Room That Remembers", "description": world_txt, "src": MOD_SRC},
        "cast": cast,
        "laws": laws,
        "history": history,
        "keeper_role": {"text": role_txt, "src": MOD_SRC},
    }

def slab_aggregates():
    """sum chars/words/law_hits/questions per slab CSV -> {slab_id: agg}"""
    aggs = {}
    for fn in os.listdir(SLAB_DIR):
        m = re.fullmatch(r"slab_(\d+)\.csv", fn)
        if not m:
            continue
        sid = int(m.group(1))
        chars = words = law = q = rows = 0
        with open(os.path.join(SLAB_DIR, fn), newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows += 1
                chars += int(r["chars"]); words += int(r["words"])
                law += int(r["law_hits"]); q += int(r["questions"])
        aggs[sid] = {"slab": sid, "rows": rows, "chars": chars, "words": words,
                     "law_hits": law, "questions": q, "src": f"state/shadow_work/slab_{sid}.csv"}
    return aggs

def main():
    world = parse_modelfile()
    os.makedirs(os.path.dirname(OUT_WORLD), exist_ok=True)
    with open(OUT_WORLD, "w", encoding="utf-8") as f:
        json.dump(world, f, indent=2)

    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    aggs = slab_aggregates()
    chunks = []
    for c in manifest["chunks"]:
        entry = {"id": c["id"], "origin": c["origin"], "biome": c["biome"],
                 "slab_id": c["slab_id"], "content_hash": c.get("content_hash"),
                 "vision_validated": c.get("vision_validated", False),
                 "stats": c["stats"], "src": MAN_SRC}
        if isinstance(c["slab_id"], int) and c["slab_id"] in aggs:
            entry["slab_agg"] = aggs[c["slab_id"]]
        chunks.append(entry)

    data = {
        "schema": "keeper_voice_data/v1",
        "generated": world["generated"],
        "builder": "dashboard/static/_build_keeper_voice.py",
        "world": world,
        "manifest_meta": {k: manifest[k] for k in
                          ("schema", "data_hash", "points", "grid", "chunk", "vision_contract")},
        "chunks": chunks,
    }
    with open(OUT_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f)

    print(f"world.json: {len(world['cast'])} cast, {len(world['laws'])} laws, {len(world['history'])} history beats")
    print(f"data: {len(chunks)} chunks ({len(aggs)} slab aggregates), {os.path.getsize(OUT_DATA)} bytes")

if __name__ == "__main__":
    main()
