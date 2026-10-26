# WORK m009

lane: hermes (headless one-shot)
ts: 2026-10-07T21:20:26.024994+00:00
ask: Investigate the citation collision between the two Mattson 1970 IBM Systems Journal papers: 'Evaluation Techniques for Storage Hierarchies' (vol.9 no.2, the stack-distance source) and 'Evaluation of Multi-Programmed Batch Systems' (vol.9 no.3, a different paper). Search Google Scholar, DBLP, and Semantic Scholar for papers that cite 'Mattson 1970' for stack distance / LRU / reuse distance and chec

---

All searches complete. Synthesizing the citation-collision report.

---

FINDING: The citation collision the user described does not exist in the verifiable record. The premise contains a phantom paper.

(1) FINDING

DBLP (dblp.org/db/journals/ibmsj/ibmsj9.html) lists IBM Systems Journal Vol.9 (1970) as:
  - No.1: Darga, Quarles, Newitt/Odarchenko, Wei Chang
  - No.2: **Mattson, Gecsei, Slutz, Traiger — "Evaluation Techniques for Storage Hierarchies", pp.78-117** (DOI 10.1147/sj.92.0078) — the stack-distance paper — plus Woodrum, Jacobs/Dillon
  - No.3: Elson/Rake, Ryder, Meyer/Seawright, Luetje — **no Mattson paper**

There is only ONE Mattson 1970 paper in IBM Systems Journal. The claimed second paper ("Evaluation of Multi-Programmed Batch Systems", vol.9 no.3) does not appear in DBLP, and the title matches no record I could find across Google Scholar, Semantic Scholar, or ACM DL.

DOI 10.1147/sj.93.206 does not resolve to a paper (doi.org returned "Not found"; the same DOI pattern with .0199 resolves to Meyer/Seawright "A Virtual Machine Time-Sharing System" pp.199-218, which is about time-sharing, not stack distance). Page 206 falls inside that non-Mattson paper.

Semantic Scholar lists the correct paper at DOI 10.1147/sj.92.0078 with 1,400 citations.

(2) STEALABLE IDEA

The real citation trap here is the *title ambiguity* between Mattson et al. 1970 ("Evaluation Techniques for Storage Hierarchies") and Belady 1966 ("A Study of Replacement Algorithms for a Virtual Storage Computer", IBM SJ vol.5 no.2) — both cover replacement algorithms in the same journal, and both get cited as "IBM Systems Journal 1970" by lazy referencers. The fix: always cite by DOI + page range, not by year+journal alone. The vol.9 no.2 vs no.3 split is a red herring; the real collision is across different volumes/years.

(3) TESTABLE HYPOTHESIS

Hypothesis: among the 1,400 Semantic Scholar citations of Mattson et al. 1970, fewer than 1% cite the wrong volume/issue (i.e., vol.9 no.3 or a non-existent Mattson batch-systems paper). Test: pull the full citation list from Semantic Scholar API for Corpus ID 8989304, filter for references containing "9(3)" or "batch systems" or "10.1147/sj.93", count mismatches. If zero, the collision is a phantom.

(4) EVIDENCE / OWED

Evidence gathered:
- DBLP Vol.9 listing (confirmed no Mattson paper in no.3)
- Semantic Scholar entry for Corpus ID 8989304 (DOI 10.1147/sj.92.0078, 1,400 citations)
- ACM DL entry for DOI 10.1147/sj.92.0078 (correct vol.9 no.2 pp.78-117)
- Bitsavers PDF of the full paper (stack-distance method confirmed)
- Rochester CS course notes, Chen Ding reuse-distance report, PATMOS paper, patent EC255FEC — all cite the CORRECT paper with full vol.9 no.2 reference
- DOI 10.1147/sj.93.206 returns "Not found" on doi.org
- Zero papers found citing "Mattson 1970" for stack distance that point to vol.9 no.3

OWED: I could not run the Semantic Scholar API pull to count the full 1,400-citation corpus for wrong-volume mismatches (no API key in this session). The hypothesis in (3) needs that automated check for a definitive count. Also, I did not find a physical/digital copy of IBM Systems Journal vol.9 no.3 to confirm the table of contents beyond DBLP — the DBLP listing is the best available authoritative source for this.
