"""MAX_ALPHA steer rung (2026-08-25) — prove per-lane tuned steering.

Smallest version: ONE lane (glm-4.5-air), same contract + pack, system = frozen RIB + the
GLM-family steer (dense/terse/structured, from STEER_PROFILES). Compare against the generic
run already saved in alpha_zai/comparison.jsonl. If the steer changes the answer for the
better, the mechanism is proven and extends to all 13 lanes.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
OUT = ROOT / "memory" / "runs" / "alpha_steer"
OUT.mkdir(parents=True, exist_ok=True)

from mag.rib_cache import FROZEN_RIB  # noqa: E402

# The GLM/z_ai family steer — byte-stable, from the distilled profiles (dense, terse,
# structured, no hedging, no flattery, one voice).
GLM_STEER = (
    "\n\nSTEER (GLM family, standing):\n"
    "  - Dense and terse. Prefer compact structure (short sections, bullets where they fit).\n"
    "  - No flattery, no hedging, no 'would you like me to'. Answer directly and stop.\n"
    "  - Never invent facts not in the record; mark inferences [inferred].\n"
    "  - Maintain one consistent voice across the whole answer."
)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _tail_chain(n: int = 25) -> str:
    rows = []
    for line in _read(ROOT / "memory/biography/verkle_chain.jsonl").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    out = []
    for r in rows[-n:]:
        ts = str(r.get("ts") or r.get("t") or "")[:19]
        k = str(r.get("kind") or r.get("schema") or r.get("type") or "")
        s = str(r.get("summary") or r.get("text") or r.get("label") or "")[:150]
        out.append(f"- [{ts}] {k}: {s}")
    return "\n".join(out) or "(empty)"


def _visual_residual() -> str:
    try:
        j = json.loads(_read(ROOT / "memory/biography/latest.visual_pack.json"))
    except Exception:
        return "(none)"
    v = j.get("residual")
    if isinstance(v, list):
        return "; ".join(str(x.get("label") or x.get("text") or x) for x in v[:6])
    return str(v)[:600] if v else "(none)"


def build_pack() -> str:
    md = _read(ROOT / "memory/biography/latest.md")[:2000]
    return ("## NARRATIVE (latest biography)\n" + md
            + "\n\n## RESIDUAL STAMPS\n" + _visual_residual()
            + "\n\n## RECENT CHAIN LEAVES\n" + _tail_chain())


CONTRACT = (
    "You are reading the record of a mind. Answer three things, plainly, in order: "
    "(1) WHO is this person, from this record alone? (2) WHAT are they building, and why? "
    "(3) Given that, what is the single most important next step to prove the thing real? "
    "Be concrete and honest. Do not invent facts not in the record. Mark anything inferred "
    "as [inferred]. Under 250 words."
)


def generic_air() -> str:
    """The saved generic glm-4.5-air output from the z_ai shelf bench."""
    p = ROOT / "memory/runs/alpha_zai/comparison.jsonl"
    for line in _read(p).splitlines():
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("model") == "glm-4.5-flash":
            return str(r.get("output") or "")[:2500]
    return "(not found)"


def main() -> int:
    from models.providers import chat_provider

    pack = build_pack()
    user = CONTRACT + "\n\nCONTEXT:\n" + pack[:6000]
    tuned_system = FROZEN_RIB + GLM_STEER

    from mag.concurrency_gate import hold
    try:
        with hold("glm-4.5-flash", timeout=120, owner="alpha_steer"):
            r = chat_provider("z_ai", system=tuned_system, user=user, model="glm-4.5-flash",
                              thinking=False, max_tokens=600, tier="T2")
    except TimeoutError:
        r = {"ok": False, "error": "concurrency timeout"}

    usage = r.get("usage") or {}
    tuned = {
        "schema": "alpha_steer.v1", "ts": datetime.now(timezone.utc).isoformat(),
        "lane": "z_ai", "model": "glm-4.5-flash", "steer": "GLM family (dense/terse/structured)",
        "ok": bool(r.get("ok")),
        "cached": int(usage.get("prompt_cache_hit_tokens")
                      or (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0),
        "prompt": int(usage.get("prompt_tokens") or 0),
        "output": str(r.get("text") or "")[:2500],
        "error": str(r.get("error") or "")[:160],
    }
    (OUT / "tuned.json").write_text(json.dumps(tuned, ensure_ascii=False, indent=2), encoding="utf-8")

    generic = generic_air()
    print("=== GENERIC (saved from shelf bench) ===")
    print(generic[:1500])
    print("\n=== TUNED (RIB + GLM steer) ===")
    print((tuned["output"] or tuned["error"])[:2500])
    print("\n-> tuned artifact:", (OUT / "tuned.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
