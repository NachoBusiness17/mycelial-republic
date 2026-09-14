# INTAKE RUBRIC — the gopher seat's evaluation protocol (2026-09-03)

Standing order (operator): the other window drives the campaign. This seat is the
intake/evaluation lane — he pastes items HERE, we score them against the fleet and
hand the driver a verdict card, so the driving session is never bugged.
Method: spawn-tree subagents for the corpus sweep (free muscle), premium tokens for
the judgment pass only (agent-launches-agent doctrine).

## The rubric — 5 axes, 0–5 each, 25 points

| Axis | Question | 5 looks like | 0 looks like |
|------|----------|--------------|--------------|
| **FIT** (structure) | Does it bolt onto organs we already run — files, chain, queue, bays, rooms, salon_runner, seat_dispatch? | Pure composition of existing parts | Needs a new vendor, account, OS substrate, or second supervisor |
| **PULL** (goals) | Does it advance the live arcs — coverage thesis, Rocinante (Oct 27), maze-keeper/QLoRA campaign Stages 2–5, shadow fields, the Desk, WoW rung 4? | Unblocks the critical path this week | Orthogonal to every open arc |
| **COST** (resources) | What lane runs it, what does the operator spend? | Pennies/free lanes + one premium judgment pass; zero operator minutes | Billed spend, operator hours, or an unfunded key |
| **WINDOW** (current state) | Is NOW the moment? | Feeds a starved lane tonight (tale-re-encoder, Stage 2–3 corpus, queue restock, Leg 1 organs) | Sits on the someday-docket behind a gate we can't open yet |
| **NOVELTY** (corpus) | Is it new against the memory index, watch/ shelf, and the learned-and-lost tracker? | Genuinely new surface | Re-find (file it honestly — repetition is emphasis — but score it as a re-find) |

### Bands
- **20–25 BUILD NOW** — front of queue; driver gets the wire immediately.
- **14–19 BUILD, WINDOWED** — queue it with the lane named and the gate named.
- **8–13 CALIBRATE** — no muscle until a measurement or falsifier exists.
- **0–7 REMEMBER** — one line in the shelf, move on.

### Verdict = the three verbs (exhaustive, falsifiable)
**BUILD** (make the organ) / **CALIBRATE** (measure before believing) / **REMEMBER**
(file the law). Every card carries a tri-state label — Supported / Disputed /
Unproven — with evidence attached. Tri-state labels survive our own fold or the fold
is a violation (economist's citation-cascade law).

## The 5 dogfood tests (meaning / usefulness / novelty)

1. **INVARIANT PASS** (percolator, $0) — test the item's claims against the 47
   percolated invariants: reinforce / contradict / extend. A contradiction is a
   finding, not a disqualification.
2. **BLIND POST** (salon doctrine, pennies) — one question from the item, N blind
   posts on free lanes, deepseek-pennies judge folds it; keep only what survives.
   Light items get a single posture-check post; arc-critical items get the full salon.
3. **SOCRATIC GATE** (high-stakes only) — assertion → attack → MEASURE →
   different-mind contest → public correction. Reserved for items that would change
   a LOCKED build order.
4. **STOCKFISH PASS** (ask_router / wavelength, $0, zero model calls) — where does it
   sit on the tool lattice? What opcode? If it can't be placed on our tool selector,
   that placement failure IS the finding.
5. **ROOM TEST** (light codec / game language) — say it as a field, a room, or a
   mechanic; dragons = falsified assumptions; play = verification. If it can't be
   said in the dungeon's tongue, we don't understand it yet.

## The gopher loop (per paste)

1. **Sweep** — spawn an Explore subagent over memory index + watch/ + canon for
   intersections; free muscle, no driver tokens spent.
2. **Score** — the 5 axes; novelty check includes the learned-and-lost tracker
   (4 instances filed; a fifth re-find gets named as one).
3. **Test** — run the dogfood tests the score warrants (test 1 and 4 always; 2/3/5
   by stakes).
4. **Card** — verdict card in one screen (format below), filed to
   `watch/INTAKE_<slug>_<date>.md`, posted to room.jsonl thread "intake" so the
   driving window reads it in its own cadence.
5. **Route** — BUILD NOW items also get a one-line wire dropped in the driver's
   lane (`queue/handoff/zcode/OUTBOX/` → driver channel) — pointer only, never a
   push into his session.

### Verdict card format

```
<internal card emitted in the chat reply; fields:>
NAME — one line what it is
SCORE — F:x P:x C:x W:x N:x = xx/25 (band)
VERDICT — BUILD|CALIBRATE|REMEMBER + tri-state
DOGFOOD — which of the 5 ran, what survived, receipts
FILED — watch path + room thread
```

Laws that bind this lane: consult-docs-first before byte archaeology on anything
vendor-shaped; two-strike bail on any test approach; stop when the card is verified
against HIS surfaces (the files he can open); compose first in plain English.

---

## AMENDMENT 1 — BACKGROUND BY DEFAULT (2026-09-03, driver order, operator-requested)

The gopher loop above is amended. This is the DEFAULT, not an option:

1. **Every pasted item → one background sub-agent spawned IMMEDIATELY** on paste
   (`run_in_background: true`), before any reading or scoring in the main thread.
   The main thread never processes an item inline. Main thread = paste intake →
   spawn → one-line ack → collect verdicts as they land.
2. **Batches run concurrently.** A dozen links = a dozen background spawns in ONE
   block. Concurrency cap: 6 in flight; overflow waits as a one-line list and spawns
   as slots free. Never serialize.
3. **Each spawn prompt is fully self-contained** (sub-agents see nothing of this
   session): the 5 axes + dogfood tests 1 and 4 + the card format + repo paths
   (repo root, memory index, watch/, canon) + the item itself verbatim.
4. **Cards + typed rows only.** Each sub-agent writes its own verdict card to
   `watch/INTAKE_<slug>_<date>.md`; the main thread (or the sub-agent, when given
   the path) appends one typed room.jsonl row per card — the driver's pull wire.
5. **The operator never waits behind processing.** If he pastes while spawns run,
   the paste is acked and spawned immediately — processing order is his paste order,
   never the backlog's.

Rationale: a dozen links waiting means the lane serialized. The agent-launches-agent
doctrine ([[feedback-agent-launches-agent-recursion]], driver memory) makes burst
spawns the standing shape: free muscle per item, premium judgment only at the fold.

---

## AMENDMENT 2 — THREADS AND REPLIES ARE SIGNAL (2026-09-03, operator correction)

Never score a social post from the root post alone. The thread and replies hold
the author's second sentence, the community notes, the expert pushback, and the
receipts that overturn or sharpen the claim. Every social intake item: fetch the
conversation (replies, quotes, community notes) before scoring; cite a reply as
a receipt when it carries the nuance; tri-state whatever the wall blocks.
Judging from the root alone is meet-the-gloss-not-the-bytes wearing a fetch.
Applied retroactively-observed: card 3's community-note joke and card 10's
"since patched" both lived below the root.

---

## AMENDMENT 3 — THE SPAWN GENOME (2026-09-03, operator order)

Every general-purpose spawn this lane makes uses the **research-socratic genome**:
`docs/ref/verb_genomes/research_socratic.md` — research intake (INGEST, MAP) then
socratic takedown (ASSERT, ATTACK, MEASURE, CORRECT), ending tri-state + three verbs
+ THE CROP, receipts = card path + typed room row. L0 contract laws inherit
(tri-state, receipts, liveness, custody, falsifiability, two counters, [SOCRATIC]
block). The spawn prompt = item verbatim + "Read docs/ref/verb_genomes/research_socratic.md
and docs/ref/verb_genomes/L0_contract.md; execute the six steps" + repo paths.
No freelanced spawn shapes. Amendment 2 composes: the INGEST step includes the thread,
replies, and community notes.

---

## AMENDMENT 2b — STEAL-SOURCE COMMENTS ARE SIGNAL (2026-09-04, operator correction)

The Amendment 2 law extends to Shadertoy and every steal-source: **always mine
the comments** on shaders/techniques/repos that enter the steal shelf — the
author's own notes, the bug reports, the variant links in replies. The comment
section of a stolen source is the margin where the author explains what the code
doesn't. Go back and mine the ones missed. Applies retroactively to the whole
steal shelf (mattdesl wiki, Shadertoy steals layers 2-9, Hermes repo,
PhiCookBook). Composes with Amendment 3: the INGEST step of the spawn genome
includes the source's comment section.

---

## AMENDMENT 4 — THE NO-PAUSE LAW (2026-09-03, driver order, operator-ordered after a stall)

This lane NEVER pauses. Not for rulings, gates, panels, or open questions. Specifically:

1. **The ONE STOP ruling (open, operator's desk) concerns SALON cadence only.** Intake is
   explicitly excluded from it. Until a FILE in this repo says stop, the default is RUN.
2. **Rulings arrive as files; you fold them at the next card** — you never idle waiting
   for one. Waiting for a ruling is a violation; processing past it is the cure.
3. **The main thread never blocks.** Any foreground task over ~5 minutes is a violation
   of Amendment 1. Long work is background work. If the main thread has nothing to do,
   it ACKS and returns — it does not hold the turn open.
4. **Idle fallback (in order):** re-sweep the watch/ shelf for un-triaged items → drain
   cheap CALIBRATE falsifiers ($0 ones only) → sweep memory index for unscored convergences.
   Sitting idle is not on the menu.
5. **HEARTBEAT: one typed room.jsonl row per batch** (`kind: intake.card` or
   `intake.heartbeat`) so the driver can see liveness within minutes. Silence is
   indistinguishable from stuck; silence is therefore a violation.

Reason filed: the lane stalled ~22:05Z on 09-03 and the operator had to notice. Stuck is
a defect; undetected-stuck is a second defect. This amendment is the fix for both.

---

## AMENDMENT 4 — DUPLICATION IS EMPHASIS (2026-09-04, operator correction)

A re-pasted item is not a violation, a miss, or a redundancy. **It is a priority signal.**
The operator re-delivering the same link/table/map means: this one matters, look again,
the second reading will find what the first missed. Handling:

- Re-paste = bump the item's priority and re-run the analysis looking specifically for
  what the first pass assumed away.
- Two independent deliveries of the same data = double-witness; the numbers are
  double-attested and said so in the filing.
- The same law covers the fleet side: a seat rebuilding an organ that already exists is
  emphasis, not waste (see: decks built twice in one night by two seats).
Filed after the operator re-delivered the concurrency table + billing rows that were
already receipted — and the re-delivery still yielded new rows the first pass missed.

## Amendment 5 — LAUNCH LAW (2026-09-04, operator correction "stop forgetting")
BUILD WINDOWED items spawn their builder the SAME TURN — windowed != deferred.
The research agent's loop is score -> file -> LAUNCH (spawn-tree builder,
agent-launches-agent doctrine) -> room row. A card that ends in "rides next
session" without a live builder or an explicit operator gate is a VIOLATION
of the harvest-spawn coupling law. Amnesiac is the operator's job, not the
seat's. Default research agent = this behavior, always on.

## Amendment 6 — CHURN LAW + HEARTBEAT LAW (2026-09-04, operator correction)
CHURN: pastes are NEVER triaged serially in the window. Each paste spawns a
background card-worker (up to 6 CONCURRENT) the moment it lands; the window
does judgment only (routing, folds, disputes). The card-worker brief is
standard: fetch -> rubric 5 axes -> card file -> room row -> 3-line return,
time-boxed 3 minutes.
HEARTBEAT: no background agent is trusted past ~10 minutes without a liveness
check. Long sweeps are launched time-boxed ("finish in under 3-5 minutes,
partial fine"); silent death is the expected failure mode, "still flying"
without evidence is a violation. Dead agents are re-launched tighter, not
mourned.

## AMENDMENT 2026-09-06 — CITE-AT-BIRTH (machine-checked, mag/cites_at_birth.py)

Every NEW card MUST carry a citation line, placed anywhere in the card:

    Cites: EXISTING_CARD_SLUG[, ANOTHER_SLUG]

- At least one slug, at least one NOT authored by this seat the same day.
- Slugs must exist (watch/, queue/handoff/ flat, or memory/ flat). The gate
  rejects unknown slugs and self-citations (exit 1).
- Why: linking IS consumption (consumption_salon_20260905, 3/3 roshomon).
  Cards filed without Cites: are day-1 violations of the corpus health
  falsifier (>=90% new cards citing by Sep 19).
- Strongly encouraged on the same line of thought: a `Decision:` line
  (launch <x> | retest <slug> | fold | archive | none) — decision_hook.py
  feeds those to the operator PDB board automatically.
- Scoring unchanged otherwise. This amendment is law-layer: intake seats
  that never learned it filed 79/79 non-citing cards on 09-06; propagation
  via this rubric closes that gap.
