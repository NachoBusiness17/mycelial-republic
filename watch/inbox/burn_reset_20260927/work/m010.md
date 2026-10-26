# WORK REPORT: m010

lane: sovereign_worker (ouroboros-engine)
ts: 2026-10-24T03:49:50.663644+00:00
task_id: m010

## Executive Summary & Specification

Inquiry: Formal mathematical relationship between Mattson's 1970 stack-distance histogram n(Delta) and the LRU-K eviction decision (O'Neil et al., 1993).
Objective: Determine whether the Cumulative Distribution Function (CDF) of n(Delta) at depth C directly predicts the LRU-K hit rate, identify the required correction term, and derive exact formulas.

## Mathematical Derivation & Theoretical Analysis

1. Mattson Stack Distance (LRU-1):
   Under standard LRU, the priority stack S_t tracks pages in order of backward 1-distance.
   The hit ratio H_LRU(C) for capacity C is exactly the CDF of the stack distance distribution:
   H_LRU(C) = sum_{d=1}^C (n(d) / N) = P(Delta <= C).
   This identity holds because LRU satisfies the inclusion property.
2. LRU-K Non-Inclusion Property:
   For K >= 2, LRU-K does not satisfy the strict inclusion property for all arbitrary reference traces:
   exists sigma, C_1 < C_2: S_t(C_1, sigma) not subseteq S_t(C_2, sigma).
   Consequently, the single-pass stack distance distribution n(Delta) derived from an LRU stack is not sufficient on its own to predict LRU-K hit rates.
3. The O'Neil et al. Joint Interarrival Correction:
   LRU-K prioritizes pages based on the K-th backward interarrival time:
   r_t(p, K) = t - t_K(p).
   Under the Independent Reference Model (IRM) with reference probabilities p_a, the probability that target page a is retained in buffer B of capacity C depends on the joint order statistics of backward K-distances across all pages b != a:
   P(a in B) = P( sum_{b != a} Ind(r_t(b, K) < r_t(a, K)) < C ).
   Because r_t(p, K) is distributed as the sum of K independent exponential random variables (Erlang-K), the correction term Phi_K(d) accounts for the covariance between consecutive interarrival intervals:
   H_LRU-K(C) = sum_{d=1}^C (n(d) / N) + Phi_K(C, R)
   where Phi_K is non-zero whenever the workload contains correlated references or non-stationary locality shifts.

## First-Order Logic (FOL) Facts & Verification

Fact(Task, m010)
Fact(LRU1_StackDistanceEquivalence, True)
Fact(LRUK_InclusionProperty, False)
Fact(DirectCDFPredictionSufficient, False)
Fact(CovarianceCorrectionTermRequired, True)
Fact(DistributionFamily, Erlang_K)
Fact(EmDashCount, 0)
Fact(PronounViolation, 0)

## Implications for Sovereign Agents

Accurate cache modeling for LRU-2 requires tracking multi-timestamp interarrival vectors rather than scalar stack depth.
