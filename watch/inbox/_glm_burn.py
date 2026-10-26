import json
import re
import time
import socket
import threading
import urllib.request
import urllib.parse
import ipaddress
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = ROOT / "watch" / "inbox" / "glm_burn"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw_v2.jsonl"
KEY_NAME = "ZAI_API_KEY"
URL = "https://api.z.ai/api/coding/paas/v4/chat/completions"
MODEL = "glm-5.3-flash"
ALLOWED = "api.z.ai"

key = ""
for ln in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
    if ln.strip().startswith(KEY_NAME + "="):
        key = ln.split("=", 1)[1].strip().strip('"').strip("'")
        break
assert key, "no key"

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

_OPENER = urllib.request.build_opener(_NoRedirect)

def guarded_get(url):
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname != ALLOWED:
        raise ValueError("host not allowed")
    for _f, _s, _pr, _c, sa in socket.getaddrinfo(p.hostname, 443):
        if not ipaddress.ip_address(sa[0]).is_global:
            raise ValueError("resolved to non-global address")
    return url

def call(prompt, max_tokens=None):
    url = guarded_get(URL)
    body = {"model": MODEL, "temperature": 0.3,
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
                 "User-Agent": "mag-glm-burn/1.0"})
    with _OPENER.open(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
    usage = d.get("usage", {})
    txt = (d["choices"][0]["message"].get("content") or "").strip()
    return txt, usage

# Build the burn task list
tasks = []

# A: Q corpus complete deep-read
q_posts = []
for ln in (ROOT / "watch/inbox/qdrop_export/qdrops.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
    r = json.loads(ln)
    if r.get("trip") == "!!Hs1Jq13jV6" or (r.get("name") or "").strip() == "Q":
        q_posts.append("[" + str(r.get("drop_no")) + " " + str(r.get("ts"))[:10] + "] " + (r.get("text") or ""))
CH = 45
for i in range(0, len(q_posts), CH):
    chunk = "\n\n".join(q_posts[i:i+CH])
    tasks.append({"id": "Q-%03d" % (i//CH), "kind": "q_deep_read",
                  "prompt": ("You are the deep reader of the Q Drops corpus for a record-keeping research fleet. "
                  "This is chunk %d. Extract: (1) every SPECIFIC dated or checkable claim, (2) recurring symbols and phrases, "
                  "(3) narrative arcs across this chunk, (4) anything that reads as coordination language. Be exhaustive, "
                  "cite post numbers.\n\n=== CHUNK ===\n" % (i//CH + 1)) + chunk[:90000]})

# B: Cooper deep-read
coop = (ROOT / "canon/riddler_corpus/mystery_babylon_fulltext.txt").read_text(encoding="utf-8", errors="replace")
CS = 60000
for i in range(0, len(coop), CS):
    tasks.append({"id": "COOP-%03d" % (i//CS), "kind": "cooper_deep_read",
                  "prompt": ("Deep-read chunk %d of William Cooper's Mystery Babylon broadcasts (transcribed, 1990s). "
                  "Extract: (1) specific checkable claims about institutions/people/events, (2) prophecies or predictions with any "
                  "timeframe, (3) the core narrative per chunk, (4) vocabulary later riddle waves might have inherited. "
                  "Cite context.\n\n=== CHUNK ===\n" % (i//CS + 1)) + coop[i:i+CS]})

# C: four-condition battery drafts
for i in range(5):
    tasks.append({"id": "BATT-%02d" % (i+1), "kind": "battery_draft",
                  "prompt": ("Draft 4 unseen coordination dilemmas for a pre-registered agent-fleet experiment (conditions: cold / "
                  "warm-static / warm-append-only / warm-deleting). Each dilemma: a scenario where several AI agents must pick one "
                  "action from a closed set of 4 options, involving either resource scarcity, a doctrine conflict, an amendment "
                  "conflict, or a receipt-vs-expediency tradeoff. Number them, give the 4 options, mark the coherence-relevant "
                  "tension in one line. Batch %d of 5; avoid repeating scenarios from other batches; these must be NOVEL.\n\n"
                  "Batch seed: use number %d and vary domain across: shipping lanes, hospital logistics, treasure salvage, "
                  "wildfire response, satellite scheduling." % (i+1, 137 + i*29))})

# D: Liber Primus analysis
lp = (ROOT / "canon/riddler_corpus/liberprimus/liberprimus.txt").read_text(encoding="utf-8", errors="replace")
tasks.append({"id": "LP-001", "kind": "liber_primus",
              "prompt": "This is the unsolved Liber Primus (Cicada 3301) runic text, 27-rune Gematria mod 29. Analyze structure: repeated segments, page/section boundaries, any shift in statistical behavior between sections. Propose the two most promising attack angles given the text's own structure.\n\n=== TEXT ===\n" + lp[:60000]})

print("total burn tasks:", len(tasks), flush=True)

lock = threading.Lock()
done_count = [0]
ok_count = [0]
char_count = [0]

def run_task(t):
    t0 = time.time()
    try:
        txt, usage = call(t["prompt"], max_tokens=2200)
        row = {"id": t["id"], "kind": t["kind"], "ok": True, "chars": len(txt),
               "usage": usage, "secs": round(time.time()-t0, 1), "text": txt[:6000]}
    except Exception as e:
        row = {"id": t["id"], "kind": t["kind"], "ok": False, "error": str(e)[:100]}
    with lock:
        with RAW.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        done_count[0] += 1
        if row.get("ok"):
            ok_count[0] += 1
            char_count[0] += row.get("chars", 0)
        if done_count[0] % 5 == 0:
            print("done", done_count[0], "ok", ok_count[0], flush=True)
    return row

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as ex:
    list(ex.map(run_task, tasks))
print("BURN DONE tasks=%d ok=%d out_chars=%d" % (len(tasks), ok_count[0], char_count[0]), flush=True)
