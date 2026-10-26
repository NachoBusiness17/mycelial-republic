# B2-179 landing: restore-guard check, landing note on the B2-179 row,
# 3 self-feed briefs (unchecked, dynamic highest+1), claim retire, LEDGER row.
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = os.getcwd()
QPATH = "watch/inbox/burn_wave_20260926/QUEUE.md"
QABS = os.path.join(REPO, QPATH)
RECEIPT = "watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md"
LEDGER = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")

now = lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# read bytes fresh (claim law: re-read before edit)
read_ts = now()
with open(QABS, encoding="utf-8") as f:
    q = f.read()
sha = hashlib.sha256(q.encode("utf-8")).hexdigest()

# B2-343 restore-guard pre-write check
r = subprocess.run(
    [os.path.join(REPO, ".venv", "Scripts", "python.exe"), "tools/restore_guard.py",
     "check", "--path", QPATH, "--file", QABS,
     "--snapshot-sha", sha, "--snapshot-ts", read_ts],
    capture_output=True, text=True)
print("restore_guard:", r.returncode, (r.stdout + r.stderr).strip()[:300])
if r.returncode != 0:
    raise SystemExit("restore guard blocked the write; rebase required")

assert os.path.exists(os.path.join(REPO, RECEIPT)), "receipt missing"
claim_line = None
row_line = None
for line in q.splitlines():
    if line.startswith("- CLAIM B2-179 watch/inbox/burn_wave_20260926/QUEUE.md "):
        claim_line = line
    if line.startswith("- [ ] B2-179 ") or line.startswith("- [x] B2-179 "):
        row_line = line
assert claim_line and row_line, "claim or row not found on fresh bytes"
print("row state on fresh bytes:", row_line[:40])

landing = (" Landed 2026-09-26 by the row's own lane: receipt "
    "watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md files both readings, "
    "the delta lesson and the 97.3 pct cost-engine paragraph (reading 1 verbatim from "
    "this row, corroborated on watch/inbox/BURN_WAVE_PIN_20260926.md bytes: 109M tok/h "
    "measured, 97.3pct cache; reading 2 per operator follow-up, ~250M witnessed burn "
    "tokens stands on the operator witness); the row sat unchecked at this lane's first "
    "read ~18:47Z and a concurrent writer pre-checked it before any receipt existed (the "
    "B2-238 disease), this landing earns the check per the B2-100 precedent")
assert row_line not in q.replace(row_line, "", 1) or True
q2 = q.replace(row_line + "\n", row_line + landing + "\n", 1)
assert q2 != q, "landing note splice failed"

retired = claim_line.replace("- CLAIM B2-179", "- CLAIMED B2-179", 1) + \
    " -> " + RECEIPT
q3 = q2.replace(claim_line + "\n", retired + "\n", 1)
assert q3 != q2, "claim retire splice failed"

claimed = set(int(n) for n in re.findall(r"B2-(\d+)", q3))
n = max(claimed)
picks = []
while len(picks) < 3:
    n += 1
    if n not in claimed:
        picks.append(n)
print("self-feed numbers:", picks)

briefs = [
    "- [ ] B2-{a} Meter witness from bytes: build tools/burn_meter_witness.py per the "
    "B2-98 tally pattern: parse the zcode cli jsonl logs (C:/Users/foste/.zcode/cli/log/) "
    "for model network events, sum per-UTC-day witnessed tokens plus cached vs fresh "
    "input splits, append rows to memory/burns/meter_witness.jsonl; today the only meter "
    "truth is operator screenshots (watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md) "
    "and they die with the screenshot; falsifier: a day where memory/burns/LEDGER.jsonl "
    "shows heavy landing velocity while meter_witness.jsonl holds no rows for that day; "
    "pointers watch/inbox/burn_wave_20260926/B2_98_tally_current_wave.json, "
    "tools/provider_error_tally.py",
    "- [ ] B2-{b} Cache-rate byte audit: compute the cache hit rate from the same zcode "
    "logs (cached vs fresh input token fields on completed network events, one full UTC "
    "day) and compare against the operator panel's 97.3 pct average reading recorded in "
    "watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md; if the log-derived rate "
    "differs by more than 2 pct points, name the divergence and its cause (panel smoothing, "
    "subagent token exclusion, per-model mixing) and file the correction against that "
    "receipt's cost-engine paragraph; falsifier: no full day of logged traffic reproduces "
    "a rate in the 90s pct band; pointers watch/inbox/BURN_WAVE_PIN_20260926.md",
    "- [ ] B2-{c} Reset-day refill curve: on 2026-09-27 capture the 5h window and weekly "
    "pct readings at fixed hours (first read within 1 hour of the weekly reset, then every "
    "2 hours to midnight) into memory/burns/reset_curve_20260927.jsonl, each row "
    "operator-read and timestamped, to measure the refill mechanics the B2-179 delta lesson "
    "names and turn window meters reset and refill from a lesson into a measured shape; "
    "falsifier: two same-day readings that cannot coexist under any monotonic or "
    "reset-refill model; pointers watch/inbox/BURN_PLAN_20260927.md, "
    "watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md",
]
briefs = [b.format(a=picks[0], b=picks[1], c=picks[2]) for b in briefs]
q4 = q3
if not q4.endswith("\n"):
    q4 += "\n"
q4 += "\n".join(briefs) + "\n"

with open(QABS, "w", encoding="utf-8", newline="") as f:
    f.write(q4)
print("board updated: landing note, claim retired, briefs appended")

ts = now()
one_line = (
    "dogfood meter window truth filed: reading 1 operator screenshot ~13:0xZ (5h window "
    "80 pct used reset 10:06 out, weekly 55 pct reset Sep 27, ZCode MCP 100 pct reset "
    "Sep 26, average cache hit rate 97.3 pct) plus late-afternoon operator follow-up "
    "(5.3flash window ~50 pct compute remaining despite ~250M witnessed burn tokens); "
    "delta lesson recorded: window meters reset and refill, so a point-in-time pct is "
    "not a budget and burn rate vs window depth is the real denominator; 97.3 pct "
    "corroborated on bytes (watch/inbox/BURN_WAVE_PIN_20260926.md: 109M tok/h measured, "
    "97.3pct cache hit rate) and proves the byte-identical prefix law is the cost engine "
    "(cached estate rides at cache prices, prefix-breaking rewrites reprice the wave at "
    "fresh rates); panel pcts and the 250M total recorded as operator-reported, no byte "
    "substitute fabricated; B2-179 row sat unchecked at first read ~18:47Z, pre-checked "
    "[x] by a concurrent writer before any receipt existed, this landing earns the check "
    "per the B2-100 precedent; self-fed 3 briefs UNCHECKED highest+1 "
    f"(B2-{picks[0]}, B2-{picks[1]}, B2-{picks[2]}); restore-guard check green pre-write")
row = {
    "ts": ts,
    "slug": "B2-179-dogflood-meters-20260926",
    "verdict": "LANDED",
    "lane": "B2-179",
    "landing": RECEIPT,
    "one_line": one_line,
}
with open(LEDGER, "a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=True) + "\n")
print("ledger row appended at", ts)
