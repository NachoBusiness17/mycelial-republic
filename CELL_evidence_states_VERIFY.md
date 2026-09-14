# evidence_states — declared/attempted/verified discipline

## Finding — what your cell yields
The evidence_states domain is **Supported** by the repo's tri-state claim discipline, enforced through the AOS integrity kernel (`mag/embassy_integrity.py` and `mag/integrity_kernel.py`) and recorded in the durable work register (`mag/work_register.py`). The discipline is: Supported claims require Evidence; Disputed claims require contradicting evidence; everything else is Unproven. This is not aspirational—it is mechanically enforced by the kernel's `validate()` method and the work_register's claim folding that degrades invalid claims to Unproven.

## Evidence — what in the repo supports it (file/shape, no invention)
- `mag/embassy_integrity.py` lines 7–60: defines the tri-state claim model (Supported/Unproven/Disputed) with Evidence/Inference/Assumption basis; the `validate()` method enforces that Supported claims must have Evidence and Disputed claims must have contradicting evidence.
- `mag/integrity_kernel.py` lines 1–95: vendored AOS integrity kernel implementing the same tri-state discipline and validation rules.
- `mag/work_register.py` lines 59–100: the `record()` function folds tri-state claims into the durable manifest (`memory/runs/work_register/manifest.jsonl`) and degrades invalid claims to Unproven; claim validation happens before folding.
- `memory/runs/work_register/manifest.jsonl` (shape): the durable manifest records every folded claim with its validated status, basis, and evidence—this is the concrete evidence surface.
- `logs/claims.jsonl` (shape): every claim folded into the register is also logged here with timestamp and validation outcome.
- `mag/embassy_integrity.py` lines 84–130: VerkleWitness provides tamper-evident provenance for the evidence chain (append-only, hash-linked nodes), satisfying the "evidence-first" requirement.

## Risk if wrong — what the audit breaks on if this is missed
If the examiner finds that the repo conflates declared/attempted/verified states without mechanical enforcement, the entire tri-state discipline collapses. Steiniger's abliteration instinct would strip safeguards and reveal that claims are self-reported rather than evidence-backed. The audit would fail on **Evidence Supremacy** (ARK Article II analog) and **False-Success Guard** violations. The verkle chain's tamper-evident provenance would be undermined if claims are not rigorously evidence-first.

## The act — the concrete prep step (file/spec/number)
Create a one-page **evidence_states_audit.md** at `docs/ref/evidence_states_audit.md` that:
1) States the tri-state discipline as a **law** (not guideline): every claim in the repo must carry a status (Supported/Unproven/Disputed) with basis and evidence.
2) Lists the **enforcement points**:
   - `mag/embassy_integrity.py::Claim.validate()` enforces the discipline.
   - `mag/work_register.record()` degrades invalid claims to Unproven before folding.
   - `memory/runs/work_register/manifest.jsonl` and `logs/claims.jsonl` are the durable evidence surfaces.
3) Provides a **checklist** for the examiner:
   - Scan `memory/runs/work_register/manifest.jsonl` for any claim with status=Supported but no evidence field.
   - Verify that every Disputed claim has a contradicting evidence entry.
   - Confirm that the kernel's `validate()` method is called before folding in `work_register.record()`.
4) Adds a **falsifier**: a script `scripts/evidence_states_audit.py` that programmatically checks the manifest for violations and prints a verdict (PASS/FAIL).

## Falsifier — what would prove this wrong
- Any claim in `memory/runs/work_register/manifest.jsonl` with status=Supported but missing evidence field.
- Any claim with status=Disputed but missing contradicting evidence.
- A claim that passes the kernel's `validate()` but is still folded with an invalid status (the kernel degrades it, so this would indicate the degradation logic is bypassed).
- The examiner runs `python scripts/evidence_states_audit.py` and it returns FAIL.
