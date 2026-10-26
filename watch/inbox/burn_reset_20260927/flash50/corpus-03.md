# CORPUS-03: ZCode operating playbook audit vs current ZCode source (2026-09-28)

Item: corpus-03, flash50 gopher. Ask: read `corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md`,
verify every law against the current ZCode version, answer "have any changed", and mine tonight's
sessions for new laws. Mesh note: sibling item f-25 banked `playbook-audit.md` (same flash50 dir)
against the same clone earlier tonight; my independent reads agree with all 13 of its verdicts, and
this file adds what f-25 did not have: one substantive law correction it missed (law 6 gloss),
one correction to f-25's own citation, and the new-laws-from-tonight answer (its Q3 was compliance,
not new laws).

## Version pin: has the ZCode source changed? NO.

Commands run this ask against `C:/Users/foste/.zcode/workspace/default/zcode-repo`
(shallow clone of https://github.com/zai-org/ZCode, branch main):

- `git log -1 --format="%H %ci %s"` = `29628c9acdb81b703bbd4080c207a0e7ce5e276e 2026-09-24 14:49:06 +0800 feat: update v3.14.3`
- `git fetch origin main` (ran live 2026-09-28, network OK): FETCH_HEAD = same hash.
- `git rev-list --count HEAD..origin/main` = `0`.

So the clone IS the current ZCode version (v3.14.3, commit 29628c9) and it is the same commit the
playbook was verified against. Zero upstream drift: no law is invalidated by a source change.

## Per-law verification (13/13 operational claims TRUE; 3 citation defects, 1 inverted gloss)

Every verdict below is from reading the cited file in the current checkout during this ask
(Read tool with line ranges + `grep -n`). No live workflow/compact/hook behavior was executed
(see NOT RUN).

| # | Law (short) | Verdict | Evidence read this ask (current checkout) |
|---|---|---|---|
| 1 | Amend-cache keyed on byte-identical ask text | TRUE, citations exact | `dynamic-workflow/src/engine/hash.ts:48` is `inputHash` = fnv1a over canonicalJson (:34-45, basis 0x811c9dc5 / prime 0x01000193); `imported-cache.ts:51` `take(seq, hash)` diverges on `entry.inputHash !== hash` (:54); instruction-only coverage proven at `scheduler.ts:125` `const hash = inputHash(instructions)` |
| 2 | First workspace write closes the amend-cache | TRUE, citation exact | `scheduler.ts:233-237` is now the design comment: "现在关门的是**第一笔写入**" (driver `askMutating` or a live `world.run` closes the gate; turning live alone does not, with the measured 6-of-50 fanout loss); post-close purity at `imported-cache.ts:70-79` `takeIfPure` rejects `entry.stats?.worldToolCalls !== 0` (:73) |
| 3 | Resuming a failed run replays the failure | TRUE, citation exact | `scheduler.ts:363-382` `settleCachedAsk`; failed branch :371-381 ends `deferred.reject(WorkflowError.fromJSON(recorded.error!))` at :380; comment :372 names the try/catch-replay rationale |
| 4 | ProviderStop runs resumable, journal work free | TRUE, CITATION IMPRECISE | Current `engine.ts:114-122` is the `inheritedTokens` doc (supports only the "spend includes all predecessors" half). The stop path: `bootstrap/src/app/workflow-driver-model-failure.ts:51-55` (policy `stop` -> `host.sink.stopRun(providerStopError(...))`, comment "可恢复" = recoverable). The resumability predicate: `bootstrap/src/app/dynamic-workflow-run-observation.ts:572-574` `isResumableSettlement` = `status === "stopped" && stopReason !== "superseded"` |
| 5 | Hung-looking run is transient backoff, 2s->60s, forever | TRUE, lines exact, path moved | `bootstrap/src/app/workflow-driver-model-failure.ts:81-125` is exactly `scheduleTransientRedrive` (Retry-After first :90-91, unbounded per doc comment :79 "无上限"); constants `TRANSIENT_BACKOFF_BASE_MS = 2_000` / `TRANSIENT_BACKOFF_MAX_MS = 60_000` at `workflow-driver-helpers.ts:219-220`, jitter [0.5,1] at :223-226 |
| 6 | Auto-compact cliff ~166K on 200K window | TRUE number, PATH WRONG, GLOSS INVERTED | File is `core/src/compact/policy.ts`, NOT `core/src/runtime/compact/policy.ts` (playbook path does not exist; found via `find`). Constants at :6-14: `DEFAULT_COMPACT_CONTEXT_WINDOW = 200_000` (:6), `PREFLIGHT_AUTOCOMPACT_OUTPUT_RESERVE_TOKENS = 21_000` (:10), `AUTOCOMPACT_BUFFER_TOKENS = 13_000` (:12). Math (:67-88): effective = window - reserve; reserve = `min(maxOutputTokens ?? 32_000, 21_000)` (:75-82); threshold = effective - 13_000 (:84-88) = 166,000 |
| 7 | Manual /compact preserves nothing verbatim | TRUE, citations exact | `compact-selection.ts:36` `baseGroupsToPreserve = split.shouldPreserveRecent && ... ? 1 : 0`; `shouldPreserveRecent` at :225 = `trigger === CompactTrigger.Auto \|\| trigger === CompactTrigger.Reactive`, so Manual gets 0 preserved groups (:42-44) |
| 8 | Bash output caps at 30KB inline, rest to disk artifact | TRUE, NUMBER REFINED, CITATION WAS MISSING | `core/src/tool/handlers/bash.ts:70` `MAX_INLINE_OUTPUT_BYTES = 30_000` (30,000 BYTES, not 30,720); resultBudget strategy `"artifact"` :480-491; persisted cap `MAX_RUNTIME_PERSISTED_OUTPUT_BYTES = 5 * 1024 * 1024 * 1024` at :71. The playbook named no path for this law, breaking its own open-append rule; citation supplied |
| 9 | Compact->giant-output->compact x3 trips a breaker | TRUE, citations exact | `turn-loop-state.ts:21-22` `RAPID_REFILL_TOOL_TURN_THRESHOLD = 3` / `MAX_CONSECUTIVE_RAPID_REFILLS = 3`; `evaluateRapidRefill` :154-168, `shouldBlock` at :165 |
| 10 | Only exit 2 or valid JSON deny hard-blocks; else fail open | TRUE, citations exact | `configured-runner-callback.ts:123-129`: exit 0 -> parse stdout, exit 2 -> `createExitCodeBlockOutput`, anything else throws `ToolExecutionFailed` "Hook process failed" (:131-145); exit-2 deny synthesis PreToolUse `permissionDecision: "deny"` at :195-211; schema-invalid stdout throws :177-190; `runner.ts:42` `defaultTimeoutMs ?? 60000` (enforced :340-355); the runner catch emits `HookRunFailed` and CONTINUES (fail open) |
| 11 | Hook stdout/stderr never reach the model | TRUE | `core/src/hooks/types.ts:23-31` `HookCallbackDiagnostics` doc: diagnostics only enter lifecycle events, "不会...暴露给模型"; model-visible channels are additionalContext + deny reason (callback wiring :148-163 attaches previews to events only) |
| 12 | yolo bypasses disallowedTools | TRUE, citation exact | `core/src/permission/service.ts:136-138` yolo allow (`"mode.yolo"`) precedes the `disallowedTools` deny at :149-156. Phone-relay yolo phase NOT probed this ask |
| 13 | Any input rewrite is re-normalized and re-permissioned | TRUE | `core/src/tool/executor/permission-input-recheck.ts:24+` `recheckPermissionHookModifiedInput` re-runs `permissionService.checkPermission` on `modifiedInput` (:50-55), deny short-circuits :65-70 |

Citation defect summary (playbook fixes needed): law 6 wrong directory (`runtime/compact/` ->
`compact/`), law 4 imprecise range (engine.ts:114-122 is the spend half only; add the
`isResumableSettlement` predicate), law 8 missing citation (add `bash.ts:70`, tighten 30KB to
30,000 bytes). No law's operational claim is false at 29628c9 EXCEPT the law 6 gloss:

**NEW finding tonight (not in f-25): law 6's parenthetical "smaller declared output moves it
earlier" is INVERTED by the current code.** From policy.ts:71-82: reserve =
`min(maxOutputTokens ?? 32_000, 21_000)`, threshold = 200_000 - reserve - 13_000. A model
declaring maxOutput < 21K gets a SMALLER reserve and therefore a HIGHER threshold (e.g. declared
8K -> threshold 179K), i.e. auto-compact fires LATER, not earlier. Any model declaring >= 21K
pins the reserve at 21K -> 166K regardless. The dig (ZCODE_ENGINE_DIG_20260925.md operator note)
carries the same inverted phrasing, so this is an inherited error, not drift.

Cross-checks against f-25 (`playbook-audit.md`): same clone, same 13/13 TRUE, same law 6 path and
law 8 findings. Corrections to f-25's own cites from my reads: `isResumableSettlement` is defined
at `dynamic-workflow-run-observation.ts:572-574` (f-25 said :564-566; :562-568 is
`isResumableRecord`), and its law 8 `bash.ts:71` 5 GiB cite is corroborated exactly.

Estate-side section of the playbook: `githooks/pre-push`, `tools/freshness_check.py`,
`configs/violation_baseline.json` all exist (ls run this ask). Gate states tonight were measured
by f-25, not re-run by me (ratchet FAIL 1 new debt, config-seal FAIL 3 configs, freshness PASS).

## New laws from tonight's sessions (candidates to append, per the playbook's open-append rule)

1. **The [1301] bell laws (TONIGHT, 2026-09-28T20:58:41Z).** Source read this ask:
   `watch/inbox/panda_panel_recovery_20260928.md`. A 4-lane ractor panel lost its window when the
   synthesis turn was struck by GLM-5.3-Flash `[1301] unsafe/sensitive content`
   (retryable=false; explicitly "No 429, no quota event, no subscription ghost"). Laws banked
   there: (a) receipt before speech: file every lane's pack before the synthesis turn runs;
   (b) verdict, not vocabulary: a synthesis voice reads a tuned-for lane's verdict one level up
   and never re-carries the lane's vocabulary; (c) 1301 is a diagnostic, not a moral: route
   around, do not tune content to the gate. Engine mapping to playbook laws 4/5: a deterministic
   model-side stop is stop-class (`workflow-driver-model-failure.ts:51-55` ->
   stopped(provider), resumable per law 4's predicate), but resume replays the same ask bytes, so
   1301 re-rings on the same glass; the survival move is amend with rewritten vocabulary.
2. **Estate-side: the driving ladder is now code-as-law (TONIGHT).** Source read this ask:
   `memory/rib/RIB_DRIVING_LADDER_20260928.md` (minted from three operator corrections on the
   09-27/28 night): ONLY Hermes ($180 Nous credits) is funded, Anthropic keys UNFUNDED; free
   stealth lanes are sensing-only, banked as findings, never as done/trusted work; verification
   climbs to the funded tier; remember-before-running (load ribs + state before building any
   mechanism). Mirrored in AGENTS.md DRIVING LADDER entry.
3. **Estate-side: fence-owner law (2026-09-28, tonight's working-tree AGENTS.md edit).** Every
   fence section carries a `# fence-owner:` comment naming owner and receipt; receipt
   `watch/inbox/fifty_wide_20260917/FW11_fence_owners.md` (verified exists this ask).
4. **Pre-tonight but absent from the playbook (post-landing ZCode dispatch-shape laws, receipts
   verified tonight):** (a) fan-out width law: workflow children get `maxAttempts 0`
   (zero adapter retries; a 50-wide workflow-child dig 429/1302-storms the account) while Task
   agents ride `maxAttempts 11` + driver backoff and measured clean at widths 3/6/10/12;
   sources: `corpus/steal/TETHERED_LINK_STEAL_20260925.md:17` ("workflow-child requests get
   `maxAttempts 0, maxRetries 0`"), `watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md:65-66,84`
   (storm table; "Workflow children inherit zero absorption"); (b) max-concurrency standing law:
   5 workflows x max_concurrency 10 = 50 children plus burn cron plus offpeak ran clean for
   hours; the first rate-limit contact at that shape is a HOLD signal, not a width cut;
   source: `watch/inbox/ENVELOPE_50W_HIT_20260926.md:3`.

## NOT RUN (stated, not guessed)

- No live ZCode workflow, compaction event, or hook verdict was exercised this ask; all 13
  verdicts are source reads at the pinned commit plus a live `git fetch`. No run of this session
  exercised amend-cache or hook behavior to observe the laws in vivo.
- Law 12's phone-relay yolo phase: not probed (same limit f-25 declared).
- Estate gates (ratchet / config-seal / freshness): not re-run by me; tonight's numbers are
  f-25's, cited above.

## Recommended appends (operator call; not applied by this item)

1. Law 4: add `isResumableSettlement` at `bootstrap/src/app/dynamic-workflow-run-observation.ts:572-574`.
2. Law 6: fix path to `core/src/compact/policy.ts` (:6-14 constants, :67-88 math) and REPLACE the
   inverted gloss: a declared maxOutput below 21K RAISES the threshold (compacts later); >= 21K
   pins 166K.
3. Law 8: append `core/src/tool/handlers/bash.ts:70` and say 30,000 bytes.
4. Add the four new-law groups above (1301 bell; driving-ladder rib; fence-owner; dispatch-shape
   pair) with their receipt paths.
