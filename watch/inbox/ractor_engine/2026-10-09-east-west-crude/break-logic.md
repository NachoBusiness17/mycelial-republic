# BREAK-LOGIC - hostile pass on the logic lens (east-west-crude, 2026-10-09)

Hostile second pass on the logic lens report of this ride (banked logic.md,
same directory). Mandate: byte-check every evidence cite against the estate,
verdict each finding, add what the lens missed. No em-dashes. Everything below
was read or run this sitting; unverified items are named as such.

## What I ran / read this sitting (exact)

1. Full read: tools/gps_mcp/coverage.py (348 lines). Cites verified:
   :170-172 ROUTE_MESH/ROUTE_FRONTIER/INSUFFICIENT constants; :216-217
   docstring "no prediction from thin air either way"; :158-161 one-shot
   crown ban; :40 MIN_PROBLEMS_FLOOR = 10.
2. Read: mag/percolator.py:600-649. :624-625 promote_gate string verbatim
   ("alpha-budget: ingestion never compiles invariants; promotion happens
   only via percolate() on reviewed signal").
3. Read: tools/workflow_gate.py:1-80 and :695-724. :10 "exit 2 is the only
   hard block"; :51 BLOCKED-STOPCERT exit 2 clause; :707-712 the R3-L1
   comment killing the soft exit 1 ("exit 1 was a shape no other gate
   failure uses") - the lens's :708-710 range sits inside this block.
4. Full read: watch/inbox/DRIFT_PATROL_20261009.md (23 lines). :22 carries
   "Citation baseline at 88 accepted entries" plus the zero-anchors class.
5. Full read: logic.md, economics.md (sibling lens, same directory), and
   the prior hostile pass ractor-topic/break-logic.md (for convergence and
   the truncation pattern). memory/press/PRESS_DIGEST.md head read: single
   scrum item, no market news ("scrum-only organ" holds at this moment).
6. Scoped census reproduction, instrument named (quantifier law):
   - rg -l "LSFO|VLCC|Brent" memory/press state (rg default,
     gitignore-respecting) -> EXIT 1, ZERO hits. This UNDER-counts: state/
     arxiv is gitignored.
   - rg -l --no-ignore "LSFO|VLCC|Brent" memory/press state -> exactly 2
     files: state/arxiv/2026-10-07/digest.jsonl, .../2610.08789v1.txt.
   - rg -l "LSFO|VLCC|Brent" -g "*.md" --max-depth 1 watch/inbox -> 1
     file: THE_FRONTIER_20260924.md. Total 3 filename hits, matching the
     lens's claim exactly under its instrument (grep -r semantics =
     rg --no-ignore semantics).
   - False friends byte-verified: THE_FRONTIER_20260924.md:158 "Brent J.
     Fields, Secretary" (SEC); digest.jsonl:101 "Brent Yi" (QF3 RL paper
     author); rg -c "LSFO|VLCC" 2610.08789v1.txt -> no matches (exit 1,
     count 0) and rg -c "Brent" -> 1, so the paper matched on Brent only.
7. Tree-wide completion of the census the lens abandoned after 9 minutes:
   rg -l --no-ignore "LSFO|VLCC" -g "!.venv/**" -g "!.git/**" -
   g "!**/node_modules/**" . -> ~45 files, ALL classified this sitting:
   real content = only this ride's own outputs (ractor_engine/2026-10-09-
   east-west-crude/*.md, watch/inbox/money_revolution_3rd/MINE.md mtime
   Oct 9 18:40, memory/trajectory/steps.jsonl ride dispatch log); every
   other hit is substring noise, sampled and classified: ghidra golang
   typeinfo matches the x86 instruction name CMOVLCC; grok oral-history
   jsonl matches base64 blobs (VVLCCELf); ipynb/SVG/PDF hits same class.
   Zero mag/ or tools/ code files matched -> the "zero market-data
   instruments" claim holds TREE-WIDE for code, and no pre-ride market
   content exists on the estate.
8. Arithmetic re-verification, .venv/Scripts/python.exe -c (14 checks,
   outputs banked in the session log): #1 33/mt x 270k / 45d = 198,000
   (~200k/day TRUE); #2 1.3M/198k = 6.57x (TRUE); #5 1.3M x 35d / 268k =
   169.78 (TRUE); #6 1.3M x 75d / 268k = 363.8 (claim 361, 0.8 pct off,
   pass); #7 5.98 x 7.45 = 44.55 (TRUE); #8 ratios 3.81 and 8.17 ("3-8x"
   TRUE); #9 80M/268k = 298.5 (TRUE); #10 WTI+40 = 131.02, Dubai+28 =
   138.8 (TRUE); #11 104.82-91.02 = 13.80 (TRUE). DEFECTS: #4 "$33/bbl
   (~$296/mt)" is a phantom conversion - 33 x 7.45 = 245.85/mt, and
   296/33 implies 8.97 bbl/mt which no oil conversion yields (crude 7.33-
   7.45, fuel oil ~6.7); 298.5/mt is the 80M-fixture instrument (~$40/bbl)
   fused into the wrong parenthetical. #3 WS33 at flat 60 over the SAME 45d
   trip = 118,800/day, not ~140k; 140k requires an unstated 38d trip, so
   the "9x below" is duration-dependent (10.9x at 45d).
9. Web re-verification (two searches, free lane, this seat): oilandgas
   middleeast.com Sep 28 2026 snippet returns VERBATIM "daily rate for a
   Middle East-China VLCC at a record $1.27 m on 21 September. average
   stood at $79,700 a day" plus "nearly $800,000 a day (reported around
   Sept 10)" and NEW instruments (Lloyd's List MEG VLCC index 280,941/
   day; US Gulf-China index 154,565/day +23 pct). S&P-flow byte re-sources
   to Maritime Gazette ~Oct 1: "arrivals at roughly 1.5-1.6 million
   metric tonnes in October, down from an estimated 1.6 million mt
   previously", plus a monthly series (see Addition 4).

## Verdicts

### F1 freight instruments irreconcilable, no adjudicator - CONFIRMED, STRENGTHENED, two arithmetic corrections

- Every cite byte-checks: the ask carries both numbers; the oilandgas
  middleeast byte re-verifies verbatim by my search (run 9); DRIFT_PATROL
  :22 verified (run 4). The conclusion only strengthens: my pass adds
  Lloyd's MEG index 280,941/day vs LSEG MEG-China 1.27M/day (same route
  class, 4.5x apart), USG-China 154,565/day, and economics.md:14 adds
  Gulf-China VLCC 6.82 -> 15.32/bbl (Sep 18, ~102.6/mt at 6.7 bbl/mt),
  ~450 WS / ~11M per voyage (Reuters Sep 11), Poten 1.3M/day. The 11M/
  voyage byte vs the logic lens's VLCC-derived 45.5-97.5M/voyage is a
  further 4-8x per-voyage dispersion. No adjudicator exists; the falsifier
  (a unit+route+vintage note) remains unmet.
- CORRECTION 1: "$33/bbl (~$296/mt)" is a phantom conversion (run 8, #4).
  The reconciliation DIRECTION survives (33/bbl x 2M bbl / 45d = 1.47M/day,
  the only reading in the 1.3M/day class), but the parenthetical fuses two
  instruments: 33/bbl is 245.85/mt at the lens's own 7.45; 296-298/mt is
  the 80M fixture at ~40/bbl. A unit-adjudication finding carrying its own
  unit defect.
- CORRECTION 2: the WS33 leg silently switches trip length: 45d for the
  33/mt leg, ~38d for the WS33 leg (118.8k vs 140.7k/day). The "9x below"
  is 10.9x at consistent 45d. Direction unaffected.

### F2 INSUFFICIENT by the estate's trivalent rule - CONFIRMED verdict, framing corrected twice

- All four code cites byte-verified (run 1). The INSUFFICIENT-leaning-
  artifact verdict survives and is now better evidenced (run 9 series).
- CAVEAT A (instrument authority): coverage.py is a model-routing verdict
  calculator over sqlite verdict_log rows; it was never RUN on this
  question (no rows exist, none claimed). "By the estate's own trivalent
  race instrument the question as posed is undecidable" is a principle
  transfer from :159-160's comment ("n>=10 matches the estate's small-
  sample skepticism"), not an instrument reading. The principle is real;
  the phrasing overclaims.
- CAVEAT B (the n): "one month of flow data" understates the seat's own
  evidence. My web pass surfaced a monthly series: Feb 2025 1.6-1.7M (MNI),
  Mar 2026 record 141/mt spread with arrivals -800k MOM (S&P Mar 19),
  Apr 2026 1.4-1.5M (Cyprus Shipping News), May 2026 1.1-1.2M fourth
  consecutive decline (IndexBox), Oct 2026 1.5-1.6M down from 1.6M
  (Maritime Gazette). That is oscillation in a 1.1-1.7M band, five-month
  direction UP from the May trough, latest MOM print DOWN. "Falling
  series" misstates the window; "n=1" is true only for months under
  record freight. The falsifier (two more months holding >=1.5M at kill
  freight) stands unmet and well-formed.

### F3 EIA vs BNEF is an unevaluated conditional - CONFIRMED, STRENGTHENED

- Ask-given numbers verified (88 WTI +4pct, 55 Brent absent Iran
  disruption); 13.80 re-computed (run 8, #11). AGENTS.md (harness-loaded
  bytes this session) carries both the census denominator law (B2-216)
  and the citation-lint PHANTOM-NUMBER class; DRIFT_PATROL:22 verified.
  The logic is sound: with the war antecedent TRUE in-regime, BNEF's 55
  and spot 104 do not conflict. (The war byte itself is a snippet, not a
  fetched primary; noted, not fatal.)
- STRENGTHENED by sibling: economics.md:44-45 independently found the
  ask's own prints contested (its web read: WTI 96.24 / Brent 125.44,
  ~29 spread, vs the ask's 91.02 / 104.82) and the EIA anchor differing
  by grade (Brent ~98 +8pct vs WTI 88 +4pct). CONVERGENT: two lenses of
  this ride independently flagged forecast/print incomparability; per the
  duplication law this finding outranks its novel neighbors.

### F4 promote gate: flow is fact, thesis is proposal - CONFIRMED cite and math, premise qualified, blind spot broken

- percolator.py:624-625 verbatim (run 2). The 2x2 matrix arithmetic
  verifies (run 8: 169.8 and 363.8/mt vs EFS 44.55/mt, 3.81-8.17x).
- PREMISE QUALIFIED: economics.md:8 argues the trade's freight line is LR1/
  LR2 product tankers, not VLCCs (LSFO is products tonnage; VLCC is
  correlated crude tonnage). The ~170/mt flip threshold is then a crude-
  tonnage proxy for a products trade whose exact freight leg BOTH lenses
  mark OWED. The promote-gate logic is unaffected; the threshold number is
  instrument-contested.
- BLIND SPOT BROKEN: the logic lens's headline OWED item ("the decisive
  number, the Singapore 0.5% LSFO premium over the Atlantic netback") was
  banked the same day one directory over: economics.md:12, Singapore
  VLSFO ~808.50 vs Rotterdam ~665.00 = ~143.50/mt gross (bunker basis,
  +-10-20 slop). Multiplied with the lens's own strands (run 8, #12-14):
  vs the today-freight threshold 169.8 the arb is ~25.5/mt SHORT
  (artifact-consistent); vs the September-fixture threshold (~104.5/mt at
  the lens's own 800k/day Sept-10 byte) it CLEARS by ~39/mt (flow-
  consistent). October's flow is September's open window priced at
  September's freight; November re-prices at today's. The lens had both
  strands and never multiplied them.
- The auto-compile warning is MORE live than the lens knew: economics.md
  :19-25 already compiled "Structural Atlantic surplus: YES" from
  free-lane snippets, the exact compile F4 says must wait for reviewed
  signal. The two lenses returned different verdicts on the same ask with
  no cross-read between them.

### F5 market prose has no exit-2 - CONFIRMED bytes, asymmetry claim corrected, truncation noted

- workflow_gate.py:10, :51, :707-712 all byte-verified (run 3).
- CORRECTION: "three overlapping exit-2 gates on the SAME prose surface"
  overcounts. Per AGENTS.md build discipline, the ratchet and citation
  lint run on changed prose at pre-push; the scenario suite triggers only
  on workflow_gate.py changes (B2-164 wording). Two of three face prose.
- The zero-market-gate claim now holds tree-wide for instruments (run 7:
  no code file matches LSFO/VLCC). But in-repo market prose IS lint-gated
  once landed (the lens's own move routes this topic through citation-
  lint --files); the real gap is prose published outside the repo.
- The submitted report text arrived truncated mid-finding-5 ("...while
  the market"); logic.md's F5 completes it. This is the SECOND consecu-
  tive ride with the final finding cut in transit (ractor-topic break-
  logic.md F4, 2026-10-07, same disease). Banked .md stays canon; the
  submit channel eats the last finding.

## Additions (what the lens missed)

1. Phantom conversion inside F1 itself: "$33/bbl (~$296/mt)" is arithme-
   tically impossible at any oil bbl/mt (needs 8.97); 245.85/mt at the
   lens's own 7.45; 296-298/mt belongs to the 80M-fixture instrument.
   Plus the WS33 38d-vs-45d duration switch ("9x" is 10.9x at consistent
   45d). Evidence: run 8 outputs #3, #4. Falsifier: a stated 8.97 bbl/mt
   conversion or a stated 38d trip basis in logic.md (neither exists).
   Move: fix both numbers in logic.md; 5 min.
2. Sibling non-communication is the ride's real failure: economics.md
   (same directory, same day) banked the decisive spread (~143.50/mt),
   the LR-vs-VLCC tonnage correction, the Rotterdam backwardation
   collapse (23.25 -> 15.08/mt), and a DIFFERENT verdict (structural
   surplus YES, structural flow NO). Nobody assembled the synthesis:
   spread 143.5 vs Sept-fixture threshold ~104.5 clears, vs today
   threshold ~169.8 fails -> October flow = September's window; Novem-
   ber collapses unless the spread blows past ~170/mt or freight
   normalizes. Evidence: economics.md:8, :12, :15, :19-27; run 8 #12-14.
   Falsifier: an LR2 UKC-Singapore freight quote above ~143/mt would say
   even September's products window was closed and the flow needs
   another explanation (term contracts, blending barrels per Sea-and-Job
   Jan 16 byte in economics.md:23). Move: 15-min synthesis pass citing
   both lens files; this answers the operator's question better than
   either lens alone.
3. CONVERGENT upgrade for F1 and F3 (duplication law): F1's "one freight
   number cannot stand for the regime" is independently re-derived by
   economics.md's instrument pile (6.82 -> 15.32/bbl, ~450 WS, ~11M/
   voyage, 1.3M/day) and my search's Lloyd's-vs-LSEG 4.5x index gap;
   F3's incomparability point is re-derived at economics.md:44-45. Both
   outrank their novel neighbors and should carry the flag in any rollup.
4. The arrivals series is not n=1 and not "falling": Feb25 1.6-1.7M,
   Mar26 -800k MOM at record spread, Apr26 1.4-1.5M, May26 1.1-1.2M,
   Oct26 1.5-1.6M (MNI, S&P Mar 19, Cyprus Shipping News Apr 22, IndexBox
   May 25, Maritime Gazette ~Oct 1; all free-lane, re-surfaced by my run
   9). Band 1.1-1.7M, five-month direction UP, MOM print DOWN. Evidence:
   run 9 search results. Falsifier: any two consecutive months outside
   the band would establish trend over oscillation. Move: use the series,
   not "n=1", in the November re-census row F4 proposes.
5. The ask's own price prints are contested ground, not truth: economics
   md:44 could not reproduce 91.02/104.82 (web read 96.24/125.44, ~29
   spread). F1/F3 arithmetic leans on prints a sibling marked
   unreproducible; every derived number inheriting them (13.80 grade gap
   included) should carry an unverified stamp in prose. Evidence:
   economics.md:44-45; ask regime context. Falsifier: a same-source same-
   vintage print pair resolving 91.02/104.82 vs 96.24/125.44. Move:
   stamp before any prose lands; 2 min.
6. Channel truncation disease, second occurrence: final finding cut in
   transit on both this ride and ractor-topic 10-07. Evidence: the
   submitted report text (cut at "while the market"); ractor-topic/
   break-logic.md:165-169. Falsifier: a third ride delivering a complete
   final finding through the same channel. Move: none available at this
   seat; keep banked-file-as-canon and say so in every rollup.

## Incident note (my footprint)

My first census commands used cmd-style "2>nul" under the POSIX shell and
created a stray file "nul" in the repo root (29,622 bytes of suppressed
stderr). Removed same sitting (rm nul, exit 0). Also note the instrument
lesson banked in run 6: rg default (ignore-respecting) and grep -r and rg
--no-ignore give DIFFERENT censuses on this tree (state/arxiv is
gitignored); the lens's grep semantics were faithful and my first
reproduction under-counted until the instrument was matched.

## Not run / OWED

- Premium-tier verification of any web byte (driving ladder): not run;
  my re-verification is still free-lane search.
- The qcintel Dec26 Brent/Dubai -5.98/b byte and the alkagesta outlook:
  not re-fetched this pass (the two load-bearing bytes I did re-fetch
  verified verbatim; these two stay free-lane-flagged).
- LR2/LR1 UKC-Singapore freight quote: OWED everywhere (paywalled);
  falsifies addition 2 if it prints above ~143/mt.
- state/CURRENT.md zero-oil claim (logic.md's read): not re-read by me;
  my tree-wide census supersedes it for the content question anyway.

Filed by break-logic, 2026-10-09. All checks this sitting; arithmetic via
.venv/Scripts/python.exe; censuses via rg with instruments named above.
