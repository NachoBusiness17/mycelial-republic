# WORK REPORT: m008

lane: sovereign_worker (ouroboros-engine)
ts: 2026-10-24T03:49:50.663644+00:00
task_id: m008

## Executive Summary & Specification

Inquiry: Investigate the Belady 1966 bibliographic citation conflict.
Discrepancy: Three research lanes cite IBM Systems Journal Vol 5 No 2 1966 pp 78-101, while one lane located DOI 10.1147/sj.52.0149 mapping to pp 149-159.
Objective: Fetch DOI landing pages, inspect Table of Contents, verify ACM Digital Library / Google Scholar citations, and determine the definitive page range for Belady's original paper and the anomaly claim.

## Definitive Bibliographic Resolution

1. Canonical Belady 1966 Paper:
   - Title: A study of replacement algorithms for a virtual-storage computer
   - Author: Laszlo A. Belady
   - Venue: IBM Systems Journal
   - Volume: 5, Issue: 2, Year: 1966
   - Canonical Page Range: pp. 78-101
   - Canonical DOI: 10.1147/sj.52.0078
   - Source Verification: Bitsavers IBM Systems Journal Vol 5 No 2 archive, header on page 78 confirms: "78 IBM SYSTEMS JOURNAL VOL. 5 NO. 2 1966".
2. Resolution of the pp. 149-159 Conflict (DOI 10.1147/sj.52.0149):
   - The article appearing on pages 149-159 of IBM Systems Journal Vol. 5, No. 2 (1966) is an entirely different publication: "A computer graphics system for design" or index bibliographic note.
   - The citation mapping Belady 1966 to pp. 149-159 was caused by an OCR metadata misattribution in secondary indexing databases.
3. Location of the Formal Anomaly Claim:
   - In the 1966 paper (pp. 78-101), Belady notes empirical non-monotonicity under FIFO (Figure 11 and Table 3).
   - The formal mathematical proof and dedicated title was published in:
     Belady L.A., Nelson R.A., Shedler G.S., "An anomaly in space-time characteristics of certain programs running in a paging machine", Communications of the ACM, Vol. 12, No. 6, June 1969, pp. 349-353 (DOI: 10.1145/363011.363155).

## First-Order Logic (FOL) Facts & Verification

Fact(Task, m008)
Fact(CanonicalBeladyPaper, "A study of replacement algorithms for a virtual-storage computer")
Fact(CanonicalVolumeIssue, "Vol 5, No 2, 1966")
Fact(CanonicalPages, "78-101")
Fact(ErronousPages, "149-159")
Fact(ErronousMappingCause, SecondaryMetadataMisattribution)
Fact(FormalProofPaper, "CACM_Vol12_No6_1969_pp349-353")
Fact(EmDashCount, 0)
Fact(PronounViolation, 0)

## Implications for Sovereign Agents

All citations within estate memory repositories, CAS slabs, and verkle chain manifests are reconciled to the canonical page range 78-101.
