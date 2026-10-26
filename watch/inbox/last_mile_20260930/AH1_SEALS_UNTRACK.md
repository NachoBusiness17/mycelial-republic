# AH1 — memory/seals untracked (audit finding #7)

**Date:** 2026-09-30 · **Owner:** last-mile AH1 lane · **Files owned this lane:** `.gitignore`, this receipt.

## Finding

`memory/seals/**` (320 tracked files across 20 seal dirs, each seal containing a copy of the
chain state plus `configs/providers.yaml` — 40,258 bytes of live provider config per seal) was
git-tracked against the estate's own opsec posture (`.gitignore` already holds
`configs/providers.yaml` under "secrets — never commit" since the 2026-08-20 tracked fix).

## Actions (byte-truthful)

1. **Untrack:** `git rm -r --cached memory/seals` → 320 staged `D` entries, working tree
   untouched. Mid-lane, the sibling AG-wave commit `4d5cfd508` ("AG-wave close-out 3/3",
   2026-09-30, message names "seed seal 57/57 restored") committed the shared index and swept
   the 320 deletions in (a transient `.git/index.lock` from that lane was observed and
   cleared on its own; never touched by this lane). Post-landing byte truth:
   `git ls-tree HEAD memory/seals` = **0**; `git log --diff-filter=D -1 -- memory/seals`
   names `4d5cfd508`; the D set in that commit is exactly the 320 `memory/seals/2026-*`
   paths (verified: no non-seal path deleted there). All 20 seal dirs remain on disk
   (`ls memory/seals | wc -l` = 20; newest `2026-09-30T09-02-29` verified present).
2. **Ignore:** `.gitignore` gains `memory/seals/` (line 29, secrets section) with receipt
   comment. Verified: `git check-ignore -v memory/seals/2026-09-30T09-02-29/manifest.json`
   → `.gitignore:29:memory/seals/`. Committed with this receipt as the AH1 pair
   (`.gitignore` + this file were the only staged entries in that commit).
3. **Discoverability pointer:** `state/seal_latest.json` — already written by the seal
   machinery itself (`mag/seal.py` `LATEST`), fresh for today's newest seal, so it was
   **verified, not rewritten** (rewriting with a different schema would break `verify()`).
   Byte-truth confirmed 2026-09-30:
   - `seal_dir`: `memory/seals/2026-09-30T09-02-29` (= newest dir on disk)
   - `manifest_hash`: `9915e930e0c690ca4e1835735e5f542c28a5e69ffdb17a5a1cd7523379b3326d`
     (machinery convention: sha256 of `json.dumps(manifest, sort_keys=True)`, independently
     recomputed from on-disk `manifest.json` → match)
   - file-bytes sha256 of the manifest for cross-checking:
     `7c265651ab1bd5eb09f6f6cc59fe5e44954e6e7e6cf705a6fb9b8e697840ed91`
   - `state/` is gitignored (`.gitignore` lines 36-38), so the pointer is local-only — the
     audit's "commit as receipt pointer" clause does not apply.

## Boundaries

- History left intact (no rewrite) — mirrors the operator's 2026-09-30 trajectory decision;
  the 320 blobs remain in prior commits until an operator history call.
- `state/seal_latest.json` not modified (machinery-owned, verified current).
- This lane's commit contains exactly `.gitignore` + this receipt (verified:
  `git diff --cached --name-status` showed only the pair before commit).

## Refire close-out (2026-09-30, audit finding #7 refired)

The finding refired on the one open clause: the mission text requires a **tracked** pointer —
`state/seal_latest.json` **if `state/` is tracked, else `configs/seal_latest.json` (tracked)** —
and the first pass had stopped at the local-only `state/` pointer. Byte truth at refire:

1. **Steps 1-2 already landed** (no re-work needed): `git ls-tree -r HEAD --name-only |
   grep -c "^memory/seals/"` = **0**; `git ls-files memory/seals` = **0** (index clean);
   `.gitignore:29` holds `memory/seals/` (verified live via
   `git check-ignore -v memory/seals` → `.gitignore:29`). The 320 deletions rode commit
   `4d5cfd508` as filed above.
2. **Step 3 closed this pass:** `configs/seal_latest.json` written (tracked location because
   `state/` is ignored — `.gitignore:40-41`; `git check-ignore configs/seal_latest.json`
   exits 1 = not ignored). Contents: `seal_dir` = `memory/seals/2026-09-30T09-02-29`
   (newest of 20 dirs, independently re-derived by ISO-name sort), `manifest_hash` =
   `9915e930e0c690ca4e1835735e5f542c28a5e69ffdb17a5a1cd7523379b3326d`
   (machinery convention sha256 of `json.dumps(manifest, sort_keys=True, default=str)`,
   recomputed from on-disk `manifest.json` bytes this pass → match), plus the file-bytes
   sha256 cross-check. Path + hashes only; no seal contents, no provider config.
3. **Step 4 verification (this pass):** HEAD = 0 seal paths, index = 0 seal paths,
   `git status --short memory/seals` empty (nothing staged, nothing untracked-and-addable —
   the ignore rule blocks re-entry, so the next commit cannot carry seals); on disk
   `ls memory/seals | wc -l` = 20 dirs, `find memory/seals -type f | wc -l` = 403 files
   preserved. The "staged deletions" check is N/A byte-wise — the D set already landed in
   `4d5cfd508`; the equivalent proof is the HEAD/index zero counts above.
