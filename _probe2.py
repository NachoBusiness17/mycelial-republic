from pathlib import Path
import json
t = Path("mag/game_campaign.py").read_text(encoding="utf-8")
i = t.find("def _room(")
print("ROOM FN")
print(t[i:i+700])
print("RIB BABEL")
j = t.find("def _rib_babel_speech")
print(t[j:j+900])
print("LOOK HOOK FALLBACK")
k = t.find("if n and n in desc.lower()")
print(t[k:k+500])
ws = json.loads(Path("memory/game/world/world_state.json").read_text(encoding="utf-8"))
# walk for keep_gate
def walk(o, path=""):
    if isinstance(o, dict):
        if "keep_gate" in o:
            print("FOUND", path, "keys", list(o.keys())[:20])
            print(json.dumps(o.get("keep_gate") or o, default=str)[:800])
        for k,v in o.items():
            if k in ("keep_gate","table.room.keep_gate") or "keep_gate" in str(k):
                print("KEY", path+"/"+k, json.dumps(v, default=str)[:600])
            walk(v, path+"/"+str(k)[:40])
    elif isinstance(o, list) and len(o)<50:
        for n,v in enumerate(o[:20]):
            walk(v, path+f"[{n}]")
walk(ws)
