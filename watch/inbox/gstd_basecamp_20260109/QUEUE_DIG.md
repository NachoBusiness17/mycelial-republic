# QUEUE DIG - the queue/ ledger mined from bytes (GSTD basecamp, DIG lane wave 2)

Instrument: `.venv/Scripts/python.exe` os.walk + json parse of declared ids (handoff_id / run_id), scan moment 2026-10-08 (~22:30 local). No content walks beyond queue/ except targeted landing-path existence checks (.meta.json reads, mtimes, 3 globs in memory/research_packs + corpus/steal + mag/).

## 1. SHAPE

- 727 files total under queue/ (os.walk, moment 2026-10-08). Census carrier UNTOUCHED_SURFACES.md read 691 at its 2026-10-09T04:30Z stat moment; the tree grew +36 under it between the two instruments.
- Stale (mtime < 2026-09-18): 651 of 727 = 89.5 pct.
- Oldest file: queue/results/20260725-003128-hermes.json (2026-07-24).
- mtime histogram by month: 2026-07: 4 - 2026-08: 236 - 2026-09: 448 - 2026-10: 39.
- Subdir breakdown (files / stale): handoff 529/516 - results 93/72 - lanes 87/57 - root 9/4 - hermes_247 4/0 - ds_overflow 3/0 - shitpost 2/2.
- Extensions: .md 466 - .json 187 - .jsonl 27 - .txt 24 (all 24 txt are tmp* scratch in results/) - remainder single digits (.py, .log, .xml, .bak).
- handoff internals: 207 of 529 are openclaw OUTBOX ext-*.md inter-agent mail; claude-zai OUTBOX 53; openclaw PATCHES 34 (28 applied / 4 rejected / hooks); root asks 122 (83 .md + 38 .json + 1 gitkeep); the .md root class: STEAL_ 22, GHOST_ 10, BUILD_ 9, DEEP_ 5.

## 2. THE JOIN (asks vs results, by declared id)

Ask side: 34 true asks (json in handoff root). The 4 *.meta.json files are NOT asks - they are inline receipts (ok: true, model, cost, tokens; verified by reading all 4). Result side: 67 result jsons, 67 distinct declared handoff_ids.

- MATCHED (ask id has a queue/results json): 13 of 34 - 7 cloud-* + 6 peer-*.
- UNCLAIMED (ask filed, no queue/results json): 21 of 34. But bytes say most were banked elsewhere:
  - Receipt-in-research_packs (4): DEEP_DIVE_VERKLE_SELFREPLICATION, DEEP_RESEARCH_FLOCKING_GA, STEAL_FREE_COMPUTE, STEAL_MEMLANG_QUANTIZER - each has memory/research_packs/*answer.remote.md + .meta.json ok:true.
  - Landed-in-code, receipt never folded back (6): RenderMan shader system (mag/shader_bus.py 08-10, mag/shader_rib.py 08-11) - Sancho Layer spike (watch/sancho_boot_hook.py 08-08, same day as the ask, + watch/DIALECTIC_LA_sancho.md 09-04) - Session State History (mag/session_card.py 08-04 .. session_bridge.py 08-31 family) - bones-referee (mag/wow_bones_session.py mtime 09-16, the ask date) - index-foldback (watch/inbox/INDEX.json live 10-08, shared_surface validate is a standing command) - VERKLE_RIB (memory/rib/ verkle ribs are core estate now).
  - Superseded (2): cloud-3b5553e28f + peer-9ce633bb4a (09-01, repair Z.AI GLM-5.3-Flash path + stale supervisor) - the 09-25 provider rewire (nous glm-5.3-prime, todo.md) and this session running GLM-5.3 moot it.
  - Superseded by law (1): HANDOFF-2026-08-08-5-item pile reorg - the pile habit is standing AGENTS.md law.
  - STILL OPEN MONEY (6 asks / 3 subjects): magMap VS-Code migration spike, 2 asks (cloud-75a0c7433c + peer-a46efc8273, both 08-08), zero landing trace anywhere (no magmap/webview/vscode files) - 3x taskold-files-probe (09-29, assignee grok per their .md twins, 9d old, unreturned) - qwen-wire-test-20260807 (trivial wire probe).
- ORPHANS (result with no ask): 0 true orphans. The other 54 result jsons are SELF-ORIGINATED runs that never had an ask file: hermes/harness timestamped probes, glm_coder/grok_build_coder/codex_coder runs, grokterm r1 pairs. Of the 54: 24 ok:true, 28 ok:false, 2 unparsable/other (20260808-184418-harness.json is not valid JSON).

## 3. THE OLD MONEY (July-August)

- The July mass is 4 files only: 3 hermes probe results (all 07-24, all FAILED - gemma:2b 8K context below the 64K Hermes minimum) + 1 tmp scratch. The lesson is already codified (AGENTS.md tiers gemma:2b as janitor scut, never Hermes); the files themselves are dead weight.
- The real old money is 2026-08-08: one operator fan-out of 4 goals to 8 asks (cloud + peer duplicates). Bytes verdict: 3 of 4 goals landed (shader system, sancho hook, session-state family) - 1 goal never landed: the dashboard-into-VS-Code migration (magMap.direct webview). Cross-check vs queue/todo.md: zero sancho/renderman/session-state-history hits (dead subjects); referee + supervisor + glm-5.3 hits all belong to newer, closed rows. The dashboard still lives at :8765 (mag.cmd lab) - the migration subject is 61 days unanswered, not obsolete.

## 4. VERDICT (compost law)

- DEAD - delete-class: 24 tmp*.txt in queue/results/ (tmp scratch; census already flagged tmpvlnnejkn ZERO). Revival condition: any tmp file cited by watch/inbox/INDEX.json stays.
- DEAD - archive to queue/results/archive-2026-07-08/ (move, never delete): the 54 self-originated run jsons older than 2026-09-18 (keep the 09-21 hermes + 09-25 grok47 rows in place, they are recent-era evidence). Why: smoke-probe record whose lessons (gemma context floor, harness wiring) are codified; revival condition: a hermes_burn or cost audit cites them.
- DEAD - archive wholesale: openclaw OUTBOX 207 ext-*.md + claude-zai 53 + other OUTBOX mail (inter-agent cache, pre-shared-surface era; the shared inbox contract superseded it). Revival condition: a verkle-chain audit of agent mail needs the corpus.
- LIVE - keep in place: queue/todo.md (fresh 10-07), STANDING_RAILS.md (10-07), PITCHES_NEXT.md (09-30), queue_index.jsonl (+ its lock log), hermes_247/, ds_overflow/, lanes/ (57 of 87 stale but the lane dirs are the running fleet's own surface - prune lane-by-lane only with the owning lane's say).
- UNCLAIMED-MONEY - surface to operator: (1) the magMap VS-Code migration, 2 asks 61d cold, the only 08-08 goal with zero landing - re-ask or kill it; (2) the 3 grok old-files probes (09-29) - this basecamp census covers their ground, so close them with a pointer to UNTOUCHED_SURFACES.md or let grok return; (3) qwen-wire-test - close as dead.
- STRUCTURAL FINDING: the estate law "unbanked work is lost work" is violated in the opposite direction here - 0 orphan results, but 10+ asks whose work landed in code or research_packs while the queue receipt never came back. queue/results stopped being the truth ledger around 08-08; watch/inbox (shared surface, INDEX.json) is the live ledger. Recommendation: freeze queue/results + handoff root as a pre-shared-surface historical surface (one INDEX row saying so), route all new ask/result traffic to the shared inbox, and only the LIVE set above stays mutable.

Numbers recap (all instrument-cited above): 727 files / 651 stale / asks 34 / matched 13 / unclaimed 21 (of which open money 6 asks, 3 subjects) / orphans 0 / self-runs 54 (24 ok, 28 fail, 2 other) / tmp scratch 24.
