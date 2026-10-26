# BURN receipt: third-way-game, 2026-09-26

## Verdict
steal

## Evidence
- "Boon drafts. Level up and the game pauses: three cards, three gods, press 1/2/3. Twelve boons - chain lightning, knockback, wider torch, crits, death clouds, speed, longer SUPERHOT, lifesteal, thorns, berserker, wide arc, roll-refresh." (FROM_MUD_TO_WOW_20260914.md)
- Why the stub defines every field explicitly: "The boon filter is dead code. `!b.max` is always true because no boon defines `max`" (same file). Undefined fields silently disable gates.
- "Billy never vows; he drifts, and his serenity is acceptance, not faith." (STORYTELLER_SIX_RACTOR_20260925.md) - source of the vow-eligibility rule.
- "The Vow system is the small-lies gym: players train belief on boon drafts before anything larger asks for it." (same file, Turtle chair)
- "Zagreus' Attack, Special, Cast, Dash, and Call abilities have one boon slot, and cannot hold multiple ability boons." (Hades Wiki, Boons, fetched 2026-09-26). Same page sells boons for run currency at Charon's shop: precedent for vm_cost.
- WebFetch on the Hades wiki returned HTTP 403; the page was read via the web reader fallback. Read, not synthesized.

## Steal or Vacuous
Steal. Two stubs landed, advancing paper to data shape:

1. watch/inbox/THIRD_WAY_BOONS_STUB.json - all twelve MUD boons extended with Third Way fields (id, name, god_face, tier, vm_cost, vow_eligible, vow_multiplier, seed_locked). Design decisions: (a) Unstuck-face boons (crits, longer_superhot) are vow_eligible=false on canon: Billy never vows; (b) roll_refresh is the only seed_locked=false boon, its peeked variant being the Finite Improbability Generator, which burns its users; (c) the Inefficiency Law (F6) encoded as arithmetic: vow_multiplier capped at 1.5 while Vow price is 2x vm_cost, so pledged power per VM is strictly worse than plain picks; (d) two boons per god_face, census block included so the stub is self-checking.
2. watch/inbox/THIRD_WAY_VOW_LOG_SCHEMA.json - JSON Schema (draft 2020-12) locking the exact playtest line fields (event, seat, t, vow, price, improbable_spent, seed_mode), additionalProperties=false, vow ids constrained to the boon stub, Unstuck ids documented as never valid. The GRACE line schema is named owed, not fabricated.

Web validation: Hades gates special boons on prerequisites and constrains drafts by slot exclusivity; the Third Way constrains by price and seed lock instead, fitting a design whose thesis is that faith must not be optimizable. Prerequisite gating backs the vow_eligible field as genre-standard.

## Falsifier
Pre-registered, F8-pledge-inefficiency: in two seed-matched 20-minute runs, if a vowed build's net VM beats the best unvowed build's net VM by more than 15 percent, the stub constants (vow_multiplier 1.5, price 2x vm_cost) are re-priced before expansion. Conformance gate: any VOW-TAKEN line failing the schema, or any vow on crits or longer_superhot, voids that run's ledger row. Census check: 12 boons, 10 vow-eligible, 1 seed-unlocked; drift voids the stub.

## Bibliography
- watch/inbox/STORYTELLER_SIX_RACTOR_20260925.md (read)
- watch/inbox/BURN_third-way-game_20260925.md (read)
- corpus/game_estate/FROM_MUD_TO_WOW_20260914.md (read)
- https://hades.fandom.com/wiki/Boons (read 2026-09-26; WebFetch 403, reader fallback)
- Web search run 2026-09-26. The "Solving RNG Abuse in Roguelikes" result (gamedeveloper.com) appeared in the search summary but was never fetched: OWED, not cited. Search-layer summaries naming bare-domain sources were treated as unread and uncited.

## Addendum 2026-09-26 (_b): GRACE schema-consistency rule

The GRACE line schema named owed above is landed as watch/inbox/THIRD_WAY_GRACE_SCHEMA.json (draft 2020-12, additionalProperties=false; fields: seat, t, pair_id, seed_hash, mode, improbable_spent, roll_total, outcome, grace_pool_id; all required). Rule: peeked and unpeeked rolls MUST log identical field sets; the seed audit compares distributions across the shared fields only. seed_hash carries the sha256 of the session seed, never the seed itself; both legs of a pair share one seed_hash and one pair_id.
