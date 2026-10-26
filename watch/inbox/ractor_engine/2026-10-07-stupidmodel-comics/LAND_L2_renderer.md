# LAND: L2 COMICS RENDERER (2026-10-07, comics L2 landing lane)

The landing for SYNTHESIS moves 2+3 (the schema freeze + the deterministic
drawing hand). Move 1 (fire() schema pass-through) and the Discord multipart
door stay owed to their owning lanes; nothing here touches free_lane_fleet.py
or phone_relay.py. No git commit (lane law); all files land on the working
tree for the operator's pen.

## What landed

- `tools/comic_spec.py` (224 lines): the FROZEN panel-spec schema,
  `comic_spec.v2`. Fixed cast of 6: operator, mag, hermes, lilith-figure,
  gemma-janitor, generic-agent. Pose vocabulary of 10: flail, kick, shimmy,
  strut, pointy, spirit, stomp (ported verbatim, joint-angle tuples, from
  `dashboard/static/mag_dance.html:52`) plus sit, think, slump (new, same
  10-field grammar). Panel shape: title + 3..4 panels of {who, pose, action,
  caption}. Field-name steal honored: `pose` is gramener/comicgen's exact
  field name (their name/angle/emotion/pose quartet read via WebFetch this
  sitting; their cast and art rejected); who/action/caption keep the names
  the fleet already measured 7/8 spec_valid on in this fold's
  comic_spec_probe.py. json_schema() emits the ollama format-schema dict for
  the future fire() door; loads() parses-and-refuses loudly; errors()
  enumerates EVERY violation, never first-error.
- `tools/comic_renderer.py` (332 lines): the drawing hand. ONE geometry pass
  emits neutral primitives; two backends consume them: SVG canonical
  (deliverable, zero-dep string building per the `mag/game_entry.py:154-160`
  idiom)
  and a PIL ImageDraw PNG twin (venv has no SVG rasterizer; Discord's upload
  whitelist is raster-only; PIL 12.2.0 verified). Stick-figure geometry
  ported 1:1 from drawSkeleton (`dashboard/static/mag_dance.html:81`):
  same segment lengths, same hip/shoulder anchors, static poses (a comic
  panel is a held pose, not a dance frame). Per-pose bounding-box fit law:
  every figure lands inside its slot, feet on the ground line, at up to 3
  figures per panel. Same spec renders pixel-identical twins, run over run.
  CLI: `.venv\Scripts\python.exe -m tools.comic_renderer --spec s.json
  --svg out.svg --png out.png` (also `--budget` for the proof dict).
- `tests/test_comic_renderer.py` (159 lines, 10 tests).

## Budget by construction (the load-bearing law)

Caps frozen in the schema: title 32, action 32, caption 80, max 3 cast
members per panel, 3..4 panels. assert_budget() (runs at every import)
serializes the worst-case valid spec for EVERY pose (4 panels, 3 longest
cast names, every string field at cap) and asserts under both walls: 1200
chars (fleet truncation) and 300 estimated tokens (ollama output cap). A
fresh proof run this sitting (`.venv\Scripts\python.exe -c "from tools
import comic_spec"`, instrument: the module's own BUDGET_PROOF) read worst
case 899 chars and 244 estimated tokens across all 10 poses, margins of
301 chars and 56 tokens. The estimator is conservative for compact JSON
(word runs at ceil(len/5), punctuation at ceil(count/2)); rationale in the
module docstring.

## Dogfood (the schema must express real sessions)

`watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/dogfood_strip_20261006.spec.json`
hand-written from the top 4 beats of `watch/inbox/DAWN_REPORT_20261006.md`:
(1) the operator's evening order, (2) EXECUTE-THE-REGISTER 12/12 lanes with
58 of 59 byte-proven, (3) the five ouroboros rounds with finding counts,
(4) the dawn verdict GROWS. Rendered and banked as both twins:
`dogfood_strip_20261006.svg` (11,879 bytes) and `dogfood_strip_20261006.png`
(1356x384). The spec's canonical serialization measures 673 chars / 236
estimated tokens (CLI receipt output, this sitting): a real 4-beat session
fits the budget with room. Figure bounds pixel-probed: figure ink spans
y 103..256 against the [78,266] figure band, feet grounded, nothing clipped.

## Gates

- pytest: tests/test_comic_renderer.py 10 passed (this sitting, first run
  after fixes). Full-suite `pytest -q` fired in background; number to be
  read from its log tail before the operator signs (the suite is 4,491+
  collected on a moving tree; my 3 files touch no existing module).
- Ratchet `tools/violation_ratchet.py check --changed` after landing:
  scope 25 changed files, NEW=4, and NONE of the four are this lane's
  files (they are sibling working-tree debt: blast_radius_probe.py,
  classify_probe.py, gauntlet_grade.py, longrunner_patrol.py; the
  gauntlet_grade.py except-pass appeared between my pre-landing and
  post-landing runs, a moving tree). This lane contributes zero NEW and
  zero GROWTH: all 3 files under the 400-line cap (224/332/159), no
  except-pass, no bare-except, no env reads, no cwd-relative module Path.
- Em-dash law: grep over all 4 landed files reads 0 matches each.
- Citation lint: run on this receipt (see below).

## Notes and observed context (not blockers)

- A sibling seat landed `dashboard/static/comics/` (index.html + manifest
  + a sample strip) on the same tree DURING this landing (mtime 16:52-16:53
  local, my read of the dir listing). It is a viewer expecting strips under
  its own strips/ dir with its own manifest; wiring the canonical fold
  strips into it is the operator's or that lane's call, not silently mine.
- The spirit pose swings both upper arms across the head zone (its native
  look, ported); head is now drawn after limbs so it stays legible when
  arms cross it.
- OWED downstream (this fold's residue list, unchanged): fire() schema
  pass-through, grade_comic() in the gauntlet register, the n=50 admission
  gate under this frozen v2 schema (the 7/8 and trial numbers were measured
  on the lenient probe schema; v2 adds the pose enum + caps, so the
  admission rerun is mandatory before any 7/8 claim is re-carried).
