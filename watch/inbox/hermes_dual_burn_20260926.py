import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

sys.path.insert(0, os.getcwd())
from models.env_load import load_dotenv  # noqa: E402

load_dotenv()

ALLOWED_HOST = "inference-api.nousresearch.com"
BASE = "https://" + ALLOWED_HOST + "/v1"
KEYS = [k for k in (os.environ.get("HERMES_API_KEY_1"), os.environ.get("HERMES_API_KEY_2")) if k]
MODELS = ["z-ai/glm-5.3-prime", "qwen/qwen3.8-max-prime", "fireworks/ember-1"]
OUT_FILE = "logs/hermes_dual_20260926/output.jsonl"
ASK_TAIL = ("Extract the mechanic's concrete numbers (rates, curves, unlock gates, economy costs) "
 "from design wikis and patch notes, the retention hook it pulls, the abuse vector players found, "
 "and a clone-or-skip verdict for a Roblox-style lane that already runs VM currency + boon drafts "
 "+ faction war + shared-respawn Pilgrim class. Quote load-bearing lines verbatim with sources. "
 "Never fabricate: if you could not fetch a source, say OWED. No em-dashes. "
 "Format: NUMBERS / RETENTION HOOK / ABUSE VECTOR / CLONE-OR-SKIP / EVIDENCE / SOURCES.")
LAWS = "Never fabricate. No em-dashes."
JID_RE = re.compile(r"^[a-z0-9-]+$")


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
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
        raise ValueError("host not allowed: " + str(parsed.hostname))
    for info in socket.getaddrinfo(parsed.hostname, 443):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise ValueError("resolved to blocked address")
    return urllib.request.build_opener().open(req, timeout=timeout)


def call(model, prompt, key):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 8000, "temperature": 0.4}).encode("utf-8")
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with guarded_open(req, timeout=540) as r:
        return json.loads(r.read())


def main():
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    jobs = load_briefs()
    done = load_done()
    print("jobs:", len(jobs), "already done:", len(done), flush=True)
    ok = len(done)
    for idx, (jid, game, mech) in enumerate(jobs, 1):
        if not JID_RE.fullmatch(jid) or jid in done:
            continue
        prompt = ("GAME: " + game + "\nMECHANIC: " + mech + "\n\nTASK: " + ASK_TAIL + "\n\n" + LAWS)
        model = MODELS[idx % len(MODELS)]
        result = None
        for attempt in range(1, 6):
            key = KEYS[(attempt - 1) % len(KEYS)]
            try:
                d = call(model, prompt, key)
                content = d.get("choices", [{}])[0].get("message", {}).get("content", "")
                usage = d.get("usage", {})
                result = {"id": jid, "game": game, "mechanic": mech, "model": model,
                          "ok": True, "content": content,
                          "prompt_tokens": usage.get("prompt_tokens"),
                          "completion_tokens": usage.get("completion_tokens")}
                break
            except urllib.error.HTTPError as e:
                err = "HTTP " + str(e.code)
            except Exception as e:
                err = type(e).__name__ + ": " + str(e)[:120]
            with open(OUT_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps({"id": jid, "ok": False, "attempt": attempt, "error": err}) + "\n")
            time.sleep(30 * attempt)
            model = MODELS[(MODELS.index(model) + 1) % len(MODELS)]
        if result is not None:
            with open(OUT_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
            ok += 1
        if idx % 10 == 0 or idx == len(jobs):
            print("progress:", idx, "/", len(jobs), "ok:", ok, flush=True)
    print("COMPLETE. jobs:", len(jobs), "ok:", ok, flush=True)


if __name__ == "__main__":
    main()
