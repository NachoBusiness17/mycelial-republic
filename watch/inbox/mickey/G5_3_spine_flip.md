# G5-3 — HUM SPINE FLIP (2026-09-11)

Spawned from G4-3's completion of kv_os.html. Target: dashboard/static/hum.html.

## What flipped

1. **SPINE row — KV OS chip amber → green.**
   - Before: `["KV OS","a","charter 09-11, page pending (kv_os.html)"]`
   - After: `["KV OS — <a href='kv_os.html'>open kv_os.html</a>","g","charter 09-11 — page LIVE (G4-3 build landed)"]`
   - Note: the organ renderer prints the name field via innerHTML (the third
     description element is data-only, never displayed), so the link had to go in
     the name field to be visible. Chip now reads "KV OS — open kv_os.html" and
     is clickable.

2. **EYES row — operator-action note added.**
   - The EYES organ chips were already amber (spec'd), but the live probe's dark
     fallback (G4-4 wiring, `liveLine("eyes", ...)` in the fetch catch) still
     renders honest-dark when the eye at 127.0.0.1:11434 doesn't answer.
   - Appended one line to that dark message: "ollama restart required — operator action."

## Verification

- `python -c "from html.parser import HTMLParser; HTMLParser().feed(open('dashboard/static/hum.html').read())"` — PARSE OK.
- Confirmed dashboard/static/kv_os.html exists on disk (link target is real).

## Not touched

- Everything else on the board stays as-is: EARS honest-dark probe, HANDS
  cage-side-by-law note, CONDUCTOR clerk red chip, wiring list. Statuses above
  the fold remain card-truth with the stale-feed caveat until overseer.json ages
  back under the stale threshold.
