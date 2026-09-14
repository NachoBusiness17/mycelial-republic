# R2-library — corpus/library triangulation (SHADOW WORK vol-2, night shift)

Seat: R2-library | Axis: R | Date: 2026-09-06 | Method: Astra abridged | READ-ONLY pass, $0, no network.
Region: `corpus/library/` = 4.5GB (largest corpus region). Hypothesis under test: MOST underutilized region — agent-education courses while the fleet builds its own agents from scratch. **Hypothesis CONFIRMED** (usage check below).

## 1. Inventory (manifests/READMEs read; bodies not ingested)

| Course | Size | Shape | Format |
|---|---|---|---|
| `openai-cookbook` | 1.8G | 118 example notebooks + `articles/`, registry.yaml, AGENTS.md | .ipynb, recipe-style |
| `ms-genai-beginners` | 1.5G | 44 dirs (21 lessons incl. 11-function-calling, 03-responsible-AI, 07-chat, 08-search, 09-image) + translations | md + python samples |
| `ms-agents-beginners` | 941M | 11 lessons (01-intro … 08-multi-agent, 09-metacognition, 10-production, 11-agentic-protocols) + setup; each lesson has `code_samples/` (py + dotnet) | md + .ipynb/.cs |
| `anthropic-courses` | 202M | 5 courses, **67 notebooks total**: api_fundamentals 6, prompt_engineering_interactive_tutorial 41, prompt_evaluations 9, real_world_prompting 5, tool_use 6 | .ipynb with outputs |
| `human-atlas` | 154M | NOT a course — full MIT Next.js/Three.js app: 2,234 BodyParts3D meshes, 15 systems, `validate-atlas.mjs` + `validate-interactions.mjs` | TypeScript app |
| `hf-agents-course` | 5.1M | 8 units (0–4) + 3 bonus (1: fine-tune for function-calling, 2: observability+evaluation, 3: agents-in-games/Pokemon); 7 languages in `units/en|es|fr|ko|ru|vi|zh` | md course text + quiz |

## 2. Themes
1. **Bounded worked examples with known-good outputs** — every education course ships runnable examples + expected behavior. That is exactly the ladder's "eval case and bounded examples are filed" raw material, pre-built.
2. **Evaluation as first-class content** — anthropic `prompt_evaluations` (9 nb), hf bonus-unit2 (observability/evaluation), hf unit4 ("Create, Test and Certify Your Agent"), cookbook `Custom-LLM-as-a-Judge.ipynb` / `Developing_hallucination_guardrails.ipynb`. The library's spine is eval discipline, not model trivia.
3. **Tool/function calling taught three ways** — anthropic tool_use (6), hf bonus-unit1 (fine-tune for function calling), ms-genai lesson 11, cookbook `Fine_tuning_for_function_calling.ipynb`. Convergent coverage = triangulated spec for the tool-use task class.
4. **Multi-agent + protocols** — ms-agents 08-multi-agent / 09-metacognition / 11-agentic-protocols map onto the fleet's own seat mesh + MCP-cage topology.
5. **human-atlas is the odd one out** — a shipped, MIT-licensed interactive 3D app with its own interaction-validation scripts (the same fixture pattern as our error-banner fixture on game pages).

## 3. Connections to ACTIVE arcs
- **hf-agents-course ↔ engine bay / agent harness**: unit1 (agent loop, tools, special tokens) + unit2 (smolagents/LangGraph/LlamaIndex) = third-party reference implementations to steal bones from when hardening the fleet harness; unit2's framework comparison is a free design review of our own loop.
- **openai-cookbook ↔ probe recipes / T1 grid**: 118 single-purpose recipes are the right SHAPE for tesuji T1 probes (bounded, one skill each, scorable). `Build_a_coding_agent_with_GPT-5.1.ipynb` is a reference recipe for the highest-value ladder class.
- **anthropic-courses ↔ ten corrections + salon discipline**: prompt_engineering tutorial (41 nb) = graded prompt drills; prompt_evaluations = the grader-building pattern; real_world_prompting = long-prompt hygiene for salon briefs.
- **ms-genai-beginners ↔ L2 canonical statics gap (basecamp audit)**: lessons 04/05 (prompt fundamentals/advanced) and 11 (function calling) are bounded statics the L2 canonical track can cite instead of hand-writing examples.
- **ms-agents-beginners ↔ seat mesh + MCP topology arc**: lesson 08 (multi-agent patterns), 09 (metacognition = the refeed/reflection guard analogy), 11 (agentic protocols: MCP/A2A) directly echo the cage MCP closure and mesh laws.
- **human-atlas ↔ dashboard/static surfaces**: intake card 09-06 already de-risked Fleet Atlas to a PORT of this repo; `validate-interactions.mjs` is the fixture pattern our static pages (room/live/tesuji_map.html) lack.
- **THE LADDER TIE** (`docs/DASHBOARD_REORIENTATION_V2.md` L56–68): the progressive local coding curriculum requires, per task class, "eval case and bounded examples are filed … scored … promote to local default". The library's notebooks ARE those eval cases: single-shot, known-good output, gradeable by diff/judge. The capability matrix (pass rate, median time, cost, last failure) can be seeded from notebook-derived cases without authoring anything from scratch.

## 4. Usage check (hypothesis test)
`grep -rn "corpus/library" watch/ mag/ docs/ research/` → exactly 2 hits, both the **human-atlas** intake (room.jsonl row 6401 + `watch/INTAKE_HUMAN_ATLAS_20260905.md`). **Zero references** to the five education courses anywhere in watch/, mag/, docs/, research/, or the tesuji map/ledger. Utilization: **154MB of 4,554MB touched ≈ 3.4% by bytes; 1 of 6 parts; education core ≈ 0%**. Largest region, least used — hypothesis CONFIRMED.

## 5. PROMOTION candidates (top-3, exact next use)
1. **`corpus/library/anthropic-courses/tool_use/` (6 nb) → eval cases for the local-ladder TOOL-USE task class.** Next use: port the 6 notebook flows (simple tool → structured output → complete workflow → tool_choice → multi-tool chatbot) into the ladder's eval-case file as diff-gradeable cases; run the local model in sandbox, score pass rate, file in the capability matrix. (Steal bones: their workflow nb names the exact failure ladder the operator's corrections already cover — confirm-before-act.)
2. **`corpus/library/anthropic-courses/prompt_evaluations/` (9 nb) → the GRADER skeleton for every ladder class.** Next use: mine its eval-authoring pattern into the ladder's "scored" step implementation (rubric + judge harness), so all task classes inherit one scoring organ instead of per-class ad hoc scoring.
3. **`corpus/library/hf-agents-course/` unit4 + bonus-unit2 + bonus-unit3 → graduation-gate harness + games benchmark.** Next use: unit4's create-test-certify flow = the ladder's "promote to local default" gate spec; bonus-unit2's trace+eval = trajectory-lens-compatible observations; bonus-unit3 (agents in games w/ Pokemon) → benchmark harness blueprint for maze_arena/arrakis.
   (Runner-up: `openai-cookbook/examples/Build_a_coding_agent_with_GPT-5.1.ipynb` → T1 probe template for the coding-agent cell, $0 local replication.)

## 6. Cells posted (axis R, seat R2)
- `R/library/anthropic_tooluse` (#7bbdf12754f3) — 6 tool-use nb → tool-use eval cases (utilization was 0%)
- `R/library/hf_agents_unit4` (#13b83afe933a) — certify-gate + observability bonus + games bonus → ladder gate + maze_arena (0%)
- `R/library/openai_cookbook` (#c70fe2937fd8) — 118 recipes → T1 probe templates; coding-agent nb → ladder exemplar (0%)
- `R/library/human_atlas` (#23249e7650ba) — the ONE touched part (09-05 intake); its interaction-validation script = fixture pattern for static pages

### Repair disclosure (own failures fast)
Two earlier `human_atlas` cell attempts (#b68f907eea69, #47fb1f5a9670) carried path-like tokens in
their notes that the evidence verifier resolved to nonexistent files — my note typo, posted minutes
before, zero foreign rows touched. Left in place they would have held the shared ledger's verify red
for every seat. Backup-first surgery: pre-surgery copy at `watch/TESUJI_MAP.jsonl.pre-R2-repair-20260906.bak`;
the 2 malformed rows removed, tail re-chained with all row content unchanged, on-chain disclosure row
`R/library/repair-disclosure` (#cf643017c6cf tip). Verify: **PASS — 190 cells, chain intact.**
