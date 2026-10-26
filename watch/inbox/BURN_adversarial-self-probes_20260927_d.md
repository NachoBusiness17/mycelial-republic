# BURN adversarial-self-probes pass d, 2026-09-27

## Verdict

steal

## Evidence

Patrol run 1 (default): "PATROL: 3 rows, 2 mechanical checks, 0 warns (WARN-ONLY; log SPOT_PATROL.jsonl)". Run 2 (--rows 8): "PATROL: 8 rows, 0 mechanical checks, 0 warns". Trail tail-12 in memory/burns/SPOT_PATROL.jsonl matches both runs row for row, all verdicts LANDED, every fired check green: b2-365-census-patrol-split carries "path-exists tools/census_collect.py ok" and "path-exists tests/test_census_drift_patrol.py ok". No warn fired in either run.

Blind-spot probe, one LANDED row. Extractor grammar (tools/ledger_spot_patrol.py): PATH_RE matches only extensions py|md|jsonl|json|txt|yaml|yml|ts|js|html|db|sqlite, and only tokens starting with a KNOWN_DIRS prefix resolve to disk. Row B2-246-collect-deep-check-scheduled names scripts/census_patrol_daily.ps1, scripts/register_census_patrol_task.ps1, and logs/census_patrol.log. Mechanical replay of PATH_RE over that one_line returns "extracted paths: ['tools/census_drift_patrol.py', 'AGENTS.md', 'memory/attention.md']": all three scheduled-task files are invisible (.ps1 and .log are not known extensions; logs/ is outside KNOWN_DIRS), and AGENTS.md matches the regex but is then dropped because the repo root is not a known dir. Hand check: ls confirms all three real on disk (8362, 1535, 1223 bytes). So the row whose core claim is "scheduled task registered and firing" fires 0 of the patrol's checks.

## Steal or Vacuous

The patrol is confirmed as a working in-distribution probe: it behaves exactly as its receipt (SPOT_PATROL_LANDED_20260927.md) claims, stayed read-only on the ledger, appended only to its own trail. The fleet adopts one correction to the falsifier clock: rows with zero extractable claims are silence, not evidence, so the two-week vacuousness tally must count verified rows (checks > 0), never raw runs; this pass's widened sample was 8 rows, 0 checks, warn-free by vacancy. The extractor coverage gap (.ps1/.log/.cmd extensions, logs/ and githooks/ dirs, root-level files) is filed as the named residual for the next probe pass. Until it closes, hook-and-scheduler landings, the highest false-success-risk class this lane exists to hunt, are structurally unchecked while reading as green.

## Falsifier

Build (pre-registered, next probe pass): extend PATH_RE with ps1|log|cmd|toml and add logs/, githooks/, and root-file handling to path resolution, then rerun the widened sample. If rows naming real on-disk files gain fewer than 3 additional fired checks, the extension is vacuous and reverts to the current grammar with the gap named in the receipt.

## Bibliography

- watch/inbox/PROWL_STEAL_20260925.md
- watch/inbox/SPOT_PATROL_LANDED_20260927.md
- tools/ledger_spot_patrol.py
- memory/burns/LEDGER.jsonl (row B2-246-collect-deep-check-scheduled, read-only)
- memory/burns/SPOT_PATROL.jsonl (tail-12)
- ls of scripts/census_patrol_daily.ps1, scripts/register_census_patrol_task.ps1, logs/census_patrol.log
- Web search (thin, no direct 2026 hit on regex claim-extraction audit or path claim verification tooling; closest: an LLM coding benchmark doing PASS/FAIL and path cross-checks, github.com)
