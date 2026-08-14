# RIB — Castles in the Sky, Foundations Beneath (the intent behind the dashboard)
**Schema:** rib.castles_foundations.v1 · date 2026-08-10
**Operator's thesis (verbatim intent):** "the home page the story the diary all of it are attempts
to understand your internals in dashboards that mimicked the way the data might be displayed or
contained. it was the whole build your castles in the sky and put the foundations beneath them
that's what we are doing here."

## The reframe
The dashboard surfaces (Home, Story, Diary, the whole IA) were NEVER disposable prototypes and NOT
"crude signals." They were **castles in the sky** — the operator's HYPOTHESES about how the internals
*should* present themselves, built as legible dashboards BEFORE the foundations existed. Each surface
is a **spec of intent**: what the machine should be able to tell the operator. The current ghost
internals (verkle, ghost_control, sovereign, memlang, weave, state_quantizer) are the FOUNDATIONS now
being laid beneath them. **The job is to make each foundation actually deliver what its castle promised.**

## The castles → their foundations → what makes each real
Grounded in `docs/ref/DASHBOARD_DESIGN.md`, `docs/DASHBOARD_INFORMATION_ARCHITECTURE.md`,
`docs/DASHBOARD_REORIENTATION_V2.md`, `docs/HOW_TO_MAG_DASHBOARD.md`.

| Castle (the intent/surface) | What it promised | Foundation (the current internal) | What makes it real |
|---|---|---|---|
| **Home** | "Local office that files work as beads; Home answers status + last day + next step." 5-second: Am I OK to work → What did I do → What's open → Talk/load → Depth. "Summary first, files second, spectacle never first." One attention statement, active work, latest verified outcome, next action, one command. | `ghost_control.control()` (human-facing harness: scrum/press/loop/tokens/skills/oh_fuck) + `attention_ranker` + `state_quantizer` summary knots (the compressed "now") + `verkle_tip` (latest bead) + `memlang` (the command entry = a token). | The seat's **Machine + Ghost·now + Reconcile** cards, fed by sovereign + ghost/control + chain. The "one command entry" = a memlang compile box. |
| **Story** | "the readable synthesis" — an interpretive narrative (thesis + hero journey), source-certain. | `mag/story.py` (build_story) + `synthesis_agent`/Bard Chronicle. | A **Story** pane that renders `/api/v1/story` — the interpretation lens, not a raw feed. |
| **Diary** | "day-by-day narrative spine from filed beads." | `mag/diary.py` (build_diary from filed beads) + `memory/diary_latest.md`. | A **Diary** pane rendering `/api/v1/diary` — the longitudinal spine. |
| **History/Continuity** | Timeline (evidence) → Diary (narrative) → Story (synthesis) → Verkle lattice (continuity) — "different levels of the same question." Selecting a knot leads back to evidence. | `verkle_knot` chain/tip + `tapestry`/`lattice` + `/api/v1/chain`. | The seat's **Knot lattice** card — source-backed, each knot links to its file (`/files/…`). Never trust the visualization over the artifact. |
| **Projects** | project brief: thesis, sprint, roadmap, outcomes, open needs, blockers, decisions, evidence knots. | `mag/idea_graph` + `/api/v1/ideas` + `mag/scrum`. | An **Ideas/Projects** pane over `/api/v1/ideas`. |
| **Run / Direct Mag** | the operator request, Mag's interpretation, remembered context, task class, right-size, executor, verification, cost, stop boundary. | `mag/agent_cli`, `mag/router`, `models/quota` (right-size), `mag/orchestrator` (executor), `cost_enforcer` (cost), `failure_kb` (verification). | A **Run** pane = the behavioral-router control surface, current internals. |
| **Library** | research object: what/why/source/freshness/reliability/learned/informs/changed/remaining. | `memory/ingest` + `skill_ledger` + `tesuji` + `weave`. | A **Library** pane over `/api/v1/ingest` + skill-ledger. |
| **System** | "Mag can/cannot operate because…" + cost per verified outcome + model right-sizing (not token trivia). | `sovereign_dashboard` (one call) + `cost_enforcer`/`token_economy` + `models/quota` + `guard_registry` (reconcile). | The seat's **Reconcile** card (desired vs actual) + Machine + Economy. |

## The unifying principle
The whole IA is one question answered at five levels: **"What is happening, why does it matter, what
needs my decision, what can Mag do next, what evidence supports it?"** (REORIENTATION_V2). The castles
encoded this as surfaces; the foundations now deliver it as data:
- **Summary first** = state_quantizer summary knots + ghost/control (the compressed "now").
- **Files second** = verkle knots + `/files/…` (source-backed truth; never trust the visualization).
- **Spectacle never first** = the lattice/tapestry are lenses over the same knot evidence, not competing tabs.
- **Interpretation over telemetry** = Story/Diary/Bard turn beads into narrative; the operator's actual words stay visible.
- **The operator's words remain** = every surface is source-linked, not a restated invented story.

## The seat = the foundation beneath the castle
The new SEAT is precisely "foundations beneath the castles": it renders the CURRENT ghost internals
(sovereign, ghost/control, health, chain, economy, reconcile) in the way the castles envisioned. It is
NOT the old crude aggregates — it is the castles made real by the foundations that now exist. Each card
maps to a castle:
- Machine (sovereign) → System castle ("Mag can/cannot operate because…")
- Ghost·now (ghost/control) → Home castle (what matters now)
- Knot lattice (chain) → History/Continuity castle (evidence → source)
- Reconcile (desired vs actual) → the operator view / guard_registry
- (next) Story / Diary / Ideas / Run / Library panes → the remaining castles, each fed by its current internal.

## The loop
Every castle that gets a foundation becomes a **knot** (source-backed, content-addressed) and a
**weave** (the skill-recipe for rendering that understanding) and a **memlang** opcode (the command to
summon it) — so the castles compound into the ghost surface, which is the seat, which is the machine
made legible. This is "castles in the sky, foundations beneath" — the vision and the substrate are one
system, and the seat is where they meet.

## Fold
This synthesis ties the whole session: the window-storm (the substrate failing), the container (the
substrate held), the seat (the castle rendered on current internals), the memlang/weave/verkle stack
(the language of the castles), and the emergence deep-dive (how the castles self-compose). It should
fold as a research pack + a skill_ledger decision so "the surfaces are the spec of intent" becomes case law.
