# INVARIANTS SHRINK — FULL FORENSICS (2026-09-06, seat shrink)

Follow-up to `research/orphan_registry/memory_orphans.md` row 4 (the finding) and
`watch/SELF_STEAL_ORPHANS_20260906.md` incident row. Evidence, not blame. $0, no network,
live file NOT touched. Tesuji: R/incident/invariants/{timeline,mechanism,recovery},
verify PASS (255 cells, tip 47b8d8ec35e6).

## VERDICT (one line)

The registry was not "shrunk by a buggy writer" — it was WIPED out-of-band in the
Sep 5 21:37 → Sep 6 04:49 local quiet window; the (merge-safe) behavioral percolator
then rebuilt it from scratch at 04:49:55 local. **Lost-unique = 0**: the fullest state
(57 gens / 44,653 counts) survives in a seal snapshot the finding doc didn't know about.
Recovery is BETTER than the .bak the finding pointed at.

## 1. Timeline (all times local = UTC-4; Z where marked)

| When | Event | Evidence |
|---|---|---|
| Aug 30–Sep 2 | Registry at 45 gens / 15,896 counts; last fat write Sep 2 13:26:14Z | content of both .bak files (last_seen fields) |
| Sep 2 09:26:14 | `invariants.json.bak-20260902` created 4 ms after that write (deliberate backup) | file mtime 09:26:14.960951 vs last_seen 13:26:14.956938Z |
| Sep 5 01:23:43Z | seal: **47 gens / 36,574 counts** — registry grew ~2.3x Sep 2→5 (behavioral flood) | `memory/seals/2026-09-05T01-23-43/` |
| Sep 5 21:37:32 | last registry write before the wipe (212719f4 + f0879ec0 last_seen) | seal0906 entries |
| Sep 5 21:40:13 | seal: **57 gens / 44,653 counts — THE FULLEST STATE** | `memory/seals/2026-09-06T01-40-13/` (dir name is UTC) |
| Sep 5 21:46:11 | MEMORY.md trim backup (`MEMORY.pre_trim_20260906.bak`) — memory-hygiene active in the wipe window | file mtime |
| Sep 5 22:50:29 | MEMORY.md edited again (dual-index drift day) | file mtime |
| Sep 6 01:03:44 | ORPHAN_RUN card written | watch/ORPHAN_RUN_20260906.md mtime |
| Sep 6 01:04:50 | `invariants.json.bak` created — but its content is byte-identical (sha d93fca0f4041) to the STALE Sep-2 backup, NOT to the then-live 44K-count registry: a backup made from the WRONG source (`cp bak-20260902 bak`) | byte comparison, mtimes |
| Sep 6 01:40–04:49 | **THE WIPE** — invariants.json deleted/emptied out-of-band; no code path and no card names the act | window bounded by seal last_seen (01:37:32Z) and first fresh first_seen (08:49:55Z) |
| Sep 6 04:49:55 | Behavioral percolator resumes, finds registry missing/empty, reseeds: fresh entry 212719f4 count=1; f0879ec0 one second later | live file first_seen fields |
| Sep 6 12:18 | Finding doc observes live at 5 gens / 2,678 counts | memory_orphans.md row 4 |
| Sep 6 13:00:47 | live at 5 gens / 2,919 counts — writer still ticking (2,389+ on the top ID by staging time) | mtime, count drift between my reads |

PRIOR ART: the same replace-not-merge signature happened BEFORE — seals show 552 gens
(Aug 24 17:06Z) → 90 gens (Aug 26 06:17Z), counts rising (2,568 → 4,977): rebuild-from-recent,
generation loss. This is a RECURRING pattern, not a one-off.

## 2. Diff (live vs .bak vs seals)

- Sources: live 5 gens / 2,919→3,063 counts (growing); .bak == .bak-20260902 byte-identical,
  45 gens / 15,896 (STALE Sep-2 content); seal 2026-09-06T01-40-13 = **57 gens / 44,653**;
  seal 2026-09-05T01-23-43 = 47 gens / 36,574.
- The 5 live IDs are all in the seal; seal counts for them are 36,349 / 7,715 / 108 / 82 / 32
  (vs live's fresh 2,389 / 534 / 11 / 4 / 2 — the writer RESET, did not continue).
- Dropped from live: 52 IDs. **In .bak but not in the Sep-6 seal: none. In Sep-5 seal but not
  Sep-6 seal: none. Union of all sources = 57 = exactly the Sep-6 seal.**
- **LOST-UNIQUE = 0.** Nothing exists only in the shrunken file; nothing is unrecoverable.
- The finding doc's "13,218 counts dropped" = 15,896 − 2,678 (bak-vs-live arithmetic). True
  dropped-from-live delta vs the real fattest state: 44,653 − 2,678 ≈ **41,975 counts**, all
  recoverable from the seal. The finding's "recoverable from .bak" UNDERSTATES recovery by
  28,757 counts and 12 generations.

## 3. Mechanism (file:line) — tri-state

- SUPPORTED — the only writer of the registry is `mag/percolator.py:145-147`
  (`_save_registry`), and its write path is MERGE-SAFE: `_compile_invariant`
  (`mag/percolator.py:193-205`) does load → update-or-insert → save. It cannot shrink a
  healthy file.
- SUPPORTED — the continuous writer is the behavioral-event pipeline:
  `mag/operator_inbox.py:424-426` calls `percolate_signal(..., domain="behavioral")` on every
  failure/steer/swarm-health event. At 04:49:55 local Sep 6 it found the registry
  missing/empty; `mag/percolator.py:137-138` (`_load_registry`: missing file →
  `{"invariants": {}}`) plus `:203` (insert fresh) rebuilt it with new first_seen — the exact
  disk signature observed.
- SUPPORTED — no script in mag/ scripts/ watch/ queue/ writes a fresh registry (grep: only
  seal.py copies it; seed_percolator keeps its own registry.jsonl; template_invariant writes
  its own ledger). Therefore the wipe was OUT-OF-BAND: a shell delete/empty/overwrite by an
  agent during the quiet window.
- UNPROVEN (the actor) — no card, receipt, or log names the act. Circumstantial only: heavy
  memory-hygiene activity inside the wipe window (MEMORY trim backup 21:46:11, MEMORY.md edit
  22:50:29, dual-index drift same day) and a wrong-source ".bak" made at 01:04:50 by an
  unknown hand 66 s after the ORPHAN_RUN card. Name mechanisms, not seats: verdict stays
  UNPROVEN against any seat.

## 4. Staged recovery (DONE — awaiting operator GO to swap)

`research/corpus_triangulation/invariants_merged_restore.json` — 57 gens / **47,716 counts**
= Sep-6 seal (44,653, covers ≤01:40:13Z) + live post-shrink accrual (3,063 at stage time,
08:49Z→17:00Z). Time ranges do not overlap, so summing double-counts nothing; 0 text
mismatches on the 5 colliding IDs; schema is identical (same writer). Live NOT overwritten.

SWAP COMMAND (operator blessing required; re-merges from the seal + live AT SWAP TIME so
counts accrued after staging are kept; backup-first per law):

```bash
cd /c/Users/foste/Documents/projects/local_sovereign_agent && python -c "
import json, shutil
src='memory/percolator/invariants.json'
seal='memory/seals/2026-09-06T01-40-13/memory/percolator/invariants.json'
shutil.copy2(src, src+'.bak-preswap-20260906')
live=json.load(open(src,encoding='utf-8')); base=json.load(open(seal,encoding='utf-8'))
m=base['invariants']
for k,v in live['invariants'].items():
    if k in m:
        m[k]['count']+=v.get('count',0)
        m[k]['last_seen']=max(m[k].get('last_seen') or '', v.get('last_seen') or '')
    else: m[k]=v
base['false_positives']=max(base.get('false_positives',0), live.get('false_positives',0))
json.dump(base, open(src,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('restored:', len(m), 'gens,', sum(v['count'] for v in m.values()), 'counts')
"
```

Idempotence note: swap is ONE-SHOT — running it twice would double the live-side counts.
The .bak-preswap copy is the undo.

## 5. Prevention (the one-line structural fix)

Make the writer never trust an empty room: in `_load_registry`
(`mag/percolator.py:136-142`), when the file is missing or unparseable, auto-heal from the
newest `memory/seals/*/memory/percolator/invariants.json` (merge, never start empty) — and
make `_save_registry` atomic (write temp + `os.replace`). One line of doctrine: **the
registry is append-only by law; a writer that finds it empty must merge the newest seal
before its first save — replace-not-merge becomes structurally impossible.**

## Falsifier

- "Lost-unique = 0": any invariant ID claimed lost that resolves in no seal and no .bak —
  re-run the union scan (57 IDs total, all in seal 2026-09-06T01-40-13).
- "Wipe was out-of-band": any code path found that writes `{"invariants": {<5 hashes>}}`
  fresh to INVARIANT_REGISTRY — none exists today (grep receipt in tesuji cell mechanism).
- "Counts don't double-count": the 5 shared IDs' seal last_seen ≤ 01:40:13Z Sep 6 and live
  first_seen ≥ 08:49:55Z Sep 6 — disjoint by construction.

---
Run by seat `shrink`, 2026-09-06, for the 11PM Astra salon prep. Tesuji cells
R/incident/invariants/{timeline,mechanism,recovery} — verify PASS 255 cells.
