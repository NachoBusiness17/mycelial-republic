import json
from pathlib import Path

row = {
    "ts": "2026-09-26T14:05:00Z",
    "slug": "B2-198-owed-b2-41-receipt",
    "verdict": "DISCHARGED",
    "landing": "watch/inbox/burn_wave_20260926/B2_198_owed_receipt_20260926.md",
    "one_line": (
        "owed B2-41 receipt discharged: the receipt the brief called missing exists "
        "(watch/inbox/burn_wave_20260926/B2_41_hash_freshness_20260926.md, 4342 bytes), disk sha256 "
        "4280FA418FEDE65EF2DFEF0A7984733A148ECD1CF27AC5CBDA49FED2CAAC0A32 equals the registration at "
        "index_events.jsonl:3089 seq 1789823567015749402 (13:29:52.864Z), so the 13:21:20Z LINKS purpose line "
        "(seq ...401) was a forward pointer that resolved 8m32s later, not fabricated-by-pointer; the false "
        "'does not exist on disk' premise lives on in LIVING_HASH_LAW_20260926.md:20-21 (sealed sha 9B931917, "
        "seq ...408) and in this LEDGER's B2-156 row written 11m23s after the receipt registered; LINKS.jsonl "
        "now carries the B2-156 living prefix seal (size 219904, sha 9DC30BDD byte-verified, 568 growth bytes) "
        "and validate shows no error on any file named here; self-feeds B2-202 (law doc erratum addendum) and "
        "B2-203 (LEDGER one_line existence re-check convention) appended"
    ),
}

p = Path("memory/burns/LEDGER.jsonl")
with p.open("a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("appended row, slug:", row["slug"])
