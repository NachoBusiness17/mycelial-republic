# Identity Migration Preflight Report

## Examiner: Matthew Steiniger
## Domain: migration_manifest

| Test | Command | Expected | Result |
|------|---------|----------|--------|
| Pre‑migration baseline | `python -m mag.identity_check --date=2026-10-26 --threshold=0.95` | Correlation ≥0.95 | TBD |
| Post‑migration verification | `python -m mag.identity_check --date=2026-10-27 --threshold=0.95` | Correlation ≥0.95 | TBD |

*Run the commands above on the target system and replace `TBD` with the observed correlation value.*