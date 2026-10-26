# PORT WAVE 2026-10-07, LANE P6: three small ports (receipt)

Seat: port-order lane P6 from the day-7 mine fold. Repo tree at execution:
working tree shared with sibling lanes (their modified files are theirs; this
receipt claims only the files listed under each port). Python: .venv\
Scripts\python.exe throughout. No git commit (lane law). No em-dashes added
(diff-grep verified: 0 added U+2014 in both edited code files).

## Port 1: QUANT A/B SPEC AMEND

File: watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md (new).

The owed qwen2.5:7b Q4_K_M-vs-q8_0 A/B is amended, not fired. Debt pins
verified on this tree: the probe list at
watch/inbox/frontier_olm_2026-10-03/lens/burns.md:118-123 (probe 5 at :122),
re-owed at watch/inbox/frontier_olm_2026-10-03/DIGEST.md:224 and :274. The
day-7 card's pointer to burns lines 97 and 218 did not verify to the quant
debt (those lines are the agent-limit-retry find row and the counts-law
bullet); the drift is named in the amend file. The four-pinned-choices rule
comes from watch/inbox/frontier_olm_2026-10-07/steal/
quantization-compression.md steal 1 (arXiv 2610.07781). "changes direction
across prompts and evaluation targets" is byte-present at
state/arxiv/2026-10-07/2610.07781v1.txt:6.

Amended legs:
at-least-5 prompts per task; full-pipeline success as the only deployment
verdict; matched-task deltas diagnostic only; strict-parse success banked as
its own channel with the Qwen-flat prior stated up front; per-task spread
reported; GGUF artifact hashed plus conversion toolchain pinned; plus the new
promotion gate blocking any single-prompt quant score from entering
configs/lanes.yaml pins (janitor pins :31-33, worker pin :37, envelope :28 -
all read this sitting). Citation lint on the file: ok, 13 anchors, 0 blocking,
0 warns.

## Port 2: MARKER-PENALTY CHEAP LEG

Files:
- configs/marker_penalty_profile.json (new): mined candidate set. Census run
  this sitting over the EMPTY_REASONING receipt surfaces (memory/runs/
  hermes_burn/*.jsonl + driver.log, memory/behavioral/animals/*.jsonl,
  watch/inbox/model_garden/FABLE1.md, RIB_MODEL_GATES_20261001.md): actually
  26, therefore 12, however 3, wait 2, maybe 1, hmm / alternatively /
  on-the-other-hand 0. Zero-hit hedge-class candidates carried per the
  finetuning card's class definition; receipt census is banked beside the
  markers. Note: a python json-parse walk this sitting over every hermes_burn
  ledger read zero rows with empty_reasoning true (instrument: json.loads row
  walk, moment 2026-10-07); the mined
  signals come from the ramble/receipt surfaces above, and that zero is
  stated, not smoothed over.
- mag/marker_penalty.py (new, 85 lines): load_penalty_profile + 
  penalty_logit_bias. Mechanism cited in the module docstring:
  watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.md:31
  (training-free token-specific penalties recovered up to 9.8 accuracy points
  while cutting CoT length up to 51.3 percent), staged as the cheap leg by
  watch/inbox/frontier_olm_2026-10-07/steal/finetuning-adaptation.md find 1.
- mag/llama_cpp_bridge.py (edited): optional penalty_profile constructor arg
  and --penalty-profile CLI flag (new main()), OFF by default; the
  _completions_payload helper keeps the no-profile body byte-identical to the
  pre-profile bridge (test-pinned). Ratchet cure this sitting: the first
  inline version breached the 400-line cap (ratchet NEW
  015abeaa0503ee62 at 446 lines), cured by the mag/marker_penalty.py
  extraction, not by baseline acceptance; final bridge is 399 lines.
- tests/test_marker_penalty_profile.py (new, 10 tests): profile loads and
  validates; malformed bodies raise; default payload has no logit_bias and is
  byte-identical to legacy; profile adds logit_bias and nothing else;
  token_id form; constructor accepts path/dict/None; fallback generation
  unchanged with profile armed; CLI accepts the flag on and off.

Wire honesty: logit_bias string-token acceptance on the estate's
llama-cpp-python 0.3.36 server is UNMEASURED; the flag arms an experiment and
certifies no wire shape (stated in code and profile).

## Port 3: BLIND-SWEEP PLACEMENT LAW

File: tools/workflow_gate.py (edited, ADDITIVE; G8-width card, stop-cert and
FIRE_LEDGER shapes untouched).

- Module docstring: dated 2026-10-07 clause, the G2 PLACEMENT LAW: interagent
  findings feed happens at review; blind sweeps within a pass are legal;
  cross-pass pooling only after review. Reference implementation named:
  .zcode/workflows/olm-mine.dwf.ts:272-289 (blind sweep asks), :342-349
  (independent confirms), :396-403 (pooling at the steal round beside the
  reviewer). Source: watch/inbox/frontier_olm_2026-10-07/steal/
  swarm-orchestration.md steal 1 (ArcticSwarm).
- WARN-level soft row on the G2 check (same soft family as the G6 dated stamp
  and the G3 judge-model stamp): G2_CROSS_POOL_RE + G2_REVIEW_STEP_RE grep
  approximation over comment-stripped code text; a cross-pass pool token
  before the first review step, or with no review step at all, soft-warns
  with the placement reason. The 0/1/2 exit contract is unchanged.
- Calibration this sitting: the reference mine carries zero pool tokens (grep
  verified), and no scenario fixture carries one, so the live shape and the
  LAW-12 suite stay clean.
- tests/test_g2_placement_law.py (new, 6 tests): reference shape clean,
  pool-before-review warns soft not hard, pool-with-no-review warns,
  review-then-pool legal, warn never enters the failed set, comment-only pool
  token does not warn.

## Gates

- Scenario suite: `.venv\Scripts\python.exe tools\workflow_gate.py check
  --scenarios configs\workflow_gate_scenarios` -> "9 cards validated read-only
  (no registry row written)", pass_control all 8 gates clean.
- Reference implementation smoke: gate check --no-register on
  .zcode/workflows/olm-mine.dwf.ts -> PASS, digest c7c95efcd512, G1-G8 all ok,
  no WARN.
- Ratchet (`tools/violation_ratchet.py check --changed`): this lane's files
  contribute ZERO NEW. The run still prints FAIL with NEW=2, both in
  tools/code_execution.py (file-too-long :652, except-pass :446) - a sibling
  lane's in-flight file, not touched by this lane; plus non-blocking GROWTH
  lines for tools/hermes_burn.py (+124, sibling) and tools/workflow_gate.py
  (+84, this lane's additive law text; cure is the gate owner's named
  re-acceptance or a split, not done unilaterally here).
- Full pytest: run on the stable post-refactor tree; result recorded in the
  final report line of this lane. Targeted sets this sitting:
  tests/test_marker_penalty_profile.py 10 passed,
  tests/test_g2_placement_law.py + tests/test_workflow_gate.py +
  tests/test_scenarios_gate_hook_pin.py 26 passed,
  tests/test_selfplay_orchestrator.py + tests/test_inference_budget.py 47
  passed.
- Citation lint: QUANT_AB_SPEC_AMEND.md ok (0 blocking, 0 warns). Other
  changed-tree lint findings (memory/zknot/LATEST.md PHANTOM-NUMBER x2,
  DAWN_REPORT warns) are sibling files, not this lane's.

## Owed / not done here

- The A/B itself is still UN-RUN; this wave amends its instrument only.
- deepseek-r1:1.5b q8_0 twin pull (sibling probe) untouched.
- logit_bias string-token wire acceptance on 0.3.36: unmeasured.
- tools/workflow_gate.py GROWTH +84 and the two code_execution.py NEW rows
  belong to their owners; no baseline rows were accepted by this lane.
