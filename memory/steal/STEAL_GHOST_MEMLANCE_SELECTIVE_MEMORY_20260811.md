# STEAL — ghost_memlance: selective, grounded memory-state selection (2026-08-11)

Operator: "use our ghost steal module like pylance so we can select memory states selectively without
bringing hallucination with [it]." → Build the ghostlance analog for MEMORY: deterministic, $0,
provenance-grounded memory-state selector that NEVER drags in hallucinated/unverified context.

## STEAL ANALYSIS
- SELF: ghost_pylance (GHOSTLANCE) = deterministic code-intelligence memtool (diagnose/symbols/
  references/trace_value/imports/self_check, stdlib-ast, registered as ghost `code/intel`). The SAME
  shape applied to MEMORY is the anti-hallucination selector: reason over stochastic recall, but
  SELECT + VERIFY memory against ACTUAL bytes on disk, never synthesize a state from memory-of-memory.
- EXTERNAL: RAG grounding + provenance discipline — retrieval returns source bytes + a verification
  verdict, and LABELS what is not grounded instead of silently passing it. Adapted as a deterministic
  contract, no prompt DNA.

## Built: mag/ghost_memlance.py (ghost_memlance.v1, $0, stdlib-only)
- index()      — index real memory states from disk (steal/rib/law/decisions/directives/handoff/runs_top/
  biography-verkle): path, kind, title, ts, tags, grounding verdict, real excerpt bytes.
- select(goal) — select RELEVANT + GROUNDED states for a context. Only reads REAL bytes from disk;
  ranked by keyword/title overlap + verified-weight. Returns provenance (path) + `verified` verdict.
  Unverified-but-matching states are returned clearly flagged so the ghost does not carry them forward.
- trace_state(key) — provenance + cross-refs of one state (like trace_value for memory).
- verify(key)  — deterministic grounding verdict + the markers that prove/refute it.
- self_check() — counts: n states, verified vs unverified, by_kind.

## Grounding verdict (deterministic, conservative — the anti-hallucination bead)
- VERIFIED only if bytes carry a real-data/RIB marker: verified/grounded/measured/billed/rib_/frozen/
  real data/real billing/rib-debug/validated/shipped.
- Explicitly NOT grounded if it carries: unverified/derived/estimated/assumption/plan only/
  not runtime-proven/handwave → forces verified=false (even if a generic marker appears).
- Default = UNVERIFIED (no marker) → the ghost knows not to carry it as truth.

## Verified (via OUR headless runner, ghostlance surface — NOT external Pylance MCP)
- ghostlance self_check: 510/510 modules syntax-clean (ghost_memlance included).
- memlance self_check: 1304 states indexed; 207 verified (15.9%), 1097 flagged unverified.
- memlance select("grok key funding supergrok front-end") → returns grounded grok-4.5 hub/swarm design
  with provenance + verified=true, correct ranking, no fabricated content.

## Lesson / law
- Execution carrier matters: verified via mag.headless.run_headless (OUR runner), not the external
  Pylance MCP tool as carrier. See /memories/repo/ghostlance-not-pylance-20260810.md.
- Anti-hallucination = ground in the bytes on disk + label unverified, never recall-from-recall.
