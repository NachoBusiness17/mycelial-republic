"""PRICING DIFF CRON — cached-vs-compute token ratios across the four providers, daily.

Ask A6 (2026-09-22): fetch the public docs pricing pages of the four providers that
publish a cached/compute token split — Anthropic, OpenAI, Google (ai.google.dev),
DeepSeek — extract each flagship's cached price, compute (base input) price and their
ratio, and seal a daily dashboard to watch/inbox/pricing_ratios_YYYYMMDD.csv
(provider,cached_price,compute_price,ratio,source_url). Hugging Face's
inference-providers pricing docs are checked too but publish NO cached/compute split
(billed per-provider routing credits), so it is reported as excluded, not a row.
Prints a diff against the most recent previous pricing_ratios_*.csv if one exists.

Usage (repo root): .venv/Scripts/python.exe tools/pricing_diff.py
Schedule: cron-ready, one line in the estate's daily task (same pattern as
tools/meters_nightly.py); self-registers its CSV into watch/inbox/index_events.jsonl.

Egress law (Mimosa PreToolUse constraint, 2026-09-22): https only, host allowlist,
every resolved IP must be public (no loopback/private/link-local/metadata), and every
redirect hop is re-validated before being followed.
"""
from __future__ import annotations

import csv
import hashlib
import ipaddress
import json
import re
import socket
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "watch" / "inbox"
INDEX = INBOX / "index_events.jsonl"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%d")
OUT = INBOX / f"pricing_ratios_{STAMP}.csv"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) mag-estate-pricing-diff/1.0"
TIMEOUT = 30

ANTHROPIC_URL = "https://platform.claude.com/docs/en/about-claude/pricing"
OPENAI_URL = "https://developers.openai.com/api/docs/pricing"
GOOGLE_URL = "https://ai.google.dev/gemini-api/docs/pricing"
DEEPSEEK_URL = "https://api-docs.deepseek.com/quick_start/pricing"
HUGGINGFACE_URL = "https://huggingface.co/docs/inference-providers/pricing"

ALLOWED_HOSTS = {
    "docs.anthropic.com",  # legacy alias, 301s to platform.claude.com
    "platform.claude.com",
    "platform.openai.com",  # legacy alias, 301s to developers.openai.com
    "developers.openai.com",
    "ai.google.dev",
    "api-docs.deepseek.com",
    "huggingface.co",
}


def validate_url(url: str) -> str:
    """HTTPS + allowlisted host + every resolved IP public. Returns the hostname."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https":
        raise ValueError(f"blocked non-https URL: {url!r}")
    host = (parts.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"blocked non-allowlisted host: {host!r}")
    for info in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(info[4][0]).is_global:
            raise ValueError(f"blocked non-public resolved IP {info[4][0]} for {host}")
    return host


class _PinnedRedirect(urllib.request.HTTPRedirectHandler):
    """Re-validate every redirect hop against the same egress law."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_CTX = ssl.create_default_context()
_OPENER = urllib.request.build_opener(
    _PinnedRedirect,
    urllib.request.HTTPSHandler(context=_CTX),
)


def safe_get(url: str) -> str:
    """SSRF-guarded https GET of one allowlisted public docs page."""
    validate_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with _OPENER.open(req, timeout=TIMEOUT) as resp:
        if resp.status != 200:
            raise ValueError(f"HTTP {resp.status} from {url}")
        return resp.read().decode("utf-8", "replace")


def strip_tags(fragment: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", fragment.replace("<!-- -->", ""))
    return re.sub(r"\s+", " ", txt).strip()


def first_price(text: str) -> float:
    """First $amount in a cell/line — for 'through <date>' cells that is the current price."""
    m = re.search(r"\$\s*([0-9]+(?:\.[0-9]+)?)", text)
    if not m:
        raise ValueError(f"no $amount in {text[:80]!r}")
    return float(m.group(1))


def table_rows(table: str) -> list[list[str]]:
    rows = []
    for raw in re.findall(r"<tr.*?</tr>", table, re.S):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", raw, re.S)
        rows.append([strip_tags(c) for c in cells])
    return rows


# --------------------------------------------------------------------------
# extractors — each returns dict(model, cached, compute, source, note)
# rule: first listed current-generation flagship on the page, short-context/peak rates
# --------------------------------------------------------------------------
def ex_anthropic() -> dict:
    body = safe_get(ANTHROPIC_URL)
    table = next(t for t in re.findall(r"<table.*?</table>", body, re.S) if "Cache hits and refreshes" in t)
    for cells in table_rows(table):
        if len(cells) < 6 or cells[0].lower().startswith("model"):
            continue
        name = cells[0]
        if "retired" in name.lower() or "limited availability" in name.lower():
            continue
        return {
            "model": name,
            "cached": first_price(cells[4]),  # "Cache hits and refreshes"
            "compute": first_price(cells[1]),  # "Base input tokens"
            "source": ANTHROPIC_URL,
            "note": "cache-read vs base input, per MTok",
        }
    raise ValueError("anthropic: no eligible pricing row")


def ex_openai() -> dict:
    body = safe_get(OPENAI_URL)
    for table in re.findall(r"<table.*?</table>", body, re.S):
        if "Cached input" not in table:
            continue
        i_in = i_cached = None
        for cells in table_rows(table):
            low = [c.lower() for c in cells]
            if low and low[0] == "model":
                i_in = low.index("input")  # first = short context
                i_cached = low.index("cached input")
                continue
            if i_in is None or i_cached is None or len(cells) <= max(i_in, i_cached):
                continue
            return {
                "model": cells[0],
                "cached": first_price(cells[i_cached]),
                "compute": first_price(cells[i_in]),
                "source": OPENAI_URL,
                "note": "short context, first price table",
            }
    raise ValueError("openai: no table with Cached input column")


def ex_google() -> dict:
    body = safe_get(GOOGLE_URL)
    for section in re.split(r"<h2[^>]*>", body)[1:]:
        name = strip_tags(section.split("</h2>")[0])
        tm = re.search(r"<table.*?</table>", section, re.S)
        if not tm:
            continue
        input_price = cache_price = None
        for cells in table_rows(tm.group(0)):
            if len(cells) < 3:
                continue
            if cells[0] == "Input price" and input_price is None:
                input_price = first_price(cells[2])  # paid tier, current window
            if cells[0] == "Context caching price" and cache_price is None:
                cache_price = first_price(cells[2])  # first $ = cached token read
        if input_price is not None and cache_price is not None:
            return {
                "model": name,
                "cached": cache_price,
                "compute": input_price,
                "source": GOOGLE_URL,
                "note": "context caching read vs input, paid tier, per 1M tokens",
            }
    raise ValueError("google: no section with Input price + Context caching price")


def ex_deepseek() -> dict:
    body = safe_get(DEEPSEEK_URL)
    txt = re.sub(r"\s+", " ", strip_tags(re.sub(r"<script.*?</script>", "", body, flags=re.S)))
    # pricing block (not an HTML table): "1M INPUT TOKENS (CACHE HIT) OFF-PEAK $a $b PEAK $c $d"
    # price order: [col1-offpeak, col2-offpeak, col1-peak, col2-peak]; columns as listed:
    # "MODEL deepseek-flash ... deepseek-v4-pro" -> col 1 = deepseek-flash
    hit = re.search(
        r"1M INPUT TOKENS \(CACHE HIT\)\s*OFF-PEAK \$([0-9.]+) \$([0-9.]+) PEAK \$([0-9.]+) \$([0-9.]+)",
        txt,
        re.I,
    )
    miss = re.search(
        r"1M INPUT TOKENS \(CACHE MISS\)\s*OFF-PEAK \$([0-9.]+) \$([0-9.]+) PEAK \$([0-9.]+) \$([0-9.]+)",
        txt,
        re.I,
    )
    if not (hit and miss):
        raise ValueError("deepseek: cache hit/miss pricing block not found")
    models = re.search(r"MODEL\s+(deepseek-[a-z0-9-]+)", txt, re.I)
    return {
        "model": (models.group(1) if models else "deepseek-flash") + " (col 1)",
        "cached": float(hit.group(3)),  # PEAK = standard rate; off-peak halves both, ratio unchanged
        "compute": float(miss.group(3)),
        "source": DEEPSEEK_URL,
        "note": "cache-hit vs cache-miss input, peak rate, per 1M tokens",
    }


def check_huggingface() -> str:
    """HF inference-providers pricing docs bill routing credits — verify no cached split."""
    body = safe_get(HUGGINGFACE_URL)
    txt = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    n_cache = len(re.findall(r"cache", txt, re.I))
    n_token_price = len(re.findall(r"per (?:1M|M) tokens?|\$\s*[0-9.]+\s*/\s*M", txt, re.I))
    if n_cache == 0 and n_token_price == 0:
        return f"excluded: no cached/compute token split on docs page (cache mentions: {n_cache}, per-token prices: {n_token_price})"
    raise ValueError(f"huggingface: unexpected page shape (cache={n_cache}, tokenprice={n_token_price}) — inspect manually")


EXTRACTORS = [
    ("anthropic", ex_anthropic),
    ("openai", ex_openai),
    ("google", ex_google),
    ("deepseek", ex_deepseek),
]


def write_csv(rows: list[dict]) -> None:
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["provider", "cached_price", "compute_price", "ratio", "source_url"])
        for r in rows:
            w.writerow([r["provider"], f"{r['cached']:g}", f"{r['compute']:g}", f"{r['ratio']:.4f}", r["source"]])


def previous_csv() -> Path | None:
    cands = [p for p in sorted(INBOX.glob("pricing_ratios_*.csv")) if p != OUT]
    return cands[-1] if cands else None


def read_dashboard(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8") as f:
        return {row["provider"]: row for row in csv.DictReader(f)}


def print_diff(prev: Path, rows: list[dict]) -> None:
    old = read_dashboard(prev)
    print(f"[diff] vs {prev.name}:")
    changes = 0
    for r in rows:
        o = old.pop(r["provider"], None)
        if o is None:
            print(f"  + {r['provider']}: added (cached={r['cached']:g} compute={r['compute']:g} ratio={r['ratio']:.4f})")
            changes += 1
        elif (o["cached_price"], o["compute_price"]) != (f"{r['cached']:g}", f"{r['compute']:g}"):
            print(
                f"  ~ {r['provider']}: cached {o['cached_price']}->{r['cached']:g}, "
                f"compute {o['compute_price']}->{r['compute']:g}, ratio {o['ratio']}->{r['ratio']:.4f}"
            )
            changes += 1
        else:
            print(f"  = {r['provider']}: unchanged (ratio {r['ratio']:.4f})")
    for name in sorted(old):
        print(f"  - {name}: removed from dashboard")
        changes += 1
    if changes == 0:
        print("  no changes")


def register(path: Path, purpose: str) -> None:
    """Append-only self-seal, same convention as tools/meters_nightly.py."""
    sha = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    now = datetime.now(timezone.utc)
    line = json.dumps(
        {
            "seq": int(now.timestamp() * 1e6),
            "ts": now.isoformat(timespec="seconds"),
            "op": "register",
            "file": "/board/inbox/" + path.name,
            "sha256": sha,
            "class": "RECEIPT",
            "purpose": purpose,
        },
        ensure_ascii=False,
    )
    with INDEX.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> int:
    rows: list[dict] = []
    failures: list[str] = []
    for provider, fn in EXTRACTORS:
        try:
            d = fn()
            d["provider"] = provider
            d["ratio"] = d["cached"] / d["compute"] if d["compute"] else 0.0
            rows.append(d)
            print(
                f"[pricing] {provider:10s} {d['model']}: cached=${d['cached']:g} "
                f"compute=${d['compute']:g} ratio={d['ratio']:.4f}  ({d['note']})"
            )
        except Exception as exc:  # noqa: BLE001 — one provider failing must not kill the rest
            failures.append(provider)
            print(f"[pricing] {provider:10s} FAILED: {type(exc).__name__}: {exc}")
    try:
        print(f"[pricing] huggingface {check_huggingface()}")
    except Exception as exc:  # noqa: BLE001
        print(f"[pricing] huggingface CHECK FAILED: {type(exc).__name__}: {exc}")

    if not rows:
        print("[pricing] no provider succeeded; dashboard not written")
        return 1
    INBOX.mkdir(parents=True, exist_ok=True)
    write_csv(rows)
    print(f"[csv] wrote {OUT} ({len(rows)} provider rows)")

    prev = previous_csv()
    if prev is None:
        print("[diff] no previous pricing_ratios_*.csv in watch/inbox — baseline established")
    else:
        print_diff(prev, rows)

    register(OUT, "pricing diff cron: cached/compute ratio dashboard")
    print(f"[register] sealed {OUT.name} into {INDEX.name}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
