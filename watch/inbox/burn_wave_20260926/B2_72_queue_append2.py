"""B2-72 queue self-feed, dynamically numbered (first attempt lost a race to B2-224).
Run with .venv/Scripts/python.exe."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
queue = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
text = queue.read_text(encoding="utf-8")

nums = [int(n) for n in re.findall(r"B2-(\d+)", text)]
start = max(nums) + 1
mine = [start, start + 1, start + 2]
for n in mine:
    assert ("B2-%d" % n) not in text, "B2-%d already present" % n

briefs = """- [ ] B2-{a} build_sections assignment-law spec: B2-72 proved the 0.483 adventure target is an artifact of first-match dict order (swap moves adventure -0.276 to 0.207 and hands cheapest-hill to water_computer 0.482; full reverse makes adventure DARK with grok losing all 7 paragraphs); write the assignment law (declared priority order or multi-label) into tools/curvature_scan.py docs before B2-71's bar-raise changes any bytes, so the +0.017 target cannot silently change meaning; pointers watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md + tools/curvature_scan.py:133-145.
- [ ] B2-{b} deepseek normal truncation erratum: version_deepseek.md ends mid-sentence "action: push right from (0," at byte 27594 / line 515 (blob-double Level 3 cut off, no trailing newline), so every downstream cosine reads a partial normal; file an append-only erratum in memory/runs/combined_game_triangulation/ and check manifest_deepseek.json + BUILD_RECEIPT_20260921.md for whether Level 3 completion exists in another carrier; pointers memory/runs/combined_game_triangulation/version_deepseek.md:515 + watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md side finding.
- [ ] B2-{c} contested-paragraph class audit: the 11 both-family paragraphs B2-72 censused (4 grok + 7 deepseek) are headers, connection tables and through-line prose, not region room content, so build_sections cosines measure spec-page overlap as much as builder agreement; decide whether to down-weight connector/meta paragraphs or multi-label them before any cosine is quoted as builder agreement again; pointers watch/inbox/burn_wave_20260926/B2_72_order_probe.py census output + watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md.
""".format(a=mine[0], b=mine[1], c=mine[2])

assert text.endswith("\n")
with open(queue, "a", encoding="utf-8", newline="\n") as f:
    f.write(briefs)
print("queue appended: B2-%d, B2-%d, B2-%d" % tuple(mine))

erratum = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-72-self-feed-renumber",
    "verdict": "ERRATUM",
    "landing": "watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md",
    "one_line": (
        "the B2-72 ledger row said self-feeds B2-224, B2-225, B2-226; a live "
        "queue race claimed B2-224 through B2-228 before this lane's append, so "
        "the actual self-feeds landed as B2-%d, B2-%d, B2-%d (QUEUE.md tail); "
        "first append attempt correctly refused on its own B2-224 assert, "
        "ledger row from 1st append untouched"
        % tuple(mine)
    ),
}
ledger = ROOT / "memory" / "burns" / "LEDGER.jsonl"
with open(ledger, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(erratum, ensure_ascii=False) + "\n")
print("ledger erratum appended")
