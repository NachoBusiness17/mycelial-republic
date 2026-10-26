# break-moonshot-2: hostile second pass on moonshot-2.md (GAP_REGISTER dogfood ride)

2026-10-01, hostile pass. Every cite in moonshot-2.md was re-run against the live tree this
session; commands and outputs are named inline. Nothing I could not verify is asserted;
unverifiable items are marked OWED. No em-dashes. No subprocess spawns (the win32
CREATE_NO_WINDOW law is trivially honored; all checks were direct file reads and shell greps).
The pasted report in the ask was truncated mid-finding-4; the full report was read at
watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/moonshot-2.md (7,454 bytes, mtime
2026-10-01 22:53:42 EDT). It holds exactly 4 findings.

## Verdicts

### Finding 1 (MISRANKED POST-FIX: rank 1 fixed pending fire, rank 2 is the live S1): CONFIRMED

Every cite byte-checked and holding:

- scripts/estate_walk_daily.ps1:5-13: PATH LAW comment at lines 5-10, absolute $repo at
  line 11, absolute log/alarm at 12-13. Read in full this session.
- logs/estate_walk_daily.log tail: `od -c` shows the END line
  "END 2026-10-02T00:37:54Z exit=0" (= 20:37:54 EDT Oct 1); `git log -1 5d2263f10` reads
  "2026-10-01 20:46:30 -0400"; delta 8m36s, the "9 min" claim holds.
- `cmd /c schtasks /Query /TN EstateWalkDaily /V /FO LIST`: "Last Run Time: 10/1/2026
  9:15:01 AM", "Last Result: 1", "Next Run Time: 10/2/2026 9:15:00 AM", "Status: Ready",
  "Task To Run: powershell -NoProfile ... estate_walk_daily.ps1". The falsifier fire has
  not happened; the executor is Windows PowerShell 5.1.
- watch/inbox/48h_synth/: no receipt present. NIT: the dir holds SIX 09-30 story files
  (STORY, lattice, laws, measure, next, steals), not "five" as the lens and register say.
- queue/lanes/elder/inbox.jsonl: 0 bytes, mtime 2026-09-04 10:43:28. Exact match.

Sharpening the lens did not do: commit 5d2263f10 carries BOTH the rank-1 fix
(scripts/estate_walk_daily.ps1, 19 lines changed) and GAP_REGISTER.md (247 insertions),
so the register was born stale: its rank-1 row still reads "repeats 10-02 09:15 with the
same relative-path defect" while the same commit removes that defect. And the fix proof is
MORE incomplete than the lens said: `grep -n "ESTATE-WALK" memory/attention.md` returns
exit 1 (zero matches ever), so the alarm channel has never fired in recorded history and
fill 1's "prove BOTH channels fire on an injected failure" is undone; the hand smoke
proved only the success/log channel. See also Addition 2 (F6 already falsified).

### Finding 2 (NEW GAP: bake log is UTF-16LE, grep-blind): CONFIRMED, mechanism corrected

- `wc -c` = 1,166 bytes. `od -c` head: "377 376" BOM then null-interleaved ASCII
  (UTF-16LE) throughout. `grep -c END` = 0, exit 1. STRONGER THAN CLAIMED: even
  `grep -a -c END` = 0, exit 1, so binary-mode grep is blind too.
- `iconv -f UTF-16LE -t UTF-8` decodes two END lines: 2026-09-29T22:16:50Z (registration
  smoke, commit bd286f138) and 2026-10-02T00:37:54Z (fix smoke). No END line for the
  10-01 09:15 scheduled fire, consistent with the failure story.
- MECHANISM ERROR in the lens: "Add-Content (lines 20, 23) writes ANSI" is false on the
  bytes. The od tail shows the Add-Content-written END line is null-interleaved
  ("E \0 N \0 D \0"), i.e. PS 5.1 Add-Content detected and matched the existing file's
  UTF-16LE encoding; the mixed-encoding file the lens implies does not exist. Also only
  line 23 writes the log; line 20 writes the alarm file (memory/attention.md). The
  conclusion (every grep instrument blind to the success channel) survives; the cure
  (explicit -Encoding utf8 on redirect and Add-Content) is still right.
- ADDITION: the log is tracked in git and clean (`git ls-files` lists it; porcelain
  empty), so the repo versions a NUL-byte UTF-16LE log and every fresh clone's grep is
  equally blind. Log mtime 20:46:30.509 equals the commit second (git artifact).

### Finding 3 (META-GAP 1 dominates, the register is its own specimen): WEAKENED

All 9 verifiable row states re-confirmed untouched (commands run this session):

- rank 2: inbox.jsonl 0 bytes (above). rank 3: `ls tools/citation_lint.py` = No such file.
- rank 4: STORY.md:240 carries "191.8M tokens spent" (`grep -n`); `grep -c "191"
  watch/inbox/frontier_olm_20260928/DIGEST.md` = 0; `find watch/inbox -maxdepth 2 -iname
  "*ERRATA*"` = nothing.
- rank 5: `ls $HOME/.mag` = only steer_seal_seen/; mag/seed_seal.py and
  tests/test_seal_forge_drill.py absent; `find . -name "*.seal" -not -path "./.git/*"` = 0.
- rank 6: `grep -c candidates mag/percolator.py` = 0, exit 1; invariants.json mtime
  2026-10-01 19:17:50, `grep -c frontier_olm` = 0.
- rank 7: watch/inbox/frontier_olm_2026-09-30/ = lens, steal, sweep only.
- rank 9: ARXIV_REGISTER.json mtime 2026-09-29 05:59:04, `grep -cE "2606\.03458|KVarN"` = 0.
- rank 10: quantization-compression.md exists (15,590 bytes, Oct 1 15:11), 0 hits for
  1sy7srk or 2609.21341.
- rank 11: TICKET_LEDGER.md 10,140 bytes, mtime Oct 1 17:35:33, 0 SS-1/CP-1/R2-1 hits.

But the finding's temporal frame is FALSE. GAP_REGISTER.md mtime = 2026-10-01 18:41:58
EDT; landing commit 5d2263f10 = 20:46:30 EDT; the lens's checks ran ~22:50 EDT
(moonshot-2.md mtime 22:53:42). That is ~4.2h since the register was written and ~2.1h
since it landed, not "24h after the register landed". At +2h on the landing evening,
10 untouched rows demonstrate nothing about a standing law; the indictment is premature,
not proven. Count nit: "10 of 12 rows byte-verify untouched" over-counts by one; it is 9
byte-verified rows plus rank 12, which is surface-only (spiking_wide/ holds the eight
original sweep files, no probe receipt, but the RX 5600 XT box state is OWED, and the
lens itself marked it so). Direction remains plausible (the register's own meta-gap 1 and
the commit message agree); the evidence as stated does not carry it.

### Finding 4 (register NOT-INDEXED, violates the contract it enforces): WEAKENED, core claim KILLED

- KILLED: "it is itself NOT-INDEXED (0 hits in watch/inbox/INDEX.json)". INDEX.json's own
  schema header: "INDEX.json is now DERIVED from the append-only event log
  index_events.jsonl ... The log is the source of truth." The event log holds the
  register at birth: index_events.jsonl:8183-8184, ts 2026-10-01T22:41:58Z (= 18:41:58
  EDT, the file's write moment), op register + autoseal, sha256
  33ad2a6d416f8ba496a4a5f1c8b0213468e0cd87cf7503215cc45ea13170e4ec, writer md-record-seal.
  The derived INDEX.json (mtime 18:00:56) predates the file by 41 minutes; its 0-hit is a
  stale derivation, not an indexing absence. Subdir files are indexed normally
  (48h_synth/STORY.md, burn_reset_20260927/work/... present in INDEX.json), so no schema
  exclusion applies. The lens's own blind spot #3 ("could understate ... I grepped, I did
  not parse its schema") is exactly where it broke. The "violates the contract it
  enforces" framing dies with it: the register was sha-bound into the shared surface at
  birth. Ironic coda: the lens's own reports were event-logged at birth by the same
  mechanism (moonshot-1 registered 2026-10-02T02:50:53Z).
- CONFIRMED legs: the register has no status column and no re-verification loop (read in
  full, zero status mechanism); olm-mine.dwf.ts is unamended (`grep -in INDEX` = one
  match, `indexOf` at line 259); the heal content is real (register.jsonl = 2,
  percolator_candidates.jsonl = 1, quantization-compression.md = 2 hits in INDEX.json;
  INDEX.json mtime 18:00:56 follows the day-2 heal commit 2093ca518 at 16:44:35 EDT).
  The proposed tools/gap_register_check.py survives as the right move; the "one
  sanctioned-writer run to index gap_analysis_20261001/" half is moot (already in the
  log; the next derivation picks it up).

## Additions (what the lens missed)

1. F6 IS FALSIFIED NOW, UNSTAMPED. watch/inbox/48h_synth/next.md:260-263 pre-registered:
   "logs/estate_walk_daily.log gains END lines with exit=0 for the scheduled fires of
   2026-10-01 and 2026-10-02 ... Falsified by: a missing END line ... or an
   ESTATE-WALK-BAKE-FAILED line in memory/attention.md (either way 'green cadence' is
   dead)." The 10-01 09:15 fire produced no END line and no alarm line (iconv of the log
   shows only the two smoke ENDs; attention.md grep = 0), so the 48h card's own
   falsifier condition has been met since 10-01 09:15 and no artifact in the chain
   (card, register, lens) stamps it. The 10-01 leg is permanently unrepairable: a fire
   cannot retroactively emit END. Falsifier: a stamped F6 verdict (or a retro-documented
   re-fire under a simulated System32 CWD) would close it. Move: 15 min, stamp F6
   FALSIFIED-10-01-LEG in next.md's falsifier ledger and note the 10-02 leg as the live half.
2. ALARM CHANNEL NEVER PROVEN. attention.md carries zero ESTATE-WALK lines ever (grep
   exit 1), so the rank-1 fix's proof is success-channel-only and fill 1's injected-
   failure proof of BOTH channels is undone. Falsifier: one injected-failure hand run
   that lands an "ESTATE-WALK-BAKE-FAILED" line in attention.md. Move: 10 min, inject,
   run, grep, then stamp rank 1 FIXED-PENDING-FIRE with both channels green.
3. RANK 2'S CLOCK HAS NO PROVENANCE. The card's own falsifier
   (.agents/skills/elder-lens/SKILL.md:37-38) is "a lens is dead if no organ acts on its
   question within one week - the question ledger's answer-rate is the lens's own
   meter": no date anywhere. The "~10-02" appears first as a hedge in the a05 lane
   ("window closes ~10-02", lanes/a05-ractor50.json), survives into the register
   ("before ~10-02", GAP_REGISTER.md:95), and hardens into the lens's "hard clock
   (~10-02)". The meter organ itself, the question ledger (SELF_STEAL_DEEP 2026-09-18
   per SKILL.md:10-11), is not locatable at state/, queue/, or watch/ standard paths.
   The urgency that makes rank 2 "TOP SEVERITY NOW" rests on an unverified derivation.
   Falsifier: the question ledger surfacing with a different window start (the card's
   git birth is 2026-09-18 02:27, 66a69c3db; one week from THAT is ~09-25, already past,
   which would make the card dead rather than dying). Move: 10 min, locate or declare
   OWED the question ledger, and restate the rank-2 clock as its literal one-week form.
4. THE ELDER WORK EXISTS UNBANKED. queue/lanes/elder/surface.md (35,198 bytes, mtime Oct 1
   08:00) holds fresh elder-voice synthesis (surface.md:49 measurement back-action,
   :95 the falsifier-gate 60.7% datum, :264 where the loop closes); a05 knew this ("a
   35KB elder surface.md + trail.jsonl went active Oct 1 08:00 but the falsifier organ
   is the inbox"). The missing piece is a pointer row in inbox.jsonl (the lane's
   tri-state receipt organ), so the "20-minute write" cure is plausibly a 2-minute
   pointer write and "0 bytes of progress" measures the pointer file, not the work.
   Falsifier: surface.md's new material turning out to be curated input rather than
   lens output would restore the 20-minute cost. Move: 5 min, bank the pointer row.
5. REGISTER QUOTE FIDELITY VERIFIED (blind spot #1 closed in the register's favor). All
   five load-bearing quotes grep -cF = 1 in their lane files: "scheduled on zero
   surfaces" (a06-spiking.json), "a third shape the falsifier battery did not name" and
   "it is the synthesis' one number that fails a byte check" (a08-48h-synth.json),
   "zero-hit grep is a finding: the wave never folded to corpus/steal"
   (a07-localfirst.json), "ZERO OF THE 18 SKILL VERDICTS' CONCRETE ACTIONS WERE
   EXECUTED" (a05-ractor50.json). The register's provenance section is honest.
6. DERIVED-VIEW VS EVENT-LOG SPLIT IS THE REAL RANK-8 DISEASE. The day-2 heal (INDEX.json
   mtime 18:00:56) and the register's birth event prove the shared surface's truth
   lags its log: writers append events at write time, the derived INDEX.json catches up
   later. Any patrol that greps INDEX.json measures the lag, not the index. This is a
   sharper statement of rank 8 than either the register's or the lens's phrasing.
   Falsifier: a day-3 olm run whose events append but whose derived view still omits
   them after the sanctioned writer runs would falsify the lag framing and restore
   "indexes never again".

## Dogfood roll-up (the topic's questions)

- Still real: ranks 2,3,4,5,6,7,9,10,11 byte-verified untouched; rank 12 surface-real,
  box state OWED (not run: any off-repo RX 5600 XT check; no access from this session).
- Already fixed: rank 1 code-fixed and success-smoked (alarm channel and scheduled-fire
  proof still open); rank 8 symptom-healed in the derived view (workflow law unamended).
- Misranked: rank 2 leading the S1 band is directionally right but its clock is
  unproven (Addition 3); rank 1's row was born stale in its own landing commit.
- Dominant meta-gap: MINED-NEVER-SCHEDULED stands as the register's own diagnosis and
  the commit message's; the lens's "the register is its newest specimen" is premature
  on the real (2h) timeline. The honest current claim: zero fills fired in the register's
  first evening except the rank-1 fix that rode the landing commit itself.
- What the register missed: F6 already falsified (Addition 1), the never-proven alarm
  channel (Addition 2), the rank-2 clock's missing provenance (Addition 3), the unbanked
  elder material already on disk (Addition 4), and the encoding defect that blinds the
  log channel the register's own rank 1 depends on (finding 2, confirmed).

## Checks not run

No test suite, percolator run, or pre-push gate was run (none named by the ask); the
rank-12 RX 5600 XT box state is unverifiable from this session and stays OWED; the elder
question ledger was searched at state/, queue/, watch/ shallow paths and by grep across
.agents/skills/ and watch/RESEARCH_LANE_ARCHITECTURE_20260904.md and was not found (its
absence as a file is itself a candidate gap, stated in Addition 3 as unverified because
the ledger may live in a receipt document this pass did not locate).
