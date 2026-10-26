# FW-42 — Netlify pre-flight: build + dist check PASS; one-command deploy card

**2026-09-28 · Q-027 (burn-reset gopher) · task: fifty-wide 09-17 board §H**
Site: **Nacho Business** — public at `https://scintillating-cranachan-d6e93e.netlify.app`,
Cloudflare mirror named `nacho-business` (`site/wrangler.jsonc`). Builder: `site/build.py`
(md pages + verbatim game copies + assets → `site/dist/`). All checks below ran this session.

## Pre-flight results (all PASS)

| check | command | result |
|---|---|---|
| build | `./.venv/Scripts/python.exe site/build.py` | exit 0, zero `MISSING:` lines (re-ran, grep clean) |
| dist pages | recount | 15 md-pages + maze.html + 8 onboard pages present (16/16 of the page list) |
| dist games | recount | **22/22** games in `dist/games/`, none missing |
| dist total | — | 42 files (incl. `static/rounds_real.json` — the maze_arena `?real=1` 404 fix — and 4 suno mp3s) |
| fresh game copy | sha256 | `dist/games/mud.html` byte-identical to `dashboard/static/games/mud.html` (125,486 bytes — carries the FW-37 ws client) |
| idempotency | rebuild + hash | `index.html` hash stable across two consecutive builds |
| deploy tooling | `npx netlify-cli --version` | netlify-cli 27.7.0 present; **NOT logged in** (`~/.netlify` absent) |
| CF mirror tooling | `npx wrangler` | present; **NOT logged in** (`~/.wrangler` absent) |
| live site | `curl -sI https://scintillating-cranachan-d6e93e.netlify.app/` | 200 OK — but `/games/mud.html` serves **31,674 bytes vs 125,486 local**: the public MUD predates the entire monastery restructure (rooms/champions/sigils, W4 ghosts, W5 ascension, ws relay). Everything since the 09-14 touch is undeployed. |

## The one-command deploy (operator hands only — neither door is authenticated from the shell)

```text
npx netlify-cli deploy --dir site/dist --prod
```

That's the whole push. One-time prerequisites, in order:

1. `npx netlify-cli login` (browser) — or export `NETLIFY_AUTH_TOKEN` in env, which also
   unlocks letting the drift patrol keep the site current automatically (flagged patrol risk #2
   in `memory/continuity/seat_memory_20260927/nacho-business-site-deploy.md`).
2. If it asks for a site on first deploy, pick the existing `scintillating-cranachan-d6e93e`
   (the live one) — do NOT create a second site.

Cloudflare mirror (optional, same dist): `cd site && npx wrangler deploy` (own login).

## Pre-deploy checklist (operator, ~5 minutes)

- [ ] `./.venv/Scripts/python.exe site/build.py` (rebuild fresh — build.py is dist's only writer;
      it is lock-tolerant by design, a held dist handle no longer half-empties it).
- [ ] FW-41 quick rulings that gate the public face (see `FW41_adam_questions.md`):
      **Q3** the Adam letter shipping alongside the Nacho persona (letter.html builds verbatim
      every time), **Q4** the "10/10 games" stat vs the 22 games actually shipped, **Q14** the
      letter's final text. Silence = defaults apply (leave both personas; recount the stat).
- [ ] Skim `dist/index.html` in a browser from a local serve (any static server of `site/dist`).

## Post-deploy verify (30 seconds)

```bash
curl -s https://scintillating-cranachan-d6e93e.netlify.app/games/mud.html | wc -c   # expect 125486, was 31674
curl -s -o /dev/null -w '%{http_code}' https://scintillating-cranachan-d6e93e.netlify.app/static/rounds_real.json   # expect 200
```

Then play one room of the deployed monastery — the live site jumps four game-generations in one
click (rooms/champions → torch vision → ascension → ws relay).
