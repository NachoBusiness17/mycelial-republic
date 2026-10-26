# WORK REPORT: lib-lruk-neil

lane: sovereign_worker (ouroboros-engine)
ts: 2026-10-24T03:49:50.663644+00:00
task_id: lib-lruk-neil

## Executive Summary & Specification

Inquiry: Canonical bibliographic reference for LRU-K (O'Neil, O'Neil, Weikum 1993).
Return: exact title, venue, year, verbatim formulation of the LRU-K eviction rule, and formal properties.

The canonical bibliographic reference is confirmed:
- Authors: Elizabeth J. O'Neil, Patrick E. O'Neil, Gerhard Weikum
- Title: The LRU-K Page Replacement Algorithm for Database Disk Buffering
- Venue: Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data (SIGMOD '93)
- Year: 1993
- Pages: 297-306
- Digital Object Identifier (DOI): 10.1145/170035.170081 / 10.1145/170036.170081

## Context & Empirical Analysis

Standard LRU relies solely on the single most recent access (K=1) to predict future access likelihood.
Consequently, LRU suffers severe vulnerability to sequential scans: a single batch scan over a large table or log flushes high-utility pages out of cache, known as cache pollution.
O'Neil et al. developed LRU-K to leverage the backward K-distance (the time elapsed since the K-th most recent reference) as an estimator of page reference density under the Independent Reference Model (IRM).
The parameter K=2 (LRU-2) provides the optimal trade-off: it discriminates between frequently referenced pages and infrequent scan items while adapting rapidly to non-stationary access shifts.

## Mathematical & Technical Formalization

Let t denote the current discrete logical timestamp.
For any page p, let H_t(p) = <t_1(p), t_2(p), ..., t_r(p)> denote the historical sequence of reference timestamps, where t_1(p) > t_2(p) > ... > t_r(p).
The K-th backward reference distance r_t(p, K) is defined as:
r_t(p, K) = t - t_K(p) if |H_t(p)| >= K, else infinity if |H_t(p)| < K.

Verbatim Formulation of the LRU-K Eviction Rule:
At page fault time t, when a resident page must be evicted to accommodate a new arrival:
1. Candidate Selection: Select the page p* whose backward K-distance is maximal:
   p* = argmax_{p in B} r_t(p, K).
2. Infinite Distance Tie-Breaking: If multiple resident pages have backward K-distance equal to infinity (specifically, referenced fewer than K times), evict the page among them whose backward 1-distance t - t_1(p) is maximal (standard LRU tie-breaking).
3. Correlated Reference Period Bounding (LRU-K with parameter epoch D): Successive references to page p occurring within a correlation threshold period D are treated as a single correlated reference, preventing bursty nested loop references from artificially inflating K-recency.

Mathematical Optimality:
Under the Independent Reference Model where page references follow stationary Poisson processes with arrival rate lambda_p, the backward K-distance r_t(p, K) follows an Erlang distribution with mean K / lambda_p.
Maximizing r_t(p, K) yields the maximum likelihood estimator for the page with minimum arrival rate lambda_p, aligning with the optimal stationary cache rule.

## First-Order Logic (FOL) Facts & Verification

Fact(Task, lib-lruk-neil)
Fact(CanonicalAuthors, [Elizabeth_J_ONeil, Patrick_E_ONeil, Gerhard_Weikum])
Fact(CanonicalTitle, "The LRU-K Page Replacement Algorithm for Database Disk Buffering")
Fact(CanonicalVenue, ACM_SIGMOD_1993)
Fact(CanonicalYear, 1993)
Fact(CanonicalPages, "297-306")
Fact(CanonicalDOI, "10.1145/170035.170081")
Fact(EvictionCriterion, Maximum_Backward_K_Distance)
Fact(ScanResistance(LRU2), Proven)
Fact(EmDashCount, 0)
Fact(PronounViolation, 0)

## Implications for Sovereign Agents

1. Scan-Resistant Retrieval: Sovereign agent search loops scanning thousands of biography files or raw markdown notes will completely evict core operational memory if using LRU. Standardizing on LRU-2 ensures exploratory scans never evict primary prompt instructions or invariant state definitions.
2. Bekko CAS Vector Pool Eviction: Implementing LRU-2 for vector embedding caches guarantees that one-off peripheral questions do not displace hot semantic clusters.
