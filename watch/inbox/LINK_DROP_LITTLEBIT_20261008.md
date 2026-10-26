# LINK DROP: LittleBit sub-1-bit quantization (operator X link, 2026-10-08)

Drop: operator pasted https://x.com/thesupermannx/status/2108098865073410484
(Samsung open-sourced a method shrinking a 13B LLM to under 1GB, "LittleBit",
latent factorization, sub-1-bit, XOR-based inference).

## Primary source verified (arXiv API this sitting, not from the tweet)

- **LittleBit: Ultra Low-Bit Quantization via Latent Factorization**, arXiv
  2506.13771v5, Banseok Lee, Dongkyu Kim, Youngcheon You, Youngmin Kim
  (Samsung Research), accepted NeurIPS 2025. Claims carried from the abstract:
  targets ~0.1 bits per weight, ~31x memory reduction, Llama2-13B under 0.9 GB,
  at 0.1 BPW beats leading methods running at 0.7 BPW on Llama2-7B, and a
  "potential" 11.6x inference speedup vs FP16. Code: github.com/SamsungLabs/LittleBit.
- **LittleBit-2** (follow-up), arXiv 2603.00042v2: names the failure mode of
  v1-class methods ("Latent Geometry Misalignment": standard singular vectors
  too coherent for binarization), cures with Internal Latent Rotation +
  Joint-ITQ at zero inference overhead, and reaches sub-1-bit SOTA MATCHING
  leading 1-bit baselines on Llama-2/Llama-3.

## The fine print (the tweet's three impressions vs the paper's words)

1. "0.1 bits per weight" is an amortized memory figure over a low-rank latent
   factorization + binarized factors + learned multi-scale importance params
   (Dual-SVID for QAT initialization, residual compensation). It is a TRAINING
   pipeline, not a weight dtype: you cannot re-quantize an existing GGUF into
   LittleBit with a converter pass.
2. The 11.6x speedup is kernel-potential vs FP16, not shipped software. No
   llama.cpp / GGUF / Ollama backend runs LittleBit today; the XOR/popcount
   kernels are the same family XNOR-Net promised in 2016 and are the whole
   ballgame for the estate.
3. Quality: v1 beats other SUB-1-BIT methods; v2's own abstract concedes
   sub-1-bit only now MATCHES 1-bit baselines. It is not FP16 parity and the
   paper does not claim it.

## Estate overlap (priors it lands on, all on disk)

- Quant A/B instrument already amended and waiting:
  watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md (the four-pinned-choices
  rule; the owed probe 5 qwen2.5:7b Q4_K_M vs q8_0 stays UN-RUN).
- Day-7 steal card: watch/inbox/frontier_olm_2026-10-07/steal/quantization-compression.md
  (round-2 byte-verified; the compression axis is already a named steal lane).
- Mesh expansion roster (tablet, smashed-screen phone, ~6 Rokus): this paper's
  own framing is "memory-constrained devices", and the estate's appliance fleet
  is the exact deployment target class.
- The 10-07 falsifier law applies unchanged: if a runnable LittleBit artifact
  ever lands, the pre-registered test is the four-pinned-choices A/B on
  matched-task deltas, fired once, signature banked before the run.

## Disposition

CARD ONLY, $0. No run fired, no model pulled, no repo cloned. Watch-item: a
LittleBit GGUF/Ollama kernel PR (llama.cpp) or a Samsung release with runnable
checkpoints flips this from watch to pull. Until then the estate's quant debt
is still the boring one: probe 5, un-run.
