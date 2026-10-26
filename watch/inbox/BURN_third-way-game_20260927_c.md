# BURN third-way-game 2026-09-27 (pass c)

## Verdict

steal

## Evidence

Stub (adventure_2d6_stub.v1.json, verbatim): `"resolution": {"dice": "2d6", "pass_on": 7}`; `"player_start"` carries `"hp"`, `"hp_max"`, `"ac"`, `"attack_bonus"`, `"damage"`, `"traits"`, `"inventory": ["walking stick", "waterskin"]` and no currency field anywhere; `"event_tables": {"rest_safe": [...]}`; rooms carry `"exits"`, `"hooks"`, `"encounter"`, `"invariant"`.

Atlas (GAMEDIG_MASTER_ATLAS_20260927.md, verbatim): law 1 "Meta-currency pays out only when a run ends and forfeits on early leave"; law 2 "Interest $1 per $5 held capped at $5"; law 3 "pair-gated drops with named completion payouts (15 Ambrosia for all 28)"; law 4 "Presence-locked production plus a care-debt meter". Ractor (STORYTELLER_SIX_RACTOR_20260925.md): "the Vow costs, the Seed wastes, the Pilgrim sheds loot"; canon "twelve boons including roll-refresh"; "Resolution stays 2d6, pass on 7".

## Steal or Vacuous

Patch spec, one item per adopted law. READ-ONLY today: the stub edit is a later gated build.

1. ATLAS LAW 1, settlement ledger. Add new top-level `"vm_ledger"` (sibling of `"resolution"`): `{"virtue_marks": 0, "settle_on": "run_end", "forfeit_on_early_leave": true, "settlement_text": "so it goes"}`. No existing field modified; the stub has no wallet to migrate. Gated by F8.
2. ATLAS LAW 2, Vow interest. Add inside `"vm_ledger"`: `"vow_interest": {"per": "1 VM per 5 VM held per settled run", "cap": 5}`. The cap is law; the reward half is hostage to F6: a meta-min-maxed Vow yield re-prices to zero. Gated by F6.
3. ATLAS LAW 3, boon codex. Add new top-level `"boon_codex"`: `{"boons": 12, "gods": 3, "pair_gate": "one boon from each of two distinct gods", "completion_payout": "named per-god meter reward"}`. Twelve count from ractor canon. Codex progress persists cross-run by design, so the spec explicitly excludes it from `"vm_ledger"` income: otherwise F8's leak check false-positives on the codex. Gated by F6.
4. ATLAS LAW 4, care-debt meter. Add new top-level `"vm_pool"`: `{"care_debt": 0, "feeding": "presence-locked per session", "neglect": "bleeds pool yield"}`. Gated by F7 plus the F8 dead-meter clause.
Untouched by this patch: `"pass_on": 7` stays (ractor law), `"player_start"`, rooms, `"encounter"`, `"invariant"`. Atlas law 5 stays a build gate on any summon/target mechanic, not a stub field. Web search "2d6 tabletop rpg economy balance design patch 2026": thin. Closest 2026 hit is FAST RPG OSR style (epicsavingthrow.com, Feb 2026, "2d6 +6 for heroic characters" ability scores); no economy-patch design work surfaced. Nothing stealable from the web.

## Falsifier

- Patch 1, F8: fails if any playtester sustains VM income across two consecutive runs without a settling run end.
- Patch 2, F6: fails if a meta makes capped Vow interest dominant; re-price to zero.
- Patch 3, F6: fails if the pair gate does not break single-god drafting lines; F8 carve-out verified at F1.
- Patch 4, F7: endgame abolition must sever `"vm_pool"` and `"care_debt"` for all players; F8: meter never leaves zero in ten sessions means dead meter, cut it.
All checked at F1-F7 review per pass b pre-registration.

## Bibliography

- memory/game_modules/adventure_2d6_stub.v1.json (read whole)
- watch/inbox/BURN_third-way-game_20260927_b.md (read whole)
- watch/inbox/GAMEDIG_MASTER_ATLAS_20260927.md (read whole)
- watch/inbox/STORYTELLER_SIX_RACTOR_20260925.md (read whole)
- WebSearch "2d6 tabletop rpg economy balance design patch 2026", 2026-09-27 (thin; epicsavingthrow.com FAST RPG, Feb 2026)
