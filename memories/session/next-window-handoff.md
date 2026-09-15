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

- **2026-09-15:** Discord bot LIVE (Mag#2124, guild NT-ACv2, token in `%LOCALAPPDATA%\hermes\.env`,
  gateway green, AGENTS.md truncation fixed via `context_file_max_chars: 40000` in Hermes config).
  Receipt: `watch/inbox/HERMES_DISCORD_SETUP_20260915.md`.
  Checkpoint `aa9bea1b7`. Fifty-wide board: `memory/plans/fifty_wide_20260915.md` (50 tasks, seeded in queue/todo.md).
  Goal horizon: **Sep-20 proof** — gate = operator beacon read (`watch/inbox/DAWN_READING_MIRROR_20260907.md`);
  Astra bundle fixes + retro-knotter GO are the big prep lanes.
- **Known warts:** inbox INDEX fold stale (pre-existing, append-only); hosted_room_worker sqlite
  lock (non-blocking); netlify deploy auth pending; token rotation for the Discord bot recommended
  (clipboard-only lander: `%TEMP%\discord_token_land.py`).
