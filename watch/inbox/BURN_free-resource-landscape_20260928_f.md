# BURN free-resource-landscape 2026-09-28 f (DeepSeek window-definition contest closed)

## Verdict

steal

## Evidence

- Official page fetched 2026-09-28 ~08:03Z: https://api-docs.deepseek.com/quick_start/pricing. Footnote (2), verbatim: "Off-peak rates are half of the peak rates. Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays. All other hours are off-peak, including weekends and Chinese public holidays in full."
- Official table (per 1M tokens, deepseek-flash / deepseek-v4-pro): input cache miss $0.15 / $0.66 off-peak vs $0.3 / $1.32 peak; input cache hit $0.003 / $0.022 vs $0.006 / $0.044; output $0.6 / $1.98 vs $1.2 / $3.96.
- Time math: `date -u` at fetch read 2026-09-28T08:03:50Z; weekday verified Monday (`date -u -d 2026-09-28`). 08:03Z sits inside official peak band 06:00-10:00 (Mon), so off-peak is CLOSED now; next off-peak open is 10:00Z today. Under the same official shape, pass e's 07:03:52Z probe also ran inside peak, the worst slot, not merely out of the old canon window.
- Shape check: canon 16:30-00:30 UTC overlaps neither official peak band, so it is a strict subset of weekday off-peak: safe but narrow, missing 00:00-01:00, 04:00-06:00, 10:00-16:30, and entire weekends (2026-09-27 was Sunday: all off-peak officially, canon called it out-of-window).
- Aggregator cross-check: pass e's unofficial summary ("off-peak at 50% discount outside 01:00-04:00 and 06:00-10:00 UTC") is CONFIRMED on band shape and REFINED by the official text: the peak bands apply weekdays only, excluding Chinese public holidays; weekends and Chinese public holidays are fully off-peak. No WebSearch was needed; the first fetch carried the window.

## Steal or Vacuous

Steal. The window-definition contest is closed against the one source both shapes defer to, and the official shape is pinned. Fleet canon corrected: the DeepSeek freelane window is now defined as all hours outside 01:00-04:00 and 06:00-10:00 UTC, Monday through Friday, excluding Chinese public holidays; weekends and Chinese public holidays are fully off-peak at 50 percent discount. The old 16:30-00:30 canon demotes from window to safe-subset shortcut. Receipt stands in watch/inbox; ledger note: current UTC at pinning was peak, so no hammer fired this pass and none may be claimed; the in-window authenticated hammer stays owed at the next off-peak open (10:00Z Monday) or any weekend hour.

## Falsifier

Pre-registered build: pass g fires the authenticated hammer (driver file, key material never read or printed) inside 2026-09-28T10:00-16:30Z, an officially off-peak slot. Falsifier 1: if observed billing or usage metadata on those calls fails to reflect the 50 percent off-peak discount (deepseek-flash cache-miss input $0.15, not $0.30), the pinned shape is wrong and the contest reopens. Falsifier 2: any hammer inside 06:00-10:00Z Mon billed at off-peak rates likewise falsifies the shape.

## Bibliography

- https://api-docs.deepseek.com/quick_start/pricing (official DeepSeek pricing page, fetched 2026-09-28 ~08:03Z via WebFetch)
- `watch/inbox/BURN_free-resource-landscape_20260928_e.md` (read 2026-09-28; the contested definitions as landed)
- `watch/inbox/LINKS.jsonl` (tail -30, read 2026-09-28; no DeepSeek window rows)
- `date -u` readings: 2026-09-28T08:03:50Z; weekday checks for 2026-09-26, 2026-09-27, 2026-09-28
