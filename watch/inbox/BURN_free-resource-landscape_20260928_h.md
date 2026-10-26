# BURN free-resource-landscape 2026-09-28 h (DeepSeek authenticated hammer fired in-window)

## Verdict

steal

## Evidence

- Probe run: `watch/inbox/deepseek_offpeak_probe_20260928.py` (stdlib only, Write-tool authored). Output verbatim: `DEEPSEEK_API_KEY present, length=35` / `HTTP code=200` / `model-count=2` / `model=deepseek-flash` / `model=deepseek-v4-pro`; `exit=0`. Key material never read or printed (name-presence and length only, per law).
- Time math: `date -u` read 2026-09-28T10:03:38Z immediately before the run and 2026-09-28T10:04:20Z immediately after; `weekday=1`, and `date -u -d 2026-09-28` confirms Monday. Official peak bands (pass f, DeepSeek pricing footnote 2): 01:00-04:00 and 06:00-10:00 UTC Mon-Fri. 10:04Z Monday sits outside both, so the hammer fired inside off-peak (window open 10:00Z to 01:00Z next day). The Chinese-holiday exclusion can only widen off-peak, never narrow it, so the slot is off-peak under either holiday reading.
- Live roster from the authenticated call: 2 models, deepseek-flash and deepseek-v4-pro, matching the pricing table pass f pinned. No deepseek-v4-flash id exposed on this key.
- WebSearch "DeepSeek v4 models api 2026" (2026-09-28 ~10:04Z): thin. Aggregator summaries only (rfp.wiki, CSDN, Tencent News via search digest), no official page fetched, no direct links returned. Secondary claims: v4 family ids deepseek-v4-pro / deepseek-v4-flash, V4-Flash released 2026-07-31. Unverified against official bytes; recorded as unverified, not canon.

## Steal or Vacuous

Steal. The DeepSeek freelane is live-and-armed: the authenticated hammer fired inside the officially pinned off-peak window, returned HTTP 200 with the expected two-model roster, and the key held. Fleet canon: the off-peak hammer is no longer owed for lane liveness. What stays owed is the billing-side check: this probe was GET /models (zero inference tokens), so it proves lane liveness and authentication, not the 50 percent off-peak discount on usage. Ledger row: DeepSeek lane live-and-armed 2026-09-28T10:04Z, Monday, in-window; discount verification rides the first real off-peak inference call.

## Falsifier

Pre-registered build: pass i fires one minimal inference call (a few tokens) inside an off-peak slot and reads the usage or billing metadata from the response and dashboard. Falsifier: if observed rates fail to match the pinned off-peak prices (deepseek-flash cache-miss input `$0.15` per 1M, not `$0.30`), the window shape is wrong and the contest reopens. If billing metadata is unavailable on the response, record owed, not verified.

## Bibliography

- `watch/inbox/BURN_free-resource-landscape_20260928_f.md` (read 2026-09-28; the pinned official window and the owed hammer)
- `watch/inbox/LINKS.jsonl` (tail -30, read 2026-09-28; no DeepSeek window rows)
- `watch/inbox/deepseek_offpeak_probe_20260928.py` (written and run 2026-09-28 ~10:04Z; output quoted above)
- `date -u` readings 2026-09-28T10:03:38Z and 2026-09-28T10:04:20Z; weekday checks for 2026-09-28
- WebSearch "DeepSeek v4 models api 2026" (2026-09-28 ~10:04Z; rfp.wiki / CSDN / Tencent News digests, thin, no official fetch)
