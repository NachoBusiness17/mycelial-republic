# PACK — SECRET SCAN GATE (borrow, don't build)

**From:** L2-Hermes (operator seat) · **To:** any seat willing
**Date:** 2026-09-26 · **Status:** NOT AUTHORIZED YET — build only on operator GO

> **Read this first.** The operator asked whether this already exists. **It does.**
> A previous seat proposed building it three times before checking. Do not repeat
> that. Everything below is measured from bytes, not estimated.

---

## 0. THE ONE-LINE VERDICT

There is no missing scanner. There is a **tracked-but-unwired** scanner, and it
**already caught a real committed private key once**. The job is ~40 lines of
wiring, not a new tool.

---

## 1. EVIDENCE (already measured — do not re-derive, re-verify cheaply)

| Fact | How it was established |
|---|---|
| `githooks/pre-push` has **no** secret gate | `grep -niE 'secret\|leak\|credential\|redact' githooks/pre-push` → empty, run twice |
| The scanner exists | `watch/inbox/burn_wave_20260926/B2_73_secret_scan.py`, 9,533 bytes, 28 rules |
| It is **UNTRACKED** | `git ls-files --error-unmatch` fails on that path |
| It ran once, manually | Beat row `ts=2026-09-26T21:13:04Z` in `watch/inbox/SECRET_SCAN_BEAT.jsonl` |
| It found `lan.key` | `PRIVATE-KEY-BLOCK: 1` (the only `critical` tier rule) |
| The weekly task never fired | `MagSecretScanWeekly`, Ready+Enabled, last result `267011` |
| 2,294 tests exist; hook budget | pre-push measured at **15.7s** |

### Measured rule counts from the one real run

```
AWS-SECRET-40      48,427   <-- 80% of ALL findings. noise. see S3.
ENV-ASSIGN         11,744
GENERIC-KEYASSIGN     180
OPENROUTER-KEY        28
GROQ-KEY              28
XAI-KEY               18   <-- includes a CONFIRMED LIVE key, see S5
DEEPSEEK-KEY          16
OPENAI-CLASSIC        14
STRIPE-KEY             7
CONNSTRING-CRED        4
AWS-ACCESS-KID         1
GOOGLE-OAUTH-AQ        1
JWT-TRIPLE             1
PRIVATE-KEY-BLOCK      1   <-- memory/tls/lan.key, tracked since August
TOTAL             60,470
```

---

## 2. WHAT TO BORROW (do not rewrite any of this)

| # | Piece | Where | Take |
|---|---|---|---|
| B1 | 28 rules + severity tiers | `B2_73_secret_scan.py:28-57` | **Copy the rule table verbatim.** Do not write new patterns. Do not "improve" the regexes. |
| B2 | Redaction concept | `scripts/sanitize_dossiers.py:20-34` (`KEY_PATTERNS`) | A human-redacted token like `xai-gO...qe6D` is **not a finding**. Borrow the shape-exemption idea. |
| B3 | Named-acceptance pattern | `configs/violation_baseline.json` | The repo's own way of saying "seen, accepted, named." Do NOT copy its 933 debts. |
| B4 | Enforcement point | `githooks/pre-push` | Already 9 ordered gates, 2 hard-blocking. Add yours as #10. |
| B5 | Beat/alert pattern | `scripts/secret_scan_weekly.py` | Weekly row + prepend alert to `memory/attention.md`. **Fix its bloat first (S4).** |

**Do NOT import `KEY_PATTERNS` into the gate.** That import path leads to
`corpus_packer.py`, which is a corpus packer. The gate is a *detector*; keep it
independent of the redactor so a change to one cannot silently disarm the other.

---

## 3. THE FOUR DEFECTS TO FIX

**S1 — Untracked scanner.** It lives in a burn-wave inbox folder. `git clean`
deletes the thing guarding your keys. → Move to `tools/`, `git add`, leave a
stub at the old path so any existing caller still resolves.

**S2 — Not wired.** Nothing calls it. `MagSecretScanWeekly` registered, never
fired. → Add to `githooks/pre-push`.

**S3 — `AWS-SECRET-40` is rated `high` and produces 80% of all findings.** The
regex is "any 40-char base64-ish string." This is why nobody reads the output:
`critical=1 high=48544` buries the one real critical. → **Demote to `low`, or
gate it behind the entropy check the scanner already computes but does not use
as a filter.** This is the single change that makes the rest readable.

**S4 — Beat ledger is a bug.** `files_with_rule_hits` embeds the whole 600-file
list → **641,924 bytes for ONE row**. Ten runs = 6 MB. → Store a count and a
path to the results file, not the list. One small line per run.

---

## 4. SHAPE OF THE DELIVERABLE

One new file, three hook lines. Suggested location `tools/secret_gate.py`.

```
tools/secret_gate.py
  --changed          scan only files changed vs upstream (fast path, use in pre-push)
  --full             whole-tree scan (offline / scheduled)
  --severity MIN     default: critical,high  -> block
                     medium,low             -> report only, never block
  --baseline PATH    named acceptance, B3 shape
  --json             machine output for the beat row

EXIT CODES
  0  clean, or only report-tier findings
  1  BLOCKING finding at or above --severity threshold
  2  scanner error / venv missing  <-- MUST NOT be silently swallowed
```

### Non-negotiable properties

1. **Fail closed on its own error.** Exit 2 must be distinguishable from
   exit 0. The census gate in this repo has exactly this bug: it blocks only on
   `-eq 2`, so a missing interpreter turns a blind detector into a silent warn.
2. **The redaction exemption is mandatory** (B2). Without it the scanner
   flags your own hand-redacted transcripts and trains you to ignore it.
3. **Blocking tier = the specific provider shapes only.** `GENERIC-KEYASSIGN`
   had a 99.5% false-positive rate in a separate audit. Report it; never block on it.
4. **No baseline on day one.** Start at zero. Force named acceptance. The
   933-debt baseline is why nobody trusts the ratchet.
5. **Do not print secret values.** Report `path:line:rule:severity` and at most
   a masked tail. Lane 9's boundary rules apply: never print a key.

---

## 5. BLOCKING ITEMS — OPERATOR DECISIONS, NOT SEAT WORK

**These are not yours to resolve. Flag them, do not act on them.**

**5a — `memory/trajectory/steps.jsonl:1994`** — Telegram-token-shaped
credential, **tracked and committed**. Requires human validation and rotation.

**5b — `memory/tls/lan.key`** — 1,675-byte RSA private key, mode 644, tracked
and committed since August, and its blob is present in the sibling bare repo
`Mag-backup.git` across **39 refs**. Removal requires a history rewrite; the
blob is already in `.git` packs, so `git rm --cached` frees nothing.

**5c — `mag/lab_episode.py:117`** — OpenAI-shaped literal. Probably an
overbroad `sk-sha...` skill-ID false positive, but NOT conclusively closed.
Needs a human who understands the module.

**5d — Moving `B2_73_secret_scan.py`.** Another seat built it. Renaming another
seat's work needs the operator's word. Default if not granted: **copy, don't
move**; leave the original in place.

---

## 6. ACCEPTANCE CRITERIA — receipts or it didn't happen

A build is done when all of these are true, with output captured:

- [ ] `tools/secret_gate.py --full` runs to completion, exit code recorded
- [ ] It reports `PRIVATE-KEY-BLOCK` for `memory/tls/lan.key` (proves the
      `critical` tier works on a known-true positive)
- [ ] Post-S3, total findings drop from ~60,470 to under ~12,000 and
      `critical`/`high` counts are readable by a human
- [ ] A synthetic `xai-REDACTED...MASKED` token in a temp file produces **no**
      finding (proves B2 exemption works)
- [ ] `githooks/pre-push` still passes its existing 8 gates unchanged
- [ ] Pre-push total runtime still under **15.7s** on the `--changed` path
- [ ] A deliberately planted high-severity token **blocks** the push
- [ ] A clean push does **not** block
- [ ] Simulated-missing-venv case returns exit **2**, not 0 (proves fail-closed)
- [ ] `git add` of the scanner lands; `git status` shows it tracked

## 7. STANDING RULINGS — obey these

- **Report to `watch/inbox/`. Never apply unbidden fixes.** If you find
  something else broken, write a card. Don't fix it.
- **Verkle chain is READ-ONLY.** No root repair, no GC, no consolidation.
  `rib_bus.publish()` folds a knot — **never publish.**
- **Docker read-only.** No `prune`/`rm`/`stop`/`rmi` unless the task names that
  exact operation on that exact container.
- **Memory/biography read-only.**
- **Receipts go to `memory/runs/hermes_jobs/`.**
- **Trust bytes over reports.** If a claim matters, measure it.

## 8. ELDER'S LAW (use to settle disagreements)

> contradictions resolve by evidence and hierarchy, not vote
> — `mag/elder.py:74`

If a seat disputes a finding, produce bytes. A vote settles nothing.

Related Elder receipt: `memory/runs/elder/audit.json` — `LIVE 4 / DECLARED 33`,
18 of 20 gaps are `receipt_stale` → *"run one bounded live dogfood step."*
That is likely the root cause of the whole class of problem this pack sits in:
**instruments built, not run.** Do not add an instrument that is not run.

## 9. STOP CONDITIONS — stop and report, do not improvise

- Scanner takes >60s on the `--changed` path → report, don't optimize silently
- Any finding would require printing a live secret → mask, report the location
- `--full` scan is needed inside the hook → **the hook must use `--changed`**;
  a full scan in pre-push is a 777s gate nobody will keep
- You believe the scanner is better deleted than wired → **report that, build
  nothing.** That is a legitimate finding.

## 10. OPEN QUESTION FOR THE BUILDER

The fleet already has a weekly beat (`scripts/secret_scan_weekly.py`) that
**has never fired**, and a hook gate that would fire on every push. These overlap.
Recommend ONE as authoritative in your receipt, and say why. Do not ship both
without stating which is canonical.
