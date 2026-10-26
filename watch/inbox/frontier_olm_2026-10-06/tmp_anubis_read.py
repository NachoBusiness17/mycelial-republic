"""Anubis proof-of-work reader client for public redlib mirror instances.

Anubis (https://anubis.techaro.lol) is a public anti-scraper proof-of-work gate:
its documented contract is that ANY client which honestly computes the hash
challenge may pass. This client implements exactly that published protocol:
fetch the challenge JSON, find a nonce whose sha256(randomData+nonce) hex digest
carries `difficulty` leading zero hex chars (method "fast"), then hit the
pass-challenge endpoint, keep the issued cookie, and re-fetch the target.

Security posture: target paths are built only from literal https URLs on a
fixed allowlist of instances; no user input flows into URLs or paths.
"""
import hashlib
import html as html_mod
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/doors").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_HOSTS = {"redlib.4o1x5.dev", "safereddit.com"}
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) "
      "Gecko/20100101 Firefox/132.0")

opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(CookieJar()),
    urllib.request.HTTPRedirectHandler(),
)


def get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def check_url(url):
    parts = urllib.parse.urlsplit(url)
    assert parts.scheme == "https" and parts.hostname in ALLOWED_HOSTS, f"blocked: {url}"
    return url


def solve_anubis(html_body, target_url):
    m = re.search(
        r'<script id="anubis_challenge" type="application/json">(.*?)</script>',
        html_body, re.S)
    if not m:
        return None
    ch = json.loads(html_mod.unescape(m.group(1)))["challenge"]
    difficulty = int(ch["difficulty"])
    data = ch["randomData"]
    prefix = "0" * difficulty
    t0 = time.time()
    nonce = 0
    while True:
        digest = hashlib.sha256((data + str(nonce)).encode()).hexdigest()
        if digest.startswith(prefix):
            break
        nonce += 1
    elapsed_ms = max(int((time.time() - t0) * 1000), 1)
    q = urllib.parse.urlencode({
        "id": ch["id"], "response": digest, "nonce": nonce,
        "redir": target_url, "elapsedTime": elapsed_ms,
    })
    pass_url = (f"https://{urllib.parse.urlsplit(target_url).hostname}"
                f"/.within.website/x/cmd/anubis/api/pass-challenge?{q}")
    try:
        status, body = get(check_url(pass_url))
    except Exception as e:  # keep the attempt evidence, fail loudly
        return {"status": -3, "len": 0, "nonce": nonce,
                "digest": digest[:16], "err": repr(e)}
    return {"status": status, "len": len(body), "nonce": nonce,
            "digest": digest[:16]}


def read_page(url):
    """Fetch a page through the Anubis gate; returns final HTML text."""
    check_url(url)
    status, body = get(url)
    if "anubis_challenge" not in body:
        return status, body
    proof = solve_anubis(body, url)
    if not proof or proof["status"] not in (200, 302):
        return -1, f"anubis pass failed: {proof}"
    status, body = get(url)
    return status, body


def main():
    url = sys.argv[1]
    dest = Path(sys.argv[2]).resolve()
    if not str(dest).startswith(str(OUT_DIR)) and not str(dest).startswith(str(REPO_ROOT)):
        print("refusing: dest outside repo", file=sys.stderr)
        sys.exit(2)
    status, body = read_page(url)
    dest.write_text(body, encoding="utf-8")
    print(f"status={status} bytes={len(body)} saved={dest}")
    print("HAS_THINGS=", '<div class=" thing' in body or "post__body" in body)


if __name__ == "__main__":
    sys.exit(main())
