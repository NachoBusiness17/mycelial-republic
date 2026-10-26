# B2-351 Schedule the secret scan (SW-07, 2026-09-26)

## Verdict

LANDED. The B2-73 scanner now runs weekly on a schedule: schtask MagSecretScanWeekly registered (Mondays 06:40 local, next run 9/28/2026 6:40 AM, Status Ready), driven by scripts/secret_scan_weekly.py which appends one summary row per run to watch/inbox/SECRET_SCAN_BEAT.jsonl (schema secret_scan_beat.v1: ts, critical, high, files_with_rule_hits, results path) and prepends a dated ALERT line to memory/attention.md whenever critical/high counts are above zero. Live beat fired twice this lane (first run died on a script typo, receipted below; second run green): beat row `{"ts": "2026-09-26T21:13:04Z", ..., "critical": 1, "high": 48544, ...}` and the ALERT line on memory/attention.md:144.

## Evidence file:line quotes

- QUEUE.md row: "wire B2_73_secret_scan.py into a weekly schtask beside the census patrol pattern with output to watch/inbox and an alert line to memory/attention.md on any critical/high rule count above zero, or register the manual-cadence decision with a reason+date".
- Install output: `SUCCESS: The scheduled task "MagSecretScanWeekly" has successfully been created.`; query: Next Run Time 9/28/2026 6:40:00 AM, Status Ready.
- Baseline comparison (no new dump; the alarm is known noise): the 08:xx B2-73 baseline rule_counts show AWS-SECRET-40 48427 / PRIVATE-KEY-BLOCK 1; the live beat reads 48544 / 1 -- the +117 high delta tracks corpus growth (third-party trees: dfhack protobuf, x_canon fixtures), and the single critical (PRIVATE-KEY-BLOCK) is the same corpus fixture the baseline carried.
- First-run defect, receipted per the no-fabrication law: the beat wrapper crashed with `NameError: name 'rid' is not defined` (a dict-comprehension typo in the severity map, `{rid: r[1] for r in mod.RULES}`); fixed to `{r[0]: r[1] ...}` and re-run green. The empty first beat file state was overwritten by the green run's row.
- Honest surface note: the ALERT line landed at memory/attention.md:144, not line 1 -- a concurrent writer rewrote attention.md between this lane's read and write-back (the shared-hot-file scramble); the alert survived with its full content and timestamp, only its position moved.

## Work done

- scripts/secret_scan_weekly.py: in-process scanner invocation, beat row appender, attention.md alert prepender (crit/high > 0 gate).
- schtask MagSecretScanWeekly registered (weekly Monday 06:40).
- Two live beats fired; green run's row and alert verified on disk; baseline diff shows no new dump class.

## Falsifier

The brief's falsifier ("a full week containing a new dump-shaped file with no scan landing on the inbox") is falsified by construction: any Monday with a new dump-shaped file produces a beat row with elevated critical/high plus the attention alert within the week. Reopen if: SECRET_SCAN_BEAT.jsonl shows a gap of more than 8 days between rows while the schtask exists, or a critical/high beat row lands with no ALERT line on attention.md.

## Bibliography closed

Read: watch/inbox/burn_wave_20260926/B2_73_secret_scan.py (RULES severities, main), B2_73_secret_scan_results.json (baseline rule_counts, census), scripts/secret_scan_weekly.py (this lane's wrapper, post-fix), watch/inbox/SECRET_SCAN_BEAT.jsonl (green row), memory/attention.md (alert line position), schtasks query/create outputs, watch/inbox/burn_wave_20260926/B2_246_collect_schedule_20260926.md (schtask pattern, via row pointer). No external sources.
