# AG1 — Secrets containment (P0, audit finding #1)

**Date:** 2026-09-30 · **Source:** `watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md` finding #1 (7 live API keys committed in tracked `memory/trajectory/steps.jsonl`)
**Laws kept:** names only in this receipt (no key VALUE anywhere); NO history rewrite (operator decision — keys in history stay until rotated by the operator).

## What landed

| # | Move | File | State |
|---|---|---|---|
| 1 | Untrack, keep on disk | `memory/trajectory/steps.jsonl` | `git rm --cached` — staged deletion (`D`); working file untouched (36.6 MB, 37,047 rows) |
| 2 | Ignore | `.gitignore` | `memory/trajectory/steps.jsonl` added under the secrets block; `git check-ignore` confirms |
| 3 | Write-side redaction | `mag/trajectory_step.py` | `redact()` / `redactions()` / `_parse_env_pairs()`; `make_row` scrubs live `.env` VALUES → `<REDACTED:name>` **before** the 400-char excerpt cut and **before** the hash basis (so a key straddling the cut can't land half-live, and `verify` stays self-consistent). Longest-value-first ordering (prefix overlaps can't leave residue). Quotes, `export` prefix, trailing ` #` comments handled; `MIN_SECRET_LEN=8` skips toy values; over-matching is the safe direction. |
| 4 | Commit gate | `tools/precommit_secret_check.py` (new) | Substring match of live `.env` values against **staged blob** content (`git show :path`), same method as the audit. Reuses the hook's parser (one law, no drift). Exit 0 clean / 1 leak / 2 cannot-verify (fail closed: no repo, no parsable `.env`, git failure). `MAG_ENV_FILE` override exists so tests use synthetic fixtures, never real values. |
| 5 | Hook wiring | `githooks/pre-commit` (new) | **Deviation from the tasking (".git/hooks/pre-commit"), on evidence:** `git config core.hooksPath` = `githooks`, which makes `.git/hooks/` inert — a hook file there would be a fake fix under build discipline. No pre-commit existed in either location (verified before writing; nothing overwritten). If `core.hooksPath` is ever unset, re-point this gate. |
| 6 | Tests | synthetic fixture (mktemp, deleted after) | Fake keys only, e.g. `FAKE_AG1_KEY`. All pass: leak staged → exit 1 with name only; clean staged → exit 0; missing env → exit 2; redaction unit cases (quoted/exported/short-skipped/prefix-overlap/cut-order/hash-basis); schema falsifier still PASS; `tests/test_trajectory_bounds.py` + `tests/test_trajectory_rib.py` 3 passed. |

## Evidence

- Parser reads the live `.env`: **52 values** parsed; all audit-named keys present (`ALIBABA-MODEL-STUDIO_1/2`, `VERCEL_KEY`, `ZAI_API_KEY_Pro`, `HERMES_API_KEY_1/2`, …) — names only, values never printed.
- Real-hook smoke: `bash githooks/pre-commit` from repo root, staged set = the `steps.jsonl` deletion only (`--diff-filter=d` excludes deletions) → exit 0.
- Pre-existing (NOT caused by this change — `cmd_verify` and the stream bytes are untouched): `verify` reads 36,118/37,047 rows hash-clean. Filed for the drift lane, out of AG1 scope.

## Not done here (operator calls)

1. **Rotate the 7 keys** — they remain in git history and in the on-disk pre-containment rows of `steps.jsonl` until rotation; redaction only protects future rows.
2. Commit the staged untrack + the new files (left unstaged/unstaged for the operator's own pre-push gates).
3. Scrub-or-keep of historical on-disk `steps.jsonl` rows — `.env` itself also lives on disk, so disk exposure is unchanged; rotation is the real fix.
