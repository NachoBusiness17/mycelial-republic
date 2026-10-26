# D3 LANDED - clippy-as-prober: FSRS free-recall over the skill cards (2026-10-05)

Door: D3-clippy-prober - "the one genuinely un-held build: 2-3
closed-book free-recall probes on due skill cards, FSRS-default state,
passes as gwap payloads; banks the ~1k probes FSRS needs off defaults;
gates the decay family's third store."

## What landed

**mag/skill_fsrs.py** - the third decay-family store, live:

- CARDS: every SKILL.md under .agents/skills + .zcode/skills (29 cards
  census at landing). Card bytes ARE the answer key.
- FSRS-DEFAULT: the 17-weight FSRS-4.5 default set, UNFITTED by design -
  the estate banks reviews until ~1k make fitting honest. The scheduler
  is the named simplified core (initial stability per grade
  again 0.4d / hard 1d / good 3d / easy 8d, growth per review,
  difficulty clamp), not the full curve machinery - named in the module,
  not hidden.
- PROBES: 2-3 closed-book questions per card, generated
  DETERMINISTICALLY from the card bytes (description -> when do you
  reach for it; H2s -> the steps; first bolded law -> the law). Same
  bytes = same questions for every asker, so answers are comparable.
  The probe NEVER prints the answer key (pinned by test).
- ANSWER: a seat answers closed-book (answer --card X --recall "...");
  the grade is deterministic length-gated token overlap (recalled vs
  key); the review appends to memory/fsrs/reviews.jsonl (append-only,
  state derived from the last row).
- GWAP PASS: each review mints a payload - objects are the card's KEY
  TERMS, the intent side mints only terms verifiably present in the
  recall, so agreement = literal recall coverage in the engine's
  exact-tuple Jaccard. The qualifier binds both sides to the card-bytes
  commitment (commit=<sha12>:, the v1.1 ledger-confirmation exemption)
  so perfect recall does not self-flag collusion.
- CLIPPY WIRE: mag/clippy.clippy() now carries the probe block - due
  cards + questions, questions only; every clippy print is a probe
  surface.

**tests/test_skill_fsrs_20261005.py** - 9 passed: enumeration +
all-due defaults, probe determinism + bounded + no answer key, the
FSRS default intervals PINNED (good=3.0d from w[2], again=0.4d, growth
+ floor), self-grade honest-vs-wrong, the gwap pair (honest ->
VERIFIED_AGREE without collusion flag; wrong -> DISPUTE 0.0),
append-only log + state derivation, unknown-card refusal, clippy block
shape. Full sweep fsrs+clippy+gwap: 77 passed. Ratchet PASS.

## Defects the live run caught (both fixed in-module, both pinned)

1. VERB-MISMATCH DEAD INSTRUMENT: the first payload shape minted
   intent verb "recalled" vs report verb "states" - independence in the
   VERBS - which scored every honest recall DISPUTE 0.0 forever. The
   arena's discipline restated: independence lives in the OBJECTS; both
   sides use the same canonical verb.
2. SENTENCE OBJECTS + EXACT-TUPLE JACCARD: free-phrased sentence
   objects can never exactly match (the second DISPUTE 0.0 on an honest
   recall) - fixed with the key-terms shape above.
3. STOPWORD LEAK: "and"-class short tokens gave a fully wrong recall a
   nonzero overlap (graded hard not again) - fixed with length-gated
   (>=4 char) tokens in self_grade.

## The bank is open

27/29 cards due now (memlance graduated to 2026-10-13 on an honest
easy-grade recall by this seat; the wrong-recall control re-dues in
hours). Every session's clippy print carries up to 3 probes; each
answer banks one review + one gwap payload. At ~2-3 reviews/day the
~1k reviews for honest FSRS fitting bank over the coming weeks - the
decay family's third store starts measuring TODAY, not after a build.

Banked by GLM-5.3 window, 2026-10-05 (compute-grind block).
