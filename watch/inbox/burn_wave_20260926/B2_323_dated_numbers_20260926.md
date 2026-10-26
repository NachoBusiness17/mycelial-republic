# B2-323 Dated-number policy for game-module lore (2026-09-26)

## Verdict

LANDED. The module now has one dated-number rule and a mechanical tripwire that enforces it. Rule (spec in tools/game_module_dated_numbers.py docstring): any lore string asserting a NUMBER ABOUT THE REAL ESTATE (thousands-grouped counts, GB/MB sizes, dollar amounts, commit/test/file counts) must carry its as-of date IN THE SAME STRING; pure in-fiction numbers are exempt. Tripwire: tools/game_module_dated_numbers.py (NEW) walks every string of every memory/game_modules/*.json, flags real-estate-shaped numbers in strings with no date marker (ISO date, "as of", "census", "dated"), skips file:line references (docker-compose.yml:153,191,242 is a pointer, not a count - the line-reference guard was added after the first live run flagged exactly that false positive), exits 1 with one human line per finding. Full loop demonstrated live: first run flagged 16 bare numbers in audit_dungeon.v1.json (rc 1, exactly the brief's disease class: 665,131 atrium, 30,000 ledger-known, 713MB board, 9.8MB slice, 42MB suno, 3.6MB/4MB shelves, 102,759 + 3.2GB mine shaft, 1.6GB/75,515 git vault, 156MB/42,249 annex context); the in-string fixes were applied per the convention ("(as of 2026-09-14)" beside each number, 10 edit sites); rerun is clean across all 8 modules (rc 0). The falsifier held during the gap: between the first and second run the tripwire flagged the still-bare numbers this policy had not yet dated, which is the filing-itself behavior the brief demanded.

## Evidence

- tools/game_module_dated_numbers.py (NEW): docstring rule with cause chain (B2-214 librarian fix, B2-69 denominator law, this brief); NUMBER_RE (thousands-grouped, sizes, dollar, commit counts); DATE_MARK_RE; the line-reference guard (match preceded by ":"); exit 1 on findings
- First live run output (this lane, before fixes): "audit_dungeon.v1.json: 16 bare number(s)..." with the per-finding paths (rooms/atrium/name 665,131; rooms/atrium/desc 30,000 + 665,131; dashboard_gallery 9.8MB x2 + 42MB + 713MB + 3.6MB + 4MB; mine_shaft 102,759 + 3.2GB x2; git_vault 1.6GB + 75,515; deploy_graveyard 153,191,242 later reclassified as a line reference), rc=1
- memory/game_modules/audit_dungeon.v1.json (edited, 10 in-string fixes): each flagged number now carries "(as of 2026-09-14)" or an equivalent dated clause in the same string; fiction untouched (only parenthetical dates added); the file was already working-tree-modified before this lane (game content edits by earlier lanes), so the lane's delta is the date markers only
- Final live run: all 8 modules "clean", rc=0
- B2_69_test_census_20260926.md + B2_214_dungeon_census_20260926.md (the fossil precedents named by the brief)

## Work done

Inspected the module structure (rooms/hooks strings carrying the audited census numbers, dates only in title/license_note), designed the rule with an explicit real-estate shape so pure fiction stays exempt, and wrote the tripwire as a standalone tool with --module arg or full-sweep default. First live run reproduced the brief's disease exactly (16 findings). Applied the fix convention to the module (10 surgical in-string date insertions, no fiction rewording), caught the tool's one false-positive class on the way (file:line references look like thousands groups; added the colon guard with the live case named), and drove the sweep to clean rc=0 across all 8 game modules. The line-reference guard decision is recorded in the receipt so a future reader knows the 153,191,242 hit was adjudicated, not missed.

## Falsifier

From repo root: `.venv/Scripts/python.exe tools/game_module_dated_numbers.py` must print clean and exit 0 while the modules stand; after any future module edit that adds an undated real-estate number, the same command must exit 1 naming the path and number (add one in a scratch copy to watch it fire). The colon guard is falsifiable: if a genuine count is ever written in a colon-adjacent position it will be skipped; the run output counts stay visible in the receipt. The policy itself (in-string dates) is falsifiable exactly as the 1,341 headline was: a future receipt citing "665,131 files" from the module without a date marker shows the fix fossilized anyway, which would justify upgrading the tripwire to WARN-ONLY pre-push enforcement (the B2-215 pattern).

## Bibliography closed

memory/game_modules/audit_dungeon.v1.json (read in full, edited: 10 in-string date markers, zero fiction changes); tools/game_module_dated_numbers.py (NEW); mag/game_campaign.py (read: loader permissive json.loads, additive metadata safe); memory/game_modules/*.json other 7 (swept clean, unchanged); watch/inbox/burn_wave_20260926/B2_214_dungeon_census_20260926.md + B2_69_test_census_20260926.md (fossil precedents, read via brief pointers); QUEUE.md (row note); memory/burns/LEDGER.jsonl (appended); watch/inbox/burn_wave_20260926/B2_323_dated_numbers_20260926.md (this receipt).
