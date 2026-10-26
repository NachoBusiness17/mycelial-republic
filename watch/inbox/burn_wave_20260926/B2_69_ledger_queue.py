import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")

# 1. Ledger row (append-only, json.dumps, never heredoc)
row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-69-test-census-recount",
    "verdict": "landed",
    "landing": "watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md",
    "one_line": (
        "Recount pytest --collect-only -q: 1,837 tests collected / 301 files, exit 0; "
        "1,341 headline retired as hand-copied (provenance = commit message 9669eec5b in "
        "memory/trajectory/steps.jsonl:4729, no count bytes; 09-14 trio sums 1,348); "
        "AGENTS.md:27, seed/TRUST_BYTES_LAW.md:16-20, THE50_W9_T43 receipt:37, "
        "THE50_W9_T45_EDGE_SCHEMA.md:110 updated in lockstep; both same-day full runs cited "
        "as pass counts (B2-34 executed 1,776, B2-51 executed 1,782); dungeon lore 1,341 "
        "filed owed as B2-214."
    ),
}
led = root / "memory" / "burns" / "LEDGER.jsonl"
with led.open("a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("ledger rows now:", sum(1 for _ in led.open(encoding="utf-8")))

# 2. Self-feed briefs under '## Open'
q = root / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
briefs = [
    "- [ ] B2-214 Dungeon lore census fossil: memory/game_modules/audit_dungeon.v1.json:147 "
    "still recites the retired \"1,341 tests across 264 files; 34 shelves currently fail\"; "
    "update the flavor to the 2026-09-26 census (1,837 collected / 301 files, 38 failing "
    "files) or mark the card in-world history; pointer "
    "watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md.\n",
    "- [ ] B2-215 Census freshness tripwire: the estate carried the stale 1,341 headline 12 "
    "days because no gate watches test-count carriers; add a drift-patrol or "
    "freshness_check-style rule that flags a census line older than N days while tests/ "
    "keeps growing; pointers tools/freshness_check.py, AGENTS.md:27, "
    "watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md.\n",
    "- [ ] B2-216 Collected-vs-executed delta: same-day collect-only reads 1,837 while the "
    "B2-34 and B2-51 full runs execute 1,776 and 1,782; one lane attributes the 55-61 gap "
    "(mid-wave landings vs collection-only artifacts) and pins the census denominator law "
    "next to AGENTS.md:27; pointers B2_34_cluster_detectors_20260926.md:22, "
    "B2_51_autorun_autopsy_20260926.md:22, watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md.\n",
]
text = q.read_text(encoding="utf-8")
anchor = "## Open\n"
i = text.index(anchor) + len(anchor)
text = text[:i] + "\n" + "".join(briefs) + text[i:]
q.write_text(text, encoding="utf-8", newline="\n")
print("queue briefs appended: 3")
