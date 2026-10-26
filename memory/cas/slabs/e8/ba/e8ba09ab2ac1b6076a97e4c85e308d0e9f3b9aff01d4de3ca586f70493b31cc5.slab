# WORK m008

lane: openrouter model: meta/muse-glimmer-30b
ts: 2026-10-07T20:16:19.136682+00:00
finish: stop cached_tokens: 32
ask: Investigate the Belady 1966 citation conflict: three lanes cite IBM Systems Journal Vol 5 No 2 1966 pp 78-101, one lane (space-bunny) found DOI 10.1147/sj.52.0149 mapping to pp 149-159 — same volume/issue but different page range. Determine whether these are two distinct Belady 1966 papers (the 78-101 paper may be a longer study while 149-159 is a shorter note), or a citation error in one camp. Re

---

(1) FINDING
Unable to definitively resolve the Belady 1966 page-range conflict from offline knowledge alone. The canonical work most cited as Belady 1966 is “A Study of Replacement Algorithms for a Virtual-Storage Computer”, IBM Systems Journal Vol 5 No 2 1966 pp 78-101. The DOI 10.1147/sj.52.0149 is assigned by IBM to IBM Systems Journal 5, 2, and the DOI suffix 52.0149 is consistent with issue 5-2 article 149. I could not verify in this session whether pp 149-159 in the same issue is a second distinct Belady 1966 paper, a reprint/erratum, or a citation error propagated by the space-bunny lane. Live fetch of the DOI landing page and the Vol 5 No 2 Table of Contents is required to confirm titles and page ranges.

(2) STEALABLE idea worth keeping
Treat DOI + volume/issue/page triple as a primary key for citation de-duplication. When a conflict arises, force a live lookup of the DOI resolver and the journal TOC for that volume/issue and record title, start page, end page, and article number. This prevents propagating a page-range mismatch across lanes.

(3) TESTABLE hypothesis
Hypothesis: DOI 10.1147/sj.52.0149 resolves to a different Belady 1966 item than pp 78-101, e.g. a short note “Optimal Strategies for a Virtual Storage Computer” or an editorial reprint, and the space-bunny lane conflated the two. Test by fetching https://doi.org/10.1147/sj.52.0149 and comparing its metadata title/pages to the IBM Systems Journal Vol 5 No 2 TOC entries for pp 78-101 and pp 149-159.

(4) EVIDENCE or OWED
EVIDENCE: none verified in this session. 
OWED: 
- DOI 10.1147/sj.52.0149 landing page title, author list, page range, and PDF metadata
- IBM Systems Journal Vol 5 No 2 1966 official Table of Contents showing article titles for pp 78-101 and pp 149-159
- Google Scholar / ACM DL records confirming distinct Belady 1966 works with those page ranges
- Verbatim-quote source for the OWED quote across lanes

No sources cited.
