# RIB SWARM SPEC v1 (rib_swarm.law_row.v1 / rib_swarm.genome.v1)

Status: PROTOTYPE (2026-10-01, lane GENOME-1). Owner of the behavior implemented by
`tools/rib_swarm.py` + `tests/test_rib_swarm.py`. NOT wired into any production carrier:
the prototype lands its own receipt under `watch/inbox/model_garden/` and nothing else
reads it yet. Wiring into carriers is a separate operator decision (see section 8).

Operator mission (2026-10-01): "i want the swarm communicating in ribs and doing our
genetic lensing and algos". Two behaviors live here:

1. RIB COMMUNICATION: swarm units exchange findings as LAW ROWS (the ractor50
   claim/evidence/steal/falsifier shape), not prose. The intercommunication medium is
   the SAME FORMAT as estate memory, so swarm output is rib-readable by default.
2. GENETIC LENSING: a selection-mutation-crossover loop over ASK CANDIDATES. A
   population of review contracts, fitness = machine-graded yield of the asks they
   produce (REAL clusters per dollar), select top, crossover contract clauses, mutate
   one clause, fire children cheap, measure, repeat.

## 1. LAW ROW format (the rib medium)

The grammar is the ractor50 idiom already banked in `memory/runs/salon1/` unit outputs
and estate rib rows. One law row is exactly six lines:

```
L<n>: <short title, under 12 words>
CLAIM: <the law; one to three sentences>
STEAL: <the one-sitting action another seat can take>
FALSIFIER: <the observation that would kill the claim>
SOURCE: <evidence: path plus verbatim short quote in "double quotes">
LEVERAGE: high | medium | low
```

Parser law (`parse_law_rows`):
- A row opens with `^L(\d+):\s*(.+)$` and closes when the next `L<n>:` opens or text
  ends. Field lines match `^(CLAIM|STEAL|FALSIFIER|SOURCE|LEVERAGE):\s*(.*)$`.
- Parsing is LENIENT: unknown lines inside a row are kept in `raw` and counted as
  shape violations, never fatal. Grading is STRICT (below).
- `law_id` is the `L<n>` string, namespaced by ask in the ledger, so duplicate ids in
  one reply both survive.

Grade checks per row (`checks` dict, all booleans):
- `claim`: CLAIM present and non-empty.
- `falsifier`: FALSIFIER present (a law without a falsifier is an opinion).
- `leverage`: LEVERAGE in {high, medium, low}.
- `source`: SOURCE names a path-like token (contains "/" or "." before any quote).
- `no_em_dash`: no U+2014 in the row text (the estate standing law).
- `title_short`: title is 12 words or fewer.

A row passes grade when claim, falsifier, leverage, and no_em_dash hold. source and
title_short are graded facts only (reported, not gating), matching the parse/grade
split law of `tools/code_swarm.py` (parse never guesses, grade never crashes).

Round-trip law: `render_law_rows(parse_law_rows(text))` must reparse to identical
field values, so a rib file can quote a ledger row verbatim and any seat can re-derive
the parsed row from the rendered bytes.

## 2. Rib ledger (per-run)

Path: `watch/inbox/model_garden/<run>/rib_ledger.jsonl`, append-only, one JSON object
per parsed law row, atomic tmp+replace on write:

```
{"schema": "rib_swarm.law_row.v1", "ts": "...", "run": "...", "round": 1,
 "unit": "U1", "family": "deepseek", "ask_id": "...", "mock": false,
 "law_id": "L2", "title": "...", "claim": "...", "steal": "...",
 "falsifier": "...", "source": "...", "leverage": "high",
 "checks": {...}, "reply_sha256": "<sha256 of the raw reply, 16 hex>"}
```

Ledger laws:
- Every parsed row from every round is banked, including failing-check rows (a
  failing row is evidence about the family, per the battery mask law).
- `mock: true` rows are synthetic (offline prototype mode); they never enter
  `memory/runs/model_garden/usage.jsonl` and must never be cited as family behavior.
- The ledger is the ONLY intercommunication surface between units (section 3).

## 3. Rib communication round

One round = stage, fire, parse, bank, converge. Units are (slice, family) pairs,
mirroring the salon1 shape (`memory/runs/salon1/`: round1 blind, round2 mesh).

Round 1 (blind mint): each unit gets one self-contained ask whose output contract
demands EXACTLY 3 to 5 law rows in the section 1 grammar, over its own target slice.
Fires ride the gated rail `tools/model_garden.run_ask` (inference_budget recipes,
refusal + EMPTY_REASONING terminals, usage ledger), one attempt per ask, budget cap
checked against the run's metered rows before every dispatch.

Round 2 (law-rows-only intercommunication): each unit's ask embeds, verbatim via
`render_law_rows`, (a) its OWN round-1 law rows for continuity and (b) the round-1
law rows of its siblings. It NEVER embeds sibling raw replies. The contract's
material block is built exclusively from ledger rows, so raw prose physically cannot
leak (the builder takes parsed rows, not text). The round-2 output contract demands
law rows again: refinements, contradictions, and connections, each citing sibling
law ids like (U2 L3).

Convergence pass (`converge_laws`): cross-INSTANCE law agreement, ranked.
- An INSTANCE is a (unit, family) pair: the same unit's ask is fired by every
  family with byte-identical contract (G2 law), so two families minting the
  same law on one slice is independent corroboration, exactly code_swarm's
  REAL semantics; different units on different slices corroborate only when
  their laws genuinely overlap.
- Signature of a row = lowercase `[a-z_]+` tokens of title+claim, tokens over 3
  chars, minus the code_swarm stopword set. Reuse, not re-invention.
- Two rows from DIFFERENT instances agree when signature intersection is 2 or
  more tokens AND the intersection is at least half the smaller signature
  (containment guard: without it, pairwise union-find chains transitively
  through shared harness vocabulary and merges unrelated laws into one
  mega-cluster; observed live 2026-10-01 when all 90 rows of riblive1 collapsed
  into a single cluster; calibrated on the same ledger: true cross-family
  agreement measures 13 to 19 shared tokens at ratio 0.52 to 0.59, while
  different-file vocabulary collisions measure 4 shared at ratio 0.12 to 0.19).
  Agreement is union-found into clusters.
- Basis: round 1 rows only (the blind mint, pre-intercommunication). Round-2
  rows cite sibling ids by contract, so their vocabulary overlap is by
  construction, not agreement; they stay in the ledger, out of the convergence
  denominator.
- Cluster status: CONVERGED (2+ distinct instances) else SINGLE.
- Rank order: more distinct families first, then more distinct units, then
  better leverage (high > medium > low, cluster takes its best), then more
  member rows, then law_id for determinism.
- Convergence is corroboration, not adjudication (the G2/GPS law): a CONVERGED
  law still needs a byte walk before it steers anything.

## 4. Genetic lensing

### 4.1 Genome

A genome IS an ask contract candidate, expressed as evolvable clauses
(`rib_swarm.genome.v1`):

```
{"id": "g0-3", "gen": 0, "origin": "seed|crossover|mutant|crossover+mutate",
 "parents": ["g0-0", "g0-2"], "lens": "<LENS_POOL entry>",
 "target": "<repo-relative file>", "max_defects": 3,
 "anchor_family": "deepseek", "probe_family": "glm-flash"}
```

Clause semantics:
- `lens`: the review angle instruction injected into the contract.
- `target`: the file under review (inline SOURCE block, sha-stamped).
- `max_defects`: how many DEFECT rows the contract demands (2 to 5).
- `anchor_family` + `probe_family`: the two cheap families that fire the genome's
  ask. Fitness NEEDS two families (cross-family convergence is the signal), so every
  genome fires twice per measurement. anchor is fixed per run; probe is evolvable.

LENS_POOL (seeded from the battery + swarm contracts): cost-leak, security-boundary,
correctness-race, dead-code, wiring-organs, error-swallow, shape-law.

### 4.2 Contract rendering

The rendered contract must demand the `tools/code_swarm.py` reply grammar
(`DEFECT n | EVIDENCE | FIX`, DEAD-CODE, ONE-SITTING FIX) so replies grade through
`code_swarm.parse_reply` and converge through `code_swarm.converge` unchanged: the
genetic loop measures with the swarm's own instrument, not a new grader. The lens
clause is injected as a prioritization paragraph; `max_defects` scales the demanded
DEFECT rows. AUTHORED contract text (template + lens clauses) carries no em-dash
bytes, asserted at render; the pasted SOURCE block is frozen evidence bytes
(battery law 2) and is graded on the reply, never rewritten to satisfy the ask-side
law.

### 4.3 Fitness

Per genome, fire anchor+probe on its target, grade both replies, converge the pair:

```
yield = n_REAL + 0.25 * n_COLOCATION
fitness = (yield + 0.05 * parse_ok_rate) / max(cost_usd, 0.01)
```

- REAL clusters per dollar is the dominant term (the operator's words).
- The 0.05 * parse_ok_rate term only orders zero-yield genomes (a contract whose
  replies do not parse has measured nothing and must not tie a contract whose
  replies parse but find nothing).
- cost floor $0.01: sub-cent cost noise must not dominate yield.
- cost_usd = the run-prefixed metered ledger rows for that genome's two asks.

### 4.4 Operators (all pure, seeded-rng deterministic)

- `select(pop, k)`: top k by (-fitness, id). Elites survive to the next generation.
- `crossover(a, b, rng)`: per clause (lens, target, max_defects, probe_family),
  uniformly take parent a's or b's value. Child id `g<gen>-<n>`, gen = max+1,
  parents recorded. Invariant: every child clause value is one of its parents'.
- `mutate(g, rng, rng_targets)`: perturb EXACTLY ONE clause: lens resampled from
  LENS_POOL (different value), max_defects +-1 clamped to 2..5, probe_family
  resampled from the run's family pool, target swapped only when a target pool of
  more than one file is given. Invariant: exactly one clause differs from parent.
- Population defaults: size 8, generations 3, stagnation stop after 1 generation
  without best-fitness improvement. Children per generation fill the population
  back to size after elites.

### 4.5 Loop and exit semantics

```
seed population (from battery/swarm-derived clauses over the target pool)
for gen in 0..max_gens-1:
    measure every genome (fire anchor+probe, grade, converge, fitness)
    bank generation row (genomes.json + generations.jsonl under <run>/genetic/)
    exit STAGNANT  if gen > 0 and best_fitness <= run best so far
    exit BUDGET    if run spend >= cap (checked before every dispatch too)
    breed next generation (elites + crossover children, half mutated)
exit GENERATIONS at max_gens
```

Exit reason is banked in the run receipt. The falsifier of the whole loop: a week of
generations where best fitness never beats the seed population's best = the lens
pool or the fitness instrument is blind, fix the instrument before spending more.

### 4.6 Mock mode

`--mock` replaces the fire path with a deterministic offline replier (seeded rng,
lens-dependent reply quality drawn from a fixed landscape table) and synthetic
per-family costs. Mock rows land in the ledger and receipts with `mock: true` and
never touch the usage ledger. Mock exists to test the LOOP MACHINERY offline; mock
fitness numbers are never family verdicts. Two shaping laws: (a) in rib rounds the
mock replier shapes law rows with a fixed lens (cost-leak) so cross-unit law
convergence is demonstrable offline (the shaping lens is a staged-dict field only,
never contract bytes); (b) zero-yield lenses mint fully noise-flavored claims and
the shared DEAD-CODE/ONE-SITTING suffix rows carry only one shared token each, so
nothing converges below 2 shared tokens by construction.

## 5. CLI surface

```
python tools/rib_swarm.py --run <id> --rib-round [--mock] [--units N]
    [--targets f1 f2 ...] [--families deepseek glm-flash kimi]
    [--concurrency 4] [--cap 0.5]
python tools/rib_swarm.py --run <id> --genetic [--mock] [--pop 8] [--gens 3]
    [--targets f1 f2 ...] [--families deepseek glm-flash kimi]
    [--anchor deepseek] [--seed 7] [--concurrency 4] [--cap 0.5] [--stagnation 1]
```

Landing layout under `watch/inbox/model_garden/<run>/`: `asks/<ask_id>/ask.json`,
`rib_ledger.jsonl`, `rounds.json`, `genetic/genomes.json`,
`genetic/generations.jsonl`, `genetic/fires.jsonl`, `run_receipt.json`. Real replies
land at the garden carrier path `watch/inbox/model_garden/<ask_id>.md` per the
carrier contract; spend is metered by `tools/model_garden.py` in
`memory/runs/model_garden/usage.jsonl`.

## 6. Exit codes

0 = completed (either mode); 2 = usage error (no targets, unknown family, empty
pool). Fire failures are per-ask facts banked in the receipt, never a nonzero exit
by themselves (the burn law: terminals stay dead, the run keeps going).

## 7. Test obligations (tests/test_rib_swarm.py)

1. Law-row parser: happy path, blank-line tolerance, prose tolerance, missing
   fields, leverage validation, em-dash grading, round-trip identity.
2. Ledger: append + render round-trip; mock flag survives.
3. Round-2 contract builder: contains sibling CLAIM lines and cannot contain
   sibling raw prose (built from rows only).
4. converge_laws: cross-unit agreement cluster, ranking order, SINGLE status.
5. crossover: clauses only from parents, determinism under fixed seed.
6. mutate: exactly one clause differs, bounds hold.
7. fitness: REAL-per-dollar dominance, zero-yield tiebreak, cost floor.
8. Mock genetic cycle: seed landscape where some lenses outyield others; the loop
   must raise best fitness after one cycle (the prototype's core claim, offline).
9. Rendered contracts: no em-dash bytes anywhere.

## 8. Production wiring (explicitly NOT done here)

To promote past prototype the estate needs, in order: (a) a carrier decision that
rib_swarm receipts may be read by mag/ surfaces (today nothing parses them); (b) a
scheduler + drift gate shape like the census patrol (daily fire over sha-changed
files only); (c) convergence laws feeding `tools/animal_profiles.py` observations;
(d) the genetic loop's winning contracts promoted into the standing
`tools/code_swarm.py` CONTRACT by operator acceptance, never by the loop itself
(model text can propose; the operator authorizes). Budget law: the prototype's cap
is $0.50 per run, checked before every dispatch against metered rows.

## 9. Lineage

- ractor50 law-row grammar: `memory/runs/salon1/round*/` unit outputs.
- Round structure: `memory/runs/salon1/inputs/prompt_r1..r3.md` (blind, mesh,
  convene), simplified here to blind + law-rows-only mesh.
- Grading + convergence reuse: `tools/code_swarm.py` parse_reply/converge (SWARM-1).
- Fire rail: `tools/model_garden.py` run_ask (gated, budget recipes, terminals).
- Battery seeding: `watch/inbox/model_garden/BATTERY.md` design laws (identical
  bytes, surface freeze, inline paste, no em-dash, cost banking, contamination
  flags, blind naming) all apply to rib_swarm asks unchanged.
