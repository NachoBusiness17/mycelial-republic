# B2-60 judge-independence sweep - 2026-09-26

## Verdict

Lens: VisualPrompter Appendix L same-VLM bias (B2_09_prompt_uplift_20260926.md:13, first-hand): "the use of the same VLM for both the internal optimization feedback and the final evaluation may introduce potential bias." Result: REGISTRY.jsonl is clean (19 rows, all deterministic regex gate output); 8 rule-judge paths TOLERATED; 3 same-VLM DEFECTS (quorum self-vote tally, workflow reviewer seats, constitutional filter critic); 2 TOLERATED with conditions; fix named per defect.

## Evidence

- D1 mag/quorum_window.py:377 `for chair in p1s:` every P1 returner votes on every addition; :398-399 `denom = len(p1s)` / `need = math.ceil(2 * denom / 3)`; :404-405 yes/no tallies include the author; the fold stores the author; the tally never reads it. DEFECT: a producer votes toward the 2/3 bar on its own addition. Mitigations: :298 flag, rotation falsifier. Fix: exclude the author chair from votes and denominator per addition (~4 lines in the p4 loop); author vote = ABSTAIN.
- D2 workflow reviewer seats are same-session-model: grep of .zcode/workflows/*.ts finds zero subagent_model. the-gala.dwf.ts:295-296 `agent("midnight-reader", { system: "Fresh reader. You have not seen this work. Judge the archive...` ; mickey17-v2.dwf.ts:328-329 and the-50.dwf.ts:181 same shape; REVISE drives a repairer (:302-306, :337-342). "Fresh reader" is context freshness, not weight independence: the exact Appendix L condition. Mitigation: tier-2 is mechanical (the-gala :342 grep byte-check); tier-1 entailment (:251) stays same-VLM. Fix: judge agents get subagent_model on a different provider family; tools/workflow_gate.py G3 (:55-59) gains an independence marker; REGISTRY G3 ok rows certify steering presence, not independence.
- D3 mag/ghost.py:1970 `cr = filter_response(output, tier="T2", model="deepseek")` critiques output with a hardcoded critic; the producer model is a variable (ghost.py:1125); mag/constitutional_critique.py:200 `model: str = "deepseek"`, :111 "the model reviews its own". CritiqueResult records the critic, never the producer. DEFECT: producer-critic family equality is unenforced and unrecorded. Fix: thread producer_model into CritiqueResult; on family match refuse model critique, fall back to local heuristics marked same-family-refused.
- T1 configs/lanes.yaml:114-118 "The judge never moves its own gate ... writable by the governor only"; :121 judge_seats [local, flash, frontier] share the worker ladder; :140-143 both_orders_debias only under contested_merit_only; :144 cascade_exempt_seats [rule]. TOLERATED as frozen registration (:116 "No module reads these keys yet"); add judge-seat != builder-seat by governor amend before B2-111 wires it.
- T2 tools/compaction_eval.py:51-52 GEN_MODEL == JUDGE_MODEL == "qwen2.5-3b-instruct"; one model picks keep/reject (:113), writes the summary arm (:62), takes the exam (:300); final hit is substring; sanity_gate :182 pre-gates. TOLERATED (symmetric arms, rule grade); JUDGE_MODEL is a misnomer (examinee); log judge/producer identity in JSON.
- T3 tools/wandr_selfeval.py:292 deterministic STUB judge; :37-38 "WANDR uses an LLM judge here; swap judge_record() when the BURN judge lane populates". TOLERATED now; the swap must name judge_model and reject judge_family == producer_family.
- Rule judges clean: mag/lane_runner.py:190-193 GATE_VERDICT (field/ttl/anchor only); tools/workflow_gate.py :45-79; tools/steer_compare.py:174-192; tools/ghost_tournament.py:142,178; mag/arena_bench.py:8,238; mag/run_worth.py:287+; configs/conductor_eval.yaml; configs/improve.yaml.

## Work done

Whole-file reads: lanes.yaml, workflow_gate.py, lane_runner.py, quorum_window.py, wandr_selfeval.py, conductor_eval.yaml, QUEUE.md, B2_08 receipt. Targeted: compaction_eval, constitutional_critique, ghost, three workflow scripts, improve.yaml. All quotes grep -n verified against bytes; zero subagent_model in all four scripts; 19 REGISTRY rows gate-regex-only.

## Falsifier

F1: apply the D1 exclusion to memory/runs/salons/quorum_* VERDICT.md; no PASSED flip means the author vote was never pivotal; D1 downgrades. F2: rerun one fold with the reviewer on a different provider family; matching strikes and REVISE rate vs same-model runs downgrade D2. F3: log producer_model 30 days of ghost filter calls; zero same-family events closes D3 as absence-filed.

## Bibliography closed

This lane, from bytes: files under Work done plus QUEUE.md. Lens: arXiv 2506.23138v2 Appendix L sentence carried from B2_09_prompt_uplift_20260926.md:13 (first-hand fetch by that lane 2026-09-26; not refetched here). Context: B2_08_judge_lane_20260926.md, B2_58 receipt.
