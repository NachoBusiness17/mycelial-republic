---
name: box-burn-90-percent-law
description: Operator law 9/26 — saturate the box at 90-100% on estate work "intelligently", never as a Defender accident; GPU unlock = llama-server Vulkan already proven on the RX 5600 XT; family-box night window; filed as Stone 7
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_71c96bdc-4107-40e1-96f8-7211934ac587
---

During the 09-25/26 Defender storm (MsMpEng at 50% CPU + 100% disk catching up on the estate's real write storm; zero threats found; operator rebooted at 23:47:05) the operator watched the meters peg and said "damn this is what i want haha... man i wanna go to 90% on all that shit intelligently if not 100%". When I framed the storm as an error he corrected me: "not a glitch ahaha". He added the Defender exclusions himself ("done ty it worked man").

**Why:** box saturation is the goal state, not a malfunction. The only thing wrong that night was that the burned work belonged to Defender's scanner instead of the fleet.

**How to apply:**
- Heavy local runs at NIGHT only, hard stop 07:00 (family-box law). The window is ENFORCED, not advisory: the **amd_window_guard** (ghost FKB signal, 180 hits sampled 9/26) silently reaps daytime/evening heavy local jobs — it killed three Arm C 200-leg attempts mid-problem before attribution. Schedule night jobs as detached schtasks (MagArmC200 = run_armC.py at 09-27 01:00, full interpreter path) instead of fighting it. tools/box_burn_watch.py (built 09-26) samples cpu/mem/disk-rate/gpu every 60s into state/fuel/box_burn_watch.jsonl until 07:00; tune burns against that curve, not vibes. First full night: 362 samples, CPU avg 39 / peak 97.1, GPU avg 1 / peak ~100 (GPU belongs to llama-server, idle without it). NOTE: sampling continued past 07:00 — either a second writer (gala afterparty lanes churned all night on the same jsonl) or a stop-logic miss; check before trusting the curve.
- SHARED-OLLAMA THRASH LAW (learned 09-26 morning): the family ollama instance serves every seat, and concurrent jobs from different models evict each other (qwen2.5-coder vs gemma:2b = full 1.7-5GB model swap per call). Arm C starved 5 hours on ONE problem this way. Any long local run must pin "keep_alive" in the generate payload (and ideally run when other seats are quiet), or the burn silently turns into model-swap I/O.
- GPU unlock is REAL and already on the box: the RX 5600 XT is gfx1010 (ROCm will never support it) but llama-server.exe drove the GPU to 53% sampled via llama.cpp Vulkan while ollama runs CPU-only at 3%. Wire estate lanes to that llama-server or an ollama Vulkan backend; the training spine (QLoRA/Rocinante) is the biggest GPU sink once inference is GPU-routed.
- Demand stack that legitimately eats the ceiling: pile classify (drained 137/137 on 09-26, gauge complete), full_scan briefs (walk scope drained: 3,165 briefed, 92-record tail cleared 80 ok / 12 fail — the daily plan's "3,185 remaining" was stale), the Mr Pool 340-video whisper backlog (transcriber lives OUTSIDE the repo, path unlocated), training spine.
- Filed as Stone 7 in queue/todo.md.

Related: [[boot-lane-interference-burn-20260925]], [[burn-program-24x7-20260925]], [[law-11-credits-over-failure]].
