from mag.game_campaign import latest_any, _room, people_in_room, parse_player_speech, apply_action
from mag.chasm_state import recall
from mag.wave import snapshot
c = latest_any()
rid = c.get("room_id")
room = _room(c)
log = c.get("log") or []
print("cid", c.get("campaign_id"))
print("room", rid, room.get("name"))
print("desc", room.get("desc"))
print("hooks", room.get("hooks"))
print("exits", room.get("exits"))
print("who", people_in_room(c))
print("turns", len(log), "status", c.get("status"))
print("==== last 25 log ====")
for e in log[-25:]:
    if not isinstance(e, dict):
        print(e)
        continue
    print((e.get("ts") or "")[-12:], e.get("action") or e.get("type") or "", (e.get("text") or e.get("line") or str(e))[:140])
print("==== chasm ====")
mem = recall(c.get("campaign_id"), rid, limit=8)
for m in mem or []:
    print(str(m)[:180])
s = snapshot()
print("SPEAK", (s.get("speak_text") or "")[:160])
