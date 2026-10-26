"""Finish-line byte check for lane mcp-corporate-patterns (division B).

Verifies: lane JSON parses and carries required fields; every row quote is a
byte-copied substring of the evidence file; no em-dash/en-dash characters in
the lane JSON or the evidence file. Prints PASS/FAIL lines and exits 0 or 2.
"""
import json
import os
import sys

LANE = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\gala_20260925\rung\lanes\mcp-corporate-patterns.json"
EVID = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\gala_20260925\rung\lanes\mcp-corporate-patterns.evidence.md"
CHECK = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\gala_20260925\rung\lanes\mcp-corporate-patterns.check.txt"

failures = []

def check(name, cond, detail=""):
    if cond:
        print("PASS | " + name + ((" | " + detail) if detail else ""))
    else:
        print("FAIL | " + name + ((" | " + detail) if detail else ""))
        failures.append(name)

with open(LANE, "r", encoding="utf-8") as f:
    lane_bytes = f.read()
with open(EVID, "r", encoding="utf-8") as f:
    evid_text = f.read()

lane = json.loads(lane_bytes)

check("lane_json_parses", True, "lane=%s division=%s ok=%s" % (lane.get("lane"), lane.get("division"), lane.get("ok")))
required = ["lane", "division", "ok", "note", "rows", "checks", "decision_changed", "artifact"]
missing = [k for k in required if k not in lane]
check("lane_json_required_fields", not missing, "missing=%s" % missing if missing else "all %d present" % len(required))

rows = lane.get("rows", [])
check("rows_count", len(rows) == 7, "rows=%d" % len(rows))

row_req = ["law", "claim", "quote", "source", "steal", "falsifier", "leverage"]
for i, r in enumerate(rows):
    miss = [k for k in row_req if k not in r or not r[k]]
    check("row%d_fields" % i, not miss, ("missing=%s" % miss) if miss else r.get("law", "?"))
    q = r.get("quote", "")
    in_evid = q in evid_text
    words = len(q.split())
    check("row%d_quote_byte_in_evidence" % i, in_evid, "%d words | found verbatim in evidence file" % words)
    check("row%d_quote_le40_words" % i, words <= 40, "%d words" % words)

for label, text in (("lane_json", lane_bytes), ("evidence", evid_text)):
    bad = [ch for ch in ("\u2014", "\u2013") if ch in text]
    check("no_emdash_endash_" + label, not bad, "clean" if not bad else "found %r" % bad)

check("artifact_path_absolute", lane.get("artifact", "").startswith("C:/Users/foste/Documents/projects/local_sovereign_agent/"), lane.get("artifact", ""))
check("row_sources_absolute", all(r.get("source", "").startswith("C:/Users/foste/Documents/projects/local_sovereign_agent/") for r in rows), "all rows")

print("")
print("LANE_JSON : %s (%d bytes)" % (LANE, os.path.getsize(LANE)))
print("EVIDENCE  : %s (%d bytes)" % (EVID, os.path.getsize(EVID)))
print("CHECK_OUT : %s" % CHECK)
print("")
print("RATCHET   : not run; this lane wrote only under watch/inbox/gala_20260925/rung/lanes/ (no mag/ or tools/ code touched, so the ask's ratchet condition does not fire)")
print("")
print("RESULT: %s (%d failure(s))" % ("FAIL" if failures else "PASS", len(failures)))
sys.exit(2 if failures else 0)
