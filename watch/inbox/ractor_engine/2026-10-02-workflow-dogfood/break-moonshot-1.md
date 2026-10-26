# break-moonshot-1: hostile byte-check of lens moonshot-1

Moment of this pass: 2026-10-04T03:40-04:00Z. Seat: break pass inside run Ractor-dogfood-workflows
(dwfrun-ed1dbbae). Every check below was executed this sitting; instrument named per check.
Handed report: `moonshot-1.md` (this dir); the handed JSON carried findings F1-F3, F4, and a
truncated duplicate of F4 at index 4 (the copy in `moonshot-1.md` F4 section is complete; the
duplicate was verdicted once as F4).

Instrument notes up front:
- `ListSavedWorkflows` returned count=19 this sitting (tool output).
- `ListWorkflowRuns` is unreachable from this seat too: the tool returned
  `workflow_introspection_unavailable` ("this session cannot read workflow runs"). The lens's
  instrument claim is CONFIRMED: the read-only sqlite census is the only run instrument here.
  Command: sqlite read-only over `C:/Users/foste/.zcode/cli/db/db.sqlite`, table `dwf_run`
  (`.venv\Scripts\python.exe` + sqlite3, URI mode=ro; no writes).
- dwf_run schema read this sitting: columns include `script_hash`, `resumed_from`, `failure_json`,
  `time_created` (epoch ms), `spent_tokens`, `status`. `script_hash` = sha256(script_text),
  verified: Tree Doctrine row's text hashes to exactly its stored `da62eaa8c17f...`.
- Snapshot law: the lens read 5.05B tokens / 63 registry rows; this pass reads 5,111,769,862
  tokens (5.11B) / 75 registry rows. Drift = 3 in-flight runs banked tokens + a +17-row
  working-tree registry batch (`git diff -U0 -- memory/workflows/REGISTRY.jsonl` = 17 added, 0
  removed vs HEAD). Counts are per-moment, per B2-216.

## Verdicts

### F1 (fleet is one template wearing 8 skins; ~5 organs; clones inherit mickey17 filesystem): CONFIRMED, two numeric corrections
Every cited byte reproduced by my own runs:
- difflib exact ratios this sitting over `.zcode/workflows/*.dwf.ts` (19 files): salon-mine vs
  the-gala 0.9395; fill-ball vs wide-dig 0.9506; fill-ball vs wide-dig = 39 opcodes, 19 non-equal
  blocks. All exact.
- Six-file family (drop-dig, fill-ball, librarian-expedition, salon-mine, the-gala, wide-dig):
  all 15 pairs in 0.9395-0.9506, floor salon-mine/the-gala. Falsifier ("any pair below 0.85")
  fails.
- gap-analysis.dwf.ts:82 (`WSOUT = "C:/Users/foste/.zcode/workspace/default/mickey17_v2"`), :83
  (FOLD_SH), :91 (`LANES = ESTATE + "/memory/runs/mickey17_v2/runs/" + RUNSLUG + "/lanes"`): all
  present, and NOT dead code: LANES is the lane write path (:149 incremental backup ask, :162,
  :295 deep-persist, :318, :337) and WSOUT/FOLD_SH drive the fold gate (:312, :321) and the fold
  writes (:338 MASTER_MICKEY17_V2.md, :349, :355). Live-write proof: `memory/runs/mickey17_v2/runs/`
  holds `gap-analysis-of-the-estate-s-09--15` (mtime 2026-10-01T23:37:26Z, 30 lane jsons) and
  `run-0` (mtime 2026-10-04T01:05:51Z, 30 lane jsons), both written by gap-analysis-labeled runs.
- Fleet size: ListSavedWorkflows count=19 vs the ask's 12. Exact.
Corrections inside the finding:
1. The range "93.95-99.4%" is wrong. The six-family spans 93.95-95.06%. My untruncated all-19
   pairs census (171 pairs) finds exactly two clone clusters at >=0.93: the six family
   (0.9395-0.9506) and the five game-dig clones (0.9618-0.9869, max creature-farming vs
   horror-maze 0.9869). NO pair measured 99.4%. The lens's own evidence lines did not contain the
   99.4% figure either.
2. "8 skins" understates. Run-level census (dwf_run GROUP BY script_hash, 138 rows): one shared
   body text (sha256 11327967455d...) ran 21 times for 485,917,613 tokens under 12+ different run
   labels (Salon-mine-20deep, Librarian-gathering-expedition, Fill-ball-one-sittings,
   Vonnegut-final-cut, Hitler-dig-full-dogfood, Spiking-wide-dig, Localfirst-steal-wave,
   Music-ractor, Lyric-workover-stage1, Ouroboros-meta, Salon-vault-*, ...), and that text is
   byte-CONTAINED in all six family files. The six skins are one body plus per-file headers; at
   run time the label is decorative (see A1).
- gap-analysis vs mickey17-v2 direct ratio: 0.865 (partial inherit, below family floor, consistent
  with chimera not clone). gap-analysis.dwf.ts:129's lane system prompt still reads "You are one
  lane of a MICKEY-17 v2.1 frontier-steal burn" while the header (:2-13) and lane table (:107-121)
  are gap-analysis.

### F2 (fire census: most of the fleet fired clean once; registry cannot count the fleet): CONFIRMED, registry leg cured by drift since the lens's moment
Re-census this sitting (read-only sqlite, untruncated): 138 rows; status 77 completed / 35 failed /
23 cancelled / 3 running; failed+cancelled 58 = 42.0% (exact); sum spent_tokens 5,111,769,862.
- 'Tree Doctrine 50-wide dig (gated)': exactly 1 row, completed, 106,564,604 tok, created
  2026-09-25T18:59:07Z. Exact match to all three cited numbers.
- 'Fill-ball-one-sittings': created 2026-10-02T03:51:44Z, completed, 68,689,159 tok, fill-ball's
  only clean fire (2 rows total). Exact.
- 'Fill-ball-amend': failed, 0 tok, created 2026-10-03T22:38:56Z. Exact.
- Dormancy: the-50's last fire created 2026-09-25T18:53:02Z ('THE 50 - full program relaunch',
  ran to 09-26T01:07Z): "dormant since 09-25" holds on start-time. mickey17's last fire 'Mickey17
  Wave 3' completed 2026-09-28T21:16:22Z: "dormant since 09-28" holds. librarian-expedition: 1
  clean fire (10-01T22:57Z, 37,569,179 tok) + 1 zero-token cancel. salon-mine: 1 clean fire
  ('Salon-vault-stragglers', 10-02T14:53Z, 66,293,099 tok). drop-dig: zero rows under its own name
  (its label mapping is the shared body, see A1; the lens's Hitler-dig pairing stays unproven, and
  my byte check shows it is unresolvable to drop-dig specifically: 'Hitler-dig-full-dogfood' ran
  the shared family body, which is contained in all six files, not drop-dig alone).
- Registry leg: at the lens's moment true, now false. `memory/workflows/REGISTRY.jsonl` now has 75
  rows (lens read 63); `git diff -U0` shows +17 working-tree rows vs HEAD; fill-ball / salon-mine /
  librarian-expedition / drop-dig each have exactly one PASS row now (rows 66/68/69/71, stamped
  2026-10-04T02:33:49-02:34:00Z, a full-fleet gate sweep 13 rows in 19 seconds). "Names drift
  across 25 spellings" is byte-exact: 25 distinct script basenames across the 75 rows. The five
  game-dig vein clones remain registry-invisible (no game-dig-* basename appears in the 25).

### F3 (game-dig family is the theater-burner): CONFIRMED on every measured number; the "theater" reading narrows because the deliverables landed
- ListSavedWorkflows count=19 (tool, this sitting). Five game-dig vein clones + deep-dig parent
  present; five clone files share mtime 2026-09-27 07:21 (`ls -la .zcode/workflows/`).
- dwf_run 'Game dig%' family: 34 attempts (8+8+6+6+6), 29 failed+cancelled, 5 completed, sum
  643,862,449 tok, window 2026-09-26T22:22:38Z to 2026-09-27T05:36:37Z (lens said 22:22Z-05:36Z,
  exact). 85.3% per-attempt failure. Zero game-dig rows created after 2026-09-27 (query this
  sitting). Falsifier ("a game-dig dwf_run after 09-27") fails.
- Registry leg stale: "last game-dig gate rows 2026-09-26" was the registry state at 63 rows; the
  current 75-row file carries game-mechanics-deep-dig gate rows at 2026-10-02T10:42:55 and
  10:43:41 (rows 57-58). The dormancy conclusion survives anyway on the dwf_run evidence.
- Blind spot 4 closed by this pass: the wheel specs DID land. `watch/inbox/GAMEDIG_MASTER_ATLAS_20260927.md:3`
  claims "Total wheel-spec surface ~487KB"; the five primary artifacts named at :7-13 all exist
  this sitting: GAMEDIG_co-op-social-ValheimDST-vein_20260926.md (88,529 B),
  GAMEDIG_creature-farming-PalworldStardew-vein_20260926.md (105,782 B),
  GAMEDIG_horror-maze-DOORSLethal-vein_20260926.md (121,819 B),
  GAMEDIG_liveops-seasonal-GAGAdopt-Me-vein_20260926.md (86,059 B),
  GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md (87,639 B) = 489,828 bytes. The theater
  verdict therefore rests, correctly, on burn + dormancy only: what remains of "theater" is cost
  per clean dig (~128.8M tokens average once the ~283.6M of failed/resumed attempts is spread over
  5 completions) and zero fires in the 7 days since.

### F4 (the gap-analysis -> fill-ball mega-workflow exists as a file contract and has never run as one): WEAKENED, the file-contract leg dies under the lens's own falsifier
- "Never ran as one script": CONFIRMED and mechanism-named. The 10-03 22:38Z chain attempt died at
  spawn: 'Fill-ball-amend' failure_json = DriverError "no lanes passed", which is fill-ball.dwf.ts:96's
  own throw. Nothing ever cut the register into lanes; the human fire passed none.
- The falsifier, run this sitting: `args.register` appears ONLY in fill-ball.dwf.ts's header
  (lines 9 and 15-19). The body builds ALL from `args.lanes` (:93-94) and never reads the register:
  grep for readFile/readTextFile/world.read/fs. over the whole file returns ZERO hits. The register
  path is decoration.
- The other end is equally unwired: gap-analysis.dwf.ts's body emits no GAP_REGISTER.md anywhere.
  Its writes are mickey17_v2 lane jsons (:149, :295), MASTER_MICKEY17_V2.md (:338), and a spec
  addendum (:363). The register that exists (watch/inbox/gap_analysis_20261001/GAP_REGISTER.md,
  verified on disk this sitting) was produced by seat discretion in the 10-01 run, not by script
  contract. Note the 10-01 provenance run 'Gap-analysis-100m' (completed 63,068,813 tok) ran
  mickey17-v2.dwf.ts's exact text (hash 34341bd5), not any gap-analysis file (see A2).
- Verdict: the mega-workflow exists as PROSE ONLY at both ends. The ~45-min wrapper move is still
  the right move, but it is wiring to BUILD, not a contract to LIGHT.

### Handed-JSON duplicate (index 4, truncated): same finding as F4, verdicted once above.

## Additions (what the lens missed)

### A1. The label-to-file mapping is not "by name only", it is actively unmoored, and the instrument to fix it already exists
21 of 138 fires (485,917,613 tok, 2026-10-01T08:56Z to 10-03T22:38Z) ran one shared script text,
sha256 11327967455d..., under 12+ labels; that text is byte-contained in all six family saved
files (drop-dig, fill-ball, librarian-expedition, salon-mine, the-gala, wide-dig). 'Ball-
20260929-dance2' (the lens's uncertain the-gala pair) ran hash bfc763fe (19,923 chars) which
matches NO on-disk file: it rode a retired text, so the pair is FALSE for the saved the-gala.dwf.ts.
Evidence: sqlite GROUP BY script_hash + containment test (run text substring of disk text) over
19 files x 79 distinct run texts; every check this sitting.
Falsifier: a labeled run whose text is NOT contained in its namesake file (already exists: every
pre-amend label) or a second clean mapping contradicting the shared-body reading.
Move: ~15 min. Build the hash-to-file containment map once and make every future fire census
group by script_hash (present on 138/138 rows) instead of by name.

### A2. gap-analysis has never had its own engine
'Gap-analysis-100m' (the 10-01 provenance run, completed 63,068,813 tok) ran mickey17-v2.dwf.ts's
exact text (hash 34341bd5 = mickey17-v2.dwf.ts by containment); the 10-03 fires
('Gap analysis: arena day one' failed 0-tok attempt at 21:13 also ran 34341bd5; the completed 21:18
run, the amend, and tonight's 'Gap-analysis-evening' all ran a8d2c84f = current gap-analysis.dwf.ts).
The chimera is not a one-off bug; it is the workflow's entire history.
Falsifier: a gap-analysis-labeled run with a third, gap-specific script hash.
Move: ~10 min. State the inheritance in gap-analysis.dwf.ts's header and stop describing it as a
15-auditor engine until the body matches the description.

### A3. The chimera is live and self-colliding in the mickey17 tree
'Gap analysis: arena day one' (completed 58,604,905 tok, 10-03T21:18Z to 10-04T01:39Z),
'Gap-analysis-amend', and 'Gap-analysis-evening' (running, 20.4M tok at read time) all fired with
no topic arg, so RUNSLUG collapses to "run-0" (gap-analysis.dwf.ts:90). Three runs share
memory/runs/mickey17_v2/runs/run-0/lanes (30 json files, dir mtime 2026-10-04T01:05:51Z); the
"per-run archive" first-fire fix (:87-91) defeats itself on every no-arg fire.
Falsifier: distinct RUNSLUG subdirs for those three runs.
Move: ~20 min. Throw on empty topic (the script already throws on empty targets at :124-126), or
derive RUNSLUG from the run label.

### A4. Three saved workflows have never fired in their current byte form, and one of them is the standing audit engine
0 of 79 distinct dwf_run script texts are contained in ractor-engine.dwf.ts, the-50.dwf.ts, or
music-cut.dwf.ts (strict containment + 1500-char mid-body probe, both zero). Every "Ractor" run to
date rode older texts (792dc8e7 x4 incl Ractor-fleet-meta and this run; 11d9bda2 x2; bfc763fe x8);
THE 50's two fires (fa5fb020) predate its saved file's current bytes. Gate PASS rows for these
files (registry rows 67/74, 2026-10-04T02:33Z) check the bytes but are not fires.
Falsifier: any dwf_run row whose text is contained in one of the three files.
Move: ~15 min. Fire each saved file once for real (or re-save from the last-fired text) so the
saved bytes and the proven bytes stop diverging.

### A5. The 0-token trio is no longer OWED: two causes, not one
Read from failure_json this sitting: (1) 'Ractor-fleet-meta' (created 22:37:54Z, cancelled
23:16:44Z): ProviderStop quota, "invalid_request [1005]: exceed quota limit", subagent
lens-lineage, providerId account:zai-start-plan, GLM-5.3-Flash. (2) 'Gap-analysis-amend' (created
22:38:57Z, cancelled 23:16:46Z): same quota stop, subagent lane-a03-tavern-curve, ~38 min of
subagent work that never banked a token. (3) 'Fill-ball-amend' (created 22:38:56Z, failed in 1 s):
DriverError "no lanes passed", the script's own throw at fill-ball.dwf.ts:96. The common "zero
tokens" reading is an accounting artifact on the two quota cases, not zero work.
Falsifier: the failure_json fields read differently on re-query.
Move: ~5 min. Bank this attribution in the dogfood receipt and close the OWED.

### A6. The lens's proposed script_hash receipt fix is already built; the real gap is file drift
dwf_run.script_hash exists on 138/138 rows and equals sha256(script_text) (verified exactly on the
Tree Doctrine row: stored da62eaa8c17f... == recomputed hash of its script_text; and Tree
Doctrine's hash is the same digest its own description cites as the gate registry digest,
tree-doctrine-dig.dwf.ts header). What is missing is not the column, it is the mapping: saved
files drift from fired texts (10 of 19 saved files match no run text byte-for-byte beyond the
header-strip; 3 match nothing at all, A4).
Falsifier: a row where sha256(script_text) != script_hash.
Move: ~10 min. Point the census at the existing column with the containment map (A1) instead of
adding anything.

### A7. Resume chains (lens blind spot 2) traced: 48/138 rows carry resumed_from
The game-dig veins each needed 5-7 resumed attempts to complete; the five completions cluster in a
12-minute span at the window's end (05:24:50-05:36:37Z on 09-27). Ball-20260929-dance2,
Hitler-dig-full-dogfood, Librarian, Salon-mine, OLM, Ractor-dogfood-gaps, Ractor-50-wave-retro and
the mickey17 first-fire all show cancelled/failed parent + resumed child pairs. Resume is the
fleet's normal recovery path, not an exception path.
Falsifier: a completed family run with no resumed_from ancestor.
Move: ~5 min. Count per-family resume depth in the standing census; resume depth is the real
reliability meter (the 42.0% per-attempt failure rate overstates fleet unreliability; per-logical
run it is far lower).

### A8. F5 recensus (banked report's keep-list numbers do not reproduce)
The banked F5 claims "olm-mine: 12 attempts across 5 distinct days, 30.1 percent of all fleet
tokens". Untruncated `%OLM%` name census this sitting: 9 rows across 5 distinct days (09-29 to
10-03), 1,185,997,264 tok = 23.2% of 5,111,769,862. The qualitative claim (the only sustained
multi-day cadence) HOLDS; the two quantities do not reproduce at this moment and were not in the
handed findings, so no verdict is entered, only the recensus.
Falsifier: a wider OLM match (e.g. including 'Frontier OLM mine' generational duplicates under
other hashes) that reaches 12 rows and 30%.
Move: ~5 min. Re-derive F5's two numbers from the same instrument as F2 before they circulate.

## Convergence flags
- My independent difflib re-run reproduced F1's ratios digit-for-digit: CONVERGENT, F1 outranks
  single-source findings.
- My independent dwf_run re-census reproduced F2/F3's counts digit-for-digit (138, 58, 42.0%,
  106,564,604, 34/29/643,862,449, the window): CONVERGENT.
- Additions A1-A8 are novel to this pass (run-level hash census, chimera lineage, run-0 collision,
  never-fired trio of files, trio cause, registry drift, resume chains, wheel-spec landing).

## Bottom line for the ask
Minimum viable fleet at byte level: 5 organs is defensible and now sharper: (1) the family shell
(11327967455d, one body, six headers, 21 fires), (2) mickey17-v2's engine (also gap-analysis's
actual engine), (3) olm-mine (the only multi-day cadence), (4) the game-dig shell (5 clones +
parent, 96-98% mutual), (5) the ractor lineage (currently unsaved-in-fireable-form, A4).
tree-doctrine-dig (1 fire ever), the-50 (dormant, saved bytes never fired), music-cut (saved bytes
never fired) are the retire-or-revive candidates, exactly the shape the lens proposed. Composition
is consolidation plus ONE wiring job (F4's wrapper), not chaining 12 engines.
