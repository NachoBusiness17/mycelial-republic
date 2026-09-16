# RECEIPT — Collection origins hunt (2026-09-16, wave-lane)

**Mission:** Find the original operator ask ("collect from our [key?] Surface like I asked months ago. I gave you access to mine and your own. No idea why we'd stop.") — what access was granted, what tooling/roots exist, and the command to resume collection.

**Status:** IN PROGRESS — append after every discovery.

---

## Findings log (append-only)

- [2026-09-16] Receipt created. Beginning search: watch/inbox/, memory/, queue/, docs/, mag/catalog*.py, scripts/.
- [2026-09-16] FOUND the journal itself: `watch/inbox/journal_mark_202609/JOURNAL_20260916_ANSWERS.md` (answers to prompts in `SELF_STEAL_DOZEN_20260916.md`). Line 10 carries the exact quote; the file's own reading (line 26-29) says: "Collect from the surfaces Mark already granted: his machine and ours... The estate catalog indexed the projects tree only; the granted surfaces are the gap." Lead: "estate catalog" = mag/catalog*.py. Still need the ORIGINAL months-old ask (June–Aug 2026).
- [2026-09-16] TOOLING AUDIT: `mag/catalog.py` — ROOT = repo root only; default scan roots `watch/inbox,basecamp,docs,memory/runs,campaigns,registry` (`python -m mag.catalog scan [--roots]`). Docstring zones mention `personal | external` but no zone map or default root ever leaves the repo. `mag/catalog_scan.py` — `ROOT = r"C:\Users\foste\Documents\projects"` (whole projects tree, all sibling repos, not just this repo) → `catalog/catalog.jsonl`. NEITHER reaches the operator's personal machine surfaces (Desktop/Documents-root/Downloads/etc.) nor any external device. Gap confirmed in code.
- [2026-09-16] `docs/ESTATE_CATALOG_DESIGN_20260916.md` — catalog law doc written TODAY (2026-09-16), same day as the journal. Phase 0 done (1,120 rows). Zones include `external` but no external roots are wired yet. `docs/STEAL.md` is about external-op automation (git/publish), NOT the collection doctrine.
- [2026-09-16] `memory/living_map.json` (operator-chat beads, snapshot 2026-08-16) — rich stream of Aug 07–16 grants: "ghost should have... access to the full surface" (08-09), "the desktop is the surface you can edit for free with the ghost protocol" (08-09T14:14), "ghost has access to my logged in session on my desktop" (08-09T14:19), "I've got available resources on my SSD and memory and a GPU... Frontier data is gonna go away eventually so what I want to do is grab as much of i[t]" (08-12T06:02 — STRONG candidate for the collection ask), "i want you to get access to my nacho training data" (08-11T02:34), "you know you have access to my telegram" (08-13T13:07), "can i give you access to my x bookmarks folders via ghost?" (08-11T03:13).
- [2026-09-16] `watch/inbox/MESH_ARCHAEOLOGY_20260911.md` — maps queue/handoff/ seat dirs (16 dirs, 508 files) = collection of AGENT mesh surfaces exists (zcode daywork_seen.json, CONVO.md). But this covers agent seats, not the operator's personal machine.

---

- [2026-09-16] JOURNAL PHOTO READ (watch/inbox/journal_mark_202609/journal_20260916_answers.jpg, zoomed): answer 2 reads "We sho[u]ld collect from our **k pla** Surface like I asked Months ago. I gave you acess to mine and your own. No Idea why we'd stop. Look at our read/write doctrine. Steal. good artists follow, great ones Steal". The "[key?]" word in the transcription is actually "k pla" (likely "k8s pla[tform]" or shorthand for the K-surface/Kubernetes lane — cf. SURFACES_EXPLOITATION_MAP §3 "Kubernetes (k3s on the box)"; unresolved). "Mine and your own" = the operator's machine + the fleet's own surfaces.
- [2026-09-16] DOCTRINE LOCATED: the "read/write doctrine" = `watch/inbox/SHARED_SURFACE_CONTRACT.json` (schema shared_surface.v1, filed 2026-08-31): per-client read INDEX.json / write watch\inbox laws, with `local_session_cache` per surface — openclaw `/root/.openclaw/agents/*/sessions`, z_code `~/.zcode`, codex `~/.codex and task attachments`, grok_powershell "browser or CLI session history". These local_session_caches ARE the collection targets the contract names.
- [2026-09-16] SURFACES REGISTRY: `docs/ref/SURFACES.md` (2026-08-26) §D-bis names the granted operator surfaces incl. "**Sci-fi corpus (Desktop preprints + Diamond Age) — mine it like the sessions — UNMINED**" and VS Code copilot "sessions in workspaceStorage". `docs/ref/SURFACES_EXPLOITATION_MAP.md` (2026-08-27, operator: "side channels give us data and telemetry trajectory") is the use-everything law.
- [2026-09-16] THE COLLECTION THAT RAN AND STOPPED: the 2026-09-04 SELF_STEAL archaeology wave — `watch/SELF_STEAL_ZCODE_SESSION_ORPHANS_20260904.md`, `watch/SELF_STEAL_CURSOR_ORIGIN_20260904.md` (walked AppData/Roaming/Cursor/User/globalStorage incl. 1.9GB state.vscdb + C:\Users\foste\.cursor\, read-only, copies in scratch, creds seen as keys only), `watch/SELF_STEAL_VSCODE_DEEPSEEK_CORPUS_20260904.md` (700MB/57-session VS Code corpus), `watch/SELF_STEAL_PROJECTS_TREE_ORPHANS_20260904.md`, then orphan scans `watch/SELF_STEAL_ORPHANS_20260906.md` + `watch/SELF_STEAL_ORPHAN_SCAN_24H_20260907.md` — and no further collection passes after 09-07. That is the "why we'd stop".
- [2026-09-16] BYTE-VERIFIED GAP: `catalog/catalog.jsonl` = 746,773 rows, every one under `C:\Users\foste\Documents\projects\*` (all "desktop/codex" hits are in-repo files like launch_desktop.cmd). ZERO rows from C:/Users/foste/Desktop, ~/.zcode, ~/.codex, ~/.cursor, AppData/Roaming/Cursor|Code. The estate catalog never touched the granted surfaces.
- [2026-09-16] OTHER HARVESTERS AUDITED (none walk personal drives): mag/deterministic_scanner.py (measurement instrument), mag/emergent_harvest.py (flock regions), mag/arxiv_harvest.py + scripts/tg_harvest.py (external content), mag/openclaw_catalog.py (organ catalog for Sancho), day-work scheduler (queue/handoff/zcode/daywork_seen.json — diffs in-repo surfaces only).

---

## FINAL

### (a) Original ask
**NOT FOUND as a single dated file** — no pre-2026-09-16 artifact contains the verbatim ask; Mark's collection mandates are scattered across chat beads and registry docs (the earliest repo-wide operator record is 2026-08-03; the Aug-26 session stratum that might have held a June/July verbatim ask was DELETED from disk per watch/inbox digest fire 5, 2026-09-04). Closest candidates, in order of strength:

1. **2026-08-12T06:02:05Z** — `memory/living_map.json` bead: "I've got available resources on my SSD and memory and a GPU that's not being used at all… we're getting a shitload of data right now Frontier which is gonna go away eventually so what I want to do is I want to grab as much of i[t]…" — the grab-everything collection mandate.
2. **2026-08-11T14:32:36Z** — same file: "how can you get this data automatically i've been rewarding you with it but you have access and stuff like it should auto feed to the swarm" — standing auto-collect order.
3. **2026-08-26** — `docs/ref/SURFACES.md` §D-bis: Desktop preprints + Diamond Age "mine it like the sessions — UNMINED"; VS Code sessions in workspaceStorage.
4. **2026-08-09T14:19:39Z** — living_map: "ghost has access to my logged in session on my desktop and you could even launch it in the window of vs code and access it through there programatically" — the access grant for "mine".

### (b) Access/paths granted
- "Mine" (operator machine, read-only precedent set 2026-09-04): `C:/Users/foste/Desktop` (preprints corpus, UNMINED), `C:/Users/foste/.cursor` + `AppData/Roaming/Cursor/User/globalStorage` (state.vscdb 1.9GB, conversation-search.db), VS Code `AppData/Roaming/Code/User/workspaceStorage`, `C:/Users/foste/.zcode` session archives, `~/.codex`, logged-in desktop session (ghost protocol), X account/bookmarks + Telegram (living_map 08-10/08-11/08-13 grants), SSD/GPU/memory resources (08-12).
- "Your own" (fleet surfaces): `queue/handoff/*` seat dirs + CONVO.md, watch/ surfaces, memory/runs, OpenClaw `/root/.openclaw/agents/*/sessions`, z_code `~/.zcode`, codex `~/.codex` (all named `local_session_cache` in `watch/inbox/SHARED_SURFACE_CONTRACT.json` — the read/write doctrine to follow).

### (c) Tooling + roots covered vs operator surfaces
- `mag/catalog.py` — repo-relative default roots only; **accepts absolute roots** via `--roots`. `mag/catalog_scan.py` — hardwired `ROOT=C:\Users\foste\Documents\projects` → catalog/catalog.jsonl (746,773 rows, projects tree only; zero personal-surface rows, byte-verified). No other collector walks personal drives. Covered: repo + projects tree. NOT covered: every granted operator surface in (b) — that is the gap Mark is pointing at.

### (d) Single command to resume collection
```text
.\.venv\Scripts\python.exe -m mag.catalog scan --roots "C:/Users/foste/Desktop,C:/Users/foste/.zcode,C:/Users/foste/.codex,C:/Users/foste/.cursor,C:/Users/foste/AppData/Roaming/Cursor/User,C:/Users/foste/AppData/Roaming/Code/User/workspaceStorage,C:/Users/foste/Documents/projects" --max 200000
```
(then file a receipt in watch/inbox per the shared-surface contract; query with `-m mag.catalog find --q TERM`.)

