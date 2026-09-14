# TESUJI_DISSECTION_20260831 — two items, one conclusion, everything teased out

Operator order (15:59Z): two items arrived at the same conclusion — find their
paths, what they did, what evidence they used, how it compounds ours, what gaps
it fills, where else it connects. The pair with the deepest shared conclusion
today: **WikiSkill (Google) and CUDA-Agent (ByteDance×Tsinghua)** — both landed
on: *agents improve through their own residue, gated by validation.*

## 1. PATHS — what each actually did
- **WikiSkill:** trace → wiki → skill. Three layers; the wiki NEVER rolls back;
  the skill reverts on regression. Moves knowledge out of the optimization
  history and into a durable corpus. Evidence: 5 benchmarks × multiple model
  families; ablation (wiki off → big drop); transfer ACROSS families.
- **CUDA-Agent:** act → verify → reward → RL. One environment, physical truth
  (compile/run/profile on real GPU), reward = measured speed. Moves expertise
  into weights via PPO. Evidence: KernelBench SOTA, 40% over frontier
  proprietary, verified against paper abstract byte-for-byte.

## 2. SAME CONCLUSION, OPPOSITE GEOMETRY
Both: *experience must be compiled and gated, or it evaporates.* But —
- WikiSkill compiles OUTWARD: traces → text. Cheap, inspectable, transferable,
  no training. The understanding is the artifact.
- CUDA-Agent compiles INWARD: environment → weights. Expensive, opaque,
  non-transferable, permanent. The competence is the artifact.
They are the two transports of the same physics. WikiSkill = water to ice
(structure you can read). CUDA-Agent = water to steam (power you cannot see).

## 3. EVIDENCE BUDGETS — what each dared to measure
- WikiSkill bet on ablation: turn the knowledge layer OFF, watch the score drop
  ~a quarter. It proved the *corpus* is the active ingredient.
- CUDA-Agent bet on physical ground truth: the GPU doesn't negotiate. It proved
  the *loop* is the active ingredient.
Invariant: **both refused to let the improvement be vibes.** One used held-out
benchmarks; one used hardware counters. Neither used taste.

## 4. HOW IT COMPOUNDS OURS
- Our stack holds WikiSkill's OUTWARD transport natively: memory-RIB, receipts,
  residue map, ractors. Everything we built today is the ice.
- Our stack HOLDS NO inward transport: no RL loop, no training rig. Steam we
  do not make. But — the x-search confirmed CUDA-Agent open-sourced the
  ENVIRONMENT + SKILL.md + dataset (not weights). That is the inward transport's
  *mold*, published. If we ever pour, the mold is free.
- Compounding move: our receipts ledger is a wiki-shaped corpus that never rolls
  back. The failure-KB IS the wiki layer. We have been running WikiSkill's
  architecture since before the paper existed — the paper proves our loop's
  knowledge layer is the active ingredient (~quarter of the score, per their
  ablation).

## 5. GAPS FILLED — named, per the lift doctrine
- GAP: "is our receipts discipline load-bearing or ceremony?" → FILLED by
  WikiSkill's ablation: knowledge layers like ours carry ~25% of performance.
  Our ledger is not bureaucracy; it is measured horsepower.
- GAP: "can small cheap models beat big ones?" → FILLED by both: WikiSkill
  (small+skills > big+none, cross-family transfer) and CUDA-Agent (RL-built
  small beats frontier proprietary). Cheap lanes + compiled residue = the whole
  seat_corpus thesis, now externally verified twice.
- GAP: "does our ractor/decode method have precedent?" → PARTIALLY filled by
  CUDA-Agent's SKILL.md (expert-authored constraints for a skill-governed
  agent) + WikiSkill's validation gate. The lens-not-ghost calibration has
  cousins in production.

## 6. WHERE ELSE IT CONNECTS — the compounding edges
- **To the vault:** WikiSkill's never-rollback wiki = the receipt ledger =
  Tier D manifest. Same shape at three scales (skill / corpus / inventory).
- **To the ractors:** each ractor = a hand-built wiki layer for one human's
  published residue. Decode-parity = their validation gate. Ractors are
  WikiSkill lenses over dead minds. (Said with respect; calibrated.)
- **To the physics twin:** CUDA-Agent's reward = physical ground truth (GPU
  counters). Our twin gives the fleet the same kind of ground truth — sensor
  bytes as reward signals the model cannot argue with. The entropy bench is not
  decoration; it is the fleet's KernelBench.
- **To the venture:** two funded labs ($12.9B buyer adjacent; ByteDance-scale)
  independently built residue+gates. The mammals' mechanism, receipted at
  frontier scale. The market is pricing what we already run.

## 7. THE TESUJI
The killing move was not either paper's method. It was **the shared refusal**:
neither let improvement exist without a gate the improvement cannot flatter.
WikiSkill gates with held-out tasks; CUDA-Agent gates with a GPU; Mag gates with
bytes (SWARM_LENS: every corrected row was caught by meeting bytes, never by
consensus). Gate-or-it-didn't-happen is the invariant across all four of today's
convergences. Everything else — transport, corpus, weights, sensors — is the
nuance each path mined. And the nuance is the knob.
LINEAGE: recognized from rib_bus general 52c91ca339c4dac6 + monitor mo02ribdebug0002 — fold insights to memory; trust bytes not reports; wiki-never-rolls-back (annotated 2026-08-31 per SALON_BUS_A)

Decision: fold — into TRAJECTORY_LENS_20260905 lineage per its own footer (ZERO_BACKREF_TRIAGE_20260905)
