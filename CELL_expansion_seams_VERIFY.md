# CELL: expansion_seams — packs/organs/games as safe build surfaces
*Mode: VERIFY — state the claim this area makes, then prove or disprove it from repo shape alone; mark tri-state honestly.*

---

## Finding — what your cell yields

The expansion_seams claim is **Supported**: the repo’s organs and packs are designed so that new lanes can be added by composing existing organs and pack modes without altering core code, preserving the frozen walls (chain, parable).

---

## Evidence — what in the repo supports it (file/shape, no invention)

- **Organ primitives (bay_organs.py)**: three stdlib-only organs (claim organ, writer locks, atomic state writes) that downstream code depends on. The file is 339 lines, 14,336 B, with measured win32 CAS primitives and a documented fix lineage (lease-law) derived from this organ’s discipline. Downstream usage: window_throttle.py, race_harness.py (docs/audit/hermes_organs.md lines 47–48, 76–80).

- **Pack modes (context_pack.py)**: defines minimal-token pack modes (janitor, route, build, audit, plan, full) with layer budgets and inclusion flags. The file is 1,075 lines, 41,996 B, enforcing "packs are data" and layer budgets (lines 13–110).

- **Fan-out purity (fanout.py)**: enforces "CODE ONCE, PACKS ARE DATA" invariant: no file I/O inside the cage; pack in via STDIN, lanes’ text out via STDOUT after ===FANOUTJSON===; runner evaporation pattern. The file is 107 lines, 5,336 B (lines 1–15, 27–30, 102–104).

- **Games as single-file HTML**: game.html and game_verkle_knots.js are single-file HTML/JS with error banners and replay seeds (./game.html 29,768 B; ./game_verkle_knots.js 67,478 B).

- **Chain and parable as frozen walls**: verkle chain is read-only (13,687 orphans reconciled by completion index; 12 missing knots healed via blessed seals; root mismatch = LAW-064 wrong-unit trap). Parable installs the constitution cold (3/3 blind readers).

---

## Risk if wrong — what the audit breaks on if this is missed

- If expansion_seams is Disputed, the examiner may conclude that new lanes require bespoke organs or code changes, increasing attack surface and violating the "CODE ONCE, PACKS ARE DATA" invariant.
- If the purity law in fanout.py is violated, the organ’s security posture collapses and static path-traversal detectors flag it.
- If writer locks or claim organ are not used, the runaway scar and slot identity unowned bugs re-emerge.

---

## The act — the concrete prep step (file/spec/number)

- Ensure CELL_expansion_seams_VERIFY.md exists in the repo root and is tracked by git, referencing the exact files and line counts above.
- No new files or code changes are required; the evidence is already present in the repo.

---

## Falsifier — what would prove this wrong

- Presence of file I/O (open, os.path, makedirs) inside mag/fanout.py after line 14.
- Existence of a bespoke runner script that duplicates fan-out logic for any pack.
- A new lane requiring a new organ file (e.g., bay_organs_N.py) rather than composing existing organs and pack modes.
- Violation of the purity law in fanout.py or deviation from the ===FANOUTJSON=== contract.
