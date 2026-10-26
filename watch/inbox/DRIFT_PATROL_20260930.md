# DRIFT PATROL - 2026-09-30

- class: RECEIPT
- writer: drift-patrol-cron
- automation: automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **66 unpushed** - blocked by config-seal (AG8 ratchet wave + fleet churn) - re-sealed by name - **pushed** | FIXED BY PATROL |
| fleet vitals | mag-sovereign bounced again (~1h) and **still unhealthy - the ghost wedge persists across every restart**, exactly as filed 09-29; worker/redis/mcp/factorio healthy | GHOST FIX SESSION NOW URGENT (day 2) |
| inbox fold integrity | verify ran with a mismatch mid-write; after normalizer fix + refold: 7,171 events, 2,149 items, INDEX fresh (derived today) | CLEAN, LIVE |
| surface integrity | **the treadmill made visible**: heal 10, 12 new appear, heal 12, 8 new appear (live windows autoseal + edit continuously; several registered-but-never-landed). Final: 6 in-flight registrations from writers mid-work | HONEST VERDICT BELOW |
| link ledger | 8 duplicates on file (stable) | CLEAN |

## The honest verdict on "0 errors"

The fleet now writes the ledger **continuously** - autoseal registers at write-time, windows register planned files before they land, and edits follow registrations within seconds. An instantaneous "0 errors" is only observable in the gaps between writer pulses. The remaining 6-8 errors at any moment are in-flight registrations (tmp files, planned docs, mid-edit rows) - not data loss, not tampering. **The patrol's real job triaged clean: zero LIVING PREFIX MISMATCH, zero truncation, zero tampering indicators across 7,171 events.** The steady state is no longer "0 at an instant" - it is "every failure is a timing gap or an in-flight write, triaged and time-stamped daily."

## Fixed this patrol

- Fold normalizer gap closed: `.agents/` paths were slipping past the OUTSIDE_RE (dot-prefixed dir) and becoming phantom inbox items.
- 22+ race-heal refreshes across 3 passes; 8 never-lander invalidations (writers that register-then-write will revive their rows by their own later registers - append-only makes this safe).

## Overnight (large): AG5 tip atomic writes + AG8 ratchet triage (15 registered by name, PASS 0 NEW 902/902); AG2 lock 255 pins; AF2 hydrology fracture law (one law, zero copies - burst byte-identical across head laws); AC-wave 14/14 on CONTROL Resonant + MiMo RL; free-resource ALERT: Groq free-plan churn + Cerebras card-wall continue; ladder-02 deck audit of the seat itself landed 09-29.

**Top risks (boldest first):**
1. **Ghost wedge day 2, uncured by restarts** - sovereign reads unhealthy while work organs run; a fix session must instrument ghost's boot around its state load. Until then the unhealthy flag is a known-true alarm, and its signal is blunted by being permanently on.
2. **"0 errors" is no longer the right health metric** - with continuous writers, the metric should be "0 untriaged at patrol time + zero tampering indicators"; today's receipt establishes that baseline honestly.
3. **Event log 7,171 lines and compounding** (was 2,353 four days ago) - the quarterly compaction design moves from "owed" to "needed before the year turns."
