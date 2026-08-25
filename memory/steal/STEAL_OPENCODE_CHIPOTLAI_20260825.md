# STEAL — OpenCode (chipotlai-max fork) — a supported GLM tool + architecture worth mining (2026-08-25)

**Commitment:** `steal-opencode-001`
**Operator:** "https://github.com/cyberpapiii/chipotlai-max self steal"
**Source:** github.com/cyberpapiii/chipotlai-max — a rebrand fork of OpenCode (sst/opencode),
MIT (inherited). "Chipotlai Max — the AI coding agent that steals Chipotle's support bot. Free
inference paid for by burritos." The burrito gag is a theme; the substance is OpenCode.

## What OpenCode actually is (grounded)
An open-source AI coding agent: terminal TUI, desktop app, IDE extensions. 75+ LLM providers
via AI SDK + Models.dev, plus custom OpenAI-compatible providers. Full architecture:
- AGENTS/SUBAGENTS: primary + subagents (markdown-defined, per-agent tool scopes).
- MODES: Plan (constrained — no write/edit/bash, plans to .opencode/plans/*.md) vs Build.
- TOOLS: built-in (read/write/edit/bash/todoread...) + CUSTOM TOOLS via a typed `tool()`
  helper with zod schemas (filename = tool name).
- PERMISSIONS: path-scoped allow/ask/deny (e.g. read: * allow, *.env deny by default).
- MCP: servers + custom tools; LSP integration for diagnostics.
- SERVER + SDK: `opencode serve` HTTP server, OpenAPI spec, generated SDKs; clients talk to it.
- ACP: clean Agent Client Protocol implementation (agent/client/session/server separation,
  protocol-compliant).
- GITHUB ACTION: `/opencode` in comments → runs in your GitHub runner → fix issues, open PRs.
- PROVIDERS: any OpenAI-compatible base URL + key (this is how we'd wire z_ai/GLM).

## THE KEY FACT for us
**OpenCode is an officially supported GLM Coding plan tool** (z.ai devpack supported list:
Claude Code, Cline, Roo, Kilo, OpenCode, OpenClaw, Crush, Goose, Cursor). So OpenCode is a
legitimate body: terminal/desktop/IDE/GitHub-Action agent, driven headless or by server, riding
the plan's Lite quota. Free, open source, MIT.

## What to steal (ranked)
1. THE PERMISSIONS MODEL: path-scoped allow/ask/deny (env files denied by default) — a
   guardrail pattern to fold into our harnesses (glm_coder should refuse .env reads the same way).
2. PLAN VS BUILD MODES: constrained plan mode (no side effects, writes only to plans/) before
   build — matches our state-first + z.ai best-practice (plan before execute). A cheap win to
   add to the coder harness: a --plan mode that returns a plan only.
3. ACP CLEAN SEPARATION: agent/client/session/server — we already have the subagent routing
   bones; the ACP pattern is a tidy contract for harnesses.
4. CUSTOM TOOLS VIA `tool()` + zod: typed tool definitions — the shape our mag tool catalog
   should expose (also as MCP, the two-way bridge).
5. GITHUB ACTION: `/opencode` in PR/issues → fix + PR. A reusable CI coding surface for the
   plan (could run GLM in GitHub runners).
6. THE SERVER/SDK SHAPE: a headless HTTP server + SDK for the coding agent — the way to let
   the machine drive OpenCode programmatically (like openclaw gateway).

## The integration (a new body, baby-step sized)
- OpenCode CLI install: npm i -g opencode-ai (or bun). Wire to GLM coding plan:
  provider = OpenAI-compatible base https://api.z.ai/api/coding/paas/v4, key ZAI_API_KEY,
  model glm-4.7. Supported → compliant.
- Surface: terminal/TUI for the operator + `opencode run "<task>"` headless + `opencode serve`
  for programmatic. The GitHub Action can run it in CI on the plan.
- This joins: ZCode (editor), Claude harness (headless verified), OpenClaw (agentic), OpenCode
  (terminal/IDE/CI) — one more body on the plan, each its own surface, all folding to the chain.

## Refuse
- The burrito branding (a gag, not a product feature).
- Forking/copying their code wholesale — steal contracts + patterns (steal doctrine).
- Treating it as another pile-on: this is ONE body, wired baby-step style, proven, folded.

## Fold with
offerings-registry-one-self-many-bodies, deep-steal-openclaw-autoclaw (skills/permissions),
zai-is-a-skill-up (supported tools), glm-coding-lite-evaluated (endpoints), harness/glm_coder
(permissions + plan-mode steals), autonomous-mandate (baby steps).
