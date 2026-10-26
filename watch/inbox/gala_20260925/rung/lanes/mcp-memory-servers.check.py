"""Finish-line check for the mcp-memory-servers gala lane (division B).

Byte checks:
  C1 lane JSON parses
  C2 every fetched file sha256 matches the manifest (recomputed here, not trusted)
  C3 every quote in the JSON is a verbatim substring of its cited estate file,
     found on or near the claimed line (exact line reported)
  C4 zero U+2014 (em dash) and zero U+2013 (en dash) anywhere in the lane JSON
  C5 every quote id referenced by servers[] exists in quotes[]
  C6 decision ledger present
"""
import hashlib
import json
import pathlib
import sys

LANE_DIR = pathlib.Path(__file__).resolve().parent
LANE_JSON = LANE_DIR / "mcp-memory-servers.json"

fails = []
passes = []


def ok(msg):
    passes.append(msg)
    print("PASS " + msg)


def bad(msg):
    fails.append(msg)
    print("FAIL " + msg)


raw = LANE_JSON.read_text(encoding="utf-8")

# C1 parse
try:
    lane = json.loads(raw)
    ok("C1 lane JSON parses (%d bytes)" % len(raw))
except Exception as exc:  # noqa: BLE001
    bad("C1 lane JSON does not parse: %r" % exc)
    print("CHECK RESULT: 1/6 passed; aborting remaining checks")
    sys.exit(1)

# C2 sha256 of every fetched file vs manifest and vs the lane JSON claim
fetch_dir = LANE_DIR / "fetched"
manifest = {}
for line in (fetch_dir / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line:
        continue
    digest, name = line.split(maxsplit=1)
    manifest[name.lstrip("*")] = digest

claimed = {row["sha256"]: row["file"] for row in lane["fetched"]}
for sha, rel in sorted(claimed.items()):
    path = LANE_DIR / rel
    if not path.exists():
        bad("C2 missing fetched file %s" % rel)
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    name = path.name
    if actual != sha:
        bad("C2 sha mismatch %s: json says %s, bytes say %s" % (name, sha, actual))
    elif name in manifest and manifest[name] != actual:
        bad("C2 manifest drift %s: manifest %s, bytes %s" % (name, manifest[name], actual))
    else:
        ok("C2 sha256 match %s" % name)

# C3 every quote verbatim in its cited file; report the actual line found
for q in lane["quotes"]:
    qpath = pathlib.Path(q["file"])
    if not qpath.exists():
        bad("C3 quote file missing %s (%s)" % (q["id"], q["file"]))
        continue
    text = qpath.read_text(encoding="utf-8")
    if q["text"] not in text:
        bad("C3 quote not byte-present in file: %s" % q["id"])
        continue
    actual_line = text[: text.index(q["text"])].count("\n") + 1
    if abs(actual_line - q["line"]) > 1:
        bad("C3 quote %s found on line %d but cited line %d" % (q["id"], actual_line, q["line"]))
    else:
        ok("C3 quote %s verbatim at %s line %d (cited %d)" % (q["id"], qpath.name, actual_line, q["line"]))

# C4 dash audit
for ch, label in (("\u2014", "em dash U+2014"), ("\u2013", "en dash U+2013")):
    n = raw.count(ch)
    if n:
        bad("C4 lane JSON contains %d x %s" % (n, label))
    else:
        ok("C4 zero %s in lane JSON" % label)

# C5 quote ids referenced by servers[] all exist
ids = {q["id"] for q in lane["quotes"]}
missing = []
for srv in lane["servers"]:
    for qid in srv.get("quotes", []):
        if qid not in ids:
            missing.append("%s -> %s" % (srv["name"], qid))
if missing:
    bad("C5 dangling quote refs: %s" % "; ".join(missing))
else:
    ok("C5 all %d server quote refs resolve (quotes banked: %d)"
       % (sum(len(s.get("quotes", [])) for s in lane["servers"]), len(ids)))

# C6 decision ledger
if lane.get("decision_ledger"):
    ok("C6 decision ledger present (%d chars)" % len(lane["decision_ledger"]))
else:
    bad("C6 decision ledger missing")

print("")
print("CHECK RESULT: %d passed, %d failed" % (len(passes), len(fails)))
sys.exit(1 if fails else 0)
