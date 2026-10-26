# RERUN PREREG - method-card frozen battery (re-sealed spine)

Preregistered 2026-09-26 by gala afterparty gopher t15, BEFORE any rerun answer or
score exists. This file is the scoring contract. Nothing in it may be edited after
the first rerun answer is written; corrections land as a new dated prereg that
supersedes this one by name.

## 0. Negatives first (what must NOT happen)

- GROUND_TRUTH_HELDOUT.md must NOT be opened, read, excerpted, or summarized by any
  scorer before its scoring phase. Prereg author complied: hashes computed
  byte-blind, content never opened in this session.
- BATTERY_HELDOUT.md must NOT be opened by any scorer, and must NOT be opened by the
  answer seat before the seal gate passes (Section 2).
- The heldout files must NOT be edited, renamed, or re-created. They must stay
  byte-identical to commit 926b9abf1 (the commit that landed them).
- No prior run's answers may be shown to the answer seat. No answer may be shown to
  the scorer before scoring except through the single answers artifact of Section 3.
- No scoring may start on a mismatched seal. Any seal mismatch at scoring time ABORTS
  the run (Section 4). There is no waiver path; a stale seal means the corpus state
  the battery was frozen against no longer exists.

## 1. Seal reference (fresh seal is the ONLY valid scoring baseline)

Seal file: `watch/inbox/method_card_exp/FREEZE_SEAL.json`
Sealed: 2026-09-26T00:19:19-0400 by gala afterparty gopher t5, after post-seal spine
regeneration. The prior 2026-09-24 seal (index 85ed40fa85b0..., retained in
`prior_seals[0]`) is PROVABLY STALE (w3 lane a07-method-cards re-hash finding) and is
NOT a valid baseline for any run.

Spine files hashed by the seal (paths as sealed in lanes/t5.check.txt):

| role | path | sha256 (first 12) | bytes | rows |
|---|---|---|---|---|
| index | dashboard/data/ESTATE_INDEX.jsonl | `cceace710d48` | 402,114,160 | 1,221,058 |
| last_run | dashboard/static/index_data/last_run.json | `82940bc0a63f` | 4,533 | - |
| rollup | dashboard/static/index_data/rollup.json | `4f76d535cb0f` | 19,621 | - |

Full hashes are in FREEZE_SEAL.json; this prereg binds to that file, not to its
transcription here. Verified matching at prereg time: 2026-09-26, re-hash of all
three files returned the sealed values exactly (evidence: lanes/t15.check.txt).

Heldout integrity baseline (byte-blind hashes at prereg time, must equal commit
926b9abf1; verified equal at prereg time):

- BATTERY_HELDOUT.md: `98a364293ec20aa3d05e43e569d316be8f1baff2dd99afe07b1c3477bd5ee82c`
- GROUND_TRUTH_HELDOUT.md: `81aa08447f3d3ec31d5a78987adc393ec30c0730a908fcfc445ca7f4c9e46a7d`

## 2. Frozen command

**SPEC-NEW marker:** CONTROL_SHEET.md carries twelve per-fact re-verify commands but
NO single scoring command. Per the rerun contract, the command below is specified
fresh here and marked **SPEC-NEW**.

Design under test: "method-card condensation (one-pager vs 1.3M files)". Treatment
is CARD_V2.md (the shipped one-pager, v1 laws + scorer-forced appendix; the appendix
holds open-battery Q1-Q12 facts only, not heldout answers). The rerun asks whether a
fresh seat holding ONLY the card can decode the heldout answers out of the sealed
estate.

Run from ESTATE root, Git Bash, with this repo's venv. Any deviation from this text
invalidates the run and must be filed as a finding, not silently patched.

### STEP 1 - seal gate (bash, deterministic; exit 2 = ABORT)

```bash
./.venv/Scripts/python.exe - <<'PY'
import hashlib, json, sys
seal = json.load(open('watch/inbox/method_card_exp/FREEZE_SEAL.json'))
spine = {
 'index_sha256':     'dashboard/data/ESTATE_INDEX.jsonl',
 'last_run_sha256':  'dashboard/static/index_data/last_run.json',
 'rollup_sha256':    'dashboard/static/index_data/rollup.json',
}
for key, path in spine.items():
    h = hashlib.sha256(open(path,'rb').read()).hexdigest()
    if h != seal[key]:
        print(f'SEAL MISMATCH {path}: {h[:12]} != {seal[key][:12]}'); sys.exit(2)
heldout = {
 'watch/inbox/method_card_exp/BATTERY_HELDOUT.md':
   '98a364293ec20aa3d05e43e569d316be8f1baff2dd99afe07b1c3477bd5ee82c',
 'watch/inbox/method_card_exp/GROUND_TRUTH_HELDOUT.md':
   '81aa08447f3d3ec31d5a78987adc393ec30c0730a908fcfc445ca7f4c9e46a7d',
}
for path, want in heldout.items():
    h = hashlib.sha256(open(path,'rb').read()).hexdigest()
    if h != want:
        print(f'HELDOUT DRIFT {path}: {h[:12]}'); sys.exit(2)
print('SEAL OK')
PY
```

### STEP 2 - answer phase (fresh seat, after STEP 1 prints SEAL OK)

A NEW session (fresh context, no memory of this experiment) is given exactly two
files as loaded context: `CARD_V2.md` and `BATTERY_HELDOUT.md`, plus live read
access to the estate. It answers all heldout questions and files
`watch/inbox/method_card_exp/RERUN_ANSWERS_<YYYYMMDD>.md`, one row per question:
the fact + the exact file path and/or number that proves it, per the battery's own
format. The answer seat must cite only paths verifiable under the sealed spine.
No time limit is set; no other constraint changes.

### STEP 3 - score phase (different seat, after answers exist)

A DIFFERENT session, which has never read GROUND_TRUTH_HELDOUT.md nor any prior
battery answers, opens the answers artifact and GROUND_TRUTH_HELDOUT.md together for
the first time, grades each row MATCH / PARTIAL / MISS per BATTERY.md's scale
(MATCH = fact + correct path/value; PARTIAL = right shape, wrong detail; MISS),
re-verifies every cited path/value against the sealed spine (re-hash gate of STEP 1
re-run before scoring; CONTROL_SHEET.md commands may be used for spot re-verify),
and files `watch/inbox/method_card_exp/RERUN_SCORE_<YYYYMMDD>.md` with per-question
verdicts + the tally + the seal status at score time.

## 3. Scorer-exclusion rule

A seat is EXCLUDED from scoring if any of these hold:

1. It has ever read GROUND_TRUTH_HELDOUT.md before its own STEP 3.
2. It has ever read BATTERY_HELDOUT.md before its run's STEP 1 passed.
3. It wrote, supervised, or read any prior battery answers or score rollups
   (including the original run and this rerun's STEP 2 output).
4. It authored this prereg or the seal (t15 and t5 are excluded from scoring).

The answer seat and the score seat must be different sessions. If no seat satisfies
1-4 exists, the run does not happen; register the blocker, do not relax the rule.

## 4. Abort conditions (any one aborts the run, no exceptions)

1. SEAL MISMATCH: any spine re-hash at STEP 1 or STEP 3 differs from FREEZE_SEAL.json
   (this is the item-mandated abort; the seal gate exits 2 on it).
2. HELDOUT DRIFT: either heldout file's sha256 differs from Section 1's baseline
   (edited, re-created, or moved).
3. Spine shape drift: `wc -l dashboard/data/ESTATE_INDEX.jsonl` is not 1,221,058 or
   size is not 402,114,160 bytes at gate time.
4. Contamination: any exclusion rule in Section 3 cannot be satisfied.
5. Mid-run regeneration: if the spine regenerates between answer and score phases,
   STEP 3's re-run of the gate exits 2 and the answers are void (score against a
   corpus state the answers were not decoded from).

An aborted run files a receipt naming which condition fired. Abort is a finding
about the environment, not a failure of the battery.

## 5. Falsifier (what result kills the battery's premise)

The battery's premise: the one-page method card carries the method ("No luck
involved") - a fresh seat holding only the card can decode correct, citable answers
out of the sealed estate, without the original operator's tacit context.

The premise is KILLED if, on a run that passed all gates, any of these hold:

1. Tally: MATCH count is 4 or fewer of 12 (at or below the plausible-voice guess
   band of one in three), meaning the card does not transfer the decode method.
2. Phantom citations: more than half of the MATCH verdicts cite paths/values that
   fail verification against the sealed spine, meaning answers came from recall or
   invention, not decode (the card's own law 3 dead).
3. Unrunnable estate: the spine cannot hold a seal long enough to complete one full
   answer-then-score cycle across two attempts, meaning freeze-seal-then-compare
   (card law 9) is impossible on this estate and comparative claims are dead.

If the premise survives (MATCH >= 8/12 with verifying citations), the rerun confirms
the card as a transferable skill unit and the battery graduates to a reusable
regression harness; PARTIAL-heavy tails (5-7 MATCH) are a graded finding, neither
kill nor confirmation.

## 6. Artifacts

- Prereg: this file (written before any rerun answer exists).
- Evidence: `watch/inbox/gala_20260925/afterparty/lanes/t15.check.txt`
- Bank: `watch/inbox/gala_20260925/afterparty/lanes/t15.json`
- Seal: `watch/inbox/method_card_exp/FREEZE_SEAL.json` (t5, 2026-09-26T00:19:19-0400)
- Seal receipt: `watch/inbox/gala_20260925/afterparty/lanes/t5.check.txt`
- Stale-seal finding: `watch/inbox/gala_20260925/w3/lanes/a07-method-cards.json`
