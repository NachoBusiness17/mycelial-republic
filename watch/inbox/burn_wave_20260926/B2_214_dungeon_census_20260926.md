# B2-214 dungeon lore census fossil (2026-09-26)

## Verdict

landed. memory/game_modules/audit_dungeon.v1.json:147 no longer recites the retired "1,341 tests across 264 files; 34 shelves currently fail" as live truth: the librarian line now carries the 2026-09-26 census (1,910 tests collected / 303 files, `pytest --collect-only -q`) with the retired 1,341 kept as a labeled in-world exhibit, and the room's lying-number hook was rewritten against current AGENTS.md:27 bytes it had fossilized. Both options the brief allowed were used at once: flavor updated AND the old count marked in-world history.

## Evidence

- AGENTS.md:27 current bytes: "1,910 tests collected / 303 files (2026-09-26 census, `pytest --collect-only -q`" with the retirement clause naming the 1,341 headline hand-copied, never byte-backed (the 09-14 trio 1305 passed / 34 failed / 9 skipped sums to 1,348).
- This lane's fresh re-take the same day: `./.venv/Scripts/python.exe -m pytest --collect-only -q` tail "1914 tests collected in 2.72s", exit clean, 303 unique files under `tests/`, no collection errors. Delta vs the carrier reading is +4, consistent with tests landing mid-wave between the carrier's refresh moment and this lane's moment (the same-day movement the B2-216 denominator law names); this lane did not attribute the 4 individually. Both numbers are dated snapshots with the instrument named; no differencing is claimed.
- The day's executed counts stay the property of their own receipts, cited not recomputed: B2_34_cluster_detectors_20260926.md:22 "38 failed / 1728 passed / 9 skipped / 1 error"; B2_51_autorun_autopsy_20260926.md:22 "1734 passed / 38 failed / 9 skipped / 1 error". The dungeon card carries the collected census, never an executed sum.
- The QUEUE card text (burn_wave_20260926/QUEUE.md:63) suggested "1,837 collected / 301 files, 38 failing files"; bytes moved past it (carrier 1,910/303, lane re-take 1,914/303). Per the brief, AGENTS.md:27 current bytes win; the card's older figures were treated as its writing moment, not as today's truth.
- The room's hook "The lying number: AGENTS.md:27 claims 39 deterministic green" had gone byte-false against current AGENTS.md:27, which makes no such claim anymore; the hook now names the retirement and carries this receipt's path. The neighboring "parked lie" hook is left as history: current AGENTS.md still reads "dispatch log active 2026-09-09, $220 armed", so its premise still matches bytes.
- Post-edit checks: JSON parses (10 rooms); edited lines 147 and 157 carry no raw em-dash character and no unicode-escaped em-dash sequence; the 17 other escape-bearing lines in the module are untouched history, left as-is per the B2-69 precedent.

## Work done

1. Read the target module whole, plus the pointer receipt B2_69, the QUEUE.md law header block, and AGENTS.md:27.
2. Re-ran the census twice (collected count, then unique-file count); 1,914 / 303, clean exits.
3. Checked the shared-file claim law: the dungeon JSON is git-tracked and clean, so no claim attaches to it; QUEUE.md is working-tree-modified and shared, so a CLAIM line was appended before its edits and retired CLAIMED in the same write per the B2-257 pattern, after a fresh re-read of the target lines.
4. Edited the two lines with anchored unique-string replacements (desc line 147, lying-number hook line 157); validated JSON parse and the em-dash law on both.
5. Wrote this receipt, appended the LEDGER row via venv python json.dumps, registered this receipt via `node scripts/index_fold_host.mjs add` (writer b2-214-dungeon-census), then ran `mag.shared_surface validate`. Defect and repair, disclosed: the first register (seq 1789823567015749482) passed a `watch/inbox/`-prefixed path, which the fold's OUTSIDE_RE drops as outside, so it never reached INDEX items (the same poison class as the 239 pre-existing watch/ events, but fresh, so repaired in-lane); the poisoned event was invalidated and the receipt re-registered with the absolute host root, the exact form the B2-157 normalizer strips to the bare inbox-relative path.
6. Self-fed B2-323 (dated-number policy for module lore) and B2-324 (sibling-module retired-headline sweep) under Open, unchecked; first drafted as B2-316 and B2-317, both numbers taken by concurrent self-feeds mid-lane, renumbered highest+1 at append time per the B2-167 law.
7. Checkbox note: QUEUE.md:63 was found already pre-checked [x] with no landing receipt on disk (the B2-238 disease, same as the B2-252 row's opening state); this landing earns the check per that precedent, noted on the card.

## Falsifier

Re-run `./.venv/Scripts/python.exe -m pytest --collect-only -q` on any later day: it will read higher than 1,914 as tests land, and that is fine, because the card's claim is pinned to its moment by date and instrument. The failure modes are exact: the dungeon card again becomes the only place a test count lives; the sentence loses its date or its instrument; or a future editor restores live-tense to the 1,341 exhibit. Grep audit_dungeon.v1.json for "1,341": it must appear only inside the labeled exhibit clause, never as present tense.

## Bibliography closed

memory/game_modules/audit_dungeon.v1.json:147,157; AGENTS.md:27; watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md; watch/inbox/burn_wave_20260926/B2_34_cluster_detectors_20260926.md:22; watch/inbox/burn_wave_20260926/B2_51_autorun_autopsy_20260926.md:22; watch/inbox/burn_wave_20260926/QUEUE.md (header law block, B2-214 row, B2-257 claim pattern, B2-252 precedent); watch/inbox/LIVING_HASH_LAW_20260926.md (open-shape registration); memory/burns/LEDGER.jsonl.
