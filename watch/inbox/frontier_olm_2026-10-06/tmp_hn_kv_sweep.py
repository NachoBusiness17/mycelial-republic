"""Pass-1 HN Algolia candidate extraction for the kv-context-engineering sweep.

SSRF-hardened per the Mimosa gate: literal https URLs, single allowlisted
public host (hn.algolia.com), resolved-IP check that blocks private/loopback/
link-local/reserved addresses before connect, and redirects refused. Saves
raw JSON evidence and prints deduped candidate rows.
"""
import ipaddress
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "sweep" / "_raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_HOSTS = {"hn.algolia.com"}

# (slug, literal_url). Window: created_at_i>1788652800 == 2026-09-06T00:00:00Z.
CALLS = [
    ("bydate_01_prompt_caching",
     "https://hn.algolia.com/api/v1/search_by_date?query=prompt%20caching&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_02_prompt_cache",
     "https://hn.algolia.com/api/v1/search_by_date?query=prompt%20cache&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_03_prefix_caching",
     "https://hn.algolia.com/api/v1/search_by_date?query=prefix%20caching&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_04_kv_cache",
     "https://hn.algolia.com/api/v1/search_by_date?query=KV%20cache&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_05_context_engineering",
     "https://hn.algolia.com/api/v1/search_by_date?query=context%20engineering&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_06_context_window",
     "https://hn.algolia.com/api/v1/search_by_date?query=context%20window&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_07_context_compression",
     "https://hn.algolia.com/api/v1/search_by_date?query=context%20compression&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_08_context_rot",
     "https://hn.algolia.com/api/v1/search_by_date?query=context%20rot&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_09_cache_hit",
     "https://hn.algolia.com/api/v1/search_by_date?query=cache%20hit&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_10_context_length",
     "https://hn.algolia.com/api/v1/search_by_date?query=context%20length&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_11_system_prompt",
     "https://hn.algolia.com/api/v1/search_by_date?query=system%20prompt&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("bydate_12_llamacpp_cache",
     "https://hn.algolia.com/api/v1/search_by_date?query=llama.cpp%20cache&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("rel_13_prompt_caching",
     "https://hn.algolia.com/api/v1/search?query=prompt%20caching&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("rel_14_kv_cache",
     "https://hn.algolia.com/api/v1/search?query=KV%20cache&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("rel_15_context_engineering",
     "https://hn.algolia.com/api/v1/search?query=context%20engineering&tags=story&numericFilters=created_at_i%3E1788652800"),
    ("rel_16_compaction",
     "https://hn.algolia.com/api/v1/search?query=compaction&tags=story&numericFilters=created_at_i%3E1788652800"),
]


def _ip_blocked(ip_text: str) -> bool:
    ip = ipaddress.ip_address(ip_text)
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_reserved or ip.is_multicast or ip.is_unspecified)


class _NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(
            newurl, code, "redirects refused by sweep policy", headers, fp)


_OPENER = urllib.request.build_opener(_NoRedirects)


def guarded_fetch(literal_url: str) -> dict:
    parsed = urllib.parse.urlparse(literal_url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"URL outside sweep allowlist: host={parsed.hostname!r}")
    infos = socket.getaddrinfo(parsed.hostname, 443, proto=socket.IPPROTO_TCP)
    for info in infos:
        if _ip_blocked(info[4][0]):
            raise ValueError(f"resolved IP blocked: {info[4][0]}")
    req = urllib.request.Request(
        literal_url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
    with _OPENER.open(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    seen = {}
    per_query = []
    for slug, url in CALLS:
        payload = guarded_fetch(url)
        (OUT_DIR / (slug + ".json")).write_text(
            json.dumps(payload, indent=1), encoding="utf-8")
        hits = payload.get("hits", [])
        per_query.append((slug, len(hits)))
        for h in hits:
            oid = h.get("objectID")
            if oid and oid not in seen:
                seen[oid] = h
        time.sleep(0.4)

    rows = []
    for h in seen.values():
        title = h.get("title") or h.get("story_title") or ""
        if not title:
            continue
        rows.append({
            "id": h.get("objectID"),
            "title": title,
            "pts": h.get("points") or 0,
            "comments": h.get("num_comments") or 0,
            "date": (h.get("created_at") or "")[:10],
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
        })
    rows.sort(key=lambda r: (r["pts"] + r["comments"]), reverse=True)
    (OUT_DIR / "candidates.json").write_text(
        json.dumps(rows, indent=1), encoding="utf-8")
    print(f"== per-query hit counts ({len(CALLS)} calls)")
    for name, n in per_query:
        print(f"  {name}: {n}")
    print(f"\n== distinct candidates: {len(rows)}")
    for i, r in enumerate(rows[:60], 1):
        print(f"{i:2d}. [{r['id']}] {r['pts']:>4}pts {r['comments']:>3}c {r['date']} "
              f"{r['title'][:96]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
