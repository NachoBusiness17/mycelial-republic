"""arch-01 probe 2: render-logic proofs with a hand-built pack.

Redirects PACK_OFFLOAD_FILE to a probe-local jsonl so live ledger is untouched.
No subprocess. ASCII only.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
if not (ROOT / "mag" / "context_pack.py").is_file():
    ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

import mag.context_pack as cp

cp.PACK_OFFLOAD_FILE = HERE / "_arch01_offload_probe.jsonl"

out = {}

# 1. Quoted-key scan, BOTH quote styles, render region (lines 993..end).
src = (ROOT / "mag" / "context_pack.py").read_text(encoding="utf-8")
lines = src.splitlines()
render_region = "\n".join(lines[992:])
keys = ["compass_framework", "checkpoint_restore", "commands", "layers",
        "token_note", "resonance_cards", "models", "bonds_meta", "health",
        "quantized_laws", "doctrine", "directives"]
out["render_key_hits"] = {
    k: {"dq": len(re.findall('"' + re.escape(k) + '"', render_region)),
        "sq": len(re.findall("'" + re.escape(k) + "'", render_region))}
    for k in keys}

# 2. Hand-built pack: which sections render unclipped, what stage 3 sheds.
BIG = "X" * 3000


def make_pack() -> dict:
    return {
        "schema": "probe", "mode": "build", "job": "build", "pack_max_chars": 5500,
        "ts": "probe", "for": "probe", "token_note": "TN", "operator_path": "op",
        "layers": [], "nervous_system": {}, "tip": {"ok": False, "error": "probe"},
        "agent_state": "AS", "agent_state_meta": {}, "continuity": "CONT_BODY",
        "health": {"status": "probe"}, "models": {"worker": "probe"},
        "brief": "BRIEF_BODY", "bonds": "BONDS_BODY", "bonds_meta": {"n": 0},
        "open_loops": ["l1"], "run_trail": {"text": "TRAIL_BODY"},
        "skills_excerpt": "SKILL_BODY", "proven_moves": "PM_BODY",
        "quantized_laws": "[compile v0.3 probe]\n- LAW_BODY", "solved_excerpt": "SOLVED_BODY",
        "ijl_skills": "IJL_BODY", "mirror_voice_excerpt": "", "clue_chain_excerpt": "",
        "build_excerpt": "BUILD_BODY", "scope_excerpt": "",
        "behavioral_excerpt": "BEH_BODY", "compass_framework": "COMPASS_BODY",
        "checkpoint_restore": "CKPT_BODY", "coordination_excerpt": "COORD_BODY",
        "zeitgeist_excerpt": "ZEIT_BODY", "resonance_cards": [], "resonance_l0e": "",
        "dirac_loops": {"closed": 0, "total": 0}, "live_tail": "LIVE_BODY",
        "attention_tail": "ATT_BODY", "directives": "DIRECTIVE_BODY " + "y" * 500,
        "doctrine": "### L0d RIB Doctrine header\n" + BIG,
        "subchain_full": "", "world_state": "", "full_context": False,
        "todo_open": ["t1"],
        "commands": {"load": "probe"},
    }


# 2a. Unclipped render (huge budget): what the full layout contains.
p = make_pack()
unclipped = cp.format_context_pack_text(p, mode="build", max_chars=200000)
out["unclipped"] = {
    "chars": len(unclipped),
    "has": {m: (m in unclipped) for m in
            ["RIB Doctrine", "DIRECTIVE_BODY", "BONDS_BODY", "BUILD_BODY",
             "BRIEF_BODY", "LAW_BODY", "CONT_BODY", "BEH_BODY", "COORD_BODY",
             "ZEIT_BODY", "PM_BODY", "SOLVED_BODY", "SKILL_BODY", "TRAIL_BODY",
             "LIVE_BODY", "ATT_BODY"]},
    "never_even_unclipped": {m: (m in unclipped) for m in
                             ["COMPASS_BODY", "CKPT_BODY"]},
}

# 2b. Same pack, build budget 5000: stage 3 fires, ctx tier gone.
p2 = make_pack()
clipped = cp.format_context_pack_text(p2, mode="build", max_chars=5000)
rows = []
pf = HERE / "_arch01_offload_probe.jsonl"
if pf.is_file():
    rows = [json.loads(l)["stage"] for l in pf.read_text(encoding="utf-8").splitlines() if l.strip()]
out["stage3_clipped"] = {
    "chars": len(clipped),
    "stages_fired": rows,
    "shed": {m: (m in clipped) for m in
             ["RIB Doctrine", "DIRECTIVE_BODY", "CONT_BODY", "BEH_BODY",
              "COORD_BODY", "ZEIT_BODY", "PM_BODY", "SOLVED_BODY"]},
    "kept": {m: (m in clipped) for m in
             ["LAW_BODY", "BONDS_BODY", "BUILD_BODY", "BRIEF_BODY"]},
}

# 2c. Janitor: budget 1200 with a 2198-char objective -> prove laws+task die.
p3 = make_pack()
p3["mode"] = "janitor"
jan = cp.format_context_pack_text(p3, mode="janitor")
out["janitor_1200"] = {
    "chars": len(jan),
    "has_law": "LAW_BODY" in jan,
    "has_brief": "BRIEF_BODY" in jan,
    "has_bonds": "BONDS_BODY" in jan,
    "tail": jan[-100:],
}

# 2d. models/bonds_meta/health DO render (single-quote p.get) as raw dict reprs.
out["dict_repr_lines"] = [
    ln for ln in unclipped.splitlines() if ln.startswith("- models:") or ln.startswith("- bonds_meta:") or ln.startswith("- health:")
]

dump = HERE / "_arch01_out2.json"
dump.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
print(f"out dumped: {dump}")
