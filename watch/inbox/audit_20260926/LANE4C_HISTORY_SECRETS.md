# LANE4C — git-HISTORY secret scan

**Question:** are there secrets that exist ONLY in historical commits (deleted from the working tree but still recoverable from git objects)?

**Answer: YES.** Two HIGH findings under rule `XAI-KEY` exist only in history. Their paths are gone from the working tree and absent from `HEAD`, but the blobs stay reachable from **19 commits** (union; 37 + 18 per blob), spanning 2026-08-01 to 2026-09-14.

Audit only. Nothing was fixed, rotated, purged, or rewritten. Read-only git plumbing (`rev-list`, `cat-file`, `ls-tree`, `log`, `ls-files`).

## 1. History-only secrets (the deliverable answer)

| # | rule | sev | blob sha | token len | entropy | commits | first commit (date) | last commit (date) | path at finding |
|---|------|-----|----------|-----------|---------|---------|--------------------|-------------------|------------------|
| 1 | `XAI-KEY` | high | `aadba40d727d5dab0961cb20645b2303127863e1` | 84 | 5.41 | 37 | `cd2f8e6a520d` (2026-08-01) | `261c895ad3e4` (2026-09-14) | `memory/biography_backup_20260825/019f4d15-dee6-76d3-9e1f-cc5dff56720d.dossier.json` |
| 2 | `XAI-KEY` | high | `140c5e6e72e6bd67b81227f2ad094f5bbcb8db8f` | 84 | 5.41 | 18 | `cb26bc2cdcb0` (2026-08-25) | `261c895ad3e4` (2026-09-14) | `memory/biography_backup_20260825/biography/residual/019f4d15-dee6-76d3-9e1f-cc5dff56720d.json` |

Both rows are the **same credential** (identical sha256 fingerprint, token length 84, entropy 5.41). Verified absent from the tree two ways: `git ls-files --error-unmatch` returns rc=1, and `git cat-file -e HEAD:<path>` returns rc=128.

Each blob is reachable at more than one historical path:

- `aadba40d727d` -> 37 commits across 3 path(s):
  - `memory/biography_backup_20260825/019f4d15-dee6-76d3-9e1f-cc5dff56720d.dossier.json`
  - `memory/biography_backup_20260825/biography/019f4d15-dee6-76d3-9e1f-cc5dff56720d.dossier.json`
  - `memory/portable_bags/bag-20260727T214646Z/memory/biography/residual/019f4d15-dee6-76d3-9e1f-cc5dff56720d.json`
- `140c5e6e72e6` -> 18 commits across 1 path(s):
  - `memory/biography_backup_20260825/biography/residual/019f4d15-dee6-76d3-9e1f-cc5dff56720d.json`

**Commit range carrying history-only findings:** `cd2f8e6a520d67553d3e9c1486b6703a75646fec` (2026-08-01) through `be3ffa520a21418da3b3d72a61fc6459cb084c18` (2026-09-14).

## 2. Premise correction — the tar is NOT hand-redacted

The brief stated `attic/20260923_biography_rotation/biography_backup_20260825.tar` contains HAND-REDACTED key references only, not live values. **That is wrong, and it is the single most important finding of this lane.**

Tar members are invisible to `git grep` and to any working-tree scan, so a second pass extracted and scanned every member with the same imported rule table. The archive carries a live-shaped `xai-` credential:

- token length **84**, strictly alphanumeric after the 4-char prefix
- shannon entropy **5.41** bits/char (well above the 4.3 floor)
- **no redaction marker** on any of its 10 occurrence lines (no REDACTED / MASKED / `***` / `xxxx` / ellipsis)
- it survives the gate's own `ALLOW_RE` suppression, which is exactly what a hand-redacted token would NOT do
- 10 occurrences across 10 members, all the same fingerprint `fp_2fc97957ab09`
- sha256 fingerprint **matches** the two history-only loose blobs above

So the exposure is not confined to unreachable history: **the same live-shaped key is still inside a tracked tar in the current tree.** Deleting the loose history paths would not remove this credential.

Archive pass totals: 36 candidate blobs, 34 archives read, **369,722 members** extracted (709,443,753 bytes), 69923 members carrying findings.

## 3. `memory/tls/lan.key` — present in history, but NOT history-only

- path `memory/tls/lan.key`, rule `PRIVATE-KEY-BLOCK`, severity **critical**
- **present in 318 commit trees**, `799ddb6feaad` (2026-08-19) through `e73b60c54aa3` (2026-09-27), `HEAD` included
- introduced once by `799ddb6feaad` on 2026-08-19; the blob was never modified after that
- still tracked in `HEAD` and present in the working tree: **history-only = False**

Confirmed live in the tree, so it is a present-tense exposure, not a history artifact.

## 4. Provider API key prefixes

| prefix | rule | rows |
|--------|------|------|
| `xai-` | `XAI-KEY` | 34 |
| `sk-ant-` | `ANTHROPIC-KEY` | 0 |
| `gsk_` | `GROQ-KEY` | 0 |
| `sk-or-v1-` | `OPENROUTER-KEY` | 0 |
| `AIza` | `GOOGLE-API-KEY` | 0 |
| `ghp_` | `GITHUB-TOKEN` | 0 |
| `glpat-` | `GITLAB-PAT` | 0 |

Only `xai-` fired. Zero rows for Anthropic, Groq, OpenRouter, Google, GitHub and GitLab shapes across all 66,204 blobs and every tar member.

There are **two distinct** xai- credentials (two sha256 fingerprints):

- fingerprint `fp_98980f98afe1` in `memory/trajectory/steps.jsonl` — **live in the working tree**, 4 commit(s) contain it, first `d575bc1686b4` (2026-09-14). This is the token-shaped credential at `memory/trajectory/steps.jsonl:1994` already on record.
- fingerprint `fp_2fc97957ab09` in the two history-only blobs and the tracked tar (section 1-2).

## 5. All CRITICAL/HIGH findings, by rule

| rule | severity | rows | note |
|------|----------|------|------|
| `AWS-SECRET-40` | high | 363 | 40-char base64 runs that clear the 4.3-bit entropy floor across 25 paths; never blocks by gate design |
| `XAI-KEY` | high | 34 | 2 distinct credentials; 2 rows are history-only |
| `TELEGRAM-BOT` | high | 32 | 32 rows in `memory/trajectory/steps.jsonl`; live in tree |
| `STRIPE-KEY` | high | 10 | 10 rows across `boe*.html`, `corpus/tmp_enoch/*.htm`, `module_audit.ipynb` |
| `PRIVATE-KEY-BLOCK` | critical | 1 | `memory/tls/lan.key` |

Total CRITICAL/HIGH rows: **440** (deduped on blob+rule+line) out of 374,117 rows scanned at all severities.

Medium/low volume is dominated by the gate's own generic shapes: `ENT` (entropy pseudo-rule) and `ENV-ASSIGN`. These are report-tier and never block; they are the documented 48k-hit noise floor the S3 entropy filter addresses.

## 6. Coverage and runtime

| measure | value |
|---------|-------|
| objects enumerated (`rev-list --objects --all`) | 71,314 |
| non-blob objects (trees/commits/tags) skipped | 4,940 |
| blobs >10 MB skipped | 170 |
| **blobs scannable (content-pass input)** | **66,204** |
| **blobs content-scanned** | **58,475** |
| blobs skipped as binary (gate's own sniff) | 7,728 |
| **coverage of scannable set** | **100%%** (complete, not extrapolated) |

Method: `rev-list --objects --all` -> size filter through `cat-file --batch-check` -> content read one persistent `cat-file --batch` pipe per worker. Bounded batches, checkpointed to disk every 250-500 blobs, no giant list ever held in memory.

Runtime: base pass 417s, 12-way sharded pass 204s wall (12 of 16 cores), tar-member pass 685s, commit attribution 102s. **Total wall ~1408s (23 min).**

Attribution walked all **580 commits** with `ls-tree` to place every one of the 131 target blobs in an exact commit set — no sampling, no extrapolation.

## 7. Constraint compliance

- **No secret value is printed anywhere.** This receipt and the JSON carry path, blob sha, commit sha, rule id, severity, token length, shannon entropy and a 12-hex sha256 fingerprint. No token body, no masked head, no last-4 tail.
- The prior attempt's failure mode (raw `xai-` values into a transcript) is the exact thing this lane was built to avoid; the detector reuses the repo's own rule table but replaces the gate's `mask()` head-mask with a hash so no fragment can leak.
- Read-only: no remediation, no rotation, no history rewrite, no working-tree edit.
- No full test suite or long walk was run; this was git plumbing plus tar extraction.

## 8. Two harness bugs I hit and fixed (recorded so the numbers are trustworthy)

1. **Shard partitioning was a no-op.** The first 12-way fanout used `(idx - start) % nshard != 0` instead of `!= shard`, so all 12 workers redundantly scanned shard 0's slice and produced 12 byte-identical output files. Caught because the known `lan.key` PRIVATE-KEY-BLOCK finding was absent from the results. Re-ran after the fix; the corrected run reports 66204 blobs and does find `lan.key`.
2. **Import side effect.** A pass-2 module imported the pass-1 scan script, which would have re-run the entire 66k scan on import. Caught before running it; pass 2 was rewritten against a shared rules module instead.

A third harness failure was inherited and avoided by design: the first attempt died on a 64,816-blob enumeration held in memory, so every pass here streams and checkpoints.

## 9. Bottom line for the integrator

- **History-only secrets exist.** Rule `XAI-KEY`, severity high, 2 findings, reachable from 19 commits (cd2f8e6a520d..be3ffa520a21). Deleting the file does not delete the blob.
- **The tar is not the safe artifact the brief assumed.** Same credential, tracked, current tree, invisible to `git grep`.
- `lan.key` is real, committed, and still in `HEAD` (318 commit trees).
- `memory/trajectory/steps.jsonl` carries a second distinct xai- credential, live.
- Removing any of these from the working tree changes nothing about history; the blobs stay in the object store and in the sibling bare repo `Mag-backup.git`.

Machine receipt: `memory/audit_20260926/lane4c_history.json`
