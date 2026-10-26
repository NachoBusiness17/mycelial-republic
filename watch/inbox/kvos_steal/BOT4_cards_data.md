# BOT4 — cards + data feeds that record cache/session/memory state
Lane: KV OS self-steal survey, 2026-09-11 (box time). Read-only. No fixes, no spawns.

## THE POINT

The fleet already runs a continuous KV-state telemetry loop — `logs/kpi.jsonl` (457 MB,
unbroken since Jul-21, still appending today) plus the estate index (402 MB) are the two
big rehearsal datasets; the per-session layer (active_session.json, summarized_sessions.json,
monitor_lane.state, session_digest.jsonl) is live and appending as of this morning. The
doctrine for what the KV OS must honor is already on the cards: cache identity is byte-exact
(99.87% hit at zero drift, 778x prefill speedup, one-byte head drift collapses it 690x),
claims are hash-chained tri-state rows with a second-witness truth-gate, and senses/memory
live behind loopback cage organs (:8765 dashboard, :8001 MCP) — transport, never authority.
One correction to the brief: three of the seven named feeds live in `watch/`, not
`dashboard/static/` — the live session feeds write to watch/, the dashboard serves snapshots.

## Feed table (fresh = Sep 10; today's box date 2026-09-10/11)

| Feed | Path | mtime (EDT) | Size | State | What it records |
|---|---|---|---|---|---|
| overseer.json | dashboard/static/ | 2026-09-07 02:16 | 1,286 B | STALE (pre-rebuild) | Docker fleet census, schema overseer.v1 (ts, tag, per-container status). Lists mag-openclaw — retired 09-09. Wrong census if read today. |
| tesuji_map.json | dashboard/static/ | 2026-09-09 16:03 | 51,537 B | fresh-ish (2 d) | 5.3-flash tesuji field: T0 probe ledger + grid cells for the model-as-field map. |
| witness_snapshot.json | dashboard/static/ | 2026-09-09 01:06 (built_at 09-09T01:06Z) | 502,156 B | STALE vs live chain | Verkle chain witness: published_root, 7,377 leaves, tip index 7376 (tip ts 09-06 23:08Z). Chain has moved since (boot memory: 7,392 leaves). |
| index_data/ | dashboard/static/ | 2026-09-09 11:19–15:35 | 402 MB + small files | fresh (Sep 9) | ESTATE_INDEX.jsonl (402,115,634 B) + last_run.json, orphan_ledger.json (4 MB), rollup.json, verkle_birth.json (+2 .bak). The estate/knowledge index build. |
| summarized_sessions.json | **watch/** (not dashboard/static) | 2026-09-10 08:11 | 51,131 B | LIVE | Array of session ids already summarized (dedupe marker for the summarizer lane). |
| monitor_lane.state | **watch/** (not dashboard/static) | 2026-09-10 08:22 | 8,861 B | LIVE | Research-lane state: per-source cooldowns (arxiv/openalex/hn epoch stamps) + claimed item ids ("agent swarm concurrency"). |
| active_session.json | **watch/** (not dashboard/static) | 2026-09-10 08:02 | 211 B | LIVE | Current session_id, cwd, updated_at, last_hook ("stop"). The seat's live cursor. |
| (bonus) session_digest.jsonl | watch/ | 2026-09-07 11:18 | 5.5 MB | aging | Per-session digest rows — the bridge from kpi counts to per-session content. |
| (bonus) last_seen_session.txt | watch/ | 2026-08-10 | 36 B | STALE (1 month) | Last seen session id (legacy cursor). |
| (bonus) GROUNDING_WAVE.jsonl | watch/ | 2026-09-09 21:39 (md rows through 09-10T01:39Z) | 64,594 B | LIVE | Hash-chained tri-state claim ledger. |
| kpi.jsonl | logs/ | 2026-09-10 08:12 (ts 09-10T12:12:16Z) | 457,910,952 B | LIVE, continuous since Jul-21 | See schema below. |

Port probe: http://127.0.0.1:8765/static/overseer.json returned 200 — dashboard server is up; it serves the stale Sep-7 snapshot, so the server is live but that one organ hasn't re-run since the 09-08 rebuild.

## kpi.jsonl schema (P2 replay dataset)

One line, schema `mag_records_kpi.v1`:
`{"schema","ts","source"(pack-status|backfill|summarize,...),"n_sessions","n_complete","n_incomplete","complete_pct","n_leaves","tip_root","incomplete_ids":[...],"note"}`
Jul-21 head: 8 sessions / 2 complete / 25%. Sep-10 tail: 3,538 sessions / 2,696 complete / 76.2%, 7,483 leaves.
Honest note (tri-state): these rows do NOT carry tokens, cache-hit, or cost fields — kpi.jsonl is
records-office health + chain-tip telemetry, re-appended every run (the full incomplete_ids array
per row is why it is 457 MB). Per-turn token/cost/cache telemetry lives elsewhere
(memory/runs/, night_cache_receipts.jsonl, the trajectory envelope), not here.

## Cache/session/memory cards (filenames found, then the 3 read)

Found in watch/ (+inbox): CACHE_YIELD_MATH_20260901, NIGHT_CACHE_RECEIPTS_20260901,
W3_CACHE_IDENTITY_20260907 (inbox), SELF_STEAL_MEMORY_20260901, SELF_STEAL_SESSION_20260902_03,
SELF_STEAL_TRAJECTORY_20260901, SELF_STEAL_TRAJECTORY_STEP_20260905, TRAJECTORY_LENS_20260905,
TRAJECTORY_ENVELOPE_COMPILE_20260905, THE_VERKLE_HOLOGRAM_20260908, VERKLE_FAMILY_SURVEY_20260911
(inbox), NIGHT_MEMORY_AUDIT_20260911 (inbox), AGENT_SESSIONS_DECODE_20260911 (inbox),
SELF_STEAL_ZCODE_SESSION_ORPHANS_20260904, GROUNDING_WAVE.md/.jsonl, SELF_STEAL_MCP_TOPOLOGY_20260904.

1. **watch/GROUNDING_WAVE.md (+.jsonl)** — every claim is one hash-chained tri-state row
   (SUPPORTED/DISPUTED/UNPROVEN), SUPPORTED-without-second-witness auto-demotes (truth-gate v3),
   and the ledger itself now carries the cache arithmetic as verified rows (cache share 0.9437
   CONFIRMED). Doctrine into the OS: memory writes are claims with prev-hash linkage and a
   witness gate — the KV OS inherits the ledger, not a database.
2. **watch/inbox/W3_CACHE_IDENTITY_20260907.md** — falsifier receipt on real ollama prefill
   timers: byte-identical seed = 13.8 ms warm vs 10,711 ms cold (778x, hit_ratio 0.9987);
   one-byte drift at 10% of body (head/system-prompt region) re-costs ~full prefill (9,496 ms);
   tail drift at 95% only 922 ms (tail_retention 0.914). Doctrine into the OS: put mutable bytes
   at the tail — prefix/genome stability IS the cache economy; head drift is the expensive sin.
3. **watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md** — the autopsy of senses spawning host-side:
   28 console children per boot because defaults bypassed the adoption organ. Doctrine into the
   OS: senses/memory live in the cage behind loopback organs (:8765 dashboard, :8001 MCP bridge),
   transport-not-authority, one-sense-one-instance, adoption = three-gate (manifest → real-task
   proof in TTL → kill-switch), senses expire — nothing whitelists forever.

## Top-3 datasets for KV-OS training/replay ore

1. **logs/kpi.jsonl** — 457 MB, LIVE, continuous Jul-21 → today. The only unbroken long-horizon
   telemetry series the fleet owns (including the Aug 16–31 silence window). Replay baseline:
   session-pack health + chain-tip drift over 51 days. (Caveat: summary rows, not per-turn token data.)
2. **dashboard/static/index_data/ESTATE_INDEX.jsonl** — 402 MB, Sep 9. The estate/knowledge index
   itself — corpus-shaped rows; the closest thing to "the memory" as a loadable artifact.
   Pair with orphan_ledger.json (4 MB) for what fell out.
3. **watch/GROUNDING_WAVE.jsonl + dashboard/static/witness_snapshot.json** — the verification
   layer: hash-chained claims with tri-state verdicts, plus the chain witness (root/leaves/tip
   frozen at 09-09). This is the ground truth a replay must check against — what was claimed,
   when, and whether it survived witnesses.

Honorable mention: watch/session_digest.jsonl (5.5 MB) — per-session digests, the pointer layer
from kpi counts to actual session content; watch/active_session.json + monitor_lane.state are the
live write-heads to sample during any replay run.
