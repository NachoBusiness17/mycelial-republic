# RAW EVIDENCE: WebSearch summaries, 2026-10-01, lane nonnvidia-stacks (division B, spiking-wide)
# Search-grade evidence (secondary sources), tri-stated against primary fetches where they exist.
# NOTE: several queries hit web_search 429 rate limits; each 429 is recorded. The used-GPU-price
# query (used RTX 3090 price October 2026 / RX 7900 XTX price) FAILED after multiple 429s: no
# fresh price datapoint was retrieved. The only price on record for the 3090 rung is the estate's
# own stale quote (watch/inbox/ball4/compute.md:15, ~$1,100-1,300, dated 2026-09-01). The search
# tool's fallback prose ($600-800) is UNVERIFIED general knowledge and is REJECTED as evidence.

## SEARCH 1: "ROCm 7 training 7B fine-tune LoRA consumer RDNA3 7900 XTX 2026" -> OK
- AMD ROCm Blog: Fine-tune Llama with LoRA: https://rocm.blogs.amd.com/artificial-intelligence/llama-lora/README.html (official LoRA fine-tune on single AMD GPU)
- GitHub Discussion, LLM GRPO Training on RX 7900 XTX: https://github.com/ROCm/legacy-rocm-build/discussions/6553 (community warning: QLoRA "actively harmful" on RDNA3 for training; prefer non-quantized LoRA)
- HuggingFace community KB: 7B-13B QLoRA fine-tune on RDNA3 16-24GB cards: https://huggingface.co/datasets/John6666/knowledge_base_md_for_rag_1/blob/24fa6877b2779b087c622f529dce27cabb435e03/amd_gpu_ai_20251121.md
- GPUHunter blog: ROCm 7.2 viable for local inference; 7900 XTX ~66 tok/s Llama 8B Q4, 24GB: https://www.gpuhunter.io/blog/amd-vs-nvidia-local-ai-2026
- TRI-STATE: community "QLoRA harmful on RDNA3" (one discussion) vs vendor QLoRA support (ev_unsloth_amd.md). Both recorded; vendor matrix is primary.

## SEARCH 2: "Huawei Ascend 910C MindSpore CANN training maturity 2026 DeepSeek" -> OK
- Tom's Hardware: Huawei-led team claims it post-trained DeepSeek's 1.6T-parameter models on Ascend 910C chips (~1,000 chips, V4-Pro): https://www.tomshardware.com/tech-industry/artificial-intelligence/huawei-led-team-claims-it-post-trained-deepseeks-1-6-trillion-parameter-models-on-ascend-910c-chips
- TrendForce 2026-09-23: DeepSeek reportedly expands Huawei chips to AI training, new supply could arrive in 4Q26; Liang Wenfeng called Huawei training chips the company's biggest bet: https://www.trendforce.com/news/2026/09/23/news-deepseek-reportedly-expands-huawei-chips-to-ai-training-new-supply-could-arrive-in-4q26
- Maturity note: CANN and MindSpore "continues to mature but remains less established outside China, and public benchmarks are still limited"; DeepSeek open-sourced core tools supporting Huawei AI chips. 910C ~60% of H100 inference perf (same coverage).

## SEARCH 3: "Cambricon MLU SpikingBrain PyTorch training domestic GPU 2026" -> OK (after 4 429 retries)
- PyTorch blog: Cambricon Joins the PyTorch Foundation as a Platinum Member (Torch-MLU, native PyTorch dev experience on MLU for large-scale LLM training/inference): https://pytorch.org/blog/cambricon-joins-the-pytorch-foundation-as-a-platinum-member
- PyTorch Conference China 2026 talk: "Towards Device-agnostic PyTorch: Building Unified Infrastructure"
- Tom's Hardware: Cambricon targets ~500,000 AI chips in 2026 (tripling production; yield and HBM supply risks named)
- SpikingBrain 2.0 released April 2026, "upgraded architecture and training token efficiency plus broader hardware support": https://github.com/BICLab/SpikingBrain-7B

## SEARCH 4: "RX 5600 XT RDNA1 gfx1010 ROCm llama.cpp Vulkan support 2026" -> OK (after 4 429 retries)
- RDNA1 cards "no longer officially supported by ROCm"; community workaround HSA_OVERRIDE_GFX_VERSION
- llama.cpp GitHub issue #20564: ROCm regression affecting all RX 5000 series users, workaround available
- RCCL does not support gfx1010 (RDNA1 lacks P2P); one user compiled RCCL from source for 3-GPU RX 5700 XT: https://www.reddit.com/r/LocalLLaMA/comments/1rjq75f/i_compiled_rccl_from_source_for_amd_gfx1010_rdna1
- ollama-rdna1 fork (drop-in Ollama for RDNA1 cards): https://github.com/myusername68/ollama-rdna1
- llama.cpp Vulkan backend works on gfx1010 without ROCm hacks

## SEARCH 5: "MetaX C500 GPU SpikingBrain 7B training cluster" -> OK
- arXiv 2509.05276 abstract (primary fetch in ev_arxiv_2509_05276_abstract.md): MetaX GPU cluster, hundreds of GPUs, weeks stable
- CAS Institute of Automation news (2025-09-15): training/inference frameworks built for domestic GPUs, MetaX C550 cluster, Triton operator library: http://brain-ai.ia.ac.cn/en/news/202509/t20250915_773125.html
- MetaX C500 product page: https://www.metax-tech.com/en/goods/prod.html?cid=107&id=21
- CORRECTION to the ask's framing: the documented SpikingBrain cluster is MetaX C550 (C500 is a sibling product)

## SEARCH 6: "Google TPU v7 Ironwood general availability 2026 price per hour" -> OK (Ironwood pricing conflicting across secondary sources; RESOLVED by primary fetch ev_tpu_pricing.md: $12.00/chip-hr us-central1 on-demand, $6.00 Flex-start; the "$6" secondary figure was the Flex-start rate)
- dataknobs: TPU v5e $1.20/chip-hour on-demand, ~$0.54-0.60 committed; v5e 2.5x throughput-per-dollar vs v4: https://www.dataknobs.com/generativeai/8-tpu-gpu/tpu-gpu-cost.html

## SEARCH 7: "Unsloth AMD ROCm 7B QLoRA RDNA3 support official 2026" -> OK (after 2 429 retries)
- Unsloth official AMD docs (primary fetch in ev_unsloth_amd.md): https://unsloth.ai/docs/basics/amd
- AMD developer article (2026): https://www.amd.com/en/developer/resources/technical-articles/2026/train-and-run-models-on-amd-gpus-with-unsloth.html
- Compute Market buyer guide: ROCm support landed in Unsloth 0.7; 7B and 13B QLoRA on 7900 XTX works, 10-20% speed penalty vs RTX 4090: https://www.compute-market.com/blog/best-amd-gpu-local-llm-inference-2026

## SEARCH 8: "export control ECCN 3A090 consumer GPU threshold RTX 4090 AI diffusion rule 2026 status" -> OK
- BIS guidance dated May 31, 2026 (3A090.a and AI Diffusion Rule enforcement status): https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf
- Jan 15, 2026 BIS final rule shifting advanced-AI-chip export policy (per C4ADS "Covert Compute" Sept 2026 report: https://c4ads.org/wp-content/uploads/2026/09/Covert-Compute-C4ADS.pdf)
- Federal Register, Framework for AI Diffusion (the original Jan 2025 rule): https://www.federalregister.gov/documents/2025/01/15/2025-00636/framework-for-artificial-intelligence-diffusion
- Substance: AI Diffusion Rule's worldwide tiering rescinded/not enforced; ECCN 3A090.a country licensing remains (RTX 4090 still restricted to China); consumer gaming carve-outs (GVG/NAC-style license exceptions) persist; Chip Security Act (location verification) pending pressure

## SEARCH 9 (FAILED): "used RTX 3090 price October 2026 RX 7900 XTX 24GB price local LLM" -> 429 RATE-LIMITED TO DEATH
- No fresh price datapoint retrieved. Estate stale quote stands as the only number on record.
