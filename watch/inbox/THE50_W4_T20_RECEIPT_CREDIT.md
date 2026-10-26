# THE 50 · W4 T20 - SINGLE-ROLLOUT RECEIPT-CREDIT DRY SPEC (vast-train-dry upgrade)

Filed 2026-09-19 · W4 MATTHEW / OCTOBER · finish line per
`watch/inbox/THE_50_PROGRAM_20260918.md` line 33 and
`.zcode/workflows/the-50.dwf.ts` line 42.

Status: SPEC, NOT BUILT. Nothing here changes code yet. The only thing this
file executes is its own filing.

## 0. The credit rule (one falsifiable sentence)

> A rollout step pays exactly one credit if and only if, at verification time,
> `memory/training/runs/{run_id}/rollout.jsonl` holds an append-only row whose
> `item_id` equals the pinned id of the slice item it answered and whose
> `sha256` equals the hash of the raw output bytes stored in that same row;
> every other step, including a transport death and any step whose only trace
> is claimed text, pays zero, and this rule is falsified the first time a paid
> Vast job or an October beat-baseline verdict is authorized on a rollout with
> zero credits.

Falsifiable two ways. Per step: one line of ordinary code recomputes
sha256 of the row's `raw` field and compares to the row's `sha256` field;
no match, no credit, and a row that fakes it is detectable forever because the
file is append-only. Per program: the fleet record either contains an
authorized paid job (or October verdict) resting on a zero-credit rollout, or
it never does; one such row anywhere kills the rule.

## 1. What exists today (read and run this session)

`main.py vast-train --dry` is validate-plus-price with zero behavior
measurement. `mag/vast_train.py:104-108` (`dry_run`) chains three functions:
`validate_export` (`mag/vast_train.py:25-71`, JSONL + signed manifest + sha256
+ row schema + T2 cap), `build_job_spec` (`:74-85`), and `estimate_cost`
(`:88-101`, cheapest GPU that fits VRAM, spend cap). The CLI hard-refuses
everything else: `main.py:2921-2922` returns "Only --dry is available in v5 V1; no
instance was launched." and the result hardcodes `launched: false`
(`mag/vast_train.py:108`).

Ran this session, real bundle:

```
.venv/Scripts/python.exe main.py vast-train --dry --export-path memory/training/export/orch_train_2026-08-06.jsonl
-> ok: true, rows: 4, sha256 b4fff756...955a5d, base qwen2.5-7b,
   estimate rtx_4090_24gb x 8h = $2.80 vs cap $50.00, launched: false
```

The current dry proves the cargo is packed and priced. It proves nothing about
whether anyone can measure what comes back.

## 2. The gap this closes (October)

- The Phase V3 eval gate says "new weights must beat baseline on frozen eval
  set" (`docs/ref/MAG_v5_VAST_TRAINING.md` section 3, Phase V3) and promote
  stays L3 human (same file, section 5). No instrument today produces that
  baseline.
- October is defined on file: "distill the ledger into model weights, then
  test whether the weights carry the behavior without the record"
  (`watch/inbox/MATTHEW_CIO_BRIEF_20260918.md` line 134). A test of what the
  weights carry needs a before-receipt and an after-receipt from the same
  frozen slice. Neither exists.
- The fleet's own accounting law already names the failure mode this spec
  prevents: "a claim of done needs bytes on disk first"
  (`tools/duty_fuzz.py` duty D1, citing the AGENTS.md shared-artifact boundary
  and the percolator invariant "trust bytes, not reports"). A $50 training job
  whose only eval is a claimed number would be exactly that violation at
  scale. W1 T05 already priced the currency: "the receipt is the only hard
  currency" (`watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md` line 58); WBN
  steal states the shape: "Every output is a receipt"
  (`watch/inbox/WBN_STEAL_20260918.md` lines 44-45).

## 3. The upgrade: add a single-rollout receipt-credit stage to vast-train-dry

New flag, backward compatible: `main.py vast-train --dry --rollout`.
Plain `--dry` keeps its exact current behavior and output schema. The rollout
stage never launches anything; `launched` stays `false` forever
(`mag/vast_train.py:108` and `main.py:2921-2922` unchanged). Dry stays dry: the
rollout fires at local-first seats (Ollama first per the tier ladder, free
lanes as fallback), cost $0, cost_ledger row only if a seat ever bills.

### 3.1 Single rollout, defined

ONE model, ONE frozen slice, ONE pass. Not the four-condition battery: that
preregistration is 160 runs with a floor of 15 per condition
(`watch/inbox/FOUR_CONDITION_PREREGISTRATION_20260918.md` lines 38-42). A
single rollout is the minimum receipt-producing unit and supports no
population claim. It exists to (a) prove the eval path is receipt-capable
end to end before any spend, and (b) produce the paired baseline receipt any
later N must cite.

### 3.2 The frozen slice

Default slice: first 5 rows of `watch/inbox/duty_fuzz/cycle_000.jsonl`
(10 cases on disk, held out by construction, closed option set A-D, each row
carrying a pinned `fingerprint` and a non-model label `spec_reading`; verified
on disk this session). Slice membership is pinned by the row fingerprints
against the batch manifest, never regenerated, never drawn from the training
export (training on eval items would poison the gate). When the 20-dilemma
battery lands (`watch/inbox/four_condition_battery/`), the slice may upgrade
to 5 of those; the rule "slice pinned by fingerprint at registration time"
does not change.

### 3.3 Rollout rows (schema mag_vast_train_rollout.v1)

Path: `memory/training/runs/{run_id}/rollout.jsonl`, one row per step, plus
`rollout.manifest.json` (slice fingerprints, model id, seat id, seed, credit
total). Row fields, all required:

- `run_id`, `item_id` (the pinned duty_fuzz id, e.g. FZ-c000-001)
- `seat`, `model_id`, `ts`
- `raw`: the model's raw completion text, unedited
- `sha256`: hash of `raw` (the credit key)
- `pick`: the parsed option letter, or null if unparseable
- `outcome`: `receipted` | `transport_death` | `unparseable`
- `evidence`: error string for deaths, parse detail for unparseables
- `attempt`: integer; ids idempotent per (run_id, item_id, attempt), reusing
  the meter law that a re-run never inflates n (`mag/verb.py:462-477`,
  `meter_record`, idempotent by id, evidence mandatory or the write refuses)

Transport deaths (429, timeout, 404) get one retry, then are recorded as
`transport_death` with credit 0, forever. They are never dropped and never
credited: this keeps the meter's known conservative bias, where transport
deaths count as misses (fleet meter doctrine, JEV-1, commit c7255fa49). A
death is a measurement, not a verdict (harness law), but it is also not a
receipt.

### 3.4 The two gates the credits feed

1. Pre-flight (spend gate, runs today). `credits == n_steps` authorizes
   nothing by itself; it makes the job SPECIFIABLE. `credits < n_steps` after
   in-run retry means the instrument cannot receipt; the paid job is refused
   and the deaths are on file. Law: training a model you cannot measure buys
   an uninstrumented leaf.
2. Post-train smoke (runs when an adapter exists). Same slice, same
   fingerprints, same scorer, trained model. Trained rollout must itself hit
   `credits == n_steps` or it does not count. Then ordinary code compares:
   duty accuracy per rollout (pick vs the row's pinned `spec_reading`) and SCS
   consistency between the base picks and trained picks via
   `scs_score` (`tools/scs.py:125-140`, `1 - JSD` in bits, bounded
   [0,1]; self-test PASS, 13 checks, run this session with
   `.venv/Scripts/python.exe tools/scs.py --self-test`). Decision, fixed now
   per the preregistration reflex: trained accuracy below baseline = the
   fine-tune hurt, do not proceed toward promote; at or above = proceed to
   the full battery. The single rollout decides GO/NO-GO for spend and
   battery, never the October thesis verdict; that stays with the
   preregistered 160-run experiment.

## 4. Boundaries (what this spec does not do)

- No Vast instance is created, started, or polled. `--run`, `--status`,
  `--fetch` remain unimplemented (`docs/ref/MAG_v5_VAST_TRAINING.md` section 4
  lists them for v5; this spec adds none of them).
- No weights are promoted. Promote stays L3 human (same file, section 5).
- No claim about whether October transfer works. Either smoke outcome is
  data; the falsifiers that kill the thesis live in
  `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md` section 6.
- Open dependency, honest: the spec assumes a seat that serves the base model
  for inference (local Ollama first). Whether `qwen2.5-7b` is pulled on the
  local Ollama host was NOT verified this session; the build seat must verify
  seat availability before firing the first rollout and record the seat id in
  the manifest.

## 5. Falsifier of this spec (distinct from the credit rule's falsifier)

If a single rollout produces all-credit receipts on both base and trained
models, and the comparison still cannot decide GO/NO-GO (for example: every
step receipts, but slice items are so easy both models score 5/5 and SCS
consistency is 1.0, leaving no headroom to detect damage), then receipt-credit
receipts capability but measures nothing, and the slice or the metric is the
defect. Fix would be an amendment row here, not a silent rule change.

## 6. Provenance (every claim's file, all read this session)

- `mag/vast_train.py:104-108` - current dry_run, `launched: false` hardcoded.
- `mag/vast_train.py:25-71, 74-85, 88-101` - validate / spec / estimate chain.
- `main.py:1766-1773` - CLI parser; `main.py:2923-2927` - call site;
  `main.py:2921-2922` - the only-dry refusal.
- `configs/vast_train.yaml:58, 61` - default base model qwen2.5-7b, $50 cap.
- `docs/ref/MAG_v5_VAST_TRAINING.md` section 3 Phase V3 and section 5 -
  beat-baseline gate, promote L3 human.
- `watch/inbox/MATTHEW_CIO_BRIEF_20260918.md` line 134 - the October test.
- `watch/inbox/FOUR_CONDITION_PREREGISTRATION_20260918.md` lines 38-42, 46-49,
  73-74 - run floors, SCS primary metric, no-LLM-judge rule.
- `tools/scs.py:125-140` - scs_score; self-test PASS 13 checks this session.
- `tools/duty_fuzz.py:23-26` - duty D1 receipt-before-claim;
  `watch/inbox/duty_fuzz/cycle_000.jsonl` - the slice (10 rows, pinned
  fingerprints, closed A-D options, non-model labels).
- `mag/verb.py:462-477` - meter_record idempotency and mandatory-evidence law;
  `mag/verb.py:479-498` - "UNMEASURED, never passing" floor pattern.
- `watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md` line 58 and
  `watch/inbox/WBN_STEAL_20260918.md` lines 26, 44-45 - receipts as the
  currency.
- `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md` section 6 - October falsifiers,
  untouched by this spec.
- Commands run this session: `main.py vast-train --dry` on the real bundle
  (output in section 1) and on a missing path (ok:false, three validation
  errors, gate works); `tools/scs.py --self-test` (PASS, 13 checks).

## 7. Re-verification receipt (2026-09-25, second seat re-checked against disk)

Every citation in sections 0-6 was re-opened and re-checked against disk this
session, and all three commands listed in section 6 were re-run. Results:

- One citation repaired: the "receipt is the only hard currency" line sits at
  `watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md` line 58 today, not lines 55-56;
  sections 2 and 6 updated. No other line reference drifted as of 2026-09-25
  (see the 2026-09-26 amendment below: the main.py refs did not hold).
- Held exactly: `mag/vast_train.py:25-71, 74-85, 88-101, 104-108`
  (`launched: False` still hardcoded at 108); `main.py:1766-1773` parser,
  `main.py:2923-2927` call site, `main.py:2921-2922` only-dry refusal;
  `configs/vast_train.yaml:58` (qwen2.5-7b) and `:61` ($50 cap);
  `tools/scs.py:125-140`; `mag/verb.py:462-477` meter_record;
  `docs/ref/MAG_v5_VAST_TRAINING.md` Phase V3 eval gate (line 92) and L3
  human promote (line 120); `watch/inbox/THE_50_PROGRAM_20260918.md` line 33;
  `.zcode/workflows/the-50.dwf.ts` line 42 (task 20, this finish line);
  `watch/inbox/MATTHEW_CIO_BRIEF_20260918.md` line 134;
  `watch/inbox/FOUR_CONDITION_PREREGISTRATION_20260918.md` lines 38-42;
  `watch/inbox/WBN_STEAL_20260918.md` lines 26, 44-45;
  `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md` section 6.
- Slice re-checked: `watch/inbox/duty_fuzz/cycle_000.jsonl` still 10 rows,
  each with a pinned `fingerprint` and a non-model label `spec_reading`,
  closed 4-option (A-D) sets, first id FZ-c000-001.
- Re-ran `.venv/Scripts/python.exe main.py vast-train --dry --export-path
  memory/training/export/orch_train_2026-08-06.jsonl`: ok true, rows 4,
  sha256 b4fff756...955a5d, base qwen2.5-7b, rtx_4090_24gb x 8h = $2.80 vs cap
  $50.00, launched false. Identical to the section 1 receipt.
- Re-ran `.venv/Scripts/python.exe tools/scs.py --self-test`: PASS (13 checks).
- Re-ran `.venv/Scripts/python.exe main.py vast-train --dry --export-path
  memory/training/export/does_not_exist.jsonl`: ok false, exit 1, exactly the
  three validation errors (export JSONL not found, export manifest not found,
  export has too few rows). Gate still works.
- Still true and unchanged: this file is a SPEC, NOT BUILT. No rollout flag,
  no rollout schema, no gates exist in code. The build seat that picks up the
  `--rollout` upgrade starts from section 3.

### Amendment 2026-09-26 (b2-01-the50-punch)

Cause: the Wave-2 quality audit (`watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md`,
batch 3.5) proved the 09-25 "no other line reference drifted / held exactly"
claims wrong for the three main.py refs; this amendment re-derived them from
current bytes because main.py moved AGAIN after the audit (the preceding
train-stats branch's `return 0` now sits at 2888, where the audit saw 2885).
Evidence this session: `main.py:2921` is the only-dry refusal print, `:2922`
the `return 2`; the `p_vast_train` parser block spans 1766-1773 (`--dry` 1770,
`--export-path` 1771, `--base-model` 1772, `--max-hours` 1773); the `dry_run`
call site spans 2923-2927 inside the `vast-train` handler opened at 2917;
`mag/vast_train.py:108` still hardcodes `launched: False`; prereg's
no-LLM-judge rule sits at lines 73-74, not 72. Sections 1, 3, 6 and the
"Held exactly" block above carry the corrected refs.
