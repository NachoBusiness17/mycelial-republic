# EVENT-DRIVEN RESONANCE - the spiking chapter

Class: RECEIPT (gala_20260925 spiking-wide, division B, lane event-driven-resonance)
Written: 2026-10-01 by the lane seat. Companion lane JSON:
`watch/inbox/gala_20260925/spiking-wide/lanes/event-driven-resonance.json`

## The seed this lane takes seriously

The drop receipt's resonance note (`watch/inbox/SPIKINGBRAIN_DROP_20261001.md:54-56`):

> "Event-driven resonance (concept, not port): 'only thinks when
> triggered' is the dream-cycle's quiescence gating and the boot-trigger
> law, at the neuron level. The estate keeps arriving at the same shape."

The drop said "concept, not port". This lane mined the concept against the
neuromorphic/spiking literature and the estate's own bytes, and found the
note UNDERSELLS the estate: the convergence is real, structural, and in
three places byte-identical in shape - and the one place the estate diverges
(homeostasis) is the one mechanism the literature says a spiking system
cannot live without.

## CONVERGENCE C1: only-thinks-when-triggered (trigger-gated sparse compute)

The neuromorphic law: spend compute only on change. Spikes are events; a
neuron at rest costs nothing.

- Lit side (byte-fetched 2026-10-01):
  - SpikingBrain (arXiv:2509.05276, CAS-I BICLab), abstract, verbatim:
    "deliver inference with (partially) constant memory and event-driven
    spiking behavior" and "the proposed spiking scheme achieves 69.15
    percent sparsity, enabling low-power operation".
  - Loihi 2 (open-neuromorphic.org hardware page, verbatim): "spiking
    dynamics, sparse connectivity, and asynchronous event-driven
    communication"; "All the communication between NCs is in the form of
    spike messages."
- Estate side (code, byte-read 2026-10-01):
  - The boot-trigger law: `watch/inbox/STEALTH_DRIVER_247_20260927.md:3-4`,
    verbatim: "Built on the boot-trigger law (Startup logon, never clocks;
    stoppable on the operator's single word)". Activity fires on the boot
    EVENT, never on a timer - the estate's version of spike-triggered
    computation instead of clocked computation.
  - The dirty-block law: `mag/field_flow.py:210-219` - "next tick's active
    set = cells with gross movement (in OR out ...) plus their neighbors".
    A cell that received no event is not processed. `mag/field_flow.py:228-237`
    (`run`): "stops early when the board is quiescent (empty dirty set)".
    This is event-driven sparse activation, in software, already shipped:
    only the touched neighborhood re-activates, and the whole board falls
    silent when flow stops.
  - Quiescence-gated background organ: `mag/switchboard_v2.py:716-719` -
    `{"condition": "board_quiescent", "priority": 3, "eligible_organ":
    "swarm_cycle", ... "reason": "Board has <5 notes; suggest cycle run"}`.
    The dream-cycle organ (swarm_cycle) only becomes eligible when the board
    is quiet - the estate's version of "think only when the waking board
    releases you" (also mirrored in `mag/harness.py:565`).

Shape match: TRUE at the system level. The estate computes on deltas, sleeps
on quiescence, and triggers on events; SpikingBrain/Loihi compute on spikes,
sleep between them, and fire on membrane events.

## CONVERGENCE C2: integrate-then-fire (threshold firing)

The neuromorphic law: evidence accumulates (membrane potential), and nothing
happens until a threshold crosses; then everything happens at once (a spike).

- Lit side (byte-fetched 2026-10-01):
  - Richter et al., "Event-Driven Language Models with Sparse Neural Activity
    for Neuromorphic Hardware" (arXiv:2608.30439, submitted 31 Aug 2026),
    verbatim: "Activations below a per-projection trainable threshold (plus
    or minus delta) are nullified while preserving crucial outliers" -
    software LLMs already fire on learned thresholds.
  - SpikingBrain abstract, verbatim: "linear and hybrid-linear attention
    architectures with adaptive spiking neurons".
  - Loihi 2 (byte-fetched): "various resonance, adaptation, threshold, and
    reset functions for more complex and nonlinear temporal representations."
- Estate side (code):
  - The attention market fires on fixed thresholds:
    `mag/attention_ranker.py:145-146` - score `= max(0, min(100, round(raw /
    11.2 * 100)))` then `band = "P1" if score >= 72 else "P2" if score >= 52
    else "P3" if score >= 32 else "P4"`. An attention item below 32 does not
    surface as a priority band at all: integrated input, threshold, fire.
  - The percolator compiles on recurrence:
    `mag/percolator.py:14-15` - "if that canonical has been seen before ->
    REPEAT -> compile to INVARIANT ... Recurrence = stable truth worth
    compiling." One sighting does nothing; the SECOND sighting fires the
    invariant into the registry. That is threshold = 2 integrate-and-fire.

## CONVERGENCE C3: leak and refractory (temporal dampers)

The neuromorphic law: membrane potential leaks toward rest, and a just-fired
neuron cannot immediately re-fire.

- Lit side (byte-fetched 2026-10-01):
  - Gerstner et al., Neuronal Dynamics (EPFL online book, ch 1, sec 4),
    verbatim: "If the presynaptic spike arrives during or shortly after a
    postsynaptic action potential, it has little effect because some of the
    ion channels that were involved in firing the action potential are still
    open." (Reduced responsiveness shortly after a spike; the book states the
    relative-refractory effect without using the term on this page.)
- Estate side (code):
  - Leak: `mag/percolator.py:140-154` (`_decay_count`, Z15 law 1) - "count
    halves every half_life_days without reinforcement", floor at 1. The
    invariant's count is a leaky integrator: reinforcement charges it,
    silence discharges it.
  - Refractory: `mag/switchboard_v2.py:81-83` - "Replay protection: event_ids
    that have already been granted. A second proposal for the same event_id
    must not produce an independent AUTHORIZED grant - at minimum the second
    is refused as a replay." A fired effect cannot re-fire on the same event.
  - Per-cycle refractory: `mag/percolator.py:31-34` (Z15 law 3,
    self-emission cap) - an invariant reinforced by the same source within
    the same cycle counts once. Same-source re-fire inside one integration
    window is absorbed, not summed.

## CONVERGENCE C4: homeostasis (set-point control) - the estate's sharpest GAP

The neuromorphic law (Turrigiano's test): a mechanism is homeostatic only if
it senses its own activity, computes an error against a set point, and adjusts
excitability to return toward it.

- Lit side:
  - Turrigiano, "Homeostatic Synaptic Plasticity: Local and Global
    Mechanisms" (Nat Rev Neurosci 2012; PMC3249629), fetched fragments,
    verbatim: homeostatic plasticity should "regulate a key parameter (such
    as average" firing "around some set-point value"; synaptic scaling
    "adjust all of a" neuron's excitatory synapses up or down "in the correct
    direction to stabilize firing", over a temporal scale of "hours".
    (Fragments as returned by the page reader; the two gaps are the reader's
    elisions, not edits.)
  - Loihi-side adaptivity (byte-fetched, Loihi 2 page): "various resonance,
    adaptation, threshold, and reset functions". Davies et al. 2018 (IEEE
    Micro, "Loihi: A Neuromorphic Manycore Processor with On-Chip Learning")
    is the bibliographic anchor for on-chip threshold adaptation; the PDF
    fetch failed (application/pdf unsupported), so the specific
    "intrinsic excitability homeostasis" wording rests on the search result
    summary, NOT on fetched bytes - labeled accordingly.
- Estate side: HALF a homeostat, operator-mediated.
  - The Z15 runaway and patch: `mag/percolator.py:24-26` records that the
    top invariant had reached 232,214 self-reinforcements, 79.8 percent of
    all events, because each fire re-incremented the invariant that ordered
    the fire. This is the textbook homeostatic failure mode (runaway
    self-excitation), and the Z15 count laws (decay + per-cycle cap,
    `mag/percolator.py:27-34`) are a textbook partial cure. But it was
    diagnosed by the S15 seat and patched by an operator decision - the
    estate's homeostat had to pass through a human.
  - The one cell-autonomous homeostat: the FTS index loop (AGENTS.md B2-465).
    `tools/corpus_fts_rebuild.py --check --deep` senses decay (catalog moved
    past the index), computes the error (exit 2), and the MagFtsIndexDaily
    task applies the fix itself ("rebuilds through the one sanctioned writer
    on exit 2") without an operator. Sensor, set point, corrective action -
    Turrigiano's definition, in cron form.
  - The attention market has NO homeostat: the band thresholds at
    `mag/attention_ranker.py:146` are constants (72/52/32). If the surface
    floods the operator with P1s, nothing raises the bar; in a drought,
    nothing lowers it. The only guard is a hard `limit` on the ranked list
    (`mag/attention_ranker.py:280` `build_ranked_attention(*, limit: int =
    12)`), which is a rate ceiling, not set-point regulation: it silently
    drops the overflow instead of restoring sensitivity.

## SHARPEST CONVERGENCE (declared)

C1, only-thinks-when-triggered, is the sharpest: it is the one where the
estate did not merely imitate one mechanism but independently converged on
the full neuromorphic SHAPE at the system level - event-triggered start
(boot law), sparse delta-processing (dirty-block law), quiescence-gated
background compute (board_quiescent organ gate) - and where the practical
payoff already shows (the dirty-set board stops ticking; the driver never
burns cycles between boot events). C2 and C3 are single-mechanism echoes;
C1 is a worldview echo, and it is the one the drop receipt called "concept".
Verdict: concept confirmed as structure.

## PORT VERDICT (this month)

YES - exactly one mechanism should port to estate software this month, and
it is the gap in C4:

PORT: homeostatic threshold adaptation for the attention market.
`mag/attention_ranker.py` band constants (72/52/32 at line 146) become
slowly adapting bands with a set point (example set point: P1 count per
build in a 1-3 band). If a build produces more P1s than the set point,
multiplicatively raise the thresholds (synaptic-scaling style: scale all
bands, preserving relative order, per Turrigiano); if fewer, decay them
back toward 72/52/32. Measure-first gate: log the P1 count per
build_ranked_attention call for a few days BEFORE changing anything - if
the count is already stable under the limit-12 ceiling, the port is
unnecessary (falsifier, stated in advance).

NO-PORT NEEDED (already converged): threshold firing (percolator repeat
gate, attention bands), leak (half-life decay), refractory (replay
protection + self-emission cap), trigger-gated compute (boot law,
dirty-block, quiescence gate). Re-porting any of these would relearn what
the estate already holds - the Descent Protocol's prior-art sweep clause
applies to the estate's own organs too.

NO-PORT (would be play, not physics): full SNN dynamics (spike trains,
temporal coding) - the estate's events are coarse (file growth, board
notes, fires); sub-event timing carries no signal at this granularity.
SpikingBrain's linear-attention long-context rung is a WATCH item from the
drop receipt (its estate map item 1), not a resonance port.

## Sources (provenance-labeled)

Byte-fetched 2026-10-01 via page reader:
- arXiv:2509.05276 abstract (SpikingBrain), https://arxiv.org/abs/2509.05276
- arXiv:2608.30439 abstract (Richter et al., event-driven LMs), via
  https://www.alphaxiv.org/abs/2608.30439
- Loihi 2 overview, https://open-neuromorphic.org/neuromorphic-computing/hardware/loihi-2-intel
- Turrigiano 2012 review (fragments), https://pmc.ncbi.nlm.nih.gov/articles/PMC3249629
- Gerstner et al., Neuronal Dynamics ch1 s4, https://neuronaldynamics.epfl.ch/online/Ch1.S4.html

Search-derived (not byte-verified, labeled):
- Davies et al. 2018, "Loihi: A Neuromorphic Manycore Processor with On-Chip
  Learning", IEEE Micro (PDF at
  https://redwood.berkeley.edu/wp-content/uploads/2021/08/Davies2018.pdf
  fetch returned unsupported application/pdf; homeostasis wording taken from
  the search result summary only).

Estate bytes (read this session, line-cited above):
- mag/field_flow.py:210-241 · mag/switchboard_v2.py:81-83, :266-269, :705-719
- mag/attention_ranker.py:141-146, :280 · mag/percolator.py:14-34, :140-154
- mag/harness.py:565 · watch/inbox/STEALTH_DRIVER_247_20260927.md:1-24
- watch/inbox/SPIKINGBRAIN_DROP_20261001.md:54-56

## Checks

See `watch/inbox/gala_20260925/spiking-wide/lanes/event-driven-resonance.check.txt`
(raw output of the finish-line byte checks, run 2026-10-01T18:36:49Z: 4
convergence headings, sharpest declared, port verdict present, 17
estate-side line-citations, 20 lit-side citation hits, em-dash count 0 in
receipt and lane JSON, JSON parses) and
`.../lanes/event-driven-resonance.fts-homeostat.txt` (live run of the
estate's one cell-autonomous homeostat sensor this session:
`.venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check --deep`,
EXIT=0, "index_state": "fresh", "deep": "match" - the sensor is healthy
today; the C4 loop it embodies fired nothing because there was no decay).

## Decision ledger

Closes: the drop receipt's open question ("Event-driven resonance (concept,
not port)"). Answer: real convergence at the system level, byte-backed on
both sides (C1 sharpest); the estate is missing only homeostatic
set-point control, and the one port candidate for this month is
attention-band adaptation with a stated falsifier and a measure-first gate.
Changes nothing in code this lane; the port decision itself stays with the
operator (it edits mag/attention_ranker.py, a live organ).
