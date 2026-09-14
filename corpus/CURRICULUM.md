# THE COMPANY CURRICULUM — role → materials map (2026-09-04, license-verified)

The training library for an AI company staffed by agents. Three shelves: VENDOR
(docs/ref/zai_docs_mirror — proprietary, RAG-only) · BEHAVIORAL (our laws/scifi/handbook
— weights-clean by construction) · CURRICULUM (this file's materials — license-split).
**Eligibility rule:** MIT/Apache/BSD/CC-BY(-SA) = **W** (weights-eligible training
corpus) · CC-BY-NC / no-license / proprietary = **R** (RAG-only, never bake into weights).
Every license below was verified against the actual LICENSE file or repo, not guessed.

## Headline findings
1. **Weights-eligible core = 24 of 33 materials** — all cloneable today.
2. **The NC traps:** anthropics/courses (CC-BY-NC-4.0) + HF evaluation-guidebook
   (CC-BY-NC-SA-4.0) — reference shelves ONLY, never training corpus.
   android/ai-samples + Karpathy LLM101n ship NO license — reading copies only.
3. **openai/evals reads "Other" on the API but the LICENSE is MIT** — weights-eligible.
   unslothai/notebooks is LGPL-3.0 — reference use, don't strip into pipelines.
4. **Evals (our #1 hire) has the strongest fully-open shelf of any role.**
5. **Economist lane has zero weights-eligible external canon** — the FinOps/pricing
   literature is all proprietary/RAG. Our internal burst doctrine + ZAI reference ARE
   the lane's corpus (matches the design doc: STRONG, measured, ours).
6. Repo moves caught: verl → verl-project/verl · Triton → triton-lang/triton ·
   google-gemini/generative-ai-android DEAD (successor: android/ai-samples).

## 1. AGENTS (Manager + lanes)
- ms-agents-beginners (18 lessons) — MIT W — ✅ CLONED — foundations → multi-agent design patterns
- hf-agents-course — Apache W — ✅ CLONED — smolagents → frameworks → certification projects
- OpenAI Agents SDK (openai-agents-python) — MIT W — handoffs, guardrails, sessions/tracing
- Anthropic engineering essays (effective-agents, multi-agent-research, context-engineering) — R (WebFetch) — doctrine layer; our charter mirrors it
- anthropic-courses — CC-BY-NC R — ✅ CLONED (reference shelf ONLY)

## 2. POST-TRAINING / RL (the WHALE gap)
- TRL (huggingface/trl) — Apache W — SFT/DPO/PPO/GRPO cookbook + conceptual guides
- verl (verl-project/verl, 23k★ lab standard) — Apache W — industrial RL post-training
- HF deep-rl-class — Apache W — RL fundamentals → RLHF theory spine
- Unsloth notebooks — LGPL-3.0, reference-OK — fine-tuning recipes per open model
- Karpathy nn-zero-to-hero — MIT W — backprop→GPT from scratch, onboarding

## 3. INFERENCE-OPT / KERNELS (Economist + Builder)
- GPU MODE lectures (gpu-mode/lectures) — Apache W — THE kernels course (Triton, fused kernels, profiling)
- vLLM — Apache W — PagedAttention, batching, quantization, serving economics
- SGLang — Apache W — RadixAttention cache reuse (our cache-99.5% doctrine's twin)
- Triton (triton-lang/triton) — MIT W — the kernel language + tutorials
- Also W: Liger-Kernel (BSD-2) · NVIDIA cuda-samples · HF TGI (Apache)

## 4. EVALS (the lane we must hire — strongest open shelf)
- openai/evals — MIT W (license file verified past the API's "Other") — harness patterns + benchmark registry
- promptfoo — MIT W — declarative evals, CI/CD, AI red-team scanning
- HELM (stanford-crfm/helm) — Apache W — the benchmark framework
- Anthropic "Demystifying evals for AI agents" — R — the doctrine piece (tool-selection evals, drift)
- HF evaluation-guidebook — CC-BY-NC-SA R — leaderboard operators' knowledge (reference only)

## 5. ECONOMIST / COST (zero W external canon — ours IS the canon)
- FinOps token economics — R · Poyar usage-pricing playbook — R · Stanford agentic-token study (measured: ~1000x chat tokens, input-dominated = external proof of our OUTPUT-RATIO law) — R · arXiv 2605.09104 token-economics-for-agents — R (weights-gray)
- INTERNAL (weights-clean, ours): burst doctrine + docs/ref/ZAI_API_EXPERT_REFERENCE.md + the hunger ledger

## 6. RESEARCH / DATA (restock-first)
- Stanford CS336 lecture PDFs — MIT W — tokenizers→data→training→serving, lab-grade (assignments repo UNLICENSED = R)
- mlabonne/llm-course (82k★) — Apache W — the roadmap + Colabs, all-lane onboarding
- HF datasets — Apache W — data-team tooling canon
- awesome-llm-post-training survey — no license R — the restock hunt map

## 7. BUILDER
- LangGraph — MIT W — durable-execution harness pattern
- smolagents — Apache W — minimal-harness philosophy (we share it)
- Google ADK — Apache W — code-first agent build/eval/deploy

## 8. EMBODIED / ANDROID (field office)
- LeRobot — Apache W — VLA/imitation, embodied course+lib
- android/ai-samples — NO LICENSE R — on-device GenAI patterns (reading only)
- google-gemini/cookbook — Apache W — incl. AI Edge on-device paths
- Gemini Nano docs — R — AICore, offline inference

## 9. SECURITY
- OWASP LLM Top 10 — CC-BY-SA W — the threat canon
- llm-attacks (GCG) — MIT W — adversarial suffix mechanics
- JailbreakBench — MIT W — attack/defense eval loop

## 10. GENERAL HANDBOOKS (day-one onboarding)
- ms-genai-beginners (21 lessons, 119k★) — MIT W — ✅ CLONED
- stas00/ml-engineering — CC-BY-SA W — big-training ops handbook
- GCP generative-ai — Apache W — prompt notebooks + agent samples
- Karpathy LLM101n — no license R — reading copy
- NOT downloadable (gated video): DeepLearning.AI short courses · Anthropic Academy/Skilljar · Google Prompting Essentials — RAG/citation only

## Clone queue (next wave, all W)
trl · verl · deep-rl-class · nn-zero-to-hero · gpu-mode/lectures · vllm · sglang · triton ·
openai/evals · promptfoo · helm · cs336-lectures · llm-course · datasets · langgraph ·
smolagents · adk-python · lerobot · gemini-cookbook · owasp-llm · llm-attacks ·
jailbreakbench · ml-engineering · gcp-generative-ai

## Wave 1 build landed (2026-09-04, builder gopher)

The five base libraries are on disk under `corpus/library/`, shallow clones (depth 1,
blob:none), per-repo facts in `<name>/.corpus-meta.json`:

| Clone | Source | License | W/R | Size (total / worktree) |
|---|---|---|---|---|
| `anthropic-courses` | anthropics/courses | CC-BY-NC-4.0 | R | 202 / 113 MB |
| `ms-agents-beginners` | microsoft/ai-agents-for-beginners | MIT | W | 941 / 537 MB |
| `ms-genai-beginners` | microsoft/generative-ai-for-beginners | MIT | W | 1536 / 926 MB |
| `hf-agents-course` | huggingface/agents-course | Apache-2.0 | W | 6 / 4 MB |
| `openai-cookbook` | openai/openai-cookbook | MIT | W | 1755 / 1085 MB |

- `openai-cookbook` working tree was extracted manually (Windows cannot check it out
  natively — one subtree has an NTFS-invalid trailing-space dir name; excluded 31 sample-data
  files, all 3133 remaining files size-verified against the git tree).
- Size honesty: corpus total ~4.4GB, over the ~500MB clone budget. Bulk = duplicated media in
  the Microsoft courses' ~20-30 language translations. Trim candidates identified, NOT deleted
  (operator GO required). Next-wave clone queue above was NOT started (budget breach first).
- `corpus/dumps/` created, empty, reserved.

*Catalog verified 2026-09-04 by the library scout (licenses at the file level). Feeds the
weights-day plan: the W shelf = training corpus for the Distiller + lane fine-tunes
(WHALE amendment); the R shelf = RAG reference only. See corpus/LICENSES.md for the ledger.*

## ADDENDUM 2026-09-05 — human-atlas
ashemag/human-atlas (MIT) — TypeScript/Next.js 3D atlas over BodyParts3D meshes.
The architecture steal for the FLEET ATLAS: system toggles -> fleet systems; "find a
structure" -> find-an-organ; tap-to-inspect -> piece card w/ laws cited + receipts.
Weights-eligible: YES (MIT). Cloned to corpus/library/human-atlas (154MB, meshes incl).
