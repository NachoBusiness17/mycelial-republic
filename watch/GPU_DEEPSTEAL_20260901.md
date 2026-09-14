# GPU DEEPSTEAL — verdict (2026-09-01, salvaged from GLM_K8S_MCP_DEEP_RESEARCH_20260826.md + compose file)

## 1. Hardware: UNVERIFIED from cage
No nvidia-smi in the WSL cage; the research doc never names OUR card — it plans around "a 24 GB GPU plausible" (4-bit GLM ≈ 15GB floor, 17–22GB realistic). Operator's one `nvidia-smi` in PowerShell confirms model + VRAM. Everything below sized for the 24GB planning assumption.

## 2. What the month actually was (chronology from the doc, 08-26)
- A **serving-architecture deep research**: GLM family (4.6V-FP8 vision = 4×datacenter GPUs, impractical; 4.6V-Flash BF16 ≈ 20.6GB; GLM-Image 34–45GB; 4-bit ≈ 17–22GB) mapped onto **Kubernetes/K3s + MCP + distributed caching** — device plugins, runtimeClassName: nvidia, edge caches, GLM-OCR (0.9B) on K3s for concurrency.
- The doc's own technical notes are GOOD: prefer **vLLM/SGLang over GGUF** for write-capable GLM agents (llama.cpp has documented CUDA/Vulkan/flash-attention/quantized-KV problems on GLM-4.7-Flash); K3s = edge tool, "full Kubernetes for central/high-scale."

## 3. Why it stalled (root cause, documented + verified)
1. **The ollama container has NO GPU reservation** (compose verified today, 14:17Z) → CPU-only inference → "our local sucks" regardless of model.
2. **Orchestration-first sequencing**: a month went into multi-host topology (K8s/K3s/MCP/cache layers) for a **single GPU on a single host** — the doc's own line: "K3s for edge or resource-constrained clusters." Docker compose is already the orchestrator at this scale.
3. **GGUF trap avoided on paper, not in practice**: the doc prefers vLLM/SGLang (Linux-native serving) but the host runs Windows + docker + WSL2 — the serving stack never got stood up on actual silicon.

## 4. The goal (per doc): a write-capable local agent seat — vision + OCR + coding, self-hosted, $0 marginal.

## 5. THE PATH (GPU-first, orchestration-last)
- **Step 1 (operator, 2 min):** `nvidia-smi` in PowerShell → confirm card, VRAM, driver ≥ CUDA 12 class.
- **Step 2 (operator, 5 min):** ollama compose block gets:
  ```yaml
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
  ```
  WSL2 caveat: docker-in-WSL needs the NVIDIA Container Toolkit installed on the WSL docker host; Windows driver provides libcuda to WSL natively. Verify: `docker exec mag-ollama nvidia-smi` shows the card.
- **Step 3:** pull VRAM-sized model — 24GB: GLM-4.7-Flash or 14B-class runs fast; 8–12GB: 7B–8B. (The GGUF warnings were GLM-4.7-Flash-on-llama.cpp-specific; ollama's CUDA path with a clean model is fine for seat duty. vLLM serving is the LATER rung for concurrency.)
- **Step 4:** SKIP k8s/k3s until multi-host. The doc agrees; the estate agrees; one card doesn't need a control plane.
- **Step 5:** local seat re-enters the salon/lane rotations — strike reset, the fence was the missing GPU.

## Meta-lesson (v5 methods chapter)
A month went to orchestration research while the blocker was a 6-line YAML stanza. v5 law candidate: **hardware-reality check before architecture research** — `nvidia-smi` before `deep-research`. The pre-flight self-review, applied to infrastructure.

Labels: root cause MEASURED (compose file); chronology MEASURED (doc); hardware UNVERIFIED (needs operator nvidia-smi); path RECOMMENDED (not yet executed).
