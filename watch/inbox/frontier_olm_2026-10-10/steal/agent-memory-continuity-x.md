# STEAL CARD: agent-memory-continuity-x (frontier_olm 2026-10-10, round 2)

Round 2 amended per review (verdict: one blocking fix, find 1 provenance; every other byte
reproduced by the reviewer). Amended this round: find 1's overlap and OWED now credit the estate
holdings the review surfaced (the 09-30 percolator port shape and the 10-05 decision rule, both
verified verbatim by this seat before amending); round 1's overlap grep is restated honestly (it
was head-truncated at 5 files per id, and the deepest SAGE hit, the 09-30 file, appeared in the
broad pass and was then dropped in synthesis); the sibling cite is split; the cascade queue's
zero rows are named; the coverage screen's rule is spelled out and re-run; the trajectory counts
are moment-stamped with the strict/loose definitions named.

Seat: steal gopher, area agent-memory-continuity-x. Four confirmed finds from this run's x-door
sweep (the door ran degraded; every banked read landed via arxiv.org or raw.githubusercontent.com,
declared at `watch/inbox/frontier_olm_2026-10-10/sweep/agent-memory-continuity-x.md:8`, read in
full this session; below, "sweep" is that file). Quotes are ask-carried verbatim from the sweep's
banked items (sweep:53-57). MemoWM's headline numbers were additionally verified this session
against the local full text the sweep left on disk (`sweep/_tmp/txt_2610.10778.txt:116,185-186`).
Every estate byte below was read, counted, or executed this sitting; commands are named inline.
Anything not verifiable is marked OWED, never asserted.

## Headline steal (mechanism, not a link dump)

The four finds assemble into one gated write path for agent memory, in commit order:

1. ACCEPT: an edit lands only when its per-item paired wins are statistically reliable against
   its losses; closed-form statistics, no LLM judge, no replay pool (SAGE,
   https://arxiv.org/abs/2609.36043).
2. ALLOCATE: store only what exceeds the world model's predictive prior; reconstruct the rest and
   pay an explicit reconstruction-error-versus-storage trade (MemoWM,
   https://arxiv.org/abs/2610.10778).
3. IDENTIFY: two memory states are the same state only when their shared actions lead to agreeing
   outcomes and successor blocks; observation similarity never enters the rule; nothing is trained
   (action-conditioned bisimulation, https://arxiv.org/abs/2609.38778).
4. INGEST CHEAP: the write side stays near-free (verbatim append-only, LLM-free insertion) or the
   amortization ledger goes negative at ingest (MemFit, https://arxiv.org/abs/2610.00872).

Estate one-liner: the percolator's promote path gets the statistical acceptance gate it lacks
(the decision rule itself is estate-held at digest depth since 10-05; the wiring, probe, and
falsifiers are this card's contribution); the world-rib schema gets its two missing laws
(allocation calculus plus territory identity, the exact gap of laws lens q4); the context pack's
write side is measured already near-free this session, so the MemFit port is the verbatim
retrieval mount, not ingest machinery.

## Find 1: SAGE, a statistical acceptance gate for self-evolving agents

Organ: percolator (write gate). Secondary: the gopher fleet's candidate intake.

Quote (ask-carried, sweep:54): "a one-sided paired test that commits an edit only when its wins
are statistically reliable against its losses".

Mechanism: per-item paired comparison of current versus edited behavior; a one-sided test commits
only on reliable net wins; an asymmetric penalty makes regressions expensive; closed-form
statistics with no LLM judge; regression rates cut in 19 of 20 settings (sweep:30). The estate
already holds the decision rule at digest depth, banked by the 10-05 evals sweep and verified
verbatim this session: "one-sided exact conditional binomial test (reduces to one-sided exact
McNemar at lambda=1); commit only if discounted net gain > 0 AND p < alpha AND regression
fraction <= tau; abstain otherwise (m=0 means p=1 means abstain)", with the ablation split
"paired comparison alone gives +6.20, the statistical test adds +2.53"
(frontier_olm_2026-10-05/sweep/evals-self-improvement-arxiv.md:42). The sweep itself staked the
port: "SAGE's paired test is the acceptance gate a fill-ball should pass before minting a steal
node" (sweep:30).

Estate map, OVERLAP STATED:
- Id-level: no steal card anywhere in watch/inbox mentions 2609.36043 (rg over every
  `frontier_olm_*/steal/*.md`, run in rounds 1 and 2: zero hits other than this card). The
  estate holds MORE than round 1 credited, in three places. (i) The 09-30 evals sweep banked this
  card's own port shape at digest depth: "the direct upgrade path for mag/percolator.py:264-272's
  bare counter" and "Steal-shape for the percolator: promotion = paired per-invariant comparison
  current-law vs candidate on identical probes, commit only on statistically reliable wins,
  abstain otherwise; a bare never-regressed count is not an instrument"
  (frontier_olm_2026-09-30/sweep/evals-self-improvement-arxiv.md:41, verified verbatim this
  session; same organ, same mechanism shape, banked 10 days before this card). The named region
  exists and reads seal/invariant generations (sed of mag/percolator.py:264-272 this session);
  the bare-counter characterization is that row's, not re-derived here. (ii) The 10-05 evals
  sweep banked the full decision rule and ablation (quoted in the mechanism above, :42). (iii)
  The 10-06 evals files carry both as register candidates
  (`frontier_olm_2026-10-06/sweep/evals-self-improvement-arxiv.md:80`,
  `evals-self-improvement-hn.md:53`). Provenance confession, per the review: round 1 wrote "this
  card adds the port mapping only", which understated the estate's holdings, and round 1's per-id
  grep was head-truncated at 5 files per id, so the 09-30 file never reached the list round 1
  synthesized from, even though the earlier broad pass had shown it. The instrument is restated
  in Checks. What this card actually adds, stated exactly: the queue wiring (which review queues
  the gate serves, with the cascade queue's zero rows named below), the git-history replay probe
  with its two falsifiers, the revert census (0 revert-named commits, so catch-value cannot be
  calibrated on history), and the cross-area pull: the mechanism lived in the evals area's files
  with no organ wired to it, and this card moves it onto the memory-continuity wire so the fold
  sees one port, not two.
- Mechanism-level: the write-gate wire is crowded and this card joins it rather than re-minting
  it. Day-9 owns the read half ("The port move is the read half plus the activation gate, not more
  edges", `frontier_olm_2026-10-09/steal/agent-memory-continuity.md:15-19`). Today's sibling
  Skill-V card owns the deterministic write-gate legs: structural validation is its port move A
  (`frontier_olm_2026-10-10/steal/agent-memory-continuity.md:53-55`), shadow replay and
  non-regression are its port move B (sibling :56-63), and its OWED names the exact hole SAGE
  fills: the candidates' cited receipts "have no replay harness yet" (sibling :179-185). SAGE is
  the no-replay answer to that OWED: paired outcomes are computable wherever a before/after
  behavior pair exists, and the estate already owns a paired-outcome generator (pytest; see
  probe). The legs compose: Skill-V checks structure (criterion ids, versions), SAGE decides
  numerically whether the edit keeps its wins.
- Concrete port move: an `accept_paired(wins, losses)` gate function in mag/percolator.py
  implementing the estate-held decision rule (one-sided exact conditional binomial over
  discordant pairs; commit only if discounted net gain > 0 AND p < alpha AND regression fraction
  <= tau; abstain otherwise), wired as the numeric decision inside the standing promote path
  ("promotion happens only through the standing percolate() path on reviewed signal",
  `mag/percolator.py:26-27`). Today that path has structure checks and count laws (half-life,
  heal-merge max, self-emission cap, `mag/percolator.py:29-39`) and a cascade that emits
  PROPOSALS, NEVER MUTATIONS (`mag/percolator.py:54-58`), but no statistical acceptance anywhere
  (the 09-30 row said the same about the bare counter, :41). The gate serves two queues, stated
  honestly: the candidates lane (measured this session: 31 rows, 26 promoted=False, 0 ever
  promoted; `.venv/Scripts/python.exe` json count over memory/percolator/candidates.jsonl) and
  the cascade queue, which is a code path with ZERO rows today: memory/percolator/cascade_queue.jsonl
  does not exist on disk (ls memory/percolator/ this session; the path constant sits at
  `mag/percolator.py:737` and the file is created on the first cascade run), so the gate's first
  live decisions would all be on the 26 pending candidates. The gopher fleet feeds the first
  queue directly (digest ingest, `mag/percolator.py:23-24`).

Probe (falsifiable, this week, $0, deterministic): replay the gate over git history. For the last
10 commits touching mag/, run the affected test files at parent and child, build per-test pass/fail
pairs (wins = fail-to-pass, losses = pass-to-fail), apply the one-sided paired test with asymmetric
loss penalty. Two falsifiers: (a) if the gate REJECTS kept commits that carried zero losses and net
wins, the closed form miscalibrates at estate paired-n scale (tens of items, not the paper's
20-config settings) and the port needs the sample-size guidance before landing (constant values
and sample-size guidance OWED below); (b) history cannot calibrate catch-value at all: `git log
--oneline --grep=revert -i` returns 0 commits (verified this session), so no landed regression
exists to catch and the gate's first live decision must be prospective, on the 26 pending
candidates. NOT RUN this session (the replay is the probe; only its inputs were measured).

## Find 2: MemoWM, the allocation calculus for what memory must hold

Organ: quantizer. Secondary: knowledge_graph schema v3, world_rib schema v2.

Quote (ask-carried, sweep:53): "uses shared predictions to compress retained information and
reconstruct omitted content".

Mechanism, verified first-hand from the local full text (txt_2610.10778.txt:116): "Its task-aware
allocation rule balances the expected impact of reconstruction errors against storage cost,
retaining information with downstream value beyond the predictive prior." Measured there: 42.42
percent average accuracy, plus 2.62 points over the strongest baseline, average experience-specific
storage down 53.9 percent relative to MIRIX (txt:116, restated at txt:185-186); stronger world
models reduce per-experience storage, and storage-optimal shared-model capacity grows as more
interactions are retained (txt:116).

Estate map:
- The quantizer today compresses by aggregation only: N verkle knots become one lossy quantum
  summary knot via theme vectors, tension indices, pattern transitions (`mag/state_quantizer.py:1-19`);
  the module's stated design has no store-versus-reconstruct decision anywhere (header and
  architecture read this session). Port: the aggregation gains MemoWM's allocation rule as its
  admission criterion: an element enters the dense summary only if its residual against the
  estate's predictive prior (rib law-heads, invariants) carries downstream value; the rest is
  pointerized and reconstructed on read, with reconstruction-error tolerance an explicit knob.
  knowledge_graph schema v3 gains the store_vs_reconstruct column exactly as the sweep's RQ4
  column 4 specified it ("the graph analogue is not storing derivable joins", sweep:38), which
  answers the linking poverty measured by the graph lens (122/140 steals zero-degree, only 18
  already_inside edges, `lens/graph.md:33`) by making derivable joins non-storage.
- OVERLAP STATED: MemoWM is the one clean-new find of the four at steal depth. The id appears in
  no prior-day file except day-9's census, which explicitly left it among 17 unread candidates
  (sweep:15, and the ask's own overlap field); the 3 catalog rows are this sweep's own intake
  artifacts (zone intake, mtime 2026-10-10T14:55-14:56Z, verified by `rg -o` over
  catalog/catalog.jsonl this session).

Deterministic screen, RUN this session (`.venv/Scripts/python.exe` unigram-coverage script,
command shape in Checks): retained rows versus model surface. Model surface = memory/rib_boot.json
+ memory/warm_state.json + today's six lens files (2,391 content words). Retained: the candidates'
claim+falsifier text (30 of 31 rows had content words): mean coverage 0.665 (min 0.491, max 0.846);
memory/zknot/LATEST.md: 1,677 words, coverage 0.723. Honest reading, both directions: (a) shared
provenance inflates these numbers (the lens digests summarize the very sweep that produced the
candidates), so 0.665 is an optimistic ceiling on reconstructible lexical material, not a
reconstruction rate; (b) the floor is the useful half: at least a third of retained-row vocabulary
is model-invisible residual that no allocation rule may drop. The paper's achieved 53.9 percent
cut sits below the optimistic ceiling, so the port is not vocabulary-starved; the screen cannot
prove reconstruction and does not claim to. Round 2, per review, the rule spelled out so the
screen is reproducible from this card alone: tokens are re.findall(r'[a-z]{4,}') over lowercased
text; the stoplist is the 33-word list "this that with from have been will would there their
about which when what where into more most than then them they some such only over also just
like after before other while these those upon through"; the surface is memory/rib_boot.json +
memory/warm_state.json + the six lens/*.md files (8 files, 2,391-word vocab); the metric is the
fraction of a row's non-stopword tokens present in the surface vocab. Re-run at
2026-10-10T14:33:20, the numbers reproduce exactly: 30 rows, mean 0.665, min 0.491, max 0.846;
zknot 0.723 over 1,677 words. The reviewer's independent analog with a different stoplist lands
at mean 0.650 over 30 rows (vocab 2,897): same shape, so the claim is robust to the stopword
choice.

Probe (falsifiable, this week, $0, local ollama): reconstruction test proper. For 20 candidate
rows, give gemma:2b the model surface plus a row stub (origin, kind, first 8 content words) and
score regenerated rows at 80 percent content-word recall. Prediction: regeneration rate tracks the
coverage screen. Falsifier: if rows above 0.75 coverage fail to regenerate above chance, unigram
anchoring is not reconstruction, a store_vs_reconstruct column would mint lossy pointers, and the
port stops until a stronger prior exists (the estate's own grounding law: a lying map is caught,
`mag/world_rib.py:5-6`).

## Find 3: action-conditioned bisimulation, the re-derivable-territory guard

Organ: world rib (schema v2). Secondary: water graph as falsification territory.

Quote (ask-carried, sweep:55): "Two states merge only when their shared actions lead to agreeing
outcomes and successor blocks under an affordance label".

Mechanism: state identity is action-outcome equivalence; observation similarity is excluded from
the rule by construction; nothing is trained, the agent fills an empirical predictive state graph
as it acts (sweep:42). This is the lowering rule the world-rib contract lacks, verbatim.

Estate map:
- Laws lens q4 names the exact gap: "a RIB schema that lowers to 2D field, 3D, world, code, plus
  the re-derivable-territory guard" (`lens/laws.md:51`; the contract stays unbuilt per
  `lens/questions.md:68-69`). Today mag/world_rib.py compiles a rib to a 2D field to a 3D mesh
  with byte-stable determinism (`mag/world_rib.py:8-16`), and its grounding check rederive()
  verifies only that the same rib recompiles identically (`mag/world_rib.py:142-149`); there is no
  territory-identity rule at all, so nothing in the schema says which territory states are the same
  state, and therefore nothing says what may be re-derived rather than stored. Port: world_rib.v2
  gains two fields and one predicate, and they are this card's finds 2 and 3 braided: (a)
  territory identity: two territory states are equivalent iff every shared action yields agreeing
  outcomes and equivalent successors (bisimulation); (b) allocation: a state need not be stored if
  it is re-derivable from an equivalent stored ancestor (MemoWM's residual rule instantiated on
  the equivalence classes). The water graph is the natural falsification territory: integer
  volumes, conservation by construction, zero RNG (`mag/water_graph.py:10-34`; water computer
  organ at `mag/organ_map.py:48-50`).
- OVERLAP STATED: bisimulation was banked at abstract-page depth by the 10-03 area sweep ("banked,
  at abstract-page depth, eight items... Action-Conditioned Bisimulation 2609.38778",
  `frontier_olm_2026-10-03/sweep/agent-memory-and-continuity-arxiv.md:114`) and used there as a
  merge warning for the 300 law rows (similarity clustering cannot separate nodes with no
  distinguishing surface, `frontier_olm_2026-10-03/sweep/agent-memory-and-continuity-x.md:40`).
  No steal card carries it (rg over all steal dirs: zero). This card adds the organ it was always
  for: the world-rib schema guard, a different surface than the 10-03 knowledge-graph dedup
  context.

Deterministic leg, RUN this session on the estate's own action-outcome log (counts
moment-stamped per the census-denominator law; the stream is live and grew during this run):
memory/trajectory/steps.jsonl, schema trajectory_step.v1. T1 (round 1): 77,014 lines,
75,165,519 bytes, 105 parse failures. T2 (review): 77,308 lines, 75,444,307 bytes, 106. T3
(round 2 re-run, 2026-10-10T14:33:23): 77,390 lines, 75,529,138 bytes, 106. Over the last 20,000
rows, grouped by face plus first command token: 82 groups with 5 or more samples at every
moment (group count 205 at T1, 203 at T3; the sliding window moves as the stream grows). At both
moments: 19 strict-all-success groups (every exit present and equal to 0; the loose reading, all
non-missing exits equal to 0, gives 27, verified at T3), 2 all-failure, 53 groups showing both a
success and a nonzero exit (some of those 53 also carry rows with missing exit fields), 36 of the
82 containing at least one missing exit. Concrete span at T1: bash|ls exits 0 at 0.914 (n=1230)
while bash|dir exits 0 at only 0.255 (n=440). Every load-bearing ratio held across T1 and T3. Reading, stated both ways: a majority of well-sampled actions have state-dependent
outcomes, so an identity rule keyed on action appearance (or any observation shortcut) would merge
states that diverge, exactly the mis-merge the guard exists to refuse; and roughly a quarter of
the well-sampled actions are outcome-deterministic, which is the reconstructible territory find 2
pointerizes. Caveat carried: first-token grouping is a coarse affordance label; a finer grammar
(full command plus argument kinds) shifts groups toward the pure classes, so 53-of-82 is an upper
bound on action-token mis-merge risk, not a property of the true label set.

Probe (falsifiable, this week, $0, deterministic): compute the guard on the water graph. Enumerate
reachable volume-states from a start config under the action set (open a named valve, boil a named
node), then compute action-conditioned equivalence classes by iterative refinement (merge iff all
shared actions agree on delivery outcomes and successors stay equivalent). Two falsifiers:
(a) zero nontrivial classes means the guard compresses nothing on this territory and find 2's
allocation rule loses its merge partner; (b) count state pairs with identical volume histograms but
divergent delivery outcomes: if that count is zero, the guard adds nothing over a cheap checksum
on this graph and the schema should ship the checksum instead. NOT RUN (proposed; the graph is on
disk, deterministic, and the computation is stdlib-only).

## Find 4: MemFit, the ingest-cost condition under which amortization holds

Organ: context pack. Secondary: the trajectory store (the verbatim tier).

Quote (ask-carried, sweep:57): "stores each turn verbatim in an append-only store with
near-instantaneous, LLM-free insertion".

Mechanism: verbatim append-only long-term store, near-free insert, multi-path retrieval at LoCoMo
SOTA. The sweep prices why the estate should care: the route-map 25x boot cut amortizes only if
the write side is near-free, or "the amortization ledger goes negative at ingest" (sweep:34, RQ3;
the 03902 economics put the re-read crossover at 2-14 uses of the same material).

Estate map, with the port narrowed by measurement:
- The route-map mechanism is banked as of this morning (night cools, commit b928a2240): startup
  memory 45,128 down to 1,781 o200k_base tokens, both 12-question sets held, routes registered by
  hand, "costs more on tiny docs" (`watch/inbox/night_cools_20261010/grokbot_finds.md:29-38`, read
  this session). RQ3 owns its non-generalization conditions (sweep:34).
- Measured this session, three legs: (1) the pack builder is already LLM-free and network-free:
  `rg "requests|ollama|http|urllib|subprocess"` over mag/context_pack.py finds only status-display
  strings (`mag/context_pack.py:1592,2038`), and a live janitor-mode build takes 5.27 seconds for
  a 27,472-char str(pack) render (command in Checks). (2) The estate already owns a verbatim turn
  log: memory/trajectory/steps.jsonl, 77k rows, 75.2MB, schema trajectory_step.v1 with a hook-door
  write path (`mag/trajectory_step.py:28`), referenced by 23 files across mag/ and tools/ (`rg -l
  steps.jsonl`); immutability of old rows was not verified, only the append-style write door and
  the readers. (3) The gap is the read side: mag/context_pack.py contains zero references to
  steps.jsonl or trajectory (rg this session), so no pack mode mounts the verbatim tier (modes are
  janitor/route/build/audit/plan/full, `mag/context_pack.py:16`; the offload stubs at
  `mag/context_pack.py:35-47` are a write-time shed with sha-verified restore, not a retrieval
  path; trajectory-to-RIB organ at `mag/organ_map.py:138-140`).
- Port move: a pack mode (or a route in boot_routes.md, once minted) that mounts the trajectory
  store behind multi-path retrieval (session_id, face, command token, exit class), keeping ingest
  exactly as is. Nothing about insertion needs porting; that is the finding.
- OVERLAP STATED, the heaviest of the four: MemFit was deep-read at full-text depth by the 10-02
  memory-continuity arxiv sweep ("Full-text reads... MemFit 2610.00872",
  `frontier_olm_2026-10-02/sweep/agent-memory-continuity-arxiv.md:31`; its digest row: "beats the
  banked MemCodex LoCoMo number; append-only plus BM25 hybrid", same file :58; the PDF render is
  OWED at `frontier_olm_2026-10-04/DIGEST.md:113`). The wider surface, surfaced by the review and
  re-counted this session with the untruncated sweep: the id appears in 12 prior-day files from
  10-02 through 10-09 (both the 10-02 and 10-04 DIGEST rows, the 10-02 quantization-compression
  sweep, and the daily memory-continuity arxiv sweeps 10-03 through 10-09), so the fold should
  read MemFit as continuously held, not twice-mentioned. No steal card carries it. This card
  adds not the mechanism (estate-known since 10-02) but the amortization reading and the measured
  estate fit: write side already $0, verbatim tier already on disk, so the port reduces to the
  retrieval mount plus crossover accounting.

Probe (falsifiable, this week, $0): amortization ledger on a COPY, never the live organ. Copy
steps.jsonl to a temp path, append 100 synthetic trajectory_step.v1 rows through the hook door's
schema (`mag/trajectory_step.py:28`), then time 20 target lookups (known session_ids and command
tokens) by linear scan against the pack rebuild baseline (5.27 seconds, measured above).
Falsifier: if median linear-scan retrieval over 75MB exceeds the pack rebuild, the route-map cut's
amortization ledger goes negative on retrieval unless a corpus-FTS-style index
(catalog/catalog_fts.sqlite precedent) is mounted over the tier first; if lookups run far under
rebuild cost, the port is glue and should ship.

## Overlap statement (anti-rebank, per the sweep-wide lens law)

- Commands, restated honestly per the review: round 1's per-id sweep was
  `rg -l "<id>" watch/inbox | head -5` per id, so each list was TRUNCATED at 5 files; round 1
  then reported the shown hits as if complete and dropped the deepest SAGE holding (the 09-30
  file) even though the earlier broad pass had listed it. Round 2 re-ran the sweep untruncated
  (`rg -l "<id>" watch/inbox`, full lists this session). Prior-day file counts by id: 2610.10778
  one (the day-9 census, which left it unread); 2609.36043 six (09-30, 10-05, and four 10-06
  files); 2609.38778 two (both 10-03); 2610.00872 twelve (10-02 through 10-09, both DIGEST
  rows). No steal card in any frontier_olm day mentions any of the four ids (rg over
  `frontier_olm_*/steal/*.md`, rounds 1 and 2: only this card itself). Catalog: 3 rows for
  2610.10778, all this sweep's own intake artifacts (zone intake, today's mtime); zero rows for
  the other three ids (`rg -c` per id over catalog/catalog.jsonl).
- The ask's own overlap fields were accurate for their stated scope (catalog at sweep time, day-9
  register, memory/ trajectory-only); the cross-area sweep hits above are additive, not
  contradictory: the sweep's greps covered the catalog and register, not other areas' sweep files.
- The memory-continuity wire now has three cards that must land as one migration: day-9 (read
  half plus activation gate), the sibling Skill-V card (deterministic write-gate structure, whose
  :39-44 merge paragraph is the coordination point for schema v3), and this card (statistical
  acceptance, allocation calculus, territory identity, ingest economics). Two uncoordinated v3
  proposals on one wire would be drift; this card defers to the sibling's merge paragraph.

## Checks run and not run this ask

Run (all through `.venv/Scripts/python.exe`, never bare python):
1. Candidates census (json count over memory/percolator/candidates.jsonl): 31 rows, 26
   promoted=False, 0 promoted=True; last-row fields claim/falsifier/kind/origin/source/ts.
2. Trajectory scan (streaming parse of memory/trajectory/steps.jsonl), run twice and
   moment-stamped: T1 77,014 lines / 75,165,519 bytes / 105 parse failures / 205 groups; T3
   (2026-10-10T14:33:23) 77,390 / 75,529,138 / 106 / 203 groups. Both moments: last 20,000 rows
   sampled, 82 groups at n>=5, 19 strict-all-success (loose reading 27, verified at T3), 2
   all-failure, 53 with both outcomes, 36 with at least one missing exit; T1 exit-0 fractions
   bash|cd 0.883 (n=9421), bash|ls 0.914 (n=1230), bash|dir 0.255 (n=440).
3. Coverage screen, rule fully specified in find 2 (tokens re.findall(r'[a-z]{4,}') lowercased,
   the 33-word stoplist spelled out there, surface = 8 files, vocab 2,391). Run twice with
   identical output: 30 rows with content words, mean 0.665 (0.491-0.846); zknot/LATEST.md 1,677
   words, 0.723; the T3 rerun (2026-10-10T14:33:20) reproduces round 1 exactly. Reviewer's
   independent analog, different stoplist: mean 0.650, vocab 2,897, same shape.
4. Pack build timing (build_context_pack, mode janitor): 5.27 seconds, len(str(pack)) 27,472.
   LLM-free check: rg over mag/context_pack.py, only display strings at :1592 and :2038; zero
   references to steps.jsonl or trajectory anywhere in the module.
5. Revert census: `git log --oneline --grep=revert -i` piped to wc -l: 0.
6. Anti-rebank sweeps: round 1's per-id rg was head-truncated at 5 files per id (the defect the
   review caught); round 2 re-ran it untruncated (rg -l per id over watch/inbox), plus rg over
   every `frontier_olm_*/steal/*.md` and rg -c per id over catalog/catalog.jsonl. Per-id
   prior-day file counts are in the overlap section.
7. Round-2 verification reads, all before amending: the 09-30 evals SAGE row and the 10-05 evals
   SAGE row, verified verbatim (rg -n pins at :41 and :42); ls memory/percolator/ (no
   cascade_queue.jsonl and no cascades.jsonl; candidates, explore*, heal.log, invariants plus
   baks only); sed mag/percolator.py:264-272 (region exists, reads seal/invariant generations;
   the bare-counter reading is the 09-30 row's); sed mag/percolator.py:733-742 (CASCADE_QUEUE
   constant at :737).
8. Reads: sweep file in full; sibling and day-9 steal cards; lens laws (:51 block), questions
   (:60-84), graph (:33,35); grokbot_finds.md:27-40; mag percolator (:1-60), state_quantizer
   (:1-60), world_rib (all 172 lines), context_pack (:1-60, :1097-1126), water_graph (:1-55),
   organ_map (registry rows), trajectory_step (:1-29); warm_state.json in full;
   txt_2610.10778.txt (:116, :185-186).
Not run: pytest (no code changed this ask); the four probes' remaining legs, each marked NOT RUN
in its find; immutability audit of old steps.jsonl rows; the SAGE full text fetch (still not on
disk; no longer blocking the port, see OWED).

## OWED

- Full texts on disk: only txt_2610.10778.txt exists in sweep _tmp. Narrowed per review, because
  the estate holds more than round 1 credited: for 2609.36043 the test family and commit rule
  are ALREADY banked estate-side at digest depth (the 10-05 row: one-sided exact conditional
  binomial reducing to one-sided exact McNemar at lambda=1; commit only if discounted net gain
  > 0 AND p < alpha AND regression fraction <= tau; abstain otherwise). What remains genuinely
  OWED for SAGE is only the tuned constant VALUES (alpha, lambda, tau; the paper's own non-claim
  is "thresholds manually tuned", per the 10-05 row) and the sample-size guidance at small
  paired-n; the full-text fetch is nice-to-have, not blocking. Still OWED before their ports
  land: 2609.38778 (the affordance-label grammar the guard keys on) and 2610.00872 (the
  multi-path index structure; the 10-02 PDF render is OWED there too, DIGEST.md:113).
- The reconstruction probe's scoring rubric (what counts as 80 percent recall on a claim+falsifier
  row) needs one operator decision; proposed default is content-word recall against the row's own
  words, strictly checkable.
- De-inflating the coverage screen: a rerun with the six lens files excluded from the model
  surface (30 seconds, same script) would bound the shared-provenance inflation; not run this
  sitting.
