from mag.game_campaign import latest_any, apply_action, parse_player_speech, _room
from mag.chasm_state import persist, recall
from mag.wave import snapshot
from mag.party_subchain import append
c = latest_any()
cid, rid = c.get("campaign_id"), c.get("room_id")
room = _room(c)
name = room.get("name")
hooks = room.get("hooks")
mem0 = recall(cid, rid, limit=1)
s0 = (snapshot().get("speak_text") or "").strip()
persist(c, events=["The crack of light holds. Dust still falls."], action="idle")
s1 = (snapshot().get("speak_text") or "").strip()
look = apply_action(cid, parse_player_speech("look"))
nar = (look.get("narrate") or "")[:220]
mem1 = recall(cid, rid, limit=1)
append(seat="ghost", ok=True, move="AFK 15:57 FILE tick room="+str(rid), kind="turn")
print("room", rid, name)
print("hooks", hooks)
print("SPEAK0", s0[:160])
print("SPEAK1", s1[:160])
print("changed", s0 != s1 or rid != "courtyard")
print("NAR", nar)
print("MEM", (mem1[-1] if mem1 else "")[:140])
