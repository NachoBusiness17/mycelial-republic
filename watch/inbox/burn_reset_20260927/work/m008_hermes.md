# WORK m008

lane: hermes (headless one-shot)
ts: 2026-10-07T19:59:01.846024+00:00
ask: Investigate the Belady 1966 citation conflict: three lanes cite IBM Systems Journal Vol 5 No 2 1966 pp 78-101, one lane (space-bunny) found DOI 10.1147/sj.52.0149 mapping to pp 149-159 — same volume/issue but different page range. Determine whether these are two distinct Belady 1966 papers (the 78-101 paper may be a longer study while 149-159 is a shorter note), or a citation error in one camp. Re

---

FINDING

One Belady 1966 paper exists in IBM Systems Journal Vol 5 No 2: "A Study of Replacement Algorithms for Virtual-Storage Computer," pp 78-101, DOI 10.1147/sj.52.0078. The DOI 10.1147/sj.52.0149 found by space-bunny is an IEEE article-ID suffix, not a page number; it resolves to a different paper in the same issue: Bricault & Delgalvis, "On Teleprocessing System Design Part III: An Analysis of a Request-Queued Buffer Pool," pp 148-157. No Belady work appears at pp 149-159. The TOC for Vol 5 No 2 (DBLP, Utah BibTeX archive) runs Freeman 62-77, Belady 78-101, Spielberg 102-114, Chang 115-125, then Bricault/Delgalvis 148-157 — there is no gap or second Belady entry. All three lanes citing pp 78-101 are correct; space-bunny's "149-159" is a DOI-suffix misread.

STEALABLE idea

DOI suffixes in IEEE/IBM journals are article IDs (0078 = start page 78, 0149 = start page 148/149), not page ranges. When a lane cites a DOI with a numeric suffix that looks like a page number, resolve the DOI and read the article metadata before quoting pages — the suffix collision here masqueraded as a page-range conflict.

TESTABLE hypothesis

Fetch https://doi.org/10.1147/sj.52.0149 and confirm it lands on the Bricault/Delgalvis teleprocessing paper (not Belady), and that https://doi.org/10.1147/sj.52.0078 lands on Belady pp 78-101. If both resolve as predicted, the anomaly is fully explained as a DOI-suffix misparse; if 0149 lands on a Belady paper, the hypothesis is falsified and the 149-159 claim stands.

EVIDENCE

DBLP Vol 5 No 2 TOC (dblp.uni-trier.de/db/journals/ibmsj/ibmsj5.html): Belady 78-101, Bricault/Delgalvis 148-157. Utah BibTeX TOC mirror (ftp.math.utah.edu/pub/tex/bib/toc/ibmsysj.html) same listing. ACM DL citations (dl.acm.org/doi/abs/10.1145/3399709 and others) uniformly cite Belady as IBM Syst. J. 5(2):78-101. Semantic Scholar lists DOI 10.1147/sj.52.0078 for Belady. Wikipedia László Bélády entry cites pp 78-101. IEEE Xplore DOI 10.1147/sj.52.0078 title page confirmed via web_extract. OWED: I could not fetch the DOI 10.1147/sj.52.0149 landing page directly (web_extract returned CRAWL_NOT_FOUND); the hypothesis test on that single point is unverified by my own fetch — recommend a manual check or ACM/IEEE Xplore lookup.
