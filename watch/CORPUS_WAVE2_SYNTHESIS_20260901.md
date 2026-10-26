# CORPUS BUILD WAVE 2 — SYNTHESIS (2026-09-01 ~18:12Z)

All 4 lanes landed + parent-verified at bytes. The corpus tree now holds the primer's
directory layout with real cache-ready content.

## The corpus after wave 2 (one day, from empty skeleton)

```
corpus/
├── 00_PRIMER.md                          ✅ L0 charter (operator-delivered, verified)
├── L0_universal_contract.DRAFT.md        ✅ six functions + universal RNG (5 historical modes)
├── L1_engines/
│   ├── race_dice.DRAFT.md                ✅ (wave 1)
│   ├── sowing_capture.DRAFT.md           ✅ NEW — born from the oware boundary test
│   ├── constraint_puzzle.DRAFT.md        ✅ NEW — 5-part grammar + 7-clause vocabulary
│   └── rpg_engine.DRAFT.md               ✅ NEW — dice ladder + solo oracle + narrator/archivist split
├── L2_games/
│   ├── kakuro.DRAFT.md                   ✅ NEW — first proof-pack of the grammar
│   ├── hitori.DRAFT.md                   ✅ NEW
│   └── nonogram.DRAFT.md                 ✅ NEW
├── L3_packs/                             ✅ 7 cultural packs (wave 1) + spore seed
├── L4_instances/                         (ephemeral by design)
└── L5_themes/                            (skins, pending)
```

## What wave 2 contributed beyond mass

1. **sowing_capture engine** — the oware boundary test's honest refusal became the corpus's
   7th engine family. Falsification → architecture, the primer's own method.
2. **constraint_puzzle grammar** — the 5-part grammar (TOPOLOGY/DOMAIN/CLAUSES/INSTANCE/
   VERIFIER) with a 7-clause reusable vocabulary (all-different, sum-equals, edges-diff,
   isolate, line-model, count-marks, consecutive) and the universal verifier chain
   (parse→assert→solve-count→technique-ladder; solve-count==1 = acceptance oracle). The
   Kakuro proof-pack instantiates 2 of 7 clauses and proves the "one clause-swap → Sudoku"
   generalization claim.
3. **The cache-boundary decision rule, formalized:** pure-rule variants extend the static
   prefix atomically (prior layers still cache-hit); structural variants extend the dynamic
   layer AND patch the engine's clause vocabulary. This is the rule that keeps the byte
   law from becoming a straitjacket.
4. **rpg_engine** — the primer's big-payload jackpot as prompt text: dice ladder + Mythic/
   Ironsworn solo oracle + scene state machine + the narrator/archivist split (arXiv
   2502.19519) + the static payload map (system 2-10K / bible 5-50K / bestiary 3-20K at
   ~95% hit = the corpus's largest absolute savings).

## Engine coverage: 4 of 7 families (57%)

✅ race/dice · sowing/capture · constraint/puzzle · narrative/RPG
⬜ board/strategy-war/capture (chess/go/tafl — L1 spec pending)
⬜ card systems (hanafuda/dominoes/trick-taking — L1 spec pending)
⬜ tile matching is partially covered by race_dice + the L3 mahjong packs

## Meter & status
Wave-2 spend: ~4 lanes × 17-31k tokens on deepseek + cerebras (free) — inside the balance
already reported ($21.81 post-fanout). E7 vast hour: parked after 4 search-API strikes
(each a distinct vast quirk: equal→eq, q-JSON format, cost_per_hr→dph_total naming);
known one-line fix awaits attempt 8, OR the LM Studio host arm makes it moot (chat model
pending in LM Studio). All files registered with SHA-256 in INDEX.
