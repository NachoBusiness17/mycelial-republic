# B2-299 receipt (2026-09-26)

## Verdict

LANDED. scripts/index_fold_host.mjs verify now resolves item paths against INBOX_DIR instead of process cwd. From the repo root AND from the drive root, verify reports 0 MISSING over 1061 active items; the cwd trap the brief proved (8+ MISSING lines from root, 0 from watch/inbox) cannot recur, and no runner can be sent chasing phantom truncations. The INDEX die message now carries the cwd and root hint for the env-override case.

## Evidence file:line quotes

- scripts/index_fold_host.mjs:581 (before edit): `const p = it.path;` followed by `if (!existsSync(p))` — it.path is the inbox-relative string normInboxFile produces (line 460 `path: ev.file`), guaranteed relative by the B2-147 writer guard (writerGuard dies on any path with no inbox-relative form), so existsSync resolved it against process cwd.
- scripts/index_fold_host.mjs (after edit): new import `import { isAbsolute, join as pathJoin } from 'path';` and in verify: `const raw = it.path; const p = isAbsolute(raw) ? raw : pathJoin(INBOX_DIR, raw);` with the cause comment naming the observed 8+-MISSING-from-root census.
- scripts/index_fold_host.mjs verify die (after edit): `INDEX.json not present to verify against (cwd=...; INDEX root=...; set INDEX_INBOX_DIR if the inbox root moved)`.
- Post-fix run from repo root, tail: HASH MISMATCH lines for genuinely changed files only (QUEUE.md, B2_465_rebuild_schedule receipt), no MISSING.
- Post-fix run from C:/ (drive root, the strongest cwd-independence case): `verify: 1037 hash-clean, 11 living-ok, 1 living-open, 12 mismatched, 0 missing, 0 living-unverified (of 1061 active items)`. The 12 mismatches are living/appended files whose register events predate later appends (QUEUE.md is appended by every lane today); they are the B2-156 living-law domain, not this defect, and 0 of them are MISSING.
- The brief's cited B2_199 receipt verify evidence (MISSING from root) reproduces no more: the falsifier configuration now returns 0 missing.

## Work done

1. Traced the path shape through the writer guard and fold (inbox-relative by construction at both) so the fix lands at the reader, not by changing the log.
2. Replaced the raw existsSync with the INBOX_DIR join plus an absolute-path bypass; added the cwd/root hint to the INDEX die.
3. Verified behavior change from two different cwds (repo root and drive root) with the counts quoted above; the 12 mismatches were inspected and are genuine post-register appends (living law), not resolution failures.

## Falsifier

Replay: from any directory other than watch/inbox, run `node scripts/index_fold_host.mjs verify`; before this fix every registered file reported MISSING (the B2-199 evidence shape), after it missing counts only genuinely absent files (0 today). If a future edit reintroduces a cwd-dependent resolution anywhere in the verify path, the drive-root run is the detector: any MISSING line from C:/ that is absent from the watch/inbox run is the disease back. The fix itself falsifies if events ever legitimately store absolute paths under a moved INDEX_INBOX_DIR root; the isAbsolute bypass and the new die hint name that case instead of silently hashing the wrong file.

## Bibliography closed

- scripts/index_fold_host.mjs (imports, verify loop, die line; normInboxFile/OUTSIDE_RE/isUnresolved and writerGuard read unmodified)
- watch/inbox/burn_wave_20260926/B2_199 receipt (verify MISSING evidence, pointer from the brief)
- QUEUE.md row B2-299 (line 459 at lane start)
