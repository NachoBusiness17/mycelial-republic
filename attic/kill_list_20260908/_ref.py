from pathlib import Path

# --- game_campaign ---
p = Path("mag/game_campaign.py")
t = p.read_text(encoding="utf-8")
old = '''        if low.startswith("barkeep"):
            name = "barkeep"
        elif "stranger" in low:
            name = "stranger"
        elif ":" in s[:28]:
'''
new = '''        if low.startswith("barkeep"):
            name = "barkeep"
        elif "stranger" in low:
            name = "stranger"
        elif "merchant" in low or "captive" in low:
            name = "merchant"
        elif "goblin" in low:
            name = "goblin"
        elif ":" in s[:28]:
'''
if old not in t:
    raise SystemExit("people block missing")
t = t.replace(old, new, 1)

old2 = '''            line = "You walk " + direction + " and a building appears: " + name + "."
'''
new2 = '''            low_n = name.lower()
            if any(w in low_n for w in ("cave", "hall", "fork", "cellar", "tunnel", "pit", "road")):
                line = "You walk " + direction + " into " + name + "."
            else:
                line = "You walk " + direction + " and a building appears: " + name + "."
'''
if old2 not in t:
    raise SystemExit("walk line missing")
t = t.replace(old2, new2, 1)

old3 = '''    line = "The torch pops — Calcifer, same fire as the lantern."
    try:
        from mag.fish_ear import decompile, originate
        decompile("babel fish")
        origin_what = str(((originate() or {}).get("origin") or {}).get("what") or "")
    except Exception:
        origin_what = ""
    voice = ""
    try:
        from mag.persona_recall import recall
        pr = recall(archetype="trickster", region="babel")
        voice = str(((pr.get("persona") or {}).get("voice") or "")).strip()
    except Exception:
        voice = ""
    rib = _rib_babel_speech()
    bits = [line]
    if voice:
        bits.append(voice)
    if rib:
        bits.append(rib)
    elif origin_what:
        bits.append(origin_what)
    bits.append("The liquid familiar is that fish in a body of work, not a pet on the floor.")
    return _player_signal(" ".join(bits), source="calcifer") or line
'''
new3 = '''    line = "The torch pops — Calcifer, same fire as the lantern."
    rib = _rib_babel_speech()
    bits = [line]
    if rib:
        bits.append(rib)
    return _player_signal(" ".join(bits), source="calcifer") or line
'''
if old3 not in t:
    raise SystemExit("calcifer talk missing")
t = t.replace(old3, new3, 1)

# merchant talk after calcifer tlow
old4 = '''    if "calcifer" in tlow or tlow in ("fire", "hearth", "torch", "flame"):
        events.append(_talk_calcifer(camp) or "The fire pops. You named it Calcifer.")
        return events
'''
new4 = '''    if "calcifer" in tlow or tlow in ("fire", "hearth", "torch", "flame"):
        events.append(_talk_calcifer(camp) or "The fire pops. You named it Calcifer.")
        return events
    if "merchant" in tlow or "captive" in tlow:
        hit = _hook_for_person(room, "merchant") or "The merchant is bound. The crate with the keep seal sits in reach."
        events.append(hit)
        return events
'''
if old4 not in t:
    raise SystemExit("calcifer tlow missing")
t = t.replace(old4, new4, 1)
p.write_text(t, encoding="utf-8")
print("campaign patched")

w = Path("mag/wave.py").read_text(encoding="utf-8")
# skip nested remember-of-idle in bits
if "This place remembers" in w and "chasm_recall" in w:
    oldm = '''                if mem:
                    line = _re.sub(r"\\bsession[_-]?id\\S*", "", str(mem[-1]), flags=_re.I)
                    line = " ".join(line.split())
                    if line:
                        bits.append("This place remembers: " + line[:160])
'''
    newm = '''                if mem:
                    line = _re.sub(r"\\bsession[_-]?id\\S*", "", str(mem[-1]), flags=_re.I)
                    line = " ".join(line.split())
                    if "`idle`" in line.lower() or line.lower().startswith("this place remembers"):
                        line = ""
                    if line:
                        bits.append("This place remembers: " + line[:160])
'''
    if oldm not in w:
        print("idle remember block missing")
    else:
        Path("mag/wave.py").write_text(w.replace(oldm, newm, 1), encoding="utf-8")
        print("wave idle nested skip")
