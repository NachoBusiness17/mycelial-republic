# r-moe-offload: llama.cpp MoE expert offloading (--n-cpu-moe, -ot) on consumer AMD GPUs via Vulkan

Deep-dive banked 2026-09-28 by flash50. Every claim below cites a source fetched or command run in this session, or is explicitly labeled DERIVED (arithmetic from verified numbers) or OWED (could not verify). No benchmarks were run on local AMD hardware (this machine has none in scope); this is a literature + source-code dive.

## 1. TL;DR

- MoE expert offloading in llama.cpp is tensor-level buffer-type overriding: expert weight tensors (`ffn_gate_exps`, `ffn_up_exps`, `ffn_down_exps`) are allocated in a CPU (host RAM) buffer instead of VRAM, while attention, router, shared experts, embeddings, and KV stay on GPU. It is an official feature: llama.cpp README lists "CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity" (fetched README, master branch, this session).
- `-ot/--override-tensor` is the general regex mechanism (PR #11397, slaren, merged 2025-01-24). `--cpu-moe` and `--n-cpu-moe N` are convenience wrappers that generate the same kind of overrides (PR #15077, slaren, merged 2025-08-04): for each of the first N layers it appends the pattern `blk\.N\.ffn_(up|down|gate)_exps` mapped to `ggml_backend_cpu_buffer_type()`.
- Override resolution is first-match-wins over a single ordered list: `src/llama-model-loader.cpp` `buft_for_tensor` lambda iterates the override array, matches with `std::regex_search`, and breaks on the first hit (raw source fetched this session).
- On the Vulkan path, MoE support has landed progressively: initial `MUL_MAT_ID` shaders (PR #7628, merged 2024-06-03), fused `topk_moe` shader port (PR #16641, merged 2025-10-18), FlashAttention tuning specifically for MoE on AMD (PR #18280, merged 2025-12-24, +7.2 to +14.3 percent tg128 on Radeon 8060S / Radeon Pro VII).
- For 8 GB VRAM the practical recipe is `-ngl 99 --n-cpu-moe N` with N found by decrement-to-OOM-plus-one. A verified 8 GB datapoint (GTX 1080, CUDA, mdda.net): Qwen 3.6 35B-A3B Q4_K_M has floor N=30 at ~24-25 tok/s with 32 GB RAM. For Qwen3-30B-A3B Q4 on 8 GB, DERIVED arithmetic puts the floor in the same N=28-34 region.
- Models that page well have (a) a high expert fraction of the file, (b) low active-bytes-per-token, (c) fine-grained many-expert routing. Qwen3-30B-A3B-class (128 experts, 8 active), GLM-4.5-Air, gpt-oss (4 active), and Qwen3-Next-80B-A3B (512 experts, 10 active) fit; DeepSeek-V3/R1 671B does not fit consumer RAM at all (config-verified: 256 experts x 44M params x 58 layers means ~373 GB of expert weights at Q4-class rates, DERIVED).

## 2. Mechanism: what the flags actually do

### 2.1 `-ot` / `--override-tensor` (the general mechanism)

- Added by PR #11397 "llama : add option to override model tensor buffers", slaren, merged 2025-01-24 (GitHub issues API search, fetched this session). Syntax per the current server README: `-ot <tensor name pattern>=<buffer type>,...` (server README fetched, master). Env var `LLAMA_ARG_OVERRIDE_TENSOR` added by PR #18267, merged 2025-12-21.
- The tensor-name side is a `std::regex`, applied with `std::regex_search`, i.e. substring semantics: the community shorthand `-ot "exps=CPU"` matches any tensor whose name contains "exps" (all three expert tensors do), and PR #11397's own description cites `-ot exps=CPU` as the canonical example (API fetch).
- Resolution code (raw `src/llama-model-loader.cpp`, fetched this session), the `buft_for_tensor` lambda inside `llama_model_loader::create_tensor`:

```cpp
for (const auto * overrides = tensor_buft_overrides; overrides->pattern != nullptr; ++overrides) {
    std::regex pattern(overrides->pattern);
    if (std::regex_search(tensor_name, pattern)) {
        ...
        break;   // first matching override wins
```

  When the override targets the CPU buffer type it still goes through `select_weight_buft(hparams, t_meta, op, buft_list_cpu)`, which walks a (device, buffer-type) list and returns the first entry where `weight_buft_supported` passes. So a CPU override means "allocate in a host-RAM buffer", not "skip quantization support checks".
- Ordering consequence: because resolution is first-match over the ordered override list, and `--n-cpu-moe` pushes its entries at its position on the command line (PR #15077 implementation, see below), command-line order sets precedence between your `-ot` patterns and the `--n-cpu-moe`-generated ones (inference from the two verified facts; the resolved per-tensor semantics are verified in source).

### 2.2 `--cpu-moe` / `--n-cpu-moe N` (the convenience wrapper)

- PR #15077 "llama : add --n-cpu-moe option", slaren, created and merged 2025-08-04 (GitHub issues API, fetched). Implementation (PR files page fetched this session), in `common/arg.cpp`:
  - `--n-cpu-moe N` loops `for (int i = 0; i < value; ++i)` and appends `string_format("blk\\.%d\\.ffn_(up|down|gate)_exps", i)` per layer, each pushed into `params.tensor_buft_overrides` with `ggml_backend_cpu_buffer_type()`.
  - One alternation `(up|down|gate)_exps` covers all three expert tensors per layer.
  - `--cpu-moe` was refactored in the same PR to the single pattern `\.ffn_(up|down|gate)_exps` mapped to CPU.
  - Negative N rejected with `invalid value`; env `LLAMA_ARG_N_CPU_MOE`; server README confirms help text "keep the Mixture of Experts (MoE) weights of the first N layers in the CPU" and `--cpu-moe` "keep all Mixture of Experts (MoE) weights in the CPU".
- Draft-model variants `--override-tensor-draft`, `--cpu-moe-draft`, `--n-cpu-moe-draft` added by PR #15191, merged 2025-08-09 (API fetch; server README fetched shows the draft flags exist on the server).
- `llama-bench` gained `--n-cpu-moe` support in PR #15952 (merged, created 2025-09-12), which is what makes systematic N sweeps scriptable.
- "First N layers" counts from layer 0 upward; layers N-1 onward keep their experts on GPU. Note some architectures open with dense layers (DeepSeek config: `first_k_dense_replace: 3`; GLM-4.5-Air config: `first_k_dense_replace: 1`, both HF config fetches), where the flag simply has no expert tensors to match for those blocks.

### 2.3 What happens at runtime (why it is fast at all)

- Weights placed in a CPU buffer are computed where they live: the ggml scheduler runs the expert FFN ops on the host, so the per-token cost is host RAM bandwidth for reading only the k activated experts' weights, plus per-layer hidden-state round trips over PCIe between GPU and host. The per-token expert READ is k-of-n sparse: for Qwen3-30B-A3B, 8 of 128 experts per MoE layer (HF config fetch: `num_experts_per_tok: 8`), i.e. ~6.25 percent of the expert bytes per layer per token.
- The same design principle powers KTransformers-style 671B-on-one-GPU setups (surfaced in the override-tensor search this session), and llama.cpp itself markets it as "CPU+GPU hybrid inference" (README fetch).
- `--no-op-offload` exists ("whether to offload host tensor operations to device", default true, raw `common/arg.cpp` grep this session); it does not move CPU-buffered weights to the GPU, it concerns host-side tensor OPS. The expert matmuls stay on CPU regardless, because their weights are CPU-resident.
- Load modes relevant to true disk paging (raw `common/arg.cpp`, fetched this session):
  - `-lm, --load-mode MODE` default `auto`: "auto: mmap, unless a device does not support it"; options none / mmap / mlock / mmap+mlock / dio.
  - `-lzm, --lazy-mode MODE` (default auto): "on: read the rows of such tensors from disk on demand instead of keeping them resident (requires mmap)"; "auto: on, but only for tensors larger than 4 GiB". This is the closest thing to real on-demand paging of tensor rows from disk in current llama.cpp.

## 3. The byte math (why some models page well and others crawl)

Per-token host-traffic lower bound for a CPU-resident expert set:

```
bytes_per_token_CPU ~= sum over CPU-resident MoE layers of ( n_active_experts x bytes_per_expert_layer )
tok/s ceiling ~= effective_system_RAM_bandwidth / bytes_per_token_CPU
real-world efficiency observed: ~50-65 percent of theoretical bandwidth (DERIVED from the mdda.net datapoint, see section 5)
```

- All architecture numbers below are verified from HF `config.json` fetches this session. Per-expert bytes are DERIVED as `3 x hidden_size x moe_intermediate_size` params times an assumed ~0.55-0.6 bytes/param for Q4_K_M-class quants (standard K-quant rate; the rate itself is assumption, the param counts are config facts).

| Model | layers | experts | active | hidden | moe_inter | per-expert params | DERIVED expert slab per layer @ ~0.57 B/param | DERIVED active expert bytes/token (all layers CPU) |
|---|---|---|---|---|---|---|---|---|
| Qwen3-30B-A3B | 48 | 128 | 8 | 2048 | 768 | 4.72M | ~345 MB | ~1.03 GB (48 layers) |
| gpt-oss-20b | 24 | 32 | 4 | 2880 | 2880 (i) | 24.9M | ~422 MB (MXFP4: ~330 MB) | ~0.3-0.4 GB |
| gpt-oss-120b | 36 | 128 | 4 | 2880 | 2880 (i) | 24.9M | ~1.3-1.7 GB | ~1.9-2.4 GB |
| GLM-4.5-Air | 46 (first dense) | 128 + 1 shared | 8 | 4096 | 1408 | 17.3M | ~1.26 GB | ~3.2 GB (40 MoE layers) |
| Qwen3-Next-80B-A3B | 48 (hybrid linear attn, full_attention_interval 4) | 512 | 10 + shared | 2048 | 512 | 3.15M | ~0.92 GB | ~1.5 GB |
| DeepSeek-V3/R1 671B | 61 (first 3 dense) | 256 + 1 shared | 8 | 7168 | 2048 | 44.0M | ~6.4 GB | ~11.6 GB (58 MoE layers) |

(i) gpt-oss config exposes `intermediate_size`, not `moe_intermediate_size`; experts are `hidden x intermediate` per projection, same 3-projection shape, per llama.cpp's GGUF conversion (shape math DERIVED; the config fields are verified).

Reading of the table:

- Small active-bytes-per-token is the king metric. gpt-oss-120b (4 active experts) and Qwen3-30B-A3B (8 small experts) page cheaply per token; GLM-4.5-Air's 12B active and DeepSeek's 37B active are expensive per token and need bandwidth (or much better RAM).
- Fine-grained routing (512 x 10 in Qwen3-Next, 128 x 8 in Qwen3/GLM) spreads reads across many small slabs, which keeps per-layer VRAM chunks small enough to tune N finely. DeepSeek's 6.4 GB per-layer expert slab (DERIVED) is larger than the entire spare VRAM of an 8 GB card, so on such a card effectively all DeepSeek experts belong on CPU and N-tuning is pointless there.
- Total file still has to fit in VRAM + usable RAM. Qwen3-30B-A3B Q4 (~17-19 GB file, DERIVED from 30.5B params at K-quant rates) fits 8 GB VRAM + 16 GB RAM. GLM-4.5-Air Q4 (~60 GB, DERIVED from 106B total, model-card figure not re-verified this session) needs 64 GB class RAM. DeepSeek-V3/R1 Q4 (~373-405 GB, DERIVED + widely known file size, not re-verified) needs server RAM; it is not a consumer-8GB play at all.

## 4. Vulkan on consumer AMD: state of the path

Why Vulkan is the practical AMD consumer path: `docs/build.md` (raw fetch this session) documents HIP/ROCm per GPU architecture (build examples target `gfx1030` / `gfx1100`, i.e. officially supported archs) and states the `HSA_OVERRIDE_GFX_VERSION` workaround for unsupported GPUs is "not supported on Windows". The Vulkan path needs only the Vulkan SDK and `-DGGML_VULKAN=ON`, and is documented for Windows, Linux, Docker, and macOS. The docs do not editorialize a recommendation; the support-surface difference (above) is the fact base for "Vulkan is the low-friction consumer path". Known ROCm-path fragility for this exact workload: issue #15198 "GLM V4.5 Air + ROCm + exps=CPU broken outputs" (closed 2025-08-09, API fetch).

Vulkan MoE timeline (all from GitHub API + PR pages fetched this session):

- 2024-06-03: PR #7628 merges basic Vulkan MoE support (MUL_MAT_ID, SUM_ROWS, DIV shaders); noted as slow, bottleneck in matrix-vector shaders.
- 2025-10-18: PR #16641 "vulkan: Implement topk_moe fused shader, ported from CUDA" - author reports qwen3moe tg128 260 to 285 tok/s (full-GPU bench).
- 2025-10-29: PR #16656 extends topk_moe fusion to gpt-oss late-softmax routing.
- 2025-12-13: PR #17872 allows non-power-of-2 n_experts in topk_moe.
- 2025-12-24: PR #18280 "Vulkan: Tune Flash Attention for MoE on AMD GPUs" (commit 7f459c9, approved by jeffbolznv). AMD benches, all FULL GPU offload (ngl 99), qwen3moe 30B.A3B Q2_K_Medium: Radeon 8060S tg128 94.54 to 101.33 (+7.2 percent with coopmat, +8.2 without); Radeon Pro VII tg128 84.25 to 96.28 (+14.3 percent); RTX 3090 control moved -0.1 to -2 percent. This PR is the strongest evidence that the Vulkan MoE path is being tuned ON AMD hardware specifically.
- 2026-01-05 / 2026-01-20: PRs #18582 (fix topk_moe_sigmoid_norm_bias for GLM-4.6) and #18947 (GLM-4.7-Flash fusion, closed unmerged) show the fusion being chased across new MoE architectures.

Open caveats on this path (verified issue titles/dates via API, bodies not read unless noted):

- #16134 (open, created 2025-09-20): "Vulkan backend shows negative scaling at low batch sizes with MOE models".
- #21895 (closed): "very low tok/s on moe models on radeon vii gpus on ubuntu using vulkan" - old GCN hardware; RDNA-era cards are the sane target, but I found no first-hand RDNA2/3 hybrid tok/s receipt this session (OWED, section 7).
- `--n-cpu-moe` flag maturity bugs on other backends worth knowing before trusting the flag blindly: #15136 and #16579 (multi-GPU splitting), #18143 (router ignores n-cpu-moe), #20414 (breaks with fused gate + up tensors, 2026-03-11), and CUDA-graph interplay #18593 + #18934 (graphs disabled then re-enabled for n-cpu-moe, Jan 2026). Single-GPU 8 GB use dodges the multi-GPU class.

## 5. Tuning rules for 8 GB VRAM

### 5.1 The verified 8 GB datapoint (mdda.net, GTX 1080, CUDA)

Source: "Running ~30B MoE models on an old GTX 1080", https://mdda.net/blog/tech/dl/llama-cpp-moe-on-an-old-gtx-1080 (fetched this session). Hardware: GTX 1080 8 GB (Pascal), i7-6700, 32 GiB RAM, Fedora 42, CUDA build (NOT Vulkan - method transfers, numbers are CUDA's). Models Q4_K_M from an AtomicBot TurboQuant fork:

- Qwen 3.6 35B-A3B: floor `--n-cpu-moe 30` (29 OOMs at both 64k and 128k ctx); ~24-25 tok/s at 64k, ~24 at 128k; raising to 35 worked but slowed to ~21.6.
- Gemma 4 26B-A4B: floor 20 (19 OOMs); ~19.8 tok/s at the floor vs ~16 at N=29; with the built-in MTP draft head plus `--override-tensor-draft "token_embd\.weight=CUDA0"` to keep the draft embedding on GPU, ~24.5 tok/s at ~79 percent acceptance.
- Startup memory breakdown at N=29 (Gemma, 128k ctx): 8107 MiB total = model 2103 + ctx 664 + compute 532 MiB on GPU, ~4.6 GiB free, host held ~14.7 GiB. This is the concrete shape of where 8 GB goes: context and compute buffers, not just weights.
- Bottleneck finding: PCIe-bandwidth-limited (GPU 40-50 percent utilized, link at 8 GT/s under load) - confirms the two-cost model in section 2.3 (expert reads from host RAM plus per-layer PCIe round trips).
- The tuning method, explicitly: start with N high, drop one layer at a time (pushing more experts onto GPU) until OOM, then back off by one. No closed-form formula; the author states none exists. llama-bench + `--n-cpu-moe` (PR #15952) is the scripted version of the same sweep.

### 5.2 Rules of thumb for 8 GB (each labeled)

1. Base command shape: `-ngl 99 --n-cpu-moe N` (all layers' dense parts on GPU, first N layers' experts on CPU). Verified flag semantics, section 2.
2. Expected N for Qwen3-30B-A3B-class Q4_K_M on 8 GB: DERIVED, ~28-34. Arithmetic: ~345 MB expert slab per layer (section 3), leave ~2-3 GB of the 8 for attention/dense/embeddings + KV + compute (mdda's breakdown shows 3.3 GiB GPU usage at his floor), giving ~5 GB for ~14-16 GPU-resident expert layers out of 48, i.e. N ~= 32-34. Consistent with the measured floor 30 for the similar 35B-A3B.
3. gpt-oss-20b on 8 GB: DERIVED, N ~= 12-16 at native MXFP4 (~330 MB/layer, 24 layers; keep ~8-12 layers' experts on GPU). Less benefit per offloaded byte than A3B-class models because the file is only ~12 GB and 4-expert routing already reads little; try full offload after KV-trimming first.
4. RAM bandwidth sets your tok/s ceiling: use section 3's table. Dual-channel DDR5-6000 (~96 GB/s theoretical, ~55-65 effective at the observed 50-65 percent efficiency factor, DERIVED): Qwen3-30B-A3B fully-CPU experts ceiling ~50-60 tok/s, at the 8 GB floor N~32 ceiling ~65-80 tok/s of expert-read time - the measured 24-25 tok/s on older DDR4 shows real runs land well under ceilings (PCIe round trips and CPU compute share the blame, mdda's utilization data).
5. Context length is paid in VRAM and it competes with expert residency: every GB you give KV + compute is a GPU-resident expert layer you must give up (each ~345 MB for A3B-class). mdda's numbers: 664 MiB ctx + 532 MiB compute at his floor. KV quantization frees VRAM but I did not verify the exact flag names this session (OWED).
6. Sweep with llama-bench, do not hand-guess: `-ngl 99` fixed, sweep `-ncmoe` (PR #15952 added the option; comma-list sweep syntax follows llama-bench conventions but I did not verify the list syntax for this specific param).
7. Env-var equivalents for server deployments: `LLAMA_ARG_N_CPU_MOE`, `LLAMA_ARG_CPU_MOE`, `LLAMA_ARG_OVERRIDE_TENSOR` (server README + PR #18267, fetched).
8. Prefer mmap (`--load-mode auto` default): experts are touched lazily, and `--lazy-mode auto` additionally on-demands tensor rows larger than 4 GiB from disk (both verbatim from `common/arg.cpp` this session). Do not use `mlock` on a box where the model + experts nearly fill RAM; the help text itself warns mlock forces residency.

### 5.3 Cookbook (8 GB AMD, Vulkan)

```bash
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release -j

# sweep for the floor (syntax per llama-bench; #15952 added -ncmoe)
build/bin/llama-bench -m Qwen3-30B-A3B-Q4_K_M.gguf -ngl 99 -ncmoe 24,28,30,32,34 -p 0 -n 256

# serve at the found floor
build/bin/llama-server -m Qwen3-30B-A3B-Q4_K_M.gguf \
  -ngl 99 --n-cpu-moe 32 -c 16384
```

Equivalent legacy form (`-ot`, pre-dating the wrapper flags, and still the tool when you want non-uniform splits):

```bash
build/bin/llama-server -m model.gguf -ngl 99 -ot "exps=CPU"          # ALL experts on CPU
build/bin/llama-server -m model.gguf -ngl 99 -ot "ffn_(up|down|gate)_exps\.layer\.([0-9]|1[0-9]|2[0-9]|3[0-1])=CPU"
# (per-layer-range regex form; the exact range regex is your own composition - the mechanism
#  (regex_search, first match wins, buffer type after '=') is verified in section 2.1)
```

Caution: `-ot "exps=CPU"` matches by substring and wins or loses by list order against `--n-cpu-moe`-generated entries (section 2.1). mdda's draft-embedding trick shows the fine-grained use: `--override-tensor-draft "token_embd\.weight=CUDA0"` forced the draft model's embedding onto the GPU and was worth ~3 tok/s on his box. The equivalent Vulkan device token (the `CUDA0` analogue) was NOT verified this session - grep of `ggml-vulkan.cpp` found no literal device-name string with my patterns (OWED; check `--device` output on your build).

## 6. Which MoE models page well

Paging well = high expert fraction, low active bytes/token, fine-grained experts, and a file that fits VRAM + sane RAM. Verified configs in section 3; verdicts combine those with the verified bench receipts above.

Pages well (8 GB VRAM tier):

- Qwen3-30B-A3B (+ the Coder 30B-A3B variant): the canonical case. 128 x 8 fine-grained routing, ~345 MB/layer slabs, ~21.5 MB active reads per CPU layer per token (DERIVED). mdda's 35B-A3B sibling: floor N=30, ~24-25 tok/s on 8 GB + 32 GB RAM.
- Gemma 4 26B-A4B (A4B routing, 4 active): floor N=20 on 8 GB, ~20-24.5 tok/s with MTP (mdda.net, verified receipt).
- gpt-oss-20b: tiny active-byte profile (4 experts), MXFP4 keeps the file at ~12 GB; Vulkan's late-softmax topk_moe fusion (#16656) exists specifically for its routing. On 8 GB only a few layers offload (DERIVED N~12-16), so treat it as "mostly fits" rather than a paging showcase.

Pages well (needs 64 GB-class RAM alongside the 8 GB card):

- GLM-4.5-Air (106B-A12B): 128 experts x 8 active, ~1.26 GB/layer slabs (DERIVED). Community interest is high and the ROCm bug #15198 was filed against exactly this model with `exps=CPU`, which is itself evidence the hybrid pattern is the standard way people run it. No first-hand tok/s receipt verified this session (OWED).
- Qwen3-Next-80B-A3B: config-verified 512 experts x 10 active, hybrid linear attention (full attention only every 4th layer), the most fine-grained routing in the table - cheap per-token reads. Mainline llama.cpp runs it per a Jan 2026 GitHub thread ("Qwen3 Next seems to work well with the lower batch size", search-surfaced, secondary); the original support PR number was not found this session (OWED).

Not a consumer-8GB play (verified configs):

- DeepSeek-V3 / R1 671B: 256 x 8 with 44M-param experts (config-verified) means 6.4 GB expert slabs per layer and ~11.6 GB active reads per token across 58 MoE layers (DERIVED) - it requires server-class RAM (384 GB+ at Q4) and bandwidth; on an 8 GB desktop card the N flag has nothing useful to tune.
- gpt-oss-120b: 4-expert routing pages cheaply per token (~2 GB/token DERIVED) but the ~63 GB file needs 64 GB+ RAM; viable hybrid, wrong tier for this ask.
- Kimi K2, Llama-4, Mixtral, Hunyuan: NOT examined this session - no config fetch, no bench receipt. Listed here only to mark the gap (OWED if needed).

## 7. Sources banked by name

Primary (fetched this session):

1. `tools/server/README.md` (raw.githubusercontent.com, master) - flag help text: `-ngl`, `-ot`, `-cmoe`, `-ncmoe`, env vars `LLAMA_ARG_*`, draft variants, `--override-kv`.
2. `src/llama-model-loader.cpp` (raw, master) - `buft_for_tensor` first-match-wins override resolution, `std::regex_search`, CPU override goes through `select_weight_buft(..., buft_list_cpu)`.
3. `common/arg.cpp` (raw, master, via curl grep) - `--no-op-offload` help, `-lm/--load-mode` (auto/mmap/mlock/mmap+mlock/dio, default auto), `-lzm/--lazy-mode` (on/auto/off, on-demand rows >4 GiB requires mmap), `--numa`.
4. `README.md` (raw, master) - "CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity".
5. `docs/build.md` (raw, master) - HIP per-arch GPU_TARGETS examples gfx1030/gfx1100, `HSA_OVERRIDE_GFX_VERSION` "not supported on Windows", Vulkan documented cross-OS.
6. `ggml/src/ggml-vulkan/ggml-vulkan.cpp` (raw, curl grep) - checked for device-name literals; none matched my patterns (negative result, section 5.3).
7. GitHub issues API: `repo:ggml-org/llama.cpp n-cpu-moe in:title` - PR #15077 (added --cpu-moe/--n-cpu-moe, slaren, merged 2025-08-04), #15191 (draft variants, merged 2025-08-09), #15952 (llama-bench support), #15975, #15136/#15538/#16579/#18143 (multi-GPU/router bugs), #18593/#18934 (CUDA graphs off/on), #20414 (fused gate+up bug).
8. GitHub issues API: `override-tensor in:title` - PR #11397 (added -ot, slaren, merged 2025-01-24), #18267 (env var), #15198 (GLM-4.5-Air ROCm exps=CPU broken).
9. GitHub issues API: `vulkan moe in:title` - PR #7628 (2024-06-03), #16641 (topk_moe port, qwen3moe tg128 260 to 285), #16656 (gpt-oss late softmax), #17872 (non-pow2 experts), #18280 (AMD FA tune), #16134 (negative scaling, open), #21895 (Radeon VII slow).
10. PR #15077 files page - implementation quotes: `blk\.%d\.ffn_(up|down|gate)_exps` generation, `ggml_backend_cpu_buffer_type()` mapping, `static std::list<std::string> buft_overrides` lifetime fix.
11. PR #18280 page - AMD bench tables (Radeon 8060S, Radeon Pro VII numbers in section 4), merge date 2025-12-24, commit 7f459c9, reviewer jeffbolznv.
12. Issue #13616 page - no sizing formula exists in-tree; the offered method is `llama-gguf file.gguf r n` piped through awk/sort to list tensors by size (bennmann, 2025-05-18).
13. HF `config.json` fetches: Qwen/Qwen3-30B-A3B-Instruct-2507, zai-org/GLM-4.5-Air, openai/gpt-oss-20b, openai/gpt-oss-120b, deepseek-ai/DeepSeek-V3, Qwen/Qwen3-Next-80B-A3B-Instruct (all fields in section 3 table).

Secondary (fetched, concrete numbers):

14. mdda.net, "Running ~30B MoE models on an old GTX 1080", https://mdda.net/blog/tech/dl/llama-cpp-moe-on-an-old-gtx-1080 - the 8 GB floor methodology and numbers in section 5.1. CUDA on NVIDIA; the method transfers, the tok/s numbers are not Vulkan-on-AMD numbers.

Search-surfaced, NOT independently verified (treat as leads, not receipts):

15. TechPowerUp forum thread - 7900 XTX, llama.cpp Vulkan, Unsloth Qwen3 35B-A3B Q4, 130-140 tok/s at ~20.5 GB VRAM (full offload, not hybrid).
16. vramcalculator.com - @splizard 7900 XTX 48.5 vs 71 tok/s software-stack spread; smol.ai AINews - "7900 XTX Vulkan comparable to a 4090, CUDA ~10 percent faster". Both secondhand summaries.
17. Qwen3-Next mainline support: Jan 2026 GitHub thread quote (search snippet only); original PR number OWED.
18. latent.space AINews - "~20-21 tok/s using --cpu-moe" for a 35B-A3B-class model, hardware unstated.

## 8. Not verified / OWED

- No primary-source tok/s benchmark of `--n-cpu-moe` hybrid inference on a consumer RDNA2/3 card (7800 XT / 9070 XT class) over Vulkan was found in this session. The closest verified anchors are mdda.net (8 GB, CUDA) and PR #18280 (AMD, Vulkan, full offload only). If the fleet has a 7800 XT / 9070 XT in reach, the 20-minute receipt is: build with `-DGGML_VULKAN=ON`, run the section 5.3 sweep, file the llama-bench rows.
- Exact Vulkan device token for `-ot <pattern>=<Vulkan-device>` (the analogue of mdda's `CUDA0`): not verified; grep of ggml-vulkan.cpp found no name literal under my patterns.
- KV-cache quantization flag names: not verified this session, not named in section 5.2 beyond the concept.
- Qwen3-Next original support PR number in ggml-org/llama.cpp: not found.
- The igorsky.de MoE-offload article: searched four phrasings, not located; dropped rather than paraphrased from memory.
- All per-layer/per-token byte figures labeled DERIVED assume ~0.55-0.6 bytes/param for Q4_K_M-class and ~0.53 for MXFP4; the parameter counts behind them are config-verified, the bytes-per-param rate is a standing approximation, and none of the derived VRAM figures were measured on hardware here.
