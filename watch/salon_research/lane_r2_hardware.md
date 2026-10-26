# LANE R2 — HARDWARE LEVER: is 128GB DDR4 (@$600) the best spend this quarter?
Date 2026-09-01 07:14Z · Cage: WSL2 on Ryzen 7 3800XT (8C/16T), 32GiB RAM, 1TB NVMe (~640GB free tonight), no GPU in cage. Host = Windows, **specs UNKNOWN**. Prices QUOTED+URL'd or UNVERIFIED.

**HEADLINE (blunt): the ~$600 RAM quote is UNDER street.** The 3800XT/consumer AM4 runs **non-ECC only** (IMC lacks ECC) → 128GB non-ECC new kit = **$800–950**, not $600. So either a stale/used/regional figure or a too-good deal. **$600 buys ~64GB today, not 128.** Verify the listing before spend. Ranking holds but RAM's edge shrinks at $850 not $600.

## 1. STREET (verified 2026-09-01)
- **128GB DDR4 (4×32) non-ECC**: $800–950 (A-Tech $904, Timetec $891, NEMIX $913–917; 2666 $799–854) — amazon.com search. **Operator quote ~$600 ≠ street → UNVERIFIED/flagged.**
- **ECC UDIMM 128GB**: $1,190+ — IRRELEVANT, AM4 no ECC (macsales/NEMIX).
- **20TB CMR HDD** (WD Ultrastar HC560): renewed **$328–630** ($16.40–31.50/TB); new $950–1,200 (datacenterdisk, diskdojo, storagediskprices).
- **4TB NVMe Gen4 QLC**: **$470–490** ($117–122/TB: Lexar NQ780 $468, SP UD90 $490); TLC $600+ (cheapestssd).
- **Used RTX 3090 24GB**: **$1,100–1,300** (med ~$1,200; +35% MoM, AI demand) — pcprice.watch, siliconcomps, ebay sold.
- **RTX 4090 48GB-mod**: **$2,500–5,500** (USA-mod $3,990–5,555; Chinese $3,800–4,600; used ~$3,600) — no warranty, high fail — ebay.co.uk/227143676586, techpowerup.
- **Used RTX A5000 24GB**: **$1,700–2,500** (typ $1,800–2,200) — gpudojo/a5000, ebay.

## 2. WHAT EACH LEVER UNLOCKS
- **128GB RAM**: in-cage serving of **GLM-5.3-Flash IQ1_M 90.9 / IQ2_XXS 94.9 / IQ2_K_XL 101.3 / IQ3_XXS 112.1 GiB** (measured, glm53flash_quant_menu) via 18B-active MoE → **2–6 t/s CPU serving on own weights** on existing 16T. Cheapest "local fleet on our weights THIS QUARTER." No VRAM → no FreeToken edge-MoE.
- **RTX 3090 24GB**: **FreeToken edge-MoE + probe + fine-tune forge (QLoRA 7B–13B)** — the ONLY capability no subscription sells (keep own weights). Load-bearing = 27–34B MoE at Q4 25–80 t/s; 70B/120B does NOT fit single 24GB. Cage/g WSL2 caveat: card must live on Windows host, not cage.
- **4090 48GB-mod**: 48GB → bigger quants/batches, but 3–4× the 3090 for 2× VRAM, no warranty. Skip.
- **A5000**: 24GB like 3090 at $1.7–2.5k = $500–1,300 premium for ECC/stability we don't need. Skip.
- **20TB HDD (~$328 renewed)**: Phase 4 full-precision cold archives (DS-V4-Flash 570GB + GLM-5.3-Flash 640GB + gpt-oss-120b 130GB + DS-V4-Pro 1.3TB) + DataComp-LM banking per WEIGHTS_PLAN trigger. Sovereignty/provenance, NOT serving.
- **4TB NVMe (~$470)**: warm-cache nicety, not structural.

## 3. RANK, estate-$/$
1. **128GB RAM (~$850 real / $600 quoted)** — turns paid cage into live in-house fleet on GLM-5.3-Flash our-weights NOW. Rank 1.
2. **20TB HDD (~$328 renewed)** — cheapest capable; completes phase-4 custody + DataComp. Sovereignty-dollar, doesn't serve.
3. **Used 3090 (~$1,200)** — highest capex, ONLY forge+capex capability; dead-as-cost-play, live-as-capability/sovereignty (HARDWARE_RADAR verdict). Host-placement friction.
4. **4TB NVMe (~$470)** — nice, not structural.
5. **A5000 (~$1,700–2,200)** — 3090 at 1.5–1.8×. Skip.
6. **4090 48GB (~$3–5.5k)** — 3–4× 3090 for 2× VRAM, no warranty. Skip.

## 4. CHEAPEST "LOCAL FLEET ON OUR WEIGHTS" THIS QUARTER
**RAM-first in cage (~$850, or $600 if quote real)**: verified non-ECC 128GB → 3800XT/AM4 → serve GLM-5.3-Flash IQ1/IQ2 on 16T → own-weights Tail + probe + daily-driver at 2–6 t/s. Add **20TB renewed (~$328) as phase-4 follow** for full custody. GPU (3090) deferred to the forge/FineToken need-gate. **RAM+drive ~$1,180 serves AND stores — strictly more estate per $ than $1,200 3090 alone this quarter.**

## 5. FLAGS
- **UNVERIFIED**: host Windows GPU/PSU/case compat; power rate; the $600 RAM listing itself (street $800–950); 3800XT 4-DIMM may downclock / need manual tuning; verify board QVL+BIOS for 128GB before buying.
- GPU into WSL2 cage ≠ GPU on Windows host (Mag venv on Windows) — placement decides what the GPU serves.
- Storage already at ~640GB tonight; RAM+drive buys *future* phase-4 room (~2.5TB), not tonight's custody.

## FETCH LOG
6 web_search calls (grok-provider, untrusted wrappers treated as leads, cross-tagged vs held HARDWARE_RADAR + glm53flash_quant_menu). Zero blocks, no two-strike bails. Held data reused not re-fetched. Board-only; no messaging.
