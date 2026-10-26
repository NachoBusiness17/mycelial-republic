# Local Ollama only (qwen2.5:3b-instruct), temperature 0. No network beyond localhost.
import json, os, urllib.request, datetime
D = os.path.dirname(os.path.abspath(__file__))
P = open(os.path.join(D, "PROMPT_3B.txt"), encoding="utf-8").read()
s = datetime.datetime.now().astimezone().isoformat()
b = json.dumps({"model": "qwen2.5:3b-instruct", "prompt": P, "stream": False, "options": {"temperature": 0, "num_ctx": 8192}}).encode()
r = json.load(urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/generate", b, {"Content-Type": "application/json"}), timeout=600))
os.makedirs(os.path.join(D, "raw"), exist_ok=True)
open(os.path.join(D, "raw", "qwen3b_output.md"), "w", encoding="utf-8").write(r["response"])
json.dump({"model": r.get("model"), "start": s, "end": datetime.datetime.now().astimezone().isoformat(), "eval_count": r.get("eval_count"), "prompt_eval_count": r.get("prompt_eval_count")}, open(os.path.join(D, "raw", "qwen3b_meta.json"), "w"), indent=1)
print(r["response"])
