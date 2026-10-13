# witness_sampling — statistical honesty at scale

## Finding
witness_sampling is **NOT a standalone module**; it is a **statistical honesty discipline** enforced across the fleet by the **roshomon multi-witness invariant** and the **adventure_moonshot pipeline**. The claim this area makes is: *statistical honesty emerges from convergent multi-witness comparison (roshomon) and is anchored deterministically via verkle knots (lens_chain), not from isolated sampling artifacts.* This is **Supported** by repo shape.

## Evidence
- **roshomon.py** implements the multi-witness invariant: the same question is answered by N models (Rashomon), normalized into statements, and convergent statements become the ROSHOMON CORE (higher-confidence truth); divergent statements are preserved as perspective. The module dispatches via k8s swarm_worker and compares through invariants (lines 17–21).
- **adventure_moonshot.py** embeds this discipline: the pipeline is PRIOR -> WITNESS (roshomon.compare) -> SHADOW -> KNOT (lens_chain.resolve) -> MARRIAGE -> ROUTE. WITNESS is explicitly defined as `roshomon.compare(ask)` (lines 101–108, 19, 104–105).
- **swarm_worker.py** owns the dedicated queue drained by the k8s CronJob, ensuring no double-drain and no local spawns (lines 14–22, 50–63).
- **lens_chain.py** anchors each resolution as a content-addressed verkle knot with O(log n) inclusion proofs (lines 20–22, 159–186).
- **shadow_work.py** surfaces the Jungian shadow of each invariant, ensuring the system sees its repressed inverse (lines 1–19, 67–88).

No files named `witness_sampling.py` or `witness.py` exist; the domain is implemented as cross-cutting invariants and pipelines, not a module.

## Risk if wrong
If the audit treats witness_sampling as a module rather than a discipline, the examiner will miss that:
- Statistical honesty is enforced by convergent multi-witness comparison (roshomon) and deterministic anchoring (lens_chain), not by isolated sampling artifacts.
- The fleet's honesty relies on k8s-dispatched swarm_worker and content-addressed verkle knots; misreading this as "sampling rate" would break the understanding of how honesty is achieved.

## The act
Create a one-page **witness_sampling_primer.md** under `docs/ref/` that:
- States the claim: *statistical honesty = convergent multi-witness invariant + deterministic verkle anchoring.*
- Lists the three organs that enforce it: roshomon (multi-witness comparison), lens_chain (deterministic verkle knots), swarm_worker (k8s-dispatched queue).
- Names the one trap: treating it as a module rather than a discipline.

File: `docs/ref/witness_sampling_primer.md`

## Falsifier
To prove this wrong, show a file named `witness_sampling.py` or `witness.py` that implements a sampling-specific module with its own tests and schema. Absence of such a file falsifies the claim that it is a discipline, not a module.
