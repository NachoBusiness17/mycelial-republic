# WHAT REMAINS - verkle audit + open-work inventory (2026-09-19)

Ordered by "what remains to be done check the verkle" - the chain itself is HEALTHY.
Every claim below is read from disk this window, not recalled.

## Verkle verdict: GREEN

- `memory/biography/verkle_chain.jsonl`: **8,686 knots, 0 broken prev-links**, tip
  ts 2026-09-19T12:33:02Z (fresh, autonomous janitor session fkb-d9435a).
- Root pinned 46d8e5ecfd7de0f6 per witness fold (commit 7a35ab29e) - tip matches.
- Owed on the chain itself: **append-only doctrine reconciliation** - the amendment
  path (void/contest/witness rows, `mag/grounding_wave.py` _KIND_KEYS) exists in
  code but chain law never names it. One-paragraph law file.
- Small debt: `chain_guard` has no direct test file.

## Fixed this window (was burning)

- **AMENDMENT 001 violation in build lane** (`scripts/build_lane_game.py`): a run
  that died in transport (HTTP 404 stealth death) was counted as a REJECTION and
  burned attempts. Fixed: `all_transport` flag per run; transport deaths now land in
  `transport_pruned`, never `rejected`/`attempts`.
- **Ledger repaired** (`build_lane/state.json`): recomputed from proposals.jsonl -
  of 32 recorded "rejections", only **2 were real gate rejections**; 26 runs were
  pure transport deaths (21 of them on briefs that later promoted anyway).
  Confirms REJECTION_TAXONOMY: the pipe, not the gate, was the bottleneck.
  `DD-blob-double` + `DD-split-path` attempts reset (were marked dead by 404s).
- Stealth 404s on DD batch (gelatinous-cube/mimic-plate/riddle-door/dragon-hoard)
  = the same window death; briefs remain open, will fire on the live model.

## REMAINS - meters before audits (Elder passes 2/3 are blocked on these)

1. **UF-109 degeneracy probe** - spec filed, no code. The evolution loop's
   selection gradient is unmeasured.
2. **UF-47 Librarian citation battery** - 20 fixed questions + ground truth.
   Imprint decay stays unverified until this runs.
3. Elder pass 2 = re-audit WITH meters; pass 3 after traits into step().

## REMAINS - engine work (small, named)

4. **Traits into step()**: thorns (skip-next-turn on contact) + chain (drag room
   tick parity) still unwired; vision + berserk are live in ruins_go_engine.js.
5. **Blob-double engine v1.2**: push-duplicates-block, ~3 lines + blobMode flag;
   spec filed, kubernetes mapping done.
6. **maze_arena seeded harness**: 10 Math.random sites, biggest untested surface;
   needs seeded stream + input tape (F1/F2 pattern).
7. **Mud duplicate fork**: `dashboard/static/mud.html` vs `dashboard/static/games/mud.html`
   byte-identical; link-map check, then delete the stale mirror.
8. **Difficulty hole**: no bred level lands 10–14 moves; briefs owe a targeting pass.

## REMAINS - fleet surfaces

9. **Astra v4 dispatch** - brief CONVERGED (RS-DPO+HyPO, sealed-first curator,
   three-family audit). Nothing has been sent. The $100 Hermes plan rides on it.
10. **NPC face registry live**: kabuki_cast schema extension + 3 starter faces
    (innkeeper, vault warden, bones guide) through chat_provider.
11. **Thought quantizer v0.3**: two-pass classification (over-refuses error-quoting
    laws), source-distinct weighting, wire into wave rebuilds.
12. **6 knowledge-graph organs unfilled**: doctrine-canon edge typing, evolution-loop
    output ledger, versioned lane registry, estate→canon promotion pipeline,
    training outcomes ledger, percolation run log.
13. **External better-executor sweep** (who executes our ideas better than us).

## REMAINS - Sep-20 TRUNK (tomorrow)

14. Astra I2/I3 · HOLD 3/4 rehearsal · the founding ASTRA blind-review (prompt
    preserved; Astra now public, answerable). Operator decision pending: say
    "go trunk" and windows serve Sep-20.
15. Junction `training/` policy (mirror vs duplicate) - operator decision.
16. Netlify deploy auth + Discord token rotation - whenever.

## Law of the day (from this audit)

Transport deaths masquerading as verdicts was found TWICE now (cycle_elder trail
lying on 429 days; build lane counting 404s as rejections). Standing rule going
forward: **every trail that records a verdict must distinguish reached-the-gate
from died-in-transit.** Instruments that cannot make that distinction file no
verdict at all.
