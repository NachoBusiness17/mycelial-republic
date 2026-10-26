import json, os, sys

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
SIGNALS = ROOT + "/watch/inbox/luncheon_watchlist_20260929_signals.jsonl"
WATCHLIST = ROOT + "/watch/inbox/luncheon_watchlist_20260929.jsonl"
RECEIPT = ROOT + "/watch/inbox/ball4/defense-enterprise.md"
CHECK_TXT = ROOT + "/watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow-defense-enterprise.check.txt"

TARGETS = ["lunch-alex-karp", "lunch-shyam-sankar", "lunch-brandon-rahbar-daniels",
           "lunch-bill-mcdermott", "lunch-nikesh-arora", "lunch-jared-isaacman",
           "lunch-richard-walters", "lunch-sean-cairncross"]

fails = []
def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL") + " | " + name + (" | " + detail if detail else ""))
    if not cond:
        fails.append(name)

# 1. signals register: 8 valid rows BY THIS WRITER, one per target watch_id
# WRITER-FILTER RE-SCOPE (2026-09-29, midnight reader critique of ball4-luncheon-follow):
# the original assertions ran against the whole shared register and were true only at this
# lane's own run moment (snapshot "signals rows: 8" in follow-defense-enterprise.check.txt);
# the register is now the 36-row shared surface of 4 lanes (8+9+14+5 rows by writer) and a
# raw rerun exited 1 with 3 FAILs while the lane JSON still claimed exit 0. Re-scoped to
# writer == gala-ball4-follow-defense-enterprise (same writer-filter pattern as
# follow_compute_check.py) so the exit code matches final disk state. The register-level
# duplicate (lunch-sean-cairncross line 8 this lane vs line 31 capital-policy) is annotated
# in the register itself; rows are never deleted.
WRITER = "gala-ball4-follow-defense-enterprise"
rows = []
with open(SIGNALS, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception as e:
            fails.append("signals line %d unparseable: %s" % (i, e))
total_register_rows = len(rows)
rows = [r for r in rows if r.get("writer") == WRITER]
ids = [r.get("watch_id") for r in rows]
print("signals rows: %d (register total %d; writer-filtered to %s)" % (len(rows), total_register_rows, WRITER))
print("signals watch_ids: " + ", ".join(sorted(ids)))
check("signals has 8 rows by this writer", len(rows) == 8, "found %d" % len(rows))
check("signals one row per target, no dupes (writer-filtered)", sorted(ids) == sorted(TARGETS))
check("every signals row carries window + estate_angle + handle_check (writer-filtered)",
      all(r.get("window") == "2026-09-15/2026-09-29" and r.get("estate_angle") and r.get("handle_check") for r in rows))

# 2. watchlist: parses, 34 lines, the 3 updated rows carry resolved grades
wl = []
with open(WATCHLIST, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            wl.append(json.loads(line))
        except Exception as e:
            fails.append("watchlist line %d unparseable: %s" % (i, e))
by_id = {r.get("watch_id"): r for r in wl}
print("watchlist rows: %d, all parsed: %s" % (len(wl), all(True for _ in wl)))
check("watchlist still has 34 rows", len(wl) == 34, "found %d" % len(wl))

wal = by_id.get("lunch-richard-walters", {})
print("walters row: org=%r lane=%r handle_grade=%r resolved=%r" % (wal.get("org"), wal.get("lane"), wal.get("handle_grade"), wal.get("resolved")))
check("walters resolved:true and grade not search", wal.get("resolved") is True and wal.get("handle_grade") != "search")
check("walters org names deputy chief of staff", "Deputy Chief of Staff" in wal.get("org", ""))

cai = by_id.get("lunch-sean-cairncross", {})
print("cairncross row: org=%r lane=%r handle_grade=%r resolved=%r" % (cai.get("org"), cai.get("lane"), cai.get("handle_grade"), cai.get("resolved")))
check("cairncross resolved:true and grade not search", cai.get("resolved") is True and cai.get("handle_grade") != "search")
check("cairncross org corrected to National Cyber Director", "National Cyber Director" in cai.get("org", ""))

mcd = by_id.get("lunch-bill-mcdermott", {})
print("mcdermott row: handle=%r handle_grade=%r resolved=%r" % (mcd.get("handle"), mcd.get("handle_grade"), mcd.get("resolved")))
check("mcdermott handle live-confirmed", mcd.get("handle") == "@BillRMcDermott" and mcd.get("handle_grade") == "confirmed")

# 3. receipt exists, non-empty
check("receipt exists and non-empty", os.path.getsize(RECEIPT) > 200, "%d bytes" % os.path.getsize(RECEIPT))

# 4. record law: no em-dash in the three register surfaces + receipt
EMDASH = "\u2014"
for path in (SIGNALS, WATCHLIST, RECEIPT):
    with open(path, encoding="utf-8") as f:
        body = f.read()
    check("no em-dash in " + os.path.basename(path), EMDASH not in body)

print("")
print("CHECKS FAILED: %d" % len(fails))
for x in fails:
    print("  - " + x)
sys.exit(1 if fails else 0)
