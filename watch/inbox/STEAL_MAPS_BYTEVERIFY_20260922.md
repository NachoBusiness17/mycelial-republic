# STEAL MAPS — BYTE VERIFY — 2026-09-22 (ask A10)

Two scoreboard repos shallow-cloned into `corpus/library/` and byte-verified.
Clones ran exactly as asked: `git clone --depth 1 <url>` from
`C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/`.
Counts via house venv python (`os.walk`, `.git` excluded): files = regular files
walked; total bytes = sum of `os.path.getsize` over those files. Symlinks skipped.

This is the byte-verify memo only. No additional steal memo is being filed with it.

---

## Repo 1 — azerothcore/mod-playerbots

- Local path: `C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots`
- HEAD: `49dfc1fb4a0068a1537571d2dbb29ab0dea3ac53`
  - `49dfc1fb4a0068a1537571d2dbb29ab0dea3ac53 2021-12-28 03:23:18 +0300 Update Bots` (author: celguar)
  - Single squashed root commit at this tip (diffstat shows the whole tree added in one commit).
- Remote verification (run post-clone):
  - `git ls-remote https://github.com/azerothcore/mod-playerbots HEAD` → `49dfc1fb4a0068a1537571d2dbb29ab0dea3ac53`
  - `refs/heads/master` → same sha. Local == remote. Not stale, not redirected.
- Byte verify (verbatim venv-python output, `.git` excluded):
  - `mod-playerbots files= 4196 total_bytes= 237459694` (≈226.4 MiB)
- License: **GPL-2.0** — `LICENSE.md` opens "GNU GENERAL PUBLIC LICENSE Version 2, June 1991".
- What it actually is: a **CMaNGOS (mangos-wotlk) server snapshot**, not an AzerothCore module tree.
  - `README.md` is the C(ontinued)-MaNGOS README ("Doing Emulation Right!").
  - `src/` layout is MaNGOS-style: `framework/ game/ mangosd/ realmd/ shared/ modules/`.
  - `COPYRIGHT.md` speaks for "CMaNGOS project" and asserts Fair Use of Blizzard® material.
  - Tags on remote: `Last_mangos-wotlk_PreBuild`, `v0.12`…`v0.16-dev2`.
- **Critical caveat — the bots are NOT in this repo.** `.gitmodules` maps
  `src/modules/Bots` → `https://github.com/celguar/mangosbot-bots.git`, and that
  directory is **empty** in our depth-1 clone (submodules are not fetched by
  default). The commit subject "Update Bots" + empty dir say the same thing.
  Anyone steering on "playerbots code lives here" is wrong by one hop: the bot
  payload is in the submodule.
- GitHub API cross-check (`api.github.com/repos/azerothcore/mod-playerbots`):
  `description: "NOT READY TO BE USED AS MODULE YET"`, `default_branch: master`,
  `pushed_at: 2021-12-28T00:26:05Z`, `license: GPL-2.0`. So the famous
  actively-developed playerbots module is **not** this URL's tip; name collision.
  If the estate wants the live playerbots project, that is a different upstream
  and needs its own ask.

### Stance
Keep as **terrain sample, not dependency**. GPL-2.0 is viral for our purposes:
read/learn, never paste into estate code without accepting GPL obligations.
The interesting maps here are (a) the MaNGOS-era server architecture
(`realmd`/`mangosd`/`shared`/`game` separation, 237 MB of C++ emulation
practice) and (b) the *pointer*: `celguar/mangosbot-bots` is the actual bot
brain and should be cloned separately if bot behavior is ever the target.
The name on the tin ("azerothcore mod-playerbots") does not match the contents
(CMaNGOS + empty Bots dir) — logged so no downstream lane chases this repo for
playerbot logic.

---

## Repo 2 — evennia/evennia

- Local path: `C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/evennia`
- HEAD: `a89a9b94e4d7ed0acfee86def533b77bf6baa512`
  - `a89a9b94e4d7ed0acfee86def533b77bf6baa512 2026-08-19 23:26:05 +0200 Merge pull request #3976 from evennia/dependabot/uv/sqlparse-0.6.0`
- Remote verification (run post-clone):
  - `git ls-remote https://github.com/evennia/evennia HEAD` → `a89a9b94e4d7ed0acfee86def533b77bf6baa512`. Local == remote.
- Byte verify (verbatim venv-python output, `.git` excluded):
  - `evennia files= 1626 total_bytes= 14725585` (≈14.0 MiB)
- License: **BSD 3-Clause** — `LICENSE.txt` opens "BSD 3-Clause License",
  "Copyright 2012- Griatch … Gregory Taylor".
- What it is: **Evennia**, a modern Python library for creating online multiplayer
  text games (MUD/MUSH/MUX/MUCK/MOO). Per its README: "Evennia does not impose a
  particular style, genre or game mechanic… Coding in Evennia is done using
  normal Python modules imported into the server at runtime." Ships `evennia/`
  package, web client, `pyproject.toml`, `uv.lock`, extensive `docs/`.
- GitHub API cross-check: `description: "Python MUD/MUX/MUSH/MU* development
  system"`, `default_branch: main`, `pushed_at: 2026-09-19T01:46:46Z`
  (actively maintained), `stargazers_count: 2105`, `license: BSD-3-Clause`.

### Stance
This is the **closest living relative to the game-organ estate**: a pure-Python,
permissively licensed (BSD-3) framework whose entire subject is *running a
persistent multiplayer game world* — sessions, accounts/characters, command
parser, scripted objects, web+telnet front doors, django-backed persistence.
Maps worth stealing for the estate:
- **Runtime-imported game modules**: content as ordinary Python imported at
  server runtime — same move as our organ/house "code as law" pattern.
- **Command parser as a thin user-facing shell over object methods** —
  mirrors the scoreboards/verbs split.
- **Typeclass persistence** (objects as Python classes with DB rows) —
  directly relevant to persistent estate state.
- **Account ↔ puppet (character) separation** — a clean model for
  operator vs. agent identities in the estate.
BSD-3 means we may borrow patterns and even code with attribution; no copyleft
contagion. Safe to study deeply and lift ideas from.

---

## Verification commands actually run (receipts)

```
git clone --depth 1 https://github.com/azerothcore/mod-playerbots   # 4197 files checked out
git clone --depth 1 https://github.com/evennia/evennia              # 1626 files checked out
git -C .../mod-playerbots rev-parse HEAD   # 49dfc1fb4a0068a1537571d2dbb29ab0dea3ac53
git -C .../mod-playerbots log -1 --format='%H %ci %s'
git -C .../evennia rev-parse HEAD          # a89a9b94e4d7ed0acfee86def533b77bf6baa512
git -C .../evennia log -1 --format='%H %ci %s'
git ls-remote https://github.com/azerothcore/mod-playerbots HEAD refs/heads/master
git ls-remote https://github.com/evennia/evennia HEAD
<venv python> os.walk byte count  (C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe)
  → mod-playerbots files= 4196 total_bytes= 237459694
  → evennia        files= 1626 total_bytes= 14725585
head -30 LICENSE.md (GPL-2.0) / head -30 LICENSE.txt (BSD 3-Clause)
cat .gitmodules → src/modules/Bots → https://github.com/celguar/mangosbot-bots.git
curl api.github.com/repos/{azerothcore/mod-playerbots,evennia/evennia}
```

Note on counts: git checkout reported 4197 files for mod-playerbots; the walk
counts 4196 — difference is the empty `src/modules/Bots` submodule directory
(unpopulated, zero files). Byte counts exclude `.git` by design (working-tree
payload only).

— A10, 2026-09-22
