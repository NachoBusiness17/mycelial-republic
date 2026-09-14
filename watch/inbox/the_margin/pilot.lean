import Mathlib.Data.Nat.Prime.Factorial

open Nat

/-!
# THE MARGIN — pilot node `margin-primes-infinite`

B9 build, 2026-09-06. One statement, one seat, staged for scale.

Statement split from intent (Prove2Me grammar): the DAG node in
state/the_margin_dag.json carries this theorem statement as its `statement`
string, verbatim; the proof below is the attempt logged on that node.

HONEST PROVENANCE: the infinitude of the primes is ancient and mathlib
already carries it — `Nat.exists_infinite_primes` (Mathlib/Data/Nat/Prime/
Infinite.lean:33, mathlib4 @ 80cbd0498ab39e21d24d6730b3f932cec672a702).
This file is a fleet-namespace re-derivation, honestly labeled: the artifact
under test is the PIPELINE (statement-DAG -> kernel -> append-only attempt
log), not novelty. Same genre as FLT: a re-proof of a known theorem, judged
by a kernel, not a vibe.

Euclid's factorial form: any prime dividing `n ! + 1` cannot be `<= n`
(it would divide `n !` too, hence `1`), so `(n ! + 1).minFac > n`.
-/

/-- THE MARGIN pilot: Euclid's theorem on the infinitude of the primes,
in the strict form `forall n, exists p > n, p is prime`. -/
theorem margin_infinitude_of_primes : ∀ n : ℕ, ∃ p, n < p ∧ Nat.Prime p := by
  intro n
  have h1 : n ! + 1 ≠ 1 := ne_of_gt (Nat.succ_lt_succ n.factorial_pos)
  have hp : Nat.Prime ((n ! + 1).minFac) := Nat.minFac_prime h1
  refine ⟨(n ! + 1).minFac, ?_, hp⟩
  by_contra hle
  have hle' : (n ! + 1).minFac ≤ n := Nat.le_of_not_gt hle
  have hdvd : (n ! + 1).minFac ∣ n ! :=
    (Nat.Prime.dvd_factorial hp).mpr hle'
  exact hp.not_dvd_one
    ((Nat.dvd_add_iff_right hdvd).2 (Nat.minFac_dvd _))
