# MORPHOGENIC SWARM DEFENSE STEAL (2026-08-10)
Researcher: ghost · Operator vision: "shape our agent swarms on the fly into shapes to carry out
fixes while shit hits the fan — a firefighting robot swarm." · Sources: morphogenetic robotics (Jin),
artificial immune systems (Forrest et al.), swarm robotics (Dorigo et al.) + our OWN signal_flare/
shape_map/flock_field/process_reaper/swarm_health.

## The one-line
The firefighting swarm is MORPHOGENIC defense: the incident doesn't select a pre-made formation — it
MORPHS one. A regulatory program maps stimulus -> shape, the swarm grows the right counter-formation
live, fights under fire, then dissolves back.

## EXTERNAL STEAL — 3 real systems, 3 invariants
1. MORPHOGENETIC ROBOTICS (Jin): self-organization, self-reconfiguration, self-assembly, self-adaptive
   control; morphogenetic swarm robotics = self-organizing multi-robots via gene-regulatory-network (GRN);
   modular robots adapt their CONFIGURATION autonomously. INVARIANT: **the shape is regenerated from a
   regulatory program + environmental signal, not stored** -> shape is DERIVED, not fixed.
2. ARTIFICIAL IMMUNE SYSTEMS (Forrest et al.): negative selection (train detectors on normal, flag
   anomalous), clonal selection / affinity maturation (remember + IMPROVE response to antigens over time),
   immune network (nodes/edges by affinity), danger theory (respond to DANGER signals, not just foreign),
   dendritic cell algorithm (multi-scale granulation). INVARIANT: **a distributed doctor that learns,
   remembers, and mounts a shaped response** = our failure_kb + doctor + swarm.
3. SWARM ROBOTICS (Dorigo et al.): no centralized control or global knowledge, local perception+feedback,
   cooperate, fault-tolerant, scalable, heterogeneous formations (flying+climbing+ground), stigmergy as
   coordination (indirect comm via environment). INVARIANT: **decentralized, stigmergic, heterogeneous** =
   our flock_field (field IS coordination, no central orchestrator) + flock on k8s.

## SELF-STEAL — we already hold the machinery (compose, don't reinvent)
- signal_flare: distress protocol; a flare = MINIMAL hash + pattern fingerprint + breadcrumb; contains
  NOTHING sensitive; "I am stuck. Here is the SHAPE of the problem." LAW: flares public, problems private.
  = the DEAD DROP + shape intel, already built.
- shape_map: every subsystem as a portable VERKLE-backed shape; merkle verify; stateless reconstruction.
  = the SHAPE substrate for morphogenesis.
- flock_field / flock_scheduler: geometric field-steering, emergent allocation, cheapest-capable tier.
  = the decentralized swarm that can re-form.
- process_reaper / process_supervisor: supervised leak sweep + start/stop/restart/reap.
  = the fire axe (runaway-python counter-formation).
- swarm_health: liveness/heartbeat/staleness + breaker. = the vital signs.

## THE COMPOSED INVARIANT (the steal)
Morphogenic swarm defense = incident signal (from failure_kb/leak_detector/sentinels) -> a REGULATORY
function (the incident-shape -> counter-formation map, grounded in shape_map) -> the flock morphs into
the counter-formation (reaper-swarm for process sprawl, heartbeat-swarm for connection-refused,
deamplifier for collapse, sprouter for capacity starvation) -> fights under fire -> dissolves.
The doctor (AIS) remembers + improves the response; failure_kb (negative selection) learns what's normal;
signal_flare is the dead drop. Response is decentralized (swarm robotics) and shape is derived (morpho).

## Fold note
Compose signal_flare + shape_map + flock_field/scheduler + process_reaper + swarm_health + failure_kb +
doctor into a dispatcher: signature -> formation. This is the emergency mode of the ghost server.
