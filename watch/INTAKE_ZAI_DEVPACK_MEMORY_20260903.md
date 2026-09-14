# INTAKE: Z.AI DEVPACK FAMILY MAP (memory-mechanism + overview + best-practice + coding-tool-helper + tool/others) — 2026-09-03

Genome: research_socratic (six steps) on L0 v1. Fold: operator pasted 1 URL + 4 coordinator
addenda — the complete /devpack/ family as far as the docs index reveals. One card, one pass.

## ITEM
1. https://docs.z.ai/api-reference/introduction (API root; auth, base URL, glm-5.3 examples)
2. https://docs.z.ai/devpack/resources/memory-mechanism (the "memory mechanism" page)
3. https://docs.z.ai/devpack/overview (devpack parent: GLM Coding Plan feature family, credits)
4. https://docs.z.ai/devpack/resources/best-practice (context/session best practices)
5. https://docs.z.ai/devpack/extension/coding-tool-helper (`@z_ai/coding-helper` CLI)
6. https://docs.z.ai/devpack/tool/others (16 coding tools + 3 general agents, base URLs)
Measure pass added: https://docs.z.ai/llms.txt (docs sitemap — the falsifier)

## THE SIX STEPS

### 1. INGEST — verbatim receipts
- Base URL (standard API): "https://api.z.ai/api/paas/v4"; auth "Authorization: Bearer ZAI_API_KEY".
- Coding-plan door (Anthropic Messages): "https://api.z.ai/api/anthropic"; OpenAI CC: "https://api.z.ai/api/coding/paas/v4"; OpenAI Responses: "https://api.z.ai/api/v1".
- Wrong-endpoint warning: "inability to use GLM Coding Plan subscription quota."
- Scope gate: plan "is limited to use within the following officially supported tools and product environments"; general-purpose agents served "on a best-effort basis" — under load "some requests may face temporary rate limits."
- Memory-mechanism page, the whole claim: "Memory enables a coding agent to retain context across tasks and sessions" — implemented as FILES: CLAUDE.md, ".claude/rules/", MEMORY.md ("the first 200 lines of MEMORY.md are included automatically"), `/memory`, `/init`, plus RAG ("query → embedding → vector search → retrieve documents"). Attributes ALL of it to Claude Code: "Claude Code docs explicitly states that each session begins with a fresh context window."
- Overview credits: Lite 2,000/10,000 · Pro 12,000/60,000 · Max 28,000/140,000 (5h/weekly), "Starting at just 18 USD per month". Multipliers GLM-5.3 6.9/1.7/24, GLM-5.3-Flash 2.3/0.56/8, MCP servers 1.2 output-only. "MCP tool credit usage = Number of calls × Output multiplier."
- Off-peak: "During off-peak hours, model usage is charged at 50% of the standard credit rate" — peak "Monday to Friday, 14:00–18:00 Singapore Standard Time (UTC+8)".
- Campaign: paid plans get "unlimited usage" of GLM-5.3-Flash via ZCode from 23:00–09:00, plus doubled quota on other Agents.
- Auto-routing: "Requests for GLM-5.2/GLM-5.1 will be automatically routed to GLM-5.3, requests for GLM-4.7" → GLM-5.3-Flash.
- coding-helper: `npx @z_ai/coding-helper`; manages "Claude Code, Codex, OpenCode, Crush, Factory Droid" via `coding-helper auth glm_coding_plan_global <token>` / `auth reload claude` / `doctor`. (ZCode NOT in its managed list; ZCode IS first in tool/others' 16-tool list.)
- Best-practice: "put temporary instructions in the prompt, and put long-lived rules in project-level configuration files"; "session management is a form of context management"; "If a prompt pattern or task flow is used repeatedly, it should probably be captured as a Skill."
- Plan-family extras: all plans include "Vision Understanding, Web Search MCP, Web Reader MCP and Zread MCP".
- MEASURE (llms.txt): NO memory endpoint anywhere in the API reference — "the only memory-related content in the entire index is the 'Memory-mechanism' guide." One unfetched door found: `https://docs.z.ai/guides/capabilities/cache.md` (Context Caching).

### 2. MAP — corpus intersections
- **claude-zai door**: `.claude/settings.json` already carries `"ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic"`; `harness/glm_coder.py:29` pins the same. Our door is a hand-configured instance of the tool/others path — coding-helper is an alternative wizard to the same door, zero new capability. `mag/offerings.py:100` lists both endpoints.
- **verkle chain / memlang / room.jsonl / session transcripts**: vendor "memory" is client-side markdown + RAG ADVICE, not a server substrate. It cannot replace the chain; it CORROBORATES it — the vendor's own margin says memory lives in files the operator owns. Files+chain over processes wins by vendor concession.
- **cache doctrine**: GLM53_ARCHITECTURE_PRO.md ("PROMPT CACHE ≠ KV CACHE"), GLM53_FLASH_EXPLOITATION.md (stable prefixes, off-peak 50%). Overview CONFIRMS the off-peak 50% credit rate vendor-side; cache.md (Context Caching guide) is the unfetched sibling of the KVFlow/cache-farming arc.
- **fuel_feed lanes**: the 23:00–09:00 unlimited-flash campaign is a lane-config upgrade candidate — Unproven until receipted. Auto-routing (4.7→5.3-flash) is exactly the class of silent pin-break ZAI_LITE_ISOLATION_LAW_20260901.md guards; our glm-4.5-flash pin is outside the stated routing set TODAY, but routing sets grow.
- **QLoRA campaign**: no collision — vendor ships no model-side memory product; deep-compile memory has no competitor here.
- **Expert reference**: credits table matches docs/ref/ZAI_API_EXPERT_REFERENCE.md numbers exactly (already receipted). New intel in card: off-peak window definition (SGT), MCP multipliers, campaign, 16-tool list, coding-helper CLI.
- Re-find honesty: credits/multipliers = re-find (repetition is emphasis). Off-peak hours definition, night-flash campaign, MCP credit rule = new.

### 3. ASSERT — steel-man, one sentence
z.ai's devpack "memory mechanism" is the vendor documenting the client-side file-memory pattern (markdown layers + RAG + compression) that coding agents should run, bundled inside a GLM Coding Plan whose real substance is credits, endpoints, off-peak pricing, and a managed tool-integration CLI.

### 4. ATTACK — strongest counter-case
- **Cause 1 — title promises a product, body delivers a tutorial.** "Memory-mechanism" names a mechanism; the page contains "No z.ai API names, endpoints, parameters, limits, or pricing" (ingest receipt). Anyone bolting an adapter onto "z.ai memory" builds against nothing. The ITEM's hypothesis dies here.
- **Cause 2 — summary-of-a-summary.** Every technical fact on the page is attributed to Claude Code's docs ("Claude Code docs explicitly states…"). Secondhand vendor prose fails the ingest law's no-summary-of-a-summary bar; the 200-line MEMORY.md limit is Anthropic's number, not z.ai's.
- **Cause 3 — the tool-scope gate is a real exposure.** "limited to use within the following officially supported tools" + best-effort rate limits for general agents. Our custom harnesses (harness/glm_coder.py, watch/invariant_probe_001.mjs) ride the door from OUTSIDE the blessed 16-tool list shape — a usage-policy exposure the vendor can enforce at any time. (Enforcement against us: Unproven.)

[SOCRATIC] Assumption attacked: that "devpack memory-mechanism" is a vendor memory product competing with our organs. Instrument: full-text ingest of the page + sitemap falsifier (llms.txt grep). What survives: a best-practices page corroborating files-over-processes, plus real quota/pricing intel in the SIBLING pages — the value was in the fold, not the headline.

### 5. MEASURE — falsifiers run
- $0 RUN: llms.txt sitemap grep → zero memory endpoints in the entire API reference; only the devpack advice guide. DISPROVES "server-side memory API exists." Kill condition for this card's central verdict: a `/memory`-family endpoint appearing under docs.z.ai/api-reference, or a `context caching` write API documented in guides/capabilities/cache.md with store/recall semantics — either reopens the MAP as a competitor/substrate.
- $0 RUN: `.claude/settings.json` + `harness/glm_coder.py` contain the exact endpoint tool/others documents → door identity Supported by local receipt, not just vendor claim.
- NOT RUN (written for next seat): the 23:00–09:00 SGT "unlimited GLM-5.3-Flash via ZCode" probe — fire one cheap flash call inside tonight's window, echo the model name back (routing-drift check per isolation law), log credits before/after. Kill condition: either the call bills credits at standard rate, or the served model ≠ glm-5.3-flash → campaign claim Disputed, fuel_feed stays as-is.

## SCORE (5 axes, 0–5)
- FIT 2 — corroborates organs, adds no bolt-on surface; door/lanes already exist.
- PULL 3 — cache-doctrine off-peak law, free-lane redeploy night window, isolation-law watch all live.
- COST 5 — six fetches + repo greps, $0 API spend, one pass.
- WINDOW 4 — ran on the intake lane; night probe is window-bound by design.
- NOVELTY 2 — most of overview was already receipted in the expert reference; off-peak/SGT definition, night campaign, MCP credit rule, coding-helper CLI are the new residue.
**TOTAL 16/25 → BUILD WINDOWED band.**

## READ (honest)
The headline is a ghost: "memory mechanism" is the vendor teaching Claude Code's file-memory pattern, with zero z.ai API behind it — so there is nothing for the chain to consume and nothing consuming the chain. The REAL cargo is in the siblings the operator pasted around it: off-peak is 50% credits inside a named SGT window, paid plans claim unlimited GLM-5.3-Flash 23:00–09:00, MCP tools bill at a 1.2 output-only multiplier, and the plan is contractually scoped to a 16-tool list our hand-rolled harnesses sit just outside. Net: our memory organs are confirmed sovereign by the vendor's own margin; the quota intel is worth calibration and one windowed probe.

## TRI-STATE
- "z.ai ships a server-side memory feature for the devpack" — **DISPUTED**. Evidence: ingest receipts (no API names/endpoints/pricing on the page); llms.txt falsifier (zero memory endpoints in API reference).
- "Devpack memory doc = client-side file-memory advice (Claude Code patterns)" — **Supported**. Evidence: memory-mechanism extraction quotes; best-practice page consistency.
- "api.z.ai/api/anthropic is the coding-plan door for Claude-Code-shaped tools" — **Supported**. Evidence: tool/others receipt + local `.claude/settings.json` + `harness/glm_coder.py:29`.
- "Off-peak model usage bills at 50% credits" — **Supported as vendor claim** (overview quote); **Unproven as receipt** (no metered pair across the peak boundary).
- "Unlimited GLM-5.3-Flash via ZCode 23:00–09:00 on paid plans" — **Unproven** (marketing; needs the night-window probe).
- "Auto-routing 5.2/5.1→5.3, 4.7→5.3-flash" — **Unproven**; watch-item for ZAI_LITE_ISOLATION_LAW (silent pin-break class).
- "coding-helper manages auth for Claude Code/Codex/OpenCode/Crush/Factory Droid" — **Supported as documented** (page quotes); **Unproven in operation** (not run; ZCode absent from its managed list).
- "Plan limited to officially supported tools; general agents best-effort" — **Supported as vendor policy** (quotes); enforcement against custom harnesses **Unproven**.

## VERDICT (three verbs, exhaustive)
- **CALIBRATE (now, $0)**: fold off-peak SGT window + night-flash campaign + MCP credit multipliers + 16-tool scope into docs/ref/ZAI_API_EXPERT_REFERENCE.md and GLM53_FLASH_EXPLOITATION.md; add routing-drift watch-item to the isolation law's surface.
- **BUILD (windowed, needs operator GO — spends plan quota)**: the 23:00–09:00 unlimited-flash receipt probe (one call, model echo, credit delta) — this is the score-band's windowed build; it upgrades or kills a fuel_feed lane config.
- **REMEMBER**: the memory-mechanism page as corroboration-not-capability; this card is the record.

## ROUTE
- Operator-GO question: the devpack family is a SUBSCRIPTION BUNDLE (Lite/Pro/Max, 5h+weekly credits, off-peak 50%, night flash window, 4 MCP servers included) — does the operator want the night-window probe fired tonight (23:00–09:00 SGT) to receipt the unlimited-flash claim before any fuel_feed repoint? One call, pennies at most.
- Fuel_feed owner: candidate lane config if the probe receipts; routing-drift echo check belongs in every probe per the isolation law.
- Watcher: vendor can enforce the 16-tool scope against hand-rolled harnesses — no action, just eyes.
- No memory-organ adapter to build. The chain stands.

## TWO COUNTERS
- FORBIDS: building any adapter, consumer, or sync for a "z.ai memory API" — none exists; routing effort there is chasing a page title.
- PAID RENT: off-peak/night-window + MCP-multiplier intel now on record for lane economics, and the isolation-law routing-drift watch has a named vendor behavior to watch.

## THE CROP (visibly incomplete)
- NOT fetched: https://docs.z.ai/guides/capabilities/cache.md — the Context Caching guide, the one live door where a server-side cache API could actually live; next intake should fetch it before any cache-doctrine calibration lands. Also unfetched: per-tool subpages (/devpack/tool/droid, /crush, …), /devpack/usage-policy, /devpack/faq, /devpack/mcp/* (four MCP servers).
- NOT receipted: the night-window flash claim, the off-peak metered pair, enforcement behavior of the tool-scope gate.
- NEXT LENS: fuel_feed owner (lane config + probe) and the isolation-law holder (routing drift); operator GO for the windowed probe. Cache.md wants the cache-doctrine chair, not the memory chair.

## RECEIPT (room row)
`2026-09-03 | zcode | INTAKE_ZAI_DEVPACK_MEMORY_20260903 | devpack family mapped (6 pages + sitemap falsifier): vendor "memory" = client-side advice, no API — chain corroborated not consumed; off-peak 50% SGT + night flash campaign = calibrate; night probe pending GO | verdict CALIBRATE 16/25 BUILD-WINDOWED`
