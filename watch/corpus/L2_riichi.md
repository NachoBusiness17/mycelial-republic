# L2 Riichi Mahjong Static Contract (SELF-BUILT-CORPUS)

STATUS: SELF-BUILT-CORPUS (fallback draft; not builder-original)
SCHEMA: l2_riichi_static.v1
EXTENDS: L0 Universal Game Contract (six functions, RNG protocol, verdict vocab).
ROLE: W1 insurance — deterministic contract text a verifier can enforce.

## 1. Tile Set & Wall

- 34 distinct tile types; 4 copies each => 136-tile wall.
  - Man (萬) 1-9: 9 types
  - Pin (筒) 1-9: 9 types
  - Sou (索) 1-9: 9 types
  - Honors: East, South, West, North (風) + Haku, Hatsu, Chun (三元): 7 types
- Absolute tile `id`: canonical ordering (man1..9, pin1..9, sou1..9, ez..nz, haku, hatsu, chun) = 0..33, ×4 instances.
- Wall 136 is drawn deterministically from the L0 RNG stream (sec 2 of L0).
- No joker/wild tiles.

## 2. Deal & Turn Order

- Players labeled 0..3, counter-clockwise deal order; seat 0 = East (dealer).
- Deal: 13 tiles to each player; dealer (East) draws the 14th to open.
  - Per contract order: each player takes 4 at a time, 3 rounds (12 each), then 1 each (13), dealer takes 1 => 14.
- Turn: the actor in turn draws 1 from the wall (or a claimed discard), then
  may optionally act, then MUST discard 1 tile face-up (unless winning/kan on draw).
- Turn passes to the next player counter-clockwise after a discard; kan-forward may
  grant the same player a replacement (rinshan) draw.

## 3. Call Rules

Claims on another player's discard, in priority order (highest first):

1. `riichi` — declared (see sec 5). Does not consume the discard.
2. `pon` — 2 matching tiles already held + discard => triplet (3).
3. `kan` — 3 matching + discard => quad; OR closed kan from hand (4 held); OR
   added kan on an already-called pon. Kan claims turn order; rinshan draw replaces.
4. `chi` — 2 sequential same-suit tiles + discard, low/mid position toward the
   discarder only (cannot chi off the player two seats away). Pon/kan beat chi.

Enforcement:
- A claim halts the normal turn, grants the claiming player the discard, and
  interleaves the claimant as next actor. Only one call consumes a discard.
- A player who could have called but declines loses that chance for this discard
  (except riichi priority per house rule; contract default = strict single chance).

## 4. Hand Structure & Yaku Minimum

- Winning hand (tenpai) = 4 melds (chi/pon/kan) + 1 pair = 14 tiles; special 7-pairs
  (7 distinct pairs) and thirteen-orphans are also valid hands.
- Standard contract default: **yaku minimum = 1**. A hand with 0 yaku is NOT a win.
- With a double riichi / all-simples (tanyao) house-rule toggle, minimum may be 1
  with open hand restrictions; contract default = standard Aotenjou rules, min 1, no
  extra penalty beyond yaku count.

Common yaku contract table (name -> definition, han):
- Riichi (1) — closed hand, riichi declared, no tile change after.
- Ippatsu (1) — riichi win on the next draw/discard before any claim.
- Tanyao (1) — all simples, no terminals/honors.
- Pinfu (1) — 4 chi + open pair, no points on pair/discard waits.
- Tsumo (1) — self-draw win.
- Yakuhai (1/2) — triplet of seat/round wind or dragon.
- ... (full yaku list is normative reference; this file enumerates the skeleton.)

## 5. Riichi

- Declared on a closed hand with 4 melds of chi only (no pon/kan on suits) and >=1
  available discardable tile; score sacrifice = 1000 points placed at stake.
- After declaration the hand is locked (no further meld except closed kan on
  existing material); any subsequent winning discard/draw may add ippatsu.
- Riichi is void when furiten (discarded a tile that would complete the win).

## 6. Scoring Table Skeleton

- Base points = fu × 2^(han+2) (cap 2000 for mangan).
- Actual win = base × (1) for non-dealer / (2) for dealer; losses paid by the discarding
  player (ron) or split among all (tsumo).
- Point ladder contract (count of han):
  - 1 han — 1000 (base+3000 offset for dealer variants; table row)
  - 2 han — 2000
  - 3 han — 4000 (mangan floor)
  - 4 han — 8000 (mangan)
  - 5 han — 8000 (mangan@5), 6-7 — haneman 12000, 8-10 — baiman 16000,
    11-12 — sanbaiman 24000, 13+ — yakuman 32000.
  - Yakuman variants (kokushi, suuankou, etc.) fixed 32000 / 48000 dealer.
- Ties to fu: fu is computed deterministically from hand composition; the scoring
  table is static and verifiable given fu+han.

## 7. Draw / Abort Rules

- Draw (exhaustive/sanma): if no win and fewer than 4 kan remain (dead wall limit
  at 14 tiles) => draw. Points: noten penalty (1000 each to the tenpai) per standard.
- Abortive draws (kyuushuu kyuuhai, 4 kans, 4 riichi, 9 terminal-first-draw, chonbo)
  abort the round with no score change. All defined deterministically:
  - 9 terminals/honors in initial hand — abort option.
  - 4 kans — round re-dealt.
  - 4 riichi — round re-dealt.
  - Same wind x4 on first discard — abort.
- Renchan: dealer win or (contract: dealer tenpai on exhaustive draw) keeps the
  dealer seat; otherwise seat rotates. Contract default: dealer win OR tenpai draw
  keeps seat; abortive draws rotate.
- All draw/abort outcomes resolve to verdict TIE with reason code (STALEMATE_TIE,
  ABORT_<rule>) as specified.

## 8. Verifier Enforcement Notes

- All transitions are pure functions over GameState given the L0 RNG stream.
- `legal(state, actor)` must include all claims, riichi, kan, and tsumo/ron options.
- `move` MUST reject calls out of priority order (e.g., chi over a valid pon unless
  declared riichi/tsumo override).
- Every victory is validated against the yaku table (min 1 yaku) and fu/han scoring
  before emitting PASS with reason code + scoring detail.
