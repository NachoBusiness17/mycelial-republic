# NONNVIDIA-STACKS: the non-NVIDIA compute layer, 2026-10-01

Class: RECEIPT · Writer: gala-nonnvidia-stacks (division B, spiking-wide) ·
Register: `watch/inbox/spiking_wide/nonnvidia_stacks_signals.jsonl` (8 rows, one per
stack/context) · Evidence raw captures:
`watch/inbox/gala_20260925/spiking-wide/lanes/ev_unsloth_amd.md`,
`ev_tpu_pricing.md`, `ev_arxiv_2509_05276_abstract.md`, `ev_search_summaries.md`

## What was owed

The non-NVIDIA compute dig: state of training AND inference on non-NVIDIA silicon in
2026. ROCm's real state for 7B-14B training (our ~6GB AMD box is inference-only; what
CAN it run), Ascend/MindSpore maturity, Cambricon post-SpikingBrain, TPU, and the
estate question: cheapest non-NVIDIA path to fine-tune a 7B locally, and does the
export-control bound actually bind at OUR scale or only at frontier scale. Started
from the SpikingBrain drop (`watch/inbox/SPIKINGBRAIN_DROP_20261001.md`, which proved
7B-class training on MetaX/Cambricon-class domestic clusters).

## Prior-art sweep (Descent Protocol leg 1)

The estate already held five pieces; this lane builds on them and does not re-derive:
- `watch/inbox/SPIKINGBRAIN_DROP_20261001.md`: the seed receipt, tri-stated
  (100x is TTFT at 4M tokens, not general speed; 97%-energy is tweet-grade).
- `watch/inbox/ball4/compute.md:15-19,47`: compute economics: used-24GB 3090 ladder
  ~$1,100-1,300 (quote dated 2026-09-01, reads optimistic under the HBM memory
  supercycle); QLoRA-13B-on-one-3090 named the load-bearing local rung; HBM sold out
  through CY2026.
- `watch/inbox/ball4/capital-policy.md:43-60`: the MODEL-level export-control channel
  (ECRA, June 2026 Is-Informed Letter precedent: open-weight release is an
  unambiguous export under that theory; AI Exports Program deadline passed silently).
- `docs/ref/HOME_HARDWARE_ENVELOPE.md:4,13`: the box: DESKTOP, 64GB RAM, AMD RX 5600
  XT ~6GB VRAM, no CUDA; 6GB VRAM = one resident model. (Note: the ask said 4GB; the
  estate law file says ~6GB. Conclusion below is unchanged under either number.)
- `watch/inbox/48h_synth/steals.md:292`: prior steal: verify one estate GGUF loads
  under a Vulkan or ROCm llama.cpp backend.
- Sibling lane `gala_20260925/spiking-wide/lanes/spikingbrain-deep.json` owns the
  paper deep-dig; this lane owns the broad stack map. No overlap.

NO prior sovereignty-compute table exists anywhere in the estate (grep receipt in
`nonnvidia-stacks.check.txt` CHECK 1: zero hits for sanctions-proof /
sovereignty-compute / sovereign compute table across watch/inbox, docs, memory,
state). The table below is therefore CREATED here, fulfilling "updated" as
"now exists and is current as of 2026-10-01".

## THE SOVEREIGNTY-COMPUTE TABLE (what a sanctions-proof local stack looks like in 2026)

| Rung | Hardware | Capital | Train or infer | Stack | Primary evidence |
|---|---|---|---|---|---|
| R0: own box, $0 | RX 5600 XT ~6GB RDNA1 gfx1010 (already owned) | $0 sunk | 7B-class Q4 GGUF INFERENCE only (llama.cpp Vulkan or ollama-rdna1 fork); NO training, ever, on this silicon | llama.cpp Vulkan / ollama-rdna1 | Unsloth matrix: "RDNA 1 supports only Vulkan inference, not full training." (ev_unsloth_amd.md); ROCm dropped RDNA1, RCCL/P2P absent (ev_search_summaries.md SEARCH 4); envelope law docs/ref/HOME_HARDWARE_ENVELOPE.md:13 |
| R1: cheapest NEW owned fine-tune card | RX 7900 XTX 24GB RDNA3 | ~$900-1,000 new (STALE/GRADE-C: fresh price query 429-failed, see Date honesty) | 7B-14B QLoRA TRAINING, vendor-supported, Windows or Linux | Unsloth 0.7+ on ROCm | Unsloth matrix Full support RDNA3 + "4-bit training: bitsandbytes-based QLoRA support" (ev_unsloth_amd.md); 10-20% penalty vs 4090 (ev_search_summaries.md SEARCH 7) |
| R1-alt: cheapest USED fine-tune card | RTX 3090 24GB (NVIDIA, listed because it is the incumbent rung the non-NVIDIA rungs must beat) | ~$1,100-1,300 used (estate quote 2026-09-01, supercycle inflating) | 7B-14B QLoRA, CUDA mature | CUDA + Unsloth | watch/inbox/ball4/compute.md:15,47 |
| R2: cheapest RENTED fine-tune (no capital) | Google TPU v5e (non-NVIDIA silicon) | $0.60-1.20/chip-hour; 7B QLoRA run = single-digit dollars | TRAINING (full fine-tune feasible; LoRA trivial) | JAX / HF on TPU | Google price page fetched live: v5e us-central1 $1.20 on-demand, $0.60 Flex-start (ev_tpu_pricing.md) |
| R2-alt | MI300X-class rentals, 192GB | search-grade, not quoted | TRAINING | ROCm Linux-only for collectives | Unsloth matrix CDNA rows (ev_unsloth_amd.md) |
| R3: the China path (proven, not purchasable here) | Ascend 910C / Cambricon MLU / MetaX C550 | n/a US-side | FRONTIER POST-TRAINING claimed (1.6T on ~1,000 910C); 7B upcycle-training PROVEN on hundreds of MetaX GPUs, weeks stable | CANN/MindSpore, Torch-MLU, MetaX stack | ev_search_summaries.md SEARCH 2/3/5; ev_arxiv_2509_05276_abstract.md |
| Bound layer | export-control law | binds CHINA-ACCESS and FRONTIER VOLUME (ECCN 3A090.a, AI Diffusion rescinded, consumer carve-outs live); does NOT bind a one-box US estate. The live model-level channel (Is-Informed precedent) threatens WEIGHT DISTRIBUTION, not local fine-tune for own use | | | ev_search_summaries.md SEARCH 8; watch/inbox/ball4/capital-policy.md:43-60 |

Reading of the table: a sanctions-proof LOCAL stack in 2026 is not one chip, it is
this ladder: inference you already own (R0, $0), fine-tuning rented by the chip-hour
off NVIDIA silicon (R2, dollars per run), fine-tuning owned on a single 24GB card
(R1, ~$1k, AMD now vendor-supported end to end), and a proven-at-scale non-Western
training layer (R3) that exists as feasibility evidence even though none of it is
buyable at a US retail counter.

## The estate question, answered

1. **Cheapest non-NVIDIA path to fine-tune a 7B locally:** two answers, by cost
   shape. Zero-capital: TPU v5e Flex-start at $0.60/chip-hour (Google's own price
   page, fetched live) puts a one-off 7B QLoRA run in the same single-digit-dollar
   band the descent protocol already pays for premium turns; zero VRAM purchase, and
   it sidesteps the memory supercycle entirely. Owned-hardware: the RX 7900 XTX 24GB
   is the first rung where the ENTIRE train stack (Unsloth, QLoRA via bitsandbytes,
   ROCm) is vendor-supported on non-NVIDIA silicon on a consumer OS; the used-3090
   rung it replaces is rising under the HBM supercycle per the ball4 receipt. The
   estate's own box cannot train a 7B under any non-NVIDIA stack: RDNA1 is
   inference-only at the vendor-matrix level, and 6GB is below the 8GB floor even
   Unsloth claims for small-model training.
2. **Does the export-control bound bind at OUR scale?** No. It binds at two places,
   neither of which is a one-box US estate: (a) China's ACCESS to frontier silicon
   (ECCN 3A090.a country licensing; the reason Ascend/Cambricon/MetaX exist and the
   reason SpikingBrain's MetaX result is strategically load-bearing), and (b)
   frontier volume/interconnect class. The 2026 loosening is real: the AI Diffusion
   Rule's worldwide tiering was rescinded (BIS May 31 2026 guidance; Jan 15 2026
   final rule) while country licensing and consumer carve-outs stand. The bound that
   could someday touch this estate is the MODEL-level licensing channel
   (capital-policy.md's Is-Informed precedent: open-weight distribution as export),
   which is a threat to weight AVAILABILITY, not to our local compute; and
   fine-tuning for own use is not a distribution act. Verdict: the bound binds at
   frontier scale and at China's border, not at ours; our binding constraint is VRAM
   economics, not law.
3. **What CAN our box run (the 4GB/6GB question):** 7B-class Q4 GGUF inference via
   the Vulkan backend (or ollama-rdna1) at small context per the envelope's
   one-resident-model law; gemma:2b / qwen-desk remain the fitted residents. 14B Q4
   does NOT fit in ~6GB with usable context. Training: none, on any non-NVIDIA
   stack, on RDNA1.

## What landed

- Register: 8 rows in `watch/inbox/spiking_wide/nonnvidia_stacks_signals.jsonl`
  (amd-rocm-consumer, amd-cdna-datacenter, huawei-ascend-mindspore, cambricon,
  metax, google-tpu, export-control-bound, estate-local-ladder-rdna1), each with
  primary maturity evidence + quote + raw-capture pointer + tri-state + falsifier.
- This receipt + the sovereignty-compute table (created; none existed before,
  CHECK 1).
- 4 raw evidence captures in the lanes dir (3 live fetches byte-captured: Unsloth
  AMD matrix, Google TPU pricing, arXiv 2509.05276 abstract; 1 search-summary file
  with every 429 recorded).
- Lane JSON: `watch/inbox/gala_20260925/spiking-wide/lanes/nonnvidia-stacks.json`.

## Date honesty

- Live-fetched 2026-10-01: Unsloth AMD support matrix, Google Cloud TPU pricing,
  arXiv 2509.05276 abstract (quotes byte-captured in evidence files).
- Search-grade (2026-10-01): Ascend 910C DeepSeek post-training claim, TrendForce
  4Q26 supply, Cambricon PyTorch Foundation + 500k-chip target, RDNA1 ROCm dropout
  details, ECCN 3A090 status. None byte-fetched; tri-stated in the register.
- The Ironwood pricing conflict across secondary sources ($6 vs $12) was resolved by
  the primary page: $12.00 on-demand us-central1, $6.00 is the Flex-start rate.
- FAILED retrieval, stated plainly: fresh used-3090 / 7900 XTX street prices. The
  search tool 429'd to death on that query (recorded in ev_search_summaries.md
  SEARCH 9). The ~$900-1,000 7900 XTX figure in the table is GRADE-C stale general
  price knowledge, labeled as such; the 3090 number is the estate's own 2026-09-01
  quote. Do not spend against either without a re-quote.
- The ask's "4GB AMD box" vs the estate law file's "~6GB" (RX 5600 XT,
  docs/ref/HOME_HARDWARE_ENVELOPE.md:4): recorded, conclusion unchanged.

## Checks

- CHECK 1 no-prior-table grep, CHECK 2 register JSONL parse+count, CHECK 3 receipt
  bytes, CHECK 4 evidence-file quote substrings, CHECK 5 em-dash scan, CHECK 6 live
  ollama/GPU probe of the actual box, CHECK 7 lane JSON parse: all in
  `watch/inbox/gala_20260925/spiking-wide/lanes/nonnvidia-stacks.check.txt`.
- Ratchet: no code under `mag/` or `tools/` touched by this lane (receipt + register
  + evidence files only); `tools/violation_ratchet.py check --changed` not
  applicable, not run.

Read-only intelligence per the sensed-never-done law: findings banked, no hardware
bought, no stack installed from this lane.
