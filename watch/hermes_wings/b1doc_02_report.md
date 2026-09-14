# hermes docs wing 02

via resident b1 beat ext-fcf70944b4 folded=True

Agent requests NAS to arm one external one-shot per job at its real next-fire time; NAS calls back with a short-lived JWT, agent verifies and runs the job, then re-arms the next one-shot. Uses JWT verification, compare-and-set claim for at-most-once, and store-level CAS across replicas. No single-po
