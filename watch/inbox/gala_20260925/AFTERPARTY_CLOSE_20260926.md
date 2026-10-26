# AFTERPARTY CLOSE - 2026-09-26 (window closed by operator)

THE GALA + AFTERPARTY totals for this window:
- GALA: 36/36 lanes danced, 36 LINKS rows, ~38M witnessed agent tokens, widths 3-6-12 clean.
- AFTERPARTY: 94 lane JSONs banked (dispatch chain self-fed from the gala's own decision
  ledger), zero outstanding at close, 2 rate-limit deaths at width ~15 refired to completion,
  1 more at 12 after a burst (rolling-throughput law recorded).
- Envelope law measured, not guessed: Task agents clean at 3/6/12; ceiling between 12 and 16;
  after a burst even 12 gets 1302s until the window decays. On any 1302: hold fires ~10 min.
- Commit: 790145ab1 (whole night, one sweep).
- Seal: 47/47 PASS, re-sealed by name zcode-gala-afterparty-closer-20260926 after the
  operator reviewed the masked 17-provider surface in chat (saelis ghost caught by him).
- Ratchet: 9 hits registered by name at close, check PASS 875/875.
- Provider health probe added to doctor (route-correct per provider; saelis dormant:true,
  cited to the operator's browser probe). Quote hit-rate meter landed: 52% standing number.
- Battery: frozen rerun 12/12 twice (one disclosed Q3 grep caveat lifted by the clean rerun),
  graduated to tools/battery_rerun.py, registered in the harness.
- Ghost lanes caught by operator probes: saelis (dead, dormant-marked), MagImproveDaily
  (Disabled, re-registered Ready by t8, doctor + improve --status now both surface it).

LEFT RUNNING / NEXT WINDOW:
- Morning-after wave at T+24h per watch/inbox/GALA_MORNING_AFTER_PREREG_20260926.md.
- Operator-gated: providers.yaml historical attestation note (this re-seal covers current
  bytes; if older drift matters, say so), referee GO unspent, Studio playtest Sep 29.

## AMENDMENT 2026-09-26 (B2-25 envelope re-measure, appended only, originals above untouched)

- Burn wave 20260926 measured a new rung: Task agents width 10, two waves back-to-back
  (11:24:57Z and 11:48:23Z). Wave 1: 10/10 completed clean, 37,386,533 witnessed tokens
  in 1229.9 s = 109.4M tok/h. Wave 2 at measure time: 8/10 completed (22.8M tokens,
  partial 85.6M tok/h), 2 still running. Zero 1302 in any agent output of the session.
- Clean ladder now reads 3-6-10-12 (width 10 was previously untested between 6 and 12).
- The rolling-throughput penalty (1302 at 12 after a burst) did not trigger at width 10
  across three waves fired within 37 min (wave gaps 176.9 s and 762.7 s).
- The 15-16 ceiling rung stays untested by this burn; today's data neither confirms nor
  overturns it.
- Blind spot named: the main-session retry path (maxAttempts 11,
  corpus/steal/TETHERED_LINK_STEAL_20260925.md) can absorb a 1302/429 without a
  lane-visible trace, so "zero recorded" means zero surfaced, not proven zero occurred.
- Full timing table + citations:
  watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md

## AMENDMENT 2026-09-26 (B2-97 width-15 probe: precondition checked, NO operator GO, wave NOT fired, probe armed)

- B2-97 ran its precondition sweep 2026-09-26 18:20-18:27Z: QUEUE.md, this receipt and all
  2026-09-26 burn receipts carry no explicit operator GO for width 15 (the header operator order
  is a generic burn order; this file's operator-gated list names attestation, referee GO and the
  Sep 29 playtest only). Per the lane's own "when operator-ordered" gate the wave was not fired.
- The 15-16 ceiling rung therefore remains untested and the clean ladder stands 3-6-10-12,
  unchanged by this lane.
- Probe armed, not fired: the ready-to-fire card with the full harvest plan (15 Task agents, one
  wave, metadata.json durations/tokens/tool_uses, 1302 + 429 grep over all agent outputs,
  amend-this-block either way, no refire inside the probe) is
  watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md. Fire only on an explicit
  operator GO for width 15.
- Receipt: watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md

## AMENDMENT 2026-09-26 (B2-476 proven-width table + source-cited envelope contract, appended only)

The envelope law is a function of (transport retry budget, width, window burst
state), never a width constant. Proven-width table, every row receipt-cited:

| window | transport | outcome | citation |
|---|---|---|---|
| 50-wide, 9/25 18:59Z | workflow children (maxAttempts 0) | 1302 STORM (1,838 429/1302 log lines; fake "subscription" crashes) | corpus/steal/TETHERED_LINK_STEAL_20260925.md:10-16 |
| 3/6/12 Task agents | main session (maxAttempts 11) | clean | AFTERPARTY_CLOSE above (widths 3-6-12 clean) |
| 10 x3 waves in 37 min | Task agents | clean, 109.4M tok/h, zero surfaced 1302 | watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md |
| ~15 | Task agents | 2 rate-limit deaths, refired to completion | AFTERPARTY_CLOSE above |
| 12 after a burst | Task agents | 1302s until the window decays (rolling throughput) | AFTERPARTY_CLOSE above + memory/burns/LEDGER.jsonl afterparty-94-lane-churn row |
| 10-12 outstanding lanes, all day 9/26 | dispatcher-held flash lanes | sustained, no account death | memory/burns/BURN_WAVE_STATE.json + memory/burns/LEDGER.jsonl |
| dwf children 9/20-9/26 | workflow children (maxAttempts 0) | 896 network failures, 817 of them the 1302 shape, 11 terminal actors in 2 runs, zero tally visibility | watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md |

UNANCHORED rows (claimed by the B2-477/B2-476 briefs, no receipt found in this
lane, do not cite as measured): "THE 50: 50-wide clean", "afterparty 24-agent
continuous windows", "today 12-wide with 1,741 absorbed". Anchor them by
receipt before citing.

CONTRACT (source-cited, supersedes any constant cap):
1. Clean rungs are MEASURED per transport: Task agents 3/6/10/12 clean; 15-16
   untested; workflow children have NO measured clean rung on this account
   (their only data points are storms).
2. Rolling throughput is the binding constraint after any burst: even a clean
   width takes 1302s until the window decays; hold fires ~10 min on 1302.
3. Workflow children inherit zero absorption (maxAttempts 0): their safe width
   at ANY window state is strictly below the Task-agent rung of the same day;
   B2-443 measured their failure surface invisible to the tally.
4. Off-peak earns more headroom; the 15-16 rung stays untested without an
   operator-ordered probe (B2-97 precondition law).
