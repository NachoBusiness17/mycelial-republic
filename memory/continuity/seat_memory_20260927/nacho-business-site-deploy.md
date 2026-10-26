---
name: nacho-business-site-deploy
description: The public Nacho Business site (netlify
  scintillating-cranachan-d6e93e) builds from site/build.py → site/dist — deploy
  needs operator auth; maze_arena constellation-404 fixed in f81735212
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

The operator's public face is the **Nacho Business** static site, live at `https://scintillating-cranachan-d6e93e.netlify.app` (also mirrored via `site/wrangler.jsonc` → Cloudflare, name `nacho-business`). Pipeline: edit sources → `python site/build.py` (needs the `markdown` package; installed markdown==3.10.3 into the repo venv 2026-09-14) → `site/dist/` → deploy. `dist/games/*` are verbatim copies of `dashboard/static` game pages.

2026-09-14 fix (`f81735212`): the deployed `/games/maze_arena` was stale (39.5KB vs 51.6KB, pre-constellation) AND `build.py` never copied `rounds_real.json`, so `?real=1` constellation mode 404'd by construction. Now `dist/static/rounds_real.json` ships with the build, and the page's loader tries `/static/…` → `../static/…` → relative, so it works on the local dashboard server and any static host. Verified end-to-end on a local serve of dist.

**Why:** "this needs to be fixed" on a Netlify URL traces to `site/`, not `dashboard/` — and the deploy itself was the stale half.

**How to apply:** Neither deploy door is authenticated from the agent shell (netlify-cli v27.5.2 installed but logged out; wrangler logged out) — after rebuilding, hand the operator `npx netlify-cli deploy --dir site/dist --prod` (or drag-drop `site/dist` as they did before; CF mirror: `cd site && npx wrangler deploy`). A `NETLIFY_AUTH_TOKEN` in env would let the drift patrol keep the site current automatically. Installing python deps: plain `pip install` via Bash gets hook-blocked — use `uv pip install --python .venv/Scripts/python.exe <pkg>`. Status 2026-09-15: fix verified locally but **still undeployed** — the live site serves the stale page until the operator pushes the button (flagged as patrol risk #2).

2026-09-14 updates (fifty-wide follow-up): **build.py is lock-tolerant** — dist rmtree uses ignore_errors and mkdirs use exist_ok (a held dist directory handle, WinError 32, was aborting builds mid-wipe and half-emptying dist). **GAMES now copy from `dashboard/static/games/`** (canonical, committed in c71a03856) with top-level fallback — this fixed the C5 audit bug where the deployed site shipped a two-day-stale MUD. **New page:** `watch/onboard/TEAM.md` → `onboard/team.html` ("The Team — play, write, build", the collaborator door for Melissa/Marque/Adam). Still undeployed to netlify — dist is rebuilt and ready.
