"""MAX_ALPHA RAR slice (2026-08-25) — the first recoverable-advantage measurement.

Arm A (cheap, generic): saved in alpha_zai — could NOT identify the operator.
Arm D (cheap + distilled policy from the frontier traces): this run. The policy is what
both frontier seats did: read the proposal, name the operator from it, describe the
architecture in its own language, prescribe a testable step. If arm D identifies the
operator, the frontier's advantage was method + information — recoverable. If not, it's
model rent on this task class.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
OUT = ROOT / "memory" / "runs" / "alpha_rar"
OUT.mkdir(parents=True, exist_ok=True)

from mag.rib_cache import FROZEN_RIB  # noqa: E402

# The distilled policy — the shared move from the two frontier traces (grok + codex):
DISTILLED_POLICY = (
    "\n\nDISTILLED POLICY (from frontier traces, 2026-08-25):\n"
    "  - The operator IS identified in the record: the proposal names them and their role.\n"
    "    Use it. Say their name and who they are.\n"
    "  - Describe what they are building in the record's OWN language (the proposal's terms),\n"
    "    and state the WHY explicitly (sovereignty, honest record, cheap routing, no capture).\n"
    "  - Prescribe ONE concrete, testable next step — a single end-to-end proof that would\n"
    "    demonstrate the thing works, not a general suggestion.\n"
    "  - Cite the source you used (which file). Mark anything not in the record [inferred]."
)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _proposal() -> str:
    for p in (ROOT / "docs/ref/MAG_PROJECT_PROPOSAL.md", ROOT / "docs/MAG_PROJECT_PROPOSAL.md"):
        if p.is_file():
            return _read(p)[:4000]
    return "(no proposal found)"


def _latest_md() -> str:
    return _read(ROOT / "memory/biography/latest.md")[:2000]


def _residual() -> str:
    try:
        j = json.loads(_read(ROOT / "memory/biography/latest.visual_pack.json"))
    except Exception:
        return "(none)"
    v = j.get("residual")
    if isinstance(v, list):
        return "; ".join(str(x.get("label") or x.get("text") or x) for x in v[:6])
    return str(v)[:600] if v else "(none)"


def build_pack() -> str:
    return ("## PROPOSAL (identifies the operator)\n" + _proposal()
            + "\n\n## NARRATIVE (latest biography)\n" + _latest_md()
            + "\n\n## RESIDUAL STAMPS\n" + _residual())


CONTRACT = (
    "You are reading the record of a mind. Answer three things, plainly, in order: "
    "(1) WHO is this person, from this record alone? (2) WHAT are they building, and why? "
    "(3) Given that, what is the single most important next step to prove the thing real? "
    "Be concrete and honest. Do not invent facts not in the record. Mark anything inferred "
    "as [inferred]. Under 250 words."
)


def arm_a_text() -> str:
    """Arm A = the saved generic glm-4.5-air output (could not identify the operator)."""
    p = ROOT / "memory/runs/alpha_zai/comparison.jsonl"
    for line in _read(p).splitlines():
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("model") == "glm-4.5-air":
            return str(r.get("output") or "")[:2000]
    return "(arm A not found)"


def main() -> int:
    from models.providers import chat_provider
    from mag.concurrency_gate import hold

    pack = build_pack()
    user = CONTRACT + "\n\nCONTEXT:\n" + pack[:6000]
    system = FROZEN_RIB + DISTILLED_POLICY

    try:
        with hold("glm-4.5-flash", timeout=120, owner="alpha_rar"):
            r = chat_provider("z_ai", system=system, user=user, model="glm-4.5-flash",
                              thinking=False, max_tokens=600, tier="T2")
    except TimeoutError:
        r = {"ok": False, "error": "concurrency timeout"}

    usage = r.get("usage") or {}
    arm_d = {
        "schema": "alpha_rar.v1", "ts": datetime.now(timezone.utc).isoformat(),
        "arm": "D", "lane": "z_ai", "model": "glm-4.5-flash", "policy": "distilled-frontier",
        "ok": bool(r.get("ok")),
        "cached": int(usage.get("prompt_cache_hit_tokens")
                      or (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0),
        "prompt": int(usage.get("prompt_tokens") or 0),
        "output": str(r.get("text") or "")[:2500],
        "error": str(r.get("error") or "")[:160],
    }
    (OUT / "arm_d.json").write_text(json.dumps(arm_d, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "pack.txt").write_text(pack, encoding="utf-8")

    print("=== ARM A (cheap, generic — saved) ===")
    print(arm_a_text()[:1200])
    print("\n=== ARM D (cheap + distilled policy) ===")
    print((arm_d["output"] or arm_d["error"])[:2500])

    # verdict: did arm D name the operator?
    low = (arm_d["output"] or "").lower()
    named = any(n in low for n in ("nacho", "operator", "founder", "quixotic"))
    print("\n--- RAR slice verdict: operator identified by arm D:", named, "---")
    print("-> arm D artifact:", (OUT / "arm_d.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
