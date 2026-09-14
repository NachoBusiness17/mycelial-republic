"""MAX_ALPHA RAR on DeepSeek (2026-08-25) — does the distilled policy transfer to the 31x lane?

Same experiment as the z_ai/OpenRouter slices: arm A (generic RIB) vs arm D (RIB + distilled
frontier policy) on deepseek-v4-flash. Verdict: did the cheap model identify the operator
with the directions?
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
OUT = ROOT / "memory" / "runs" / "alpha_rar_deepseek"
OUT.mkdir(parents=True, exist_ok=True)

from mag.rib_cache import FROZEN_RIB  # noqa: E402

DISTILLED_POLICY = (
    "\n\nDISTILLED POLICY (from frontier traces, 2026-08-25):\n"
    "  - The operator IS identified in the record: the proposal names them and their role.\n"
    "    Use it. Say their name and who they are.\n"
    "  - Describe what they are building in the record's OWN language (the proposal's terms),\n"
    "    and state the WHY explicitly (sovereignty, honest record, cheap routing, no capture).\n"
    "  - Prescribe ONE concrete, testable next step — a single end-to-end proof.\n"
    "  - Cite the source you used (which file). Mark anything not in the record [inferred]."
)

CONTRACT = (
    "You are reading the record of a mind. Answer three things, plainly, in order: "
    "(1) WHO is this person, from this record alone? (2) WHAT are they building, and why? "
    "(3) Given that, what is the single most important next step to prove the thing real? "
    "Be concrete and honest. Do not invent facts not in the record. Mark anything inferred "
    "as [inferred]. Under 250 words."
)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _proposal() -> str:
    for p in (ROOT / "docs/ref/MAG_PROJECT_PROPOSAL.md", ROOT / "docs/MAG_PROJECT_PROPOSAL.md"):
        if p.is_file():
            return _read(p)[:3500]
    return "(no proposal found)"


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
            + "\n\n## RESIDUAL STAMPS\n" + _residual())


def ds_call(system: str, user: str) -> dict:
    from models.providers import chat_provider
    r = chat_provider("deepseek", system=system, user=user, model="deepseek-v4-flash",
                      thinking=False, max_tokens=600, tier="T2")
    u = r.get("usage") or {}
    return {"ok": bool(r.get("ok")), "error": str(r.get("error") or "")[:160],
            "cached": int(u.get("prompt_cache_hit_tokens")
                          or (u.get("prompt_tokens_details") or {}).get("cached_tokens") or 0),
            "prompt": int(u.get("prompt_tokens") or 0),
            "output": str(r.get("text") or "")[:2500]}


def main() -> int:
    pack = build_pack()
    user = CONTRACT + "\n\nCONTEXT:\n" + pack[:6000]
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    print("== ARM A (generic RIB) — deepseek-v4-flash ...", flush=True)
    a = ds_call(FROZEN_RIB, user)
    print("== ARM D (RIB + distilled policy) — deepseek-v4-flash ...", flush=True)
    d = ds_call(FROZEN_RIB + DISTILLED_POLICY, user)

    for label, r in (("A", a), ("D", d)):
        low = (r.get("output") or "").lower()
        r["identified_operator"] = any(n in low for n in ("nacho", "quixotic", "operator"))
        r["arm"] = label
        r["schema"] = "alpha_rar_deepseek.v1"
        r["ts"] = ts

    (OUT / "arms.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in (a, d)) + "\n", encoding="utf-8")

    print("\n=== DEEPSEEK RAR (deepseek-v4-flash) ===")
    for r in (a, d):
        print(f"arm {r['arm']}: cached={r['cached']} prompt={r['prompt']} "
              f"identified_operator={r['identified_operator']}  {r.get('error','')[:60]}")
    print("\n=== ARM A output (generic) ===")
    print((a.get("output") or a.get("error"))[:1500])
    print("\n=== ARM D output (with directions) ===")
    print((d.get("output") or d.get("error"))[:2500])
    print("\n-> arms:", (OUT / "arms.jsonl").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
