# B2-424 receipt (2026-09-26)

## Verdict

LANDED. tools/envelope_harvest.py turns the B2-97 card's prose harvest into one command and reproduces the B2-25 wave-1 numbers exactly from live bytes: 37,386,533 tokens, 1229.9 s max duration, 109.4M tok/h, width 10 with 10/10 completed, window 11:24:57.106Z to 11:45:27.043Z (0.34165 h) - all four validation checks green, exit 0.

## Evidence file:line quotes

- Validation run (this lane, full live data): `python tools/envelope_harvest.py --agents-dir C:/Users/foste/.zcode/cli/agents/sess_fd5ec147-a47d-41ee-91f4-afd899b524ca --validate-b2-25 --limit 1` returns wave 1: `"tokens_total": 37386533`, `"dur_s_max": 1229.9`, `"tokens_max": 8767163` (lane "B2-01 THE50 punch list"), `"tools_mean": 54.0`, `"window_h": 0.34165`, `"tok_per_h": 109.4`, `"partial": false`; `"validation": {"pass": true}`; process exit 0. Session now holds 191 metadata.json (156 at B2-25 time; the extra lanes fired later in the day - clustering handles them, the first wave is unchanged, which is itself validation of the clusterer).
- The reproduced B2-25 receipt numbers: watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md Verdict "banking 37,386,533 witnessed tokens in 1229.9 s (20.50 min): 109.4M tok/h at width 10" and the wave table (mean 905.9 dur / 3738653 tokens / 54.0 tools - all three means reappear identically in the script's wave summary).
- Script shape: tools/envelope_harvest.py clusters agents by createdAt gaps (over 5 minutes starts a new wave; wave lanes were created within the same second), summarizes per wave the B2-25 table fields (dur s, tokens, tools: mean/max/total plus per-lane rows), computes the tok/h window from first creation to last completion, marks partial waves (open lanes), and greps 1302/429 across agent_*/output.txt and agent_*/task.output into a per-signal files/hits count.

## Work done

1. Read the B2-25 receipt for the exact table shape, formulas, and the wave-1 targets; inspected the metadata.json shape live (totalDurationMs/totalTokens/totalToolUseCount/createdAt/completedAt/status).
2. Landed tools/envelope_harvest.py with cluster/summarize/grep arms and the --validate-b2-25 arm so a firing lane can prove its tooling on the reference session in one command.
3. Ran the validation arm against the 191 live metadata files; all four checks pass on exact equality (or the named tolerance for the rounded floats).

## Falsifier

The brief's falsifier: "the script's wave-1 totals differ from B2-25 by anything but rounding". The validation arm encodes that as an exit-1 condition on exact token total, 0.05 s duration tolerance, and 0.05 M tok/h tolerance; rerunning it against the reference session is the standing check. Named limits, carried honestly from B2-25's own falsifier 1: the grep arm counts surfaced 1302/429 strings in output files; the main-session retry path can absorb errors silently (maxAttempts 11), so zero hits proves zero surfaced, not zero occurred. The window/tok-h figure is open-ended for partial waves and marked partial: true.

## Bibliography closed

- tools/envelope_harvest.py (new)
- watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md (targets + table shape)
- C:/Users/foste/.zcode/cli/agents/sess_fd5ec147-a47d-41ee-91f4-afd899b524ca/ (191 metadata.json + output files read)
- watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md (fire procedure the card came from)
