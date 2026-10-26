# FOUNDATIONAL-GAPS: held vs cited-from-memory (librarian expedition, division B)

Lane: foundational-gaps · 2026-10-01 · writer: gala lane seat
Check battery: `watch/inbox/gala_20260925/librarian-expedition/lanes/foundational-gaps.check.txt` (run 2026-10-01T23:20:13Z + correction block 23:21:30Z)

## The lens law

A claim whose founding primary is not held is a claim that cannot be re-verified
offline - the exact dependency the sovereignty thesis exists to end. This card
asks, for every founder the estate named in its last 48h of claims: are the
bytes on disk, or is the estate citing from memory?

## Scoreboard (ask's named list, byte-checked this session)

| Named source | State | Evidence |
|---|---|---|
| Federalist papers | HELD | `memory/corpus/founding_law/federalist_papers_gutenberg_1404.txt` 1,206,592 B + no78 excerpt + NARA constitution/BOR/amendments + Magna Carta + `manifest.json` ("Founding-law canon: the append-only amendment lineage the VOID procedure inherits.") |
| Bernays | HELD | `corpus/library/ractor_starter/bernays/propaganda_1928_pg78634.txt` 227,563 B + `crystallizing_public_opinion_1923_archive_djvu.txt` 270,482 B + `corpus/ractor_ribs/BERNAYS/` case law |
| Jung | HELD | `memory/corpus/ractors/jung/texts/pg48225.txt` 1,107,487 B (Collected Papers on Analytical Psychology) + pg61543/pg65903/pg66041 (Psychology of the Unconscious) + `corpus/library/ractor_starter/jung/psychology_of_the_unconscious_pg65903.txt` + `corpus/ractor_ribs/JUNG/` (case law + invariants) + `Red Book Liber Novus 2009.pdf` |
| Arditi et al. 2024 | NOT HELD | zero bytes under corpus/, docs pdfs, state/arxiv; catalog 0. The map row itself says it (see table row 1) |
| Verlinde | NOT HELD | zero bytes; catalog 0; DOUBLE_DROP says so (table row 4) |
| Cialdini | NOT HELD | catalog 0, corpus rg 0; DOUBLE_DROP flags it (table row 5) |
| quant-cliff trio (2609.31678 / 2609.25447 / 2609.18526) | PARTIAL | 2609.25447 has abstract-level state dump `state/arxiv/2026-09-23/2609.25447v1.txt`; 2609.31678 and 2609.18526 have zero bytes (all three carry verbatim register quotes) |
| REUSE (prefix-reuse economics) | PARTIAL | provider docs primary HELD-in-quote form (B2-340, LINKS.jsonl:343, fetched 2026-09-26 with verbatim quotes); SemiAnalysis post is note-only (LINKS.jsonl:204, title empty, content not fetched); "When Fancy Eviction Fails" is abstract-only (`frontier_olm_2026-10-01/arxiv_deepread.xml:192`) |
| Vonnegut | NOT HELD | catalog 0, corpus rg 0; cited in `mag/narrative_engine.py:26,126,271` and `mag/game_campaign.py:786` |
| Cas Mudde | NO CITATION EXISTS (negative) | word-boundary rg over catalog/corpus/docs/watch = 0 genuine hits; the only inspected substring match is base64 noise (`memory/corpus/ai_canon/chapters/dlb_graphical_models.html:3574`, "Muddes5aUwB1..."). The nearest "mud" referent is the MUD-Dev mailing-list archive, held by URL only (`watch/inbox/mountain_climb/BIBLIOGRAPHY.md:20`) |

Also verified held (outside the ask's list, from earlier librarian waves): the
record-class primaries Dynamo 2007 (900,468 B), Hurlbert 1984 (3,362,874 B),
Haber-Stornetta 1991 (825,065 B), Belady 1966 (1,363,487 B), Mattson 1970
(3,183,872 B), ARC 2003, Fagan 1976, Lamport Part-Time Parliament - all in
`docs/report_v1/sources/pdfs/` with sha receipts (fetched 2026-09-10), plus the
22-PDF merge of 2026-09-29 in `corpus/papers_reference_nonredistributable/`.

THE FINDING: the estate's foundation is better than the ask feared. The
systems/record founding texts and three of the named founders (Federalist,
Bernays, Jung) are held as bytes. The live gap is RECENCY: every primary the
estate leaned on in the last 48 hours (C1/Arditi, the refusal-regime trio,
Verlinde, Cialdini) is cited-from-memory or abstract-only. New claims outrun
the held shelf; the librarian debt is at the frontier, not the foundation.

## THE TABLE - missing primaries, ranked by claim-weight

### 1. Arditi et al. 2024 - refusal direction (arXiv 2406.11717) - weight: HIGH
- Leans on: the C1 censorship mechanism program. `docs/ref/BIBLIOGRAPHY_MAP.md:134` row status "UNVERIFIED-in-estate (literature-cited by the ask; paper never pulled, no sha)"; the row's own words: "no arXiv id pinned because the paper bytes were never in evidence". Consumed by `watch/inbox/hermes_burn/C1_censorship_ASSEMBLED.md`; owed row at `watch/inbox/hermes_burn/DAY1_SKILLS_DOGFOOD.md:347`.
- Landing: `corpus/papers_reference_nonredistributable/2406.11717.pdf` + per-id receipt in `docs/report_v1/sources/receipts/` + pin the id into the map row.
- Fetch source: https://arxiv.org/abs/2406.11717 ("Refusal in Language Models Is Mediated by a Single Direction", Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee, Nanda; verified live today, full text freely downloadable).
- Fetchable today: OPEN (verified this session via web fetch).

### 2. arXiv 2609.31678 - soft refusals under KV cache compression - weight: HIGH
- Leans on: the banked refusal-regime law "audits need judge ensembles matched to the serving context, never keyword rates" (`watch/inbox/frontier_olm_2026-10-01/DIGEST.md:11`, register row 19 with verbatim quote `register.jsonl:19`); feeds the C1 E1-E3 amendment and the quantizer probe.
- Landing: `corpus/papers_reference_nonredistributable/2609.31678.pdf` + receipt; register row already carries the quote, bytes are the missing leg.
- Fetch source: https://arxiv.org/abs/2609.31678 (not fetched this session; arXiv abstract page registered in the same register row).
- Fetchable today: OPEN (arXiv; download not run this session - reported as the owed fetch, not as done).

### 3. arXiv 2609.18526 - llama.cpp cross-tenant state-restore flaw - weight: HIGH
- Leans on: the janitor host hardening ticket (isolation, prompt-lifetime guarantee), DIGEST.md:11 and the OLM MINE DAY 2 banked findings; the estate's sovereign-mirror posture leans on this finding being real.
- Landing: `corpus/papers_reference_nonredistributable/2609.18526.pdf` + receipt.
- Fetch source: https://arxiv.org/abs/2609.18526.
- Fetchable today: OPEN (arXiv; download not run this session - owed, not done).

### 4. Verlinde 2010 - emergent gravity (arXiv 1001.0785) - weight: MEDIUM
- Leans on: the 2026-10-01 canon drop, Drop B. `watch/inbox/DOUBLE_DROP_20261001.md:50-51`: "the paper itself not fetched. Banked as CANON, not as instrument." The canon resonance (verkle leaves / seat mesh) leans on a lineage the estate cannot re-read offline.
- Landing: `corpus/papers_reference_nonredistributable/1001.0785.pdf`.
- Fetch source: https://arxiv.org/abs/1001.0785 ("On the Origin of Gravity and the Laws of Newton", Erik P. Verlinde, 2010; verified live today, full text freely downloadable).
- Fetchable today: OPEN (verified this session via web fetch).

### 5. Cialdini persuasion-jailbreak paper - SSRN 5357179 - weight: MEDIUM-HIGH
- Leans on: the 7-pattern persuasion-scanner probe filed as the estate move (`DOUBLE_DROP_20261001.md:33-40`) and prior art at `watch/WAR_ROOM_PRIOR_ART_20260909.md:112,191`. The drop itself flagged the gap: "Exact paper identity not fetched this session" (:18-19). Identity pinned TODAY: "Call Me A Jerk: Persuading AI to Comply with Objectionable Requests" (Meincke, Shapiro, Duckworth, Mollick, Mollick, Cialdini, Wharton GAIL, July 2025); the study's numbers (28,000 conversations, 33 pct baseline to 72 pct compliance) match the drop's claims.
- Landing: new shelf `corpus/library/persuasion/` (sibling of `ractor_starter/bernays/`); the SSRN preprint plus, eventually, a bought copy of Influence (in-print, not open).
- Fetch source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5357179 via the Wharton GAIL page (verified live today); Influence (2006 ed.) is in-print only.
- Fetchable today: the SSRN preprint = free download (SSRN sometimes gates behind a free account - download not run this session); the book = NOT open.

### 6. SemiAnalysis agentic-traffic post - weight: MEDIUM
- Leans on: the serving-layer reuse economics the estate cites as "vendor-confirmed economics, not just fleet taste" (`watch/inbox/LINKS.jsonl:204`, 2026-09-17). The row is note-only: title empty, content never fetched, no fetch artifact referenced.
- Landing: re-register through the fetch-and-quote pattern (B2-340, LINKS.jsonl:343 is the template) with verbatim quotes; file the post text under `watch/inbox/`.
- Fetch source: https://x.com/SemiAnalysis_/status/2100600804038099217 (public web; X reachability varies - the estate's own LINKS lane resolves via fxtwitter).
- Fetchable today: PUBLIC (fetch not run this session - owed, not done).

### 7. "When Fancy Eviction Fails: Rethinking Cache Replacement For LLM Prefix Reuse" - weight: MEDIUM
- Leans on: the prefix-reuse law family; abstract held (`frontier_olm_2026-10-01/arxiv_deepread.xml:192-196`), zero PDF bytes; it is external convergence for the byte-stable-prefix doctrine.
- Landing: `corpus/papers_reference_nonredistributable/` + receipt; the paper promises released traces - a second-order corpus steal for the P2 replay lane.
- Fetch source: arXiv (id in the deepread XML; fetch not run this session).
- Fetchable today: OPEN (arXiv).

### 8. Vonnegut story-shapes primary - weight: LOW
- Leans on: `mag/narrative_engine.py:26` ("Vonnegut - story shapes (man in hole, boy meets girl, etc.)"), :126 (story-shape table), `mag/game_campaign.py:786`. The shapes are now internalized estate code, which is why this is low-weight: the claim the code makes no longer depends on the book.
- Landing: `corpus/library/` only via a purchased copy; no legal open copy of "A Man Without a Country" (2005) exists.
- Fetch source: in-print book.
- Fetchable today: NOT OPEN (buy/library). Leave cited-from-memory, but label it so in the engine comment (currently unlabeled).

## Negative finding

"Cas mud-referents" resolves to nothing: no genuine Cas Mudde citation exists
anywhere in the estate (word-boundary rg over catalog + corpus + docs + watch;
the sole inspected substring match is base64 noise at
`memory/corpus/ai_canon/chapters/dlb_graphical_models.html:3574`). The nearest
referent is the MUD-Dev mailing-list archive (1996-2007, 31,406 messages),
held by URL only at `watch/inbox/mountain_climb/BIBLIOGRAPHY.md:20`. If the
mountain_climb lane ever leans on it as a finding source, the raphkoster.com
full download is the fetch (public, not run this session).

## Decision ledger

Closes: the held-vs-memory question for every founder the ask named. Changes:
the Arditi map row can be upgraded from UNVERIFIED-in-estate to a pinned,
fetched, sha'd row today at zero spend; the librarian fetch order is fixed as
2406.11717 -> 2609.31678 -> 2609.18526 -> 1001.0785 -> SSRN 5357179 -> the
prefix-reuse pair; and the doctrine lands that the offline-re-verification gap
is a recency problem (new claims outrun the shelf), not a foundation problem.

## Method notes (honesty ledger)

- Two probe-labeling defects in the first check run were corrected IN the check
  file by a correction block, not silently: (1) a corpus rg exit was labeled
  with head's exit (rerun: rc 1, zero corpus hits for Cialdini/Vonnegut/Verlinde);
  (2) "catalog Jung: 618" was substring noise - word-boundary recount is 215
  real hits, which is exactly how Jung flipped from presumed-gap to HELD.
- Web verifications this session: arXiv 2406.11717 (open), arXiv 1001.0785
  (open), Wharton GAIL page (SSRN 5357179 identity), search for the Cialdini
  study identity and Jung Gutenberg availability. Downloads were NOT run - the
  table marks each as owed, not done.
- No code under mag/ or tools/ was touched, so the violation ratchet was not
  run (nothing changed to check).
