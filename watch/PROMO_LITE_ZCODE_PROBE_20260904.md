# PROMO PROBE RECEIPT — Lite key in ZCode, promo window (2026-09-04)

**Hypothesis under test**: the GLM Coding **Lite** key, called from ZCode during
the promo window (Sep 3–20, 8AM–6PM PT), gets the same "In ZCode: Unlimited
GLM-5.3-Flash" treatment as the Pro/Max keys — i.e. its billing rows land
$0 / 0 credits in-window.

**Probe** (single call, $0-budget, fired 11:2x AM EDT = inside window):
- endpoint: api.z.ai/api/coding/paas/v4 (coding-plan door, same as lite_lane_probe.mjs)
- model: glm-5.3-flash, thinking low, max_tokens 1536
- result: **HTTP 200, alive** in 4.1s
- usage: prompt 19 tok (0 cached), completion 79 (76 reasoning + 3 visible), total 98
- aliveness: Supported. The Lite key rides the coding-plan door fine in-window.

## What this receipt does NOT prove
Aliveness ≠ promo coverage. The CONFIRMING receipt is the **billing row**: if
the promo covers Lite-in-ZCode, this call (and today's other Lite traffic)
should appear as **$0 / 0 credits / promo-class**. If the row shows credits
consumed, the promo is Pro/Max-only and the day-shift Lite economy collapses
back to Max-only — which changes the 10-Lite-accounts-vs-one-Max math the
operator ran this morning.

## Next confirming step (operator hand or tomorrow's check)
One glance at the GLM billing dashboard tomorrow morning: read today's Lite
glm-5.3-flash rows. $0/0cr = promo covers Lite (Supported). Credits burned =
promo is Max/Pro-only (Disputed). Either way this file carries the verdict
line when it lands.

Probe script: scripts/promo_lite_probe.mjs (single-shot, no loops, key never
echoed — read from .env at runtime only).

---

## VERDICT LANDED (2026-09-04 ~23:0x EDT, operator's dashboard screenshot)

**Promo is Max/Pro-only. Lite pays real credits. DISPUTED → resolved FALSE.**

Confirming evidence (operator's own z.ai manage-apikey dashboard, Lite key page):
- Weekly limit: **6.42K / 10K credits consumed** (window 2026-08-29 → 09-04, includes 2 promo days)
- Key died DURING the promo window: the Lite-lane driving window stopped loading, operator: "we blew through its credits, it's out"
- Lifetime on the key: 304.5M cumulative tokens, peak 106.59M (08-29), 4d current streak
- 5-hour bucket showed 0/2K (fresh reset) while weekly sat at 64% — the weekly pool is the binding constraint
- **1 unused weekly quota reset in pocket** (resets expire; also resets the 5h bucket when spent)

Nuance for the record: the weekly counter spans pre-promo days too, but the key
dying mid-promo while the churn lanes were actively grinding Lite is the direct
read: credits moved during the window. Promo coverage would have landed $0/0cr.

**Consequence**: the 09-04 morning math ("10 Lite accounts vs one Max") flips —
Lite is not free ride-along capacity, it is a metered 10K-credits/week pool
(≈1.4K/day pacing or it dies mid-week). Day-shift Lite economy collapses back to
Max-only until more Lite accounts are bought WITH the metering in mind.
