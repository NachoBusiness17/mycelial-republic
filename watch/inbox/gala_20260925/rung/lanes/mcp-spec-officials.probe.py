"""mcp-spec-officials falsifiable probe (division B, GALA rung 2026-10-10).

Claims under test (both falsifiable, both live-fetched):
  C1: The newest FINAL (non-RC) spec tag in github.com/modelcontextprotocol/modelcontextprotocol
      is exactly "2026-07-28".
      Falsifier: any newer final tag (e.g. 2026-10-15) appears.
  C2: The 2026-07-28 transports index names exactly two standard bindings,
      stdio and Streamable HTTP, and does NOT name "HTTP+SSE" as standard.
      Falsifier: a third standard binding listed, or HTTP+SSE reinstated as standard.

Exit 0 = both claims hold; exit 1 = at least one falsified (prints which).
"""
import json
import re
import sys
import urllib.request

UA = {"User-Agent": "mcp-spec-officials-probe/2026-10-10 (estate gala lane)"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
        return resp.read()


failures = []

# C1: newest final spec tag
tags_raw = fetch("https://api.github.com/repos/modelcontextprotocol/modelcontextprotocol/tags?per_page=100")
tags = [t["name"] for t in json.loads(tags_raw.decode("utf-8"))]
final_tags = [t for t in tags if not re.search(r"-RC|-final|-draft", t)]
final_tags_sorted = sorted(final_tags, reverse=True)  # ISO dates sort lexicographically
newest = final_tags_sorted[0] if final_tags_sorted else None
print("C1 tags seen (final only):", ", ".join(sorted(final_tags)))
if newest == "2026-07-28":
    print("C1 PASS: newest final spec tag = 2026-07-28")
else:
    failures.append("C1")
    print(f"C1 FAIL: newest final spec tag = {newest!r}, expected '2026-07-28'")

# C2: transports index bindings
body = fetch("https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/index.md").decode("utf-8")
has_stdio = bool(re.search(r"\bstdio\b", body))
has_streamable = bool(re.search(r"Streamable HTTP", body))
mentions_httpsse_standard = bool(re.search(r"HTTP\+SSE", body))
binding_items = re.findall(r"^\d+\. \[(stdio|Streamable HTTP)\]", body, re.M)
print("C2 numbered standard-binding items:", binding_items)
if has_stdio and has_streamable and binding_items == ["stdio", "Streamable HTTP"] and not mentions_httpsse_standard:
    print("C2 PASS: standard bindings = stdio + Streamable HTTP; HTTP+SSE absent from the 2026-07-28 transports index")
else:
    failures.append("C2")
    print(f"C2 FAIL: stdio={has_stdio} streamable={has_streamable} items={binding_items} httpsse_mentioned={mentions_httpsse_standard}")

if failures:
    print("PROBE VERDICT: FALSIFIED on " + ",".join(failures))
    sys.exit(1)
print("PROBE VERDICT: both claims hold (exit 0)")
sys.exit(0)
