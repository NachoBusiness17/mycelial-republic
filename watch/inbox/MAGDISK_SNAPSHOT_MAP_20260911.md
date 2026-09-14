# MAGDISK SNAPSHOT MAP 2026-09-11 — `_archaeology_out/` full inventory + incarnation verdict

**Commission:** lost-record dig, rotation width 2 (relaunch after the 13:02 rate-limit death).
Lane: the OTHER half of PREMAP's flag — game_sessions/ + full inventory + chain-lost material.
Read-only except this file. Absorbed: `watch/inbox/ATTIC_STRATA_20260911.md` (attic = retired
code + founding doctrine, no session history) and `watch/inbox/PREMAP_ARCHAEOLOGY_20260911.md`
(parts 8+9+10 = zero-overlap 3-way split of one Sep-5 live-repo snapshot; 42 extinct mag/ organs).

---

## 1. Inventory (os.walk, measured 2026-09-09)

**Total: 3,448 files, 158,752,106 B (151.4 MiB).** All mtimes are the 09-05 copy instant
(extracted 18:02–18:03, zips 18:04) — content dates come from inside files, never mtimes.

| item | files | bytes | notes |
|---|---|---|---|
| `mag-disk-20260905/` (extracted) | 3,444 | 77,792,792 | handoff(1,018) + mag(1,774) + dashboard(242) + memory(380: steal 139, working/game_campaigns 217, working/game_sessions 7) |
| `nacho-archaeology-part8-mag-disk.zip` | 236 entries | 23,525,567 | split slice 1 |
| `nacho-archaeology-part9-mag-disk.zip` | 792 | 9,508,910 | split slice 2 |
| `nacho-archaeology-part10-mag-disk.zip` | 2,416 | 7,445,202 | split slice 3 |
| `nacho-archaeology-part8-mag-disk-FULL.zip` | 3,444 | 40,479,635 | the WHOLE tree again in one zip |

Split arithmetic confirms PREMAP: 236+792+2,416 = 3,444 = extracted count, zero overlap.
**Refinement PREMAP missed: part8-FULL.zip is a redundant superset** — the same 3,444 files
shipped TWICE in this directory (~77 MB duplication). Halving this stratum is one `rm` away.

## 2. Incarnation verdict

**"Sep-5 snapshot of the live body, not an ancestor" — SUPPORTED, now byte-proven against live.**
Set-diff of the whole extracted tree vs the live repo (pycache excluded):

- `handoff/`: disk 1,018 = live 1,018, **disk-only 0** — identical path sets.
- `memory/`: disk-only **0** (live memory/ is the living superset).
- `mag/`: disk 1,774, disk-minus-live = **exactly 42** — see §4.
- `dashboard/`: disk-only **1** — `static/room_game.html`, the single unique file in the tree.

## 3. game_sessions anatomy

7 files, `memory/working/game_sessions/seal_gc-<campaign>_<isots>.json`, schema
`mag_game_session_seal.v1` (turn-sealed state: player sheet, flags, metrics, log_tail, tldr,
dogfood_dm, transfer_checklist). Range **2026-08-07T04:07Z → 2026-08-29T22:36Z**. 3 campaigns:

- `gc-846c347911` — "The Guttered Lantern → Classic Keep" (`dnd_classic_stub` homage), player
  **Ash** the fighter, `voice_session_id: dm-seal-smoke`, tldr "Primer smoke". **The 08-07 seal
  is the oldest hard content byte in the entire dig** — it predates the corpus chats (Aug 11/12,
  per PREMAP) and fleet day one (Aug 25). The game lineage started Aug 7.
- `gc-785079f254` — one seal, Aug 15.
- `gc-faec71d3da` — "The Clear Pipes — a water-computer keep" (`water_computer`), player
  **Operator** the engineer, `voice_session_id: grok-play`; 5 seals on Aug 29 22:23→22:36;
  final tldr: "Grok played water keep honest… won=true cheated=false".

**Lost? NO — all 7 byte-identical (sha16) to the live `memory/working/game_sessions/`.**
This organ's history was never at risk; the disk copy is pure redundancy.

## 4. The 42 extinct organs

All three probes byte-exist in the disk: `mag_soul.py` (5,279 B, sha16 `da7b5ba9a0415f19`),
`mirror_persona.py` (16,180 B, `20d8f11566e782b4`), `tesuji_steal.py` (7,106 B,
`32f6932a3fb0dd97`). **Each is byte-identical to its attic kill-list copy
(`attic/kill_list_20260908/mag/`), and filecmp(mag_soul.py disk vs attic) = identical.**

Cross-check: disk-mag minus live-mag = 42 files; those 42 ∩ attic kill-list mag = **42/42,
zero outside**. The disk's "extinct" set and the 09-08 kill-list set are THE SAME 42 files,
now preserved byte-exact in two independent copies. PREMAP's recovery list is valid but the
disk adds no unique bytes for it — the attic already holds every one (and ATTIC_STRATA §6
already names the recovery fold). Deletion window refined: not "Sep 5→9" vaguely — the files
were live at the 09-05 snapshot and gone by the 09-08 kill execution.

## 5. Chain-lost verdict + recovery value (tri-state)

- **"This directory holds chain-lost session/knot material" — DISPUTED.** Sessions 7/7 byte-live,
  handoff and memory path-identical to live, the 42 duplicated in the attic. The real
  chain-adjacent history (conversation-blobs.db, store.db, transcripts) lives in
  `corpus/oral_history/nacho_archaeology/` parts 1–7, not here (ATTIC_STRATA §4 + PREMAP).
- **"`_archaeology_out` is a code snapshot stratum" — SUPPORTED**, with exactly one orphan:
  `dashboard/static/room_game.html` — a Sep-5-era game-room page that lived on the dashboard
  and was deleted from live between 09-05→09-09. Ancestor of today's room/game surfaces;
  the only byte in 3,444 that exists nowhere else.
- **Recovery value: LOW for loss, MEDIUM as witness.** Actions worth one fold, nothing more:
  (1) skim `dashboard/static/room_game.html` before any dashboard cleanup — it's free;
  (2) treat part8-FULL.zip as the dedup candidate (~40 MB reclaimable with zero loss —
  operator-gated, this was read-only); (3) the Aug-7 "Primer smoke" seal quietly moves the
  fleet's playable-game start date to Aug 7 — worth one line in the biography when the game
  arc next gets written.

---
*Method: os.walk inventory + sha16/set-diff vs live tree, 2026-09-09, read-only except this
file. Sources: `_archaeology_out/` measured directly; absorbed cards cited above. Falsifier:
any count above reprovable by rerunning the walk; any "identical" disprovable by one sha256.*
