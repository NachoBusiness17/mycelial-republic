

## NIGHT STATE (2026-09-23, pre-dawn) — STAGED, key seat empty
- The churn script is complete (dedupe + grading + anchor map + spend ledger), but the seat it draws from is empty: `GROK_API_KEY_2` and `GROK_API_KEY` in .env are placeholder lines with no values.
- The "second grok key" rides one of three real routes, operator's pick:
  1. Paste the actual second-account API key into GROK_API_KEY_2 → script fires as-is.
  2. The Grok CLI subscription (~/.grok/bin/grok.exe, present, Super-Grok-backed) — needs a small TUI-adapter variant (20 agent sessions is the wrong shape for one nightly churn; a thin headless wrapper is the build).
  3. Arm XAI_CASH_ALLOWED=1 for one metered run on the primary API (the law's last-resort door).
- Morning audit addendum: GROK_API_KEY/KEY_2 empty placeholders + load_env does not surface them — disease #4 in the free-keys audit (same family as NVIDIA's triple-named key).
