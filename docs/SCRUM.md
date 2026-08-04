# Scrum process — agents + operator (mycelial-republic)

**Purpose:** Plan and handle work so humans and agents share one board, one Definition of Done, and one anti-capture gate — without ceremony theater.

**Related:** `docs/AGILE_PLAN.md` (vision/epics) · `docs/AGENT_ROADMAP.md` (DAG/tickets) · `docs/MILESTONES.md` (evidence) · `docs/CONSTITUTION.md` (law)

---

## 1. Roles

| Role | Who | Does | Does not |
|------|-----|------|----------|
| **PO** | Operator (you) | Prioritize backlog, accept Done, waive gates in writing | Vanish and leave agents inventing epics |
| **KERNEL** | Grok / facilitator | Sprint synthesis, board hygiene, refuse illegal work | Claim R0 without evidence |
| **AGT_*** | Specialized agents | Pull tickets in role, update board, hand off | Cross roles without PO |
| **Mag / Hands** | local_sovereign_agent | Optional: execute `[mag]` / `[scrum]` chores only | Own product priority |

---

## 2. Artifacts (source of truth)

| Artifact | Path | Owner |
|----------|------|--------|
| Product backlog | `scrum/backlog.yaml` | PO + KERNEL |
| Active sprint | `scrum/sprints/current/` | KERNEL + agents |
| Sprint board | `scrum/sprints/current/board.md` | Anyone who pulls/moves |
| Standup log | `scrum/sprints/current/standup.md` | Each agent/human daily |
| Retro | `scrum/sprints/current/retro.md` | End of sprint |
| Waivers | `scrum/waivers/` | PO only |
| Agent handoffs | `scrum/handoffs/` | Agents |

**Rule:** If it isn’t on the board or in backlog, it isn’t planned work. Side quests go to backlog first.

---

## 3. Ticket shape

Every ticket has:

```yaml
id: W0.0          # stable id (roadmap W* or SCRUM-###)
title: short
epic: 1           # AGILE_PLAN epic number
status: backlog|ready|doing|review|done|blocked
role: PO|KERNEL|AGT_DATA|AGT_TRAIN|AGT_TEST|AGT_INST|AGT_SCAFF|AGT_DOCS|MAG
priority: P0|P1|P2
depends_on: []    # ticket ids
blocks_r0: true   # if true, empty data/raw may block
dod:              # extra checks beyond global DoD
  - "evidence path exists"
estimate: S|M|L
notes: |
  free text
```

Statuses move only forward unless **blocked** (then fix or re-backlog).

---

## 4. Ceremonies (agent-executable)

| Ceremony | Cadence | Command / action | Output |
|----------|---------|------------------|--------|
| **Sprint Planning** | Start of sprint | `mycelia scrum plan` or KERNEL + PO edit board | `board.md` filled from ready backlog; knot of sprint named |
| **Daily Standup** | Daily / per session | `mycelia scrum standup --who KERNEL --did "..." --doing "..." --block "..."` | Append `standup.md` |
| **Pull work** | Continuous | `mycelia scrum pull W0.1 --role AGT_DATA` | Ticket → doing; claim file |
| **Done / Review** | Continuous | `mycelia scrum done W0.1 --evidence path` | Ticket → review/done; milestones if gated |
| **Chord Review** | End of sprint or major W* | Human/Grok strike chord on deliverable | `logs/chord_strikes/` entry |
| **Retro** | End of sprint | `mycelia scrum retro` prompts + fill | `retro.md`; 1–3 process changes |

**Planning question (PO):** “What knot do we strike this sprint?”  
**Standup questions:** What did I finish? What am I pulling? What’s blocked?  
**Retro questions:** What loops appeared? What capture risk? What one process change?

---

## 5. Definition of Done (global)

A ticket is **done** only if:

1. **Evidence** path listed (file, log, command output) — not vibes  
2. **Role match** — work done under claimed role rules  
3. **Tests** — `pytest -q` green if code touched  
4. **Gates** — if `blocks_r0` / train-related: `data/raw` or PO waiver in `scrum/waivers/`  
5. **Capture check** — no new rank/token/core-mirror; Saelis not sold as operator identity  
6. **Handoff** — if multi-agent: `scrum/handoffs/<id>.md` or handoff.v1 satisfied  
7. **Chord (major only)** — W0.8, R0, R1, constitution changes: entry under `logs/chord_strikes/`  

Minor docs/typos: skip full chord; still need evidence.

---

## 6. Standing agent gates (from AGENT_ROADMAP)

```
IF data/raw empty AND ticket not docs/W0.0/W0.4/instrument-only:
  status → blocked  reason: BLOCKED_W0.0

IF train claims operator mirror on Saelis_* primary:
  FAIL

IF mark R0 without W0.8 evidence:
  FAIL

IF invent token_balance|mirror_rank|admin_tier|core_operator:
  FAIL
```

---

## 7. Sprint length & capacity

- **Default sprint:** 7 days (or until knot resolved + retro)  
- **WIP limit:** 2 tickets in `doing` per role (KERNEL may hold 3 synthesis tasks)  
- **P0 only** may break WIP with PO note  

---

## 8. How agents start a session

1. `mycelia scrum status`  
2. Read `scrum/sprints/current/board.md`  
3. `standup` one line  
4. `pull` one ready ticket matching your role  
5. Work; update notes  
6. `done` with evidence **or** leave `blocked` with reason  
7. Handoff if next role needed  

KERNEL/Grok: prefer unblocking W0.0 and board hygiene over new epics.

---

## 9. Mag / local agent bridge

In `local_sovereign_agent/queue/todo.md`:

```markdown
- [ ] [mag] [scrum] run mycelia scrum status and append standup for MAG
```

Mag must not invent backlog items. Only execute tickets already `ready`/`doing` tagged for MAG.

---

## 10. Anti-patterns (refuse)

- Sprint as infinite feature list while `data/raw` empty  
- “Done” without evidence path  
- Parallel train + network + tokens before R0  
- Board diverging from `MILESTONES.md` (KERNEL syncs)  
- Ceremony notes that replace actual moves  

---

*Process is architecture. Keep it light enough to run every session.*
