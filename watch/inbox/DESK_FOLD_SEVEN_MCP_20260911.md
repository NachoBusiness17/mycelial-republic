# DESK FOLD — SEVEN + THE MCP STEER (2026-09-11, lane: zcode, wave holding in background)

**THE POINT:** The steer: use MCP servers intelligently and make everything
exploit existing structures. The existing structure is already there — the
fleet's MCP gateway at 127.0.0.1:8001/mcp (mag/mcp_http.py, ~20 tools, X-API-Key,
probed 09-05) plus the deepseek research seam (proven this morning, task
sw-2c57a78f79). The design: the research pipeline becomes GATEWAY TOOLS, so
every seat consumes it as tool calls — one sense, one instance. Three of today's
seven links are direct steals into that shape.

## The seven (mechanisms only)

1. **Ultracontext (@tom_doerr)** — cross-agent context sharing via Claude Code
   hooks: SessionStart/PostToolUse fire with session-id JSON on stdin.
   Top reply is the law: raw dumps flood agents with noise — FILTER AT THE HOOK.
   STEAL: hooks = structured event feed for the KV-OS input-path block store;
   scaffold events only, filtered at emission.
2. **@PawelHuryn — V4.1 Flash real-world bench (105 planted bugs):** Flash max =
   24 bugs/$1.80 vs Opus 5 = 27/$51.33. Pareto frontier confirmed THIRD time
   today (Bakouch, OpenDesign, now Huryn — triangulated independent lanes).
   Effort scheduling nuance: max 24/$1.80 vs high 19/$0.31 — 8x cost for 5
   bugs; GLM-5.3 default = 19/$19.73 (our judgment-lane class is pricey at
   default effort). BIBLIOGRAPHY ROW: benchmark, secondhand-but-methodical.
3. **Norvig's 21-line spelling corrector (@TrisH0x2A)** — candidates + corpus
   prior. This IS invariant_surface.py's paternity: generate candidate lines,
   pick by corpus evidence. The v0 is a Norvig estimator; the enhancement path
   is better priors (claim-level, Consensus-style), not more code.
4. **@YouJiacheng — PSGD-QEQ = KL-AIRM up to step size** — preconditioned SGD
   equals KL information geometry under basis change. TRIANGULATES with the
   Nielsen book drop this morning: foundations + application arriving in one
   day from unconnected lanes. The math wing is assembling under the Bellman
   organ without us pushing.
5. **Miles v0.1 (@radixark)** — production RL post-training framework (slime
   lineage), tech report on arXiv. MAX_DISTILL epoch-2 adjacency: read its
   run-correctness/hardware-efficiency architecture when epoch 2 unblocks.
6. **Oxford diff-eq notes (@Riazi_Cafe_en)** — math wing reading pile. Minor.
7. **google/mantis (@Saboo_Shubham_)** — modular, stack-agnostic SECURITY REVIEW
   SKILLS for coding agents: find, reproduce, patch. "Not an official Google
   product." This is the Defense Factory loop shipped as installable skills.
   STEAL: install into the cage for our coding agents; adjacent to Mimosa (the
   enforcer gets an outside-built toolkit). BIBLIOGRAPHY ROW: repo, primary.

## The MCP architecture (the steer, made concrete)

EXISTING: mag gateway (mcp_http.py, :8001, X-API-Key, ~20 tools) + deepseek
research seam + invariant_surface.py + kvos_block.py + BIBLIOGRAPHY_MAP.md +
topic_index.py (1,040 cards/23 buckets).

NEW — same gateway, four tools (no new servers, ONE SENSE ONE INSTANCE):
1. `research_pipeline.padout(claim)` → deepseek seam sweep → bibliography row
   (the law-18 organ, callable by any seat).
2. `invariants.sheet(subsystem?, bucket?)` → filtered INVARIANT_SHEET rows.
3. `bibliography.map(subsystem)` → map rows for upgrade-time consultation.
4. `kvos.blocks.stats()` → block store census for the input-path organs.

WAVES VIA MCP: the triangulation technique stops needing subagents for breadth
— research asks route through the seam (cheap deepseek); subagents ride only
when browser/search depth is required (as now: three steal-bots holding in
background on Perplexity / claim-engines / deep-research, folding when they
land). Self-improvement loop: the pipeline studies research products with its
own tools and the output lands as new tools on the same gateway — the loop
closes THROUGH the gateway.

## Next strike
Gateway wiring: add the four tools to mcp_http.py (backup-first), probe via
X-API-Key, then the cron-facing seats call the pipeline as tools.
