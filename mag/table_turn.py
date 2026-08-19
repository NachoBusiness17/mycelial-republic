"""table_turn — MUD door. Channel=table never Voice Mag, never DeepSeek.

Steal: LocalLLaMA 152w71n (engine owns structure) + Chasm (state is files).
The lantern is a game. Howdy is talk. A mug is drink. A paragraph is in-world talk.
Player speech is character action AND Mag work (attention map). Wait for the player.
"""
from __future__ import annotations

import re
from typing import Any

SCHEMA = "mag_table_turn.v1"
_WORK_RE = re.compile(r"\b(patch|hang|steal|fix|cook|file|share|bounty|work)\b", re.I)


def _speech_plain(text: str) -> str:
    """fish_ear.decompile -> percolator.partition. Session ids are noise."""
    t = (text or "").strip()
    try:
        from mag.fish_ear import decompile
        t = str((decompile(t) or {}).get("decompiled") or t)
    except Exception:
        pass
    try:
        from mag.percolator import partition
        part = partition(t, source="table_turn")
        kept = [str(r.get("sentence") or "").strip() for r in (part.get("signal") or [])]
        kept = [s for s in kept if s]
        if kept:
            t = " ".join(kept)
    except Exception:
        pass
    t = re.sub(r"\bsession[_-]?id\S*", "", t, flags=re.I)
    return " ".join(t.split())


def _map_work(text: str) -> str:
    """Existing APIs only. dungeon_dev if coding-task seam. detect, never fanout."""
    bits: list[str] = []
    blob = (text or "").lower()
    seam = False
    try:
        from mag import dungeon_dev
        hay = blob.replace("-", " ")
        for r in dungeon_dev.ROOMS:
            name = str(r.get("room") or "").replace("-", " ")
            region = str(r.get("region") or "").replace("-", " ")
            if (name and name in hay) or (region and region in hay):
                dungeon_dev.dungeon_state()
                bits.append(
                    "The coding-task room "
                    + str(r.get("room"))
                    + " is already on the dungeon map ("
                    + str(r.get("region"))
                    + ")."
                )
                seam = True
                break
        if not seam:
            st = dungeon_dev.dungeon_state()
            ip = list(st.get("in_progress") or [])
            if ip:
                bits.append("A coding-task seam is already in progress: " + str(ip[0]) + ".")
                seam = True
    except Exception:
        pass
    if not seam:
        try:
            from mag.swarm_emerge import detect
            det = detect()
            if int(det.get("n_detected") or 0) > 0:
                bits.append("The swarm still sees a seam. No fanout.")
        except Exception:
            pass
    try:
        from mag.socratic_research import SOCRATIC_TURNS, frame
        frame()
        q = str((SOCRATIC_TURNS or [""])[0] or "")
        q = re.sub(r"^SOCRATIC TURN \d+\s*\([^)]*\):\s*", "", q).strip()
        if "?" in q:
            q = q.split("?")[0].strip() + "?"
        else:
            q = q[:180]
        if q:
            bits.append(q)
    except Exception:
        pass
    return " ".join(bits)[:400]


def handle(body: dict[str, Any]) -> dict[str, Any]:
    text = str(body.get("text") or body.get("transcript") or "").strip()
    sid = str(body.get("session_id") or "").strip()
    text = _speech_plain(text) or text
    from mag.game_campaign import (
        apply_action,
        begin_play,
        latest_any,
        latest_for_session,
        parse_player_speech,
        save_campaign,
    )

    camp = latest_for_session(sid) if sid else None
    if not camp:
        camp = latest_any()
    if not camp or camp.get("status") not in ("active", "paused", "awaiting_character"):
        bp = begin_play(module_id="classic", voice_session_id=sid)
        camp = bp.get("campaign") or latest_any()
    if not camp:
        return {
            "ok": False,
            "schema": SCHEMA,
            "answer": "No campaign. The lantern is dark.",
            "speak_text": "No campaign.",
            "provider": "game_engine",
            "used_llm": False,
            "route": "table_void",
        }
    if camp.get("status") == "paused":
        camp["status"] = "active"
    if sid:
        camp["voice_session_id"] = sid
        save_campaign(camp)

    import re as _re
    chunks = _re.split(r"\s+(?:and|then)\s+", text, maxsplit=1)
    outs = []
    for chunk in chunks[:2]:
        chunk = (chunk or "").strip()
        if not chunk:
            continue
        act = parse_player_speech(chunk)
        if act is None:
            low = chunk.lower()
            inv = [str(x) for x in ((camp.get("player") or {}).get("inventory") or []) if x]
            hit = next((i for i in inv if i.lower() in low), "")
            if hit:
                act = {"type": "look", "item": hit}
            elif any(w in low.split() for w in ("hand", "hands", "bag", "bags", "have")):
                act = {"type": "look", "item": "hand"}
        if act is None or (act.get("type") == "drink" and len(chunk) > 48):
            act = {"type": "talk", "raw": chunk[:400]}
        outs.append(apply_action(str(camp.get("campaign_id")), act))
    out = outs[-1] if outs else {}
    if len(outs) > 1:
        bits = [str(o.get("narrate") or " ".join(o.get("events") or []) or "").strip() for o in outs]
        out = dict(out)
        out["narrate"] = " ".join(b for b in bits if b)
        out["choices"] = outs[-1].get("choices") or out.get("choices")
    speak = str(out.get("narrate") or " ".join(out.get("events") or []) or "").strip()
    if not speak:
        speak = "The fire pops. Nothing else answers."
    if _WORK_RE.search(text or ""):
        note = _map_work(text)
        if note:
            try:
                from mag.party_subchain import append as _ps_append
                _ps_append(seat="table", ok=True, move=note[:240], kind="play_as_work")
            except Exception:
                try:
                    from mag.steer import emit as _steer_emit
                    _steer_emit("play-as-work", "table", note[:400], steer_back=False)
                except Exception:
                    pass
            speak = (speak + " " + note).strip()
    try:
        from mag.game_dm_voice import extract_narrator
        wrapped = speak if speak.lstrip().startswith("#") else ("## Narrator\n\n" + speak)
        speak_text = " ".join(str(extract_narrator(wrapped) or speak).split())[:480]
    except Exception:
        speak_text = speak[:480]
    return {
        "ok": bool(out.get("ok")),
        "schema": SCHEMA,
        "session_id": sid,
        "transcript": text,
        "answer": speak,
        "speak_text": speak_text,
        "seat": "table",
        "route": "table_engine",
        "provider": "game_engine",
        "used_llm": False,
        "conversation": True,
        "campaign_id": camp.get("campaign_id"),
        "legal": out.get("legal"),
        "choices": out.get("choices") or [],
        "token_note": "table channel — engine only, no DeepSeek, no Voice Mag, no game_dm.turn",
    }
