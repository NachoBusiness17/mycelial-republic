# mcp-hosting-ops lane validator (gala 20260925, division B)
# Byte checks: JSON parses, rows schema-shaped, quotes verbatim-copied from sources
# (whitespace runs collapsed to single spaces to survive markdown line-wrap),
# quote word count <= 40, leverage enum valid, source files sha256'd,
# lane JSON scanned for em/en dashes (record law: none allowed in lane prose).
import hashlib
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent / "mcp-hosting-ops.json"
SOURCES = Path(__file__).resolve().parent / "mcp-hosting-ops.sources"
WS = re.compile(r"\s+")
failures = []

def norm(s):
    return WS.sub(" ", s).strip()

raw = LANE.read_bytes()
text = raw.decode("utf-8")
try:
    data = json.loads(text)
    print(f"[ok] lane JSON parses: {len(raw)} bytes")
except Exception as exc:
    print(f"[FAIL] lane JSON does not parse: {exc}")
    sys.exit(1)

for key in ("lane", "division", "ok", "note", "rows", "checks", "decision_changed", "artifact"):
    if key in data:
        print(f"[ok] base key present: {key}")
    else:
        failures.append(f"missing base key: {key}")
        print(f"[FAIL] base key missing: {key}")

for bad, name in (("\u2014", "em-dash U+2014"), ("\u2013", "en-dash U+2013")):
    if bad in text:
        failures.append(f"{name} found in lane JSON")
        print(f"[FAIL] {name} present in lane JSON")
    else:
        print(f"[ok] no {name} in lane JSON")

rows = data.get("rows", [])
print(f"[info] rows: {len(rows)}")
source_cache = {}
for i, row in enumerate(rows, 1):
    rid = row.get("law", f"row{i}")
    src = Path(row.get("source", ""))
    if not src.is_absolute() or not src.exists():
        failures.append(f"{rid}: source missing or not absolute: {src}")
        print(f"[FAIL] {rid}: source missing/not absolute: {src}")
        continue
    if src not in source_cache:
        source_cache[src] = norm(src.read_text(encoding="utf-8"))
    quote = row.get("quote", "")
    if norm(quote) in source_cache[src]:
        print(f"[ok] {rid}: quote verbatim in source ({src.name})")
    else:
        failures.append(f"{rid}: quote NOT found byte-for-byte in source")
        print(f"[FAIL] {rid}: quote NOT found byte-for-byte in source")
    wc = len(quote.split())
    if wc <= 40:
        print(f"[ok] {rid}: quote word count {wc} <= 40")
    else:
        failures.append(f"{rid}: quote word count {wc} > 40")
        print(f"[FAIL] {rid}: quote word count {wc} > 40")
    lev = row.get("leverage", "")
    if lev in ("high", "medium", "low"):
        print(f"[ok] {rid}: leverage={lev}")
    else:
        failures.append(f"{rid}: bad leverage {lev!r}")
        print(f"[FAIL] {rid}: bad leverage {lev!r}")

print("[info] source byte manifest (sha256, bytes):")
for src in sorted(source_cache):
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    print(f"  {digest}  {src.stat().st_size:>7}  {src.name}")

if failures:
    print(f"[FAIL] {len(failures)} failure(s):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("[PASS] all byte checks green")
sys.exit(0)
