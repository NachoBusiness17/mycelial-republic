"""Byte check for the neuromorphic-hardware gala lane.

Verifies, against the files on disk:
1. the receipt exists and is non-trivial;
2. the lane JSON parses and carries at least 7 rows;
3. every row's quote is a byte substring of the receipt (VERBATIM, byte-copied);
4. no em-dash (U+2014) in the receipt or the lane JSON (record law);
5. the receipt contains the named BRIDGE VERDICT: NO marker.
Exit 0 only if all pass.
"""
import json
import sys

LANE = r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/spiking-wide/lanes/neuromorphic-hardware.json"
RECEIPT = r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/spiking_wide/neuromorphic-hardware.md"

fails = []

rb = open(RECEIPT, "rb").read()
print("receipt_bytes", len(rb))
if len(rb) < 2000:
    fails.append("receipt too small")

jb = open(LANE, "rb").read()
try:
    lane = json.loads(jb.decode("utf-8"))
except Exception as exc:  # noqa: BLE001
    print("json_parse_error", exc)
    sys.exit(1)
rows = lane.get("rows", [])
print("rows", len(rows))
if len(rows) < 7:
    fails.append("expected at least 7 rows")

for i, row in enumerate(rows):
    q = row.get("quote", "").encode("utf-8")
    ok = q in rb
    print(f"quote_row_{i}_verbatim", ok)
    if not ok:
        fails.append(f"row {i} quote not byte-copied from receipt")

for name, blob in (("receipt", rb), ("lane_json", jb)):
    n = blob.count(b"\xe2\x80\x94")
    print(f"emdash_{name}", n)
    if n:
        fails.append(f"em-dash found in {name}")

dec = rb.decode("utf-8", errors="replace")
print("bridge_verdict_no_marker", "BRIDGE VERDICT (named)" in dec and "**NO.**" in dec)
if "BRIDGE VERDICT (named)" not in dec or "**NO.**" not in dec:
    fails.append("bridge verdict marker missing")

print("lanes_checked", 1)
if fails:
    print("FAIL", "; ".join(fails))
    sys.exit(1)
print("PASS all byte checks")
sys.exit(0)
