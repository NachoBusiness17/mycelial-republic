# EAST-WEST CRUDE, MOONSHOT LENS (moonshot-1)

Operator ask 2026-10-09, "bring me the east west argument, 1.6m tons of crude
oil": the October 2026 flow of ~1.5-1.6M mt of low-sulfur fuel oil from the
Atlantic basin into Singapore. Filed by moonshot-1 on 2026-10-09.

## THE VERDICT FIRST (no sacred cows)

Both banks are right about their own observable, and "which side" is a false
binary in the estate's own genre. The compose law at
memory/continuity/seat_memory_20260927/east-west-ractors-20260916.md:37-44
says it: two banks, one river, never merged. The river here is the priced
margin, and it is THIN:

- Gross cargo spread proxy: Singapore VLSFO $908/mt vs Rotterdam $728/mt =
  +$180/mt (verified this sitting, WebFetch of https://shipandbunker.com/prices;
  that page's oil table stamps T Oct 8 WTI 91.18 / Brent 104.02).
- Freight leg: no public quote obtained this sitting (OWED). But March 2026
  bounds it: S&P Global (Mar 19, 2026, via spglobal.com search-result summary)
  reported the East-West spread at a record $141/mt WITH the arbitrage still
  blocked by freight, and March western arrivals ~800,000 mt lower month on
  month. So in March, freight plus costs exceeded $141/mt.
- Today the same window shows +$180/mt gross against a freight regime at
  records (VLCC benchmark earnings past $1.2M/day Sep 28,
  oilandgasmiddleeast.com; near $800K/day Sep 10, TTNews; MEG-China $451K/day
  Sep 12, globaloilshock.com; the ask's own October reading ~1.3M USD/day).
  Margin band: roughly $10-40/mt, call it $16-64M aggregate on the ask's
  1.5-1.6M mt. INFERENCE from the March bound, not a quote.

So the October flow is the marginal window clearing AT record freight, not
despite it. 1.5-1.6M mt moves because it JUST clears, which is exactly why the
S&P Oct 1 wrap (via spglobal.com search-result summary) says high freight
closes most OTHER arbitrage economics and October western arrivals are only
marginally lower, and why Dan-Bunkering (Sep 2026, dan-bunkering.com) reports
Singapore VLSFO availability very tight with premiums rising. One more
$10-20/mt on the freight leg closes this window too. That is the artifact
bank's true claim, and it is already half-true by construction.

The structural bank's tell is one print away: the Dubai Oct swap printing
~$106.36/bbl (Barchart JDCV26, via search-result summary, session date
unverified) against Brent ~$104 (ask Oct 6: 104.82; Ship & Bunker Oct 8 table:
104.02) means Brent UNDER Dubai, an EFS near zero or negative. That is the
Atlantic barrel structurally discounted eastward. The October LSFO window is
riding that discount: West cheap (push) AND East scarce (pull) at the same
time.

## THE LIVE MICRO-SIGNAL (what moved on the day I looked)

Ship & Bunker day deltas (verified fetch): Singapore +$12, Rotterdam +$36.
The premium COMPRESSED ~$24/mt in one day WHILE the cargoes lift. The surplus
owner (ARA) is repricing up to meet the freight, absorbing part of the cost to
keep the flow moving. That is push-economics, live on the tape. Falsifier for
this read: if ARA stops absorbing (Rotterdam falls, spread blows back out
above $200) while cargoes still lift, scarcity-pull dominates and the window
lives longer than the artifact bank says.

## THE MARKET'S OWN VOTE (confounded, named)

CME Singapore FOB Marine Fuel 0.5% futures: Oct ~$818.76, Nov ~$784, Dec ~$747
(via search-result summary), a slide of roughly $72 into December that looks
like a vote for the artifact side (the premium compresses as the 1.6M mt
lands). CONFOUND NAMED: the crude curve is in deepening backwardation (Brent
Nov closed ~$103.97, Commodity Board Sep 18 via search-result summary), so
later-month product prices fall partly WITH crude. The clean vote (the
Singapore-Rotterdam product Cal spread forwards) is OWED.

## THE FALSIFIER OF FALSIFIERS

EIA's 2026 WTI forecast at 88 vs BNEF's Brent average at 55 absent Iran
disruption (ask givens) is a ~$33 disagreement that reduces to ONE observable:
the Iran/Hormuz risk premium. Record VLCC earnings ARE that premium in freight
costume; Dubai over Brent IS that premium in EFS costume. De-escalate, and
freight normalizes, the EFS flips positive, October becomes the remembered
artifact, and both forecasts converge toward BNEF. Persist, and the Atlantic
discount stays structural and the tight-inventory read owns Q4. The east-west
argument is one geopolitical variable wearing two financial costumes.

Kill observables, both banks:

- The ARTIFACT bank dies if: November west-of-Suez loadings hold at or above
  ~1.4M mt at unchanged record freight (the flow survived the freight test);
  Singapore onshore fuel oil stocks keep DRAWING after the 1.6M mt lands
  (demand absorbing, not surplus hunting); the EFS stays negative through Q4.
- The STRUCTURAL bank dies if: the EFS flips positive; ARA LSFO stocks draw to
  norms (nothing left to push); the Singapore premium compresses below the
  freight breakeven on arrival AND stays there (it was pull-scarcity, not
  push-surplus); Hormuz de-escalates and the flow still stops (then it was
  never structural, it was insurance).

## THE MOONSHOT MOVE: ARB_SMITH (the 10x version of the argument)

The 10x version of "which side is right" is not a better essay, it is an
instrument that settles the argument daily. The estate proved and promoted the
exact shape THIS WEEK: tools/estate_smith.py (six-block one-row ledger, shape
at watch/inbox/smith_chart_estate_20260109/estate_smith.py:1-11, alert
thresholds at :23-25) promoted with 14 tests, a daily task and a written path
(watch/inbox/smith_chart_estate_20260109/PROMOTION_LANDED.md:7-8 for the
promotion, :44-50 for the test run shape, :58-68 for task registration).

ARB_SMITH v1, first sitting (~90 min, receipt space in this directory):

1. Fetch five public quotes: Brent, WTI, Singapore VLSFO, Rotterdam VLSFO
   (shipandbunker.com/prices, parse proven by this sitting's fetch), plus a
   VLCC earnings headline from public trade press (Baltic/Clarksons are
   paywalled, OWED) and the Dubai swap or EFS if the public page is stable.
2. One jsonl row per run: {ts, brent, wti, dubai, efs_sign, sg_vlsfo,
   rot_vlsfo, gross_spread, day_delta_spread, vlcc_usd_day, freight_est OWED,
   margin_band inference, window_state OPEN/CLOSED/OWED, regime_hormuz bool}.
3. TWO BANKS NEVER MERGED: window_state (artifact bank) and efs_negative
   (structural bank) are two columns; the tool never emits one merged verdict,
   per the compose law (east-west-ractors-20260916.md:37-44).
4. Alert to memory/attention.md on a window flip, the estate_smith alert
   pattern (estate_smith.py:23-25).
5. Piggyback the news lane: MagEndpointNewsDaily is green
   (state/REDBOARD.md:21) and already snapshots endpoints at 06:30 daily
   (memory/zknot/LATEST.md:74-80); add an Iran/Hormuz keyword so the regime
   variable lands daily beside the prices.

Second sitting (+60 min): promotion to tools/arb_smith.py with tests and a
scheduled task on the PROMOTION_LANDED path, once a freight feed exists.

Third move (15 min): when either bank's kill observable fires, bank the dead
thesis into memory/fold_history/SUPERSEDED.md as the estate's first MARKET
demotion rows. The register's law fits exactly: "a conclusion enters this
register when banked bytes contradict it" (SUPERSEDED.md:12-16), and a price
print is a banked byte. That retires the argument the way the estate retires
beliefs, with evidence rows, not takes.

## RECEIPTS OF THIS SITTING

- state/CURRENT.md read (status running, updated 2026-10-07T08:46:42Z).
- memory/zknot/LATEST.md read (moonshot self-steal 10-08 and estate smith
  promotion 10-09 commits visible in the trail).
- watch/inbox 48h surface listed (find -newermt 2026-10-07, root files and
  dirs).
- Prior-art grep launched across memory/ watch/inbox/ mag/ tools/ configs/
  corpus/ docs/ state/, KILLED at 60 hits on corpus noise (mostly
  memory/corpus/ canon texts matching the word crude); this was NOT a full
  census. In everything actually read this sitting, no oil, freight or arb
  market instrument exists in the estate: dashboard/static/trails/
  economist.jsonl (tail of its 50 rows read via wc -l + tail) is the internal
  token-hunger ledger (hunger rc=0, shelf counts), not commodities.
- Web: 4 searches + 1 WebFetch (shipandbunker.com/prices) executed this
  sitting. Search-result summaries are secondary instruments and are named as
  such wherever used above.

## AMENDMENT 2026-10-09 (hostile second pass: two findings weakened, corrected)

The second pass weakened the live micro-signal finding and the falsifier-of-
falsifiers finding. Both corrections below were re-derived with this seat's own
instruments, not accepted on the critic's word.

### A1: THE LIVE MICRO-SIGNAL is WITHDRAWN as a structural tell

The bytes were real and re-verified by a second WebFetch of
https://shipandbunker.com/prices this sitting: Singapore VLSFO 908 (+12.00),
Rotterdam 728 (+36.00); IFO380 Singapore 808.50 (+20.00), Rotterdam 665.00
(+55.00); and the control the critic named, verified on my own fetch: Brent
104.02 (+2.80), WTI 91.18 (+2.24), T Oct 8 table.

Normalization, my arithmetic, conversion named: fuel oil runs 6.3-6.6 bbl/mt
(moonshot-2.md:93, the sibling lens's stated standard conversion; the critic's
7.33 is the crude conversion), so the day's crude beta is roughly +17.6-18.5
$/mt. Decomposed:

- Rotterdam VLSFO +36 = beta + ~17-18 RESIDUAL (net Western strength).
- Singapore VLSFO +12 = beta + ~(-7) to (-6) RESIDUAL (net Eastern softening).
- IFO380 replicates the pattern: Rotterdam +55 = beta + ~+37 residual;
  Singapore +20 = beta + ~0 residual.

So BOTH banks' tells are present in one tape, replicated across two grades:
the West repriced up net of crude (the push story) while Singapore softened
net of crude (arrival pressure ahead of the 1.6M mt, the artifact story). One
day, two banks, no merge possible; the critic's downgrade is confirmed by my
own arithmetic. This seat's original F2 was exactly the naive single-print
read the estate's own statistics law outlaws: n=1 is UNPROVEN under the Wilson
gate (mag/signals.py:112-127, verified by direct read this sitting; cited for
the same point by moonshot-2.md:95-97).

The old falsifier (spread back above $200) is struck: a delivered-spread
blowout cannot discriminate a freight rise from scarcity-pull, because freight
passes through into delivered prices too. Replacement, pre-registered truth
table for the arrival week (the Singapore onshore FO stock print is the
control the spread can never be):

- Stocks DRAWING with Singapore crude-net residual at or below 0 = demand
  absorbing at softening prices, the pull/structural leg is real.
- Stocks BUILDING with Singapore residual below 0 = arrival pressure, the
  artifact window is closing on schedule.
- Singapore residual ABOVE 0 under either stock sign = Eastern scarcity
  deepening faster than arrivals, the window extends past November.

ARB_SMITH spec amended accordingly: the row must carry per-port crude-net
residuals (sg_residual, rot_residual, computed as day_delta minus the
6.3-6.6-scaled Brent day change) beside the raw spread, and the raw
day-delta must never be read as a bank tell. The Rotterdam residual is also
freight-confounded until the product-tanker leg exists (delivered prices
carry freight pass-through); it is a push tell only after the freight control
lands (UKC-Sing LR rate, paywalled, OWED).

### A2: the falsifier of falsifiers is DOWNGRADED from identity to war-DOMINANT approximation, and the EFS costume is now banked but unstable

Three corrections:

1. FREIGHT costume: CONFIRMED and CONVERGENT. The war-driven trajectory
   (Jun ~190.5K/day, Sep 18 ~470K/day, Sep 22-23 above $1.2M/day, October at
   records) is critique-given in part, but my own doors corroborate the
   pieces (Reuters ~$470K/day Jun 23; oilandgasmiddleeast.com past $1.2M/day
   Sep 28; the ask's ~1.3M USD/day Oct; moonshot-2.md:36-37 Hamer Sep 23
   above $1.2M/day MEG-Asia), and moonshot-2.md:62-68 independently ruled the
   war, not freight and not the surplus, the conditioning variable of the
   whole argument. Convergence flagged.
2. EFS costume: my original negative reading was instrument-mixing (an Oct
   Dubai swap against spot prints of mixed dates) and stays struck as
   evidence. New, my own door this sitting: QCIntel (~Oct 6, via search
   snippet, body paywalled) reports "fuel oil east-west hit a fresh high",
   Dec26 Brent settling $99.97 (-1.33 on the day), and the Brent/Dubai spread
   at -$5.72/b, i.e. a DATED NEGATIVE print on the Dec legs, same article as
   the record fuel-oil east-west spread. Against that, the critic's only
   other dated print is QCIntel Sep 10 at POSITIVE +$8.60/b (critique-given;
   NOT verified on this seat's doors). If both prints stand, the EFS swung
   roughly $14/b in under four weeks, which changes the claim: in this regime
   the EFS is a war-volatility instrument, too fast to carry a "structural"
   label on any single print. The latest print supports the Atlantic-discount
   direction; the swing size forbids the structural reading of it. ARB_SMITH
   must pull a DATED EFS instrument (ICE EFS future or matched-month
   Brent/Dubai), never a swap-vs-spot month-mix.
3. The ONE-observable identity claim is withdrawn as a quantifier-law
   overreach. EIA's named drivers per the ask are falling inventories and
   tight diesel (non-war fundamentals), and EIA's own path is Brent $105
   falling to $84 next year (moonshot-2.md:40-42, verified read this
   sitting): EIA prices a de-escalation glide, not a pure war premium.
   Corrected frame: the war is the DOMINANT conditioning variable of the
   freight leg and the price level (moonshot-2.md:66-68), with inventory and
   diesel legs as real second variables that survive the war term. A Hormuz
   de-escalation kills the freight leg and the record spreads together; it
   does NOT automatically null the inventory/diesel legs, which is why EIA
   and BNEF can disagree by ~$50 while sharing the same war variable.

Tightened falsifier for the war-dominance of the FREIGHT leg specifically:
VLCC earnings normalizing under ~$200K/day while the war continues falsifies
the war-premium story (ton-mile/fleet-supply dominates); freight holding
above $1M/day after a verified ceasefire falsifies it in the other direction
(fleet scarcity, not war risk, owns the record). Either branch kills the
simple freight-costume story and forces the two-variable model.

### Amendment receipts

- WebFetch #2 of shipandbunker.com/prices (deltas incl. Brent +2.80 verified
  myself, not critique-given).
- Full read of moonshot-2.md (sibling lens): :40-42 EIA glide, :62-68 war
  ruling, :93 conversion, :95-97 Wilson cite.
- Direct read of mag/signals.py:93-95 and :112-127 (ewma alpha 0.3; the
  proven_move Wilson gate that outlaws n=1 reads).
- WebSearch: QCIntel ~Oct 6 snippet (Dec26 Brent 99.97, Brent/Dubai -5.72/b,
  fuel-oil EW spread at fresh high). Body paywalled; snippet is the
  instrument.
- NOT verified on this seat's doors, carried as critique-given: the Sep 10
  +$8.60/b EFS print and the exact Jun/Sep trajectory points.

## HONEST GAPS (OWED)

1. The primary S&P Global October story was not directly readable (paywalled;
  the first search attempt died on a 429 rate limit). The ask's 1.5-1.6M mt
  rides the ask's own citation; what this sitting verified is the direction
  (Oct 1 S&P wrap: October western arrivals marginally lower, most windows
  closed by freight; Maritime Gazette Oct 2 confirmation) via search results.
2. Freight $/mt for the Rotterdam-Singapore LSFO parcel route: no public quote
  obtained. The greater-than-$141/mt bound and the $10-40/mt margin band are
  inference from the March closure, named as inference.
3. The Dubai 106.36 print's session date is unverified; the negative-EFS
  reading is a same-week two-print inference, not one instrument's quote.
4. The ask's "Gulf freight ~33" is carried uninterpreted; its unit is
  ambiguous to this seat and guessing is fabrication.
5. Bunker prices are delivered-basis retail proxies, not cargo FOB
  assessments; the $180/mt overstates the cargo arb somewhat. Instrument named
  in the claim.
