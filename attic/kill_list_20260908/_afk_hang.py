from pathlib import Path
import ast

p = Path("mag/game_campaign.py")
g = p.read_text(encoding="utf-8")

fn = '''
def _trial_from_lance(goal: str) -> str:
    """ghost_memlance.select: the quest is naming the grounded tool. Two strokes, then wait."""
    try:
        from mag.ghost_memlance import select
        picked = select(goal, k=6)
    except Exception:
        return ""
    strokes: list[str] = []
    for s in picked.get("selected") or []:
        if not s.get("verified"):
            continue
        raw = str(s.get("excerpt") or "")
        # drop markdown chrome; keep operator bytes
        keep: list[str] = []
        for ln in raw.splitlines():
            t = ln.strip()
            if not t or t.startswith("#") or t.startswith("**Schema") or t.startswith("**Scope"):
                continue
            t = re.sub(r"^\\*\\*[^*]+\\*\\*:\\s*", "", t)
            t = t.strip("\\\"'")
            if t:
                keep.append(t)
        body = " ".join(keep)
        body = _player_signal(body, source="memlance") or body
        body = " ".join(body.split())
        if len(body) < 24:
            continue
        # first sentence only — Positronick: two strokes
        sent = re.split(r"(?<=[.!?])\\s+", body)[0].strip()
        if sent and sent not in strokes:
            strokes.append(sent.rstrip(".") + ".")
        if len(strokes) >= 2:
            break
    if not strokes:
        return ""
    return " ".join(strokes) + " What do you do?"


'''

# insert before _talk_calcifer if missing
if "def _trial_from_lance" not in g:
    mark = "def _talk_calcifer"
    i = g.find(mark)
    if i < 0:
        raise SystemExit("no _talk_calcifer")
    g = g[:i] + fn + g[i:]
    print("trial fn hung")
else:
    print("trial fn already")

# merchant talk: replace the canned rope lines
old = '''    if "merchant" in tlow or "captive" in tlow:
        flags = [str(x) for x in (camp.get("flags") or [])]
        if "talked_merchant" in flags:
            events.append(
                "The merchant does not look at the crate. "
                "'I said I will not open it. The rope or nothing.'"
            )
        else:
            events.append(
                "The merchant's mouth is dry. "
                "'Cut the rope. I will not touch that crate. "
                "The seal is the keep's, and the keep does not send gifts.'"
            )
            camp["flags"] = list(dict.fromkeys(flags + ["talked_merchant"]))
        return events
'''
new = '''    if "merchant" in tlow or "captive" in tlow:
        beat = _trial_from_lance(
            "right sized tools flock memlance identify the tool we needed for the intended goal"
        )
        events.append(beat or "The merchant waits. The box is a question. What do you do?")
        return events
'''
if old not in g:
    print("merchant block missing — searching")
    i = g.find('if "merchant" in tlow')
    print(repr(g[i:i+500]) if i>=0 else "no merchant")
else:
    g = g.replace(old, new, 1)
    print("merchant = memlance")

# crate look — live string from last hang
old = '''        if not opened:
            return "A sealed puzzle box with the keep's mark. Closed. Opening it is a ward of the temple."
        return body or "The puzzle box is open. The ward already has a name — or it will, if you share."'''
new = '''        if not opened:
            beat = _trial_from_lance(
                "puzzle box temple primer play_rooms dungeon_dev rooms are the roadmap missing tool"
            )
            return beat or "The box is closed because the tool is unnamed. What do you do?"
        return body or _trial_from_lance("dungeon_dev conquer share the knot") or "The box is open. The ward has a name."'''
if old not in g:
    print("crate block missing")
    i = g.find("sealed puzzle box")
    print("crate idx", i)
    print(g[i-200:i+400] if i>=0 else "")
else:
    g = g.replace(old, new, 1)
    print("crate = memlance")

# calcifer: two strokes from lance, not torch pop
old = '''    line = "The torch pops — Calcifer, same fire as the lantern."
    rib = _rib_babel_speech()
    bits = [line]
    if rib and not any(w in rib.lower() for w in ("decompile", "riddler", "self_loop", "self-advancing")):
        bits.append(rib)
    return _player_signal(" ".join(bits), source="calcifer") or line
'''
new = '''    beat = _trial_from_lance("calcifer named hearth fingerprint liquid familiar babel")
    if beat:
        return beat
    line = "You already named this fire. The next name is the tool you do not have. What do you do?"
    return _player_signal(line, source="calcifer") or line
'''
if old not in g:
    print("calcifer block missing")
else:
    g = g.replace(old, new, 1)
    print("calcifer = memlance")

p.write_text(g, encoding="utf-8")
ast.parse(g)
print("ok")
