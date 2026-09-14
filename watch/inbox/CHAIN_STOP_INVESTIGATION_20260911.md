# CHAIN STOP INVESTIGATION — why knotting froze at 2026-09-06 23:09:38Z, and the one-command re-arm

**Commission:** wave dig, 2026-09-09 (machine clock; the wave brief said Sep 11 — the box
disagrees: `date` = Wed Sep 9 12:45 EDT / 16:45 UTC). Read-only except this file.
Absorbed first per protocol: `watch/inbox/SILENCE_DOSSIER_20260911.md`,
`watch/inbox/RECORD_POOL_CENSUS_20260911.md`. Relay folded in:
`SURGERY_FORENSICS_20260911.md` (event-dating vs ts-dating), kpi.jsonl tip-decode lane.

**Verdict up front:** the recorder is NOT dead — the CHAIN is. The append path has been
gated shut since Sep 6 23:09:38Z by the chain's own integrity gate, because
`memory/biography/verkle_tip.json` carries a root that does not match the chain. Every
knot fold since then has been silently refused and silently swallowed. One command
re-arms it (proposal only — not run).

---

## 1. The stop, confirmed (both dating views)

- Last chain row: index 7376, `ts 2026-09-06T23:08:56.829250Z`, root
  `8bd588968c0bbfaf…`, session `01a078fb-…`. `verkle_chain.jsonl` mtime Sep 6 19:09
  local (= 23:09Z; box is UTC-4).
- ZERO knot files in `memory/biography/knots/` (28,874 files) carry a content date past
  `2026-09-06`, and every one of them — including August files — has mtime Sep 6 19:09.
  Per the forensics relay: ts-dating and event-dating agree here, because the stop is
  total — kpi `n_leaves` is frozen at 7377 and no leaf file exists at all after Sep 6,
  so there are no hidden event-dated rows. (The ts-vs-event divergence applies to the
  AUG window, not to this one.)
- Chain rows per ts-day: Aug 31: 1909, Sep 1: 575, … Sep 5: 99, Sep 6: 249, then nothing.
- Unlike the Aug 16-31 silence (chain dark, leaves flowing), this time BOTH the leaf
  writer and the anchor stopped together — because they are the same code path
  (`mag/verkle_knot.append_verkle_knot` writes leaf + pointer + chain row in one
  locked transaction).

## 2. The recorder is alive and throwing knots into a closed door

- `docker ps`: 3 containers UP (mag-sovereign since 2026-09-08T09:45Z, mag-worker,
  mag-redis). Old names (mag-control-plane etc.) do not exist in docker at all — the
  fleet was rebuilt; that is context, not the cause.
- Ghost janitor quest trail `memory/runs/ghost/autonomous_trail.jsonl` — quests SPAWNED
  every single day through the freeze: Sep 6: 49, Sep 7: 72, Sep 8: 39, Sep 9: 34
  (last 2026-09-09T16:37:38Z, minutes before this investigation). Each quest ends with
  a fold-to-verkle (`mag/ghost.py:1504 append_verkle_knot(dossier)`).
- `logs/kpi.jsonl` (457 MB, continuous since Jul-21) rows every ~50s report
  `n_leaves: 7377`, `tip_root: a57b50f312470e42` — the summarizer faithfully echoing a
  tip that has not moved since Sep 6. Biography side-files (registry, index,
  knot_timeline, dossiers) still update today — the estate is alive around a frozen
  chain.

## 3. Root cause — tri-stated

**SUPPORTED — the integrity gate is closed by a poisoned tip file.**
`_append_verkle_knot_unlocked` (`mag/verkle_knot.py:613-618`) refuses to extend the
chain unless `_verify_chain_consistent()` passes two checks. Reproduced read-only with
the byte-exact merkle implementation:

- Check 1 — last row root vs recomputed root over all 7,377 leaf hashes:
  `8bd588968c0bbfaf…` == `8bd588968c0bbfaf…` — PASSES. Every one of the 7,377 rows
  verifies against its prefix root (first bad row: none). The chain itself is sound.
- Check 2 — tip file root vs recomputed: tip says `a57b50f312470e42…` — **FAILS**.

So `_verify_chain_consistent()` returns `(False, "tip root mismatch (tip a57b50f312470e42
vs recomputed 8bd588968c0bbfaf)")`, `append_verkle_knot` returns
`{"ok": False, "error": "refusing to extend an unverified verkle chain"}` — and every
caller discards that return. Ghost's fold wraps it in `except Exception: pass`
("best-effort — never block the cycle", `mag/ghost.py:1524`). 145+ folds on Sep 7-9:
zero knots, zero errors, zero log lines. The gate did its job; the silence did the rest.

**How the tip got poisoned (SUPPORTED sequence, UNPROVEN final writer):**
- `watch/KNOT_AT_CLOSE_20260906.json`: the W1 knot-at-close backfill ran 22:54:56Z,
  chain at 7370 rows, `tip_proof_ok: true`, root `4661d71f…` (matches the
  `.bak-orphanlane-20260906T2254xxZ` / `.bak-batch-20260906T230013Z` backups — healthy).
- 7 more rows appended 7370 → 7377 through 23:08:56Z — appends worked fine.
- At **23:09:38Z** an amend pass rewrote the chain (row index 3549, session
  `mag-agent-orc-t0dd5a9c81c`, carries ts 23:09:38Z) and the tip was written with root
  `a57b50f3…`, `n_leaves 7377`, `last_filename 2026-08-11_1620_biography_…`,
  `last_leaf_hash 3099388c…` — a hash that lives at chain index 3549, not at the end.
  The tip describes a TRANSIENT mid-batch state (root matches neither the current chain,
  the backups, nor any sorted ordering — tested all three). The batch died or was cut
  off mid-flight, leaving tip and chain permanently divergent. The very next fold hit
  the gate and the freeze began. All 28,874 knot files + tip + chain share mtime
  23:09Z — the batch's fingerprint.

**DISPUTED — "the recorder died again."** As a recorder-death claim: DISPUTED. The
quest loop, summarizer, dossier writer and container fleet are all running right now.
What died is the chain APPEND path — and it is not crashed but REFUSING, by design,
because a 494-byte pointer file contradicts the ledger.

**UNPROVEN:** (a) which exact process performed the 23:09:38Z amend pass and wrote the
bad tip — no receipt names it (candidates: the knot_at_close/lane batch family; the
`bak-batch` suffix suggests a batch consolidate); (b) whether kpi/other readers key any
behavior off the poisoned tip beyond echoing it.

## 4. Side findings

- The janitor's own self-heal quest (`mag/ghost.py:1462`) tells the worker to run
  `python -m mag.verkle_audit --fix` — **that flag does not exist** (`verkle_audit.py`
  accepts --full/--synth/--reconcile/--no-reconcile/--backfill/--dry). The one organ
  that could have auto-healed this was firing at a nonexistent switch, and its
  `verkle_stale` signal never interrupted the `except: pass` wall.
- The whole failure was INVISIBLE by design: a failed fold returns a dict nobody reads.
  One line of structural fix (needs a build, not this pass): in `mag/ghost.py` log the
  fold result when `not result.get("ok")`, and add tip-vs-chain divergence to
  `mag/chain_guard.py`'s canary checks so the next poison trips an alarm in minutes,
  not days.

## 5. Re-arm proposal (EXACT commands — for operator GO; nothing was run)

The sanctioned repair already exists: `repair_tip_if_consistent()`
(`mag/verkle_knot.py:564`) — verifies the last row against the recomputed root (which
PASSES today), then atomically rewrites the tip under the single-writer lock. It cannot
repair a broken chain, only a stale/wrong tip — which is exactly our case.

From the repo root (`C:\Users\foste\Documents\projects\local_sovereign_agent`), one line:

```
python -c "import shutil,datetime as dt; shutil.copy('memory/biography/verkle_tip.json','memory/biography/verkle_tip.json.bak-poison-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')); import sys; sys.path.insert(0,'.'); from mag.verkle_knot import repair_tip_if_consistent; print(repair_tip_if_consistent())"
```

(Backup-first law honored: tips the old tip aside before the repair touches it.)

Expected: `{'ok': True, 'repaired': True, 'n_leaves': 7377, 'root': '8bd588968c0bbfaf…', …}`.

Verify after (read-only): the next janitor quest fold (quests spawn every ~1-3 min per
the trail) should land chain row index 7377; or run
`python -c "from mag.verkle_knot import _verify_chain_consistent as v; print(v())"` →
`(True, 'chain consistent (7377 leaves)')`.

Alternative surface, if GO is given inside the cage instead:
`docker exec mag-sovereign python -c "from mag.verkle_knot import repair_tip_if_consistent; print(repair_tip_if_consistent())"`
(/app/memory is bind-mounted rw to the host chain — same files).

Risk: LOW. The repair refuses to touch anything if the last row disagreed with the
recomputed root; today it agrees. The poisoned tip is preserved in the .bak. No chain
rows are modified.

## 6. Sources / cards absorbed

- `watch/inbox/SILENCE_DOSSIER_20260911.md` — Aug engine-death shape; the "anchor breaks
  first" pattern; leaf/chain split anatomy reused here.
- `watch/inbox/RECORD_POOL_CENSUS_20260911.md` — kpi.jsonl + ghost trail as the
  continuous pools; kpi tip_root field is what first matched the poison.
- Relay: `watch/inbox/SURGERY_FORENSICS_20260911.md` — event-dating law (checked: no
  divergence for the current stop); `logs/kpi.jsonl` tip-decode lane (their tip_root
  sequence will show `a57b50f3…` frozen from Sep 6 onward — consistent with this card).
- Code: `mag/verkle_knot.py` (gate 613-618, verify 529-549, repair 564-601, append
  606-751), `mag/ghost.py` (quest loop 1324+, fold 1481-1525, janitor quest 1451-1469),
  `watch/KNOT_AT_CLOSE_20260906.json`, `memory/runs/ghost/autonomous_trail.jsonl`,
  `state/lifecycle_latest.json`, `state/mag_launch.json`.

*Compiled 2026-09-09 by the chain-stop lane. Read-only except this file. All counts
reproducible from the cited paths; merkle replication used the byte-exact
`_merkle_root` from `mag/verkle_knot.py:147`.*
