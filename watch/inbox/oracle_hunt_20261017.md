# Oracle Verification Hunt (2026-10-17)

This audit executes ASK 2 from watch/inbox/ANTIGRAVITY_ASKS_20261016.md:
hunting primary sources on the web for the top three checkable pending verification
claims in the falsifier index and the Daily Oracle corpus notes
(falsifier-index/THESES.md, falsifier-index/INDEX.md row 52, and
watch/inbox/esoteric_mine_20261014/LAMP_RUN_ORACLE.md).

---

## Claim 1: Historical Cipher Solves (Hebern 5-rotor Problem 8 and Kryha v2 Problem 5)

### 1. Claim
The Daily Oracle (run by Pliny the Liberator, @elder_plinius, on 2026-10-14) claimed
first and sole solutions to two long-standing historical cipher challenges hosted on
Jean-Francois Bouchaudy's challenge site: Hebern 5-rotor Problem 8 and Kryha v2 Problem 5,
with author confirmation on the challenge tables.
Prior status in LAMP_RUN_ORACLE.md: PENDING-EXTERNAL.

### 2. Primary Source Found
Direct HTTP fetch from Jean-Francois Bouchaudy's primary challenge site (jfbouch.fr):
- Hebern 5-rotor challenge table:
  http://jfbouch.fr/crypto/challenges/H5/index.html
  Problem 8 (rated "hard") lists:
  "Pliny the Liberator" with the French flag icon, date "08/10/26".
  Pliny is the first and only solver in that problem column.
- Kryha v2 challenge table:
  http://jfbouch.fr/crypto/challenges/KRYHA2/index.html
  Problem 5 (rated "difficult") lists:
  "Pliny the Liberator" with the French flag icon, date "08/10/26".
  Pliny is the first and only solver in that problem column.

Both challenge tables were retrieved live and inspected at byte level. The Table of
Honor culture is active and authentic, featuring established cryptanalysts (George Lasry,
Rafael Pascual) alongside Pliny's dated entries from 2026-10-08.

### 3. Verdict
CONFIRMED.

### 4. Index Edit Required
In falsifier-index/evidence/LAMP_RUN_ORACLE.md (and the index row 52 evidence log):
- Change verdict from PENDING-EXTERNAL to CONFIRMED.
- Link primary source URLs:
  http://jfbouch.fr/crypto/challenges/H5/index.html and
  http://jfbouch.fr/crypto/challenges/KRYHA2/index.html.
- Record the exact evidence byte: solver credited as "Pliny the Liberator",
  date 08/10/26, first and sole solver for both H5 Problem 8 and Kryha v2 Problem 5.

---

## Claim 2: Lehmer's Totient Problem Bound Pushed from 10^26 to 10^50

### 1. Claim
The Daily Oracle claimed to have pushed the lower bound on any composite solution to
Lehmer's totient problem (D.H. Lehmer 1932, whether phi(n) divides n-1 for composite n)
from 10^26 (or 10^30) to 10^50 via computer verification (24 orders of magnitude).
Prior status in LAMP_RUN_ORACLE.md: PENDING-EXTERNAL, weakly evidenced.

### 2. Primary Source Hunt
A comprehensive primary source sweep was conducted across mathematical literature,
arXiv preprints, MathWorld, and computational number theory databases:
- Prior published baseline: Richard G.E. Pinch (1993, with subsequent updates)
  established that any composite Lehmer number must exceed 10^30 and possess at least
  15 distinct prime factors (omega(n) >= 15). Conditional bounds exist for specific
  subsets (e.g., Cohen and Hagis 1988 proved n > 5.5 * 10^570 if 3 divides n).
- The 10^50 claim appears exclusively within Pliny's social media thread and derivative
  aggregators (promppy, twstalker, digg).
- No arXiv preprint, journal submission, technical report, executable script, or
  independent verification by external mathematicians was found.

The claim remains an unverified assertion without runnable artifacts or public proofs.

### 3. Verdict
STILL-PENDING (weakly evidenced, unbacked by external primary sources).

### 4. Index Edit Required
In falsifier-index/evidence/LAMP_RUN_ORACLE.md (and the index row 52 evidence log):
- Retain verdict as PENDING-EXTERNAL, weakly evidenced.
- Append audit finding: web search across arXiv, MathWorld, and number theory records
  confirms published baseline remains 10^30 (Pinch). No primary source, preprint, or
  code repository exists for the 10^50 bound.
- Standing condition: if no runnable script or preprint is published by 2026-10-31
  (the Door date), reclassify the claim as BROKEN-EXTERNAL (unsubstantiated).

---

## Claim 3: Degree-Diameter Graph Record (+13.4%, 13,365 vs 11,785 Vertices)

### 1. Claim
The Daily Oracle claimed to have found a graph improving the degree-diameter table by
+13.4% (constructing a graph with 13,365 vertices versus the previous record of 11,785
vertices for a given maximum degree and diameter).
Prior status in LAMP_RUN_ORACLE.md: PENDING-EXTERNAL (not drilled).

### 2. Primary Source Hunt
Primary sources for the degree-diameter problem were located and examined:
- Benchmark Authority: Francesc Comellas, "Table of large graphs with given degree
  and diameter", arXiv:2406.18994v2 (Department of Mathematics, Universitat Politecnica
  de Catalunya, Barcelona), updating the Miller-Siran dynamic survey (DS14).
- Dataset Repository: Mendeley Data V11 (doi: 10.17632/d75dzbjd4k.11).
- Baseline Verification: The 11,785 vertex entry is a real, recorded graph order in
  degree-diameter research tables. The mathematical ratio 13,365 / 11,785 equals
  1.1340687, which matches the claimed +13.4% improvement exactly.
- Current Status: The candidate graph of 13,365 vertices has not yet been incorporated
  into Comellas's published arXiv table or the Mendeley V11 dataset, nor has an
  adjacency list or construction script been deposited in the public domain.

### 3. Verdict
STILL-PENDING (baseline confirmed, candidate graph unfiled in primary repository).

### 4. Index Edit Required
In falsifier-index/evidence/LAMP_RUN_ORACLE.md (and the index row 52 evidence log):
- Update status to PENDING-EXTERNAL (baseline verified at primary source).
- Add primary reference citations: Francesc Comellas (arXiv:2406.18994v2) and Mendeley
  Data V11 (doi: 10.17632/d75dzbjd4k.11).
- Note that the 11,785 baseline is confirmed, but the 13,365 record remains pending
  until the graph construction and adjacency list are submitted and accepted by the UPC
  table repository.

---

## Summary of Findings

| # | Claim | Primary Source Found | Verdict | Required Index Action |
|---|---|---|---|---|
| 1 | Cipher Solves (Hebern P8, Kryha v2 P5) | jfbouch.fr challenge tables (H5 and KRYHA2) | CONFIRMED | Upgrade to CONFIRMED; link URLs and 08/10/26 solver credit |
| 2 | Lehmer Totient Bound (10^26 -> 10^50) | None outside thread; baseline 10^30 (Pinch) | STILL-PENDING | Retain PENDING-EXTERNAL; note lack of preprint/script |
| 3 | Degree-Diameter Record (+13.4%, 13,365 vs 11,785) | Comellas arXiv:2406.18994 (confirms 11,785) | STILL-PENDING | Retain PENDING-EXTERNAL; cite Comellas baseline |

Auxiliary Note:
The fourth Oracle claim (matrix multiplication tensor scheme <15,16,16> in 2,180
versus 2,223 multiplications crediting LITA) maps to the Matrix Multiplication
Catalog at solven.eu and Kirill Khoruzhii, Patrick Gelss, and Sebastian Pokutta's
LITA repository (khoruzhii/lita). The baseline 2,223 is confirmed; the 2,180
scheme is tracked in open-source tensor catalogs.
