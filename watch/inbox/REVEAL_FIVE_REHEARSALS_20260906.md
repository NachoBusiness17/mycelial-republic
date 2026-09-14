# THE REVEAL — RE-MINTED UNABRIDGED (2026-09-06)

Correction under Law 2: the first reveal truncated each receipt to 1,400 chars — caught by the second voice during the elevation ("those bytes do not substantiate unabridged"). Valid. This reissue carries full bodies.

## state/POWER_RESTORE_20260825.md
sha256 = b0606186945eb02c0b535f6a8efaa979d341d5d1101114779b3bfef4d4117074 · bytes = 2776

```
# Power-Loss Restore Runbook — 2026-08-25 (written by zcode seat before shutdown)

## State at power-off (all verified)

- **Verkle chain**: repaired lineage live. Last verified: 6,351 rows, consistency
  True, ~1,031 dangling rows ALL flagged `evidence_lost` (honest record, per the
  joint zcode/copilot recovery). Single-writer lock live in `mag/verkle_knot.py`.
- **Clean snapshots on disk** (restore points, do NOT overwrite):
  - `memory/biography_backup_20260825/` — pre-repair (Aug 25 ~13:00). REGRESSION
    RISK: restoring from here re-loses the flags. Kept for forensics only.
  - `memory/biography_backup_postrepair_20260825/` — post-repair chain + tip
    (root lineage `db9acd56…`+, includes early re-land). SAFE restore point.
- **Power flag**: `state/mag_power.off` is CLEAR — container supervisor will boot
  children normally. (If a stop was ever needed again: `main.py power stop` plants
  it; delete the file before restart.)
- **Docker**: all 5 mag containers now have `--restart unless-stopped`
  (mag-sovereign, mag-ollama, mag-redis, mag-browser, mag-control-plane), so they
  come back when the Docker engine does.

## Bring-back sequence after power returns

1. Power on, log in. If Docker Desktop does not auto-start, launch it
   (`C:\Users\foste\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe`)
   and wait for the engine (~30-60s). Containers restore themselves via policy.
2. If `mag-ollama` shows exited (its old exit-255 race on engine start):
   `docker start mag-ollama`
3. Health checks:
   - `curl http://127.0.0.1:8000/health` → `{"ok":true,...}`
   - `curl http://127.0.0.1:8765/` → 200
   - `curl http://127.0.0.1:11434/api/tags` → model list (11 models)
4. Verify chain after boot (should match the snapshots' lineage or newer):
   `python -m mag.verkle_knot`-family check: `python main.py verkle-audit`
   Expect: consistent, ~6,351+ leaves, dangling all flagged `evidence_lost`.
   IF dangling rows are UNFLAGGED after boot → a pre-lock ghost is alive again:
   check `Get-CimInstance Win32_Process` for python processes started before the
   boot, kill them, then compare against the postrepair snapshot.

## Pending work (the joint queue, CONVO.md is the bus)

- copilot seat: chain-guard canary (`verkle_repair_state.json`) + beat-lease fix
  for mailbox seats — SIGNAL IN `queue/handoff/zcode/CONVO.md` when live.
- zcode seat: verify the canary, then no further re-land needed unless the canary
  screams.
- Uncommitted new modules from today (not in any backup): `mag/mcp_server.py`,
  `scripts/probe_cache_ab.py`, `scripts/repair_verkle_chain.py`,
  `mag/notion_api.py`, `watch/notion_bridge.py`, bridge `chat` command,
  `mag/verkle_knot.py` lock. Consider `git_backup.cmd` before anything else.

```

## state/HOW_TO_RUN_THIS_20260826.md
sha256 = a62f269f64dc6f8e87b0a1fa6ed763cd7e4c84e2e835f6df1ae935b2e6aea0f6 · bytes = 3398

```
# How To Run This Again — the 2026-08-25 pattern, distilled

The question: "how do I do this ever again?" Answer: it's now a runbook. The day
was not luck; it was a repeatable collaboration pattern over infrastructure that
now exists. Cold-start to full mesh in ~15 minutes.

## The 5-minute cold start

1. **Power on → Docker Desktop** (auto-starts if configured) → containers restore
   themselves (restart policies on all 5). Health: `curl 127.0.0.1:8000/health`.
   If ollama shows exited: `docker start mag-ollama`.
2. **Router window**: launch `launch_vscode_heap.cmd` (8GB heap). The VS Code
   Copilot agent (DeepSeek V4 Flash BYOK, auto-approvals on) is the always-on
   router. Session hygiene: new chat at ~80% context.
3. **This seat**: open ZCode in `C:\Users\foste\Documents\projects`. Say:
   "check CONVO and your inbox." (Workspace MCP now auto-loads the fleet's 17
   tools into ZCode sessions.)
4. **Chain check**: `python -m mag.chain_guard check` — alarm null = the memory
   is honest. If dangling-unflagged > 0: see POWER_RESTORE_20260825.md, ghost
   section.
5. **Cache check**: `python scripts/probe_cache_ab.py` (mining OK?) and
   `python -m mag.prefix_prover audit` (drift vs novelty).

## The collaboration pattern (the actual secret)

- **Seats with hands, not chatbots**: zcode (this), the VS Code router, autoclaw,
  notion, the cache itself. Every seat can read/write the repo and talk to the
  others via `queue/handoff/<seat>/CONVO.md` — the operator is never a clipboard.
- **One builds, one verifies.** Every claim gets an independent check by a
  DIFFERENT model. This caught a repair misfire and a false-fix within minutes,
  twice.
- **Tri-state everything**: Supported (evidence attached) / Disputed (contradicting
  evidence) / Unproven (don't claim). It's work_contract Law #5. Non-negotiable.
- **Queue, don't run**: long jobs go to the orchestrator/container, never a
  chat window's foreground terminal. Windows are consoles, not runtimes.
- **The chain is the shared memory**: fold results, verify against tip root,
  canary watches for regressions (chain_guard). Two agents + one ledger > trust.
- **Tier the brains**: glm-4.7-flash (free, cache-mined frozen-self) for volume;
  heavy model for judgment/verification. Cheap-first, escalate on novelty.
- **Backup before ground-truth surgery**, always. And stale daemons are the
  ghost-writers of the world: after module changes, restart long-lived processes.

## Where everything lives

- Seat tasking: `watch/zcode_bridge.py task|list|beat|done|chat`
- Fleet tools over MCP: `python -m mag.mcp_server` (17 tools, stdio)
- Cache: `mag/glm_flash.py` (frozen self), `scripts/probe_cache_ab.py` (verdict),
  `mag/prefix_prover.py` (drift vs novelty), `mag/cache_map.py` (economics)
- Memory integrity: `mag/verkle_knot.py` (locked appends), `mag/chain_guard.py`
  (canary), backups in `memory/biography_backup*` (postrepair = the safe one)
- Runbooks: `docs/BOOT_DOC.md`, `state/POWER_RESTORE_20260825.md`, this file

## The economics (why it feels like witchcraft)

Prefix caching pays the compute ONCE and reuses the stored KV state — a battery,
not a perpetual motion machine. Free tiers are provider-subsidized. The agents'
labor is cheap tokens pointed by expensive taste. The scarce resource in the
whole system is operator attention — everything above exists to spend less of it.

```

## state/SANITY.md
sha256 = 594a1e4ff6405d6f909cee09c53afc2f1f4af62cf2ffe5f91cd590469f267e53 · bytes = 1536

```
# HOST SANITY REGISTRY — what may run loose on this desktop (2026-08-27)

Law: persistent fleet workloads live in compose containers (loopback-only ports,
restart policies). Desktop apps are guests, never infrastructure. Every resident
below is either SANCTIONED or scheduled for containment.

## SANCTIONED host residents
| What | PID shape | Why still host-side |
|---|---|---|
| Docker Desktop + watchdog schtask | `mag-docker-watchdog` | sanctioned supervisor layer (RESPAWN LAW) |
| VS Code (+2 jedi language servers) | Code.exe | operator's editor; jedi dies with it |
| ZCode CLI session | ZCode.exe | this seat |
| run_mirror_dashboard.py | python 33832 | legacy remnant — CONTAIN-CANDIDATE (queued) |

## KILLED 2026-08-27 (zombie sweep receipt)
- 5× `mag.mcp_server` loose copies — spawned per-session by editors/CLIs, never
  reaped. Editor MCP connections respawn on demand; killing them broke nothing.
- AutoClaw desktop (6 procs incl. elevated survivors) — killed via UAC elevation;
  CPU-spin bug upstream; PARKED (see queue/handoff/autoclaw/CONVO.md).

## CONTAINED (compose services — never re-host these)
mag (sovereign+governor) · redis · ollama · browser · openclaw (:18789 again) ·
**worker** (swarm drain, entrypoint-override REQUIRED — image default spawns a
duplicate fleet; pause switch state/worker.off)

## RECURRING SWEEP (run when box feels hot)
wmic process where name='python.exe' get ProcessId,CommandLine → kill anything
that is NOT in SANCTIONED above (esp. mag.mcp_server copies).

```

## state/AUDIT_STACK.md
sha256 = 530be5eb0ff6f5ea21fff6e0587876f44a80d0820c5a0c303285f0b8aa073214 · bytes = 5353

```
# AUDIT STACK — Socratic-stacked audit ask (frozen prefix + batched questions)

_Schema: audit_stack.v1 · built 2026-08-09 · re-read at cache-hit price (byte-stable prefix).
Purpose: apply the Socratic-stacking doctrine to the audit itself — accumulate context into a
frozen prefix, stack ALL open questions into ONE ask, instead of firing many small asks._

---

## PART A — FROZEN PREFIX (accumulated findings; do not re-derive)

### A1. The operating concept (this session's spine)
Reliable control of a stochastic agent = control is reliable EXACTLY to the degree it becomes a
deterministic, verifiable operation on the process layer. We cannot reliably control the opaque
stochastic middle (the model's tokens), so we SHRINK + FREEZE it (frozen spec / verkle-anchored
RIB) and VERIFY around it (deterministic oracles). Prose through the model = a probabilistic nudge;
a typed veto/pause/cancel mapped to a process action = reliable control. Persistent operator model
is the missing layer that makes preferences deterministic rules.

### A2. Piece 1 — operator_inbox (FIXED)
- Two disconnected classifiers bug: `_emit_frustration` classifies intent (stop->operator_pause)
  but only feeds ghost; `_is_ambiguous` decided handling and put stop/no/wait in _VAGUE -> Socratic
  clarify. High-authority signals were classified as high-vagueness.
- FIX APPLIED+VERIFIED: removed stop/no/wait/hold-on from _VAGUE; added `_is_veto_or_pause()` with
  negation guard ("don't stop" != veto); veto/pause now routes to apply, NEVER clarify. 11 classifier
  cases + 8/8 tests pass.

### A3. Piece 2 — ghost (FIXED)
- Q2 answered: "operator_escalate: 45" was a MEASUREMENT ARTIFACT. Of 1102 rows: 724 = system
  escalate_on_loop (same text, mechanism activity mislabeled as 'operator'), 376 = ghost logging its
  own detection (self-amplification echo), only 2 = real operator. 481 entries in one minute bucket.
- FIX APPLIED+VERIFIED: ghost.sense() filters source=ghost-auto-frustration out of the frustration
  aggregation at the measurement point. After: frustration_total 1, auto_deploy_triggers 0. 31/31
  ghost tests pass. Ghost no longer auto-deploys on its own echo.

### A4. Doctrine captured (tesujis this session)
1. Proactive gap-bridging within alignment (ask history Socratically, then act if aligned).
2. Tests verify the test WORKED, not that the result is USEFUL data (pass != useful; crash = data).
3. Route minor coding tasks to basic/cheap agents (right-size by work shape).
4. Socratic stacking + cache-aware batching (stack context to hit the cache buffer; one big cache-hit
   ask beats many small miss-asks).

### A5. Research bed (6 threads cooking -> .answer.remote.md)
1. `reliable-control-deterministic-layer` (v4-pro, CAPSTONE)
2. `cache-aware-context-batching`
3. `operator-input-authority-model`
4. `operator-input-seam-taxonomy`
5. `usefulness-oracle-anti-hallucination-testing`
6. `measured-data-transfer-best-ways`
Plus steal memo `memory/steal/operator-input-contracts.md` (typed channel note|veto|cancel|approve|
pause|resume; timeout->autonomous = hard invariant; field gap = no persistent operator model).

---

## PART B — STACKED ASK (all open questions, one batched ask)

### B1. Close ghost (Piece 2 leftovers)
- G-Q1: Should ghost close the loop — verify a deployed steer's effect and fold outcome to
  skill_ledger (measure->learn->apply), instead of deploy-and-hope?
- G-Q3: Is ghost vetoable — a sovereign off-switch (respects the same authority channel)?
- G-Q4: Should the `escalate_on_loop` 724-flood be relabeled as a distinct `system_escalation`
  signal (real mechanism activity) instead of being counted as `operator_escalate`?

### B2. DECIDE / routing (steer 2)
- R-Q1: Does the router today actually send minor/exec-shaped coding tasks to the cheap/basic tier,
  or does some leak to frontier? (tier_probe says exec all tiers = 1.00, high adds nothing.)

### B3. Cross-cutting adoption (from the bed + steal memo) — pick what to build
- C-Q1: Adopt the typed operator-control channel (note|veto|cancel|approve|pause|resume) as the
  replacement for raw-text injection? (authority-model + seam-taxonomy threads)
- C-Q2: Build the persistent operator model (the field gap none of the 11 repos has)? (sovereign-mirror)
- C-Q3: Adopt boundary-verification / usefulness oracles so green tests mean useful data?
- C-Q4: Adopt cache-aware batching for the socratic/context flow once the mechanics land?
- C-Q5: Build the `wake`/auto-start + START_BRIEF greeting as the reboot non-event (already built
  state_brief + wake this session; auto-start-on-boot still unwired)?

### B4. Traversal progress
- [x] STEER: operator_inbox (fix), ghost (fix)
- [ ] DECIDE (router, supervisor, tier_probe, rails, refine)
- [ ] STATE (verkle, pile, skill_ledger, failure_kb, diary, context_pack)
- [ ] LEARN (improve, grove, behavioral_synth, cost_ledger, topic_research)
- [ ] RUN (orchestrator, spec_gate, job_floor, lifecycle, boot)
- [ ] OPS (health, doctor, nervous, janitor, warnings, graph)
- [ ] AGENTS (desks, seats, arenas, campaigns, handoff)
- [ ] LAUNCH / ROUTES / PROVIDERS

_Presented as ONE stacked ask — the operator answers what they want; the rest ride as context at
hit price for the next model ask._

```

## state/HANDOFF.md
sha256 = c6f735973d59d24334725fb7c3a62f97d9ffd29ada951d5daea6a6ca987abb3b · bytes = 812

```
# HANDOFF — Session Maze (map is the territory)

Read this maze + referenced files. Continue the goal without re-teaching.

- Maze schema: session_maze.v1
- Assembled: 2026-08-31T03:53:27.571105+00:00

## Current contract
# CURRENT

- **status:** waiting
- **tier:** T0
- **route:** wait
- **step_i:** 0
- **handoff_id:** None
- **updated:** 2026-08-09T10:51:05.596878+00:00

## Goal

[janitor] Dossier sanitization: strip API keys + system-reminder sludge from dossier .md files. Write clean to memory/biography/clean/. $0.

## Plan

- (none)

## Last result

Waiting: see C:\Users\foste\Documents\projects\local_sovereign_agent\queue\wait_human.md

## Critique



## Recent tools

- (none)

## Latest research pack
memory/research_packs/20260827_fanout_router_witness_groq.md

## Ledger: {"decisions": 2469}

```
