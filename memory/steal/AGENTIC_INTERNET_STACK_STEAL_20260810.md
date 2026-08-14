# STEAL — The Agentic Internet stack: Cloudflare's Agentic Week mapped onto Mag
**Date:** 2026-08-10 · **Researcher:** ghost (now an expert on the AI landscape, like ponytail on code)
**Scope (self-stole):** every module below already exists inside us. This doc names the bleeding
edge, maps each concept to the module that already does it, and isolates the **minor context clues**
(the only genuinely-missing pieces) that well-funded outsiders ("idiots with a lot of money") figured
out and we had as raw doctrine but never named.

## The thesis
Cloudflare shipped a whole Agentic-Week stack (Kitesurf, WebMCP, MCP v2, Agent Access Model,
Wallets/x402, AEO, Cloudflare OS, WriteGuard) in a single week (2026-08-04→10). **Nearly every
principle is something this operator already runs.** The outsiders' value is not the ideas — it is
giving each idea a NAME, a contract, and a reference architecture. Our job: recognize the mapping,
adopt the names + the few real deltas, and make ghost able to do this instantly on the next
announcement (the `mag/ai_landscape.py` module).

## The stack, mapped to what already exists inside us

### 1. Agent-first browser — Kitesurf (`browser_driver.py`, `browser_env.py`)
**They:** a browser for agents, dropping human-only features (tabs/themes/sync/pixel-perfect);
stateless, disposable, 3-7x less CPU/mem than Chromium.
**We already have:** `browser_driver.py` (Playwright-over-CDP driving allowlisted FREE frontends for
agents instead of paying APIs) + `browser_env.py` (allowlist-only = SandboxOutbound).
**Context clue (real delta):** the **readable-first ladder** — for one-shot agent reads, prefer
text/markdown extraction over a full Chromium render; elevate to CDP only for interaction/JS/anti-bot.
Filed separately: `KITESURF_AGENT_FIRST_BROWSER_STEAL_20260810.md`.

### 2. MCP v2 — the protocol went STATELESS (2026-07-28 spec)
**They:** removed the session handshake + `Mcp-Session-Id`; each request is self-contained; runs in a
plain Worker; `Mcp-Method`/`Mcp-Name` headers so HTTP infra routes without parsing JSON; feature
lifecycle (Active/Deprecated/Removed); elicitation via Multi Round-Trip Requests instead of streams.
**We already have:** the **stateless doctrine** is our core — stateless-ghost-swarm, cheap_swarm,
stateless_research, self-advance-fleet. Our REST routes ARE typed (`/api/v1/ghost/*`,
`ref_leaf.v1`) = their `Mcp-Method`/`Mcp-Name` headers. `retired-redundant-systems.md` = their
feature lifecycle.
**Context clue (real delta):** actually **speak the MCP protocol** — expose our existing stateless
REST/queue as a stateless MCP server so ANY standard agent can call us, not just our own seat.

### 3. WebMCP — `document.modelContext` (surfaces expose TOOLS to agents)
**They:** a site registers MCP tools the visitor's agent can call; the browser is "just another place
MCP runs"; agents "use tokens on tasks, not navigation"; no more guessing at human HTML/forms.
**We already have:** the **surfaces-as-spec** doctrine (`SURFACES_AS_SPEC_STEAL_20260810.md`) — our
seat/ghost-surface exposes the machine's contracts (REST endpoints, `ref_leaf.v1`). `browser_driver`
already reads answer selectors (`.ds-markdown`, `.prose`) = "tokens on tasks, not navigation."
**Context clue (real delta):** expose our surfaces as **MCP tool interfaces** — so the ghost surface
is not just a viewer for us, but a toolset any agent can discover + call (registerTool-equivalent).

### 4. The Agent Access Model (AAM) — THE recognition. This is US.
**They:** an enterprise security architecture for task-scoped agents. Six components + five principles.
**We already have — the mapping is almost one-to-one:**
- **"Human oversight is exceptional. Approvals are reserved for decisions that warrant them. An
  approval that is always granted is not a control; it is a ritual that trains people to ignore the
  one prompt that matters."** → This is LITERALLY the operator's standing directive (routing.md:
  "stop pinging me with bullshit", "just do it" = permanent permission; UAC-fatigue warning).
- **"Enforcement lives in the harness and the network, not the prompt. The prompt is where you
  express intent. It is never where you enforce a boundary."** → routing.md: "default to the
  architecture, NOT ad-hoc terminal commands"; "The prompt is not a perimeter" = our
  `operator-code-as-law-catalog` + enforcement-registry-design.
- **Agent Identity Broker** (short-lived task-scoped credential) → our queue dispatches each task
  with a budget tier (grok_rightsize/queue_rightsize).
- **Task-Scoped Access Engine** (capability ceiling per task, deny-by-default, templates) → our
  `cost_enforcer` + budget tiers + task-scoped queue.
- **Mediation Layer** (harness + network; independent fail-closed enforcement) → our `browser_env`
  allowlist (network) + queue/orchestrator (harness).
- **Trust Ratchet** (capability state only NARROWS during a task; hold protected data until
  restrictions active; fail closed) → our `browser_env` "residual stays local" + behavioral_analytics
  leak detection + cost_enforcer kill-on-spend.
- **Agent Activity Log** (append-only, source of truth, independent of model self-report) → our
  `ghost_ledger` (single source of truth for spend) + `memory_events` + `skill_ledger`.
- **Grant Review Loop** (evidence-based least-privilege review) → our `cost_learn` / `learn_rightsize`
  (review from captured evidence, adjust future templates).
**Context clue (real delta):** a **named Trust Ratchet** — we have all the pieces (allowlist, cost cap,
leak detection) but never formalized "capability state moves in one direction during a task, and only
a newly-authorized task can restore it." Naming it lets us enforce it deterministically + audit it.

### 5. Wallets / x402 — agentic payments (Account + Virtual wallets, guardrails)
**They:** humans delegate spend to agent "virtual wallets" with allowance + allow-list + max-tx-size;
caps give agents MORE freedom to explore; attribution via human-readable agent identity.
**We already have:** `cost_enforcer` (kill-on-spend-cap) + `ghost_ledger` + `grok_rightsize` budget
tiers + the free-tier-bulk-frontier-loop doctrine (explore autonomously within cost bounds).
**Context clue (real delta):** a formal per-agent **budget envelope** (allowance/allow-list/max) that
is delegated, not re-asked — we cap spend but don't frame it as a delegatable, guardrailed envelope.

### 6. AEO / Agent Readiness — agents are the new audience
**They:** >half of web requests now come from machines; are you readable/discoverable/recommended by
agents? Diagnostics scans the way an agent reads (robots.txt, sitemap, markdown, headers).
**We already have:** we build surfaces FOR agents end-to-end; `corpus_expand` harvests readable text;
`context_compression` optimizes token cost.
**Context clue (real delta):** the OUTWARD lens — "are we discoverable/recommended by the frontier
agents?" We build inward; AEO is the external visibility audit we don't have (and may not want).

### 7. Markdown for Agents / readable-first
**They:** serve clean machine-readable content; every human-only HTML tag is wasted tokens.
**We already have:** `context_compression`, `corpus_expand`, `skill_drop.right_size`, and the
readable-first ladder from the Kitesurf steal.
**Context clue:** none new — confirms the readable-first ladder. Already adopted.

## The unified insight ("minor context clues from idiots with a lot of money")
They formalized our raw doctrine into enterprise contracts. The four names/contracts actually worth
stealing (the real deltas):
1. **WebMCP** — expose our surfaces as MCP tools so ANY agent calls us (not just our seat).
2. **MCP v2 stateless** — speak the standard protocol over our existing stateless REST/queue.
3. **Trust Ratchet** — name + enforce "capability state only narrows during a task; only a new task
   restores it" as a first-class control.
4. **Budget envelope (wallets)** — per-agent delegated spend with allowance/allow-list/max, so
   autonomous exploration is bounded-but-free.

Everything else is recognition: we already run agent-first browsers, stateless-everywhere,
human-oversight-exceptional, enforcement-in-harness-not-prompt, activity-log-as-truth, and
cost-capped exploration. The outsiders added names; the operator had the doctrine.

## Folds
Filed to `memory/steal/`. Operationalized in `mag/ai_landscape.py` (ghost's AI-expert module: a
deterministic registry mapping emerging concepts → our modules, plus a `research()` intake that maps
any new announcement and emits the delta). Emit a memory_event + pro_library move so "ghost is an
expert on the AI landscape" becomes case law like "ponytail is an expert on code."
