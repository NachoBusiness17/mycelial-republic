# LANE R4 — ABLITERATED / PHASE-6 QUARANTINE (2026-09-01 ~07:2xZ)
Full salon on the abliterated ecosystem for our fleet families. Dered first (receipts
abliteration_sweep 08-31 20:33Z + abliteration_ai_glm53_release 08-31 23:42Z), then fresh HF API sweeps.

## FLEET FAMILY — CURRENT STATE (HF search, 2026-09-01)
- **Huihui-DeepSeek-V4-Flash-0731-abliterated** → huihui-ai GGUF 574K dl, **license:mit confirmed** (cardData license=MIT). The original 08-31 receipt is current. Plus many mirrored GGUFs (CoreWolf 2.6K, kepom, Justbackup). VERIFIED.
- **Gemma-4-31B-abliterated** → wangzhang/it-abliterated 699K dl (Athena base, Apache) still the crown; huihui-ai now has **v2** (53.6K dl) beyond the 08-31 receipt. VERIFIED.
- **Qwen3.6-35B-A3B-abliterated** → BOTH engines live: Bahushruth v4 1.01M dl AND huihui-ai Apache-2.0 (24.3K dl) + NVFP4/MTP quant variants. The 08-31 sweep named only Bahushruth; huihui-ai official variant is the higher-fidelity pick. VERIFIED.
- **GLM-5.3-Flash abliterated** → **CONFIRMED EXISTS NOW** (the 08-31 receipt flagged "if exists"): lovesenko/GLM-5.3-Flash-tr3-4bpw-Abliterated, created 2026-09-01T04:26Z, **license:mit**, base zai-org/GLM-5.3-Flash, tr3 4-bit, 0 dl (hours old). Also orcarouter/dealignai "Uncensored-FP8" (1.5K/1.4K dl, MIT) — same lane, laxer method than proper abliteration. VERIFIED.

## UPSTREAM LICENSE MATTERS (self-host legality)
- zai-org/**GLM-5.3-Flash** = **license:mit** (1827 likes, 379K dl). Abliterating an MIT-weight then self-hosting is license-clean IF the derived-work clause is honored. VERIFIED.
- zai-org/**GLM-5.3** (full 753B sibling) = **license:other** (66K dl) — NOT permissive; abliterated full-model self-host = contract-uncertain. The abliteration.ai product rides THIS model but is **US-hosted API, FP8, 1M ctx, zero-retention, commercial** — weights NOT published (per provider self-report; flag: weights-vs-API unconfirmed). VERIFIED via provider.
- So GLM-5.3 **Flash** abliterated = quarantinable; GLM-5.3 **full** abliterated = provider/API lane, not weights custody.

## EVAL-HARNESS MATURITY
- treadon/abliteration-eval (Apache, 99 dl) = **<1K samples, text-gen, refusal/jailbreak benchmark — THIN**. No standardized harness in the ecosystem; eval is hobby-grade, not IEEE-grade. Treat harness results as indicative, not certifying. VERIFIED.

## PHASE-6 CUSTODY VERDICT (what belongs vs noise)
Belongs in quarantine (license-clean, mirror fleet exactly):
1. huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF (MIT) — current.
2. wangzhang/gemma-4-31B-it-abliterated (Apache) — current.
3. Bahushruth/Qwen3.6-35B-A3B-abliterated-v4 (Apache) + huihui-ai Qwen3.6-35B-A3B-abliterated (Apache) both.
4. **NEW:** lovesenko/GLM-5.3-Flash-tr3-4bpw-Abliterated (MIT) — add to Tier B grab.
5. Datasets: harmful-enriched (Apache), ShrimpMoss (MIT), abliteration_en (MIT), treadon eval (Apache). Skip scarysnake/code-refusal (CC-BY-NC).
Noise/not weights-custody: abliteration.ai GLM-5.3-large product → provider-mining lane (API), NOT quarantine; "Uncensored-FP8" forks (orcarouter/dealignai) optional at best — lax abliteration, skip for now.

## FLAGS / UNVERIFIED
- lovesenko GLM-5.3-Flash-abliterated = 0 dl, hours old, single maintainer → unproven; verify weights+base-compat before grab.
- Abliteration.ai GLM-5.3-large weights-availability unconfirmed (provider self-report only).
- HF downloads are HF-reported, not independently verified (as prior 08-31 flag).
- No legal opinion offered; MIT/Apache derivable-work clauses are the boundary. Self-hosting abliterated MIT weights = defensible; GLM-5.3-full (license:other) = do not touch.

## FETCH LOG (mandatory)
| ts | organ | probe | result | verif |
|---|---|---|---|---|
| 07:16Z | hf_api | search=Huihui-DeepSeek-V4-Flash-0731-abliterated | 574K dl, MIT confirmed via cardData | VERIFIED |
| 07:16Z | hf_api | search=gemma-4-31B abliterated | wangzhang 699K + huihui v2 53.6K | VERIFIED |
| 07:17Z | hf_api | search=Qwen3.6-35B-A3B-abliterated | Bahushruth 1.01M + huihui Apache | VERIFIED |
| 07:17Z | hf_api | search=GLM-5.3 abliterated + GLM-5.3-Flash | lovesenko tr3-4bpw abliterated (NEW) | VERIFIED |
| 07:18Z | hf_api | model zai-org/GLM-5.3-Flash | MIT (379K dl) | VERIFIED |
| 07:18Z | hf_api | model zai-org/GLM-5.3 | license:other (66K dl) | VERIFIED |
| 07:19Z | hf_api | dataset treadon/abliteration-eval | Apache, <1K, thin | VERIFIED |
| 07:21Z | hf_api | model huihui Qwen3.6 + Bahushruth recheck | both live | VERIFIED |
No two-strike bail needed (all HF API probes returned within budget).
