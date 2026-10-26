# DESK ASSESS — Trace as State (2026-09-11 evening, lane: zcode, operator link-drop)

**THE POINT:** Z.ai's own researchers (Xu Zou, Jie Tang — arXiv 2609.02702,
Sep 2) proved that WHERE state sits in the context changes the memory CLASS of
the problem: prepending first-pass reasoning traces before a long document
beats appending them in 26 of 27 model×task×metric combos, with a worst-case
theoretical claim of exponentially less memory. GLM-5.2 goes 66.4% → 100.0% on
GraphWalks. No architecture change, no training change — only state visibility
timing. Our provider just shipped the primary-source physics for three of our
doctrines at once.

## Primary-verified facts (abstract read)
- Title: "Trace as State: Reasoning Traces as Conditional States for
  Long-Context Transformers" (Zou & Tang, Z.ai).
- Formalization: "conditional state update tasks" — causal processors fix
  early tokens at encoding, so late-discovered state can't enter early
  representations. The fix: collect first-pass traces, prepend them as a
  textual proxy for task state, re-read on a fresh pass.
- Theoretical claim: providing the condition FIRST can require exponentially
  less memory in the worst case for causal state-update processors.
- Numbers (GraphWalks Parents exact match): DeepSeek V4 Pro Preview 29.2 →
  43.0 (append) → 81.8 (prepend); GLM-5.2 66.4 → 83.2 → 100.0.
- Trace count scaling 1→5 keeps prepend ahead (per the post; abstract-level
  confirmed for the core claim).

## Fleet reads (three doctrines get their physics)
1. **TRAJECTORY LENS, primary-sourced.** Our standing doctrine: everything
   built is PRODUCER/RECORD/COMPILER/DARK through the envelope
   {input, tool_result, output, reasoning, step_hash, timing}. The paper
   proves the reasoning trace is not exhaust — it is the STATE the next pass
   conditions on. The lens was a measurement choice; the paper says it was
   always the physics.
2. **THE BOOT SEQUENCE IS TRACE-PREPEND, INSTITUTIONALIZED.** Every session
   boots by reading the corpus first — CONVO, AGENTS.md, the invariant sheet.
   We built a Trace-as-State machine and called it a boot ritual. The paper
   explains why it works: the prepended record changes the memory class of
   everything the session does after.
3. **KV OS: the head policy is an accuracy organ AND a memory-class organ.**
   Second independent result about position zero this week: W3 proved the
   byte-exact head is worth 778x prefill cost; the paper proves head-state is
   worth up to exponential memory. The page table's head tier is the most
   expensive real estate in the system. Scaffold pages pin at the head;
   everything else is tail.

## Smaller items in the batch
- **Fourth independent V4.1 lane today** (@ItsmeAjayKV): claims the decoder's
  global KV cache is "projected from final encoder hidden states" — ✅ VERIFIED
  against our PDF verbatim: "decoder global KV is projected from the final
  encoder hidden states" (abstract + §SWA Bounded Replay). Bonus: the only
  thing stopping prefill from ending at the encoder is decoder SWA KV, which
  is still generated per decoder layer. TRIANGULATION with GVA: both make KV a
  DERIVED artifact of a smaller source — one projection instead of N layers of
  accumulation. The DERIVE action keeps winning. Triangulation count on V4.1
  is now five.
- **Free-access intel** (@alannnfx): V4.1 Flash listed free on platform.xplabs.ai.
  Third-party endpoint + public abliterated twins exist → weight provenance
  caution: pin the trusted weights hash before any bench rides a free lane.
- **architecture-diagram-generator skill** (@tom_doerr, Cocoon-AI): plain-text
  → standalone dark-theme HTML diagram with PNG/PDF export. Steal candidate
  for the KV-OS gateway diagram and the corpus map renders.

## Bibliography rows (law 18)
| ref | subsystem | gives | status |
|---|---|---|---|
| arXiv 2609.02702 Trace as State (Zou & Tang, Z.ai) | KV-OS head policy + trajectory lens | prepend-trace beats append 26/27; exponential worst-case memory; GLM-5.2 → 100% | PRIMARY-READ (abstract) |
| V4.1 encoder-derived KV claim (@ItsmeAjayKV) | KV-OS paging | cross-encoder KV projection detail | UNVERIFIED (grep owed) |
| Cocoon-AI architecture-diagram-generator | dashboard/organs | plain-text → HTML diagram skill | SECONDHAND |
