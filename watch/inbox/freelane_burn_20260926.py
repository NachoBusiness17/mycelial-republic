import ipaddress
import json
import os
import re
import socket
import sys
import threading
import time
import urllib.parse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.getcwd())
from models.env_load import load_dotenv  # noqa: E402

load_dotenv()

OUT_FILE = "logs/freelane_burn_20260926.jsonl"
WORKERS = 12
ASK_TAIL = ("Extract the mechanic's concrete numbers (rates, curves, unlock gates, economy costs) "
 "from design wikis and patch notes, the retention hook it pulls, the abuse vector players found, "
 "and a clone-or-skip verdict for a Roblox-style lane that already runs VM currency + boon drafts "
 "+ faction war + shared-respawn Pilgrim class. Quote load-bearing lines verbatim with sources. "
 "Never fabricate: if you could not fetch a source, say OWED. No em-dashes. "
 "Format: NUMBERS / RETENTION HOOK / ABUSE VECTOR / CLONE-OR-SKIP / EVIDENCE / SOURCES.")
LAWS = "Never fabricate. No em-dashes."
JID_RE = re.compile(r"^[a-z0-9-]+$")

LANES = [
    {"lane": "openrouter", "base": "https://openrouter.ai/api/v1", "keys": [os.environ.get("OPENROUTER_API_KEY"), os.environ.get("OPENROUTER_API_KEY_2")], "models": ["fireworks/ember-1", "aion-labs/aion-3.5-mini", "typesafe/jev-router"]},
    {"lane": "mistral", "base": "https://api.mistral.ai/v1", "keys": [os.environ.get("MISTRAL_API_KEY"), os.environ.get("MISTRAL_API_KEY_2")], "models": ["mistral-small-latest", "magistral-small-latest"]},
    {"lane": "cohere", "base": "https://api.cohere.com/compatibility/v1", "keys": [os.environ.get("COHERE_API_KEY_FREE")], "models": ["command-a-03-2025", "command-a-plus-05-2026"]},
    {"lane": "deepseek", "base": "https://api.deepseek.com/v1", "keys": [os.environ.get("DEEPSEEK_API_KEY")], "models": ["deepseek-chat"]},
]
LANES = [l for l in LANES if any(l["keys"])]
for l in LANES:
    l["keys"] = [k for k in l["keys"] if k]
HOSTS = {urllib.parse.urlparse(l["base"]).hostname for l in LANES}

print_lock = threading.Lock()


def load_briefs():
    jobs = []
    for name in ("GAMES_BRIEFS_creature-farming.json", "GAMES_BRIEFS_roguelike-run.json",
                 "GAMES_BRIEFS_horror-maze.json", "GAMES_BRIEFS_liveops-seasonal.json",
                 "GAMES_BRIEFS_coop-social.json"):
        with open("watch/inbox/" + name, encoding="utf-8") as f:
            for b in json.load(f):
                jobs.append((b["i"], b["g"], b["m"]))
    return jobs


def load_done():
    done = set()
    try:
        with open(OUT_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                    if row.get("ok"):
                        done.add(row.get("id"))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return done


def guarded_open(req, timeout):
    parsed = urllib.parse.urlparse(req.full_url)
    if parsed.scheme != "https" or parsed.hostname not in HOSTS:
        raise ValueError("host not allowed: " + str(parsed.hostname))
    for info in socket.getaddrinfo(parsed.hostname, 443):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise ValueError("resolved to blocked address")
    return urllib.request.build_opener().open(req, timeout=timeout)


def call(lane, model, prompt, key):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 6000, "temperature": 0.4}).encode("utf-8")
    req = urllib.request.Request(lane["base"] + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with guarded_open(req, timeout=300) as r:
        return json.loads(r.read())


def run_job(job):
    jid, game, mech = job
    if not JID_RE.fullmatch(jid):
        return 0
    prompt = ("GAME: " + game + "\nMECHANIC: " + mech + "\n\nTASK: " + ASK_TAIL + "\n\n" + LAWS)
    for attempt in range(1, 7):
        lane = LANES[(hash(jid) + attempt) % len(LANES)]
        model = lane["models"][(attempt - 1) % len(lane["models"])]
        key = lane["keys"][(attempt - 1) % len(lane["keys"])]
        try:
            d = call(lane, model, prompt, key)
            content = d.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = d.get("usage", {})
            result = {"id": jid, "game": game, "mechanic": mech, "lane": lane["lane"], "model": model,
                      "ok": True, "content": content,
                      "prompt_tokens": usage.get("prompt_tokens"),
                      "completion_tokens": usage.get("completion_tokens")}
            with print_lock:
                with open(OUT_FILE, "a", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
            return 1
        except urllib.error.HTTPError as e:
            err = "HTTP " + str(e.code)
        except Exception as e:
            err = type(e).__name__ + ": " + str(e)[:120]
        with print_lock:
            with open(OUT_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps({"id": jid, "ok": False, "attempt": attempt,
                                    "lane": lane["lane"], "error": err}) + "\n")
        time.sleep(15 * attempt)
    return 0


def main():
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    jobs = load_briefs()
    done = load_done()
    todo = [j for j in jobs if j[0] not in done]
    print("jobs:", len(jobs), "done:", len(done), "todo:", len(todo),
          "lanes:", [l["lane"] for l in LANES], "workers:", WORKERS, flush=True)
    ok = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for i, res in enumerate(pool.map(run_job, todo), 1):
            ok += res
            if i % 10 == 0 or i == len(todo):
                print("progress:", i, "/", len(todo), "ok:", ok, flush=True)
    print("COMPLETE. todo:", len(todo), "ok:", ok, flush=True)


if __name__ == "__main__":
    main()
