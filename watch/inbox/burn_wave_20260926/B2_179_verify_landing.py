# B2-179 verification pass landing: claim line, restore-guard check,
# landing note with both receipt pointers on the B2-179 row,
# 1 self-feed brief (unchecked, dynamic highest+1), claim retire, LEDGER row.
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = os.getcwd()
QPATH = "watch/inbox/burn_wave_20260926/QUEUE.md"
QABS = os.path.join(REPO, QPATH)
RECEIPT = "watch/inbox/burn_wave_20260926/B2_179_dogfood_meters_20260926.md"
PRIMARY = "watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md"
LEDGER = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")

now = lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def read_q():
    with open(QABS, encoding="utf-8") as f:
        return f.read()

# ---- fresh read + restore-guard pre-write check ----
q1 = read_q()
sha = hashlib.sha256(q1.encode("utf-8")).hexdigest()
ts0 = now()
r = subprocess.run(
    [os.path.join(REPO, ".venv", "Scripts", "python.exe"), "tools/restore_guard.py",
     "check", "--path", QPATH, "--file", QABS,
     "--snapshot-sha", sha, "--snapshot-ts", ts0],
    capture_output=True, text=True)
print("restore_guard:", r.returncode, (r.stdout + r.stderr).strip()[:300])
if r.returncode != 0:
    raise SystemExit("restore guard blocked; rebase required")

# ---- write 1: append the CLAIM line ----
claim = ("- CLAIM B2-179 " + QPATH + " " + ts0 +
         " (B2-179 verification and pointer-repair pass: landing note with both receipt "
         "pointers on the B2-179 row, 1 self-feed brief, claim retire; the row's work landed "
         "18:50:31Z per LEDGER line 244, this pass repairs the post-repair missing pointer; "
         "foreign active CLAIMs honored, anchored edits on freshly-read bytes, no whole-file "
         "rewrite)")
if claim not in q1:
    q1w = q1
    if not q1w.endswith("\n"):
        q1w += "\n"
    q1w += claim + "\n"
    with open(QABS, "w", encoding="utf-8", newline="") as f:
        f.write(q1w)
    print("claim filed at", ts0)
else:
    print("claim already present (rerun)")

# ---- write 2: anchored edits on freshly-read bytes ----
q2 = read_q()
assert claim in q2, "own claim vanished from board before the landing edit"

row_line = None
for line in q2.splitlines():
    if line.startswith("- [ ] B2-179 ") or line.startswith("- [x] B2-179 "):
        row_line = line
        break
assert row_line, "B2-179 row not found on fresh bytes"
print("row state on fresh bytes:", row_line[:42])

q3 = q2
if "Landed 2026-09-26" in row_line:
    print("landing note already on row (rerun), skipping note append")
else:
    note = (" Landed 2026-09-26 (original landing 18:50:31Z per LEDGER line 244; receipt "
            "recovered after board-repair, this pass re-verified every byte anchor green and "
            "restored the pointer the repair dropped): " + PRIMARY +
            " (primary meters filing) plus " + RECEIPT +
            " (lane receipt, byte verification, 143-of-144 absorbed precision note, pointer repair)")
    q3 = q2.replace(row_line + "\n", row_line + note + "\n", 1)
    assert q3 != q2, "landing note splice failed"

retired = claim.replace("- CLAIM B2-179", "- CLAIMED B2-179", 1) + " -> " + RECEIPT
q4 = q3.replace(claim + "\n", retired + "\n", 1)
assert q4 != q3, "claim retire splice failed"

claimed = set(int(n) for n in re.findall(r"B2-(\d+)", q4))
n = max(claimed)
while n in claimed:
    n += 1
brief_num = n
print("self-feed number:", brief_num)

brief = ("- [ ] B2-" + str(brief_num) + " Checked-row pointer liveness patrol: (self-fed by B2-179) "
         "during this lane's 2026-09-26 verification pass the B2-179 row flipped [ ] to [x] between "
         "two reads minutes apart with no landing pointer attached (concurrent bare flip), and the "
         "board repair recovered note-less checked rows whose landing text survived nowhere, while "
         "the self-feed law says the flip carries the pointer, so checked rows with a missing or "
         "unresolvable receipt pointer are a recurring state no surface names; add the patrol "
         "(tests/test_census_drift_patrol.py pattern or an improve --status row): walk every [x] "
         "row on watch/inbox/burn_wave_20260926/QUEUE.md, resolve its receipt pointer, name rows "
         "with no pointer or a pointer whose target file is absent on disk; complements the B2-487 "
         "row in this file (CLAIM ghosts), not a duplicate: that one audits claim lines, this one "
         "audits landed rows; falsifier: on a sandbox copy, delete one landed receipt file and "
         "blank one checked row's pointer, run the patrol, nothing names either; pointers the "
         "B2-487 row in this file, watch/inbox/burn_wave_20260926/B2_355_checkbox_reaudit_20260926.md, "
         "watch/inbox/burn_wave_20260926/B2_238_checkbox_law_20260926.md")
q5 = q4
if not q5.endswith("\n"):
    q5 += "\n"
q5 += brief + "\n"

with open(QABS, "w", encoding="utf-8", newline="") as f:
    f.write(q5)
print("board updated: row pointer, claim retired, brief B2-" + str(brief_num))

# ---- ledger row ----
ts = now()
one_line = (
    "B2-179 verification and pointer-repair pass: the brief's meters receipt already landed "
    "2026-09-26T18:50:31Z (LEDGER row 244, watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md) "
    "and every byte anchor re-verified green (BURN_WAVE_PIN line 19: 109M tok/h measured, 97.3pct "
    "cache; ASTRA witness3 line 123: 97.3 pct cache; B2_98 totals: 507 matched, 363 completed, "
    "144x429, 143 absorbed retries, 0 terminal failed turns; self-fed briefs B2-453 and B2-455 "
    "Open unchecked, B2-454 landed); this pass filed the dispatcher-named lane receipt "
    "(watch/inbox/burn_wave_20260926/B2_179_dogfood_meters_20260926.md), restored the landing "
    "pointer the board repair dropped from the B2-179 row (row flipped bare to [x] between two "
    "reads minutes apart), self-fed 1 brief UNCHECKED highest+1 (B2-" + str(brief_num) + "); "
    "primary meters text not forked, the 18:50:31Z ledger row untouched")
row = {
    "ts": ts,
    "slug": "B2-179-dogfood-meters-verify-20260926",
    "verdict": "LANDED",
    "lane": "B2-179",
    "landing": RECEIPT,
    "one_line": one_line,
}
with open(LEDGER, "a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=True) + "\n")
print("ledger row appended at", ts)
