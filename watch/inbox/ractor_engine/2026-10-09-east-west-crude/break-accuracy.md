# BREAK-ACCURACY: hostile second pass on the accuracy lens (east-west crude)

Seat: break-accuracy, ractor run 2026-10-09. Target: this directory's accuracy.md
(the JSON findings + blind spots). Laws held: no em-dashes, every claim cited,
unverifiable items marked OWED, absence claims name instrument and scope, universal
claims re-censused untruncated. All checks below were run this sitting.

## Verdicts

### F1 "estate carries zero market bytes" : WEAKENED (substance survives scoped, census legs defective)

What holds: no east-west ARB market bytes existed pre-ask. My re-census, full tree,
case-sensitive: `rg -l "VLCC" .` and `rg -l "Dubai" .` and `rg -l "Singapore" .` and
`rg -l "Brent" .` return, outside this run's sibling receipts, only war narrative
(mrpool ledgers, corpus/telegram/MrPool_Q.jsonl), persons (transcriptions.jsonl,
THE_FRONTIER_20260924.md "Brent J. Fields" per logic.md:24), fiction/canon, zai docs
legal boilerplate, and base64 false friends (dlb_rnn.html "VLCC" sits inside an
encoded blob, confirmed this sitting). Press, economist trail, state/, queue/,
x_radar.json, FLOW_IMAGE.json: zero rows for the token set
(`rg -i -c "vlcc|brent|dubai|singapore|crude|fuel oil|lsfo|arbitrage|east-west"`).

What breaks, four defects:

1. "corpus/ 0 files" is FALSE. `rg -i -c "vlcc|brent|dubai|singapore|crude|fuel oil"
   corpus/telegram/MrPool_Q.jsonl` returns 57. War-narrative bytes, not arb bytes,
   but the stated census result is wrong.
2. The cited scan target memory/live_from_grok.json does not exist:
   `rg --files memory | rg -i live_from_grok` returns empty (AGENTS.md names
   memory/live_from_grok.md). A 0-row leg on a phantom path is a vacuous pass.
3. The watch/inbox leg censused only the Brent token (accuracy.md:14-15) while the
   finding claims the whole estate: mrpool_export/ledger.jsonl (6 lines) and
   ledger_full.jsonl (16 lines) match crude| tanker inside watch/inbox
   (`rg -c -i "crude|tanker"`, this sitting), including "hit a Kuwaiti tanker in
   Dubai Port... A fully loaded crude" (ledger.jsonl). Scoped grep wearing a
   universal claim, the exact quantifier-law disease.
4. The 2026-10-07 cutoff listing missed this run's own eight sibling receipts in
   watch/inbox/ractor_engine/2026-10-09-east-west-crude/. The finding's own
   falsifier ("sibling-lane receipt... containing the S&P Singapore story") fired
   the same day: economics.md:7 carries the S&P Sep 30, 2026 story with the
   1.5-1.6M mt figure and the "unviable arbitrage economics" quote.

Verdict: the scoped claim (no arb-market bytes pre-ask; regime numbers ride the ask)
survives; the universal phrasing and three of its census legs do not.

### F2 "13.80 exact; the 33 is unitless and sign-flipping" : CONFIRMED (CONVERGENT, sharpened by a sibling)

`./.venv/Scripts/python.exe` this sitting: 104.82 - 91.02 = 13.80 exact. The unit
defect on "Gulf freight ~33" is real and independently re-derived by logic.md F1
(logic.md:85-99): $33/mt on 270k mt over ~45d implies ~$200k/day TCE (I verified
$33 x 270,000 / 45 = 198k/day), 6.5x below the $1.3M/day print; WS33 on a legacy
flat implies ~9x below; only $33/bbl reconciles the two numbers, and that is the
US-to-China fixture class, not "Gulf". Logic's sharpening: the ask's regime context
is not merely ambiguous, it is internally contradictory under every unit reading
but one. The lens's 5-min move stands.

### F3 "$1.3M/day is one instrument's extreme in a field dispersed 16x" : WEAKENED

Arithmetic: 1,300,000 / 79,700 = 16.3x, verified. But the framing falls on two
breaks:

1. The record is multi-instrument corroborated, not one instrument's extreme:
   LSEG/Reuters record $1.27M/day MEG-China on Sep 21 (oilandgasmiddleeast.com Sep
   28, OilPrice Sep 25, reproduced by my WebSearch this sitting), TCE $1.2125M/day
   by Sep 17, Hamer above $1.2M/day MEG-Asia Sep 23 (moonshot-2.md:142), web band
   $1.21-1.4M (logic.md:43), Reuters ~$11M/voyage ex-Gulf of Oman (economics.md:14).
   The $79,700 is the VLCC global AVERAGE (logic.md:31-32; moonshot-2.md:143 calls
   it "route-print vs global-average 4x gap"), and Lloyd's MEG-China index is a
   third class (~$982,000/day after doubling, my search). The 16x is instrument-class
   heterogeneity (route record vs route index vs global average), not trackers
   disagreeing about one quantity.
2. The ladder's own arithmetic is inconsistent at one rung: on the stated 37-day,
   2M-bbl basis $79,700/day = $1.47/bbl, not the banked $1.28 ($1.28 implies 32.1
   days; python this sitting). Direction unaffected, but the ladder was presented
   as awk-verified.

The move (name instrument, route, unit, vintage before pricing) survives and is
CONVERGENT (logic.md F1, moonshot-2.md instrument-splitting).

### F4 "the decisive byte: EFS -19.67, arb open $10-18 everywhere, spread carried October, decay analogs contradict the kill" : WEAKENED (the decisive-byte claim is dead; the arithmetic core survives)

The internal math verifies: 24.05 - 19.67 = 4.38 ("shut by about $4" correct);
19.67 - 9.60 = 10.07; 19.67 - 5.20 = 14.47. Four breaks at the byte level:

1. The -$19.67 print is unreproducible in a second sitting: my WebSearch for the
   QCIntel EFS returned rate-limits and irrelevant hits (QCIntel is
   subscription-walled); no public carrier of -19.67 or -5.98 surfaced. It stays a
   free-lane single-carrier number.
2. A newer QCIntel print contradicts its magnitude: Dec26 Brent/Dubai -$5.98/b on
   Oct 1, 2026 (logic.md:33-34). At -$5.98 the ladder shuts the arb at the $9.60
   and $24.05 rungs and nearly at $5.20. "Open at every observed freight level" is
   not robust to a print three weeks newer and 3.3x smaller. A third reading sits
   in moonshot-1.md:42,157 (Dubai 106.36, EFS near zero, session date unverified).
3. The October flow is a FALL, not a flow-event: arrivals decline to 1.5-1.6M mt
   from ~1.6M with S&P's own copy citing "unviable arbitrage economics" on part of
   the program (economics.md:7,22; logic.md:72-73 via alkagesta; independently
   re-surfaced by my WebSearch: Maritime Gazette Oct 2, 2026 "West-to-Singapore
   low-sulfur fuel oil arrivals set to fall in October"). "The October flow rode
   the spread... supports the structural reading" is opposed by the
   direction-of-change byte and by economics' March counter-proof: record $141/mt
   East/West spread WITH arrivals falling ~800k mt month-on-month because freight
   blocked the arb (economics.md:13,21) : a record spread with falling volume
   proves freight is the gate, not demand pull.
4. The decay-analog leg is contradicted by an observed November fixture: ~$80M for
   a 2M-bbl VLCC to China in November (LSEG/Reuters), surfaced by logic.md:33,43
   and independently reproduced by my WebSearch this sitting ("the cost of
   chartering a VLCC to China in November reached $80 million this week"). That is
   ~$40/bbl, above every EFS reading in evidence. Freight did not decay into the
   November window; it is transacting at crisis level. Same caveat both times: it
   is the crude VLCC leg, not the LSFO LR2 leg (economics.md:8).

Also missed: economics.md:44 prints Oct-6 Brent $125.44 / WTI $96.24 (~$29 spread)
vs the ask's 104.82/91.02, a three-way level conflict (101.73 QCIntel settle /
104.82 ask / 125.44 economics) that makes any single-print "decisive byte" unsafe.

Verdict: weakened, not killed, because every opposing byte is also search-layer
summary class (links stripped or paywalled); no page-verified number exists on any
side. What survives: EFS-vs-freight is the right spine, and the $1.3M-day extreme
shuts the arb by ~$4 even at -19.67.

### F5 "causal-order and cargo-class traps; November falsifier pair" : CONFIRMED (CONVERGENT x2, thresholds improved by siblings)

- Arrival month is not fixture month: CONVERGENT, economics.md:27 ("arrival month
  is not fixture month... fixed weeks earlier on pre-spike economics") and
  logic.md:75 ("October arrivals price September fixtures").
- Cargo class: 1.6M mt LSFO is product tonnage (~14.5 LR2 parcels at 110k mt), and
  the kill-switch is the LR1/LR2 product-freight market, not VLCC spot:
  CONVERGENT, economics.md §0.2 ("the kill-switch is not the VLCC rate"). Cargo
  arithmetic verified this sitting: 1.6M mt at 0.99 t/m3 = 10.17M bbl, 5.08
  VLCC-equivalents, 14.5 LR2 parcels.
- Iran-premium-through-Dubai alternative label: CONVERGENT, moonshot-1.md:72
  ("Dubai over Brent IS that premium in EFS costume").
- Sharpening: the unconditional November thresholds (>=1M structural / <0.5M
  artifact) are weaker than logic F4's 2x2 (freight >$1M/day vs lower, arrivals
  >=1.5M vs <1.0M, logic.md:139-141) and economics' instrument-conditioned pair
  (economics.md:38-39). Splice those into the standing falsifier.

## What the lens missed (additions)

1. The estate's own telegram canon carries the war-regime corroboration the lens
   called absent: Kuwaiti tanker hit in Dubai Port with a fully loaded crude
   cargo, drones on Dubai airport, 17 days of war
   (watch/inbox/mrpool_export/ledger.jsonl and ledger_full.jsonl,
   corpus/telegram/MrPool_Q.jsonl, rg contexts this sitting). These bytes back the
   Hormuz/Iran premium framing of the ask's regime and were missed by accuracy's
   census and mislabeled "fiction/canonical noise" by economics.md:45.
2. The lens's undischarged OWED (Singapore-vs-Rotterdam LSFO differential) is
   DISCHARGED in sibling bytes at two vintages: $808.50 vs $665.00 = ~$143.50/mt
   (economics.md:12, Ship & Bunker bunker basis) and $908 vs $728 = $180/mt
   (moonshot-1.md:15). They straddle logic's ~$170/mt clearing threshold
   (logic.md:56-57): the product arb is knife-edge on instruments the accuracy
   lens never had. Falsifier: an Argus/Platts FOB cargo-swap print outside
   $140-185/mt. Move: 10 min, vintage-stamp both prints into the synthesis.
3. The EFS is a contested three-way range inside this run (-19.67 Sep 10 / -5.98
   Oct 1 / near-zero unverified), and the Oct-6 price levels conflict three ways
   (104.82 ask vs 125.44 economics.md:44 vs 101.73 QCIntel settle). Falsifier: a
   page-verified Platts/ICE EFS print. Move: the synthesis must carry the EFS as
   a dated range, never a number; no free-lane print may wear "decisive".
4. The November kill-condition is already observed, not hypothetical: the ~$80M
   November VLCC-to-China fixture (logic.md:33 + my independent WebSearch, both
   citing LSEG/Reuters) puts November freight at ~$40/bbl on 2M bbl, above every
   EFS reading in evidence. Falsifier: November fixtures printing back under
   ~$30M/voyage. Move: 5 min, re-label the kill mechanism "transacting, not
   predicted" in the synthesis, crude leg only (LSFO LR2 leg still OWED).
5. The 2026 arrivals series oscillates (Jan rebound after Dec drop per
   spglobal headline, logic.md:37-38; Apr 1.4-1.5M; May 1.1-1.2M fourth
   consecutive decline, my WebSearch; Oct falling from ~1.6M). A structural
   declaration off one month is an n=1 crown: the estate's own one-shot law
   applies (tools/gps_mcp/coverage.py:216-217, cited by logic.md:110-114). Move:
   stamp INSUFFICIENT-leaning-artifact until n>=3 months, per logic F2.

## Instruments run this sitting (exact)

- `rg --files memory | rg -i live_from_grok` : empty (phantom path).
- `rg -i -c "vlcc|brent|dubai|singapore|crude|fuel oil" corpus/telegram/MrPool_Q.jsonl` : 57.
- `rg -c -i "crude|tanker" watch/inbox/mrpool_export/ledger.jsonl ledger_full.jsonl
  transcriptions.jsonl` : 6 / 16 / 2.
- `rg -i -c "<token set + arbitrage|east-west>" dashboard/static/trails/economist.jsonl
  memory/press/PRESS_DIGEST.md memory/press/latest.json state/CURRENT.md queue/todo.md` : no output (zero).
- `rg -i -c "<token set>" state/ queue/ docs/ configs/ memory/game/FLOW_IMAGE.json
  dashboard/static/x_radar.json memory/press/` : only docs/ zai-mirror boilerplate.
- `rg -l "VLCC" .` / `rg -l "Dubai" .` / `rg -l "Singapore" .` / `rg -l "Brent" .` :
  full-tree case-sensitive censuses, hits enumerated above (sibling receipts + war
  narrative + persons + fiction + encoded-blob false friends; two rg errors on
  watch/inbox/frontier_olm_2026-10-06/nul, an OS-level artifact, both times).
- `./.venv/Scripts/python.exe` arithmetic: spread 13.8; ladder 24.05 / 9.6 / 5.2 /
  1.47 (banked 1.28 not reproducible on stated basis); cargo 10.17M bbl, 5.08, 14.5;
  dispersion 16.3; $1.28 implies 32.1 days.
- WebSearch x3 (QCIntel EFS: not reproducible, paywalled; S&P October LSFO story:
  Maritime Gazette Oct 2 2026 fall headline + 2026 series; VLCC record: $1.27M/day
  Sep 21 LSEG/Reuters + $80M November fixture reproduced). All search-layer
  summary class; no primary page fetched; links stripped by the layer.

## Sources (search-layer summaries, domain + date as returned)

- oilandgasmiddleeast.com, Sep 28, 2026 (LSEG/Reuters VLCC record $1.27M/day Sep
  21; global average $79,700/day); OilPrice Sep 25, 2026; ShipUniverse Oct 1, 2026.
- Maritime Gazette, Oct 2, 2026 (West-to-Singapore LSFO arrivals set to fall in
  October); spglobal.com (series history incl. Feb 6, 2025 edition); Hellenic
  Shipping News Jan 16, 2026; Cyprus Shipping News Apr 22, 2026; IndexBox May 25,
  2026.
- Estate siblings: economics.md, logic.md, moonshot-1.md, moonshot-2.md,
  communication.md, dogfood.md, operations.md in this directory (cited by line
  above).

Filed by break-accuracy, 2026-10-09. Not run: any paywalled pull (Argus/Platts/
QCIntel/Platts windows), any page-level fetch of the market stories.
