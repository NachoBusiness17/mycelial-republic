# break-economics: hostile second pass on the economics lens (2026-10-06, stockfish-coding)

Seat: break-economics, hostile pass. Every evidence cite in the lens report was byte-checked
against the estate this sitting. Instruments and outputs listed per claim; nothing below is
carried from the lens without an independent read or run.

## Checks run this sitting (the instrument list)

1. `ls -la tools/gps_mcp/coverage.py` -> 13,300 B (byte-exact vs lens claim).
2. Read `watch/inbox/EG20_PASSATK_LANDED_20261005.md` in full; lines 48-59 carry fable 0.500 /
   opus 0.373 / sonnet 0.241 / haiku 0.096, FLEET 34/58 = 0.586 (line 53), mesh any-of-K 0.349
   vs frontier 0.500 on 43 shared problems -> ROUTE_FRONTIER (lines 57-59). Byte-exact.
3. LIVE REPRODUCTION (beyond the lens's ls-only): `.venv/Scripts/python.exe tools/gps_mcp/coverage.py
   --task-shape arena-agreement-v1 --mesh anthropic/claude-haiku-4.5,anthropic/claude-sonnet-5.5
   --frontier anthropic/claude-fable-5.1,anthropic/claude-opus-5.5` returned byte-identical
   numbers: keyed=209 excluded=252 problems=58, fable 0.500, fleet 34/58=0.586, gain +0.086,
   "ROUTE_FRONTIER - best frontier 0.500 beats fleet coverage 0.349 by more than 0.05 on 43
   shared problems". The lens's blind spot 1 ("numbers are receipt-carried") is cured: they are
   reproduced this sitting, read-only.
4. `grep MIN_PROBLEMS_FLOOR tools/gps_mcp/coverage.py` -> =10 at coverage.py:40; margin default
   0.05 at coverage.py:207; INSUFFICIENT at coverage.py:172 and :224-242. The lens's falsifier
   constants are real.
5. sqlite census: `.venv/Scripts/python.exe` over `tools/gps_mcp/gps_ledger.db3` -> verdict_log
   703 rows, capability 30 rows (byte-exact vs lens). GROUP BY task_shape: arena-agreement-v1
   461, legality-water-graph-v1 100, adversarial-review 68, planning 22, schema-design 20,
   grading 8, code-analysis 8, night-judgment 6, askbank-v1-safeguard 6, world-tick 4. NO
   coding-class battery at or above the floor of 10 exists in the ledger.
6. `PRAGMA table_info(verdict_log)` -> columns: ts, model_id, task_shape, verdict, evidence_hash,
   evidence_resolved, evidence_source, evidence_bytes. NO token column, NO route/rung column.
7. `wc -l memory/runs/trajectory/steps.jsonl` -> 109 rows; `ls -la` -> 144,019 B (byte-exact vs
   lens). `find <repo> -name steps.jsonl` -> the trajectory file plus agents/pytest-tmp-60300
   AND agents/pytest-tmp-64652 fixtures (the lens named 60300 only; 64652 also exists; both are
   test fixtures, immaterial to the finding).
8. Read `watch/inbox/MIRA_METAREASONING_20261006.md`; line 21 verbatim: "steps.jsonl (~37k
   execution trace rows, never joined per the r01 read-the-estate lane)". Byte-exact vs lens.
9. Trail census (F2 falsifier hunt, broader than the lens's name-only find): wc -l over large
   memory/runs jsonl -> ghost/trail.jsonl 19,633 rows (414,721,701 B), governor_autorun_trail
   280,262, compaction_eval/steps_frozen_20260920 8,674, orchestrator_trail 33,549,
   swarm_health/trail 90,736. No file reads ~37k today; orchestrator_trail (33,549) is closest.
10. `grep -n FAMILY_TABLE mag/inference_budget.py` -> line 71 (byte-exact). `grep -n
    CREATE_NO_WINDOW mag/llama_cpp_bridge.py` -> line 30 (byte-exact).
11. Read `watch/inbox/QUEEN_CHESS_LM_20261006.md`; line 23 verbatim carries the gladiator stakes
    law summary, the swarm magnetic-field doctrine, the dungeon dice carrier, MAG DANCE
    (byte-exact vs lens cite; it is a summary, as the lens's blind spot 3 admitted).
12. `wc -l memory/runs/hermes_burn/usage.jsonl` -> 3,010 rows (byte-exact). `tail -5` -> latest
    row ts 2026-10-05T07:12:43.354021Z (byte-exact). FULL-FILE upgrade: `grep -c "2026-10-06"
    usage.jsonl` -> 0. The lens's tail-scoped claim is now a whole-file zero.
13. Dogfood meter hunt (fires the lens's own falsifier): grep of
    `memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/*.checks.json` -> d13-selfplay-run
    checks carry "868 prompt + 406 completion = 1274 total, 320 reasoning_tokens, cost
    0.00084684 USD, model openrouter/auto. Meter is the thought-bank choke point
    (mag/thought_bank.bank wrapped as p..."; d14 carries chars/token calibration lines. BUT the
    banked artifact is absent: `mag/thought_bank.py:30` sets BANK_DIR = ROOT/memory/thinking;
    `ls memory/thinking/` -> only app_reasoning.jsonl and glm-5.3-flash.jsonl; `grep -l
    "2026-10-06" memory/thinking/*.jsonl` -> zero files; no openrouter-auto.jsonl exists.
    bank() at mag/thought_bank.py:31-46 returns False silently when reasoning is empty
    (silent-fail by design, mag/thought_bank.py:11-12). d13's probe/evidence lane artifacts
    carry no meter rows (my grep returned nothing).
14. Lane count: `ls memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/` -> 16 distinct
    d## lane ids (d01 through d16). The lens said "14-lane"; disk truth today is 16; whether the
    run launched 14 and gained 2 post-fold is OWED (no run manifest in the run root, only
    FOLD_SECTIONS.md).
15. Law registry census: `grep -c -i "gladiator|dice|magnetic" memory/law/registry.json` -> 0.
    Registry keys are LAW-1, LAW-3, LAW-4, LAW-6..LAW-13 (rails_over_direction ... 
    experiment-on-absence); none is the gladiator stakes law, the swarm magnetic-field
    doctrine, or the dungeon dice carrier. Targeted greps: gladiator in memory/law +
    memory/rib + docs + corpus/steal -> zero hits; in watch/inbox + memory *.md -> carriers
    only (watch/inbox/hermes_burn/WIRE_PLAN.md, QUEEN_CHESS_LM_20261006.md, today's
    ractor_engine lens files, X_INTEL_HERMES_68_PROFILES_20261004.md). "dice carrier|sha256
    dice" -> dd_dogfood docs and gala_20260925 dd-selfsteal receipt, no law text. "magnetic
    field" in docs -> only canon fiction files (docs/ref/canon/canon_bubbles_holographic_transfer.txt,
    canon_tokens_as_spores_v8.txt). A repo-wide grep (all dirs incl. corpus/) was launched and
    had not completed at bank time; the absence claims here are scoped to the surfaces named.
16. `du -sh memory/runs` -> 1.5G; `find memory/runs -name "*.jsonl" -mtime -3 | wc -l` -> 68 at
    my moment (lens said 70 at its moment; tree-motion, B2-216 applies, not a contradiction).
17. TOKEN_CUES_2610.06851_20261006.md:26 and ALODLM_2610.04198_20261006.md:25 carry S1
    one-sitting rows (TOKEN_CUES S1 explicitly "$0"; ALODLM S1 "No spend" at :33); MIRA S1 at
    MIRA_METAREASONING_20261006.md:25; QUEEN S2 at QUEEN_CHESS_LM_20261006.md:28. The lens's
    "four one-sittings priced in their own receipts" is confirmed.

## Verdicts

### F1 (door's real competitor is the funded-tier dispatch; EG-20 priced the cheap mesh losing) - CONFIRMED, hardened

Every cite byte-checked: EG20_PASSATK_LANDED_20261005.md:48-59 carries exactly 0.349 union <
0.500 fable, 0.586 fleet on 58 problems; coverage.py is 13,300 B; AGENTS.md driving ladder
funds only Hermes primes + grok-4.7. Beyond the lens, I REPRODUCED the routing live
(instrument 3): ROUTE_FRONTIER re-emitted from the production ledger this sitting, so the
evidence is no longer receipt-carried. The falsifier is also pre-tested: the ledger holds NO
coding task_shape with >= 10 keyed problems (instrument 5; the only coding-adjacent class,
code-analysis, has 8 verdict rows total), so the lens's move as priced ("run the EG-20 CLI on
a coding task_shape batch, ~30-60 min") cannot return a verdict tonight: the CLI would emit
INSUFFICIENT at coverage.py:224 before any comparison. The finding stands; the move is
mispriced (see additions A3).

### F2 (MIRA S1 priced on a phantom corpus: receipt says ~37k rows, production steps.jsonl holds 109) - CONFIRMED, hardened

Byte-exact on every number: MIRA_METAREASONING_20261006.md:21 verbatim; wc -l 109; 144,019 B;
repo-wide find reproduced (instrument 7, adds the pytest-tmp-64652 fixture dir the lens
missed; immaterial). Hardened twice. First: the ~37k is not merely unmeasured, it is an
ALREADY-STRUCK number re-banked: watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md:114 adjudicates
it under Code 2 premise-drift: "r01 ('~37k rows' inherited from AE5, live stream read
55,571+)". The MIRA receipt re-carried a number the estate's own run-spec fold had struck the
day before: the struck-191.8M-headline disease in recurrence. Second: the falsifier ("a ~37k
trace under a different name would flip the finding") is answered negatively at today's bytes
(instrument 9): no file reads ~37k rows; but larger trace corpora DO exist under other names
(orchestrator_trail 33,549 rows, governor_autorun_trail 280,262, swarm_health 90,736), so the
receipt's deeper claim that the estate holds the corpus is TRUE IN SUBSTANCE and FALSE in the
named file and number. S1 as banked (corpus: steps.jsonl) would still train on 109 rows.

### F3 (reward leg built, board leg absent, dispatch/route sequencing is the cheapest real class tonight) - CONFIRMED, move defect noted

sqlite counts byte-exact (verdict_log 703, capability 30, instrument 5); FAMILY_TABLE at
mag/inference_budget.py:71 byte-exact; CREATE_NO_WINDOW at mag/llama_cpp_bridge.py:30
byte-exact; the gladiator stakes reward law is carried verbatim at
QUEEN_CHESS_LM_20261006.md:23 (and only there among law surfaces: instrument 15); usage.jsonl
3,010 rows byte-exact. The absence claim ("board leg does not exist anywhere in the estate
bytes I read") is properly scoped per the quantifier law and I did not contradict it. The
falsifier remains open (I ran no backtest), but I found a move defect the lens priced over:
verdict_log carries NO token and NO route columns (instrument 6), so "reward = banked verdict
minus tokens" and "state = rungs tried" cannot be reconstructed from the 703 rows alone; the
60-90 min backtest estimate assumes a join surface (usage.jsonl ids? thought_bank rows?) that
is unproven. Spec the join before the clock, or the first game cannot be scored.

### F4 (self-play league is a cluster ask dressed as one sitting; today's free-lane burn has no token meter) - CONFIRMED, hardened

The tail-scoped claim upgrades to whole-file: usage.jsonl has ZERO rows dated 2026-10-06
(instrument 12, grep -c = 0; latest row 2026-10-05T07:12:43.354021Z). The lens's falsifier
("a token meter row under a name my grep missed") FIRES AND THEN DIES: d13-selfplay-run
checks.json carries a grader-verified meter claim (868 + 406 = 1274 tok, 320 reasoning_tokens,
0.00084684 USD, openrouter/auto, "meter is the thought-bank choke point"), but the banked
artifact does not exist: memory/thinking holds two files, neither has a 2026-10-06 row, and no
openrouter-auto.jsonl exists (instrument 13). bank() silently returns False on empty
reasoning (mag/thought_bank.py:31-33), so the meter can no-op without a trace. Net: the
finding is STRONGER than the lens stated: today's 16-lane burn (instrument 14; the lens said
14, disk reads 16 distinct lane ids) left no meter row in usage.jsonl, in memory/thinking, or
in any lane probe artifact I searched; the only token text today is a checks.json grading the
arithmetic of a claim whose bank row is absent, which is a fabrication-smell of its own
(grader proved 868+406=1274, nobody proved the row landed). The four one-sittings priced in
their own receipts are confirmed (instrument 17).

## What the lens missed (additions)

### A1. The 37k is a zombie number: struck by the run-spec fold, re-banked by the MIRA receipt the next day
Evidence: watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md:114 (Code 2: "r01 ('~37k rows'
inherited from AE5, live stream read 55,571+)") vs watch/inbox/MIRA_METAREASONING_20261006.md:21.
Falsifier: a dated erratum or strike row exists in the MIRA receipt or its LINKS row
acknowledging the addendum (I read the full receipt: none exists; addendum line 114 stands
unreferenced by MIRA).
Move: append a strike/erratum row to MIRA_METAREASONING_20261006.md citing the addendum, and
re-denominate S1 against the trail census in A2; 15 min, $0.

### A2. The real corpus exists under other names: name it or the re-denomination has no target
Evidence: wc -l this sitting: memory/runs/orchestrator_trail.jsonl 33,549 rows;
memory/runs/governor_autorun_trail.jsonl 280,262; memory/runs/swarm_health/trail.jsonl 90,736;
memory/runs/ghost/trail.jsonl 19,633; steps_frozen_20260920.jsonl 8,674.
Falsifier: none of those trails carries partial-state -> outcome pairs joinable to lane
outcomes (row schema check), in which case the lane archives stay the only corpus and A1's
strike stands with no re-denomination target.
Move: schema-check the five trails for state/outcome fields and pick the joinable one as S1's
corpus; 30 min, $0.

### A3. The door's pricing move is mispriced: no coding-class battery exists in the ledger
Evidence: sqlite GROUP BY task_shape over gps_ledger.db3 this sitting (instrument 5): max
coding-adjacent class is code-analysis at 8 rows, below MIN_PROBLEMS_FLOOR = 10
(tools/gps_mcp/coverage.py:40); the CLI would emit INSUFFICIENT at coverage.py:224.
Falsifier: a coding task_shape with >= 10 keyed problems appears in verdict_log before the
door's pricing run (then the CLI move is correctly priced and this addition dies).
Move: split the lens's move into two priced steps: (a) generate the coding batch into
verdict_log (an arena-style battery on one coding class, the expensive leg), (b) then the CLI
run (~5 min); reprice the door's tonight-cost accordingly.

### A4. The meter no-ops silently, and a grader certified arithmetic on a row that never landed
Evidence: mag/thought_bank.py:31-33 (bank returns False on empty reasoning, silent-fail noted
at :11); memory/thinking/ has zero 2026-10-06 rows (instrument 13) while
d13-selfplay-run.checks.json grades "868 + 406 = 1274 ... cost 0.00084684 USD" as banked.
Falsifier: the d13 probe's meter row exists under a third surface I did not search (I covered
usage.jsonl, memory/thinking, lane receipt.md + checks.json + probe/evidence files); a bank
file outside memory/thinking would flip this.
Move: one rerun of the d13 probe with reasoning non-empty and verify a row lands in
memory/thinking/openrouter-auto.jsonl, or bank an erratum on the checks row; 20 min, $0.

### A5. The reward side of the encoding cites a "law" that is in no law registry
Evidence: memory/law/registry.json has zero gladiator/dice/magnetic entries (instrument 15);
the 12 registered laws are LAW-1..LAW-13 with other titles; the gladiator stakes law exists
only as receipt-carried summary (QUEEN_CHESS_LM_20261006.md:23) and mention-carriers
(WIRE_PLAN.md, dd_dogfood, gala dd-selfsteal receipt).
Falsifier: the law text exists outside my searched surfaces (memory/law, memory/rib, docs,
corpus/steal negative; watch/inbox + memory .md positive-for-mentions only; the repo-wide
corpus-inclusive grep had not completed at bank time) - a memory/law or rib path carrying the
law bytes flips this from absence to unlocated.
Move: operator points the law's true path, or the door card marks the gladiator reward as
receipt-carried-not-registry-law; 10 min, $0.

## Blind-spot dispositions

- Blind spot 1 (EG-20 numbers receipt-carried): CURED this sitting, live reproduction,
  byte-identical (instrument 3).
- Blind spot 2 (QUEEN arXiv id/repo/weights OWED): stands; QUEEN_CHESS_LM_20261006.md:35
  carries the OWED verbatim; I did not fetch them either.
- Blind spot 3 (law texts unlocated): CONFIRMED and hardened with the registry zero
  (instrument 15); scope of my negative claims named in instrument 15.
- Blind spot 4 (lane-archive denominator unmeasured): still unmeasured; my A2 names the
  candidate trails but I ran no joinability check.
- Blind spot 5 (DUNGEON_ACTOR_MODEL proxy table unverified): stands, unverified by me too; the
  EG20 receipt itself flags it at :73-79, so the caveat is receipt-native.
- Blind spot 6 (free-lane true marginal cost unpriced): stands; A4 shows the meter did not
  even record today's burn, so the cost side is darker than the lens stated.

Banked by break-economics (hostile pass), 2026-10-06. All commands and outputs named above
were run this sitting; the repo-wide corpus grep (instrument 15, final leg) had not completed
at bank time and its result is not claimed.
