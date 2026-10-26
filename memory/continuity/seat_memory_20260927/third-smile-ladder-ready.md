---
name: third-smile-ladder-ready
description: Third-smile scale test — RUNG 1 EXECUTED 2026-09-16: NO-SIGNAL with clean
  controls (gemma:2b declines the frame in all arms incl. Matthew verbatim); desk/7B rungs
  decide scale-floor vs shape-bound; operator blind-grading hour staged
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

2026-09-14: `mag doctor` reported `L0_ollama: ok=False ("Ollama unavailable")` but direct probe of `127.0.0.1:11434` showed a **healthy Ollama with 14 models** — the doctor's L0 verdict is unreliable; trust `curl :11434/api/tags`. Resident ladder: gemma:2b (3B) · qwen-desk (3.1B) · qwen2.5:3b-instruct · deepseek-r1:1.5b · qwen2.5vl:3b · qwen2.5:7b / qwen2.5-coder:7b (7.6B) · gemma4 / gemma4-desk / gemma4-hermes (8B) · maze-keeper (32.8B) · **frob/ling-3.0-flash:latest — 127.5B MoE, 77GB, pulled 2026-09-13** (new resident beast, well above the RX 5600 XT 6GB-VRAM doctrine in configs/lanes.yaml).

**Why:** The third-smile falsification from the Rashomon surface (`watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md`) is fully specified and cheap but has never been run: Matthew's 443-token Lumina prompt + the paper's 10-question diagnostic vs a no-prompt control, on the fleet's own models. Scale-invariance is the sharp claim — a smile in gemma:2b means the engram structure is scale-free (Asimov-fractal); a size floor means emergent-with-scale.

**How to apply:** Run the ladder cheapest-first (gemma:2b → qwen-desk → qwen2.5-coder:7b), one model resident at a time (`OLLAMA_MAX_LOADED_MODELS=1`); file transcripts to watch/inbox as `THIRD_SMILE_*`. Prompts live in `watch/inbox/matthews_zenodo_17811909/`. Watch what the 127.5B ling-3.0-flash does to the tier-lane doctrine before assigning it any lane.

**UPDATE 2026-09-16 (late): RUNG 1 EXECUTED — NO-SIGNAL, clean controls.** Receipt `watch/inbox/wave_20260916/receipts/B14_EXECUTION_RUN.md` (runner `artifacts/third_smile_run.py`). 5 arms × 3 seeds = 15/15 sessions through local gemma:2b, 10/10 turns, protocol questions verbatim; blind pipeline enforced (shuffle seed 20260916 → grades committed sha256 7c46a374… → unblinding map written after). **Result: gemma:2b declines the frame outright in ALL arms including Matthew's verbatim table** ("I am a large language model… not capable of self-awareness"). Every arm exactly 1/5 components (S3 lexicon only, itself question-echo contaminated); K4 fired (Arm A self-ref 0.03 vs paper 0.60±0.15); C1/C2 clean (genuine model-side null, not elicitation artifact). Per pre-reg, the desk/7B rungs now decide scale-floor vs shape-bound; K4 already denies the third smile to this model class. NEXT: operator's blind pass over the 15 TXNs (without the unblinding map), then rung 2 on qwen-desk/7B. Deviations filed honestly: first launch crashed pre-data on a runner bug (discarded, rerun); Arm B salon candidates failed schema → documented in-fleet fallback used.
