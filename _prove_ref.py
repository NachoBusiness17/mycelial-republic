import ast
from pathlib import Path
ast.parse(Path("mag/game_campaign.py").read_text(encoding="utf-8"))
ast.parse(Path("mag/wave.py").read_text(encoding="utf-8"))
print("ast ok")
from mag.game_campaign import latest_any, people_in_room, parse_player_speech, apply_action, _room
c = latest_any()
print("who", people_in_room(c))
cid = c.get("campaign_id")
for s in ["talk to merchant", "talk to calcifer", "look crate"]:
    r = apply_action(cid, parse_player_speech(s))
    print("==", s)
    print((r.get("narrate") or "")[:280])
print("walk helper", "into " in Path("mag/game_campaign.py").read_text(encoding="utf-8"))
