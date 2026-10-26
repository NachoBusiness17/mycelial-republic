# FREE LANE INTEL — Bonsai 2 27B (2026-09-23, evening)

Intel source: operator link → https://x.com/sudoingX/status/2102829187581317225 (130 likes, 15-min video demo, quote of own teaser at 75 likes).

## What it is (verified against public sources this session)
- Prism ML's **Ternary-Bonsai-2-27B**: Qwen 3.8 27B dense, compressed to ternary (3-bit), GGUF on Hugging Face (prism-ml/Ternary-Bonsai-2-27B-gguf).
- ~5.9GB weights (vs ~54GB FP16). Runs llama.cpp. Fits 12GB VRAM with context room. MTP (multi-token prediction) for speed.
- Vendor claim: 98.2% of FP16 benchmark retention — **vendor number, grade contested** until our own bench or independent HN verification.
- Stranger demo (tweet, 2026-09-23): RTX 3060 12GB (#1 GPU on Steam), 50 tok/s fresh / 22 avg, 125k context, "hermes agent" 5 hours, 328k tokens, 8 JS files, 2,368 lines, zero hand-written code, entire game built. Video exists (903s). Grade: demonstrated-by-demo, secondary until our own run.

## Why the estate cares
1. **Overnight game-builder lane**: Bonsai 2 on our GPU during the family-off window = $0 compute for game_estate modules, beacon pages, boss-phase code. Matches the night law exactly.
2. **Convergence**: "Frontier from Flash" (Climb 1, 09-20) — stranger-proof on the median Steam GPU. Scoreboard event.
3. **Context unlock**: 125k context at 12GB — the usual local-lane killer (no context) is solved by the compression.

## Our box (checked 09-23 evening)
- Ollama up on :11434, 15 models incl. **qwen2.5:32b** → hardware already handles 32b-class; Bonsai 2 fits with room.
- nvidia-smi not answering from the shell (PATH/driver probe TBD); one qwen2.5-coder timeout at 17:25Z.
- Namesake flag: tweet's "hermes agent" ≠ confirmed our hermes harness. Unverified lineage.

## TRIAL (fires after family hours — night law)
1. `ollama pull` from HF GGUF (or Modelfile from the prism-ml file) — ~6GB download.
2. One real chore: one game_estate module OR a label-farm batch. Not a toy prompt.
3. Measure: tok/s fresh/avg, context held, quality vs qwen2.5:32b baseline on the same chore.
4. File bench receipt here (append).
5. If it holds: standing night cadence = gopher chores move local during family hours, API lanes stay for day.

Status: STAGED — awaiting night window.

## BENCH RECEIPT (night run, Nones first cell)

```json
[
 {
  "model": "hf.co/prism-ml/Ternary-Bonsai-2-27B-gguf:PTQ1_0",
  "ok": false,
  "error": "HTTPError: HTTP Error 500: Internal Server Error"
 },
 {
  "model": "qwen2.5:32b",
  "ok": true,
  "wall_s": 479.0,
  "tokens": 520,
  "tok_per_s": 1.2,
  "head": "```python\nWING_CHUN_STEP_DEGREES = 15.0\n\nBOSS_CONTEXT = {}\n\nclass Phase:\n    def __init__(self, name):\n        self.name = name\n\n    def enter(self, context):\n        pass\n\n    def update(self, contex"
 }
]
```


## NIGHT RUN FINDING (2026-09-23 ~19:0xZ)
- ollama 0.32.7 registers the model (6.6GB) but generation returns HTTP 500 reproducibly: **the PTQ1_0 ternary quant is not supported by this engine build.** Fix (morning, needs GO): update ollama to latest, or run the GGUF via llama.cpp directly per the mindstudio guide.
- Baseline receipt: qwen2.5:32b DID run the chore but at **1.2 tok/s (479s wall, 520 tokens)** — CPU-bound, not a usable chore lane on this box. Output quality was clean (correct constant, proper class structure).
- Implication: the night lane's real engine is exactly the compressed-27B class (Bonsai/ternary) or a 7b — 32b is a paper weight here at night. The trial thesis STRENGTHENS; the engine update is the only blocker.

## BENCH RECEIPT 2 — after ollama 0.32.7 → 0.34.3 upgrade

```json
[
 {
  "model": "hf.co/prism-ml/Ternary-Bonsai-2-27B-gguf:PTQ1_0",
  "ok": false,
  "error": "HTTPError: HTTP Error 500: Internal Server Error"
 }
]
```

## 7B NIGHT-LANE BENCH (fits the 6GB card)

```json
{
 "model": "qwen2.5-coder:7b",
 "ok": true,
 "wall_s": 33.8,
 "tokens": 460,
 "tok_per_s": 21.8,
 "has_constant": true,
 "has_phases": true,
 "head": "```python\nBOSS_CONTEXT = {}\n\nWING_CHUN_STEP_DEGREES = 15.0\n\nclass Phase:\n    def enter(self, context):\n        pass\n\n    def update(self, context):\n  "
}
```


## FULL-BLAST NIGHT RUN (2026-09-23 ~20:0xZ) — every lane live-fired
- **OpenRouter a1 + a2: BOTH ALIVE** — correct answer on the Church question (2.2s / 7.7s). The historical empty-content fails were model-dependent, not lane-dead.
- **NVIDIA lane RESURRECTED then RE-ENGINED**: key was orphaned under three names (fixed: NVIDIABuild); deepseek-v4-flash-0731 had rotated off the catalog (404) — catalog re-pulled (82 models) and the lane re-engined on z-ai/glm-5.3-flash (verified: correct answer, 19.7s). deepseek-v4.1-flash timed out once (cold); kimi-k2.6 404 (rotated).
- **Gopher label-farm: grew** (third batch).
- **Bonsai 2 FINAL VERDICT: hardware-incompatible with this box.** The GGUFs use Hadamard-rotated ternary (ggml type 143) requiring the PrismML-Eng/llama.cpp fork — CUDA + Metal kernels only, no Vulkan. Stock llama.cpp 'loads Q2_0 without warning and produces garbage' per the vendor. RX 5600 XT (AMD, 6GB, Vulkan) is out regardless of engine updates. Bench claim for CUDA cards: 84.78 avg vs 86.32 FP16, 262K ctx, Apache 2.0 — real, but not for this hardware. Night lane on this box = qwen2.5-coder:7b (proven 21.8 tok/s) until hardware changes.
- Free fleet standing: z_ai3 Lite + gopher KEY_2 + NVIDIA Build (glm-5.3-flash) + OpenRouter x2 + Groq x2 + Cerebras + ollama 7b + MiMo window (thru 09-28).
