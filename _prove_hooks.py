from pathlib import Path
import ast, json
ast.parse(Path("mag/game_campaign.py").read_text(encoding="utf-8"))
print("ast ok")
from mag.game_campaign import latest_any, parse_player_speech, apply_action, _narrate_room, _room
c = latest_any()
print("room", c.get("room_id"))
print("hooks", _room(c).get("hooks"))
print("NARRATE", _narrate_room(c)[:500])
cid = c.get("campaign_id")
for s in ["look", "look dice", "look sword"]:
    r = apply_action(cid, parse_player_speech(s))
    print("ACT", s, (r.get("narrate") or "")[:280])
    print("---")
ws = json.loads(Path("memory/game/world/world_state.json").read_text(encoding="utf-8"))
v = (((ws.get("world") or {}).get("table.room.keep_gate") or {}).get("value"))
print("WORLD", v)
