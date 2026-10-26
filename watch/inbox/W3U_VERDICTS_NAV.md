# W3U VERDICTS NAV (2026-09-29)

Mickey17 Wave 3 follow-up lane. Closes the nav gap left by W3_VERDICTS_PANEL_20260929:
the panel page existed (`dashboard/static/verdicts.html`) but the fleetnav bar had no
door to it.

## Files

- `dashboard/static/nav.js` (one entry, line 44): `["/static/verdicts.html", "Verdicts"],`
  inserted directly after the FW-45 `Links` entry (same lineage: verdicts.html is a
  clone of links.html). Shape matches the existing LINKS array rows exactly; nothing
  else in `dashboard/` touched. `node --check` clean; file now 5,943 bytes.

## Door verification (route function called directly, no server spin-up)

`python -c` importing `_verdicts_payload` from `dashboard.server` (import is
side-effect safe: `serve_forever` sits under the `__main__` guard at server.py:1230),
called with the real default paths, live dashboard NOT restarted:

- schema `verdicts.v1`, `json.dumps` round-trip clean.
- gps: `tools/gps_mcp/gps_ledger.db3` present on disk (16,384 bytes, mtime
  2026-09-29 21:24 local) and READ-ONLY query returned **1 row**:
  `z-ai/glm-5.3-prime | night-judgment | pass 0.8333 | n 6 | 2026-09-30T01:24:56+00:00`
  (the ledger was unseeded at panel-landing time; it has since been seeded once).
- gwap tail (`memory/runs/gwap`): **3 files** (mud-demo-20260929.jsonl,
  b3-demo-collusion-20260929.jsonl, b3-demo-clean-20260929.jsonl).
- mountain tail (`watch/inbox/mountain_climb_ractor_20260929`): **10 files**
  (RECEIPT.md, FINAL_PIECE.md, SYNTHESIS.md, LENS_SURFACE.md, LENS_SUBSTRATE.md,
  LENS_PLAYGROUND.md, LENS_BODY.md, GRADED.md, FRAME.md, DIGEST.md).

## Restart owed (NOT performed, lane law)

The operator's live dashboard process predates the W3 panel landing and must be
restarted (`mag.cmd dashboard`) before `/api/v1/verdicts` serves over HTTP; until
then the door verifies only via direct function call as above. nav.js is picked up
by pages on browser reload once the process serves the panel page. No git commit
(lane law). Em-dash count in the touched-file addition: 0.
