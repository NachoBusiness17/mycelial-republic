# LOGS_DEEP_CENSUS_20260911

The logs/ deep census: what the other 4,159+ files hold. Extends
`watch/inbox/RECORD_POOL_CENSUS_20260911.md` (the parent card, which found the pool:
4,160 files, 1.02 GB, Jul 20 - Sep 09, 831 silence-mtime files, kpi.jsonl 457 MB).
Read-only except this file. kpi.jsonl NOT decoded (sibling's lane, per wave protocol).
Method: python os.walk + filename-shape grouping (119 pattern groups), first-line spawn-ts
harvest from ALL 3,959 orchestrator files, chunked regex silence-row counts on every
timestamped ledger, head/tail samples of the top 8 groups and the silence-mtime strays.

## Headline (tri-state)

**"Aug 16-31 silence" is a CHAIN silence, not an ACTIVITY silence — SUPPORTED, measured.**
The fleet ran and recorded every single day of the window. The logs/ pool alone holds
~186,000 timestamped silence-window rows + 803 orchestrator agent-transcripts whose
content-days tile Aug 16-31 with **zero missing days**. The era ran mostly on LOCAL
ollama (1,444 provider mentions in silence spawn queries vs 146 deepseek, 29 grok,
1 z_ai) — the quiet was a quiet channel to the outside, not a dead fleet.

## 1. The group table (top groups by bytes; 119 shape-groups total)

Physical layout: `logs/` is 98% one flat subdir — `orchestrator/` 3,959 files + root 203.
File count 4,162 at this walk vs parent's 4,160 — trivial delta (live logs still
appending between walks). mtimes are local time; silence = Aug 16 00:00 - Sep 1 (matches
the parent's 831 exactly in local, 833 in UTC).

| Group | Files | MB | mtime span | sil | Format / what's inside | Session-bearing |
|---|---|---|---|---|---|---|
| kpi.jsonl | 1 | 457.3 | 09-09 | 0 | `mag_records_kpi.v1` pack-status ledger w/ tip_roots+session ids, from 07-21 — **NOT DECODED, sibling's lane** | yes (parent card) |
| dashboard_sv.err.log | 1 | 179.6 | 09-09 | 0 | uvicorn BrokenPipe tracebacks, NO timestamps | no — noise |
| orchestrator/t*.out.log | 3,954 | 28.3 | 08-03..09-09 | **815** | per-spawn agent transcript; line 1 = `--- <ISO-ts> spawn: <cmd --query ...>`, then FULL stdout incl. tool-call traces + provider tag | **YES — deepest** |
| backend_sv.log (+err) | 2 | 57.3 | 09-09/09-08 | 0 | uvicorn `/health` access lines, NO timestamps | no — noise |
| dashboard_sv.log | 1 | 55.1 | 09-09 | 0 | dashboard HTTP access lines, NO timestamps | no — noise |
| usage.jsonl | 1 | 53.2 | 09-09 | 0 | per-action JSONL: ts, lane (L0/L1), action, detail (incl. query text), session_id; 07-20 -> | **YES** |
| behavioral_events.jsonl | 1 | 39.7 | 09-09 | 0 | ts, kind (collapse/queue_enqueue/pro_fire), detail, tool, session_id; 08-04 -> | **YES** |
| failure_kb.jsonl | 1 | 26.2 | 09-09 | 0 | tool_fail KB: ts, sig, tool, error, session_id; 08-05 -> | **YES** |
| ghost_sv.log (+err) | 2 | 24.1 | 09-09/09-08 | 0 | ghost-daemon boot + `/api/v1/health` lines, NO timestamps | no — noise |
| mag_launch.log | 1 | 19.7 | 09-09 | 0 | **timestamped** spawn/respawn supervisor ledger, UTC, from 08-03 — what-ran-when spine | process-level |
| provider_usage.jsonl | 1 | 17.4 | 09-09 | 0 | per-call: ts, provider, model, tokens, cache_hit, latency, session_id; 07-20 -> (day one = ollama gemma:2b, xai grok-3-mini 403) | **YES** |
| api_gateway_sv.log | 1 | 13.7 | 09-09 | 0 | MCP/room gateway access lines | weak |
| supervisor.jsonl | 1 | 10.1 | 09-09 | 0 | process started/stopped JSONL, ts, from 08-08 | process-level |
| mag.jsonl | 1 | 8.0 | 09-09 | **0** | pre-Docker desktop-cycle decision ledger; **last row 2026-08-11, never resumes** — timeline anchor | era-anchored |
| lab_desk_ops.log | 1 | 7.8 | 08-23 only | 1 | desk_ops restart markers + session=uuid loop, ends 08-23 21:26 | sessions |
| mirror_sv.err.log | 1 | 6.2 | 08-26 | 1 | bare HTTP GET lines, no ts | no |
| lab_sv.log (+err) | 2 | 6.4 | 08-31 | 2 | lab daemon stdout | weak |
| multi_smoke_*.json | 86 | 0.22 | 07-20..09-07 | 0 | `multi_smoke.v1` self-test receipts, ts in name+body, verdict PASS | model-config history |
| All other root singletons | ~50 | ~5 | 08-03..09-08 | 14 | see section 3 | mixed |

## 2. Silence coverage map (Aug 16-31)

Silence-MTIME files: **831 = 815 orchestrator + 16 root** (lab_desk_ops, lab_sv+err,
mirror_sv.err, queue_events, supervisor_autorun, supervisor_ghost, seat_crashes,
scribe_sv, api_gateway, cache_ab_probe, consensus_witness, queue_gate_claims,
docker_watchdog, + 2 stray .py files).

Silence-CONTENT (first-line spawn ts of the 815 silence-mtime orchestrator files):
**803 of 815 carry spawn timestamps INSIDE Aug 16-31** (12 = mtime/same-day edge).
They are one-shot spawn transcripts, never rotated — silence-mtime = silence-content.

| Day | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spawns | 26 | 153 | 13 | 48 | 23 | 51 | 56 | 62 | 8 | 3 | 1 | 6 | 27 | 20 | 85 | 221 |

Whole-span check (08-03..09-09, 38 distinct days): **zero days without orchestrator
spawns.** The low-water days are 08-24..08-27 (1-8 spawns/day) — a real activity dip
mid-window, then re-ramp into Aug 30-31 (306 spawns in two days).

Silence-CONTENT rows in the timestamped ledgers (regex-counted):

| Ledger | Silence rows | Total MB | Span |
|---|---|---|---|
| mag_launch.log (lines) | 54,484 | 19.7 | 08-03 -> |
| usage.jsonl | **40,259** | 53.2 | 07-20 -> |
| behavioral_events.jsonl | **36,285** | 39.7 | 08-04 -> |
| failure_kb.jsonl | **27,740** | 26.2 | 08-05 -> |
| provider_usage.jsonl | 12,909 | 17.4 | 07-20 -> |
| supervisor.jsonl | 11,275 | 10.1 | 08-08 -> |
| tesuji_shells.jsonl | 2,056 | 1.1 | 08-05 -> (see note) |
| queue_events.jsonl | 639 | 0.54 | 08-09..08-31 04:04Z |
| memory_events.jsonl | 204 | 0.17 | (Sep-era file, rows back-dated? verify at use) |
| boot_coordination.jsonl | 70 | 0.06 | (Sep-era file) |
| claims.jsonl | 67 | 0.12 | (Sep-era file) |
| mag.jsonl | **0** | 8.0 | **died 08-11, no post-gap rows** |

Notes: (a) `tesuji_shells.jsonl` is a DIFFERENT organ from the Sep-6 TESUJI_MAP charter
(same word, earlier coinage) — a surprise-capture ledger (`what`/`surprise`/`maps_to`/
`tags`, cf. sample: the 4-year Wi-Fi WlanSvc fix), and it captured 2,056 rows through the
silence. (b) `mag.jsonl` + `lab_desk_ops.log` + scribe WinError->/app path shifts mark the
desktop->Docker pivot: desktop cycle last decision 08-11, chain genesis 08-12 (per
GHOST_GAP_HUNT_20260911), "Docker-only runtime is active" blocks in supervisor_autorun
afterward.

## 3. The silence-mtime samples (5+, verdict: CONTENT, not rotations)

1. `orchestrator/t015d4741b1.out.log` (mtime 08-17, content-day 08-17): `[verkle]
   backfill-sessions --all --provider ollama` — the silence era was BACKFILLING the chain
   from local models. Full agent stdout inside.
2. `orchestrator/t0026f990dc.out.log` (08-23/08-23): `[janitor] FKB signal
   'guard_registry:...' has 71 occurrences. Read logs/failure_kb.jsonl tail 50...` —
   self-maintenance loop reading its own failure KB.
3. `orchestrator/t0233378295.out.log` (08-29/08-29): same janitor loop, run_shell FKB
   signal, 45 occurrences — the loop ran daily through the quiet.
4. `queue_events.jsonl` (08-31): drain_start events through 08-31 04:04Z with queue/task
   ids + tier + goal text ("mission", "goal one/two/only goal") — the queue lived.
5. `supervisor_autorun.out.log` (08-31): janitor prune counts + repeated
   `[autorun] blocked: Docker-only runtime is active` — the respawn-law successor
   enforcement, mid-silence.
6. `grok_tandem_review.py` (08-17, 5.4 KB): NOT a log — a silence-era primary artifact:
   the tandem code-review driver quoting the operator verbatim 2026-08-17 ("dont repeat
   work have them work together...") and naming seats nacho=mine / sd=write.
7. `vast_real_pricing.py` (08-17, 1.4 KB): Vast.ai 48GB-GPU pricing probe incl. the
   hidden disk-fee lesson — pre-Rocinante GPU shopping, mid-silence.
Verdict: silence-mtime files hold silence-era CONTENT (agent transcripts, queue drains,
crash tracebacks, drivers). Zero of the sampled 11 are empty rotations.

## 4. Recovery ranking for the retro-knotter (what feeds it, best first)

1. **orchestrator/t*.out.log — TOP PAYOUT.** 3,954 self-contained agent transcripts,
   each opening with an exact spawn ts + full command/query + full stdout incl.
   tool-call traces; filename `t<hex>` = session id `orc-t<hex>` (pairs with
   memory/agent_sessions/, cf. AGENT_SESSIONS_DECODE_20260911). 803 cover the silence.
   A knotter can walk it date-ordered with zero parsing ambiguity: line 1 IS the knot seed.
2. **usage.jsonl** — 40,259 silence rows; per-action ts + lane + detail strings (query
   text snippets) + session_id. The session timeline spine; join key = session_id to #1.
3. **behavioral_events.jsonl + failure_kb.jsonl** — 36,285 + 27,740 silence rows; what
   broke, collapse nudges, tool failures. The failure narrative of the quiet month.
4. **provider_usage.jsonl** — 12,909 silence rows; exact provider/model/tokens/cache per
   call. Proves and prices the local-ollama era.
5. **mag_launch.log + supervisor.jsonl** — 54,484 + 11,275 silence rows; process spine
   (spawn/respawn/stop per hour). Answers "what was alive" for any silence timestamp.
6. **tesuji_shells.jsonl** — 2,056 silence rows of PRE-DIGESTED surprises with
   maps_to + tags; cheapest re-knotting of all (semantic, not mechanical).
7. **queue_events/claims/boot_coordination/memory_events.jsonl** — 980 silence rows
   total; goal-level intent log (what the fleet thought it was doing).
8. **Strays** — grok_tandem_review.py + vast_real_pricing.py (silence-era primary
   artifacts, quote the operator), lab_desk_ops.log, seat_crashes.log (crash narrative).
9. **Near-zero for history** (~320 MB of the 1 GB): dashboard_sv.log/.err,
   backend_sv.log, ghost_sv.log, mirror_sv.err, api_gateway_sv.log — timestampless
   HTTP/health noise. Exclude from knotting; keep only as liveness evidence.
10. **mag.jsonl — wrong era.** Rich pre-gap record (07-20..08-11 desktop-cycle
    decisions) but ZERO silence rows; it anchors the pivot, not the silence.

## Tri-state footnotes

- **Silence = chain-silence not activity-silence: SUPPORTED** (803 content-day-tiled
  transcripts + ~186K timestamped rows; zero missing days).
- **Silence era ran on local ollama: SUPPORTED as mention-count in spawn queries**
  (1,444 vs 146 deepseek); exact call share lives in provider_usage.jsonl (12,909
  silence rows) — UNPROVEN until that ledger is aggregated.
- **kpi.jsonl spans the silence continuously: UNPROVEN here by protocol** (sibling's
  decode; parent card's claim stands as recorded).
- **4,162 vs 4,160 file count: SUPPORTED trivial delta** (still-appending live logs).
- **memory_events/claims/boot_coordination "silence rows": DISPUTED as contemporaneous**
  — files are Sep-era mtimes holding some back-dated ts rows; verify before knotting.

Absorbed: RECORD_POOL_CENSUS_20260911 (parent), GHOST_GAP_HUNT_20260911 (chain genesis
08-12, pre-chain strata), AGENT_SESSIONS_DECODE_20260911 (orc-t session states),
DESKTOP_HOMECOMING_20260909 (inbox baseline), CENSUS_WORKSPACE_20260901 (prior census),
RESPAWN context via AGENTS.md standing wave (Docker-only blocks observed live in
supervisor_autorun.out.log).
