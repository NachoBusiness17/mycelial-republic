## PRICING & BILLING RECEIPTS (09-04, operator billing table paste — 2026-09-03 rows)

Two keys, two economies:
- **3254...c7fd = API-with-balance key (cash pricing, "Postpaid"):**
  - glm-5.3: INPUT $0.0014/kTok · OUTPUT $0.0044/kTok
  - glm-5.3-flash: INPUT $0.000075/kTok · OUTPUT $0.00025/kTok (18.7x / 17.6x cheaper than 5.3-full)
  - glm-4.5-air: INPUT $0.0002/kTok · OUTPUT $0.0011/kTok · CACHE $0.00003/kTok
  - glm-4-32b-0414-128k: NORMAL $0.0001/kTok (night B-engine burned 1.31M tok = $0.13)
- **4f8a...6464 = GLM Coding Lite V3 - Yearly PACKAGE key (all rows $0 cash, credits consumed against package):**
  - 5.3-flash night bay traffic: 573,842 INPUT + 130,511 OUTPUT + **12,353,152 CACHE** tok, 75 calls → 44.21 + 34.98 + 231.75 credits
  - 5.3: 422,248 IN + 6,043 OUT + 2,509,696 CACHE → 97.60 + 4.86 + 142.93 credits
  - web-reader plugin: $0.01/time → 1.2 credits/call

**CACHE ECONOMICS (receipted):** cache reads are $0/kToken cash but METER PACKAGE CREDITS —
12,353,152 cached tokens = 231.745 credits ≈ **53.3K cached tokens per credit** (5.3-flash
Lite). The resident-worker/cache-farming doctrine is confirmed and now has a metered rate:
a cache-heavy night bay spends package credits, not cash, at ~19 credits per million cached
tokens. Watch the weekly/5h Lite windows (2,000/10,000) against this rate.

**CAMPAIGN-WINDOW TENSION (tri-state):** the 5.3-flash Lite rows SHOW credits consumed
(44.21+34.98+231.75) on 09-03 — if the "23:00-09:00 zero-quota via ZCode" campaign applied
to these calls, the rows would presumably show 0. Either the bay traffic ran outside the
window, or the campaign doesn't zero the package-credit meter. Resolves only with an
in-window vs out-window row comparison — still Unproven, dashboard read stands.

**KEY INVENTORY CORRECTION:** ZAI_API_KEY_Lite (4f8a...6464) is NOT a raw balance key —
it IS a GLM Coding Lite Yearly package key. The empirical 50/50 concurrency pass (09-04)
therefore measured the LITE PACKAGE's concurrency: Lite carries >=50 in-flight on
5.3-flash. Plan-door row for LITE: RECEIPTED empirically. Pro's package concurrency:
still unread.

### PRO/MAX PACKAGE RECEIPTS (09-04, operator billing table — key e18f...617f, "GLM Coding Max V3 - Quarterly")

**THE ZERO-QUOTA CAMPAIGN ROW IS RECEIPTED:** glm-5.3-flash NORMAL — **32,262,464 tokens,
162 calls, $0.00, Credits Consumed 0.000000, no package attached** (09-03 row). The
"23:00-09:00 SGT zero-quota via ZCode" night window is REAL and meter-zero. "ZCode" as
this CLI is now Supported-by-billing-shape (a 32M-token row escaping both cash AND package
credits has no other explanation on file).

**CREDIT RATES (tokens per credit, measured from Pro rows):**
- 5.3-flash INPUT: 31,324,562 / 2,544.50 = **~12,312 tok/credit**
- 5.3-flash CACHE: 424,643,328 / 8,428.51 = **~50,381 tok/credit**
- 5.3-flash OUTPUT: 1,354,539 / 377.20 = **~3,591 tok/credit**
- 5.3 INPUT: ~3,767 tok/credit · 5.3 CACHE: ~14,748 tok/credit

**SWARM BUDGET MATH (Max package = 28,000 credits/5h + 140,000/week):**
- input-shaped work: 140K cr x 12,312 ≈ **1.72B input tokens/week**
- output-shaped work: 140K cr x 3,591 ≈ **503M output tokens/week**
- cache-shaped work: 140K cr x 50,381 ≈ **7.05B cached tokens/week**
- At ~500 tok/wing-request that is order **~480K wing-requests/day** on the Pro lane alone
  (before the Lite package, before the night zero-quota window, before free lanes).
- Observed spend: the bay's real 09-03 traffic (~600M tokens across cache+input) consumed
  ~17K credits — the swarm is ALREADY running inside the package with headroom.

**CONCURRENCY on Pro:** 1,081 flash calls on 09-03 through the package; the Lite package
measured >=50 in-flight empirically. Pro's per-window concurrency: expect >= Lite
(one more dashboard cell, non-blocking).

### CONCURRENCY APPENDIX — FULL TABLE (09-04, operator verbatim paste of rate-limits page; completes the fleet-rows-only receipt above)

Header caveat, verbatim: "The model concurrency on this page is only applicable to API users
with balance consumption. GLM Coding users please refer to the package benefits."
→ Our Lite/Pro PACKAGE keys do NOT ride this table; their limits = package benefits
  (Lite empirically >=50 in-flight on 5.3-flash, measured 09-04). This table governs
  balance-consumption API keys only.

Full model rows (concurrency):
GLM-4.6=3, GLM-4.6V-FlashX=3, GLM-4.7=2, GLM-Image=1, GLM-5-Turbo=1, GLM-5V-Turbo=1,
GLM-5.1=10, GLM-5.2=10, GLM-5.3=5, GLM-5.3-Flash=50, GLM-4.5=10, GLM-4.6V=10,
GLM-4.7-Flash=1, GLM-4.7-FlashX=3, GLM-OCR=2, GLM-5=2, GLM-4-Plus=20, GLM-4.5V=10,
GLM-4.6V-Flash=1, AutoGLM-Phone-Multilingual=5, GLM-4.5-Air=5, GLM-4.5-AirX=5,
GLM-4.5-Flash=2, GLM-4-32B-0414-128K=15, Web-Reader=5, Search-Prime=5,
Search-Prime-Claude=5, CogView-4-250304=5, GLM-ASR-2512=5, ViduQ1-text/Image/Start-End=5,
Vidu2-Image/Start-End/Reference=5, CogVideoX-3=1. Higher limits: application form.

NEW-LANE CANDIDATES this table reveals (never probed, all on keys we hold):
- GLM-OCR (2): OCR lane for the intake — untried.
- Search-Prime / Search-Prime-Claude (5): vendor web-search API — candidate behind the
  invariant-hunt queries; billing rows show the operator already pays $0.01/search on the
  Max package (search-prime-claude 28 calls receipted).
- Web-Reader (5): vendor reader — the intake fetcher's fallback of last resort.
- GLM-4.7-FlashX (3) vs GLM-4.7-Flash (1): a 3x-concurrency sibling of the cache-mining lane.
- GLM-ASR-2512 (5) / Vidu2 family (5): audio/video lanes — someday-docket.
SELF-STEAL CORRECTION FILED 09-04: the dashboard-read request was redundant — both answers
(concurrency here, zero-burn in the billing rows) were already in hand. Shelf-before-ask.

**FILING NOTE 09-04 (late):** the operator's second delivery of this table was filed as a
self-steal miss. Re-filed under the correct law: DUPLICATION IS EMPHASIS. Two independent
deliveries of the same table = double-attested numbers, not a redundant paste. Amendment 4,
watch/INTAKE_RUBRIC_20260903.md.
