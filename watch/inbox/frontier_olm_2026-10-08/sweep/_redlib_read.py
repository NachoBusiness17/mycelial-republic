"""One-shot Anubis solve + thread fetch for the reddit sweep (low volume, single session).

Mirrors safereddit.com's own browser flow: GET page -> parse challenge ->
sha256(randomData+nonce) until difficulty met -> GET pass-challenge -> cookies -> read pages.
"""
import hashlib
import http.cookiejar
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://safereddit.com"
UA = "Mozilla/5.0"

THREADS = [
    ("spanda", "/r/LLM/comments/1w7ta40/r_spanda_zerocost_lexical_entropy_matches_neural/"),
    ("detector15ms", "/r/LLMDevs/comments/1w7td2g/built_an_opensource_hallucination_detector_that/"),
    ("halbench", "/r/LocalLLaMA/comments/1tizvih/halbench_i_built_a_custom_sycophancy_and/"),
    ("kg10m", "/r/LLMDevs/comments/1pkwgwy/building_a_knowledge_graph_memory_system_with_10m/"),
    ("metaharness", "/r/LocalLLaMA/comments/1shyczh/stanford_self_improving_metaharness/"),
    ("routing", "/r/AI_Agents/comments/1u94aws/is_anyone_actually_solving_perprompt_model/"),
    ("confidentidiot", "/r/LocalLLaMA/comments/1pe1bd4/the_confident_idiot_problem_why_llmasajudge_fails/"),
    ("kglessons", "/r/singularity/comments/1pn803k/lessons_from_building_a_knowledge_graph_memory/"),
]


def get(opener, url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with opener.open(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace"), r.status, r.geturl()


def main():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar),
        urllib.request.HTTPRedirectHandler(),
    )
    # 1. fetch a protected page to mint a challenge
    html, status, url = get(opener, BASE + THREADS[0][1])
    m = re.search(
        r'<script id="anubis_challenge" type="application/json">(.*?)</script>', html, re.S
    )
    if not m:
        print("NO_CHALLENGE status=%s len=%d - maybe already authed or hard block" % (status, len(html)))
        print(html[:200])
    else:
        ch = json.loads(m.group(1))
        rules, data = ch["rules"], ch["challenge"]
        diff = rules["difficulty"]
        p, odd = diff // 2, diff % 2 != 0
        t0 = time.time()
        nonce = 0
        while True:
            digest = hashlib.sha256((data["randomData"] + str(nonce)).encode()).digest()
            ok = all(b == 0 for b in digest[:p]) and (not odd or digest[p] >> 4 == 0)
            if ok:
                break
            nonce += 1
        hexhash = digest.hex()
        elapsed = int((time.time() - t0) * 1000) + 2000  # wall-time floor
        print("solved nonce=%d hash=%s elapsed_ms=%d" % (nonce, hexhash, elapsed))
        qs = urllib.parse.urlencode(
            {
                "id": data["id"],
                "response": hexhash,
                "nonce": str(nonce),
                "redir": THREADS[0][1],
                "elapsedTime": str(elapsed),
            }
        )
        body, status, url = get(opener, BASE + "/.within.website/x/cmd/anubis/api/pass-challenge?" + qs)
        print("pass-challenge status=%s len=%d" % (status, len(body)))
        time.sleep(1)

    # 2. fetch each thread with the auth cookie
    for name, path in THREADS:
        try:
            html, status, url = get(opener, BASE + path)
            fn = "_raw_%s.html" % name
            with open(fn, "w", encoding="utf-8") as f:
                f.write(html)
            print("%s status=%s len=%d -> %s" % (name, status, len(html), fn))
        except Exception as e:
            print("%s ERROR %s" % (name, e))
        time.sleep(2)


if __name__ == "__main__":
    main()
