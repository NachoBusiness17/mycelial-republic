---
name: team-collaborators-roster
description: Collaborator roster + their onboarding door — Melissa (writer, Soul
  Castle world, wants team-up), Marque (builder, own games.zip, "games mapped to
  AI"), Adam (player one); TEAM.md → onboard/team.html is their page; Telegram
  is the office
metadata:
  node_type: memory
  type: project
  originSessionId: sess_cc461d2f-b0e3-4197-8520-3684da78785a
---

2026-09-14: Melissa relayed a Telegram team-up thread and the operator asked for a collaborator onboarding doc — "for all collaborators, not just Adam, less AI cult, more action and games."

- **Roster:** Nacho (games/stories/house) · **Melissa** (words — books, worlds; her ask: "Skyrim-ish but in my Soul Castle world" — maps to the mud tier wearing someone else's canon; she never touches code) · **Marque** (builder — built his own version of the stack, sent games.zip, "games mapped to AI… ambitious stuff"; his door = the single-HTML-file shelf) · **Adam** (player one) · the AI (does the typing).
- **Their page:** `watch/onboard/TEAM.md` → builds to `site/dist/onboard/team.html` (PAGES entry added to site/build.py). GAMEBOOK.md playable-surfaces section updated same day (was stale — pre-MUD). Both written to the Primer law: their door, their language, game-first, no syllabus, no AI-cult register.
- **Build note:** full `site/build.py` runs hit `rmtree(OUT)` PermissionError on Windows (locked dist dir) — build.py now uses `rmtree(ignore_errors=True)` + `mkdir(exist_ok=True)`, and pages can be rebuilt surgically through build.py's own md/page objects without the full wipe.

**Why:** the doors doctrine (WELCOME v3) — every reader enters through THEIR door; the shelf is inventory now, so collaborator games (Marque's zip) ship as single files with names on them.

**Status (2026-09-14 evening):** Marque accepted the team-up ("deal") and sent games.zip — not yet inspected/landed. **Soul Castle is named but never built** — the fifty-wide sweep found it exists only as Melissa's words in TEAM.md/team.html (gap: total); the nearest analog is memory/castle_foundation/growth.jsonl. The monastery restructure (7 rooms) is the mud-tier surface a Soul Castle skin would drop onto.

**How to apply:** new collaborators get a door on TEAM.md written to their skill (writer → "send story beats, we build it"; builder → "single HTML file, it ships"); keep the register plain and action-first per the operator's standing correction. See [[nacho-quixotic-parables-author]], [[vislab-catalog-surface]].

**Soul Castle ownership note (2026-09-16):** no Soul Castle lore file exists anywhere on disk — TEAM.md's one line is the whole world. The U6 night's four NPC speeches (monk-doorkeeper, lamplighter, doubting knight, the bell) are the first seeds laid there, and they are DRAFTS OFFERED to Melissa, not canon — canon for her world is hers to accept or overrule. Worth a line in her next Telegram note rather than a silent claim. See [[union-alpha-free-window-20260916]].
