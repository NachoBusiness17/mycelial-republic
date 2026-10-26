"""cry_mine - the demand-side frontier mine (operator idea, 2026-10-05:
"mine cries for help like this to enhance our functionality to
anticipate problems test them sort of like frontier mining. feature
requests").

The self-steal map (built on ribs, not beside them):
- frontier-mine (skill): the twin this completes - research finds ->
  steal-map onto organs; cry-mine: USER DISTRESS -> failure classes ->
  estate mirrors + anticipated-problem defenses. Same cadence law:
  intake without a cadence dies silently.
- social_rsi: the INTERNAL failure miner (lane trails -> patterns).
  cry-mine is its external input: real users' pain, classed into the
  same kind of taxonomy, and the two ledgers can be joined later
  (a class that fires both inside and outside is load-bearing).
- the X-intel pipeline: tri-state honesty (byte-visible vs inferred),
  receipts, append-only ledger - reused verbatim.
- the battery doctrine: every mined class owes a DEFENSE row - which
  estate organ already cures it (mirror) or which gap it names. A cry
  class with no mirror+defense is an UNANTICIPATED problem: that is the
  feature request, demand-verified.

v0 scope: X drops via the fxtwitter door (the operator's standing
pattern) + HN Algolia (keyless). Reddit .json + GitHub issues are v0.1
doors. Classification is DETERMINISTIC (keyword/shape rules) - LLM
classification climbs to the frontier tier only when the class space
proves too fuzzy for rules (descent protocol, cheap first).

Usage:
  python tools/cry_mine.py tweet <url> [--note ...]   # ingest one X cry
  python tools/cry_mine.py hn <query>                 # sweep HN Algolia
  python tools/cry_mine.py report                     # the mine readout
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LEDGER = ROOT / "memory" / "cry_mine" / "cries.jsonl"
SCHEMA = "cry.mine.v1"

# -- the failure-class taxonomy (v1, grown from real cries; extend by
# evidence, never by imagination) -------------------------------------------

CLASSES: dict[str, dict] = {
    "quota_wall": {
        "needles": ["usage limit", "out of usage", "cant use my extra usage",
                    "can't use my extra usage", "rate limit", "quota",
                    "hit the limit", "usage exhausted", "resets in"],
        "mirror": "the tier ladder + free-lane fleet (escape hatches the "
                  "consumer does not have); kit: local model = no billing clock",
    },
    "file_egress": {
        "needles": ["file off its computer", "get my file", "download the file",
                    "cant download", "can't download", "file from the agent",
                    "export my", "cant export", "can't export", "get the files"],
        "mirror": "kit law: the agent runs where the files already live - "
                  "no egress problem exists locally (README motivation row)",
    },
    "context_loss": {
        "needles": ["forgot what", "lost context", "does not remember",
                    "doesn't remember", "lost the thread", "context window",
                    "amnesia", "start over"],
        "mirror": "warm_state + verkle chain + MCP-lattice pull-over-dump",
    },
    "auth_loop": {
        "needles": ["login loop", "cant sign in", "can't sign in", "401",
                    "403", "api key", "auth", "token expired", "sso"],
        "mirror": "kit_doctor env-key law + the estate's key-failover ribs",
    },
    "billing_trap": {
        "needles": ["charged", "billing", "invoice", "refund", "subscription",
                    "credits", "paywall"],
        "mirror": "vendor-meter reconciliation + the $/day cap proofs",
    },
    "model_regression": {
        "needles": ["got worse", "dumber", "regression", "used to work",
                    "model update", "silent downgrade"],
        "mirror": "GPS capability ledger + metabolism (drift measured, "
                  "dispute streaks demote)",
    },
    "setup_fail": {
        "needles": ["cant install", "can't install", "setup", "wont start",
                    "won't start", "error on boot", "configure", "docker"],
        "mirror": "kit INSTALL ladder + kit_doctor + law_gate",
    },
    "data_lockin": {
        "needles": ["my data", "takeout", "export all", "locked in",
                    "delete my account"],
        "mirror": "append-only + jsonl-everywhere: the estate's files are "
                  "always the user's files",
    },
}


def classify(text: str) -> list[str]:
    """Deterministic class assignment: every class whose needles hit."""
    t = (text or "").lower()
    hits = []
    for name, spec in CLASSES.items():
        if any(n in t for n in spec["needles"]):
            hits.append(name)
    return hits


# -- ledger -------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def _append(row: dict) -> dict:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def _dedupe_key(row: dict) -> str:
    return str(row.get("source_url") or row.get("source_id") or row.get("text", "")[:80])


def ingest(*, text: str, source: str, source_url: str | None = None,
           author: str | None = None, note: str = "",
           inferred_extra: str = "") -> dict:
    """Ingest one cry. text = the BYTE-VISIBLE words only; anything we
    inferred beyond them rides inferred_extra (the tri-state law: never
    let inference masquerade as bytes)."""
    seen = {_dedupe_key(r) for r in _load()}
    key = source_url or f"{source}:{text[:80]}"
    if key in seen:
        return {"ok": False, "error": "duplicate cry (source already banked)"}
    classes = classify(text + " " + note)
    row = {
        "schema": SCHEMA, "ts": _now(), "source": source,
        "source_url": source_url, "author": author,
        "text": text[:500], "classes": classes,
        "note": note[:200], "inferred_extra": inferred_extra[:300],
    }
    _append(row)
    return {"ok": True, "row": row}


# -- sources ------------------------------------------------------------------

# SSRF door law (Mimosa L2 cure, 2026-10-05): every outbound fetch goes
# through _guarded_get - https only, HOST ALLOWLIST only (the two public
# APIs this tool is built on; no user-controlled host exists, so allowlist
# beats IP-range plumbing), redirects refused (the estate's _NoRedirect
# precedent, mag/lane_runner.py). A URL outside the fence raises before
# any socket opens.
_ALLOWED_HOSTS = frozenset({"api.fxtwitter.com", "hn.algolia.com"})


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # noqa: ANN002, ANN003
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _guarded_get(url: str, timeout: int = 30):
    from urllib.parse import urlparse

    p = urlparse(url)
    if p.scheme != "https":
        raise ValueError(f"cry-mine fetch refused: scheme {p.scheme!r} (https only)")
    if p.hostname not in _ALLOWED_HOSTS:
        raise ValueError(f"cry-mine fetch refused: host {p.hostname!r} not allowlisted")
    req = urllib.request.Request(url, headers={"User-Agent": "cry-mine/0.1"})
    return _OPENER.open(req, timeout=timeout)


def fetch_tweet(url: str) -> dict:
    """The fxtwitter door (standing pattern; sequential only - parallel
    bursts socket-fail, the rate note)."""
    m = re.search(r"(\w+)/status/(\d+)", url)
    if not m:
        return {"ok": False, "error": "not a status url"}
    api = f"https://api.fxtwitter.com/{m.group(1)}/status/{m.group(2)}"
    with _guarded_get(api) as r:
        d = json.loads(r.read().decode("utf-8", errors="ignore"))
    t = d.get("tweet", {})
    text = t.get("text") or ""
    if not text:
        return {"ok": False, "error": "no text (deleted or gated)"}
    return {"ok": True, "text": text, "author": t.get("author", {}).get("screen_name"),
            "url": f"https://x.com/{t.get('author', {}).get('screen_name')}/status/{m.group(2)}"}


def sweep_hn(query: str, cap: int = 20) -> list[dict]:
    """HN Algolia search (keyless, primary-adjacent: the API is HN's own).
    Returns candidate cries; the CALLER ingests what classifies."""
    api = ("https://hn.algolia.com/api/v1/search?query="
           + urllib.request.quote(query) + f"&tags=comment&hitsPerPage={cap}")
    with _guarded_get(api) as r:
        d = json.loads(r.read().decode("utf-8", errors="ignore"))
    out = []
    for hit in d.get("hits", []):
        txt = hit.get("comment_text") or hit.get("story_text") or ""
        out.append({"text": txt, "source": "hn",
                    "source_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "author": hit.get("author")})
    return out


# -- report -------------------------------------------------------------------


def report() -> str:
    rows = _load()
    by_class: dict[str, list[dict]] = {}
    unclassed = 0
    for r in rows:
        cs = r.get("classes") or []
        if not cs:
            unclassed += 1
        for c in cs:
            by_class.setdefault(c, []).append(r)
    lines = [f"CRY MINE: {len(rows)} cries banked, {len(by_class)} classes live, "
             f"{unclassed} unclassed (taxonomy gap = extend by evidence)"]
    ranked = sorted(by_class.items(), key=lambda kv: -len(kv[1]))
    for name, rs in ranked:
        spec = CLASSES.get(name, {})
        mirror = spec.get("mirror", "NO MIRROR NAMED")
        # the defense row: a class with a mirror AND a banked test/gap row is
        # anticipated; mirror-only means the claim is unproven
        lines.append(f"  {name:18s} x{len(rs)}  mirror: {mirror}")
    if ranked:
        lines.append("")
        lines.append("FEATURE REQUESTS (demand-verified, ranked by cry volume):")
        for name, rs in ranked:
            spec = CLASSES.get(name, {})
            if not spec.get("mirror"):
                lines.append(f"  {name}: {len(rs)} cries, NO estate mirror - this is the ask")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="cry_mine", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("tweet"); p.add_argument("url"); p.add_argument("--note", default="")
    p = sub.add_parser("hn"); p.add_argument("query"); p.add_argument("--cap", type=int, default=20)
    sub.add_parser("report")
    args = ap.parse_args(argv)
    if args.cmd == "tweet":
        t = fetch_tweet(args.url)
        if not t.get("ok"):
            print(t.get("error"))
            return 1
        r = ingest(text=t["text"], source="x", source_url=t["url"],
                   author=t.get("author"), note=args.note)
        print(json.dumps(r, ensure_ascii=False, indent=1)[:400])
        return 0 if r.get("ok") else 1
    if args.cmd == "hn":
        got = sweep_hn(args.query, args.cap)
        banked = skipped = 0
        for c in got:
            if not classify(c["text"]):
                skipped += 1
                continue
            r = ingest(text=c["text"], source="hn", source_url=c["source_url"],
                       author=c.get("author"),
                       note=f"query={args.query!r}")
            banked += 1 if r.get("ok") else 0
        print(f"HN sweep {args.query!r}: {len(got)} hits, {banked} cries banked, "
              f"{skipped} not distress-shaped (skipped honestly)")
        return 0
    if args.cmd == "report":
        print(report())
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
