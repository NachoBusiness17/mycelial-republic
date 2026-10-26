# B2-387 Canary marker_root law pin, 2026-09-26

## Verdict

DECIDED AND PINNED: repair_root is INFORMATIONAL-ONLY, one-snapshot bookmark, and the law now lives in mag/chain_guard.py check() itself. The chosen arm is both halves of the brief's either/or, in the safe direction: (a) ok/state/alarm never key on marker_root vs chain_root (documented in the code at the field), and (b) check output now carries a counted `marker_root_drift` field (0 or 1, report-not-alarm, the house pattern of the corrected 2026-08-25 evidence_lost law in the same function). The marker file bytes are deliberately untouched: B2-82's own falsifier pins verkle_repair_state.json to repair_root e26157d613efd104 / marked_at 2026-09-26T16:39:15Z, so writing an "informational-only" note into the marker would break another lane's seal. Live check this lane: marker_root e26157d613efd104, marker_root_drift 1 (chain has moved past the mark, expected), while the verdict keys only on the real conditions. Live estate observation filed honestly: the chain is currently tip_stale again (tip 5d467c26dd1d6e34 vs chain 63f2c502000ef3a2 over 9,896 rows, dangling_unflagged 0) — a genuine tip-following gap for the boot lanes or a repair pass to settle, NOT caused by this lane and NOT a marker alarm; this lane changed only the check output shape.

## Evidence file:line quotes

- mag/chain_guard.py (post-edit, inside check()): "B2-387 law (2026-09-26): the marker's repair_root is a one-snapshot bookmark of the chain AT MARK TIME, informational-only. Live boot-lane amends legitimately move the chain root minutes after any mark (proof: e26157d613efd104 -> ffee1618af5b1ead -> a7cd0866ba236af7 within two minutes of the B2-82 mark), so marker-vs-chain difference is EXPECTED drift, never a failure: ok/state/alarm never key on it ... The drift is still COUNTED here"; code `"marker_root_drift": 0 if not marker_root or not chain_root else 0 if chain_root[:16] == str(marker_root)[:16] else 1`.
- mag/chain_guard.py pre-existing alarm arms (unchanged): `"ok": not (regression or tip_stale)` and the alarm string keys only on REGRESSION (unflagged dangling) or TIP STALE (tip vs chain) — no marker term.
- Live run `python -m mag.chain_guard check` (2026-09-26 20:2xZ): {"ok": false, "state": "tip_stale", "rows": 9896, "dangling_unflagged": 0, "evidence_lost": 620, "tip_root": "5d467c26dd1d6e34", "chain_root": "63f2c502000ef3a2", "marker_root": "e26157d613efd104", "marker_root_drift": 1, "alarm": "TIP STALE: recomputed chain root does not match the tip bookmark ..."}; exit 0.
- memory/biography/verkle_repair_state.json (read, unmodified): repair_root e26157d613efd104, marked_at 2026-09-26T16:39:15Z, marked_by "chain_guard B2-82", evidence_lost_expected 620.
- B2_82_verkle_reanchor_20260926.md Evidence: "within two minutes of the repair two live boot-lane amends moved the chain root twice (e26157d613efd104 to ffee1618af5b1ead to a7cd0866ba236af7) with the tip following every move" and "The canary's repair_root ... is one snapshot of the repaired chain and already sits behind the live root; ... no re-mark treadmill is required while boot lanes amend"; its Falsifier pins the marker bytes, which is why this lane edited the guard, not the marker.
- Ratchet: `tools/violation_ratchet.py check --changed` PASS, NEW=0 after the edit.

## Work done

- Read mag/chain_guard.py check()/mark() whole, the marker JSON, and the B2-82 receipt; confirmed the drift event chain (three roots in two minutes) from the receipt's own recorded bytes.
- Weighed the two arms: a marker-note edit would break B2-82's falsifier (byte-pinned marker), so the law is pinned in the guard instead; the counted-field arm gives per-check visibility without a re-mark treadmill.
- Edited check(): added the dated law comment and the counted marker_root_drift field; ok/state/alarm paths untouched, so marker_root alone can never produce ok=false (the brief's falsifier is structurally impossible in the new shape).
- Ran check() live, py_compile clean, ratchet PASS NEW=0; added lines em-dash 0 (the one em-dash in check output is the pre-existing alarm string).
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Any future chain_guard check whose ok=false, state, or alarm text is produced by marker_root differing from chain_root ALONE (no regression, no tip_stale) inverts this verdict.
- If marker_root_drift ever feeds an alarm, a gate, or an exit code, the informational-only law is broken.
- The live tip_stale condition observed this lane (5d467c26 vs 63f2c502) is owned by the boot/repair lanes; if it persists unowned, that is the CHAIN_STOP class failure the tip canary exists for, independent of this pin.
- A marker rewrite (new mark) resets drift to 0 for the new snapshot; that is correct behavior, not a regression.

## Bibliography closed

mag/chain_guard.py (check(), mark(), the 2026-08-25 corrected law comment; post-edit whole); memory/biography/verkle_repair_state.json (read-only); watch/inbox/burn_wave_20260926/B2_82_verkle_reanchor_20260926.md (whole); live `python -m mag.chain_guard check` output; tools/violation_ratchet.py check --changed. No web sources. Em-dash count 0 in this receipt and in added lines.
