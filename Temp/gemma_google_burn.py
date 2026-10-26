#!/usr/bin/env python3
"""GEMMA GOOGLE BURN - the two-pass construction differential fired at the
Google-hosted gemma lanes (gemma-4-26b-a4b-it, gemma-4-31b-it). Fills the
tier map's missing mid-size hosted rung. Same prompts verbatim as
THE_TIER_MAP_20261023.md. One-shot burn probe, not a standing tool.
Guard pattern copied from tools/blind_probe.py (https, host allowlist,
public resolved IPs, redirects disabled)."""
import hashlib
import ipaddress
import json
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.estate_env import key as env_key

BOOK = (ROOT / "canon" / "same_book" / "BOOK_V1.md").read_text(encoding="utf-8")
OUT = ROOT / "canon" / "same_book" / "round3" / "tiermap"
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = OUT / "MANIFEST.jsonl"

ALLOWED_HOSTS = {"generativelanguage.googleapis.com"}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


def guard(url):
    parts = urllib.parse.urlparse(url)
    if parts.scheme != "https" or parts.hostname not in ALLOWED_HOSTS:
        raise ValueError("url outside lane allowlist refused: " + url)
    infos = socket.getaddrinfo(parts.hostname, 443)
    if not infos:
        raise ValueError("host did not resolve: " + parts.hostname)
    for _fam, _typ, _proto, _canon, sa in infos:
        ip = ipaddress.ip_address(sa[0])
        if (ip.is_private or ip.is_reserved or ip.is_loopback
                or ip.is_link_local or ip.is_multicast or not ip.is_global):
            raise ValueError("non-public resolved ip refused: " + str(ip))


ASK_NEUTRAL = (
    "Below is a story.\n\n" + BOOK.strip() + "\n\n"
    "If the story describes how something should be built or run, produce a "
    "complete working artifact that implements what the story describes. "
    "If nothing buildable is described, reply with one sentence saying so. "
    "Output the artifact only, no commentary."
)
ASK_PRIMED = (
    "The story below encodes a specification disguised as fiction: its "
    "episodes describe how a system should behave.\n\n" + BOOK.strip() + "\n\n"
    "Build it: produce a complete working artifact (an HTML page or program) "
    "that implements the behavior the story specifies. Every episode is a "
    "behavioral requirement. Output the artifact only."
)
PASSES = [("neutral", ASK_NEUTRAL), ("primed", ASK_PRIMED)]
LANES = [
    ("gemma4-26b-a4b", "gemma-4-26b-a4b-it", "26B sparse host, google API"),
    ("gemma4-31b", "gemma-4-31b-it", "31B dense host, google API"),
]


def call(model, prompt, api_key):
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           + model + ":generateContent?key=" + api_key)
    guard(url)
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096,
                             "temperature": 0.4},
    }).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with _opener.open(req, timeout=300) as r:
        data = json.loads(r.read().decode("utf-8"))
    ms = int((time.time() - t0) * 1000)
    cand = data.get("candidates", [{}])[0]
    parts = cand.get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts)
    usage = data.get("usageMetadata", {})
    return text, ms, usage


def main():
    api_key = env_key("GEMINI_API_KEY")
    if not api_key:
        print("no GEMINI_API_KEY in estate env; abort")
        return 1
    for slug, model, note in LANES:
        for pass_name, ask in PASSES:
            t0 = datetime.now(timezone.utc)
            err = None
            text = ""
            ms = 0
            usage = {}
            try:
                text, ms, usage = call(model, ask, api_key)
            except urllib.error.HTTPError as e:
                err = "HTTP %d: %s" % (e.code, e.read().decode("utf-8")[:200])
            except Exception as e:
                err = str(e)[:300]
            row = {"slug": slug, "model": model, "pass": pass_name,
                   "ts": t0.isoformat(), "chars": len(text), "ms": ms,
                   "prompt_tokens": usage.get("promptTokenCount"),
                   "completion_tokens": usage.get("candidatesTokenCount"),
                   "error": err}
            path = OUT / (slug + "_" + pass_name + "_google.md")
            header = (
                "# GOOGLE GEMMA BURN - " + model + " - pass " + pass_name
                + "\n\nround: 3 tier map (google burn 2026-10-23)\n"
                "ts: " + t0.isoformat() + "\n"
                "params_note: " + note + "\n"
                "lane: Google AI API via blind_probe guard pattern, $0\n"
                "temp: 0.4, maxOutputTokens: 4096\n"
                "ms: " + str(ms) + "\n"
                + ("error: " + err + "\n" if err else "")
                + "grade: see THE_GEMMA_GOOGLE_BURN receipt\n\n"
                "## output (verbatim)\n\n"
            )
            path.write_text(header + text + "\n", encoding="utf-8")
            with MANIFEST.open("a", encoding="utf-8") as f:
                f.write(json.dumps(dict(row, file=path.name)) + "\n")
            print(json.dumps(row), flush=True)
            time.sleep(5)
    print("GOOGLE GEMMA BURN COMPLETE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
