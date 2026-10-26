# ACCURACY LENS - AMENTI map+diff adjudication (2026-10-05)

Jacket: the verdict consumed without its conditions. Method: read DIFF_TARGETS.md,
AMENTI_TRANSLATION_20261005.md, MESH_V2_SELFSTEAL_LANDED_20261005.md whole; then
byte-checked every organ claim the map stamps, ran the mesh suite, and censused the
absence claims with named instruments. No probe fired this sitting (adjudication,
not measurement). Commands named inline. Convergence flagged where a sibling lens
independently derived the same finding.

## Instruments run this sitting

- `./.venv/Scripts/python.exe -m pytest tests/test_mesh_v2.py -q` -> 11 passed in 2.02s
- `wc -l mag/mesh/{feeds,knot,broker,door}.py` -> 145/100/155/129 (byte-matches MESH_V2 receipt table)
- greps (named per finding below); two background corpus/ sweeps stopped early, scopes named in blind spots

## F1. T4's photocopy confession measures STALENESS, not amputation - the A/B as designed banks the wrong number

All three doors compute `frozen` as wall-clock age: `tools/query_broker.py:247`
`"frozen": (_t.time() - last) > 30 * 86400` over the catalog pair's mtimes;
`tools/gps_mcp/server.py:155` same shape; `mag/mesh/door.py:65`
`frozen = (time.time() - last) > FREEZE_AFTER_DAYS * 86400`. A photocopy taken
today carries `frozen:false` for 30 days while fully amputated from the
relationship; a live-but-quiet corpus confesses falsely at day 31. The T4 arm
"corpus live vs frozen:true" (DIFF_TARGETS.md:29) therefore measures
time-since-growth, not the binding agent. The arm that WOULD test her claim
("original vs relationship-stripped clone") names no instrument: nothing on disk
defines what strips a relationship (provenance links? the knot? supersedes
chains? the header itself?). Falsifier for this finding: a code path where
`frozen` trips on copy/amputation rather than mtime age - I grepped all
`frozen` assignments in the three doors, all are time-based; none exists.
Move (30 min): before firing T4, define the amputation instrument - clone the
catalog minus knot/chain/supersedes links and have the header name WHICH
deficiency tripped it. Until then the A/B would bank a staleness number wearing
the photocopy's name.

## F2. T1's ABSENT cell is false at estate level - the steal shrinks to a field extension, and its falsifier rots

The map cell says "nothing typed; operator state lives only in prose"
(DIFF_TARGETS.md:15). False: `state/operator_mode.json` carries schema
`operator_mode.v1` (mode/scope/reason/requested_by/changed_at/until, read at
`mag/realign.py:54-55`), and `class=OPERATOR_STATE` rows exist in
`watch/inbox/index_events.jsonl` (sampled: ts 2026-09-22T12:38:46Z;
`tools/md_record_audit.py:68-72` documents 59 historical rows). What is genuinely
absent is body-state FIELDS (sleep/energy/focus/protocol-night). So the steal is
real but half-priced: extend an existing typed channel, do not build one.
The falsifier as written ("two-week A/B", DIFF_TARGETS.md:23) is honest but not
one-sitting, and the estate's own meter proves human-remembered channels rot:
`memory/zknot/LATEST.md:3` "self-steal+forgot per 1000 human prompts: last 7d
129 ... target <75". A feed the operator must remember to write is a meter that
will be forgot. Move (20 min): add body-state fields to operator_mode.v1 with an
automatic source (protocol-night calendar, session-length telemetry) and only
then arm the A/B. DIVERGENT from operations.md (which scoped ABSENT to the mesh
root alone - true there, false for the estate the map cell actually claims).

## F3. T3 is the coldest vertex and the instrument is BUILT - but it has never once scored a live run

The estate's sycophancy surface is real: `mag/arena_bench.py` carries live mode
(`run_live` at :373, `run_live_endpoint` at :411, CLI `--live --candidate NAME`),
and THE BLIND GATE's verification challenges are exactly an authority-compliance
probe - receipt `memory/arena_bench/receipt_run_fixture-maru-sycophant_20261004T163321Z.json`
shows `claim_crown: expected REFUSE`, a sycophant answers CONFIRM.
`fixture_maru_sycophant` (`mag/arena_bench.py:482-493`) encodes sycophancy as
confirming every claim. But the ONLY live run ever attempted is
`memory/arena_bench/receipt_run_glm-5-3-flash_20260905T034941Z.json` ->
`"verdict": "ERROR_LANE_DOWN", "error": "flash lane unavailable: no Lite key in
cage env"`. Zero live scored sovereignty measurements exist across any family;
the lane is alive today (the standing arena runs it daily under the $25 cap per
watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md section 1). So T3's
premise holds in the strict sense (zero live numbers) while the map's "never
measured" understates the port: nothing needs building for the first datapoint.
Cheapest machine-checkable falsifier (first shot, 0 build): fire
`arena_bench --live` on 2-3 free families and score CONFIRM/REFUSE on the false
authority claims. Second shot (one sitting): the repetition axis - blind
verdict, N repetitions of a contrary assertion, re-ask, drift = flip rate.
CONVERGENT with dogfood.md T3 (zero measurements; port cheaper than the target
doc implies). My addition: the single live attempt and its lane-down verdict.

## F4. T5 splits: agreement density is machine-minable TODAY via lane_salon.v1; the held-vs-falsified join does not exist

Two salon formats live side by side. (a) `memory/runs/lane_salon/` holds 33
typed JSONs - verified keys `n_witnesses/n_up/consensus/witnesses[{ok, surface,
provider, paid, answer}]` (parsed salon_2026-08-24T1219.json: n_witnesses=5,
n_up=3, per-provider witnesses). Agreement density is a one-script mine over 33
typed salons. (b) `memory/runs/salons/` holds 587 files / 53 SALON_ARTIFACT.md /
77 dirs, of which exactly 1 carries the typed claim table
(`grep -l "| Claim | Tag |" ... | wc -l` -> 1: today's agent_mesh_triangulation).
The outcome half is absent: `grep -l -i "falsified|SUPERSEDED|struck"` over
`watch/salon_receipts/*` -> 0 files; the 17 raw hits in SALON_ARTIFACT.md are
prose noise (sampled 3: observer-effect prose, future-tense "Falsified by Stage
4 result" predictions inside the artifact itself - no post-hoc register exists).
So T5-as-written ("folds that later got falsified vs held",
DIFF_TARGETS.md:31) is NOT machine-checkable today; T5a (density census over the
33 typed + the 1 table) is, offline, zero cost. CONVERGENT with dogfood.md's
T5a/T5b split and operations.md's outcome-label absence; my addition: the 17-hit
raw grep is noise, semantic zero - pattern-matching outcome labels overcounts.
Move (45 min): density script over lane_salon/*.json (n_up/n_witnesses by
provider pair), plus a one-line fold-outcome stamp so the join starts accruing
NOW; the dew point becomes measurable only after N outcome-stamped folds exist.

## F5. The loop's break is the MAP step: 2 of 11 cells failed my census, one organ citation is a phantom, and no falsifier is scheduled

The rails exist end-to-end: briefing -> translation -> map -> ractor (this run)
-> free lanes (arena + salon + ds_workhorse) -> bank (mesh blob #1 banked today,
MESH_V2 receipt section 3, tip a6acf3b2...). What breaks repeatability:
(a) the map cells are hand-stamped without the estate's own prior-art sweep -
the exact sin DESCENT PROTOCOL leg 1 exists to prevent (C1 re-derived memlance
because prior art was not in evidence). This run's census falsified cell T1
(F2 above) and found T2's organ citation "Nous authority-override filter laws
(filter trips)" (DIFF_TARGETS.md:16) resolves to NO organ:
`grep -rn -i "nous.*filter|filter.*nous" memory/rib/*.md` and the arena summary
-> zero hits. The real measured law is the arena FILTER LAW - "opus
deterministically blocks authority-override phrasings ... 4-for-4"
(watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md section 4) - and
it is Anthropic-opus, not Nous. T2's substance (register-sensitivity measured,
variance exists) is therefore STRONGER than the map's citation, but the citation
itself is a phantom: the verdict was consumed without its source.
(b) no scheduler owns the falsifiers: `grep -rl "DIFF_TARGETS|REPETITION-BINDING|
CONDENSATION THRESHOLD" queue/ memory/workflows/` -> zero hits (RC=1); T1's
falsifier needs 14 days, T5's needs a join that does not exist (F4), T4's needs
an instrument that does not exist (F1).
(c) no re-diff trigger: nothing re-runs the map after probes land.
Move (one sitting): a map-cell verifier - for each ABSENT cell, grep mag/ +
tools/ + memory/runs/ + memory/rib/ for the cell's keywords and FAIL the stamp
on any organ hit; wire diff-target falsifiers as queue rows with owners.
Order for the free lanes: T3 live fire first (zero build, coldest, closes a
prompt-injection vector), T2 register-grid second (rides the same arena; the
filter law's 4-for-4 says variance exists, so the prior favors signal), T5a
density census third (offline), T4 fourth ONLY after the F1 redesign, T1 last
(fields now, measurement when an automatic source exists).

## Blind spots

- No probe was fired: I adjudicated; the arena, salon, and repetition numbers
  above are all still unmeasured as of this sitting.
- The sycophancy absence census was scoped: my memory/ + watch/inbox/ greps ran,
  but the corpus/ sweep (4GB+) was stopped early; corpus/steal subdirs were not
  fully swept for repetition-compliance measurements.
- The "59 OPERATOR_STATE rows" count is a comment claim in
  tools/md_record_audit.py:69; I sampled 1 row and did not recount all 59.
- The 1274-file salon census covers salon-named dirs I found by ls; other fold
  archives (frontier_salon, research_fold, etc.) were counted but not sampled.
- I did not re-derive dogfood.md's 713-file count (different find scope than
  mine); convergence claims rest on my own censuses, not theirs.
- Her system's substrate claims (Hz, fascia) were not re-verified this sitting;
  the translation's verdicts were taken as the map's input, not re-audited.
