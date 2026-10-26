# L3 — Senet pack, Kendall school
# Path: corpus/L3_packs/senet_kendall.DRAFT.md

> **Status:** DRAFT for seal. **Class:** L3 pack over L1 race/dice.
> **Research flag:** reconstructed. Never upgrade.
> **School:** Timothy Kendall, *Passing Through the Netherworld: The Meaning
> and Play of Senet, an Ancient Egyptian Funerary Game* (Belmont: Kirk Game
> Company, 1978). Original published playable reconstruction used **seven**
> pieces per side; later tables circulating as “Kendall” use five. This pack
> defaults PIECES=7 and exposes PIECES as a slot. Do not silently switch.
> **Board path numbering:** the 3×10 boustrophedon path as numbered in
> Piccione’s published path diagram (standard address space). Numbering is
> shared. Rules are not.
> **Dispute line (must be shown to players):**
> Historians disagree. No attested complete Senet rulebook survives.
> This build uses Kendall 1978. A sibling pack uses Piccione.
> Do not blend.
> **License:** CC-BY-4.0. Credit: Mag Estate (corpus) · Grok/xAI (this pack)
> · Kendall 1978 (reconstruction). Historical rules remain the gift of the
> culture that played them. This file is not that gift. It is a named guess.
> **Consumption:** L0 → L1 race/dice → this pack → L4 instance.

---

## HISTORY MODULE (not mechanics)

- Object: senet boards of 30 houses in three rows of ten are attested in
  Egypt across a long period. Complete rules are not.
- Kendall 1978 is a playable reconstruction from boards, tomb scenes, and
  later religious captions. It is not period rules.
- Companion reconstructions exist (Piccione 1980/1990; also Bell 1979 and
  others). They are other packs.
- Funerary meaning of named houses is interpretive. It does not enter F3.

---

[PROMPT-BODY-START — byte-stable from here]

## PACK IDENTITY

GAME=senet
SCHOOL=kendall_1978
FLAG=reconstructed
ENGINE=race_dice
PLAYERS=2
ROLES=dark,light
FIRST_ROLE=dark
PIECES=7
CAPTURE=on
CONCURRENT=off
TRACK=linear
N=30
DEVICE=sticks4
ENTRY=off
ROLL_EXACT_BEAR=on

## SHARED BOARD ADDRESS

Houses 1..30.
Path (structural, both Senet packs):
  row1:  1  2  3  4  5  6  7  8  9 10
  row2: 20 19 18 17 16 15 14 13 12 11
  row3: 21 22 23 24 25 26 27 28 29 30
Movement is along that path only. No backward APPLY except where a clause
names a destination.

## INIT

Place 14 pieces on houses 1..14 alternating:
  1 dark, 2 light, 3 dark, ... 13 dark, 14 light.
STOCK both roles = 0.
TURN=dark.
ENTRY=off (all pieces already on track).
If PIECES=5 (slot override): place on 1..10 only, same alternation;
do not invent a third setup.

F1 example at INIT (PIECES=7):
RACE;T=linear;N=30;POS=dark:d1:1,light:l1:2,dark:d2:3,light:l2:4,dark:d3:5,light:l3:6,dark:d4:7,light:l4:8,dark:d5:9,light:l5:10,dark:d6:11,light:l6:12,dark:d7:13,light:l7:14;STOCK=dark:0,light:0;TURN=dark;ENTRY=off;CAPTURE=on;SEED={phrase};SEQ=0

## F0 BINDING

DEVICE=sticks4 as L0.
SCORE ∈ {1,2,3,4,5}.
The model reports SCORE. It does not pick a piece first and then invent
a SCORE that fits.

BONUS_TURN: none in this pack unless a later corpus patch adds one.
Do not import extra-turn-on-1-or-4-or-5 from other schools.

## MOVEMENT CLAUSES

K-M1 Move exactly one own piece by SCORE houses forward along the path.
K-M2 Destination must be empty of own pieces. Landing on own piece = illegal.
K-M3 Landing on an isolated enemy piece is a legal capture (K-C1).
K-M4 Landing on a protected enemy piece is illegal.
K-M5 A piece may not pass a wall (K-B2).
K-M6 If no legal MOVE exists for this SCORE, PASS. Do not invent a move.
K-M7 No piece may pass house 26 without having landed on 26 at least once
     this piece’s life. Bypass of 26 is illegal.

## PROTECTION AND WALLS

K-B1 PROTECTED: an enemy piece adjacent on the path to at least one other
     piece of the same role is protected. Adjacent means path-neighbors
     (e.g. 10-20, 11-21), not grid-neighbors that skip the path.
K-B2 WALL: three consecutive path-houses occupied by the enemy may not be
     passed. A move whose path interval strictly contains that block is
     illegal. Landing on the first of the three is also illegal.
K-B3 Houses 28 and 29 do not grant pair-protection even if adjacent friends
     sit there. (House 30 is capturable. House 26 is a refuge; see K-H26.)

## CAPTURE

K-C1 Isolated enemy on destination: swap.
     Mover occupies destination.
     Captured piece is sent to the first empty house of lower index than
     the destination, searching backward along the path.
     If none, UNCERTAIN — do not invent an off-board capture.
K-C2 CAPTURE is off on houses marked SAFE by house clauses.
K-C3 Capture is optional in some circulating Kendall tables and mandatory
     in others. This pack: MANDATORY if K-C1 applies and the move is the
     chosen action. Do not offer a silent ignore.

## HOUSES

K-H15 House of Rebirth. Ordinary house except it is the return target
      bound to house 27.
K-H26 House of Beauty / Happiness. Must land. SAFE refuge (no capture
      while occupying 26). From 26, later turns may proceed to 27-30
      or bear off only via later house clauses, never by skipping 26.
K-H27 House of Water / Humiliation. On landing, immediate jump to 15
      if 15 empty; else to the first empty house of index < 15,
      searching backward. Then end turn.
K-H28 House of Three Truths. Piece may not MOVE to another house.
      BEAR legal only on SCORE=3.
K-H29 House of Re-Atoum. Piece may not MOVE to another house.
      BEAR legal only on SCORE=2.
K-H30 House of Horus. Capturable (not SAFE).
      BEAR legal on SCORE=1.
      Alternate Kendall clause (slot): BEAR also legal on any SCORE
      if houses 1..10 are all empty. Default ON. Name the slot when used.

## BEAR / WIN

K-W1 BEAR removes the piece to STOCK+1 for that role. Cell becomes empty.
K-W2 WIN when STOCK[role]=PIECES.
K-W3 DRAW is not a default. Do not declare DRAW to end a stall;
     use PASS until a legal move exists or the operator aborts.

## SQEFFECT TABLE (engine order)

26: safe/ritual
27: jump target=15 (or first empty <15)
28: none (bear gate SCORE=3)
29: none (bear gate SCORE=2)
30: none (bear gate SCORE=1)
15: none
other: none

## OUTPUT

Use L0 OUTPUT CONTRACT.
FLAG=reconstructed
PACK_CLAUSE must name K-* ids.
Player-facing dispute line once per session, not every turn:
  HISTORIANS DISAGREE — this build uses Kendall 1978.

[PROMPT-BODY-END]
