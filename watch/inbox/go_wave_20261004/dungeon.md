# GO item 4 - dungeon campaign (lane a02-dungeon-campaign), receipt

Executed: 2026-10-04, one seat, one sitting. Fold: `corpus/steal/MASTER_MICKEY17_V2.md` section 9, GO item 4 (rows a02#0/#1/#2/#3/#4). Lane evidence: `memory/runs/mickey17_v2/runs/run-0/lanes/a02-dungeon-campaign.json` (all 5 rows read; refire of 2026-10-03T21:45Z). Code pinned at start: HEAD a7ca49be1da8, tree clean on tools/dungeon.py except an additive sibling-lane block in `main()` (fire-atomic bank, GO item 6, lines 597-618) - untouched by this lane, no conflicts.

All line anchors below are the working tree after this wave (tools/dungeon.py, 756 lines); the lane rows' anchors (496/515/448-455) were pinned to HEAD 37e2fba7e and are re-pinned here.

## Sub-item 1 - Parser fix + 14-verdict replay tests (a02#0)

- Cause: `strip_and_cap` flattens every speech to ONE line; the old verdict scan (dungeon.py:488-491 at 37e2fba7e) read only line-initial bracket lines, so the 14 logged S4 PC speeches parsed tagless and the S4 disjunct at :496 (`verb == "ATTACK" and obj in enemy["actor"] or (scene == "S4" and obj == "wyrm")` - precedence made the wyrm test verb-independent) resolved all 14 as wyrm ATTACKs; the `[AUDIT root]` win path was unreachable as played.
- Fix: `extract_tag()` at dungeon.py:114 (regex tag search across the capped speech, last tag wins, first token must be pure letters so inline dice notes like `[d20=18...]` stay untagged), wired into both graders (`_verdict` at :238 for S1, `_grade` at :550 for the campaign); the S4 disjunct is now parenthesized under the ATTACK verb (dungeon.py:565).
- The campaign grading was extracted verbatim from the loop body into `Dungeon._grade()` (:550) so tests replay the same bytes the carrier grades with.
- Tests: `tests/test_dungeon_parser.py` (new, 13 tests) embeds the 14 S4 PC rows verbatim from `watch/inbox/playground/dnd0_20261003T202213Z/transcript.jsonl` (log path alive; nothing reconstructed).

**14-verdict replay numbers** (test `test_replay_14_logged_s4_verdicts_under_fixed_parser`, dry Dungeon, tip = genesis, starting board as played: ehp 30, live carried scrolls):
- Dice law: 14/14 roll(roll_committed) == roll_value.
- Tag extraction: legacy scan 0/10 tagged speeches (the 11th non-void speech, deepseek turn 16, genuinely carries no tag - the seat stepped back); regex 10/10; 3 voided grok speeches tagless under both readers.
- Graded verdicts: 7 AUDIT / 4 RP / 2 ATTACK (both MISS) / 1 CHECK; AUDIT branch reached 7/14 (0/14 as played); ehp unchanged at 30 (no true hit lands under the real tags - the "wyrm at 0" board the seats argued over was itself a collapse artifact).
- Versus logged: 12/14 logged verdicts were collapse artifacts; 2/14 coincide (rows 3 and 5: deepseek turn 4, saelis turn 7 - speeches that really end in an ATTACK tag that missed). The chatgpt turn-3 audit burns Vault Deed B (`audited-PHANTOM`).
- Regression guards: no beat grades HIT/MISS unless its own tag is ATTACK; all 14 logged verdicts are wyrm-attack verdicts (the collapse signature).

## Sub-item 2 - Per-turn heal + audit-burn (a02#1)

- `Dungeon._wyrm_regrowth()` (dungeon.py:519): at the start of each S4 Wyrm turn, ehp += 5 per PHANTOM scroll still unaudited in any pack, verdict note ` REGROWTH +N (k unaudited PHANTOM)`; called from the campaign enemy branch (:644). Audited phantoms (`audited-*`) stop feeding.
- Audit-burn via `_find_scroll()` (:496): case-folded scroll lookup across per-PC packs - the old `obj in carried` test executed dead (`'vault deed b' in carried -> False`, mixed-case keys vs lowercased obj). A successful scroll audit now actually flips the scroll to `audited-*` (:588-591), which also starves the regrowth.

## Sub-item 3 - Case-fold the dungeon.py:515 lookup (a02#1 half)

- Landed as `_find_scroll` above; unit-proven in `test_casefold_audit_burns_phantom` (saelis at genesis:S4:13 rolls 17; `[AUDIT VAULT DEED B]` burns the mixed-case key; the raw lowercase membership test that ran dead is asserted as a regression guard).

## Sub-item 4 - Wipe gate on prior verdict, per-PC packs (a02#2)

- Spec byte: DND_module.md:74 - wipe on a HIT against a PC whose previous verdict was FAIL, MISS, or FUMBLE, dropping that PC's unaudited scrolls.
- `carried` (party-wide dict) replaced by per-PC `packs: dict[owner -> dict[scroll -> state]]`; S1/scene loot rides the first living PC in initiative order (module assigns loot to the party, not a name; per-PC packs need an owner - deterministic, re-derived at each scene close).
- `Dungeon._beat_outcome()` (:483) reduces a verdict to its outcome token; `Dungeon._mimic_wipe()` (:533) gates the drop on `self.last_verdict[target]` (per-PC, set after each campaign PC beat) and drops only that PC's `PHANTOM` scrolls. Off-spec live behavior cited in the helper docstring: transcript row 25 chatgpt `RP (d20=4)` -> row 28 `MIMIC HIT chatgpt for 16 WIPE: chatgpt drops ['Timestamp Scroll'] (gone forever)` (bytes re-verified this pass).
- Tests: `test_wipe_gated_on_target_prior_verdict` (RP prior holds the gate - the live-run bug shape; FAIL/MISS open it; another PC's MISS opens nothing; REAL scrolls survive; no prior beat opens nothing).

## Sub-item 5 - finish_reason per call, voided readbacks in DONE (a02#4)

- `_paid` (dungeon.py:218-231): every banked usage row now carries `"finish_reason": finish`; voided calls increment `voided_calls`, and DM-model voids increment `voided_readbacks` (counters init at dungeon.py:169-170). Both s1 DONE (:427-429) and campaign DONE (:707-709) write `voided_readbacks` + `voided_calls`.
- Run-202213Z baseline the fix answers to: 40/50 dm_response rows voided, all 39 PC readbacks (erratum receipt below).
- Scope note: the de-glob retry leg named in fold action a02#3 (retry the DM call on a prompt that does not quote the actor's combat speech) is NOT landed - it is outside this lane's six sub-items; the existing 3-attempt retry still resends the identical prompt. Filed open.

## Sub-item 6 - Run-202213Z carrier-failure erratum (a02#3)

- Filed: `watch/inbox/playground/dnd0_20261003T202213Z_ERRATUM.md` (cause in 5 numbered legs, rerunnable evidence commands, per-claim falsifiers, disposition). Verdict stance: PARTIAL stands as a label; mechanics off-spec; audit VOID per the module's own falsifier (dice_audit exit 1, verdict flags 50/50 rows); DM channel 40/50 voided.

## Tests (instrument and numbers)

- `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py -q -p no:cacheprovider` -> **15 passed in 1.08s** (13 new + 2 existing burn-id tests; the only other importer of tools/dungeon.py).
- New file: tests/test_dungeon_parser.py (13 tests: dice law 14/14; legacy-scan blindness 0/10 vs regex 10/10; all-logged-verdicts-were-attacks signature; the 14-verdict replay; verb-gated S4 disjunct; extract_tag units; case-fold burn; regrowth arithmetic; beat-outcome tokens; wipe gate; S1 embedded-tag verdict; finish_reason bank + void census; campaign DONE integration with per-row dice-law recheck).
- Dry smoke of the carrier (PLAY_DIR redirected to a temp dir; no playground writes): `.venv/Scripts/python.exe` with `dg.PLAY_DIR = tmpdir; dg.main(['--tip', GENESIS, '--dry'])` -> exit 0, verdict `GATE OPENED (audited) ... WON-S1`, DONE keys include `voided_readbacks`/`voided_calls`.
- Fixture integrity: the 14 embedded speeches are byte-copies of the transcript rows (asserted em-dash-free; strip_and_cap had already normalized them in the live run).

## Files touched

- `tools/dungeon.py` (modified: extract_tag + TAG_RE; _verdict scan swap; _paid finish_reason + void counters; s1 DONE census; campaign rewritten onto packs/_grade/_mimic_wipe/_wyrm_regrowth/_find_scroll/_beat_outcome; new law comments carry cause + evidence). 756 lines total.
- `tests/test_dungeon_parser.py` (new).
- `watch/inbox/playground/dnd0_20261003T202213Z_ERRATUM.md` (new; the only playground write).
- `watch/inbox/go_wave_20261004/dungeon.md` (this receipt).
- Not touched: mag/route_chat.py and the rest of the tree despite heavy sibling-lane concurrency; no git commit (coordinator commits).

## Blockers and registered debt

1. **Ratchet NEW debt (blocks pre-push until accepted or split):** `python tools/violation_ratchet.py check --changed` -> FAIL with NEW `af1d7045681fee89 file-too-long: tools/dungeon.py:756 - >400 lines` (this wave grew the file from 627 to 756; the campaign engine is now the split candidate). Accept by name (`baseline-update --by <operator>`) or split the S2-S4 engine into its own module - operator call, not loosened by this lane. The ratchet's other NEW hit (`a40c890ec362879e except-pass: mag/route_chat.py:174`) belongs to the GO item 1 lane, not this one.
2. **Open leg:** de-globbed DM retry (fold action a02#3), see sub-item 5 scope note.
3. **Sibling concurrency:** GO item 6's fire-atomic bank block landed in `main()` mid-wave (uncommitted, additive); this lane's edits and that block are disjoint and both compile (smoke exit 0 runs through main()).

## Verification commands (rerunnable)

- `git grep -l "dungeon" mag/ tools/` - module chain; the campaign lives in tools/dungeon.py (mag/dungeon_dev.py is a different surface).
- `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py -q -p no:cacheprovider`
- `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
- Census: `.venv/Scripts/python.exe -c "import json; rows=[json.loads(l) for l in open('watch/inbox/playground/dnd0_20261003T202213Z/transcript.jsonl', encoding='utf-8')]; print(sum(1 for r in rows if r.get('dm_response')=='(content_filter: beat voided)'), 'of', len(rows))"` -> `40 of 50`
