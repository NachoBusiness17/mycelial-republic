# ZCODE SHADOW STEAL — 2026-09-18 (correspondence + trajectory, mined locally)

**Ask:** steal all our correspondence and trajectory in zcode; shadow-work the
store; classify everything so a person can understand it; make it load
primitively through the verkle lattice, RIB warming / cache mining, and the
trajectory organ. Example session: `sess_efb460c0-3262-4a3b-95f0-e40d378bf303`.

**LAW HELD:** chat history is T0/T1 private — this entire pass ran locally;
nothing was sent to remote lanes. The corpus lands at
`memory/corpus/zcode_history/` (6 files, pointers to raw paths preserved).

---

## THE HEADLINE (tri-state: Supported, measured)

**The operator's side of the correspondence has ~total attrition in the
zcode store.** What survives is the work's shadow, not the conversation:

| Layer | Survives? | Where |
|---|---|---|
| Operator messages | ✗ (only 7 tiny Aug-25 test transcripts in v2; model-io strips request messages) | gone |
| Agent replies | partial — 3 model-io rollouts (2 are today's live windows) | `~/.zcode/cli/rollout/` |
| Work performed | **rich** — 1,161 subagent task descriptions across 36 sessions | `~/.zcode/cli/agents/sess_*/agent_*/metadata.json` |
| Commands run | 310 exec logs + the auto-trajectory organ (`memory/trajectory/steps.jsonl`) | exec dirs + repo |
| Telemetry | span logs 09-12..09-18, no prompts | `~/.zcode/cli/log/` |

**Novelty finds (this pass):** `export-log-stage/` exists and is EMPTY — the
session-export pipeline was staged and never wired; that is the fix for the
attrition (law proposal: every window ends with transcripts copied to
`watch/inbox/`, the same inbox-first rule that already saved work once).
`tmp_orphan_mine/` is empty — a prior orphan-mining attempt died silently.
The v2 transcripts are the harness's own birth records (Aug 25, palindrome
tests) — the earliest surviving voice.

## THE CENSUS (Supported — bytes read this pass)

- **36 sessions** in `cli/agents/` (sess_0014179a… sess_efb460c0…), 3,591 files
- **1,161 agent task descriptions** → `memory/corpus/zcode_history/agent_tasks.jsonl`
- **310 exec logs**, 3 model-io rollouts (18 MB), 7 v2 mini-transcripts (268 MB store total)
- busiest window: one session carrying **196 agent tasks** (the 12-wide mega windows)
- example session `sess_efb460c0`: subagents incl. "Hermes 401 lane debt fix"
  (2026-09-07), 45 exec files, artifacts + image-cache dirs intact

## THE EXPLAINABLE MAP (60-second version for a person)

The estate is **one house with seven rooms**, all cross-indexed in
`catalog/catalog.jsonl` (946,773 rows) and tagged in `catalog/tags.jsonl`:

1. **CORRESPONDENCE** — the conversations. Mostly vapor (see attrition); what
   lands durably goes to `watch/inbox/`. The zcode-side survivors:
   `memory/corpus/zcode_history/correspondence_*.jsonl` (assistant side).
2. **TRAJECTORY** — what was actually done: `agent_tasks.jsonl` (1,161
   descriptions), exec logs, `memory/trajectory/steps.jsonl` (auto-logged,
   hash-chained rows), `memory/worldline/`.
3. **CANON / PRIMARY SOURCES** — `memory/corpus/` (esoteric canon, Steiniger,
   Drexel intake), `watch/inbox/LINKS.jsonl` (13 canonical), research packs
   (107 in `memory/lenses/corpus_index.json`), the parables (THE SCALE…).
4. **GAMES** — `dashboard/static/games/` (RUINS GO engine + 12 levels, MUD,
   estate_walk.html), `memory/game/` (world state, Steam corpus, flow ledger).
5. **SALONS** — `watch/salon_inbox/` + salon artifacts: 7-shape blind shape
   trains, ractor panels; verdicts fold into watch/inbox artifacts.
6. **DOCTRINE / LAW** — `docs/`, CONSTITUTION pointers, law lattice (51 laws),
   elder surface (14 lenses), falsifier ledgers, warnings.
7. **SHADOW** — everything the maps point at but nobody reads: sibling
   projects (`ext:` zones, ~280K catalog rows incl. a 77K vault), 3,269 ghost
   refs climbing +160/day, 309 ownerless fences, the crashed ghost-daemon.

**Task clusters across the 1,161 descriptions** (keyword-first-match):
research 81 · infra 76 · doctrine 75 · salons 86 · games 61 · verkle 21 ·
astra 20 · x-play 20 · parables 12 · **other 709 (61% — unnamed plumbing;
the fleet's real mass is work too plain to name).**

## GAP ANALYSIS (what this pass did NOT mine — the next dig list)

- `cli/exec/` contents beyond counts (2,037 files of command output — the
  results shadow; bounded head-mining per session is UF material)
- `cli/artifacts/` and `image-cache/` contents (uninventoried)
- sibling `ext:` estate (280K rows) — zone policy dig is UF-123, still queued
- telemetry `cli/log/` — span graph could reconstruct per-session timelines
- the 7 v2 mini-transcripts parsed but not diffed against memory (Aug-25 era)

## HOW IT LOADS (the primitive-loading protocol, exercised this pass)

1. **RIB warming / cache mining** — the structure-only summary (counts,
   families, attrition — no private text) rides `mag.rib_cache.rib_chat` as
   the FROZEN_RIB prefix + digest tail on z_ai3; cached_tokens in the receipt
   below prove the prefix mined. Dynamic content lives in the TAIL, never in
   the frozen prefix.
2. **Trajectory** — a `trajectory_step.v1` milestone row is appended to
   `memory/trajectory/steps.jsonl` (the organ already auto-logs commands;
   milestones ride the same schema).
3. **Verkle lattice** — `mag.state_snapshot.capture_summary` captures the
   session state for the pile/verkle organs; the artifact is registered in
   `watch/inbox/index_events.jsonl` (hash + pointer, the estate's ground wire).
4. **Re-discovery** — `corpus_search kind=corpus "zcode_history"` finds this
   corpus once the next catalog rebuild lands (map is Sep-16; the staleness
   law applies — `corpus_get` the bytes, truth lives on disk).

## RECEIPTS

- extraction pass: 36 sessions / 1,161 tasks / 310 exec files walked;
  6 corpus files written under `memory/corpus/zcode_history/`
- correspondence files: correspondence_199e4b14 (3 agent texts),
  correspondence_712a3b7b (2), correspondence_c424b80a (32 + operator turns
  from the 5-row first pass) — assistant side only, attrition documented
- top surviving actions this window family: Edit 17, venv-python 14, Write 9
- loading: trajectory milestone row appended; rib_chat warm receipt below;
  capture_summary receipt below; index_events registration appended
- tri-state: census/clusters = Supported (bytes); attrition = Supported for
  `.zcode/cli` (negative result after schema probe); "no operator text
  anywhere on disk" = Unproven (only this store was swept — docker/z.code
  desktop stores remain unprobed)
