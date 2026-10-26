# MAHJONG × SUDOKU — OPERATOR-ATTACHED LEAD (2026-09-01 ~12:10Z)

> **Grading: external-content LEAD** (operator-attached AI report, same chain as the
> genome lead). History section: consistent with known facts (madiao→Mahjong 1870s;
> Babcock 1920s; NMJL 1937; Garns/Dell 1979; Nikoli 1984; Gould/Times 2004; Lo Shu legend;
> Euler 1783; 17-given minimum) — no fabrication flags. **One caught error:** state space
> for Sudoku stated as 7.2×10²⁰ — actual ≈ 6.67×10²¹ (log for the record). The 8-9× cost
> claim is Anthropic-pricing-consistent but OUR measured number remains E6's 4.7× on
> Together. Everything else: structure maps 1:1 onto the games-salon architecture.

## Sancho's mapping (what this doc adds to what we built)

1. **The cache-boundary decision rule (new, load-bearing):** *"pure-rule variants (X, Hyper)
   extend the static prefix; structural variants (Killer, Jigsaw) extend the dynamic layer."*
   Knowing which side of the boundary a variant falls on = the key architectural decision.
   Adopted into the build-row schema as a required field: `boundary: static|dynamic`.
2. **Compact canonical encodings (new):** Tenhou tile notation (hand ≈ 10-15 tokens vs
   60-100 prose) + 81-char Sudoku grid strings. Token density multiplies cache value.
3. **The verification protocol (matches our truth/narration law):** LLM as orchestrator
   around deterministic verifiers (Sudoku solver/uniqueness count; Mahjong shanten/ukeire/
   yaku-table check) — same as our meter law, applied to puzzles. Verifiable in node (no
   python needed): Sudoku parse + constraint check + solution count is trivial JS.
4. **First two farm families named:** Mahjong (3-layer: static ~2K / variant ~1K / instance
   ~200 tokens — Layer-1 hit every request, only ~10% fresh) and Sudoku (pure deduction,
   no RNG block needed, 81-char instances).
5. **Hybrid designs (gamedesigner seat backlog):** Nine Halls (★★★ immediate — Sudoku
   logic, mahjong skin, entire rule system ~300-token static block), Lo Shu Bridge (★★★
   + cultural module), Constraint Riichi (★★), Tile Deduction (★ multi-agent).
6. **Historical modules as one-time cache writes** shared across a game family — the Lo Shu
   module serves Sudoku + hybrids + cultural variants. Cross-game prefix reuse, confirmed
   by our own lane topology.

## Relationship to the corpus/salon (no conflicts)
- The 3-layer structure = our L0/L1/L2 mapping, independently restated with concrete
  token budgets. The "cache-boundary rule" is the ONE genuinely new architectural idea.
- Implementation roadmap Phase 1 (static asset creation) = actionable now as freeze-pack
  files; Phase 4 (hit-rate instrumentation) = our meter law already does it.

## E8 CANDIDATE (the obvious next experiment)
Farm build #1: **Sudoku via the cache-farm pattern** — static prefix (81-char schema +
constraints + verification protocol) + one instance delta; node-side solver verifies
uniqueness; build-row lands in meter_readings.jsonl with cached_tokens from the provider.
Cheapest possible first proof of the whole farm loop end-to-end.

## Original report (operator paste, verbatim from "Certainly! I will detail..." through
the Phase 4 checklist — preserved in the session transcript of 12:10Z; the load-bearing
sections are restated above. Full text held in transcript as primary; this file is the
graded board copy. If verbatim storage is wanted, the operator paste can be appended.)
