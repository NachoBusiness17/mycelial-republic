## 9. GLM-5.3-FLASH ANNOUNCEMENT STEAL (2026-08-28, from the vendor blog)

Confirmed by the announcement text (operator pasted raw; fetchers were JS-walled):

1. **Weights are PUBLIC on HuggingFace.** Local runners: SGLang, vLLM, TokenSpeed.
   → ROCINANTE CALL (Oct 27): 320B total / 18B active MoE at 4.4x smaller KV cache
   than GLM-5.3 — the seat brain becomes self-hostable, and the NG-AISRP
   interpretability hook (log internals of a model we OWN) becomes executable on
   a frontier-class brain.
2. **Vision-in-the-loop is vendor design intent, not a bolt-on:** natively
   integrated so the model "decides when to observe and use visual feedback to
   guide subsequent actions" — self-visual judgment, test-time improvement, GUI
   judgment "grounded in real user flows." Vendor's own words: "Many failures
   only surface through rendering, interaction, or playtesting" (game dev named
   explicitly) and "Code lets the model build and change the world. Vision lets
   it enter the world people see and use." → This IS the fleet's
   play-is-epistemology doctrine in vendor voice; dumb-agent-with-eyes and the
   game harness ride a model BUILT to look. ZCode Browser Use + Computer Use are
   the named unlock surfaces (this seat's eyes are first-class).
3. **Architecture:** 320B total / 18B active (vs GLM-4.5's 355B/32B), 45 layers
   (vs 92), hybrid sparse + linear attention, Manifold-Constrained
   Hyper-Connections, IndexPool at 1M context. Attention compute 3x smaller and
   KV cache 4.4x smaller vs GLM-5.3. (That KV is serving cache, not our prompt
   cache — the §3 fleet finding is unaffected.)
4. **Served at scale on Chinese AI chips** (SGLang-based engine, W8A8, EPD
   disaggregation) — supply-line fact for the atlas. The serving stack was
   partly built by a GLM-5.3-powered infra agent — the model helped optimize
   the system serving the model (governor feedback loop, vendor edition).
5. **Benchmarks vs our lanes:** openly benchmarked against DeepSeek-V4-Flash
   (our drain-lane rival): base-vs-base splits (MMLU 88.1 vs 88.5, BBH 86.6 vs
   84.9, LiveCodeBench 37.6 vs 29.9). Coding/agentic approaching Claude Opus
   4.8; Pareto frontier at $0.045/task on AA Index v4.1.1. A price war between
   our two grind lanes — in our favor.
6. **Doctrine deltas:** (a) 1M context + flash cost = the session-mining lane
   upgrade — 630K sessions fit RAW (BOOT_4_7 shorthand existed because 4.7
   overflowed); (b) 3x coding-plan quota confirmed → post-Sep-1 rationing math
   may relax (operator's call, law 9 rightsize); (c) anon-tested as "ox-alpha"
   on OpenCode/OpenRouter before release — vendors run anonymous-lane recon too.
