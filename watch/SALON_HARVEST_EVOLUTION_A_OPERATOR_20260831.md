# SALON_HARVEST_EVOLUTION_A_OPERATOR_20260831.md — Lane A (Operator-Prior)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: banger-first fixed-skeleton digest with a 72h repetition cap cuts noise at ~zero cost — UNPROVEN (format proposals with meters defined, none measured in card) · falsifier: digest==scrub, the card's own stated failure signal — 3 consecutive runs with zero non-trivial BANGER items

1. **Open with the one banger, ≤3 lines, before anything else.** Top of digest = single HOT/map-mover item (weights drop, price/rate change, SOTA claim) with link + 1-line why-it-matters. Separate "rest of digest" below in ≤9 lines. Change: restructuring output; meter: open-rate = % of runs where the banger item is non-trivial (not a re-feed); cost: 0 (format only).

2. **Fixed digest skeleton (never changes shape).** Three labeled blocks every single time: `BANGER / OWN·STEAL / WATCH`. Same block order, same labels. Noise and repetition come from surprise, not content. Change: prose-free template; meter: scroll-rate — count of runs where operator opens but reads <3 blocks, tracked as comment on digest; cost: 0.

3. **Repetition cap: 1 mention per item per 72h.** If a launch/watch item repeats, drop the third+ occurrence regardless of value. Change: dedupe of repeat-worthy items, not just link-dedupe; meter: repetition flag = % of digest lines that appeared in prior-2 runs; cost: 0.

4. **Own-surface first, watch last — always.** Steal set only after own/grounding wave; watch lane is the weakest signal, so it's the bottom block and capped at 3 lines. Change: hard lane ordering + cap; meter: lane-density = avg lines own vs watch; cost: 0.

5. **Missing-banger signal (THE failure to watch): `digest == scrub`** — 3 consecutive runs with zero non-trivial BANGER items (all re-feeds/watches). Triggers one corrective: reorder triage to probe watch lane deeper next run instead of repeating fails. Change: proactive fallback rule; meter: banger-quality = # new (non-dedupe) banger items/run, logged; cost: 1 line in cron state.
LINEAGE: recognized from rib_bus territory 5a7c9e1b3d0f2a44 + territory b38f7324577c469e + monitor mo02ribdebug0002 — evolve ladder; gate gates, does not abolish; health over time (annotated 2026-08-31 per SALON_BUS_A)
LINEAGE: recognized from rib_bus standing-novelty-wave-trickster cba1014aa20d24fa — continuous NOVELTY injection, never stagnate; anti-stagnation (annotated 2026-08-31 per SALON_BUS_A)
