# ESTATE SMITH PROMOTED - lane B3 of the standing-wave build - 2026-10-09

The receipt-space v1 instrument (this directory, `estate_smith.py`, one row in
`estate_smith.jsonl`) is now a repo tool with tests and a daily task, per the
promotion path in `watch/inbox/smith_chart_estate_20261009/SPEC.md` (steps 1
and 2 of "Promotion path"). The Smith chart of the estate water computer is no
longer receipt-space: it is `tools/estate_smith.py`, pinned by
`tests/test_estate_smith.py`, firing daily as MagEstateSmithDaily.

## Landed

- `tools/estate_smith.py` (298 lines): the six blocks unchanged in kind from
  v1 - STORAGE (volume free + last two disk_smith rows incl pagefile.sys file
  size), PRESSURE (RAM/pagefile, allocated vs used), COMPUTE (per-seat
  CPU-seconds stock + RSS + proc counts via psutil), FLOW (events + burn
  LEDGER rows last 24h, bounded 2MB tail reads), LOSS (zcode_cache delta
  between disk_smith rows), RESONANCE (fill rate vs the prior row). Ledger
  moved to `logs/estate_smith.jsonl` (this tool is the only writer). `--dry`
  prints without appending; `--history N` prints the last N rows flat like
  disk_smith; alerts append `memory/attention.md` lines and exit 1 on: ram
  avail < 8GB, disk free < 15GB, pagefile.sys file > 40GB (the file size from
  the last disk_smith row, not the allocation). Containment held: psutil +
  bounded tails of repo files only, no disk walks. Ratchet scan via
  `tools/violation_ratchet.py violations_in`: CLEAN (0 hits; also 0
  em/en-dash hits, under the 400-line cap).
- `tests/test_estate_smith.py`: 14 tests - block-shape on faked psutil organs
  (disk/vm/swap/process_iter monkeypatched, ledger paths pointed at tmp),
  alert-threshold units with quiet boundaries (7.9 fires / 8.0 quiet, 14.9
  fires / 15.0 quiet, 40.1 fires / 40.0 quiet), delta math on a synthetic
  two-row ledger (4h window, 10GB filled, gb_filled_per_h 2.5), loss window
  from synthetic disk_smith rows, 24h flow counter (stale and ts-less rows
  excluded, missing organ reads None), history flag (last-N flat, no-ledger
  path), and main write semantics (--dry writes nothing; live appends exactly
  one row and exits 0 healthy; breach appends attention + exits 1 with the
  row still landing).
- `scripts/estate_smith_daily.ps1` (mirrors `scripts/census_patrol_daily.ps1`:
  UTF-8 per-line Add-Content logging, no Tee-Object, log
  `logs/estate_smith.log`, venv-missing = exit 2) and
  `scripts/register_estate_smith_task.ps1` (schtasks via the run_hidden.vbs
  launcher, same shape as the census patrol registration).

## Tests - real numbers

Command: `.venv\Scripts\python.exe -m pytest tests/test_estate_smith.py -q`
Moment: 2026-10-09T03:36:34Z (third consecutive green run; first run tripped a
transient WinError 5 on the conftest basetemp cleanup, the known
agents/pytest-tmp AV-flake class, clean on rerun; one test bug found and fixed
- the synthetic prior row sat at NOW so the tail read a 0h window, now the
ledger holds an 8h-old row and a 4h-old row and asserts the tail takes the
latest). Result: **14 passed in 0.72s**, zero failures, zero errors.

## Task - registered and verified

Registered via `cmd //c powershell -NoProfile -ExecutionPolicy Bypass -File
scripts\register_estate_smith_task.ps1` (through cmd because Git Bash mangles
schtasks slashes - reproduced live: a bare `schtasks /Query` in bash errored
with "Invalid argument/option - 'C:/Program Files/Git/Query'").
`schtasks /Query /TN MagEstateSmithDaily /V /FO LIST` returns:

```text
TaskName:            \MagEstateSmithDaily
Next Run Time:       10/9/2026 9:05:00 AM
Status:              Ready
Scheduled Task State: Enabled
Schedule Type:       Daily
Task To Run:         wscript.exe //B //Nologo ...\run_hidden.vbs powershell.exe
                     -NoProfile -ExecutionPolicy Bypass -File ...\estate_smith_daily.ps1
```

09:05 sits after the disk smith 08:50, preserving the one-disk-process
stagger the SPEC names. The daily script was NOT fired by hand: the ledger
would have gained a third row the same night; its first scheduled fire is the
query's Next Run Time above.

## The live row - second ledger row, landed for real

`logs/estate_smith.jsonl` was seeded with the v1 receipt row (ts
2026-10-09T02:23:24Z, the only row this directory's estate_smith.jsonl held)
so the lineage survives the move; the tool is the only writer from seeding
on. The live run (`.venv\Scripts\python.exe -m tools.estate_smith`, exit 1)
appended row 2, ts 2026-10-09T03:36:03Z. Highlights, all from that row:

- STORAGE: 455.8GB free of 1862.2GB (75.5% used); last disk_smith free 458.1;
  pagefile.sys file 63.95GB.
- PRESSURE: 35.5GB RAM available of 64.0GB (44.4% used); pagefile 64.0GB
  allocated vs 0.9GB used - the balloon gauge gap the chart exists to show.
- COMPUTE: 7 seat buckets live (other 283 procs / 43.9 cpu-hours / 15.8GB
  RSS; python 15 / 3.3 / 3.5; docker 11; grok, ollama, node, codex each
  present); top RSS: vmmem 3.47GB, python 2.25GB, memcompression 1.36GB.
- FLOW: 5385 events in 24h, 0 burn LEDGER rows (organ quiet tonight).
- LOSS: zcode_delta_gb -234.91 over the 00:48Z -> 02:16Z disk_smith window
  (the cache clear, now charted as leakage in the negative).
- RESONANCE: rows_before 1, dt_h 1.21, gb_filled_per_h 1.9.
- ALERT (real breach, truthful): PAGEFILE FILE BALLOON - pagefile.sys at
  63.95GB > the 40.0GB cap; appended to memory/attention.md as
  "2026-10-09T03:36:03.194471Z ESTATE_SMITH PAGEFILE FILE BALLOON: ..." next
  to the standing DISK_SMITH lines for the same balloon; exit 1 per contract,
  and the row still landed (one writer, one row, even on alert).

## One-liner for the board

14 tests green, MagEstateSmithDaily Ready at 09:05, and the castle's second
chart row reads: 455.8GB free, 35.5GB RAM avail, pagefile balloon 63.95GB
alerting as designed, disk emptying at 1.9GB/h.
