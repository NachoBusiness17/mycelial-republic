from pathlib import Path
t = Path("mag/game_campaign.py").read_text(encoding="utf-8")
old = '''    rib = _rib_babel_speech()
    bits = [line]
    if rib:
        bits.append(rib)
    return _player_signal(" ".join(bits), source="calcifer") or line
'''
new = '''    rib = _rib_babel_speech()
    bits = [line]
    if rib and not any(w in rib.lower() for w in ("decompile", "riddler", "self_loop", "self-advancing")):
        bits.append(rib)
    return _player_signal(" ".join(bits), source="calcifer") or line
'''
if old not in t:
    raise SystemExit("rib bits missing")
Path("mag/game_campaign.py").write_text(t.replace(old, new, 1), encoding="utf-8")
print("rib theater skip")
from mag.game_campaign import latest_any, parse_player_speech, apply_action
c = latest_any()
r = apply_action(c.get("campaign_id"), parse_player_speech("talk to calcifer"))
print((r.get("narrate") or "")[:240])
