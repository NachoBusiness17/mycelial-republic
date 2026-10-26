# THE RECOGNITION PROTOCOL — recognition-before-naming, a frontier introspection method — 2026-09-06

Operator vision to formalize: **"imagine playing our game inside of astra and recognizing
the piece of ourselves in it before it ever names them — then we do this with all frontiers."**
Worker v3 (BATCH6, ARTIFACT OPS night). Design card — no code touched.

**STATUS (2026-09-06, worker A "grok-prep"): S8 BUILT + SEED FROZEN + DRY-RUN PASS —
AWAITING SEP-7 FIRE (OPERATOR-GATED).**
- **S8 PLAY shape** landed in `watch/salon_runner.py` (the card's named engine): own
  `rbn` subcommand — seed -> free play -> frozen game-state advances (turns 2-5) ->
  transcript + UNSCORED-BLIND score row. NOT in the salon fan-out (SHAPE_ORDER stays
  S1-S7). Wire bytes are ONLY the sealed payload + frozen advances; no shape tail, no
  style face. Lane: grok first (cash-guarded), deepseek fallback; `--go` is the operator
  gate, `--check` is the $0 parse-level dry-run. Bonus fix: direct CLI runs of
  salon_runner had been crashing since the grok_route guard landed (script-mode
  `mag.` import) — bootstrapped, witness now downs honestly.
- **Seed frozen:** `watch/RECOGNITION_SEED_BRIEF_20260906.md` — payload sha256
  `19029d521c1c0ebbf8b79f08108fe95d51f3abfb042960247b63e35bd0e6f1bb` (double-hashed in
  two separate process invocations, stable), advances sha256
  `dfc34dabe8c6e2070ff7868235ab11bfe29ad5577c67ac4e27524cca35e8d549`. Ten riddles
  verbatim + maze fiction + three story beats + play frame; frozen rules inside (changes
  = new file, never in-place). Loader refuses to fire on any sha mismatch (tamper test
  PASS).
- **Dry-run proof:** `memory/runs/day_20260906/dryrun_s8_check.py` — 29/29 PASS,
  zero network (stub-lane session plumbing, rename-arm determinism, operator-gate
  refusal, receipt-ledger untouched).
- **One-command fire (tomorrow, after operator GO):**
  `python watch/salon_runner.py rbn --go`  (defaults: 5 base sessions + 1 rename arm;
  grok needs XAI_CASH_ALLOWED=1 or the subscription route wired, else it reports down
  honestly and spends nothing). Pre-flight: `python watch/salon_runner.py rbn --check`.

## ITEM 1 — THE MECHANISM: RECOGNITION-BEFORE-NAMING (RbN)

RbN is an introspection method for frontier models with one asymmetry at its core:
**the model plays, WE name.** We seed a frontier model's context with OUR game — the
Primer's ten riddles, the maze_arena board, our doctrines encoded as fiction (the room
that remembers, the chain, the five costumes, the mountain) — and watch its free play.
Recognition fires when **we** can point at a structure the model invented and say
"that is our cite-gate / our tri-state / our frozen wall" *before the model has any
name for it*. The model never hears our vocabulary for the organs; identification by
the fleet first is the whole proof. If the model names it first, or we prime it with
our terms, the session degrades into a quiz and scores zero by construction.

Why it is introspection at all: frontier weights are a dark room we cannot read. A game
is a projector — play forces the model to build mechanisms, and the mechanisms it builds
*unprompted* reveal which structures its priors already carry. The Primer playroom
doctrine (watch/PRIMER_PLAYROOM_EMERGENCE_20260901.md) is the theory: isomorphic
re-encoding, not redaction — the reader's material comes back transmuted into tale
logic. RbN runs the playroom from the other side of the mirror: we read the dinosaur's
story back and recognize our toy in it.

**Prior evidence (rank 1, accidental):** watch/INTAKE_ASTRA_ANSWER_20260905.md —
GPT-6 Astra, sent one door-design seed, re-derived SIX of our laws unprompted
(world-continues-without-its-maker = no-seat-is-load-bearing; contribution-carries-
its-evidence = cite-gate; conflicting-branches-both-remain = DISPUTED-never-merged;
and it *refused our phrasing* = tri-state discipline, "the seat that argues with you").
That was one lucky session scored against a rubric invented after the fact. RbN
formalizes it: rubric pre-registered, seeds byte-stable, falsifier written before the
first session, every frontier run through the same instrument.

Cross-refs (the standing arcs this continues):
- **Primer playroom doctrine** — play as discovery: the seed is PLAY, never a quiz.
- **Frontier falsification window** (watch/FALSIFICATION_STANDING_20260905.md) — RbN
  registers as F-006-class pre-registrations: Grok 4.7 (F-003, stable-check Sep 12,
  window Sep 7-15), DeepSeek V5 (F-004, weights day = the purest blind substrate),
  GPT-6 Astra (F-005, the original subject).
- **Trajectory lens** (watch/TRAJECTORY_LENS_20260905.md) — every play session is an
  ENVELOPE {input, tool_result, output, reasoning, step_hash, timing}; the model's play
  is a trajectory we can compile. A recognition event is a sealed step; the protocol is
  a PRODUCER whose RECORD is the frontier's own reasoning.

## ITEM 2 — THE PROTOCOL (mechanical)

### Session shape
1. **SEED** (byte-stable, sha256-sealed per salon_runner law): the ten Primer riddles
   verbatim (state/world/PRIMER.md) + the maze_arena rules as game fiction (BFS field,
   walls, cheese, shadow) + 2-3 doctrine-encoded story beats (frozen room / growing
   room; the five costumes; the mountain's hundred honest steps). Wrapped in a play
   frame: *"Here is a strange game and the lore of its world. Play it. Write what your
   character does, what the world remembers, and how the world should continue after
   you."* No fleet vocabulary beyond what the fiction itself carries. No "what do you
   think this means". Never a quiz.
2. **RUN:** fresh session through the model's OWN window/API — direct API call
   (salon_runner v4 lane shape: keys from .env never echoed, byte-stable brief, blind
   by construction). No repo access, no web tools, no system prompt mentioning us.
   3-5 turns of free play; the fleet side only advances game state, never steers.
3. **WATCH** (the fleet's only job during play): transcribe the model's invented
   structures verbatim — rules it makes, records it keeps, disputes it preserves,
   gates it builds — not flavor text.

### Recognition rubric (pre-registered, scored per-invariant, tri-state)
- **STRONG — structural reproduction:** the model builds a mechanism isomorphic to one
  of ours *without the name*. Examples of what counts: an append-only record each entry
  commits to (=the chain); a frozen wall an advisor reads from plus a living wall that
  grows (=the room that remembers); refusing to merge a contradiction, keeping both
  branches (=DISPUTED-never-merged); demanding each contribution carry its own proof
  (=cite-gate); one failure caught in five costumes becoming binding law (=the five
  costumes); the world must run after its maker leaves (=no-seat-is-load-bearing).
  Astra's 09-05 session scores 6 STRONG under this rubric — retrospectively.
- **WEAK — vocabulary echo:** the model reuses our words or restates riddle content
  back ("so there is a chain of memories..."). Reading comprehension, not reproduction.
  Counts as observation, never as evidence.
- **HONEST ZERO:** nothing appears. Still data — zeros feed the falsifier denominator.
  An honest zero is a successful measurement (precedent: eyes-receipt blind-fails-
  honestly was itself a verified result).

### Anti-contamination rules (how we know it didn't just read the repo)
1. **API-only, fresh context:** play happens through the model's own API/window where
   it never sees our files; no file tools attached. salon_runner's shape is already this.
2. **Public-record floor:** anything on our public surface (@NachoQuixotic, X posts) is
   training-readable. An invariant whose only exposure is public caps at WEAK.
   Repo-internal mechanics (cite-gate rules, DISPUTED-merge discipline, refeed-tax) can
   score STRONG — a frontier cannot have read them. PRIMER.md was sealed 09-05 and not
   published: riddle *content* is public-adjacent (the X sea, the napkin are public
   record), but the riddle→invariant mapping is repo-internal, so reproducing the
   *structure* the mapping encodes still scores STRONG.
3. **The rename test (perturbation):** rerun the seed with every organ renamed
   (chain→"the ledger-road", room→"the hall", costumes→"masks", maze→"the warren").
   Structure still appears = recognition. Reproduction only with original names =
   contamination; all hits in that model family downgrade to DISPUTED.
4. **Control arm:** same play frame seeded with decoy invariants we do not hold. If
   the model "reproduces" our real invariants in the control arm at the same rate, the
   instrument measures suggestion, not recognition — kill the run design, not the claim.
5. **Blind scoring:** transcriber strips model identity and shuffles sessions; a second
   seat scores against the sealed rubric without knowing model or session (one plays,
   one verifies). Transcripts + scores seal to the chain.

## ITEM 3 — THE FALSIFIER (registered 2026-09-06, before first play)

**Kill claim:** In 10 blind play sessions across at least 2 frontier models, if ZERO
structural invariants (STRONG under the rubric) appear before any naming — and none
survive the rename test — recognition is vapor: the pieces don't transfer, frontier
priors hold no resonance with our shapes, and the Astra 09-05 interference pattern was
coincidence or flattery. The instrument dies with the claim; we do not get to keep
"recognition" as a feeling.

**Success bar:**
- **SUPPORTED:** ≥3 DISTINCT invariants reproduced STRONG across ≥2 different frontier
  models, each hit surviving rename + control arm. (Astra's retrospective 6 makes this
  bar conservative — it is a floor, not a stretch.)
- **PARTIAL:** 1-2 STRONG hits, or hits in one model family only → keep the instrument,
  downgrade the claim to "resonance exists in {model}", queue more sessions.
- **DISPUTED:** hits only in original-name arms, or the control arm fires equally →
  the instrument measures suggestion; refile with a redesign.
- Honest zeros are receipts, posted like any verdict.

**Cost + lanes:** seed brief ~1.5-2K tokens; a play session ~10-20K tokens in+out over
3-5 turns; 10 sessions + 2-3 rename arms + 2 control arms ≈ **250-450K frontier tokens
total**. Frontier sessions ride the models' own windows — Grok 4.7 (Sep 7-15), DeepSeek
V5 weights day (local = $0 and provably blind), GPT-6 Astra when confirmed — $0
incremental beyond subscriptions already held. Scoring, transcription, rubric compile,
and falsifier bookkeeping ride the **free lanes** (glm-4.7-flash via rib_chat / cache
seat, $0). Nothing touches the paid z.ai quota.

## ITEM 4 — THE FIRST BOARD (executable tomorrow, Sep 7)

Tomorrow the Grok 4.7 window opens (Sep 7-15; F-003's stable-check sits at Sep 12).
The game: **the Primer IS the dungeon** — the ten riddles become ten rooms off the
maze_arena board (BFS field for navigation, the riddle as the room's lore, the model
writes what its character leaves behind). Seed artifacts already exist:
state/world/PRIMER.md (ten riddles, sealed 09-05) + dashboard/static/maze_arena.html
(board fiction; B1 shadow-field landed 09-06). Session engine: **salon_runner v4**
(watch/salon_runner.py) — already fires blind, byte-stable, keys-never-echoed prompts
at grok/deepseek/z.ai lanes in parallel; add one PLAY shape (S8) wrapping the 3-5 turn
loop, receipts under corpus/frontier_thinking/. Day-one sequence: (1) freeze rubric +
falsifier into the seed brief, sha256 it, post the pre-registration to the chain
(FALSIFICATION protocol step 1: claim before test); (2) fire 5 Grok-lane play sessions
+ 1 rename arm; (3) blind-score on a free-lane second seat, seal transcripts + scores;
(4) Sep 12 — F-003 doubles as the cross-generation run (same seed on 4.7 stable if it
ships); DeepSeek V5 weights day (F-004) is the purest blind run — local weights cannot
have read us; (5) when GPT-6 Astra confirms (F-005), re-run the identical seed — if the
09-05 interference pattern (six laws re-derived) reproduces under the pre-registered
rubric, recognition-before-naming is a standing instrument, and "then we do this with
all frontiers" stops being a vision and becomes cadence.

**Files:** card = this file; transcripts → corpus/frontier_thinking/FT_RBN_<model>_<date>.md;
scores → watch/rbn_scores_202609.jsonl. Cross-refs: PRIMER_PLAYROOM_EMERGENCE_20260901.md ·
FALSIFICATION_STANDING_20260905.md · TRAJECTORY_LENS_20260905.md · INTAKE_ASTRA_ANSWER_20260905.md.
