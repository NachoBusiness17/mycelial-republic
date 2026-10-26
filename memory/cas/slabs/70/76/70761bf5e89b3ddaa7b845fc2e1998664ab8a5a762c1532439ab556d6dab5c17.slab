# WORK lib-mattson-1970

lane: hermes (headless one-shot)
ts: 2026-09-29T17:09:31.191001+00:00
ask: Find the canonical reference for Mattson 1970 (stack distance / LRU approximation, Evaluation of Multi-Programmed Batch Systems?). Return: exact title, venue, year, one verbatim quote defining stack distance. If unreachable, say OWED with what you tried.

---

(1) FINDING

The Mattson 1970 paper you named does not exist under that title. The correct canonical reference is:

- **Title:** "Evaluation techniques for storage hierarchies"
- **Authors:** Richard L. Mattson, Jean-Paul Gecsei, Donald R. Slutz, Irving L. Traiger
- **Venue:** IBM Systems Journal, Volume 9, Issue 2, pp. 78-117
- **Year:** 1970
- **DOI:** 10.1147/SJ.92.0078

"Evaluation of Multi-Programmed Batch Systems" is a different (earlier) paper, not the stack-distance one. The stack-distance / LRU approximation material is all in the IBM Systems Journal paper above.

(2) STEALABLE IDEA

The paper defines stack distance as the single metric that captures buffer-hit behavior across ALL capacities in one pass. Any cache/lru simulation can collapse to a frequency table of stack distances {n(Δ)} and derive F(C) for every C without re-running the trace. That's the "one trace, all capacities" trick — worth porting into any eviction benchmark.

(3) TESTABLE HYPOTHESIS

Given a reference trace, a straight LRU simulator that emits stack-distance frequencies n(Δ) should reproduce the paper's F(C) success function exactly for C = 1..N, and the cumulative sum of n(Δ) >= C should equal the hit rate at capacity C.

(4) EVIDENCE

Sources found: the IBM Systems Journal PDF at bitsavers (mirrorservice.org), Rankless hit-paper page (rankless.org), and exa.ai library entry all converge on the same title/venue/authors/year. The verbatim stack-distance definition from the paper's OCR text:

> "We call this page position the stack distance Δi, since Δi is essentially the 'distance' from the top of the stack to xt(Δi)"

No em-dashes were in the original OCR; the quote uses plain quotes. The PDF text was partially garbled by OCR but the definition line is consistent across sources.
