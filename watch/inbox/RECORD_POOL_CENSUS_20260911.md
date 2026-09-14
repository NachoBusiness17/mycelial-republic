# RECORD_POOL_CENSUS_20260911

The record-pool census: every raw record pool in the estate that could hold fleet
history the chain forgot. Walked with python os.walk; counts, bytes, and spans are
mtime-derived unless noted. Companion to the knot-archive payout (21,479 orphans).
Census run 2026-09-11, read-only except this file.

## The census table

| Pool | Location | Files | Bytes | Date span (mtimes) | Format | Era of fleet history covered |
|---|---|---|---|---|---|---|
| logs/ | `local_sovereign_agent/logs/` | 4,160 | 1.02 GB | 2026-07-20 .. 2026-09-09 | .log 4,006, .json 92, .jsonl 26; dominated by `orchestrator/` (3,957 spawn/stdout logs) | July smoke era (38 files, sparse) through ALL of August incl. the Aug 16-31 silence (831 files mtimed in that window) to today. `kpi.jsonl` (457 MB, `mag_records_kpi.v1`, first row 2026-07-21) is a continuous pack-status ledger with tip_roots + session ids. |
| memory/runs/ | `local_sovereign_agent/memory/runs/` | 21,619 | 595 MB | 2026-07-27 .. 2026-09-09 (June "235 files" = bundled host_browser Chrome profile, not history) | .json 18,436, .md 1,805, per-run `trail.jsonl` | Run-artifact strata from 2026-07-27 (compose-substrate-smoke) to now: orchestrator 12,820, swarm_worker 3,105, flex 1,324, salons 502, session_mining 136, riddler, campaign, brain_reads... |
| ghost trail (inside runs/) | `memory/runs/ghost/trail.jsonl` | 1 | 309.7 MB | content 2026-08-08 .. 2026-09-09 (live, still appending) | JSONL state snapshots w/ recent_events | The ONE continuous unbroken record across the Aug 16-31 silence. Plus `swarm_health/trail.jsonl` (10.7 MB, Aug 09 ->, health_law events) and `steer/` 430 KB, `switchboard/` 87 KB. |
| memory/agent_sessions/ | `local_sovereign_agent/memory/agent_sessions/` | 2,660 | 64 MB | 2026-08-02 .. 2026-09-09 | orc-t*.json per-agent session states | Unlisted pool found via ESTATE_INDEX grep. Full August incl. silence. |
| window/ | `local_sovereign_agent/window/` | 23 | 599 KB | 2026-08-23 only | .md session transcripts (`# Session <uuid>`, "Source: .jsonl") + surface.json | One day: the Aug 23 session-mining outputs. Already-extracted, tiny. |
| mine/ | `local_sovereign_agent/mine/` | 103,949 | 5.75 GB | 2026-08-04 .. 2026-08-06 | .ts/.py/.tsx/.rs source + git packs (largest 1.0 GB pack) | Session-mining SOURCE harvest from other repos — code, not fleet chat. 92% is third-party source trees. |
| watch/inbox/ | `local_sovereign_agent/watch/inbox/` | 245 | 69 MB | 2026-08-11 .. 2026-09-09 | .md 149, .txt 28, .json 25, .png 19, mp4/seg.raw/tar.gz | Operator pastes + research artifacts. 194 were catalogued by DESKTOP_HOMECOMING_20260909; ~51 files are newer/uncatalogued delta. |
| Desktop "New folder" | `C:/Users/foste/Desktop/New folder/` | 248 | 245 MB | 2025-10-05 .. 2026-09-09 | .jpg 35, .mp4 34, .txt 32, .pdf 23, .md 19 | Operator hand-saves. Text saves are the history payload: wow.txt 1,207,024 B (Aug 31), dogfood-trajectory save.txt (Sep 5), compuiter.txt (Aug 30), salon4.txt, ractor-salon-001/002.txt (Sep 9). |
| queue/handoff/ | `local_sovereign_agent/queue/handoff/` | 508 | 5.2 MB | 2026-08-03 .. 2026-09-09 | .md 409, .json 95 | The mesh channel itself: 16 seat dirs. zcode/CONVO.md = 1,055 lines, 577,838 B, still hot. openclaw 244, claude-zai 53, ractors 16, zcode 14, openclaw-worker 13, opencode 8, sherpa_economist 8, autoclaw 7. VERKLE_RIB.json 2.2 MB. |
| corpus/ | `local_sovereign_agent/corpus/` | 42,899 | 5.4 GB | mtimes 2026-09-04..09-06 = docker-cp dates, NOT content era | library 38,824 (4.8 GB ref material), oral_history 3,872 (270 MB), canon 159, training_materials 27, apk 2, telegram 2 | `oral_history/nacho_archaeology/` (3,867 files, 10 zipped parts + extracted + TRANSCRIPT_MAP.txt) = the ancient strata: 92-agent archaeology, visible content Aug 11-14 and earlier. THE pre-Aug-16 pool. |

## Ranked: chain-lost history recovery value

1. **logs/ + kpi.jsonl — TOP PAYOUT, the Aug 16-31 silence lives here.** 831 files
   mtimed inside the silence window; kpi.jsonl is a 457 MB continuous pack-status
   ledger from 2026-07-21 with tip_roots and session ids. SUPPORTED: continuous
   coverage; UNPROVEN: how much conversational (vs mechanical) content survives.
2. **ghost/trail.jsonl (309 MB, Aug 08 -> now)** — the only single-file unbroken
   record spanning the silence; state snapshots + recent_events. Append-only, live.
3. **memory/agent_sessions/ (2,660 orc-t*.json, Aug 02 ->)** — uncovered pool, era
   matches the gap exactly. Needs one sample read to grade depth.
4. **Desktop New folder .txt saves** — wow.txt (Aug 31, 1.2 MB) and siblings are
   operator-hand-saved sessions dated INSIDE/around the silence. Human-curated.
5. **corpus/oral_history/nacho_archaeology** — the ancient strata (pre-Aug-16).
   Already catalogued (TRANSCRIPT_MAP.txt, 92 agents); recovery = re-mining, not
   discovery.
6. **watch/inbox** — partly indexed; ~51-file delta since DESKTOP_HOMECOMING needs
   the standard READ-FILTER-INTERPRET-CITE pass.
7. **queue/handoff CONVO.md + VERKLE_RIB.json** — chain-adjacent and live; this IS
   the signed-adjacent record, not recovery material.
8. **window/** — 23 files, one day (Aug 23), already-extracted transcripts. Low.
9. **mine/** — source-code mining, not fleet history. Near-zero for this purpose.
10. **corpus/library (38,824 files)** — reference corpus, not history. Out of scope.

## Tri-state notes

- **deepseek/grok seat inboxes in queue/handoff: DISPUTED (absent).** No such dirs
  exist. Seats present: autoclaw, autoclaw-2 (empty), cache, claude-zai, intake,
  notion, openclaw-heavy, openclaw-worker, openclaw, opencode, ractors, requests
  (empty), shapes, sherpa_economist, zcode-cli, zcode. Deepseek lives in memory via
  `oral_history/deepseek_share_Q_posts_archives_20260905.md`, not as an inbox.
- **memory/runs June-2026 span: DISPUTED as history.** All 235 "June" files are a
  bundled host_browser Chrome profile; real runs strata starts 2026-07-27.
- **corpus/ content era: UNPROVEN from mtimes.** docker cp reset all mtimes to
  Sep 04-06; era evidence comes from content (TRANSCRIPT_MAP shows Aug 11/14).
- **watch/inbox 245 vs 194 catalogued: SUPPORTED delta of ~51** (mtimes through
  Sep 09; homecoming card counted an earlier snapshot).
- **logs/ July coverage: SUPPORTED but sparse** (38 files Jul 20-31; kpi.jsonl
  itself starts 2026-07-21 — the record system is older than the fleet's day-one).
