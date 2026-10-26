# GPU LADDER evidence (o5-gpu-ladder, 2026-10-07) - verbatim captured command outputs

Each block names the command that produced it. Captured during the live test; the LM Studio server was stopped and the imported gguf copy removed after measurement (see watch/inbox/GPU_LADDER_20261007.md Dismount).

## Card detection

Command: `wmic path win32_VideoController get name,adaptercompatibility,driverversion`

```
AdapterCompatibility    DriverVersion        Name
Advanced Micro Devices, Inc. 32.0.21045.5002  AMD Radeon RX 5600 XT
```

Command: `powershell -NoProfile -Command "Get-CimInstance Win32_VideoController | ForEach-Object { '{0} | driver {1} | {2} MB' -f $_.Name, $_.DriverVersion, [math]::Round($_.AdapterRAM/1MB) }"`

```
AMD Radeon RX 5600 XT | driver 32.0.21045.5002 | 4095 MB
```

(WMI AdapterRAM 4095 MB is the 32-bit WMI cap on this 6 GB card; true VRAM below from the ollama Vulkan log.)

## Ollama GPU path (rung 3)

Command: `grep -i "gfx|vulkan|rocm|cuda|gpu|unsupported|warning" C:/Users/foste/AppData/Local/Ollama/server.log` (tail, excerpt)

```
cmn  common_param:   - Vulkan0 : AMD Radeon RX 5600 XT (6128 MiB, 5334 MiB free)
common_params_fit_impl:   - Vulkan0 (AMD Radeon RX 5600 XT): 11 layers,   4108 MiB used,   1226 MiB free
load_tensors: offloading output layer to GPU
load_tensors: offloading 10 repeating layers to GPU
load_tensors: offloaded 11/65 layers to GPU
```

Command: `curl -s http://127.0.0.1:11434/api/generate ... gemma:2b num_predict 256 temperature 0` (two runs) then `ollama ps`

```
RUN 1 eval_count: 168 eval_duration: 1983706000 prompt_eval_count: 47 load_duration: 25157000 tok_s: 84.7
RUN 2 eval_count: 165 eval_duration: 1938823000 prompt_eval_count: 47 load_duration: 10312000 tok_s: 85.1
NAME        ID              SIZE      PROCESSOR    CONTEXT    UNTIL
gemma:2b    b50d6c999e59    2.1 GB    100% GPU     8192       14 minutes from now
```

Command: same shape on qwen2.5:7b, then `ollama ps`

```
qwen2.5:7b eval_count: 128 eval_duration: 6468348000 tok_s: 19.8
NAME          ID              SIZE      PROCESSOR          CONTEXT    UNTIL
qwen2.5:7b    845dbda0ea48    5.4 GB    18%/82% CPU/GPU    8192       4 minutes from now
```

## Ollama ROCm kernel inventory (rung 6 ladder row: no gfx1010)

Command: `find .../lib/ollama/rocm_v7_1 -iname "*gfx*"` (excerpt)

```
Kernels.so-000-gfx1030.hsaco
Kernels.so-000-gfx1100.hsaco
Kernels.so-000-gfx1101.hsaco
Kernels.so-000-gfx1102.hsaco
Kernels.so-000-gfx1150.hsaco
Kernels.so-000-gfx1151.hsaco
Kernels.so-000-gfx1200.hsaco
Kernels.so-000-gfx1201.hsaco
Kernels.so-000-gfx906-xnack-.hsaco
```

No gfx1010/gfx1011/gfx1012 file exists in that tree.

## LM Studio/Bionic Vulkan test (rung 1)

Command: `curl -s -H "Content-Type: application/json" http://127.0.0.1:1234/api/v0/chat/completions -d '{...gemma-2b, 256 max_tokens, temperature 0...}'` then `.venv/Scripts/python.exe` dump of the response envelope (model warm; first JIT-cold run read tokens_per_second 53.07821128594424)

```json
{
 "model": "gemma-2b",
 "usage": {"prompt_tokens": 32, "completion_tokens": 148, "total_tokens": 180},
 "stats": {"tokens_per_second": 53.07821128594424, "time_to_first_token": 0.638079, "generation_time": 3.4075770000000003, "stop_reason": "eosFound"},
 "model_info": {"arch": "gemma", "quant": "Q4_0", "format": "gguf", "context_length": 8192},
 "runtime": {"name": "llama.cpp-win-x86_64-vulkan-avx2", "version": "2.53.0", "supported_formats": ["gguf"]}
}
```

Two warm reruns of the same request (loop output):

```
RUN 2 tok_s: 72.97 ttft_s: 0.015819 gen_s: 2.03 tokens: 148
RUN 3 tok_s: 72.86 ttft_s: 0.01485 gen_s: 2.032 tokens: 148
```

Command: `curl -s -m 4 -o /dev/null -w "LMS_PORT:%{http_code}" http://127.0.0.1:1234/v1/models` AFTER `lms server stop`:

```
LMS_PORT:000
```

## Import provenance (since reverted, one-line re-import documented in the receipt)

Command: `cat ~/.ollama/models/manifests/registry.ollama.ai/library/gemma/2b` (layers excerpt)

```
application/vnd.ollama.image.model sha256:c1864a5eb19305c40519da12cc543519e48a0697ecd30e15d5ac228644957d12 1678447520
```

That blob was copied to .lmstudio/models/mag-lane/gemma-2b-q4_0/gemma-2b-q4_0.gguf for the test and deleted after (`rm` verified by the models/ tree listing returning to the original 6 directories: Qwen, bridge-inbox, deepseek-ai, google, ollama, saelis-31b).

## Web captures (searches run 2026-10-07, verbatim fragments with sources)

- Used-price captures: "RTX 3060 12GB (used): roughly $180-300 depending on condition and market" and "RX 6700 XT (used): about $210-250 on eBay as of July 2026". Sources: siliconcomps.com used-GPU price tracker, promptquorum.com "Best Budget GPU for Local LLMs 2026", pcpartdeals.eu "RTX 3060 vs RX 6700 XT" comparison.
- llama.cpp issue 20564 (github.com/ggml-org/llama.cpp/issues/20564, CLOSED): RDNA1 gfx1010 ROCm-backend crash, "HSA_STATUS_ERROR_MEMORY_APERTURE_VIOLATION", reporter trace "hipMalloc started returning addresses beyond the gfx1010 aperture after ROCm 5.3"; flags listed: HSA_OVERRIDE_GFX_VERSION=10.3.0, ROC_ENABLE_PRE_VEGA=1, HSA_ENABLE_SDMA=0.
- llama.cpp issue 20515 (github.com/ggml-org/llama.cpp/issues/20515): Vulkan backend vk::DeviceLostError crashes, sensitive to -ubatch-size tuning.
- exo-explore/exo issue 434 "Rocm support planned" OPEN (github.com/exo-explore/exo/issues/434): no confirmed proper ROCm path; exo's supported shape is macOS Metal + Linux NVIDIA CUDA; no Windows/AMD support landed through 2026 (exo README, deepwiki exo build-system page).
- AMD HIP SDK for Windows system requirements (rocm.docs.amd.com): Windows ROCm/HIP officially supports RX 7000/9000 series; RDNA1/2 consumer cards stay off the Windows support list.
