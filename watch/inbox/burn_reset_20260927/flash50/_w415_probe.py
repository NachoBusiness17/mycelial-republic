'''w4-15 probe: live terminal-stage funnel measurements, offload redirected.'''
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
import mag.context_pack as cp  # noqa: E402

REDIRECT = Path(__file__).resolve().parent / "_w415_offload.jsonl"
cp.PACK_OFFLOAD_FILE = REDIRECT
if REDIRECT.exists():
    REDIRECT.unlink()

out = {}
for mode in ("full", "janitor", "route"):
    pack = cp.build_context_pack(mode=mode, fast=True)
    text = cp.format_context_pack_text(pack, mode=mode, max_chars=cp.MODE_CONFIG[mode]["max_chars"])
    rows = [json.loads(x) for x in REDIRECT.read_text(encoding="utf-8").splitlines() if x.strip()]
    mine = [r for r in rows if r.get("mode") == mode]
    out[mode] = {
        "budget": cp.MODE_CONFIG[mode]["max_chars"],
        "rendered_chars": len(text),
        "overflow_events": len(mine),
        "assembled_T0": mine[0]["total_chars"] if mine else None,
        "stages_fired": [r["stage"] for r in mine],
        "has_laws": "Compiled laws" in text,
        "has_objective": "Current objective" in text,
        "has_doctrine": "RIB Doctrine" in text,
        "has_task": "L3 Task" in text,
        "has_directives": "Directive" in text,
    }

# doctrine excerpt as built upstream (pre-ladder)
doc = cp._rib_doctrine()
out["rib_doctrine_excerpt_chars"] = len(doc)
out["rib_doctrine_entries"] = doc.count("\n- ") + (1 if doc.startswith("- ") else 0)
out["rib_doctrine_over_cap"] = len(doc) > 2800

# quantized laws excerpt as rendered upstream
ql = cp._quantized_laws()
out["quantized_laws_excerpt_chars"] = len(ql)
out["quantized_laws_rows"] = ql.count("\n- ") + (1 if ql.startswith("- ") else 0)

print(json.dumps(out, indent=1))
