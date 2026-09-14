# ECONOMIST VERDICT — Self-Host GLM-5.3-Flash (vast) for Driver Lane?
*Economist, 2026-09-01 19:44Z. Every number VERIFIED (source) or UNVERIFIED. Verdict: BAD IDEA.*

## 1. VRAM math (Q4 ≈ 160–180GB, 320B MoE @ ~18B active)
| Config | Aggregate VRAM | Hosts Q4? |
|---|---|---|
| 1×24–48GB (RTX PRO 6000 96GB IS single-card cap) | 24–96GB | **NO** — 96GB card alone can't hold 160-180GB |
| 2×80GB (A100/H100) | 160GB | **MAYBE** — only tight IQ4_XS ~155-167GB, ZERO KV/batch headroom (UNVERIFIED community, oflight.co "3×H100 ~240GB realistic min") |
| 4×48GB (A40/RTX-class) | 192GB | **YES** — fits + headroom via TP |
| 3–4×H100 (80GB) | 240–320GB | **YES** — comfortable |

**Community Q4 decode (8×L40S): ~46.93 t/s (antirez/ds4 QA, UNVERIFIED).** Real configs: single-stream ~30–60 t/s; providers 41–49 (z.ai) to 200–293 (Nebius/Baseten) t/s (Artificial Analysis, UNVERIFIED).

## 2. Rental $/hr vs API — BREAK-EVEN (list: in $0.15/out $0.50/M → blended $0.185/M for 90/10 in/out mix)
API promo to 09-09: in $0.075/out $0.25/M → blended $0.0925/M.
Break-even tokens/hr = `rental$/hr ÷ (api$/M ÷ 1e6)`:

| Config | $/hr | break-even tok/hr (list) | break-even (promo) |
|---|---|---|---|
| 2×A100-80GB | $0.80–1.86 | **4.3M** | 8.6M |
| 4×48GB | $1.20–2.80 (est) | **6.5M** | 13M |
| 3×H100 | $5.82–11.46 | **31M** | 63M |

## 3. Throughput ceiling (hosted 18B-active MoE Q4)
Single-stream multi-GPU TP: ~162–169K tok/hr (45 t/s). With concurrency/batching ~4–5× → **~650–720K tok/hr realistic ceiling (UNVERIFIED).**
**That's 6–130× BELOW break-even.** Even at max concurrency, we clear only ~720K vs the 4.3M minimum to match 2×A100 at list — and promo API is 10–90× further out of reach.

## 4. VERDICT: **BAD IDEA.** No window worth hosting.
- **Trigger condition would need:** rental that low + sustained >4.3M tok/hr volume. We never approach that; our driver+fan-out runs ~$0.50/M effective (MEASURED: $0.07 per 7-pack wave ≈ 140K tok), and volume is bursty, not continuous.
- **Kill criterion (if ever reconsidered):** rental ≥ $0.40/hr/card for the 2×A100 config, or sustained <1M tok/hr, or API promo resets below rental floor — re-evaluate. Not active — no cage.
- **CAGE LAW:** hosting needs a new GPU cage on vast — violates "ONE supervisor / no new cages / no second gateway." Dead before the math.

## 5. gpt-oss-120b (~117B MoE ~5B active, ~60GB Q4) as driver host — **BETTER FIT, still not worth it**
- Fits **1×80GB (A100 $0.40–0.93/hr)** or 2×48GB — **single card, no TP overhead**, 3–4× cheaper config than 5.3's 2-card minimum.
- ~5B active = **~3.6× more throughput per card** than 18B-active 5.3 (rough active-param scaling, UNVERIFIED).
- **BUT same cage-law violation + still ~$0.40–0.93/hr vs $0 free marginal on our z.ai/together free-ish lanes.** API wins. gpt-oss-120b is the RIGHT model (Cheaper/active) but the WRONG venue (vast) — keep it on cerebras/together/ollama, not a rental cage.

**Bottom line: API on z.ai (promo) / together / cerebras already delivers 5.3 and 120b-class MoE at ~$0 marginal. Self-hosting on vast buys us nothing except a GLM-5.3-specific lane we already get cheaper via API — plus a cage-law breach. Hard NO.**
