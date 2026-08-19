from mag.game_campaign import latest_any, apply_action, parse_player_speech, _room
from mag.chasm_state import persist, recall
from mag.wave import snapshot
from mag.party_subchain import append
c = latest_any()
cid, rid = c.get("campaign_id"), c.get("room_id")
room = _room(c)
s0 = (snapshot().get("speak_text") or "").strip()
persist(c, events=["The captive breathes. The crate does not move."], action="idle")
s1 = (snapshot().get("speak_text") or "").strip()
look = apply_action(cid, parse_player_speech("look"))
nar = (look.get("narrate") or "")[:240]
append(seat="ghost", ok=True, move="AFK 16:57 FILE room="+str(rid), kind="turn")
print("room", rid, room.get("name"))
print("hooks", room.get("hooks"))
print("SPEAK", s1[:180])
print("moved", rid not in ("claw_hall",))
print("speak_changed", s0 != s1)
print("NAR", nar)
