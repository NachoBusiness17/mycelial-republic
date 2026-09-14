# L3 Pack Review — 2026-09-01 (game-designer charter)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: of 7 L3 packs, 3 RATIFY / 4 REVISE / 0 REJECT, all PUBLIC-SAFE with full determinacy and seeded-external RNG discipline — SUPPORTED (per-pack rule-check table with named, specific defects) · falsifier: a RATIFIED pack failing verifier enforcement, or a REVISE defect absent on re-read

Role: L3 pack review. Reviewed 7 `L3_packs/*.DRAFT.md` against the charter: (1) COMPLETE
(verifier-enforceable rules), (2) VERIFIER-COMPATIBLE (deterministic state, legal-move fn
derivable), (3) PUBLIC-SAFE (one-way mirror — no personal content), (4) HISTORICAL accuracy.
All 7 pass PUBLIC-SAFE (zero personal content). Full determinacy and RNG discipline hold
everywhere (seeded-external, never LLM-improvised).

## Per-pack table

| Pack | COMP | VERIF | HIST | Verdict | Reason |
|---|---|---|---|---|---|
| **oware** | ✓ | ✓ | ✓ | **RATIFY** | Honest non-engine boundary-exception. Sowing is not race_dice; pack states the refusal and maps cleanly (12 pits, feeding rule, 2/3-chain capture, win≥25). Fully deterministic — legality fn derivable. Note: mis-filed under race_dice; should spawn its own `L1 sowing_capture` engine. |
| **patolli** | ✓ | ✓ | ✓ | **RATIFY** | Self-contained & concrete: 52 indices, 5 marked beans, entry on 1/5, capture on, safe junction+arm-bases, roll-exact all-piece win. Durán/Sahagún/Culin/Murray cited, schools named, 1569 ban carried as history-not-rule. Strong. |
| **snakes_ladders** | ✓ | ✓ | ✓ | **RATIFY** | Concrete: 100 sq [0..99], single seeded 1d6, land-exact clamp→99, full ladder/chute bindings listed. One-token-per-player win clear from build prompt (minor wording tension in "all pieces enter at 0"). Gyan-chaupar origin + 1892 commercialization handled accurately. |
| **senet** | ✗ | ✗ | ✓ | **REVISE** | Historical handling is exemplary (Kendall vs Piccione, reconstructed). BUT rule delta is self-contradictory: MOVEMENT says `min(current+roll,29)` (a clamp) yet claims land-exact clamp is NOT used and overshoot "passes through" — impossible to reconcile. Bear-off mechanism undefined (no path off square 29). ENTRY hedged ("commonly any roll"), hazard-square location school-dependent. Verifier cannot resolve. |
| **senet.gptoss** | ✗ | ✗ | ✓ | **REVISE** | Compact derivative. Drops bear-off semantics entirely, no overshoot/land-exact handling, entry "any exact roll" is vague, and it collapses the two schools into "debated." Four-stick 0–4 spread is a useful delta but already listed as a main-senet variant. Less complete than main senet. |
| **pachisi** | ✗ | ~ | ✓ | **REVISE** | Capture/safe/hub/entry all well-specified, Fatehpur Sikri sensitivity good. BUT pack constants are unbound: entry-qualifying `Q`, lap count `LAPS`, and cowrie count (6 "common; others per region") are never assigned defaults, and "counts arrive seeded-external" is hand-wavy. Legal-move fn under-specified until constants are pinned in the default build. |
| **ur** | ~ | ~ | ✓ | **REVISE** (light) | Strong (Finkel BM 33333, attested/reconstructed split, 2400-yr gap honesty). Near-ratify; only defect is the SQEFFECT table lists the two "shared crossing" rosette squares without indices, and base single-track vs short/long route is slightly loose. Pin the two crossing-square indices and it ratifies. |

**Counts:** RATIFY 3 · REVISE 4 · REJECT 0.

## Senet vs Senet.gptoss — verdict

**Winner: `senet` (main).** It is the more complete and historically rigorous pack: it carries the
Kendall/Piccione two-school delta, a defined jump-to-afterlife-exit passage, concrete materials and
five named variants. `senet.gptoss` is a thinner derivative that omits bear-off and overshoot
semantics and flattens the two contested readings into a single "debated" flag. gptoss's one
genuine addition — the four-stick (0–4) spread — is already listed as a main-senet variant. So
main wins but is itself not yet solid (see its REVISE).

## Next steps

- **ratify (oware, patolli, snakes_ladders):** lock status; add to L3 registry; wire to L2 statics game-ids.
- **senet / senet.gptoss:** resolve the min+clamp-vs-land-exact contradiction and define the bear-off
  operator explicitly; pick ONE entry rule and pin the hazard square per a stated school. Then fold the
  merged better-senet (keep gptoss four-stick as a listed variant) into ratify.
- **pachisi:** assign concrete defaults for `Q`, `LAPS`, and cowrie count in the active build so a
  verifier can construct the legal-move function.
- **ur:** pin the two shared-crossing rosette indices; then re-verdict to ratify.
- **oware (process):** file a corpus ticket to spawn a `L1_engines/sowing_capture` engine so Oware/Bao
  stop living awkwardly inside race_dice.
