# GWAP INDEPENDENT COP - door 1 of the 24-wide dig, landed (2026-10-04)

Operator GO: "do it" on the 24-wide receipt's first build
(watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md, the independent-cop door).

## The defect (three symptoms, one cause)

tools/arena_gwap.py actor_payloads minted BOTH the robber's intent and the
cop's report from the SAME verdict bytes (_firstverb(verdict) on both sides,
same qualifier). The cop copied the fighter's triple by construction, so:

1. agreement was theater - the carrier agreed with itself, no independent
   parse existed
2. every honest 2+-claim session fired the collusion fingerprint (identical
   claim ORDER between "independent" authors): 196 suspected-collusion rows
   in the banked ledger, 188 of them demoting VERIFIED_AGREE to CHALLENGE
3. a silent tavern cop (no judge ruling) banked absence as disagreement:
   3,802 silent vs 282 ruled tavern rows (2026-10-04 census), feeding the GPS
   router fake DISPUTE signal

## The fix (three parts)

1. ADAPTER INDEPENDENCE (tools/arena_gwap.py): intent mints from the
   fighter's pre-roll SPEECH ([CHECK omen] tag -> action family); report
   mints from the dice law's POST-ROLL RECORD (ruling prefix -> action
   family); both bind the same qualifier commit=<roll_committed>. The parses
   are independent: a declared check ruled RP-no-tag now disagrees (the
   model claimed an action the law did not recognize); a declared attack
   ruled MISS still confirms (the law RULED the action - the outcome is the
   law's, not the fighter's claim). engine_version -> arena-*-v3-independent-cop.
2. ENGINE EXEMPTION (mag/gwap_payload.py collusion_fingerprint v1.1):
   identical order between different authors with EVERY qualifier externally
   bound (commit=<hex>: or ruling=) is a ledger confirmation - two
   independent readers of one chronological record - and does not flag.
   Free-form identical phrasing still flags (regression-tested). This is the
   188-row self-flag cure; the fingerprint keeps its teeth for the real
   copy class.
3. SILENT COP = BLOCKED (adapter + engine's existing BLOCKED precedence): a
   tavern actor with zero judge rulings banks one cop claim "copsilent: no
   judge ruling banked this session" against taboo_list ["copsilent"] ->
   taboo violation -> verdict BLOCKED (engine precedence over the score
   ladder). Un-judged speech stops poisoning GPS routing as fake
   disagreement; the reason word rides the payload. Mixed sessions bank
   their ruled rows only. Tavern actor model fallback: the row's own model
   field, fail-closed (mob actors clockwork/mimic/wyrm stay unmapped-skip).

## Instrument deltas, measured on the real tree (2026-10-04)

Banked old ledger (memory/runs/gwap/arena-capability.jsonl, 613 rows, the
append-only record of the old instrument):
  VERIFIED_AGREE 119 | CHALLENGE 204 | DISPUTE 290 | suspected-collusion 196

New instrument over all playground run dirs (529 bankable payloads):
  VERIFIED_AGREE 161 | CHALLENGE 88 | DISPUTE 64 | BLOCKED 216

Reading: the 290 DISPUTes collapse to 64 real ones (the 216 fake empty-cop
classes now BLOCKED honestly); the 204 CHALLENGEs drop to 88 as the self-flags
dissolve; VERIFIED_AGREE rises 119 -> 161 (honest agreements no longer
demoted). The GPS feed built on future banking inherits the honest shape.

## Tests

tests/test_gwap_independent_cop_20261004.py, 9 passed; full gwap surface
regression 65 passed (test_gwap_payload + test_gwap_to_gps + test_gwap_mud +
the new file), 2026-10-04, pytest -q. Coverage: honest session agrees without
self-flag (the 188-cure), independence bites on family mismatch (checked
declared vs attacked/spoke ruled -> DISPUTE), NOROLL voids disagree,
free-form identical order still flags (exemption is narrow), commit-bound
identical order exempt, silent cop BLOCKED with copsilent violation, ruled
tavern agrees, mixed tavern banks ruled only, decide_verdict two-argument
regression unchanged.

## Scope and follow-ups

The 613 old rows stay banked (append-only law; they are the record of the
old instrument's behavior). Historical re-grade = bank fresh v3 payloads
under new scene ids - an operator decision because it changes GPS ledger
totals. The GPS feed door: the next --backfill of NEW run dirs banks v3.
Mob actors (clockwork/mimic/wyrm) are carrier-side creatures, correctly
unmapped - if they should route, name their models in DUNGEON_ACTOR_MODEL.

Next doors in the receipt's build order: arena-bench CI tripwire (1-2h),
clippy-as-prober (2-4h), night-cycle checkpoint legs (2-4h).

Writer: zcode-53-strategy-window
fetched: 2026-10-04
