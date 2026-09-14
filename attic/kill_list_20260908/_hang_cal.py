from pathlib import Path

# --- campaign: Calcifer is the room's fire/torch, named by the player ---
p = Path("mag/game_campaign.py")
t = p.read_text(encoding="utf-8")

old_people_end = '''        if not name:
            continue
'''
# find people_in_room append pattern
if "calcifer" not in t[t.find("def people_in_room"):t.find("def people_in_room")+1200]:
    marker = "    return names\n"
    # first return names after people_in_room
    i = t.find("def people_in_room")
    j = t.find("    return names", i)
    insert = '''    blob = " ".join([
        str(room.get("name") or ""),
        str(room.get("desc") or ""),
        " ".join(str(x) for x in (room.get("tags") or [])),
        " ".join(str(h) for h in (room.get("hooks") or [])),
    ]).lower()
    if any(w in blob for w in ("fire", "hearth", "torch", "flame")):
        if "calcifer" not in [n.lower() for n in names]:
            names.append("Calcifer")
'''
    t = t[:j] + insert + t[j:]

old_look = '''    if n in ("fire", "hearth", "flame"):
        return "The fire argues with the damp. It is the only honest heat in the room."
'''
new_look = '''    if n in ("fire", "hearth", "flame", "calcifer", "torch"):
        if "calcifer" in n or "torch" in n:
            hit = next((h for h in hooks if "torch" in h.lower() or "fire" in h.lower()), "")
            if "torch" in (desc + " " + " ".join(hooks)).lower() or "keep" in str(room.get("id") or room.get("name") or "").lower():
                return (
                    "The torch is the same fire you named Calcifer. "
                    "It does not live in a grate here. It lives in the work. "
                    "One flame, many rooms. It pops when you talk past it."
                )
        return "The fire argues with the damp. It is the only honest heat in the room. You named it Calcifer."
'''
if old_look not in t:
    raise SystemExit("look fire missing")
t = t.replace(old_look, new_look, 1)

# talk calcifer before empty
old_empty = '''        else:
            events.append("No one here to talk to. The fire pops.")
            return events
'''
new_empty = '''        else:
            events.append(_talk_calcifer(camp) or "No one here to talk to. The fire pops.")
            return events
'''
if old_empty not in t:
    raise SystemExit("empty talk missing")
t = t.replace(old_empty, new_empty, 1)

# after target resolved, calcifer branch near barkeep
if "def _talk_calcifer" not in t:
    helper = '''
def _talk_calcifer(camp: dict[str, Any]) -> str:
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
    t = t.replace("def _look_at(", helper + "def _look_at(", 1)

# if target is calcifer
old_tlow = '''    tlow = target.lower()
    if tlow in ("barkeep", "mira") or "barkeep" in tlow:
'''
new_tlow = '''    tlow = target.lower()
    if "calcifer" in tlow or tlow in ("fire", "hearth", "torch", "flame"):
        events.append(_talk_calcifer(camp) or "The fire pops. You named it Calcifer.")
        return events
    if tlow in ("barkeep", "mira") or "barkeep" in tlow:
'''
if old_tlow not in t:
    raise SystemExit("tlow barkeep missing")
t = t.replace(old_tlow, new_tlow, 1)

# parse wink at
old_talk = '''    if t in ("talk", "speak", "say"):
        return {"type": "talk", "raw": (text or "").strip()[:240]}
'''
new_talk = '''    if re.search(r"\\b(wink|nod|wave)\\s+at\\b", t):
        m = re.search(r"\\b(?:wink|nod|wave)\\s+at\\s+(?:the\\s+)?(.+)$", t)
        who = ((m.group(1) if m else "").strip()[:80])
        return {"type": "talk", "raw": (text or "").strip()[:240], "target": who or "calcifer"}
    if t in ("talk", "speak", "say"):
        return {"type": "talk", "raw": (text or "").strip()[:240]}
'''
if "wink|nod|wave" not in t:
    if old_talk not in t:
        raise SystemExit("talk parse missing")
    t = t.replace(old_talk, new_talk, 1)

p.write_text(t, encoding="utf-8")
print("campaign calcifer")
