# B2-50 Missing-triage sweep (2026-09-26)

## Verdict

LANDED. The INDEX.json vs index_events.jsonl diff surfaced exactly 3 files with broken triage, and all 3 are now triaged in the event log: FRONTDOOR_MISSING_JOINS_20260901.md (class UNPROVEN since 9/01, never classified) refiled as STEAL; RESOLUTION_J1_CAGE_TO_MAG_ROUTE_20260901.md (UNPROVEN since 9/01) refiled as RECEIPT; LAW13_EXPERIMENT_ON_ABSENCE_20260926.md (registered 12:55Z under an absolute Windows path that never folds into INDEX) invalidated and re-registered on the bare inbox path as DOCTRINE. INDEX now folds to 972 active items, 0 UNPROVEN, 0 missing files.

## Evidence with file:line quotes

- watch/inbox/index_events.jsonl:25: `"op":"register","file":"/board/inbox/FRONTDOOR_MISSING_JOINS_20260901.md","class":"UNPROVEN","purpose":"Provenance unknown (foreign agent session); classify before use"` (seq 25, 9/01). Line 26 is the identical UNPROVEN row for RESOLUTION_J1_CAGE_TO_MAG_ROUTE_20260901.md. Neither was ever re-registered.
- watch/inbox/index_events.jsonl:3060: `"file":"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/LAW13_EXPERIMENT_ON_ABSENCE_20260926.md"` (md-record-seal autoseal). Fold-exact replay in Python (watch/inbox/burn_wave_20260926/B2_50_diff2.py) gave computed active 972 vs INDEX 971, the delta being that absolute-path row: OUTSIDE_RE only strips watch/ prefixes, so `C:/Users/...` folds as a phantom inbox item that INDEX (folded 12:47:37Z) predates.
- Byte verification: current sha256 of FRONTDOOR (5C9AE92FBACA...) and RESOLUTION_J1 (F01B59CD6E43...) match their 9/01 registrations byte for byte; LAW13 sha C3FCEBFAE496... matches event line 3060 and the LAW-13 entry in memory/law/registry.json, whose `file` pointer reads `watch/inbox/LAW13_EXPERIMENT_ON_ABSENCE_20260926.md`.
- Alternatives eliminated against the log: the 3 malformed rows (94-96, workspace_snapshot tarball) were already recorded (line 98 note) and repaired (line 908 `op":"repair"`, 9/21); INDEX.md and SHARED_SURFACE_CONTRACT.json on disk unregistered is deliberate (lines 1381/1379, "retire: self-referential derived file", patrol law 20260922); the LINKS/QUIET_RADAR/cathedral_v1 invalidates (2553/2551/2549) are superseded by later bare re-registers (2904/2936/3001), so the fold is self-consistent there.

## Work done

Built two diff probes (B2_50_diff.py naive, B2_50_diff2.py fold-exact, both in burn_wave_20260926/); read all 3 target files in full; ran `invalidate` x1 and `add` x3 as INDEX_WRITER=zcode-b2-50-burn-20260926 from watch/inbox cwd (bare paths, the only form that updates bare INDEX items); rebuild + verify: `968 hash-clean, 4 mismatched, 0 missing (of 972 active items)`; UNPROVEN census now 0. Files triaged: FRONTDOOR is an archivist.artifact.v1 self-steal join-gap map (J1-J6); RESOLUTION_J1 is a workboard.resolution.v1 closure receipt (mag-sovereign:8001 verified live); LAW13 is the LAW-13 standing rule text. One anomaly observed, not caused by this lane: scripts/index_fold_host.mjs was edited by a concurrent lane mid-pass (one transient crash, rerun clean with new outsideDropped telemetry).

## Falsifier

Run `cd watch/inbox && node ../../scripts/index_fold_host.mjs verify`: it must report 972 active, 0 missing, and the UNPROVEN census must stay 0. A rebuild that drops the 3 items, reverts their classes, or resurrects the `C:/Users/...` LAW13 phantom falsifies this receipt. The pre-existing 4 hash mismatches are outside this lane's scope and tracked as B2-145/146 below.

## Bibliography closed

watch/inbox/INDEX.json; watch/inbox/index_events.jsonl (lines 4, 25, 26, 90, 94-99, 908, 1379, 1381, 1411-1416, 2549-2554, 2904, 2936, 3001, 3054-3061); scripts/index_fold_host.mjs; memory/law/registry.json (LAW-13); memory/trajectory/steps.jsonl (sess_71c96bdc steps 11:06-11:13Z); watch/inbox/burn_wave_20260926/QUEUE.md; the 3 triaged files in full; state/fuel/unindexed_batch.json.
