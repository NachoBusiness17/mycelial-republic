# W3H — ADAM first-external-dev pack (2026-09-29/30)

MISSION: the B4 first-external-dev pack at `docs/ADAM_QUICKSTART.md` in
the-mountain, written for ADAM: plain language, zero estate jargon, assumes
Godot installed + repo access. Committed.

## LANDED

- `docs/ADAM_QUICKSTART.md` in the-mountain, commit `2fcda8f` on main, 97
  lines (mission cap: 120). Not pushed (mission said commit; push is the
  fence-owner's move).
- Six sections per mission: (1) clone + one bootstrap line — the hooksPath
  line from README/CONTRIBUTING, verified both name it; (2) F5 first-frame
  expectations rebuilt from `game.gd` `_draw()` + HUD code: six pools with
  real starting volumes (spring 6, hollow 2), CROWN 0/4 ring, pipe colors,
  siphon dot, 12 fish at spring, controls, win overlay; (3) dual-mode kept
  honest: standalone complete today, networked client + server NOT in this
  repo yet, next sync; when it lands it is `python -m server.server` from
  the companion repo — invocation verified real (`server/server.py` has a
  `__main__` entry, line 389); (4) poke map: `POOL_LAYOUT` dict + `_build_water()`
  + `WIN_CROWN`, water laws as one paragraph (integer determinism, XOR
  gate1, 2-unit siphon prime, steam-to-highest-cold); (5) issue template
  (ordered steps, expected-vs-saw, Godot version + OS, verbatim Output
  panel — determinism makes steps replay exactly); (6) receipts not vibes,
  with before/after-run framing.
- Jargon scrub: no "estate", "sovereign", "B0", seat names, or verkle
  vocabulary in the pack.

## JOURNEY

- Read the-mountain README → CONTRIBUTING → game/README → game.gd →
  project.godot (window 1152x648, features 4.3) before writing: the F5
  section had to be byte-honest about what renders, not vibes from the
  README's prose.
- Checked `server/` in the estate repo: `python -m server.server` is a real
  invocation, so the mission's dual-mode note could keep the command AND
  stay honest that the server is not published in the-mountain yet
  (game/README verification-status section says the same).
- Peeked REGISTER_NOTE.md to shape this receipt (path-report law: JOURNEY
  section embedded). No dead ends this run; one turn worth naming — wrote
  the pack to the ADAM audience (external, no estate access) rather than
  copying repo-internal framing, which is why section 3 leads with
  "nothing in this repo secretly needs the server".
