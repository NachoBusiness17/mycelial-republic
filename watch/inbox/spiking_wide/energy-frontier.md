# ENERGY FRONTIER: energy per token across architecture classes (gala spiking-wide, energy lane)

Class: RECEIPT · Writer: energy-frontier lane (division B) · Date: 2026-10-01
Start point: the tweet's "97% less energy" on SpikingBrain, tri-stated tweet-grade in
`watch/inbox/SPIKINGBRAIN_DROP_20261001.md`. This lane dug the primary numbers.

## 1. The headline tri-state, closed with primary bytes

The tweet's 97% traces to arXiv:2509.05276 (SpikingBrain, CAS BICLab) and it is an
ANALYTIC PER-OPERATION ESTIMATE, not a measurement. Paper's own words (HTML v3,
fetched this session):

- "Conventional FP16 MAC: Each operation consumes 1.5 pJ"
- "INT8 MAC: Each operation consumes 0.23 pJ"
- "the average MAC energy cost is about 0.034 pJ (1.13 × 0.03 pJ)" (avg 1.13 spikes/channel)
- "Our scheme reduces energy consumption by 97.7% compared with FP16 MACs and by
  85.2% compared with INT8 MACs, yielding energy-efficiency improvements of up to
  43.48× and 6.76×"

There is NO joules-per-token or watt figure anywhere in the paper. The estimate is
based on "published hardware energy consumption data at 45nm technology" and
requires "specialized asynchronous hardware architectures (e.g., neuromorphic
chips)" that do not exist for this workload. What IS measured in the paper is
speed: 26.5x TTFT speedup at 1M tokens and >100x at 4M (fitted extrapolation,
Qwen2.5 couldn't run 4M), 5.36x throughput at 128k, all on MetaX C550 GPUs; and
CPU speedups of 4.04x/7.52x/15.39x at 64k/128k/256k vs Llama3.2-1B on an Intel
Core i5-12600KF with llama.cpp Q4_0. VERDICT ON THE TWEET: the 97% is a per-MAC
multiplication at 45nm literature values, contingent on hypothetical hardware.
Keep it as a direction, not a number.

## 2. The comparison table (primary numbers, hardware named)

Units: J/token measured on GPU power; kWh per million tokens derived
(1 J/token = 0.2778 kWh/Mtok). "Measured" = power metered while serving;
"estimate" = labeled as such.

| Class | Model | Hardware | Energy/token | kWh / Mtok | Grade | Source |
|---|---|---|---|---|---|---|
| Dense Transformer | LLaMA 65B | 8-32x V100/A100 (250-300W caps) | 3-4 J/token (measured, 512-tok gen) | ~0.83-1.11 | measured | arXiv:2310.03003 |
| Dense Transformer | Qwen3 32B | 1x B200, batch 128-512 | 0.151-0.312 J/token (Zeus metering) | 0.042-0.087 | measured | arXiv:2601.22076 |
| MoE (sparse) | Qwen3 30B-A3B | B200 | 3.56x LOWER J/token than 32B dense, same total params | ~0.012 (derived) | measured ratio | arXiv:2601.22076 |
| MoE (sparse) | Mixtral-8x7B | H100 cluster | ~ dense 8B J/token at ~56B-class quality | ~ dense-8B row | measured | arXiv:2512.03024 |
| Dense scale law | Llama-3 1B -> 70B | 4x H100 | 7.3x J/token growth for 70x params | (ratio) | measured | arXiv:2512.03024 |
| Linear attention (hybrid-linear) | SpikingBrain-7B | MetaX C550 GPU; i5-12600KF CPU | NO joules published; 26.5x TTFT @1M tok; 5.36x tput @128k; 4-15x CPU speedups vs Llama3.2-1B | n/a | speed measured, energy NOT | arXiv:2509.05276 |
| Spiking (event-based) | SpikingBrain spike scheme | 45nm literature values, neuromorphic chips (hypothetical) | -97.7% vs FP16 MAC, -85.2% vs INT8 MAC, PER OPERATION ONLY | not convertible | analytic estimate | arXiv:2509.05276 |
| Linear attention (plain SSM) | Mamba | A100-class | 5x throughput reported; no joules-per-token in literature | n/a | throughput only | arXiv:2312.00752 |
| Per-query standard (mixed small models) | 88 models, text generation | CodeCarbon GPU metering | ~0.047 kWh per 1,000 queries (gen) vs ~0.002 classification (30x spread) | ~0.16 at ~300 tok/query (derived) | measured | arXiv:2311.16863 |
| Quantization FP16->FP8 | Llama-3 405B | 16x H100 | ~30% J/token cut; 45 kJ -> 32 kJ per heavy batch | (ratio) | measured | arXiv:2512.03024 |
| Quantization FP8 caveat | Qwen3 235B-A22B | 8x H100 | up to +56% MORE energy at batch 8-16; -11% median at batch 65-256 | (ratio) | measured | arXiv:2601.22076 |
| Serving knob: frequency | Llama-2 70B | DGX-H100 | 2GHz->1.6GHz: same throughput at <80% energy; ~20% power cut, no latency hit | (ratio) | measured | arXiv:2403.20306 |
| Serving knob: power cap | LLaMA 65B | 4x A100 | 250W->175W cap: -23.2% energy, +6.7% time | (ratio) | measured | arXiv:2310.03003 |
| Serving knob: batch | Qwen3 32B, DeepSeek R1 | B200 | 3-5x J/token reduction unlocking batch | (ratio) | measured | arXiv:2601.22076 |
| Context length tax | Llama-3 70B | H100 | 2K->10K context: ~3x J/token | (ratio) | measured | arXiv:2512.03024 |
| OUR STACK: janitor | gemma:2b (Q4, ollama/llama.cpp) | Ryzen 7 3800XT CPU only, MSI MS-7C91, no dGPU | 84.65 tok/s measured; 0.3-1.7 J/token ESTIMATE (package 25-142W bound); ~0.08-0.47 kWh/Mtok | 0.08-0.47 | rate measured, watts ESTIMATE | run this session, receipt below |
| OUR STACK: second point | deepseek-r1:1.5b (Q4) | same box | 118.91 tok/s measured (output includes <think> tokens) | same bound class | rate measured | run this session |

Excluded as snippet-grade: MIT Tech Review's "~17,800 J/query" DeepSeek figure
(search snippet only, primary not fetched). One KTH thesis snippet (DeepSeek 1.5B
7-15 J/query on CPU) also left out: snippet-grade, hardware not verified.

## 3. Our own stack: what was measured and what the metering recipe is

Measured this session on the estate box (commands run, output quoted):

```
ollama run gemma:2b --verbose "Write a detailed explanation of the water cycle..."
  prompt eval rate:     366.67 tokens/s
  eval count:           369 token(s)
  eval rate:            84.65 tokens/s
ollama run deepseek-r1:1.5b --verbose "<same prompt>"
  eval count:           1110 token(s)
  eval rate:            118.91 tokens/s
```

Box: AMD Ryzen 7 3800XT (8C/16T, 105W-TDP class), no dGPU (`nvidia-smi` absent),
no battery (desktop). Hardware recon: no LibreHardwareMonitor / OpenHardwareMonitor
installed.

Honest negative: W metering via the OS is NOT possible on this box as it stands.
Windows exposes no CPU power counter on AMD desktop parts without a kernel driver
(RAPL is Intel; Zen2 package energy lives in MSR 0xC001_029B, readable only through
a driver like WinRing0). `typeperf` gives utilization %, never joules.

The recipe (three rungs, in order of truth):

1. GOLD (whole-box truth): an external watt meter or energy-monitoring smart plug
   at the wall. Log idle baseline P0 for 60s, run a fixed-prompt ollama benchmark,
   integrate (P - P0) over the eval window, divide joules by `eval count`. Includes
   PSU loss, RAM, fans: the number the electric bill sees.
2. OS-ADJACENT (package truth): install LibreHardwareMonitor (its WinRing0 driver
   reads Zen2 package energy counters); log package W at 1 Hz during the benchmark;
   J/token = package joules / `eval count`. This is the number papers like Samsi
   report (GPU package power; here CPU package power).
3. BOUNDED ESTIMATE (what this receipt ships, labeled): J/token = P/tok_rate with
   P bounded by idle-ish 25W and package PPT 142W. gemma:2b at 84.65 tok/s:
   0.30-1.68 J/token, ~0.08-0.47 kWh per million tokens. Realistic center near
   60W memory-bound: ~0.7 J/token (~0.19 kWh/Mtok). NOT a measurement; replace
   with rung 1 or 2 before spending on it.

## 4. The verdict: architecture change or quantization at OUR scale?

At estate scale (1-8B models on CPU/desk hardware, short-to-medium context, janitor
workloads), the measured literature says energy per token is dominated by
MEMORY TRAFFIC and SERVING CONFIGURATION, not by attention math:

1. QUANTIZATION MOVES ENERGY, MEASURED: FP16->FP8 cuts ~30% J/token at production
   batch (arXiv:2512.03024), and at our scale the Q4 GGUF files (1.7GB gemma:2b)
   mean ~4x fewer bytes moved per token than FP16, which on a bandwidth-bound CPU
   decode is roughly the energy lever. Caveat learned from B200 data: FP8 at LOW
   batch can COST energy (+56%); quantization pays when bytes dominate, which they
   do on our CPU stack.
2. SERVING KNOBS ARE FREE ENERGY: frequency 2->1.6GHz = same throughput at <80%
   energy (arXiv:2403.20306); power capping -23.2% energy for +6.7% time
   (arXiv:2310.03003); batching 3-5x J/token (arXiv:2601.22076). Our single-user
   decode cannot batch, so our lever is power capping + the Q4 files + model SIZE
   (1B->70B is only 7.3x energy: small models are the whole game, arXiv:2512.03024).
3. ARCHITECTURE CHANGE PAYS THROUGH ONE DOOR ONLY: linear attention does not show
   up as joules at short context (Mamba publishes 5x throughput, no joules;
   SpikingBrain publishes speedups, no joules). It pays where the quadratic term
   was the cost: LONG context. SpikingBrain's 26.5x TTFT at 1M tokens is real and
   is exactly the property the estate wants for reading the whole residual store
   (drop receipt estate-map item 1). Its energy claims, by contrast, are per-MAC
   estimates for neuromorphic chips that do not exist.
4. THE HONEST LITERATURE GAP: almost no architecture-class paper reports
   joules/token on identical hardware; MoE is the one class with a clean measured
   cross (3.56x lower J/token than a same-total-param dense model, arXiv:2601.22076)
   and even there the rule is "ACTIVE parameters drive energy, total parameters
   drive memory". Spiking's headline number lives at the operation level; linear's
   lives at the throughput level; only dense/MoE/quant/serving have joules.

VERDICT, one line: at our scale, quantization (bytes) + serving knobs (power cap,
frequency) move measured energy by 1.3-5x TODAY, while architecture change moves
our energy only via the long-context door later; the 97% tweet number is a 45nm
per-operation estimate, not a machine measurement, and must not be used to justify
an energy bet on spiking.

## 5. Decision ledger

Closes the gala spiking-wide decision "does the SpikingBrain energy claim justify
an architecture bet for energy at estate scale": NO on energy (per-MAC estimate,
hardware hypothetical), YES only on long-context speed (measured 26.5x TTFT @1M);
the near-term energy lever is Q4 quantization + power capping on the janitor rung,
with rung-1/rung-2 metering (above) as the falsifiable follow-up.

Falsifier: a metered rung-1/rung-2 measurement showing our janitor's package
energy per token above ~1 J at Q4 with power capping enabled, or a published
joules/token measurement of a spiking model beating a same-size dense model on
the SAME silicon, would kill this verdict.

## 6. Sources (all fetched or run this session)

- arXiv:2509.05276 (SpikingBrain tech report, HTML v3): energy estimates + speed tables
- arXiv:2310.03003 (From Words to Watts, Samsi et al., HTML v1): 3-4 J/token, power caps
- arXiv:2601.22076 (ML.energy Leaderboard v3, HTML v2): Zeus-measured B200/H100 dense vs MoE
- arXiv:2512.03024 (TokenPowerBench, HTML v1): H100 scaling, MoE, FP8, context tax
- arXiv:2403.20306 (Towards Greener LLMs, HTML v1): frequency scaling on H100
- arXiv:2311.16863 (Power Hungry Processing, Luccioni et al.): kWh per 1,000 queries
- arXiv:2410.12032 (MLPerf Power): the measurement standard (wall-measured, mW-to-MW)
- arXiv:2312.00752 (Mamba): 5x throughput, no joules
- watch/inbox/SPIKINGBRAIN_DROP_20261001.md: the drop receipt, tri-state source
- This box: ollama benchmarks quoted in section 3; CPU/box recon via PowerShell CIM
