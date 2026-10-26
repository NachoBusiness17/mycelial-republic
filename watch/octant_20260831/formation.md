# ox-archaeology — the ACTUAL past ox formation (2026-08-31)

Method receipts: `wc -l /board/grok_feed.jsonl` = **12,681 lines** (span 2026-07-21 → 2026-08-31). Sampled tail 200 lines only. Bounded greps: `session_start` = 13 in first 2000 lines, 7 in last 2000. Salon file + `game_grok_night` (11 files, head -10) read.

## 1. The ox feed: one main seat + short-lived specialist lanes

The tail-200 window (2026-08-30 01:06 → 08-31 04:32) shows **6 distinct sessions**, two kinds:

**Main interactive seat** (`01a04e25…`): 175 events, ~50-min visible span, 11 user prompts, 12 stops — human-in-the-loop, conversational ("i'm impressed", "this is the perfect dogfood environment"). Tool mix: read_file 57, grep 41, search_replace 35, run_terminal_cmd 11, write 3 — read-heavy (~40% read, ~23% edit, ~27% search). Tool-call deltas: **median 0.4s, p90 24.7s** — bursty: rapid mechanical bursts, then long human-turn pauses. The main seat did its OWN recon (no delegation layer).

**5 specialist lanes** (`01a0558e/90/91` at 02:03–02:07; `01a05615/16` at 04:30–04:32): identical fixed prompt — "You are the specialist lane for Sovereign Mag… Reply with exactly GROK_OK… One job… DO NOT load any framework… answer DIRECTLY." Each lived **25–73s**: session_start → user_prompt_submit → stop → session_end. Fire-and-forget probes, no iteration.

Event vocabulary of the feed: `session_start / user_prompt_submit / post_tool_use / stop / session_end`. Client is an IDE-class host on the Windows box (cwd `C:\Users\foste\...`); identity of the client is unverified from the feed itself — tool-name signature only (read_file/search_replace/run_terminal_command).

## 2. The salon: 4 heterogeneous seats × 2 rounds

`SALON_DIAMOND_AGE_20260831_ROUNDTABLE.md`: seats A–D on **deliberately different models** (openrouter/auto, nvidia/deepseek-v4-flash, zai/glm-5.3-flash, cerebras/gpt-oss-120b). Round 1 = one position + ONE NAMED ACTION per seat. Round 2 = witness passes + consensus stress-test. Rate-limit handling = lane-swap (Seat A: Groq failed twice → swapped). Ran as OpenClaw subagent fan because the host roundtable command was blocked (WSL vsock interop failure) — the swarm runs where the lanes are, not where the plan was written.

## 3. game_grok_night: 2 lanes × 2 rounds × artifact chain

11 files = lanes **A and B**, each with raw capture (`grokA_raw.json`, `grokB_raw.json`), round-1 and round-2 deliverables (`grokA.md`/`grokA2.md`, `grokB.md`/`grokB2.md`), canon (`grokA2_canon.json`, `grokB2_canon.json`), and derivatives (`archetypes`, `quests`). Pattern: raw → md → canon.json → derivative docs, filed to a slot "so dawn merge has bytes." Night lanes wrote long-form canon in one pass each round.

## The formation's actual shape

- **1 interactive main seat** (IDE-hosted, human-paired, does its own greps, bursty cadence)
- **N short-lived specialist lanes** (fixed one-job prompts, ~30–70s lifespan, no follow-up)
- **4-seat deliberation salon** (heterogeneous models, 2 rounds: positions → witness/stress-test, one named action each)
- **2 night lanes** (long-form canon generation, 2 rounds, raw→canon→derivative chain, dawn merge)
- **One operator = spawn authority + merge point** (same structural role as Sancho now)

## OCTANT mapping — copy / improve

**Copy:** heterogeneous-model seats (the salon's model spread is a feature, not an accident); fixed one-job lane prompts with anti-framework rules; round structure (round 1 positions, round 2 witness passes); the raw→md→canon→derivative artifact chain; single merge point; "one named action" output contract per seat.

**Improve (OCTANT deltas over the past):**
1. **Pool discipline:** past lanes were unbounded and ad hoc; OCTANT caps 6 concurrent, receipts it, and backfills wave 2 as slots free.
2. **Delegation layer:** the past main seat grepped everything itself (98 read/grep calls in one window); OCTANT leads end with GOPHER briefs → $0 flash ROW lanes.
3. **Fixed output contract:** past lane output was freeform prose; OCTANT fixes output paths and ROW format up front so merge is mechanical.
4. **Resilience:** past lane-swap on rate-limit was improvised; OCTANT schedules heavy jobs inside provider windows (see zai-window lead) instead of reacting.

## GOPHER briefs

GOPHER: count and classify all session_start events across the full 12,681-line feed (interactive main vs specialist lane vs salon/night spawns — by session_id prefix and prompt shape) | pointer: /board/grok_feed.jsonl | output: /board/octant_20260831/rows/ox-archaeology-g1.row.md

GOPHER: verify the dawn merge of game_grok_night canon — find where grokA2/grokB2 canon.json content landed in campaigns/villains_guild (A2 slot receipts) | pointer: /mag/memory/runs/game_grok_night + /mag/campaigns/villains_guild | output: /board/octant_20260831/rows/ox-archaeology-g2.row.md

GOPHER: find the spawner receipt for the 5 "specialist lane… GROK_OK" fanouts (run_terminal_command or equivalent in the feed around 2026-08-30 02:03 and 04:30) | pointer: /board/grok_feed.jsonl tail | output: /board/octant_20260831/rows/ox-archaeology-g3.row.md

## Self-attack (once)

Weakest sentence was "the IDE feed is Codex/VS Code hooks" in my draft — the feed never names its client; tool names only *suggest* it. Fixed: the doc now states "IDE-class host… identity unverified from the feed itself — tool-name signature only." Second fix: draft conflated salon seats and night lanes into one "2–4 seats" range; the doc now keeps them as two distinct sub-formations (4-seat deliberation vs 2-lane canon generation).
