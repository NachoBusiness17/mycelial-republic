# RESEARCH PROJECT — LANE ARCHITECTURE: per-lane agents on MCP wiring (2026-09-04)

**Operator thesis (verbatim):** "i just gave you a shitload of mcp servers. i think that's
the key i can smell it. now i have each lane built. Each one needs its own agent and
logic/automations you control/set remotely you are the manager of all of them you browse
them like we did the x surface of pro. it's the same thing."

**Inputs:** full corpus brief (watch/SALON_BRIEF_SETUP_20260904.md — doctrine/current/open,
three parts) · salon `salon_lane_architecture_20260904` — groq, cerebras, deepseek-pro
substantive; together honest-down (reasoning budget). Operator's lane board: Day Work ·
Builder · Bard/Ledger · Elder · Research · Android Surface · Economist (+ Day-work
scheduler firing live).

## THE PER-LANE AGENT CONTRACT (3-witness convergence, 8 clauses)

1. **IDENTITY — a lane manifest** (`queue/lanes/<name>/manifest.md`): purpose, current
   arc, laws, MCP whitelist, kill-switch location. Read at spawn, NEVER at runtime
   (deepseek-pro). The AGENTS.md pattern, applied per lane.
2. **INBOX — one file** (`queue/lanes/<name>/inbox.jsonl`): manager writes compact
   handoffs `{where, why, ttl, anchor}` — pointers, never attachments. Agent polls.
3. **SURFACE — one read-only output file** (`queue/lanes/<name>/surface.md`): the lane's
   digest/log. THE MANAGER BROWSES SURFACES, NOT CONTEXTS (the X-deck pattern inward;
   day_work_digest.md is lane 1's surface, already live).
4. **AUTOMATIONS LIVE IN ONE SCHEDULER ORGAN, not per-lane timers** — "no lane agent
   runs its own timer" (deepseek-pro clause 4). The 30-min scheduler diffs every lane
   surface and answers. This kills the zombie-heartbeat class ARCHITECTURALLY (the tick
   was a lane agent with its own premium timer).
5. **MCP SUBSET WHITELIST** — each lane may call only its manifest's servers. MODEL-PIN
   ISOLATION applied to tools; no lane inherits another's premium surface.
6. **TRI-STATE RECEIPTS** — every action appends a typed row; no receipt = never
   happened (coverage thesis, wire verb).
7. **KILL-SWITCH** — one word per lane in the GO menu (`KILL BUILDER`); flush, write
   KILLED receipt, exit. The tick-kill pattern applied preemptively.
8. **BUDGET GUARDS** — rolling OUTPUT-RATIO (<0.01/24h self-suspends) + CONTEXT-DEBT
   cap (re-feed ≤ 3× useful output). Enforced in receipts, measured nightly from the
   usage db (the meter that was always on disk).

## MCP WIRING MAP (deepseek-pro base, 3-witness concur on principle)

| Lane | MCP servers | Rationale |
|---|---|---|
| Day Work | mag (run_python/shell/blackboard) + web_reader | digest lane: files in, digests out |
| Builder | mag (run_python/shell) + github | the repo is its surface; no browser, no vision |
| Bard/Ledger | mag blackboard + cloudbase | writes state, not prose; ledger/canon substrate |
| Elder | mag research-swarm + web_reader + image_search | reads, synthesizes — never clicks |
| Research | mag research + browser-use + node_repl | the ONLY lane that clicks |
| Android Surface | android-emulator (23 tools) + computer-use + vision | embodied lane; AX-first law enforced |
| Economist | mag run_python + mimosa | reads usage db/prices claims; security-stamps |

**Rule the map encodes:** least-privilege per lane; exactly one lane holds the browser,
one holds the phone — actuation surfaces are singleton, judgment is pooled.

## THE MANAGER SURFACE (how one seat browses seven lanes)

Per-lane surfaces mirrored to `/static/lanes/` + one browse board `lanes.html` — the
deck pattern inward: lane cards (state, last receipt, burn, kill word), the operator
reads state and fires one-word GOs, the manager seat does the same from files. Manager
never opens 7 chat contexts; it reads 7 files and writes inboxes.

## WHAT BREAKS FIRST (witnesses concur, from our own laws)
1. **Manager context debt** — browsing 7 lanes inside one conversation re-feeds 7
   contexts (the Lite verdict at fleet scale). Fix: manager reads SURFACES only.
2. **Heartbeat multiplication** — 7 lane timers = 7 zombie candidates. Fix: clause 4
   (one scheduler organ).
3. **Cross-lane premium inheritance** — a builder spawn inheriting a premium pin. Fix:
   clause 5 (whitelists) + flash pins on all lane agents.

## BUILD ORDER (prove on lit lanes first)
1. **Day Work lane — ALREADY LIT** (scheduler + digest + daytool = the reference
   implementation of the whole contract). ✅
2. **Economist lane next** — smallest scope (read the usage db nightly, one SELECT,
   tri-state stamp) and it ENFORCES clause 8 for all other lanes. The meter guards
   the meters.
3. **Builder lane third** — after the throttle organ exists (Launch Law coupling).
Then Bard/Ledger, Elder, Research, Android Surface (rig already live as its body).

## TRI-STATE
Contract convergence: **Supported** (3/3 substantive witnesses citing corpus; receipts in
memory/runs/lane_salon). MCP map specifics: **Supported as design, Unproven as wiring**
(no lane agent spawned under a whitelist yet). Build order: **Supported** (day-work lane
empirically proves clauses 1-4,7 already). Blind spot (each witness's #6): no lane agent
has been KILLED yet — the kill-switch path is designed, never fired (the claim-organ
lesson: harnesses must test the takeover/death path FIRST).

## BUILT THIS TURN (the first physical increment)
- `queue/lanes/<name>/manifest.md + inbox.jsonl + surface.md` for all 7 lanes (the
  constitution files; Day Work manifest documents what already runs).
- `dashboard/static/lanes.html` — the manager browse board + mirrors.
- This card = the research project's charter. Economist lane agent arming = next gate
  (one cron, flash-pinned, nightly usage-db sweep — the OUTPUT-RATIO law made an organ).

*Folded by the zcode seat (Max) as manager-designate; salon witnessed; operator rules.*
