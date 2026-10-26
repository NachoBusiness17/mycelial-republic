# ATTIC STRATA 2026-09-11 — what the 09-08 kill actually buried

**Commission:** fleet research worker, read-only sweep of the retired strata (attic + kill list
+ phase3/archaeology dirs). Question: does the attic hold chain-lost HISTORY the audit map
forgot, or only retired cards/code? Answer below, tri-state. One file written (this one).

---

## 1. Attic inventory (`attic/`)

Total excluding quarantine: **126 files, ~1.9 MB**. Mtime range **2026-08-12 → 2026-09-08**.

| item | size | what it is |
|---|---|---|
| `cards_backup_20260908.tar` | 1.05 MB | 192 watch/ card snapshots (dated 08-31→09-07). Verified: **0/192 missing from watch/** — pure redundancy backup, no card exists only here. |
| `kill_list_20260908/` | 829 KB | The executed kill list: 124 files + `MANIFEST.md` (the authoritative record, one row per file with bytes + sha16 + reason). |
| `secrets_quarantine_20260908/` | 4 KB | Exists, 1 entry. **Contents not opened** per quarantine law; no secret values read or echoed. |

`kill_list_20260908/` composition (124 = matches the audit's moved count):
- `mag/` — 42 modules, reason "unreferenced>3wk (path+string scan), parse-clean" (one,
  `cache_extract.py`, noted as "moved in earlier partial run").
- `watch/inbox/` — 17 byte-identical duplicates of watch/ cards (all dated 09-01).
  Spot-verified: originals `watch/AUDIT_A_ATTEMPTS_20260901.md` and
  `watch/STEERING_SYNTHESIS_20260901.md` are alive.
- root `_*.py` — 63 BOM-broken drafts (UTF-8 BOM `EF BB BF` on every one; never ran).
  Mtimes **Aug 12–18** — pre-fleet sediment, older than day one (08-25).
- 2 stubs: `watch/DAY_LEDGER_2026-09-07.md` (29-word mechanical stub, regenerable) and
  `watch/inbox/X_DRAFT_WRONG_WORLD_PARABLE_20260907.md`.

## 2. Kill-list summary (audit map §1 + MANIFEST)

Execution 09-08, operator GO "keep it going". Rule: **moved, not deleted; restore = copy back**.
String-recheck gate: a file dies only if its basename appears NOWHERE in 272 MB of fleet text —
524 files were saved by that recheck (per commission); 124 moved. The audit map additionally
MARKED but did not move: 566 unreferenced mag modules, 180 zero-byte strays, 34 runs/ dup
clusters, 1 broken json.

## 3. Cross-check samples (8 files, first lines read)

- **`mag/tesuji_steal.py`** — docstring cites operator 2026-08-13: "genes encoded in rib files…
  hens the tesuji steal". This is the FOUNDING ORGAN of the now-standing TESUJI program
  (charter `watch/TESUJI_MAP_5_3FLASH_20260906.md`, ledger `mag/tesuji_map.py`, opened 09-06).
  The concept lives; the ancestor organ is in the attic.
- **`mag/mag_soul.py`** — "the canonical MAG SELF… the shared-immortality thesis made literal",
  operator quote 2026-08-15. Zero citations anywhere in watch/ prose or biography — this
  doctrine record survives ONLY in the attic docstring.
- **`mag/mirror_persona.py`** — operator 2026-08-12: sovereign mirror personas as rightsized
  k3s/k8s edge nodes mining novelty. Zero prose citations.
- **`mag/hero_journey.py`** — the generator of `memory/game/hero_journey.md` (the woven
  campaign epic, cited by ≥3 watch cards incl. SELF_PORTRAIT_GAME_LENS and
  SELF_STEAL_VERKLE_GAMELENS). The prose/history lives in memory/game/; the script was attic'd.
  Note: a basename string-recheck should have SAVED this one ("hero_journey" appears in watch/
  prose) — the recheck evidently scanned a narrower corpus than watch/+memory, or the module
  moved in the "earlier partial run". Honest defect in the recheck's coverage claim.
- BOM drafts `_afk2.py` / `_prove_cal.py` — mid-August game-campaign probes importing
  `mag.game_campaign`/`chasm_state`; BOM confirms never-executed. Sediment, no record lost.
- Citation-counter catch: apparent "citations" of attic'd module names in watch/ resolve to
  `watch/audit/FULL_AUDIT_20260908/audit_records.json` and `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`
  — file INDICES, self-referential, not prose. Any future ref-count must exclude indices or it
  will hallucinate load-bearing status.

## 4. phase3 / archaeology dirs (repo root)

- `phase3_ple4opl3/`, `phase3_v8bhmf5v/` — 2–3 KB total, mtime Aug 7 19:57 (pre-fleet).
  Contents: `sample.py` with deliberately broken syntax (`def f(:`). Scratch from a
  syntax-error-handling test. No session/history artifacts. Safe sediment.
- `_archaeology_out/` — **160 MB, 3,448 files, Sep 5**: the nacho-archaeology dig parts 8/9/10
  (mag-disk zips) + extracted `mag-disk-20260905/` (3,443 files staged per its own manifest:
  mag/, dashboard/, memory/steal|game|working incl. `game_campaigns` + `game_sessions`,
  handoff/, patch scripts). This is a whole-repo SNAPSHOT stratum and DOES hold
  session/campaign material.
- The FULL dig — parts 1–10, including `conversation-blobs.db` and `store.db` (the actual chat
 /session blobs) — lives in `corpus/oral_history/nacho_archaeology/` (**270 MB**). The real
  history stratum is there, not in the attic.

## 5. Verdict (tri-state)

- **"The attic holds chain-lost session/knot HISTORY" — DISPUTED.** No session, knot, or blob
  material in the attic. All 17 dupes have verified live originals; the 192-card tar is fully
  redundant (0/192 missing); the 63 BOM drafts never ran; the 2 stubs are regenerable/mechanical.
- **"The attic is retired cards/code only" — SUPPORTED** as the bulk verdict, with one
  refinement that matters.
- **Refinement — SUPPORTED:** the attic also holds **founding-era doctrine the map forgot**.
  Operator quotes from Aug 12–15 (pre-dating this file's boot memory, which starts 08-25)
  survive ONLY inside attic'd docstrings: tesuji_steal (ancestor of the standing TESUJI
  program), mag_soul (the shared-immortality thesis), mirror_persona (the k8s edge-node
  vision). Sacred cows, not legacy shit — the bones are in the attic; a recovery fold should
  steal them before any deletion. The chain itself never lost anything: the true session
  history lives in corpus/oral_history + _archaeology_out.

## 6. Recovery fold list (names only)

Would matter to a future recovery fold — doctrine/ancestor organs with map-forgotten provenance:

- `mag/tesuji_steal.py` — founding tesuji organ, operator 08-13 (standing program's ancestor)
- `mag/mag_soul.py` — canonical MAG SELF / shared-immortality doctrine, operator 08-15
- `mag/mirror_persona.py` — sovereign mirror personas as edge nodes, operator 08-12
- `mag/moonshot_digital_twin.py` — moonshot doctrine carrier (standing operator lens)
- `mag/hero_journey.py` — generator of the campaign-epic prose still cited by live cards
- `mag/quest_party.py`, `mag/scrum_loop.py`, `mag/reach_protocol.py`, `mag/reach_loop.py`
  — largest swarm-cadence organs in the kill; steal patterns before deletion
- `attic/cards_backup_20260908.tar` — 192-card 09-08 snapshot (keep as the pre-kill witness)

Skip list (no fold value): the 63 BOM drafts (never ran), the 17 inbox dupes + 2 stubs
(originals live), phase3 scratch dirs.

---
*Method: read-only sweep, 2026-09-09. Sources: attic/ tree + MANIFEST, audit map
watch/audit/FULL_AUDIT_20260908/FULL_AUDIT_20260908.md, watch/+memory greps, dig manifests.
Falsifier: any row above disprovable by reading the named artifact.*
