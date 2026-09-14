# CATALOG — L2 Games Review (2026-09-01)

**Seat:** L2 catalog / local-tutor siting. **Standard:** L0 `LEGAL?(state,T)->Bool` — deterministic, verifier-enforceable, never-invented. **Split:** 2 sowing/runtime (bao, kalah) + 4 constraint puzzles (hitori, kakuro, nonogram, sudoku). All DRAFT; none verified.

---

## Per-static table

| Static | Verifier-enforceable? | VRAM/complexity (local tutor) | Completeness gaps |
|---|---|---|---|
| **bao** (sowing_capture) | **PARTIAL.** Deterministic core (own-side pit, sow cascade, own-opposite capture, store-majority 33/64). But 3 clauses `reconstructed`/speculative: waiting-obligate opening, nyumba home-priority, grand-slam+lape. Verifier written to draft ≠ verifier to tournament Bao; target underspecified. | Heavy. 32-pit ring + empty-before-sow + capture-walk + lape bonus-turn. State≥32+2. Fits mid seat, but costliest verify of the six. | No V-signature block (unlike the 4 puzzles). Non-empty sweep tie-break fuzzy. Must pin 3 reconstructed points to one recension first. |
| **hitori** (constraint_puzzle) | **YES.** V1/V2/V3 pure, deterministic, JS-implementable (O(W²) BFS/ufind + backtracking uniqueness). Zero-move (F4/F6 null). Strong. | Low. Cheapest of the six; trivial RAM/VRAM. | Rules `attested`, no contested flags. No substantive gap. |
| **kakuro** — proof-pack | **YES.** parse → sum-solver → `solve-count==1`; all five slots filled; all-different+sum per run canonical. Numeric T1–T5 ladder. Strong. | Low. Per-run sum/diff + uniqueness; light. | `game id` enum not literally spelled in header (kakuro & sudoku both) — needed for RNG/dedupe hard-keying; cosmetic, fixable. |
| **kalah** (sowing_capture) | **YES.** Fully deterministic: lift ≥1, sow w/ own-store deposit (skip opp store), single-capture to store, `LAPE: store-landing` bonus turn, instant win 25/48. No `reconstructed` flags; every variant defaulted. Best-enforceable grower. | Heavy-ish but clean. N=12 + store-pass + capture + bonus-turn; state 12+2. Fits mid seat. | Variants each defaulted (`CHAIN on` alt, `s=3` alt) — verifier keys on named default. No V-signature block (engine-shared). Akan note is cultural, not mechanical. |
| **nonogram** (constraint_puzzle) | **YES.** V0/V1/V2/V3 pure; line-DP expansion + row/col walk + backtracking. Deterministic. | Medium. Line DP O(W·k·W) + grid walk/backtrack. Light RAM; heaviest puzzle only in edge branching. | `Ø` clue spelled; both VALID gates supplied. No substantive gap. |
| **sudoku** — flagship | **YES.** Clause 1 ×3 rows/cols/boxes, 81-char instance, `solve-count==1`, ladder. | Low. All-different ×3 + uniqueness; famously small. | Terse (40 lines). No explicit `game id` enum; no V-signature heads (prose-only, engine-shared). Lineage + McGuire note honest. |

---

## Gauntlet-readiness (W2 dual verify+synthesize+siting)

**Top-3 most gauntlet-ready:**
1. **kakuro** — proof-pack; exercises every grammar part (run TOPOLOGY, sum+all-different pair, stub-board encoding, numeric ladder). Verifier functions + uniqueness gate already concrete. Best W2 stress (parse/assert/solve-count round-trip).
2. **hitori** — cleanest smallest verifier (3-rule + uniqueness), zero-move, `attested`, no contested flags. Cheapest to instrument; ideal "smallest trainable" family reference.
3. **kalah** — fully deterministic, zero `reconstructed` flags, every variant pinned to a default; simplest grower. Proves the sowing-engine verifier end-to-end (contrast bao).

**Watch-list (defer gauntlet):** **bao** — pin 3 reconstructed clauses to one recension before verifier is stable. **nonogram**/**sudoku** are verifier-solid; sudoku needs `game id` + V-signatures for RNG/dedupe hard-keying (cosmetic).

**Recommendation:** 6/6 verifier-enforceable core; 6/6 gauntlet-runnable, but only **kakuro, hitori, kalah** gauntlet-ready without an editing pass. Push bao to pin recension; add `game id` enums to kakuro+sudoku.
