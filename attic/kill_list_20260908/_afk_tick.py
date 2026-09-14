from mag.game_campaign import latest_any, apply_action, parse_player_speech
from mag.chasm_state import persist, recall
from mag.wave import snapshot
from mag.party_subchain import append
import time
c = latest_any()
cid, rid = c.get("campaign_id"), c.get("room_id")
beat = "Calcifer keeps the heat. Dice wait mid-game. The dock still drinks paint."
persist(c, events=[beat], action="idle")
t0 = time.time()
s = snapshot()
dt = round(time.time() - t0, 2)
speak = (s.get("speak_text") or "")[:180]
look = apply_action(cid, parse_player_speech("look"))
nar = (look.get("narrate") or "")[:280]
r = append(seat="ghost", ok=True, move="AFK tick: keep_gate chasm + speak_text. Phone mic is trycloudflare HTTPS not LAN http.", kind="turn")
print("room", rid)
print("dt", dt)
print("SPEAK", speak)
print("NAR", nar)
print("sub", r.get("ok"), r.get("n"))
mem = recall(cid, rid, limit=1)
print("MEM", mem[-1][:160] if mem else "none")
