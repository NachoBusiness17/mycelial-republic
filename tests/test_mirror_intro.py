"""Mirror first-run tour assets are present in the dashboard shell."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 2026-09-27 markup-contract repoint (burn lane mirror_intro; byte-proven):
# commit d575bc168 (2026-09-14 checkpoint) moved the mag-board dashboard shell
# (dock UI + full mirror guide markup) to dashboard/static/museum/index_old_mag_board.html
# and replaced index.html with the self-contained FLEET CONSOLE page, which loads
# neither app.js nor cli.css. The tour assets stayed live at HEAD: app.js still ships
# MIRROR_GUIDE_STEPS / wireMirrorGuide / maybeStartMirrorGuide bound to these ids and
# cli.css still ships the mirror-intro-v1 block. The shell that hosts the markup and
# loads both assets via /static/ URLs is the museum mag-board page, so the markup
# contract pins there now (the old index.html pointer was the stale pin; audit
# 2026-09-26 lane7 already named this failure "stale_baseline_pin").
SHELL = ROOT / "dashboard" / "static" / "museum" / "index_old_mag_board.html"
APP_JS = ROOT / "dashboard" / "static" / "app.js"
CSS = ROOT / "dashboard" / "static" / "cli.css"


def test_mirror_guide_markup_in_index():
    html = SHELL.read_text(encoding="utf-8")
    assert 'id="mirrorGuide"' in html
    assert 'id="mirrorGuideTitle"' in html
    assert 'id="btnMirrorReplay"' in html
    assert "mirror-intro-v1" in CSS.read_text(encoding="utf-8")
    # the hosting shell must still wire the assets, or the ids are inert markup
    assert "/static/app.js" in html
    assert "/static/cli.css" in html


def test_mirror_guide_logic_in_app_js():
    js = APP_JS.read_text(encoding="utf-8")
    assert "MIRROR_INTRO_KEY" in js
    assert "MIRROR_GUIDE_STEPS" in js
    assert "maybeStartMirrorGuide" in js
    assert "Hi — I'm your Mirror" in js
