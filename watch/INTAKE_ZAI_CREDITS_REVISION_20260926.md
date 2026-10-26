# INTAKE — Z.ai coding plan → credits system, multipliers + off-peak grace (night shift card, glmwatch rotation, 2026-09-26)

**Deck:** glmwatch | **Find:** vendor's own notice (docs.z.ai/devpack/notice/
usage-revision, July 30 2026) — READ AT THE BYTES this fire. Score: 18/25 ROUTING
(pacing-law consequence, no build).

**The facts (vendor primary source):**
- Coding plans moved to **credits-based billing**; legacy plans protected to end of
  current billing cycle, then renew/upgrade only.
- Multipliers: **GLM-5.3 = 1× off-peak / 3× peak; GLM-5.3-Flash = 0.4× off-peak /
  1.2× peak.** Flash is the vendor's own discount door — our workhorse choice was
  correct, now provably 3× cheaper than full 5.3 off-peak.
- **Peak = Mon–Fri 14:00–18:00 SGT = 02:00–06:00 EDT.** Our night automation fires
  23:00/02:00/05:00 EDT — the 02:00 and 05:00 fires ride 1.2× flash peak. The 23:00
  fire is off-peak.
- 🌊 **Sept 25 – Oct 7 2026: ALL-DAY off-peak rates** (grace window) — ACTIVE NOW.
  Every token burned this fortnight is at the cheap rate regardless of hour.
- Legacy V2 weekly prompt-quota table: Lite ~80/5h ~400/wk; Pro ~400/5h ~2,000/wk;
  Max ~1,600/5h ~8,000/wk; one "prompt" ≈ 15–20 invocations. This reconciles with
  the 09-05 dashboard: the "10K credits/week" Lite pool IS the credits system.

**Route (pacing law updates):** (1) grace-window burn — anything expensive on the
z.ai lanes should fire BEFORE Oct 7 (off-peak everything); (2) after Oct 7, the
night-shift 02:00/05:00 fires ride 1.2× — the checklist's spend-light design is
already right, keep WebSearch-only sweeps; (3) lane-risk register row: vendor moved
billing terms mid-relationship — watch for multipliers changing AGAIN at renewal.

**Tri-state:** notice contents = Supported (read at the bytes, vendor domain).
Current billing behavior matching the notice = Supported (the 09-05 dashboard 6.42K/10K
row + this week's grace window both corroborate). Team-plan seat pricing relevance
to a future fleet buy = Unproven (no purchase decision on the table).

**Falsifier:** if the next legacy billing cycle ends and quotas/multipliers DON'T
match this table, the card downgrades to "notice ≠ implementation" and the lane-risk
row gets company.
