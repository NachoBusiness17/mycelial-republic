"""mem_state_feed — feed OUR REAL MEMORY STATE into the desktop app's input via memlance (operator,
2026-08-13: "how could we use mem lance to speed this conversation" -> "contacting the desktop mem
state input instead of using the app surface"). 

THE MECHANISM: instead of steering the ChatGPT/Grok desktop app with a throwaway prompt, we:
  1. SELECT the relevant grounded memory slice with memlance (ghost_memlance.select) — only real
     bytes read from disk, each with provenance (path) + a deterministic verified verdict.
  2. FORMAT that slice into a compact, provenanced context (titles + verified excerpts + paths).
  3. FEED it into the desktop app's input via the verified chatgpt_desktop / grok_desktop steer.

That "speeds the conversation": the frontier gets the DISTILLED, relevant, grounded state (the mem
language — sw59-62) instead of raw dumps or a generic prompt. Memlance is the moka pot applied to
conversation memory: many states -> the relevant one, grounded + provenanced.

THE LAW (honest, anti-hallucination): only verified grounded excerpts are carried forward as truth;
unverified-matching states are flagged, never presented as fact. What we feed the frontier is
REAL bytes, never synthesized.

Schema: mem_state_feed.v1 · deterministic $0 · reuse: ghost_memlance.select, chatgpt_desktop,
grok_desktop
"""
from __future__ import annotations

import sys
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "mem_state_feed.v1"


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def select(goal: str, *, k: int = 8) -> dict[str, Any]:
    """memlance.select — the RELEVANT, GROUNDED memory states for the goal. Real bytes from disk,
    each with provenance + a deterministic verified verdict. Never synthesizes content."""
    try:
        from mag import ghost_memlance
        return ghost_memlance.select(goal, k=k)
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "goal": goal, "error": str(e)[:160],
                "selected": []}


def _format(sel: dict[str, Any]) -> str:
    """Format the memlance selection into a compact, provenanced context prompt — the grounded mem
    language fed to the frontier. Verified excerpts first; unverified clearly flagged (never as
    truth)."""
    lines = ["GROUNDED MEMORY STATE (selected by memlance; real bytes with provenance):"]
    sel_items = sel.get("selected") or []
    if not sel_items:
        return "GROUNDED MEMORY STATE: (no matching grounded states selected)"
    for s in sel_items:
        tag = "VERIFIED" if s.get("verified") else f"UNVERIFIED[{s.get('reason', '?')}]"
        title = s.get("title") or s.get("path") or "?"
        excerpt = (s.get("excerpt") or "").strip()
        lines.append(f"- [{tag}] {title}")
        if excerpt:
            lines.append(f"    {excerpt[:240]}")
    return "\n".join(lines)


def feed(goal: str, *, seat: str = "chatgpt-desktop", k: int = 8,
         max_wait_s: int = 45) -> dict[str, Any]:
    """FEED the mem state into the desktop app's input: memlance select -> format -> desktop steer.
    The frontier sees our real, grounded state, not a generic prompt."""
    sel = select(goal, k=k)
    if not sel.get("ok"):
        return {"ok": False, "schema": SCHEMA, "seat": seat, "goal": goal,
                "error": sel.get("error", "memlance select failed")[:160]}
    prompt = _format(sel)
    # ROUTE BY SURFACE (operator 2026-08-13: "render the page as me, see everything"): prefer the
    # CONTAINER browser over CDP (:9222) — it renders the logged-in page and reads the REAL DOM,
    # touching ZERO of the operator's local windows. The desktop seats (set_focus + type) are what
    # kept "typing in my windows" and their Electron CDP ports are typically closed — so they're the
    # LAST resort, never the default.
    browser_surface = {"grok-desktop": "grok", "chatgpt-desktop": "chatgpt"}.get(seat)
    if browser_surface:
        try:
            from mag import cdp_runner
            r = cdp_runner.ask_browser(browser_surface, goal + "\n\n" + prompt,
                                       timeout_s=max(90, max_wait_s + 20))
            return {"ok": bool(r.get("ok")), "schema": SCHEMA, "seat": seat, "goal": goal,
                    "surface": browser_surface,
                    "n_mem_states": sel.get("n_selected", 0),
                    "reply": (r.get("answer") or "")[:2000],
                    "error": (r.get("error") or "")[:160],
                    "note": "fed the grounded mem state into the container browser over CDP "
                            "(renders the page as the operator, reads the DOM — no local window)"}
        except Exception as e:
            return {"ok": False, "schema": SCHEMA, "seat": seat, "goal": goal,
                    "surface": browser_surface,
                    "error": f"container-browser route failed: {str(e)[:160]}"}
    # LAST RESORT: only if no browser surface maps (or the operator explicitly asked for desktop).
    try:
        from mag import grok_desktop, chatgpt_desktop
        mod = grok_desktop if seat == "grok-desktop" else chatgpt_desktop
        r = mod.steer(goal + "\n\n" + prompt, max_wait_s=max_wait_s)
        return {"ok": bool(r.get("ok")), "schema": SCHEMA, "seat": seat, "goal": goal,
                "n_mem_states": sel.get("n_selected", 0),
                "reply": (r.get("reply") or "")[:2000],
                "error": (r.get("error") or "")[:160],
                "note": "fed the grounded mem state into the desktop input (fallback)"}
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "seat": seat, "goal": goal,
                "error": str(e)[:160]}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "select(goal,k)->memlance's relevant grounded memory states (real bytes + "
                        "provenance + verified verdict); _format(sel)->compact provenanced context; "
                        "feed(goal,seat)->memlance select -> format -> drive into the ChatGPT/Grok "
                        "desktop input (the mem state input).",
            "cost": "deterministic $0 (memlance + the desktop apps, front-end only)",
            "surface": "the desktop MEM STATE INPUT — memlance selects our state, the desktop app "
                       "receives it",
            "reuse": "ghost_memlance.select, chatgpt_desktop, grok_desktop"}


def main(argv: list[str] | None = None) -> int:
    import argparse, json
    ap = argparse.ArgumentParser(prog="mem-state-feed")
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "select", "feed"])
    ap.add_argument("goal", nargs="*", default=[])
    ap.add_argument("--seat", default="chatgpt-desktop")
    ap.add_argument("--k", type=int, default=6)
    a = ap.parse_args(argv)
    goal = " ".join(a.goal) or "the game and the standing wave"
    if a.cmd == "select":
        print(json.dumps(select(goal, k=a.k), indent=2, default=str))
    elif a.cmd == "feed":
        print(json.dumps(feed(goal, seat=a.seat, k=a.k), indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
