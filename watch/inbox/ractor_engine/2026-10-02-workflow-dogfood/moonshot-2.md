# moonshot-2: ractor the 12 saved workflows (dogfood the standing fleet)

Run: ractor_engine / 2026-10-02-workflow-dogfood, lane moonshot-2. Written 2026-10-04 ~02:50Z.
Instrument note up front, per the quantifier law: `ListWorkflowRuns` returned
`workflow_introspection_unavailable` in this session (same gap the dogfood-48h
run reproduced, watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md:130-132,
CONVERGENT). Every "fires" count below is therefore scoped to two instruments I
actually ran: (a) receipt folders under `watch/inbox/` listed by `ls`, and (b)
`memory/workflows/REGISTRY.jsonl` gate rows (63 rows at my first grep, 75 at my
last). A run that died pre-receipt, or filed receipts outside these shapes, is
invisible to me and OWED to whoever has introspection.

## F1. The standing fleet is 2 workhorses plus the gala battery; the rest is a museum

The ask's premise of "12 saved workflows" undercounts: `.zcode/workflows/` holds
19 `.dwf.ts` files (ls, this sitting), the 7 extra being 5 game-dig vein copies,
`game-mechanics-deep-dig`, and `music-cut`. Firing census (receipt folders, ls
this sitting): olm-mine has 5 (`watch/inbox/frontier_olm_20260928/` plus
`-2026-09-30`, `-2026-10-01`, `-2026-10-02`, `-2026-10-03`, the last's
RECEIPT.md opens "source-fetched: 2026-10-03"); ractor-engine has 5 dirs under
`watch/inbox/ractor_engine/` (ractor-topic, 2026-10-01-dogfood-gaps,
2026-10-02-dogfood-48h, 2026-10-03-grokbot-estate, 2026-10-03-surface-migration)
plus this run; the-gala's archive `watch/inbox/gala_20260925/` holds 18
per-run `*_RECEIPT.md` files (rung, gala-rung0, dd-selfsteal, build-it-all,
ractor50, vonnegut-final, hitler-dig, music-ractor, ouroboros, lyric-workover,
ball-20260929, ball3-suite-green, ball4-luncheon-follow, wave5-repair,
fillball-1001, librarian-expedition, salon-vault-stragglers, spiking-wide,
48h-synthesis). Everything else fired once or never: the six 10-01-wave
workflows have exactly one receipt set each (gap_analysis_20261001/GAP_REGISTER.md,
fillball/ 7 receipts, salon_mine/, librarian_exp/, spiking_wide/, localfirst/);
the-50's outputs stop at `memory/runs/the50/` mtime 2026-09-27 09:57 EDT and its
3 gate rows all stamp 2026-09-26T05:30-05:36Z (2 FAIL then PASS); tree-doctrine-dig's
founding receipts (TREE_DOCTRINE_*.md, 2026-09-25) predate its save and no
post-save receipt folder exists. Convention drift found inside the gala archive:
four OTHER workflows' receipts (fillball-1001, librarian-expedition,
salon-vault-stragglers, spiking-wide) live under `gala_20260925/`, so the
de facto shared run archive defeats folder-name accounting for everyone.
Falsifier: any second fire receipt for the-50 or tree-doctrine-dig post-09-27,
or any receipt for the 10-01 six-pack beyond the one set each.
Move (~35 min): a fleet ledger, one row per saved workflow with fires, last
fire, receipt paths, owned by the daily gap sentinel so "never fired twice" is
a query, not an archaeology dig.

## F2. The gate law had a 40-hour hole and THIS run closed it live

`AGENTS.md` (Build discipline) says no ungated CreateWorkflow and every check
registers a row in `memory/workflows/REGISTRY.jsonl`. Measured: the six 10-01
wave workflows ran 2026-10-01 and were saved 2026-10-02 morning (file mtimes
07:01 to 08:02), yet their first saved-path gate rows are stamped
2026-10-04T02:33:47Z to 02:34:06Z (fill-ball, salon-mine, librarian-expedition,
wide-dig, drop-dig; gap-analysis had one earlier row 2026-10-03T21:17:54Z). I
watched the registry grow 63 to 75 rows between two greps minutes apart in this
session: 12 PASS rows, one per named workflow, ~1 to 2 seconds apart, which is
this dogfood run (or its sibling) batch-gating the entire fleet mid-raction.
The gate exists at fire time, not at save time; saves sat ungated for ~40h.
Falsifier: a gate row for any of those five files dated before 2026-10-04, or a
SaveWorkflow hook I failed to find.
Move (~45 min): wire the save path itself, `workflow_gate.py check --script`
on SaveWorkflow, or teach `tools/census_drift_patrol.py`-style patrol to flag
saved definitions with zero gate rows older than N hours.

## F3. olm-mine's own description claims a cron that does not exist

The saved olm-mine description says "cron fires it with today's date as slug"
(ListSavedWorkflows text, same string in `.zcode/workflows/olm-mine.dwf.ts`
header). Measured this sitting: `MSYS_NO_PATHCONV=1 schtasks /Query /FO CSV`
full list read; the non-Microsoft root tasks are Estate* (7), mag-docker-watchdog,
Mag* (14: Census/Corpus/EndpointNews/Fts/GapSentinel/GateCanary/Improve/
Leave/QCaption/SecretScan/TipWitness/Vision/XRadar + 2 disabled), OpenClaw
Gateway, StartCN, cua-driver-serve. None names olm, mine, frontier, gala, or
ractor. Bounded grep `olm` over `scripts/ configs/ queue/` hits only
`queue/handoff/zcode/CONVO.md` conversation files. The fleet's ONLY daily-cadence
workflow is hand-fired by seats while 14 lesser surfaces enjoy scheduled tasks.
This is the phantom-citation disease in metadata form: a description asserting
infrastructure that is not there.
Falsifier: an olm-mine task under Task Scheduler (including any nested folder I
filtered, though my CSV grep for mine/olm/frontier across the full CSV read
nothing), or a driver-stack automation firing it outside schtasks.
Move (~20 min): register OlmMineDaily reusing the `scripts/fts_index_daily.ps1`
pattern, or amend the description to "seat-fired, daily habit" today.

## F4. Five saved files are one fan-out engine wearing different coats; the-50 freezes dead data in source

The gate's own G1-G7 vocabulary (Mickey17 gopher fan-out, passoff, steering,
salvage, deliverable, receipts, laws, read in REGISTRY.jsonl rows) is ONE shape:
fan-out, verify, steer, fold. Saved copies of it: mickey17-v2, the-gala, the-50,
tree-doctrine-dig, game-mechanics-deep-dig. the-gala is the general form: lanes
arrive as a json arg, `{id, division, what, start, finish, evidence}`
(`.zcode/workflows/the-gala.dwf.ts:18-21`). the-50 hardcodes a ~40-row TASKS
table from a 2026-09-18 program into source (`.zcode/workflows/the-50.dwf.ts:31-70`)
and its own amendment comment admits the lineage direction: "t83 amendment ...
amended in place per the-gala.dwf.ts idioms" (`the-50.dwf.ts:22`). The 5 game-dig
vein files are byte-near-twins: `diff game-dig-coop-social.dwf.ts
game-dig-roguelike-runs.dwf.ts` = 25 changed lines of 168, description and brief
content only; the parametrized parent `game-mechanics-deep-dig` already exists
and takes `briefs_path` + `vein_slug` args. Minimum fleet arithmetic: the-gala as
the single battery engine (mickey17-v2's two-tier DeepCheck/ReviewVerdict
verification ports in as an optional division), game-mechanics-deep-dig as the
single dig-parent (vein files become args), the-50 and tree-doctrine-dig retire
into their grave receipts.
Falsifier: a structural capability in mickey17-v2 or tree-doctrine-dig that a
gala lane type cannot express; I read heads and interfaces, not full files, so
this is the claim most likely to have an exception hiding in it.
Move (~90 min): one sitting to port DeepCheck as division D into the-gala, mark
the 4 absorbed descriptions retired (amend, never delete, per the gala grave
law), and delete-or-merge the 5 vein files into deep-dig args.

## F5. The designed mega-workflow exists only as prose; nobody ever ran the loop

The composition is already written down twice: gap-analysis's saved description
("the register this emits IS fill-ball's lane table") and fill-ball's ("work ->
gap-analysis -> fill-ball -> (ractor-engine on anything ambiguous)";
`.zcode/workflows/fill-ball.dwf.ts:17` takes the register path as an arg). The
handoff is a human copying a path. Measured: every stage of the loop was fired
exactly once, all on 2026-10-01 (F1 census), and never chained again. The 10x
move is one composed self-repair cycle, burst -> gap-analysis -> fill-ball ->
librarian-expedition (holdings close) -> ractor-engine (verdict), with the
register path passed by reference. This run is a live proof-of-concept waiting
to happen: its findings array IS a register.
Falsifier: any wrapper that chains them, or mechanical (non-human) handoff
evidence in the 10-01 receipts.
Move (~60 min): amend fill-ball to accept slug-only and resolve the register
itself, then fire the composed loop once on this run's own findings before the
window closes.

## OWED (honest residue)

- Whether the 2026-09-29 MICKEY17 wave rode the saved mickey17-v2 workflow or a
  draft: no receipt folder ties it to the saved script name. OWED.
- music-cut: saved 17:55 and gated 2026-10-03T21:56:30Z today, but I found no
  post-gate receipt folder. Fire status OWED.
- Which seat fired the 02:33Z batch gate sweep: correlation is temporal only.
- Per-ball attribution inside `gala_20260925/` (which receipts rode the saved
  the-gala file vs pre-save drafts): OWED.
- mickey17-v2 vs the-gala full structural diff: not run (heads and interfaces
  only). OWED.

## CONVERGENT flags

- workflow_introspection_unavailable: independently re-derived from the 10-02
  run (SYNTHESIS.md:130-132). Counts as emphasis, outranks my novel findings.
- Built-never-fired organ disease (seed_seal, percolator --candidates,
  SYNTHESIS.md:55-58, 153-158) is the same genus as my F1/F3 at the workflow
  layer: the estate builds faster than it fires, then describes the firing it
  never did. Two lenses, two layers, one law.

Filed by moonshot-2. Em-dash count 0 (checked on write). Every number above was
read or ran this sitting; nothing hand-copied.

## HOSTILE-PASS CORRECTIONS (2026-10-04 ~03:10Z, second pass verdicted F1 and F4 weakened; re-checked this sitting)

F1 CORRECTED (weakened, survives with three fixes). The critique's three hits
all verify against estate bytes: (a) `watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json`
exists, filed "2026-09-29T00:20:52Z" per its own header, finish_line
tools/oracle_calibration.py, program_row THE_50_PROGRAM_20260918.md line 46;
my "outputs stop 2026-09-27" claim dies, and my own falsifier fired: the-50's
one fire has straggler receipts through 2026-09-29T00:20:52Z (T26 straggler
09-27T01:07:04Z). No the-50 fire evidence after that moment exists in any
census I ran. (b) mickey17-v2 is MULTI-FIRE: `ls memory/runs/mickey17_v2/runs/`
shows 4 run trees (agent-engineering-frontier-sweep-40 Sep 25 19:21,
gauntlet_w4 Sep 26 00:41, gap-analysis-of-the-estate-s-09--15 Oct 1 19:37,
run-0 Oct 3 21:05); my per-workflow table wrongly filed it one-fire-or-never,
and I never opened this census site. (c) Double-count confirmed: of my 18 gala
receipts, 5 (fillball-1001, librarian-expedition, salon-vault-stragglers,
spiking-wide, localfirst-steal) are the receipt side of the same 10-01 wave
runs whose lane outputs I also counted in the standalone folders:
gala_20260925/spiking-wide/ holds a lanes/ dir while spiking_wide/ holds the
8 lane .md files; gala_20260925/localfirst-steal/ holds lanes/ + fetched/ while
localfirst/ holds adjacent.md, aida.md, atlas.md, lbrain.md, ownmem.md, pam.md,
ragos.md. All 18 receipt mtimes span 2026-09-29 10:00 EDT to 2026-10-03 18:19
EDT (stat, this sitting), all post-save. Corrected fire table: multi-fire =
olm-mine (5), ractor-engine (5 dirs + this run), the-gala (13 non-double-counted
gala receipts, Sep 29 through Oct 3; per-ball engine attribution the-gala vs
ractor-lineage drafts is OWED), mickey17-v2 (4 run trees). One-fire-or-never =
gap-analysis, fill-ball, salon-mine, librarian-expedition, wide-dig, drop-dig,
the-50 (one fire, stragglers to 09-29T00:20:52Z), tree-doctrine-dig, music-cut
(unresolved). New structural fact surfaced by the hit: the 10-01 estate gap
analysis RODE THE mickey17-v2 ENGINE (memory/runs/mickey17_v2/runs/
gap-analysis-of-the-estate-s-09--15/, FOLD_SECTIONS.md opens "MICKEY-17 v2.1
SCRIPTED FOLD SECTIONS", 32 lane files = 16 auditor lanes a01-a16 x .json +
.checks.json), so the six saved 10-01 definitions are post-hoc formalizations
of runs that fired on mickey17-v2's run tree, not evidence the saved files
fired. Headline survives: 4 engines carry every fire in the fleet; the coat
count is still 19.

F4 CORRECTED (weakened, collapse claim strengthened). My blind-spot candidate
exception is disproven by grep: `grep -c DeepCheck` gives mickey17-v2.dwf.ts 7,
the-gala.dwf.ts 5, the-50.dwf.ts 0, tree-doctrine-dig.dwf.ts 0. the-gala
already carries the two-tier verification (interface at :67, deepAsk at :189,
fan-out at :364-367 with agent("deep-" + x.lane + ...) mechanical verifiers),
so mickey17-v2 needs NO port to collapse into the-gala; the cost of my proposed
90-min port drops to a description amendment. The-50 is the actual structural
outlier (0 DeepCheck, hardcoded TASKS at :31-70, artifact-existence
verification instead), and tree-doctrine-dig is a zero-arg frozen one-off.
Corrected move (~30 min): amend mickey17-v2's and tree-doctrine-dig's
descriptions to "retired, ride the-gala" and merge the 5 game-dig vein files
into game-mechanics-deep-dig args; the only real porting work left is the-50's
artifact-existence check becoming a gala lane field, if anyone ever wants a
second fire.

Bank note: this section appends; the original text above is left standing per
the no-deletion law, and its two wrong lines (outputs-stop-09-27,
mickey17-one-fire) are corrected here, not edited in place.
