# ENVELOPE LAW - provider-error tally (B2-441, 2026-09-26)

Any wave receipt claiming a 1302 count ("zero 1302", "N x 1302") is INVALID
unless it cites a provider_errors.json (or equivalent per-wave tally JSON)
written in the SAME session as the wave.

Dispatcher post-wave one-liner (run after every wave lands):

    python tools/provider_error_tally.py --session <wave-session-id> --out <session-dir>/provider_errors.json

Falsifier: a receipt claiming "zero 1302" whose session dir holds no tally
file, or whose tally shows a nonzero network_failed_events count, is invalid.
Origin: B2-25 measured 287 absorbed 1302 retries across three waves the B2-25
receipt had called clean with zero surfaced bytes; tool and law:
tools/provider_error_tally.py (docstring carries the same law),
watch/inbox/burn_wave_20260926/B2_98_error_visibility_20260926.md.
