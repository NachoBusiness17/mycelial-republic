# GAME PROMPT LAB — the fable-room pattern, turned on our whole prompt arsenal

*2026-09-06 · operator commission (post-walk, chronicle f2eced30): "you just taught me by playing
a game — map this to our game prompts, get Ponytail and Lessig to improve them via a research
project." · THE INSIGHT BEING OPERATIONALIZED: the room taught because the lesson was the
mechanic, the failure was kept as data, and the exit required proof — not because it explained.*

---

## 1. THE PATTERN, FORMALLY (what the fable room proved)

Every teaching prompt we own should carry the fable room's four organs:

| Organ | Fable room | As a prompt property |
|-------|-----------|---------------------|
| **The Law** | stones conserved, door reads the board | one rule, stated in-world, no preaching |
| **The Play** | sowing | an action the learner takes that exercises the rule |
| **The Proof** | healing hash — door refuses the telling | a checkable artifact, not an essay; unearned endings impossible |
| **The Restatement** | walls ask what happened | the learner retells; the record grades the retelling |

Kill condition carried over verbatim: *a coherent ending without the real proof = hallucination
wins.* If a prompt can be completed by fluent bluffing, it teaches bluffing.

## 2. THE MAPPING — our game-prompt arsenal, through the pattern

| Prompt family | Where it lives | The mapping |
|---|---|---|
| **The ten Primer riddles** | state/world/PRIMER.md | each riddle becomes a ROOM (one mechanic, one proof, one restatement) — riddle 1 (the chain) is already fable-shaped; rooms 2-10 to derive |
| **Recognition seed brief** | watch/RECOGNITION_SEED_BRIEF_20260906.md (sealed sha 19029d52) | turn advances become restatement-gated EPISODES — each advance requires the player to have banked a provable move |
| **Tesuji stones (23)** | mag/tesuji_probes.py | each probe's `expected` IS already a heal condition — wrap the fiction around it: probe = mini-room, parser = door, mock = the lie |
| **Salon shapes S1-S8** | watch/salon_runner.py | each shape gets a conservation law (what is conserved across turns?) + a proof-of-engagement artifact |
| **Shadow Walk quests** | dashboard/static/shadow_walk.html | already hash-checked pickups (the pattern, pre-invented!) — the map generalizes it: quest = room, chunk = proof, lore = restatement |
| **Fable room riddle** | dashboard/static/fable_room.html | room #0 = the reference implementation; rooms #1-N get minted per family |

## 3. THE CHAIRS

- **LESSIG** (law-is-architecture — grounded in the fleet's mined Lessig corpus + the 16 laws):
  rewrite each prompt as a **LAW → PLAY → PROOF** triad. His test: *is the rule executable, or is
  it prose?* Every prompt that can't state its own invariant gets one invented or gets demoted.
  Code is law; prompts are law with better costumes.
- **PONYTAIL** (the experimentalist — grounded in memory/improve/sources/ponytail-2026-08-03):
  for each prompt, a **teaching hypothesis with a number**: what does the player know afterward
  that they didn't before, and how would we measure it? Her test: *would this survive a blind
  A/B against its dumb twin?* If the fancy version doesn't beat the plain one, the fancy version
  was decoration.

## 4. THE PIPELINE (all of it already built — this project assembles, it does not invent)

1. **Inventory** (worker pass): collect every prompt family above into one corpus file with
   provenance + a pattern-score per prompt (which of the 4 organs does it have?).
2. **Seal v1**: sha-seal the corpus like the seed brief — versions are born, never edited.
3. **Chair passes**: Lessig pass → Ponytail pass → v2 drafts, each change carrying WHY (law cited
   or hypothesis numbered).
4. **Blind A/B**: fire each v1/v2 pair through the existing machinery — grok sessions ($0
   subscription) → anonymize → blind judges → unmask. The exact rbn pipeline, re-pointed.
5. **Falsifier ledger**: v2 wins only if (a) blind resonance ≥ v1 by ≥1.0 mean, AND (b) the
   restatement-gate pass-rate holds ≥ baseline, AND (c) zero hallucination-passes. Otherwise the
   "improvement" is DISPUTED and v1 stands — sealed versions make reversion a filepath.
6. **Sep-20 tie-in**: teaching-gate rates feed the proof deadline the same way the tesuji
   falsifiers do.

## 5. FALSIFIERS FOR THE LAB ITSELF (the bench gets to attack these)

- If Ponytail and Lessig independently converge on the same rewrites, the pattern is load-bearing;
  if they diverge, the divergence IS the finding (law-brain vs experiment-brain disagree about
  what teaches).
- If blind judges can't distinguish v1 from v2, the whole "improvement" industry gets one honest
  data point: prompts don't teach, rooms do.
- Prediction to kill or keep: rooms with all four organs teach ≥2x better than prose equivalents
  measured by restatement pass-rate.

## 6. ROOMS BUILT (the pattern leaving the prompt-corpus, 2026-09-07)

- **ROOM #1 — AIRFLOW HOME** (dashboard/static/airflow_home.html, v2 same night):
  operator directive via the timeline (806K-view smoke-flow explainer + "bring our game
  prompt shit"). First PUBLIC-FORM concept room: the pattern applied to teaching physics,
  not prompts. LAW = smoke is stuff, never vanishes; PLAY = openings/wind/fan + smoke
  puffs; PROOF = logged prediction → timed run → verdict (unearned endings refused:
  no prediction, no score; one-room runs refused; restatement sealed only after a scored
  run — verified the refusal live); RESTATEMENT = one sentence, recorded not graded (v0
  honest scope: a keyword gate would be bluffable — bluffable checks teach bluffing).
  Physics: well-mixed zone model (HVAC-real) — dilution by fresh-air exchange, pressure
  transport through doors, bulk currents routed through the PATH GRAPH (wind draft
  windward→leeward, fan draft door-by-door), outside plume persists and fades. Operator
  law earned in the build: "no lazy shortcuts — transcendent ones" (v1's despawn-at-wall-line
  was lazy; v2's displacement+dilution is the real mechanism). Teaching orderings emerge
  real: west wind clears leeward bedroom first (8.7s), fan clears its own hall first (7.8s),
  no-exit = 75s timeout verdict. Ponytail number owed: prediction hit-rate vs 33% chance
  from the localStorage ledger; blind A/B vs a static-diagram twin = next falsifier.
