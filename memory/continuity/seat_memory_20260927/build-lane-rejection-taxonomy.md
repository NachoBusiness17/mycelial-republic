---
name: build-lane-rejection-taxonomy
description: "Build lane rejection taxonomy mined from 41 rows: only 2 merit (BFS unsolvable), 39 infrastructure (200-error-body, 404 window-end, empty_content, schema). The gate isn't strict — the pipe is unreliable. Transport-deaths ≠ model-quality signal."
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Mined 2026-09-17 from 41 rejection rows in the build lane's proposals.jsonl.

**The finding:** only 2 of 41 rejections were merit (BFS said the level was unsolvable).
The other 39 were infrastructure: 200-error-body (16, stealth windows flap), 404
window-end (11, stealth model's free window ended), empty_content (12, reasoning channel
consumed budget pre-cap-removal), schema (2, brief format), IncompleteRead (1, network).

**Why it matters:** the model quality signal was hidden inside transport noise. When a
model actually produced a level, it passed the gate ~52% of the time first-pass. After
seeing its own failures (gen-2+), pass rate approached 100%. The 18 "rejections" misled
us into thinking the models were bad designers when most failures were the pipe.

**Laws this confirmed:** Amendment 001 (transport-deaths-never-count-as-attempts);
prune-then-reset pattern for attempts; rotation law (union → glm → pareto).

**Astra connection:** the 39 infrastructure rejections + 2 merit rejections ARE the
negative examples for the astra training corpus. The model must learn the difference
between "the pipe broke" and "the design is wrong." Filed:
watch/inbox/REJECTION_TAXONOMY_20260917.md

Related: [[amendment-001-model-law]], [[astra-v4-converged-training-brief]],
[[ruins-go-shipped-20260917]].
