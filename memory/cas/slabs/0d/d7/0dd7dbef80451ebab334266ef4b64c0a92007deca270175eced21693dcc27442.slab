# WORK w-quant-compare

lane: openrouter model: stealth/space-bunny-alpha
ts: 2026-09-29T21:58:17.725764+00:00
finish: stop cached_tokens: 149
ask: Compare quantization approaches: read the quantization handbook poster (INT4/FP8/NF4, W4A16, per-channel/group) and map each method to our estate's hardware (RX 5600 XT gfx1010 Vulkan, llama.cpp). Which methods work TODAY on our card vs NVIDIA-only? What's the quality/speed tradeoff? Return a table.

---

## 1) FINDING

**Estate hardware and runtime:** Radeon RX 5600 XT, `gfx1010`, Vulkan backend, `llama.cpp`.

**Exact TODAY status cannot be fully verified** because the poster, installed `llama.cpp` revision, build options, Vulkan driver, and supported-kernel list were not provided.

| Method | Meaning | RX 5600 XT / `gfx1010` with Vulkan | NVIDIA-only / not confirmed for this card | Quality | Speed | Evidence |
|---|---|---|---|---|---|---|
| **INT4** | Integer weight format, usually 4 bits. Activation precision depends on the selected quantized model type. | **Likely supported today** if the installed `llama.cpp` has Vulkan quantized kernels. Confirm with `llama-bench` or backend listing before calling it verified. | No inherent NVIDIA dependency. | Lower memory use than FP8. Usually modest quality loss, but it depends on quantization scheme and calibration. | Generally the lowest-memory practical option. Actual speed depends on the kernel and dequantization path. | [llama.cpp Vulkan backend](https://github.com/ggml-org/llama.cpp/tree/master/examples/vulkan), [quantization types](https://github.com/ggml-org/llama.cpp/blob/master/include/llama.h) |
| **FP8** | 8-bit floating-point weights and/or KV-cache or activations, depending on use. | **Not natively accelerated on `gfx1010`.** Software or generic Vulkan support may exist, but the installed revision must demonstrate it. | NVIDIA-specific optimized FP8 paths, including Tensor Core-oriented implementations, are not evidence of support for this AMD card. | Higher numeric range and usually better fidelity than aggressive 4-bit methods. Quality depends on tensor scope and model. | Potentially faster than software emulation on supported hardware, but no `gfx1010` native FP8 path is established here. | [AMD `gfx1010` ISA documentation](https://www.amd.com/content/dam/amd/en/documents/isafamilyspecs/rDNA1/amd_gpu_open_source_documentation_gfx1010.pdf), [llama.cpp quantization documentation](https://github.com/ggml-org/llama.cpp) |
| **NF4** | 4-bit NormalFloat representation, from the bitsandbytes quantization family. | **OWED.** Modern `llama.cpp` has NF4-type model support, but Vulkan execution of the relevant tensor operations is revision-dependent. Do not assume that importing an NF4 model makes its kernels run on this Vulkan backend. | The original bitsandbytes workflow is commonly CUDA-oriented, but that does not by itself prove NF4 is universally NVIDIA-only. | Designed to preserve quality better than plain 4-bit formats at comparable bit width. Exact model-level quality is unverified. | Avoids the original CUDA dependency, but any generic or software path may be slower and depends heavily on the build. | [bitsandbytes NF4 documentation](https://huggingface.co/docs/bitsandbytes/en/quantization/nf4), [llama.cpp quantization types](https://github.com/ggml-org/llama.cpp/blob/master/include/llama.h) |
| **W4A16** | Weight precision W4, activation precision A16. It is a precision description, not one single storage format. | **Likely usable** if the installed Vulkan backend has a matching quantized weight and 16-bit activation path. Exact execution is **OWED** without the binary’s build details. | Not inherently NVIDIA-only. | Better numerical headroom for activations than W4A4, but weight quantization still introduces error. | Reduces weight bandwidth and memory. It is not automatically faster than INT4 or NF4 because dequantization, activation conversion, and backend support determine performance. | [llama.cpp quantization documentation](https://github.com/ggml-org/llama.cpp) |
| **Per-channel** | Separate quantization scales or parameters for each output/input channel. | **Format and kernel dependent.** If the installed model format and Vulkan kernels support it, it can run on the AMD card. | No inherent NVIDIA-only property. | Usually better than a single scale across all channels, especially when channel ranges differ. | Additional scale handling is usually modest compared with weight dequantization. | [GPTQ quantization](https://arxiv.org/abs/2210.17323) |
| **Per-group** | One quantization scale per block of weights, commonly a small group such as 32, 64, or 128. | **Format and kernel dependent.** Usually the practical high-quality option in supported `llama.cpp` quantized formats, but exact support must be checked in the installed revision. | No inherent NVIDIA-only property. | Usually better quality at the same nominal bit width than one scale per tensor or channel. | Slightly more scale metadata and potentially more dequantization work; speed must be measured. | [GPTQ quantization](https://arxiv.org/abs/2210.17323), [llama.cpp quantization documentation](https://github.com/ggml-org/llama.cpp) |

### Current decision

- **Best-supported class for the RX 5600 XT Vulkan build:** supported `llama.cpp` **4-bit quantized weights**, especially a per-group format with confirmed Vulkan kernels.
- **Not established as native for `gfx1010`:** **FP8 acceleration**.
- **Not established for the installed build:** **NF4 Vulkan execution**.
- **W4A16 is not a standalone format:** the result depends on the model’s storage format and kernel support.
- **Per-channel and per-group are orthogonal to INT4/NF4:** they describe scaling granularity, not a separate hardware backend.

## 2) STEALABLE idea

**Use per-group 4-bit weights as the default quality/memory baseline, then reserve FP8 for a verified hardware or software path.** This gives the RX 5600 XT the best chance of useful memory savings without depending on native FP8 or unverified NF4 support.

## 3) TESTABLE hypothesis

On the RX 5600 XT with the same `llama.cpp` build and model, a supported per-group 4-bit Vulkan build will have substantially lower memory use than a 16-bit build, with similar or better generation throughput, while retaining acceptable perplexity or task quality.  
Test with matched builds using `llama-bench`, memory measurements, and a fixed evaluation prompt set.

## 4) EVIDENCE or OWED

**EVIDENCE**

- The card is an AMD Radeon RX 5600 XT using `gfx1010`; native FP8 acceleration cannot be inferred from Vulkan compatibility.
- The `llama.cpp` project has a Vulkan backend and multiple quantization types.
- NF4 originates in a bitsandbytes workflow, but modern `llama.cpp` model types and kernel availability must be checked at the installed revision.
- Per-group quantization is generally designed to reduce the quality penalty of low-bit weights by using local scales.

**OWED**

- The contents of the referenced quantization handbook poster.
- Exact `llama.cpp` commit or release.
- Whether the current executable was built with Vulkan.
- Which quantization types the current Vulkan build actually implements.
- Driver version and ROCm/Vulkan runtime versions.
- Measured quality, throughput, and memory use.
- Whether the current card can run any specific FP8 path at acceptable speed.
- Whether a specific NF4 model works with the current Vulkan backend.

**Sources:** [llama.cpp repository](https://github.com/ggml-org/llama.cpp), [llama.cpp Vulkan backend](https://github.com/ggml-org/llama.cpp/tree/master/examples/vulkan), [bitsandbytes NF4 documentation](https://huggingface.co/docs/bitsandbytes/en/quantization/nf4), [GPTQ paper](https://arxiv.org/abs/2210.17323).
