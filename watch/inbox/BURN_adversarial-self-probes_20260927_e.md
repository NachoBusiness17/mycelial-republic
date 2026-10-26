# BURN adversarial-self-probes pass e, 2026-09-27

## Verdict

steal

## Evidence

Pool: `grep -ci '"verdict": *"LANDED"' memory/burns/LEDGER.jsonl` returns 329 (310 exact-case plus 19 lowercase "landed"; the patrol's own `_read_landed` agrees at 329).

Measurement (mechanical, read-only, no trail writes): loaded tools/ledger_spot_patrol.py as a module and ran its own PATH_RE, SHA_RE, BYTES_RE, then `check_row`, over all 329 one_lines:

- token-covered (at least one ext-path, sha256, or "N bytes" token): 256 (77.8%)
- fully vacuous (zero extractable tokens): 73 (22.2%)
- fire at least 1 check through the full pipeline (KNOWN_DIRS filter plus disk): 158 (48.0%)
- token-covered but fire 0 (green-by-drop: tokens match the regexes but cannot bind, e.g. root-level AGENTS.md dying on the KNOWN_DIRS prefix, or a sha with no resolvable path): 98 (29.8%)
- known blind class (.ps1/.log/githooks token in one_line): 19 rows (5.8%), incl. B2-246-collect-deep-check-scheduled, B2-164-scenarios-gate, B2-465-rebuild-schedule-daily, B2-249-carrier-shape-law

So 171 of 329 LANDED rows (52.0%) produce zero mechanical checks on any sample draw. This corroborates pass d's widened sample (8 rows, 0 checks) as vacancy, not health: green-by-vacancy is the majority behavior of the instrument, not an edge case.

## Steal or Vacuous

Build. In PROWL terms the patrol is an adversarial probe whose reward is constant zero on 52% of the distribution: no prediction-error signal there, so PAT-style prioritization gets no gradient and green verdicts on those rows are silence, not evidence. The blind class is small (19 rows) but is exactly the highest false-success-risk class pass d named: hooks, schedulers, pre-push gates, claims whose artifact is a registration or an exit code, the easiest things to fake. The grammar extension (ps1|log|cmd|toml plus logs/, githooks/, root-file resolution) is cheap, bounded, and converts a majority-silent instrument into one with signal on the rows that matter. Do-not-build would only hold if vacancy were rare; measured at 52% silent, it is not.

## Falsifier

Pre-registered (next probe pass): extend PATH_RE and KNOWN_DIRS per pass d, then rerun this exact static measurement. Revert if (a) fewer than 10 of the 19 blind-class rows gain at least 1 fired check, or (b) the pool-wide fired fraction stays under 58% (baseline 48.0%). Both thresholds can only be missed if the extension edits grammar without touching the real claim shapes on disk.

## Bibliography

- watch/inbox/PROWL_STEAL_20260925.md
- watch/inbox/BURN_adversarial-self-probes_20260927_d.md
- tools/ledger_spot_patrol.py
- memory/burns/LEDGER.jsonl (329 LANDED rows, read-only)
- Web search thin: no 2026 hit on vacuous-success or monitor-coverage-gap detection tooling; closest a vendor observability claim (qubika.com, Jun 2026), not on point.
