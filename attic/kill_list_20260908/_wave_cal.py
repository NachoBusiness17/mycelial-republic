from pathlib import Path
t = Path("mag/wave.py").read_text(encoding="utf-8")
old = '''        if not name:
            continue
        if any(x["name"].lower() == name.lower() for x in out):
            continue
        out.append({"name": name, "role": "here", "kind": "room", "talkable": True})
    return out
'''
new = '''        if not name:
            continue
        if any(x["name"].lower() == name.lower() for x in out):
            continue
        out.append({"name": name, "role": "here", "kind": "room", "talkable": True})
    blob = " ".join([str(sc.get("room_name") or ""), str(sc.get("room_desc") or ""), str(sc.get("hook") or "")]).lower()
    if any(w in blob for w in ("fire", "hearth", "torch")):
        if not any(str(x.get("name") or "").lower() == "calcifer" for x in out):
            out.append({"name": "Calcifer", "role": "hearth", "kind": "room", "talkable": True})
    return out
'''
if "Calcifer" not in t:
    if old not in t:
        raise SystemExit("who return missing")
    t = t.replace(old, new, 1)
old_keep = '''        parts.append('<text x="360" y="58" text-anchor="middle" fill="#f2f2f2" font-size="18" font-family="Helvetica, Arial, sans-serif" data-look="keep" class="exit" cursor="pointer">keep</text>')
'''
new_keep = '''        parts.append('<text x="360" y="58" text-anchor="middle" fill="#f2f2f2" font-size="18" font-family="Helvetica, Arial, sans-serif" data-look="keep" class="exit" cursor="pointer">keep</text>')
        parts.append('<text x="470" y="200" text-anchor="middle" fill="#f2f2f2" font-size="16" font-family="Helvetica, Arial, sans-serif" data-talk="calcifer" class="exit" cursor="pointer">calcifer</text>')
'''
if 'data-talk="calcifer"' not in t:
    if old_keep not in t:
        raise SystemExit("keep label missing")
    t = t.replace(old_keep, new_keep, 1)
Path("mag/wave.py").write_text(t, encoding="utf-8")
print("wave ok", "Calcifer" in t, 'data-talk="calcifer"' in t)
