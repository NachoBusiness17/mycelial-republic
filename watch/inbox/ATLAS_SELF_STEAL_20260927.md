# ATLAS SELF-STEAL — THE FLEET'S ORGANIZATIONAL MACHINES — 2026-09-27

Three deep digs (billboards census, organ census, width synthesis) folded into one doctrine. Sources: three digger reports in-session, all byte-read.

## 1. The CS structure you remembered: WE BUILT THE LAYERED STACK

The billboard census found the fleet unknowingly rebuilt the classic communication-theory layer cake, each layer a different temporal contract:

- **L0 event log** (append-only record): trails/*.jsonl, pile summaries, EVENTS.jsonl, the verkle chain
- **L1 state snapshot** (point-in-time, TTL decay): state/CURRENT.md, runner_state.json, organ_vitals (temp tiers HOT/WARM/COLD/FROZEN)
- **L2 index/registry** (inventory): ESTATE_INDEX (1.7M rows), INDEX.json, SEATS.md, VERSION_REGISTRY
- **L3 broadcast board** (human aggregate): deck.html, fleet console, lanes/*.md, DAY_WORK_DIGEST, drift_board
- **L4 gallery** (culture/memory): viz_gallery, games arcade, museum ("beautiful, wrong, kept as the record")
- **L5 pack** (bounded channel into a stateless receiver): context-pack, bonds; decoder = the AGENTS.md load order
- **L6 ephemeral console**: the visor (born yesterday; zero persistence; the surfaces ARE the communication)

Notable natives: drift_board is the feedback channel (claimed direction vs observed motion); the pile is the learning loop's return path; the frozen brief is a deliberate channel shutdown whose decoder was never updated.

## 2. The flywheel, confirmed at byte level

Momentum is stored in exactly four places: append-only ledgers (552-row burn ledger, 29-row gate registry, LINKS ledgers, 11-law registry), saved workflows (5 gated shapes: reruns amend, never rewrite), the catalog+FTS map with its daily rebuild and two-plane freshness gates, and bonds/wave-state (due-oldest round robin, PAT demotion). The lane panel doctrine (LINKS-342) confirmed byte-level: the flywheel is the organ state; lanes are bearings.

**The leak law (the dig's sharpest find):** the wheel loses momentum at every hop where a receipt lands without a ledger row, a ledger row without an index key, or an index without a reader. Concrete leaks on file: 99 receipts landed-unindexed; no content-layer search (FTS5 indexes path+title ONLY: any claim inside 11K receipts is unfindable unless you already know the filename); attention.md degraded to notification spam; briefs organ frozen; librarian report 16 days stale owing 198 primary pulls; four inventory organs with disjoint key schemes and zero cross-joins; 10 workflow drafts unpromoted.

## 3. The three load-bearing gaps (highest leverage first)

**GAP 1: Every cold seat is being poisoned right now.** The brief organ (memory/briefs/latest.md) was frozen 2026-09-26 because regenerators wore August fossils, but BOTH consumers still point at it: the AGENTS.md load order AND context-pack's brief layer. Every mode-tiered pack (janitor through full) injects the frozen fossil with its freeze banner. Truth exists (state/CURRENT.md, verkle_tip.json, inbox INDEX) but no single provenance-guaranteed "what is happening now" text feeds the pack. FIX (one pointer, operator-gated because the freeze was operator-gated): repoint the AGENTS.md load-order row and context_pack's brief layer to state/CURRENT.md (or mint a new brief writer with a fresh face).

**GAP 2: No billboard carries the org chart as it exists.** SEATS.md (Aug 14) and HABIT.md (Aug 6) predate the current era: they do not know the GLM coding plan as primary seat, the width laws, Hermes dispatch-capable status, the workflow-gate discipline; HABIT's default loop still routes through a dead path (memory/handoff/latest.md, last written Jul 31). The live org chart lives only in AGENTS.md prose. FIX: refresh SEATS.md from today's truth (one seated write), repoint HABIT's dead loop step.

**GAP 3: No lane-writer liveness surface.** Stalled lanes (economist 19.3h, prose 19.8h, elder reduced to daily 429 death rows) and dead data feeds (17 Sep-era JSONs with no writer) are invisible as a class: the estate index proves a file FROZEN but nothing answers "which surfaces still have a living writer, which lane is starving now." FIX: extend the visor with writer-liveness (per billboard: last-writer mtime + writer identity), making it the one console that answers both session AND organ aliveness.

## 4. The clever mechanism (the operator's ask)

One instrument family, three blades, all self-stolen from patterns we already run:

1. **WIDTH LEDGER** (born yesterday): lane / measured width / first-failure / cost shape / probe date + the router rule at its head. Answer to the standing question "where does this wave go."
2. **CONTENT FTS** (the retrieval unlock): extend the sanctioned FTS writer to index receipt BODIES (Evidence + one_line) into a second FTS table keyed to landing paths. This single change makes every claim the fleet ever filed searchable by content. The librarian's 198 owed pulls and the 99 unindexed receipts become findable debt.
3. **WRITER-LIVENESS VISOR v2**: every billboard declares its writer; the visor computes per-surface liveness (writer mtime + identity); stalls surface as a class instead of hiding in one trail row.

Together: dispatch (width) + memory (content search) + awareness (liveness) = the flywheel's bearing, index, and tachometer.

## 5. Width answers (already filed: WIDTH_LEDGER_20260926.md)

Flash Task agents: 10 sustained (109.4M tok/h), 12 fresh, 15 deaths-start; constant silent contact (1,741 absorbed 1302s one session; clean = zero terminal, not zero contact). Regular GLM: DARK, never measured, baseline wave owed. Workflow children: law 3 vs unbanked 50-hours-clean; Stage-2 probe settles. Hermes 6 clean. Free lanes 12 clean, 18 via lane-pinning. Six staged probes filed.

## Fix queue (all operator-gated, in leverage order)

Q1 repoint brief consumers (GAP 1) · Q2 SEATS/HABIT refresh (GAP 2) · Q3 visor v2 writer-liveness (GAP 3) · Q4 content-FTS writer extension · Q5 the 99-receipt INDEX backfill · Q6 librarian v1 198-owed drain or formal retirement of the report · Q7 draft promotion sweep (10 unpromoted)
