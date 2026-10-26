"""B2-72 ledger append + queue self-feed. Run with .venv/Scripts/python.exe."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECEIPT = "watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md"

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-72-curvature-order-sensitivity",
    "verdict": "LANDED",
    "landing": RECEIPT,
    "one_line": (
        "keyword-order sensitivity measured, settlement NOT order-robust: "
        "probe reproduces all 6 filed cosines bit-for-bit (adventure 0.48307382, "
        "margin 0.01692618); holding order and varying keyword sets moves "
        "adventure at most -0.003 (settlement survives, river keyword has zero "
        "marginal effect); swapping water_computer first moves adventure -0.276 "
        "to 0.207 and flips cheapest-hill to water_computer 0.482 margin 0.018; "
        "full reverse makes adventure DARK (grok loses all 7 paragraphs, "
        "cheapest becomes audit_dungeon 0.039); both regions stay SADDLE under "
        "every variant, nothing crosses 0.5; contested boundary censused at 4 "
        "grok + 7 deepseek both-family paragraphs; side finding: "
        "version_deepseek.md truncated mid-sentence at byte 27594 line 515; "
        "self-feeds B2-224, B2-225, B2-226"
    ),
}

ledger = ROOT / "memory" / "burns" / "LEDGER.jsonl"
with open(ledger, "a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("ledger rows now:", sum(1 for _ in open(ledger, encoding="utf-8")))

briefs = """- [ ] B2-224 build_sections assignment-law spec: B2-72 proved the 0.483 adventure target is an artifact of first-match dict order (swap moves adventure -0.276 and hands cheapest-hill to water_computer 0.482; full reverse makes adventure DARK); write the assignment law (declared priority order or multi-label) into tools/curvature_scan.py docs before B2-71's bar-raise changes any bytes; pointers watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md + tools/curvature_scan.py:133-145.
- [ ] B2-225 deepseek normal truncation erratum: version_deepseek.md ends mid-sentence "action: push right from (0," at byte 27594 / line 515 (blob-double Level 3 cut off, no trailing newline), so every downstream cosine reads a partial normal; file an append-only erratum in memory/runs/combined_game_triangulation/ and check manifest_deepseek.json + BUILD_RECEIPT_20260921.md for whether Level 3 completion exists in another carrier; pointers memory/runs/combined_game_triangulation/version_deepseek.md:515 + watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md side finding.
- [ ] B2-226 contested-paragraph class audit: the 11 both-family paragraphs B2-72 censused (4 grok + 7 deepseek) are headers, connection tables and through-line prose, not region room content, so build_sections cosines measure spec-page overlap as much as builder agreement; decide whether to down-weight connector/meta paragraphs or multi-label them before any cosine is quoted as builder agreement again; pointers watch/inbox/burn_wave_20260926/B2_72_order_probe.py census output + watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md.
"""
queue = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
text = queue.read_text(encoding="utf-8")
assert "B2-224" not in text, "B2-224 already present"
assert text.endswith("\n")
with open(queue, "a", encoding="utf-8", newline="\n") as f:
    f.write(briefs)
print("queue appended: B2-224, B2-225, B2-226")
