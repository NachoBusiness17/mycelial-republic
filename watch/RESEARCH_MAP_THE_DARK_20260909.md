# RESEARCH — MAP THE DARK: VidMap + GPS-denied SLAM (2026-09-09 ~02:5xZ)

**Paste pair** (operator: "those are research or at least might have something
useful"): pesarlin's VidMap (ECCV 2026) + tokufxug's cave SLAM. One theme:
**mapping dark space by walking it.** Desk drafts staged on both (dual-use).

## 1 — VidMap (cvg/vidmap, Apache-2.0)

- **What:** offline Structure-from-Motion for monocular video → camera poses +
  sparse 3D map (COLMAP-format) + browser/Rerun viewers. Temporal point tracks,
  loop closures, metric depth, global optimization.
- **Lineage:** COLMAP / MP-SfM / hloc; transformer matching under the hood
  (~9 GB checkpoints). Maturity: fresh paper release (9 commits, 418 stars).
- **RUNNABLE NOW: NO.** Linux x86-64 + NVIDIA required — host has **no NVIDIA
  GPU** (checked tonight), and Rocinante is Apple Silicon (Oct 27). COLMAP
  built-from-source + optional Ceres/CUDA/cuDSS: moderate-high install.
- **Route:** (a) VAST-lane candidate — rent-by-the-hour GPU for one-shot
  reconstruction jobs (the vast-autopilot pattern; a job, not an install);
  (b) watch the license-named deps — Apache-2.0 core passes the license gate.

## 2 — Cave SLAM (Livox Mid360 + IMU + iPad SLAMLab)

- **What:** GPS-denied 3D mapping of a physical cave; loop-closed to tens-of-cm
  drift. Recipe: ~$600 LiDAR + Xsens IMU + consumer tablet app.
- **Doctrine bridge (the load-bearing finding):** the verkle chain IS SLAM for
  truth — dead-reckoning by hashing (each knot hashes what came before), no
  external GPS (no ground truth to trust), **loop closure = independent
  re-verification** (tonight's three-way fold of 7,377 rows was one). Drift =
  the ~12 healing knots. The cave team's trick — close the loop, forgive the
  drift, keep the terrain — is exactly the chain's repair pattern (repair
  twice, history intact). Card routes to the audit/tesuji lane as a vocabulary
  import: WALK = map; LOOP CLOSURE = independent fold; DRIFT = healing knots.

## 3 — The pipeline it joins (the real score)

**Recording farm → VidMap → hologram.** The farm already captures video of the
fleet playing (classics ladder webm receipts). VidMap turns any such video into
a walkable 3D space. That is the machinery of the recurring dream — *the world
renders only where visited* — as a buildable chain: play all → play well →
record → **walk it.** The hologram charter's zones are hand-built; this is the
generated-rooms door. Candidate name: F-BOAT (the dream on file, buildable).

## Rubric

| | score | note |
|---|---|---|
| Fleet-useful | HIGH (doctrine) / MED (tool) | chain-as-SLAM lands tonight; tool needs rented GPU |
| Runnable now | NO (local) | no NVIDIA; VAST lane possible |
| Cost | $ (doctrine) / $$ (VAST job) | ~9GB + hourly GPU if run |
| Falsifier | F-BOAT-1 | a recorded fleet session reconstructs into a walkable map a stranger recognizes |
| Timing | AFTER Sep-20 wall | parked with the senses wing; doctrine lands free tonight |
