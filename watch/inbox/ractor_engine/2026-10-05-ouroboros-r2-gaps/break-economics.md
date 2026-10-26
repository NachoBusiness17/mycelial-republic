# BREAK-ECONOMICS: hostile pass on the R2 gap-surface economics lens (2026-10-05)

Filed by the break-economics seat (ouroboros R2 of 5, the gap surface). Every
byte below was read or run this sitting, 2026-10-05 ~12:19-12:35Z, instrument
named per claim. The lens report under the knife: the economics.md filed in
this directory (4 findings, 5 blind spots, text truncated mid-finding-4's
falsifier in the handoff copy; the truncation is noted where it bites).

## VERDICTS

### Finding 1 (fold cannot count tier-2 verdicts; exec fold not fired): CONFIRMED

Every evidence leg re-verified byte-for-byte:

- `tools/mickey17_v2_fold.py:181` reads `for x in (c.get("unconfirmed") or [])` (my Read this sitting).
- `grep -c "deep_tier2" tools/mickey17_v2_fold.py` = 0 (my grep this sitting). Zero tokens, whole file, untruncated count.
- mtime `2026-09-25T23:21:06Z` (my os.stat) = the lens's "Sep 25 19:21" in EDT. Unchanged.
- The runner persists under the `deep_tier2` key: `.zcode/workflows/mickey17-burn.dwf.ts:476` ("Append these tier-2 verdicts to ... under the key \"deep_tier2\"", my sed read; also :14, :330-331, :444-489).
- `memory/runs/mickey17_v2/runs/2026-10-05-exec/` holds ONLY `lanes/` at my read moment 12:19:56Z (my os.walk): 16 files = e01-e08 lane JSON + checks (e06 has no checks.json yet) + the e05 candidates file. No FOLD_SECTIONS.md. My read postdates the lens's ~07:00Z read by ~5h20m and the fold STILL has not fired, so the open-window claim survives a much later moment-read.
- Convergence x3 verified: R1 `SYNTHESIS.md:97` (amendment row 1), R1 `economics.md:104` (amendment row 1), and both addenda exist and carry the defect (`grep -c deep_tier2` = 9 in `watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md`, 13 in `watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md`, my greps).

Added nuance the lens underplayed: the fold's VERIFIER TABLE block
(`tools/mickey17_v2_fold.py:156-162`) counts EVERY list-valued key by length,
so `deep_tier2` entries DO surface in the printed verdict-count line; the
PRISMA half (`:179-191`) walks only `unconfirmed`. The instrument sees the
verdicts it refuses to exclude. Also: e12's lane task edits the same file
(unbound-aggregate check, `mickey17-burn.dwf.ts` e12 entry, my sed read), and
the lens's executor-fence on that coordination is correct.

One status fact this seat could NOT verify: whether dwfrun-e9656e14 is still
alive. Last lane mtime is 06:38:45Z (e06), ~5h41m silent at my read; the
ListWorkflowRuns tool is unavailable in this session (capability gap, error
"workflow_introspection_unavailable"), so liveness stays unread, not asserted.
Either way the fix window is OPEN and wider than the lens implied.

### Finding 2 (fleet probe battery blind to probe-field candidates): CONFIRMED

- `tools/free_lane_fleet.py:169` is byte-exact as cited: `fals = str(r.get("falsifier") or r.get("amended_metric") or "")` (my Read).
- I re-ran the exact selection logic (`probe_items`, `:158-187`) over the actual 29-row store this sitting: the last-12 window (lines 18-29) yields exactly 1 item (line 18, source DROP-SCHMIDHUBER-COMPRESSION); line 19 skips for MISSING CLAIM (its claim-shaped field is `amends`; `amended_metric` is present as a dict but `claim/title/id` are all absent); lines 20-29 (e05's filing, all ts 2026-10-05T05:22:33Z) skip for missing falsifier/amended_metric. The lens's count is right; its skip-reason label for line 19 was slightly off.
- Falsifier checked against bytes: all 20 `probe-` rows in the 40-row ledger are `probe-DROP-SCHMIDHUBER-COMPRESSION` (my full read of `memory/runs/free_lane_fleet/ledger.jsonl`); zero probe rows ever fired for any e05 candidate. No probe-carrying row has ever been reached.
- Worse than reported: the single-item battery is REPETITIVE. 20 of 40 ledger rows (50%) re-ask the same meta-row's falsifier across providers and cycles. Blindness plus repetition.
- Fix refinement: the one-line `or r.get("probe")` insertion makes the 10 e05 rows and (if filed) the 10-04 window rows probeable (both schemas carry claim+probe, my parses this sitting), but line 19 stays skipped unless the claim chain also gains `r.get("amends")`. State the skip knowingly or fix both chains.

### Finding 3 (transfer debt recurred: 10-04 window never reached the master store): CONFIRMED and STRENGTHENED

- `watch/inbox/frontier_olm_2026-10-04/percolator_candidates.jsonl`: 10 rows parsed, exactly 1 carrying AQLM (row index 8, my parse).
- `grep -c "frontier_olm_2026-10-0[34]" memory/percolator/candidates.jsonl` = 0 (re-run this sitting); my full read of the 29-row store confirms the newest window citation anywhere is 2026-10-01.
- e05's idempotence rerun is byte-backed: `memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/e05-transfer-debt.json:33` `{"n_candidate": 0, "n_dupe": 10, "n_promoted": 0, "store_rows_after_rerun": 29}`.
- The lens's own blind spot (schema not diffed, command shape assumed) is RESOLVED by my bytes, upgrading the move to executable-as-specced: the 10-04 rows carry `claim/estate_map/probe/source_url` (my key-census), which matches the sanctioned writer's documented intake ("the row's source_url / estate_map / probe (and area / card_path when the mine emitted them)", `mag/percolator.py:553-556`, my sed read) and matches e05's accepted input shape (`area/card_path/claim/estate_map/probe/source_url`, my parse of the e05 raw file). The banked command shape is at `e05-transfer-debt.json:5` (`-m mag.percolator --candidates <path>`), and `mag/percolator.py:977` carries the `--candidates` flag.
- THIRD stranding leg the lens missed: the 10-04 candidates file is ALSO absent from the shared-surface index. My python walk of `watch/inbox/INDEX.json`: entries matching percolator_candidates + 2026-10-04 = 0, while the 10-01 window's file has exactly 1. GAP_REGISTER rank 8's index-last disease (the register row: "fold writes last, indexes never again") recurred for exactly this file. The close should append the index step.

### Finding 4 (fleet ledger = research-lane disease, 40 rows, zero readers): WEAKENED (evidence confirmed, headline falsified, and the truth is more urgent)

- Zero-consumer claim re-verified in named scopes: `grep -rln free_lane_fleet` over `tools/ mag/ scripts/ tests/` = the tool, two pycache artifacts, and `scripts/free_lane_fleet_cycle.ps1` only (my census); `ledger.jsonl` is referenced in code only by its writer (`tools/free_lane_fleet.py:52`); no prose consumer in `watch/inbox/*.md`, `docs/*.md`, `memory/attention.md` (my grep, zero hits). A full-tree grep was launched but not completed at bank time (stopped; the scoped claim above names its scopes).
- Register row 9 cite confirmed: `corpus/steal/MASTER_READ_ESTATE.md:231` (feed-or-kill verdict shape). VeriHarness row confirmed: `memory/percolator/candidates.jsonl` line 17, falsifier present.
- BUT the headline "minting the research-lane disease on a 24/7 schedule" is falsified by bytes: the ledger's 40 rows all fall in ONE 14-minute burst, 06:47:58Z to 07:01:51Z (my full read), and every scheduled fire since then FAILS (see Addition A1). The fleet is not minting anything on any schedule; it is a broken task plus one hand-fired burst. A dead instrument outranks an unread one in urgency, which is why this is weakened, not killed: the evidence rows stand, the frame inverted.

## ADDITIONS (what the lens missed)

### A1. The 24/7 fleet is DARK: 9 consecutive ModuleNotFoundError fires since 07:33Z (the loudest one-sitting close on this surface)

`logs/free_lane_fleet.log` (full read this sitting): every entry from
07:33:04Z through 12:04:16Z, one per 30 minutes, reads `ModuleNotFoundError:
No module named 'tools'`. Cause by bytes: `scripts/free_lane_fleet_cycle.ps1`
names absolute `$py` and `$repo` but never `Set-Location $repo` before
`& $py -m tools.free_lane_fleet --cycle`; Task Scheduler starts it in
System32; `python -m` resolves modules from CWD. This is the EXACT disease
class repaired 2026-10-01 in `scripts/estate_walk_daily.ps1` (its header:
"PATH LAW (2026-10-01 repair): Task Scheduler runs this with CWD at
C:\Windows\System32, so every relative path silently failed"). The cure was
written into one script and the new script written four days later inherited
the disease. CONVERGENT with GAP_REGISTER rank 1 (a08-r3) and with the
fork-and-forget class R1 struck. Secondary defect in the same file: the
try/catch never sees a native rc=1 (python exits 1 without throwing), so the
script exits 0, `errors.log` stays empty, and `memory/attention.md` gets no
alarm; the estate_walk repair added exactly that alarm half and this script
did not copy it. Zero ledger growth 07:01Z to 12:19Z is fully explained.
Close (10 min): `Set-Location $repo` before the fire plus a
`$LASTEXITCODE` check that appends the alarm to `memory/attention.md`,
mirroring `estate_walk_daily.ps1`; receipt beside the log.
Falsifier: the next scheduled fire banking ledger rows past 40, or a log
stamp without the module error.

### A2. GAP_REGISTER exists; the lens's "not found" blind spot is falsified, and the register itself carries a stale-open row

`find . -iname "*GAP_REGISTER*" -not -path "./.git/*"` returns
`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md` (depth 4 from the repo
root, inside the lens's claimed maxdepth-4 scope; why its find missed it is
unexplained). My full read: ranks 2/3/4/6/7 carry FILLED annotations
(fillball-1001), but rank 1 (EstateWalkDaily red-and-silent bake) is
cured-by-bytes yet UNANNOTATED: `scripts/estate_walk_daily.ps1`'s header
names the 2026-10-01 repair and the founding receipt, and my head-read shows
the absolute-path shape live. That is the stale-owed drift class already
struck as defect N6 row a14#4 (`corpus/steal/MASTER_MICKEY17_V2.md:205`).
Close (20 min): annotate rank 1 filled with the script's receipt pointer,
then byte-check the still-unannotated ranks 5 (seal arming, operator half),
8 (index-last; partially recurred per A3/verdict 3), 10 (trio carry-forward),
11 (three tickets; SS-1's landing needs its own grep), 12 (Vulkan probe)
before any execution pass fires them. Falsifier: any of those rows already
annotated or independently landed.

### A3. The 10-04 candidates file is triply stranded, not singly

Folded into verdict 3's close: absent from the master percolator store (grep
0), absent from `watch/inbox/INDEX.json` (my walk: 0 entries vs 1 for the
10-01 file), invisible to the fleet battery (verdict 2's field gap). The
lens saw leg 1; legs 2 and 3 are this pass's. The one-sitting close is
finding 3's ingest + a 5-minute index step through the sanctioned
shared-surface writer.

### A4. The build-wave owed items got zero lens coverage and stay UNLOCATED (OWED, not asserted)

The ask's gap-source (2) named cache-receipt producer stamping, B1
already_inside 29 edges, and the uppercase-hex seal false-drift. The lens
report contains no finding on any of them. My receipt-hunt (grep over
`watch/inbox/ractor_engine/` R1+R2 dirs and the watch/inbox top level for
already_inside / cache-receipt / seal-hex shapes) found only THIS round's
lens prose discussing the terms, no owning owed-list receipt; the sole code
anchor for already_inside is `mag/knowledge_graph.py:239`. Neither open nor
closed by bytes this sitting. The fold must locate the owning receipt before
ranking these; asserting either state would be fabrication.

### Blind-spot verdicts (the lens's own five)

- BS1 (moment-read of a live run): fair, and extended by A1's log; executor liveness is unreadable from this seat (ListWorkflowRuns capability gap, named above).
- BS2 (10-04 schema not diffed): resolved by my bytes; verdict 3 upgraded to executable-as-specced.
- BS3 (GAP_REGISTER not found): KILLED by A2; the file exists inside the lens's claimed search scope.
- BS4 (mutating instruments not run): fair; none were asked of the lens. This pass also ran none (pytest, the fold script, gate --script mode, any ingest, any edit outside this receipt).
- BS5 (b2 producer call sites priced, not located): stands; A4 extends it to the whole build-wave owed list.

## CENSUSES AND INSTRUMENTS (what was actually run)

- probe selection simulation: python replication of `tools/free_lane_fleet.py:158-187` over the 29-row store, 12:19Z (1 item, 11 skips, reasons itemized above).
- consumer censuses: greps as named in verdict 4; scopes named per the quantifier law; full-tree grep stopped incomplete, no universal claim rides on it.
- fleet liveness: full read `logs/free_lane_fleet.log` (10 lines) + `memory/runs/free_lane_fleet/health.json` (providers alive, last_ok 07:0xZ; openrouter-free-1 at 2 consecutive fails).
- exec lane census: os.walk + mtimes of `memory/runs/mickey17_v2/runs/2026-10-05-exec/` at 12:19:56Z.
- store and window parses: full reads of `memory/percolator/candidates.jsonl` (29 rows), `watch/inbox/frontier_olm_2026-10-04/percolator_candidates.jsonl` (10 rows, keys censused), e05 raw candidates file (10 rows, keys censused).
- INDEX walk: python string-walk of `watch/inbox/INDEX.json`.
- Convergence greps: deep_tier2 counts in both addenda; frontier_olm_2026-10-0[34] count in the master store.

## THE ONE-LINE RANK FOR THE FOLD

A1 (broken cycle, 10 min, unblocks everything the fleet was built to sense)
> finding 2 + finding 3 + A3 (the candidate wire: read the probe field, file
the 10-04 window, index it; 20 min combined) > finding 1 (fold deep_tier2
walk, 30 min, fenced on e12, window still open at 12:19Z) > A2 (register
annotations, 20 min) > finding 4's residual (a real consumer for the ledger;
design decision, not a one-liner) > A4 (locate the build-wave receipt first).
