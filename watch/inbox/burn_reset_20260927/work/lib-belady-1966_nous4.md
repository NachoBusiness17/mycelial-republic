# WORK lib-belady-1966

lane: nous model: qwen/qwen3.8-max-prime
ts: 2026-09-28T08:54:54.104490+00:00
finish: stop cached_tokens: 0
ask: Find the canonical reference for Belady 1966 (the Belady anomaly / FIFO page-replacement study). Return: exact title, venue, year, and one verbatim quote of the anomaly claim with page if findable. If unreachable, say OWED with what you tried.

---

(1) FINDING

Canonical reference: L. A. Belady, “A study of replacement algorithms for a virtual-storage computer”, IBM Systems Journal, volume 5, number 2, pages 78 to 101, year 1966.

Verbatim anomaly quote with page: OWED.

(2) STEALABLE

Use monotonicity counterexamples as property tests. If a system claims that more cache, memory, or quota cannot worsen performance, test it with a Belady style trace that can break that assumption.

(3) TESTABLE

Hypothesis: FIFO page replacement on reference string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 produces 9 faults with 3 frames and 10 faults with 4 frames. A simple FIFO simulator can accept or reject this.

(4) EVIDENCE or OWED

OWED. I could not verify a verbatim quote or page number from the 1966 paper. I tried recall of standard citations and common descriptions of the anomaly, but I did not access the IBM Systems Journal article, a scan, or a reliable quotation. Sources directly consulted: none.
