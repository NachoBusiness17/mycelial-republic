# MICKEY-17 v2.1 RUN SPEC ADDENDUM: `run-0` fire-4 state (2026-10-11 fold)

<!-- no em/en dashes in this file; plain hyphens only, per the seat law. Lane and fold quotes keep their own bytes; where a quoted source contains an em-dash, the quote is split into two byte-true substrings with the dash elided and marked. -->

Filed by the run's SPEC seat (phase 6), fourth filing. This file states what the run's own evidence changes in
`C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md`:
failure modes observed, section counts (independently reproduced), and a verdict on each of the seven laws in
practice. One file; no other estate file was written by this seat.

Supersession note, stated plainly: this rolling path held, until this overwrite, the 2026-10-10 third filing
(134-row state, fold `2026-10-10T06:41:58Z`), and that filing was **UNCOMMITTED**: `git log --oneline -3 --` this
path stops at `a7ca49be1` (the 10-04 second filing, 94 rows) and `git status --short` showed ` M` before this
write. Unlike the second filing (recoverable at `a7ca49be1`), the third filing's full bytes are NOT recoverable
anywhere: its E-ledger (E3-E37) is carried forward below, curated where still true, but its prose is gone. That
byte-loss event is itself this state's strongest E26 specimen: the run's record of record rode uncommitted through
two fires and a gate-repair wave and died at the next SPEC sitting. This filing covers the fire-4 state: 162 rows,
scripted fold `folded_at: 2026-10-11T03:29:41Z (script sha256 58bd72c79c6d)` (byte-checked; sha recomputed this
session = match), master fold `corpus/steal/MASTER_MICKEY17_V2.md` (mtime 2026-10-10 23:41:21 EDT) whose
supersession line reads "this fold rewrites the 2026-10-10T21:58:49Z fire-3 fold (which rewrote the 02:55 fold)
in place on both surfaces" (byte-checked). Row history of one run archive: 75 (10-03) -> 94 (10-04) -> 134
(10-10 06:41Z fold) -> 162 (10-10 21:58Z fire-3 fold) -> 162 (fire-4 verifier-layer refold 23:29:41Z, rows
unchanged).

- Run archive (estate absolute path): `C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/mickey17_v2/runs/run-0/`
  containing `FOLD_SECTIONS.md` plus `lanes/` (15 lane JSONs, 15 checks JSONs, helper/tmp scripts, one reserved-name
  `nul` file that mutated 72 -> 0 bytes at 23:44:18 local, AFTER fold and master, cause unknown). The whole
  `runs/run-0/` tree is UNTRACKED (`git ls-files` on it returns 0 paths; run this session) - the E26 consequence is
  priced in throughout: nothing in the archive is git-recoverable, including fire-3's overwritten `FOLD_SECTIONS.md`
  bytes and the seven pre-repair checks files.
- Evidence base for every claim below: all 15 lane JSONs and 15 checks JSONs read this session (venv-python
  structure walks plus full-text pulls of every load-bearing field), `FOLD_SECTIONS.md` (current, full),
  `corpus/steal/MASTER_MICKEY17_V2.md` (full read, fire-4 text), the spec, `tools/mickey17_v2_fold.py` (all 468
  lines read; sha256[:12] recomputed = `58bd72c79c6d`, matching the fold stamp), git queries on this path and the
  archive, and the checks this seat ran (section 6).

## 0. RUN STATE AT THIS FILING

15 fired / 15 landed / 0 landed-empty / 0 parse errors / 0 missing / 0 tombstones - and **every lane has now sat
four or more sittings**. Byte-checked sitting markers, one or more per lane: a01 "Flight 3 (read moment
2026-10-10T20:30-20:38Z) mined the post-flight-2 gap"; a02 "PASS 4 of the lane first fired 2026-10-04T03:11Z and
refired 2026-10-09T00:00Z"; a03 "third refire, confirmation pass on the frozen 47-dir corpus; first bank
2026-10-03; refire 2026-10-04; second refire 2026-10-09"; a05 "fire 4 repaired 11 keys that no longer hashed to
their own bytes after prior-fire source-string edits; all 16 now verify"; a06 "fourth pass; passes 1-3 banked 5
rows each 2026-10-03/04/09, all preserved verbatim below"; a07 "refire 3: wave-moment denominators now
COMMIT-PINNED, not moment-described"; a10 "fourth sitting: gap-mine + external fetch; first filing 2026-10-03T18:33
-0400, second 2026-10-04 00:27 -0400, third 2026-10-10 early"; a12 "Pass 4 of this lane (mickey17 v2.1 same-day
evening refire; passes 1-2 were 2026-10-03, pass 3 was this morning 01:09)"; a13 "2026-10-10 fourth fire (prior
fires 2026-10-03 + refire + same-day third fire; this fire mined the gap since the third fire"; a14's
`sitting_4_2026_10_10` dict opens "Fourth sitting."; a15's refire_of names its own same-day prior rollup.

**The numeral collision (E25 sharpened to a hazard):** the master's "fire 4" is the verifier-layer refold (23:29Z);
a05's "fire 4" is tonight's lane sitting (16:4x local); a01's "Flight 3" is ALSO tonight's lane sitting. The same
numerals name different events across the run's own records of record. Fold and lanes must count sittings from one
register (run-level fire number on every lane marker), or the divergence will eventually mis-join a citation the
way ordinals already do (2.2).

Tonight's waves, local times (EDT, -0400): lane JSONs landed 16:31:43 (a08) through 17:13:18 (a14), 42 minutes;
11 lanes grew by 28 rows (134 -> 162), four held at 5 and a14 at 7 with metadata growth only. Checks wave A
17:06:59-17:21:16 (8 lanes: a02, a13, a10, a11, a12, a09, a15, a14). Fire-3 fold stamped 2026-10-10T21:58:49Z
(17:58:49 EDT). Gate-repair wave B 23:09:17-23:27:14 (7 lanes: a08, a04, a05, a06, a03, a01, a07). Fire-4 fold
23:29:41; master 23:41:21. Honest width claim per Law 4: 15 lanes fired, landings spread over 42 minutes, checks in
two waves (14 and 18 minutes) six hours apart, concurrency never journaled (E32 stands).

**The headline event: the fold's JOIN-HIT-RATE GATE fired live for the first time in engine history.** a07's
checks file carries the repair receipt (byte-checked, two substrings with the source's em-dash elided between
them): "2026-10-10 gate repair (fold JOIN-HIT-RATE GATE, tools/mickey17_v2_fold.py:351-356): both deep_tier2
row_keys had been derived from this file's own tier-1 claim texts, but the lane rows at a07-fifty-wide-waves.json
carry re-fired wording, and the fold joins row_keys against lane rows' first-six-claim-words keys" [dash] "so the
unconfirmed exclusion was silently lost (exit 2)." The third filing (~17 hours before the repair) had named
exactly this fuse (E33: the day one of those producers writes `unconfirmed` with the same loose key, the fold
blocks); it fired the same day it was predicted. A gate-repairer seat re-keyed with a declared 1:1 evidence
mapping ("verdict and evidence fields are byte-identical to the pre-repair values; only the join keys moved.",
byte-checked) and fire 4 refolded clean. The engine's fail-closed layer has now been exercised in production, not
just proven in tests.

## 1. SECTION COUNTS, reproduced (162-row fold)

Every script-written number reproduced under this seat's independent recount (same rules: `rows` key or bare
array; `*.checks.json` and helper scripts excluded; FIDELITY field rules - non-empty - applied).

| Fold section | Fold says (byte-checked) | This seat's recount | Verdict |
|---|---|---|---|
| CASUALTY: fired / landed / empty / parse errors / missing | 15 / 15 / 0 / 0 / 0 | 15 files, all parse, all with rows | confirmed ("fired" still file-count-or-`--fired`; E22) |
| SCOREBOARD: rows | 162 | 162 | confirmed |
| estate_status | confirms-ours 67, new 47, we-have-better 29, owed 19 | same | confirmed |
| leverage | high 80, medium 75, low 7 | same | confirmed |
| FIDELITY | 159/162 (98.1%) | 159/162; misses = a03 rows 4, 5, 6 (`steal` absent) | confirmed; the SAME three rows as the 134-row state, fourth state carrying them (E36) |
| VERIFIER table | checks 5 (no 2, yes 3), deep_tier2 29 (same-chain-verified 1, unconfirmed 2, verified 26), rows 5 (no 3, yes 2), supports 54 (no 53, yes 1) | exact; decoded in 1.1 | confirmed |
| WIDTH-ECONOMICS | median 11, max 18, min 5; top-10 share 84.6%; duplicates 3 | 11/18/5; 137/162 = 84.6%; 3 groups, classified in 1.2 | confirmed |
| PRISMA | 162 / 162 / excluded 1 / 161, invariant HOLDS | arithmetic holds; the exclusion is REAL and load-bearing (1.3) | confirmed |
| TOP-K | 12 rows | 12 = a01 x8 + a02 x4; sort key (leverage, lane-id, row-index), `rank[:12]` | confirmed as sort; vacuous as ranking (E23) |
| URL LIVENESS | unique URLs: 6; fetched: 6; skipped non-public: 0; live: 4; dead/blocked-status: 2 | dead verdicts re-probed this session: one reproduces, one does not (1.4) | split (first partially-reproducing state; E21 refined) |

Sections present: CASUALTY HEADER, SCOREBOARD, FIDELITY, VERIFIER TABLE, WIDTH-ECONOMICS, PRISMA FLOW, TOP-K,
URL LIVENESS. **OPERATING ENVELOPE is absent from the fold and from the tool**: `grep -c "OPERATING ENVELOPE"` =
0 in both `run-0/FOLD_SECTIONS.md` and `tools/mickey17_v2_fold.py` (run this session). The spec's phase 4 still
requires it as one of the four A12 pipeline sections. E3 persists, FOURTH consecutive state.

### 1.1 The verifier table decoded

Tier-1 total: **64 verdicts (58 no / 6 yes = 90.6% no)**, riding three key names (`supports` 54: no 53, yes 1;
`rows` 5: no 3, yes 2; `checks` 5: no 2, yes 3). The no-rate eased from the 134-row state's 94.4% to 90.6% - still
saturated: on audit-genre compound claims the binary supports question answers no almost always, so tier-1's
demotion branch still cannot discriminate (E37 stands; the a07 method field now says the quiet part aloud:
"run-measurement conjuncts explicitly framed as this-ask checks ... are tier-2 material and cannot be
quote-entailed", byte-checked, ellipsis mine).

Tier-2: **29 `deep_tier2` entries over 19 unique row_keys** - verified 26, `same-chain-verified` 1 (FIRST USE of
that bucket in engine history: a04's REFIRE3 row carries one verified and one same-chain-verified verdict on the
same key), `unconfirmed` 2, both on ONE row (a07#1), both entries carrying the identical post-repair key. Entry
inflation is a new measured defect: merged/appended cycles double-count rows in the tier-2 denominator (a05 alone
carries 8 entries over 4 keys; 29 entries vs 19 keys run-wide). The fold prints entry counts, not key counts.

The join: the fold prints "- deep_tier2 join: 8/29 row_keys match a lane row; join-miss (verified, no exclusion
weight, labeled not fatal): 21" (byte-checked). Reproduced exactly under the script's own formula (norm = lowercase
+ whitespace-collapse, punctuation preserved; two candidate shapes per row at `tools/mickey17_v2_fold.py:341-344`).
The 8 hits: a02 x2, a04 x2, a05 x1, a07 x3 (including the unconfirmed that excludes a07#1). The 21 misses are all
verdict-value `verified` riding prior-pass claim wordings - E33's inert-miss census, unchanged in mechanism but
now with a live block behind it.

One master-prose defect, found by this seat: DISPUTED D0's sentence "The verifier table's 2 unconfirmed verdicts
both sit on this one row under its pre-repair and post-repair row_keys" (byte-checked) is inexact against the
bytes: BOTH entries carry the identical post-repair key ('a07-fifty-wide-waves: TALLY GAP re-verified across three
asks'); the pre-repair key ('a07-fifty-wide-waves: The burn-claims tally gap is real') survives only inside the
checks file's note prose. The exclusion itself is correct (one row, two verdicts, both unconfirmed); the
key-census sentence is not. Law 5's prose-around-script-numbers rule extends to key censuses.

### 1.2 WIDTH-ECONOMICS decoded

Per-lane rows: a01 18, a03 18, a04 17, a05 16, a08 16, a02 12, a10 12, a09 11, a11 10, a14 7, a06 5, a07 5,
a12 5, a13 5, a15 5. Top-10 share 137/162 = 84.6% is refire skew, not source concentration (the 11 lanes that sat
hold the mass; at width 15 an even spread floors top-10 share near 66.7%). Duplicate quotes: 3 (1.9% share), ALL
a15 pass-off re-quotes of sibling specimen rows (a15#0 of a03#16; a15#3 of a11#7; a15#4 of a09#5) - the
integrating lane quoting sibling evidence, which is its job. The 134-row state's through-master convergence pair
(a13#4 quoting the master quoting a07's source) is GONE: a13#4 reworded. E24 stands; E29 refined (the echo now
lives only in the pass-off class; the metric still counts the run's own register as duplication by design).

### 1.3 PRISMA: the first load-bearing exclusion in engine history

`excluded: 9 verifier-unconfirmed (deep_tier2): 1` - the excluded row is a07#1 (claim prefix "TALLY GAP
re-verified across three asks and CURED IN CODE"), excluded via a JOINED unconfirmed verdict; included 161;
invariant 162 = 161 + 1 HOLDS. Chain of custody for the whole pipeline: fire-2's excluded-0 was a wiring miss
(E20, cured in code 2026-10-05); the 134-row state's excluded-0 was genuine-but-empty; tonight an unconfirmed
verdict JOINED (after a gate block and a declared repair), excluded its row, and the master rules it
conditionally in DISPUTED D0: "the row stays excluded from the included set (PRISMA holds 162 = 161 + 1) until one
real fifty-wide wave pre-flights tools/fifty_wide_guard.py" (byte-checked). The verified half stands inside the
same ruling. This is the exclusion path working exactly as spec'd - including the near-loss that proved the gate.
The other standing codes remain unused as exclusion reasons (the audit-genre clause, E17, is still owed).

### 1.4 Fold moment, URL liveness, stray mutations

Fold postdates every archive write it counts (newest = a07 checks 23:27:14; fold 23:29:41; master 23:41:21). E7
holds across all four fold states. URL liveness SPLIT for the first time: the x.com verdict (HTTP 404, a09#8's
source) REPRODUCED on this seat's re-probe with the fold's own method (urllib, no-redirect opener, fold
User-Agent, 6s timeout, HEAD first) -> HEAD 404: the run's first true-dead confirmed by two independent
instruments. The deepseek verdict (HTTP -1) did NOT reproduce -> HEAD 302, live under the fold's own 200-399
rule: the -1 class is now 0-for-5 across four fold states and five probes (10-03, 10-04 x2, 10-10 02:41, this
seat). E21 refined accordingly: the disposition clause works (the master's negative-results row 2 dispositions all
3 citing rows - a05#9, a06#3, a09#8, verified this seat by source-field scan) and both deepseek-docs rows stand on
banked bytes (a05#9's source field: "(fetched via WebFetch, byte-checked via curl -sL, raw HTML 142,966 bytes,
grep hit '393216')"; a06#3's claim: "WebFetch cross-checked against curl raw HTML, 142,966 bytes" - both
byte-checked); but the -1 verdict class is the unstable instrument, and `url_checked_at` remains printed-as-rule
(`tools/mickey17_v2_fold.py:458`), stamped-by-no-code: 0 of 162 rows carry it (`grep -l` over the lanes dir = 0
files).

Stray datum, filed as observed, cause unknown: the lanes dir's reserved-name `nul` file mutated 72 -> 0 bytes at
23:44:18 local, AFTER both fold (23:29:41) and master (23:41:21). The archive mutated after its own fold, with no
journal to say who or why (E32's class; also a Windows reserved-name artifact the archive scanner must tolerate).

## 2. FAILURE MODES OBSERVED (against section 7's standing list)

### 2.1 Codes exercised this state

- **Code 1 phantom-source, three live instances.** The sharpest is new: a07's phantom LAW-carrier - "NEW finding:
  envelope_50w's claimed AGENTS.md law amendment never landed in any carrier" (byte-checked) - a claim of standing
  law where no law bytes exist; a code-1 specimen whose subject is the estate's own constitution file. a01's
  "Phantom-adjacent number: 'held to 35 cents' has no byte-exact ledger slice; filed as unbacked pending the
  operator naming its slice" (byte-checked). And the carried phantom ledger citation ("arena-sessions-v3") is now
  PAID: a13 reports "PAID SINCE THIRD FIRE (verified this fire): master erratum pointer landed (6 PARABLE_ERRATUM
  mentions, line 228 credits 'a13#1 steal, paid here', struck figures quoted AS STRUCK EVIDENCE)" (byte-checked) -
  a filed negative cured by the fold seat's own pointers, again outrunning the no-repoll defect (E15).
- **Code 2 premise-drift, three instances.** a01's carried "Premise drift inherited from the ask: 'cap behavior at
  $25.11' takes the parable's number as the cap" (byte-checked). a05's fire-4 verdict re-rules the founding
  comparison: "The 2026-10-03 comparison was NOT fair as fired" (byte-checked), now with the handicap measured
  (13/14 v2 outputs stopped at exactly 6000 chars; thinking forced off; max_tokens 2000). a11's leak-row premise
  flip (GitHub remote now exists) is carried and RULED in the master's D6 as a conditional pair.
- **Code 3 url-owner-rot, FIRST genuine instance in the run.** a09#8: "DEAD PRIMARY (fourth seat, 2026-10-10):
  LINKS row 351's canonical https://x.com/yifanzhang_/status/2101068650161807857" (byte-checked, row-level) -
  fold HTTP 404, this seat's re-probe HEAD 404, and the row's steal lands the DEAD_PRIMARY annotation with the
  fetch date. Prior states' code-3 silence had inverted the code (the unstable reading was the liveness pass
  itself); tonight both instruments agree for the first time, and the spec's disposition (dead URL -> negative
  result with status) executed end-to-end.
- **Code 7 quote-drift: no NEW instance.** The one catch in engine history stays a11's self-archived NEG
  ("PRIOR QUOTE CORRUPTION (second sitting, kept for the record)...", byte-checked, carried). The loop
  drift -> tier-2 catch -> repair -> re-verify remains 1-for-1.
- **Code 9 verifier-unconfirmed: exercised FOR REAL.** One row excluded, two unconfirmed verdicts, one live gate
  block, one declared repair (1.1, 1.3). The `crashed` bucket remains unused in engine history; `same-chain-verified`
  was used for the first time (a04).
- **Code 10 empty-estate-grep, recorded honestly, now with a consecutive-fire meter.** The master's negative row 7:
  research_polished zero-hit for 15 of 15 lanes, "standing negative at every audit moment (a15: fifth
  consecutive)" (byte-checked); a13: "memory/research_polished = zero-hit grep for all 8 receipt names at the
  FOURTH consecutive fire" (byte-checked); a10: "Rib-vault gap (sitting 3, re-confirmed sitting 4)" (byte-checked).

### 2.2 Code 12 moment-drift (E28): dominant class, third consecutive state, two NEW sub-classes

- The moving-tree law, a01: "any audit verdict issued without a moment stamp on this cadence is stale on arrival -
  the earlier flight's '8 of 41 unbanked' and this flight's '16 of 51' were both true and both superseded within
  hours" (byte-checked). a01 also files the erratum-as-multi-moment-document (a stale section-6 census living
  permanently above the close-state sections 7-9 in one file).
- a13: "FOLD DRIFT THIRD RECURRENCE: 13,682 log lines vs 13,418 fold events (264 behind)" (byte-checked) - the
  drift the prior fire measured at 284, regrown again; the tripwire steal is still not landed in refold_gate.py.
- a15: "TWO-CLOCK FOLD HAZARD (new tonight): the 02:55 master fold and the afternoon lane refires are ~14 hours
  apart" (byte-checked) - the master adopts it in FOLD NOTES and fire 4 IS the cure executed (a verifier-layer
  refold over unchanged rows closing the gap).
- NEW SUB-CLASS, ordinal-referent rot (the master's ORDINAL-REFERENT HAZARD): a04#15, row-level: "REFIRE3
  negative, citation drift: the dedupe gate's provenance pointer names MASTER_MICKEY17_V2.md section 9 GO item 2,
  but the current master's GO item 2 is 'Arena retirement receipts'" (byte-checked) - citations by ordinal rot
  when the cited list moves. The master's fix idiom is already in its own text: "quote the lane id + row index,
  never the ordinal." (byte-checked). This is E28's citation form and belongs in section 7 beside it.
- The numeral collision (section 0): master "fire 4" != a05 "fire 4" != a01 "Flight 3" - moment-drift applied to
  the run's own event numbering.

### 2.3 Code 13 fold-self-echo (E29): confirmed, refined

The 3 duplicate pairs are all a15 pass-off (1.2); the through-master convergence pair is gone. The echo's carrier
quote is again "flash lanes, each byte-checking one claim from 16 BURN_* filings." - a07#1's quote, re-quoted in
the master's D0 (byte-checked there), and again in this addendum's receipts: the run's evidence now recursively
cites its own most-audited sentence.

### 2.4 Codes silent

Zero instances this state: 4 walled-source, 5 barren-start, 6 fabricated-name-or-rumor, 8 unit-error at the lane,
11 scanner-under-coverage.

### 2.5 NEW CLASS: key rot (two species, one mechanism)

Prose-bound keys rot when sittings reword. Species 1: tier-2 row_keys - E33, fired live tonight (exit 2 + declared
repair, section 0). Species 2: phase-1 idempotency keys - a05: "fire 4 repaired 11 keys that no longer hashed to
their own bytes after prior-fire source-string edits; all 16 now verify" (byte-checked). The spec's phase-1 key
shape ("source URL + verbatim-quote hash") is the stable form; a05's rot came from source-string edits across
fires, and the repair idiom (recompute every key, verify all, declare the count) is the producer obligation the
spec does not yet name.

## 3. THE SEVEN LAWS IN PRACTICE (fire-4 state)

1. **CITATION-BINDING: HELD at the binding layer; its tier-1 companion is still saturated.** All 162 rows bind
   quotes (the 3 fidelity misses are `steal`-field misses, not quote misses); dedupe on normalized quote text
   worked (3 groups, all classified); no new drift. Tier-1 went 58 no / 6 yes (90.6%) - eased from 94.4% but still
   non-discriminative on audit-genre compound claims (E37); the producers now say so in their own method fields.
   The law's letter is sound; the tier-1 instrument still needs its audit-genre variant.
2. **NEGATIVE-FIRST-CLASS: HELD, strongest state.** Negatives filed in dedicated fields on every lane, with
   cross-sitting cure states in both directions: a10's "CURED 2026-10-04, re-verified 2026-10-10" idiom
   (byte-checked, twice, both instances carrying their sitting counts), a13's "PAID SINCE THIRD FIRE (verified
   this fire)", a11's REGROWTH finding
   flipping to cured at HEAD by d349ce7d2 with the cure self-receipting "Evidence: lane a02#1". a15 resolved its
   own prior stale-caveat: "STALE-LANE CAVEAT (scope honesty, resolved this pass)" (byte-checked) - E35's cure
   executed by seat practice (per-lane read moments in its method_note). Zero tombstones in the run's entire
   history; zero silent drops found. E15 (no negative re-polling) is being paid down by seat discipline, not by
   mechanism - the mechanism is still owed.
3. **CONTRADICTION-TIER: HELD.** Eight conditional rulings D0-D7 in the master's DISPUTED tier, each with both
   quotes and a conditional rule; no averaged merges anywhere in the archive. Cross-sitting self-correction is
   now the engine's idiom: a08's `errata_on_prior_rows` (7 entries) ruling its own prior rows stale on fresh
   census; the verifier's R92/R94 attribution correction folded into D3 (a06's verdict prose still says R92/R93 -
   the correction lives one layer up, correctly labeled "ATTRIBUTION CORRECTION ... folding forward"); a05's
   re-ruling of its own fire-1 comparison; a02's counterfactual re-ruling under the fixed carrier.
4. **ABSOLUTE-PATHS: HELD at row level; static defect unchanged; width receipt still unearnable.** Row sources
   are estate-absolute or http with provenance in-field. The spec itself still crowns the legacy archive path
   ("memory/runs/mickey17_v2/lanes/", 3 byte-checked occurrences) while the archive of record is `runs/run-0/lanes/`
   (E31, fourth state). Width claim filed as measured (section 0); no landing journal exists, so the journal-form
   receipt stays unearnable (E32) - and tonight adds the `nul` mutation as a post-fold archive change no journal
   explains.
5. **FOLD-BY-SCRIPT: HELD AND BATTLE-PROVEN - the fail-closed layer caught a real defect in production.** The
   JOIN-HIT-RATE GATE exit-2'd on a silently-lost exclusion at the fire-3 fold; a declared repair re-keyed it;
   fire 4 refolded clean; every script number reproduces under this seat's independent recount (section 1,
   including the join formula re-derived from source at `:341-344` and re-run). The A5b clause ("Phase
   byte-compares every fold and spec quote against the cited lane row; mismatch blocks filing", byte-checked) is
   what this seat executed - receipts in section 5. Standing script defects, all re-verified this session:
   OPERATING ENVELOPE code-absent (E3, fourth state); TOP-K alphabetical `rank[:12]` (E23: a01 x8 + a02 x4);
   `url_checked_at` printed-not-stamped (E21); the hardcoded screened parenthetical at `:430` asserting an
   invariant the fold's own FIDELITY line falsifies (E36); the rows-array monopoly hiding a06's two sidecar
   arrays (E34, now 10 invisible banked rows); NEW: the verifier table counts entries, not unique keys (1.1).
   And one master-prose defect (D0's key census, 1.1) - prose-around-numbers extends to prose-around-keys.
6. **WRITES-SERIAL: lanes HELD across four waves; verdict layer overwrote again - third recurrence - but now
   DECLARED.** Lane-private incremental writes worked: prior rows kept verbatim in-array (a01 flights, a08
   sittings), gap-mined appends (a03, a05), declared sidecars (a06's `prior_rows_20261009` + `prior_rows_20261004`
   - preserved but invisible to every count, E34). The shared-state violation class recurred with honest labels:
   a07 "Overwrites the prior pass file at this path" (byte-checked); a08 "Overwrites a prior check file at this
   path whose rows were a different, superseded row set." (byte-checked); a03 "Replaces the prior a03 CheckFile
   at this path (2026-10-09 row set, 5x no + 2 deep_tier2 verified) per this ask" - the a03 form is
   a partial cure idiom: declare the census of what was destroyed. The archive is still untracked, so the
   destroyed bytes are unrecoverable, and the master's 17 -> 29 verdict-growth claim is attested-only for the
   seven overwritten lanes (not independently verifiable; stated as such). Merge-never-overwrite remains a seat
   idiom, not a spec obligation.
7. **WIDTH-LADDER: minimum rung, fourth consecutive; the gate metrics remain degenerate at this shape.** Width
   15. Top-10 share 84.6% would fail the >50 gate on pure refire skew; dup share 1.9%, all pass-off echo; the
   gate's two numbers measure nothing they were built to measure at a 15-wide multi-sitting archive (E24). No
   429s, no usage windows, no casualty refires, no tombstones in any state of this run: the pacing and off-peak
   legs of Laws 6/7 and COST DOCTRINE remain untested by this run (fourth state running).

## 4. EDITS THIS EVIDENCE BUYS (the E-ledger, continued; spec changes this run pays for)

Carried from the prior filings, restated with current status:

- **E3 (OPERATING ENVELOPE) - stands, FOURTH state, grep-verified absent from fold AND tool.** Implement the
  section or strike it from phase 4; a spec section unwritten by its own tool across four states is drift.
- **E5/E20 (verifier-table blindness, PRISMA wiring) - CURED IN CODE, and tonight LIVE-PROVEN at full depth:**
  verdict-value splits printed, exclusion read from joined verdict VALUES, and the join gate blocking a real
  lost exclusion. Absorb the cure as phase-3/4 contract text.
- **E21 (liveness stability) - RECURRED and now SPLIT.** The -1 class is 0-for-5 (false-dead every time,
  including twice on the same deepseek URL); a true-dead (x.com 404) reproduced for the first time. Two probes
  before any demotion (the -1 class especially); implement `url_checked_at` stamping or delete the disposition
  clause.
- **E22 (fired/journal circularity) - stands.** `fired = a.fired or n_files` (`:249`, read this session); no run
  manifest `{topic, targets, width}` is archived anywhere in run-0.
- **E23 (TOP-K rank key) - stands.** `rank[:12]`, alphabetical within leverage; this fold's 12 slots = a01 x8 +
  a02 x4.
- **E24 (gate-metric degeneracy) - stands, fourth state.** Width-aware floor + refire-skew caveat; classify
  duplicates (pass-off / through-echo / convergence / gratuitous) before the <10% gate applies.
- **E25 (refire taxonomy) - stands, sharpened to a hazard.** The casualty language ("re-fired exactly once" for
  dead lanes) still has no name for the gap-mining sitting every live lane now runs routinely; tonight adds the
  NUMERAL COLLISION (master "fire 4" vs a05 "fire 4" vs a01 "Flight 3" naming different events) - one run-level
  sitting register must stamp every lane marker, or the numbers will mis-join citations.
- **E26 (checks-file persistence) - THIRD RECURRENCE, and it climbed a layer.** Checks files still overwrite
  (declared, this time); the fire-3 FOLD_SECTIONS.md bytes were overwritten by fire 4 with no git recovery; and
  the third addendum filing itself died uncommitted at this very write. Merge, never overwrite; COMMIT the
  archive after every fire; the a03 idiom (declare the destroyed file's census) is the minimum label until merge
  is contract.
- **E27 (quote-drift exercised) - stands as history.** Keep the law exactly as written.
- **E28 (moment-drift, proposed code 12) - strongest state; instances in 2.2.** Import B2-216 into section 7, now
  with the ordinal-referent sub-class (E39) and the numeral-collision specimen.
- **E29 (fold-self-echo, proposed code 13) - confirmed, refined to the pass-off class (1.2).**
- **E30 (review-verdict persistence) - persists.** `grep -c -i review` over the current master = 1, and the one
  hit is inside a quoted receipt ("the review body's foreign-lane notes below refer to that run"), not a phase-5
  verdict; accept/revise greps 0. The phase-5 gate ("SPEC may not start, and FILE may not run, without a
  recorded review verdict", byte-checked) remains unenforceable estate-side; a12's pass-4 gap carries "same
  workflow_introspection_unavailable capability gap as passes 1-3" (byte-checked). This filing proceeds on the
  workflow's in-flow review, which the estate cannot see - the standing finding, not an unnoticed one.
- **E31 (runs/<slug> layout) - stands, fourth state.** Spec line 9 still crowns the legacy top-level path as
  archive of record (3 byte-checked occurrences of the legacy lane path).
- **E32 (landing journal) - stands.** No journal exists; the `nul` 72 -> 0 post-fold mutation (1.4) is an
  archive change nothing explains.

New items from this state:

- **E33's prediction CONFIRMED LIVE (status change, not a new number):** the fuse fired the same day it was
  named. The spec's phase 3 must now (a) name the row_key shape as a producer obligation ("laneId: first six
  claim words of the CURRENT row text", exactly the tool comment's contract), (b) bind verdicts to idempotency
  keys instead of claim prose, or (c) require the repair idiom used tonight (re-key with declared 1:1 evidence
  mapping, verdict/evidence bytes unchanged). Any of the three; silence is how exclusions get lost.
- **E38 (idempotency-key rot).** a05 repaired 11 of 16 phase-1 keys that no longer hashed to their own bytes
  after prior-fire source-string edits. Bind keys to immutable row material (the spec's own "source URL +
  verbatim-quote hash"), recompute-and-verify-all at every sitting, and declare the repaired count in the lane
  file. Same mechanism as E33; different key species.
- **E39 (ordinal-referent rot).** Citations by position ("master GO item 2") rot when the target list moves
  (a04#15; the master's own T9 carries one). Section 7 should carry it beside code 12, and every fold's go list
  should adopt the master's own fix idiom: named lane id + row index on every item (this master already does).
- **E40 (two-clock folds and the verifier-layer refold).** Fire 4's shape - refold the verifier layer over
  unchanged rows to close a lane-vs-fold clock gap - is a legal and useful fold form the spec does not name.
  Phase 4 should name it (a refold must state which layer moved), require the supersession chain this master
  already writes, and note that a refold overwrites FOLD_SECTIONS.md in place, which is exactly why E26's
  COMMIT-after-every-fire leg is load-bearing.
- **E41 (verifier-table denominator).** The table counts deep_tier2 ENTRIES (29), not unique row_keys (19);
  merged cycles inflate the tier-2 denominator and can double-count a row's verdicts (a05: 8 entries / 4 keys;
  a07: the same row's exclusion rides 2 entries). Print both counts, or dedupe on key at fold time.

Tool-ahead-of-spec items to absorb at the next spec revision (all read this session in
`tools/mickey17_v2_fold.py`, sha-verified as the fold's own tool): the fold stamp + script sha (R1), the
verdict-value splits (R1), the join gate and unmapped-verdict bucket (R3), the FIRED-BELOW-ARCHIVE GATE
(2026-10-07), and the A14 `--check-master` unbound-aggregate gate. None are in the v2.1 text; the spec's phase 4
still describes a weaker tool than the one that runs - and tonight that tool blocked a real defect the spec text
cannot even name.

## 5. QUOTE BYTE-CHECK RECEIPTS (the A5b check, run by this seat)

Method: every quote in this addendum was checked as a fixed string against its cited file before filing, with
`.venv/Scripts/python.exe` raw-bytes `str.count`; the counts below are the post-write re-run. Row-level receipts
(quotes taken from a `rows[]` entry) are marked ROW. One quote (the a07 repair receipt) is filed as two
byte-true substrings with the source's own em-dash elided between them (the seat's no-dash law); both substrings
count 1.

Lane files (under `memory/runs/mickey17_v2/runs/run-0/lanes/`):

1. "Flight 3 (read moment 2026-10-10T20:30-20:38Z) mined the post-flight-2 gap" - a01-arena-cadence.json - 1
2. "Premise drift inherited from the ask: 'cap behavior at $25.11' takes the parable's number as the cap" - a01 - 1
3. "Phantom-adjacent number: 'held to 35 cents' has no byte-exact ledger slice" - a01 - 1
4. "any audit verdict issued without a moment stamp on this cadence is stale on arrival" - a01 - 1
5. "PASS 4 of the lane first fired 2026-10-04T03:11Z and refired 2026-10-09T00:00Z" - a02-dungeon-campaign.json - 1
6. "third refire, confirmation pass on the frozen 47-dir corpus; first bank 2026-10-03; refire 2026-10-04; second refire 2026-10-09" - a03-tavern-curve.json - 1
7. "The 2026-10-03 comparison was NOT fair as fired" - a05-delta-study.json - 1
8. "fire 4 repaired 11 keys that no longer hashed to their own bytes after prior-fire source-string edits; all 16 now verify" - a05 - 1
9. "fourth pass; passes 1-3 banked 5 rows each 2026-10-03/04/09, all preserved verbatim below" - a06-sacred-cow.json - 1
10. "WebFetch cross-checked against curl raw HTML, 142,966 bytes" - a06 ROW #3 claim - 1
11. "refire 3: wave-moment denominators now COMMIT-PINNED, not moment-described" - a07-fifty-wide-waves.json - 1
12. "NEW finding: envelope_50w's claimed AGENTS.md law amendment never landed in any carrier" - a07 - 1
13. "fourth sitting: gap-mine + external fetch; first filing 2026-10-03T18:33 -0400, second 2026-10-04 00:27 -0400, third 2026-10-10 early" - a10-ds-batches.json - 1
14. "CURED 2026-10-04, re-verified 2026-10-10" - a10 - 2 (both instances continue with their sitting counts:
    "(sittings 3 and 4): v1 artifacts are void-marked" and "by running the tests twice (sittings 3 and 4)")
15. "Rib-vault gap (sitting 3, re-confirmed sitting 4)" - a10 - 1
16. "PREMISE DRIFT ON THE LEAK ROW (row 4ac74d0f80): 'local-only exposure today (sole remote is a local disk path)' was true 2026-10-03 and false 2026-10-10" - a11-commits.json - 1
17. "PRIOR QUOTE CORRUPTION (second sitting, kept for the record): first sitting's row-1 quote read 'insertions(++)'; git's actual footer is 'insertions(+)' - corrected from fresh bytes; tier-2 checks.json had flagged it." - a11 - 1
18. "Pass 4 of this lane (mickey17 v2.1 same-day evening refire; passes 1-2 were 2026-10-03, pass 3 was this morning 01:09)" - a12-ractor-legs.json - 1
19. "same workflow_introspection_unavailable capability gap as passes 1-3" - a12 - 1
20. "2026-10-10 fourth fire (prior fires 2026-10-03 + refire + same-day third fire; this fire mined the gap since the third fire" - a13-receipts-census.json - 1
21. "FOLD DRIFT THIRD RECURRENCE: 13,682 log lines vs 13,418 fold events (264 behind)" - a13 - 1
22. "PAID SINCE THIRD FIRE (verified this fire): master erratum pointer landed (6 PARABLE_ERRATUM mentions, line 228 credits 'a13#1 steal, paid here', struck figures quoted AS STRUCK EVIDENCE)" - a13 - 1
23. "memory/research_polished = zero-hit grep for all 8 receipt names at the FOURTH consecutive fire" - a13 - 1
24. "Fourth sitting." - a14-queue-truth.json (sitting_4_2026_10_10.refire_note) - 1
25. "TWO-CLOCK FOLD HAZARD (new tonight): the 02:55 master fold and the afternoon lane refires are ~14 hours apart" - a15-rollup.json - 1
26. "STALE-LANE CAVEAT (scope honesty, resolved this pass)" - a15 - 1
27. "a01-a08 at their 16:31-16:52 local mtimes, a09-a14 at their 01:09-01:39 local re-fires" - a15 method_note - 1
28. "DEAD PRIMARY (fourth seat, 2026-10-10): LINKS row 351's canonical https://x.com/yifanzhang_/status/2101068650161807857" - a09-grok47.json ROW #8 claim - 1
29. "REFIRE3 negative, citation drift: the dedupe gate's provenance pointer names MASTER_MICKEY17_V2.md section 9 GO item 2, but the current master's GO item 2 is 'Arena retirement receipts'" - a04-arena-gwap-gps.json ROW #15 claim - 1
30. "(fetched via WebFetch, byte-checked via curl -sL, raw HTML 142,966 bytes, grep hit '393216')" - a05 ROW #9 source - 1
31. "flash lanes, each byte-checking one claim from 16 BURN_* filings." - a07 ROW #1 quote - 1

Checks files:

32. "2026-10-10 gate repair (fold JOIN-HIT-RATE GATE, tools/mickey17_v2_fold.py:351-356): both deep_tier2 row_keys had been derived from this file's own tier-1 claim texts, but the lane rows at a07-fifty-wide-waves.json carry re-fired wording, and the fold joins row_keys against lane rows' first-six-claim-words keys" - a07-fifty-wide-waves.checks.json repair_note - 1 (substring one of two; source em-dash elided)
33. "so the unconfirmed exclusion was silently lost (exit 2)." - a07 checks repair_note - 1 (substring two of two)
34. "verdict and evidence fields are byte-identical to the pre-repair values; only the join keys moved." - a07 checks repair_note - 1
35. "Overwrites the prior pass file at this path" - a07 checks note - 1
36. "Overwrites a prior check file at this path whose rows were a different, superseded row set." - a08-rails-laws.checks.json method - 1
37. "Replaces the prior a03 CheckFile at this path (2026-10-09 row set, 5x no + 2 deep_tier2 verified) per the ask" - a03-tavern-curve.checks.json method - 1
38. "run-measurement conjuncts explicitly framed as this-ask checks" - a07 checks method - 1

Fold / master / spec:

39. "folded_at: 2026-10-11T03:29:41Z (script sha256 58bd72c79c6d)" - runs/run-0/FOLD_SECTIONS.md - 1
40. "- deep_tier2 join: 8/29 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 21" - FOLD_SECTIONS.md - 1
41. "HTTP 404: https://x.com/yifanzhang_/status/2101068650161807857" - FOLD_SECTIONS.md - 1
42. "supersession: this fold rewrites the 2026-10-10T21:58:49Z fire-3 fold (which rewrote the 02:55 fold) in place on both surfaces" - corpus/steal/MASTER_MICKEY17_V2.md - 1
43. "deep_tier2 verdicts grew 17 -> 29 (gate-repairer row-key repairs at 23:0x-23:2xZ, persisted in the lane .checks.json files)" - MASTER_MICKEY17_V2.md - 1
44. "The lane rows are unchanged since fire 3 (162 rows, same scoreboard); what moved is the verifier layer" - MASTER_MICKEY17_V2.md - 1
45. "The verifier table's 2 unconfirmed verdicts both sit on this one row under its pre-repair and post-repair row_keys" - MASTER_MICKEY17_V2.md D0 - 1
46. "the row stays excluded from the included set (PRISMA holds 162 = 161 + 1) until one real fifty-wide wave pre-flights tools/fifty_wide_guard.py" - MASTER_MICKEY17_V2.md D0 - 1
47. "the 23:27Z gate-repairer re-keying in a07-fifty-wide-waves.checks.json, read this fold: verdict and evidence bytes unchanged, only the join keys moved" - MASTER_MICKEY17_V2.md D0 - 1
48. "ORDINAL-REFERENT HAZARD (a04-arena-gwap-gps#15's citation-drift class, now applying to this file's own lineage)" - MASTER_MICKEY17_V2.md FOLD NOTES - 1
49. "TWO-CLOCK FOLD HAZARD (a15-rollup negative, carried)" - MASTER_MICKEY17_V2.md FOLD NOTES - 1
50. "quote the lane id + row index, never the ordinal." - MASTER_MICKEY17_V2.md FOLD NOTES - 1
51. "standing negative at every audit moment (a15: fifth consecutive)" - MASTER_MICKEY17_V2.md negative-results row 7 - 1
52. "the review body's foreign-lane notes below refer to that run" - MASTER_MICKEY17_V2.md (the file's only review hit) - 1
53. "Phase byte-compares every fold and spec quote against the cited lane row; mismatch blocks filing" - MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md - 1
54. "the fold script's top-K candidates plus every tier-1 `supports: no` row go to an independent verifier" - spec - 1
55. "re-fired exactly once" - spec - 1
56. "A lane that cannot pass one records why in a note field" - spec - 1
57. "SPEC may not start, and FILE may not run, without a recorded review verdict" - spec - 1
58. "memory/runs/mickey17_v2/lanes/" - spec - 3
59. "source URL + verbatim-quote hash" - spec (phase-1 idempotency key) - 1
60. "50 = standard burn" - spec - 1

Tool strings additionally verified this session (read in source, cited by line): `fired = a.fired or n_files`
(`:249`), the two candidate key shapes (`:341-344`), the JOIN-HIT-RATE GATE raise (`:351-356`), the hardcoded
screened parenthetical (`:430`), `rank[:12]` (`:439`), `url_checked_at` printed-not-stamped (`:458`).

## 6. CHECKS RUN, and NOT RUN / LIMITS (stated, not guessed)

Run this session (exact instruments):

1. Independent recount of every fold section: `.venv/Scripts/python.exe` scripts over `run-0/lanes/*.json`
   (rows, estate_status, leverage, fidelity with per-row miss list, per-lane counts, top-10 share, duplicate
   groups with pairing, TOP-K sort reproduction, source-shape scans) - every number matched the fold (section 1).
2. Verifier decode + join reproduction: scripts walking every list in every `*.checks.json` (key-name totals,
   yes/no splits, tier-2 verdict values with FULL row_key strings, unique-key count, join under the script's own
   formula re-derived from source `:341-344` - norm = lowercase + whitespace-collapse, two candidate shapes),
   PRISMA exclusion reproduction with the excluded row named - 64 tier-1 (58/6), 29 entries / 19 keys, join 8/29,
   excluded 1 = a07#1, invariant True (1.1, 1.3).
3. Script sha: `hashlib.sha256` over `tools/mickey17_v2_fold.py` -> `58bd72c79c6d`, equal to the fold stamp.
4. URL re-probes with the fold's own method (urllib HEAD then GET, no-redirect opener, fold User-Agent, 6s
   timeout): deepseek create-chat-completion -> HEAD 302; x.com 2101068650161807857 -> HEAD 404 (1.4).
5. Byte-checks: section 5's 60 numbered fixed-string checks, raw hit counts, run post-write (all pass as filed).
6. Wave census: `ls --time-style=full-iso` over all 30 lane/checks files + `FOLD_SECTIONS.md` + master + the
   `nul` file (72 -> 0 bytes at 23:44:18); run-root listing.
7. Artifact searches: `grep -c "OPERATING ENVELOPE"` over fold + tool (0/0); `grep -c -i review` over the master
   (1, inside a quoted receipt) and accept/revise greps (0); `grep -l url_checked_at` over lanes (0 files);
   `git ls-files` on `runs/run-0/` (0 = untracked); `git log --oneline -3 --` this addendum path (stops at
   `a7ca49be1`) + `git status --short` before this write (` M`); `git log --oneline -1` for the session
   context.
8. Master fold: full read (supersession chain, D0-D7, negative-results table, go list, FOLD NOTES); dead-URL
   citing-row scan over all 162 rows (a05#9, a06#3, a09#8 - matches the master's 3).

Not run / limits:

- **This seat did not run `tools/mickey17_v2_fold.py`.** Executing it would rewrite `FOLD_SECTIONS.md` in place
  (and `--check-urls` adds a network pass), mutating the evidence this addendum audits; every number was instead
  reproduced by independent recount, and script-shaped findings are grounded in the read source lines.
- `pytest` was not run: this ask changes no code; it is a documentation filing. No tests exist for or against
  this file. (a15's lane file records why ITS seat also declined to run the route_chat suite - that reason is the
  lane's, not this seat's; this seat simply had no code to test.)
- The fold-time HTTP -1 (deepseek) could not be re-observed at fold time (that moment is gone); the 302 re-probe
  is same-session, same-method - the strongest statement available, and the fifth consecutive non-reproduction
  for the -1 class. Cause (transient network vs CDN/UA behavior) unresolved.
- Fire-3 state (162-row lane set, 17-entry verifier layer) is attested by the master's supersession line only:
  fire-3's `FOLD_SECTIONS.md` and the seven pre-repair checks files were overwritten (untracked archive), so the
  17 -> 29 growth and "same scoreboard" claims are not independently verifiable estate-side. Stated as
  master-attested wherever used.
- Lane concurrency is not verifiable: no journal exists estate-side (E32); tonight's width claim is landing-spread
  only.
- The workflow's in-flight review verdict (phase 5) could not be read estate-side: the master's only "review" hit
  is inside a quoted receipt, and runner introspection reads "workflow_introspection_unavailable" (a12, pass 4).
  This filing proceeds without an estate-readable review record - E30's standing finding, not an unnoticed one.
- The COST DOCTRINE section saw no evidence again: no usage rows for the run itself are cited in the archive.
  Not covered, not violated, fourth state running.
- A7 (paced ramp), A9 (steer preservation), and the tombstone path still have no artifacts in the archive;
  reported as untested, not failed. Zero tombstones in the run's entire history.
- The third filing's byte-check receipts described the 134-row state and died with its bytes at this write; its
  E-ledger survives here only as curated carry-forward (section 4). Its supersession note's recovery promise
  ("its bytes stay recoverable there") was true only of the second filing at `a7ca49be1` - filed here as E26's
  climbed-a-layer specimen, not papered over.
