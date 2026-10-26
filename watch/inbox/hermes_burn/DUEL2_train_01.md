# DUEL2_train_01 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Contender pass: ab1-gates-falsify (v1t-0002, train half)

## 1. Blocking finding: the material is absent from the evidence

The EVIDENCE block is empty. The contract gives only:

- `material_path`: `docs/ref/OPERATOR_GATES_SCHEMA.md`
- `material_sha256`: `740686330a8d27fd5ca0e2ae189cfa07b10872149e1f8b6520d02b27bd7c23f6`
- `first_line`: `You are a falsification engineer. Below is the full text of docs/ref/OPERATOR_GATES_SCHEMA.md (OPERATOR_GATES_SCHEMA, th` (truncated)

The file text itself never arrived. Under the estate laws I cannot cite file:line, and I cannot confirm that the bytes match the sha256. Every statement below about the schema's content is therefore **UNVERIFIED**, and I make none. I will not invent gate names, fields, or line numbers.

Negative example (what I refuse to do):
> "Line 41 says gates must be ordered; this is falsified by..."

That would be a fabricated citation.

## 2. Deliverable: a landable falsification protocol

A seat with the file can apply this as-is. It turns the document into falsifiable claims and a verdict table.

### Step A: Pin the bytes
1. Run `sha256sum docs/ref/OPERATOR_GATES_SCHEMA.md`. It must equal `740686330a8d27fd5ca0e2ae189cfa07b10872149e1f8b6520d02b27bd7c23f6`. If not, stop and report a MISMATCH, because every later verdict is about a different file.
2. Run `cat -n` on the file. All citations use that numbering.

### Step B: Extract claims
Take each sentence that asserts a checkable property. Look for "must", "never", "always", "required", "exactly one", "default", a numeric threshold, or an enumerated value set. Record each in this form:

```
CLAIM-<n>
  cite:      docs/ref/OPERATOR_GATES_SCHEMA.md:<line>  "<quoted bytes>"
  type:      {field-required | enum | range | ordering | exclusivity | default | cross-ref | semantics}
  falsifier: <the concrete input or observation that would make it false>
  instrument: <schema validator | grep | code path | runtime log>
  moment:    <static / load-time / run-time / at gate evaluation>
  context:   <assumed config, version, operator role>
  verdict:   {HOLDS | FALSIFIED | UNDETERMINED}
  evidence:  <file:line quote of the counterexample, or "none found under stated conditions">
```

### Step C: Probe by claim type

| Type | Falsification probe |
|---|---|
| field-required | Build an instance without the field. If it validates, FALSIFIED. |
| enum | Submit a value outside the set, and a case variant of a valid value. Acceptance of either contradicts a closed enum. |
| range | Test min-1, min, max, max+1. |
| ordering | Permute the gate sequence. If the outcome is unchanged, the ordering claim is vacuous. |
| exclusivity | Set both "exclusive" fields. Both accepted means FALSIFIED. |
| default | Omit the field and read the resolved value. It must match the doc. |
| cross-ref | Resolve every referenced file, field, or section. A dangling reference is FALSIFIED. |
| semantics | Find the code that implements the gate (grep the identifier) and compare behavior to the prose. Cite the code file:line. |

### Step D: Internal consistency sweep
- Compare each term's first definition with its later uses. Two values for one default is a contradiction.
- Compare every example in the doc against its own stated rules. An example that violates its schema falsifies the doc or the example.

### Step E: Verdict rules
- A verdict without instrument, moment, and context is invalid. Mark it UNDETERMINED.
- A HOLDS verdict means only "no counterexample found under the stated probes". Never write "proven".
- Rank the top 3 FALSIFIED claims by operator impact (a gate that fails open ranks above a typo).

## 3. Well-formed vs ill-formed entries

Positive (shape only; contents are illustrative placeholders, not claims about the file):
```
CLAIM-7  cite: <path>:<N> "<quoted bytes>"
  type: enum
  falsifier: value "Allow" (capitalized) accepted by the validator
  instrument: schema validator v<X> run against fixture f1
  moment: load-time   context: default config, operator role
  verdict: FALSIFIED  evidence: <path>:<M> "<quoted case-insensitive match>"
```

Negative:
```
CLAIM-7  The gates seem too permissive.   verdict: FALSIFIED
```
This has no citation, no falsifier, no instrument, and no conditions.

## 4. Falsifier for this deliverable

This protocol is wrong or useless if either of the following holds:
- Applied to the real file, it yields zero extractable claims of the types in Step C. The taxonomy would then not fit the document.
- Two independent seats applying Steps B-E to the same sha-verified bytes produce materially different FALSIFIED sets. The protocol would then be under-specified.

## 5. What is needed to finish

Supply the file text (or the `cat -n` output) matching the sha256. I will then fill the CLAIM table with real quoted citations and name the top falsified claims.
