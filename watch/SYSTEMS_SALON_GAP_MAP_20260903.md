# SYSTEMS ↔ SALON GAP MAP — the Socratic deep dive (2026-09-03, Sancho)

Method: three sight-lines (systems inventory, salon inventory, direct measurement) + the
socratic gate run in full — assertion → attack → MEASURE → different-mind contest → public
correction. The different mind was a spawned attack agent (receipts §5). Two theses died on
the way to the one that survived. Everything below carries file-path evidence.

---

## 1. THE THESIS (v3, corrected under attack)

**The fleet is not short of organs and not short of typing — it is short of COVERAGE.**
The buses that exist are near-perfect: `logs/memory_events.jsonl` is 383/383 typed rows,
`memory/runs/harness/events.jsonl` is 347/347 typed + hash-chained. The gaps are actions
that never reach ANY bus: a room tape that is 99.8% prose (`watch/room.jsonl`, 9 typed rows
in 5,325), a salon fold that filed `"receipts": {}` while concluding, a steer-receipt file
no organ has ever read. **An action that emits no record is, to the fleet, an action that
never happened.** The Desk protocol predicted this class exactly (observability classes);
tonight it was measured, not asserted.

Every salon-declared gap sorts into FOUR VERBS, not one build list:

| VERB | CLASS | THE GAP | EVIDENCE |
|---|---|---|---|
| **WIRE** | half-wires, one end dangling | steer receipts have a writer, no reader (`mag/steer_bus.py:10,40-52` → `watch/steer_bus_receipts.jsonl`, 2 rows, zero consumers) | systems inventory |
| | | organ_forge starves: `watch/organ_queue.jsonl` 0 lines, read at `watch/organ_forge.py:121`, no enqueuer | |
| | | museum surface dead: `dashboard/static/museum.jsonl`, zero code references | |
| | | nav lacks the API-route half of the atlas (`watch/SURFACE_ATLAS_20260903.md:57-61`) | |
| **TRANSDUCE** | record-makers for ambiguous actions | writer identity/lockfile on ractor_board (713MB, no in-repo writer attributable); retry-dedup intent ids; WAL-before-side-effect; observation authority; correction journal; tale-re-encoder; KZG proof field in `event_stream.emit`; gate v3 classifier (after its falsifier) | desk_scaffold_salon artifacts; TITOR_STACK:24-27; planning_rake |
| **DISPOSE** | built but unrun / unowned / stale | gate_v3 falsifier BUILT, never run; hyperspectral ROI falsifier unrun (BLOCKED on itself); chord test designed, unrun; lane_probe has no cadence owner ("no cron mills" — planning_rake:27); `state/CURRENT.md` stale since Aug 9 | hyperspectral_c:38; planning_chord_test:29 |
| **SUBSTRATE** | true waits | CUDA/ROCm (QLoRA → Rocinante Oct 27); flapping internet (tab_train). HUMILITY CLAUSE: the zcode-cli headless door was filed "substrate/blocked" — and the SAME night the claude-zai route closed it ("DOOR PROVEN 2026-09-03", `watch/engine_spec.json` engine-Z note). Re-verify substrate verdicts before believing them. | CAMPAIGN_SYNTHESIS:63-74 + engine_spec |

**The salon results, read together, are a wiring diagram — not a build list.** And the
diagram's shape is single-ended: everything must terminate at the tape, typed.

## 2. THE MEASURE (census, 2026-09-03 ~20:00Z)

- `watch/room.jsonl`: 5,325 rows; 5,315 carry no type/kind (prose `detail`); exactly 9 rows
  carry a kind (`salon`, from salon_runner's log_room). The humans' mirror is a chat
  transcript, not a bus — fine per tiered language law, FATAL for any action that ONLY
  becomes prose.
- `logs/memory_events.jsonl`: 383/383 typed memory_event.v1. `memory/runs/harness/events.jsonl`:
  347 rows, kind+seq+prev_hash+hash, live since 08-28. Typing is SOLVED where it is applied.
- Half-wire census: steer receipts 2 rows / no reader. organ_queue 0 rows / starving reader.
  bay_share 51 rows / TWO readers (the one fully-wired rail — and it is the youngest).
- `memory/biography/verkle_chain.jsonl`: 7,003 knots (was 6,537 at Titor filing — live growth).
- Receipt irony, filed as evidence: `watch/salon_receipts/campaign_build_order_20260903.json`
  carries `"receipts": {}` — the receipts organ filed an empty receipt for a salon ABOUT
  receipts. P-violation class "presence-of-output-as-substance," observed at home.

## 3. THE SOCROTIC ARC (what died, and why)

- **R0 — "The fleet lacks organs; build more."** DIED. 887 .py organs in mag/ alone; the
  organ-builder has an empty queue; four same-day planning salons independently concluded
  mostly DON'T-build (gate_v3, rake DELETE GUARD, tab_train nice-to-have, shadow_fields
  design-kills). Kill-list convergence is the fleet's strongest measured signal.
- **R1 — "Then the gaps are pure wiring."** DIED. The declared-missing list contains new
  code, not connections: tale-re-encoder, WAL-before-effect, retry-dedup identity are
  translators that do not exist. Connections cannot connect what isn't there.
- **R2 — "Then it's discriminators + typed-event density; the tape is weakly typed."**
  DIED under different-mind attack (§5). The buses are already ~100% typed — density ~1.0
  where buses exist; 0.2% was an artifact of reading the chat mirror. One "substrate" wall
  fell to a routing change the same night it was declared. A fourth gap class exists.
- **R3 — v3 survives (§1): coverage, four verbs.** The attack that killed v2 built v3:
  WIRE the half-wires, TRANSDUCE the ambiguous, DISPOSE the built-but-unrun, wait on true
  SUBSTRATE — and re-verify every substrate verdict against the attempt to route around it.

## 4. SYSTEMS ↔ SALON MAPPING (headline rows)

| Salon verdict | System evidence | Class |
|---|---|---|
| one_surface: "the one wire = steer receipt → event.v1, partially live" | producer exists (steer_bus.py), 2 receipts, NO reader ever found | WIRE (consumer end) |
| Titor: "missing ONLY layer-2: KZG into event_stream.emit" | emit rail clean + hash-chained (347 rows); proof field absent | TRANSDUCE |
| campaign: "biggest risk — ungated wings corrupt the maze-keeper brain" | gate_v3_falsifier.py BUILT, step-0 gate honest, never run | DISPOSE |
| planning_rake: "lockfile still unbuilt (2.24GB runaway scar)" | ractor_board.jsonl 713MB; no in-repo writer attributable | TRANSDUCE |
| desk_scaffold: 5 missing organs (WAL, obs-authority, correction journal, retry-dedup, late-binding) | no counterparts in mag/ | TRANSDUCE ×5 |
| captain_planet: seats hallucinated `mag cycle --check` | no such organ; real holder `mag/water_computer.py gravity_tick` | the discriminator absence, felt live |
| hyperspectral: "ROI falsifier unrun → premise BLOCKED" | one-script spec delivered; unrun | DISPOSE |
| shadow_fields: "every build is a design until it runs" | steer_field is the counterexample that RAN (FIELD.json + 3 consumers, receipt FIELD-L3-001) | pattern proven once — repeat |
| long_horizon: "disk is the supervisor" | the supervisor's own desk: state/CURRENT.md stale 25 days | DISPOSE |
| primer: "the ONE missing organ = tale-re-encoder" | no counterpart; starved by campaign order (correctly, per window math) | TRANSDUCE |
| stockfish: "eval ≠ decision" | eval organs exist (ask_router, percolator 47); decisions land as prose | TRANSDUCE |
| chord theory: "fold beats best post — unproven" | N=12 test designed ($0), unrun | DISPOSE |

## 5. ATTACK RECEIPTS (different-mind agent, 09-03)

- ATTACK 1 (closed loops without event.v1): steer_field↔churn closes on field.v1 + memlang
  tails; reconciler closes on snapshot diff; eyes receipt closed on vision.v1. **GRAZES** —
  closure needs schema'd artifacts, not event.v1 specifically. → v3 generalizes the currency
  and moves the claim to COVERAGE.
- ATTACK 2 (taxonomy break): fourth class exists — disposition debt (ownership, unrecoverable
  provenance, unrun falsifiers; verb = RUN/ASSIGN/EXCLUDE); headless door misfiled as
  substrate. **LANDS** → v3 adopts four verbs + the substrate humility clause.
- ATTACK 3 (metric wrong): buses already ~100% typed; 0.2% was the chat mirror; half-wire
  census itself CONFIRMED (writer-only / no-enqueuer / zero-refs). **LANDS** → v3 restates
  the metric as typed-event COVERAGE of real actions, not density on any one tape.

## 6. FALSIFIABLE PREDICTIONS of thesis v3 (kill conditions)

1. If coverage is the bottleneck: giving steer receipts ONE reader (a consumer organ) should
   produce a visible consumer behavior change within one cadence — zero new writer organs.
2. If disposition debt dominates: running the $0 gate_v3 falsifier flips a BLOCKED salon row
   to a verdict and changes a downstream build decision (per planning_gate_v3: no gate build
   until AUC ≠ ~0.5).
3. If the thesis is WRONG: the next new effector organ (another actor) will outperform
   wire/transduce/dispose work — the kill-list convergence predicts the opposite.
4. Metric: coverage = fraction of real actions (salon folds, wing completions, steers,
   dispatches) landing as typed rows on ANY bus. Baseline recorded in §2. Health = the
   fraction rising week over week. The room mirror may stay prose; the ACTIONS may not.

## 7. NEXT (cheapest first, all $0, awaiting window — two burst agents live on this box now)

1. DISPOSE: run `watch/gate_v3_falsifier.py` (headroom check first — it reads the 713MB board).
2. WIRE: one reader for steer_bus_receipts (the twin of the write that already happened).
3. TRANSDUCE: writer-identity lockfile on ractor_board (the runaway scar's actual fix).
4. DISPOSE: lane_probe owner assignment + CURRENT.md refresh (the supervisor's desk).

Sources: systems inventory + salon inventory (spawned sight-lines, this date), direct
measurement (§2), watch/TITOR_STACK_20260903.md, watch/CAMPAIGN_SYNTHESIS_20260903.md,
memory/runs/salons/* (19 results), watch/SURFACE_ATLAS_20260903.md,
memory/runs/salons/captain_planet/VERDICT.md, attack-agent receipts (§5).
