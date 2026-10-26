# ATLAS DIG + DOWNSTREAM RE-EVALUATION PORT SPEC (atlas lane, 2026-10-01)

Lane: gala_20260925/localfirst-steal, division B, lane atlas.
Start file: `watch/inbox/LOCALFIRST_MEMORY_LANDSCAPE_20261001.md` (brief claims:
local belief store, SHA-256 hash chain, downstream belief re-evaluation on fact
change, Apache-2.0, on Graphiti).
Method: shallow clone `github.com/RichSchefren/atlas` HEAD `229df544944ffb1dadf4d155bcb41334e850da0c`
(committed 2026-08-10), 339 files, read first-hand; own unit tests executed in a
scratch venv; estate organs read directly. Verbatim excerpts with per-file
sha256: `watch/inbox/gala_20260925/localfirst-steal/lanes/evidence/atlas_excerpts.md`.

## 1. TRI-STATE VERDICTS on the brief's claims

| Claim | Verdict | Byte evidence |
|---|---|---|
| SHA-256 hash chain | **VERIFIED (code + run)** | `atlas_core/trust/ledger.py`: v1 hash = sha256 of `previous_hash\|event_type\|recorded_at\|object_id\|payload_json` (L135-142); v2 hashes the full canonical envelope incl. `chain_sequence` (L145-182); append links `previous_hash = last["event_id"]` under `BEGIN IMMEDIATE` (L294, L313-315); `verify_chain()` walks genesis-to-latest, checks sequence gaps + prev linkage + recomputes every event_id (L422-559). Own suite run this session: `tests/unit/test_ledger.py` **26/26 passed** (genesis, tamper-any-field, atomic append, typed_roots, is_promoted) on a Python 3.12 scratch venv. |
| Downstream belief re-evaluation on fact change | **VERIFIED, with one honest caveat** | `RippleEngine.propagate()` = 4 stages: AnalyzeImpact (BFS over INCOMING DEPENDS_ON edges, visited-set cycle guard, max_depth 10 / max_nodes 5000) -> Reassess (per-dependent confidence proposals) -> contradiction detection -> 3-bucket routing (`atlas_core/ripple/engine.py` L8-16). Trigger is real and deduped: `materialize_approved_candidates` fires `ripple_engine.propagate(...)` once per ledger-promoted candidate, guarded by `ripple_ledger_event_id` (`atlas_core/ingestion/materializer.py` L323-340). CAVEAT: the AUTO_APPLY route has **no executor** in the production tree (grep negative, section 2 item 1): routine proposals are computed + routed but only human-resolved decisions (Obsidian checkbox, fswatch, MCP `adjudication.resolve`) reach AGM `revise()`. So "re-evaluates" is accurate for compute + route + human-resolve; the auto-apply bucket is declared, not wired. |
| Apache-2.0 | **VERIFIED** | `LICENSE` L1-2 "Apache License / Version 2.0, January 2004"; `NOTICE` "Atlas / Copyright 2026 Richard Schefren and Atlas Contributors". |
| On Graphiti | **VERIFIED, substrate-only** | `atlas_core/graphiti.py` L46: `class AtlasGraphiti(Graphiti)`; `pyproject.toml` L40 `graphiti-core>=0.28.2`. But L52-54: AGM-managed edges (SUPERSEDES, DEPENDS_ON, DERIVED_FROM, CONTRADICTS, SUPPORTS) **bypass** Graphiti's LLM-driven `resolve_extracted_edges`; L3-5: raw Graphiti extraction "is intentionally separate from trusted Ripple execution". Graphiti is the ingestion/extraction substrate; the reasoning layer is hand-rolled deterministic code. |

Also verified beyond the brief: adjudication writes an Obsidian markdown queue
with checkbox decisions + per-component audit breakdown (`adjudication.py`
L197-273); a resolver applies accepted decisions through the AGM revise()
operator and appends a ledger audit event even on reject (`resolver.py`
L177-270+); temporal decay half-life 90 days (`reassess.py` L179-195).

## 2. DEFECTS FOUND IN ATLAS ITSELF (steal the warnings, not just the wins)

1. **AUTO_APPLY is unwired.** No module in the production tree consumes
   `AdjudicationRoute.AUTO_APPLY` (grep over atlas_core/ excl. adjudication.py,
   engine.py, __init__.py: zero hits, exit 1; the only other hits in the whole
   clone are two test ASSERTIONS, tests/integration/test_adjudication.py:138,252,
   which check that route_proposal returns the AUTO_APPLY label and apply
   nothing; `adjudication.py` L344-347 says routine proposals are "auto-applied
   via AGM revise() upstream" but no caller does it; the materializer checks
   only `cascade.succeeded`). A routing bucket without an executor is a belief
   that work happened when it did not.
2. **Doc/code formula drift inside one file.** `reassess.py` L245-247 (the Args
   docstring of `reassess_dependent`) still states the OLD weighted-average
   formula that L37-49 documents as buggy and L282-286 replaced with the
   damped-perturbation form. Their own spec-keeper missed a docstring; the same
   class of drift our spec-before-behavior law exists for.
3. **Chain honesty is already priced in.** Their docstring concedes the limit:
   "A local writer with database access can still rewrite the chain and recompute
   hashes unless the head hash is externally anchored" (`ledger.py` L13-15) and
   "This detects corruption; it is not a signature or external anchor" (L194).
   Any estate port inherits this limit; external anchoring (our verkle knot) is
   the missing half on both sides.
4. **Confidence floats with uncalibrated weights.** Weights 0.50/0.30/0.15/0.05
   are "calibrated empirically in Phase 3" per comments (`reassess.py` L30, L48)
   and the HeuristicReassessor fallback bounds the LLM delta at +/-0.5 (L137-141).
   The numbers are plausible, not proven; the benchmark
   (`benchmarks/business_mem_bench/`) exists in-tree but I did not run it.

## 3. THE ESTATE GAP, CONFIRMED AT THE DATA LEVEL

`memory/percolator/invariants.json`: 639 invariants, dict keyed by 16-hex
content hash. Full key coverage over all 639 rows: `text, count, first_seen,
domain, last_seen, decay_as_of, cycle_hits`. **No dependency field of any
kind** (no depends_on, no parents, no derived_from, no confidence, no status).
The percolator compiles repeatable signal into flat counters with half-life
decay (`mag/percolator.py` L8-17, L24-34: half-life, max-merge, self-emission
cap). When a fact changes, nothing re-evaluates anything downstream. The
landscape brief's pre-read ("the percolator promotes but never re-evaluates
dependents; a belief-graph port is the missing half") is confirmed.

Closest existing estate organs the port composes with (all read this session):

- `tools/doctrine_arbiter_core.py` L23: `STATUSES = ("PENDING", "VINDICATED",
  "EXPIRED", "VOID", "RETIRED")` - the estate already scores beliefs; terminal
  verdicts freeze status. The port's "confidence" is this verdict enum plus
  check receipts, NOT a float.
- `mag/fact_bus.py` L90 `publish_fact(...)` (folds via verkle + publishes) -
  the existing channel cascade events ride.
- `mag/invariant.py` freeze/check + `check_instructions()` (L149-182, L231-248)
  - the estate's byte-pin invariants (sha256 + verkle anchor) are already a
  fact-dependent invariant with a re-check, for exactly two pinned subjects.
- The census claim machinery (AGENTS.md census bullet + `tools/census_drift_patrol.py`
  with `--collect`, per AGENTS.md B2-244/B2-249) - the estate already runs ONE
  downstream re-evaluation loop end to end: a claim, an instrument, a trigger
  (daily task + pre-push), a falsifier (>=20 drift), and an attributed refresh
  path. The port generalizes that shape from one bullet to a graph.

## 4. THE PORT SPEC: DOWNSTREAM RE-EVALUATION ON ESTATE ORGANS

Name: **the cascade ledger** (working name `mag/invariant_cascade.py`, $0,
stdlib-only, deterministic, schema `invariant_cascade.v1`). Four parts:

### 4.1 The belief graph: which invariants depend on which

Estate invariants do not primarily depend on each other; they depend on FACTS
(the volatile world their text embeds). The graph is invariant -> dependency
edges, with invariant-to-invariant edges only where one invariant cites another
by hash. Each row in `invariants.json` gains an optional field:

```
"depends_on": [
  {"kind": "census",        "key": "tests.collected",        "observed": 3550,     "as_of": "..."},
  {"kind": "file-sha",      "key": "state/SESSION_SEED.md",  "observed": "<sha>",  "as_of": "..."},
  {"kind": "law-status",    "key": "doctrine_arbiter:<row>", "observed": "VINDICATED", "as_of": "..."},
  {"kind": "queue-state",   "key": "handoff.open_count",     "observed": 5,        "as_of": "..."},
  {"kind": "receipt-exists","key": "watch/inbox/...",        "observed": true,     "as_of": "..."}
]
```

Edges are mined two ways, both deterministic:
- DECLARED at fold time: the lane that compiles an invariant names what facts
  its text is about (costs one dict, stays honest).
- MINED retroactively: a token scan over `text` for volatile payloads -
  integers, paths, count-bearing phrases (`N tests`, `improve_queued=0`,
  `handoffs=5`), file paths. Real rows prove the need: of the registry's top
  rows, "source=swarm_health_law improve_queued=0 handoffs=5" (count=32)
  embeds two volatile numbers; "[steer] Verify with git diff / actual file
  bytes before declaring done" (count=32) embeds none and gets
  `depends_on: []` (command-shaped invariants are fact-free and never cascade).

Concrete dependency examples on our organs:
- The AGENTS.md census bullet depends on `tests.collected` (instrument:
  `pytest --collect-only -q`; this is B2-244 generalized).
- Session/instruction pins (`mag/invariant.py`) depend on `file-sha` of
  SESSION_SEED.md, work_contract.BRIEF, FROZEN_RIB, corrections SKILL.md
  (instruments already exist: `check()`, `check_instructions()`).
- Doctrine laws depend on `law-status` of their arbiter rows (instrument:
  arbiter status read; PENDING rows re-check on cadence, terminal rows freeze
  - reusing arbiter semantics instead of inventing a confidence float).

### 4.2 What triggers re-check

One trigger, three doors (mirrors how the fleet already runs checks):
1. POST-FOLD: after `percolate()` compiles an invariant, run the instruments
   for its edges once and pin `observed` + `as_of` at birth.
2. MAINTENANCE: `maintenance()` already exists for half-life decay
   (`percolator.py` count law 1); a cascade pass rides the same call: for each
   dependency kind, run its instrument (a small registry: census-collect,
   file-sha, arbiter-status, queue-scan, receipt-exists), compare to `observed`.
3. ON-DEMAND: `python -m mag.invariant_cascade check` for any lane that just
   changed a fact (the "I changed the tests" door).

Instrument failures are UNVERIFIED, never silently stale: an instrument that
cannot run pins `observed: null, note: "instrument failed: <e>"` and cascades
as UNVERIFIED (citation-resolution law: bytes or UNVERIFIED).

### 4.3 The cascade

On observed != pinned, BFS the graph over reverse dependency edges (dependents
first, Atlas's `analyze_impact` shape: visited-set cycle guard, max_depth 10 /
max_nodes 5000 defaults, BFS order shallowest-first - all stolen, all that
terminates). Each visited invariant yields a PROPOSAL, never a mutation
(Atlas's proposal-not-mutation doctrine, `reassess.py` L7-10, is correct and
is kept):

- REFRESH: the fact moved but the invariant is still true with new numbers
  (census drift). Auto-APPLIED by re-stamping the row (new `observed`, new
  `as_of`, count preserved, supersede note appended) - this is where the
  estate beats Atlas: our instruments are deterministic, so the auto-apply
  bucket actually has an executor. Atlas's unwired AUTO_APPLY (defect 2.1)
  is the anti-pattern named and avoided.
- ESCALATE: the invariant's premise broke (a law it cites went EXPIRED, a
  receipt it cites was superseded). Lands as a queue row (Atlas's Obsidian
  checkbox idea, rebased on our inbox: `memory/percolator/cascade_queue.jsonl`,
  status pending -> resolved by the next lane that touches the subject) and a
  fact_bus publish. No silent demotion; the doctrine-arbiter EXPIRED path stays
  the only kill path.
- ANNOTATE: premise softened (fact moved without breaking the premise) -
  append `cascaded_at` + note, count untouched.

### 4.4 What the cascade receipt shows

One row per cascade in `memory/percolator/cascades.jsonl`, folded via
`fact_bus.publish_fact`, chained like Atlas's ledger but scoped to cascades:

```
{"schema": "invariant_cascade.v1",
 "cascade_id": "<sha256(prev_cascade_id|origin|proposals_json)[:16]>",
 "prev_cascade_id": "<...>",
 "origin": {"kind": "census", "key": "tests.collected", "old": 3550, "new": 3551},
 "impacted": 4, "depths": [1, 1, 2, 3],
 "proposals": [
   {"key": "<invariant hash>", "depth": 1, "route": "refresh",
    "components": {"observed_delta": 1, "dependents": 0, "age_days": 31},
    "rationale": "census moved; row re-stamped as_of <ts>"},
   {"key": "<invariant hash>", "depth": 2, "route": "escalate",
    "components": {"law_status": "EXPIRED"},
    "rationale": "cites a law row that went EXPIRED; queue row written"}],
 "routes": {"refresh": 3, "escalate": 1, "annotate": 0, "unverified": 0},
 "ts": "..."}
```

The receipt shows, per cascade: the origin fact with old/new, the BFS shape
(counts per depth), per-proposal route + component breakdown (stolen from
Atlas's `ReassessmentProposal.components`, their best audit idea), the route
tally, and the chain coordinates. `cascade_id` hash-links the previous cascade
so any edited history breaks the walk - the Atlas ledger property at cascade
grain, with the SAME honest limit their `ledger.py` L13-15 concedes: tamper
DETECTION only, no signature; the verkle knot anchor (fact_bus already folds
there) is the external-anchor half.

## 5. GRAPHITI vs THE HAND-ROLLED SPINE

Atlas's own architecture answers the question: the load-bearing layer is
hand-rolled and deterministic; Graphiti is used for raw extraction only and is
deliberately prevented from touching the reasoning edges (`graphiti.py` L3-5,
L52-54). The five AGM edge types, the ripple traversal, the hash chain, the
adjudication queue: all plain Python + SQLite, with Neo4j as storage.

The estate's spine (percolator lexicon scoring, flat JSON registry, verkle
knot, fact_bus, doctrine arbiter, receipts + byte checks) already occupies the
hand-rolled layer. What Atlas has that we lack: dependency edges + a trigger +
a structured cascade receipt. What we have that Atlas lacks: deterministic
instruments (so auto-apply can actually execute), an external anchor habit
(verkle), a verdict-enum belief scorer (arbiter) instead of uncalibrated
floats, and a receipts culture they partly reinvent.

**Verdict: do not adopt Graphiti or Neo4j.** The estate graph is a dict
adjacency over 639 invariants - a JSON file, not a graph database. Adopt the
SHAPE: impact BFS + proposals + 3-bucket routing + human adjudication queue +
ledger-audited resolutions, per section 4. If the registry ever outgrows a
single JSON file (10x today is ~6400 rows, still trivial), revisit; not before.

## 6. HONEST GAPS

- Benchmark `benchmarks/business_mem_bench/` present in-tree, not run (needs
  LLM keys + full deps); their "100% across 49 scenarios" AGM claim is the
  paper's (`paper/atlas.md`), UNVERIFIED here.
- `tests/unit/test_graphiti_ripple_boundary.py` NOT RUN: imports
  graphiti-core, deliberately not installed in the scratch venv (heavy deps).
- 45 other unit tests PASSED first-hand (test_ledger 26, test_reassess 11,
  test_proposal_vs_mutation + test_depends_on_edge_property 8) on a scratch
  Python 3.12 venv (pytest, python-ulid, pytest-asyncio only).
- The port is a SPEC, not code: nothing under mag/ or tools/ was touched this
  lane, so the violation ratchet was not run (no diff to check).

## 7. FILES THIS LANE WROTE

- `watch/inbox/localfirst/atlas.md` (this receipt)
- `watch/inbox/localfirst_memory_landscape_signals.jsonl` (register row, atlas)
- `watch/inbox/gala_20260925/localfirst-steal/lanes/atlas.json` (lane out)
- `watch/inbox/gala_20260925/localfirst-steal/lanes/atlas.check.txt` (raw check output)
- `watch/inbox/gala_20260925/localfirst-steal/lanes/evidence/atlas_excerpts.md` (verbatim excerpts)
