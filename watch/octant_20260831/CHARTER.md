# OCTANT formation charter (2026-08-31, operator: 8× 5.3 leads, each with own deepseek gophers)

## Slot law (hard constraint, receipted)
- OpenClaw caps this session at 6 active children. Leads + gophers share the pool.
- Pool discipline: 6 leads max concurrent; as each completes, its gophers launch from its briefs; wave 2 fills freed slots. Total 8 leads + unbounded gophers across waves.
- Sancho = spawn authority + merge point (by design, one synthesizer — swarm_cycle law).

## Efficiency law for 5.3 (what "using it efficiently" means here)
1. **Warm start:** each lead reads only its pack slice + 2-3 primary files. No transcript copies.
2. **Iterate inside the lead:** draft → self-attack once (name your weakest sentence, fix it) → final. Iteration is internal, not extra spawns.
3. **Gopher offload:** leads NEVER do mechanical fetch/grep recon themselves — they end with GOPHER briefs:
   `GOPHER: <one claim to verify/fetch> | pointer: <path> | output: /board/octant_20260831/rows/<lead>-g<N>.row.md`
   Sancho converts briefs → flash lanes (fixed ROW format, $0).
4. **Output contract:** every lead writes exactly one file in /board/octant_20260831/ + reports ≤3 lines.

## Wave 1 (6 leads)
| Lead | Mission | Output |
|---|---|---|
| ox-archaeology | Reconstruct the ACTUAL past ox formation from /board/grok_feed.jsonl (bounded: count first, sample ≤200 lines total) + salons + game_grok_night trails: how many concurrent agents, what roles, pairing, iteration cadence. We clone the real thing. | formation.md |
| doctrine-canonical | Fold audit + T1/T2/T3 verdicts + 11 patches into ONE canonical authority-doctrine doc (the thing a new seat reads first). | doctrine.md |
| atlas-draft | Draft the Atlas/Basecamp receipts-first map for board surfaces (what host `mag.atlas build` should produce; cage-side draft with pointers). | atlas_draft.md |
| riddler-tape-v1 | The timed-out trajectory riddle, redone: last 40 tape lines, 7-10 conclusions, surrogate cast, forbidden-string self-check. | riddler_v1.public.json |
| apply-runbook | One-page operator runbook: apply order for 11 patches + lattice, bless decisions (kind:seat), row-zero pipe, verification steps. Operator-surface language. | runbook.md |
| zai-window | Half-price window plan till 09-09: which heavy jobs run when (charters, iterations, T-cycles), Mag host lanes stay deepseek off-peak — schedule doc. | window_plan.md |

## Wave 2 (queued, 2 leads — spawn as slots free)
- codex-brief-writer: next 3 codex job contracts from T-verdicts.
- drift-hardening: drift rotation schedule + auto-rebaseline procedure.

## Gopher pool
Briefs land in this dir as leads finish. Sancho spawns ≤6-concurrent flash lanes per brief, ROW format, merge into ledger.
