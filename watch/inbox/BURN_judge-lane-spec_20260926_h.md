# BURN: judge-lane-spec pass h (2026-09-26)

## Verdict

steal

## Evidence

- Blocker (a) still cold: grep mag/lane_runner.py for `_emit_gate_verdict_v2` = 0 hits. `gate_drop_v2` def sits at :301 with zero call sites; every other GATE_VERDICT_V2 hit (:321 writer row, :433, :541, :554, :563) is the b2-34 reader organ, not an emitter.
- Blocker (b) still cold: grep `cascade_exempt_seats` across mag/, tools/, tests/ = 0 hits. The key exists only at configs/lanes.yaml:145 (`cascade_exempt_seats: [rule]`). lanes.yaml still has no `emitters` key anywhere.
- Blocker (c) still cold: queue/lanes/*/trail.jsonl has v2=0 on all 15 lanes; scalar counts unchanged from pass g (builder 13, research 14).
- Ledger tail (last 5 rows through 2026-09-27T00:08Z): b2-239, b2-151, free-resource-landscape, rsi-harness, b2-wave-fold. No row claims emitter wiring; b2-wave-fold says "nothing wired live".
- Patch anchors byte-true on current bytes: `def gate_drop` :171, scalar `_trail(lane, "GATE_VERDICT",` :192, seat check `if judge_seat not in seats:` at exactly :237, `def gate_drop_v2` :301.
- Web: "Post-generation cascading in production: a cheap model attempts first, output quality is evaluated, and low-quality outputs escalate to a stronger model" (MLflow blog, Sep 7, 2026, mlflow.org). JEV-as-a-Judge recap still the closest research item; no new deployment shape beyond the spec already filed.

## Steal or Vacuous

All three blockers from pass g are still cold: emitter unwired, cascade_exempt_seats registered-but-unread, zero V2 rows trailed. No window wired the emitter since g. The spec's diff was re-verified against current bytes instead of re-filed: every old-line anchor matches exactly, so the pass-g patch stands unchanged and is NOT re-filed (byte-check only, per instructions). One genuine advance since g: b2-34 landed the reader half of the pipeline (_trail_verdicts reads GATE_VERDICT_V2 nested verdict objects at :541-554, cluster_step + detectors wired), so the consumer side is built and waiting on rows no writer emits. The remaining work is exactly the two pass-g edits: the _emit_gate_verdict_v2 call after the scalar trail at :192, and the :237 seat check reading cascade.cascade_exempt_seats, plus the lanes.yaml emitters.gate_drop:false flag. Web adds no new requirement; production cascade practice (MLflow Sep 2026) matches the two-band shape already frozen at B2-32 registration. Verdict stays steal: the spec is complete, byte-verified, and solely blocked on the governor flip.

## Falsifier

Unchanged from pass g: after emitters.gate_drop flips true, the next 100 scalar GATE_VERDICT rows must be accompanied by >= 1 GATE_VERDICT_V2 row; zero V2 at 100 proves the wiring vacuous. Secondary: every V2 row carries judge_seat "rule" and confidence exactly 1.0 on all three axes. New proxy falsifier available now: the b2-34 organ can be replay-tested against the pass-g patch's synthetic V2 rows before the governor flip, proving reader-emitter shape compatibility offline.

## Bibliography

- Read: watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md; watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md; watch/inbox/BURN_judge-lane-spec_20260926_g.md; memory/burns/LEDGER.jsonl (b2-32 :76, b2-34 :100, tail :681-685); mag/lane_runner.py (:84, :171-193, :228-260, :301, :541-563); configs/lanes.yaml :145; queue/lanes/*/trail.jsonl.
- Web (fresh, one search): mlflow.org blog Sep 7 2026 (production cascading); alphaxiv.org (dynamic routing/cascading Aug 2026); rcap.io (JEV recap). Closed.
