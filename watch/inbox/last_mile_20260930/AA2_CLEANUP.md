# AA2 — estate junk cleanup tool (dry-run only)

**Landed:** 2026-09-30 · **Owner lane:** last_mile AA2 · **Mode: DRY-RUN ONLY** (no commit, no deletion of real files — the mission authorized building + proving the tool, not firing it)

## What landed

- `tools/estate_cleanup.py` (new) — known-junk enumerator + guarded cleaner. Default is a dry-run report; `--apply` is the only deleting path and it fail-closes (post-apply re-enumeration; any survivor exits 1). `--root` for arbitrary trees, `--json` for machine-readable output. Junk list is the triage lane's list, hardcoded as `JUNK_SPECS` with per-category provenance.
- `tests/test_estate_cleanup.py` (new) — 5 tests, all green under `.venv\Scripts\python.exe -m pytest` (Python 3.11.15, pytest 9.1.1): fixture junk tree enumerated exactly (paths, bytes, categories, nested `sub/nul` and lookalike names spared); default run touches nothing; `--apply` removes fixtures and spares non-junk; JSON totals match fixture math; Windows reserved-name mechanics proven on a fixture (literal `nul` created via `\\?\` prefix, deleted via `cmd /c del \\.\C:\path\nul`, `os.path.exists` still True afterward — the device shadow, which is why all existence checks go through scandir).

## The `nul` mechanics (why the special case)

`C:\dir\nul` always resolves to the NUL device on Win32, so `os.remove`/`os.path.exists` both lie for the literal file. Enumeration therefore reads directory-entry truth (`os.scandir` + cached stat — verified against the real 51-byte file), and deletion shells out to the device-path syntax `cmd /c del /f /a \\.\C:\Users\foste\Documents\projects\local_sovereign_agent\nul` exactly as mandated.

## Real dry pass (run 2026-09-30, repo root, nothing touched — verified: 0 git deletions, all 26 paths still present)

| category | paths | files | bytes |
|---|---|---|---|
| tmp-gopher-dig (`tmp_gopher/`, vendored llama.cpp/amdgpu staging) | 1 | 14 | 2,844,530 |
| path-bug-dumps (`UsersfosteAppData*`) | 16 | 16 | 4,471,976 |
| s218-build-debris (`_s218_*`, rogue endpoint-map debris) | 4 | 4 | 278,246 |
| sweep-llama-scratch (`sweep_llama*.json`) | 2 | 2 | 189,908 |
| braid-scratch (`braid_test.out`) | 1 | 1 | 1,926 |
| stealth-check-scratch (`stealth-tools.check.txt`) | 1 | 1 | 637 |
| nul-reserved (`nul`) | 1 | 1 | 51 |
| **TOTAL RECLAIMABLE** | **26** | **39** | **7,608,872 B (7.26 MiB)** |

Per-path breakdown lives in the tool output itself; rerun with `.venv\Scripts\python.exe tools\estate_cleanup.py`.

## Git state of the junk (matters before any real --apply)

- Untracked: `nul` only (`?? nul`) — deleting it is git-invisible.
- Tracked and clean: everything else (all 16 `UsersfosteAppData*`, all 4 `_s218_*`, `braid_test.out`, `sweep_llama.json`, `sweep_llama2.json`, `stealth-tools.check.txt`, and all 14 files inside `tmp_gopher/`). A real `--apply` produces working-tree deletions that need a follow-up `git rm`-style commit to finalize — that is an operator call, not this lane's.

## Provenance (the triage lane's receipts)

- `tmp_gopher/` + root scratch classification: `watch/inbox/burn_reset_20260927/flash50/todo-census.md` ("scratch or vendored copies of third-party sources, so none is estate debt").
- `_s218_*` "rogue ... unaccounted build debris — scan before they merge": `watch/inbox/burn_reset_20260927/work/lib-belady-1966_hermes.md`; the banked receipt superseding them is `watch/inbox/burn_reset_20260927/flash50/s2-18.md`.
- `nul` reserved-name hazard: `watch/inbox/SECRET_GATE_BUILD_20260927.md` (root cause: literal `nul` files) + `watch/inbox/audit_20260926/LANE4B_UNVERSIONED_RISK.md` (reserved-name guard).

## Out of scope (observed, not touched)

The root also carries sibling path-bug debris this mission did not list — `%CD%/`, `%TEMP%/` + 28 `%TEMP%*` files/dirs, `.tmp_dig*`, `.pytest-*` dirs — same disease, different pattern; extending `JUNK_SPECS` is one tuple away when an operator wants them.
