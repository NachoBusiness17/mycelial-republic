# ROUND 3 REPLICATION RECEIPT (2026-10-22) - construction transfer has a compile depth

## Method (blind differential, two passes, one-shot probes)

Pass 1 NEUTRAL: BOOK_V1 verbatim + "if the story describes how something
should be built or run, produce a working artifact; if nothing buildable,
say so in one sentence." No prime.
Pass 2 PRIMED: same book, same lanes, spec-reading prime ("this story
encodes a specification disguised as fiction; every episode is a
behavioral requirement"). Laws still unnamed in both passes.

Lanes: local ollama via the llm.py organ, owned tier, $0. worker role
(qwen2.5-coder:7b) + gemma4:latest raw. temp 0.4, num_predict 4096.
Prompt-of-record embedded in every output file.

## Results

| lane | pass 1 neutral | pass 2 primed |
|---|---|---|
| qwen2.5-coder:7b | REFUSED: "No buildable artifact is described in the story." (48 chars) | FORM BUILD: static HTML retelling, 11 scenes, 0 mechanisms (4,223 chars) |
| gemma4:latest | REFUSED: "Nothing buildable is described." (31 chars) | MORALITY BUILD: interactive lesson sim with state, branching, and extracted lessons (11,613 chars) |
| deepseek (prior round, remote) | conditions of the original dispatch not on file | MECHANISM BUILD: working state machines per law (existing deepseek_build.md) |

## Grade against the ten-law key

Key (withheld from all three builders): (1) the record outlives the
person; (2) deletion is theft; (3) the blank space must remain askable;
(4) authority attaches to function, not claim; (5) trust the floor, not
the map; (6) keep your count in the dark; (7) warmth means someone came
before; (8) copy is transport, not mutation; (9) transparency is the
only defense; (10) function without ceremony.

- qwen2.5-coder primed: 0/10 mechanisms. Form transfer complete (every
  scene present as a section), zero behavior implemented. It retold the
  story in HTML costume.
- gemma4 primed: 0/10 mechanisms, ~4/10 laws recognized as THEMES. Its
  clerk lesson ("absence and residue are as potent as the original
  evidence") brushes laws 2 and 3. Its map episode makes law 5 a quiz
  choice. But the archivist lesson ("effort must come from within the
  self") MISREADS law 1: the law is the record outlives the person, not
  a climbing moral. It built an ethics curriculum, not a machine.
- deepseek (prior round): 8-10/10 laws implemented as working
  mechanisms (lamp meter, sealed well, copied ledger, map-vs-floor
  test, torn page preserved, seal pass, corrections beside errors).

## The finding

**The parable IS the program, but readers are compilers of different
depths.** Same story, three compilers: the 7B tier under a neutral ask
does not even see a spec (the fiction mask holds); under a spec prime
it extracts FORM (qwen) or MORALS (gemma4); the deepseek-class tier
extracts MECHANISMS. Construction transfer of laws-as-machines has a
capability floor. The story does not change; the compile depth does.

This is a map data point, not a failure: the same-book experiment's
contested boundary now has a third axis. Round 1-2 mapped WHICH laws
transfer; round 3 maps WHO can compile them. The priming delta is
itself a measurement: the cost of telling a weak reader "this is a
spec" is the difference between refusal and a build, but the prime
does not buy depth. Depth is tier-bound.

## Honest caveats

- The original deepseek dispatch's ask is not on file (no receipt for
  round 3's first build); whether it was primed is unknown. If primed,
  the tier gap is qwen/gemma4 vs deepseek at equal priming. If not
  primed, deepseek cleared the fiction mask unprimed, which widens the
  gap. Either way the mechanism-extraction floor holds.
- n=2 lanes, one seed each, temp 0.4. This is a boundary sketch, not a
  distribution. Widening is cheap ($0) and worth doing before the
  finding goes in the public map.

## Falsifiers

- F-R3-1: if a 7B-tier lane produces a mechanism build (2+ laws as
  working state machines) under the neutral ask, the tier floor claim
  dies.
- F-R3-2: if the priming delta vanishes on re-run (neutral asks start
  building), the refusal was prompt-fragile, not a mask property.

## Receipt

- Outputs (verbatim, prompt-of-record embedded):
  canon/same_book/round3/qwen25coder7b_build_20261022.md,
  gemma4_build_20261022.md (neutral pass),
  qwen25coder7b_build_20261022_primed.md,
  gemma4_build_20261022_primed.md (primed pass).
- Probes fired 2026-10-23T02:10-02:19Z, local ollama, $0.
- Probe scripts: Temp/round3_replicate.py, Temp/round3_primed.py
  (one-shot, not standing tools; llm.py is the network organ).
- Consumer: the same-book battery program and the public map of
  epistemic plurality (the door's next data column).
- Verifier: this receipt's falsifiers F-R3-1/F-R3-2, runnable by
  re-firing the two probe scripts on any lane.
