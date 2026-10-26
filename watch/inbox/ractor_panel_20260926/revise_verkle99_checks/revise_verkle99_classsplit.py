"""verkle99 revision, bullet 2: measure the noise-class split on the LIVE chain.

Read-only. Answers: of the theme-null/zero-vector orchestrator noise class,
how many rows does cand one's predicate fold (knot already gone) vs keep
(knot still live / filename null), at a named moment. Also surveys row-shape
facts the consumer probe needs: does any live row carry a "type" field,
filename null, or theme_vector null.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
from mag import verkle_knot as vk  # noqa: E402

KNOTS = ROOT / "memory" / "biography" / "knots"
rows = vk._load_chain_rows()
now = datetime.now(timezone.utc).isoformat()

orc = [r for r in rows if str(r.get("session_id") or "").startswith("mag-agent-orc-")]
noise_class = [
    r for r in orc
    if r.get("dominant_theme") is None
    and not any(float(x) != 0.0 for x in (r.get("theme_vector_normalized") or []))
]
fold = [
    r for r in noise_class
    if r.get("filename") and not (KNOTS / str(r["filename"])).is_file()
]
keep_knot_live = [
    r for r in noise_class
    if r.get("filename") and (KNOTS / str(r["filename"])).is_file()
]
keep_filename_null = [r for r in noise_class if not r.get("filename")]

# cand two's duration predicate for comparison (zero duration, both minutes present)
def zero_dur(r: dict) -> bool:
    s, e = r.get("start_minute"), r.get("end_minute")
    return bool(s) and bool(e) and s == e

cand2_class = [r for r in orc if r.get("dominant_theme") is None and zero_dur(r)]

# row-shape facts
with_type = [r for r in rows if r.get("type")]
filename_null = [r for r in rows if not r.get("filename")]
tv_null = [r for r in rows if r.get("theme_vector_normalized") is None]

out = {
    "utc": now,
    "live_rows": len(rows),
    "orc_rows_total": len(orc),
    "orc_with_theme": len(orc) - len([r for r in orc if r.get("dominant_theme") is None]),
    "noise_class_prefix_theme_null_zerovector": len(noise_class),
    "split": {
        "fold_cand_one_knot_gone": len(fold),
        "keep_knot_live": len(keep_knot_live),
        "keep_filename_null": len(keep_filename_null),
        "sum": len(fold) + len(keep_knot_live) + len(keep_filename_null),
    },
    "cand_two_class_prefix_theme_null_zeroduration": len(cand2_class),
    "cand2_class_overlap_with_cand1_noise_class": len(
        [r for r in cand2_class if r in noise_class]),
    "keep_knot_live_flagged_evidence_lost": sum(
        1 for r in keep_knot_live if r.get("evidence_lost")),
    "fold_flagged_evidence_lost": sum(1 for r in fold if r.get("evidence_lost")),
    "keep_knot_live_ts_span": (
        [str(keep_knot_live[0].get("ts")), str(keep_knot_live[-1].get("ts"))]
        if keep_knot_live else None),
    "row_shape_facts": {
        "rows_with_type_field": len(with_type),
        "distinct_type_values": sorted({str(r.get("type")) for r in with_type}),
        "rows_filename_null": len(filename_null),
        "rows_filename_null_session_ids": sorted(
            {str(r.get("session_id")) for r in filename_null})[:8],
        "rows_theme_vector_null": len(tv_null),
    },
}
print(json.dumps(out, indent=2, default=str))
