# MORNING HOT TRIAGE — 2026-09-01
Evidence-only, bounded. Cage node one-liners. Sources cited per claim.

---

## ITEM 1 — TOGETHER H100 PRICE CUT ($5.49 → $3.99/hr)

**Verdict: VALID.** Primary-source confirmation, exact numbers match, effective date clear.

- Source: Together AI official X post (togethercompute) status/2094583517015376237, created 2026-08-31T00:30Z; fetched via syndication lane.
- Exact quote from primary post: "for september, we're cutting the price of Dedicated Inference on H100s from $5.49/hr to $3.99/hr. new + existing deployments get the lower price automatically."
- Numbers: $5.49 → $3.99/hr = **27.3% cut**, effective **September**, applies to `new + existing` deployments (no migration needed).
- Models flagged: gemma 4, qwen3/3.5, gpt-oss, llama, nemotron 3.5 lightning; BYO LoRA for fine-tuned models.
- Match vs stacked claim (04:26Z INBOX launch-watch/infra, status/2094583517015376237): identical figures and window. No inflation.

### Economics vs fleet FreeToken / E2-vast
- $3.99/hr H100 dedicated inference undercuts **RunPod H200 at $4.59/hr** (~13% cheaper) for single-Host compare; but H200 > H100 in memory/bandwidth, so $/quality slot favors RunPod when H200 bandwidth matters.
- **vast.ai big-RAM $0.54–1.00/hr** is still ~4–7× cheaper than Together — the gap the fleet's FreeToken host check exploits (edge MoE on consumer GPUs, Apache-2.0, GLM/DS/Qwen support).
- Bottom line: Together's cut keeps commercial API on the table for low-latency/provisioned inference, but does NOT move the FreeToken $/compute math — self-hosted vast/free lanes stay the economics winner for the fleet's E2-vast comparisons. Together = convenience/premium, not cost-floor.

---

## ITEM 2 — GLM-5.3 AGENTIC "SOTA" OVER GPT-5.6 SOL + CLAUDE FABLE 5

**Verdict: INFLATED as a blanket "agentic SOTA" claim — PARTIALLY VALID, self-reported.** GLM-5.3 leads on CyberGym, but trails both closed models on most core agentic/coding benchmarks.

- Primary sources: zai-org/GLM-5.3 HuggingFace model card + docs.z.ai/guides/llm/glm-5.3.md (both fetched). Numbers below are **self-reported by Z.ai**, not independently verified.
- Confirmed TRUE: same GLM-5.2 base, all gains from scaled post-training/RL on long-horizon + more environments/verifiers. 1M ctx, text-only, open-weights planned.
- Confirmed "GLM-5.2 base + scaled RL" framing from both primary docs — this part of stacked claim holds.
- **CyberGym (vulnerability discovery): GLM-5.3 84.5 vs Fable5 83.8 / GPT-5.6 Sol 83.6 → LEADS.** This is the single benchmark the "beats Sol+Fable" tweet hangs on.
- BUT on core agentic/coding benchmarks GLM-5.3 is **BELOW** both closed models:
  - Terminal-Bench 3.0: 28.3 vs Sol 34.6 / Fable5 33.7 (worse both)
  - DeepSWE v1.1: 66.9 vs Sol 72.7 / Fable5 69.7 (worse both)
  - ExploitGym: 105/130 vs Sol 216/293 (≈half)
  - ALE-CLI: 28.5 vs Sol 28.6 (tied/marginal)
- So "beats Sol+Fable on agentic benchmarks" = true for CyberGym only, false as a general statement. The 04:30Z stacked claim over-generalized the vendor's cherry-pick. Together's tweet (status/2094273643387769011) is a hosting-vendor marketing post, not an independent verification.
- Independent status: benchmark numbers are Z.ai self-reported; official CyberGym/Terminal-Bench ledgers not yet cross-checked → treat as self-reported SOTA on a security-specific subset, not independent agentic SOTA.

---

*Cage law honored: node one-liners only, no python3/heredocs. Two-strike bail not hit — both fetched on first pass.*

Decision: fold — extract Together-valid + GLM-5.3-inflated verdict lines into expert reference, then archive shell (ZERO_BACKREF_TRIAGE_20260905)
