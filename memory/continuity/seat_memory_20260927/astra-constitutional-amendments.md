---
name: astra-constitutional-amendments
description: Three constitutional laws for the Astra training pipeline (2026-09-17→18) — A1 adapter-is-not-identity, A2 no-stage-personified, A3 second-model-never-judges; these close the three ways self-improving systems eat themselves
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Three constitutional laws filed 2026-09-17→18 (commit 9a0e9ce39, ASTRA_CONSTITUTIONAL_AMENDMENTS.md) — absolute, binding every future astra iteration. They close the exact failure modes that kill self-improving systems.

**A1. Adapter is not identity / not the persistent inference voice.** The QLoRA adapter proposes tickets; it does not become the fleet's voice. When a new adapter promotes, the old one retires with a tombstone. If it starts speaking as "I" persistently across regenerations, it has become a persona — kill it and re-train.

**A2. No stage may be personified.** The harness audit, curator, validator, SFT, RS-DPO, GRPO, eval, promotion — none gets a name, character, opinion, or voice. The moment a pipeline stage has preferences, it is a learned reward model by accident.

**A3. Second model never judges.** The gate is ordinary code: BFS, hash checks, schema validators, test runners. A second model scoring the first's tickets is a learned reward model with extra steps. If a judgment call is needed, fix the code.

Together they close: the adapter identifies as the fleet → the pipeline stages get named and opinionated → a second model judges the first → the gate moves inside the weights → the whole thing is a mirror running its own hallucinations back to itself. Related: [[astra-v4-converged-training-brief]].
