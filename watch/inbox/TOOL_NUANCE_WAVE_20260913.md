# TOOL NUANCE WAVE — FOLD (2026-09-13, operator GO "20 wide")

**Wave receipt:** 20 lanes, one tool/model family each (memory/runs/tool_nuance_wave/pack.md). Flight 1: 14/20 clean in 59.9s. Flight 2 (repair, rotate-not-retry): 6/6 clean in 37.9s. Lanes: ling-3.0-flash-sante:free ×9, longcat-2.0:free ×5, laguna-s ×2, deepseek-chat ×2 (~$0.01), fin ×1, returns in memory/runs/tool_nuance_wave/returns/. **Wave cost ≈ $0.01.** Casualties: `stepfun/step-3.7-flash:free` and `upstage/solar-pro4:free` went HTTP-400 stale since the 09-12 head-museum run — free-lane slugs rot in <2 days; freshness check before every wave.

**Primary-source receipts pulled seat-side:** fal's own pricing docs confirm billing is **output-based** — per image, per megapixel, or per second of video (fal.ai/docs/documentation/model-apis/pricing), with a pricing API endpoint (fal.ai/docs/platform-apis/v1/models/pricing). Public nano-banana-lite edit is **~$0.034/image** (Google launch pricing) — the platform's $0.00 row diverges from public pricing.

## THE NUANCES THAT CHANGE BEHAVIOR (tri-state)

1. **THE SHEET'S STICKERS ARE FLOORS, NOT PRICES.** Video rows are **per second of output**: veo3.1 5s clip ≈ **$2.10**, kling 4k 10s ≈ **$4.41** — 5-10x the number the sheet shows. Image rows are per image **at default resolution**; a 4-image batch or 2x-res render multiplies units. [Supported: fal pricing docs + L01]
2. **$0.00 EDIT ANOMALY SHARPENED.** google nano-banana-2-lite.edit $0.00 sits against public pricing of ~$0.034 and a $1.05 sibling on the same platform row. Ranked causes (L02): loss-leader promo > SKU metering bug > restricted backend (watermark/low-res) > hard cap. falsifier: 50-edit burst + invoice CSV + watermark inspection. If real, it's a free image-edit organ. [Unproven, test ≤ $0.00]
3. **KREA 55x GAP.** fal's krea row has no style-ref SKU (direct itemizes it at +$0.005) and unit semantics are undefined — could be per-step, not per-image. Falsifier: identical prompt both surfaces, hash-diff outputs; if identical, fal always wins bulk. [Unproven, test ≈ $0.06]
4. **TEXT-IN-IMAGE IS THE TIER DISCRIMINATOR** (L09/L10/L11 converge): cheap tiers ($0.005-0.08) re-render glyphs as gibberish; mid ($0.15 nano-banana-pro) holds short strings; premium ($1.05 gpt-image-2) is the only reliable long-string edit. And the pro-edit premium's real product is **identity preservation across an edit chain** — the most expensive failure mode in game-asset pipelines. Cheap band for palette swaps/prop variants; pro only when the face must survive. [Unproven per-tier, one 3-constraint ladder test ≈ $1.15 settles all four rungs]
5. **PREMIUM VIDEO'S TWO REAL JUSTIFICATIONS** (L07): **native synced audio** (veo3.1 — penny lanes output silent video) and **true 4K delivery** (kling v3). For B-roll, pre-viz, social loops, storyboards: seedance/grok/pixverse pass the threshold. Wow-surface-only rule: CONFIRMED, with the audio exception named. [Supported]
6. **TTS CHAR-vs-TOKEN INVERSION** (L14): tts-1 per-char ≈ $0.00006/token-equivalent vs token-billed speech $0.0000126 — **~4x cheaper per sentence on the token side**. A 10K-char script: $0.30 on tts-1-hd vs ~$0.03 token-billed. Inverts on symbol-heavy text (URLs, code). hd premium only pays listener-facing >10s. [Supported math, per-content flip Unproven]
7. **TRANSCRIBE INVERSION CANDIDATE** (L15): GPT-4o transcribe at $2.62/1M in + $10.50/1M out may be **~2-3x CHEAPER than whisper's $0.0063/min** for standard speech (150 words/min ≈ $0.0037) — AND it natively diarizes and streams, which whisper doesn't. Weak link: the audio-tokenization rate is assumed. Falsifier: one 1-min file through both, read usage. [Unproven — but if true, the sheet's "100x premium" row is actually the bulk lane for diarized work]
8. **BROWSER USE CROSSOVER FORMULA** (L16): bandwidth dominates when **KB > 4.4 × seconds**. Modern SPA = 1-3MB before interactivity → one page can out-cost a minute of session. Text-only/DOM extraction keeps crawls minute-priced. [Supported arithmetic; per-page MB figures Unproven]
9. **MODAL** (L17): per-second billing, 1s minimum; snapshots kill cold starts; memory at $0.0084/GiB-hr means a 10GB model idles for **$0.084/hr** — cheap enough to keep warm; egress is the hidden fee. Burst-rent only when local queue depth > 0 or hardware class is missing. [Supported]
10. **FIRECRAWL** (L18): JS-rendered pages cost 2-3x credits; `cache=True` = free repeats within ~24h; anti-bot retries multiply credits. Plain fetch beats it for static pages. [Supported docs, retry multiplication Unproven]
11. **FAL QUEUE OPS** (L19): **zero volume discounts** — 20-wide costs exactly 20x linear; webhooks are at-least-once → no idempotency key = double-bill on retry; sync endpoints for sub-30s stills, queue+webhook for video; 20-wide polling risks a thundering-herd 429. [Supported]
12. **WHISPER TRAPS** (L13): 25MB file cap ≈ ~25 min/upload (the "$1 = 158 min" math needs chunking); hallucination-on-silence fills gaps with confident gibberish that passes visual QA — transcript receipts mandatory. [Supported]
13. **TURBO-TIER PROMPTING** (L04): negative prompts lose efficacy in few-step distilled models — prompt strictly positive; hands/text/multi-subject are the quality floor. [Supported literature]
14. **RECRAFT V4 IS THE SONNET-OF-IMAGES** (L12): 240x krea, justified ONLY for vector/SVG output or brand-locked assets; fleet bulk never touches it. [Supported]
15. **THE PRICING-TABLE AUDIT ORGAN** (L20 — reusable on any future sheet): six patterns = loss-leader ($0.00 under $1.05 sibling), distillation dumping (old SKU below marginal cost), mispriced rows (lite 12x full — likely unit mismatch), unit redefinition (same tool, two meters: min vs GB), tier cannibalization (v3 $0.0315 → v4 instant $0.0053), judgment-bait (equal prices, different brand anchors). One-line probe per pattern in returns/L20.

## GO-GATED RECEIPT TESTS (the "nail the nuance" menu — total ≈ $3.70, mostly test 4)

| # | test | cost | settles |
|---|---|---|---|
| 1 | 50× nano-banana-2-lite.edit burst + invoice read | $0.00 if real | the free-edit organ |
| 2 | veo3.1 1s vs 5s clip | ~$2.50 | per-second metering |
| 3 | krea same-prompt A/B: direct vs fal | ~$0.06 | the 55x arbitrage |
| 4 | 3-constraint edit ladder (qwen/nb2/nbpro/gpt-image-2) | ~$1.15 | the edit-tier map |
| 5 | whisper vs gpt-4o transcribe, same 1-min file | ~$0.01 | the transcribe inversion |

Spend gate = operator. Tests 1+3+5 are sub-penny combined.

---

[CORRECTION 2026-09-13, seat: the casualty line above mis-reads the failure. The step/solar HTTP-400s are NOT fresh staleness — the lane-arm recipe (reference-lane-arm-firing-recipe) documented them on 09-12: gated listings requiring a Nous-specific tags param; "CATALOG LISTING ≠ SERVABLE." The seat re-fired them anyway and ate the same 400s — a read-the-row failure, the known root costume. Original line kept per drift law. Practical law, twice-confirmed now: minimal-payload probe any zoo row BEFORE routing a wave to it.]
