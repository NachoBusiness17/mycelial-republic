# PLAYBOOK AUDIT (f-25) - ZCODE_OPERATING_PLAYBOOK_20260925.md vs ZCode source vs our behavior

Date: 2026-09-28. Item: f-25, flash50 gopher.
Playbook: `corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md` (3,542 bytes, 13 laws + estate-side section).
Source audited: `C:/Users/foste/.zcode/workspace/default/zcode-repo` (shallow clone of https://github.com/zai-org/ZCode).

## Method

Every law was checked by reading the cited file at the cited lines in the clone during this ask
(`sed -n` ranges and `grep -n` per law). Commands run from repo root with the venv python for
estate gates. No fabrication: anything not executed here is marked NOT RUN.

## Question 1: Has the ZCode source changed? NO.

- Local clone HEAD: `git log -1` = `29628c9acdb81b703bbd4080c207a0e7ce5e276e` (2026-09-24, "feat: update v3.14.3"), working tree clean.
- Upstream: `git ls-remote origin HEAD refs/heads/main` returned `29628c9acdb81b703bbd4080c207a0e7ce5e276e` for both, fetched 2026-09-28 during this ask. `git rev-list --count HEAD..origin/main` = 0.
- The steal map (corpus/steal/ZCODE_REPO_STEAL_MAP_20260924.md:3) pins the playbook's verification to this exact commit. Zero drift: playbook and source are still in sync at the byte level of the commit.

## Question 2: Is each law still accurate? 13/13 claims TRUE; 3 citation defects found.

| # | Law (short) | Verdict | Evidence read this ask |
|---|---|---|---|
| 1 | Amend-cache keyed on byte-identical ask text | TRUE, citation exact | `hash.ts:48` is the tail of `fnv1a` (32-bit, basis 0x811c9dc5, prime 0x01000193, over canonicalJson); `imported-cache.ts:51` is `take(seq, hash)` which diverges on hash mismatch; instruction-only coverage proven at `scheduler.ts:125` `const hash = inputHash(instructions)` |
| 2 | First workspace write closes the amend-cache | TRUE, citation exact | `scheduler.ts:233-237` comment: gate closes on FIRST WRITE (driver `askMutating` or live `world.run`); post-close purity at `imported-cache.ts` `takeIfPure` (`stats?.worldToolCalls !== 0` rejects) |
| 3 | Resuming a failed run replays the failure | TRUE, citation exact | `scheduler.ts:371-381`, recorded failure replays `deferred.reject(WorkflowError.fromJSON(recorded.error!))` at :380 |
| 4 | ProviderStop runs resumable, journal work free | TRUE, CITATION IMPRECISE | `engine.ts:114-122` is the inheritedTokens lineage-spend doc (supports only the spend half). The resumability predicate is `isResumableSettlement` at `bootstrap/src/app/dynamic-workflow-run-observation.ts:564-566`: `status === "stopped" && stopReason !== "superseded"`. ProviderStop maps to `stopped(provider)` per `dynamic-workflow/src/engine/errors.ts:37-38` |
| 5 | Hung run is transient backoff, retry 2s to 60s forever | TRUE, citation exact | `bootstrap/src/app/workflow-driver-model-failure.ts:81-125` `scheduleTransientRedrive`, doc comment says unbounded ("无上限"); constants `TRANSIENT_BACKOFF_BASE_MS = 2_000` / `TRANSIENT_BACKOFF_MAX_MS = 60_000` at `workflow-driver-helpers.ts:219-220`; `run-stalled` / `node-waiting` event names exist (`dynamic-workflow-run-roster-events.ts:46`) |
| 6 | Auto-compact cliff ~166K on 200K window | TRUE, PATH WRONG | File is `core/src/compact/policy.ts`, NOT `core/src/runtime/compact/policy.ts` (the playbook's path does not exist; found via `find`). Constants correct at :6-14 (`DEFAULT_COMPACT_CONTEXT_WINDOW = 200_000`, reserves 32_000/21_000, buffer 13_000). Arithmetic verified in code: reserve = `min(maxOutputTokens ?? 32_000, 21_000)` = 21,000 (policy.ts:77-83); threshold = (200,000 - 21,000) - 13,000 = 166,000 (:85-91) |
| 7 | Manual /compact preserves nothing verbatim | TRUE, citation valid | `compact-selection.ts:36` gates the preserve count on `shouldPreserveRecent`; definition at :225: `trigger === CompactTrigger.Auto || trigger === CompactTrigger.Reactive`, so Manual is false and `baseGroupsToPreserve` is 0 |
| 8 | Bash output caps at 30KB inline, rest to disk artifact | TRUE, NUMBER REFINED, CITATION WAS MISSING | `MAX_INLINE_OUTPUT_BYTES = 30_000` at `core/src/tool/handlers/bash.ts:70` (30,000 BYTES, about 29.3 KiB, not 30,720); `maxModelBytes: 30_000` at :482; persisted cap 5 GiB at :71. The playbook carried no path for this law, breaking its own "add laws only with a path citation" rule; citation supplied here |
| 9 | Compact x3 rapid-refill trips a breaker, fails the turn | TRUE, citation exact | `evaluateRapidRefill` at `core/src/runtime/methods/turn-loop-state.ts:154-168`; thresholds `RAPID_REFILL_TOOL_TURN_THRESHOLD = 3` / `MAX_CONSECUTIVE_RAPID_REFILLS = 3` at :21-22; `shouldBlock` at :165; error thrown at `turn-loop.ts:92` and `turn-model-step.ts:765` (`createCompactRapidRefillError`) |
| 10 | Only exit 2 or JSON deny hard-blocks; crash/hang/bad-JSON fails open | TRUE, citations exact | `configured-runner-callback.ts:123-129`: exit 0 parses stdout JSON, exit 2 returns block output, anything else throws; schema-invalid stdout throws at :180-186; all land in the `runner.ts` catch which emits `SessionEventType.HookRunFailed` (fail open) around :216; default timeout 60,000 ms at `runner.ts:42`, enforced at :340-355 |
| 11 | Hook stdout/stderr never reach the model | TRUE | `hooks/output.ts:44-49`: model-visible channels are `additionalContexts` assembled from `systemMessage`, deny `reason`, and `additionalContext`; stdout/stderr ride only sanitized diagnostic previews in hook events |
| 12 | yolo bypasses disallowedTools | TRUE, citation exact | `core/src/permission/service.ts:136` yolo allow (`"mode.yolo"`) precedes the `disallowedTools` deny at :149 in the main flow (both line numbers grep-verified). The phone-relay yolo phase named in the law was NOT probed this ask |
| 13 | Any input rewrite is re-permissioned | TRUE | `core/src/tool/executor/permission-input-recheck.ts:29` `recheckPermissionHookModifiedInput` re-runs `permissionService.checkPermission` on the modified input at :50-54 |

Citation defect summary: 1 wrong directory (law 6), 1 imprecise range (law 4), 1 missing citation (law 8), plus one numeric refinement (law 8: 30,000 bytes, not 30 KiB). No law's operational claim is false at commit 29628c9acdb.

Estate-side section of the playbook: both named gates exist and are wired (`githooks/pre-push` runs `tools/violation_ratchet.py check --changed` and `tools/config_seal.py verify` as blocking steps; 30 PUSH-GATE steps in the hook file). Accurate.

## Question 3: Are we following our own playbook? YES on every observable; 1 check NOT RUN.

Evidence gathered this ask:

- **Hooks follow law 10 exactly.** `.zcode/cli/config.json` registers 4 hook commands (prebuild_gate.py timeout 60; md_record_seal gate and seal, timeout 15 each; trajectory_step.py, timeout 15). `C:/Users/foste/Documents/projects/scripts/hooks/prebuild_gate.py` lines 73-102: allows with `sys.exit(0)`, blocks with `permissionDecision: "deny"` JSON + `sys.exit(2)` (lines 95-101). That is the law-10 contract verbatim: hard-block only via exit 2 or valid deny JSON.
- **The workflow gate is active and registering rows.** `memory/workflows/REGISTRY.jsonl`: 30 rows, 21 PASS / 9 FAIL, 14 unique workflow names, span 2026-09-25T18:52:02Z to 2026-09-27T06:46:25Z (counted by python json parse this ask). The 7 LAW-12 scenario cards exist (`configs/workflow_gate_scenarios/G1_multiplicity.card.json` ... `G7_laws.card.json` + fixtures).
- **Saved workflows exist for amend-not-rewrite reruns.** Project `.zcode/workflows/` holds 10+ saved `.dwf.ts` definitions (mickey17-v2, the-50, the-gala, tree-doctrine-dig, game-dig family, ...). 46 `.mjs` run scripts in project `.zcode/workflow-runs/`.
- **The fan-out shape law is in use right now:** this session is itself a per-item named gopher (item f-25) inside the flash50 burn-reset fan-out.
- **Estate gates enforced, currently red in the by-name-or-fix state** (both commands run read-only this ask with `.venv/Scripts/python.exe`):
  - `tools/violation_ratchet.py check --changed`: "hits=12; registered=11; NEW=1" then "RATCHET: FAIL", NEW hit = `2c7e16bf178da9d0 shell-true: tools/fossil_check.py:73` (subprocess shell=True). A push now blocks until this debt is accepted by name or fixed, exactly as the playbook's estate-side law prescribes.
  - `tools/config_seal.py verify`: "CONFIG-SEAL: FAIL", 3 modified configs vs seal: `improve.yaml`, `mirrors.json`, `violation_baseline.json`.
  - `tools/freshness_check.py`: "FRESHNESS: PASS, boot docs inside the bar" (BOOT_4_7.md 2.8d frozen-ok; CURRENT.md 1.5d ok; START_BRIEF 0.1d ok; HANDOFF 2.4d frozen-ok).
- **Playbook hygiene facts:** the playbook has exactly one commit (`b1d714b02`, the landing) and zero appends since, despite declaring itself open-append. It contains 12 U+2014 em-dashes (byte-counted this ask); informational only, the no-em-dash law binds our outputs, not stored corpus text.

NOT RUN (stated, not guessed):

- Run-level resume-vs-amend behavior: the workflow introspection tool is unavailable in this session ("workflow_introspection_unavailable"), so no live run history could be read to confirm stopped runs are amended rather than resumed. No contrary evidence found on disk; the AFTERPARTY_CLOSE B2-476 contract cited in AGENTS.md remains the governing receipt but was not re-verified here.
- Law 12's phone-relay yolo phase: the law's source claim is verified; whether the phone-relay still runs a yolo phase was not probed this ask.

## Recommended appends (operator, per the playbook's own open-append rule; not applied by this census item)

1. Law 4: add the exact predicate citation `dynamic-workflow-run-observation.ts:564-566` (stopped and not superseded = resumable) alongside engine.ts.
2. Law 6: correct the path to `core/src/compact/policy.ts` (constants :6-14, threshold math :77-91).
3. Law 8: append the citation `core/src/tool/handlers/bash.ts:70` and tighten "30KB" to "30,000 bytes".
