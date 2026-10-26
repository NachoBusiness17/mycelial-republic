# LINK DROP: Wafer AI performance engineering repo, part 10 CUDA (operator X link, 2026-10-08)

Drop: operator pasted https://x.com/wafer_ai/status/2108025691535229086

## FABRICATION CAUGHT (receipt first)

The web-search tool's first summary of this tweet returned a detailed
narrative: "Cerebras announced Waffle-2-Expanse tonight... a 671B model now
runs 16x cheaper... $0.08/M input, $0.40/M output." Follow-up search found NO
evidence "Waffle-2-Expanse" exists at all, and the primary fetch of the
tweet shows an entirely different post. The price-list story was the search
summarizer inventing a plausible tweet body. Struck in full. The estate law
held: the primary fetch outranks the summary, every time.

## What the tweet actually is (fetched verbatim this sitting)

@wafer_ai (the AI performance company), 2026-10-08T02:44Z: they launched
"the most comprehensive ai performance engineering repo in the world" and
are posting it as a series; this is part 10, a reading of NVIDIA's CUDA
Programming Guide for LLM performance work. Six mechanics named, each tied
to an LLM-serving symptom:

1. Kernel tuning (SIMT, CUDA Tile chapters; why bigger tiles or more fusion
   cause register spills).
2. Overlapping data movement with compute (async copies, TMA,
   producer/consumer pipelines).
3. Growing KV caches via virtual memory: reserve an address range, map
   physical pages in as the cache grows, no relocation (the PagedAttention
   idea living in the driver).
4. Cutting inter-kernel overhead: CUDA Graphs, stream-ordered allocation.
5. Cross-GPU stall diagnosis: peer access, NCCL completion fences blocking
   unrelated compute, memory synchronization domains.
6. CPU memory offload economics: residency, migration, interconnect cost.
   Plus validation before deploy: reduction order, accumulation precision,
   fast math.

The repo itself is linked in the thread and was NOT fetched this sitting;
only the tweet bytes are verified.

## Estate placement (small, honest)

- Reference row for the performance axis, ARMORY-class index material. The
  estate's fleet largely runs llama.cpp/Ollama on Vulkan and AVX2 backends
  (the eight reaped servers this morning were vulkan-avx2 builds), so CUDA
  chapters apply at the next hardware rung (the 3090-rung class) or if
  llama.cpp gets built CUDA-first on-box.
- Two chapters touch work the estate has already done by hand: the KV-cache
  virtual-memory model (our q8_0 KV sweep measured decode doubling,
  build-wave 9/9) and CPU offload economics (the burners-cage CPU-relief
  lanes). When kernel-level tuning day comes, this series is the map.
- Pull trigger: none now, $0. If a CUDA tuning pass ever opens (3090 rung),
  walk the repo's parts before touching flags.

## Disposition

CARD ONLY. Also banked as a live demonstration of the no-fabrication law:
the search layer fabricated an announcement; the primary fetch struck it.
