# OUROBOROS R3 - TRUST INSTRUMENTS - break-accuracy (hostile second pass, 2026-10-05)

Verifier seat: break-accuracy. Job: byte-check the accuracy lens's evidence,
attack its falsifiers, find the conditions it dropped. Every row below was
re-run or re-read this sitting; commands named; nothing taken from the lens
on trust. No em-dashes. Working tree untouched (probes ran from %TEMP% or
in-memory; the one in-memory patrol probe wrote watch/inbox/tmp3y4_s1jt.probe.txt
and deleted it in its own finally block).

## VERDICTS

### Finding 1 (consensus layer certifies degenerate input): CONFIRMED

All four probes reproduce exactly, this sitting, repo venv:

- `.venv/Scripts/python.exe -c "from mag.consensus_gate import verdict; ..."`
  - `verdict(['the answer is 42'], model_params_b=27)` -> `CONFIRMED`
  - `verdict(['I cannot answer that']*3, model_params_b=27)` -> `CONFIRMED`
  - `consensus_quality(['root anchored ok']*3, independent=[True,True,True])`
    -> `n_independent: 3, verdict: 'strong'`
  - same bytes, no flags -> `n_independent: 1, verdict: 'correlated_weak'`
- Code cites byte-accurate: `sample_count` accepted at mag/consensus_gate.py:71
  and never referenced in the body (inspect.getsource count = 1, the signature
  line itself); the unanimity branch at mag/consensus_gate.py:86-98; the
  independence-flag path at mag/memweave.py:165-169 with the verdict ternary at
  mag/memweave.py:178-180. Dialect split verified: CONFIRMED/UNVERIFIED/DISPUTED
  vs strong/correlated_weak/single/empty.
- Nuance kept: "inverting the CID law it cites" is judgment, not bytes; the
  docstring at mag/memweave.py:120-127 frames the flag as the designed strong
  case. The operational fact stands unharmed: an unattested caller flag mints
  independence and converts a byte-identical echo into 'strong'.

### Finding 2 (workflow_gate passes pure prose; envelope exception content-blind; missing script exits 1): CONFIRMED

- Re-ran `workflow_gate.py check --script watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/probes/g8_vacuous_envelope.dwf.ts --no-register`
  -> `workflow_gate PASS digest=661e5b317ecb`, exit 0, G1/G2/G4/G5/G6/G7/G8
  all ok, G3 soft WARN. Identical to the lens claim.
- Re-ran on `watch/inbox/no_such_script.dwf.ts` -> `GATE ERROR: cannot read
  script: [Errno 2]`, exit 1. Identical.
- Code verified: the ONLY receipt-content test in g8_width_shape_ok is
  `os.path.isfile(path)` at tools/workflow_gate.py:191; G1-G7 are whole-text
  substring/regex checks over the full file (CHECKS table,
  tools/workflow_gate.py:83-128), no ask-body extraction anywhere; the
  unreadable-script path at tools/workflow_gate.py:444-449 returns 1.
- Two scoping notes that narrow but do not break:
  1. The only in-repo consumer of gate output found (githooks/pre-push:310-319)
     consumes the SCENARIO mode by first-line text match and is fail-closed on
     crash ("SCENARIOS ok"* arm, else exit 1). No consumer of `check --script`
     exit codes exists in-repo (searched githooks, scripts, tools, .zcode,
     .agents; ~/.zcode has no settings.json). So the exit-1-vs-2 fail-open arm
     is convention-conditional, exactly as the lens scoped it (CLI level only);
     the seat-law hook wiring remains unlocated, still OWED.
  2. Fix hardening the lens missed: `grep -io "envelope|max_concurrency|
     measured width" watch/inbox/INDEX.json` returns 5 hits (ENVELOPE,
     ENVELOPE_50W_HIT_20260926, ENVELOPE_LAW_20260926, envelope_50w_20261003,
     max_concurrency). INDEX.json is an index that REFERENCES receipt files and
     even contains the string max_concurrency, so the lens's proposed fix
     ("receipt-carrying pattern (measured width + date + token counts) inside
     the named file") must anchor a DATED MEASUREMENT shape, not keyword
     presence, or INDEX.json keeps passing it.

### Finding 3 (seal patrol permanently red, cannot separate noise from target): WEAKENED

Core re-proven live; the manual adjudication presented as evidence and the
falsifier are disproven by the bytes.

Confirmed parts:
- Re-ran `.venv/Scripts/python.exe tools/prepush_seal_patrol.py --rows 1000`
  -> `SEAL-PATROL: DRIFT`, exit 1, 11 drifted files at my moment (the lens's
  12th, evals-self-improvement-reddit.md, left the window's latest-seal
  between runs; moving tree, both moments named).
- Patrol core verified at tools/prepush_seal_patrol.py:108-137: whole-bytes
  compare (`actual == sha.lower()` at :132), no length, no prefix distinction.
- All three claimed POST-SEAL-EDIT files verified tracked AND git-clean
  (`git ls-files` + `git status --porcelain`): MASTER_EXECUTE_REGISTER.md,
  moonshot-1.md, STEALTH_SWEEP_LATEST.md. Committed bytes diverge from their
  seal. Seal timestamps in my pull match the lens's table exactly (12:09:11 /
  12:09:13 / 12:09:15 for the three register-op rows, autoseal rows to the
  second).

Weakening parts, byte-proven using the patrol's own resolver
(parse_ledger + resolve_sealed_path imported from tools.prepush_seal_patrol;
probe: sha256 over every line-boundary prefix of current bytes vs the full
sealed sha):
- All 5 WRITER-RACE rows (RECEIPT.md +22s, open-and-local-language-models
  via x.md +31s, open-and-local-language-models-x.md +28s, laws.md +116s,
  r06_free_probe.py +3m01s) have NO line-boundary prefix of current bytes
  hashing to the sealed sha. A "seal computed before the final flush landed"
  would leave the sealed bytes as a prefix; these files were rewritten in
  place, not flushed to. The lens's causal story for 5 of 12 rows is not what
  the bytes show.
- moonshot-1.md, one of the 3 "real post-seal edits", IS a byte-pure append:
  sealed sha == sha256 of the first 10664 of 13005 bytes.
- DOORS.jsonl, classified LIVE-APPEND, has NO prefix match (not a clean
  append vs its seal either).
- Therefore the falsifier as stated ("prefix-hash check ... would reclassify
  the LIVE-APPEND and WRITER-RACE rows as benign and leave exactly the
  POST-SEAL-EDIT rows red") is false in BOTH directions on the lens's own
  example set: moonshot-1.md would go benign, DOORS.jsonl would stay red.
  The mtime+git taxonomy and the byte taxonomy disagree on 7 of 11 rows.
  Neither the instrument NOR the lens's manual method separates the classes;
  only the prefix test does, and it draws different lines than the report
  drew. The finding's thrust (permanently-red alarm, instrument cannot
  adjudicate, fatigue risk) survives and is strengthened; its evidence table
  and its fix's claimed effect do not.

## ADDITIONS (what the lens missed, ranked by blast radius)

1. G8 envelope-receipt existence test is CWD-relative: the same script digest
   flips PASS to FAIL depending on the invocation directory. Ran the banked
   fixture from the repo root -> PASS exit 0; ran the identical file from
   %TEMP% -> `FAIL G8-width-shape`, same digest 661e5b317ecb. Cause:
   `os.path.isfile(path)` at tools/workflow_gate.py:191 resolves the stamp
   against the process CWD (the docstring at :183-184 admits "resolved from
   the repo root the gate runs in"). Blast radius first: the width law (the
   anti-429-storm instrument) gives environment-dependent verdicts; any hook,
   CI leg, or sibling seat invoking from another directory gets the opposite
   answer, and the false-block direction trains authors to strip stamps and
   cut widths. Falsifier: anchor resolution to Path(__file__).parents[1] and
   re-run from %TEMP%; verdicts must become identical, else my CWD story is
   wrong. Move: one-line anchor plus a foreign-CWD scenario card, ~15 min.
2. Seal patrol "latest seal" is last-row-wins in ledger order, not max-ts: a
   false-CLEAN constructor. Live-proven in-memory: rows [newer seal ts
   20:00 sha(v2), then older ts 19:00 sha(v1) later in the ledger], disk
   bytes = v1 -> patrol() returned drifted=[] (MATCH/ok) while the newest
   seal is violated. Cause: iterate-and-overwrite at
   tools/prepush_seal_patrol.py:112-116 with no ts comparison. Any writer
   appending out-of-order or backdated rows masks the true latest seal; a
   green lie certifies, which outranks the red-alarm fatigue the lens
   ranked. Falsifier: max-ts selection makes the same probe return DRIFT.
   Move: select by max ts in window plus a unit fixture from my in-memory
   probe, ~20 min.
3. credential_shape provider-family blindness, upgraded from the lens's
   code-read to live-proven: fake shape-only tokens (invented, zero secret
   value) `ghp_` + 36 alnum, `AKIA` + 16, and a bare JWT all scan clean
   (0 findings each via scan_text); a line carrying two distinct sk- values
   yields exactly 1 finding (rx.search first-match-only per shape per line).
   Tools/prepush_credential_shape.py:70-91 (SHAPES has no GitHub/AWS/JWT
   rows), :112 (search, not finditer). The instrument that caught the live
   key on day one is blind to three whole credential families and to the
   second key on any line. Falsifier: add the three shapes plus finditer
   and the identical probe must flag 3 more findings. Move: ~15 min.

## Blind-spot corrections (the lens's own list, byte-checked)

- mag/consensus_merge.py indeed does not exist; the symbol is
  mag/memweave.py:208; mag/_consensus_witness.py exists and is now read: a
  3-lane ground-truth witness harness (correct-vs-ground-truth counting,
  mag/_consensus_witness.py:64-70), a third consensus organ with yet another
  semantics; no verdict dialect at all. The dialect-count claim in finding 1
  understates: three organs, two dialects, one ground-truth counter.
- The cache_receipt producer behind cache_kpi's receipted split is
  mag/flight_recorder.py (grep -rln cache_receipt over mag/ models/ tools/),
  NOT mag/context_checkpoint.py; context_checkpoint.py is the prefix
  freeze/verify engine (freeze_receipt :138, verify_strict_prefix :161).
  The blind spot stands; its attribution was wrong. Producer still unexamined
  this round (both seats): OWED.
- FIRE_LEDGER.jsonl 2 rows vs REGISTRY.jsonl 90 at my moment (lens: 1 vs 89;
  moving tree). The width-join-is-dark claim holds.
- FOLD_SECTIONS.md exists under memory/runs/mickey17_v2/runs/<slug>/ for five
  slugs (2026-10-04-0 among them); the fold-not-rerun blind spot is real and
  remains: OWED to the operator (slug-copy run).
- The fold archive census reproduces EXACTLY: 52 deep_tier2 verdict rows,
  {'verified': 46, 'unconfirmed': 6}, 0 rows without verdict, over all
  *.checks.json under memory/runs/mickey17_v2. CONVERGENT with the lens
  (independently re-derived this sitting).
- Green claims re-run: golden vector 11/11 exit 0; scenario suite "9 cards
  validated read-only" exit 0; citation_lint --changed ok (records=7 at my
  moment vs the lens's 5, moving tree, 0 blocking both times); cache_kpi
  rows=77716 matches the lens census exactly (the all-ISO sub-claim was NOT
  re-verified and rides on the lens's word).
- metadata patrol SCAN_DIRS verified project-only at
  tools/prepush_workflow_metadata.py:64; ~/.zcode/workflows does not exist on
  this machine today (latent claim confirmed).

## R3 DRIVER AMENDMENT (round-4 gap, extends the lens's own amendment)

The lens's amendment (a vacuous-pass probe per instrument) is endorsed but
incomplete. R4's driver must also require, per instrument touched:
(b) INVOCATION-INVARIANCE: same input, foreign CWD / foreign invocation
shape, identical verdict. The G8 CWD flip is the exemplar: every fixture in
the repo's suites runs from the repo root, so no in-repo card can see it.
(c) BYTE-ADJUDICATION BEFORE CLASS-NAMING: no drift/alarm class may be
named from mtime plus git alone; the prefix test reclassified 7 of 11 rows
the mtime method labeled, and the lens's own falsifier died on it.
Without (b), R4's fixture suite passes in CI while field hooks flip
verdicts; without (c), R4 re-banks mtime stories as evidence.

## Commands run this sitting (the full list, for the receipt)

- consensus probes (4, one python -c, repo venv, output above)
- workflow_gate check --script <banked fixture> --no-register (PASS exit 0)
- workflow_gate check --script watch/inbox/no_such_script.dwf.ts --no-register (exit 1)
- workflow_gate check --script <same fixture, absolute path, CWD=%TEMP%> (FAIL G8)
- prepush_seal_patrol.py --rows 1000 (DRIFT exit 1, 11 files)
- git status --porcelain + git ls-files over the 11 drifted files
- adjudication probe (patrol's own parse_ledger/resolve_sealed_path/patrol,
  sha256 over line-boundary prefixes), %TEMP% script
- in-memory last-row-wins masking probe via patrol()
- scan_text credential probes (4 fake shape-only tokens)
- prepush_golden_vector.py (11/11), workflow_gate check --scenarios (9 cards),
  citation_lint.py check --changed (ok), cache_kpi.py (77716 rows)
- fold census over memory/runs/mickey17_v2/**/*.checks.json (52/46/6/0)
- greps: seat_law/workflow_gate consumers; cache_receipt producers;
  INDEX.json envelope mentions; SCAN_DIRS; FOLD_SECTIONS.md find
