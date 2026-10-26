# STEAL: HERMES-AGENT (Nous Research) — dossier v0 (2026-09-02)
*Operator word: "steal all of it." Source: C:\Users\foste\AppData\Local\hermes\hermes-agent
(git clone of github.com/NousResearch/Hermes-Agent, MIT, installed today 14:50Z,
5 Electron processes live, window "Hermes"). The steal law: take the bones, name
the reinterpretation, never call it copying. Deep mine queued to the scrum —
this dossier is the map.*

## WHAT IT IS (tri-state: Supported — read from source, not the website)
A self-improving agent framework: CLI (cli.py ~1MB, ~250 command modules),
gateway (Telegram/Discord/Slack/WhatsApp/Signal), desktop TUI, cron scheduler,
skills/plugins/toolsets, MCP both directions (mcp_serve.py + optional-mcps
catalog), ACP editor adapter, any-model providers (Nous Portal/OpenRouter/
OpenAI/own endpoint, `hermes model` switches), seven terminal backends (local/
Docker/SSH/Singularity/Modal/Daytona/Vercel — serverless hibernation "costs
nearly nothing when idle"), and a closed learning loop: agent-curated memory,
autonomous skill creation, FTS5 session search, Honcho user modeling.

## THE CONVERGENCE TABLE (their organ ↔ ours ↔ the shared law)
| Theirs | Ours | The law, rediscovered |
|---|---|---|
| drain_control: NO control channel into a running gateway — marker files only | steer_47 marker gate, dogfood_47.active, room adapter | files are the body |
| agent_cache_pressure: per-session cached agent reuses prompt prefix, bounded by bytes not entries | resident steered workers, byte-stable prefixes, ~90% cost cut | the cache is memory, not mind |
| hosted_rooms: append-only event log, "compose without a second transport queue" | event.v1 ONE stream, governor sole committer | one tape, many windows |
| kanban_swarm: planning root → parallel specialists → verifier → synthesizer, "no second scheduler", JSON-comment blackboard | one-builds-one-verifies, blackboard, respawn law | no duplicate supervisors |
| trajectory_compressor: protect first/last turns, compress middle to budget, "preserve training signal" | trajectory→RIB compiler, MAX_DISTILL, session mining | the tape is training data |
| moa (mixture-of-agents slash command) | the salon, the council | one question, N blind posts |
| learning loop: skills created from experience, self-improved in use | seed percolator, verb genomes | the seat writes its own genome |
| scale_to_zero + serverless backends | compute-never-idle, vast rehearsal | work flows or compute stops |
| model_cost_guard | honest cost ledger, covenant | unwatched meters are the only waste |
| SOUL.md + AGENTS.md + skills/ (agentskills.io) | openclaw workspace identity + skills | the prefix is the mod |

**Verdict: duplication-is-emphasis ACROSS ORGANIZATIONS.** Two civilizations,
same cathedral. Theirs is shipped/productized where ours is doctrine/organ —
that asymmetry is the steal.

## THE ADOPTION MAP
**Steal now (fits existing arc):**
1. **trajectory_compressor + batch_runner** — the training-data moonshot the
   operator named hours ago ("all our training data in one place") is BUILT
   here; steal the pipeline shape for our 66-session mine + Saleis corpus.
2. **agent_cache_pressure's byte/entry bounding** — harden our resident-worker
   prefix cache with their memory-pressure math before the scrum scales.
3. **kanban_swarm topology** (root→specialists→verifier→synthesizer, no second
   scheduler) — adopt as the scrum's task-graph shape; it IS our verifier law.
4. **FTS5 session search** — our session_transcripts are sqlite already; their
   search+summarize pattern upgrades the VS Code census gap.

**Adapt (drive surfaces — "drive it like the rest"):**
- CLI: `python hermes` shim → hermes_cli.main (gateway/cron/doctor subcommands)
- Identity injection: SOUL.md + AGENTS.md + skills/ — the DFHack prefix-mod,
  same as the cage; a Hermes seat speaks fleet memlang the same way
- .env + cli-config.yaml (113KB schema): point providers at GLM lanes
- cron/: native scheduler — candidate conductor for the scrum cadence
- gateway/: Telegram surface = the operator's phone door, no Cloudflare needed
- MCP bridge: it can SERVE MCP (mcp_serve.py) — join it to the mesh senses

**Skip (for now):** pets.py, skin_engine, sticker_cache, 15 SaaS optional-mcps,
billing/subscription organs — vendor scaffolding, not bones.

## DRIVE RECIPE v0 (first boot plan)
1. `hermes doctor` — health surface, same as the cage's PONG.
2. Provider lane: .env → one GLM free lane first (gopher body, $0).
3. Identity: drop fleet AGENTS.md + tiered-language block into its SOUL/AGENTS
   files; skills/ gets the verb genomes as its first skill pack.
4. First beat: one queued task via CLI; receipt filed here. NO seat status
   until it survives the blind-falsifier gate like everyone else.

## CUSTODY
- Recon receipts: this session, mag bus, 3 passes (inventory / hearts / README).
- Deep mine (250 modules, 1MB cli.py, 95KB AGENTS.md, docs/rfcs): queued to
  scrum wing-miner gophers — hermes wings join the 48.
- Upstream: MIT licensed; debt noted to Nous Research (the EUT/lattice debt
  already on the shelf grows by one castle).
