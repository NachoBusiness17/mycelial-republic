# L3 — Senet pack, Piccione school
# Path: corpus/L3_packs/senet_piccione.DRAFT.md

> **Status:** DRAFT for seal. **Class:** L3 pack over L1 race/dice.
> **Research flag:** reconstructed. Never upgrade.
> **School:** Peter A. Piccione. Primary meaning-work: “In Search of the
> Meaning of Senet,” *Archaeology* 33.4 (1980): 55–58. Corpus primer also
> cites Piccione 1990. This pack is the Piccione *school*, not a recovered
> rulebook. The 1980 article reconstructs meaning and describes play as
> two sides freely passing toward the end of the board; it does not ship
> a complete modern tournament code. House-effect tables below are the
> playable reconstruction commonly attributed to that school
> (rejuvenation extra-turn, waters as pitfall, exact exits on 28–30).
> Where 1980 prose and later popular tables diverge, the pack names the
> slot instead of blending with Kendall.
> **Board path numbering:** Piccione’s 1–30 path. Shared with the Kendall
> pack. Rules are not shared.
> **Dispute line (must be shown to players):**
> Historians disagree. No attested complete Senet rulebook survives.
> This build uses Piccione. A sibling pack uses Kendall 1978.
> Do not blend. Freely-passing (this pack) is not pair-walls (Kendall).
> **License:** CC-BY-4.0. Credit: Mag Estate (corpus) · Grok/xAI (this pack)
> · Piccione 1980/1990 (reconstruction). Historical rules remain the gift
> of the culture that played them. This file is not that gift.
> **Consumption:** L0 → L1 race/dice → this pack → L4 instance.

---

## HISTORY MODULE (not mechanics)

- Senet (“passing”) is attested as a 30-house game. Rules are lost.
- Piccione’s published work is primarily about religious meaning layered
  onto the board by the New Kingdom, not a claim that Old Kingdom play
  used these exact gates.
- 1980 description: contestants freely pass each other toward final
  superiority at the edge of the board. That sentence is why this pack
  does not import Kendall walls.
- Named houses in the meaning-work include rejuvenation / mummy-workshop
  at 26, waters of chaos at 27, Re-Horakhty at 30. Ritual gloss stays
  in this module. F3 uses only the clauses below.

---

[PROMPT-BODY-START — byte-stable from here]

## PACK IDENTITY

GAME=senet
SCHOOL=piccione
FLAG=reconstructed
ENGINE=race_dice
PLAYERS=2
ROLES=dark,light
FIRST_ROLE=dark
PIECES=5
CAPTURE=off
CONCURRENT=on
TRACK=linear
N=30
DEVICE=sticks4
ENTRY=on
ROLL_EXACT_BEAR=on

## SHARED BOARD ADDRESS

Identical path to senet_kendall:
  row1:  1  2  3  4  5  6  7  8  9 10
  row2: 20 19 18 17 16 15 14 13 12 11
  row3: 21 22 23 24 25 26 27 28 29 30

## INIT

All pieces start in STOCK (ENTRY=on).
POS empty.
STOCK dark=5, light=5.
TURN=dark.

F1 example at INIT:
RACE;T=linear;N=30;POS=;STOCK=dark:5,light:5;TURN=dark;ENTRY=on;CAPTURE=off;SEED={phrase};SEQ=0

PIECES slot may be 7 only if the operator sets it. Default 5.
Do not copy Kendall’s on-board alternating INIT into this pack.

## F0 BINDING

DEVICE=sticks4 as L0.
SCORE ∈ {1,2,3,4,5}.
BONUS_TURN on SCORE ∈ {1,4,5} after a legal action resolves.
If the only action was PASS, no bonus.

## ENTRY

P-E1 A role with STOCK>0 may ENTER one piece onto house SCORE
     if that house is legal under P-M2.
P-E2 Entering is an action type MOVE with from=STOCK.
P-E3 Pieces already on the track may be moved instead of entering.

## MOVEMENT CLAUSES

P-M1 Move exactly one own piece by SCORE houses forward, or ENTER.
P-M2 Destination may be empty or occupied. CONCURRENT=on.
     Freely passing is legal. No wall clause exists in this pack.
P-M3 Own pieces may occupy the same house only if CONCURRENT=on
     (default on). If an operator sets CONCURRENT=off, landing on own
     piece becomes illegal; do not then import Kendall protection.
P-M4 CAPTURE=off. Landing does not send an enemy to 15 or to STOCK.
     Do not steal K-C1.
P-M5 If no legal action exists, PASS.
P-M6 House 26 is a mandatory station: a piece may not occupy 27..30
     or BEAR unless it has LAND26=true.

## HOUSES

P-H26 House of Rejuvenation / Happiness.
      On landing: BONUS_TURN (in addition to F0 bonus if any? NO —
      one bonus maximum per turn).
      SAFE for capture (irrelevant while CAPTURE=off; kept so a later
      capture-on variant can load this house table).
      SCORE=5 while occupying 26 may BEAR directly.
P-H27 House of Water / Waters of Chaos.
      On landing: JUMP to 15 if empty, else first empty house index<15.
      Miss-a-turn for that role’s next turn.
      Slot P-H27-ALT (default OFF): instead of jump, piece stays and
      may BEAR on SCORE=4, and no other piece of that role may move
      while the drowning piece remains. If you turn this slot ON,
      say so in CITE. Do not silently enable it.
P-H28 House of Three Truths. No MOVE off this house except BEAR on
      SCORE=3.
P-H29 House of Re-Atum. No MOVE off this house except BEAR on SCORE=2.
P-H30 House of Re-Horakhty / Horus. No MOVE off this house except
      BEAR on SCORE=1.
P-OVERSHOOT If a piece on 28, 29, or 30 is forced to apply a SCORE
      that is not its bear-gate and P-H28/29/30 forbid MOVE, the
      action is illegal. Do not move backward unless the operator
      enables slot P-BACK=on (default OFF). Popular tables that
      bounce extra pips backward are not assumed.

## BEAR / WIN

P-W1 BEAR only from the house clauses above, exact SCORE.
P-W2 WIN when STOCK_OFF[role]=PIECES.
     Track off-board completions as STOCK_OFF, separate from ENTRY stock.
     Encode in POS by omitting the piece and incrementing
     STOCK_OFF in a pack tail: append ;OFF={role:count}
     to F1. L0 race grammar permits pack tails after SEQ.

## SQEFFECT TABLE (engine order)

26: reroll/bonus (BONUS_TURN), safe/ritual
27: jump target=15 (or first empty <15); miss-a-turn
28: none (bear gate 3)
29: none (bear gate 2)
30: none (bear gate 1)
15: none
other: none

## WHAT THIS PACK REFUSES

No pair-protection.
No three-piece wall.
No mandatory swap-capture.
No Kendall-on-board fourteen-piece INIT.
If a request asks for those, load senet_kendall instead.
Do not merge.

## OUTPUT

Use L0 OUTPUT CONTRACT.
FLAG=reconstructed
PACK_CLAUSE must name P-* ids.
Player-facing dispute line once per session:
  HISTORIANS DISAGREE — this build uses Piccione.
  Kendall 1978 is a different pack.

[PROMPT-BODY-END]
