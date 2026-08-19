from pathlib import Path
import json
p = Path("mag/game_campaign.py")
t = p.read_text(encoding="utf-8")
old_n = '''    hooks = room.get("hooks") or []
    rumor = ""
    for h in hooks:
        s = str(h)
        if s.lower().startswith("rumor"):
            rumor = s.split(":", 1)[-1].strip()
            break
    if rumor:
        parts.append("The problem: " + rumor)
'''
new_n = '''    hooks = room.get("hooks") or []
    rumor = ""
    situation: list[str] = []
    for h in hooks:
        s = str(h).strip()
        if not s:
            continue
        if s.lower().startswith("rumor"):
            rumor = s.split(":", 1)[-1].strip()
            continue
        if s.lower().startswith("quest"):
            continue
        situation.append(s)
    if rumor:
        parts.append("The problem: " + rumor)
    for s in situation[:3]:
        parts.append(s)
'''
if old_n not in t:
    raise SystemExit("narrate hooks block missing")
t = t.replace(old_n, new_n, 1)
old_s = '''            {"name": room.get("name"), "desc": (room.get("desc") or "")[:240]},
'''
new_s = '''            {
                "name": room.get("name"),
                "desc": (room.get("desc") or "")[:240],
                "hooks": list(room.get("hooks") or [])[:6],
            },
'''
if old_s not in t:
    raise SystemExit("set_state room blob missing")
t = t.replace(old_s, new_s, 1)
p.write_text(t, encoding="utf-8")
print("patched narrate+set_state")
