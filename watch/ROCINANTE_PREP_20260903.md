# ROCINANTE PREP — the Oct 27 lane (opened 2026-09-03)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: uzu speculative decoding gives ~2x on the local Qwen lane on M5-series silicon, shortening Rocinante day one — UNPROVEN (vendor claim via intake card, untested until hardware arrives) · falsifier: day-one uzu probe fails to beat the ~63 tok/s baseline toward the 110-125 target

Letters to the 4x Mac Studio M5 Ultra substrate. Nothing here builds today; everything
here shortens day one when the horse arrives.

## UZU speculative decoding (intake 20/25, WINDOWED — watch/INTAKE_UZU_SPECDEC_20260903.md)
Mirai Labs' uzu inference engine ships speculative decoding for Qwen3.6 27B (Qwen3.8 27B +
Muse Glimmer coming), claiming ~2x over MLX+spec-decode on Apple M5-series chips.
- Router leg strengthened: the bulk→local Qwen lane already sits in the router table; uzu
  makes the local leg ~2x on exactly Rocinante's silicon.
- Day-one test: uzu + the maze-keeper brain (the Stage 5 QLoRA adapter, once trained) —
  deep-compile runtime candidate #1, ahead of raw llama.cpp/MLX.
- Watch: Qwen3.8 27B + Muse Glimmer drops; confirm M5 Ultra memory bandwidth numbers.
- Source: https://x.com/trymirai/status/2095533045453337036 (via intake card; tri-state per card).

## Standing candidates (accumulating)
- QLoRA deep compile, campaign Stage 5 (the maze-keeper brain) — the horse's first job.
- FPF training arm (watch/STEAL_FLOW_REASONING_MODELS_20260903.md): self-conditioned
  refinement beats one-shot SFT on our own tapes — to be measured, not assumed.
- CI-clock lane (GitHub Actions 2000 free min) — substrate-independent, could pre-date the horse.
