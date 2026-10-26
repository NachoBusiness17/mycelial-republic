# r-belady-lruk: canonical refs for Belady 1966 FIFO anomaly, Mattson 1970 stack distance, LRU-K (O'Neil 1993)

Date: 2026-09-28. Every claim below names what I read or ran in this session. No em-dashes anywhere, per law.

## 1. Belady 1966 (FIFO anomaly)

**Citation (Crossref-verified, `api.crossref.org/works/10.1147/sj.52.0078`):**
L. A. Belady, "A study of replacement algorithms for a virtual-storage computer", *IBM Systems Journal*, vol. 5, no. 2, pp. 78-101, 1966. DOI 10.1147/sj.52.0078.

**Primary-source verification:** downloaded the scan `http://bitsavers.informatik.uni-stuttgart.de/pdf/ibm/IBM_Systems_Journal/052/belady.pdf` (24 pages) and read it page by page: title page shows the title, "by L. A. Belady", and footer "78 IBM SYSTEMS JOURNAL * VOL. 5 * NO. 2 . 1966"; last text page is journal p.101. Crossref agrees on 5(2):78-101, 1966.

**Defining quote (verbatim, journal p.83, from pypdf text extraction of the scan, lines 227-229 of belady1966.txt):**

> FIFO always replaces the block having spent the longest time in memory.

**Second verified quote (Summary comment, journal p.100):**

> In some cases, too much reliance on cumulative information actually resulted in lower efficiency.

**Anomaly status, stated exactly:** the word "anomaly" does NOT occur anywhere in the 1966 paper's prose. I grepped the full pypdf text layer for "anomal", "more faults", "faults.*increase", "patholog", "perverse", "paradox" (zero hits), and I rendered and visually read every page whose OCR text layer was blank (PDF pages 2, 3, 12, 19, 20, 21, 22, 23, 24 = journal pages 79, 80, 89, 96, 97, 98, 99, 100, 101). The counterintuitive FIFO behavior the paper is remembered for appears graphically in Figure 13, "Efficiency bounds of algorithms for a wide range of memory sizes" (journal p.98), where the FIFO upper-bound curve of replacement efficiency visibly sags as the parameter range widens, not as an explicit sentence.

**The paper that says "anomaly" out loud (Crossref-verified, `api.crossref.org/works/10.1145/363011.363155`):**
L. A. Belady, R. A. Nelson, G. S. Shedler, "An anomaly in space-time characteristics of certain programs running in a paging machine", *Communications of the ACM*, vol. 12, no. 6, pp. 349-353, June 1969. DOI 10.1145/363011.363155. All three authors at IBM Thomas J. Watson Research Center. Independently cross-checked: this exact reference (mangled by OCR as "spare-time") is item 18 in the bibliography of Mattson et al. 1970, which I read in the same session (tail of mattson1970.txt).

**OWED:** a verbatim "more memory causes more page faults" sentence from Belady 1966 itself. The full text I hold (all 24 pages: OCR plus rendered images of the blank-OCR pages) does not contain one; if such a sentence exists in the paper I did not find it, and I will not invent it.

## 2. Mattson 1970 (stack distance)

**Citation (Crossref-verified, `api.crossref.org/works/10.1147/sj.92.0078`):**
R. L. Mattson, J. Gecsei, D. R. Slutz, I. L. Traiger, "Evaluation techniques for storage hierarchies", *IBM Systems Journal*, vol. 9, no. 2, pp. 78-117, 1970. DOI 10.1147/sj.92.0078.

**Primary-source verification:** downloaded `http://bitsavers.informatik.uni-stuttgart.de/pdf/ibm/IBM_Systems_Journal/092/ibmsj0902B.pdf` (40 pages). Title page reads "Evaluation techniques for storage hierarchies" with byline (footer of p.1: "MATTSON, GECSEI, SLUTZ, AND TRAIGER IBM SYST J"); last page footer: "NO. 2 . 1970 STORAGE HIERARCHY EVALUATION 117". Crossref agrees on 9(2):78-117, 1970.

**Defining quote (journal p.86; page rendered to image at 150 dpi and read visually, so subscripts are trustworthy):**

> We call this page position the *stack distance* Δ<sub>t</sub>, since Δ<sub>t</sub> is essentially the "distance" from the top of the stack to [ x<sub>t</sub> = s<sub>t-1</sub>(Δ<sub>t</sub>) ].

The sentence closes with the displayed equation, shown in brackets here. Same page, also verbatim:

> The significance of stack distances is that they lead directly to the success function.

**Abstract quote (journal p.78, OCR text layer; the "ff" ligature OCR renders as "efJicient" and is normalized to "efficient" here, noted as such):**

> This paper describes a new and efficient method of determining, in one pass of an address trace, performance measures for a large class of demand-paged, multilevel storage systems utilizing a variety of mapping schemes and replacement algorithms.

**Why it matters (same abstract, verbatim):** "The technique depends on an algorithm classification, called 'stack algorithms,' examples of which are 'least frequently used,' 'least recently used,' 'optimal,' and 'random replacement' algorithms." This is the inclusion-property result: one pass over a trace yields miss/success curves for every buffer size at once.

**Not verified this session:** full given names of the four authors. Crossref lists initials only (R.L., J., D.R., I.L.); the scan byline also uses initials. The commonly given full names (Richard L. Mattson, Jacques Gecsei, Donald R. Slutz, Irving L. Traiger) are plausible but unverified here, so I do not assert them.

## 3. LRU-K (O'Neil, O'Neil, Weikum 1993)

**Citation (Crossref-verified, `api.crossref.org/works/10.1145/170035.170081`):**
E. J. O'Neil, P. E. O'Neil, G. Weikum, "The LRU-K page replacement algorithm for database disk buffering", *Proceedings of the 1993 ACM SIGMOD international conference on Management of Data* (SIGMOD '93), Washington, D.C., pp. 297-306, June 1993. Proceedings DOI 10.1145/170035.170081; journal version in *ACM SIGMOD Record* 22(2):297-306, June 1993, DOI 10.1145/170036.170081 (both Crossref-checked).

**Defining quote (paper abstract, verbatim; reconstructed from OpenAlex `W2054308357` abstract_inverted_index and independently confirmed against the Crossref abstract on DOI 10.1145/170035.170081, which matches word for word):**

> The basic idea of LRU-K is to keep track of the times of the last K references to popular database pages, using this information to statistically estimate the interarrival times of references on a page by page basis.

**Full abstract opening (same two-source verification):**

> This paper introduces a new approach to database disk buffering, called the LRU-K method.

**Venue corroboration from the author's own hand:** Patrick O'Neil's publications page (`https://www.cs.umb.edu/~poneil/publist.html`, fetched this session) lists it as "Presented at ACM SIGMOD Conference, May 1993, Washington, D.C, Proceedings pp. 296-306". Note the discrepancy: the author's page says pp. 296-306, Crossref and OpenAlex both say pp. 297-306. I report 297-306 as canonical (two independent bibliographic indexes agree; the author's hand-maintained HTML disagrees and I flag it, not resolve it).

**OWED:** the paper's introduction contains the stronger claim often quoted as "LRU-K provides strong, non-adaptive real-time guarantees in the face of pathological access patterns." I could NOT verify that sentence verbatim this session: ACM DL is Cloudflare-blocked, archive.org was temporarily offline during this ask (its CDX and availability endpoints returned "Temporarily Offline"), the author's `lru-k.ps` and four sibling paths return 404 on cs.umb.edu, and the Semantic Scholar API returned 429 on every attempt. The abstract quote above is the verified one; treat the intro "guarantees" phrasing as unverified until the full text is accessible.

## Evidence trail (what I ran)

- `curl -s -o belady1966.pdf http://bitsavers.informatik.uni-stuttgart.de/pdf/ibm/IBM_Systems_Journal/052/belady.pdf` (24 pp) and `.../092/ibmsj0902B.pdf` (40 pp), plus `.../052/ibmsj0502B.pdf` (checked and rejected: it is the D. N. Freeman macro-language paper, not Belady).
- Text extraction: repo venv `.venv/Scripts/python.exe` with pypdf `PdfReader`/`extract_text` into belady1966.txt (41 KB), mattson1970.txt (82 KB); greps for "anomal", "fifo", "stack distance", "increas".
- Image rendering of blank-OCR pages: pymupdf installed to a temp target dir (`pip install --target .../flash50/pylibs pymupdf`, repo venv untouched), rendered at 150 dpi and read visually: belady PDF pages 2, 3, 12, 18-24; mattson PDF page 9 (journal p.86).
- Bibliographic API GETs (all this session): `api.crossref.org/works/10.1147/sj.52.0078`, `.../10.1147/sj.92.0078`, `.../10.1145/170035.170081`, `.../10.1145/170036.170081`, `.../10.1145/363011.363155`, `api.openalex.org/works/W2054308357`, `api.openalex.org/works?filter=title.search:LRU-K page replacement algorithm`.
- Fetched `https://www.cs.umb.edu/~poneil/publist.html` (LRU-K entry, pp. 296-306 discrepancy, lru-k.ps link is dead).
- Blocked and reported as blocked, not faked: dl.acm.org (Cloudflare challenge), archive.org (offline), Semantic Scholar API (429 x4), fatcat API (connection dead), OpenAlex DOI:10.1145/191839.191876 (404; the working DOIs are the two above).
- Cleanup: two junk artifacts my first command created in the repo root (`C:UsersfosteAppDataLocalTempflash50/` empty dir, `nul` empty file) were deleted immediately; `ls` confirmed zero remaining. Files under `%TEMP%\flash50` (PDFs, PNGs, JSON) are left in OS temp.

## One-line summary

Belady 1966 IBM SJ 5(2):78-101 (FIFO defined verbatim on p.83, anomaly shown in Fig 13 not named), named-out-loud anomaly is Belady/Nelson/Shedler CACM 12(6):349-353 1969; Mattson/Gecsei/Slutz/Traiger 1970 IBM SJ 9(2):78-117 gives stack distance verbatim on p.86; O'Neil/O'Neil/Weikum SIGMOD '93 pp. 297-306 gives LRU-K, abstract quote verified against OpenAlex + Crossref.
