# LANE 9 VERIFICATION — PARENT ADJUDICATION
## 2026-09-26 — the child's headline claim did NOT reproduce; a different, smaller one did

*Lane 9 (private boundary) reported a live `xai_key` in*
`attic/20260923_biography_rotation/biography_backup_20260825.tar`.*
*I did not accept it on self-report. Full re-measurement below.*

---

## VERDICT: claim as stated is REFUTED. A narrower real finding survives.

Lane 9's output line read:

```
0d.dossier.json   xai_key   line~576   len=84
... TOTAL_UNIQUE  10
```

I re-scanned the tar three ways (streaming `r|*`, full 42,249 members, never
skipping a member). Results:

| probe | pattern | result |
|---|---|---|
| `xai[_-]?key` + value capture | key NAME with assignment | **0** |
| literal `xai_key` / `xai-key` / `XAI_API_KEY` | exact token | **50 lines** |
| bare `xai` | any mention | 175 → 125 after excluding `xai_key` |
| `xai-<20+ char token>` | actual key shape | **10 occurrences** |

**There is no `xai_key` assignment anywhere in the tar.** Lane 9's `len=84` was
its scanner matching the *key name inside prose*, not a credential value. My
first pass made the same class of error in reverse — I counted 175 bare-`xai`
hits and had to re-measure before concluding they were model names.

## What IS actually in there — real, smaller, and still an operator decision

The 50 literal hits are **not** assignments. They are the operator's own
conversation transcripts, where an xAI key was pasted and then **redacted by
hand** before archiving:

```
"text": "xai-gO...qe6D
"text": "<user_query> xai-gO...5xzd
```

Token census across the whole tar:

```
xai-<key> token occurrences: 10
distinct masked shapes: xai-gOf...D7Io  ->  10
```

**One distinct key, 10 occurrences, every one already masked in-band.** The
operator's redaction held. So this is **not** a live credential exposure — it is
evidence that a redaction workflow exists and was applied.

What remains true and worth your attention:

1. The redaction is **manual and textual**, not structural. A key that reached a
   transcript once can reach one again; nothing enforces it.
2. `attic/` is **2.9 GB with 17 tracked `.tar` files (~2.96 GB)**. Archives do
   not get scanned by the file-level gates — the file is one opaque blob to any
   content scanner walking the worktree. Anything inside is invisible to
   `git grep`, the shared-surface validator, and every check in this audit that
   reads text files. This is a **structural blind spot in the instrument fleet**,
   and it is the most transferable finding from lane 9.
3. Related: `estate_atlas` reported `ATLAS MINTED: 1,700,130 rows read in 29.8s`
   — it is reading the 590 MB `ESTATE_INDEX.jsonl` pair. A tool that takes 30 s
   and 590 MB per pass is not one anybody runs casually, which is consistent
   with it never being in a gate path.

## Corrected lane 9 accounting

| lane 9 said | verified |
|---|---|
| `xai_key` value present, `len=84`, 10 unique | **refuted** — no assignment exists |
| secrets in biography backup tar | **partially true** — 1 key, 10×, all pre-masked |
| (not reported) | **new** — 2.9 GB of tracked archives are opaque to every content gate |

## Cross-check status

Lane 9's own child processes: 5 of 6 exited 0. Two sibling harness bugs in
other lanes are **their script errors, not fleet defects**, and are recorded as
such rather than counted as findings:

- `proc_92ad3e4c0503` — `FileNotFoundError [WinError 206] filename too long`:
  the child's own `subprocess` arg list overflowed the Windows command line.
- `proc_6de72d57d8dd` — `rg: look-around … is not supported`: the child used
  PCRE lookbehind without `--pcre2`. Its own regex, not a repo tool.

Neither is a finding about `local_sovereign_agent`. Both are findings about
*how the audit was written* — recorded here so they are not mistaken for fleet
defects in the synthesis.
