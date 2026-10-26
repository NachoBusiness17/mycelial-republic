# OUROBOROS R3 (TRUST INSTRUMENTS): COMMUNICATION LENS FOLD (2026-10-05)

Lens: relay auditor. The question this seat asked of every instrument: what does
the operator RECEIVE (exit code, table, ledger row, fold section) versus what the
instrument actually CHECKED. The R1/R2 lessons (vacuous G8 headers, lengths-not-
values fold, case-blind seal compare) are all one disease in this lens: the
channel says CERTIFIED while the check walked a proxy. This round found the same
disease one layer up: in the artifacts the instruments already wrote, in the
ledger columns they journal, and in the no-data-vs-measured-zero rendering of
their tables.

Moment law: every number below was measured this sitting (2026-10-05, roughly
14:40 to 15:10 EDT) on a live tree; the seal ledger and daemon files moved
between my own runs and are named as moments, not constants.

## SEAL PATROL ADJUDICATION (the ask's explicit ask)

The ask's "10 real drifts" is the R2-close moment. My rerun this sitting:
`./.venv/Scripts/python.exe tools/prepush_seal_patrol.py --rows 1000` exit 1,
11 drifted (336 distinct, 316 match, 9 missing-on-disk per the a12 law). Sibling
lenses read 12 at their moments; the count oscillates with ledger appends.

Adjudication, every path measured against the FULL unwindowed ledger (latest row
per file, anywhere in the ledger) plus a CRLF/LF-normalization probe plus git:

- ZERO of the 11 is a window artifact: every file's true latest ledger row (not
  just the in-window row) still mismatches its bytes.
- Line-ending hypothesis REJECTED: sha256 of raw, crlf->lf, and lf->crlf
  variants of every drifted file match no sealed sha (the harness Edit-tool
  normalization documented at tools/prepush_workflow_metadata.py:37-39 is not
  the cause).
- 3 of 11 are live-daemon churn (STEALTH_SWEEP_LATEST.md, PACK_OFFLOAD.jsonl,
  STEALTH_MINED_FINDINGS.jsonl): sealed by register ops at 12:09Z, appended
  since, re-registered again between my runs (matched at my window-150 run,
  drifted again at my final probe). Oscillating race class, self-healing only
  when the register writer next fires.
- 8 of 11 are static post-seal movements: frontier_olm_2026-10-04 sweep and
  steal mds, RECEIPT.md, eleven-doors/DOORS.jsonl, ribvault r06_free_probe.py,
  r2-gaps/moonshot-1.md, frontier_olm_2026-10-05/lens/laws.md, and
  corpus/steal/MASTER_EXECUTE_REGISTER.md. Authorship is benign (owning writers,
  consistent with the economics lens 12/12-benign read) BUT all 8 are git-clean
  in the working tree (git status --porcelain empty on all 8): the drifted
  bytes are COMMITTED. No matching re-seal row exists anywhere in the ledger.
  These will read DRIFT on every wide run forever; nothing heals them.
- The operator-visible default window (150, what githooks/pre-push:503-515
  fires) showed only 2 of the 11 at my moment. The channel that reaches the
  operator surfaces 18 percent of the real drift; the WARN never blocks.

## RANKED BLINDNESS TABLE

Rank 1 (blast radius: the width-law crash class; operator reads "compliant").
Instrument: tools/workflow_gate.py G8 + memory/workflows/FIRE_LEDGER.jsonl.
Fooling shape: CONVERGENT with all three sibling lenses on G8 (probes A and B
both PASS exit 0 this sitting: camelCase/variable width evades
G8_MAX_CONCURRENCY_RE tools/workflow_gate.py:176; envelope stamp validated by
os.path.isfile only, tools/workflow_gate.py:189-192; my probe B named
watch/inbox/INDEX.json and unlocked mc 50). MY DELTA, the relay layer: the live
fleet carries width ONLY as comment stamps ("// max_concurrency: 3 ... the
firer still sets it at run time", .zcode/workflows/mickey17-burn.dwf.ts:48 and
18 siblings; the-gala.dwf.ts:11 says outright "Width rides max_concurrency on
the run, NOT in asks"), so the FIRE ledger (R1 row 7, built to join width to
script identity, tools/workflow_gate.py:495-505) journals the COMMENT: 2 rows,
both mc=3 parsed from stamps, while the fired width is set at CreateWorkflow
dispatch outside the gate's view. A declaration ledger wearing a fire-ledger
name: the operator receiving "verdict PASS mc=3" cannot tell declared from
fired. Cheapest probe: already fired this sitting (probe A/B PASS; ledger
census Counter({'3': 2})). Fix: stop minting width rows from script text; join
the harness fire payload's real max_concurrency (the docstring itself says the
journal's fire payloads are width-less and need this join); until then rename
the column declared_max_concurrency so the channel stops over-claiming.

Rank 2 (blast radius: steal-promotion decisions read "clean fold").
Instrument: tools/mickey17_v2_fold.py + the FOLD_SECTIONS.md artifacts + the
tier-2 ceremony. Three blindnesses, one layer:
(a) ARTIFACT LAYER (mine, novel): the de-blinded fold only ever ran on the exec
archive. 4 of 5 FOLD_SECTIONS.md carry no folded_at stamp (census this
sitting: exec=1, all others=0) and communicate the blind ancestor's numbers.
Sharpest: memory/runs/mickey17_v2/runs/2026-10-04-0/FOLD_SECTIONS.md:40 prints
"excluded: 0" and :42 "60 = 60 + 0" while that run's own *.checks.json carry 5
unconfirmed deep_tier2 verdicts, ALL 5 of which join lane rows (probe
replicated the fold's exact deep_keys logic, tools/mickey17_v2_fold.py:339-342).
The de-blinded fold would print included 55, excluded 5. An operator reading
that fold today reads "clean". (b) CRASH-KEY GRAMMAR (mine, novel): the
ceremony's own crash handler mints row_key "<lane>: crashed"
(.zcode/workflows/mickey17-v2.dwf.ts:263), a shape that can NEVER equal
"<lane>: <first six claim words>" (:164, the only join the fold walks);
proven in-memory this sitting: crash key joins a real claim row = False. Every
crash-path verdict is a structural orphan; a crashed row rides included and
"9 verifier-crashed (deep_tier2)" can never fire from the crash path. Latent
today (0 crashed verdicts in the 5 archives censused) but proven from the two
codebases' bytes. (c) join coverage: 9 of 59 exec rows match any deep_tier2
row_key (CONVERGENT with economics finding 2; my census: run-0 6 of 16
orphaned, exec 3 of 12, 2026-10-04-0 1 of 12, gap-analysis 1 of 12) and the
fold has no orphan counter. Cheapest probe: already fired (all censuses this
sitting). Fix: rerun the de-blinded fold over all 5 archives in the R3 landing
commit (the folded_at stamp versions them); fix the crash row_key to carry the
claim prefix; add a join-hit-rate line where a deep_tier2 entry matching zero
rows is an integrity error, not silence (operations lens proposed exit 2).

Rank 3 (blast radius: the receipt trust anchor silently stale).
Instrument: tools/prepush_seal_patrol.py + watch/inbox/index_events.jsonl.
Fooling shape: CONVERGENT with accuracy (perpetual red) and operations (ledger
self-authenticating: a forged re-seal row erases drift); my deltas are the
adjudication facts above: full-ledger re-check (no window artifact), CRLF
rejection, the 8 static drifts are committed git truth no one re-seals, and
the default window surfaces 2 of 11. Cheapest probe: already fired. Fix:
re-seal-on-commit rule in the owning writers (a board that moves after its
seal re-seals in the same write); split the live-append churn class from the
closed-board class (accuracy's sealed-prefix test); raise the default window
(window 1000 hashed 336 files in seconds this sitting; the 1.81 GB cost law at
tools/prepush_seal_patrol.py:23-27 is a full-ledger cost, not a 1000-row one).

Rank 4 (blast radius: cache economics decided on 96.6 percent nominal).
Instrument: tools/cache_kpi.py. Fooling shape: CONVERGENT with economics
finding 3 (zero receipt stamps, recv_tok 0 everywhere; my census: 0 stamped
rows in BOTH logs, provider_usage 77716 rows, flight_recorder 1456). MY
DELTA, the relay: the default resolution prefers logs/provider_usage.jsonl
(tools/cache_kpi.py:48-51) while the receipt producer stamps
watch/flight_recorder.jsonl (mag/flight_recorder.py), so even when callers
wire, the DEFAULT operator read never sees the stamps; and the human table
renders the absence as MEASURED zero (recv_hit% 0.0, printed by _fmt_rate at
tools/cache_kpi.py:198-199 because the denominator exists) with no
receipt_rows column in the table header (tools/cache_kpi.py:244-246) to say
"no data" - the JSON carries receipt_rows, the channel the operator reads
does not. Cheapest probe: already fired (both runs this sitting). Fix: KPI
reads both logs or the producer stamps the primary log; recv_hit% prints n/a
when receipt_rows=0; add the receipt_rows column.

Rank 5 (latent; no live caller found in mag/ or tools/ this sitting).
Instrument: mag/consensus_gate.py. Fooling shape: CONVERGENT with accuracy
finding 1 (N=1 returns CONFIRMED at 27B; refusal strings confirm); my delta:
empty responses are FILTERED before the unanimity test
(mag/consensus_gate.py:86), so verdict(['', 'x'], model_params_b=30) =
CONFIRMED - a crashed-empty witness vanishes rather than counting against
consensus; plus the FORK: memweave.consensus_quality returns "single" (not
strong) for one voice (mag/memweave.py:178-182 verdict ladder) while
consensus_gate returns CONFIRMED - two instruments carrying the same CID law
with opposite N=1 behavior and no canonical named. The MCP mesh spec banked
yesterday will wire verify interfaces; whichever instrument it picks silently
decides whether one voice certifies. Cheapest probe: already fired
(python -c, outputs above). Fix: require >=2 non-empty responses; refuse
empty-crash strings; name the canonical instrument in both docstrings.

## R3 DRIVER AMENDMENT (round-4 relevant gap)

The R3 ask audited instrument CODE ("read current bytes"). The two worst
blindnesses this lens found live OUTSIDE the code: in artifacts the fixed
instruments never re-ran on (rank 2a), and in channels that journal or render
one thing while naming another (ranks 1 and 4). Amendment for the R4 driver:
every instrument amendment must carry (a) a BACKFILL PROOF: the amended
instrument rerun over its standing artifacts (old folds, live fleet scripts,
full ledger) in the same sitting, with the deltas filed as findings - a fix
that lands without recounting what the blind version already wrote is half a
fix; (b) a RELAY CONTRACT line naming, for each channel the instrument owns
(exit code, table, ledger row, section file), whether it communicates no-data,
declared, or measured - and rendering them differently (n/a vs declared vs
number); (c) a convergence check against the sibling lens folds before
ranking, since CONVERGENT findings outrank novel ones (this round: G8 was
independently derived by all four lenses).

## BLIND SPOTS (honest)

- I did not rerun the fold on the old archives (it would overwrite the ancestor
  artifacts mid-audit); the 55/5 recount is derived by replicating the fold's
  own deep_keys logic, not by a fold execution.
- I did not audit githooks/pre-push beyond grepping instrument calls; the
  hook's own plumbing (exit-code handling per tool) was taken from read, not
  from a live push.
- consensus_gate caller census was scoped to mag/, tools/, tests/ greps; a
  caller inside .zcode workflow text or outside the repo would be invisible to
  me (I did grep neither the skills tree nor the dashboard).
- citation_lint was read (check_anchor, tools/citation_lint.py:147-196) but not
  probed this sitting beyond noting the token-free-line skip (line 180-182);
  its hard-block classes are siblings' territory (accuracy finding 6, operations
  finding 5) and I did not re-derive those.
- The seal-patrol daemon-churn adjudication rests on three observation moments
  over ~40 minutes; a longer window could show the churn class is not
  self-healing as claimed.
