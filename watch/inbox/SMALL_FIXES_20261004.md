# SMALL FIXES 2026-10-04 (operator-approved 06:52 ET)

Grok Bot, Sun 10/4 06:52 to ~07:15 ET, DESKTOP-7C70KSC. Nothing committed. No .env read. Edits backed up as .bak-20261004.
Not touched: janitor, ghost, health, verkle writers, Startup scripts, AGENTS.md.
Self-steal: tools/rotate_kpi.py (HYGIENE_WAVE_20261003.md). The slow-test diagnosis comes from watch/inbox/reboot_patches_20261003/APPLY_ORDER.md ("Hung test at 44 pct").

## 1. kpi.jsonl rotated (real run)
- Writer: mag/records.py:138 write_kpi. It is called on demand by summarize / board / operator-os / pack-status / backfill. It is not a dedicated loop. Live loops seen: ghost cycle, governor_autorun, stealth driver, hermes_burn.
- Pre-checks at 06:56 ET:
  - last write 10/3 23:08 ET, so the file had been quiet for about 8h
  - an exclusive open succeeded, so no process held it open
  - 24,558 rows
- Ran `tools/rotate_kpi.py --apply` (copy, verify, truncate; rows appended mid-run would have been preserved):
  - archive: attic/kpi/kpi_2026-09-07_2026-10-03_20261004T105614Z.jsonl.gz, 23,558 rows, 132,922,695 B, sha256 e39375a9...e98f3b
  - live file: 1,000 rows, 17,637,997 B (was 791,586,916)
- Independent read-back (separate script):
  - gzip opens and every row parses as JSON (0 bad)
  - 23,558 + 1,000 = 24,558, which equals the original row count
  - order holds: last archived row 2026-10-03T05:29:12Z, first live row 05:30:05Z
- Correction: the dry run estimated the gzip at about 7 MB from a 32 MB sample. The real size is 133 MB (ratio 0.17). The early rows compress far better than the later ones.
- synthesis_agent.py: `_last_jsonl` now reads backwards from the end of the file in growing blocks instead of read_text() on the whole file. It is the same function and gives the same result. Checks:
  - kpi last row returned in 0.001 s
  - MAG_JSONL ok; n=3, n>rows, missing and empty files all behave as before
  - tests/test_source_trace.py 9 passed
- Real diff is 25+/9- lines. Plain `git diff` shows the whole file because the working copy was already CRLF over an LF index before this edit (bak bytes != HEAD bytes, CR only).

## 2. memory/improve/SEATS.md: NOT recompiled (no compiler exists)
- rg over mag/, tools/, scripts/, configs/ and .zcode/workflows finds readers only: mag/ask.py:91, mag/launch_pad.py:33, mag/token_economy.py:36, configs/modules.yaml:197.
- configs/fossil_registry.json:43 lists it as disposition "recompile", bar 168h, with no recompile_cmd. The note says "refreshed 2026-09-27 by the are-inventory lane", meaning a hand or lane edit. Last commit was d15bc960d.
- tools/fossil_check.py check (06:5x ET): `WARN memory/improve/SEATS.md stale - 177.0h > bar 168h`. That is the only WARN, so rc=1. The stealth driver's fossil route (tools/stealth_driver.py:822 t_fossil) would report rc=1 until SEATS.md is younger than 168h.
- Not done on purpose:
  - touching the mtime: that would fake the freshness check
  - rewriting a load-first boot doc on my own: the content is stale too ("Hermes = parked" while hermes_burn runs; the Lite lane was pulled 10/3)
- Options: an operator-named content refresh, or add a recompile_cmd once a compiler exists.

## 3. test_improve_cycle_schema marked slow
- rg found no existing slow-marker convention: no mark.slow anywhere, and pytest.ini and both conftests have no markers.
- Added `@pytest.mark.slow`, with a one-line cause comment, to tests/test_improve_loop.py, and registered the marker in pytest.ini. Test logic unchanged.
- Note: a slow mark does not skip by default. Full-suite runs need `-m "not slow"`.
- Verified: `-m "not slow"` gives 1 passed, 1 deselected; `-m slow` collects exactly that test.

## 4. census_patrol_daily.ps1 in a7ca49be1
- Stats:
  - `git diff --stat`: 389 lines (194+/195-)
  - `-w --stat` and `--ignore-cr-at-eol --stat`: 3 lines (1+/2-)
- The whole-file churn is line endings. The parent blob is LF (195 lines), the commit blob is CRLF (194 lines). `ls-files --eol`: i/crlf, the only CRLF .ps1 in the index (49 others are LF). core.autocrlf=false. .gitattributes covers only *.rbxlx / *.rbxm.
- The 3 real lines are a genuine fix: the here-string tail `"@` plus a stray `-Encoding utf8` on its own line became `"@ -Encoding utf8`.
- .gitattributes left unchanged on purpose: a `*.ps1 text` or `* text=auto` rule is not tiny in effect, since it renormalizes on the next add and flags CRLF files at once. Cleaner path: re-add this one file as LF in a normal commit (operator).
- Same drift class: synthesis_agent.py (item 1).

## 5. Arm C in plain English
Arm C is one leg of a replication of a published "interference search" result: it keeps their puzzle search loop but swaps their small trained judge for a tiny local model (gemma:2b) that scores which puzzle positions look promising. It tests whether a cheap general model can stand in for the purpose-trained judge on 30 Countdown number puzzles. The frozen bar is at least 15 of 30 solved at a 200-state search budget, though the adversarial review noted their search solves all 30 at that budget anyway, so a pass would not prove the judge helps. It stands at 1 of 30: every attempt solved problem 1 and then died or was stopped inside problem 2, a full run needs about 17 hours of uninterrupted box time, and the operator's rerun-vs-retire call is pending (watch/inbox/ARMC_DECISION_MEMO_20261003.md).

## Backups
synthesis_agent.py.bak-20261004, tests/test_improve_loop.py.bak-20261004, pytest.ini.bak-20261004.
