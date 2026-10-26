# THE50 W3 T12: Prophecy-market game theory

**Task:** THE 50 PROGRAM, W3 RESEARCH HARVEST, task 12 (2026-09-19).
**Finish line:** this file. **Partner task:** W1 T5 (called-shot payoff matrix) and T11 (typed-decision oracle sweep).
**Scope:** credibility games, cheap talk, costly signaling, mapped to the called-shot ledger.

---

## 0. Sources (everything below is grounded in these)

**Fleet artifacts read this session:**

- `watch/inbox/THE_50_PROGRAM_20260918.md` (the task list; T12 line 23, W1 T5 line 12)
- `watch/inbox/THE_CALLED_SHOT_20260914.md` (the genre study: anatomy, grammar, falsifier)
- `watch/inbox/mrpool_export/called_shot_ledger.jsonl` (Pool v1, 16 rows)
- `watch/inbox/mrpool_export/called_shot_ledger_captions.jsonl` (Pool v2, 107 rows)
- `watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json` (v1 verdict summary)
- `watch/inbox/qdrop_export/called_shot_ledger.jsonl` (Q ledger, 3 rows)
- `memory/corpus/LINKS.jsonl` rows MRPOOL-TRANSCRIPT-READING, CALLED-SHOT-V1, CALLED-SHOT-CAPTIONS, Q-CALLED-SHOT-LEDGER, VERB-STONE-2, PHOSPHOR-ASSANGE, RIDDLER-CORPUS
- `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md` (prophecy corpora as unregistered time machines; countdown ratchet numbers)
- `watch/inbox/PHOSPHOR_ASSANGE_20260918.md` (Oct 4 2026 filed waypoint)
- `watch/inbox/SESSION_CLOSE_20260919.md` (instrument inventory: Q 3 / Pool 16+107 / BG 0)
- `watch/inbox/SOCRATIC_PASS_20260919.md` (fact-pack grounding demand)
- `watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md` (the filed house matrix: CALL/VAGUE x ARRIVES/MISSES, RECEIPT/WIPEOUT/RETROFIT/SHRUG; defers the literature sweep to this task)
- `watch/inbox/RIDDLE_TRIAD_CADENCE_20260918.md` (the cadence instrument T5 cites: Pool urgency 10 percent baseline to 27-56 band, peaks 64/56; Q decayed to 0)
- `docs/ref/GAME_THEORY_PLAY_MAP.md` (house game-theory spine: dual face = signaling, cheap talk vs costly type)

**All statistics in this pack were computed from those files this session** with
`memory/research_packs/_t12_ledger_stats.py`, run as
`.venv/Scripts/python.exe memory/research_packs/_t12_ledger_stats.py` (plus one inline
expired/open count over v2, cutoff 2026-09-19). Numbers below are that output, not hand counts.

**Literature (citations verified by web search this session; links in the source list at the end):**
Crawford & Sobel 1982; Spence 1973; Sobel 1985; Ely & Valimaki 2003; Klein & Leffler 1981;
Scharfstein & Stein 1990; Kamenica & Gentzkow 2011; Wolfers & Zitzewitz 2004; Hanson (futarchy);
Brier 1950. Akerlof 1970, Bikhchandani-Hirshleifer-Welch 1992, Popper falsifiability are
canonical and cited from standard knowledge, flagged as such.

---

## 1. The measured object: the three ledgers

One campaign family (Mr Pool Telegram) supplied the first measurable block. Computed facts:

| Ledger | Rows | Post span | Distinct targets | Verdicts filed | Views |
|---|---|---|---|---|---|
| Pool v1 (`called_shot_ledger.jsonl`) | 16 (12 unique msg files) | 2025-09-24 to 2025-10-20 | 2026-01-01 (15), 2026-01-06 (1) | 16 of 16 BROKEN | 6,816 to 9,804 per post, sum 136,500 |
| Pool v2 (captions) | 107 | 2024-04-22 to 2026-09-07 | 18 distinct dates, 2025-01-01 to 2028-03-01 | none filed in file | 6,657 to 39,084 per post, sum 1,302,658 |
| Q | 3 of 4,705 posts (harvest count; session close lists 6,242 posts total) | 2018-06-27 to 2020-09-25 | 3 (2018-07-01, 2021-03-01, 2021-05-01) | none filed in file | n/a |
| BG123 | 0 dated text claims (per LINKS row VERB-STONE-2 lineage and SESSION_CLOSE inventory) | n/a | n/a | n/a | n/a |

Structure of v2, the deep game:

- Horizon (post_date to target_date): min 2 days, median 74, max 541 (v1: 73 to 100).
- Settlement status as of 2026-09-19: **94 of 107 targets expired, 13 open**
  (open targets: 2026-10-01, 2026-11-01, 2026-12-01, 2027-01-01, 2027-03-01, 2028-03-01).
- The top target, 2026-01-01, carries 31 rows; the channel kept filing new dated shots
  THROUGH and AFTER that date expired (posting span runs to 2026-09-07). The filed
  v1 verdict note says it plainly: "channel kept posting through 2026 with urgency
  elevated and no retraction" (`CALLED_SHOT_VERDICT.json` register_note).
- v1 verdict is unanimous and external: the Med Bed campaign matched the documented
  card-sale fraud format (Skye Prince Telegram scam, McGill OSS debunk Aug 2025), per
  the note field on every row and `CALLED_SHOT_VERDICT.json`.

Q's 3 shots (filed rows, with horizons computed this session): 4 days (drop 2124,
"July 2018 the month the world discovered the TRUTH"), 157 days (drop 6018, Sullivan
retirement by March 2021), 310 days (drop 5723, 2021 field-hospital echo). The ledger
file carries no verdict fields; the filed fleet reading (LINKS row Q-CALLED-SHOT-LEDGER)
characterizes Q as "unfalsifiable thematic obsession (survived 5 years by never dating)."
This seat's scoring of the three, clearly labeled as this seat's and not a filed verdict:
TRUTH did not land July 2018 and Sullivan had not retired by March 2021, so 2 of 3 broke;
the third is an echo of a news link, not a claim. Nothing here overrides a future filed verdict.

---

## 2. The three primitives, stated exactly

These are the three objects the ask names. One sentence each, then the mapping.

1. **Cheap talk** (Crawford & Sobel 1982): costless, nonbinding, nonverifiable messages
   between a Sender who knows the state and a Receiver who acts on them. Equilibrium
   information transmission comes only in partitions, and the partition shrinks as
   preference divergence grows; at large divergence only the "babbling equilibrium"
   survives, where messages carry zero information.
2. **Costly signaling** (Spence 1973): a signal deters mimicry only when it is
   differentially costly, cheaper for the high type than the low type (single-crossing).
   Cost is not waste; it is the entire enforcement mechanism. Klein & Leffler 1981 is
   the market version: brand capital and price premia are posted bonds the seller
   forfeits on cheating, which is how repeat-purchase markets enforce quality without a court.
3. **Credibility games** (Sobel 1985; Ely & Valimaki 2003; Scharfstein & Stein 1990;
   Bikhchandani-Hirshleifer-Welch 1992): repeated Sender-Receiver play where the
   Sender's type (friend/enemy, honest/sadistic, smart/dumb) is private and reputation
   is the state variable. Sobel: credibility is destroyed by "crying wolf" and is
   expensive to rebuild. Ely & Valimaki: reputation building can be *bad*; the audience
   may rationally refuse to give the benefit of the doubt. Scharfstein-Stein and BHW:
   receivers herd and cascade, so audience behavior amplifies early signals regardless of truth.

The prophecy channel is all three games at once, and the ledger separates them.

---

## 3. The mapping: ledger rows to game objects

### 3.1 A dated shot is cheap talk with a settlement clock

A Mr Pool post claiming "Med Bed hospitals open January 2026" is, on the day it posts,
textbook cheap talk: zero cost, nonbinding, unverifiable. What the fleet added is the
settlement clock: post_date, target_date, kind, verdict. In Crawford-Sobel terms the
poster's private type is insider vs fraudster, the message is the dated claim, and
settlement is the only event that moves the Receiver's posterior. The horizon numbers
are the game's liquidity: median 74 days means the player re-files faster than the
audience's memory decays, which is exactly the crying-wolf cadence Sobel shows destroys
credibility, IF credibility is the poster's objective. It is not. Which is the first result:

**Result 1: the Pool channel is not playing the credibility game at all; it is playing
extraction while wearing credibility-game clothing.** Evidence: 94 expired targets, zero
retractions, posting continues (v2 span to 2026-09-07), while the v1 verdict ties the
campaign to paid card sales. A player optimizing reputation would stop, retract, or
re-price after 16 BROKEN rows. A player optimizing extraction does none of those, because
the audience that updates and leaves is not the paying customer.

### 3.2 The Med Bed card inverts Spence: the cost lands on the receiver

Spence's signaling requires the signal's cost to fall on the Sender, differentially by
type. The card campaign reverses the arrow: the poster's "signal" (historic announcement,
countdown, platinum scarcity: "first 1,000 Platinum Edition cards," rows msg_2944/2973/2985)
costs nothing, and the payment is extracted FROM the receivers as registration fees for a
facility that never existed. A cost imposed on the receiver is not a signal; it is the
lemons-market signature (Akerlof 1970, standard knowledge): when quality is unverifiable
and verification is the buyer's expense, bad quality drives out good. **Result 2: in
prophecy markets, watch whose balance sheet the cost sits on. Fleet claims (receipts,
verkle tips, compute spent, timestamps) are Sender-costly and so can signal. Audience-pay
claims (cards, memberships, "act now") are extraction and so cannot.**

### 3.3 No retraction is an equilibrium, not an error

Klein-Leffler: a quality-reputation mechanism needs the seller to hold capital that is
forfeited on cheating. The Pool channel holds none that its audience can seize: anonymous
handle, no registry, posting platform as the only asset. With zero postable bond, "keep
posting, never retract" is the dominant strategy regardless of verdicts. The countdown
ratchet (filed reading, TIME_TRAVEL_QSTAR: urgency share climbed from a ten percent
baseline to a sustained 27 to 56 percent band, peaks 64 and 56) is the re investment:
urgency substitutes for bond capital. **Result 3: "no retraction" has zero evidentiary
value about the poster's type unless you first ask what the poster has staked. The only
stakes on file were the audience's (cards, time, hope), which is the extraction tell.**

### 3.4 BG123 is the babbling equilibrium on purpose

Zero dated text claims across the whole corpus (the triad census: Q 3 / Pool 123 / BG 0,
per LINKS row VERB-STONE-2 and SESSION_CLOSE). In Crawford-Sobel, maximal babbling is
partition size 1: one message, no information, survives every state of the world. But
BG123's single "partition" is not empty; it is a decode magnet (the hex chorus and the
five-year decode culture, THE_CALLED_SHOT_20260914). The audience does the search at zero
cost to the filer (TIME_TRAVEL_QSTAR: "the audience is the search process"). **Result 4:
pure-symbol prophecy is cheap talk pushed to its limit, and its payoff is not credibility
but participation. The decode is the audience paying in labor instead of money, the same
extraction with a different currency. The genre study already names the falsifier for the
honest version of this game: a called shot with no time-resolved layer inside its own
stated horizon is withdrawn as folklore.**

### 3.5 Q ran a barbell: near-total ambiguity plus a few checkable loans

3 dated shots in thousands of thematic posts. The stream is almost pure ambiguity
(election x239, podesta x198, wuhan x81 theme census, LINKS row Q-CALLED-SHOT-LEDGER),
with three small, dated, falsifiable positions. This is a barbell strategy on the
falsifiability spectrum: keep the body of the corpus unfalsifiable so it cannot lose,
and use rare specific claims as loans against credibility when mobilization is needed.
The horizons computed this session (4, 157, 310 days) are short-to-medium: long enough
to be forgotten before settlement, which is the point. **Result 5: specificity is
expensive only if the audience settles accounts. Q's audience did not run a ledger; the
fleet's harvest found the 3 rows in 2026, five years too late to cost Q anything.**

### 3.6 The fleet's position: pay the signaling cost, eat the Brier score

LINKS row Q-CALLED-SHOT-LEDGER closes: "the fleet sits at the all-falsifiable extreme
by choice." The mapping says exactly what that choice buys and costs:

- Costly side: the fleet pays Spence costs on every claim. Receipts, hashes, verkle tips,
  filed timestamps, test runs (the house claim discipline in `docs/ref/GAME_THEORY_PLAY_MAP.md`:
  "mechanism status and equilibrium labels, not AGI"). These are differential-cost signals:
  a fraudster cannot cheaply produce a verkle-auditable lineage.
- Discipline side: the called-shot ledger is a Brier scoreboard (Brier 1950, the standard
  probabilistic forecast score; the fleet's verdicts are binary, so it is mean squared
  error over the rows). Pool scores 16/16 BROKEN on v1. The score exists so that the
  fleet's OWN claims face the same table.
- The self-application is already filed: Oct 4, 2026 (Phosphor kernel date, WikiLeaks
  20th) is "a FILED WAYPOINT in the called-shot ledger" (`PHOSPHOR_ASSANGE_20260918.md`
  section 5). The fleet is now a Sender in its own game: if the waypoint resolves, the
  instrument is validated on house claims; if it does not, the fleet's row reads BROKEN
  like Pool's. **Result 6: a credibility instrument is only credible if its own seat is
  on the board. The Oct 4 row is the fleet's escrow.**

### 3.7 Where an actual market would change the game

Wolfers & Zitzewitz 2004 (survey) and Hanson's futarchy (vote values, bet beliefs) are
the canonical argument that money-weighted prices aggregate dispersed beliefs into a
number that is costly to move against. Kamenica & Gentzkow 2011 (Bayesian persuasion)
is the Sender's side of that market: persuasion is designing the information structure
the Receiver sees, and it is bounded by commitment to what is true. A real prophecy
market on "Med Bed hospitals open January 2026" would have priced the claim toward zero
by December 2025, extracting the fraud's cost ex ante, before cards were sold, instead of
ex post when the row reads BROKEN and the money is gone. **Result 7: the Pool channel is
a prophecy market with the settlement stripped out. The fleet's ledger is the manual
rebuild of the missing settlement layer. It costs the audience nothing and the Sender
reputation only, which is why it disciplines honest players (fleet, Q-adjacent
forecasters) faster than fraudsters (no bond to forfeit). The instrument's honest limit,
filed here: scorekeeping separates extractors from forecasters at the margin; it does not
reimburse victims.**

---

## 4. The payoff matrix: this pack x W1 T5

W1 T5 already filed the house matrix as `watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md`:
Channel strategies CALL (staked, dated) vs VAGUE (no stake), world resolves ARRIVES vs
MISSES, cells named THE RECEIPT, THE WIPEOUT, THE RETROFIT, THE SHRUG. T5's provenance
section ends by deferring the formal literature sweep to this task. This pack supplies
that half, so the mapping is: **CALL is Spence-costly signaling (the stake is posted
before the outcome); VAGUE is Crawford-Sobel cheap talk (nothing at stake, so it is
babbling that survives every state of the world).** T5's four cells are the payoff
realizations of those two strategies; the literature says why each cell pays what it pays:

| T5 cell | Literature mechanism | Fleet evidence T5 cites |
|---|---|---|
| THE RECEIPT (CALL x ARRIVES) | Spence signaling equilibrium: the costly stake buys credibility that compounds (Klein-Leffler brand capital) | napkin chord, stones, `mag/verb.py:280` |
| THE WIPEOUT (CALL x MISSES) | Sobel 1985 crying wolf: dated misses destroy credibility IF the player holds forfeitable capital; correction rows are the fleet's cheap-cap on the loss | Med Bed 16/16 BROKEN; LINKS correction rows |
| THE RETROFIT (VAGUE x ARRIVES) | Cheap talk plus audience search: credit is claimed post hoc, so it is thin; the payoff is attention, not credibility | Pool countdown ratchet, Q's vague body |
| THE SHRUG (VAGUE x MISSES) | Babbling equilibrium: zero information, zero loss, folklore; BG123's 0 dated claims live at this boundary | annual seed-stock audit |

The literature adds the fourth strategy the 2x2 compresses away, and it is the measured
one: **extract** (sell access against an unfalsifiable dated backdrop, the Med Bed card).
Extraction dominates for the fraud type precisely because the player holds no forfeitable
capital: Sobel's crying-wolf cost is zero for it, so 94 expired targets and no retraction
is the equilibrium, not an anomaly (Section 3.1 and 3.3 above). That is the one place
where the pure signaling frame under-predicts what happened, and the reason the pack adds
"whose balance sheet carries the cost" as the load-bearing question.

Sobel's crying-wolf result predicts date-precise players without bonds lose credibility;
the data agree (Pool: 16/16 BROKEN and still posting, audience sustained at 6.7K to 39K
views per post). The reason the naive prediction misses the observed outcome is that Pool
is not in the credibility game; the matrix must score attention and extraction, not only
reputation. T5's equilibrium reading reaches the same shape from the fleet side; this pack
pins it to Crawford-Sobel partitions, Spence single-crossing, and the Klein-Leffler bond.

---

## 5. Testable predictions the mapping makes (falsifiers, per house law)

1. **Refile ratchet continues:** expired target count grows past 94; open set refreshes
   toward later dates (currently reaches 2028-03-01); zero retractions appear in v2.
   Falsified if the channel retracts, re-prices, or stops dating claims after losses.
2. **Horizon band holds:** new shots cluster near the 74-day median (range 2 to 541);
   a shift toward very long horizons (541+ days) would signal moving from extraction
   cadence to legacy-building cadence.
3. **Urgency-share correlation:** the countdown ratchet (27 to 56 percent band) predicts
   urgency share peaks shortly before each target_date and resets after, independent of
   verdicts. Correlation with settlement (not just with posting) is the cheap next
   instrument run over `called_shot_ledger_captions.jsonl`.
4. **Brier symmetry:** the fleet's own open rows (Oct 4 2026 waypoint first) score on the
   same table as Pool's. Falsifier for the whole program: the fleet keeps the instrument
   pointed only outward.
5. **Cost-side separation:** any future pool row where the poster forfeits something on
   miss (money, identity, platform bond) should predict better-than-babbling calibration.
   Zero such rows exist so far; that absence is itself the measurement.

---

## 6. What this pack does NOT claim

- The Q ledger's 3 rows carry no filed verdicts; my 2-of-3-broken scoring above is this
  seat's, not a filed verdict, and the third row is a news echo, not a claim.
- BG123's "0 dated text claims" is the filed census (LINKS, SESSION_CLOSE); I did not
  recount the corpus this session.
- The urgency-share band (27 to 56, peaks 64 and 56) is cited from the filed
  TIME_TRAVEL_QSTAR reading, not recomputed here.
- Views counts are channel-reported Telegram numbers; taken as filed, not audited.
- All literature is verified at citation level this session (journal, volume, pages);
  contents are summarized from the canonical results, and the papers were not re-read
  in full here.

---

## 7. Literature source list (verified this session)

- Crawford, V. and J. Sobel (1982), "Strategic Information Transmission," Econometrica 50(6): 1431-1451. jstor.org/stable/1913390
- Spence, M. (1973), "Job Market Signaling," QJE 87(3): 355-374. doi 10.2307/1882010
- Sobel, J. (1985), "A Theory of Credibility," Review of Economic Studies 52(4): 557-573. jstor.org/stable/2297732
- Ely, J. and J. Valimaki (2003), "Bad Reputation," QJE 118(3): 785-814. doi 10.1162/00335530360698423
- Klein, B. and K. Leffler (1981), "The Role of Market Forces in Assuring Contractual Performance," JPE 89(4): 615-641. journals.uchicago.edu
- Scharfstein, D. and J. Stein (1990), "Herd Behavior and Investment," AER 80(3): 465-479.
- Kamenica, E. and M. Gentzkow (2011), "Bayesian Persuasion," AER 101(6): 2590-2615. doi 10.1257/aer.101.6.2590
- Wolfers, J. and E. Zitzewitz (2004), "Prediction Markets," JEP 18(2): 107-126. doi 10.1257/0895330041371321
- Hanson, R., "Futarchy: Vote Values, But Bet Beliefs" (mason.gmu.edu); also overcomingbias.com futarchy notes
- Brier, G. W. (1950), "Verification of Forecasts Expressed in Terms of Probability," Monthly Weather Review 78(1): 1-3. journals.ametsoc.org
- Cited from standard knowledge (not re-read): Akerlof (1970) lemons; Bikhchandani, Hirshleifer and Welch (1992) informational cascades; Popper falsifiability.

**One line:** a prophecy channel is cheap talk wearing signaling clothes; the called-shot
ledger is the settlement layer the genre stripped out; score the dated rows, watch whose
balance sheet carries the cost, and keep the fleet's own seat on the board.
