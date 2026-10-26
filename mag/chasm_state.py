"""chasm_state — steal atisharma/chasm + LocalLLaMA MUD+LLM (152w71n).

The dream: a place always remembers what happened there.
Chasm: memory/places/*.md is the locus diary. events/*.md is the global log.
Mag: campaign JSON + game_world knots remain ground truth. The place file is
the visible diary. Look reads it. Overwrite is amnesia.

Schema: mag_chasm_state.v1
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "mag_chasm_state.v1"
CHASM_DIR = ROOT / "memory" / "working" / "chasm"


def _slug(s: str) -> str:
    out = "".join(c.lower() if c.isalnum() else "-" for c in (s or "x"))
    return (out.strip("-") or "x")[:48]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def place_path(campaign_id: str, room_id: str) -> Path:
    return CHASM_DIR / str(campaign_id or "none") / "places" / f"{_slug(room_id)}.md"


def recall(campaign_id: str, room_id: str, *, limit: int = 8) -> list[str]:
    """What this place remembers. Empty if the diary was never written."""
    p = place_path(campaign_id, room_id)
    if not p.is_file():
        return []
    body = p.read_text(encoding="utf-8", errors="replace")
    if "## happened" not in body:
        return []
    tail = body.split("## happened", 1)[1]
    out = []
    for line in tail.splitlines():
        s = line.strip()
        if s.startswith("- "):
            out.append(s[2:].strip())
    return out[-limit:]


def persist(camp: dict[str, Any], *, events: list[str] | None = None, action: str = "") -> dict[str, Any]:
    """Write character snapshot; APPEND the place diary. Never erase happened."""
    cid = str(camp.get("campaign_id") or "none")
    base = CHASM_DIR / cid
    (base / "places").mkdir(parents=True, exist_ok=True)
    (base / "characters").mkdir(parents=True, exist_ok=True)
    (base / "events").mkdir(parents=True, exist_ok=True)
    pl = camp.get("player") or {}
    from mag.game_campaign import _room
    room = _room(camp)
    rid = str(camp.get("room_id") or "void")
    pname = _slug(str(pl.get("name") or "adventurer"))

    (base / "WORLD_STATE.md").write_text(
        f"# WORLD_STATE\n\n- campaign: `{cid}`\n- room: `{rid}`\n- status: {camp.get('status')}\n"
        f"- turn: {(camp.get('storyteller') or {}).get('turn_n')}\n"
        f"- player: {pl.get('name') or 'unseated'}\n",
        encoding="utf-8",
    )

    exits = room.get("exits") or {}
    if isinstance(exits, dict):
        ex_s = ", ".join(str(k) for k in exits.keys())
    else:
        ex_s = ", ".join(str(x) for x in (exits or []))
    header = (
        f"# {room.get('name') or rid}\n\n"
        f"- id: `{rid}`\n"
        f"- exits: {ex_s or 'none'}\n\n"
        f"{(room.get('desc') or '').strip()}\n"
    )
    pp = base / "places" / f"{_slug(rid)}.md"
    prior = pp.read_text(encoding="utf-8", errors="replace") if pp.is_file() else ""
    diary = ""
    if "## happened" in prior:
        diary = prior.split("## happened", 1)[1]
    bits = [s[2:].strip() for s in diary.splitlines() if s.strip().startswith("- ")]
    bits = [b for b in bits if "`look`" not in b and "`status`" not in b and "`help`" not in b]
    ev_lines = [str(e).strip() for e in (events or []) if str(e).strip()]
    deed = action not in ("look", "status", "help", "inventory")
    if deed and (action or ev_lines):
        bits.append(_now() + " `" + (action or "act") + "` " + " | ".join(ev_lines)[:160])
    bits = bits[-24:]
    body = header + "\n## happened\n\n" + "".join("- " + b + "\n" for b in bits)
    pp.write_text(body, encoding="utf-8")

    inv = ", ".join(str(i) for i in (pl.get("inventory") or [])) or "empty"
    (base / "characters" / f"{pname}.md").write_text(
        f"# {pl.get('name') or 'Adventurer'}\n\n- archetype: {pl.get('archetype') or ''}\n"
        f"- hp: {pl.get('hp')}/{pl.get('hp_max')}\n- inventory: {inv}\n- room: `{rid}`\n",
        encoding="utf-8",
    )

    if action or ev_lines:
        log = base / "events" / "log.md"
        prev = log.read_text(encoding="utf-8") if log.is_file() else "# events\n\n"
        log.write_text(prev + f"- {_now()} `{rid}` `{action}` " + " | ".join(ev_lines)[:320] + "\n", encoding="utf-8")

    return {"ok": True, "schema": SCHEMA, "path": str(base.relative_to(ROOT)).replace("\\", "/"), "n_happened": len(bits)}
