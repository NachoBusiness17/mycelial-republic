# THE GPU LADDER (o5-gpu-ladder, overnight-mesh-20261007, 2026-10-07)

Question: what gets SUSTAINED GPU usage on this box? Method: byte-investigate every rung, test the free door live, cost the paid rungs, name but do not execute any purchase (operator asleep law).

## The card (byte evidence, this box)

- `wmic path win32_VideoController get name,adaptercompatibility,driverversion`: "Advanced Micro Devices, Inc. | 32.0.21045.5002 | AMD Radeon RX 5600 XT".
- True VRAM from the running ollama server log (`C:/Users/foste/AppData/Local/Ollama/server.log`): "Vulkan0 : AMD Radeon RX 5600 XT (6128 MiB, 5334 MiB free)". Note: WMI AdapterRAM reports only 4095 MB for this card (32-bit WMI cap), so never read VRAM from Win32_VideoController.
- gfx1010, RDNA1. AMD HIP SDK on Windows officially supports RX 7000/9000 only; RDNA1/2 stay off the ROCm-Windows support list (source: AMD HIP SDK system requirements, rocm.docs.amd.com).

## THE LADDER, ranked by cost x sustained-usage likelihood

| # | Rung | Cost | Sustained-usage likelihood | Measured/status |
|---|------|------|---------------------------|-----------------|
| 1 | Ollama 0.34.3 Vulkan backend (already running, PID 16804 per memory/attention.md roster) | $0 | HIGHEST - it is already the estate eye (docker-compose OLLAMA_HOST eye note) | gemma:2b 100% GPU 84.7/85.1 tok/s; qwen2.5:7b 18%/82% CPU/GPU 19.8 tok/s (timings captured: watch/inbox/gpu_ladder_20261007_evidence.md) |
| 2 | LM Studio/Bionic Vulkan door (the :1234 BIONIC_BASE_URL seat) | $0 | HIGH - the compose file already names this seat; needs a one-line gguf import | gemma-2b Q4_0 warm 72.97/72.86 tok/s, TTFT 15 ms, runtime llama.cpp-win-x86_64-vulkan-avx2 v2.53.0 (envelope captured: watch/inbox/gpu_ladder_20261007_evidence.md) |
| 3 | llama.cpp RPC desktop+bob (steal map P3 probe) | $0 | MEDIUM - untested here; the door when a model will not fit | probe staged in watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md P3 |
| 4 | Used RX 6700 XT 12GB drop-in | ~$210-250 used, captured in watch/inbox/gpu_ladder_20261007_evidence.md | MEDIUM-HIGH - ollama's rocm_v7_1 already ships gfx1030 ROCm kernels on disk; zero software change, stays AMD, 2x VRAM | NOT purchased (operator-gated) |
| 5 | Used RTX 3060 12GB drop-in | ~$180-300 used, captured in watch/inbox/gpu_ladder_20261007_evidence.md | MEDIUM - widest software door (CUDA: exo becomes viable, LM Studio nvidia-cuda runtimes 2.28.2/2.31.2 and ollama cuda_v12/cuda_v13 ALREADY staged on disk) | NOT purchased (operator-gated) |
| 6 | ROCm on THIS RX 5600 XT | n/a | DEAD - the ollama rocm_v7_1 kernel inventory in watch/inbox/gpu_ladder_20261007_evidence.md carries gfx1030/1100/1101/1102/1150/1151/1200/1201/gfx906 and NO gfx1010; upstream llama.cpp issue 20564 (also captured there) documents the RDNA1 ROCm aperture violation | documented, no action |

## Rung details

### Rung 1: LM Studio/Bionic - TESTED, the free door is real

- Installed: registry key HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\7c1a7243-201d-510b-a8e1-803c5b933ce8 reads DisplayName "Bionic 1.1.6+3", Publisher "LM Studio", InstallLocation C:\Users\foste\AppData\Local\Programs\Bionic (Bionic.exe 225,493,176 bytes, 2026-09-23). Bionic IS the LM Studio app.
- At lane start :1234 was DEAD (curl HTTP:000 after 2.0 s). The C:/Users/foste/.lmstudio tree had 2.4 GB but the models/ tree was EMPTY (0 bytes) - the 2.0 GB in extensions/backends is runtimes: llama.cpp-win-x86_64-vulkan-avx2 at 2.28.2, 2.29.1, 2.31.2, 2.41.0, 2.45.0 plus nvidia-cuda at 2.28.2/2.31.2, plus vendor win-llama-vulkan-vendor-v2.
- Test executed: copied the ollama gemma:2b gguf layer (blob sha256-c1864a5eb19305c40519da12cc543519e48a0697ecd30e15d5ac228644957d12, 1,678,447,520 bytes) to .lmstudio/models/mag-lane/gemma-2b-q4_0/gemma-2b-q4_0.gguf, ran `lms server start` (port 1234 up), first request JIT-loaded, then two warm runs against /api/v0/chat/completions (148 completion tokens each, temperature 0): tokens_per_second 72.97 then 72.86, time_to_first_token 0.0158/0.0149 s, and the response envelope names the runtime: "llama.cpp-win-x86_64-vulkan-avx2" version "2.53.0" - LM Studio serves this AMD card through Vulkan, no ROCm anywhere in the path.
- Cleanup: gguf copy and server flagged below in Dismount.

### Rung 2: llama.cpp Vulkan on gfx1010 (RDNA1) - works, proven live on this box

- The live proof IS rung 1: stock llama.cpp (LM Studio's vulkan runtime 2.53.0) ran gemma-2b Q4_0 at ~73 tok/s warm on the RX 5600 XT with zero crashes across 3 requests (the first run also absorbed JIT load at 53.08 tok/s).
- Upstream caveat 1: llama.cpp issue 20564 (github.com/ggml-org/llama.cpp/issues/20564, CLOSED) is a ROCm-backend crash on RX 5500 XT (gfx1010): hipMalloc returns addresses beyond the gfx1010 aperture after ROCm 5.3, HSA_STATUS_ERROR_MEMORY_APERTURE_VIOLATION 0x29; reporter-suggested flags were HSA_OVERRIDE_GFX_VERSION=10.3.0, ROC_ENABLE_PRE_VEGA=1, HSA_ENABLE_SDMA=0. This is the ROCm path, not the Vulkan path - it is one more reason this card rides Vulkan.
- Upstream caveat 2: llama.cpp issue 20515 documents Vulkan vk::DeviceLostError crashes sensitive to -ubatch-size; if a bare llama.cpp Vulkan build ever device-losts here, first knob is -ub (256/512).

### Rung 3: Ollama AMD/RDNA1 - the "unsupported" expectation is OVERTURNED by bytes

- Expectation on file: RDNA1 unsupported. Byte truth: ollama 0.34.3 ships C:\Users\foste\AppData\Local\Programs\Ollama\lib\ollama\vulkan\ggml-vulkan.dll (41,656,712 bytes) and the 29h-old `ollama serve` (PID 16804, longrunner roster memory/attention.md 2026-10-07T00:37:23Z) has been running models on "Vulkan0 (AMD Radeon RX 5600 XT)": server.log line "common_params_fit_impl:   - Vulkan0 (AMD Radeon RX 5600 XT): 11 layers,   4108 MiB used,   1226 MiB free" and "load_tensors: offloaded 11/65 layers to GPU" (verbatim capture: watch/inbox/gpu_ladder_20261007_evidence.md).
- Measured on the live server (POST /api/generate, stream false, temperature 0, keep_alive 15m): gemma:2b eval_count 168 at 1,983,706,000 ns = 84.7 tok/s and 165 at 1,938,823,000 ns = 85.1 tok/s, `ollama ps` reads "100% GPU"; qwen2.5:7b 128 tokens in 6,468,348,000 ns = 19.8 tok/s, `ollama ps` reads "18%/82% CPU/GPU".
- Verdict: on RDNA1 the ollama GPU door is Vulkan, and ROCm is reserved for RDNA2+ (see rung 6). The 6 GB card fully offloads the 2B janitor class at ~85 tok/s and part-offloads 7B at ~20 tok/s. The "expect unsupported, document" rung is closed as WRONG for 0.34.x - keep HSA_OVERRIDE_GFX_VERSION tricks in the drawer for the ROCm path only.

### Rung 4: exo on Windows/AMD - weak, as expected

- exo-explore/exo issue 434 "Rocm support planned" is the long-standing open AMD request; exo's supported shape is macOS (Metal) + Linux (NVIDIA/CUDA); no Windows/AMD path landed through 2026 (sources: github.com/exo-explore/exo/issues/434, exo README, deepwiki build-system page). Do not build the mesh inference plan on exo for this box.
- The estate already named the substitute: llama.cpp RPC split (steal map steal 2 + probe P3). This lane adds: the RPC hosts do NOT need a GPU each - the desktop's Vulkan llama.cpp and bob's silicon both speak the same llama.cpp dialect.

### Rung 5: the paid rungs, costed - NOT executed (operator asleep law)

- Used RX 6700 XT 12GB, ~$210-250 (eBay July 2026 market): drop-in for THIS seat. Unlocks: ollama's ROCm path lights up with zero software change because rocm_v7_1 already ships gfx1030 kernels byte-verified on this disk; 12 GB doubles the envelope so qwen2.5:7b goes 100% GPU (est. well above the measured 19.8 tok/s partial split), gemma4/gemma4-desk (9.6 GB) fully offloads, qwen2.5:32b and athena-class (32 GB) part-offload meaningfully, the ALoDLM garden's later rungs (7B/14B teachers) stop being CPU-bound. Stays AMD: the Vulkan door (rungs 1-2) keeps working unchanged.
- Used RTX 3060 12GB, ~$180-300 (2026 used market): the ecosystem pick. Unlocks: CUDA everywhere - the LM Studio nvidia-cuda runtimes (2.28.2/2.31.2) and ollama cuda_v12/cuda_v13 libs are ALREADY on disk from prior installs, so the software cost is zero; exo becomes viable (Linux CUDA shape), the garden reaches 14B-class full offload at usable tok/s, and SD/video tooling opens. Cost: leaves the AMD path, adds a second driver stack.
- Both are named, priced, and gated. NO purchase, NO order, NO driver install was executed. ALoDLM's FIRST rung needs neither card: deepseek-r1:1.5b (1.1 GB, on disk) fits the current 6 GB - the free door runs the 1.7B probe today (steal map: "pairs with the ALoDLM garden probe (1.7B first)", watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md:45).

### Rung 6: bob's GPU - exact detection commands

Windows seat (TESTED on this box, output "AMD Radeon RX 5600 XT | driver 32.0.21045.5002 | 4095 MB"):

```
powershell -NoProfile -Command "Get-CimInstance Win32_VideoController | ForEach-Object { '{0} | driver {1} | {2} MB' -f $_.Name, $_.DriverVersion, [math]::Round($_.AdapterRAM/1MB) }"
```

Legacy Windows (TESTED on this box):

```
wmic path win32_VideoController get name,adaptercompatibility,driverversion
```

TRUE VRAM (WMI caps at 4095 MB on >4 GB cards - proven here): run any model load once and read the log, or on a Linux seat:

```
lspci -nn | grep -Ei 'vga|display|3d' && vulkaninfo --summary 2>/dev/null | grep -i deviceName
```

Linux lines are copy-standard but NOT executed on this seat (no Linux host here); the Windows lines are byte-tested above. For bob's true VRAM over an ollama seat regardless of OS: `curl -s http://127.0.0.1:11434/api/ps` after a load, or read the server.log Vulkan/NVIDIA device line, which prints exact MiB (this box: "6128 MiB, 5334 MiB free").

## Dismount (what this lane left behind)

- LM Studio server: STARTED for the test (:1234), then `lms server stop` - leaving it up would add a second 24/7 inference longrunner while the longrunner patrol is still awaiting the operator ruling on ollama serve (memory/attention.md 2026-10-07T00:38:38Z LEFT ALIVE row). If the operator wants the Bionic seat live, `C:/Users/foste/.lmstudio/bin/lms.exe server start`.
- The imported gguf copy was REMOVED after measurement (anti-duplication, TS-08 lesson: the estate already flags 8.3 GB live duplication). One-line re-import when the Bionic seat is wanted: copy ollama blob sha256-c1864a5eb19305c40519da12cc543519e48a0697ecd30e15d5ac228644957d12 to .lmstudio/models/mag-lane/gemma-2b-q4_0/gemma-2b-q4_0.gguf.
- The empty .lmstudio/models dirs (Qwen2.5-3B-Instruct, DeepSeek-R1-Distill-Qwen-1.5B, Gemma-2B, gemma4-desk-latest, saelis-31b) predate this lane - someone planned these downloads and never pulled; the ollama twins of the same models are on disk, so the pulls are unnecessary duplication.

## Sources

- Live bytes this box: wmic/PowerShell output quoted above; C:/Users/foste/AppData/Local/Ollama/server.log; C:/Users/foste/AppData/Local/Programs/Ollama/lib/ollama/ tree listing; C:/Users/foste/.lmstudio tree + registry uninstall key 7c1a7243-201d-510b-a8e1-803c5b933ce8; LM Studio /api/v0/chat/completions responses (tokens_per_second 72.97/72.86, runtime llama.cpp-win-x86_64-vulkan-avx2 2.53.0); ollama /api/generate timings and `ollama ps` output.
- Estate: docker-compose.yml:26-35 (Bionic/LM Studio seat notes); watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md (exo steal 1, RPC steal 2 + P3, ALoDLM garden probe line 45); memory/attention.md longrunner rows 2026-10-07T00:30-00:38Z; memory/runs/mickey17_v2/runs/overnight-mesh-20261007/lanes/o5-gpu-ladder.json (this lane's row file).
- Web: [llama.cpp issue 20564](https://github.com/ggml-org/llama.cpp/issues/20564), [llama.cpp issue 20515](https://github.com/ggml-org/llama.cpp/issues/20515), [exo issue 434](https://github.com/exo-explore/exo/issues/434), [exo repo](https://github.com/exo-explore/exo), [exo build system](https://deepwiki.com/exo-explore/exo/9.1-build-system-and-dependencies), [AMD HIP SDK Windows system requirements](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html), [used GPU prices](https://siliconcomps.com/used-gpu-prices/), [budget GPUs for local LLMs](https://www.promptquorum.com/local-llms/best-budget-gpus-local-llm), [3060 vs 6700 XT](https://pcpartdeals.eu/articles/comparisons/rtx-3060-vs-rx-6700-xt).
