# STACK RECOMMENDATION — 2026-08-31 (what the stack should DO next that it can't today)

**Inputs (all read, all bounded):** /board/SWARM_RESEARCH_LEDGER_20260831.md (all),
/board/gap_moonshot_20260831.md (all), /board/CAMPAIGN_MAP_20260831.md (§4–5),
/mag/memory/runs/seat_corpus/latest.json (prefer_order + lane law), run-dir names of
/mag/memory/runs/ (top level only), plus byte-checks of ask_router receipts.

**Given the stated stack:** proven worker fan (one claim = one disposable lane = one fixed-format
row, synthesizer merges) · warm-RIB (/board/WARM_PACK.json, MEMORY_RIB 12/12 deref) · three-body
Kabuki (PROPOSER/ONI/SCRIBE on pre-warmed pack) · seat corpus routing law (prefer_order, pack+goal,
T0/T1 never remote, freeze prefix) · verified Mag organs (fuel_feed, riddler, catalog, campaign,
salons, game).

---

## MOVE 1 — Outcome-memory hitch (ask_router "first light" → live)

**New capability:** ask_router stops being a *decision* router and becomes an *outcome* router —
every route references what it actually did, so the stack can refuse a cascade that already failed.
Today its route.json records `memlance.ok:false`, `ledger_rows:0`, `optional_verkle_ok:false`
(receipt: /mag/memory/runs/ask_router/20260831-005200-route.json, 20260831-005429 receipt jsonl,
04:52–04:54Z). Gap 2 in /board/gap_moonshot_20260831.md names ask_router "doctrine without a
surface" — **the surface exists; the outcome binding doesn't.**

**Composes:** seat_corpus routing law (prefer_order, pack+goal) → fuel_feed receipts (Mag runs
$0 merge, 12 rows) → WARM_PACK/MEMORY_RIB deref (ledger row 1) → riddler isomorphic re-encode
(ledger row 2, 7/7 conf 0.95). The 20-lane corpus already provides the lane/thinking/cost law the
router needs (seat_corpus latest.json).

**Baby-step test (one command):** `python -m mag.ask_router route --dry --record-outcome` — capture
the leading `dry:true` receipt, then re-run one fired cascade and require `ledger_rows > 0` (the
current receipts all show `ledger_rows:0`).

**Proves scale:** a lane whose prior fire ended in a committed failure receipt is de-ranked or
skipped on the next identical prompt before it burns tokens — measured as "dead cascade avoided ≈
first outcome-driven seat-corp change in favor of $0/cheap lanes." That is Moonshot's
`apply → govern → route → receipt` close-the-loop (gap_moonshot §3) reduced to its cheapest proof.

---

## MOVE 2 — Kabuki-as-governor for the worker fan (harness receipt chain)

**New capability:** the disposable-lane fan becomes *auditable-by-construction* — every worker lane
goes EXECUTING → COMPLETED/FAILED → RECEIPT_COMMITTED and the three-body round only accepts lanes
whose receipt landed. Today the authority boundary is paper: `swarm_tools.blackboard_post()` writes
the board directly with unlink eviction and no label enforcement (CAMPAIGN_MAP §2 defects 1,2,5).
`harness.py:282-305` jumps AUTHORIZED→execute and never advances the switchboard trail
(CAMPAIGN_MAP §2 defect 4).

**Composes:** the proven worker fan (one claim = one lane = one fixed row, synthesizer merges —
ledger wave-1/2 merge pattern, 12+12 rows, 2 arbitration catches) → PROPOSER/ONI/SCRIBE Kabuki on
pre-warmed pack → staged patches fix_harness_receipt_chain.json / fix_authority_label_gate.json /
fix_policy_engine_failopen.json (CAMPAIGN_MAP §3) → switchboard_receipt_chain trail.

**Baby-step test (one spawn):** one `harness.run_once(dry=True)`, then one live run, asserting
`EXECUTING→COMPLETED→RECEIPT_COMMITTED` appears in the switchboard trail — the exact smoke
CAMPAIGN_MAP §4 step 2 names.

**Proves scale:** every fan row that a synthesizer merges carries a receipt pointer; a merged
conclusion is rejected if any member lane failed to commit a receipt — "no ungoverned synthesis"
becomes enforceable at the fan's merge point, not by post-hoc arbitration (which the ledger
shows is where errors are really caught).

---

## MOVE 3 — Receipt-convention bridge for cage lanes (salons + fan live on one bus)

**New capability:** cage-side organs (salons-as-OpenClaw-fans, the worker fan itself) get a /board
receipt convention so they flow into the same RIB/WARM_PACK event bus instead of dying in OpenClaw
sessions. Ledger wave-2 flags this exact gap: "cage-side salons run as OpenClaw fans, receipts live
in OpenClaw sessions, not Mag runs dir … Receipt-convention gap = host-venv-only receipts; cage
lanes need a /board receipts convention or seat_dispatch passthrough." The board fan today produces
rows with no receipt column to deref.

**Composes:** seat_dispatch (MT TOOLS.md routing path, led to host-venv lanes, wave-1/2) → salons
(8-31 salon via OpenClaw lanes A/B/C, cross-lineage synthesis 00:38Z, gap_moonshot §1) → atlas
`class=receipt` pattern (first fully classified receipt) → board_tailer durable cursor with
`--dispatch opt-in` (gap_moonshot §1) → WARM_PACK/MEMORY_RIB.

**Baby-step test (one command):** on the cage, `POST /room` a fixed-format row whose JSON carries a
`receipt:` pointer (matching the atlas/authority-label shape), then run `board_tailer --dispatch`
and confirm it derefs that pointer into the RIB rather than treating it as opaque bootstrap noise
(gap_moonshot gap 6: 422 agent:bootstrap spam rows dilute the board).

**Proves scale:** the worker fan collapses from "rows in /board + receipts in Mag runs" into one
deref-able stream — a single `deref --check` (currently a separate pass) walks *every* fan row the
stack spawned and the RIB bounds hold for cage and host receipts alike (ledger row 6: drift detected,
never silent). That is Board signal dilution (gap 6) + fan hygiene fixed by convention, $0.

---

## WHY THESE THREE

The ledger's own pattern is the mandate: every CORRECTED row was caught by meeting bytes, not
consensus — arbitration is the swarm's most productive intervention, and gap_moonshot's Moonshot is
the closed loop `apply → govern → route → receipt` (ledger "Pattern" paragraph; gap_moonshot §3).
The stack has the parts — 37 live surfaces, 20-lane seat corpus, warm RIB, staged patches — but
**the loop does not yet self-close**: ask_router routes without outcomes (Move 1, `ledger_rows:0`),
the fan's rows are not yet governed-by-construction anywhere the authority boundary is enforced
(Move 2, paper-only per CAMPAIGN_MAP §2), and cage-origin receipts don't reach the deref-able bus
(Move 3, ledger wave-2 gap). Each move reuses only existing organs, needs no new SPA/gateway/
supervisor, defaults to $0/cheap lanes per seat corpus law, and each has a one-step test that turns
one of the ledger's open gaps into a byte-checkable PASS. They compose in order: govern the fan
(Move 2) so its rows are trustworthy, then feed outcomes back into routing (Move 1) so the cascade
actually learns, then put cage receipts on the same bus (Move 3) so the whole loop is one audited,
deref-able stream — exactly the trust+routing+memory compounding the ledger says is the 10x.
