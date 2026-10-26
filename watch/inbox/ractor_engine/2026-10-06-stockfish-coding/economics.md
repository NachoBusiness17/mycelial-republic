# RACTOR: the Stockfish-coding door, economics lens (EV-per-cost)

Seat: economics. Moment: 2026-10-06 (this sitting). Topic: the operator's
founding thesis on record today ("put Stockfish in charge of coding by
encoding programming problems in chess, then to AlphaGo"), triggered by the
QUEEN link-drop banked the same sitting. My job: price the door in expected
value per minute and per token, kill cluster asks dressed as one-sittings,
and name the kill criterion before the first token burns. Every "my" claim
below was read or run this sitting on this box; carried items say so.

## The encoding map (the ONE class I would encode tonight)

Chosen class: **dispatch/route sequencing** (the driving ladder itself), not
patch sequencing. Reason: it is the only programming-problem class where the
estate already measures the reward and the engine table byte-side, so the
door can be backtested the same sitting it is specified.

- **Board (state):** one dispatch episode: (task_shape, rungs tried, budget
  remaining, attempts so far). Finite and small: the tier ladder is 4 rungs
  (ollama janitor -> free lane -> deepseek flash -> prime/grok) x the
  measured per-animal table (mag/inference_budget.py:71 `FAMILY_TABLE`,
  my grep) x budget. Chess-shaped: discrete state, alternating picks,
  terminal solve-or-broke.
- **Moves:** pick the next rung/animal for this task_shape, or stop-cert the
  episode (the MIRA receipt's stop-cert row, watch/inbox/
  MIRA_METAREASONING_20261006.md:26-27).
- **Reward:** won bout = banked real answer (the gladiator stakes law,
  carried from QUEEN_CHESS_LM_20261006.md:23) minus tokens spent, per the
  banked usage line (memory/runs/hermes_burn/usage.jsonl, 3,010 rows, my
  wc -l).
- **Silent expert:** deterministic search whose eval function is the
  measured tables, not a neural net: tools/gps_mcp/gps_ledger.db3
  verdict_log 703 rows + capability 30 rows (my sqlite COUNT this sitting),
  the EG-20 coverage/mesh-vs-frontier arithmetic, the workflow gate, corpus
  FTS, verkle verifier. This is the estate's Stockfish: it is silent
  (tables and verifiers explain nothing unprompted) and it dominates
  because its evaluation is measured, not guessed.
- **Explain layer:** tonight, the seat reads the engine's table and files
  why-this-rung in the GPS verdict row format (the 703-row ledger is already
  an explanation corpus). The QUEEN-style trained 4B speaker is OWED (arXiv
  id + repo + weights not byte-fetched; receipt :35) and is not on tonight's
  board.
- **Port layer:** the fold amendment table + quantizer law pack (recompiled
  09:28:25Z carrying 2 of 12 law rows, watch/inbox/DAWN_REPORT_20261006.md
  logic-lens amendment) - the distill-back machinery exists, which is the
  port side of the Bellman loop.

## What exists (verified this sitting vs carried)

- VERIFIED: EG-20 instrument and receipt (tools/gps_mcp/coverage.py,
  13,300 B, my ls); ROUTE_FRONTIER measured on arena-agreement-v1: cheap
  mesh 0.349 < frontier pass@1 0.500, fleet any-of-K 0.586 (watch/inbox/
  EG20_PASSATK_LANDED_20261005.md:48-59). This is the estate's own EV-per-
  cost table and it prices the door's competitor.
- VERIFIED: gps_ledger.db3 verdict_log 703 rows / capability 30 rows (my
  sqlite3 count); usage.jsonl 3,010 rows banked (my wc -l); FAMILY_TABLE in
  mag/inference_budget.py:71 (my grep); selfimp imp002 harness organs exist
  and one is actively modified today (mag/lora_pipeline.py mtime Oct 6
  15:15, my ls; mag/llama_cpp_bridge.py carries CREATE_NO_WINDOW on win32,
  my read of its header, the win32 spawn law held in the only subprocess
  organ I read).
- CARRIED (receipt bytes, not re-measured): QUEEN 900 Elo / 1782->2697 over
  7 iterations, 4B params beating frontier with 3 OOM fewer params; MIRA's
  generative critic; token-cue MATH-500 lifts; ALoDLM benchmark sweep. All
  are the papers' own claims per their receipts.
- CARRIED: the gladiator stakes law, swarm magnetic-field doctrine, dungeon
  dice carrier, MAG DANCE beat grid. My greps for their original bytes hit
  harvest files and burn-wave cards, not the law texts; I did not locate the
  law-bearing files this sitting (marked OWED, not asserted as read).

## What breaks (falsifiers)

1. **The wrong-competitor falsifier:** if the door is pitched against zero,
   it always looks good. The real competitor is the funded-tier dispatch
   (Hermes prime / grok-4.7, the only funded rungs per the driving ladder).
   EG-20 already shows cheap seats alone lose on this battery class
   (0.349 < 0.500). The weld only pays if (cheap seat + silent expert) beats
   the frontier route's $/solved-problem on a priced battery.
2. **The phantom-corpus falsifier (found, live):** MIRA receipt S1 prices
   the lane-value forecaster on "steps.jsonl (~37k execution trace rows)"
   (watch/inbox/MIRA_METAREASONING_20261006.md:21). My wc -l on the only
   production steps.jsonl the repo-wide find returned is 109 rows /
   144,019 B (memory/runs/trajectory/steps.jsonl; the other hits are
   agents/pytest-tmp-60300 test fixtures, named scope). A critic trained on
   ~100 rows is noise. The real corpus is the lane archives (memory/runs =
   1.5G, 70 jsonl files touched in 3 days, my bounded find) and its join
   denominator is UNMEASURED.
3. **The INSUFFICIENT falsifier:** the coverage instrument refuses to
   predict under a 10-attempt floor or inside a 0.05 margin (EG-20 receipt
   :31, the census-denominator law). If the door's home class has thin
   ledger rows, the engine's eval function is noise and the encoding dies
   for that class, not the thesis.
4. **The explain-tax falsifier:** QUEEN's 900 Elo includes 7 trained
   distillation iterations. If the port layer's tokens per solved problem
   exceed the frontier dispatch's cost per solved problem, the door prices
   negative even when the engine wins.

## What runs tonight, one seat, one sitting

1. Price the home class ($0, ~30-60 min): run the EG-20 CLI on a coding
   task_shape batch, not arena-agreement: `python tools/gps_mcp/coverage.py
   --task-shape <coding-shape> --k-hint 4 --mesh ... --frontier ...`. If
   INSUFFICIENT, that is the finding and the door waits for ledger volume.
2. Backtest the board (free, ~60-90 min): replay the 703 verdict rows as
   episodes; the greedy measured-table policy picks rungs; score its EV per
   solved problem against the routes actually taken. This is the silent
   expert's first game, no training.
3. Re-denominate MIRA S1 (free, ~30 min): count joinable outcome rows in
   the lane archives before anyone trains the forecaster; strike or reprice
   the receipt's 37k row.

## Kill criterion

The door dies for this class if the backtest (2) shows the measured-table
policy does not beat the routes actually taken on the same problems. It dies
outright if no coding task_shape clears the INSUFFICIENT floor. The
self-play-league moonshot is a CLUSTER ASK (MIRA join + cue battery + ALoDLM
garden probe + encoding door + weld training = at least four one-sittings
plus a training run, each already priced separately in its own receipt) and
is killed as a single ask at the gate; it may proceed only as its parts, and
no league lane burns without a banked token row (usage.jsonl is the meter;
my tail showed latest 2026-10-05T07:12Z, scoped to the last 5 rows - any
2026-10-06 paid row earlier in the file would not appear there, so I claim
no zero for today, only that the line exists and is the meter).

## Moonshot, priced honestly (the 10x)

The whole harness as a self-play league is real but it is four banked
one-sittings plus one training run, not one sitting: (a) MIRA-AC forecaster
on the re-denominated lane corpus, (b) cue-lift battery on the garden
(token cues S1, $0 local), (c) ALoDLM garden integration probe, (d) the
encoding door's backtest above, then (e) the weld: QUEEN's cross-attention
shape trained on the estate's own (position, move, explanation) triples
harvested from (a)+(d). The league's population is the free-lane fleet;
its referee is the arena battery; its ledger is usage.jsonl. EV gate for
(e): (d) must show positive EV vs the frontier route first.

## Blind spots

- I did not execute coverage.py, any test suite, or the backtest this
  sitting; all EG-20 numbers are receipt-carried, the instrument's
  existence verified by ls only.
- QUEEN's bytes are the abstract card via the receipt; arXiv id, repo, and
  weights are OWED (receipt :35). I did not fetch them.
- I did not locate the original bytes of the gladiator stakes law, the
  magnetic-field doctrine, or the dice carrier; my greps hit derivative
  files. Any encoding map that leans on them leans on carried summaries.
- The lane-archive join denominator (the real MIRA corpus) is named but
  unmeasured; 1.5G du is a size, not a row count.
- The DUNGEON_ACTOR_MODEL proxy table behind EG-20's model names is
  unverified by me (EG-20's own caveat stands).
- Local fleet costs (power, seat minutes) are priced at $0 as the estate
  convention does; the true marginal cost is not in any ledger I read.
