"""BLIND PROBE — the differential sensor array as a standing organ.

Method (BLIND_DIFFERENTIAL_METHOD_20260921): one blind prompt, N free lanes,
the delta is the finding, nuance routed. This tool runs a probe, files it as
md (rib.md.record.v1: prompt filed at dispatch), and keeps arena-style Elo per
lane per category (Chatbot Arena steal) for pairwise judgments.

Commands:
  probe <category> "<prompt>"   fire one blind probe at the free lanes
  judge <probe_id> <lane>       record a judgment (operator or judge lane);
                                updates Elo (K=32, base 1500)
  matrix                        render probes x lanes summary

Lanes (free tiers, keys from .env): groq (llama-3.3-70b), gemini
(gemini-2.0-flash), mistral (mistral-small-latest). A lane that errors is
filed DARK — that is a finding too.

Safety: https only; exact host allowlist; every resolved IP must be public;
redirects disabled (SSRF guard — protocol, host, and resolved-IP boundaries).
"""

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

NOW = datetime.now(timezone.utc)
ROOT = Path.cwd().resolve()
PROBES = ROOT / "watch" / "inbox" / "probes"
PROBES.mkdir(parents=True, exist_ok=True)
ELO = PROBES / "elo.json"
K = 32
BASE = 1500.0

ALLOWED_HOSTS = {"api.groq.com", "api.mistral.ai",
                 "generativelanguage.googleapis.com"}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


def guard(url):
    """https + allowlisted host + every resolved IP public. Refuse otherwise."""
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


def open_guarded(req, timeout):
    try:
        return _opener.open(req, timeout=timeout)
    except urllib.error.HTTPError:
        raise  # real API status — surface it
    except urllib.error.URLError as e:
        raise ValueError("blocked by guard (redirect/connection): " + str(e))


def env_key(name):
    from tools.estate_env import key  # the one canonical loader — no pretending
    return key(name)


def call_lane(lane, key, prompt):
    if lane == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        body = json.dumps({"model": "openai/gpt-oss-120b",
                           "messages": [{"role": "user", "content": prompt}],
                           "max_tokens": 300}).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    elif lane == "mistral":
        url = "https://api.mistral.ai/v1/chat/completions"
        body = json.dumps({"model": "mistral-small-latest",
                           "messages": [{"role": "user", "content": prompt}],
                           "max_tokens": 300}).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    elif lane == "gemini":
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               "gemini-flash-latest:generateContent?key=" + key)
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                           "generationConfig": {"maxOutputTokens": 300}}).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json"})
    else:
        raise ValueError("unknown lane " + lane)
    guard(url)
    t0 = time.time()
    with open_guarded(req, timeout=45) as r:
        data = json.loads(r.read().decode("utf-8"))
    ms = int((time.time() - t0) * 1000)
    if lane == "gemini":
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        text = data["choices"][0]["message"]["content"]
    return text.strip(), ms


LANE_KEYS = [("groq", "GROQ_API_KEY"), ("gemini", "GEMINI_API_KEY"),
             ("mistral", "MISTRAL_API_KEY")]


def load_elo():
    if ELO.exists():
        return json.loads(ELO.read_text(encoding="utf-8"))
    return {"schema": "blindprobe.elo.v1", "base": BASE, "K": K, "ratings": {},
            "matches": [], "probes": []}


def elo_get(elo, lane, cat):
    return elo["ratings"].get(cat, {}).get(lane, elo["base"])


def elo_pair(elo, cat, winner, loser):
    rw, rl = elo_get(elo, winner, cat), elo_get(elo, loser, cat)
    exp_w = 1 / (1 + 10 ** ((rl - rw) / 400))
    delta = round(elo["K"] * (1 - exp_w), 1)
    elo["ratings"].setdefault(cat, {})
    elo["ratings"][cat][winner] = round(rw + delta, 1)
    elo["ratings"][cat][loser] = round(rl - delta, 1)
    elo["matches"].append({"ts": NOW.isoformat(), "cat": cat,
                           "winner": winner, "loser": loser, "delta": delta})


def probe(cat, prompt):
    n = len(list(PROBES.glob("PROBE_*.md"))) + 1
    pid = "PROBE_%03d" % n
    prompt_sha = hashlib.sha256(prompt.encode()).hexdigest()[:16]
    lines = ["# " + pid + " — blind differential probe",
             "ts: " + NOW.isoformat() + "  ·  category: " + cat
             + "  ·  prompt_sha16: " + prompt_sha,
             "", "## prompt (filed at dispatch — prompt-of-record)", "",
             prompt, "", "## returns", ""]
    returns = {}
    for lane, keyname in LANE_KEYS:
        key = env_key(keyname)
        if not key:
            lines.append("### " + lane + "\n- DARK: no key in estate .env\n")
            returns[lane] = {"status": "DARK", "why": "no key"}
            continue
        try:
            text, ms = call_lane(lane, key, prompt)
            returns[lane] = {"status": "OK", "ms": ms, "chars": len(text)}
            lines.append("### " + lane + " — ok, " + str(ms) + " ms, "
                         + str(len(text)) + " chars\n")
            lines.append(text + "\n")
        except Exception as e:
            returns[lane] = {"status": "DARK", "why": str(e)[:140]}
            lines.append("### " + lane + "\n- DARK: " + str(e)[:140] + "\n")
    alive = sum(1 for r in returns.values() if r["status"] == "OK")
    lines += ["## delta notes", "",
              "- judgments: PENDING (operator or judge lane)",
              "- spread observed: " + str(alive) + "/" + str(len(returns))
              + " lanes alive", ""]
    p = PROBES / (pid + "_" + NOW.strftime("%Y%m%d") + ".md")
    p.write_text("\n".join(lines), encoding="utf-8")
    elo = load_elo()
    elo.setdefault("probes", []).append(
        {"id": pid, "ts": NOW.isoformat(), "cat": cat, "file": p.name,
         "prompt_sha16": prompt_sha, "returns": returns})
    ELO.write_text(json.dumps(elo, indent=2), encoding="utf-8")
    print("filed", p.name)
    for lane, r in returns.items():
        print("  %-8s %s  %s" % (lane, r["status"],
              (str(r.get("ms", "")) + " ms") if r["status"] == "OK"
              else r.get("why", "")))
    print("judgments PENDING — file with: blind_probe.py judge " + pid + " <lane>")


def judge(pid, lane):
    elo = load_elo()
    probe_row = next((p for p in elo.get("probes", []) if p["id"] == pid), None)
    if not probe_row:
        print("no such probe")
        return 1
    cat = probe_row["cat"]
    losers = [l for l, r in probe_row["returns"].items()
              if r["status"] == "OK" and l != lane]
    if not losers:
        print("no living opponent lane to pair against")
        return 1
    for loser in losers:
        elo_pair(elo, cat, lane, loser)
    ELO.write_text(json.dumps(elo, indent=2), encoding="utf-8")
    print("judged %s: %s over %s — elo: %s" % (pid, lane, losers,
          json.dumps(elo["ratings"].get(cat, {}))))
    return 0


def matrix():
    elo = load_elo()
    for p in elo.get("probes", []):
        alive = [l for l, r in p["returns"].items() if r["status"] == "OK"]
        print("%s %s cat=%-18s alive=%s" % (p["id"], p["ts"][:16], p["cat"],
                                            ",".join(alive)))
    if elo.get("ratings"):
        print("elo:", json.dumps(elo["ratings"]))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "probe" and len(sys.argv) >= 4:
        probe(sys.argv[2], sys.argv[3])
    elif cmd == "judge" and len(sys.argv) >= 4:
        sys.exit(judge(sys.argv[2], sys.argv[3]))
    elif cmd == "matrix":
        matrix()
    else:
        print(__doc__)
