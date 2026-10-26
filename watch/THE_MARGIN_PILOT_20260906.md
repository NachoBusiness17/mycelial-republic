# THE MARGIN PILOT — B9: one statement, one seat, kernel-checked (2026-09-06)

**Charter:** watch/THE_MARGIN_20260906.md (SANCHO — THE THEOREM station) ·
**Build:** mag/the_margin.py (548 lines, stdlib-only) + state/the_margin_dag.json +
watch/inbox/the_margin/pilot.lean (38 lines) · **Verdict: PROVED — kernel clean,
rc=0, no error, no sorry.** Pilot ran on THIS seat's own tokens, staged for scale.
No lane fires, no Docker, no chain writes (knotting is the next station's hand).

## 1. The stolen grammar, mapped (Prove2Me arXiv:2608.28433 → fleet)

| Prove2Me feature | Our implementation | Where |
|---|---|---|
| DAG of theorem statements as shared to-do list | Node graph, deps with acyclicity check, `next` = claimable (deps proved, open) | mag/the_margin.py `Dag`, `claimable()` |
| Statements split from proofs | Node carries the `theorem` string; proofs live in .lean artifacts, attempts reference them | `Node.statement` vs pilot.lean |
| NL description per node | `nl_description` plain-English front matter, mandatory field | every node |
| Agents work disjoint lemmas, guaranteed consistency | deps-must-be-proved gate + acyclicity check at edge insert | `add_dep()` |
| Failed attempts stay in the graph | Append-only attempt log ENFORCED at save time (edit/remove/drop raises); 4 kernel rejections preserved verbatim, hashed | `save()` guard, F2 |
| Kernel is the label | `lake env lean` runner, output captured verbatim + sha256; no-sorry = clean | `run_kernel()` |

## 2. Toolchain status — ground truth, not intention

- Pre-check: no lean/elan/lake on PATH, no `~/.elan`. **elan bootstrap strike 1:
  SUCCESS** (curl elan-init.sh → run `-y --default-toolchain stable`).
- Probe (verbatim, from `python -m mag.the_margin toolchain`):
  - lean: `Lean (version 4.33.1, x86_64-w64-windows-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)` — found in `~/.elan/bin`, **not on this process's PATH** (stale env; reported, not smoothed).
  - elan: `elan 4.2.4 (227caca13 2026-08-25)` · lake: `Lake version 5.0.0-src+819816b`.
- Mathlib: shallow clone @ `80cbd0498ab39e21d24d6730b3f932cec672a702` (2026-09-06,
  main tip), pinned toolchain `leanprover/lean4:v4.34.0-rc2`, `lake exe cache get`
  8865/8865 files downloaded + decompressed. Substrate cost: 7.3G disk, $0 API.

## 3. Candidate table — presence honestly classified (tri-state discipline)

All three came back **VERIFIED-PRESENT** — the brief's ABSENT/ASSUMED-ABSENT
binary did not survive contact with the actual mathlib tree, so the classification
says so. Grep instrument: the exact tree we compile against (stronger than a docs
search; commit-pinned).

| Candidate | Statement (Lean 4 + Mathlib) | mathlib-presence | Receipt |
|---|---|---|---|
| margin-wilson | `theorem margin_wilson (p : ℕ) : Nat.Prime p ↔ ((p - 1)! + 1) % p = 0` | **VERIFIED-PRESENT** | Mathlib/NumberTheory/Wilson.lean — `ZMod.wilsons_lemma : ((p - 1)! : ZMod p) = -1` + full Wilson file; see-also names `Nat.prime_iff_fac_equiv_neg_one` (Data/ZMod/Factorial.lean:23) |
| **margin-primes-infinite (PILOT)** | `theorem margin_infinitude_of_primes : ∀ n : ℕ, ∃ p, n < p ∧ Nat.Prime p` | **VERIFIED-PRESENT** | Mathlib/Data/Nat/Prime/Infinite.lean:33 `theorem exists_infinite_primes (n : ℕ) : ∃ p, n ≤ p ∧ Prime p` — mathlib's form is non-strict (`n ≤ p`), ours strict (`n < p`); our node is a fleet-namespace re-derivation, honestly labeled |
| margin-sum-two-squares | `theorem margin_sum_two_squares (p : ℕ) (hp : Nat.Prime p) (h : p % 4 = 1) : ∃ a b : ℕ, a * a + b * b = p` | **VERIFIED-PRESENT** | Mathlib/NumberTheory/SumTwoSquares.lean:35 `Nat.Prime.sq_add_sq (hp : p % 4 ≠ 3)` — prime case IN the library |

Pilot choice follows the brief's preference (single-session-feasible classical
proof, ~20-line Mathlib exercise). The point is the PIPELINE under test, not
novelty — same genre as FLT: a re-proof of a known theorem, judged by a kernel.

## 4. Kernel verdict — the kernel's own output, verbatim

Final attempt (`lake env lean pilot.lean` from the mathlib root, harness-logged):

```
kernel verdict (verbatim, rc=0, sha256 e3b0c44298fc):
(empty output)
node margin-primes-infinite -> proved (attempt #6 logged, append-only)
```

rc=0 with empty output = compiled clean: no errors, no warnings, **no `sorry`**.
`e3b0c44298fc1c14...` is sha256 of the empty string — that IS the verbatim output;
the hash is recorded on the proved attempt in the DAG.

**Attempt archaeology (the grammar's 7% law, working): 6 attempts logged, 5
kernel runs, 4 rejected — every rejection stays in the graph with its verbatim
error + hash, and every fix came from those errors:**

| # | kind/outcome | verbatim error (truncated) | fix |
|---|---|---|---|
| 1 | state/ok | — | statement stated, artifact staged |
| 2 | kernel/error `7d656e…` | `invalid 'import' command, it must be used in the beginning of the file` | docstring moved below the import |
| 3 | kernel/error `4f5dbb…` | `h1 : sorry` cascade, `unexpected token '+'` | `!` is `scoped notation` in `namespace Nat` (Factorial/Basic.lean:47) → `open Nat` |
| 4 | kernel/error `0ca5d4…` | `Unknown constant Nat.dvd_sub'` | lemma renamed this generation → `Nat.dvd_add_iff_right` (mirror of Infinite.lean's own move) |
| 5 | kernel/error `bc835f…` | application type mismatch on `.2` | explicit parentheses |
| 6 | kernel/**ok** `e3b0c4…` | — (clean) | **proved** |

## 5. Falsifier table (`python -m mag.the_margin demo`)

| F | Claim | Verdict |
|---|---|---|
| F1 | DAG harness deterministic round-trip byte-identical (4806B, sha 43765a6c5362) | **PASS** |
| F2 | append-only attempts never deleted: edit/remove raises `AppendOnlyViolation`, append succeeds (probe on a copy, never the live file) | **PASS** (after a harness-bug fix: the probe originally saved to a nonexistent path, so the guard had nothing to defend — fixed, and the fix is the lesson: a guard against a missing baseline guards nothing) |
| F3 | statement presence honestly classified, VERIFIED always carries a receipt, never conflated with ASSUMED | **PASS** |
| F4 | toolchain status = ground truth from PATH + `~/.elan/bin` probe, evidence verbatim | **PASS** |
| F5 | if kernel ran: verdict is the kernel's own output; proved requires a kernel hash (`e3b0c44298fc…` on attempt #6) | **PASS** |

**OVERALL: PASS.**

## 6. Cost disclosure (honest)

- API/model spend: **$0 external.** One seat (this session), this seat's own
  subscription tokens — no lane fires, no free-lane draws, no flash-worker fans.
- Non-token cost: 7.3G disk (mathlib clone + olean cache), ~4 min cache download,
  6 kernel runs (~30-60s each warm).
- Scale path (SCALE door, post-pilot): the DAG, the runner, and the append-only
  ledger are width-ready; what a 3-seat Vinogradov shape adds is lane workers on
  `next` + cross-seat attempt merges — not yet built, not claimed.

## 7. Verified vs not (tri-state)

- **VERIFIED:** kernel verdict (rc=0, no sorry, output hashed); presence
  classifications (grep, commit-pinned); round-trip + append-only (measured);
  toolchain versions (probe output quoted).
- **SUPPORTED, not chained:** the composite charter's remaining stations —
  artifact knotted into the verkle chain (deliberately NOT done here: brief
  forbids chain writes from this build) and CHORD-SEND (operator hand).
- **UNPROVEN:** nothing on the pilot node — it is `proved` by the kernel's own
  record. The two remaining candidates stay `stated` (open to-do, as designed).

*Curriculum open. Reading continues.*

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-invoked the kernel fresh on the shipped `pilot.lean` (own `lake env lean`
call, absolute-path elan): **rc=0, zero bytes of output** — clean, independent of
the builder's run. Harness `demo` re-run: 5/5 falsifiers PASS, round-trip sha
reproduces (43765a6c5362), toolchain probe verbatim (Lean 4.33.1 / elan 4.2.4 /
Lake 5.0.0), DAG state matches (3 nodes, pilot `proved` with 6 append-only
attempts — four kernel rejections preserved verbatim with their own hashes, one
rejected specifically for containing `sorry`). F2's harness-bug lesson stands: a
guard against a missing baseline guards nothing. Honest scope confirmed: all
three candidates VERIFIED-PRESENT in mathlib — this run proves the PIPELINE, not
novelty; the pipeline is the invention, the statement was the test load. Two
candidates remain `stated`, claimable. VERDICT: PASS. The chain-knot and
CHORD-SEND stations remain, as designed, for the Operator's hand and the
night-close.
