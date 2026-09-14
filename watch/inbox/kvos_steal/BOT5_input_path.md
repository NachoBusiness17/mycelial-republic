# BOT5 — KV OS steal survey: the INPUT PATH
Lane: where live session prompts/transcripts actually live — what a KV OS must page. Bounded survey, 2026-09-10. Read-only + one file.

## THE POINT
The live input path is `memory/agent_sessions/orc-*.json` — 2,654 full message-array transcripts (70 MB), written by `mag/agent_cli.py` (`_SESS_DIR`, line 2677), which re-embeds a freshly built system prompt as `messages[0]` on every turn (lines 891, 2423, 2618). The standing scaffold alone (workspace AGENTS.md + repo AGENTS.md + operator-corrections SKILL.md) is 36,806 bytes re-sent verbatim per turn — this is the concrete body of refeed_guard's 94%-refeed finding, and stored-artifact dedup (kvos_block's 2.4%) never sees it because it lives in the input path, not in stored artifacts. v0 hook: make `agent_cli.py`'s transcript write content-addressed — scaffold blocks keyed by sha256 in a shared block store, session files keep block refs — so identical scaffold pages dedupe across every seat in the agent tree and the existing hash-chain (kvos_block.py) extends over the store.

## Input-path map
| Path | Holds | Size | mtime |
|---|---|---|---|
| `memory/agent_sessions/` | LIVE session transcripts: `orc-t*.json`, full message arrays incl. system prompt (`session_id`, `provider`, `model`, `messages[]`). 2,654 files, 2,654 of them `orc-*` | 70 MB | active — `orc-t7733002cc4.json` + `LATEST.txt` 08:11 today |
| `memory/agent_sessions/LATEST.txt` | pointer to current session id (`orc-t7733002cc4`) | 15 B | Sep 10 08:11 |
| `watch/active_session.json` | live seat state: session_id, cwd, updated_at, last_hook | 211 B | Sep 10 08:02 (body `updated_at` 2026-09-10T12:02:22Z) |
| `watch/summarized_sessions.json` | list of already-summarized session ids (uuid + orc ids mixed) | 51,131 B | Sep 10 08:11 |
| `watch/monitor_lane.state` | lane monitor state | 8,861 B | Sep 10 08:22 |
| `memory/biography/verkle_chain.jsonl` | the signed chain — knot records, not raw prompts | 5.24 MB (5,239,211 B) | Sep 10 08:11 |
| `memory/biography/<uuid>.{md,pdf,dossier.json,visual_pack.json}` | per-entity biography dossiers (elder memory, not session input) | ~50-80 KB each | Jul 21 → Aug 7 |
| `queue/handoff/zcode/CONVO.md` | this seat's mesh channel (input read per boot: last 3 turns) | 612,779 B | live lane |
| `queue/handoff/{autoclaw,cache}/CONVO.md` | other seats' channels | 1,604 / 662 B | — |
| `memory/sessions/`, `memory/campaigns/sessions/` | old one-shot session records (stale) | 4 KB / 16 KB | Aug 8-9 |
| `db.sqlite` | NOT in the repo (find at maxdepth 5: 0 hits). The dead z.ai session history named in boot memory lives outside the repo tree — out of bounds here | — | — |

## Scaffold arithmetic (measured once)
- Workspace `AGENTS.md` (projects/): **21,669 B**
- Repo `AGENTS.md`: **5,745 B**
- `.agents/skills/operator-corrections/SKILL.md`: **9,392 B**
- **Total standing scaffold: 36,806 B ≈ 36 KB per turn**, byte-identical every turn, every session, every seat (plus tool defs and skill manifests — not measured, strictly larger).

Arithmetic: 36,806 B × 1,000 turns = 36.8 MB re-sent per 1,000 session-turns, per seat. With the night-wave shape (8-wide workers) and the 09-05/06 concurrency probes (5- and 8-wide clean), a fleet day of a few thousand turns re-sends tens of MB of pure scaffold. refeed_guard already measured this class at **94% of session input** (B1 REFEED_HEAVY, falsifier PASS) — the scaffold is its largest concrete, byte-measured component. Pinned in a KV block store, those bytes are sent once per scaffold revision, then every turn is a cache-read reference.

## Door check (read-only GETs)
- `GET http://127.0.0.1:8765/static/watch/active_session.json` → **404 not found**
- `GET http://127.0.0.1:8765/static/watch/summarized_sessions.json` → **404 not found** (HEAD also unsupported: 501)
- Verdict: the door does not serve `watch/` at `/static/watch/` — both files are LIVE on disk (mtimes 08:02/08:11 today, active_session `updated_at` 12:02Z) but unreachable through that URL. The mount root or path mapping differs from what the card assumed; whatever serves `/static/` is not rooted at `watch/`.

## v0 hook point (one line)
**Hook in `mag/agent_cli.py` at the transcript write (`_SESS_DIR`, line 2677) + the three `_system_prompt()` embed sites (lines 891, 2423-2424, 2618): keep format `orc-*.json` but replace the verbatim `messages[0]` scaffold with a block ref `{sha256, len}` into a shared store `memory/kvos/blocks/<sha256>` — AGENTS.md, skill text, tool defs become pinned pages deduped across the whole agent tree; kvos_block.py's hash chain extends over the store as its ledger.**
