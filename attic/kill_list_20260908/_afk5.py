from mag.game_campaign import latest_any, apply_action, parse_player_speech, _room
from mag.chasm_state import persist
from mag.wave import snapshot
from mag.party_subchain import append
c = latest_any()
cid, rid = c.get("campaign_id"), c.get("room_id")
room = _room(c)
persist(c, events=["The goblin camp holds its breath."], action="idle")
speak = (snapshot().get("speak_text") or "").strip()
nar = (apply_action(cid, parse_player_speech("look")).get("narrate") or "")[:200]
append(seat="ghost", ok=True, move="AFK 17:58 FILE room="+str(rid), kind="turn")
print("room", rid, room.get("name"))
print("hooks", room.get("hooks"))
print("SPEAK", speak[:160])
print("moved", rid != "claw_hall")
print("NAR", nar)
