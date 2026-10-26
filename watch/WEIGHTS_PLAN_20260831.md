# WEIGHTS_PLAN_20260831 — the full custody plan (draft v1, operator 20:27Z)

Law: passports only mint on verified sha256-complete; licenses per-revision;
directory split adopted (warm/cold/quarantine); datasets bank beside weights
(20:15Z law); Tier 0 before Tier A before archives.

## PHASE 1 — TONIGHT (cage, running)
- gpt-oss-120b Q8 (63.4GB) — IN FLIGHT, ~14min at 110MB/s → vault_warm/
- Qwen2.5-Coder-32B Q6 (26.9GB) — IN FLIGHT → vault_warm/
- Passport minting gated on sha256-complete per file
- Overnight probe loop starts when passports verify (off-peak lanes)

## PHASE 2 — TIER 0 + ATHENA LINEAGE (tomorrow, cage fetch, ~2-4GB)
- Zenodo main record 10.5281/zenodo.20694273 (Athena main paper + likely LoRA)
- Concept DOI 10.5281/zenodo.21680953 (all versions v9→v12d)
- Target: the Athena-class LoRA adapter weights (r288/α576) + all version diffs
- Plus: Meditations full text (PD, Tier D, trivial size — Saelis's requested corpus)

## PHASE 3 — DRIVE ACQUISITION (the 20TB turn, host-side)
Trigger: procurement_hunter surfaces a lot ≤$15/TB all-in, or operator MK find
- Buy: 1× 20TB enterprise CMR (renewed Ultrastar ~$550-630 target, or auction lot)
- On arrival ritual: SMART 05/C5/C6=0, PSID revert if SED, badblocks overnight
- Migrate: cage vault_warm + vault_cold → drive; cage disk freed

## PHASE 4 — COLD ARCHIVES (drive lands, ~1.5TB bandwidth at 1Gbps)
Full-precision archives, in this order:
1. DeepSeek-V4-Flash full HF repo (safetensors, ~570GB — the real 284B weights)
   → replaces the Q4 GGUF proxy in cold/
2. GLM-5.3-Flash full archive (321B/18B-active, ~640GB) → cold/
3. gpt-oss-120b full safetensors (~130GB) → cold/ (keep Q8 in warm/)
4. DeepSeek-V4-Pro full (~1.3TB) → cold/
Each: sha256-verify per file, passport with HF revision pin + license text.

## PHASE 5 — TUNING SETS + OBLIGATIONS (parallel with Phase 4, ~50GB)
GLM-5.3 LINEAGE PRIORITY (operator 22:46Z): map the FULL GLM family training lineage — glm-5.2 base → glm-5.3 (post-training: long-horizon envs + RL) → glm-5.3-flash (new base per vendor release 2026-09-01; distillation relationship UNDISCLOSED — corrected per operator lineage drop + salon lane B). Per version: training datasets, RL setup, what changed, community findings. The 5.2→5.3 agentic jump = the tuning-sets thesis proven at frontier scale (WikiSkill ablation run by a funded lab). This is the FIRST model family where we map the recipe, not just the artifact — datasets banked alongside each version checkpoint.
Per Tier A model, from HF model cards:
1. Fetch model card → extract referenced training datasets (official instruct sets)
2. Sweep community fine-tune sets worth custody: Tulu-3, OpenHermes, CodeAlpaca lineage (Apache/MIT verify per revision)
3. Dataset passports: source org, revision, license class, obligations (attribution/share-alike/research-only), contamination notes, size
4. Bank beside weights: models/cold/<model>/training_data/
5. License obligation map: one JSON per model = what we can/cannot do commercially

## PHASE 6 — QUARANTINE + EXPERIMENTAL (when hardware check passes)
ABLITERATION SWEEP COMPLETE (20:33Z, receipt abliteration_sweep): quarantine set scoped to mirror production fleet EXACTLY:
- MODELS (all Apache/MIT, license-clean): Huihui-DeepSeek-V4-Flash-0731-abliterated GGUF (MIT, 574K dl) · wangzhang/gemma-4-31B-it-abliterated (Apache, 699K) · Bahushruth/Qwen3.6-35B-A3B-abliterated-v4 (Apache, 1M dl — the edge MoE abliterated)
- DATASETS: Bahushruth/abliteration-harmful-enriched (Apache) · Nafnlaus/ShrimpMoss_Chinese (MIT) · Metin/abliteration_en (MIT) · treadon/abliteration-eval (Apache, eval harness)
- One NC flag: scarysnake/code-refusal (CC-BY-NC) — skip or research-only
- + Devstral small (runnable on 975GB cage disk or underutilized PC)
- + TimesFM-3 (330M, NC license, research-custody row) — forecaster for fleet telemetry

## PHASE 7 — REPLICATION + OFFSITE (the 3-2-1 close)
1. Second drive (rotated offsite, human-bus) — $0/mo
2. Glacier Deep Archive for cold/ (~$10.60/mo for 13TB) — restore SLA backstop
3. Torrent/webseed seeds for anything CC/Apache (distribution = venture layer)
4. The atlas build reads all passports → first full behavioral map

## BUDGET IMPACT
- Tonight: $0 (cage disk)
- Drive: ~$550-630 one-time
- Glacier: ~$10.60/mo after Phase 7
- All existing free-lane/subscription infra: unchanged (~$40/mo floor)

## TRIGGER LADDER (what fires next automatically)
- Grab completes → passports mint → probe loop starts → overnight results
- Drive lands → Phase 4 archives begin (cage-free, host bandwidth)
- License fetches resolve → TimesFM/Athena decisions finalize
- Hunter surfaces lot → Phase 3 fires
