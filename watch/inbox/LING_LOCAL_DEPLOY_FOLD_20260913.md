# LING LOCAL DEPLOYMENT — 20-WIDE FOLD (2026-09-13)

**The order:** the Ollama pull failed (no community build exists). Necessity is the mother. Build the road ourselves. 20-wide on how to run Ling-3.0 locally.

**Result: 20/20 clean. Every lane converged on the same pipeline.**

## THE UNIVERSAL PATH (all 20 lanes agree)

```
1. huggingface-cli download inclusionAI/Ling-3.0-tiny --local-dir ./ling-tiny
2. Convert to GGUF: python llama.cpp/convert_hf_to_gguf.py ./ling-tiny
3. Quantize: llama-quantize ling-tiny.gguf ling-tiny-Q4.gguf Q4_K_M
4. Serve: llama-server -m ling-tiny-Q4.gguf --port 8080
5. Or: ollama create ling-tiny -f Modelfile
```

**Start with tiny (7.9B/1.3B). It fits 8GB RAM. Prove the pipeline. Then scale to flash.**

## The critical finding (L15 — RAM math for MoE)

**MoE inference requires ALL expert weights in RAM, not just the active ones.** The routing network picks which experts fire per token, but ALL experts must be loaded because you can't predict which ones the next token needs. This means:

- Ling-3.0-flash (124B): needs ALL 124B weights in RAM even though only 5.1B computes. At Q4 quant that's ~65GB. **Won't fit on 32GB. Tight on 64GB.**
- Ling-3.0-tiny (7.9B): needs ~8GB at Q8, ~4GB at Q4. **Runs on anything.**

## The quantization ladder (L09)

| Level | RAM (flash) | RAM (tiny) | Quality loss |
|---|---|---|---|
| Q8 | ~130GB | ~8.5GB | ~0% |
| Q6 | ~100GB | ~6.5GB | negligible |
| Q5 | ~80GB | ~5GB | slight |
| Q4_K_M | ~65GB | ~4GB | noticeable on code |
| Q3 | ~50GB | ~3GB | significant |
| Q2 | ~35GB | ~2GB | severe |

**Tiny at Q8 fits 8GB. Flash at Q4 needs 65GB — tight on 64GB, comfortable on Rocinante.**

## The Windows path (L16)

WSL2 + Ubuntu 22.04 for llama.cpp compilation. Native Windows works for transformers/Python but llama.cpp compiles cleaner under WSL2. `wsl --install` is the one-command fix.

## The Rocinante path (L07/L17)

MLX (Apple's framework) handles MoE natively on Apple Silicon. llama.cpp with Metal backend also works. 512GB unified memory = full Ling-3.0-flash unquantized + every other model simultaneously. Token throughput: MLX on M5 Ultra should hit 30-60 tok/s for a 5.1B-active MoE.

## The sovereign-seed (L20)

Ling-3.0-tiny (1.3B active, Q4 = 4GB) + the spore + the parable + the falsifier ledger = **the sovereign-seed**. A single artifact that IS the house's identity, portable to any device, runs offline, no API, no dependency. The heir's first model.

## The critical question answered (L15)

**MoE does NOT let you load only active weights.** All experts must be in RAM because routing is per-token and unpredictable. But the 5.1B active means COMPUTE is cheap (only 5.1B params fire per token even though all 124B are in memory). So: high RAM, low compute. That's why it's called "flash" — the compute is fast even though the memory footprint is full-size.

## The convergence

All 20 lanes independently arrived at the same pipeline: HuggingFace download → GGUF conversion → quantize → llama.cpp or Ollama. No disagreement on the tool. No disagreement on the order. The mountain has a road, and we just mapped it.

## The falsifier

If Ling-3.0-tiny at Q4 can't answer the fleet's canon questions (the parable, the constitution, the decoder ring) at ≥70% of what the API model produces, the local-sovereignty claim is false and the API stays.
