# X INTEL: DEEPGEMM DROP 2026-10-01

Estate-side build lane. Three probes, all byte-honest. Sherpa triangulation already banked at
`memory/runs/hermes_burn/deepgemm_results.jsonl` (4 asks, all ok, 1 attempt each, total spend $0.002365).

## THE DROP

DeepSeek open-sourced **DeepGEMM** (MIT): GPU math library for FP8 (E4M3/E5M2), FP4 (MXFP4/NVFP4), and BF16 dense
plus MoE grouped GEMM, designed to pair with DeepEP all-to-all. Load-bearing pattern: **no install-time CUDA
build**. Kernels are emitted as CUDA C++ at first call, compiled by NVRTC into a cubin, and cached on disk keyed
by (shape, dtype, arch), so `import deep_gemm` works without nvcc and only the first call pays latency.

Sherpa verdicts already on file (field `out`, rows 1-4):
1. **mechanics**: runtime NVRTC JIT + disk cache; per-block FP8 scaling fused into epilogue; persistent
   grouped-GEMM scheduler for MoE; stream/event overlap with DeepEP.
2. **amd-vulkan**: our box is AMD RX 5600 XT, gfx1010 RDNA1. No MFMA, no cooperative matrix
   (VK_KHR_cooperative_matrix absent), only V_DOT2/V_DOT4. **DeepGEMM patterns do NOT port.**
3. **precision**: for 6 GB VRAM + 2B-7B models the practical band is Q4_K_M/Q5_K_M for 7B and
   Q5_K_M/Q6_K for 2B. FP8/FP4 unavailable on this card. Sub-3B, math/reasoning, and distilled models are the
   most low-bit intolerant class.
4. **moe-mating**: nobody exports merged/mated models as MoE; the door is unbuilt (premium adjudication ask
   staged separately, not this lane).

## QUANT PROBE

Ollama UP at probe time (2026-10-01). Exact `ollama list` output:

```
NAME                                               ID              SIZE      MODIFIED
hf.co/prism-ml/Ternary-Bonsai-2-27B-gguf:PTQ1_0    d3b5a12ac87f    6.6 GB    7 days ago
athena-class:latest                                a2237b80aba5    32 GB     9 days ago
frob/ling-3.0-flash:latest                         e9709a9878a0    77 GB     2 weeks ago
qwen2.5:7b                                         845dbda0ea48    4.7 GB    3 weeks ago
maze-keeper:latest                                 4b70a6791a49    19 GB     4 weeks ago
gemma:2b                                           b50d6c999e59    1.7 GB    4 weeks ago
deepseek-r1:1.5b                                   e0979632db5a    1.1 GB    6 weeks ago
qwen2.5vl:3b                                       fb90415cde1e    3.2 GB    7 weeks ago
qwen2.5:32b                                        9f13ba1299af    19 GB     7 weeks ago
qwen2.5-coder:7b                                   dae161e27b0e    4.7 GB    7 weeks ago
qwen-desk:latest                                   01b6981310d9    1.9 GB    8 weeks ago
qwen2.5:3b-instruct                                357c53fb659c    1.9 GB    8 weeks ago
gemma4-desk:latest                                 8b8796e7d24b    9.6 GB    8 weeks ago
gemma4:latest                                      c6eb396dbd59    9.6 GB    2 months ago
gemma4-hermes:latest                               bff15bb1649a    9.6 GB    2 months ago
nomic-embed-text:latest                            0a109f422b47    274 MB    2 months ago
```

Per-model facts from `ollama show` (architecture / parameters / quantization, verbatim):

| model | arch | params | quant | disk | ctx |
|---|---|---|---|---|---|
| gemma:2b (SCUT) | gemma | 3B | **Q4_0** | 1.7 GB | 8192 |
| deepseek-r1:1.5b | qwen2 | 1.8B | **Q4_K_M** | 1.1 GB | 131072 |
| qwen2.5:3b-instruct | qwen2 | 3.1B | Q4_K_M | 1.9 GB | 32768 |
| qwen2.5vl:3b | qwen25vl | 3.8B | Q4_K_M | 3.2 GB | 128000 |
| qwen2.5:7b | qwen2 | 7.6B | Q4_K_M | 4.7 GB | 32768 |
| qwen2.5-coder:7b | qwen2 | 7.6B | Q4_K_M | 4.7 GB | 32768 |
| gemma4:latest (SHORT WORKER) | gemma4 | 8.0B | Q4_K_M | 9.6 GB | 131072 |
| nomic-embed-text:latest | nomic-bert | 137M | F16 | 274 MB | 2048 |

Comparison against the sherpa band (7B: Q4_K_M/Q5_K_M; 2B: Q5_K_M/Q6_K):

- **gemma:2b VIOLATES the 2B band.** It runs Q4_0 (the older non-K quant, the weakest of the Q4 family), and
  sherpa row 3 says sub-3B instruction-following degrades first at low bits. TICKET: pull a Q5_K_M or Q6_K 2B
  build (e.g. `gemma2:2b-instruct-q5_K_M` or the hf.co mirror), estimated ~2.0-2.3 GB on disk (estimate, not
  measured), fits the 6 GB card with full KV. The scut is the estate's always-on janitor; this is the cheapest
  quality-per-byte win on the box.
- **deepseek-r1:1.5b sits in the WORST tolerance class for its quant.** Sherpa: math/reasoning + distilled +
  sub-3B = intolerant; Q4_K_M is below the 2B band. It is Qwen2.5-Math lineage (arch qwen2, 1.8B). TICKET:
  re-pull at Q5_K_M, estimated ~1.3 GB (estimate, not measured).
- qwen2.5:3b-instruct and qwen2.5vl:3b at Q4_K_M: borderline (between the intolerant 2B band and the tolerant 7B
  band). No forced ticket; Q5_K_M optional if reasoning complaints surface.
- qwen2.5:7b and qwen2.5-coder:7b at Q4_K_M: **ALIGNED** with the 7B band. No action. (Coder class is "marginal"
  per sherpa; Q5_K_M optional only if HumanEval-class output degrades.)
- nomic-embed-text F16 at 274 MB: fine, embeddings do not need the ticket.
- **gemma4 size anomaly (open inspection item):** 8.0B params at Q4_K_M should land near 4.9 GB
  (~0.57 bytes/param); the disk reads 9.6 GB (~1.2 bytes/param). Capabilities list vision + audio + tools +
  thinking, and `ollama show` on this build does not break out layers, so the extra ~4.7 GB is unexplained by
  visible metadata (multimodal towers and/or layered blobs are candidates, not confirmed). Audit the blob layers
  before any gemma4 re-pull decision. Also note 9.6 GB exceeds the 6 GB VRAM: this worker is already offload/CPU
  lane territory.
- Large models (athena-class 32 GB, frob/ling-3.0-flash 77 GB, qwen2.5:32b 19 GB, maze-keeper 19 GB,
  Ternary-Bonsai-2-27B 6.6 GB): none fit the 6 GB card; CPU/offload lane, out of scope. One aside: the ternary
  PTQ1_0 Bonsai is the extreme-low-bit family the sherpa flagged as intolerant for SMALL models, but at 27B dense
  it sits in the tolerant class.

## GPU-LADDER TRIPWIRE

Radar-file check performed 2026-10-01: `grep -ril supercade memory/ corpus/ docs/` returned ZERO hits; the broader
radar/gpu-ladder sweep hit only incidental word matches, and `memory/rib/RIB_DRIVING_LADDER_20260928.md` is the
model-spend ladder, not hardware. **No existing GPU-ladder/supercade radar file exists; this dossier is row
zero.** If the operator wants it standing, promote this section to `memory/rib/RIB_GPU_LADDER.md` next window.

WHEN a card makes DeepGEMM worth adopting (the tripwire, 5 gates):

- **ARCH GATE.** DeepGEMM pays on Hopper SM90 (wgmma FP8) or Blackwell SM100 (tcgen05, NVFP4). Consumer
  Blackwell RTX 50-series (SM120) exposes FP8/FP4 tensor cores, but DeepGEMM SM120 support must be verified
  against the current release before money moves. Do NOT buy Ada (RTX 40xx, SM89) for this library: FP8 exists
  there via other kernels, wgmma/tcgen05 do not. Turing/Ampere: no FP8. Our RDNA1 gfx1010: nothing ports
  (sherpa row 2, confirmed against the estate stack).
- **VRAM GATE.** 24 GB minimum before the FP8 win matters here (7B FP8 is ~8 GB weights + KV, wasted headroom
  on a 12 GB card; the grouped-GEMM MoE win needs all experts resident: a 4x7B-A12B MoE at FP8 is ~32 GB
  class). 32 GB preferred.
- **PRICE TRIGGER.** A 24 GB+ Blackwell card at or under ~$1200, or a 32 GB RTX 5090-class card at or under
  ~$1700, or any Hopper/SM100 datacenter card falling into hobbyist reach (used H100 80 GB under ~$4000:
  unlikely, but that is what the radar is for).
- **SOFTWARE GATE.** CUDA 12.8+ with NVRTC reachable via cuda-python (DeepGEMM compiles at first call without
  nvcc; that IS its pattern) plus a serving stack that routes grouped GEMM (vLLM or SGLang). None of this
  installs on the current AMD box; the trigger includes moving the inference seat to a CUDA host.
- **WORKLOAD GATE (the real one).** The card only pays when (a) the MoE-export door gets built (merged/mated
  models as experts) or (b) FP8 7B+ serving throughput actually matters. Until one of those fires, IGNORE every
  DeepGEMM-class drop; the RX 5600 XT keeps Q4/Q5 GGUF duty.

## RUNTIME-COMPILATION STEAL

Direct grep first: `nvrtc` in mag/ tools/ server/ = **zero matches**. The estate has no GPU JIT to steal from
literally. But the pattern (compile at first call, disk-cache keyed by shape/hash, never pay install-time or
per-run compile again) has one real home and one micro home:

- **THE FIND (gold): the Godot parity twins re-compile on every suite run.**
  `tools/rule_parity.py:975 run_godot` and `tools/flock_parity.py:454 _run_godot` each spawn a fresh headless
  Godot 4.3 process (`tools/godot/Godot_v4.3-stable_win64.exe`, 132,918,392 bytes, dated Aug 15 2024) per suite
  invocation. Every invocation pays engine boot + project scan/import + GDScript parse and compile of the runner
  and the twins (`roblox_to_godot/systems/water_graph.gd`, `flock.gd`, `game_constants.gd`) from source, because
  Godot 4.3 keeps no cross-process compiled-GDScript disk cache for non-exported projects. These suites are the
  estate's own verification instruments, re-run per wave (rule_parity is the C3/Q02 differentiator proof), so
  the compile cost repeats on every verification. The DeepGEMM-shaped fix: precompile the parity runner + twins
  into an exported .pck (or .gdc) whenever the script hash changes, cache keyed by (script sha256, godot
  version), and invoke the cached artifact per suite. Half the cache key already exists: flock_parity's
  constants_hash guard (sha256 over game_constants.gd float32 bit lines) is exactly the (dtype, arch)-style key
  DeepGEMM uses. Honest sizing: this is seconds per suite invocation, not minutes; it is the pattern's best
  available home in the estate, a tidy-up, not a bottleneck fix.
- **Micro-instance:** `mag/context_compression.py:141` compiles 10 shrink-map regexes inside the loop on every
  compress call. Module-level precompile is the same law at micro scale (import-time compile = the cache). Two
  lines, zero drama.
- **Where the pattern does NOT apply (recorded honestly):** module-scope `re.compile` sites (embassy_deliver,
  grok_steer, 61 sites in dissector) already compile at import, already cached. The water fixed-point engine
  (`mag/hydrology.py`, `mag/water_graph.py`) is pure integer Python with no per-call compilation to cache.
  `mag/compiler_flywheel.py` is a VRAM-metaphor instrument with no real compilation inside.

## VERDICT

DO:
1. Two quant tickets, cheap disk pulls, no hardware: replace gemma:2b Q4_0 with a Q5_K_M/Q6_K 2B build, and
   re-pull deepseek-r1:1.5b at Q5_K_M. Both fit 6 GB VRAM.
2. Audit the gemma4 9.6 GB vs Q4_K_M arithmetic anomaly (blob/layer listing) before any re-pull decision.
3. Bank the GPU-ladder tripwire above as the memory-supercade radar row zero; promote to
   `memory/rib/RIB_GPU_LADDER.md` if the operator wants it standing.
4. Optional tidy-ups: .pck/.gdc precompile cache for the Godot parity twins (reuse the constants_hash as key
   material); module-level regex precompile in context_compression.

IGNORE:
- DeepGEMM itself on this box (RDNA1; nothing ports; sherpa row 2).
- FP8/FP4 anything on the RX 5600 XT.
- Any GPU purchase until the workload gate fires (MoE export built, or FP8 QPS real).
- The MoE-mating door stays with the staged premium adjudication ask, not this lane.

Receipt: this file, landed on the shared inbox; register event appended to index_events.jsonl.

## PULL OUTCOME 2026-10-01 (honest)

Ticket 1 ATTEMPTED-NOT-LANDED: `gemma2:2b-q5_K_M` is not a registry tag; fallback re-pulled the identical digest b50d6c999e59 (Q4_0, 1.7 GB). The quant correction needs either the correct registry tag or a Modelfile build from a Q5_K_M GGUF. Ticket stays OPEN. deepseek-r1:1.5b untouched. The regex fix and GPU-ladder rib DID land (mag/context_compression.py module-scope _SHRINK_PATTERNS, memory/rib/RIB_GPU_LADDER_20261001.md).

## PULL OUTCOME 2 (2026-10-01, research lane; ticket 1 LANDED at tag level)

**Probe-method gotcha (why outcome 1 failed blind):** `ollama show <tag>` on 0.34.3 CANNOT verify a
remote-only tag (returns "model not found" without pulling), and there is no dry-list CLI. The working
verification instrument is the registry manifest API: anonymous `GET
https://registry.ollama.ai/v2/library/gemma2/manifests/<tag>` with `Accept:
application/vnd.docker.distribution.manifest.v2+json` returns 200 + a tiny manifest (only `/tags/list`
needs an auth token). Tag enumeration without pulls: the `ollama.com/library/<model>/tags` HTML page.
The correct tag grammar is `<model>:2b-instruct-q5_K_M` (with the `-instruct-` infix); the failed
attempt had dropped it.

**Ticket 1 VERIFIED + PULLED (gemma-class 2B at Q5_K_M):**
- Registry manifest 200 BEFORE pulling: model layer `sha256:b21594fe35023c20333008b4284c00869ec3904d40be091b9d99f1d41f7bd165`,
  size 1,923,278,368 bytes (template/license/params layers shared across the family).
- Verified alternates (manifest 200, not pulled): `gemma2:2b-instruct-q6_K` layer `sha256:0ba7df09...`
  2,151,392,800 bytes (the next rung up if scut quality still lags); `gemma2:2b-instruct-q4_K_M` layer
  `sha256:1e4fc624...` 1,708,582,432 bytes (rollback rung).
- PULLED: `gemma2:2b-instruct-q5_K_M`, ID 44b731fe20db, 1.9 GB on disk. `ollama show` verbatim facts:
  architecture gemma2, parameters 2.6B, context length 8192, embedding length 2304, quantization
  Q5_K_M, Gemma Terms of Use. Smoke-tested: loads and answers a one-word prompt on this box.
- Old scut `gemma:2b` (Gemma 1, Q4_0, b50d6c999e59) NOT deleted. The config flip + old-blob delete is
  operator-GO-gated; flip points: configs/lanes.yaml:31-36 (clerk/router/orchestrator/voice) and :65
  (voice_model), configs/providers.yaml:113, models/registry.py:18-19. Confound to record at flip time:
  the swap changes lineage (Gemma 1 -> Gemma 2) AND quant (Q4_0 -> Q5_K_M) in one move; P1-style
  battery comparisons must name both.
- Lineage note closed: this build IS gemma-2-2b-it, the exact lineage the OBLITERATUS drop names for
  P2 abliteration and the PACK.md E-A/E-B experiments (memory/corpus/research_packs/abliteration_crossfamily/PACK.md).

**gemma3 QAT probe (ask's example string):** `gemma3:1b-qat` does NOT exist. The real tags are
`gemma3:1b-it-qat` and `gemma3:4b-it-qat` (both manifest-verified 200). Not pulled: 1b is sub-2B class
and gemma3 ships no Q5/Q6 tags (only qat / q4_K_M / q8_0 / fp16), so the library cannot serve the
sherpa 2B band on gemma3 at all.

**Ticket 2 (deepseek-r1:1.5b at Q5_K_M): registry-impossible as a tag.** Verified tag set for 1.5b is
exactly: `1.5b`, `1.5b-qwen-distill-q4_K_M`, `1.5b-qwen-distill-q8_0`, `1.5b-qwen-distill-fp16`
(plain `1.5b` maps to the q4_K_M digest e0979632db5a, matching our local copy). NO q5/q6 tag exists at
any size. The registry hf.co mirror path
`v2/hf.co/bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/manifests/Q5_K_M` returns 404. Verified at the
source level instead (HF API tree listing): `bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF` contains
`DeepSeek-R1-Distill-Qwen-1.5B-Q5_K_M.gguf` and `-Q6_K.gguf`. Operator-GO-gated recipe, no new file
staged since the gemma gate did not trigger: Modelfile with
`FROM https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-1.5B-Q5_K_M.gguf`
plus TEMPLATE/PARAM copied from `ollama show --modelfile deepseek-r1:1.5b` (est ~1.3 GB). Interim
library-only rung if wanted before that GO: `deepseek-r1:1.5b-qwen-distill-q8_0` (manifest-verified
200; q8_0 overshoots the band). Not pulled this lane (gemma was the ask). Same bartowski pattern holds
for gemma (`gemma-2-2b-it-GGUF` has Q5_K_M / Q6_K / Q6_K_L files, HF-verified) but is moot: the
library tag landed.
