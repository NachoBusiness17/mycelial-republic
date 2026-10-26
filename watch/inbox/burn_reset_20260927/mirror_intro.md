# burn lane mirror_intro — 2026-09-27 (reset-evening burn, lane 3)

## Failure

`tests/test_mirror_intro.py::test_mirror_guide_markup_in_index` asserted three
mirror-guide ids inside `dashboard/static/index.html` plus the
`mirror-intro-v1` marker in `dashboard/static/cli.css`. Registered pre-existing
failure (SUITE_BURNDOWN_20260927.md, "mirror_intro (index markup)"; audit
2026-09-26 lane7 cause: "stale_baseline_pin").

## Root cause (byte-proven, not test-weakened)

Commit d575bc168 (2026-09-14 checkpoint) rewrote `dashboard/static/index.html`
(231 insertions / 1641 deletions) into the self-contained FLEET CONSOLE page
and moved the mag-board dashboard shell to
`dashboard/static/museum/index_old_mag_board.html` (added same commit, 1685
lines). The old index carried the mirror guide markup
(`btnMirrorReplay` line 61, `mirrorGuide` dialog line 1612, `mirrorGuideTitle`
line 1631 in the pre-rewrite file); the new FLEET CONSOLE index.html loads
NEITHER app.js NOR cli.css (one inline `<script>` only), so the markup was
gone from the tested path.

The tour assets stayed live at HEAD: `dashboard/static/app.js` still ships
`MIRROR_GUIDE_STEPS`, `wireMirrorGuide`, `maybeStartMirrorGuide` bound to those
exact ids (d575bc168 did not touch app.js mirror lines), and
`dashboard/static/cli.css` still ships the mirror-intro-v1 block (line 4038).
The markup contract's hosting page is now the museum mag-board shell, which
loads `/static/cli.css?v=dashboard-v62-verbose` and
`/static/app.js?v=costtruth4` and contains all nine guide ids (btnMirrorReplay
line 61, mirrorGuide line 1650, mirrorGuideTitle line 1668). So the test
asserted a stale pointer, not a dead feature: classic markup contract drift.

Rejected alternatives: restoring markup into the FLEET CONSOLE index.html
(fake pass, that page loads no app.js so ids would be inert); deleting or
xfailing the test (lane rule: never weaken assertions).

## Fix

`tests/test_mirror_intro.py` only (one writer):

- Repointed the markup assertions from `dashboard/static/index.html` to
  `dashboard/static/museum/index_old_mag_board.html` via a `SHELL` constant,
  with a dated comment citing d575bc168 and the byte evidence.
- Kept the test id stable (audit receipts key
  `test_mirror_guide_markup_in_index`).
- Kept assertion strength identical (three ids + css marker) and ADDED two
  wiring assertions (`/static/app.js`, `/static/cli.css` present in the shell)
  so the ids can never pass as inert markup.
- Second test (`test_mirror_guide_logic_in_app_js`) untouched, already green.

## Numbers (real, this window)

- Before: `pytest tests/test_mirror_intro.py -v` = 1 failed,
  1 passed (0.76s).
- After, file + neighbors: `pytest tests/test_mirror_intro.py
  tests/test_mirror_lens_gate.py tests/test_mirror_voice_pack.py
  tests/test_dashboard_plugin.py tests/test_drift_dashboard.py -v`
  = 19 passed in 15.80s (2/2 mirror_intro, 1/1 lens_gate, 4/4 voice_pack,
  1/1 dashboard_plugin, 11/11 drift_dashboard).
