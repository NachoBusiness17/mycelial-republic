# BALL4 FOLLOW · COMPUTE LANE RECEIPT (2026-09-29)

Class: RECEIPT · Writer: gala-follow-compute (division B, ball4-luncheon-follow) · Register: `watch/inbox/luncheon_watchlist_20260929_signals.jsonl` (rows for writer `gala-follow-compute`)

## What was owed

Mine the compute layer of the luncheon watchlist (Huang/Nvidia, Su/AMD, Tan/Broadcom, Mehrotra/Micron, plus Musk's xAI/compute buildout) for last-14-days public signals (window 2026-09-15..2026-09-29), resolve handles live, append one register row per target with the signal, date, source URL, and the concrete estate angle on our VRAM ladder and local-inference economics.

## What landed

5 register rows appended to `watch/inbox/luncheon_watchlist_20260929_signals.jsonl` (schema matched to the 17 rows sibling lanes defense-enterprise + models had already written; rows 18-22 in the file). Per target, the one-line takeaway:

| Target | In-window signal (date) | VRAM-ladder / local-economics read |
|---|---|---|
| Jensen Huang (Nvidia) | $150B buyback + AI-agent security platform + joint OpenAI safeguards (Sep 28-29) | Cash-return mode + sold-out roadmap through Rubin H2-2026 shipping: no consumer-VRAM relief; frontier rental stays supply-priced high ($0.29 naive / $0.15 batched per AGENTS.md cost model); Rubin Ultra 1TB HBM4e rung recedes from our 24GB 3090 ladder (~$1,100-1,300 used) |
| Lisa Su (AMD) | Helios shipping ~50k MI450 GPUs to Oracle Q3 2026 (Sep 28 marker); ROCm AIC KV-cache system September tech preview; stock broke $524 mid-Sept | Second GPU source at 432GB HBM4/card pressures rental prices down at the margin; AIC converges on the exact problem class our lmcache corpus tree studies; HBM4 demand tightens used-24GB street prices |
| Hock Tan (Broadcom) | Doubled down on $115B FY27 / $230B FY28 AI-chip targets despite slowdown calls (Sep 14-15, edge of window); accelerating Ironwood TPUs to Anthropic (Sep 2-3 context) | ASIC diversification leans on input/cache-side prices, confirming the only-output-cuts-are-real-cheapeners law; power-not-demand constraint keeps rental tight through 2027; QLoRA 13B on one 3090 stays the load-bearing local rung |
| Sanjay Mehrotra (Micron) | Stifel Buy $1,500 target into the Sep 30 FQ4 print (Sep 27 marker) | HBM sold out through CY2026 (50-65% of key-customer demand met, standing facts) caps rental supply growth = shallow frontier price cuts; memory supercycle INFLATES our used-24GB rungs - attic buy-window needs a re-quote, not a green light |
| Elon Musk (xAI) | x.ai/colossus fetched live: 'Introducing Grok 4.7' (Sep 21), 'Team Bots' (Sep 28), Voice Transcribe 2.0 (Sep 18); banner 'Anthropic partners with Colossus'; 200k H100 / 1M roadmap | If the banner means Anthropic-on-xAI compute, rivals are pooling compute = frontier supply loosens while release cadence accelerates; model pinning needs shorter refresh loops; orbital/Terafab (1 GW by end-2026) non-binding for local economics this quarter |

## Handle resolution (live, this session)

All 5 compute handles resolved via `https://api.fxtwitter.com/<handle>` (code 200 each):
- `@nvidia` - NVIDIA, id 61559439, 2,673,377 followers (org grade stands)
- `@LisaSu` - Lisa Su, "Chair and CEO of @AMD", 320,593 followers (declared grade stands)
- `@Broadcom` - Broadcom, id 338504881, 66,720 followers (org grade stands)
- `@MicronTech` - Micron Technology, id 19037711, 64,051 followers (org grade stands)
- `@elonmusk` - Elon Musk, 241,720,780 followers, bio link resolves to `http://Terafab.AI` (declared grade stands; new datapoint, matches the Mar 2026 $20B Terafab fab reports)

Raw capture: `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow-compute.fxtwitter.txt`. Honest wrinkle in the byte record: the re-capture pass hit a transient fxtwitter 404 "User not found" on `@Broadcom` (the same handle had returned the full profile minutes earlier and a sleep-5 retry returned code 200 with the identical profile, id 338504881, 66,720 followers) - both the 404 and the retry are preserved in the raw file; the register row's handle_check rests on the two 200 responses.

All grades in `watch/inbox/luncheon_watchlist_20260929.jsonl` verified true for the 5 compute rows; **no watchlist row edits were needed** (unlike sibling lanes, which corrected two rows).

**Ask-vs-register discrepancy, stated plainly:** the ask said "resolve the 1 search-grade handle live", but zero of the 5 compute rows carry `handle_grade: search` (mine: 2 declared + 3 org). The 6 search-grade rows in the register belong to other lanes (Kratsios, Tom Brown, Walters, Clayton, McDermott, Cairncross). The lane performed live fxtwitter resolution of all 5 of its own handles instead. Also: the luncheon briefing (`watch/inbox/SUPER_INTELLIGENCE_LUNCHEON_20260929.md`) says "the 8 search-grade ones"; the register byte-count is 6. Not my rows to fix; noted for the follow-lane fold.

## Date honesty

- In-window legs carry recency markers, not byte-verified article timestamps, except the xAI row (fetch-grade date stamps off x.ai/colossus itself).
- Nvidia buyback: "8 hours ago" marker puts it Sep 29; a Jan 22 2026 "$150 Billion Buyback Bombshell" headline also surfaced, so whether Sep 29 is an incremental authorization is UNCONFIRMED - flagged in the row.
- Tan doubling-down: reported Sep 14-15; registered at window edge Sep 15 with the range stated.
- Micron HBM4-sold-out / 50-65% facts: undated in this search bundle; registered as standing context (trace to FY26 calls from Dec 2025), not fresh in-window statements.
- Broadcom targets, AMD Helios specs, older xAI buildout: dated outside the window, folded as `out_of_window_nearest`, never as in-window.
- One search returned an MCP 429 rate-limit mid-AMD-mining; the lane re-issued and completed. Sources are domain-level URLs where the search tool returned no full article slug - stated per row.

## Estate synthesis (the compute-economics read of the two weeks)

1. **Memory is the ratchet.** Micron HBM4 sold out through CY2026 + Rubin Ultra 1TB HBM4e + MI455X 432GB HBM4 all bid for the same die-stacking capacity. Rental prices above us cannot fall fast (supply capped by HBM), and our own hardware ladder costs more every month it waits (supercycle lifts used-GPU prices). The attic radar's ~$1,100-1,300 3090 quote is stale-dated 2026-09-01 and now reads optimistic.
2. **Diversification compresses input prices, not output prices.** AMD Helios ramping + Broadcom ASICs at $115B/$230B scale = more supply of tokens, which competitive pressure lands on input/cache pricing first. The AGENTS.md cost law ("only OUTPUT-token cuts are real cheapeners; cache-read is 20x not 5x") survives this fortnight's evidence intact.
3. **Compute is becoming pooled and politicized.** OpenAI-Nvidia safeguards, an Anthropic-on-Colossus banner, the whole stack at one White House table the day this lane ran. A sovereign local stack is the hedge position all of them implicitly validate: own weights, own compute, own meter.

## Checks

- Register append: `./.venv/Scripts/python.exe watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow_compute_append.py` - "appended 5 rows (writer=gala-follow-compute had 0 rows before)"
- Finish-line byte check: `./.venv/Scripts/python.exe watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow_compute_check.py` - see `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow-compute.check.txt`
- Ratchet: no code under `mag/` or `tools/` touched by this lane - `tools/violation_ratchet.py check --changed` not applicable, not run.

Read-only intelligence per the sensed-never-done law: findings banked, no engagement from estate surfaces.
