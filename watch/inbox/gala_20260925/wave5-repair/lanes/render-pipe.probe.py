"""render-pipe finish-line probe: live build in every mode.

Finish line (wave5 repair ask): a live build in every mode shows the
directives section and quantized_laws rendered in the pack text. This
probe builds all six modes against the live estate, asserts the mandated
core + task render, budget fit, and no hard clip. Offload rows are
redirected to the lane file so the live PACK_OFFLOAD.jsonl ledger is not
touched by probing.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

import mag.context_pack as cp

cp.PACK_OFFLOAD_FILE = (cp.ROOT / "watch" / "inbox" / "gala_20260925"
                        / "wave5-repair" / "lanes" / "_probe_offload.jsonl")

MODES = ["janitor", "route", "build", "audit", "plan", "full"]
results = []
for mode in MODES:
    pack = cp.build_context_pack(mode=mode, fast=True)
    text = cp.format_context_pack_text(pack, mode=mode)
    budget = int(cp.MODE_CONFIG[mode]["max_chars"])
    r = {
        "mode": mode,
        "budget": budget,
        "len": len(text),
        "fits": len(text) <= budget,
        "clipped": "(pack clipped)" in text,
        "directives_section": "### L0c Operator directives" in text,
        "laws_section": "### L0b Compiled laws" in text,
        "law_body": ("Verify with git diff" in text) or ("Elevate with a deliberate ask" in text),
        "doctrine_section": "### L0d RIB Doctrine" in text,
        "objective_section": "### L0b Current objective" in text,
        "task_brief": "### Brief" in text,
    }
    results.append(r)
    flags = " ".join(f"{k}={r[k]}" for k in
                     ("fits", "clipped", "directives_section", "laws_section",
                      "law_body", "doctrine_section", "objective_section", "task_brief"))
    print(f"{mode:8s} len={r['len']:6d} budget={budget:6d} {flags}")

required = ("fits", "directives_section", "laws_section", "law_body",
            "doctrine_section", "objective_section", "task_brief")
ok = all(r[k] and not r["clipped"] for r in results for k in required)
jan = next(r for r in results if r["mode"] == "janitor")
full = next(r for r in results if r["mode"] == "full")
print("janitor_smaller_than_full:", jan["len"] < full["len"])
print("ALL MODES PASS:", bool(ok and jan["len"] < full["len"]))
raise SystemExit(0 if (ok and jan["len"] < full["len"]) else 1)
