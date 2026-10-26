# VAST TEMPLATE V2 — unified (canonical; supersedes V1)

> **Provenance:** SELF-STEAL RESULT. The canonical recipe existed since **2026-08-04** at
> `/mag/scripts/vast/` (TEMPLATE.md + MODEL_STACK.md + onstart_mag_ollama.sh +
> Dockerfile.mag-ollama) — found only after 5 E7 attempts re-derived a worse version.
> V2 unifies the August prior art with tonight's API lessons. **Update this file, never
> re-derive.** Source of truth for the architecture rules remains /mag/scripts/vast/.

## The August architecture rules (DO NOT INVERT — from TEMPLATE.md)
- Grok Build TUI stays on the operator's PC; Mag lab (:8765) owns DNA; **the Vast node is
  hot inference only.**
- **Never put Verkle tip / agent_state / private DNA on Vast disk** (interruptible).
- Access pattern: `ssh -N -L 11434:127.0.0.1:11434` tunnel from host, or public IP + port map.

## Hardware target
Quadro RTX 8000 48GB class (Turing Q4 inference); ≥80GB disk for model pulls; ~16 CPU /
96GB RAM slice. Budget alternative verified 2026-09-01: RTX 3090 24GB at $0.069/hr
(AWQ-capable cc 8.6; V100 cc 7.0 is NOT).

## THE RECIPE (from onstart_mag_ollama.sh, proven design)
```
image: any CUDA base (the Aug recipe installs ollama in onstart — ~40s)
onstart: |
  curl -fsSL https://ollama.com/install.sh | sh
  export OLLAMA_HOST=0.0.0.0:11434
  export OLLAMA_KEEP_ALIVE=30m
  nohup ollama serve >>/var/log/ollama-serve.log 2>&1 &
  (wait for /api/tags, then pull the stack)
stack (MAG_STACK=rtx8000_48):
  gemma:2b (clerk/router) · nomic-embed-text (embed) · qwen2.5:32b (worker, ~18-22GB Q4)
```
Alternative path (verified design, vLLM): image `vllm/vllm-openai:latest` (REAL — vastai/vllm
does not exist) + onstart `vllm serve {MODEL} --port 8080 --enable-prefix-caching`.
AWQ needs cc ≥ 7.5; 32B-AWQ ~19GB fits 24GB cards.

## Search API (2026-09-01 verified)
`GET /search/asks/?q=<urlencoded JSON>`; operators **eq|neq|gte|gt|lte|lt|in|notin**;
price key **dph_total**; compute_cap is DECIMAL (8.6); q must be valid JSON.
Known dead keys: cost_per_hr. GPU-name filter: gpu_name {in: [...]}.

## Boot windows (measured/estimated)
7B AWQ ~4.7GB: 10-15 min · 32B Q4/AWQ ~19GB: 25-40 min · ollama plant: install ~1 min +
pulls 5-25 min depending on stack. At $0.07-0.10/hr, patience is free — size the window
by pull, not impatience. Daemon errors (manifest unknown etc.) are visible on the vast
CONSOLE page only — ask the operator to paste the console block when API probes are ambiguous.

## Meter & destroy law
Every rental: pre/post balance or usage note, DELETE + re-GET /instances/ == 0 proof,
label prefix `e7`/`mag` for ownership. Never leave a box running past its rung.

## Self-steal addendum (the receipt for this file)
The E7 attempts (5 rentals, 4 distinct API quirks, ~$0.02 orphan spend — all destroyed with
proof) re-derived: the search syntax (3 quirks), the image choice (phantom), the boot
window economics. The archive held the complete answer at `/mag/scripts/vast/` since
08-04. Deref-first applies to INFRASTRUCTURE recipes, not just research claims.
