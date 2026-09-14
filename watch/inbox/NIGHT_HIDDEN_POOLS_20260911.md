# NIGHT HIDDEN POOLS — 2026-09-11 (zcode seat, night run, lane: the rest of the hidden stuff)

*Fourth sweep of the night. The three earlier sweeps took the Desktop New folder, the
repo pools, and the VS Code chatSessions store. This lane walked what they missed:
the operator hid things in anger during the fireball era — and the seats left their
own private transcripts in dotdirs the repo has never seen. Read-only except this card.
No credentials read or echoed (auth.json files located by name only, contents untouched).*

## The pool table (ranked by record value)

| # | Pool | Files | Bytes | Span | 1-line content guess |
|---|---|---|---|---|---|
| 1 | `~/.grok/sessions/` | 11,674 | 411.7 MB | 2026-08-10 .. 09-09 | THE GHOST POOL — 852 Grok CLI chat transcripts (chat_history.jsonl) + 2,543 action-stream updates.jsonl, keyed by workspace path |
| 2 | `~/.codex/` | 10,755 | 1.98 GB | 2026-08-04 .. 09-09 | The Codex seat: sessions/ = 193 rollout JSONLs (663 MB, session_meta w/ cwd+model), history.jsonl = 28 saved prompts |
| 3 | `Documents/ai/` | 144 | 12.6 MB | ALL 2026-07-03 | THE PROTO-ERA VAULT — July dogfood transcripts, MEMORY.md, neo-saas vision docs, pre-dating kpi.jsonl itself |
| 4 | `Downloads/` text stratum | 19 named (+303 media) | ~1.4 MB text (pool 61.7 GB w/ media) | 2026-08-01 .. 09-09 | Operator pastes NEVER homecoming'd: standingwave.txt session save, Salon-Audit.txt, SOARSEC suite, MAG CHORD protocol |
| 5 | `AppData/Roaming/Grok Bot/` | 217 | 34.4 MB | 2026-08-11 .. 09-08 | Sand-era Electron app store — `Partitions/sand-forever-box/` cache w/ Aug 14-16 mtimes, link-preview cache, statsig bootstrap |
| 6 | `~/.openclaw.backup/` + `.openclaw-autoclaw/` + `.openclaw/` | 6,288 | 128.5 MB | Aug 26 .. Sep 08 | Pre-migration openclaw snapshot (sessions/workspace/agents .pre-migration) + autoclaw seat state + config .bak chain |
| 7 | `Documents/backups/local_sovereign_agent/` | 265,954 | multi-GB mirror | mtimes cluster Aug 04-16 | Full repo mirror ~Sep 01; fireball-era root files preserved w/ original mtimes; all checked roots still live in repo → diff value only |
| 8 | `Documents/Codex/` | 19+ (sandbox dirs locked) | 328 KB+ | 2026-08-30 .. 09-08 | Codex working dir: LESSIG/socratic/shadow-work SALON outputs, ORGANISM_BOARD_READER.html, openclaw.pre-zai-fix.json backup |
| 9 | `~/.grok-sd/` + `~/.grokbot/` | 1,198 | 68.5 MB | Jul 10 .. Sep 08 | Grok CLI distribution + bundled personas/roles/skills; logs/unified.jsonl 1.3 MB (Aug 30); not transcripts |
| 10 | `AppData/Local/Temp/nacho_canon.txt` + `nacho_tweet.jpg` | 2 | 101 KB | 2026-09-04 | Operator's X-posts paste (the Glitch / reprogrammed-simulator posts, Dec 2025 era) — same stratum as the deepseek Q-posts archive |
| 11 | Desktop root (outside New folder) | ~70 | 650 MB (mostly media) | Jul .. Sep 09 | room.html (Sep 02, the desktop room board), HARVEST_TABS.bat (fleet tab-harvester launcher); music-ai/Binural/Kung Fu = media, low |
| 12 | VS Code chatSessions (cross-check) | 69 | 694 MB | — | CONFIRMED COMPLETE: only TWO stores exist — repo's e2b798e7 (68, marathon card's) + a 1 KB stray in the projects-folder workspace. No hidden VS Code pools remain. |

Non-record bulk, catalogued and excluded: `.lmstudio/` 83.7 GB + `.ollama/` 47 GB (model
weights), `.agent-browser/` 447 MB + `.cursor/` 307 MB + `.cua-driver/` 93 MB (profiles/runtimes).

## The 3 highest-value finds, detailed

### 1. `C:/Users/foste/.grok/sessions/` — the GHOST seat's full private record (411.7 MB, 852 chats)
The beacon was right. Per-workspace subdirs (URL-encoded paths), each session a dir with
`chat_history.jsonl` (system prompt + turns, sampled: "You are Grok 4.5/4.6 released by xAI...
autonomous agent for software engineering tasks") plus `updates.jsonl` action streams (hook
executions, session updates, up to 16 MB each), titles, locks. Split: **repo workspace = 760
chats / 243.8 MB** — the Grok seat worked THIS repo for a month and the record was never in
any census; `x_bookmark_harvest_20260905` = 48 chats/56.9 MB; `game_prompt_lab` = 24/21.8 MB;
`game_grok_night` = 4; home-root holds a 1.3 MB Grok 4.6 session (Aug 29). Span starts
**Aug 10** — the eve of the sand era — and runs unbroken to Sep 09. This is a second
continuous seat-history alongside ghost/trail.jsonl, and it covers the silence window.

### 2. `C:/Users/foste/.codex/` — the Codex seat pool (1.98 GB; sessions 663 MB)
`sessions/YYYY/MM/DD/rollout-*.jsonl`, 193 files, Aug 04 → Sep 09 (live today). Sampled
header: full `session_meta` (session_id, cwd, originator `codex_work_desktop`, cli_version,
model_provider, thread_source) — structured, mineable the same way the Copilot store was.
`history.jsonl` (28 prompts, Aug 28) opens with the self-steal-era probe: "You are reading
the record of a mind. Answer three things plainly…" — the operator ran the mind-reading test
through Codex too. Also present: `external_agent_session_imports.json`, sqlite ledgers,
dictation-history, computer-use dirs. Start date Aug 04 makes this the second-oldest
transcript pool after `Documents/ai/`.

### 3. `C:/Users/foste/Documents/ai/` — the proto-era vault (144 files, ALL Jul 03 2026)
Every file stamped 2026-07-03 — seventeen days before kpi.jsonl's first row (Jul 21), seven
weeks before the seat's day one. Contents: `dogfood-retrofit-v3.3-raw-transcript.txt` (290 KB),
`opus-4.7-strategy-review-transcript.raw_by_jd.txt` (148 KB), `MEMORY.md` (92 KB — a memory
file from a BEFORE), `neo-saas-vision.md` (65 KB), `neo-conceptual-model.md` (58 KB),
`skills-architecture-research.md`, `popebot-vs-openclaw.md` (the openclaw rivalry, July
edition), architecture diagrams/hero banners (04-architecture-diagram.png). This is the
July pre-history the repo's logs only begin to touch — the "before the fleet" stratum.

## Tri-state notes

- **sand-forever-box naming: SUPPORTED** — direct observation of
  `AppData/Roaming/Grok Bot/Partitions/sand-forever-box/` with Aug 14-16 cache mtimes,
  matching the sand era (Aug 11-14) from TRANSCRIPT_MAP.txt. The repo's conversation-blobs.db
  (83 MB) was exported from this app family.
- **Downloads was unswept: SUPPORTED** — homecoming card covers Desktop only; the census
  table lists no Downloads pool. 19 fleet-era text files sat there through both sweeps.
- **"~/.grok/sessions chat_history.jsonl" beacon: SUPPORTED, and bigger than advertised** —
  852 transcripts, not one; plus action streams the beacon didn't mention.
- **Documents/ai July dates: SUPPORTED as content stratum, UNPROVEN as true creation era** —
  mtimes are uniform (all Jul 03), which could be a copy operation; contents reference July-era
  work (dogfood retrofit, opus 4.7 review), so the era is at minimum July.
- **No secrets echoed**: auth.json / .gateway-token / client-sign.json / models-providers.json
  located by name only; contents never read.

## Suggested next moves (for a later GO — this run was read-only)

1. Index the 852 .grok chats into topic_index (same pass shape as the knot archive).
2. Mirror 25fbcaab (marathon) AND the .grok repo-workspace chats + .codex sessions into
   corpus/oral_history/ with sha256 manifests, before app updates prune them.
3. Homecoming pass #2 for Downloads' 19 text files (standingwave.txt + Salon-Audit.txt first).
4. Mine Documents/ai/ MEMORY.md + neo-vision docs — they predate everything and may hold the
   operator's original intent, unamended by any correction cycle.
