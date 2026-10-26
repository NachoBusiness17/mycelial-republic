# B2-362 FKB singleton search gap

## Verdict

LANDED. mag/failure_kb.py gains search_log + _tail_lines and a `search --log Q [--tail N] [--limit K]` CLI form: a bounded reverse-chunked tail read (64KB chunks, never loading the 39MB log whole) over the RAW log rows - the count-1 signatures the deduped index intentionally hides (the B2-87 write-amplification law). Falsifier executed live on real bytes: 2 count-1 sigs absent from the index are unfindable by every index command (query hits 0) and findable by the new log-tail search (1 hit each): read_file:8e9d6bdb2cc7 ("not a file: /app/tools/wave_lift.py") and run_shell:f6113643ecba ("command not allowlisted: mkdir"). 2 pins in tests/test_failure_kb.py (count-1 sig invisible to query, visible to search_log; tail bound + tool filter + limit short-circuit), suite 10 passed.

## Evidence file:line quotes

- mag/failure_kb.py:47-48: LOG_PATH logs/failure_kb.jsonl vs INDEX_PATH memory/failure_kb/signatures.json (the two surfaces); rebuild_index's min_count=2 policy (the B2-87 law the brief cites) is what makes count-1 sigs index-invisible.
- mag/failure_kb.py (post-patch) _tail_lines: "Last n lines of a file without loading it whole ... read backwards in 64KB chunks until n newlines are collected"; search_log docstring: "This command scans the LOG (the full-history surface) over its most recent `tail` rows, bounded so the 39MB log is never fully loaded into memory".
- CLI (post-patch): `search --log Q [--tail N] [--limit K]` branch inside the existing search dispatcher; default tail 2000, limit 20.
- Live falsifier run (this lane, bounded read of the last 5,000 log lines): "PROVEN count-1 sig: read_file:8e9d6bdb2cc7 ... index query hits: 0 ... search_log hits: 1" and "PROVEN count-1 sig: run_shell:f6113643ecba ... index query hits: 0 ... search_log hits: 1"; census in the same window: 5,000 rows, 99 distinct sigs, 32 count-1, 8 count-1 AND absent from the index.
- tests/test_failure_kb.py: 2 new pins; suite 10 passed, 0 failed.

## Work done

1. Read mag/failure_kb.py (query/lookup surface, rebuild min_count policy, verify's log recount, CLI dispatcher) and confirmed the falsifier premise structurally: nothing scanned the log.
2. Implemented _tail_lines (reverse 64KB chunk read, bounded) + search_log (case-insensitive substring over kind/tool/error/detail/sig, optional exact-tool filter, limit, returns scanned/hits) + the CLI branch.
3. Added 2 pins (hermetic tmp log + index; the index-hidden count-1 sig demonstration mirrors the live falsifier).
4. Executed the falsifier live against the real log with 2 proven index-hidden sigs.
5. py_compile OK; filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Brief's falsifier: "a sig with exactly 1 log event is unfindable by every fkb command today." TRUE at brief time (today's census: 8 count-1 sigs absent from the index in a 5,000-row window; query returns 0 for their detail substrings), FALSE after this landing (both proven sigs return exactly 1 search_log hit). Reproduction: `.venv/Scripts/python.exe -m mag.failure_kb search --log "not a file: /app/tools/wave_lift.py" --tail 5000` returns the read_file:8e9d6bdb2cc7 row while `... search "not a file: /app/tools/wave_lift.py"` (index mode) returns none, exit 1. Inversion: search_log failing to find a sig provably present in the tail window, or the tail read loading more than its bound, inverts the receipt.

## Bibliography closed

- mag/failure_kb.py (search_log, _tail_lines, CLI branch)
- tests/test_failure_kb.py (2 pins; 10 passed)
- logs/failure_kb.jsonl (the live falsifier window; read-only)
- watch/inbox/burn_wave_20260926/B2_87 receipts context (the min_count=2 law via rebuild_index docstring)
- Nothing owed.
