# MODEL_VAULT_MANIFEST_20260831 — what to hoard, ranked

Law: use-models get 3-2-1 mirrored; reference-only gets cold copy; everything
gets manifest + hash before any bytes move. License recorded per row — archival
is legal for all Apache/MIT/open-weights rows below; personal-use rows marked.

## Tier A — USE-MODELS (active fleet; 3-2-1 mirror, hot+cold)
PHASE-0 GRAB (operator 18:53Z, 975GB free): top-3 = gpt-oss-120b (Q8 ~63GB, the free-lane workhorse, Apache-2.0) + DeepSeek-V4-Flash Q4 (~170GB, measured paid spine) + Qwen2.5-32B-coder Q6 (~27GB, the local-run coder). ~260GB total, ~70% headroom. Sequence: download → sha256 → passports row → banked. Full archives wait for the drive. DOWN-TIME TEST LOOP (operator 18:53Z): banked models enter the probe pipeline automatically — passport probe pack runs on whatever is banked while operator sleeps (off-peak, free/local lanes); each result appends behavior/coverage to the passport; models never sit unprobed.
| # | Model | ~Size | Why it's load-bearing | License |
|---|-------|-------|----------------------|---------|
| 1 | Qwen2.5 family (0.5B–32B incl. coder) | ~65 GB | ollama fleet (gemma/qwen-desk/2.5-coder lanes, seat_corpus verified) | Apache-2.0 |
| 2 | Gemma family (2B/4B desk variants) | ~30 GB | janitor/capture lanes, always-on | Gemma Terms (redistributable) |
| 3 | gpt-oss-120b | ~65 GB | groq/cerebras/together workhorse; THE free-lane model | Apache-2.0 |
| 4 | DeepSeek-V4-Flash (+0731) | ~350 GB | measured paid spine (98% cache-hit, $93/mo scale) | open-weights (MIT-class per model card) |
| 5 | GLM-5.3-flash / 4.7-flash | ~400 GB | measured cheapest interactive lane (z.ai rate card) | open-weights |
| 6 | Qwen3.6-35B-A3B | ~70 GB | FreeToken-supported edge MoE (FreeToken plans) | Apache-2.0 |
| 7 | DeepSeek-V4-Pro | ~700 GB | pro salon lane (Aug billing shows pro usage) | open-weights |
| 8 | vision-exp / misc flash variants | ~100 GB | visionexp measured in billing | varies |
| **subtotal** | | **~1.8 TB** | | |

## Tier B — FUTURE-PROOF (watched, not yet run; cold copy)
TUNING-SETS FIRST (operator 20:15Z): vault's scarce layer = tuning/fine-tune datasets + their LICENSE OBLIGATIONS, grabbed after core models. Base weights get retrained; curated tuning sets are the reproducible recipe (existence proof: Steiniger's 569-example set = the Athena recipe, already banked). Datasets bank beside their weights; passports extend to datasets (source/license/hash/contamination); obligations tracked per-dataset license class. Tier B dataset sweep = next expansion after top-3 grab.
DIRECTORY SPLIT (adopted 18:52Z, Codex convergence — MODEL_LIBRARY_BOOTSTRAP): models/{warm: runnable now, cold: GLM-5.3-Flash 321B/18B-active + DeepSeek-V4-Flash 284B/13B-active archives, quarantine: abliterated 7B-30B + experimental}; behavior/{provider: grok-4.6/GPT-5.3/z.ai probes+responses (provider-only, mined not held), receipts: cost/latency/tool-behavior/failures}. Devstral + abliterated 7B-30B added to local-run set. Passports directory = identity/license/hash per model (both seats converged independently). Bottleneck = GPU/RAM not disk (30TB pool holds A+B+C).
| # | Model | ~Size | Trigger to promote | License |
|---|-------|-------|--------------------|---------|
| 9 | FreeToken runtime + FTW format tools | <5 GB | host hardware check passes → local 120B-class | Apache-2.0 |
| 10 | CUDA-Agent repo + CUDA-Agent-Ops-6K dataset | <10 GB | kernel/RL research; weights NOT included (proprietary) | repo license |
| 11 | MiniMax M3 / Kimi K3-class | ~300-700 GB | pricing/quality shift on money map | varies — check |
| 12 | Llama-3.3-70B | ~140 GB | Together batch cheap-row model | Llama license |
| 13 | Muse Glimmer 30B, GLM-5.2 | ~200 GB | FreeToken-supported; edge candidates | varies |
| **subtotal** | | **~0.8-1.3 TB** | | |

## Tier C — HISTORIC ARCHIVE (cold, single copy + erasure code)
| # | Set | ~Size | Rationale |
|---|-----|-------|-----------|
| 14 | Llama full lineage (1, 2, 3, 3.1, 3.3; code/purpose variants) | ~2.5 TB | THE pre-open-era lineage; license-flip precedent already happened here |
| 15 | Mistral/Mixtral lineage | ~1 TB | the MoE-on-edge lineage |
| 16 | Phi / small-quality lineage (1–4) | ~150 GB | small-model research line |
| 17 | Falcon/MPT/Dolly/Vicuna/Alpaca-era | ~800 GB | 2023 archaeology — where "open weights" began |
| 18 | DeepSeek R1 + V3 full family | ~1.5 TB | reasoning-lineage |
| 19 | Qwen 1/2/2.5 full + Qwen3-MoE | ~2 TB | most-permissive full-capability lineage |
| 20 | Specialized: vision (DART-adjacent SAM3-class where redistributable), embeddings (bge/e5/gte), code models | ~1 TB | non-LLM capability classes |
| **subtotal** | | **~9 TB** | |

**TOTAL VAULT: ~12-13 TB** (Tier A 1.8 + B 1.0 + C 9.5).

## Execution law
1. MANIFEST FIRST: model, HF repo id, revision hash, config/tokenizer/generation files, license text, download date → models.jsonl. A copy without its hash and license is not archival, it's hoarding.
2. GRAB SEQUENCE: Tier A first (it's what we run — lose it, lose the swarm), then B, then C oldest-first (historic = most likely to quietly vanish).
3. ENCRYPTION: age (X25519) container per model, public key in repo, private key printed on paper + one offline copy. "Fridler encryption" interpreted as this: client-side, operator-held keys, nothing readable at rest on any provider.
4. INGEST NODE: vast.ai or Hetzner box, HF hub download at 1-10 Gbps, verify sha256 per file, encrypt, stream to cold storage, wipe node. Node exists for days, not months.
5. MIRRORS: hot = host spare disk (Tier A only), warm = Hetzner Storage Box or B2, cold = S3 Glacier Deep Archive or B2. 3-2-1 for A, 2 copies for B/C (cold + warm).
6. The harvest already watches for weights drops (launch pattern #1) — new drops queue into Tier B automatically.

- BRIDGE POINTER (board action 2026-09-06): ollama blob -> GGUF for LM Studio EXISTS at tools/ollama_to_lmstudio.mjs (host-side, node zero-dep) — BLOB_BRIDGE_READY_20260901 verified live, retest PASSED. Cites: BLOB_BRIDGE_READY_20260901
