# BURN judge-lane-spec, pass c

## Verdict

green

## Evidence

- Emitter code exists: mag/lane_runner.py:305 docstring "The V2 emission path: build the three-axis verdict, run the two-band cascade, trail a GATE_VERDICT_V2 row"; :321 `row = {"ts": _ts(), "actor": f"{lane}-cage", "event": "GATE_VERDICT_V2", ... "verdict": verdict}` appended to trail.jsonl (:324-325). Landed as B2-111 per configs/lanes.yaml:116: "WIRED 2026-09-26 (burn lane B2-111): mag/lane_runner.py load_gate_block reads THIS block on every verdict".
- Zero production callers: repo grep for gate_drop_v2 and _emit_gate_verdict_v2 callers hits only tests/test_lane_runner_cluster.py:344 (`decision, v = lr.gate_drop_v2("t", ...)`), plus load_gate_block tests :271-311. Live gates unchanged: scalar gate_drop trails GATE_VERDICT at mag/lane_runner.py:192-194, called at :733 (research) and :769 (builder).
- Zero emitted rows: `grep -l GATE_VERDICT_V2 queue/lanes/*/trail.jsonl` matches no file across all 12 lane dirs present today.
- cascade_exempt_seats (configs/lanes.yaml:145) read by zero code in mag/, tools/, tests/ (grep: no hits). The rule seat is refused instead: mag/lane_runner.py:237-238 `raise ValueError(f"judge_seat {judge_seat!r} not in gate_verdict_v2.judge_seats")` with judge_seats [local, flash, frontier].
- Row-starved readers confirmed: tools/cascade_falsifier_run.py:49-62 consumes GATE_VERDICT_V2 rows from trails; cluster organ reads the same nested shape (mag/lane_runner.py:541,554).
- Ledger: b2-32 row, "organ dormant on live lanes by design (B2-32 registration: V2 emission is B2-111)"; prior pass row (2026-09-27T05:40:10Z), "cold edge stays the zero-emitter gap".
- Web search (2026-09-27): thin. Closest shapes: "Bayesian Optimal Stopping for LLM Evaluations" (openreview, confidence-based stopping) and a neuro-symbolic deterministic judge that "fires the gate" (sciencevalue). Neither supersedes the frozen two-band cascade; both rhyme with the JEV law already held.

## Steal or Vacuous

Fleet adopts a carrier correction, not a build: the gap is "emitter uncalled", not "no emitter". gate_drop_v2, load_gate_block, build_gate_verdict and apply_cascade are landed and tested; tau is read only from the yaml block (judge never moves its own gate); production callers are absent and zero V2 rows exist, so dormant-until-V2 holds exactly as b2-32 registered. Two deltas owed to the carrier text: (1) the pass-g dual-write patch (gate_drop calls _emit_gate_verdict_v2, dormancy via an emitters flag) never landed; the landed shape is a standalone gate_drop_v2 dormant by caller-absence, and no emitters key exists in the yaml block. (2) cascade_exempt_seats remains a registered-but-unread key; B2-111 callers must route rule seats around build_gate_verdict or exempt them in apply_cascade, else the key stays dead. The cluster organ and the cascade falsifier stay row-starved until the flip, which is governor-owned (writable_by: governor, lanes.yaml:158). No new external steal: web results are snippet-thin and the confidence-stopping shape is already held under the JEV cascade.

## Bibliography

- watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md (full read)
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (full read)
- configs/lanes.yaml lines 108-158 (gate_verdict_v2 block)
- memory/burns/LEDGER.jsonl lines 76, 100, 513, 548, 576 (b2-32, b2-34, judge-lane-spec passes g, h, prior)
- mag/lane_runner.py lines 171-195, 198-326, 360-374, 541-564
- tools/cascade_falsifier_run.py (grep, lines 13-62, 173)
- tests/test_lane_runner_cluster.py (grep, lines 271-344)
- queue/lanes/*/trail.jsonl (grep, zero GATE_VERDICT_V2 matches)
- openreview.net "Bayesian Optimal Stopping for LLM Evaluations"; sciencevalue.udit.es neuro-symbolic playability judge (search snippets only, pages unread)
