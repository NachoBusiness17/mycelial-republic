# riblive1-U1-r2-glm-flash (glm-5.3-flash @ zai, turn 1, channel: content)

L1: Exit 2 belongs to sibling instruments too, not just the census patrol
CLAIM: My exit-2 cannot-verify arm (L3) and the selector sibling's UNMEASURABLE guard (V2 L2, "empty shared set still yields DECORATIVE verdict") are the same law in two bodies: a verdict must never be emitted from a measurement of nothing. The FTS sibling's malformed-lines skip (V3 L4) is the third instance: skipped lines must surface as a count the operator can gate on, never as a silent pass.
STEAL: Add a shared assertion idiom to all three tools: any empty-evidence path (shared_positions == 0 in preload_selector.compare, malformed_lines > 0 in corpus_fts_rebuild.build_index, unparseable claim in census patrol) returns its tool's cannot-verify code before any verdict assignment.
FALSIFIER: Any of the three tools emitting DECORATIVE / OK / exit 0 on an input where the evidence set is empty or partially dropped.
SOURCE: my L3 (census exit-2), (V2 L2), (V3 L4) "malformed += 1"
LEVERAGE: high

L2: Frozen witnesses must never sync to live bytes, in either direction
CLAIM: My L2 freezes regression vectors against the live AGENTS.md count so the fixture can catch a grammar break. The FTS sibling's meta contract (V1 L1) is the mirror image: catalog_bytes and catalog_sha256 are frozen witnesses of the catalog at build time, and the live file drifting is what the witness is supposed to detect. Both laws say the same thing from opposite sides: the witness is frozen; the world moves; the mismatch is the signal.
STEAL: When the FTS sibling's staleness gate fires, do not refresh meta in place; route through the single sanctioned writer (V3 L1) and require a rebuild receipt, exactly as my frozen fixtures move only with a named receipt (B2-274).
FALSIFIER: Any code path that rewrites meta.catalog_bytes to match the drifted catalog instead of flagging staleness, or a fixture updater that reads the live bullet to regenerate selftest vectors.
SOURCE: my L2, (V1 L1) "detected by bytes even when a restore or a touch lies with mtimes"
LEVERAGE: high

L3: Byte-count staleness detection needs the census treatment
CLAIM: The FTS siblings' byte-gate (V1 L1, V3 L3) and my disk-shrink rule (my L2) both detect loss by size, and both inherit the same asymmetry risk: a file edited in place with equal bytes but different contents defeats the byte gate, just as intra-file parametrize growth defeats my default gate (my L5). Both instruments have a documented blind spot that only an explicit deep tier covers: sha256 for the index, --collect for the census.
STEAL: Combine the two steal actions into one scheduled job: a timer that runs tools/census_drift_patrol.py --collect and corpus_fts_rebuild.py check --deep in the same CI step with the venv present, so both deep tiers run on one cadence instead of each rotting independently.
FALSIFIER: A CI job that runs one deep tier without the other, or a timer job that passes while an in-place equal-byte catalog edit plus an intra-file parametrize addition both go undetected in the same push.
SOURCE: my L5, (V1 L1), (V3 L3) "sha256 only on --deep"
LEVERAGE: medium

L4: Same-day ambiguity is the freshness-rule law the selector lacks
CLAIM: My L1 excludes same-day commits as ambiguous; my L4 requires age AND movement. The selector sibling's recency collapse (V2 L3, missing ts -> 0.0 tail) and the zero-span dead branch (V2 L1, spec says 1.0 but code yields 0.0) show the cost of an unpinned ambiguity rule: blocks with unknown or shared timestamps silently lose ordering, and the spec and code disagree with no frozen vector catching it.
STEAL: Before patching the V2 L1 branch to (1.0 if ts and ts_span == 0 else 0.0), add a frozen vector asserting the SPECIFIED value, then pin same-day/zero-span recency semantics in the vector set so the spec and code cannot drift apart again, mirroring my strictly-after vector at 23:59.
FALSIFIER: A patched score_blocks where two identical-valid-ts blocks score 1.0 but no frozen vector exists that would fail if someone reverts to the current bytes.
SOURCE: my L1 (23:59 vector), (V2 L1) "can never yield 1.0", (V2 L3) "recency 0.0"
LEVERAGE: high

L5: Pure verdict cores need their instruments named, and the selector already does this right
CLAIM: My L3 routes every gather failure of census patrol into pure cores with distinct exit codes. The selector sibling's scope law (V4 L1: PROXY label, 2-3B specimen, never production GLM-5.3-flash fidelity) is the condition half my laws under-specify: my verdict names moment and context only implicitly. A verdict dict without instrument, moment, and context fields fails the estate rule that a verdict without its conditions is not a verdict.
STEAL: Extend census patrol verdict dicts with instrument ("census_patrol vN"), specimen context (venv present, --collect on or off), and moment (census_date compared), matching the selector's honesty field so downstream seats can cite my rows the way V4 L1 demands of its own.
FALSIFIER: A downstream consumer citing a census patrol OK verdict without being able to determine from the dict whether --collect ran, which would reproduce the aggregate-denominator hiding my L-in-5 warns about.
SOURCE: my L3, (V4 L1) "cite the honesty field in the row when reusing it downstream"
LEVERAGE: medium
