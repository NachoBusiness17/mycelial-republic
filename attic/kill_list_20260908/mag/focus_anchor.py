"""focus_anchor — the tangent-catcher turned BRAID-KEEPER: hold the thread, weave tangents in.

Operator (2026-08-16): "thats what i do it needs to be built in... we keep making the knots
ourselves. with no way to weave all these tangents into a braid we have a tangled mess."

The thing he does by hand — stopping himself, calling back to the task, NOT rebuilding the
mental map — should be BUILT IN and automatic. Catching ONE tangent is not enough: a single
anchor + a pile of logged tangents is still a tangle. The braid is the ordered thread where
every bead (task step or tangent) is WOVEN in order, and recovery returns the WHOLE braid so
nothing is lost when the thread is dropped.

Self-steal (nothing invented):
  * anchor store  -> memory/attention.md (the shared focus file)
  * tangent detect-> fork_router markers (detects planning tangents)
  * tangent log   -> mag.tangent (scouts to memory/tangents/)
  * braid journal -> memory/thread.json (NEW: the ordered thread this module weaves)
  * re-anchor     -> compass "re-anchor to the last successful bead"

Loop: anchor(task) -> weave(turn) [appends bead in order, logs tangents] -> recover() [untie].

Schema: focus_anchor.v1 · deterministic $0 · reuse: fork_router, tangent, memory/attention.md
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import ROOT

ATTENTION = ROOT / "memory" / "attention.md"
LOCUS = ROOT / "memory" / "locus.md"
THREAD_PATH = ROOT / "memory" / "thread.json"
SCHEMA = "focus_anchor.v1"

# Reuse fork_router's tangent/future markers (self-steal, don't reinvent).
_TANGENT_MARKERS = (
    "also", "as well", "another", "in addition", "feature set", "roadmap", "branch",
    "fork", "gap analysis", "not ready for production", "wouldn't it be nice",
    "would it be nice", "it might be neat", "what if", "someday", "future",
    "for later", "down the line", "in the long run", "vision", "imagine",
)
_ANCHOR_VERBS = ("task", "aim", "goal", "focus", "the task", "we were", "on track", "anchor")

# Function words pollute topic-overlap; strip them so drift = real content, not "the/and".
_STOP = {
    "the", "and", "for", "then", "but", "not", "are", "was", "were", "will",
    "would", "could", "should", "this", "that", "these", "those", "with",
    "from", "have", "has", "had", "our", "your", "their", "its", "all",
    "any", "can", "you", "they", "them", "she", "his", "her", "him", "too",
    "also", "just", "like", "what", "when", "where", "which", "into", "out",
    "one", "get", "got", "make", "much", "more", "most", "very", "really",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{3,}", (text or "").lower())) - _STOP


def read_anchor() -> str:
    """The current focus (the known route / locus). What we are supposed to be doing."""
    for p in (ATTENTION, LOCUS):
        try:
            if p.is_file():
                t = p.read_text(encoding="utf-8", errors="replace").strip()
                if t:
                    return t[:2000]
        except OSError:
            pass
    return ""


def anchor(task: str, aim: str = "") -> dict[str, Any]:
    """SET the current focus. Write it to memory/attention.md (the shared focus store)."""
    try:
        ATTENTION.parent.mkdir(parents=True, exist_ok=True)
        body = str(task or "").strip()[:2000]
        if aim:
            body = f"{body}\n\nAIM: {str(aim).strip()[:500]}"
        ATTENTION.write_text(body + "\n", encoding="utf-8")
        return {"ok": True, "schema": SCHEMA, "anchor": body[:200], "ts": _now()}
    except OSError as e:
        return {"ok": False, "error": str(e)[:200]}


def detect(text: str, anchor_text: str = "") -> dict[str, Any]:
    """Is this turn ON-task, or a TANGENT? Drift = tangent/future markers present AND low
    overlap with the anchor's own words."""
    text = text or ""
    low = text.lower()
    hit = next((m for m in _TANGENT_MARKERS if m in low), None)
    if not hit:
        return {"ok": True, "schema": SCHEMA, "on_task": True, "reason": "no tangent marker"}
    # if it's explicitly re-anchoring ("back to the task", "where were we"), that's ON-task
    if any(v in low for v in _ANCHOR_VERBS):
        return {"ok": True, "schema": SCHEMA, "on_task": True, "reason": "re-anchor verb", "marker": hit}
    # overlap with the anchor's tokens — if we still share ground with the task, it's a fork, not a loss
    if anchor_text:
        ov = _tokens(text) & _tokens(anchor_text)
        if len(ov) >= 2:
            return {"ok": True, "schema": SCHEMA, "on_task": True, "reason": "overlaps anchor", "marker": hit}
    return {"ok": False, "schema": SCHEMA, "on_task": False, "reason": "tangent marker", "marker": hit}


def log_tangent(text: str, reason: str = "") -> dict[str, Any]:
    """Log the tangent so it is NOT lost — it is a foundation, not a failure (operator:
    dead ends are castle foundations we keep forgetting). Reuse mag.tangent if available."""
    try:
        from mag import tangent
        rec = tangent.record(str(text)[:2000], source="focus_anchor", reason=reason) if hasattr(tangent, "record") else None
        if rec and rec.get("ok"):
            return {"ok": True, "logged": True, "id": rec.get("id"), "reason": reason}
    except Exception:
        pass
    # fallback: append to the tangent queue directly
    try:
        from mag.tangent import QUEUE_PATH, _ensure, _tid, _utc
        _ensure()
        with open(QUEUE_PATH, "a", encoding="utf-8") as f:
            f.write(__import__("json").dumps({"id": _tid(text), "text": str(text)[:2000],
                                              "reason": reason, "ts": _utc()}) + "\n")
        return {"ok": True, "logged": True, "id": _tid(text), "reason": reason}
    except Exception as e:
        return {"ok": False, "logged": False, "error": str(e)[:200]}


def return_to_task(text: str = "", anchor_text: str = "") -> dict[str, Any]:
    """The auto-return: catch the tangent, log it (so it is kept, not lost), and hand the
    operator the anchor back so they do NOT have to rebuild the mental map."""
    anchor_text = anchor_text or read_anchor()
    d = detect(text, anchor_text)
    if d.get("on_task"):
        return {"ok": True, "schema": SCHEMA, "on_task": True,
                "anchor": (anchor_text or "")[:160], "note": "on task"}
    logged = log_tangent(text, reason=d.get("reason", ""))
    return {
        "ok": True,
        "schema": SCHEMA,
        "on_task": False,
        "tangent_logged": logged.get("logged"),
        "reason": d.get("reason"),
        "anchor": (anchor_text or "")[:600],
        "guidance": ("Here is the task. The tangent is logged for later — it is a foundation, "
                     "not a loss. Come back to the task; you do not have to rebuild the map."),
    }


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "anchor": read_anchor()[:160],
            "braid_len": len(_load_thread()),
            "contract": "anchor(task)->set focus; weave(turn)->append bead in order + log tangents; "
                        "recover()->untie the WHOLE braid; thread()->view the braid. "
                        "Wire into cadence so drift is caught WITHOUT the operator calling back.",
            "cost": "deterministic $0"}


# ====================================================================
# THE BRAID — ordered thread journal (weave, don't tangle)
# ====================================================================

def _load_thread() -> list[dict[str, Any]]:
    try:
        if THREAD_PATH.is_file():
            t = json.loads(THREAD_PATH.read_text(encoding="utf-8", errors="replace"))
            return t if isinstance(t, list) else []
    except (OSError, json.JSONDecodeError):
        pass
    return []


def _save_thread(t: list[dict[str, Any]]) -> None:
    try:
        THREAD_PATH.parent.mkdir(parents=True, exist_ok=True)
        THREAD_PATH.write_text(json.dumps(t, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def weave(text: str = "", task: str = "", *, auto_anchor: bool = True) -> dict[str, Any]:
    """THE BRAID OPERATION. Decide this turn (task step or tangent), append it IN ORDER to the
    thread journal, and log any tangent (woven, not lost). If the thread is empty, seed it with
    the task anchor as the root bead so the braid always has its origin."""
    task = task or read_anchor()
    if auto_anchor and task and not _load_thread():
        anchor(task)
    d = detect(text, task)
    t = _load_thread()
    if not t and task:
        t.append({"type": "anchor", "text": task[:500], "ts": _now()})
    bead: dict[str, Any] = {
        "type": "task" if d.get("on_task") else "tangent",
        "text": (text or "").strip()[:500],
        "ts": _now(),
    }
    if not d.get("on_task"):
        # STEAL (LangGraph resumable-thread / Zettelkasten bidirectional link, 2026-08-16): a tangent
        # must carry a PARENT pointer back to the main-thread bead it branched from, so the return
        # path is STRUCTURAL (never lost), not remembered. "Weave tangents rather than being led
        # deeper into the woods and losing our way to them."
        parent = next((i for i in range(len(t) - 1, -1, -1)
                       if t[i].get("type") in ("anchor", "task")), None)
        if parent is not None:
            bead["parent"] = parent  # index of the main-thread bead this tangent branches from
        bead["reason"] = d.get("reason")
        bead["marker"] = d.get("marker")
    t.append(bead)
    # cap the journal so it never grows unbounded (keep the last 200 beads)
    _save_thread(t[-200:])
    if not d.get("on_task"):
        logged = log_tangent(text, reason=d.get("reason", ""))
        return {"ok": True, "schema": SCHEMA, "on_task": False,
                "braid_len": len(_load_thread()), "logged": logged.get("logged"),
                "reason": d.get("reason"),
                "anchor": task[:600],
                "guidance": ("Tangent woven into the braid — logged and kept in order, not lost. "
                             "Here is the task; you do not have to rebuild the map.")}
    return {"ok": True, "schema": SCHEMA, "on_task": True, "braid_len": len(_load_thread()),
            "anchor": task[:600], "note": "on task — woven as the next bead"}


def thread(limit: int = 40) -> dict[str, Any]:
    """View the whole braid in order — task anchor first, then every woven bead."""
    t = _load_thread()
    return {"ok": True, "schema": SCHEMA, "braid_len": len(t),
            "beads": t[-limit:], "anchor": read_anchor()[:600]}


def recover(task: str = "") -> dict[str, Any]:
    """UNTIE THE KNOT. Restore the anchor and return the full ordered braid, so when the thread
    is dropped we get it ALL back — the task and every tangent in order, nothing lost."""
    task = task or read_anchor()
    t = _load_thread()
    return {"ok": True, "schema": SCHEMA, "anchor": task[:600],
            "braid": t[-120:],
            "braid_len": len(t),
            "guidance": ("Here is the whole thread — the task and every tangent, in order. "
                         "This is the braid: pick up where the last task bead left off; the "
                         "tangents are woven, not lost.")}


def main(argv: list[str] | None = None) -> int:
    import argparse, json
    ap = argparse.ArgumentParser(prog="focus_anchor")
    ap.add_argument("cmd", choices=["status", "anchor", "detect", "return", "weave", "thread", "recover"])
    ap.add_argument("text", nargs="*")
    a = ap.parse_args(argv)
    if a.cmd == "status":
        print(json.dumps(status(), indent=2, default=str))
    elif a.cmd == "anchor":
        print(json.dumps(anchor(" ".join(a.text)), indent=2, default=str))
    elif a.cmd == "detect":
        print(json.dumps(detect(" ".join(a.text), read_anchor()), indent=2, default=str))
    elif a.cmd == "return":
        print(json.dumps(return_to_task(" ".join(a.text), read_anchor()), indent=2, default=str))
    elif a.cmd == "weave":
        print(json.dumps(weave(" ".join(a.text), read_anchor()), indent=2, default=str))
    elif a.cmd == "thread":
        print(json.dumps(thread(), indent=2, default=str))
    elif a.cmd == "recover":
        print(json.dumps(recover(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
