# DEEP-MYCELIAL-ROUTING: task flow as fungal transport physics on the estate

Authored 2026-09-28, burn_reset flash50. Every estate claim below cites a file I read or a
check I ran this session (commands and outputs in section 7). Literature anchors are named
from memory by author/year, not fetched this session; they carry no quotes and are marked as
such. No em-dashes per law.

## 1. The estate is already a mycelium; it just has not read its own plumbing

The ask asks me to design mycelial routing. The finding that reframes the design: the
estate has independently built every structural component of a fungal transport network, in
code, with dates. The hydraulic module's own docstring says it outright:

- `mag/water_graph.py:1-3`: "routing as physics, not a hardcoded pair", built by operator
  order 2026-09-27 ("use the physics instead of fighting them"). It is a real flow engine:
  one-way pipes (check-valve law, "no backflow by construction", `mag/water_graph.py:13-15`),
  integer pipe capacity, siphons that prime only above a crest volume, and junction kinds
  xor / sill / any (`mag/water_graph.py:24-31`).
- Steam is a second routing medium that "rises regardless of pipes" and condenses at the
  highest `cold` node (`mag/water_graph.py:18-20`).
- `mag/water_computer.py:119-120` already states a growth law: "an unmapped room must not
  grow a surprise valve". No accidental edge creation.
- `mag/gpipes.py:1-7` is the fan-out organ: "Governor pipes: parallel fan-out of isolated
  sub-agents + merged collection", every worker an orchestrator task so pipes inherit
  crash containment and kill-tree semantics.
- `mag/swarm_surface.py:63-70` is the exploration organ: `route_novel` dedupes a novel goal
  by anchor, idempotent, and comments "Do not silently turn every novel surface into a paid
  DeepSeek dispatch" (janitor-first flow law).
- `mag/arrival.py:3-15` is the feedback organ: the swarm authors its own RIBs from its filed
  research packs and folds them "via the shared rib_bus primitive", so "the whole swarm gets
  smarter with every fold".
- `memory/rib_bus/standing-wave.json` rib sw04struck0000004: the propagation loop is named
  in the estate's own words: "route_novel -> swarm -> field corpus -> other agents".

Mapped onto fungal transport: watch/inbox is the nutrient source; lanes (`configs/lanes.yaml:8-26`) are hyphae of different diameter; the percolator (`memory/percolator/invariants.json`) is the flow counter; rib_bus domains are the older parts of the colony; receipts and trails (`dashboard/static/trails/*.jsonl`, 26 rows in forge, 31 in elder) are the growth rings; the verkle chain is the mycelial mat everything anchors into.

## 2. Flow shapes already measured: one thick cord dominates

Fungal colonies start as an exploratory fan of fine hyphae and reorganize into a few thickened transport cords carrying most flux, with the rest pruned (Bebber et al. 2007, Proc R Soc B, "Biological solutions to transport network design"; Fricker, Boddy and Bebber 2007 on network organisation of mycelial fungi; named from memory, not fetched). The estate shows exactly this pattern in its own telemetry:

Check run this session (`memory/percolator/invariants.json`, 352 invariants total, top counts):
1. 232,214 firings: "[steer] Elevate with a deliberate ask: frozen prefix (cache-shared) + tight ask + output contract". This is the trunk cord: the deliberate-ask route carries the overwhelming majority of observed signal.
2. 38,042: "backend reported failure". 3. 8,377: "command not allowlisted: powershell". 4. 4,027: "[Errno 2] No such file or directory: 'powershell'".

Interpretation, with care: these are signal-seen counts, not work units. But the shape is mycelial: a handful of high-flux trunks, and repeated pressure against the same two walls (the powershell allowlist wall shows up as two distinct invariants, 8,377 plus 4,027, meaning the flow keeps hitting it and splitting into two marks). In a real colony a path that carries flow gets tubed (diameter grows); a wall that keeps getting hit gets a bypass grown around it or a door opened. The estate does the first by hand (laws repeated into AGENTS.md bullets) but has no automatic diameter response to wall-pressure invariants.

## 3. The pressure gradients, concretely

The ask asks: what are the pressure gradients? Four real ones exist, each with a mechanism:

**(a) Priority pressure (elevation).** `configs/lanes.yaml:76-79` defines the markers `[priority]`, `[grok]`, `[L2]`; L2 requires one (`configs/lanes.yaml:22`, `require_priority: true`); local markers (`[mag]`, `[L0]`, `configs/lanes.yaml:81-85`) are the low-elevation floor. The specialist lane only receives flow when marked, and head is finite: `grok_budget.max_escalations_per_day: 2` (`configs/lanes.yaml:72-74`). That is turgor rationing, exactly like a fungus spending its osmotic budget on the advancing margin rather than uniformly.

**(b) Deadline pressure (hydraulic head decay).** `queue/todo.md` P0 row: the Cerebras card gate "owed since 2026-09-21, deadline 2026-10-03 ... the trial-gate intel goes stale under the repo 7-day law on 2026-10-03". Deadlines here are not dates alone, they are couplings: a deadline exists because two clocks (trial expiry, staleness law) are running on the same nutrient. The strike clock makes deadline pressure audible: `scripts/tide_strike_clock.py:11-12` exit 0 clean below 2 strikes, exit 3 WARN at exactly 2 ("the obligation is one tide from its falsifier"), exit 2 VOID-CONDITION-MET at 3 or more ("this clock only makes it loud"; the void itself stays an operator gate). That is a pressure gauge, deliberately not a valve.

**(c) Freshness pressure (differential sensor).** `tools/freshness_check.py:8-11,53`: a doc is STALE when its last commit is older than STALE_DAYS=7 "while the repo itself has heartbeat" (HEARTBEAT_DAYS=2). This is the most fungal idea in the estate and I want to name why: staleness is measured RELATIVE to the living network's beating, not in absolute time. A hyphal segment is not old in days, it is regressing because it stopped sensing flow around it. The census drift patrol (B2-215/244, AGENTS.md clippy bullets) is the same gradient applied to claim freshness: the carrier counts as stale when tests/ grows underneath it.

**(d) Throughput backpressure.** AGENTS.md fan-out width law (given material, with receipts at `watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md` B2-476 and `watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md`): Task agents ride maxAttempts 11 and measured clean at widths 3, 6, 10, 12 (109.4M tok/h at width 10); workflow children get maxAttempts 0 and the 50-wide workflow shape 429-storms the account. 429/1302 contact is a HOLD signal, not a break. This is Poiseuille reality: flow through a pipe of radius r scales as r^4 under a fixed pressure drop, so flow concentrates in the widest pipes and overload appears first as rising backpressure, not instant failure. The estate's two pipe classes (Task agents wide, workflow children narrow, max_concurrency 3 or less) ARE different diameters for different classes, already tuned by experiment.

**(e) Cost pressure (the meter).** `configs/lanes.yaml:96-106`: multi-lane fan-outs must clear "premium x baseline value per 1k tokens" or the value-per-token admission gate rejects the spend. Mycelia spend cytoplasm at the margin; the estate spends tokens at the margin.

## 4. Network growth: four mechanisms present, one broken

Growth in the estate is not hypothetical; each mechanism has a body:

- **Exploration (hyphal fan):** `mag/swarm_surface.py:63-70` route_novel, anchor-deduped, free-first by default.
- **Strengthening (tubing):** the percolator accumulates counts on repeated signals (section 2); laws learned twice graduate into AGENTS.md and ribs; rib_bus folds warm the shared prefix every worker mounts (`mag/arrival.py:10-15`).
- **Fusion (anastomosis):** interagent pass-off, enforced structurally by the workflow gate: `tools/workflow_gate.py:24` shows gates G1-G7 "each minted from a real memory/workflows/REGISTRY.jsonl FAIL" row, with checks for per-item named actors and outputs feeding later asks. Scar tissue before new tissue.
- **Pruning:** measured this session on `catalog/junctions.jsonl`: 79 rows, 79 with `"action": "pruned"`, 0 with `"violation": true`. Every filesystem junction the survey found was pruned; the estate currently treats edge-creation at the OS layer as attack surface, zero tolerance. Soft pruning exists too: dormant lanes (`queue/todo.md` Cerebras "stays dormant: true, no card attach"), and FKB ratchet prune 943 to 941 (commit d90bc8607).

**The broken one, measured today:** the growth organ that folds the swarm's own authored knots is producing degenerate tissue. Check run this session on `memory/rib_bus/arrival.json` (pretty-printed JSON, 2 rib rows): BOTH rows are degenerate, the worst carries 25 literal repeats of the template string "Invariant body:" (dated 2026-09-28, today). My first attempt to parse this file as JSONL failed (JSONDecodeError, line 2); I corrected to `json.load` and reran; both numbers above are from the corrected run. Diagnosis from `mag/arrival.py`: fold_authored distills pack text mechanically; when a pack lacks a clean invariant the template's placeholder is concatenated instead of elided, so the fold publishes a tumor into the standing wave where it warms every future worker's prefix. The fungal analog is tip growth without polarity: callus, not hypha. The fix has an existing template in the estate: the STARVATION LAW in `mag/water_graph.py`'s tick (operator, 2026-09-28, "this whole starve-out thing is bullshit"): under-gate inflow is HELD, not spilled, and any loss emits a named STARVED line with node, amount, and gate. Applied to growth: a fold whose payload fails the placeholder check must be HELD (not folded, not published) and emit a named event; silent tumor growth is what a receipted network must never do.

## 5. The design: implement MYCELIAL ROUTING as a WaterGraph, with a Murray-law diameter rule

No new engine is needed. The estate's flow engine is deterministic, integer, $0, and already tested (`mag/water_graph.py:22-23`: "Deterministic: insertion-ordered pipes, integer volumes, no floats, no RNG"). My proposal is a mapping plus one dynamic law.

**Mapping:**
- **Nodes = organs.** elev = lane tier (L0 local = low ground, L2 specialist = high ground: escalation literally flows uphill against gravity, which the one-way check-valve law enforces as ascend-only; receipts descend the graded drains, descend-only). volume = pending load. `cold` node = the operator when present; `waste` = voided/L3-human overrun; a `waste` receive must always emit, never swallow (the anti-starvation law's spirit).
- **Pipes = routes.** cap = the measured concurrency envelope per pipe class (workflow children 3, Task agents up to 12, per the width law). One-way by construction: escalation only ascends.
- **Junctions:** xor = the exclusive-choice router (one task, one seat; both inlets on the same tick means the task was double-claimed and the duplicate overflows to waste, loud). sill = quorum gates: the judge cascade in `configs/lanes.yaml:120-145` (band_routine tau 0.90 pass/escalate, band_derivation always_escalate) is a sill with threshold; under-gate verdicts are HELD for a later tick, never silently spilled. siphon = the deliberate-ask: "Pay the context tax once" (AGENTS.md clippy) is exactly a crest volume that primes the big pipe; frozen RIB + brief attached (`configs/lanes.yaml:74` attach_brief) is the priming fluid.
- **Steam = deferred work.** Background cadences (MagFtsIndexDaily 09:00, MagCensusPatrolDaily 08:30, offpeak queue, per AGENTS.md) rise regardless of the pipe network and condense at the highest cold node; no operator online means they fall back to origin (run and log), which is what the scheduled tasks already do.

**Pressure gradient P at a source node** combines the four gradients additively in integer units: priority marker (+head, fixed table from lanes.yaml markers), deadline proximity (head rises as the deadline clock crosses strike thresholds, so the strike clock's 0/2/3 ladder becomes elevation), freshness delta (age minus repo heartbeat, the freshness_check comparison), and cost gate (the value-per-token test as a check-valve that refuses to open on unaffordable edges).

**The one dynamic law (diameter):** Murray's law (Murray 1926, named from memory) says the optimal vessel radius balances pumping work against maintenance cost, giving the cubic branching relation r_parent^3 = sum(r_child^3); Poiseuille's r^4 term is why doubling a cord's diameter multiplies its flow 16x. The estate's routing should adopt the flux form, not the geometry form: on every `gpipes collect` / workflow close, each traversed route's cap moves toward its measured envelope if it carried successful flow that fed a LATER ask (flow-through, not fire-and-forget), and decays toward `dormant` after W windows of zero flow-through. Two seed calibrations from this session's measurements: the deliberate-ask trunk (232,214 counts) should already be at maximum diameter, and it is (it is frozen into AGENTS.md and the rib layer); the powershell wall (12,404 combined marks on two invariants) has repeatedly been hit but never grown a bypass, which is the concrete first task the diameter rule would surface.

**Growth gate (anastomosis law):** a new edge (new lane, new rib fold, new skill) may open only from (a) a minted gate row citing a real FAIL (`tools/workflow_gate.py:24` precedent) or (b) a fold that passes the placeholder check (section 4 fix). Every growth event writes a row in the junction ledger's style (target, class, action, note) so the network's own expansion is receipted like its pruning already is: 79/79 pruned rows is the standard the growth side must meet.

## 6. What the fungi know that the estate has not copied yet

1. **Flow-sensing remodeling.** Real colonies reorganize along measured transport, not planned transport (Bebber 2007). The estate's percolator counts signal occurrences; it does not count flow-through (did this route's output feed a later ask?). The workflow gate checks pass-off structurally at submit time (`tools/workflow_gate.py` dogfood checks); making it a per-route counter is the difference between a census and a bloodstream.
2. **Bidirectional translocation.** Fungal transport runs both directions at once (Fricker et al., named from memory). Estate receipts flow one way (done, fold, warm). Negative backflow exists only at verdict points (the judge cascade escalate, `mag/lane_runner.py:278-293` band logic) and as LAW-056 counter-teeth (economist RED flags to the operator inbox, `mag/lane_runner.py:13`). Route-level backflow: a route whose result is REJECTED should lose diameter, not just the verdict escalate.
3. **Redundant loops.** Hyphae fuse into loops so one cut isolates nothing (anastomosis, Fricker et al.). The estate is tree-shaped on dispatch: one tethered account, and the width law documents 1302s after bursts. The mycelial answer is already half-present: free lanes are a SENSING surface (driving ladder, AGENTS.md), thin exploratory hyphae that map the terrain ahead of the funded transport cords. Full loop closure (a second funded medium, Hermes $180 Nous credits, dormant but dispatch-capable) is the estate's un-built anastomosis; the design does not invent it, it only notes the width law's "the limit is rolling throughput, not width-only" is a statement about one cord and would be false of a looped network.
4. **Dead-end regression.** Fungi reclaim cytoplasm from abandoned tips. `memory/rib_bus/next_wave.json` has 0 ribs (measured this session): an empty domain stub. The diameter law's decay gives this the mechanical form: zero flow-through for W windows, automatic `dormant: true` with a receipt, reactivation only through route_novel (which dedupes), never by silent re-growth.

## 7. Checks run this session (exact commands, outputs)

1. `catalog/junctions.jsonl`: `wc -l < catalog/junctions.jsonl` = 79; `grep -c '"action": "pruned"'` = 79; `grep -c '"violation": true'` = 0.
2. Percolator: `.venv/Scripts/python.exe -c` sorted `memory/percolator/invariants.json` by count: top 4 = 232,214 / 38,042 / 8,377 / 4,027; total invariants 352.
3. rib_bus domain census (each `memory/rib_bus/*.json` via json.load): 49 domain files; largest k3s-toolset 585 ribs, standing-wave 86, doctrine 25; next_wave.json 0.
4. arrival.json degeneration: first run as JSONL failed (JSONDecodeError Expecting property name, line 2); corrected to `json.load`: 2 ribs, both degenerate, max "Invariant body:" repeat count 25, ts 2026-09-28.
5. Freshness thresholds read from `tools/freshness_check.py:53` and docstring lines 8-11: STALE_DAYS=7, HEARTBEAT_DAYS=2.
6. Strike clock ladder read from `scripts/tide_strike_clock.py:11-12,92-95,101`: exit 0 / 3-WARN@2 / 2-VOID@>=3.
7. Trails: `wc -l` on forge.jsonl = 26, elder.jsonl = 31.

Not run this session: no pytest suite (the ask names no test and no code was changed), no web verification of the literature anchors (they are named from memory and carry no quotes), no live route_novel or gpipes invocation (design document only; both organs were read at source instead).

## 8. The one-sentence version

The estate does not need a mycelial metaphor bolted on; it needs its own water engine (`mag/water_graph.py`) pointed at its own task graph, with pressure defined as the priority/deadline/freshness gradients it already instruments, diameter defined as flow-through-proven capacity it already measures at the edges (width law, judge tau, percolator counts), and growth gated the way its pruning already is: every new hypha receipted, every held drop of work named, and the one place where growth is running wild today (arrival.json's 25-fold template tumor) named as the first repair.
