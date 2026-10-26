# INTAKE — FLASH LOCAL WEIGHTS (Unsloth GGUF) — 2026-09-05

**Source:** X_FLASH_HARVEST_20260905.md roots 4–5 (Unsloth guide + GGUF repo + r/LocalLLaMA M2 Ultra field test), cross-receipted web layer. **Verdict: 21/25 BUILD WINDOWED — ROCINANTE-GATED, docked beside UZU probe (watch/INTAKE_UZU_SPECDEC_20260903.md).**

## THE FIND

GLM-5.3-Flash — the model this seat rides free all week — is **MIT-licensed, weights public**, with a day-one local recipe pinned by others: Unsloth dynamic quants (1-bit ~100GB RAM / 3-bit 128GB / Q4_XS field-tested) + a special llama.cpp PR (support not upstream). M2 Ultra reality check: **works, but TTFT 3–4 min** (prompt processing bound on Apple Silicon).

## WHY IT MOVES DECISIONS

1. **Rocinante day-one probe card, sibling row to UZU:** target = GLM-5.3-Flash GGUF on 4x M5 Ultra — tok/s AND TTFT, vs the M2 Ultra honest baseline (3–4 min TTFT). Beat ~63 tok/s (UZU target) or explain why not.
2. **"Own almost everything, rent frontier for judgment"** gets a date (Oct 27) and a recipe that costs $0 to prepare. Our own weights of our own primary lane = no quota, no promo cliff, no vendor.
3. **Maze bake-off third contestant:** GLM-4.7-Flash-30B vs qwen2.5:32b vs (post-Oct-27) 5.3-Flash-A18B local.
4. **This box (68.7GB) cannot host even 1-bit** — no vanity attempt before Rocinante; the gate is real, not laziness.

## FALSIFIER

Oct 27: run Q4_XS via Unsloth PR on Rocinante. If TTFT < 60s AND gen > 30 tok/s at Q4: local flash becomes a standing fleet lane (batch-class). If TTFT > 3 min like M2 Ultra: Apple-Silicon prompt processing is structural — local lane stays batch-only, UZU spec-decode probe becomes the lever.

**Operator hands owed: none. $0. Docked.**
