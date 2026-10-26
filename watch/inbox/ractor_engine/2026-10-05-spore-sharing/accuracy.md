# ACCURACY LENS - THE SPORE SHARING PROBLEM (2026-10-05)

Lens: falsifier-hunter. Every claim below was byte-checked in this session
against the working tree at branch `mag/run-beta1-factory-build-audi-20260806T231709Z`,
moment 2026-10-05. Counts name instrument and moment. Absences name scope.
Nothing here is asserted without a path, a command, or an OWED mark.

## HEADLINE

The spore problem as posed ("push the estate to github.com/NachoBusiness17/mycelial-republic")
rests on three false premises and one missing artifact. False premise 1: that
repo already belongs to the FOREST project and already carries an opened copy
of the mag core. False premise 2: that a push of this repo is survivable - the
history carries key material by the estate's own admission and the pack is
14.37 GiB. False premise 3: that the tracked tree can boot the strongest
version - the rails' front-door config has no tracked template, so Genome Law 1
is unbootable from the shareable bytes alone. The missing artifact: a spore
exporter. The estate already built its inverse (the travel kit, which carries
.env by design) and already did one forest export by hand (3da416c), but no
repeating mechanism for a de-riddled public spore exists in the tree.

## FINDING 1 - The push target is already owned by the forest, and estate history is radioactive

Evidence:
- `git remote -v` (this repo): `github https://github.com/NachoBusiness17/mycelial-republic.git`
  is wired as fetch+push on the ESTATE. The same URL is `origin` of the sibling
  forest (`git -C ../mycelial-republic remote -v`).
- `git ls-remote github`: remote `master` = `dc66499434`, which is NOT an object
  of this repo (`git cat-file -t dc66499434...` -> fatal). It IS the forest's
  tip: `git -C ../mycelial-republic log --oneline -3` shows `dc66499 Add the
  game bones...` and `3da416c Add Sovereign Framework: the real machine core
  (30 mag modules + configs + build files) opened for collaboration,
  runtime/secrets excluded, secret-scanned`. An opened mag core has ALREADY
  been published once, by hand, into the forest repo.
- `git log --all --diff-filter=A -- "*.key" "*.pem" "*.env"`: exactly one hit,
  `799ddb6fe 2026-08-19 memory/tls/lan.key`; `git show 799ddb6fe:memory/tls/lan.key | wc -c`
  = 1675 (blob exists and is non-empty; content not printed). The in-tree
  .gitignore 2026-10-03 block says: "secrets / key material (lan.key untracked
  same day; rotate - it remains in history)". The 2026-09-30 block admits
  "7 live .env values were committed" in memory/trajectory/steps.jsonl,
  "history left intact per operator (no rewrite)".
- Weight: `git count-objects -vH` -> `size-pack: 14.37 GiB` (count 12782, plus
  3 tmp_pack garbage warnings). `git ls-files | wc -l` = 56,359 tracked files;
  `git ls-files watch/inbox | wc -l` = 17,069, of which 5,061 are .md receipts.

Consequence: `git push github <any-estate-branch>` ships 14.37 GiB of history
including the lan.key blob and the admitted .env-value commits into the forest's
public repo as a new branch. One command, one leak. The de-riddled spore must be
a fresh-root export, never a push of estate history. The 3da416c precedent is
the shape; it has no repeater.

Falsifier: repoint `github` to a dedicated new repo AND build the spore branch
orphan-rooted AND pass a full-history secret scan -> this finding no longer
applies to that path.

Move (one sitting, ~60 min): run the instrument that already exists,
`.venv\Scripts\python.exe tools\secret_gate.py check --history` (flag at
tools/secret_gate.py:119-120, "scan every ADDED line across git history"),
to census the full dirty surface, then build the orphan-root export from its
allow-list. NOT RUN in this session (14.37 GiB pack, operator-scale job);
reported as not run.

## FINDING 2 - The spore cannot boot its own Law 1: the rails' front door has no shareable config

Evidence:
- state/GENOME.md:16-19 (Law 1) and queue/STANDING_RAILS.md:10-12: every model
  call goes through mag/route_chat.
- mag/route_chat.py:51 reads `configs/providers.yaml`; :61-70 falls back to a
  literal line-scan of `ROOT/.env`.
- .gitignore: `configs/providers.yaml` is gitignored as "live provider/mesh
  credentials - never commit (tracked fix 2026-08-20)".
- `git ls-files configs | grep -i provider` -> EMPTY. The only sibling on disk
  is the untracked `configs/providers.yaml.bak-20260826-pre-deepseek-swarmcap`.
  There is NO tracked providers.yaml.example, generator, or schema. (.env.example
  IS tracked and names the key vars: XAI, OPENROUTER, DEEPSEEK, GEMINI, GROQ...)

Consequence: a cold operator regrowing from the tracked bytes gets .env.example
but no lane table, no fences, no depth attestation config - the genome's first
law points at a file the spore cannot carry and does not template. The
"strongest version" is not regrowable from the tracked tree alone.

Falsifier: a tracked configs/providers.yaml.example (or a generator script)
appearing in git cures this outright.

Move (~30 min): write configs/providers.yaml.example from the live file, keys
blanked, lanes intact, and wire a freshness note into the regrow guide.

## FINDING 3 - The routing brain is already shared state: gps_ledger.db3 is tracked, hot, and binary

Evidence:
- tools/arena_gwap.py:57: `GPS_LEDGER = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"`.
- `git ls-files tools/gps_mcp | grep db3` -> `tools/gps_mcp/gps_ledger.db3` AND
  `gps_ledger.db3.bak_pre_D2_20260930` are TRACKED.
- `git log -1 --format="%h %ad" -- tools/gps_mcp/gps_ledger.db3` -> `e80f48b8f
  2026-10-05` (committed TODAY); on-disk size 782,336 bytes, mtime Oct 5 03:15.
- Runtime lane state is also tracked: `git status` shows M on
  queue/lanes/{builder,day_work,research}/runner_state.json;
  queue/lanes/research/runner_state.json carries `rotation_epoch: 242`,
  `last_run: 2026-10-05T11:01:10Z`.
- mag/lane_runner.py:134: "the lock is external and transient, not code-side";
  :139 the cure pattern is local rename-CAS (win32 filter locks). No cross-seat
  claim system exists in the runner.

Consequence at N=2: every seat mutates the same tracked binary sqlite and the
same tracked runner_state files; git merges cannot resolve binary sqlite, so
operators either clobber each other's capability ledger at every push or fork
into divergent routing truths. A public repo also publishes the estate's
measured capability profile (win rates, fail streaks, model mix). At N=8 the
conflation gets worse and the "effective rates" the router trusts (D7
metabolism, EG-20 pass@K both read this ledger) become a blend of eight
different workloads - the rate is no longer anyone's rate.

Falsifier: untrack the db3 + ship a seed fixture, or add per-operator ledger
namespacing plus a real claim/lease layer -> N=2 composes and this finding is
falsified for that path.

Move (~45 min): `git rm --cached tools/gps_mcp/gps_ledger.db3*`, gitignore it,
commit a small seed fixture, and let each estate grow its own ledger privately
(trade summaries as receipts, not the binary).

## FINDING 4 - The republic's answer is already written in the bytes: forked estates trading receipts, not a shared chain

Evidence:
- ../mycelial-republic/README.md (read this session): "A living, forkable
  decentralized intelligence layer... Spores replicate. Nodes interconnect."
  Phase 0 "Seed Mirror"; canonical agency shape = docs/AGENCY_SHAPE.md.
- AGENTS.md (this repo): "Zeitgeist: beads (this repo) + forest
  (mycelial-republic)" - the two-repo split is doctrine, not accident.
- .gitignore: `memory/seals/` is local-only ("opsec; chain data stays on the
  machine"); `memory/runs/**` is ignored (gwap payloads/chain live local-only,
  whitelisted only README); `memory/mycelium/`, `memory/thinking/` ignored.
- The one shared substrate that exists is the public repo itself: forest master
  already carries the opened core (3da416c) and a response-doc thread
  ("ADDENDUM II - the Hologram").

Consequence: the mycelial republic is ALREADY the fork-and-trade topology:
each estate keeps its verkle chain and season ledger local, publishes opened
cores, and interconnects by receipts. "Shared chain" has no byte anywhere in
the organs. The spore's job is to make the fork leg REPEATABLE - the regrow
guide plus a de-riddled exporter - not to invent new coupling. Trap to name in
the guide: scripts/build_travel_kit.py (docstring line 4, manifest lines 156 +
166) deliberately packs `.env` and live ledgers for TWO_MACHINE_SYNC - it is
the secrets-bearing inverse of a spore and must never be the publish path.

Falsifier: a common verkle anchor registry or cross-seat chain substrate found
in either repo would revive "shared chain"; I found none (scope: .gitignore
seals comments, forest README, arena_gwap ledger wiring - not an exhaustive
full-tree census).

Move (~90 min): write the regrow guide around fork + receipt-trade: orphan-root
export (Finding 1 shape), providers.yaml.example (Finding 2), seed fixture
(Finding 3), then boot order GENOME -> STANDING_RAILS -> ribs -> CURRENT ->
Delta Register exactly as state/GENOME.md:71-75 already prescribes.

## FINDING 5 - The topic's own numbers half-fail the byte check (accuracy on the brief)

Evidence (all run this session, 2026-10-05):
- "26 doctrine ribs" PASSES: `grep -c '"invariant"' memory/rib_bus/doctrine.json`
  = 26 exactly (standing-wave.json carries 87 more).
- "The 10 corpus steals" FAILS as stated: `ls corpus/steal/*.md | wc -l` = 32
  on disk. Provenance found: the term enters the topic verbatim from
  watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md:157-159 ("state/
  GENOME.md. queue/STANDING_RAILS.md. The 26 doctrine ribs. The 10 corpus
  steals. The season ledger. The Delta Register.") - a receipt whose closing
  line claims "Every claim in this summary cites a banked artifact" (line 161),
  yet these two nouns carry no path. The "10" is either a curated canon subset
  (unidentified) or drift from the 32 on disk. OWED: the canon list of exactly
  10, or recount.
- "The season ledger" resolves only partially: `grep -rn "season"` over tools/,
  mag/, configs/ .py files finds flavor strings only (tools/dungeon.py:715 "the
  season continues"; tools/fullsend_s2.py:1,12 "season 2"). Nearest real
  anchors from the same receipt: line 77 "Receipts: the dnd0_* DONE rows,
  watch/inbox/THE_FIRST_SEASON_story" - the arena season's chain of DONE rows,
  which lives under memory/runs (gitignored) with receipts in watch/inbox
  (tracked). A file named "season ledger" does not exist by that name anywhere
  my scoped greps reached.
- The tutorial's "~5% of paid" free-lane economics: NOT FOUND in the named
  instruments - `grep -n "%"` in memory/rib/RIB_FREE_USAGE_POLICY_20260823.md
  returns only a ~98% cache-hit line; RIB_DRIVING_LADDER_20260928.md has zero %
  lines; watch/inbox/LITE_LANE_PULL_20261003.md gives the z.ai-lite shape
  (ZAI_API_KEY_Lite, glm-5.3-flash, lite_guard 10K credits/wk) but no paid-ratio
  arithmetic. OWED: a receipt carrying the ~5% computation, or strike the number
  from the tutorial.

Consequence: the tutorial and regrow guide must inherit ONLY byte-checked
numbers. The estate has a named disease here (the struck 191.8M phantom,
kept as the citation-lint founding fixture) and a gate (tools/citation_lint.py)
- writing the spore docs through that gate is the difference between sharing
knowledge and sharing the scars.

Falsifier: locating the exactly-10 steals canon list, a season-ledger file
under that concept, or a receipt carrying the ~5% arithmetic flips each item
to verified.

Move (~45 min): before drafting the tutorial, resolve the three OWEDs against
the arena receipt's own sources, or mark them OWED in the spore docs.

## BLIND SPOTS (what this lens could not see)

1. Full-history secret census NOT RUN: the "history is dirty" verdict rests on
   the lan.key blob (799ddb6fe, 1675 bytes) plus the estate's own .gitignore
   admissions, not on tools/secret_gate.py --history over the 14.37 GiB pack.
   The true count of live secrets in history is OWED.
2. lan.key rotation status unverified: the blob exists; whether the LAN TLS
   pair was actually rotated is outside my reach (state/CURRENT.md:72-73 still
   owes item 7, "Rotate the LAN TLS pair").
3. Working-tree receipt census not run: I verified the CLASS is tracked (5,061
   receipt .md) and that the 2026-10-01 .gitignore catch admits scrape exhaust
   "may carry third-party tokens", but did not scan the 5,061 files for live
   tokens. That is the secret gate's job on the export candidate, not done here.
4. N=4/N=8 gradients are design analysis extrapolated from N=2 mechanics (git
   write races, binary merge, rate conflation). No multi-operator simulation,
   load test, or second seat exists in evidence. The breakage claims are
   structural, not measured.
5. Forest depth: I read the forest README head and its git log; docs/
   CONSTITUTION.md and docs/AGENCY_SHAPE.md bodies are unread. The republic's
   full self-model may refine Finding 4 beyond fork-and-trade.
6. "Season ledger" and "10 corpus steals" carry provenance (the arena receipt)
   but no definitive file mapping; my greps were .py-scoped plus one receipt
   read, not a full-tree text census of 56,359 tracked files.

## INSTRUMENT LOG

git remote -v; git branch --show-current; git ls-remote github; git -C
../mycelial-republic remote -v / log; git cat-file -t dc66499434; git log --all
--diff-filter=A -- "*.key" "*.pem" "*.env"; git show 799ddb6fe:memory/tls/lan.key
| wc -c; cat .gitignore; git ls-files (+ grep for env/secret/token, watch/inbox,
configs/provider, tools/gps_mcp, queue/lanes, LICENSE); git count-objects -vH;
grep -c invariant on doctrine.json and standing-wave.json; ls memory/rib |
wc -l; ls corpus/steal/*.md | wc -l; sed on tools/secret_gate_scan.py,
tools/secret_gate.py, scripts/build_travel_kit.py, .env.example,
RESEARCH_SUMMARY_arena_days_one_two_20261005.md; grep on mag/route_chat.py,
mag/rib_bus.py, mag/lane_runner.py, tools/arena_gwap.py, tools/dungeon.py,
tools/fullsend_s2.py, tools/gps_mcp/*.py, both ladder ribs,
LITE_LANE_PULL_20261003.md; head of ../mycelial-republic/README.md. All on the
branch and tree named in the header, 2026-10-05.
