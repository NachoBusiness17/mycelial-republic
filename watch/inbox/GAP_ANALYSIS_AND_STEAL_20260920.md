# GAP ANALYSIS + STEAL — whole-estate receipt audit (2026-09-20)

Filed 2026-09-20 evening. Method: three parallel sweeps (research-memory layer, watch-lane debt/arcs, instruments/integrity) over the MICKEY 17 baseline (2,493 files: 639 LIVE / 1,258 DONE / 512 OWED / 84 STALE). This card is the analysis layer, not a re-scan. Evidence paths inline; every gap is named and defensible, every steal has a landing site.

---

## PART 1 — THE GAP REGISTER (ranked by damage, not by count)

### Tier 1 — structural (the estate doesn't know itself)

**G1. Backup remote diverged.** Local-only 338 / remote-only 110 commits (drift patrol, 09-20). Largest single data-loss exposure in the estate. *Merge owed; one reconciliation session.*

**G2. Steal pipeline stalled while steal material accrues.** `memory/steal/` = 140 files but only **1** surface receipt (Aug 31); execution ledger covers only the Aug 10–11 wave; ~60 Aug 14/24–25 steals never receipted. Meanwhile fresh steals (gapwave, Sept 19–20: arxiv_multiactor, ecosophia, gopher series) never promoted to the library. And `DEEP_STEAL_ROOM_THAT_REMEMBERS_20260824.md` has **no matching run** — a filed steal never executed. *The fleet's signature verb has no ledger.*

**G3. research_packs is unindexed (680 entries, zero root register).** 59 orphaned prompts (issued, never answered); five-week dump hole (Aug 28 → Sep 20 — the dump pipeline died, Sept research went to ad-hoc dirs); `beta1-scope/` is an empty shell with one HANDOFF.yaml; debris at root (`latest.*`, `_probe.md`, stray scripts). Today's two best packs (black_swan, entity_morphology) exist only because we built them by hand — `entity_morphology` still has no synthesis file.

**G4. Runs never roll up.** Only **5 of 378** run dirs carry a root digest/summary (the declared convention in `memory/README.md` is unenforced); 55 `*_empty_recovery` crash dirs (six weeks of failure residue) never consolidated despite `memory/failure_kb/` existing.

**G5. The status machine is external and static.** `watch/inbox/INDEX.json` tracks provenance, not status (no status field at all; 25 case-inconsistent class tags; ~30 fold-warning nonce collisions incl. a ns-vs-us time-unit collision). Real state lives in mickey17's MASTER_INDEX — a static snapshot that ages the day it's printed. Only ~8 of 639 cards carry an explicit Status line.

### Tier 2 — meters dark (instruments stalled while the fleet ran)

**G6. Grounding-wave falsifier ledger dark 4 days** (last row 09-16 13:16Z) while the estate ran continuously through 09-20.
**G7. cite_gate dormant since 09-07** (self-admitted gap in the bundle-attack cell).
**G8. Cliff scalar unsigned** — `law_status: CANDIDATE_UNSIGNED`, thresholds are "spec text until fired" (operator gate).
**G9. flight_recorder / session_digest stale 4d; steers.jsonl stale 9d** — the wave-era feeds predate the current THE-50/mickey17 era and nobody turned them off or fed them.
**G10. Pre-seal gate NOT cleared and the audit bundle is stale** — `audit_bundle/` untouched since 09-12: 5 files/36KB on disk vs the manifest's 1,564 files/20.5MB; no external auditor verdict since 09-12 (Matthew's audit lane is cold).
**G11. Intake organs have zero tests** — grep tests/ for cite_gate|reasoning_intake|cage_intake = 0 hits; the organs that feed the verkle chain are unverified while the chain itself has 3 test files.
**G12. reasoning_intake is one-shot** (6 sealed rows ever) — the "seven weeks of pre-sealed steps" pool has no continuing intake pipeline.

### Tier 3 — corpus coverage (we hold material we never derived)

**G13. oral_history has no derived index** — nacho_archaeology (10 extracted zips) has only TRANSCRIPT_MAP.txt; the_wall and marathon_body raw; no cadence/stego/vision pass applied.
**G14. Catalog is 77% memory-backup mass** — 585,226 of 757,667 rows are kind "other"; `corpus/library` and `corpus/oral_history` barely indexed (and library grew today: Lockwood shelf).
**G15. Mr Pool comment layer unharvested** — `comments.jsonl` is **0 bytes**; the audience-reaction instrument (reaction signatures were named as instruments on 09-18) has no data.
**G16. BG123 image-pass instrument still pending** — the one corpus where the image is primary has only a 7-artwork symbol census.

### Tier 4 — open arc-closers (mostly operator-gated)
G17 cluster: ARC_LAWS (tombstone GC + DISTINGUISH) gate · ASTRA_V4 dispatch · ASTRA constitutional ratification · ASTRA_VS_CHEAP blind-stage scoring (operator) · SPACE_CAPTURE (cookie export) · BRAIN BOX pending · 2B-burn v2 execution (v1 convicted 6/6) · chain-v2 program behind "Operation Full Shelves" · main branch 42 days stale / 101 commits ahead · UF-109 degeneracy probe (spec, no code) + UF-47 Librarian battery (never run) blocking Elder passes 2/3 · empty-chairs pilot GO · COLDEST_SHARD_VEIL_TEX_MAP routing · THE-50 tail (W4-T20, W6-T30).

---

## PART 2 — THE STEAL (external model per gap, with landing sites)

| # | Gap | Steal (source → mechanism) | Landing site |
|---|---|---|---|
| S1 | G6, G7, G9 (dark meters) | **Aviation MEL — Minimum Equipment List.** Aircraft fly with known-inoperative instruments only inside a per-item allowed-outage window, logged. Steal: `FLEET_MEL.md` — every meter gets a max-dark duration (grounding ledger 72h, cite_gate 7d, flight_recorder 7d); beyond MEL = no new arcs launch in that lane until the meter is back. | One card + one new check line in the existing daily drift-patrol automation (it already writes DRIFT_PATROL_*.md — extend, don't build) |
| S2 | G3, G4 (unindexed packs/runs) | **CI-for-indexes (mickey17's own trick, generalized).** Indexes are derived artifacts — *recounted by script, never hand-maintained.* One script walks research_packs + runs, emits root INDEX.md + per-dir PACK stubs (title, files, date, prompt-orphan flags). | `tools/index_recount.py` → `memory/research_packs/INDEX.md` + `memory/runs/INDEX.md`; drift patrol re-runs it daily. Kills G3/G4 permanently for one script |
| S3 | G1 (diverged remote) | **Bank reconciliation.** Nightly reconciliation statement: local vs remote commit lists, classified canonical-local / canonical-remote / needs-merge, printed into drift patrol. The merge itself is one operator-supervised session — but after the statement exists it can never silently rot again. | `tools/reconcile_remote.py` (git plumbing only) → DRIFT_PATROL appendix |
| S4 | G10 (stale audit bundle / cold pre-seal gate) | **Chain-of-custody (forensic evidence bagging).** Bundles are sealed by script: file count + bytes + sha256 manifest printed on the bag BEFORE it leaves. A bundle that disagrees with its own manifest is not sent. | `tools/seal_audit_bundle.py`; rerun for Matthew's lane; satisfies the bundle-attack cell's 5-point fix list |
| S5 | G2 (steal ledger) | **Double-entry bookkeeping, applied to steals.** Every steal file = a debit; every build receipt referencing it = a credit. The 1-line surface_receipts.jsonl becomes a proper two-sided ledger; unbuilt steals surface as open positions (and `ROOM_THAT_REMEMBERS` is already an open position with a named landing). | `memory/steal/execution_ledger.jsonl` + backfill of the Aug 14/24–25 wave; gapwave Sept steals promoted |
| S6 | G13 (oral_history raw) + S5's open position | **Execute the existing steal:** ROOM_THAT_REMEMBERS was filed 08-24 and never run — its landing site is exactly the oral_history index gap. Run it as the nacho_archaeology NLP pass. | `memory/runs/room_that_remembers/` (new) → derived index over the 10-zip archaeology |
| S7 | G5 (no status field) | **Event-sourcing projection (CQRS read model).** Status isn't stored, it's *projected*: a script folds index_events.jsonl + card receipts into a derived STATUS.md per lane, the way INDEX.json is already derived. State becomes reproducible from the append-only log. | `tools/project_lane_status.py` → `watch/inbox/STATUS.md` (regenerated, never edited) |
| S8 | G14 (catalog mass) | **Gärdenfors conceptual spaces (already in the library, 09-18).** Quality dimensions = catalog axes; concepts = convex regions. Re-dimension the 585K "other" rows by assigning 3–5 axes (kind, corpus, date, arc, instrument) so library/oral_history become searchable by distance. | Extend `catalog/tags.jsonl` tagging pass; TAG_REPORT tracks the "other" share falling |
| S9 | G15 (comments unharvested) + G16 (BG123 image pass) | **No external steal needed — finish the built instruments.** Comments = one harvest script (Telegram export format already proven by ledger_full); BG123 image pass = the symbol-recurrence detector already spec'd on 09-18. | `watch/inbox/mrpool_export/comments.jsonl` + `bearableguy_export/` recurrence pass |
| S10 | G4's crash residue | **Postmortem culture (SRE blameless postmortem).** The 55 empty_recovery dirs become one failure-KB page: common failure classes, detection, prevention — written once from the residue, then the dirs archive. | `memory/failure_kb/recovery_incidents_20260920.md` |

**Quick wins (≤1 day total, $0):** S3 merge statement · S2 index recount · S1 MEL card + patrol line · S4 bundle reseal · S9 comments harvest · S5 ledger backfill · G8 cliff-scalar signature · one OPERATOR_GATE_QUEUE card consolidating G17 (eleven gates, one queue, one card).

---

## PART 3 — WHAT THIS ESTATE IS (one paragraph)

The estate's production line works: cards get filed, receipts close them, the chain knots, THE-50 verifies 44/44. What's broken is the *instrument panel and the index cards of the workshop itself* — meters went dark while the frontier moved to directories (gapwave, research_packs, the 09-20 packs) that the older registers don't know exist. The gap analysis found no rot in the core; it found an unmanaged periphery and a steal library that stopped crediting itself in August. The fixes above are scripts and one card each — no new organs, no new laws. This is 5S with a hash chain.
