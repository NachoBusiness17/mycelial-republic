# VC1 — FULL CENSUS / verkle crawl (VC seat)

- **When:** 2026-09-16 (night, after WEAVE_SYNTHESIS 18:55)
- **Who:** VC seat, wave_20260916
- **Mission:** operator: "do a complete verkle crawl — you are missing a whole lot." The fold (F1_FOLD_STATE + WEAVE_SYNTHESIS) claims full coverage. Crawl EVERYTHING, find the missing mass.
- **Method:** `find`/`du` full census of memory/, state/, watch/, queue/, docs/, basecamp/, artifacts/, training/, mag/ — size + mtime per directory; cross-check against WAVE_STATE_20260916.md and the deck (N1_COMMAND_DECK, WEAVE_SYNTHESIS, F1_FOLD_STATE). No paid APIs, git read-only only.
- **Status:** CRAWL IN PROGRESS — appends below as lanes complete.

## Total sizes (du -sh, first pass)

| region | size |
|---|---|
| memory/ | 4.9G |
| state/ | 40M |
| watch/ | 1.3G |
| queue/ | 8.0M |
| docs/ | 32M |
| basecamp/ | 16K |
| artifacts/ | 257M |
| training/ | 0 (EMPTY — see §training below) |
| mag/ | 51M |

## Pass 1 — memory/ subdirectory sizes (du, 4.9G total)

| subdir | size | note |
|---|---|---|
| runs/ | 1.1G | partially touched tonight (salon_50 receipt check only) |
| ingest/ | 1.1G | NOT in fold scope |
| biography_backup/ | 769M | NOT touched |
| biography/ | 403M | expected suspect — NOT touched |
| corpus/ | 310M | expected suspect — NOT touched |
| biography_backup_20260825/ | 268M | NOT touched |
| ghost/ | 207M | NOT touched |
| training/ | 192M | (memory/training — distinct from empty top-level training/) NOT touched |
| agent_state/ | 161M | NOT touched |
| seals/ | 105M | NOT touched |
| agent_sessions/ | 75M | NOT touched |
| vault/ | 46M | NOT touched |
| bard/ | 37M | NOT touched |
| improve/ | 24M | NOT touched tonight |
| thinking/ | 22M | NOT touched |
| briefs/ | 16M | cited (latest.md) but not crawled |
| mail/ | 15M | NOT touched |
| working/ | 9.0M | NOT touched |
| trajectory/ | 5.9M | NOT touched |
| research_packs/ | 4.9M | NOT touched |
| biography_backup_flag_* ×3 + postrepair | ~17M | NOT touched |
| agent_uploads/ | 4.1M | NOT touched |
| percolator/ .. game_modules/ | 2.7M → 80K | ~40 more dirs, small but content-dense (incl. dead_drops 668K, steal 811K, audit 137K, game 569K, game_modules 80K) |

### CORRECTION to first table
- `training/` du reported **0 allocated** but `ls` shows **events.jsonl = 197,301,287 bytes (~197MB)**, mtime Sep 16 **19:05** (mid-crawl, actively appended) + cost_ledger.jsonl 1.5MB @ 17:32. It is a live telemetry firehose, not an empty dir. Trust bytes, not du.

### watch/ — what is OUTSIDE the inbox (1.3G total, fold scope was only wave_20260916 + physical_computing receipts)

| item | size | note |
|---|---|---|
| watch/ESTATE_INDEX/ | 450M | estate index store — fold never mentions it |
| watch/engine_e1.log | 246M | single log file |
| watch/bay/ | 133M | not indexed tonight |
| watch/overnight_churn.log | 127M | single log file |
| watch/inbox/ | 88M | fold only covered 2 subdirs of this |
| watch/organs/ | 63M | not indexed |
| watch/engine_b1.log | 23M | log |
| watch/KG_STORE/ | 22M | knowledge-graph store — not indexed |
| watch/verkle_construction/ | 728K | verkle knots live here, not state/ |
| watch/salon_responses/ (est.) | see §pass3 | expected suspect: astra_smoke_12 raws live here (A4 receipt) |

### state/ (40M)

- arxiv/ 8.8M · vast/ 2.7M · shadow_work/ 1.9M · memweave/ 1.5M · world/ 833K · auth_switchboard/ 226K · cloudflared/ 138K · backups/ 94K · **fuel/ 36K (expected suspect)** · memory/ 8K · keeper_world/ 8K · gstd/ 4K
- state root: ~30 status md/json files; freshest: CURRENT.md 09-15, LIVE_REPORT.md 09-16 07:38, START_BRIEF.md 09-16 08:01, aos_carrier.lock 09-16 18:51 (daemon alive during wave)

### other top-levels

- **basecamp/** = 3 files only (16K): README + BUBBLE_HOLO graphy_RESEARCH.md + CACHE_FARMING_GAME_GENOME.md, written **Sep 16 01:21–06:51** — the PRE-DAWN design morning, outside wave scope, uncited by the fold.
- **artifacts/** = 257M of which **vertigo_boat_20260908/ = 256M** (Sep 8, uncrawled); the rest is tonight's salon_ess + third_smile + quiet_forge (wave-touched).
- **queue/** = 8M: handoff/ 6.5M, lanes/ 1.2M, results/ 301K — fold requeued stubs into prose but never enumerated queue/handoff backlog.
- **docs/** = 32M: **report_v1/ = 24M** (uncrawled), ref/ 5.5M (incl. tesuji/ — sampled below), mirrors/ 1.9M.
- **mag/** = 995 top-level modules, 3,225 files total, 51M. Fold's code checks verified only ~10 named files (wow_world, wow_player, hydro_xor_sim, link_library, toy.html, test files).

## Pass 2 — file counts + mtime spans (memory/ key dirs)

| dir | files | newest | oldest |
|---|---|---|---|
| runs/ | 42,631 (360 run dirs, **7 dated tonight**) | 2026-09-16 19:03 | 2026-06-17 |
| ingest/ | 958 | 2026-09-16 17:24 | 2026-03-20 |
| biography/ | 38,969 | 2026-09-16 19:06 | 2026-07-20 |
| ghost/ | 140,101 | 2026-09-16 19:06 (leak reports ~every minute) | 2026-08-07 |
| corpus/ | 22,144 | 2026-09-14 | 2024-10-01 |
| training/ (memory/training) | 24 | 2026-09-16 17:32 (cost_ledger) | 2026-08-06 |
| agent_state/ | 35,901 | 2026-09-16 13:50 | 2026-07-28 |
| seals/ | 143 | 2026-09-05 | 2026-08-12 |
| agent_sessions/ | 2,794 | 2026-09-16 17:24 | 2026-08-02 |
| vault/ | 46 | 2026-09-11 | 2026-09-11 |
| briefs/ | 3,675 | 2026-09-16 17:24 | 2026-07-21 |
| mail/ | 4,411 | 2026-09-16 19:09 (live heartbeats) | 2026-08-03 |
| dead_drops/ | 537 | 2026-08-30 | 2026-08-12 |
| steal/ | 141 | 2026-09-08 | 2026-08-08 |
| audit/ | 12 | 2026-09-05 | 2026-09-04 |
| game/ | 21 | 2026-09-16 07:38 (FLOW_LEDGER — pre-wave) | 2026-08-14 |
| game_modules/ | 7 | 2026-09-14 | 2026-08-06 |
| archaeology/ | 2 | 2026-09-14 | 2026-09-14 |
| bard/ | 2 | 2026-09-16 19:07 (chronicle 17.2MB live) | — |

## Pass 3 — what the untouched regions HOLD (samples, one line each)

- **memory/ingest/registry.jsonl** — 1,121,310,960 bytes, ONE file, updated 17:24 tonight: the machine's master ingestion registry; `catalog.json` beside it. The deck's own INDEX health line (ok=False, 98 errors, 389 unindexed) points HERE; nobody followed.
- **watch/ESTATE_INDEX/** — ran TODAY 13:12Z: `total_files: 1,468,831, total_bytes: 44.6GB` across local_sovereign_agent (981k files), _mimosa (292k), vmangos-core, tortoise-wow, azerothcore-wow (10,436), Mag-backup_git. A pre-built full-estate census, unread.
- **memory/ghost/** — canary/leak-defense program: `leak_reports/` = 180M of minute-by-minute scans running all through tonight's wave (`0/10 canaries breached, 0 collusion` — no contradiction, but a live security organ no receipt acknowledges); plus noise/ 28M, x_surface, tesuji_probes.json.
- **memory/corpus/shadertoy21k/** — 21,809 shader files (183M: `codes/` + `all_codes.zip` + gdown.log). G3_SHADER_AUDIT (STUB, "full shader inventory" requeued) sits on top of a corpus that was never opened.
- **memory/corpus/ractors/** — 124M persona/ractor corpus: per-thinker dirs (adams, alan_moore, baudrillard, bernays…), TRAINING_INDEX.md, WISH_LIST.md, ESOTERIC_LENS_ON_THE_STACK.md. P1 tonight built a standalone `ractor-salon` plugin without citing 124M of existing ractor canon.
- **memory/game/FRONTIER_SOULS_CANON.md** (Sep 15) — buildable canon from Adam's bible: 8-omen SIGNS draft, two-clocks law, mud-steals list. U6 tonight generated "Frontier Souls SIGNs + NPC voices" without it.
- **memory/game_modules/** — 7 JSON game modules: riddler_engram, riddler_optics, fractal_maze, water_computer, dnd_classic_stub, adventure_2d6_stub, audit_dungeon. R2's 20-subsystem matrix and HG2's orphan list never named them.
- **memory/biography/** — the biographer substrate: 39k files; per-session dossiers (uuid.md/.pdf/.dossier.json), `verkle_chain.jsonl` (5.9MB, appended 19:06 tonight), `verkle_tip.json`, knots/, topic_evolution.json (356KB). The deck read ONE tip hash; the chain itself was never crawled.
- **memory/bard/** — `chronicle.md` 17.2MB "The Mycelial Chronicle — the system's full memory" + `breadcrumbs.jsonl` 21.5MB, both written 19:07 tonight. A parallel narrative history that no receipt reconciles against.
- **memory/dead_drops/** — 537 flock-control drops (dd-*.json): `{"domain":"control","flock_rule":"cohesion","instruction":"hold the invariants… aim at the coldest vertex; steal-and-adapt…","status":"dr[opped]"}` — a distributed-coordination layer, idle since Aug 30.
- **memory/steal/** — 141 steal-research markdowns (STEAL_MATRIX lineage: 555_HOLOGRAM_PLAY_MATH, GRAYSWAN_ARENA_STEAL kin, CONTEXT_GROWTH_STEAL…), idle since Sep 8.
- **memory/audit/** — 12 files: aud_orphans.json, aud_memory.json, aud_research.json, gene_pool_gen1/gen2.json — an EXISTING orphan audit D24's triage memo did not compare against.
- **memory/archaeology/** — 2 files: SYSTEM_PROMPTS_LEAKS_20260914.md + prompt_findings.jsonl (26KB) — Sep 14 prompt-leak findings, two days pre-wave, uncited.
- **docs/ref/tesuji/** — 7 diary notes (Aug 5–29): zeitgeist-amish-plain, water-computer-day-for-night, intention-fidelity-routing, grok46-tui-organs. The tesuji scores in ghost's leak reports reference this lineage.
- **docs/report_v1/FRONTIER_REVIEW_001.md** — a finished expert review of trace-as-state/KV-eviction prior art (RoleKV/PBKV/CacheWise beat LRU 1.5–2.5×; "Belady MIN, not Bellman"; DeepSeek/GLM numbers). B10's "MLP-as-KV-cache REDISCOVERED" verdict was filed without it, 6 hours later.
- **state/world/FOUNDING_RECORD.md** — world-0 founding record, sealed Sep 5: door/add/v1 hash-commitment law with SHA256 chain + WORLD LAW 1. Tonight's referee chain (A1 blind set, A2 engine) re-derived commitment-hash epistemics next to a sealed instance.
- **state/fuel/** — lite_pacing.jsonl + lite_quota_log.jsonl, appended through tonight (`concert001 burst Q2 retry 1868 tokens`, `research_fanout lane zai-lite`). CONCERT001's "$0 cash, 0.15 Lite credits" claim draws on this ledger; the fold never read it.
- **basecamp/** — 16K, two whole programs mined 2026-09-16 pre-dawn: BUBBLE_HOLOGRAPHY_RESEARCH ("complete expert-review brief awaiting domain reviewers", DORMANT) + CACHE_FARMING_GAME_GENOME ("LIVE — feeds the Astra bundle"; its core law "cache the contract, compute the delta" claims three same-night independent appearances). Outside wave scope; fold never saw them.
- **queue/handoff/** — 158 files (6.5M) incl. STEAL_MINE_DIAMONDS.md and HANDOFF-2026-09-16-index-foldback.json (TODAY). Fold requeued stubs as prose but never enumerated the standing handoff backlog.
- **training/events.jsonl** — 197MB live firehose of `mag_training_event.v1` rows (route_decision, percolator tags, exportable T2), appended at 19:07 tonight through the whole wave. `cost_ledger.jsonl` 1.5MB @ 17:32. The wave ran inside a training-data engine that no receipt mentions.
- **artifacts/vertigo_boat_20260908/** — one 256MB mp4 (tokyo_river_depth_1080p.mp4), Sep 8. Bulk, low surprise.
- **watch/ logs** — engine_e1.log 246M + overnight_churn.log 127M + engine_b1.log 23M ≈ 396M of raw engine logs, uncrawled.
- **watch/KG_STORE/** 22M (catalog.jsonl + pdf store) · **watch/organs/** 63M (kimodo, tale_re_encoder) · **watch/bay/** 133M (claims/locks/logs/repair/state — the session-lock surface HG1's "wow_world zero live sessions" verdict never checked).
- **memory/seals/** 105M, 143 files, newest Sep 5 (three seal ceremonies) · **memory/vault/** 46M Sep 11 (astra_v2_companions, session_20260911) · **memory/agent_sessions/** 75M · **memory/agent_state/** 161M/35,901 files · **docs/mirrors/mcp** 1.9M.
- **Worktrees (7 registered in .git/worktrees):** 4 codex scratch worktrees (…/.codex/worktrees/{b13a,6654,ef82,efa1}/local_sovereign_agent — 737 files each, stale since Aug 31–Sep 1), mag_env_dashboard_v3, mag_test_env, salon-arena-mvp. **No literal "sovereign-mirror" worktree found** — the suspect-list name is itself a fossil; closest live mirror is docs/mirrors/ + docs/ref/MIRROR_PRESENTED.md.

## Pass 4 — fold-coverage cross-check (WAVE_STATE + deck vs disk)

1. **Fold count "60 receipts" was stale on arrival.** wave_20260916/receipts now holds 63 files (VC1/VC2/WEAVE post-date it); physical_computing/receipts grew 25 → **51** md receipts post-fold (K1–K11 series: STAMETS_CORPUS, GALVANOTROPISM, EMBEDDED_TRACES, CAPILLARY_DESIGN, ION_DOPING, LATTICE_FARADAY, LOWV_BIO, PRIOR_ART, STEERING_TOOLKIT, LIVING_MATERIAL_SENSING; plus G-* series: SPECIES_DATA, SPINOR_LATTICE, FLUID_LOGIC_LIBRARY, WRITE_MECHANISMS, COCULTIVATION, PRINTABLE_FAB, INSTRUMENT_TIER, SIGNAL_MAGNITUDE). ≈ **30+ receipts tonight's index never saw.**
2. **Deck** (N1) covered: 11 queue/lanes, LINKS 174, GROUNDING verify (FAIL row 122, chain broken — no owner assigned), INDEX health (98 errors), 7 games, latest-8 receipts, git tip. It did NOT cover: memory/*, ingest registry, estate index, corpus, basecamp, queue/handoff, state/*, worktrees.
3. **HG2 "58-row owned inventory"** (our corpus weave) excludes: shadertoy21k (183M), corpus/ractors (124M), memory/game_modules, memory/game canons, vertigo_boat, KG_STORE — the largest corpora we own are absent from the "our corpus" weave.
4. **Every post-fold writer was live during the crawl** (ghost 19:06, bard 19:07, mail 19:09, biography 19:06, training 19:07, improve 19:09): the "fold" is a snapshot of a moving organism; the deck even admits liveness (tip moved mid-build).

## THE MISSING MASS — ranked by size × staleness × surprise

Scores: size S = bytes (1 tiny … 5 ≥250M); staleness T = days since last write as felt tonight (1 live … 5 ≥30d); surprise X = how much it changes tonight's picture (1 … 5). Rank = S×T×X (defensible ordering, not arithmetic worship).

| # | region | size | last touched | what it changes | S | T | X | SxTxX |
|---|---|---|---|---|---|---|---|---|
| 1 | ~30 post-fold receipts (K1–K11 + G-* in physical_computing; VC/WEAVE in wave) | ~0.5M | tonight, post-fold | fold's "60 receipts indexed" already false on its own disk; gen-2 requeue list is incomplete by ~10 K/G stubs it never saw | 1 | 1 | 5 | 5 |
| 2 | memory/ingest/registry.jsonl + catalog | 1.1G | tonight 17:24 | the master ingestion ledger exists, 1.1GB, and INDEX says 98 errors / 389 unindexed — the fold indexed receipts while the indexer itself is sick and unowned | 5 | 1 | 5 | 25 |
| 3 | watch/ESTATE_INDEX (last_run today) | 450M | today 13:12Z | a 1.47M-file / 44.6GB census of the WHOLE estate (incl. vmangos/tortoise/azerothcore + _mimosa) is pre-built and unread — "crawl everything" was already machine-done once and nobody consumed it | 5 | 1 | 5 | 25 |
| 4 | memory/biography (verkle chain + 39k files) + 4 backup copies (1.44G total) | 1.4G | tonight 19:06 | tonight's verkle picture = ONE tip hash; the 5.9MB chain, knots/, topic_evolution are the actual substrate the operator asked to crawl; 4 near-duplicate backups (769M+268M+17M) are D24 triage targets the memo missed | 5 | 1 | 4 | 20 |
| 5 | training/events.jsonl + memory/training | 389M | tonight 19:07 | the wave itself is being recorded as exportable training events (percolator, T2) in real time — an unacknowledged consumer of everything tonight produced | 4 | 1 | 4 | 16 |
| 6 | memory/ghost (canaries, 140k files) | 207M | tonight 19:06 | a leak-defense organ ran all night (0/10 breached) — tonight's "secure" picture is luckily true but was never checked against the one organ that checks it | 4 | 1 | 4 | 16 |
| 7 | memory/corpus/shadertoy21k | 183M | Sep 14 (2d) | G3 shader audit stub requeued "full inventory" while 21,809 shaders sit 2 days old, unopened — the audit's corpus is the audit's missing mass | 4 | 2 | 4 | 32 → but X caps at audit scope; net rank high |
| 8 | watch engine logs (e1 246M, churn 127M, b1 23M) | ~400M | tonight | ~400M of engine/churn logs nobody reads; "overnight churn" is presumably where the operator's missing mass went last time | 5 | 1 | 2 | 10 |
| 9 | memory/corpus/ractors | 124M | Sep 14 (2d) | P1 shipped a ractor package into a world that already has a 124M ractor canon + TRAINING_INDEX + WISH_LIST — naming collision risk, prior art uncited | 4 | 2 | 4 | 32 |
| 10 | docs/report_v1 (FRONTIER_REVIEW_001 + KVOS bibliography) | 24M | pre-wave | a finished frontier/KV prior-art review CONTRADICTS-ADJACENT to B10's "REDISCOVERED" verdict (Belady vs Bellman; RoleKV/PBKV/CacheWise) — B10 filed without reading the desk's own review | 2 | 2 | 5 | 20 |
| 11 | artifacts/vertigo_boat (one mp4) | 256M | Sep 8 (8d) | bulk only; a 256MB video is 74% of artifacts/ — triage question, not epistemics | 5 | 2 | 1 | 10 |
| 12 | watch/bay (claims/locks/repair) | 133M | tonight | HG1's "wow_world zero live sessions" verdict was written without the lock/claims surface that would know | 3 | 1 | 3 | 9 |
| 13 | queue/handoff (158 files) | 6.5M | TODAY (index-foldback.json) | a standing 158-item handoff backlog incl. TODAY's index-foldback — the fold requeued stubs in prose while a machine queue of asks already existed | 2 | 1 | 4 | 8 |
| 14 | memory/bard (chronicle 17M + breadcrumbs 21M) | 37M | tonight 19:07 | the Silent Bard wrote tonight's full narrative independently; no receipt is reconciled against it — two histories of one night | 3 | 1 | 3 | 9 |
| 15 | state/world (FOUNDING_RECORD, WALL, GOALS) | 833K | Sep 5–15 | a sealed hash-commitment world-law system predates the referee chain; A1/A2 re-derived its epistemics without it | 1 | 2 | 4 | 8 |
| 16 | basecamp (bubble holography + cache-farming genome) | 16K | today 01:21–06:51 | TWO pre-dawn programs — one dormant awaiting expert reviewers, one claiming to feed the Astra bundle — invisible to tonight's wave entirely | 1 | 1 | 5 | 5 (per-byte enormous) |
| 17 | memory/dead_drops (537 flock drops) | 668K | Aug 30 (17d) | a flock-control command layer ("aim at the coldest vertex; steal-and-adapt") went quiet 17 days ago — nobody filed its death | 1 | 4 | 3 | 12 |
| 18 | memory/seals (105M) | 105M | Sep 5 (11d) | three seal ceremonies, 105M, unindexed since — D24 triage never mentioned | 4 | 3 | 2 | 24 |
| 19 | state/fuel (pacing + quota) | 36K | tonight 19:02 | CONCERT001's "$0 / 0.15 Lite credits" is auditable against this ledger and was not audited | 1 | 1 | 3 | 3 |
| 20 | memory/steal (141) + audit (12) + archaeology (2) | ~1M | Sep 4–14 | steal-matrix lineage, a prior orphan audit (aud_orphans.json), and Sep-14 system-prompt-leak findings — three memory systems D24's memory-doctrine memo didn't doctrine | 1 | 2 | 3 | 6 |
| 21 | 7 git worktrees (4 codex, stale Aug 31–Sep 1) | ~10M total | Sep 1 | the "sovereign-mirror worktree" suspect does not exist by that name — fossil in the operator's own map; 4 abandoned codex worktrees still registered | 1 | 5 | 2 | 10 |
| 22 | memory/vault, mail (live), agent_state, agent_sessions, docs/ref (200+ files), watch/KG_STORE, watch/organs, docs/mirrors, salon_responses | ~470M | mixed | long tail: real programs (mailboxes heartbeating, KG pdf store, organ encoders) that no receipt indexes | 4 | 2 | 2 | 16 |

**Net statement:** tonight's fold described a wave; the repo it landed in is a 6.6G+ living estate (memory 4.9G + watch 1.3G + artifacts 257M + training 197M firehose + mag 51M) whose largest organs — ingest registry, estate census, biography/verkle chain, ghost defense, bard chronicle, training events, shader/ractor corpora — were all outside its scope, and ~30 receipts landed inside its own scope after it closed.

## Honest count — claims made without crawling these regions

Enumerated load-bearing claims tonight that rest on evidence in regions never crawled:

1. **Fold §5 "Receipts indexed: 60"** — false within the hour (63 + 51; ~30 unindexed). 1 claim.
2. **B10 "MLP-as-KV-cache REDISCOVERED, hybrid-only survives"** — filed 6h after our own FRONTIER_REVIEW_001 (docs/report_v1) covered the same prior-art ground without citing it. 1 claim.
3. **U6 "Frontier Souls SIGNs + NPC voices — use for voices, edit its morals"** — generated beside an existing FRONTIER_SOULS_CANON.md (8-omen SIGNS draft, two-clocks law). 1 claim.
4. **P1 "standalone ractor-salon plugin repo"** — no reconciliation with the 124M ractor corpus/registry it shares a name with. 1 claim.
5. **G3 stub "next: full shader inventory"** — written without noting 21,809 shaders already on disk to inventory. 1 claim.
6. **CONCERT001 "$0 cash, 0.15 Lite credits"** — never reconciled against state/fuel pacing/quota logs that recorded the same night. 1 claim.
7. **HG2 "58-row owned inventory (our corpus)"** — omits shadertoy21k (183M), corpus/ractors (124M), game_modules, KG_STORE, vertigo_boat: the corpus weave skipped our largest corpora. 1 claim (many rows).
8. **HG1/R2 "wow_world zero live sessions"** — written without watch/bay locks/claims. 1 claim.
9. **Deck "STANDING WAVE" verkle line** — one tip hash; the 5.9MB chain + knots behind it uncrawled (and GROUNDING row-122 break still unowned). 1 claim.
10. **A1/A2 referee-chain novelty** — commitment-hash epistemics re-derived beside state/world FOUNDING_RECORD (sealed Sep 5) without reference. 1 claim.
11. **Memory block line "any 'fired 50/50' line is a fossil"** — asserted without grepping the 17MB chronicle, 15MB mail, 180M leak reports where old lines persist. 1 claim.
12. **D24 "memo-only triage, deletions need human gate"** — made without memory/audit/aud_orphans.json, the biography_backup ×4 pile (1.05G), seals, or ghost. 1 claim.

**Count: 12 load-bearing claims made without crawling the regions that bear on them**, plus the global incompleteness (~30 receipts + every pre-wave region). Zero claims were found flatly contradicted by the uncrawled regions (ghost canaries 0/10 breached; fuel ledger consistent with "0.15 Lite" scale) — the missing mass is **unread, not wrong**: the fold's picture of tonight is accurate for the ~88M of wave files it read, and silent about the other ~99% of the estate it landed in.

Fossil notes for the operator's suspect list: `sovereign-mirror worktree` does not exist by that name (7 other worktrees do); `state/ verkle knots` actually live in memory/biography/knots + watch/verkle_construction; `memory/corpus/shadertoy21k` is real and 183M; `training/` top-level is a live 197MB firehose, not empty.

Receipt closed 2026-09-16 night, VC seat. No git mutations (file reads of .git/worktrees/* only), no paid APIs, $0.


