# X10 - AIRFLOW RELINK (2026-09-29)

## Change
`dashboard/static/games/index.html` - added the missing door:

```html
<a href="../airflow_home.html">Airflow Home - the house is the prompt</a>
```

plus a dated comment naming the archaeology receipt. The HVAC game gets its
index entry back after running unlinked since its conservation law was
absorbed into `games/maze_arena.html` (self-steal receipt
`watch/inbox/FLUID_LENS_MANIFEST_20260913.md`).

## Archaeology credit
`watch/inbox/water_engineering_20260930/WA_HVAC_ARCHAEOLOGY.md` (WA lane 1/6)
found the orphan: alive, self-contained, 0 inbound hrefs from the games index.

## Verification (bytes, not reports)
- File exists: `dashboard/static/airflow_home.html` (18,986 B, mtime 2026-09-07).
- href resolves: from `/static/games/index.html`, `../airflow_home.html`
  browser-normalizes to `/static/airflow_home.html` -> HTTP 200 on both live
  servers (127.0.0.1:8765 and :8000, `dashboard/static` is the StaticFiles
  mount root per `backend/server.py:256,287`). `<title>AIRFLOW HOME — the
  house is the prompt</title>` confirmed in the served body.
- Upward relative links are an established estate pattern
  (`verkle_construction.html` -> `../../viz_3d_verkle.html`).
- Self-contained CONFIRMED: 357 lines, single inline `<script>` (no `src=`),
  zero `<link>/<img>/<audio>/<source>` tags, zero `fetch(`, zero local
  `.js/.css/.json/.png` references. No sibling assets needed. Matches the WA
  receipt's claim.
- Note: `nav.js` lines 20/92 already pointed at `/static/airflow_home.html`
  (site nav); the games-index door was the gap this closes. No commit made.
