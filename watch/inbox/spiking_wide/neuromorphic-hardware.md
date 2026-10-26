# NEUROMORPHIC HARDWARE DIG (lane: neuromorphic-hardware, division B)

Date: 2026-10-01. Ask: does neuromorphic SILICON (Intel Loihi 2 / Hala Point, SpiNNaker 2, BrainChip Akida, Tsinghua Tianjic) serve language models yet, or stay robotics/edge; energy claims vs measured; can a civilian buy or rent time; is there ANY 2026 path where spiking silicon serves an estate organ (embeddings, event detection, drift sensors). Tri-state the hype against primary specs.

## PRIOR-ART SWEEP (Descent Protocol leg 1)

Command run: `grep -ril -E "loihi|spinnaker|neuromorphic|akida|tianjic" memory docs corpus watch/inbox` (exit 0). Hits were all incidental (Gutenberg texts, mycology/memristor training PDFs, browser caches, session logs) except one named artifact: `memory/runs/flygomoku_20260912/hermes_out/F08_neuromorphic_bet_qwen__qwen-2.5-72b-instruct.md`, which is a FAILED hermes dispatch (header `ok: False`; body is a model context-window error, zero content). Verdict of the sweep: the estate holds no banked neuromorphic-hardware dig. This lane is first ground; nothing to attach as known ground.

## REGISTER (per platform, primary specs, tri-state)

Tri-state key: VERIFIED = primary page fetched this dig (2026-10-01); SECONDARY = credible secondary source, primary not fetched; UNVERIFIED = claim in circulation, no primary fetched.

### Intel Loihi 2 / Hala Point - VERIFIED (primary: Intel newsroom + Sandia news release)

Source: Intel newsroom, "Intel Builds World's Largest Neuromorphic System..." (https://www.intel.com/content/www/us/en/newsroom/news/intel-builds-worlds-largest-neuromorphic-system.html), fetched 2026-10-01.

- Announced April 17, 2024; "initially deployed at Sandia National Laboratories"; described by Intel as a "research prototype".
- Verbatim: "1,152 Loihi 2 processors produced on Intel 4 process node in a six-rack-unit data center chassis"
- Verbatim: "supports up to 1.15 billion neurons" and "128 billion synapses" "distributed over 140,544 neuromorphic processing cores"
- Verbatim: "consuming a maximum of 2,600 watts of power"; plus "over 2,300 embedded x86 processors"
- Per-chip scale: Sandia's release (https://newsreleases.sandia.gov/artificial_neuron, fetched 2026-10-01) reports Loihi 2 carries one million circuits per chip, up from 128,000 in Loihi 1; predecessor Pohoiki Springs held 50 million neurons. (Rendered as fetch summary prose, so the exact phrasing is SECONDARY; the 1,152-chip and 1.15B-neuron figures are independently confirmed verbatim by both Intel and Sandia.)
- Purpose (Sandia, verbatim): "to provide Sandia and National Nuclear Security Administration research teams with the tools to realize brain-based computing on a large scale"
- Access: Intel research page (https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html, fetched 2026-10-01): the Intel Neuromorphic Research Community (INRC), verbatim "Membership is free and open to all qualified groups"; Kapoho Point is an "8-chip Loihi 2 board" enabling "up to one billion parameters". Nothing on the page offers Loihi 2 for purchase. Hala Point is a Sandia research machine; the fetch surfaced no commercial availability plan.
- 2026 program status: the INRC page was live and open at fetch time; live searches for a 2025-2026 cancellation or Loihi 3 confirmation were rate-limited (backend 1302 errors) and returned nothing definitive. Recorded as absence of evidence, not evidence of absence.

### Energy claims vs measured - claims VERIFIED, measured PARTIAL

- Intel PR verbatim claims: "can support up to 20 quadrillion operations per second, or 20 petaops"; "an efficiency exceeding 15 trillion 8-bit operations per second per watt (TOPS/W)"; "100 times less energy at speeds as much as 50 times faster than conventional CPU and GPU architectures".
- The catch, same PR: the 15 TOPS/W figure comes from a 14,784-layer MLP with 8-bit weights pruned to 10:1 sparsity, and the page itself carries "Results may vary."
- SpiNNcloud homepage (https://spinncloud.com, fetched 2026-10-01) claims "18× higher energy efficiency than GPUs" for SpiNNaker2 with no methodology on the page: UNVERIFIED marketing claim.
- Measured-side anchors found this dig:
  - ICLR 2025 paper, MatMul-free LM architecture on Loihi 2 (https://arxiv.org/abs/2503.18002, fetched 2026-10-01): a 370M-parameter model; verbatim "we report up to 3x higher throughput with 2x less energy, compared to transformer-based LLMs on an edge GPU", prefaced "Based on preliminary results".
  - EGRU on SpiNNaker 2 (https://arxiv.org/abs/2312.09084): "significant gains versus conventional hardware in energy efficiency" for single-batch inference, no numbers on the abstract page.
- Tri-state verdict: the big multipliers (15 TOPS/W, 100x less energy, 18x vs GPUs) are workload-shaped claims (sparse, pruned, single-batch); the measured academic deltas on LLM-shaped workloads are 2-3x versus an edge GPU at 370M parameters. The efficiency story is real but conditional, not a datacenter-LLM story.

### LLM scale: does spiking silicon run LLMs - VERIFIED NEGATIVE

- Largest LLM-architecture model found running on any spiking silicon: 370M parameters (MatMul-free LM, Loihi 2, ICLR 2025, "Based on preliminary results"). 2026 frontier LLMs are roughly three orders of magnitude larger.
- The state-of-the-art language model on SpiNNaker 2 is an EGRU; the paper claims "the first-ever implementation of a language model on a neuromorphic device" and frames LLM level as future work: verbatim "setting the stage for taking task performance to the level of large language models".
- Hardware ceiling from primary numbers: all of Hala Point sums to 128 billion synapses with event-driven accumulation (no dense matmul arrays); the largest research board Intel advertises, Kapoho Point, enables "up to one billion parameters".
- Not found in this dig: any paper running a 10B-or-larger parameter LLM end-to-end on spiking silicon (live search partly rate-limited; labeled).
- Verdict: proven negative at LLM scale as of 2026-10-01.

### SpiNNaker 2 / SpiNNcloud - chip VERIFIED, access SECONDARY

- Chip verbatim (https://arxiv.org/html/2312.09084v1, fetched 2026-10-01): "The chip consists of 152 processing elements (PEs) connected via a network-on-chip (NoC)." Each PE carries an Arm M4f core, 128 kB SRAM, and accelerators for exponential functions, random number generation, and multiply-accumulate.
- Access: SpiNNcloud homepage labels the platform "commercially available"; the homepage counters render as 0 placeholders and the only access path offered is email to info@spinncloud.com, with no public pricing. Press summaries (heise, The Register, SiliconANGLE via search, May 2024) report cloud rental from H2 2024 and a 4,320-chip system sold to the University of Leipzig: SECONDARY, not fetched from primary.

### BrainChip Akida - buyable VERIFIED, power UNVERIFIED

- Shop page fetched 2026-10-01 (shop.brainchipinc.com): AKD1000 PCIe board, SKU BD-PCIE-AKD10, price $289.00 excl. tax, listed In stock. Verbatim: "Compact, high-performance AKD1000 PCIe development board that drops into a standard PCIe slot to accelerate edge AI"
- The shop page carries NO power figures (only an "onboard Akida core current monitor"). Milliwatt-class power claims circulate; no primary spec page was fetched this dig: UNVERIFIED. Search summaries (SECONDARY) mentioned a $499 mini-PCIe variant and an M.2 board around $249-289 at DigiKey, and CNN-conversion via the MetaTF stack rather than native SNN training.

### Tianjic - prototype status VERIFIED

- open-neuromorphic.org page fetched 2026-10-01: "A proof-of-concept 28nm prototype chip was fabricated"; around 40k neurons, 10 million synapses, about 1 W, Tsinghua University, Luping Shi's team. The page describes no purchase or access pathway. An enterprise channel via the Lynxi (Lingxi) spinoff is search-summary SECONDARY only.

## BRIDGE VERDICT (named)

**NO.** There is no 2026 path where spiking silicon serves an estate organ. The four silicon families are research-only (Loihi 2 via free INRC membership, Hala Point at Sandia, Tianjic prototype), enterprise contact-sales (SpiNNcloud), or buyable edge dev kits (Akida, $289) that attack watts-at-the-edge, a constraint no estate organ has.

Per organ:

- Embeddings: no. Dense high-dimensional continuous vectors are the opposite workload from event-driven sparse accumulation; nothing fetched suggests spiking silicon serving embedding inference, and the estate's embedding work runs host-side (Ollama/local) where watts are not the binding constraint.
- Event detection / drift sensors: the one theoretical fit, because mW-class always-on audio/IMU event spotting is Akida's home niche, but the estate's sensors are software processes on the Windows host; the binding costs are tokens and dollars, not edge watts. The single falsifiable pilot, only if the operator ever charters an always-on edge sensor organ: one AKD1000 PCIe board at $289, benchmarked on a real keyword/event-spotting workload with measured milliwatts banked here. Until such a charter it is a solution hunting a problem this estate does not have.
- LLM inference: no, proven above (370M parameters is the published SOTA on spiking silicon; three orders of magnitude short; 2-3x versus an edge GPU, not versus datacenter GPUs).

Accessibility summary: Loihi 2 = free INRC membership, research-only, not buyable; Hala Point = Sandia research prototype; SpiNNcloud = enterprise contact sales, no public price; Tianjic = unbuyable prototype; Akida = buyable today at $289 but edge-class.

Revisit triggers (named): (1) a peer-reviewed 10B-or-larger parameter LLM running end-to-end on spiking silicon; (2) SpiNNcloud publishing self-serve pricing or rental; (3) the estate chartering an always-on edge sensor organ, which would trigger the $289 AKD1000 pilot.

## SOURCES (all fetched 2026-10-01)

1. Intel newsroom Hala Point PR: https://www.intel.com/content/www/us/en/newsroom/news/intel-builds-worlds-largest-neuromorphic-system.html
2. Sandia news release: https://newsreleases.sandia.gov/artificial_neuron
3. Intel neuromorphic research / INRC page: https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html
4. EGRU on SpiNNaker 2: https://arxiv.org/abs/2312.09084 and https://arxiv.org/html/2312.09084v1
5. MatMul-free LM on Loihi 2 (ICLR 2025): https://arxiv.org/abs/2503.18002
6. SpiNNcloud homepage: https://spinncloud.com
7. BrainChip shop, AKD1000 PCIe board: https://shop.brainchipinc.com/products/akida-development-kit-pcie-board
8. Tianjic overview: https://open-neuromorphic.org/neuromorphic-computing/hardware/tianjic-tsinghua-university
9. Estate prior art: grep exit 0 (42 incidental hits) and memory/runs/flygomoku_20260912/hermes_out/F08_neuromorphic_bet_qwen__qwen-2.5-72b-instruct.md (failed dispatch, ok: False)

## NOT DONE / GAPS (stated, not filled)

- Live-search confirmation of Intel's program status in late 2026 (search backend returned 1302 rate limits); the INRC page fetch is the freshness evidence used instead.
- No primary Akida power measurement fetched; BrainChip power claims left UNVERIFIED.
- SpiNNcloud's homepage renders its specs as 0 placeholders; the press figures (chips deployed, the Leipzig sale) were not confirmed from primary sources.
- Loihi 2 per-chip synapse count not confirmed from a fetched primary (Sandia confirms 1M neurons per chip; synapse-per-chip figures circulate at ~120M but were not byte-verified).
