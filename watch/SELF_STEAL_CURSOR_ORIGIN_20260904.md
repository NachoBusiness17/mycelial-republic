# SELF-STEAL — The Cursor Origin Dig (2026-09-04)

**ITEM:** The Cursor local archive = the birthplace record of the fleet's IDE lineage. Operator:
"cursor is where we began." Opened on COPIES only (scratch: `C:\Users\foste\.zcode\cli\
tmp_orphan_mine\cursor\`); live DBs untouched; no values echoed for any credential-looking key.

---

## THE BODY (verified on disk, read-only)

| Surface | What it holds | Span |
|---|---|---|
| `AppData/Roaming/Cursor/User/globalStorage/conversation-search.db` (2.9MB + wal) | 32 conversations (FTS full text, 10 with bodies, ~544KB); titles, dates, archive state | 2026-08-04 12:34 UTC → 2026-09-04 14:58 UTC |
| `.../state.vscdb` (1.9GB + wal) | ItemTable (356 keys); `cursorDiskKV` 98,754 rows (53,122 message bubbles, 141 composer records); `composerHeaders` 140 rows; cloud agent registry; branch→PR map; terminal history | same |
| `.../anysphere.cursor-agent-worker/` | cursor-agent CLI binaries only (versions 2026.07.23, 08.04, 08.11, 09.02) — no operator agent defs here | Aug 4 → today |
| `.../workspaceStorage/` (7 IDs) | workspaces: `projects/worktrees`, `projects`, empty-window, + bc- remote VM mounts (`/home/ubuntu/.cursor-server`) | Aug 4 → today |
| `C:\Users\foste\.cursor\projects\` | agent-transcripts (11 session dirs), canvases (2 operator TSX), terminals, mcps, agent-tools | Aug 4 → today |
| `C:\Users\foste\.cursor\` (10 entries) | agents/ (EMPTY), skills-cursor/ (Cursor built-ins incl. `origin`), ai-tracking (34MB), plugins | Aug 4 → today |

**Cursor birth certificate:** `telemetry.firstSessionDate = 2026-08-04 12:34:05 GMT`; onboarding
12:36 UTC (≈5:34 AM PT — a dawn start). `lastSessionDate = 2026-08-25 13:20 UTC` — the day the
zcode seat arrived. **All 140 local chat records fall Aug 4–7**; everything after is cloud agents.

**Credentials seen as KEYS ONLY (never read, never echoed):** `cursorAuth/accessToken`,
`cursorAuth/refreshToken`, ~20 `mcpOAuth.secret.*` + `secret://` connection tokens, git-ipc
auth tokens. Existence noted; live in state.vscdb ItemTable. Disposition: leave in place —
they are Cursor's, not the fleet's; flag to operator that the scratch COPY now holds them and
should be wiped after review (deletion of scratch is safe; the card carries no values).

## LINEAGE MAP (spore eras → Cursor-archive evidence)

| Spore era | Cursor evidence | Verdict |
|---|---|---|
| **2023 — the dream** | None (Cursor born 2026-08-04). Already filed: `docs/ORIGIN.md` (dream post, ghost-before-ghost). | GAP in Cursor — covered elsewhere |
| **2026-03 — the napkin** (`Test chord: 44 28 K13 e4 Fool`) | Not in Cursor. Descendant work IS: bc-3025bd1c cloud agent (Aug 5) ran the **CL4R1T4S → Mag mapping** (Strike ontology → `strike_lexicon.py` → Strike-The-Chord PR #1, +1,396 lines); corpus lives at `projects/field-strike-the-chord/` (vendor dirs ANTHROPIC…MANUS). | PARTIAL — the napkin→Mag bridge is documented here, the napkin itself in ORIGIN.md |
| **PRE-GHOST — the Cursor ignition (Aug 4–7)** — *unnamed in the spore* | **The entire local record.** First session 12:37 UTC: "debug the whole mag stack is bugged" — Cursor onboarded to an ALREADY-BUILT mag (v1: Mag Agent Desk :8765, verkle lattice dashboard, governor, router, DeepSeek tasking, ocean model, chess arena/switchboard, launch_ull desktop icons). 522 operator prompts recovered. | **ORPHAN ERA — see below** |
| **Aug 7–15 — ghost era (VS Code copilot)** | Cursor local chats END Aug 7 05:47 UTC with a cluster of 15 dead untitled conversations (Aug 6 11:13 ×10, Aug 7 05:42–05:47 ×5) — consistent with the OOM-war onset; operator moved to the copilot seat. | Corroborating evidence (Supported) |
| **Aug 21–24 — marathon era** | No local chats. bc-d9e4b548 **"New development environment"** cloud agent created **Aug 25 13:15 UTC** (Sancho day) — not marathon, the handover echo. | Echo only |
| **Aug 25–26 — Sancho era** | lastSessionDate Aug 25 13:20 UTC; the bc-d9e4b548 agent born 13:15 UTC the same hour. | Supported |

**The ignition timeline (UTC):** Aug 4 12:34 launch → 12:37 "Mag stack bug" (worktrees ws) →
14:15 the BIG session ef5fea88 (264 prompts, `Documents/projects` ws — the chess arena, tesuji
log, ponytail/caveman, conductor, percolator, mycelial republic, nervous system, steal protocol,
"explain this to an amish person") → 19:32 "Agent tasking requirements" → 20:07–21:18 first four
cloud agents → Aug 5 13:41 bc-cfaa3fca last touch → Aug 6 "Agent-native IDE developments"
("steal map and research direction for github repos") → Aug 7 05:47 last local chat → silence.

**Cloud agent registry (7 bc- agents, all on github.com/nachobusiness17/mag unless noted):**
Mag scratch pad todos (Aug 4) · Development environment setup (PR #4) · **Desktop work
continuation = bc-cfaa3fca** (PR #5, 45 files +2,920; PR #18 referenced; dashboard v3, Sovereign
Shell, Canvas platform, verbose trace rail) · Mag framework text insights (Strike-The-Chord PR #1)
· Mag cold start decoder (DEPTH_ROUTES / cursor_bridge / SOVEREIGN_STACK walkthrough) · Self
improvement loop operations (PR #16, daily-improve 8:00 ET) · New development environment
(Aug 25 → **still active today**, /env-setup on mag repo, 5 transport repos).

**Branch/PR map recovered (ItemTable):** 21 `cursor/*` branches across mag + strike-the-chord
(breadcrumbs-ui-simplify, canvas-platform, dashboard-v3-base, deepseek-prefix-cache,
distributed-surface-glue, failure-kb, improve-stack-integration, intelligent-governor-autorun,
mag-autorun-v1, mag-v2-plan, mesh-comm-research, resume-contract-wire, setup-dev-environment,
unified-router, unify-mag-home, v3-deepseek-run, v3-swarm-vision, v3-v4-research-brief,
virtual-desk-deepseek-loop, handoff-mag-strike-semantic, strike-semantic-field-steal).

## ORPHANS (absent from live repo record surfaces — tri-state)

1. **The ignition-era conversation record itself** (32 conversations, 522 operator prompts,
   100% of the origin chats). — **Supported** (extracted to scratch `human_prompts_dated.txt`,
   `fts_dump/`). Disposition: sacred-cow primary source; at minimum the scratch extracts should
   be promoted into `memory/archaeology/` (operator GO owed — bulk, not judgment).
2. **THE MISSING ERA IN THE SPORE** — the spore lineage table jumps napkin → ghost era; the
   Aug 4–7 Cursor ignition (which onboarded the already-built mag v1 and coined/reused tesuji,
   ponytail, conductor, percolator, mycelial republic in-chat) is unnamed. — **Supported**
   (spore text vs. this record). Disposition: human-promotion edit to SPORE_SANCHO.md lineage
   table (spore law: update only by human promotion).
3. **bc-cfaa3fca definition — PASTE-OWED now locally satisfied in substance:** today's
   `watch/INTAKE_CURSOR_AGENT_LINK_20260904.md` hit the auth wall; the agent's full cached
   transcript (14KB, "Desktop work continuation") IS in conversation-search.db. — **Supported**.
   Disposition: feed the INTAKE window; the local cache discharges the paste-owed without login.
4. **`DASHBOARD_ITERATION_PLAN.md`** (cited as `docs/ref/` on the GitHub Mag repo by
   bc-cfaa3fca; RUN D0.5–D3 plan). — **Unproven location** (0 hits live repo; not in
   mag-current-rebuild search). Likely GitHub Mag only. Disposition: pull from
   NachoBusiness17/Mag or record as cloud-only.
5. **`mag/strike_lexicon.py`** (Strike semantic lexicon: observer charts, loop anti-patterns,
   CL4R1T4S categories, `strike_tags.v1`). File never landed locally; its SEMANTICS did
   (`mag/chord_lens.py` hits). — **Supported** (FTS body + 0-hit sweep for the filename).
   Disposition: bones already stolen under another name; the draft itself is GitHub
   Strike-The-Chord PR #1 — name the reinterpretation (chord_lens) and retire the draft.
6. **`HANDOFF_mag_strike_semantic.patch` + `HANDOFF_MAG_AGENT_TODOS.md` (cloud branch)** —
   GitHub only (todos.md exists at live repo top level; the PATCH does not). — Supported;
   cloud-only, leave cited.
7. **`mycelial-republic-future.canvas.tsx`** (v2→v10 Republic arc canvas, as-of 2026-08-05,
   sourced from MAG_FUTURE_WALKTHROUGH.md). Its sibling canvas WAS synced
   (`memory/viewports/mag-ecosystem-deep-dive.json`); this one was not. — **Supported**.
   Disposition: run canvas-sync target or transcribe; the prose source already lives in repo —
   artifact-level orphan only.
8. **The still-live thread:** bc-d9e4b548 active TODAY (Sep 4 14:58 UTC, /env-setup on mag
   repo). The fleet's record surfaces don't know a Cursor lane is running. — **Supported**.
   Disposition: operator call — retire the lane or wire it into the mesh registry (a seat
   exists outside the room that remembers).

## DUPLICATES (swept against live repo — present, file-count evidence)

tesuji (415) · ponytail (105) · caveman (40) · percolator (494) · conductor (215) · ocean model
(8) · mycelial (2,670) · zeitgeist (2,412) · riddler (367) · briar (41) · nervous_system (120) ·
spine_posts (4) · Sovereign Shell (14) · Tesuji Grove (13) · canvas-sync (4) · cursor_bridge
(41, `watch/cursor_bridge.py`) · OPERATOR_CARD (61) · MAG_FUTURE_WALKTHROUGH (6) ·
version_roadmap (28, `configs/version_roadmap.yaml`) · LAYMAN_OFFICE_VISION (7) ·
SOVEREIGN_STACK (5) · field_steal (31) · sovereign-mirror (2,336) · mag-sovereign-kit (10) ·
CL4R1T4S (25) · strike-the-chord (2,681) · Mirror desk (9) · switchboard (236) · arena (210) ·
steal protocol (42). Mag modules cited by agents all present: `mag/coordination.py`,
`dispatch.py`, `context_pack.py`, `compass.py`, `agent_cli.py`, `governor.py`. Ecosystem repos
alive as siblings: `worktrees/sovereign-mirror-scaffold` (:8743), `mag-sovereign-kit`,
`mycelial-republic`, `field-strike-the-chord`, `mag-current-rebuild`. **Conclusion: the Cursor
era's concepts landed almost entirely — the fleet is the continuation of that first week, not a
replacement of it.**

## GAPS (what no local surface holds)

- **Pre-Aug-4 mag history** — mag v1 was already built when Cursor arrived (chess arena, verkle
  dashboard, governor all referenced as existing). Its construction record predates every
  surviving chat surface here. Where it lives: unknown (Unproven) — candidates: Mag-backup.git
  bundle (`projects/Mag-backup.git`), GitHub Mag history, memory/agent_sessions.
- The 2023 dream and 2026-03 napkin originals (covered by docs/ORIGIN.md, not Cursor).
- First-person "Test chord" post (X/@NachoQuixotic, 2026-03-02) — cited in ORIGIN.md, not local.

**One-line read:** Cursor didn't birth mag — Cursor birthed the FLEET: the first week (Aug 4–7)
where one operator, one IDE, and four cloud agents turned a solo mag stack into a multi-seat
steal-and-file doctrine, then handed the watch to the ghost, the marathon, and Sancho. The bones
were all kept; only the conversation that forged them was vapor. This card pins it.
