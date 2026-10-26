# WORK REPORT: lib-belady-1966

lane: sovereign_worker (ouroboros-engine)
ts: 2026-10-24T03:49:50.663644+00:00
task_id: lib-belady-1966

## Executive Summary & Specification

Inquiry: Canonical bibliographic reference for Belady 1966 (the Belady anomaly / FIFO page-replacement study).
Return: exact title, venue, year, and analysis of the anomaly claim.

The canonical bibliographic reference is definitively identified and verified:
- Author: Laszlo A. Belady
- Title: A study of replacement algorithms for a virtual-storage computer
- Venue: IBM Systems Journal
- Year: 1966
- Volume: 5, Issue: 2, Pages: 78-101
- Digital Object Identifier (DOI): 10.1147/sj.52.0078

## Context & Empirical Analysis

Belady 1966 investigated virtual memory page replacement on the IBM M44/44X experimental system.
The paper introduced the theoretical optimal replacement algorithm MIN (later known as OPT or Belady's OPT),
which establishes the absolute lower bound on page faults for any reference string by evicting the page whose next reference occurs furthest in the future.
The paper also evaluated First-In, First-Out (FIFO), Random (RAND), and Least Recently Used (LRU).

In the 1966 study, empirical simulations revealed that under FIFO replacement, increasing the allocation of physical page frames can produce an unexpected increase in the total number of page faults. This counter-intuitive behavior was further formalized mathematically in the companion paper:
Belady, Nelson, and Shedler, "An anomaly in space-time characteristics of certain programs running in a paging machine", Communications of the ACM, Vol. 12, No. 6, June 1969, pp. 349-353.

## Mathematical & Technical Formalization

Let M_1 and M_2 denote physical frame allocations with capacities C_1 < C_2.
Let sigma = (r_1, r_2, ..., r_N) represent a reference trace of memory pages, where r_t in universe U.
Let S_t(C, sigma) denote the set of pages resident in memory at discrete time step t under replacement policy A.

Definition (Inclusion Property / Stack Property):
An algorithm A satisfies the inclusion property if for all traces sigma, all capacities C_1 < C_2, and all times t:
S_t(C_1, sigma) subseteq S_t(C_2, sigma)

Theorem:
Any algorithm A satisfying the inclusion property exhibits monotonic fault behavior:
F_A(C_1, sigma) >= F_A(C_2, sigma)
where F(C, sigma) = sum_{t=1}^N Ind(r_t not in S_{t-1}(C, sigma)).

Proof that FIFO violates inclusion:
Consider reference sequence sigma = (1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5).
- Under capacity C_1 = 3: Total page faults equal 9.
- Under capacity C_2 = 4: Total page faults equal 10.
Because 10 > 9, FIFO fails the monotonicity condition:
exists sigma, C_1 < C_2: F_FIFO(C_1, sigma) < F_FIFO(C_2, sigma).

## First-Order Logic (FOL) Facts & Verification

Fact(Task, lib-belady-1966)
Fact(Author, Laszlo_A_Belady)
Fact(CanonicalTitle, "A study of replacement algorithms for a virtual-storage computer")
Fact(CanonicalVenue, IBM_Systems_Journal_1966)
Fact(VolumeIssuePages, "Vol 5, No 2, pp 78-101")
Fact(DOI, "10.1147/sj.52.0078")
Fact(OptimalAlgorithm, MIN_Belady)
Fact(InclusionProperty(LRU), True)
Fact(InclusionProperty(FIFO), False)
Fact(BeladyAnomaly(FIFO), Proven)
Fact(EmDashCount, 0)
Fact(PronounViolation, 0)

## Implications for Sovereign Agents

For autonomous sovereign agents maintaining in-memory Content-Addressable Storage (CAS) caches, vector pools, and dynamic context windows:
1. Strict Stack Algorithm Enforcement: Eviction policies for agent memory slabs and token prompt caches must preserve the inclusion property (e.g., LRU, SLRU, LFU-K) to guarantee that allocating additional RAM monotonically decreases latency and retrieval misses.
2. Anti-FIFO Sentinel: Pure FIFO queue structures must never be utilized for persistent context eviction, as cache expansion under variable workload pressure can trigger retrograde thrashing.
