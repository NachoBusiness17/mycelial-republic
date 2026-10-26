# BREAK-OPERATIONS PASS - hostile second pass on the operations lens (2026-10-02)

Break seat: break-operations, ractor-dogfood window (2026-09-30T20:00Z to 2026-10-02T11:00Z).
Method: every evidence cite re-derived this sitting from bytes on the CURRENT tree plus live
process/log/CIM instruments. Census commands named inline. Not run this sitting (honesty
ledger at the bottom). No em-dashes. All times UTC unless stated.

## Verdicts

### Finding 1 (67.6 pct re-fire excess; twin fix ~4.5 pct; no atomic claim persists): CONFIRMED

Byte-verified by a fresh census run this sitting
(`./.venv/Scripts/python.exe` over `memory/runs/hermes_burn/usage.jsonl`, 236 rows):

- 236 rows, all dated 2026-10-01, last row 21:53:52.578003Z. Matches.
- total cost_usd 37.7591. Matches to 4 decimals.
- excess after first copy per (id,turn) key: 25.5316 = 67.6 pct of total. Matches exactly.
- A1_steer_antiforgery: 52 rows (49 turn-1 + 3 turn-2), range 13:11:41 -> 20:17:25,
  costs 0.1215..0.6502, excess with each key's first row counted real = 21.0932. Matches
  (the lens's "49 times" is off by one; the true excess-row count is 50: 48 turn-1 + 2 turn-2).
- DUEL1_hidden_5 x46 and N1_parables_songmap x42, every row cost_usd 0.0, ok=false;
  total ok=false rows 89 (46 + 42 + 1 T1W2_S8_stealth), zero dollars. Matches.
- Twin slice: exactly 13 doubled keys 21:39:37-21:53:52 (12 DUEL2_train_*_r2 + N1R),
  key totals sum 2.2521 (the commit's "$2.25"), first copies 1.1229 (commit's "$1.09 real",
  method drift), excess 1.1292 = 4.42 pct of 25.5316 ("~4.5 pct" holds).
- No atomic claim in tools/hermes_burn.py: 400 lines, zero lock/O_EXCL/flock matches (the
  only "lock" hits are "block" substrings at :152/:155/:226); run_ask checks _landed_skip
  at tools/hermes_burn.py:283 then fires. CARRIER-PATCH 1/2/3 docstrings at :197-218,
  :221-255, :264-277. Cite drift only: mtime-bypass comment is :202 not :203; REFUSED patch
  is :264-277 not :264-276.

TWO EVIDENCE LEGS CORRECTED (finding survives, its "proof" leg inverts):

1. Token figure 5,639,068 = prompt+completion 4,368,123 PLUS reasoning_tokens 1,270,945
   (field present on 141 rows). Legitimate total, unnamed denominator (B2-216 law: name
   instrument before comparing).
2. "the 13 doubled keys fell AFTER _landed_skip existed" is not provable and the record now
   cuts against it. `git log -S "_landed_skip"` shows it first committed in 5d2263f10 at
   2026-10-02T00:46:30Z, 2h53m AFTER the last doubled key; the commit that CLAIMS the
   patches (43f50ed71, 2026-10-01T21:41:17Z) carries ZERO files under tests/ or tools/
   (`git show 43f50ed71 --name-only | grep -cE "^(tests|tools)/"` = 0); the _landed_skip
   tests first land in 0c9d72a06 (2026-10-02T04:18:32Z). And the pair structure argues the
   skip was INACTIVE on disk at the time: 10 of 13 pairs are 43-90s apart and the
   DUEL2 asks carry revision:null / turn2_only:false (memory/plans/hermes_burn_duel2/
   train_02_r2/ask.json read this sitting), so an active _landed_skip would have skipped a
   second fire arriving 43s after the first copy's output landed. It did not skip. The
   structural claim (check-then-fire, no claim lock) stands on current bytes; the
   historical "existed at their moment" leg inverts.

Also: the class had FOUR causes, not three. The lens missed duplicate-id staging:
memory/plans/hermes_burn_refire/{A1,B2,C1} re-stage ids already live in batch1/batch2
(ask.json mtimes 2026-10-01T18:14Z, mid-storm). No cross-queue id-uniqueness exists
anywhere in the fire path; a duplicate id today double-fires under a single driver
whenever outputs are absent.

### Finding 2 (pidfile guard inert against surviving driver 44072): CONFIRMED, STRENGTHENED

- Live CIM census this sitting (Get-CimInstance Win32_Process, 2026-10-02T11:09:54Z):
  exactly ONE real driver, PID 44072, `"C:\Program Files\Git\usr\bin\bash.exe"
  scripts/descent_driver.sh`, CreationDate 10/1/2026 5:31:24 PM local = 21:31:24Z,
  parent 50236. Direct PID query: 50236 GONE. All other bash processes are Zcode tool
  shells (the lens's contamination warning is live: my snapshot shows sibling agents'
  shells carrying 'descent_driver'/'PIDFILE GUARD' strings; classification by invocation
  shape is the only sound filter).
- state/ holds only autodrain.pid (9/22/2026 8:30:21 AM) and night_cadence.pid
  (8/28/2026 9:48:17 PM). No descent_driver.pid. The guard (scripts/descent_driver.sh:13-22;
  lens cite 12-25, actual block 10-23) passes when the pidfile is absent. Any new launch
  double-drains beside 44072 today.
- Guard committed e3c7d341c at 2026-10-02T03:31:54-04:00 = 07:31:54Z, ~10h after 44072's
  birth: its bash read pre-guard bytes. Beat: 947 events from 21:31:24Z cycle=1 to
  11:12:32Z cycle=947, zero non-increment steps, zero sub-30s gaps (lens saw 919-922 at
  10:52; same trajectory). Log tail: every ask skipped, "ledger total $37.76". Matches.

STRENGTHHENED BEYOND THE LENS:

- 44072 was one of the two colliders that produced the 13 doubled keys. Its beat's single
  1286s gap is exactly 21:31:24Z -> 21:52:50Z (cycle-1 pass, 21.5 minutes through the
  duel2 fires); the doubled keys 21:39:37-21:53:52 fall inside that pass racing the
  20:40-born stream's 27-minute cycle-61 pass (21:27:46 -> 21:54:39 in driver.log).
- "both killed" (e3c7d341c, 03:31:54Z) is byte-falsified in completeness: the 20:40:13Z-born
  stream cycles continuously to at least 07:26:57Z (cycles 1 -> 725 in the log/beat join),
  ~4h past the kill claim. The doubling stopped because queues went dry and skip logic
  caught up, not because the population was killed.
- The lens's falsifier "driver.beat showing a doubled/interleaved cadence right now (it
  does not)" rests on a blind instrument: beat uniformity cannot detect a sibling running
  older bytes. Proven in-window: 44072's beats stayed perfectly uniform 21:39-21:53Z while
  a non-beat-writing twin doubled money underneath (the beat file's first line IS 44072's
  cycle 1; no earlier driver ever wrote a beat).

### Finding 3 (guard pattern built once, never swept; 1 of 11; stale pids): CONFIRMED, CORRECTED

- Regex sweep of all named siblings this sitting: ONLY descent_driver.sh matches
  pidfile/already-running. The other ten carry nothing. The two stale pidfiles byte-verify
  (mtimes above, no reclaiming process).
- CORRECTION 1: the sibling "x_auth_loop.sh" does not exist; the file is scripts/x_auth_loop.py.
- CORRECTION 2 (changes the move): the pattern was NOT built once. The estate already owns
  at least four other instance-guard lineages that never met: scripts/build_lane_game.py:63
  (LOCK = OUT/"run.lock", stale holders self-clear 15 min), scripts/union_fullsend_day.py:57
  and :572-574 (same run.lock + self-clear), scripts/lesson_gate.py:125-129 (_Lock: O_EXCL
  lockfile with stale-lock theft), scripts/run_mate.ps1:76 ("atomic CreateNew = the lock"),
  plus mag/ pidfile writers (mag/autodrain.py matches; likely author of the stale
  autodrain.pid). And scripts/wave_driver.py:168-192 already rides an O_EXCL append lock
  (mag.grounding_wave) for ITS ledger, the exact protection tools/hermes_burn.py lacks.
  The sweep is a steal-not-build: reuse lesson_gate's _Lock as a shared helper.

### Finding 4 (kpi.jsonl still live, unrotated): CONFIRMED, WORSENED

- Three size readings: 752,865,877 (lens, ~06:44 local) -> 753,203,531 (07:04:26) ->
  753,426,479 (~07:21): +560,602 bytes in ~37 min, ~22 MB/day pace, still appending.
- Writer byte-confirmed: mag/records.py:138 write_kpi, append at :166-167, KPI_LOG =
  logs/kpi.jsonl defined at :17. grep for rotate/rotation in records.py: zero hits.
- NEW MECHANISM the lens missed: the growth COMPOUNDS. Tail rows land every ~70-110s
  (source=summarize), each ~20.3KB, and each row's incomplete_ids list is GROWING +1 per
  row (672 -> 676 across the last five rows): every appended row re-lists an ever-longer
  ungraduated set, so per-row payload rises as neglect continues. Rotation caps the file;
  only a cap/delta on incomplete_ids caps the acceleration.

## Additions (what the lens missed)

1. COMMIT-MESSAGE THEATER IN 43f50ed71 (dogfood Q1's class, in the window's own
   neighborhood): the message claims "CARRIER: 3 bleed-class patches ... + 21 tests" but
   the commit carries ZERO files under tests/, tools/, mag/, or scripts/ (name-only grep
   count 0; its files are memory/plans + corpus artifacts). The claimed patch bytes first
   land in 5d2263f10 (00:46:30Z, GAP ANALYSIS, whose message never mentions them) and the
   tests in 0c9d72a06 (04:18:32Z). Claim and bytes live in three different commits.
   Falsifier: a `git show 43f50ed71 --name-only` listing any tests/ or tools/ file.
   Move: file the erratum + a cheap commit lint (message claims "tests" -> diff must touch
   tests/), ~25 min.
2. T1W2 19:17-19:18Z DOUBLE-FIRE CAUSE NOW CLASS-ATTRIBUTED FROM ESTATE BYTES, and
   "both killed" FALSIFIED (detailed under Finding 2). driver.log line 449
   `[driver cycle 1 19:17:13Z]` is the second instance's birth; the S5-S8 double-fires
   19:17:38-19:18:33 (S7_mates two rows in the SAME second, 19:18:24/19:18:25) are its
   first pass racing driver 1's cycle-13/14 pass. The OWED item half-closes: cause class
   = concurrent instance (the pidfile guard would have prevented it); the LAUNCHER
   identity stays OWED (parent 50236 gone, confirmed by direct query).
3. BEAT-BLINDNESS LAW: a uniform heartbeat certifies only that no OTHER CURRENT-BYTES
   writer exists; siblings on older bytes are invisible to it (proven by the 21:39-21:53Z
   window). Move: write $$ into the beat line (one-line change, ~5 min) so any census can
   count writers, not cadence.
4. DUPLICATE-ID STAGING (hermes_burn_refire/{A1,B2,C1}, mtime 2026-10-01T18:14Z): a
   fourth re-fire cause with no guard anywhere. Move: run_ask refuses an id already
   claimed by another queue dir, or a staging lint at queue-scan time, ~20 min.
5. THE NIGHT'S INSTRUMENTS BUILT-BUT-NEVER-TICKETED, byte-confirmed: TICKET_LEDGER
   (watch/inbox/hermes_burn/TICKET_LEDGER.md:133-143) carries SW1-01..SW1-10 all
   LANDED-with-test plus SS53-5; grep for salon / rib_swarm / water_computer rows = ZERO
   hits. The staged-never-ticketed disease GAP ANALYSIS proved on localfirst applies to
   the estate's own model-garden night. (Also: the ask's evidence path was wrong; the
   ledger lives under watch/inbox/hermes_burn/, not memory/runs/hermes_burn/.)
6. NIGHT_CLOSE_20261002.md carries no erratum/owed lines (grep this sitting): the OWED
   erratum remains unpaid. REGISTRY.jsonl rows carry ts/name/digest/script/verdict/checks
   and NO topic field, so the topic-undefined fix cannot be verified from the registry;
   this run's own ask arrived with a well-formed topic (consistent with the fix holding),
   deeper verification OWED.

## Honesty ledger (not run this sitting)

- pytest census (the 4,147 claim), the SW1 suite, any test battery: NOT run, cited from
  receipts only. z.ai / grok / "$42 of $145" / "$47.54 Nous" dollar attribution: NOT
  summed. salon mesh, rib_swarm, water_computer dogfood depth: NOT audited beyond the
  TICKET_LEDGER grep. The 110-file working tree: sampled, not diffed file-by-file.
- Sub-process law: no python subprocess spawns this sitting (file reads + git only);
  shell calls rode the harness tool layer.

## Instrument appendix (exact commands)

- Census: `./.venv/Scripts/python.exe %TEMP%/breakops_census.py` over usage.jsonl (script
  banked in temp, logic reproduced in the numbers above).
- Process: `Get-CimInstance Win32_Process -Filter "Name='bash.exe' OR Name='sh.exe'"` +
  direct `ProcessId=50236` query at 2026-10-02T11:09:54Z.
- Git: `git log --format="%h %cI %s" -- tools/hermes_burn.py`; `git log -S "_landed_skip"`;
  `git show 43f50ed71 --name-only`.
- Logs: driver.log cycle-header extraction (1,270 headers) joined against driver.beat
  (947 events); driver.log transition greps at 19:0x-19:2x, 20:1x-20:4x, 21:2x-21:5x.
