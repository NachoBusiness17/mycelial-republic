# STEAL CARD: agent-memory-continuity (frontier_olm 2026-10-10, round 2)

Seat: steal gopher, round 2 amended per review (round 1 verdict: demand fixes then approve; both
blocking fixes were missing overlap statements, now in-body under OVERLAP, STATED). Two confirmed
finds, both verified this sitting against the sweep's own full-text extracts and against the
estate organs they feed. Every fix claim in the round-1 critique was re-verified by this seat
before amending (sources, line citations, counts, and file absences all reproduced).

## Find 1: Skill-V, verifiable self-evolving skill library

Source: https://arxiv.org/abs/2610.11781 (2026-10-08). Local full text:
`watch/inbox/frontier_olm_2026-10-10/sweep/_tmp/txt_2610.11781.txt`.

### The mechanism (not the link)

Three-part commit pipeline for agent memory, all deterministic at the gate:

1. Skills as versioned, falsifiable contracts linking semantic intent to observable behavioral
   criteria (txt:84). A revision is a contract edit, not a prose append.
2. Proposals are never committed directly. The gate verifies contract schema, unique criterion
   identifiers, allowed matcher types, criterion weights and severities, criterion-to-procedure
   traceability, source skill identity, and monotonically increasing versions, then runs shadow
   replay on the observed evidence pool and enforces non-regression on rubric metrics before the
   contract goes active (txt:903, txt:787). Measured stake: without the evidence gate 9 of 46
   committed revisions regressed on at least one replay metric; enforcing it lifted task success
   75.0 to 95.3 percent (txt:475).
3. Read-side applicability filter: semantic retrieval alone scored 71.9 percent because a judge
   labeled 29.6 percent of retrieved candidates confidently inapplicable; rejecting them plus
   keeping deterministic contract checks reached 95.3 percent (txt:516).

### Estate map (organ: percolator + the knowledge graph's supersession wire)

- OVERLAP, STATED (day-9 owns the read half; this card adds the write gate): the day-9 card for
  this same area already staked the port direction: "The estate already owns the write half...
  The port move is the read half plus the activation gate, not more edges"
  (`watch/inbox/frontier_olm_2026-10-09/steal/agent-memory-continuity.md` lines 15-19; DIGEST
  rows 4 and 1, `watch/inbox/frontier_olm_2026-10-09/DIGEST.md:44,54`, carrying 2610.10265 +
  2610.08586 + 2610.03902: activation field, hysteresis-gated transitions, per-kind percolator
  confidence bars, select-active-over-superseded in pack builders). Skill-V does not duplicate
  that; it supplies what day-9's read-path contract assumed exists: the deterministic gate that
  makes a row active in the first place. The two schema-v3 field sets compose without collision:
  day-9's activation field + hysteresis is the read side, Skill-V's criterion ids, weights,
  traceability, and monotonically increasing versions are the write side, and one schema carries
  both. Two uncoordinated v3 proposals on one 6-row wire would be drift; this paragraph is the
  merge.
- The supersession wire today mints prose-only rows: each SUPERSEDED.md row becomes a
  superseded/superseder node pair with believed/banked/superseding/evidence text and one
  superseded_by edge, no criteria, no versions, no validation
  (`mag/knowledge_graph.py:264-289`). Verified 6 numeric rows in
  `memory/fold_history/SUPERSEDED.md` and exactly 6 "superseded" + 6 "superseder" nodes in
  `memory/knowledge_graph.json` (schema knowledge_graph.v2). This is lens question 1 and 4's
  "6 placeholder supersession rows" (`watch/inbox/frontier_olm_2026-10-10/lens/questions.md:62-80`).
- Port move A (graph, schema v3): extend the wire's row schema with Skill-V's contract fields
  (criterion ids, weights/severities, monotonically increasing version, source identity) and make
  `_superseded_wire` refuse to mint a pair whose row fails structural validation.
- Port move B (percolator, the commit gate): the candidates lane already ingests frontier digests
  into `memory/percolator/candidates.jsonl` (31 rows counted this sitting; 26 carry the field and
  all 26 are promoted=False; the 5 earliest rows predate the field) with promotion only through
  the reviewed percolate() path (`mag/percolator.py:23-25`). Add Skill-V's two gate legs there:
  shadow replay over the candidate's cited evidence (the receipt paths every candidate already
  names) and a non-regression check against the invariants it would touch (the depends_on/cascade
  machinery already exists, `mag/percolator.py:38-50`). The 9-of-46 number is the falsifier shape:
  an unvalidated promote path should be expected to leak regressions at that order.
- Port move C (read side): the novelty check that today runs blind against 122 orphan steals
  (`lens/questions.md:73-80`) gains the applicability filter: before a steal node is offered as
  prior art, a cheap deterministic applicability check (does the criterion's module path exist,
  does the cited test name resolve) rejects confidently-inapplicable candidates. Skill-V's 29.6
  percent rejection rate is the prior for how much semantic retrieval overserves.

### Probe (falsifiable, this week, $0, deterministic)

Write a 30-line validator over `memory/fold_history/SUPERSEDED.md` asserting the Skill-V schema
(version integer present and increasing per source, criterion ids unique, weights in range,
evidence path exists). Prediction: 6 of 6 rows fail today (they carry only 5 prose cells,
verified from the parser at `mag/knowledge_graph.py:244-261`). Falsifier after port: a mutated
row (bumped criterion weight, dangling criterion id, repeated version) must be rejected
deterministically; if the gate passes a mutated row the port failed.

## Find 2: Progressive disclosure of agent skills (frontmatter index, body on trigger)

Source: https://arxiv.org/abs/2609.35692 (2026-09-28). Local full text:
`watch/inbox/frontier_olm_2026-10-10/sweep/_tmp/txt_2609.35692.txt`.

### The mechanism

Keep a frontmatter index of every skill in context; load the body only when triggered.
Measured at three model scales: token savings grow with library size N, reaching 81.7 percent
at N=50 (Qwen3-14B) and 67.9 percent at N=20 (Qwen2.5-7B) (txt:131, table txt:155-262); eager
loading crashes 100 percent of rollouts at N=100 while progressive disclosure crashes zero
(table, PD crash column 0.00 across all rows). Costs, stated honestly: +15 percent latency at
N=50 (txt:136) and a real regression on a weak router (Qwen3-8B, N=20: eager success 0.68 vs
progressive 0.38). The paper therefore bounds the port: the router that picks body-loads must be
stronger than the reader it serves.

### Estate map (organ: context pack + rib_boot; secondary: warm-boot chain)

- OVERLAP, STATED (the mechanism is banked as of this morning; the paper adjudicates it): night
  cools commit b928a2240 (2026-10-10 03:48) grokbot find "route-map memory 25x boot cut" already
  banked this exact shape: "The whole startup memory becomes a resident route map, and the note
  opens only when its trigger hits" with the port order "write `memory/boot_routes.md` as one line
  per load-order row in `Agents.md`: `when <trigger>, read <path>`"
  (`watch/inbox/night_cools_20261010/grokbot_finds.md:33,37-38`; measured there: 45,128 down to
  1,781 o200k_base tokens, both 12-question sets held). `memory/boot_routes.md` does not exist
  yet (verified this sitting), so the port is unexecuted, not wasted. This sweep's digest already
  names the lineage: "Q3: the production replication of the route-map 25x boot cut AND its failure
  conditions" (`sweep/agent-memory-continuity-arxiv.md:90`). What the route-map find lacked and
  this paper adds: the measured eager cliff (100 percent crash at N=100), the +15 percent latency
  cost, the router-strength guard, and the failure conditions list (small libraries: N=5 savings
  only 0.5-41 percent; weak routing models; latency-sensitive loops; single-skill tasks only,
  multi-skill untested, `sweep/agent-memory-continuity-arxiv.md:90-93`).
- The two port shapes merge, not compete: boot_routes.md is the hand-registered one-line map over
  the AGENTS.md load order; the context-pack stub regime is the same law applied to the corpora a
  pack actually mounts. The estate already has two partial organs for this. (1) `mag/rib_boot.py`:
  VAULT_RIBS mounts 7 named law ribs as 1200-char law-heads plus amendments
  (`mag/rib_boot.py:90-99` VAULT_RIBS/LAW_HEAD_CHARS, `mount_vault` at `:142-169`), which is
  progressive disclosure for the rib vault specifically. (2) `mag/context_pack.py` runs the
  bounded-view-plus-zoom story: overflow sheds whole sections to `watch/inbox/PACK_OFFLOAD.jsonl`
  as reversible stubs (`mag/context_pack.py:17,27-51`) and `restore_shed_section` re-renders a
  shed section from its stub pointer sha-verified, turning organ drift into a refused restore
  rather than silent corruption (`mag/context_pack.py:225-240`, `list_shed_stubs` at `:326`).
  Progressive disclosure is the structural version of that reactive shedding: stop loading bodies
  at build time, ship frontmatter stubs, hydrate on trigger.
- Estate-side before-metric, measured this sitting with
  `.venv/Scripts/python.exe` over the two corpora a seat pack would index:
  `memory/rib/*.md`: 57 files, 237,945 bytes total, 19,622 bytes for first-6-lines only, a 91.8
  percent cut (round-1 review independently reproduced 91.9, line-ending noise).
  `.agents/skills/*/SKILL.md`: 31 files, 100,769 bytes total, 12,399 bytes front-6,
  an 87.7 percent cut. Both N values sit inside the paper's paying regime (N >= 20), and the two
  corpora sum to 88 docs, just under the N=100 eager cliff.
- Port move: context pack modes (janitor/route/build/audit/plan/full, `mag/context_pack.py:16`)
  gain a stub regime where rib/skill/state rows carry id, purpose line, and trigger keywords, and
  boot_routes.md becomes the trigger map's first citizen; the load-order docs (AGENTS.md rows
  0a-8) and the warm-boot chain (`memory/warm_state.json`, today generated 2026-10-10T11:15:13Z
  chain index 3414; `tools/zknot.py`) reference stubs, not bodies.
- Guard from the paper: route triggers on deterministic keyword match or the funded judgment tier,
  never a janitor-class router; the Qwen3-8B 0.68 to 0.38 regression is the named failure mode,
  and the route-map find's own "costs more on tiny docs" caveat
  (`night_cools_20261010/grokbot_finds.md:31`) is the same boundary at estate scale.

### Probe (falsifiable, this week, $0)

The deterministic half already ran (numbers above). The remaining falsifiable leg: build the same
pack twice through `mag/context_pack.py`, one eager (current) and one stub-first, and compare
total_chars at N=20 and N=57 ribs. Prediction from the paper plus the measured corpora: the char
cut lands at or above 67.9 percent at N=20 and grows with N; if the stub pack saves under half
that, the estate's rib frontmatter is too thin to index and the port needs frontmatter densification
first, which is a different (and cheaper) fix.

## Overlap statement (anti-rebank, per lens/questions.md sweep-wide laws)

Id-level: `git grep -E "2610.11781|2609.35692|Skill-V"` over memory/, corpus/,
CORPUS_CATALOG.md, watch/inbox/ excluding today's sweep dir: zero hits (run this sitting,
exit 1). The catalog's rows for these ids are this sweep's own intake artifacts
(catalog/catalog.jsonl lines 1013996, 1014006, 1014019, 1013991, 1014002, 1014015, all mtime
2026-10-10T14:55-14:57Z) plus one 11-day-old title-only stub for 2609.35692 (catalog line
1001696, state/arxiv/2026-09-29/2609.35692v1.txt, 818 bytes) which find 2's overlap field
already disclosed. No prior steal card, register row, or digest mentions either paper by id.

Mechanism-level (the part round 1 severed, restored above): find 1's organ was staked by the
day-9 card (read half, `frontier_olm_2026-10-09/steal/agent-memory-continuity.md` lines 15-19);
find 2's mechanism was banked this morning as the route-map 25x boot cut (b928a2240,
`night_cools_20261010/grokbot_finds.md:33,37-38`). Both overlaps are now stated in-body under
OVERLAP, STATED with the merge worked out; neither is a silent re-confirmation.

## Limitations the papers state (dropped in round 1, restored)

- Skill-V, its own limitations section, as carried by this sweep's digest: no skill deletion
  (only boundary tightening), and historical dependency: replay evidence goes stale when
  environment rules change, with the cure named as time-weighted buffers
  (`sweep/agent-memory-continuity-arxiv.md:67-69`). The staleness limit is load-bearing for port
  move B: the estate's cited receipts age exactly the way Skill-V's trajectory pool does, and a
  replay gate over stale evidence is the paper's own named failure. The port must time-weight or
  expiry-stamp the evidence pool, not replay over it blindly.
- Progressive disclosure, its own failure conditions: neither regime consistently outperforms the
  other; small libraries save little (N=5: 0.5-41 percent), weak routers regress, latency rises
  15 percent, and the eval loads exactly one skill per task, multi-skill untested
  (`sweep/agent-memory-continuity-arxiv.md:67-69,90-93`).

## OWED

Nothing owed on the quoted numbers; all verified against the local full texts cited above. OWED
if the port proceeds: a shadow-replay evidence-pool format for percolator candidates (Skill-V
replays on its own trajectory pool; the estate equivalent is the receipt paths candidates cite,
which have no replay harness yet), and the time-weighting rule that keeps that pool honest as
receipts age.
