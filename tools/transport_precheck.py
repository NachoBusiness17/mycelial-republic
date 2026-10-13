#!/usr/bin/env python
"""transport_precheck.py — research-lane preflight transport check (B2-327).

Law: a research lane runs this on every named URL BEFORE its first model
attempt. After this gate exists, a lane must never again burn a paid model
attempt against a URL this precheck classifies 403/404 (the B2-74 death
class: pub.towardsai.net HTTP 403 bot-wall and stack-junkie.com unresolved,
both spent model attempts before the wall was discovered).

Classifier (the wall classes the B2-74/B2-16 deaths taught):
  ok              2xx and the body (when fetched) carries no interstitial marker
  bot-wall        403 (and 429 on a GET-only host): the wall class that killed
                  the strictly-2026 recipe sources
  dead            404/410: the exact-URL-unresolved class (UF-129/130/131
                  provider 404s)
  interstitial    2xx whose body carries a browser-verification marker
                  ("Just a moment", "Checking your browser", "cf-browser-...",
                  "Attention Required"): the URL answers but a model cannot
                  read it
  server-error    5xx
  unreachable     DNS failure, refused, timeout: no class beyond "the pipe
                  is down" (a lane may retry transport, never spend a model
                  attempt on it without a later ok)

Every check appends one journal row to logs/transport_precheck.jsonl
({ts, url, method, status, class, latency_ms, error}) so the lane receipt can
cite the precheck as the reason it skipped a source.

Usage:
    python tools/transport_precheck.py URL [URL ...]
    python tools/transport_precheck.py --selftest
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
JOURNAL = ESTATE_ROOT / "logs" / "transport_precheck.jsonl"
TIMEOUT_S = 12
UA = "Mozilla/5.0 (compatible; mag-transport-precheck/1; research-lane gate)"

INTERSTITIAL_MARKERS = (
    "just a moment",
    "checking your browser",
    "cf-browser-verification",
    "attention required",
    "enable javascript and cookies to continue",
    "verify you are a human",
)

WALL_CLASSES = {
    403: "bot-wall",
    429: "bot-wall",
    404: "dead",
    410: "dead",
}


def classify(status: int, body: str) -> str:
    if status in WALL_CLASSES:
        return WALL_CLASSES[status]
    if 500 <= status <= 599:
        return "server-error"
    low = (body or "").lower()
    if any(marker in low for marker in INTERSTITIAL_MARKERS):
        return "interstitial"
    if 200 <= status <= 299:
        return "ok"
    return f"http-{status}"


def _request(url: str, method: str, timeout: float):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout)


def precheck(url: str, timeout: float = TIMEOUT_S, journal: Path | None = None,
             fetch=None) -> dict:
    """Classify one URL's transport health. fetch is injectable for tests."""
    fetch = fetch or _probe
    t0 = time.monotonic()
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "url": url, "method": "", "status": None, "class": "",
           "latency_ms": None, "error": ""}
    try:
        method, status, body = fetch(url, timeout)
    except Exception as exc:  # transport-level failure, classified below
        row["latency_ms"] = int((time.monotonic() - t0) * 1000)
        row["error"] = f"{type(exc).__name__}: {exc}"[:200]
        row["class"] = "unreachable"
        _append(journal or JOURNAL, row)
        return row
    row["method"] = method
    row["status"] = status
    row["class"] = classify(status, body or "")
    row["latency_ms"] = int((time.monotonic() - t0) * 1000)
    _append(journal or JOURNAL, row)
    return row


def _probe(url: str, timeout: float):
    """HEAD first (bodies are wasted bytes); hosts that reject HEAD fall back
    to a range-limited GET so the interstitial markers stay checkable."""
    try:
        with _request(url, "HEAD", timeout) as r:
            return "HEAD", r.status, ""
    except urllib.error.HTTPError as e:
        if e.code in (403, 404, 410, 429):
            # the wall class is already decided by the status code alone
            return "HEAD", e.code, ""
        if e.code in (405, 400, 501) or 500 <= e.code:
            pass  # HEAD unsupported or server-side wobble: retry with GET
        else:
            raise
    except Exception:
        raise
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Range": "bytes=0-65535"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read(65536).decode("utf-8", "replace")
        return "GET", r.status, body


def _append(journal: Path, row: dict) -> None:
    try:
        journal.parent.mkdir(parents=True, exist_ok=True)
        with journal.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as e:
        # the gate must never fail because the journal is unwritable; the
        # named handler surfaces the loss instead of silently dropping it
        # (ratchet except-pass fix 2026-09-27)
        print(f"transport_precheck: journal unwritable, row not recorded: {e}",
              file=sys.stderr)


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    results = [precheck(url) for url in argv[1:]]
    print(json.dumps(results, ensure_ascii=False, indent=1))
    dead = [r for r in results if r["class"] in ("bot-wall", "dead", "interstitial",
                                                "unreachable", "server-error")]
    return 1 if dead else 0  # nonzero = do not spend model attempts on these


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
