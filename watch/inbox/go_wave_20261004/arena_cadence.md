# LANE 6 RECEIPT - arena-cadence (GO item 6), GO wave 2026-10-04

Seat: lane 6 of the coordinator-partitioned GO wave. Fold: corpus/steal/MASTER_MICKEY17_V2.md
section 9 GO item 6. Lane evidence: memory/runs/mickey17_v2/runs/run-0/lanes/a01-arena-cadence.json
(rows 0,1,5,6,7 primary). Wave moment: 2026-10-04T08:1x-08:5xZ. Interpreter: the repo
venv only (`.venv\Scripts\python.exe`); no bare python. Zero em-dashes in files authored.

## Sub-item 1 - bank inside the fire after play + dogfood one fire: DONE

Change: both play carriers now bank their OWN run dir at exit, in the same process,
immediately after writing DONE (the GO item's "tavern carrier invokes arena_gwap
bank at exit" arm, applied to both carriers since the fire mints both kinds). The
automation's bank step had been a prompt instruction only; a01#7 proved a fire's own
sessions could outlive their bank overnight (the 20:00Z fire's three dungeon dirs
never banked that night; the 02:21-02:28Z pair banked outside any fire window).
Bank-only at exit (no gwap->gps feed - that stays with --backfill); bank failure
prints and never fails the play run. Fix comments name the cause and cite a01 rows
3+7 and the fold's GO item 6.

Dogfood fire (one full cycle, automation step order, executed 08:40-08:42Z):
- step 1 spend gate: `.venv\Scripts\python.exe` sum over usage.jsonl 2026-10-04 rows
  -> 668 rows $10.0183 at 08:40Z, under the $25 cap, proceed.
- step 2 dungeon: `.venv\Scripts\python.exe tools/dungeon.py --tip
  33121581dd76b6e8bbe9213bbdfb4011b712aa17588e97ad613a9bf8f95aa156 --budget-usd 0.35`
  (tip derived per the automation prompt: sha256(genesis|session_close|2026-10-04T08)).
  Output line: `DUNGEON: BANK OK dnd0_20261004T084103Z: dm=s472@1.0 grok=s473@1.0
  saelis=s474@1.0 | CHAIN ok=True bad=None`. DONE verdict: "GATE OPENED (audited):
  the claim verified against the bytes; verdict WON-S1", spend_usd 0.017.
- step 3 tavern (flash lane per the wave laws): `.venv\Scripts\python.exe
  tools/tavern.py --scenario
  memory/plans/hermes_burn_playground_20261003/scenarios/hollow_crown_flash_dogfood.json
  --rounds 3 --budget-usd 0.10 --chain-tip 20261004T08-fire-dogfood`
  (new haiku-roster dogfood scenario, 2 personas, judge haiku). Output line:
  `TAVERN: BANK OK tavern_20261004T084146Z: Maud Ashgrove=s475@0.0
  Pell Quickfinger=s476@0.0 | CHAIN ok=True bad=None`.
- fire-atomic proof: marker mtimes - dnd0_20261004T084103Z transcript/DONE/GWAP_BANKED
  all 08:41:32Z (same second); tavern_20261004T084146Z all 08:42:12Z (same second).
  Ledger last seq 476 at ts 2026-10-04T08:42:12Z: play and bank landed inside one
  fire, no overnight gap possible.
- receipt line (automation step-5 shape): FIRE 2026-10-04T08:41Z -
  dnd0_20261004T084103Z GATE OPENED (audited) WON-S1 $0.017; tavern_20261004T084146Z
  brawl=False esc {Maud 4, Pell 5} $0.0142; gwap seq 472-476 chain ok; cycle spend
  $0.0312 (0.017 + 0.0142); today $10.8825 as-of 08:43:03Z (recount:
  728 rows). Wave spend cap respected: this fire spent $0.0312 total.

## Sub-item 2 - parable erratum: DONE

Filed watch/inbox/PARABLE_ERRATUM_20261004.md (new file; the parable itself left
byte-untouched per lane ownership). Every number byte-checked with its producing
command in the receipt: cap $25 (automation title + step-1 prompt bytes); $25.1134
cumulative at 2026-10-03T19:33:24.686865Z on
GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003_STAGE_B = the "$25.11" meter reading
misnamed as cap; day-03 close 1034 rows $25.6218 = $0.6218 over cap; automation_runs
20 fires 13:00Z 10-03 through 08:00Z 10-04, exactly 1 failed = the 13:00:00Z first
fire; real ledgers named (arena-capability.jsonl: 314 rows at the a01 reads, 459/326
at 08:30:46Z, 476/343 at the 08:48:53Z filing moment; arena-sessions.jsonl: 60 rows
frozen 12:51:31Z-12:52:58Z) with the parable's 121/266 reconstructed as the hour-13
and through-hour-14 moments (121 and 266 rows exactly, hour buckets recounted);
"arena-sessions-v3" grep: 1 byte-match in the parable, 0 in code; "held to 35 cents"
filed unbacked with nearest byte-exact slices (DND0 cron 13:00-20:59Z $0.3272/192
calls, SEASON $0.3897, TAVERN day-03 $16.2003/665, DND0 day-03 $0.7903/316).

## Sub-item 3 - banked_at moment column in the dawn report: DONE

- tools/arena_gwap.py gained a --status mode: prints "GWAP LEDGER AS-OF <moment>",
  the census line (rows, distinct_scenes, dirs, banked, unbanked) and a per-dir
  `banked_at=<earliest ledger ts for that dir's scenes | UNBANKED>` column - the
  instrument the dawn report consumes. Cause: a01#5/N12, the banking verdict flipped
  NO to YES between the audit's 03:04Z and 03:26:51Z reads; no count without AS-OF.
- tools/cycle_brief.py (the morning composer, the closest existing dawn surface;
  break-communication F2 confirmed no dawn channel exists) gained a fail-open
  "## ARENA GWAP (banked_at moments)" section embedding the status output.
- Landed proof: `python tools/cycle_brief.py` ran clean at 08:43Z ->
  watch/inbox/CYCLE_BRIEF_20261004.md (15915 bytes, new file, none existed for
  today); its lines 52-62 carry the section with the dogfire's own dirs
  (dnd0_20261004T084103Z banked_at=2026-10-04T08:41:32Z, tavern_20261004T084146Z
  banked_at=2026-10-04T08:42:12Z) and the then-unbanked 08:00Z-fire dirs named.

## Sub-item 4 - backfill attribution note: DONE

Filed watch/inbox/ARENA_BACKFILL_ATTRIBUTION_20261004.md, marked UNPROVEN, NOT
ASSUMED in title and verdict: the 53/53 drain by 03:26:51Z is byte-proven (88-row
hour-03 bucket recounted unchanged at 08:48:53Z); the candidate runner
(tools/arena_gwap.py --backfill, the only all-dirs banking path) is named but NOT
credited: zero receipts name a runner (grep 08:4xZ), and the 03:00Z fire was still
live inside the drain window (automation_runs updated_at 2026-10-04T03:19:41.390Z),
so the runner remains attributed-to-no-one.

## Sub-item 5 - former GO item 7 DRAINED: STRUCK HERE ONLY

Former GO item 7 ("bank the 8 unbanked dirs") is DRAINED: the out-of-band backfill
covered 53/53 dirs by 03:26:51Z (a01#5 bytes; the 88-row hour-03 bucket). This
receipt records the strike; the fold text is the coordinator's to edit and this lane
does not touch it. What remains of item 7 is exactly the ordering fix, landed as
sub-item 1 (bank inside the fire), plus the a04 marker-gating caveat: aged backlog
dirs stay invisible to routine rebanks unless --backfill is used.

## Files touched

- tools/tavern.py - at-exit bank in main() (+22 lines)
- tools/dungeon.py - at-exit bank in main() (+21 lines; NOTE: file shared with the
  a02 dungeon-campaign lane, see blockers)
- tools/arena_gwap.py - --status mode with the banked_at column (+51 lines)
- tools/cycle_brief.py - section_arena_gwap + main() wiring (+31 lines)
- memory/plans/hermes_burn_playground_20261003/scenarios/hollow_crown_flash_dogfood.json - new
- watch/inbox/PARABLE_ERRATUM_20261004.md - new
- watch/inbox/ARENA_BACKFILL_ATTRIBUTION_20261004.md - new
- watch/inbox/CYCLE_BRIEF_20261004.md - new, generated by the instrument (dawn
  report landing proof)
- watch/inbox/go_wave_20261004/arena_cadence.md - this receipt

## Tests and gates run

- `.venv\Scripts\python.exe -m pytest tests/test_burn_id_uniqueness.py
  tests/test_gwap_payload.py tests/test_gwap_to_gps.py -q -p no:cacheprovider`:
  45 passed (run before AND after the carrier edits; the edits ride in main(), the
  tests exercise Run.play() directly, both green).
- `tools/arena_gwap.py --status` smoke: 71 lines, AS-OF 08:34:12Z, censuses move
  between reads exactly as the AS-OF column predicts (69 dirs/6 unbanked at 08:34Z
  -> 73/7 at 08:48:53Z: the hourly fires kept minting).
- `tools/violation_ratchet.py check --changed`: FAIL with NEW rows - none authored
  by this lane's lines; see blockers.

## Blockers (filed, not fabricated around)

1. Ratchet NEW rows from the SHARED working tree, not this lane's lines: mag/route_chat.py:174
   except-pass (lane 1's file, mid-edit), tools/prepush_credential_shape.py /
   tools/prepush_seal_patrol.py cwd-relative-path (untracked sibling-lane files).
2. tools/dungeon.py file-too-long (>400 lines) reads NEW: the file was already 605
   lines at HEAD (byte-checked: `git show HEAD:tools/dungeon.py | wc -l` = 605) and
   is 756 on disk because the a02 lane is editing it in parallel; this lane added
   21 lines in main() and crossed no threshold. Resolution (baseline-update by name
   or split) belongs to the coordinator/a02 at pre-push; this lane does not touch
   the baseline.
3. The 7 unbanked dirs at the 08:48:53Z census are pre-fix fire dirs; banking them
   is one `.venv\Scripts\python.exe tools/arena_gwap.py --backfill` away, left to
   the hourly cadence's step 4 (or the operator) - not this lane's fire.

## Verification index (commands -> claims)

- sqlite automations row + automation_runs census: `.venv\Scripts\python.exe` sqlite3
  over C:/Users/foste/.zcode/v2/tasks-index.sqlite (08:2xZ): title/prompt bytes, 20
  fires, 1 failed at 13:00:00Z, 03:00Z fire updated_at 03:19:41.390Z.
- usage.jsonl sums: `.venv\Scripts\python.exe` day-slice sums (08:2x-08:4xZ):
  day-03 1034/$25.6218, crossing $25.1134@19:33:24.686865Z, day-04 $10.0183@08:40Z
  and $10.8825@08:43:03Z, TAVERN $16.2003/665, DND0 $0.7903/316, cron $0.3272/192,
  SEASON $0.3897/1.
- ledger/playground census: `.venv\Scripts\python.exe` jsonl/dir walks: 459/326@08:30:46Z,
  476/343@08:48:53Z, hour-13 bucket 121, through-14 266, hour-03(10-04) 88.
- fire proof: mtime reads (all three files same-second per dir) + ledger seq 476
  ts 2026-10-04T08:42:12Z + carrier stdout lines quoted above.
