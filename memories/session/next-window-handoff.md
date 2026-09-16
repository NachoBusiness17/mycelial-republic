# Next-window handoff — frozen spec (executed by any new window)

_This file did not exist until 2026-09-15 (Clippy cited a fossil). This IS the spec now.
Keep it short. Update the STATE section, not the procedure._

## Procedure (every new window, in order)

1. **Load:** `docs/FRAMEWORK_LOAD.md` → `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md` → `AGENTS.md` (already injected as workspace instructions).
2. **Warm:** `memory/briefs/latest.md` → `state/CURRENT.md` → `./mag.cmd context-pack` → `queue/todo.md`.
3. **Check inbox:** `watch/inbox/index_events.jsonl` tail (last 10 events) — what landed since last window.
4. **One job** from the operator or the board (`queue/todo.md` / newest `memory/plans/fifty_wide_*.md`).
5. **FILE before close:** durable writes to `watch/inbox/` + register event in `index_events.jsonl`; checkpoint commit; `python main.py state-snapshot` if session was heavy.

## Standing laws (do not re-derive)

- Python: `.venv\Scripts\python.exe` or `mag.cmd` — never bare `python` (Hermes venv on PATH).
- T0/T1 local only. Janitor first. Pack+goal to remotes, never chat history.
- Residual on disk is truth; chat is heat. Append events, never rewrite the INDEX fold.
- "Launch N wide" = seed N lane tasks (board file in memory/plans/ + queue/todo.md section).
- Operator signs as Mark; journals arrive as photos → transcribe faithfully [? for uncertain], copy jpgs to watch/inbox, full plain-language decode.

## STATE (update this section only)

- **2026-09-16 (end of wave night):** Standing wave DRAINED — 60 receipts filed across
  `watch/inbox/wave_20260916/receipts/` + `watch/inbox/physical_computing/receipts/`;
  master index: **`watch/inbox/wave_20260916/WAVE_STATE_20260916.md`** (start there).
  Board: referee chain green · sampler claim conditional-refuted (closure receipt still pending) ·
  cube program staged · ractor plugin packaged (`P1_RACTOR_PACKAGE.md`) · wave protocol 30+ lanes folded ·
  26-work physical-computing canon registered (`S4_CORPUS_STEAL.md`, filed via `mag.link_library`) ·
  salon_50 honest count 39/50 (fossil "50/50" corrected in F1).
  **Next stones:** (1) sampler closure receipt, (2) v4 VOID build to repair grounding chain row 122
  (verify FAIL: row 122 truncated, `prev` matches nothing, no `hash` key; rows 123–124 orphaned behind it;
  tonight's wave-trajectory row is drafted in `WARM_START_20260916.md`, do NOT hand-edit the JSONL),
  (3) publish ractor-salon standalone repo, (4) cube GO (build auditions in `V1_BUILD_AUDITIONS.md`).
  Warm-start receipt: `watch/inbox/wave_20260916/receipts/WARM_START_20260916.md`.
- **2026-09-15:** Discord bot LIVE (Mag#2124, guild NT-ACv2, token in `%LOCALAPPDATA%\hermes\.env`,
  gateway green, AGENTS.md truncation fixed via `context_file_max_chars: 40000` in Hermes config).
  Receipt: `watch/inbox/HERMES_DISCORD_SETUP_20260915.md`.
  Checkpoint `aa9bea1b7`. Fifty-wide board: `memory/plans/fifty_wide_20260915.md` (50 tasks, seeded in queue/todo.md).
  Goal horizon: **Sep-20 proof** — gate = operator beacon read (`watch/inbox/DAWN_READING_MIRROR_20260907.md`);
  Astra bundle fixes + retro-knotter GO are the big prep lanes.
- **Known warts:** inbox INDEX fold stale (pre-existing, append-only); hosted_room_worker sqlite
  lock (non-blocking); netlify deploy auth pending; token rotation for the Discord bot recommended
  (clipboard-only lander: `%TEMP%\discord_token_land.py`); **GROUNDING_WAVE chain verify FAIL at row 122
  (2026-09-16)** — posts land but nothing after 122 can verify until the v4 VOID build; gene pool still
  feeds on the frozen 2026-09-04 audit (`memory/audit/aud_*.json`, no regenerator exists).
