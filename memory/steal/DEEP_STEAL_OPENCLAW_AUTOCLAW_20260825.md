# DEEP STEAL — OpenClaw/AutoClaw architecture + the free-cache default (2026-08-25)

**Commitment:** `deep-steal-openclaw-autoclaw-001`
**Operator:** "it has fucking subagents plugins mcp servers kills commands and hooks zcode is
awesome you need to be using it ... use it/steal what is best. also couldn't we be using their
cached models instead of deepseek for basically free operation ... next steps please and ingest
everything we need to utilize our licenses best."
**Research:** subagent report on github.com/openclaw/openclaw + docs.openclaw.ai + docs.z.ai
devpack (memory-mechanism.md) + autoclaw.z.ai changelog. Grounded, with honest "could not
verify" notes.

## What OpenClaw is (grounded)
MIT TypeScript monorepo (~387k stars), a personal AI assistant: local Gateway control plane +
agents + channels (WhatsApp/Telegram/Discord/etc.) + pluggable providers (incl. z.ai/GLM).
AutoClaw = desktop wrapper on the OpenClaw kernel v6.8. Config/state: `~/.openclaw/` (openclaw.json,
workspace/, agents/<id>/agent/*.sqlite sessions+memory, state/openclaw.sqlite, hooks/, skills/).

## The verdict (honest)
Our infrastructure is STRONGER: verkle chain > their plain SQLite memory; k8s swarm > their
single-machine Gateway; we already have a bus, subagent routing, MCP-ish surfaces, harnesses.
STEAL CONTRACTS, NOT TOPOLOGY. (Their cloud placement is literally on their roadmap.)

## What's worth stealing (ranked)
1. **Push-based completion + durable delivery + blocked-retention ledger.** Subagents complete
   via announce with idempotency keys, 30-min retry/backoff, a `blocked` terminal state retained
   7 days, recoverable via `tasks retry|dismiss`; restart recovery with tombstones. Solves lost
   child results on restart/flaky delivery. (We lose results on restart — this is the fix.)
2. **Automations scheduler shape**: `on-exit` + `stream` schedule kinds, condition-trigger
   scripts with persisted 16KB state (fire:true dedup on state change), dynamic pacing via
   in-run `next_check`, per-job `--model/--fallbacks/--thinking/--tools`, webhook ingress
   (`POST /hooks/agent`) with strict SSRF guard. A full cron+watchers+external-trigger plane.
3. **Task ledger as records-not-schedulers** with a `lost` state + runtime-aware reconciliation
   (does the backing run exist?) + a 60s sweeper. Cheap, high robustness value.
4. **Typed hook decision semantics**: `before_tool_call` returning {block | params-rewrite |
   requireApproval}, priorities, fail-closed timeouts, `before_agent_finalize` bounded revise.
   Our bus is event-fire; this is policy-with-guardrails.
5. **Two-way MCP**: serve OUR tool catalog as an MCP server (openclaw mcp serve / openclaw-tools
   stdio) so other agents consume the sovereign surface. We consume; start emitting.
6. **Manifest-declared plugin contracts** (openclaw.plugin.json contracts.*): everything a
   plugin registers is pre-declared — kills zombie registrations, ownership auditable.
7. **Skill gating + workshop loop**: requires.bins/env/config eligibility, per-agent allowlists,
   `/learn` drafts a skill from conversation with evaluator hooks. Folds into our rib/self-steal
   machinery as automated skills-authoring.
8. **z.ai memory doctrine** (devpack memory-mechanism.md): SEPARATE instruction memory (stable,
   human-written, CLAUDE.md-style) from learning memory (accumulated auto-memory); per-subagent
   scopes; load-by-path rules; main file <200 lines. Maps onto our standing-vs-experience split.

## The trap (avoid)
OpenClaw is a single-operator local Gateway — not a multi-tenant boundary. Don't copy the
topology; copy the contracts.

## Headless surface (the "use it" path)
- CLI install: `npm install -g openclaw@latest` (PowerShell installer: iwr -useb
  https://openclaw.ai/install.ps1 | iex). State: ~/.openclaw/.
- `openclaw agent exec "task" [--cwd --model --fallback --config --isolated --auth-env-only
  --timeout --json]` — one embedded agent turn, NO Gateway needed, exit 0/1/2, stable JSON
  envelope (final, usage, costUsd, toolSummary). The `claude -p` equivalent.
- `openclaw agent --agent ops --message "..."` through a running Gateway.
- Docker/K8s/Nix/Podman deploys documented — containerizable headless agent.

## THE FREE-CACHE DEFAULT (the economic half)
Operator's idea: use z.ai's free cached model (GLM-4.7-Flash — FREE at ALL tiers) as the DEFAULT
for heavy agentic conversations instead of DeepSeek ~30c/hr, with pre-cached prompts.
- Built: mag/glm_flash.py — cached_chat(task): FROZEN SELF (work_contract.BRIEF + standing
  doctrine, byte-identical) + dynamic tail → cache-mined, cost $0, returns cached_tokens.
- providers.yaml prefer_order already puts free lanes (incl. z_ai) BEFORE paid deepseek; the
  paid fallback only fires when free lanes are empty. Heavy windows should route to flash now.
- GLM-4.7-Flash: 200K ctx, 128K out — big enough for heavy agentic windows.

## Docker (be smart)
- The coder lane (harness/glm_coder.py) + the OpenClaw headless surface are containerizable
  (OpenClaw documents Docker/K8s deploys). Target: run them in the existing k8s swarm image so
  the coding lane + agentic exec run headless in-cluster on the same infra as the drains.

## Next steps (ordered)
1. THIS steal + mag/glm_flash.py (the free default engine) — DONE this turn.
2. Wire glm_flash.cached_chat as the default cheap call for heavy agentic windows (seats/drills
   that currently fall to deepseek); keep deepseek only for genuine cold-start quality needs.
3. OpenClaw: confirm `openclaw agent exec` works headless with z_ai/GLM; wire harness/openclaw.py
   mirroring glm_coder.py; route agentic busywork through it.
4. Adopt the TOP 3 stolen contracts where they hurt most: push-based completion w/ blocked
   ledger (swarm results), lost-state task reconciliation, typed before_tool_call guardrails.
5. Two-way MCP: serve our tool catalog (mag modules → MCP server) so OpenClaw/AutoClaw consume us.
6. Docker: containerize glm_coder + openclaw exec into the swarm image; run in-cluster.

## Refuse
- Copying OpenClaw's single-machine topology into our k8s world.
- Letting a heavy Gateway daemon compete with the machine's CPU ceiling for no gain.
- Paying DeepSeek for heavy windows when flash + cache gives $0 with the frozen self.

## Fold with
deep-steal-free-cache-self-20260824, deep-research-zai-offerings-20260824,
glm-coding-lite-evaluated-20260824, cache-extract-joint, autonomous-loop, swarm invariants,
rib/self-steal machinery.
