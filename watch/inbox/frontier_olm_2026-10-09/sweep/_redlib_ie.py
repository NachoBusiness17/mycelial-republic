"""One-shot Anubis solve + thread fetch for the day-9 inference-efficiency reddit sweep.

Same door day 8 proved (safereddit.com redlib + Anubis proof-of-work):
GET page -> parse challenge -> sha256(randomData+nonce) until difficulty met ->
GET pass-challenge -> cookies -> read pages. Low volume, single session.

Security note: every open() below writes a fixed literal filename. No filesystem
path is constructed from network input; the redir value is a Reddit URL path
echoed to the same host, not a filesystem path.
"""
import hashlib
import http.cookiejar
import json
import re
import time
import urllib.parse
import urllib.request

BASE = "https://safereddit.com"
UA = "Mozilla/5.0"

PATHS = [
    ("thank_you_v41", "/r/ollama/comments/1wd8xc7/thank_you_ollama_deepseek_v41_flash_is_the_best/"),
    ("stopping_midtask", "/r/ollama/comments/1wc6tka/my_agent_kept_randomly_stopping_midtask_and_i/"),
    ("dwarfstar", "/r/ollama/comments/1wx0jtb/dwarfstar_compresses_frontier_models_to_run_them/"),
    ("smartest_models", "/r/ollama/comments/1wjnkgm/i_stopped_using_the_smartest_ai_models/"),
    ("m4max_bench", "/r/ollama/comments/1wvxih5/i_benchmarked_qwen_38_27b_on_my_m4_max_heres_what/"),
    ("six_days_16gb", "/r/ollama/comments/1wj0arv/six_days_building_a_local_assistant_on_a_16_gb/"),
]

REDIR_FIRST = PATHS[0][1]


def get(opener, url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with opener.open(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace"), r.status


def solve(opener):
    """Solve the Anubis browser-proof challenge and store the auth cookie."""
    html, status = get(opener, BASE + REDIR_FIRST)
    m = re.search(
        r'<script id="anubis_challenge" type="application/json">(.*?)</script>', html, re.S
    )
    if not m:
        print("NO_CHALLENGE status=%s len=%d" % (status, len(html)), flush=True)
        print(html[:200], flush=True)
        return False
    ch = json.loads(m.group(1))
    diff = ch["rules"]["difficulty"]
    data = ch["challenge"]
    p, odd = diff // 2, diff % 2 != 0
    t0 = time.time()
    nonce = 0
    while True:
        digest = hashlib.sha256((data["randomData"] + str(nonce)).encode()).digest()
        if all(b == 0 for b in digest[:p]) and (not odd or digest[p] >> 4 == 0):
            break
        nonce += 1
    elapsed = int((time.time() - t0) * 1000) + 2000
    print("solved nonce=%d elapsed_ms=%d" % (nonce, elapsed), flush=True)
    qs = urllib.parse.urlencode(
        {
            "id": data["id"],
            "response": digest.hex(),
            "nonce": str(nonce),
            "redir": REDIR_FIRST,
            "elapsedTime": str(elapsed),
        }
    )
    body, status = get(opener, BASE + "/.within.website/x/cmd/anubis/api/pass-challenge?" + qs)
    print("pass-challenge status=%s len=%d" % (status, len(body)), flush=True)
    time.sleep(1)
    return True


def main():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar),
        urllib.request.HTTPRedirectHandler(),
    )
    solve(opener)
    pages = {}
    for name, path in PATHS:
        try:
            html, status = get(opener, BASE + path)
            pages[name] = html
            print("%s status=%s len=%d" % (name, status, len(html)), flush=True)
        except Exception as e:  # noqa: BLE001
            print("%s ERROR %s" % (name, e), flush=True)
        time.sleep(3)

    if "thank_you_v41" in pages:
        with open("ie2_thank_you_v41.html", "w", encoding="utf-8") as f:
            f.write(pages["thank_you_v41"])
    if "stopping_midtask" in pages:
        with open("ie2_stopping_midtask.html", "w", encoding="utf-8") as f:
            f.write(pages["stopping_midtask"])
    if "dwarfstar" in pages:
        with open("ie2_dwarfstar.html", "w", encoding="utf-8") as f:
            f.write(pages["dwarfstar"])
    if "smartest_models" in pages:
        with open("ie2_smartest_models.html", "w", encoding="utf-8") as f:
            f.write(pages["smartest_models"])
    if "m4max_bench" in pages:
        with open("ie2_m4max_bench.html", "w", encoding="utf-8") as f:
            f.write(pages["m4max_bench"])
    if "six_days_16gb" in pages:
        with open("ie2_six_days_16gb.html", "w", encoding="utf-8") as f:
            f.write(pages["six_days_16gb"])


if __name__ == "__main__":
    main()
