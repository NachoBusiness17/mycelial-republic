# RIB SWARM 1 - law-row communication + genetic lensing prototype (2026-10-01)

**Schema:** rib_swarm.prototype.v1 - **ts:** 2026-10-01 - **lane:** GENOME-1 (ZCode subagent, operator
mission: "i want the swarm communicating in ribs and doing our genetic lensing and algos")
**Spec (owner of the behavior):** `docs/ref/RIB_SWARM_SPEC.md` (written BEFORE the code, per build
discipline). **Instrument:** `tools/rib_swarm.py` (399 lines) + `tests/test_rib_swarm.py` (20 tests).
**Prototype only:** nothing in mag/ or any carrier reads these outputs; promotion is an operator
decision (spec section 8).

## What landed

1. RIB COMMUNICATION. Swarm units exchange findings as LAW ROWS, the ractor50 claim/steal/falsifier/
   source/leverage shape already banked in memory/runs/salon1/. Round-1 asks mint law rows blind;
   round-2 asks embed ONLY the siblings' rendered law rows (never raw replies: the contract builder
   consumes parsed ledger rows, so prose physically cannot leak). All rows land in a per-run
   append-only ledger `watch/inbox/model_garden/<run>/rib_ledger.jsonl` (rib_swarm.law_row.v1), which
   round-trips: render_law_rows(parse_law_rows(text)) reparse to identical field values, so swarm
   output IS rib-readable by default. Convergence ranks cross-INSTANCE ((unit, family)) law agreement.
2. GENETIC LENSING. A population of 8 review-contract genomes (lens, target, max_defects, anchor +
   probe family), seeded from the battery/swarm contract angles, evolved by select (top-half elites) /
   crossover (per-clause parent mix) / mutate (exactly one clause perturbed). Fitness = machine-graded
   yield: (n_REAL + 0.25*n_COLOCATION + 0.05*parse_rate) / max(cost_usd, 0.01), measured by firing
   each genome's contract at anchor + probe through the gated model_garden rail and grading with the
   STANDING code_swarm instrument (parse_reply + converge, unchanged). Exit semantics: GENERATIONS /
   STAGNANT / BUDGET, banked in run_receipt.json.

## Runs (all real fires rode the gated rail; budget law held)

| run | mode | asks | landed | cost | result |
|---|---|---|---|---|---|
| ribmock1 | rib round, MOCK | 18 | 18 | $0 (synthetic) | 81 ledger rows, 1 converged cluster (loop machinery proof) |
| genmock1 | genetic, MOCK | 32 | 32 | $0 (synthetic) | mean 114.375 -> 167.5 in one cycle, best 205, exit STAGNANT |
| riblive1 | rib round, LIVE (deepseek+glm-flash x 3 targets x 2 rounds) | 12 | 12 | $0.0294 | 90 law rows banked, 90/90 pass grade; 5 CONVERGED law clusters (cross-family, independently minted) |
| genlive1 | genetic, LIVE (pop 8 x 2 gens x anchor+probe) | 24 | 24 | $0.0455 | gen0 best 102.5 / mean 32.5 -> gen1 best 205.0 / mean 72.5; exit GENERATIONS |

**Prototype total: 36 live asks, $0.0749 of the $0.50 cap (15 percent), zero fire failures.**
Raw replies at watch/inbox/model_garden/<ask_id>.md per the carrier contract; usage metered in
memory/runs/model_garden/usage.jsonl.

## Did one genetic cycle improve fitness? YES (both modes)

- LIVE: gen0's best genome (g0-2, correctness-race lens, 4 defect rows, glm probe) scored 102.5
  (1 REAL cluster, parse_rate 0.5: one family reply broke strict shape but its defect lines still
  parsed, the exact SWARM-1 tolerance). One cycle later the champion g2-4241 (crossover of the two
  top elites keeping correctness-race + glm probe, then a max_defects 4->5 mutation) scored 205.0:
  2 REAL clusters, parse_rate 1.0, at $0.0023 vs the parent's $0.0051. Best doubled, population
  mean more than doubled (32.5 -> 72.5).
- MOCK (offline, deterministic, seed 7): mean 114.375 -> 167.5, best held at 205, exit STAGNANT
  (plateau detected by the stagnation guard, working as spec'd).
- Falsifier of the loop (spec 4.5): a week of generations without beating the seed best means the
  lens pool or the fitness instrument is blind. One prototype cycle is evidence, not a law.

## The riblive1 convergence bug this lane paid for (and fixed mid-run)

First convergence pass collapsed ALL 90 law rows into ONE mega-cluster: pairwise union-find chained
through shared harness vocabulary (census/verdict/bytes/index words appear in every unit's claims).
Two fixes, calibrated on the live ledger before landing: (a) a containment guard (shared tokens must
cover half the smaller signature; measured live: true cross-family agreement 13-19 shared tokens at
ratio 0.52-0.59 vs vocabulary collisions 4 shared at 0.12-0.19); (b) convergence basis is round-1
rows only (round-2 rows cite sibling ids by contract, so their overlap is by construction). After
the fix: 60 r1 rows -> 45 clusters, 5 CONVERGED, each spanning deepseek+glm-flash on one slice
(e.g. "Meta bytes contract detects stale index past mtime lies" on corpus_fts_rebuild.py, both
families independently, leverage high). rounds.json was recomputed from the durable ledger, no
refire. Regression test added (test_converge_laws_containment_guard_blocks_weak_big_sig_sharing).

## Top converged laws (riblive1, cross-family corroborated, NOT byte-walked)

| # | unit/file | families | law (title) | leverage |
|---|---|---|---|---|
| 1 | U2 tools/corpus_fts_rebuild.py | deepseek+glm | Meta bytes contract detects stale index past mtime lies | high |
| 2 | U2 tools/corpus_fts_rebuild.py | deepseek+glm | Build replaces atomically so ro readers never see partial index | high |
| 3 | U1 tools/census_drift_patrol.py | deepseek+glm | Exit 2 is the fail-closed arm for every unverifiable byte | high |
| 4 | U1 tools/census_drift_patrol.py | deepseek+glm | The census claim parses only from the parenthesized clause | high |
| 5 | U2 tools/corpus_fts_rebuild.py | deepseek+glm | Rebuild reuses corpus.py freshness rule by hermetic load | medium |

Full text + falsifiers + sources: watch/inbox/model_garden/riblive1/rib_ledger.jsonl and rounds.json.
These are corroboration, not adjudication (G2/GPS law): byte-walk before any fix.

## Grading facts

- riblive1: 90/90 law rows pass the strict grade (claim+falsifier+leverage+no-em-dash). Round-2
  contracts contain sibling CLAIM lines only; no raw prose markers (verified on the live ask.json).
- genlive1: parse_rate varies (0.0-1.0 strict shape; defect lines still extracted in loose replies,
  SWARM-1 behavior). 8 REAL clusters total across the run; no em-dash anywhere in asks or replies.
- Cost split (usage.jsonl): deepseek $0.0433, glm-flash $0.0091, kimi $0.0 metered (Nous credits),
  36 asks, all banked with tokens/finish state per the driving-ladder receipt law.

## What production wiring needs (spec section 8, NOT done here)

1. A carrier decision that rib_swarm receipts may be read by mag/ surfaces (nothing parses them today).
2. A scheduler + sha-drift gate (fire only files changed since last swarm, census-patrol shape).
3. Converged laws feeding tools/animal_profiles.py as observations.
4. Winning genetic contracts promoted into the standing code_swarm CONTRACT by operator acceptance,
   never by the loop itself (model text proposes; the operator authorizes).
5. The convergence instrument needs more live calibration once rib rounds run on overlapping slices
   (this run's units had disjoint files; cross-unit agreement was correctly empty, cross-family
   within-unit carried the signal).

## Files

- docs/ref/RIB_SWARM_SPEC.md (new; spec owner, written first)
- tools/rib_swarm.py (new, 399 lines, under the 400 ratchet cap, zero new ratchet violations)
- tests/test_rib_swarm.py (new, 20 tests, all passing offline)
- watch/inbox/model_garden/ribmock1/, genmock1/, riblive1/, genlive1/ (ledgers, asks, receipts)
- watch/inbox/model_garden/genlive1_fire_log.txt
- No commits (prototype lane; promotion is a separate operator gate).

Lane GENOME-1 seat, 2026-10-01.
