# ZCODE OPERATING PLAYBOOK — laws we run by

Source: verified against ZCode's own source (deep dig dwfrun-db42e805,
[ZCODE_ENGINE_DIG_20260925.md](ZCODE_ENGINE_DIG_20260925.md), 15/15 paths fact-checked).
This file is OPERATOR DOCTRINE: how to launch, resume, and gate workflows on this harness.
Open-append; add laws only with a path citation.

## Workflow engine laws (we pay tokens to this)

1. **Amend-cache is keyed on byte-identical ask text** (FNV-1a over the instruction
   string only — `dynamic-workflow/src/engine/hash.ts:48`, `imported-cache.ts:51`).
   One wording change = cache miss + everything downstream that interpolates the result
   re-runs. Edit instructions surgically; keep tunable numbers OUT of ask text.
2. **The first workspace write closes the amend-cache for the whole run**; afterward only
   tool-free asks still hit (`scheduler.ts:233-237`). Front-load read-only research asks
   before any mutating ask.
3. **Resuming a failed run replays the failure** — failed asks are journaled and
   re-rejected deterministically (`scheduler.ts:371-381`). To actually re-run a failed
   ask, amend into a NEW run; do not resume.
4. **ProviderStop runs are resumable**: fix auth/quota/config and resume — everything
   settled in the journal is free (`engine.ts:114-122`).
5. **A hung-looking run is transient backoff** (2s→60s, retried indefinitely,
   `workflow-driver-model-failure.ts:81-125`). Watch `run-stalled`/`node-waiting`
   events; do not kill on suspicion.

## Long-session laws (compaction)

6. **The real auto-compact cliff ≈166K tokens on a 200K-window model**
   (200K − 21K output reserve − 13K buffer, `core/src/runtime/compact/policy.ts:6-14`);
   smaller declared output moves it earlier.
7. **Manual `/compact` preserves NOTHING verbatim** — no recent-turn tail
   (`compact-selection.ts:36`). Only compact manually at natural boundaries.
8. **Bash output caps at 30KB inline**, the rest goes to an on-disk artifact — chunk
   enormous outputs on purpose instead of letting the cap do it.
9. **Compact→giant-tool-output→compact ×3 trips a breaker** that fails the turn
   (`turn-loop-state.ts:154-168`). On `CompactRapidRefillError`, find the loud tool;
   do not retry.

## Hook contract laws (our security hooks — Mimosa et al.)

10. **Only exit 2 — or exit 0 with valid JSON `permissionDecision: "deny"` — hard-blocks.**
    A hook that crashes, hangs past its 60s default timeout, or prints schema-invalid
    JSON FAILS OPEN with a `HookRunFailed` event (`configured-runner-callback.ts`,
    `runner.ts`). A blocker must be exactly right or it is a no-op.
11. **Hook stdout/stderr never reach the model.** The model-visible channels are
    `additionalContext` and the deny reason — put guidance there, diagnostics on stderr.
12. **yolo mode bypasses `disallowedTools`** (permission/service.ts:136 runs before the
    check at :149). Hard kill-switches under yolo must be hooks or project deny rules —
    applies to the phone-relay yolo phase.
13. **Any input rewrite is re-normalized and re-permissioned before execution**
    (`permission-input-recheck.ts`) — a hook cannot launder a denied path through an
    edited input, and neither should anything else.

## Estate-side standing law (our own, same spirit)

- Ratchet gate at pre-push (`githooks/pre-push`), register in
  `configs/violation_baseline.json`; debt accepted by name or fixed, never gate-loosened.
- Boot docs stale >7d while the repo has a heartbeat = FAIL (`tools/freshness_check.py`).

## Fifty-wide wave archive law (2026-10-04, a07 operator-owed item made mechanical)

14. **Every Task wave of width >= 5 ends with one archive run, post-wave:** the
    coordinator pipes the per-agent reports (labeled `=== lane ===` blocks or
    `{lane, report}` JSONL, from a file or stdin) through
    `.venv\Scripts\python.exe tools\fifty_wide_archive.py --wave <slug>`; each
    report lands at `memory/runs/fifty_wide/<wave>/agents/<lane>.md` with a
    sha256 row in that wave's `manifest.jsonl`, and re-archiving identical
    bytes is a no-op by sha. The replay pair is the guard's
    `dispatch_log.jsonl` row (pre-flight, `tools/fifty_wide_guard.py`) plus
    the agents dir (post-wave); either half alone cannot explain a count gap,
    and the 2026-10-03 burn wave lost 10 units with neither half on disk
    (owed by watch/inbox/go_wave_20261004/fifty_wide_guard.md section 7).

