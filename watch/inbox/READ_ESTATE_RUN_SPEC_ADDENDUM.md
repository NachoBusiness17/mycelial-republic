# MICKEY-17 v2.1 RUN SPEC ADDENDUM: `2026-10-04-0` read-the-estate state (2026-10-04)

<!-- no em/en dashes in this file; plain hyphens only, per the seat law. -->

Filed by the run's SPEC seat (phase 6). This file states what the run's own evidence changes in
`C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md`:
failure modes observed, section counts (independently reproduced), and a verdict on each of the seven laws
in practice when the engine runs over estate-bytes lanes (reading the estate's own files) instead of audit
lanes (auditing receipts). One file; no other estate file was written by this seat. The precedent shape is
the run-0 filing at `watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md`; E-item numbering continues from its E32.

- Run archive (estate absolute path): `C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/mickey17_v2/runs/2026-10-04-0/` containing `FOLD_SECTIONS.md` (scripted fold) plus `lanes/` (12 lane JSONs r01-r12, 12 checks JSONs, one lane-authored helper script `tmp_r09_analyze.py`, and a `.mimosa` runtime dir).
- Prose master fold (estate absolute path): `C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/steal/MASTER_READ_ESTATE.md` (258 lines, 12 sections 0-11, mtime Oct 4 21:12 EDT).
- Evidence base for every claim below: the 12 lane files and 12 checks files read in full this session, `FOLD_SECTIONS.md`, the master fold, the spec, `tools/mickey17_v2_fold.py` (all 235 lines read), `.zcode/workflows/mickey17-v2.dwf.ts` (runner excerpts read), `memory/workflows/REGISTRY.jsonl` (mickey17 rows), and the checks this seat ran (commands and outputs in section 6). Nothing is adopted from a lane's self-report without saying so.

## 0. RUN STATE AT THIS FILING

12 fired, 12 landed, 0 landed-empty, 0 parse errors, 0 missing, 0 tombstones, 0 refires - the first engine
archive with a clean single-pass casualty line. Every lane landed exactly 5 rows; no lane died once, so A2's
refire machinery and the tombstone path saw no live exercise (untested, not failed). The genre is new: all 12
lanes read estate bytes (a live trajectory stream, the ESTATE_INDEX pair, trail JSONLs, the rib vault,
LINKS.jsonl, the catalog, dashboard graphs, the fold archive), so `unique URLs: 0` is structural, not a
finding, and the run's dominant discovery class is the estate's own unread output (section 2, proposed code 14).

## 1. SECTION COUNTS, reproduced (60-row fold)

Every script-written number in `FOLD_SECTIONS.md` reproduced under this seat's independent recount (same
rules: `rows` key or bare array; `*.checks.json` and helper scripts excluded). A5 holds.

| Fold section | Fold says | This seat's recount | Verdict |
|---|---|---|---|
| CASUALTY: fired / landed / landed-empty / parse errors / missing | 12 / 12 / 0 / 0 / 0 | 12 files, all parse, all with `rows` | confirmed as file counts; "fired" is self-referential this run, see 1.2 |
| SCOREBOARD: rows | 60 | 60 (5 x 12 lanes) | confirmed |
| estate_status new / confirms-ours / we-have-better / owed / green-solved | 24 / 15 / 11 / 8 / 2 | 24 / 15 / 11 / 8 / 2 | confirmed; "green-solved" is a 5th status outside the spec's section-2 enum, see E34 |
| leverage high / medium / low | 34 / 24 / 2 | 34 / 24 / 2 | confirmed |
| FIDELITY (quote/source/steal/estate_status non-empty) | 60/60 (100.0%) | 60/60 | confirmed |
| VERIFIER table | `verdicts: checks 10, deep_tier2 12, entries 5, supports 45` | true as a per-KEY-NAME list-length sum; decoded in 1.1 | confirmed as tally; defect stands |
| WIDTH-ECONOMICS median / max / min rows per lane | 5 / 5 / 5 | 5 / 5 / 5 (zero variance) | confirmed; fully degenerate, see Law 7 |
| top-10 lane share | `top-10 lanes share: 83.3%` | 50/60 = 83.3% | confirmed; arithmetically forced (10 of 12 lanes at the uniform 5-row floor) |
| cross-lane duplicate quotes | `exact cross-lane duplicate quotes (normalized): 2` | 2, both classified: r12#4 re-quotes r01#3 and r12#0 re-quotes r04#0 (the rollup's pass-off re-quotes of its inputs), 0 gratuitous | confirmed and re-caused |
| PRISMA: identified / screened / excluded / included | 60 / 60 / `excluded: 0` / 60, invariant HOLDS | arithmetic holds; substantively false, see 1.1 | confirmed arithmetic, defect re-bitten at 5x |
| TOP-K | 12 rows, all leverage-high | rank key is (leverage, lane-id, row-index): alphabetical; r05#3 is cut at 12 while 21 later-alphabet high rows rank below | confirmed as sort; r12's five self-ranked register rows appear nowhere in it, see 1.3 |
| URL LIVENESS | `unique URLs: 0; fetched: 0; skipped non-public: 0; live: 0; dead/blocked-status: 0` | all 60 row sources are estate-internal absolute paths; 0 public URLs | confirmed as a structural no-op for this genre |

Sections present in the scripted fold: CASUALTY HEADER, SCOREBOARD, FIDELITY, VERIFIER TABLE,
WIDTH-ECONOMICS, PRISMA FLOW, TOP-K, URL LIVENESS (8). **OPERATING ENVELOPE is absent from a fifth
consecutive archived fold** (fixed-string check, 0 hits in this `FOLD_SECTIONS.md`; the fold script writes no
such section - E3 persists). The prose master fold carries 12 sections (0-11): 12 TOP-STEALS entries
(TS-01 to TS-12), a 10-entry DISPUTED tier (D1-D10), an 11-row counted negative-results table, a top-10
curiosity register plus 3 just-missed, a 10-item standing-numbers block, and a provenance section that
records the fresh-reader pass.

### 1.1 The verifier table decoded (E5, fifth recurrence) and the PRISMA wiring miss re-bitten at 5x (E20)

The fold line is a per-key list-length sum (`tools/mickey17_v2_fold.py:160`, `vc[k] += len(v)`, byte-checked).
The run's tier-1 verdicts ride under three key names across the 12 checks files: `supports` (45), `checks`
(10), `entries` (5) - true tier-1 total **60 verdicts: 48 `no`, 12 `yes`** (80% no; run-0 measured 84%).
The 48/12 distribution is computed nowhere in the fold; the master fold's seat layer decoded and carried it
("12 yes / 48 no", byte-checked, tagged carried). The table counts list LENGTHS, never verdict VALUES, so the
tier-2 split that actually exists on disk - **7 `verified` / 5 `unconfirmed` across 12 `deep_tier2` entries** -
appears in no fold number either; the master fold carried that split too ("7 verified / 5 unconfirmed",
byte-checked).

The PRISMA defect is now provably permanent, not a formatting accident. The fold's exclusion logic reads a
top-level `unconfirmed` list (`tools/mickey17_v2_fold.py:181`, `c.get("unconfirmed")`, byte-checked) and
matches on `norm(x.get("claim",""))[:80]` (`:183`, `:190`). The runner persists tier-2 verdicts under the key
`deep_tier2` (`.zcode/workflows/mickey17-v2.dwf.ts`, "under the key \"deep_tier2\"", byte-checked), and the
persisted entries carry exactly the fields `evidence`, `row_key`, `verdict` - **no `claim` field at all**
(this seat walked all 12 deep_tier2 entries). The two shapes can never meet: even a correctly-keyed file of
these entries would match nothing. Result: 5 substantive unconfirmations (r04#1, r05#0, r05#1, r05#2,
r05#3, row_keys byte-checked in section 5) rode `included` while the fold printed `excluded: 0`. The seat
layer caught what the script cannot see, for the second run running - the master fold's DISPUTED tier D6-D10
carries all five with their measured corrections.

### 1.2 The casualty "fired" number is self-referential this run (E22, new live evidence)

The run directory is named `2026-10-04-0`. Under the runner's slug formula (`mickey17-v2.dwf.ts:88`,
byte-checked: topic-slug + `"-"` + `String(... args.targets ...).length`), the name decodes as topic
`2026-10-04` (each lane's own `topic` field, byte-read, corroborates) plus a targets-array length of **0**.
The runner passes that same count to the fold wrapper (`:300`, `[FOLD_SH, String(TARGETS.length), RUNSLUG]`,
byte-checked), and the fold defaults `fired = a.fired or n_files` (`tools/mickey17_v2_fold.py:120`,
byte-checked) - so `--fired 0` falls back to the file count, and `missing = fired - n_files` (`:125`) is 0 by
construction. Stated as inference, with the limit named: no run manifest `{topic, targets, width}` is
archived in the run dir, so the interface record is unreconstructible from the estate and a hand-made dir
name cannot be excluded - but the slug bytes, the runner line, and the fold default are the only consistent
reading, and under it the casualty header's `fired: 12 / missing: 0` measured nothing about firing. If
targets was empty at submit, the spec's `lanes = targets 1:1` mapping broke silently and 12 lanes ran
targetless. E22's manifest demand is now backed by a live decode, not just a code cite.

### 1.3 TOP-K composition and the DISPUTED clause (E23, reconfirmed behaviorally)

The rank key is `(leverage-map, lane-id, row-index)` (`tools/mickey17_v2_fold.py:204`, byte-checked). With 34
high rows, the 12 slots are exactly r01#0, r01#3, r02#0, r03#0, r03#1, r04#0, r04#1, r04#2, r04#4, r05#0,
r05#1, r05#2 - alphabetical by lane, cutting r05#3 (r05's fourth high row) while 21 later-alphabet high rows
in r06-r12 rank below. The truncation is visible in the fold file itself: claims are cut at 110 characters
(`:207`, byte-checked), so several TOP-K lines end mid-word ("across 98", "added 2026-10-04"). Separately:
r12-rollup authored its own register ranking (rank 1-5 by the Schmidhuber metric, byte-read in its rows) and
**none of its five rows appear in the script's TOP-K**, so the spec's own clause - "a lane-claimed top steal
outside the script's top-K files as DISPUTED" (spec section 4, byte-checked) - files all five as DISPUTED.
The master fold's seat handled this by carrying the register as its section 9; the script layer has no
mechanism for it.

### 1.4 Fold moment

Newest lane-side landing at the current fold: `r03-corpus-founding.checks.json` 20:29 EDT; `FOLD_SECTIONS.md`
written 20:31 EDT; master fold 21:12 EDT. E7 (fold postdates newest landing) holds. The fold file still
carries no timestamp - a reader cannot tell which fold state they hold without stat (E7 stands, second run).

## 2. FAILURE MODES OBSERVED (against section 7's standing list)

### 2.1 Codes exercised this run

- **Code 2 premise-drift, the run's dominant exercised code (6 instances, all retired by bytes).** The asks
  themselves carried stale numbers, a genre signature: r01 ("~37k rows" inherited from AE5, live stream read
  55,571+), r03 ("The ask's premise figure 'founding record reads 7.5 percent cited' was NOT located in the
  bytes", byte-checked - recorded as-is, unverified), r04 ("Premise drift in the ask: '3.4GB' is stale",
  byte-checked, actual 4,150,418,528 B; plus a missing axis - the ask asked for an event-type distribution on
  a file-census surface), r07 (~700 rows premised, wc -l reads 422), r09 (the ask's "3,804 nodes, 713 edges"
  is a two-instrument chimera splicing F13's 09-30 rib_fork census onto the walk file's edge count). The
  master fold's negatives row 2 counts 6. Run-0's moment-drift was tree-motion; this is upstream of it: the
  ask's own premises are stale at fire time. Code 2 holds as written.
- **Code 7 quote-drift (quote-real-claim-unsupported), exercised once, caught, ruled.** r07#1 claims "51
  event rows migrated to watch/inbox/EVENTS.jsonl" while its own bound quote says the rows "stay in place
  per the append-only law" (both fragments byte-checked in the same lane row). Found by r12's checks census,
  ruled D2 in the master fold ("treat 'migrated' as unsupported"), corrected conditionally, not averaged.
  The quotes themselves were byte-exact everywhere else: all five tier-2 quantity strikes (2.1 code 8) hit
  claims whose quotes verified byte-exact.
- **Code 8 unit-error, exercised at tier 2 as quantity strikes on live-file counts.** The 5 unconfirmations
  are all arithmetic corrections: 917 identical OSError rows is actually 910 (builder 370 not 376; the rows
  are identical only within each trail - D6); "30 consecutive nightly composites" is 28 with a Sep 22 gap
  (D8); the "160 chars" clip constant is a cross-lane transposition, the research writer clips at 250
  (mag/lane_runner.py:755) - D9; "89.4% ... ALL of them resolve under .mimosa\hook-state\" is false for
  355,798 rows (single-root exclusion retires 86.01%, not 89% - D10); "137/137 CRLF-terminated .env" appears
  in no source (D7). Each correction is filed as a standing number, not averaged back (master section 10).
- **Code 9 verifier-unconfirmed, exercised at 5 - all invisible to the fold's own PRISMA (1.1).** The
  `crashed` and `same-chain-verified` buckets remain unused in engine history (7th run of the engine, never
  once fired).
- **Code 10 empty-estate-grep, the run's central finding, exercised en masse.** 27-29 zero-hit terms across
  12/12 lanes (master negatives row 1): estate_index in corpus/steal and memory/rib (r04), every LINKS
  register theme in both (r07), the trail system in steal (r05), steps.jsonl and corr_id in rib (r01),
  queue_close and burn_reset_20260927 in both (r02), the curriculum (r08), five graph terms (r09), the
  card ids and seat_move (r10), 191.8 and attention_feedback in rib (r11), schmidhuber and
  CURIOSITY_REGISTER (r12). The steal corpus and the rib vault have never ingested the estate's own
  surfaces. Every zero-hit is recorded as a finding, per the rubric.
- **Code 1 phantom-source, found in the audited estate.** r06: RIB_FRONTIER_ASK_20260929 - "designed
  2026-09-29, never minted, no file anywhere in memory/watch/corpus/docs/tools/mag/configs/queue/state
  (find run)", yet cited twice as if named (byte-checked). r09: 188 of 4,848 graph nodes are id-only
  X-status placeholders and one is the graph's 7th-most-connected node at degree 34 - the estate graph's
  backbone is partially phantom. r01: duels.jsonl does not exist at the paths the AH14 docstring implies.
  Master negatives row 7.
- **Code 3 url-owner-rot, inverted onto estate-internal citations.** No public URL rotted (there are none);
  instead r09 measured a receipt's byte-size citation of a regenerating surface rotting +295% in 7 days
  ("Byte-size citations of regenerating surfaces rot within a week.", byte-checked), a stale ROLLUP_DELTA
  (generated 09-30), and a Sep 9 orphan ledger still cited as current. The code's disease class applies to
  estate citations of regenerating surfaces; the spec names only URLs.
- **Code 6 fabricated-name-or-rumor, audited-artifact instances only.** r11 banks the already-struck 191.8M
  phantom (its quote "## ERRATA 001: the 191.8M-token mine headline is a phantom; STRUCK", byte-checked) and
  finds next.md's forecast battery F2/F3 falsified by bytes with no falsification receipt banked anywhere;
  r07's register line 336 records phantom arXiv citations inside the estate's own DeepSeek share doc. No
  lane fabricated anything this run.

### 2.2 New class candidate for section 7

- **Proposed code 14, unread-output: a surface built, visualized, or counted whose outputs no downstream
  surface ever consumed.** This is the read-estate genre's signature class - the estate reading itself finds
  the estate's own unread outputs. Instances, all byte-read: the 4,047,714-byte orphan ledger unread since
  Sep 9 with 21,479 of 28,838 knots unchained (r09); the research lane 84% spool rows with zero recorded
  downstream consumption since Sep 6 (r05, D9-corrected); harvest fetching 300/run with hits=0 for 18 days,
  forge forged=0 on all 30 cycles, the economist sweep pointer frozen 25 days, bard appending 39 duplicate
  rows in an hour, jev a 6-row orphan ledger (r05 extra findings); 50 of 53 ribs carrying law content in no
  boot surface while the module minted to mount them reads zero vault files (r06); museum remnants verified
  real and unrecorded (r09). Distinct from code 10 (knowledge surfaces not ingesting a topic): code 14 is a
  surface's own outputs never consumed downstream.

### 2.3 Codes silent

Zero instances this run: 4 walled-source (the .env was read for line endings only, by design - the wall was
respected, not hit), 5 barren-start (all 12 lanes mined richly), 11 scanner-under-coverage (no security-gate
contact in a read-only genre). Archive hygiene note, not a code: the lanes dir carries a lane-authored
helper script (`tmp_r09_analyze.py`, byte-checked in r09's method note) and the run dir carries a `.mimosa`
runtime dir - the fold's glob tolerates them, but they are not lane records.

## 3. THE SEVEN LAWS IN PRACTICE (read-the-estate state)

1. **CITATION-BINDING: HELD.** 60/60 fidelity reproduced; every row binds a verbatim quote. The run's one
   true quote-claim contradiction (r07#1, 2.1) was caught by a lane's checks census, ruled conditionally in
   DISPUTED D2, and corrected - the law's full loop, second run running. Tier-1 went 48 no / 12 yes (80%) on
   compound claims; the demotion-rule-instead-of-demotion pattern (E6) persists - `no` rows stay included
   with their lane's own cross-check evidence standing in, and substance lives at tier 2. New: this is the
   first run with an estate-side decode of the tier-1 split, and it required walking the checks files by
   hand because the fold's table cannot say it (1.1).
2. **NEGATIVE-FIRST-CLASS: HELD - the run's strongest law.** Every lane files dedicated negative fields
   (`negative_findings`, `notes`, `dead_leads`, `not_run`, `rubric_gaps`); zero silent drops found; 0
   tombstones, 0 casualties. The master fold files an 11-row counted reasons table, and r05 shows the law's
   mature form: it explicitly retracts a would-be finding ("honest non-finding: index_data/beat_map_*.json
   ... are NOT unread - sibling MAG DANCE V02 lane wired them today"). The genre adds a new negative class
   (proposed code 14, 2.2) that only this run could have found.
3. **CONTRADICTION-TIER: HELD - again the best evidence for the law.** The DISPUTED tier carries D1-D10,
   every ruling conditional, nothing averaged. D1 is the model case: the LINKS hardlink claim ("hardlinks to
   ONE physical 3.4GB file") versus two independent fsutil runs each returning only the path itself, ruled
   "either the claim was wrong at write time or a later write broke the link (mechanism not determined; no
   verdict offered on intent)" (byte-checked in r04#3's row) - both quotes carried, mechanism marked
   undetermined. Section 10's standing numbers block rules with corrections (910 not 917; 28 not 30; 250 not
   160; 89.3/86.01 not 89.4-with-ALL) and explicitly refuses to average struck values back.
4. **ABSOLUTE-PATHS: HELD at the row level - first run at 60/60.** All 60 row sources are estate-absolute
   (recount, section 1), against 76/94 in run-0; r04's rows use backslash form and the rest forward-slash,
   both absolute. The width receipt remains unmet and got structurally worse: no landing journal exists, and
   1.2's decode says the run's own input record (targets) is unreconstructible - "width N held" is now
   unverifiable on both the concurrency side and the input side. Honest width claim: 12 lanes fired, 12
   landed, 60 rows, concurrency never journaled.
5. **FOLD-BY-SCRIPT: counts hold exactly; the extensions are the defect surface; the seat layer is carrying
   the verdict-level truth the script cannot see.** Every scoreboard number reproduced (section 1). Against
   that: the verifier table's list-length sums (1.1), the verdict-value blindness (48/12 and 7/5 computed
   nowhere by script), the PRISMA wiring miss re-bitten at 5x with the mismatch now proven permanent from
   runner + fold source lines (1.1), `fired` circularity live (1.2), no OPERATING ENVELOPE in a fifth fold
   (E3), the screened line's parenthetical is a hardcoded literal, not a check (`:197`, byte-checked), TOP-K
   alphabetical with mid-word truncation (1.3), no fold timestamp (E7), and the A11 `url_checked_at` stamp
   still unimplemented (`:225` prints the clause; no code stamps it - moot at 0 URLs but the clause remains
   code-absent). The master fold's seat layer decoded the splits, carried the DISPUTED corrections, and
   struck its own unreconcilable headline on the fresh-reader pass. Law 5's letter - "Phase byte-compares
   every fold and spec quote against the cited lane row; mismatch blocks filing" - is what this seat
   executed; the receipt is section 5.
6. **WRITES-SERIAL: HELD, and run-0's checks-overwrite defect did not recur.** Lanes wrote only their own
   files; tier-2 persistence ran as per-lane merge-appends (the runner instructs the writer to keep "any
   existing deep_tier2 entries" and append - byte-checked at the runner's persist phase), and all 12 checks
   files carry both tier-1 and tier-2 sections: E26's merge-not-overwrite rule was followed this run without
   being specced. r12's idempotency line marks its own write honestly ("not a refire: no prior
   r12-rollup.json existed when written", byte-checked). Minor hygiene: one helper script and a `.mimosa`
   dir sit inside the archive (2.3 note).
7. **WIDTH-LADDER: ran below the ladder's minimum with fully degenerate gate metrics.** Width 12 is under
   Law 7's own "14 = day minimum, 50 = standard burn" (byte-checked) - the second consecutive filing under
   the minimum rung, and the ladder has no rung language for a read-the-estate genre at all. With every lane
   at exactly the 5-row floor, median = max = min = 5, top-10 share is pure arithmetic (83.3%), and the
   Law-7 gate line prints itself with zero discriminating power (E24 reconfirmed at the extreme). The 2
   duplicate quotes are both r12 pass-off re-quotes of its own input lanes - the engine's interagent
   pass-off, which Law 7's trial named legitimate. No 429s, no usage windows, no pacing evidence: the
   cost-doctrine legs saw no evidence this run (estate reads, not web fetches). And per 1.2, the input side
   of "lanes = targets 1:1" apparently broke silently - if targets was empty, width 12 was never an argument
   the engine received.

## 4. EDITS THIS EVIDENCE BUYS (the E-ledger, continued)

Carried and updated from the run-0 filing:

- **E3 (OPERATING ENVELOPE code-absent) - 5th consecutive archived fold, 0 hits.** Stands unchanged.
- **E5 (verifier table = list-length sums) - 5th recurrence.** The script must read `verdict`/`supports`
  VALUES from the tier lists and print the yes/no and verified/unconfirmed splits; this run those splits
  existed only because the seat layer hand-decoded them (1.1).
- **E6 (tier-1 no-rate on compound claims) - census updated: 48/12 = 80% no; the quote-narrower-than-claim
  reading is now adopted in the master fold's own section 0.** Tier-2 remains where substance lives.
- **E7 (fold timestamp) - stands, second run.**
- **E19 (idempotency-key convention) - census updated, 5 shapes on 60 rows:** `key` x40, `idem_key` x5,
  `id`+`idempotency` x5, `idempotency_key`+`id` x5, and **`NONE` x5 (r06's rows carry no key field at all)**;
  content ranges from bare 8-hex (r11 `deb391fb`) to path+label (r01). Spec line 41's formula is only
  mechanical if the script computes the key itself. Still owed.
- **E20 (verdict wiring) - RECURRED at 5x and upgraded from defect to proof: the runner persists
  `deep_tier2` (byte-checked), the fold reads top-level `unconfirmed` (byte-checked), and the persisted
  entries carry no `claim` field, so the match can never meet even with the right key.** Fix: read
  `deep_tier2[].verdict`, count `unconfirmed`/`crashed` into PRISMA excluded under their own codes, and
  assert before writing.
- **E22 (fired/journal circularity + manifest) - RECURRED with a live decode: the `-0` slug suffix plus the
  runner's `String(TARGETS.length)` fold argument plus the fold's `a.fired or n_files` default make this
  run's `fired: 12` self-referential (1.2).** Archive a per-run manifest; the spec's ports section should
  require it.
- **E23 (TOP-K rank key) - reconfirmed behaviorally, plus two new notes:** the r05#3 cut at 12, the 110-char
  claim truncation (`:207`), and the r12-vs-TOP-K disagreement that triggers the spec's own DISPUTED clause
  for all five register rows (1.3).
- **E24 (gate-metric degeneracy) - reconfirmed at the extreme:** a uniform 5-row floor makes top-10 share
  83.3% and median=max=min, so neither gate metric can discriminate at any width where lanes land equal
  rows. Classify duplicates and require row-variance before the gate applies.
- **E26 (checks-file persistence) - CURE OBSERVED: the merge-not-overwrite behavior ran correctly on all 12
  files this run (tier-1 and tier-2 both present), via the runner's own persist phase, without a spec
  change.** Promote what the runner already does into the spec's A3+A4 wording.
- **E28 (moment-drift, proposed code 12) - new instances inside the run's own verification layer:** r12's
  checks census read "the 8 sibling checks files hold 36 tier-1 verdicts: 4 yes / 32 no" at its moment
  (byte-checked) while the final archive holds 60 (12/48) - both true at their moments; r05's own tier-2
  re-measured 3037/3618 seven minutes after the lane's 3030/3610 on the live research trail; r06 read 53
  rib .md files, r12's two instruments read 52 at 22:5xZ, miscount unresolved and recorded over either
  single number. Import B2-216 into section 7.
- **E29 (fold-self-echo, proposed code 13) - new mechanism instance: the trajectory ledger as echo channel.**
  r08 caught its own false positive: "the match is the trajectory ledger recording my own grep command, not
  a prior consumer" (byte-checked) - the run's activity enters the audited surfaces through steps.jsonl
  itself, not only through the run's fold files. The grep rule should tag or exclude the run's own artifacts
  AND moment-slices of the trajectory stream.
- **E30 (review-verdict persistence) - PARTIAL CURE: the fresh-reader pass left its record estate-side in
  the master fold's provenance section** ("CHECK 5 fail: the pack rows overclaimed one sitting", byte-checked,
  plus the struck grep headline; the relabels are grounded in the lane rows' own one-sitting sentences).
  REVISE-once was exercised and the revision landed. Still owed: the literal ACCEPT/REVISE token rides only
  the workflow report (runner `review.decision`, report line "fresh-reader review verdict recorded"), and
  the run archive holds no review file - require the token written into the filed master fold.
- **E31 (runs/<slug> layout) - third slug shape (`2026-10-04-0`) and it decodes (1.2).** The spec's ports
  section should pin the slug formula, the manifest, and the master-fold naming in one place.
- **E32 (landing journal) - stands, unmet; mtime ordering is again unreliable (checks files postdate lane
  JSONs by hours).**

New items from this state:

- **E33 (master-fold naming drift).** The runner hardcodes `MASTER_MICKEY17_V2.md` (8 occurrences,
  byte-checked) but this run's filed master is `MASTER_READ_ESTATE.md`, whose own provenance cites a
  workspace copy beside the estate one. Either the fold seat deviated from the saved runner or the runner's
  name constant is stale for named runs; the spec's port 3 should name the per-run master convention so the
  archive stays predictable.
- **E34 (estate_status enum).** The spec's section-2 enum is `confirms-ours | owed | we-have-better | new`
  (byte-checked); this run's lanes used a 5th value, `green-solved` (2 rows, r02 - a door that landed and
  whose adoption clause executed), and the fold counted it faithfully because the scoreboard is an open
  Counter. Extend the enum or bless the extension; do not leave the interface dictating 4 values while
  lanes emit 5.
- **E35 (the read-estate genre paragraph).** The spec's rubric and interface assume outward-facing sources:
  A11 URL liveness, check-1 "primary source fetched", `targets[].start`. This run exercised a valid but
  unnamed mode where all 60 sources are estate-internal: URL liveness is a 0/0 structural no-op, check-1
  becomes disk-read instruments (streaming parses, fsutil, git cat-file, schtasks), `start` is unused, the
  `topic` field degenerated to a date string in lane metadata, and the dominant failure class inverts to
  the estate's own unread output (code 14) plus stale ask premises (code 2). One section should name the
  estate-read genre so its no-ops are expected, not defects, and its premise discipline (retire ask numbers
  by bytes, stamp read moments) is explicit.

## 5. QUOTE BYTE-CHECK RECEIPTS (the A5b check, run by this seat)

Method: every quote in this addendum was checked as a fixed string against its cited file before filing,
with `.venv/Scripts/python.exe` raw-byte `str.count` over the utf-8-decoded file bytes. JSON files carry
quoted strings in JSON-escaped form (backslashes doubled); the one backslash-bearing quote (item 5) was
additionally verified by decoded deep-containment (`json.loads` equality). 45 fixed-string checks were run
this session; 44 distinct quotes; 43 passed as first cited and 1 failed and was corrected before filing
(item 5: the seat's own check needle was malformed by shell escaping - it carried a real CR byte where a
backslash belongs; re-checked raw-escaped and decoded, PASS; the lane file was correct all along). All 44
pass as filed. Counts are raw hits in the cited file.

Lane/checks files (under `memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/`):

1. "39 open / 8 superseded / 3 closed of 50" - r02-nightburn-unread.json (r02#0 quote) - 1
2. "The ask's premise figure 'founding record reads 7.5 percent cited' was NOT located in the bytes" - r03-corpus-founding.json (premise_note) - 1
3. "Premise drift in the ask: '3.4GB' is stale" - r04-estate-index-anatomy.json (negative_findings[0]) - 1
4. "either the claim was wrong at write time or a later write broke the link (mechanism not determined; no verdict offered on intent)" - r04-estate-index-anatomy.json (r04#3 claim) - 1
5. "lane-down: Invalid header value b'Bearer sk-or-v1-41679b3f[REDACTED]\r'" - r05-trails-deep.json (r05#1 quote) - 1 raw-escaped, decoded-equality True
6. "still not have read the 51 frozen ribs that say what the system is FOR" - r06-rib-vault.json (r06#3 quote) - 1
7. "designed 2026-09-29, never minted, no file anywhere in memory/watch/corpus/docs/tools/mag/configs/queue/state (find run)" - r06-rib-vault.json (negative_findings[0]) - 1
8. "the 51 event rows (lines 275-305 scout/seat events, lines 312-331 endpoint-news events) stay in place per the append-only law" - r07-links-register.json (r07#1 quote) - 1
9. "51 event rows migrated to watch/inbox/EVENTS.jsonl" - r07-links-register.json (r07#1 claim, the contradicted conjunct) - 1
10. "the match is the trajectory ledger recording my own grep command, not a prior consumer" - r08-catalog-library.json (notes) - 1
11. "Byte-size citations of regenerating surfaces rot within a week." - r09-museum-graphs.json (negative_first_class) - 1
12. "memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/tmp_r09_analyze.py" - r09-museum-graphs.json (method note) - 1
13. "sampled evidence ids (x:1892200889844142376, x:1997810985646645710) grep zero files under corpus/canon/" - r10-canon-patterns.json (r10 row-5 claim) - 1
14. "## ERRATA 001: the 191.8M-token mine headline is a phantom; STRUCK" - r11-fold-history.json (r11#0 quote) - 1
15. "no r09-r11 existed in the lanes dir" - r12-rollup.json (negative_findings) - 1
16. "the 8 sibling checks files hold 36 tier-1 verdicts: 4 yes / 32 no" - r12-rollup.json (CHECKS CENSUS) - 1
17. "not a refire: no prior r12-rollup.json existed when written" - r12-rollup.json (idempotency field) - 1
18. "r04-estate-index-anatomy: The skip list is arithmetic, not" - r04-estate-index-anatomy.checks.json (deep_tier2 unconfirmed row_key) - 1
19. "r05-trails-deep: The largest recorded failure in the" - r05-trails-deep.checks.json (deep_tier2 unconfirmed row_key) - 1

Fold / master / spec / runner / tool:

20. "verdicts: checks 10, deep_tier2 12, entries 5, supports 45" - runs/2026-10-04-0/FOLD_SECTIONS.md - 1
21. "excluded: 0" - runs/2026-10-04-0/FOLD_SECTIONS.md - 1
22. "unique URLs: 0; fetched: 0; skipped non-public: 0; live: 0; dead/blocked-status: 0" - runs/2026-10-04-0/FOLD_SECTIONS.md - 1
23. "exact cross-lane duplicate quotes (normalized): 2" - runs/2026-10-04-0/FOLD_SECTIONS.md - 1
24. "top-10 lanes share: 83.3%" - runs/2026-10-04-0/FOLD_SECTIONS.md - 1
25. "OPERATING ENVELOPE" - runs/2026-10-04-0/FOLD_SECTIONS.md - 0 (the absence, measured)
26. "12 yes / 48 no" - corpus/steal/MASTER_READ_ESTATE.md - 2
27. "7 verified / 5 unconfirmed" - corpus/steal/MASTER_READ_ESTATE.md - 2
28. "CHECK 5 fail: the pack rows overclaimed one sitting" - corpus/steal/MASTER_READ_ESTATE.md - 1
29. "Workspace copy of this fold: `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_READ_ESTATE.md`" - corpus/steal/MASTER_READ_ESTATE.md - 1
30. "confirms-ours | owed | we-have-better | new" - MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md - 1
31. "14 = day minimum, 50 = standard burn" - spec - 1
32. "a lane-claimed top steal outside the script's top-K files as DISPUTED" - spec - 1
33. "stamps every rendered row" - spec - 1
34. "+ \"-\" + String(Array.isArray(args.targets) ? (args.targets as unknown[]).length : 0);" - .zcode/workflows/mickey17-v2.dwf.ts - 1
35. "world.run(\"bash\", [FOLD_SH, String(TARGETS.length), RUNSLUG]" - .zcode/workflows/mickey17-v2.dwf.ts - 2
36. "under the key \"deep_tier2\"" - .zcode/workflows/mickey17-v2.dwf.ts - 1
37. "MASTER_MICKEY17_V2.md" - .zcode/workflows/mickey17-v2.dwf.ts - 8
38. "vc[k] += len(v)" - tools/mickey17_v2_fold.py - 1
39. "c.get(\"unconfirmed\")" - tools/mickey17_v2_fold.py - 1
40. "norm(r.get(\"claim\"))[:80]" - tools/mickey17_v2_fold.py - 1
41. "fired = a.fired or n_files" - tools/mickey17_v2_fold.py - 1
42. "(all rows carry the six rubric fields or their gap notes)" - tools/mickey17_v2_fold.py - 1
43. "norm(r.get('claim'))[:110]" - tools/mickey17_v2_fold.py - 1
44. "\"deep_tier2\"" - tools/mickey17_v2_fold.py - 0 (the absence, measured: the fold script never reads the key the runner persists)

## 6. CHECKS RUN, and NOT RUN / LIMITS (stated, not guessed)

Run this session (exact commands or instruments):

1. Full 12-lane read (every lane file and checks file read in full via the Read tool).
2. Independent recount + censuses: `.venv/Scripts/python.exe` heredoc over `lanes/r*.json` computing rows/lane, estate_status, leverage, fidelity, cross-lane duplicate quotes (normalized), top-10 share, source-shape census (60/60 estate-absolute), and the idempotency-key field census (section 1; scoreboard matched the fold exactly).
3. Checks decode: second heredoc walking every list in every `*.checks.json`, printing per-key list-length sums, tier-1 verdict VALUES (48 no / 12 yes), tier-2 verdict VALUES (7 verified / 5 unconfirmed), the top-level-key census (`unconfirmed` present in 0 of 12 files), and the field shape of the deep_tier2 entries (`evidence`/`row_key`/`verdict` only, no `claim`).
4. Unconfirmed row_key + evidence extraction over all 12 checks files (5 printed with their evidence heads).
5. Source reads with line numbers: `tools/mickey17_v2_fold.py` in full (Read); runner excerpts via `sed -n` / `grep -n` on `.zcode/workflows/mickey17-v2.dwf.ts`; master fold via `sed -n` ranges plus header/TS/D counts via `grep -c`.
6. Registry: grep over `memory/workflows/REGISTRY.jsonl` - 4 `mickey17-v2.dwf.ts` rows, latest PASS 2026-10-04T02:34:02Z (predates this run's first lane landing; no per-run gate row exists for this run).
7. Byte-checks: section 5's 44 fixed-string checks (one batch heredoc, plus the item-5 correction heredoc), all recorded with raw hit counts.
8. Structural counts: master fold section headers (12, `grep -n "^## "`), TOP-STEALS entries (12), DISPUTED entries (10), fold TOP-K high rows (12).

Not run / limits:

- **This seat did not execute `tools/mickey17_v2_fold.py`.** It was read in full; executing it would rewrite `FOLD_SECTIONS.md` in place, mutating the evidence this addendum audits. Every fold number was reproduced by independent recount; the script-shaped defects are grounded in read source lines plus live decode, not in an executed failure.
- **The targets-array-was-empty reading (1.2) is inference.** It is the only reading consistent with three byte-true artifacts (the dir name, the runner's slug formula at `:88`, the fold's `--fired` default at `:120`), but no run manifest exists estate-side to prove it; a hand-made directory name cannot be excluded. Stated as inference with its basis, not as fact.
- **The 5 tier-2 unconfirmations were not independently re-verified by this seat.** Their corrections (910/370, 28 composites, 250-char clip, 86.01%/89.3%, the 136-line .env) are the deep checker's own measurements, persisted in the checks files and ruled in D6-D10; this seat verified the checks files' structure and the fold's blindness to them, not the underlying re-measurements (including the 4.15GB re-parse).
- **pytest was not run:** this ask changes no code; it is a documentation filing. No tests exist for or against this file.
- **Lane concurrency is not verifiable:** no landing journal exists estate-side (E32); the width receipt remains unearnable.
- **The literal ACCEPT/REVISE review token was not found estate-side.** The fresh-reader pass is recorded in the master fold's provenance section (byte-checked), and the runner holds `review.decision` in the workflow report only; the run archive contains no review file. Reported as a partial cure (E30), not a full one.
- **Live-file moments:** steps.jsonl appends ~3 rows/min and research.jsonl every ~15 min per the lanes' own moment notes; every count in this addendum is a moment-read (B2-216 applies to this file too).
- **The cost-doctrine section of the spec saw no evidence this run:** no usage rows for the run are cited in the archive. Not covered, not violated. A7 (paced ramp) and A9 (steer preservation) likewise left no artifacts; reported as untested, not failed.
- The run-0 filing's E-numbers describe that run's state; items carried here (E3, E5, E6, E7, E19, E20, E22, E23, E24, E26, E28, E29, E30, E31, E32) were re-grounded in this run's bytes before being restated.
