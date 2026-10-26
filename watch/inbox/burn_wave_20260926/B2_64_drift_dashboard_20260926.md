# B2-64 Drift dashboard (2026-09-26)

## Verdict
Landed. The weekly teleo verdict history is now a served lab-UI panel with a spec filed before the code. dashboard/static/drift_board.html (served at :8765/static/drift_board.html by the existing /static/ handler) renders per pair T1-T6: verdict history over weeks, current corr, live recomputed referent age, and a DRIFTING-days streak counter. Current state: 4/6 pairs DRIFTING; T1 and T3 carry 7-day DRIFTING streaks; T2's referent is 8 days stale. During the lane the board caught a live referent event: B2-65's revival appended 3 release gates and 3 release_milestone events at 13:35Z, flipping T4/T5 referent age from 51d/47d stale to 0d between two runs, which is the live-age column doing its job.

## Evidence
- tools/drift.py:15-16: "ALIGNED metric and referent move together (corr >= +0.5) / DRIFTING weak or no correlation" (source of color and streak semantics).
- dashboard/server.py:633: `if path.startswith("/static/"):` so the page needs zero server.py changes; dashboard/server.py:44-47 `_fleetbar_inject` injects the LAW-060 bar at b"</body>" (byte-verified at the file's end).
- memory/runs/adv_arc_50/teleo_drift_stamps.jsonl: 12 rows hand-read; lines 1-3 are v1 undated (excluded from day math per spec 3.1), lines 4-12 are v2 (W38 T1-T3, W39 T1-T6). Current corrs T1 -0.0271, T2 +0.8839, T3 -0.0759, T4 0.0000, T5 +0.0634, T6 +0.6387; all six match the board render.
- memory/improve/releases/gates.jsonl: 19 rows, last three ts 2026-09-26T13:35:35/46/47Z (the live catch; 16 rows ending 2026-08-06 at the 13:30Z probe).
- tools/violation_ratchet.py check --changed: NEW debt tools/drift_dashboard.py:37 except-pass (sig 59b703f590d8c52a, independently named by lane B2-216); fixed with an explicit hasattr capability check; rerun: "RATCHET: PASS".

## Work done
1. Spec first: docs/DRIFT_BOARD_SPEC.md (surface, column definitions, referent-source table, honesty laws, falsifiers), then code.
2. tools/drift_dashboard.py: ledger loader deriving v1 pair ids from labels, history/corr/streak math, live referent readers incl. the 241 MB events.jsonl regex pass, markdown + HTML renderers, --check freshness mode.
3. First render had a "?" bucket (v1 rows lack pair_id); fixed by deriving from the label; re-render matched the hand-read on all six rows.
4. Concurrent-lane drift absorbed: the stamp tool gained _apply_aging_guard (FRAGILE-ALIGNED) mid-lane; spec section 3 amended and _verdict_color extended so a W40 FRAGILE-ALIGNED row never renders unknown-gray.
5. tests/test_drift_dashboard.py: 5/5 pass. Full suite: 37 failed / 1790 passed / 9 skipped / 1 error in 19:04. My own tail-only pipe truncated the log, so file attribution is partial (zero drift_dashboard failures in what was captured); the 2026-09-14 census was 34 failed.
6. LEDGER row appended 13:54:54Z via json.dumps; self-feeds B2-224/225/226 filed under QUEUE.md '## Open' with max+1 derived at append time (concurrent lanes had reached 223).

## Falsifier
Pre-registered in spec section 5: any current corr or verdict disagreeing with a hand-read of the ledger voids the renderer (none found); T4 referent age under 30d while gates.jsonl ends 2026-08-06 would prove the live recomputation lies (today the flip happened only when real rows landed, the passing case); a W40 stamp not picked up on rebuild fails --check. The serving claim is falsified if :8765/static/drift_board.html 404s on a live lab server; owed: the lab server was not running in this lane, so the URL was byte-verified on disk and via the handler path, not fetched live.

## Bibliography closed
memory/runs/adv_arc_50/teleo_drift_stamps.jsonl; tools/drift.py; tools/drift_pairs_stamp.py; tools/drift_dashboard.py; tools/violation_ratchet.py; tests/test_drift_dashboard.py; docs/DRIFT_BOARD_SPEC.md; dashboard/server.py; dashboard/static/drift_board.html; memory/improve/releases/gates.jsonl; memory/training/events.jsonl; memory/burns/LEDGER.jsonl; watch/inbox/burn_wave_20260926/QUEUE.md; watch/inbox/burn_wave_20260926/B2_05_drift_pairs_20260926.md; watch/inbox/burn_wave_20260926/B2_64_ledger_queue.py. All repo bytes read 2026-09-26. No web sources used, none owed.
