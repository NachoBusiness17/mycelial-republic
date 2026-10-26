# One DeepSeek direct call; key via existing carrier tools.ds_workhorse.load_key (never printed).
import sys, os, json, time, urllib.request, urllib.error, datetime
REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, REPO)
from tools.ds_workhorse import load_key
D = os.path.dirname(os.path.abspath(__file__))
P = open(os.path.join(D, "BLIND_PROMPT.txt"), encoding="utf-8").read()
body = json.dumps({"model": "deepseek-reasoner", "messages": [{"role": "user", "content": P}], "max_tokens": 65536}).encode()
key = load_key(); s = datetime.datetime.now().astimezone().isoformat(); attempts = []
for i in range(2):
    try:
        req = urllib.request.Request("https://api.deepseek.com/chat/completions", body, {"Content-Type": "application/json", "Authorization": "Bearer " + key})
        r = json.load(urllib.request.urlopen(req, timeout=1200)); attempts.append("ok"); break
    except urllib.error.HTTPError as e:
        attempts.append("HTTP %s %s" % (e.code, e.read()[:300])); r = None; break   # not transport: no retry
    except Exception as e:
        attempts.append("transport " + repr(e)[:200]); r = None; time.sleep(10)
meta = {"model_req": "deepseek-reasoner", "max_tokens": 65536, "start": s, "end": datetime.datetime.now().astimezone().isoformat(), "attempts": attempts}
if r:
    m = r["choices"][0]["message"]; meta.update(model=r.get("model"), usage=r.get("usage"), finish=r["choices"][0].get("finish_reason"))
    open(os.path.join(D, "raw", "blind_content.md"), "w", encoding="utf-8").write(m.get("content") or "")
    open(os.path.join(D, "raw", "blind_reasoning.md"), "w", encoding="utf-8").write(m.get("reasoning_content") or "")
json.dump(meta, open(os.path.join(D, "raw", "blind_meta.json"), "w"), indent=1)

