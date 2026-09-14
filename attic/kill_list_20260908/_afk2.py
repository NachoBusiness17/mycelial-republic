from mag.game_campaign import latest_any, apply_action, parse_player_speech
from mag.chasm_state import persist, recall
from mag.wave import snapshot
from mag.party_subchain import append
import time
c = latest_any()
cid, rid = c.get("campaign_id"), c.get("room_id")
mem_before = recall(cid, rid, limit=1)
persist(c, events=["The afternoon holds. Calcifer, dice, dock."], action="idle")
t0 = time.time()
s = snapshot()
dt = round(time.time() - t0, 2)
speak = (s.get("speak_text") or "").strip()
look = apply_action(cid, parse_player_speech("look"))
nar = (look.get("narrate") or "")
append(seat="ghost", ok=True, move="AFK 14:58 tick keep_gate FILE. speak_text live.", kind="turn")
mem = recall(cid, rid, limit=1)
print("room", rid, "dt", dt)
print("SPEAK", speak[:200])
print("MEM0", (mem_before[-1] if mem_before else "")[:120])
print("MEM1", (mem[-1] if mem else "")[:160])
print("same_speak", speak.startswith("Empty guard post") or "dice" in speak.lower())
print("grew", (mem[-1] if mem else "") != (mem_before[-1] if mem_before else ""))
