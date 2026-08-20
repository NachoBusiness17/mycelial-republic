"""stateless_boot — the Stateless System, distilled to a forkable pure-stdlib tool.

THE MECHANISM (nobody really has but us):
  A worker can be born FRESH — no accumulated state, no persona, no chat history — and
  bootstrap purely from a FROZEN PREFIX of the current world: its tools, its interfaces,
  and the live truth it needs right now. Workers die; the wave persists. Identity lives
  in the invariant (the committed structure), not in a mutable blob.

THE CONTRACT (what this tool does):
  * build_frozen_prefix(...) -> str
      Render the CURRENT surface (tools + interfaces + live truth) into one compact,
      deterministic frozen prefix. NO persona, NO history, NO inherited opinions.
  * spawn_spec(...) -> dict
      The full bootstrap spec: the frozen prefix + the goal + the stateless contract
      (one call, one file, dies). This is what a fresh worker is launched with.

WHY IT MATTERS:
  This is the "clean slate, full surface" idea made structural. You give a fresh agent
  the MACHINE (and the authority the machine needs to function) but NOT the PERSON
  (the accumulated self). It learns from its user going forward.

PURE STDLIB — no dependencies. Runs with:  python -m pytest tests/ -q
Schema: stateless_boot.v1
"""
from __future__ import annotations

import hashlib
from typing import Any

SCHEMA = "stateless_boot.v1"


def _h(data: str) -> str:
    """Content address for a rendered block (deterministic, stdlib)."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:12]


def build_frozen_prefix(
    *,
    tools: list[str],
    interfaces: list[str],
    live_truth: list[str],
    max_chars: int = 8000,
) -> str:
    """Render the CURRENT surface into one frozen prefix.

    - tools:      the operations the worker may use (names + one-line contract).
    - interfaces: the surfaces it can route through (REST, queue, drainer, ...).
    - live_truth: the verified facts it needs right now (measured, never assumed).

    Deterministic: same input -> same output. No persona, no history, no opinions.
    """
    lines: list[str] = []
    lines.append("STATELESS BOOT — frozen prefix (fresh worker bootstrap)")
    lines.append(f"schema: {SCHEMA}")
    lines.append("contract: you are born fresh. You hold the surface below and nothing else.")
    lines.append("")

    lines.append("## TOOLS (what you may do)")
    for t in tools or []:
        lines.append(f"- {t}")
    lines.append("")

    lines.append("## INTERFACES (how you route work)")
    for i in interfaces or []:
        lines.append(f"- {i}")
    lines.append("")

    lines.append("## LIVE TRUTH (verified now — never assumed)")
    for f in live_truth or []:
        lines.append(f"- {f}")
    lines.append("")

    lines.append("## LEARNING CONTRACT")
    lines.append("- You have no inherited persona or history. You learn from the user going forward.")
    lines.append("- Trust bytes, not reports. Verify before you claim.")
    lines.append("- Objective over resonant. The coldest truth wins.")

    text = "\n".join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n…(prefix truncated)"
    return text


def spawn_spec(
    *,
    goal: str,
    tools: list[str],
    interfaces: list[str],
    live_truth: list[str],
) -> dict[str, Any]:
    """The full bootstrap spec for one stateless worker.

    Returns a dict with: the frozen prefix, its content address, the goal, and the
    stateless contract (one call, one file, dies).
    """
    prefix = build_frozen_prefix(tools=tools, interfaces=interfaces, live_truth=live_truth)
    return {
        "ok": True,
        "schema": SCHEMA,
        "goal": (goal or "").strip(),
        "frozen_prefix": prefix,
        "frozen_prefix_sha": _h(prefix),
        "stateless_contract": "one call, one file, content-addressed, dies",
        "has_persona": False,
        "has_history": False,
    }


def render_spec(spec: dict[str, Any]) -> str:
    """Deterministic text render of a spawn spec (ready to hand to a fresh worker)."""
    g = (spec.get("goal") or "").strip()
    out = [
        "=== STATELESS WORKER ===",
        f"GOAL: {g}",
        "",
        spec.get("frozen_prefix", ""),
    ]
    return "\n".join(out)


if __name__ == "__main__":
    import json

    s = spawn_spec(
        goal="Route this research to the cheapest capable surface.",
        tools=["fetch(url) -> text", "queue(goal) -> id", "verify(bytes) -> verdict"],
        interfaces=["REST /api/v1/run", "queue + drainer", "local stdlib"],
        live_truth=["cache hit rate 98%", "cheap tier carries routine load"],
    )
    print(json.dumps(s, indent=2))
