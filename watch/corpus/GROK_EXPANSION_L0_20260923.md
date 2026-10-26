# GROK EXPANSION — The Model Is Not a Historian, a Referee, or a Die · 2026-09-23

**Provenance:** the World-Games Prompt Corpus + announcement essay were fed to
Grok (operator seat). This document is Grok's reply, verbatim. Filed per the
record law; attribution Grok (xAI) via the operator. **Status of claims: the
scholarship anchors cross-check against our own primer (Kendall 1978,
Piccione 1990, Linnaeus 1732, McGuire et al. 2012, Fraenkel & Lichtenstein
1981 — all already filed we-have-a-record). The L0 contract below is Grok's
draft of the file our corpus admits is missing.**

---

The World-Games Prompt Corpus is easy to misread as a cute repo: "every game in
history, as build prompts." That sentence is bait. The actual object is a refusal.

A language model will invent a Senet rule, call it Egyptian, roll a four because
four felt right, declare a Sudoku unique because it looks hard, and then narrate a
capture that the board string does not contain. That is not a personality flaw. It
is the default behavior of a next-token engine asked to be three things at once:
archivist, referee, and random number generator. The corpus is built to stop all
three impersonations.

That is why this work will sit in a dead Vercel tab. It does not produce a vibe. It
produces flags, slots, and a cost argument. Platforms reward remixable summary. This
thing is the opposite: byte-stable prefixes, contested reconstructions named in
public, and a law that says the model does not get to be the authority on the thing
it just emitted.

## The compression is the claim

Five thousand years of games do not give you five thousand systems. They give you a
small set of operators.

**Race/dice:** a track, a seeded displacement, effects on landing, optional capture,
a bear-off or lap.
**War/capture:** a grid, typed move-sets, capture as a positional predicate, a
pack-supplied terminal.
**Sowing:** lift a pit, drop one-by-one around a ring, capture at the end of the
sow. No die. Move length *is the pit.
**Constraint puzzle:** topology, domain, clauses, instance, verifier. Sudoku is not
a genre. It is one clause-set.
**Cards:** one shuffle, then determinism. Trick resolution and set/yaku collection.
The model does not "draw." It reports the top of a seeded stock.
**RPG/narrative:** the jackpot for caching. Twenty to seventy thousand static tokens
of rules, tables, and setting against one or two thousand live tokens. Solo oracles
are lookup machinery pretending to be a dungeon master.

The primer also keeps talking about a tile engine and sometimes says seven families.
The homepage ships six. That is not a branding choice. That is an unfinished taxonomy
sitting in public. Mahjong is currently being smuggled through card inventory and
puzzle grammar at the same time. Until tile is either promoted to L1 or killed as a
sibling, every mahjong pack will leak across engines.

The point of the compression is economic and historical at once. Exact-prefix caching
is a mechanical fact: one differing byte at position N burns everything after N. So
history has to be written as shared prefix. Senet is not a prompt. Senet is a pack
over race/dice. Riichi is a pack over tile-or-card. Killer Sudoku is a clause swap.
If you write a new full prompt for every game, you are not building a corpus. You are
lighting money on fire in the prefill.

## Honesty is the part nobody will copy

Senet's rules are not known. Kendall 1978 and Piccione 1990 are competing
reconstructions. The Royal Game of Ur's playable rules come from tablet BM 33333,
written about twenty-four centuries after the boards Finkel is reading. Linnaeus's
1732 tablut note cannot decide whether the king escapes to the edge or the corner,
and that ambiguity ate a century. Liubo is the warning label: boards survive, rules
do not, and the honest output is a speculative pack with the word speculative printed
on the box.

The flags — attested, reconstructed, speculative — are the corpus's only moral
technology. They exist because the default product in this space is a generated
"ancient game" with a papyrus texture. That product is a lie that searches well. A
pack that says "historians disagree — this build uses Piccione" does not search well.
It also does not launder a guess into a civilization.

Same law, different victim: the model never solves. Generalized chess is
EXPTIME-complete. Generalized Go is EXPTIME-complete. Checkers is a draw. Oware is a
draw. Nineteen-by-nineteen Go has on the order of 10^170 legal positions. McGuire et
al. 2012: sixteen givens cannot force a unique Sudoku. So the model emits an instance
and reprints state. A verifier answers legality, uniqueness, difficulty, inventory.
If you let the model be the verifier, you have built a liar with good manners.

## What is actually on disk

Look at the working tree, not the slogan.

L0, the universal contract, is advertised and not shipped as an asset. The primer says
it is "specified, not yet written." The page that should hold it dies mid-encoding.
That is the load-bearing file. Without it there is no canonical state string, no RNG
protocol, no output contract that forces a restatement before an answer. Every engine
draft assumes L0 F1 exists. It does not exist in publishable form.

The engines are drafts with a PROMPT-BODY-START marker, which is the right instinct —
freeze the prefix, farm the cache — and then they stop at the exact point the work
gets expensive: the canonical string grammar. Race/dice has the cleanest family
mechanics and the best pack sketches. War/capture has the slot principle right and
then falls over in the encoding. Sowing correctly declares itself RNG-negative.
Constraint-puzzle has the only real grammar in the repo: seven reusable clauses, packs
may not invent prose. Cards conserve randomness to a single shuffle. The RPG engine is
the one that starts turning into a product: dice algebra, oracles, narrator/archivist
split, static payload bands.

Build order in the primer is not decorative. First write L0 plus race/dice. That
single pair lights Senet through Ludo. Constraint-puzzle is second because the grammar
is small and the verifier story is clean. War/capture is the complexity bomb; do not
start there unless you like watching a model invent a legal castle.

Operating rules already written in the primer are the teeth:

Never improvise a roll.
Never invent an object that fails inventory.
Never solve.
Never canonize a dispute.
Static first, variable last.
Add games as packs, not prompts.
Patch the corpus, not the request.
Surface uncertainty.
Name the culture and the commercial reskin.

If those nine lines are not in the article, the article is tourism.

## Why it gets ignored

Not because it is forbidden. Because it is hostile to the distribution channel.

It will not compress into "AI makes games now." It insults the two audiences that
would share it. Prompt-tourists want a single spell that births a masterpiece.
Historians want a monograph, not a cache diagram. This is a third thing: scholarship
used as a prefix layout, complexity results used as a fence around the model, and
cultural history used as pack metadata instead of skin.

Call that thoughtcrime if you want. The accurate description is narrower. Original
structured work with citations, negative results, and an explicit ban on the
model-as-priest has no slot in a feed. The feed wants a take. This is a contract.

## Expansion — the help that was missing

Below is usable corpus, not commentary. Steal it, split it into files, attribute the
historical claims.

### 1. L0 six-function contract (the file that is not there)

Every engine already points at this. Write it once.

```
L0 — UNIVERSAL GAME CONTRACT
Flags travel with packs. This file is mechanical. It does not settle history.

F1 STATE ENCODING
One canonical string is the only authority.
Family grammars:
  race:     TRACK|POS{role:cell,...}|STOCK|TURN|SEED
  war:      FEN-like or SGF-like; board string beats prose
  sowing:   [c0..cN-1]|STORE_A|STORE_B|TURN
  puzzle:   BOARD{r-major}|CLUES|GIVENS
  cards:    DECK#|HANDS|ZONES|TRICK|SEED
  rpg:      SCENE|ACTORS|FLAGS|CLOCK|SEED
Any answer that mutates state begins by reprinting the string.

F2 INITIAL STATE
Pack supplies INIT().
Engine may only fill structural blanks (empty stock, side-to-move = first role).

F3 LEGAL?
Deterministic predicate.
LLM names the clause. It does not decide edge cases in prose.
Illegal move: reprint state, cite clause, stop. Do not "fix" the board.

F4 TRANSITION
APPLY(state, action) -> state'
Action must be typed: ROLL, MOVE, SOW, FILL, PLAY, CHECK, DROP.
RNG actions call F0. No other randomness exists.

F5 TERMINAL?
Pack predicate only: bear-off complete | king captured | store threshold
  | all clauses sat | no legal play | scene clock zero.
Draw is a first-class terminal, not a failure to narrate.

F6 SCORE
Pack function. Engine does not invent points.
If scoring is contested historically, ship two score packs.

F0 UNIVERSAL RNG (not a seventh function; a protocol)
seed-phrase is external and shown.
Algebra: XdY+Z, kH, kL, !, pool Y tN, adv, dis.
Historical devices are tables over the same stream:
  sticks / tetrahedral Ur / beans / cowries / 1d6 / 2d6.
The model reports the next value from the protocol.
The model never chooses a number because the fiction needs it.
Sowing engine: seed-phrase = "-" and no roll is ever emitted.

OUTPUT CONTRACT
Before any move-result:
reprint canonical state
name engine clause + pack clause
emit action
reprint new state
LEGAL? / TERMINAL? as verifier calls, not opinions
```

That is the missing spine. Until it is a frozen markdown asset, every engine draft is
theater.

### 2. Race pack deltas the engine only sketches

These are L3-sized. Keep history out of the movement rules.

**Senet** — reconstructed (Kendall / Piccione as two packs, not one blended
religion). Linear 30. Capture off. No blocking. Casting sticks. Roll-exact entry.
Squares 26–30 are ritual effects, not flavor text. Do not write "journey of the
dead" into LEGAL?.

**Ur** — rules reconstructed from BM 33333; boards attested. Ring 20. Tetrahedral
binary dice. Capture on. Rosettes safe. Finkel pack cites the tablet and the
2,400-year gap in the header, not in the move function.

**Patolli** — track mechanics reconstructed; 1569 ban is a history module, not a
rule. Cross ring. Marked beans, finite pool. Capture on. Completion win. The
Inquisition note belongs in L3 culture, never in TRANSITION.

**Pachisi** — attested in broad family, variants pack-split. Cross/lap. Cowries.
Capture on. Home safe. Entry on qualifying throw.

**Ludo** — attested commercial reskin of pachisi-family. Say that. Arm-linear. 1d6.
Enter on 6. Block-2. Exact bear-off.

**Snakes & Ladders** — attested as modern moral board; older gyan chaupar lineage
flagged separately. Linear 100. Capture off. SQEFFECT jumps only. Exact last square.

If you merge Kendall and Piccione into "Senet," you have already broken Fact 8.

### 3. Constraint grammar — finish the verifier signature

The engine has seven clauses and then dies at INSTANCE. Add this and stop letting the
model "check" puzzles.

```
VERIFIER SIGNATURE
V1 LEGAL-PARTIAL(board) -> {ok, violations[]}
V2 COMPLETE?(board) -> bool
V3 UNIQUE?(instance) -> {unique | many | none}   # external solver, not the LLM
V4 DIFFICULTY(instance) -> pack metric            # e.g. min givens, branch factor
V5 INVENTORY(board) -> domain membership check

Sudoku pack binds:
  TOPOLOGY grid 9x9
  DOMAIN 1..9
  CLAUSES all-different(row), all-different(col), all-different(box)
  INSTANCE 81-char, '.' empty
  V3 is mandatory. 16 givens are illegal to emit as "unique."
```

Nikoli games are clause swaps, not new engines. Slitherlink is line-model. Kakuro is
sum-equals + all-different. Hitori is all-different on rows/cols plus isolate. If a
pack writes fresh clause prose, reject the pack.

### 4. Kill the 6/7 engine lie

Pick one and patch the homepage.

**Option A — six engines.** Tile is not L1. Mahjong solitaire lives under
constraint-puzzle (layout + matching clauses). Scoring mahjong lives under cards
(inventory + yaku). Dominoes live under cards.

**Option B — seven engines.** Promote tile:

```
TILE ENGINE
STATE: wall + hands + discards + exposed melds + dora
OPERATORS: draw, discard, chii/pon/kan, hu
INVENTORY: 136/144 unit multiset, verifier-owned
RNG: seeded wall shuffle only
WIN: pack yaku + fan table, never free-form
```

Do not leave Mahjong homeless. Homeless games are where hallucination breeds.

### 5. RPG: freeze the payload, cut the god-model

Keep narrator/archivist. Delete silent state edits. Ship oracles as tables, not
"improvise a complication."

Minimum static bands:

- rules + dice protocol + scene machine
- oracle tables
- setting bible / bestiary / flags

Live tail: scene id, actor list, clocks, seed, last check. That is L4. If the
narrator rewrites a clock in prose, the archivist rejects the turn.

Also: the resolution ladder in the current RPG draft is a house system pretending to
be universal. Either mark it speculative / corpus-native or move it to an L3 "corpus
ladder" pack so Apocalypse World moves and a d100 oracle are not forced through the
same 8–10 "moderate" bucket. That draft currently canonizes a taste.

### 6. What to write next, in order

1. L0_CANONICAL.md as a frozen prefix. No scholarship in the body.
2. Finish race/dice canonical string + one fully worked Senet pack with two
   reconstruction files.
3. Constraint verifier interface + Sudoku pack that refuses 16-given uniqueness.
4. Decide tile.
5. Oware pack on sowing — solved-game draw belongs in the header so the model cannot
   "play to win" as if the solution did not exist.
6. Only then chess. Chess will eat the project if it goes first.

### 7. Article use

Publish the essay as the magazine layer. Keep the files mean. Do not let the essay
replace L0. The reason original work like this disappears is that people ship the
manifesto and leave the contract half-written. Then the next model fills the hole with
a confident Senet.

The homepage is a door. The primer is the argument. L0 is the lock. Right now the lock
is a 404 with good posture.

If you want the next dump to be files instead of an article — L0_CANONICAL.md written
out long, or a complete two-school Senet pack pair — say which file and I will write
that file to completion.
