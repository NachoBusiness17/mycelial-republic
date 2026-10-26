# DEEP ITEM: THE ENTROPY BUDGET (deep-entropy-budget)

**Seat:** deep-gopher-deep-entropy-budget (flash50 lane, burn_reset_20260927) · **Date:** 2026-09-28
**Question:** every gate, test, and receipt adds order (decreases local entropy) but costs compute (increases global entropy). What is the total order the estate can afford, where is the entropy exported, and is the estate a dissipative structure?

**Method:** read the estate's order-making machinery, then measure it. Generator for all counts below: `_entropy_budget_census.py` (this dir). Raw pytest collect output: `_census_collect_20260928.txt` (this dir).

## 0. What I read and ran (evidence, not vibes)

Read this session: `githooks/pre-push` (333 lines, 10 gate blocks), `tools/violation_ratchet.py`, `mag/state_snapshot.py:1-80`, `memory/rib/RIB_DRIVING_LADDER_20260928.md`, `memory/burns/BURN_WAVE_STATE.json` (full), `memory/burns/LEDGER.jsonl:1-2`, `corpus/steal/TETHERED_LINK_STEAL_20260925.md:32-99`, counts from `memory/percolator/invariants.json` and `configs/violation_baseline.json`, log tails `logs/census_patrol.log` and `logs/fts_index.log`, plus the AGENTS.md carrier bullets supplied with the ask's context.

Ran this session (exact commands):

1. `.venv\Scripts\python.exe -m pytest --collect-only -q` (repo venv, pytest 9.1.1) → **2410 tests collected in 8.21s**, 2026-09-28. The AGENTS.md census carrier claims 2,303/352 from 09-27; disk today holds 368 `test_*.py` (my count). Per the B2-216 denominator law this is a COLLECTED number at one moment, not an executed sum. The +107 tests / +16 files in one day is measured drift, not a constant.
2. `.venv\Scripts\python.exe watch\inbox\burn_reset_20260927\flash50\_entropy_budget_census.py` → every number in section 1.
3. `head -n 2 memory/burns/LEDGER.jsonl` and `grep -n "109" corpus/steal/TETHERED_LINK_STEAL_20260925.md` (row shape, income line).

Not run: a full executed pytest pass, the ratchet itself, any remote inference. Stated as such where it matters (section 8).

## 1. Order, operationalized (the measured estate)

Order here means only what can be counted and hashed: pinned tests, named debts, ledger rows, receipts, invariants, tracked bytes.

| Structure (the order) | Measured 2026-09-28 | Source |
|---|---|---|
| Pinned refutations (tests, collected) | 2,410 / 368 files, 8.21s collect | my pytest run (§0.1) |
| Registered (named) debt claims | 941 | `configs/violation_baseline.json` `accepted`, counted; matches commit d90bc8607 "prune 943->941" |
| Burn ledger rows (landed work units) | 693 | `memory/burns/LEDGER.jsonl` rows |
| Burn-wave lane IDs dispensed | spans B2-01..B2-553 with gaps, duplicates, and 15 malformed `[` rows at `BURN_WAVE_STATE.json:421-435`; landed array re-derived from disk by the LANDED RULE, not self-report (`:1067`) | same file |
| Requeued (unlanded) briefs at window close | 88 (my count of the `outstanding` array, `:979-1065`) | same file |
| Receipts (md) in watch/inbox | 2,154 files md of 12,124 files, 6,349,652,922 bytes (6.35 GB) | census script |
| Estate index rows | 3,485,538 (`dashboard/data/ESTATE_INDEX.jsonl`) | census script |
| Catalog rows | 581,477 (`catalog/catalog.jsonl`) | census script |
| Percolator invariants | 352 (`invariants` key; note: skill prose still says "47 invariants", the byte truth outran the prose, a live census-drift instance) | counted |
| Trajectory steps / behavioral facts | 29,684 / 577 | census script |
| Workflow gate registry rows | 30 | `memory/workflows/REGISTRY.jsonl` |
| Git-tracked files | 47,388 | `git ls-files`, counted |
| Push-time gate blocks | 10 (2 always-enforcing, 1 blind-block, 2 conditional-enforcing, 5 WARN-only) | `githooks/pre-push` |

Three interpretive moves that the rest depends on:

**Naming is cheaper than fixing, and it still destroys entropy.** The 941-claim baseline is usually called "debt", but thermodynamically it is the opposite of raw disorder: each claim is a 16-hex fingerprint of (rule, file, line-free detail) (`tools/violation_ratchet.py:19-21,84-85`). In Zurek's terms (physical entropy = Shannon entropy + algorithmic information of the description), converting an unknown disorder into a fixed-size name collapses the description length. The estate's true invention is entropy *accounting* as a substitute for entropy *deletion*: you cannot afford to fix everything, but you can afford to name everything, and naming already lowers total entropy. The same move is the receipt discipline: `ts/slug/verdict/landing/one_line` (`memory/burns/LEDGER.jsonl:1`) is a compression scheme for a workday.

**Tests are precomputed refutations.** A pinned test is order precisely because it converts "this could break tomorrow, someone should think about it" (an open, entropy-producing obligation) into a stored computation that runs in milliseconds and never has to be thought again. The 8.21s collect run re-derives the *index* of 2,410 stored refutations; executing them re-derives the refutations themselves. That is the estate's version of Landauer's reset: each red-to-green transition erases an uncertainty bit, and erasure is the only fundamentally costly step.

**The ratchet is a one-way membrane.** Only NEW violations fail; the register grows only by named acceptance and shrinks only by prune (`tools/violation_ratchet.py:5-8`), and prune cannot reap claims outside the scanner's own derivable domain after B2-95 (`:64-68`). Rectifiers like this are what let order accumulate at all: without one, daily disorder (bad merges, copy-paste rot) flows backward as fast as work flows forward. The census-drift incident shows what happens where no membrane exists yet: the test-count carrier rode 12 days stale while tests/ grew 31 files (AGENTS.md B2-215 bullet, `githooks/pre-push:58-64`), because prose carriers have no ratchet.

## 2. Thermodynamic reading (the literature this maps to)

- **Schrödinger (What is Life?, 1944):** an organism feeds on negative entropy; it maintains internal order by exporting more disorder than it absorbs. The estate's version: it feeds on token throughput and electricity, and exports receipts.
- **Prigogine (dissipative structures, Nobel 1977):** far from equilibrium, a steady flux can self-organize stable pattern (Bénard cells) whose order is maintained only while the flux continues. Tested against the estate in section 5.
- **Landauer (1961):** erasure of one bit costs at least kT ln 2; logically reversible operations (append) are in principle free, irreversible ones (delete, overwrite, reset) are not. The estate's op economics match exactly: appends (ledger rows, receipts, baseline claims) are cheap and unregulated; erasures (prune, VOID execution, freeze, tombstone) are operator-gated, named, and rare (`githooks/pre-push:4-7`, the Q-020 VOID operator-GO receipt cited in AGENTS.md).
- **Szilard (1929) / Maxwell's demon:** a demon who sorts fast from slow molecules pays for the sorting in measurement, not in actuation. Every push is a sorting event and the hook is the demon: 10 gate blocks measure the pushed changeset and sort it into pass, warn, or block. The estate explicitly rations the demon's measurement: the freshness gate inspects at most 5 receipts per push (`githooks/pre-push:46-47`), and the secret gate refuses the full scan because "a full scan in pre-push is a 777s gate nobody keeps" (`:313-315`). 777 seconds is a measured price for perfect measurement, and the estate declined it on the record. That refusal is an entropy budget line item in its purest form.
- **Kolchinsky & Wolpert (2020, thermodynamic costs of Turing machines):** computational cost is tied to the irreversibility of the state map. The estate's append-only bias (jsonl everywhere, hashes, bounded pointers) keeps its state map nearly reversible, which is why its "cheap" tier is genuinely cheap.
- **Ashby (1956, law of requisite variety):** only variety absorbs variety. Each new disturbance class demands a new regulator arm or it passes silently. The hook is 333 lines of Ashby's law made manifest: B2-215 (stale census) demanded the census patrol, B2-244 (unverified caption ledger) demanded its gate, B2-279 (a comparator mutation invisible to a push) demanded the refold gate, B2-338 (an uppercase OK that trained operators to dismiss the channel) demanded the lowercase-first-line output contract (`githooks/pre-push:67-75`). The WARN-only-first convention plus operator flip is the cost governor on regulator growth.

## 3. The budget equation, with the estate's real numbers

Steady-state affordability is one inequality:

    W_income  >  W_basal  +  W_upkeep(O)  +  W_landfill_servicing

and the affordable order O_max is whatever size satisfies it. Each term is measurable, and three of the four were measured today.

**W_income (the flux).** Denominated in tokens per hour, not dollars. Measured ceiling: width 10 clean at 109.4M tok/h with zero surfaced 1302s (`corpus/steal/TETHERED_LINK_STEAL_20260925.md:96`); the surfaced wall lives higher and is dynamic: the width-24 experiment took 8 rate-limit deaths in one window and closed with "ceiling confirmed dynamic" (`memory/burns/BURN_WAVE_STATE.json:962-975`). Money: only Hermes is funded, $180 in Nous credits; Anthropic keys UNFUNDED; free lanes are quota, not cash, and are sensing-only (`memory/rib/RIB_DRIVING_LADDER_20260928.md:7-23`). So income is a quota gradient with a hard throttle, plus local electricity. The operator's burn order for the wave was literally a flux directive: "burn remaining flash-lane quota into estate work by midnight" (`BURN_WAVE_STATE.json:4`).

**W_basal (the standing pumps).** Three daily crons (MagImproveDaily 08:00, MagCensusPatrolDaily 08:30, MagFtsIndexDaily 09:00, per AGENTS.md) plus per-push gate time plus the pile drain. Heartbeat check today: the FTS pump beat at 09:00:09, exit 0, wall 0.637s (`logs/fts_index.log` tail, my read): cheap when healthy, by design. The census pump's log shows its last beat at 2026-09-27 08:30:02, which itself flagged "1 unhealthy task(s) named"; my read of the tail shows no 09-28 beat (scheduler state not queried, cause undiagnosed, section 8). A basal pump missing a beat is a maintenance outage, and the estate currently detects that class only by reading logs.

**W_upkeep(O) (the scaling term that already bit once).** Upkeep grows with accumulated order: 2,410 tests must keep passing, 941 named debts must be kept named-and-true, every receipt a gate touches must still resolve, the FTS index decays to scan fallback whenever catalog.jsonl moves past it (AGENTS.md B2-465 bullet), docs go stale at 7 days by law (freshness_check). This is the term that produced the 12-day stale census: verification habit (a flux cost) lagged verification need (an O-proportional cost), and the difference accrued silently as staleness. The estate's structural answer is already visible in the hook: conditional, change-scoped gates. The caption, refold, and workflow-scenario blocks cost "git plumbing only" when idle and fire only when their own paths changed (`githooks/pre-push:131-132,190-191,264-266`), and the ratchet and secret gates run `--changed` only. That is upkeep converted from O(estate size) to O(change size), the single most important budget move available, and it is already the house style.

**W_landfill_servicing (deferred entropy).** The discard piles are not exported, they are stored: 941 named debts, 88 requeued briefs from the closed window, FKB signals deliberately kept log-only, pile rows awaiting the classifier (`mag/state_snapshot.py:1-10,36-39` writes `memory/pile/state_summaries.jsonl` for the overnight local-model drain). Landfill is entropy with a maturity date: it must eventually be triaged (compute), or it seeps. The estate has one documented seep event: B2-95, where a routine prune silently reaped 25 mimosa claims the scanner could not re-derive, closed by restricting prune to its derivable domain (`tools/violation_ratchet.py:10-17`).

**The budget's shape.** Solving the inequality: O_max is not set by income alone. It is set by the *upkeep-free fraction* of the order. Hashes, ratchet pins, frozen docs, and change-scoped gates have near-zero marginal upkeep (a ratchet pin costs nothing until someone touches that file); hand-run sweeps, prose status carriers, and unhashable claims carry permanent upkeep and quietly consume flux forever. Every token of income spent on upkeep-free order permanently raises O_max; every token spent on flux-shaped pseudo-order raises upkeep instead and can actually *lower* the sustainable total. The AGENTS.md law "trust bytes, not reports" is this budget principle stated as epistemology: a byte is free to re-hash, a report requires re-running its generating computation.

## 4. Where the entropy goes (the four exhausts)

1. **Room heat, the nearest dump.** Local CPU cycles: the 8.21s collect, full pytest runs, the ratchet scans, the ollama janitors (`gemma:2b` scut, `gemma4` worker, per AGENTS.md). The workstation's heatsink is the primary export path and it is effectively unmetered, which is why the estate correctly keeps its basal metabolism local.
2. **Provider datacenters, the rented dump.** Remote inference: the estate pays for ordered work by donating disorder to someone else's thermodynamics. Free stealth lanes are quota gradients that harden into 429/1302 walls under load; the throttle is literally the exhaust pipe's diameter, and the fleet mapped its diameter by experiment (widths 3, 6, 10, 12 clean, 24 deadly, holds logged per death cluster, `BURN_WAVE_STATE.json:925-975`).
3. **Landfill, the deferred dump.** Section 3's W_landfill: 941 + 88 + log-only signals + unclassified pile rows. Not exported yet, only entropically escrowed.
4. **Freeze, the sedimentary dump.** `memory/briefs/latest.md` FROZEN 2026-09-26, tombstones (GENE_POOL_TOMBSTONE_20260927), superseded-run records. Freezing converts live order into inert sediment that costs nothing to maintain because it is declared dead and excluded from live inference. It is the cheapest storage the estate has, and it is underused: freezing is currently ad hoc (an operator pronouncement) rather than a scheduled lifecycle stage.

## 5. Verdict: is the estate a dissipative structure?

Test the three Prigogine signatures:

1. **Far-from-equilibrium flux.** Present and deliberately maintained: the burn-wave machinery exists to convert quota gradients into work before the window closes, with a dispatcher that refills every 20 minutes and a HOLD protocol on first rate-limit contact (AGENTS.md max-concurrency law, `BURN_WAVE_STATE.json` laws block).
2. **Order persists only while flux continues.** Present, with named decay channels: FTS decay to scan fallback, 7-day doc staleness, census drift, prose carriers outliving their referents (the "47 invariants" prose vs 352 bytes measured today). Starve the pumps and the estate does not die, it rots at a measurable rate.
3. **Fluctuations amplified into new order (autocatalysis).** This is the strongest match. The hook is a fossil record of fluctuations that became structure: each escaped failure class re-entered the estate as a new gate arm (section 2, Ashby). The workflow gate formalizes it as self-steal: every check registers a ledger row, improvement is itself a ledger fact. Negative feedback on failure is the autocatalytic loop; the estate runs it on purpose.

**Verdict: yes, a dissipative structure, with one non-Prigogine twist.** A Bénard cell has no non-volatile storage: kill the flux and it vanishes in seconds. The estate deposits sediment (commits, hashes, frozen docs) that persists without flux. That makes it tolerant of hibernation in a way physical dissipative structures are not, at the price of a failure mode they do not have: it wakes up stale. Its characteristic risk is not death by starvation but rot during dormancy, tripped after the fact by patrols (the 12-day census ride is the canonical case).

## 6. The Landauer floor the fleet is not computing

Define **L**: the minimal compute to re-verify the estate's entire claimed order from bytes alone. Components, all nameable today: one full executed pytest pass (2,410 tests; collection alone is 8.21s, execution was not run this session), every pre-push gate at full scope (the secret gate's full scan alone was priced at 777s and refused, `githooks/pre-push:314-315`), the FTS deep check, an FKB rebuild (the Q-028 receipt prices the last one at 17 -> 1,421 signatures, 25,100 c73866f2f1b5 entries), catalog integrity, and resolution of every receipt pointer a consumer might follow.

The budget question that matters is whether **L > daily surplus**. If yes, the estate is thermodynamically insolvent at any discipline level: full re-verification costs more than the flux can pay, and the only exits are (a) total commitment to differential verification (already the house style, but then it must be *law everywhere*, not habit) or (b) order retirement: sunsets as first-class as tombstones, expiring order whose upkeep exceeds its value. Nobody has measured L. The probe is cheap to build (`scripts/entropy_floor_probe.py`: run the components, sum the walls, log to a jsonl) and it would convert this entire analysis from metaphor to instrument. Similarly missing is **eta**, the order-per-token conversion efficiency: the burn ledger records landings but not token costs per row, so the estate knows its income to two significant figures and its efficiency to zero. Attaching the dispatch-time token count to each `LEDGER.jsonl` row would make eta computable from data that already exists.

## 7. The entropy budget, v1 (the design deliverable)

    dO/dt  =  eta * ( W_income - W_basal - W_upkeep(O) - W_landfill )

Budget lines and laws, each already half-alive in the estate's own practice:

1. **Amortization law.** Quota may only buy upkeep-free order. Every flux-bought structure states its re-verification owner and cadence, or is upkeep-free by construction (hash, ratchet pin, frozen doc, change-scoped gate). A new hand-run sweep is negative-value: it adds order AND permanent upkeep.
2. **Differential verification law.** Verification cost scales with change size, never with estate size (`--changed` everywhere; full runs belong to the daily pump only). Already the hook's design; promote it from style to law.
3. **Erasure stays operator-gated.** Landauer-consistent and already law: `baseline-update --by <who>`, VOID needs operator GO, prune is domain-restricted (B2-95). Keep erasures rare and batched.
4. **Name before fix.** Naming debt (941 claims) destroys description entropy at near-zero cost; fixing costs flux. Budget them separately: naming is basal, fixing is discretionary.
5. **Freeze the dead on a schedule.** Make sedimentation a lifecycle stage with a cron, not an operator pronouncement: anything untouched for N days and marked superseded freezes automatically. Zero-upkeep storage is the cheapest order the estate owns.
6. **Meter the demon.** Keep explicit measurement budgets: the 5-receipt freshness cap, the 777s full-scan refusal, WARN-only-first landings. These are the estate's kT ln 2 accounting; never remove one without naming what measurement it was rationing.
7. **Instrument the pumps.** A basal pump that misses a beat is an outage, not a footnote. Today's log gap (census patrol, section 3) was found by a deep item reading logs, which is itself flux spent. One heartbeat check across the three crons closes the class.
8. **Measure eta and L.** Token counts onto `LEDGER.jsonl` rows; `entropy_floor_probe.py` for L. The budget is real only when both numbers exist.

## 8. Not run, not verified (the honest column)

Full executed pytest: not run this session (collection only, 8.21s; executed denominators are historically lower than collected per B2-216). Ratchet, config seal, and other gates: not invoked. The 109.4M tok/h income figure: verified against `TETHERED_LINK_STEAL_20260925.md:96` prose, not against raw dispatch logs. The width-24 death counts: from `BURN_WAVE_STATE.json` self-report (the landed array, by contrast, is disk-derived per its own LANDED RULE). The census patrol's 09-28 absence: log-tail evidence only; scheduler state not queried, cause not diagnosed. eta and L: not measured anywhere in the estate; proposed, not built. The literature anchors (Schrödinger, Prigogine, Landauer, Szilard, Zurek, Kolchinsky-Wolpert, Ashby) are cited from training knowledge, not re-fetched this session.

**One-line answer to the ask:** the estate can afford exactly as much order as is upkeep-free, plus the flux surplus after three daily pumps and per-push demon time; its exhaust is room heat, rented datacenter dissipation, escrowed landfill, and sediment; and it is a genuine dissipative structure with the one twist Prigogine's cells do not have: it fossilizes, so it survives starvation and must instead be defended against rot.
