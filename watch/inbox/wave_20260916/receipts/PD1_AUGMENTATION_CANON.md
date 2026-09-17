# PD1 — AUGMENTATION CANON (receipt)

- Wave: `wave_20260916` · Lane: **PD1**
- Law: receipt FIRST, append as you go. **No git.** Free + legal fetches only (founding primary documents, institution-hosted).
- Durable write roots: canon + manifest → `memory/corpus/augmentation_canon/` · this receipt → `watch/inbox/wave_20260916/receipts/`
- Manifest contract: `memory/corpus/augmentation_canon/manifest.jsonl` — one JSON line per document: `{url,file,sha256,title,year}`
- Every copy is byte-verified (loads + content check) before manifesting. `sha256sum` over saved bytes.
- Executor: ZCode subagent (Mag harness seat), 2026-09-16.

## Targets (founding canon of computing-as-augmentation)

1. Vannevar Bush — "As We May Think", The Atlantic Monthly, July 1945
2. J.C.R. Licklider — "Man-Computer Symbiosis", IRE Trans. Human Factors in Electronics, HFE-1, 1960
3. J.C.R. Licklider — "Libraries of the Future", MIT Press, 1965
4. Douglas C. Engelbart — "Augmenting Human Intellect: A Conceptual Framework", SRI Summary Report AFOSR-3233, 1962
5. "The Mother of All Demos" — Engelbart's 1968 Fall Joint Computer Conference demonstration (video/transcript page)
6. A. M. Turing — "Computing Machinery and Intelligence", Mind LIX(236), 1950
7. Claude E. Shannon — "A Mathematical Theory of Communication", Bell System Technical Journal, 1948
8. W. Ross Ashby — "An Introduction to Cybernetics", 1956 (free institutional mirror)

## Fetch log

*(appended per document, receipt as it goes)*

### [1] Vannevar Bush — As We May Think (1945) — FETCHED
- URL: https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/ (the Atlantic's own site)
- File: memory/corpus/augmentation_canon/bush_as_we_may_think_1945.html
- Bytes: 236,743 · HTTP 200 · sha256: `4b86cb68387fde481cfd691557c44b198054f976f51a9c9f8ed369ea53504e4d`
- Verified: full text markers present — "memex" x22, "trail" x58, "trail blazers" x2, "associative indexing" x2.

### [7] Claude E. Shannon — A Mathematical Theory of Communication (1948) — FETCHED
- URL: https://web.archive.org/web/20110708025307/http://cm.bell-labs.com/cm/ms/what/shannonday/shannon1948.pdf (archived copy of Bell Labs' own shannonday PDF; live cm.bell-labs.com and math.harvard.edu mirrors unreachable from this seat)
- File: memory/corpus/augmentation_canon/shannon_mathematical_theory_of_communication_1948.pdf
- Bytes: 366,296 · HTTP 200 · sha256: `6e4e3411984f3edf99dbfe8b941cb5e8a321379ff0cae6ae5c1f592ad8882ca8`
- Verified: %PDF-1.2 header; 55 pages; pypdf text extraction contains "A Mathematical Theory of Communication", "Bell", "reprinted with corrections".

### [2] J.C.R. Licklider — Man-Computer Symbiosis (1960) — FETCHED
- URL: https://worrydream.com/refs/Licklider%20-%20Man-Computer%20Symbiosis.pdf (free institutional scan of the IRE/AFOSR paper)
- File: memory/corpus/augmentation_canon/licklider_man_computer_symbiosis_1960.pdf
- Bytes: 2,136,055 · HTTP 200 · sha256: `544ccc824d052ff4c9409dc3dd3f1c2834a72b7901146814368c9fb06ce737dc`
- Verified: %PDF header; 8 pp.; extracted text opens "IRE TRANSACTIONS ON HUMAN FACTORS IN ELECTRONICS / Man-Computer Symbiosis / J.C.R. LICKLIDER"; "symbiosis" x14, "man-computer" x13 (43,917 chars OCR-extractable).

### [6] A. M. Turing — Computing Machinery and Intelligence (1950) — FETCHED
- URL: https://www.csee.umbc.edu/courses/471/papers/turing.pdf (free university course mirror of the Mind LIX(236) paper)
- File: memory/corpus/augmentation_canon/turing_computing_machinery_and_intelligence_1950.pdf
- Bytes: 91,972 · HTTP 200 · sha256: `3cd7c57944b7b53f18fb2a7c014fe2367f3576696a1d024c840151459da2f24e`
- Verified: %PDF header; 22 pp.; text contains "Computing Machinery and Intelligence", "Can machines think", "Mind".

### [4] Douglas C. Engelbart — Augmenting Human Intellect: A Conceptual Framework (1962) — FETCHED
- URL: https://www.dougengelbart.org/pubs/augment-3906.html (Doug Engelbart Institute, full text, AUGMENT 3906). Note: first tried augment-3996 — 404; the live path is 3906. theBootstrap.org legacy name redirects to this institute.
- File: memory/corpus/augmentation_canon/engelbart_augmentation_framework_1962.html
- Bytes: 507,637 · HTTP 200 · sha256: `69536f97d895b485d48f801528c3259379fae094787f7f372a33c79f81ef5071`
- Verified: full-text markers — "augmenting human intellect" x9, "conceptual framework" x38, "AFOSR" x2, "journal" x6. (grep -a required: extended-ASCII page reads as binary otherwise.)

### [5] The Mother of All Demos — Dougs 1968 Demonstration (FJCC, 1968) — FETCHED
- URL: https://www.dougengelbart.org/firsts/dougs-1968-demo.html (Doug Engelbart Institute video/transcript page for the December 9, 1968 Fall Joint Computer Conference demo)
- File: memory/corpus/augmentation_canon/engelbart_mother_of_all_demos_1968.html
- Bytes: 83,500 · HTTP 200 · sha256: `9787a905aa502cfb1e5fdbb16047effd4326163a4cd68c47f260899a9dbc555f`
- Verified: "1968" x56, "video" x38, "SRI" x8, "demonstration" present.

### [3] J.C.R. Licklider — Libraries of the Future (1965) — FETCHED
- URL: https://worrydream.com/refs/Licklider%20-%20Libraries%20of%20the%20Future.pdf (free full scan of the MIT Press book)
- File: memory/corpus/augmentation_canon/licklider_libraries_of_the_future_1965.pdf
- Bytes: 9,103,837 · HTTP 200 · sha256: `0f47ea8642452fb5a3cbccb6af358ac6b1780b76571f705eec1f0a7a577f36af`
- Verified: %PDF header; 248 pp.; page 5 title reads "LIBRARIESOFTHEFUTURE" (OCR spacing collapsed); "librar*" x91, "procognitive" x98, "Licklider" x16. (First tried DTIC AD0623971 — DTIC under maintenance; ashby.info is the W. Ross Ashby archive, unrelated to this fetch.)

### [8] W. Ross Ashby — An Introduction to Cybernetics (1956) — FETCHED
- URL: https://web.archive.org/web/2021/http://pcp.vub.ac.be/books/IntroCyb.pdf (Principia Cybernetica free mirror via Wayback; live pcp.vub.ac.be refused connection from this seat)
- File: memory/corpus/augmentation_canon/ashby_introduction_to_cybernetics_1956.pdf
- Bytes: 2,023,477 · HTTP 200 · sha256: `26bd434d9b5d8e430c9b6aea107983249a7196b438502d4624847ab7b8c15da6`
- Verified: %PDF header; 156 pp.; "introduction to cybernetics" x130, "W. Ross Ashby" x3, "variety" x379, "requisite" x25, "homeostat" x11.

## Fetch complete — 8/8 targets on disk + manifested.

---

## Fetched table (8/8)

| # | Document | Year | File (memory/corpus/augmentation_canon/) | Bytes | sha256 (head) | Source |
|---|---|---|---|---|---|---|
| 1 | Bush, "As We May Think" | 1945 | bush_as_we_may_think_1945.html | 236,743 | 4b86cb68387f | theatlantic.com (publisher) |
| 2 | Shannon, "A Mathematical Theory of Communication" | 1948 | shannon_mathematical_theory_of_communication_1948.pdf | 366,296 | 6e4e3411984f | archived copy of Bell Labs' own shannonday PDF |
| 3 | Turing, "Computing Machinery and Intelligence" | 1950 | turing_computing_machinery_and_intelligence_1950.pdf | 91,972 | 3cd7c57944b7 | UMBC university mirror |
| 4 | Licklider, "Man-Computer Symbiosis" | 1960 | licklider_man_computer_symbiosis_1960.pdf | 2,136,055 | 544ccc824d05 | free institutional scan (IRE/AFOSR paper) |
| 5 | Engelbart, "Augmenting Human Intellect: A Conceptual Framework" | 1962 | engelbart_augmentation_framework_1962.html | 507,637 | 69536f97d895 | dougengelbart.org (Institute, full text) |
| 6 | "The Mother of All Demos" — Doug's 1968 Demo | 1968 | engelbart_mother_of_all_demos_1968.html | 83,500 | 9787a905aa50 | dougengelbart.org (video/transcript page) |
| 7 | Licklider, "Libraries of the Future" | 1965 | licklider_libraries_of_the_future_1965.pdf | 9,103,837 | 0f47ea864245 | free full scan, MIT Press book |
| 8 | Ashby, "An Introduction to Cybernetics" | 1956 | ashby_introduction_to_cybernetics_1956.pdf | 2,023,477 | 26bd434d9b5d | Principia Cybernetica mirror via Wayback |

Manifest: `memory/corpus/augmentation_canon/manifest.jsonl` — 8 lines, JSON-validated, full sha256 per line.

## Standing-wave passages (one per document, tied to the fleet)

1. **Bush 1945 → our trails (bonds):** "There is a new profession of trail blazers, those who find delight in the task of establishing useful trails through the enormous mass of the common record." And the mechanism itself: "It affords an immediate step, however, to associative indexing, ... whereby any item may be caused at will to select immediately and automatically another. ... The process of tying two items together is the important thing."

2. **Licklider 1960 → the concert:** "The hope is that, in not too many years, human brains and computing machines will be coupled together very tightly, and that the resulting partnership will think as no human brain has ever thought and no data-processing machine has ever thought before." (OCR-verified in the scan through "think as no…"; spacing normalized from the typographic scan.)

3. **Licklider 1965 → the ledger's feeding:** "The acquisition of knowledge — the initial apprehension of increments to the fund of knowledge — involves the recording and representation of events." Every wave receipt is an increment to the fund.

4. **Engelbart 1962 → the harness itself:** "By 'augmenting human intellect' we mean increasing the capability of a man to approach a complex problem situation, to gain comprehension to suit his particular needs, and to derive solutions to problems." Honest note: the fetched 1962 report's literal "journal" hits refer to journal articles — the Journal as running shared record (the true ancestor of our steps.jsonl) is Engelbart's 1969 "Journal"/dynamic knowledge repository, a follow-on document. The 1962 report here supplies the founding definition, not the journal mechanism.

5. **Mother of All Demos 1968 → the concert performed:** "The audience of ~2,000 conference-goers erupted into a standing ovation." Alan Kay: "To me he was Moses opening the Red Sea." The first time the ensemble played in public, the room stood.

6. **Turing 1950 → the standing wave itself:** "We can only see a short distance ahead, but we can see plenty there that needs to be done."

7. **Shannon 1948 → the ledger:** "The fundamental problem of communication is that of reproducing at one point either exactly or approximately a message selected at another point." And the license: "These semantic aspects of communication are irrelevant to the engineering problem." Hashes over vibes — exactly the shared-surface contract.

8. **Ashby 1956 → the fleet's law:** "This is the law of Requisite Variety. To put it more picturesquely: only variety in R can force down the variety due to D; variety can destroy variety." The fleet holds only as much wave as it can regulate.

## Fetch notes (failures + redirects, for the next lane)

- `cm.bell-labs.com` and `math.harvard.edu`: DNS unreachable from this seat → Shannon taken from Wayback copy of Bell Labs' own PDF.
- DTIC (apps.dtic.mil): "Under Maintenance" page during wave → LoF taken from free full-book scan instead.
- pcp.vub.ac.be: connection refused → Ashby via Wayback of the same PCP mirror.
- dougengelbart.org: `pubs/augment-3996` and `firsts/dougs-1968-demonstration` are 404 — live paths are `pubs/augment-3906` and `firsts/dougs-1968-demo` (receipt corrects the wave order's guessed paths).
- grep on institute HTML needs `-a` (extended-ASCII reads as binary).
- No git operations performed, per lane law. All sources free/legal (publisher, institutional, or archive copies).
