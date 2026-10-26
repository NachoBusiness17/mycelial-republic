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

- **WINDOW HANDOFF 09-27 evening (the gate-fix + lens + burn-down + preparedness window; read watch/inbox/WINDOW_CLOSE_20260927_GATEFIX_LENS.md, SUITE_BURNDOWN_20260927.md, NO_SACRED_COWS_20260927.md, PREPAREDNESS_AUDIT_20260927.md):**
  (1) SECRET-GATE ASSIGNMENT-BYPASS FIXED (audit seat found; per-rule
  BLOCKABLE_RES; 4-form proof; named acceptances incl telesco.pe CDN class).
  (2) VERKLE CHAIN BROKE TWICE and is cured: pre-race-root race class;
  post-append self-heal in mag/verkle_knot + standing tools/chain_repair.py;
  orchestrator loops RECYCLED onto guarded code (25+ rows, zero breaks).
  (3) GROUNDING ledger alive again: voids #122/#123 MALFORMED + #105
  EVIDENCE_DEAD executed via v4 verbs, operator-word witnessed; #104 void was
  an OFF-BY-ONE MISFIRE, reversed via void-of-void (designed path, first live
  fire). Falsifier tests v4-aware 3/3, xfails removed. (4) SUITE: 40F -> 12F
  (desk 6 = dashboard spec reconciliation; 6 singles root-caused in
  SUITE_BURNDOWN). (5) QUANTIZER v0.3 standing compiler + DELIVERY: compiled
  laws ride the context pack after L0b objective; stale >7d renders as debt;
  fossil arm registry-driven in 08:30 patrol (configs/fossil_registry.json);
  gene pool TOMBSTONED dead-at-birth (revive = consumer first). (6) THE LENS
  + doctrine verdicts: DRIVING = law-without-measurement (probe20 --live
  >=5 cycles is FIRST next-window action); MEMLANCE unproven coinage; AuK =
  NPC voice piece; sizegame referee pattern; seeded-rumor drill LIVE
  (tools/rumor_drill.py, deadline check at +24h). (7) PREPAREDNESS: seat
  memory mirrored to memory/continuity/seat_memory_20260927/ (382 files);
  operator owes: pack key OFF-MACHINE, xAI rotate, Drive-sync verify,
  second-machine join test. (8) Operator laws landed today: no sacred cows
  (rules revisable on grant), daemon-recycle ratified by execution, xdist
  never single-worker.

- **WINDOW HANDOFF 09-27 morning (marathon window, ledger 599->613, all rows through the wired gate):**
  (1) **GAME-DIG PROGRAM COMPLETE**: 5 veins x 30 games = 150/150 dug with evidence,
  41 clone verdicts, 2 honest skips, 5 wheel specs (~487KB) + master atlas
  watch/inbox/GAMEDIG_MASTER_ATLAS_20260927.md (8 cross-vein laws: settlement-at-death
  wallets, bounded interest, prerequisite-pair graphs, care loops, wealth-target
  threat checks + transport/no-fabrication/salvage laws). All 5 saved workflows
  RE-SYNCED with the shrink() crash fix (stale-copy regression found and closed;
  pre-rerun byte-sync check is the method). Run by name: CreateWorkflow saved
  game-dig-<vein>.
  (2) **FIVE NEW MACHINES LANDED, all falsifier-backed**: append gate
  (tools/ledger_append_gate.py WIRED into ledger_lock.py fail-closed: every
  burn-ledger row now banks through validate_line pre-lock), receipt-body FTS
  (tools/receipt_body_fts.py: 2,229 bodies searchable, check->build freshness
  law, no cron per operator law), queue-owner close verb (tools/queue_close.py,
  literal RECEIPT_BINDINGS table: closed Q-044/Q-045/Q-029, falsifier PASS 3/3,
  the LINKS-328 drain half exists), symbol dictionary (memory/corpus/
  symbol_dictionary.jsonl: ExploitGym + Jacob Coxon, siblings field landed),
  ledger spot patrol (tools/ledger_spot_patrol.py WARN-ONLY, claim-polarity fix
  proven on B2-298, two-week vacuousness clock running).
  (3) **FIX QUEUE CLOSED** (atlas self-steal Q1-Q7) plus LAW-12-AMD-1 applied
  (registry, suite green) and the State XI pilot-annotation amendment (fire 2
  unblocked). Librarian v1 retired: 191/198 resolved (189 first pass + 2 via the
  CONFIRMED zero-padding law in corpus/papers/librarian_backfill_20260927_redo.jsonl);
  3 classical print keys stay owed (S2 keyless search 429s; batch endpoint passes).
  (4) **FIRES + REDO**: 10 lean fires cycled the manifest; fresh failure-mode
  species named and ledgered (anchor rot, emitter-without-caller, lookup-scope-
  too-narrow, locator instability, re-fire collisions, zero-padding acceptance).
  REDO SWEEP closed every failure: LINKS-329 0.36x correction filed append-only
  (true figure 0.36 PERCENT, 100x off), cross-slug receipt-row gap repaired by
  retro row, LLM7 lane HOT (64 models unauthenticated free), Chutes+SiliconFlow+
  Scaleway dead, Featherless recon-only 22k models. LINKS-349 "forgetting on
  purpose" doctrine landed (deliberate forgetting = pointer-carrying drop;
  the leak law = accidental forgetting).
  (5) **OWED for the next window** (all ledgered): Fire 2 of State XI A/B
  (annotation section now authorized); Featherless roster-diff recon tool;
  generic validated-path close mode (hook refused 5 constructions, needs a
  data-file-registry shape); LLM7 token unlock probe (operator key call);
  probe20 --live (night box window per box-burn law); patrol + census task
  scheduling stays OPERATOR-GATED (no crons la
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 6300 + tail 2100 of 75130 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
 cited-missing extends the ractor50/accuracy.md:35 citation-resolver spec from resolution to HOLDINGS (every LANDED row citing an external primary leaves primary bytes in state/arxiv/<date>/<id>v1.txt or a corpus dir and cites that path; the lane's three scripts re-runnable nightly to diff fresh receipts); (6) expedition closes the cited-primaries-evaporate debt: 61 primaries landed / 90,594,721 B / 61 full-chain PASS 0 FAIL (3 P1 founding texts, 38 arXiv papers, 17 web/social sources, 13 error bodies named not landed, 6 failures named never faked), holdings audit now 262 claims / 842,965,168 B CLEAN; (7) seats-inventory rules no mass re-registration owed (891/975 bytes-verified, all 80 unregistered are clone plumbing/hook-state/pyc) and names follow-ups: 4 stale catalog rows, 6 stale INDEX sha entries, 18 mixed-convention double-registrations to unify at the next rebuild, 5 mangled-path root copies. B-division finish: 6/6 finished per lane JSON finish flags (all 6 division B lanes); division A holdings-doctrine complete. Graves filed: 0 (grep -ril GALA_GRAVE over watch/inbox/gala_20260925/librarian-expedition/ and watch/inbox/librarian_exp/ returned no matches at 2026-10-02T00:20:57Z; ballroom buried 0/0 per the fold gate; the holdings-doctrine unstaging decision stands as named debt deliberately not executed, not a grave). 7 LINKS rows (GALA-librarian-expedition-holdings-doctrine/foundational-gaps/instrument-audit/integration/cited-missing/expedition/seats-inventory) appended to memory/corpus/LINKS.jsonl after src dedupe (0 prior librarian-expedition rows under any field, case-insensitive grep; ledger 243 -> 250, whole-ledger re-parse OK 250/250, 7 ids unique, 7 srcs unique, em/en-dash scan on the appended block 0). Lane JSONs + check evidence: watch/inbox/gala_20260925/librarian-expedition/lanes/; per-lane receipts: watch/inbox/librarian_exp/ (foundational-gaps.md, instrument-audit.md, integration.md, cited-missing.md, gathering-log.md, inventory.md; holdings-doctrine files no separate receipt, its lane JSON + lanes/holdings-doctrine.check.txt are the record).
