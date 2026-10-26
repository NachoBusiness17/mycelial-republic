---
name: blob-doubling-kubernetes-mechanic
description: "Blob doubling" game mechanic (2026-09-18) — pushing a block duplicates it (Kubernetes pod-scale metaphor); briefs seeded DD-blob-double + DD-split-path; dual-window breeding produces distinct variants of same brief (union vs glm = different parents)
metadata:
  type: project
---

Operator connected "duplication is emphasis" to a playable mechanic: a block that DOUBLES when pushed, mapped to Kubernetes pod replication ("sort of mapped to dumb kubernetes"). Two briefs seeded (DD-blob-double, DD-split-path) — pushing the blob duplicates it into adjacent cells, player manages which copy survives, collapse ledges are the garbage collector.

**Why:** the fleet's own systems demonstrated the pattern accidentally — the dual-window rotation (union + glm alternating as primaries) bred the SAME briefs into DISTINCT levels because the models have different training data. The collision produced variants, not duplicates. That's the GA running wider than designed.

**How to apply:** (1) briefs.json carries the blob-doubling briefs; (2) the dual-window breeding pattern is deliberate now — fire the same brief on both windows, keep the better variant; (3) Kubernetes mapping = blob IS a pod, push IS a scale command, collapse IS the node drain, plate IS the service that comes up when replicas are healthy.

Falsifier: if blob-doubling levels prove trivially solvable (the duplicate is always safely disposable), the mechanic is decoration — the doubling must create a real spatial constraint.
