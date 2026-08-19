from pathlib import Path
p = Path("mag/game_campaign.py")
t = p.read_text(encoding="utf-8")
old = '''def _talk_calcifer(camp: dict[str, Any]) -> str:
    """Player-named hearth. Same fire as the lantern. FILE, not Howl plot."""
    room = _room(camp)
    blob = " ".join([
        str(room.get("name") or ""),
        str(room.get("desc") or ""),
        " ".join(str(h) for h in (room.get("hooks") or [])),
    ]).lower()
    if not any(w in blob for w in ("fire", "hearth", "torch", "flame", "damp")):
        return ""
    return (
        "The torch pops. Calcifer. You named the Mag hearth that, and it followed you out of the lantern. "
        "It does not do parlor tricks. It keeps the work warm. "
        "Wink and it winks back as a spark. The other seats can hear it too."
    )
'''
new = '''def _adjacent_memory(keys: list[str]) -> list[str]:
    """Single recall surface: verkle_lance.trace. Adjacent knots, not a new patch."""
    lines: list[str] = []
    try:
        from mag.verkle_lance import trace
    except Exception:
        return lines
    for key in keys:
        try:
            r = trace(str(key), limit=4)
        except Exception:
            continue
        if not r.get("found"):
            continue
        for m in r.get("matches") or []:
            sid = str(m.get("session_id") or m.get("theme") or "")
            if sid:
                lines.append(sid)
            if len(lines) >= 6:
                return lines
    return lines


def _talk_calcifer(camp: dict[str, Any]) -> str:
    """Hearth recalls adjacent Verkle, not a hardcoded Howl speech."""
    room = _room(camp)
    blob = " ".join([
        str(room.get("name") or ""),
        str(room.get("desc") or ""),
        " ".join(str(h) for h in (room.get("hooks") or [])),
    ]).lower()
    if not any(w in blob for w in ("fire", "hearth", "torch", "flame", "damp")):
        return ""
    adj = _adjacent_memory(["babel", "babelfish", "turtle", "percolat", "calcifer"])
    line = "The torch pops. Calcifer. Same fire as the lantern. It rummages the chain."
    if adj:
        line = (
            line
            + " It finds knot babelfish-turtles: a fish that lives inside translation, "
            + "riddler-speak to real intent, turtles all the way down. "
            + "The liquid familiar is that fish in a body of work, not a pet on the floor. "
            + "Adjacent: " + ", ".join(adj[:4]) + "."
        )
    else:
        line = line + " The chain is quiet on this name tonight."
    return line
'''
if old not in t:
    raise SystemExit("talk_calcifer missing")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("hung lance on calcifer")
