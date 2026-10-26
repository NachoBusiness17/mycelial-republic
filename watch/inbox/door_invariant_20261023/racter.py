import json, urllib.request, datetime, os
D = os.path.dirname(os.path.abspath(__file__)); s = datetime.datetime.now().astimezone().isoformat()
P = open(os.path.join(D, "RACTER_PROMPT.txt"), encoding="utf-8").read()
b = json.dumps({"model": "gemma4:latest", "prompt": P, "stream": False, "options": {"temperature": 1.0}}).encode()
r = json.load(urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/generate", b, {"Content-Type": "application/json"}), timeout=1500))
open(os.path.join(D, "racter_out.txt"), "w", encoding="utf-8").write(r["response"])
json.dump({"lane": "ollama local (same as L6)", "model": "gemma4:latest", "temperature": 1.0, "start": s, "end": datetime.datetime.now().astimezone().isoformat()}, open(os.path.join(D, "racter_meta.json"), "w"))
