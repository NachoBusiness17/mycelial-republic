# R4b-LB LAND: knowledge-graph residual + GENOME rival order + hygiene bundle

Lane: R4b-LB (moves 3 + 4 + 8 of the ouroboros R4 memory fold).
Parent fold: watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md
(rows S5, S8, S9, S10, S11; amendment table rows 3, 4, 8).
Moment: 2026-10-06 ~09:20-09:4x Z. Interpreter: .venv/Scripts/python.exe only.
No commit made (the git add -f staging below is the allowed extent).

## Move 3 (S5): knowledge_graph we_have filter + fold() outcome stamp

Edits (mag/knowledge_graph.py):

1. _edges() landscape branch: a we_have entry now mints an already_inside edge
   only when its leading token is a *.py path AND the target module:{name} node
   exists in the graph. Prose entries ("stateless-ghost-swarm / cheap_swarm
   (stateless doctrine)") stay on the node as recognition text; they no longer
   mint edges aimed at module ids nothing materializes.
2. fold() grows an outcome stamp: signature fold(label, kind, note,
   source="session", outcome="pending") with _OUTCOMES = held / falsified /
   pending. Invalid outcomes raise BEFORE any write. New nodes carry the stamp;
   legacy nodes read as pending by absence. CLI: fold ... --outcome {choice}.
   All existing positional callers (mag/attractor_tools.py,
   mag/doctor_rightsize.py, mag/frontier_intake.py, mag/frontier_batch.py,
   mag/ghost_doctor.py, dream()) unchanged and compatible.

Census (instrument: fresh kg.build() then count orphans = nodes in no edge
from/to; dangling = edge endpoint not in node ids; banked inline):

- BEFORE (moment 2026-10-06T09:20:14Z, pre-edit code): 2,924 nodes, 1,146
  edges, 1,203 orphans (module 446 / knot 400 / steal 140 / doctrine 217),
  29 dangling. The fold's prior census (SYNTHESIS S5: 2,921 / 1,144 / 1,204 /
  29) differs by tree movement between 02:4xZ and this run; instrument and
  moment named per the census denominator law.
- AFTER (moment 2026-10-06T09:21:53Z, post-edit code): 2,924 nodes, 1,133
  edges, 1,203 orphans (module 444 / knot 400 / landscape 2 / steal 140 /
  doctrine 217), 0 dangling.

Reading: dangling 29 -> 0 (cured). Edges -13: 13 prose mints dropped; the
other 16 previously-dangling py-shaped mints re-targeted onto real module
nodes, binding 2 formerly-orphan modules (module 446 -> 444) while 2
prose-only families became honest orphans (landscape 0 -> 2). Net orphans
unchanged; garbage connectivity became real connectivity plus honest
emptiness. Smoke: fold stamp verified via CLI and ValueError probe; smoke
node removed after capture.

## Move 4 (S8): GENOME rival boot order folded, register repointed, tracked

state/GENOME.md section 3 kept verbatim (verkle style, no silent rewrite) with
a dated AMENDMENT 2026-10-06 appended directly beneath it: section 3 is
SUPERSEDED; a cold seat boots the AGENTS.md 24/7 load order (zknot LATEST
recap -> REDBOARD -> FRAMEWORK_LOAD + compass -> machine-mounted ribs via
python -m mag.rib_boot -> state/CURRENT.md -> act). The delta register pointer
is repointed in the amendment: watch/inbox/frontier_delta_register_20261003.json
is FROZEN LINEAGE (ls: it is still the only register file), read as the day-one
selection record, never routed by; live deltas live in state/CURRENT.md and the
receipts the AGENTS.md load order names. The amendment also marks GENOME itself
as lineage, not live truth. git add -f state/GENOME.md state/CURRENT.md: both
now staged (git status shows A for each), uncommitted, so a gate can see them
drift. state/CURRENT.md bytes untouched by this lane.

## Move 8 (S9 + S10 + S11): hygiene bundle

1. mag/rib_boot.py _run(): the venv spawn now carries creationflags
   getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) on win32 (0 elsewhere),
   the same HEADLESS pattern as mag/boot_regen.py and mag/cost_enforcer.py.
2. tools/ouroboros.py docstring: phantom memory/ribs/ -> memory/rib/ (ls
   proved memory/ribs absent; RIB_DIR was already correct at line 53). Kept
   line-count neutral (400) to hold the ratchet file-too-long bar.
3. tools/freshness_check.py: heartbeat-scaled staleness bar. New
   effective_stale_days(head_age) = min(STALE_DAYS, max(STALE_FLOOR_DAYS,
   head_age * STALE_SCALE)) with STALE_SCALE 4.0, STALE_FLOOR_DAYS 1.0; the
   cap stays the one decay constant (mag.constants.PACK_STALE_DAYS = 7).
   main() prints the scaled bar and judges tracked and untracked docs by it.

## Gates (final, post-dash-fix)

- pytest tests/test_knowledge_graph_r4b_20261006.py +
  tests/test_freshness_heartbeat_bar.py + tests/test_graph_heal.py +
  tests/test_rib_boot_amendments.py + tests/test_freshness_gate.py +
  tests/test_catalog_freshness.py: 65 passed, 0 failed.
- New tests landed: the two R4b files above (we_have shape+existence filter,
  fold outcome stamp incl. reject-before-write and amend-not-erase, and the
  four heartbeat bar pins).
- Pre-existing time-bomb cured in tests/test_freshness_gate.py: the real-clock
  CLI tests carried hard-coded 2026-09-xx stamps and went red on 2026-10-04
  ("16d old; bar is 14d"); stamps are now derived from date.today() while the
  in-process TODAY pins stay frozen. Not caused by this lane's edits; verified
  by the failure text predating any surface this lane touched.
- Ratchet: NEW = 1 and it is NOT this lane's: tools/thought_quantizer.py 472
  lines (HEAD 379, +107/-14 by a concurrent sibling seat's working-tree edit;
  this lane never opened it). This lane's own footprint is zero NEW
  (tools/ouroboros.py was pushed to 401 by the first docstring edit and cut
  back to 400).
- tools/freshness_check.py live: exit 1, FAIL naming state/CURRENT.md (2.0d)
  and state/START_BRIEF.md (1.9d) against a 1.2d bar at heartbeat 0.3d - the
  demanded stale-case FAIL; --self-test PASS.
- Citation lint on state/GENOME.md: ok, blocking 0. Em/en-dash scan of every
  added line across all edited files: clean.

## Owed / blockers

- Operator or next seat: refresh state/CURRENT.md and state/START_BRIEF.md
  (both now read STALE under the honest bar) or register START_BRIEF frozen.
- The sibling thought_quantizer.py >400 NEW ratchet debt stands in the shared
  working tree; accepting it by name is the owning seat's call, not this
  lane's.
- One transient: the first post-edit pytest batch showed
  test_ouroboros_driver_mounts_the_vault_with_amendments failing once; three
  consecutive reruns (batch twice, isolated once) pass. Not reproduced; left
  as a flake note, not a cure claim.
