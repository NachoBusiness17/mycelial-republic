# THE PROMPT LIBRARY: how we make models produce Kimi/Claude-level detail

**2026-09-24 · The operator asked: "how do those models get that level of
detail, it's gotta be prompt based right?" Answer: detail = model × context ×
forcing-function prompts. The model is rented; the prompts are ours. This
library is the reusable core, distilled from 16 prompt artifacts we already
own (see watch/inbox/SELF_STEAL_PROMPT_LIBRARY_20260924.md) plus the live
board method (docs/CLONED_MECHANICS.md §5).**

> **CORRECTION (filed by gala afterparty t3, per a03 testimony):** this
> library is **5 templates + this README**, not 6 prompts. Only
> [ONE_SHOT_GAME](ONE_SHOT_GAME.prompt.md) carries the full six-move anatomy.
> [DETAIL](DETAIL.prompt.md), [PORT_GAME](PORT_GAME.prompt.md),
> [CLONE_WHEEL](CLONE_WHEEL.prompt.md), and [NPC_HEAD](NPC_HEAD.prompt.md)
> are specialist shapes with their own laws. They must not be force-fit into
> the six-move anatomy; forcing it there is a category error, not
> thoroughness.

## THE FIVE LAWS (self-stolen, load-bearing)

1. **Frozen prefix, capped tail** (from mag/context_pack.py): identity and
   rules live in a byte-identical system block; everything session-specific
   goes in a bounded tail. Cache-friendly, drift-free.
2. **Fixed-section output contract; the engine owns facts** (from
   mag/game_passage.py): demand sections by name (`## Mechanics / ## Numbers /
   ## Files`), and forbid invention: "never invent HP, rooms, exits, or loot
   not listed." Structure first, no invented facts.
3. **Evidence-quote falsifier; empty is a valid answer** (from
   mag/lane_runner.py): "No evidence quote, no clue. If nothing: []."
   Sub-80-char bodies are not a lens. A model that must quote its source
   cannot bl confidently.
4. **Closed bibliography; unlisted = CLAIMED** (from SALON_PROMPT_MANUAL):
   whitelist your sources, mark everything else CLAIMED, run a mandatory kill
   round. "The model drafts; the anchors decide."
5. **Seeded determinism; named failure codes** (from the L0 game contract):
   seeds in every prompt that touches generation, explicit FAIL(RNG_DIVERGE)
   style failures. "The LLM calls verifiers; it never is one."

Plus the Valora lens craft (STEINIGER_OPERATIONAL_STEAL): dual-anchor identity
knot (who the model is + who it is NOT), entropy-gated recursion (reflect only
when something changed), matched inference params (temp 1.1, top_p 0.95 for
creative; effort low for scut).

## THE V2 AMENDMENTS (2026-09-26)

Four amendments, landed after the full-text prompt-uplift deep dive of the
optimizer class (PRIS, VisualPrompter, GEPA, VQQA, TARA). Provenance:
watch/inbox/burn_wave_20260926/B2_09_prompt_uplift_20260926.md (full-text
reads, quotes below are its verified record) and
watch/inbox/BURN_prompt-uplift-lane_20260925.md through _d.md (the draft
this section replaces; pass d left roblox/prompts/ untouched, this section
is the first landing). Spec change only. The laws above stand; these amend
how they survive an uplift pass.

**A. Law 1 splits in two: judge-side ANCHOR vs candidate-side LOCK.** The
frozen-prefix idea controls two surfaces and both must hold.

- ANCHOR (judge side): an uplift judge scores a candidate against the SEED
  prompt p0, never against the previous candidate. First-hand canon (VQQA,
  arXiv 2603.12310): the rater "assesses each candidate against the
  original prompt p0". Candidate-to-candidate comparison lets drift
  compound silently.
- LOCK (candidate side): the invariant blocks survive byte-for-byte into
  every candidate; any delta is FAIL(BIB_LAUNDER). Per template the
  invariant block is: DETAIL `## FACTS`; PORT_GAME `## SOURCE TRUTH`;
  CLONE_WHEEL `## THE WHEEL TO CLONE` plus its item 2 source lines;
  NPC_HEAD FROZEN PREFIX + THE KNOT; ONE_SHOT_GAME ships none, so any
  sourced-looking claim a rewrite introduces is FAIL(BIB_LAUNDER).
- Both halves or neither. The surveyed class anchors judges and unlocks
  candidates: PRIS revises p into p' but "nothing constrains exact
  wording"; VisualPrompter retains well-reflected descriptions yet rewrites
  freely. Anchor without lock is half a law.
- Check shape (pass d, unchanged): extract each invariant block by fixed
  marker, sha256 against the SEED hash (never the previous candidate), no
  whitespace or unicode normalization (launder vectors), empty diff is the
  only pass, no repair round (a "corrected" FACTS block is still laundered
  provenance). Home is a pre-flight script (draft name
  tools/bib_launder_check.py, exit 2 on fail), never a judge instruction:
  byte-equality is mechanical, and a judge asked to verify bytes will
  paraphrase-verify.

**B. Law 3 extends to the judge seat: judge-must-quote.** The uplift judge
returns element + quote + verdict, not a score alone. The named
anti-pattern is the score-only judge: VQQA's judge closes "Respond with
only a number between 0 and 100", and all three academic judges in the
class are score-only or label-only (number, binary VQA, NLI count). Law 3's
protection ("a model that must quote its source cannot bl confidently")
now applies to the judge seat itself.

**C. Law 5 extension: seed-paired uplift.** Hold generation seeds fixed
across candidate prompts: run the seed and every candidate on the same
seed set (PRIS regenerates with "the top-k noise seeds"), so the measured
delta measures the prompt, not the noise. An uplift claim without seed
pairing is CLAIMED, not evidence.

**D. Law 4 enforcement: BIB_LAUNDER auto-revert, per the TARA gate.**
Flag-only is insufficient; adoption is gated. Adopt a candidate iff its
seed-paired score beats the seed's AND the gain holds across folds;
otherwise auto-revert to the seed. (B2-200, 2026-09-26, upgraded from
single seed-paired delta per the B2-59 steal: the aggregate delta alone
adopts candidates whose gain is confined to a few seeds of the seed set.)
The fold check is acceptance-rule only and costs zero extra generation:
law C already keeps per-seed paired scores, so re-partition them (split
the seed set into k = min(5, n_seeds) fixed folds; re-pick the best
candidate on all folds but one; score that pick on the held-out fold;
sum across folds) and adopt only if the held-out sum beats the seed's.
Canon (TARA, Type-Aware Repair Allocation, arXiv 2607.18724): "adopts the
repair iff s(x̂)>s(x0) and otherwise reverts"; "This accept-or-revert
regression guard is not a best-of-N selector" (gate removal costs 3.6
points in ablation). Canon (ReAnchor calibrate, dspy @experimental,
B2_59_dspy_reanchor_calibrate.py:22-26,236-252): "A setting stays unless
a candidate scores strictly better and the gain holds across folds";
strictly-better pick plus held-out fold check, restore on refuse, with
k = min(FOLDS=5, n) as the small-set answer. Composition with the lock:
FAIL(BIB_LAUNDER) still
rejects regardless of score and admits no repair round; the TARA gate
governs candidates that pass the lock but regress on score. Scores never
rehabilitate a laundering.

Kill condition (carried from B2-09): a shipped optimizer that natively
locks a user-fact block, or hard-anchors candidates to p0, demotes
FAIL(BIB_LAUNDER) from law-patch to interop note. TARA is the closest live
threat. Still owed: the per-template contract lines and the checker script
from pass d (a)/(b)/(c); this section is the law level only.

## THE TEMPLATES (5 + this README)

| File | Use it for | Shape |
|---|---|---|
| [DETAIL.prompt.md](DETAIL.prompt.md) | the forcing prompt: Claude/Kimi-grade artifact structure | specialist, law-driven |
| [PORT_GAME.prompt.md](PORT_GAME.prompt.md) | translating a fleet game (Python/JS) into Roblox Luau | specialist, source-truth-driven |
| [CLONE_WHEEL.prompt.md](CLONE_WHEEL.prompt.md) | cloning a proven mechanic with exact numbers | specialist, source-truth-driven |
| [ONE_SHOT_GAME.prompt.md](ONE_SHOT_GAME.prompt.md) | single-file playable games, the viral one-shot shape | full six-move anatomy |
| [NPC_HEAD.prompt.md](NPC_HEAD.prompt.md) | the Head Museum personas (one ractor, many faces) | specialist, knot-driven |

## ANATOMY COVERAGE: which of the six moves each template carries

The six moves are ONE_SHOT_GAME's verified anatomy
(watch/inbox/STEAL_ONESHOT_PROMPTS_20260924.md). The table is honest about
non-coverage: "no" is a first-class answer, and the adjacent device each
specialist runs instead is named below. The negatives are the design, not a
gap.

| Move | ONE_SHOT_GAME | DETAIL | PORT_GAME | CLONE_WHEEL | NPC_HEAD |
|---|---|---|---|---|---|
| 1. one self-contained file | YES | no | partial* | no | no |
| 2. bullet feature checklist | YES | no | no | no | no |
| 3. juice as explicit quality bar | YES | no | no | no | no |
| 4. stated interaction loop | YES | no | no | no | no |
| 5. named aesthetic references | YES | no | no | no | no |
| 6. multi-turn repair vs reference | YES | no | no | no | no |

\* PORT_GAME demands complete per-file code with no ellipses, but a port is
multi-file by design; M1's single self-contained file does not apply to it.

Adjacent devices the specialists run instead of the six moves:

- DETAIL: fixed-section doc contract (Board / Mechanics / Files / Falsifiers
  / Kill Round), a number on every claim, closed bibliography. Kill Round is
  a falsifier move, not M6 repair.
- PORT_GAME: source truth quoted from the files read; Mechanic Table with
  exact source numbers; Known Gaps is honest gap disclosure, not the M6
  repair loop.
- CLONE_WHEEL: wiki-quoted exact numbers, estate-canon skin table, "Numbers
  We Changed" defaults to NO deviation, one wheel per pass.
- NPC_HEAD: dual-anchor identity knot, brevity law, matched inference,
  FALSEIFIER (retire the transcript when the knot collapses into an
  assistant).

**Anti-force-fit rule:** the six moves belong to the one-shot shape. Using
ONE_SHOT_GAME for a doc pass, or demanding a juice bar from NPC_HEAD, is the
exact error this library exists to prevent. Pick by job shape.

## HOW TO USE (the ritual)

1. Pick the template closest to the job; do not freehand. Pick by shape: the
   full anatomy runs only in ONE_SHOT_GAME; the specialists run the five
   laws in their own dialects.
2. Fill the FACTS block with verified numbers (sources named; unverified
   marked CLAIMED). If you have no numbers, run the live-board pass first
   (CLONED_MECHANICS §5): the prompt cannot invent what you never fetched.
3. Keep the frozen prefix byte-identical across a working session; append
   only to the tail.
4. Demand the kill round before accepting: "list what you are unsure of."
5. File the output's falsifiers; a prompt without a falsifier is a wish.

## CHANGELOG

- 2026-09-24: library distilled from 16 prompt artifacts plus the live board
  method (CLONED_MECHANICS §5).
- corrected by gala afterparty t3 2026-09-26 per a03 testimony
- 2026-09-26: V2 AMENDMENTS section added (judge-side anchor vs
  candidate-side lock, judge-must-quote, seed-paired uplift, BIB_LAUNDER
  auto-revert per the TARA gate); from B2-09 full-text reads, first landing
  of the pass-d draft. Receipt:
  watch/inbox/burn_wave_20260926/B2_58_prompt_amendments_20260926.md
