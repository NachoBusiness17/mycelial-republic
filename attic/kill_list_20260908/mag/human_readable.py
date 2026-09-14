"""human_readable — the plain-English layer for REAL system consequences.

The operator (2026-08-15): "we need to have the real systems consequences by default to be human
readable because most of the time its cryptic self talk."

Every real consequence surfaced to a human must have a plain-language rendering BY DEFAULT. Raw
self-talk (task ids, verkle roots, internal names) is the thing we AVOID, never the default. When we
don't have a plain reading yet, we say so plainly — we never dump a raw dict as the answer.

This is the layer the game's real-consequence wiring (raise nodes / strike the dragon / collect the
invariant / correction round) will call so its log reads like a narrator, not a debug console.

Schema: human_readable.v1 · deterministic + $0 · honest (plain by default, no cryptic fallback)
"""
from __future__ import annotations

from typing import Any

SCHEMA = "human_readable.v1"

# ── the plain-English renderers for the real system consequences ──
_HANDLERS: dict[str, Any] = {}


def _f(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _raise_nodes(p: dict[str, Any]) -> str:
    n = _f(p.get("n"))
    enq = _f(p.get("enqueued"), n)
    queued = _f(p.get("queued"))
    drained = _f(p.get("drained"))
    task = _f(p.get("task_count"))
    parts = [f"Raised {n} k3s node{'s' if n != 1 else ''} — and it was real."]
    if enq or task:
        parts.append(f"dispatched {max(enq, task)} real task{'s' if (enq or task) != 1 else ''} into the swarm queue")
    if queued:
        parts.append(f"{queued} still waiting to be drained")
    if drained:
        parts.append(f"{drained} already swept up by a worker")
    return ". ".join(parts) + "."


def _strike_dragon(p: dict[str, Any]) -> str:
    drained = _f(p.get("drained"))
    cleaned = _f(p.get("processes_cleaned"))
    target = str(p.get("target") or "the Hoarded Loop")
    dealt = _f(p.get("dealt"))
    parts = [f"The swarm struck {target}."]
    if dealt:
        parts.append(f"it dealt {dealt} damage to the loop")
    if drained:
        parts.append(f"drained {drained} real queued task{'s' if drained != 1 else ''}")
    if cleaned:
        parts.append(f"swept {cleaned} stale process{'es' if cleaned != 1 else ''}")
    if not (drained or cleaned or dealt):
        parts.append("the loop barely flinched — nothing real was touched")
    return " ".join(parts)


def _collect_invariant(p: dict[str, Any]) -> str:
    title = str(p.get("title") or "an invariant")
    folded = str(p.get("folded") or "")
    leaves = _f(p.get("n_leaves"))
    root = str(p.get("root") or "")
    parts = [f"You claimed the invariant “{title}” and it is yours now."]
    if folded:
        parts.append(f"it was folded into the real chain as {folded}")
    if leaves:
        parts.append(f"the genome now holds {leaves} leaves")
    elif root:
        parts.append(f"the chain root is now {root[:12]}…")
    return " ".join(parts)


def _node_died(p: dict[str, Any]) -> str:
    name = str(p.get("name") or "a node")
    cause = str(p.get("cause") or "the loop's counter")
    return f"{name} fell apart under {cause} — its bones scatter, but the swarm persists."


def _focus(p: dict[str, Any]) -> str:
    focus = _f(p.get("focus"))
    mx = _f(p.get("max"), 100)
    spent = _f(p.get("spent"))
    note = str(p.get("note") or "")
    s = f"Focus: {focus}/{mx}."
    if spent:
        s += f" you spent {spent} raising nodes — every raise costs now."
    if note:
        s += f" {note}"
    return s


def _correction(p: dict[str, Any]) -> str:
    target = str(p.get("target") or "a node")
    vetoed = str(p.get("vetoed") or "")
    saved = _f(p.get("saved"))
    ok = bool(p.get("good_call"))
    base = (f"You corrected {target}." if target != "a node" else "You made a correction.")
    if vetoed:
        base += f" it was about to {vetoed}"
    if ok:
        base += f" — the right call, and it saved {saved} focus."
    else:
        base += " — maybe not the right call, but the swarm heeds your hand either way."
    return base


def _fallback(kind: str, p: dict[str, Any]) -> str:
    # The honest default: we don't have a plain reading yet — NEVER dump raw self-talk as the answer.
    label = str(kind).replace("_", " ").strip() or "that"
    keys = ", ".join(sorted(str(k) for k in (p or {}).keys())) if isinstance(p, dict) else ""
    msg = f"No plain reading for {label} yet — the system did something, and it's not being shown to you as cryptic self-talk."
    if keys:
        msg += f" (it touched: {keys})"
    return msg


# register handlers
_HANDLERS = {
    "raise_nodes": _raise_nodes,
    "strike_dragon": _strike_dragon,
    "collect_invariant": _collect_invariant,
    "node_died": _node_died,
    "focus": _focus,
    "correction": _correction,
}


def _polish(text: str) -> str:
    """Plain-English prose polish: capitalize each sentence start, end with a period."""
    parts = [p.strip() for p in text.split(".") if p.strip()]
    if not parts:
        return text
    out = ". ".join(p[0].upper() + p[1:] for p in parts)
    return out if out.endswith((".", "!", "?")) else out + "."


def describe(kind: str, payload: dict[str, Any] | None = None) -> str:
    """Plain-English rendering of a real system consequence. Plain by default, never cryptic."""
    p = payload or {}
    fn = _HANDLERS.get(str(kind))
    if fn is None:
        return _polish(_fallback(kind, p))
    try:
        return _polish(fn(p))
    except Exception:
        return _polish(_fallback(kind, p))


def known_kinds() -> list[str]:
    return sorted(_HANDLERS.keys())


def status() -> dict[str, Any]:
    return {
        "ok": True, "schema": SCHEMA,
        "contract": "describe(kind, payload) -> plain English, by default; never raw self-talk as the answer",
        "known_kinds": known_kinds(),
        "cost": "deterministic + $0",
        "example": describe("collect_invariant", {"title": "The Stable Prefix", "n_leaves": 5767}),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(status(), indent=2, default=str))
