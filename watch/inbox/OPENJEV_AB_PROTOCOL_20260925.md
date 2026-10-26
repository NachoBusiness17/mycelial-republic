# OPENJEV A/B PROTOCOL + FROZEN TEST SET (2026-09-25)

GO row 9 of the MICKEY17_V2 master fold: "Freeze 30 estate transcript items as a local identical-test-set and A/B the verified openjev qwen3.5-4b-nli-v5 checkpoint against the current judge" (corpus/steal/MASTER_MICKEY17_V2.md:193), scoped per DISPUTED item 7 (same file, lines 146-149). Execution is a night-window lane (family-box law; DAILY_COMPUTE_PLAN_20260924.md:27). This document is the pre-registration: the bars below were filed BEFORE any real arm ran.

## 1. Scoping per the DISPUTED ruling (what is struck, what survives)

Struck, used nowhere in this protocol (DISPUTED item 7, MASTER_MICKEY17_V2.md:146-149): "first runnable open replication" (unverifiable) and "first third-party SemIf number" (contradicted by the earlier-dated vdaular/decider-35b-a3b card, created 2026-09-23). Also not relied on: the "independent 22-model leaderboard benchmarks the whole family" roster claim (DISPUTED item 8, lines 151-154); only its protocol residue survives, which is exactly what this A/B implements: one frozen identical test set, run the challenger on it.

Surviving, verified facts this A/B stands on (openjev README, fetched 2026-09-25, byte-snapshot at watch/openjev_ab/openjev_README_snapshot_20260925.md, sha256 b42d2cf0053bd6a95049f8ce2caf41496b4197e03bafc66a4c777fa1e57bc75b): MIT license, base Qwen/Qwen3.5-4B, checkpoints v5 at 4B/2B/0.8B as subfolders (qwen3.5-4b-nli-v5 = "recommended for typed decisions"), 3-label sequence classification (contradiction / entailment / neutral), self-reported JevBench table 0.814/0.866/0.810 (discount: source-self-measured, never canon), row quote "One forward pass per option, nothing generated" (tier-2 verified byte-exact per DISPUTED item 7).

## 2. What the prep seat did and did NOT do (2026-09-25)

Did: read fleet state; fetched two small text files from huggingface.co (README.md and code/sglang_client.py; both snapshotted with sha256 in section 8); froze the 30-item set; wrote the runner; validated the full pipeline with mocked arms. Spent: 0 API credits, 0 cents.

Did NOT: download the model, run any local inference, call the judge API, or start the SGLang server. Every real number in this A/B is produced by the night window, not by this seat. The only executed runs are the freezer (determinism check) and the runner --selftest (mock arms); selftest numbers are machinery-validation, never model results.

## 3. The two arms

Arm A, the current judge: the estate's lane-runner verifier seat, verbatim. `flash_call` at mag/lane_runner.py:224-285: endpoint https://api.z.ai/api/paas/v4/chat/completions (line 220), keys ZAI_API_KEY_L / ZAI_API_KEY_LITE / ZAI_API_KEY (line 221), model glm-5.3-flash, temperature 0.2, thinking enabled + reasoning_effort low, max_tokens 1536, empty-content rescue with thinking disabled (lines 258-277), LAW-058 pin-check and lite_guard pacing inherited by import. The judge prompt is frozen verbatim in the runner (ARM_A_USER_TMPL in watch/openjev_ab/run_openjev_ab.py); it sees only premise, hypothesis, question, and rubric; output parsed as strict JSON {"supports": "yes"|"no", "confidence": 0.0-1.0, "reason": "<=40 words"}; a parse miss is recorded as a parse-fail row, never guessed.

Arm B, the challenger: AlexWortega/openjev, subfolder qwen3.5-4b-nli-v5, served by the checkpoint repo's own SGLang external-model package (README section "Serve it with SGLang"; tested there with sglang 0.5.19). Wire contract, taken from the repo's own client (snapshot watch/openjev_ab/openjev_sglang_client_snapshot_20260925.py, sha256 b928a143a3502139aba1f3f3668b0a31cae2541ab8b20b2b1d5ab06441e6112d): POST {base}/classify with body {"text": ["Premise: {premise}\nHypothesis: {hypothesis}"]} (the repo's DEFAULT_TEMPLATE), response [{"embedding": [contradiction, entailment, neutral] raw logits}]. Runner speaks this with stdlib urllib only. Pre-registered decision rule: P(yes) = softmax(entailment); label yes iff P(yes) >= 0.5. Both arms receive byte-identical premise and hypothesis strings from the frozen file; the only difference is each arm's fixed framing (arm A's prompt wrapper, arm B's Premise/Hypothesis template).

## 4. The frozen set (identical test set)

File: watch/openjev_ab/frozen30_20260925.jsonl. sha256 8e0b6da1f283a3011b68c8a277d6fac91ec4a865ec56d387d84a339c92cb856d. 30 lines, each a self-contained item: state.premise (the lane row's verbatim source quote), state.hypothesis (the judged claim), question, options ["no","yes"], rubric for both options, prior_judge (the tier-1 verdict + reason, reference only), provenance (lane, checks field/index, lane row index, source URL, alignment ratio), item_sha256. Data fields are verbatim corpus bytes, including corpus punctuation; they are data, not seat prose.

Source corpus: the estate's wave-1 tier-1 judge record, memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/*.checks.json (40 files, 200 judged rows: 101 yes / 99 no, counted this session), joined positionally to the same-dir lane JSONs for premises. Verified this session before freezing: positional alignment (checks index j to lane rows[j]) holds with difflib claim-similarity median 0.94 over all 200 pairs.

Selection rules (pre-registered, implemented in watch/openjev_ab/freeze_frozen30.py): (1) universe = rows with prior supports in {yes,no}, claim >= 40 chars, and a premise available either embedded in the checks row or from a positionally aligned lane row with claim similarity >= 0.60 (universe after rules: 174 items, 78 yes / 96 no); (2) dedupe on whitespace-normalized claim; (3) stratify 15 prior-yes + 15 prior-no; (4) within each stratum take the 15 lowest sha256("openjev-ab-frozen-20260925|lane|field|idx|claim[:120]") hashes; output ordered by hash ascending. Determinism check run this session: two consecutive freezer runs produced byte-identical files (sha256sum shown twice, identical).

Leakage control: prior_judge (verdict + reason) never enters any prompt; the runner builds prompts from state/question/options/rubric only. The frozen file's hash is re-verified at run time; on mismatch the runner refuses to score (mutated-set guard).

## 5. Metrics and escalation

Per run, computed mechanically by the runner into results/<ts>/summary.json: raw agreement arm A vs arm B (of 30), Cohen's kappa, each arm's match rate against the prior tier-1 verdicts (reference, not ground truth), arm B mean and min margin |P(yes) - 0.5|, per-arm latency, infra/parse failure counts. Escalation queue (routed to operator adjudication at the fold gate, per the pair-4 law in MASTER_MICKEY17_V2_20260924.md:125, escalation stays on a tier that can see its own limits): every item with arm disagreement, arm A confidence < 0.70, arm B margin < 0.15, or any arm infra/parse failure.

## 6. Pre-registered bars (filed before the night run)

- adopt_candidate (openjev becomes a verdict-seat candidate, pending operator gate): 30/30 pairable, zero arm-B infra failures, agreement >= 24/30 (0.80), kappa >= 0.60, AND arm B vs prior >= arm A vs prior minus 10pp.
- meter_only (confidence meter beside the flash judge, no gate authority, per the README's own injection warning): zero infra failures and agreement 18/30 to 23/30.
- fail (not adopted for judging; row stays receipt-only): agreement < 18/30.
- infra-fail (the honest empty hand): arm B cannot serve or answers off-contract. The A/B files an infra-failure verdict. No substitute model is swapped in; the DISPUTED scoping is openjev or nothing.

## 7. Execution conditions (night window, family-box law)

Window: 23:00-09:00 local; the runner hard-refuses arm-B calls outside it unless --force (refusal is receipted, nothing scored). Night-window steps: (1) serve the checkpoint on the family box with the repo's own script (README: `hf download AlexWortega/openjev --include "qwen3.5-4b-nli-v5/*" "code/*" --local-dir openjev`, then `bash serve_sglang.sh ../qwen3.5-4b-nli-v5 30000`), (2) run `./.venv/Scripts/python.exe watch/openjev_ab/run_openjev_ab.py --arms both --arm-b-url http://127.0.0.1:30000`. Arm A alone may run any time (`--arms a`), it is API-side, Lite-metered through lite_guard (30 items, roughly 25k tokens total, well under the few-cents law).

## 8. Honest priors and risks (carried from the source's own measured tables)

The checkpoint's weakest measured family is exactly this task's family: JevBench hard-tier judge_hard 0.53 (README table). It is not hardened against prompt injection: one adversarial line drops JevBench accuracy 0.833 to 0.467, so any adopted use sits next to deterministic checks, never instead of them (README "Where it is weak, measured"). v5 trained on train AND test splits of MMLU/ARC/GSM8K/HellaSwag/WinoGrande/GPQA-diamond/CLINC-150/Banking77/ESCI; those benchmark numbers are meaningless for it (README), and our items are estate claims, not those benchmarks, so no contamination path exists for this set. Serve risk: the typed-decision leaderboard run recorded openjev in not_running with "tokenizer files missing" (DISPUTED item 8); if the subfolder will not serve, the infra-fail bar in section 6 applies and the run files honestly.

## 9. Verified vs not run (this seat, 2026-09-25)

Verified by running: freezer twice, byte-identical (sha256sum 8e0b6da1f283a3011b68c8a277d6fac91ec4a865ec56d387d84a339c92cb856d both times); runner --selftest end to end on the real frozen file with a loopback mock /classify server and a patched judge door, zero network and zero inference (watch/openjev_ab/results/selftest/: 30/30 pairable, metrics + escalation + receipt all emitted; mock numbers, not model numbers); py_compile clean on both scripts.

Not run, owed to the night window: any real arm-A call, any real arm-B call, the checkpoint download and SGLang serving itself. The A/B verdict does not exist yet; nothing in this document claims one.

## 10. File manifest

- watch/inbox/OPENJEV_AB_PROTOCOL_20260925.md - this protocol (the pre-registration)
- watch/openjev_ab/frozen30_20260925.jsonl - the frozen 30-item set, sha256 8e0b6da1f283a3011b68c8a277d6fac91ec4a865ec56d387d84a339c92cb856d
- watch/openjev_ab/freeze_frozen30.py - deterministic freezer (rerunnable, must reproduce the file byte-exact)
- watch/openjev_ab/run_openjev_ab.py - the ready-to-run A/B runner (stdlib only; --selftest, --arms, --arm-b-url, --force)
- watch/openjev_ab/openjev_README_snapshot_20260925.md - fetched README bytes, sha256 b42d2cf0053bd6a95049f8ce2caf41496b4197e03bafc66a4c777fa1e57bc75b
- watch/openjev_ab/openjev_sglang_client_snapshot_20260925.py - fetched client source, sha256 b928a143a3502139aba1f3f3668b0a31cae2541ab8b20b2b1d5ab06441e6112d
- watch/openjev_ab/results/ - night-window outputs land here (rows.jsonl, summary.json, receipt.md per run)

Provenance for the ruling and row numbers: corpus/steal/MASTER_MICKEY17_V2.md (GO row 9 at line 193, DISPUTED items 7-8 at lines 146-154); lane row small-agents-week#1 at memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/small-agents-week.json (steal field); judge-lane context watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md; family-box night window watch/inbox/DAILY_COMPUTE_PLAN_20260924.md:27. Prepared by the openjev-ab-prep seat, 2026-09-25.
