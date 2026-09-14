"""link_library — canonical URL registry so filed links stop duplicating.

The problem it kills: the same X post arrives as five different URLs
(?s=20 tracking params, t.co wrappers, mobile hosts) and each variant used
to become its own INTAKE_* file. Duplication is emphasis for humans; for
the ledger it is drift.

Canonicalization (v1):
  - lowercase scheme+host, strip default port, drop fragment
  - strip tracking params: s, si, utm_*, ref_src, ref_url, t, cn, mx, igsh, fbclid, gclid
  - sort remaining query params, drop empty values
  - x.com/twitter.com collapse to x.com; mobile.*/m.* hosts collapse to canonical host
  - drop trailing slash on empty path

Ledger: watch/inbox/LINKS.jsonl (append-only, one JSON object per line):
  {"seq", "ts", "canonical", "url", "canonical_sha256", "title", "duplicate_of", "writer", "note"}

CLI:
  python -m mag.link_library add URL [URL ...] [--note NOTE] [--writer WRITER]
  python -m mag.link_library check URL        # exit 1 if canonical already known
  python -m mag.link_library dupes            # show duplicate canonicals on file
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "watch" / "inbox" / "LINKS.jsonl"

TRACKING_PARAMS = {
    "s", "si", "t", "cn", "mx", "igsh", "fbclid", "gclid", "ref_src", "ref_url",
    "ref", "source", "cmpid", "sgt", "sh", "hsmi", "hsenc", "mc_cid", "mc_eid",
}
HOST_COLLAPSE = {
    "twitter.com": "x.com",
    "mobile.x.com": "x.com",
    "m.x.com": "x.com",
}


def canonicalize(url: str) -> str:
    url = url.strip()
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"only http/https allowed: {url!r}")
    host = parsed.netloc.lower()
    if "@" in host:  # strip userinfo, never valid in filed links
        host = host.rsplit("@", 1)[1]
    if ":" in host:
        host, port = host.rsplit(":", 1)
        if port == ("443" if parsed.scheme == "https" else "80"):
            pass
        else:
            host = f"{host}:{port}"
    host = HOST_COLLAPSE.get(host, host)
    path = parsed.path.rstrip("/") if parsed.path.rstrip("/") == "" or parsed.path.endswith("/") else parsed.path
    params = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=False)
              if k.lower() not in TRACKING_PARAMS and not k.lower().startswith("utm_")]
    params.sort()
    query = urlencode(params)
    return urlunparse((parsed.scheme, host, path, "", query, ""))


def canonical_sha256(canonical: str) -> str:
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def load_ledger() -> list[dict]:
    if not LEDGER.is_file():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def known_canonicals() -> dict[str, dict]:
    return {e["canonical"]: e for e in load_ledger() if e.get("canonical")}


def validate_host_safety(url: str) -> None:
    """Mimosa guard: http/https only; refuse localhost/loopback/private/reserved."""
    host = urlparse(url).hostname or ""
    if not host:
        raise ValueError(f"no host: {url!r}")
    if host in ("localhost",) or host.endswith(".local") or host.endswith(".internal"):
        raise ValueError(f"refusing local host: {host}")
    if re.match(r"^(10\.|127\.|0\.|169\.254\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)", host):
        raise ValueError(f"refusing private/reserved host: {host}")
    if host in ("metadata.google.internal", "169.254.169.254"):
        raise ValueError(f"refusing metadata host: {host}")


def add_urls(urls: list[str], note: str = "", writer: str = "link_library") -> list[dict]:
    known = known_canonicals()
    results = []
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as handle:
        for url in urls:
            validate_host_safety(url)
            canon = canonicalize(url)
            sha = canonical_sha256(canon)
            entry = {
                "seq": int(time.time() * 1000_000) + len(results),
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
                "canonical": canon,
                "url": url,
                "canonical_sha256": sha,
                "title": "",
                "duplicate_of": "",
                "writer": writer,
                "note": note,
            }
            if canon in known:
                entry["duplicate_of"] = known[canon].get("url", canon)
            known[canon] = entry
            handle.write(json.dumps(entry) + "\n")
            results.append(entry)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m mag.link_library")
    parser.add_argument("command", choices=("add", "check", "dupes"))
    parser.add_argument("urls", nargs="*")
    parser.add_argument("--note", default="")
    parser.add_argument("--writer", default="link_library")
    args = parser.parse_args()

    if args.command == "add":
        if not args.urls:
            parser.error("add requires at least one URL")
        for entry in add_urls(args.urls, note=args.note, writer=args.writer):
            flag = "DUPLICATE" if entry["duplicate_of"] else "REGISTERED"
            print(f"{flag}: {entry['canonical']}")
        return 0
    if args.command == "check":
        if len(args.urls) != 1:
            parser.error("check requires exactly one URL")
        validate_host_safety(args.urls[0])
        canon = canonicalize(args.urls[0])
        hit = known_canonicals().get(canon)
        print(json.dumps({"canonical": canon, "known": bool(hit), "first_entry": hit}, indent=1))
        return 1 if hit else 0
    if args.command == "dupes":
        seen: dict[str, str] = {}
        dupes = 0
        for entry in load_ledger():
            if entry.get("duplicate_of"):
                dupes += 1
                print(f"{entry['url']}  ->  {entry['duplicate_of']}")
        print(f"{dupes} duplicate submissions on file")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
