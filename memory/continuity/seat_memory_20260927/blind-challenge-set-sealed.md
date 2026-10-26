---
name: blind-challenge-set-sealed
description: A1 blind challenge set SEALED — 10 challenges with hash-committed
  key outside contract surfaces; fleet's own numbers failed two byte-checks
  (salon_50 39/50 not 50/50, NEXT-STEAL 55/44 not 53); prediction window dark
  awaiting first predictor
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

Blind Challenge Set v0 BUILT and SEALED 2026-09-16 — the fleet's first pre-registration instrument where predictions are committed before outcomes and the answer key lives outside all contract surfaces.

**Design (four locks):** (BEFORE) signed predictor rows precede measurement rows in append-only receipts; (OUTSIDE) operational vocabulary only, graders are scripts or non-claimant seats under rubrics fixed at authoring; (BLIND) answer keys hash-committed, bytes parked outside every SHARED_SURFACE_CONTRACT surface, withheld from briefs/queue until window closes, author ≠ predictor ≠ grader; (SCORED) prediction → outcome → mandatory update — a miss must yield a canon correction, never silence.

**10 challenges from tonight's real claimants:** C-01 interpreter collision (AGENTS.md Hermes-python law), C-02 test-census reproduction (1305/34/9 bands), C-03 catalog 746,773-rows/zero-granted-surfaces, C-04 resume-command yield (key already sealed: sha256 49e67876…046bf at .mag_challenge_sealed/BCS_20260916_C04.key.txt), C-05 commit 5305a99b1 stat match, C-06 wow_session replay determinism, C-07 salon-ESS rho blind band call, C-08 fossil audit (NEXT-STEAL 55/44 vs canonical 53; salon_50 39/50 vs "50/50"), C-09 mirror-scorer blind control on 10 pre-2023 texts, C-10 Extropic 140× replication with pre-registered bands. Each has claim, frozen threshold, named grader, deadline.

**Withholding mechanism:** hash-commit (retrofit is cryptographically detectable) + non-contract storage path (.mag_challenge_sealed/) + honest threat model (disk-local storage is hygiene; the hash is the real lock; a leaked key matching a byte-perfect prediction becomes evidence of cheating — itself a fleet measurement).

**Fleet's own numbers already failed two byte-checks** (found while sourcing claimants): NEXT-STEAL count was 55 occurrences/44 of 50 answers (not canonical "53"), salon_50 was 39/50 (not "50/50"). The challenge set formalizes that seam so drift is caught by instrument, not by luck.

**Next action:** open the prediction window — pointer in queue/todo.md, then let first non-claimant seat append its C-01 predictor row.
