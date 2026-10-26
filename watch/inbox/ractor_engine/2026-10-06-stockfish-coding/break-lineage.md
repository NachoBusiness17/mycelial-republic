# BREAK-LINEAGE: hostile second pass on the lineage lens (2026-10-06)

Target: `watch/inbox/ractor_engine/2026-10-06-stockfish-coding/lineage.md` (on-disk, 189 lines).
The copy handed to this pass truncated F4's finding/move text and dropped F5 entirely; the
disk copy is complete (F5 at lineage.md:134-163). Verdicts cover all five findings. Every
claim below cites a byte I read or a command I ran this sitting. No em-dashes.

## Integrity notes (this pass's own instruments, per the never-fabricate law)

- cwd trap: my first NNUE census and stockfish find ran from a wrong working directory
  (the shell persists cwd across calls; an earlier `cd` into the ractor dir moved it) and
  returned false zeros. Both VOIDED. Every count below is from an explicit
  `cd /c/Users/foste/Documents/projects/local_sovereign_agent &&` re-run.
- A hook false-positive blocked one read-shaped command (sed over mag/accumulator.py was
  read as a source write); re-run via the Read tool. No writes to mag/ were attempted.
- No test suite run: none was named in the ask. Executions this sitting: file reads,
  Git Bash greps/finds/ls/sed, two corpus_search probe batches via
  `.venv/Scripts/python.exe`, one filesystem-wide find, TaskOutput waits on background
  greps (one stopped at scope, named below).

## Verdicts

### F1, founding thesis is the 09-16 journal order and its stone is pending 20 days (lineage.md:8-47): WEAKENED

Byte-checks that held:
- `memory/continuity/seat_memory_20260927/journal-orders-20260916.md:41-45`: order
  verbatim, "the cipher must be lossless or a move-only player can't act. First mapping
  stone pending." at :44-45.
- `memory/continuity/seat_memory_20260927/quest-cipher-doctrine.md:26`: inversion
  paragraph repeats the order, ends "First mapping stone pending".
- `watch/STOCKFISH_DOCTRINE_20260903.md` (2,949 B, my ls): :3 AUDIT-TYPED 2026-09-08
  LIVE with "generalization itself unbuilt"; :9-11 the eval-surface split; :42-46 the
  4-item BUILD list.
- wavelength census re-run (`grep -rn "wavelength" mag/ tools/`): only
  `mag/game_campaign.py:4034`, a word-list tuple ("waver", "waving", "waves",
  "wavelength", "waveform"). Build item 2 unbuilt, consistent with :3.
- Zero "lossless" in all six sibling lens files (grep -i lossless over accuracy,
  economics, operations, logic, moonshot-1, moonshot-2: zero hits).
- Date math: 09-16 to 10-06 is 20 days.
- "No ractor input cites either" holds for the ractor's own file set: my grep over the
  eight dir files shows no path citation of STOCKFISH_DOCTRINE_20260903, journal-orders,
  or quest-cipher outside lineage.md itself.

What breaks the finding as stated (the lens's own falsifier half-fired):
- `watch/inbox/ENGINES_IN_CHARGE_20260916.md` exists, titled "mapping stone one
  (2026-09-16)", same day as the order. It contains the full lossless mapping contract
  (:16-24, "lossless or it doesn't ship": state-to-board, action-to-move,
  legality-to-lane-rules, result-to-score), three falsifiers (:26-32), the first-stone
  plan (:34-37), and the engine-per-work-class split (:39-43).
- The same wave's audit already typed the stone's state:
  `watch/inbox/wave_20260916/receipts/MI1_INBOX_MINE_PRIMARY.md:29-33`: "UNWIRED - the
  mapping contract and 3 falsifiers are stated; 'first stone' ... has no receipt anywhere
  in the wave or repo" (:31), "DEMAND: Stone one has not been played: no GTP session log
  exists" (:32); cross-connection to the ablation defense at :33 and :222, and
  RS_EAST_PRIMARY.md:59, RS_WEST_PRIMARY.md:58.
- My census (`grep -rn -i -E "mapping[- ]stone" watch/inbox memory state queue corpus
  docs`, pending-lines filtered) found the spec and no delivery. A follow-up sweep for
  later payment (`grep -rn -i -E "katago|gtp " watch/inbox memory/runs --include="*.md"`,
  wave_20260916 and ENGINES_IN_CHARGE excluded) returns only 09-11/09-12
  stone-protocol-era bytes: no post-09-16 GTP move log exists anywhere I scanned.
- Consequence: the narrowed truth is "stone one was spec'd and receipted same day, typed
  UNWIRED by the 09-16 wave audit, and its move log is still unpaid 20 days later." The
  lens's move (write an encoding card with lossless-actability as test 1) re-mints
  ENGINES_IN_CHARGE's own falsifier 1 (:28-29, "Any move needing translation = lossy =
  fail") and its mapping contract without citing them.
- Rhetorical nuance: `watch/inbox/QUEEN_CHESS_LM_20261006.md:23` lists the founding
  thesis under "Operator prior art:" (no byte paths). The receipt remembered the thesis;
  F2's phantom pointer is the actual lineage break, not estate-wide amnesia.

### F2, the memory index points at a phantom card for the founding doctrine (lineage.md:49-71): CONFIRMED

- `memory/MEMORY.md:263` row read verbatim; it points at project-stockfish-doctrine.md.
- Find from repo root (`find . -name "project-stockfish-doctrine.md" -not -path
  "./.venv/*" -not -path "./.git/*"`): zero hits.
- Fossil: `memory/continuity/fossil_generations_20260930/MEMORY_resolved.md:256` marks it
  phantom (its "MEMORY.md:L322" is an older generation's line number; the current row
  sits at :263; the card never returned either way).
- `memory/runs/mickey17/MASTER_INDEX_20260920.md:1216` still stamps the same card [LIVE].
- My reference census, completed scope memory/ + watch/ + docs/ + state/ + queue/
  (`grep -rln "project-stockfish-doctrine"`): 11 hits, all pointer rows (MEMORY.md, two
  .bak generations, the fossil, MEMORY_TRIM_PROPOSAL, gapwave _owed_live_all.json,
  digest_mem_14.jsonl, MASTER_INDEX, thinking/app_reasoning.jsonl, this session's
  trajectory, lineage.md). Zero card content under any name. The corpus/ portion did not
  complete at bank time (stopped for scope; OWED below). The renamed-card falsifier is
  answered within the completed scope: no content-bearing reference surfaced.

### F3, the operator's pre-QUEEN brief names the rejector constraint and nothing was built (lineage.md:73-99): WEAKENED

- Constraint byte-checks: `docs/ref/NNUE_SIDECAR_BRIEF_20260904.md:18` verbatim ("a raw
  7B has no bound unless you add a rejector"); the "no bound at all / unless an outer
  loop rejects it" sentence spans :46-47, not :47-48 as cited (line nit; :47-48 does
  carry "Wrapping a 7B in naive tree search without a calibrated value head ...").
- `memory/runs/mickey17/MASTER_INDEX_20260920.md:1965` verbatim ("18/25 BUILD WINDOWED -
  design note SPAWNED and landed").
- The lens's own falsifier fired: `mag/accumulator.py` EXISTS (ls: 11,199 B, mtime
  Sep 4 18:34, three hours after the brief's 18:31; committed in 60b1bde7f). Its
  docstring: "NNUE-style accumulator v0 for a coding agent ... THIS FILE IS THE
  MEASUREMENT RIG'S DATA STRUCTURE, not a trained model" (:1-6); head is an "UNTRAINED
  placeholder" (:17); "Not here yet: decay firing on real rows, certainty fed by real
  receipts, seat wiring" (:21-22). Banked at `watch/inbox/FLEET_IMPRINT_20260917.md:17`.
  No tests (`ls tests | grep -i -E "accum|nnue"`: empty).
- "No build receipt ever fired" is contradicted at the module level and survives only
  narrowed: no measurement receipt, no calibration, no seat wiring, no tests. The
  constraint remains unwired into any door card, which is the finding's live core.
- The census characterization "only audit and imprint files" undercounts: my
  case-sensitive `grep -rl "NNUE" watch/inbox memory/runs` returns about 28 files,
  including CANON_MINING_20260916.md:9 (the brief referenced as hardware-rhyme) and
  STONE_PROTOCOL_SELF_STEAL_20260911.md:46-49.

### F4, the prior-art instrument zeroes on the thesis's own words, mirrors dilute the rest (lineage.md:101-132): CONFIRMED

Re-ran the probes (`.venv/Scripts/python.exe -c "from tools.corpus import corpus_search; ..."`):
- The three named multi-term queries return hit_count 0 / rows_scanned 0 each, engine
  fts5, index_state fresh, map_asof 2026-10-06T07:36:37Z (byte-identical to the lens's
  cite), law line intact.
- "stockfish" returns 12 hits; `watch/STOCKFISH_DOCTRINE_20260903.md` at position 6,
  exactly as claimed.
- The tool's parity_note in every response says "B2-22 measured 3 of 10 queries short"
  verbatim, citing the B2-22 path; the file itself reads "substring parity on 6 of 10
  queries, 3 small deltas all traced to mid-token matches" (:5) and "Parity: 6/10 exact"
  (:33). The lens's CONVERGENT flag is byte-true.
- Catalog: `grep -c STOCKFISH_DOCTRINE_20260903 catalog/catalog.jsonl` = 2;
  journal-orders-20260916 = 2; quest-cipher-doctrine = 2 (sum 4, as claimed).
- `tools/corpus.py`: `_fts_expr` at :133, AND-joined quoted prefix phrases, docstring
  "Kept verbatim from the B2-22 spike". The move targets the right function.
- Falsifier probe I ran: "stockfish doctrine" returns the doctrine at position 1 (2
  hits); "stockfish chess" returns 0 (the doctrine body contains no "chess" token). The
  zero-hit is AND-token-shape fragility, exactly the outcome the lens's falsifier
  predicted; the finding survives as framed.
- Nits: I count 8 stockfish.html copies on the board (positions 1,2,3,4,7,8,9,10), not
  "FOUR ... plus lsa_reboot_staging mirrors" as worded (position 7 is the
  _archaeology_out/mag-disk-20260905 copy, unnamed); the INTAKE_NNUE_ACCUMULATOR card
  also outranks the doctrine at position 5. The "10 of 12 echoes" arithmetic holds
  (everything except positions 5 and 6).

### F5, EG-20 re-banked as a steal one day after landing (lineage.md:134-163): CONFIRMED, weak form

- QUEEN receipt S4 verbatim at :30; the row says "extending the EG-20 pass@K column"
  (acknowledges the base column) but carries no pointer to the landing receipt. The
  lens's own falsifier ("if the next receipt edit adds the pointer, the finding collapses
  to a wording nit") already half-fired in the original text.
- EG20 receipt byte-checks: `watch/inbox/EG20_PASSATK_LANDED_20261005.md:23` ("the
  existing capability.pass_rate meaning"), :44 (209 keyed / 252 excluded / 58 problems /
  4 models), :49 (fable 40 attempts / 0.500), :57-59 (mesh any-of-K 0.349 vs frontier
  best pass@1 0.500 on 43 shared problems, ROUTE_FRONTIER).
- `watch/inbox/ractor_engine/2026-10-04-eleven-doors/lineage.md:22-45` confirms EG-20
  was the only door with a measured effort figure, silently dropped from the handed queue.
- Composition cites: `mag/agent_arena.py:20` (SUPPORTED_GAMES = frozenset({"chess"})),
  :30 START_FEN; `mag/effect_broker.py:317` ("schema": "effect_broker.v1" exactly at
  :317). The amend move (add the pointer to S4) stands.

## Additions (what the lineage lens missed)

Non-convergent check: grep for ENGINES_IN_CHARGE|accumulator|STONE_PROTOCOL across the
four sibling hostile passes (break-accuracy, break-economics, break-operations,
break-dogfood) returns zero hits; none of the six additions below is banked elsewhere.

- A1: The ractor's flagship move re-mints banked bytes. ENGINES_IN_CHARGE_20260916.md:16-43
  already states the lossless mapping contract, the lossless-actability falsifier
  (:28-29), and the first-stone plan; MI1_INBOX_MINE_PRIMARY.md:29-33 already types it
  UNWIRED with the move-log demand. The door card should cite and inherit those
  falsifiers; the one-sitting action is playing stone one (one lane, one session, log
  move-to-action pairs), not re-specifying it. Falsifier: a byte-diff showing the card's
  test 1 differs materially from ENGINES' falsifier 1. Move: 0 extra minutes; it replaces
  the lens's 90-minute card-writing move with the stone the operator already ordered.
- A2: A fourth prior articulation the mine missed:
  STONE_PROTOCOL_SELF_STEAL_20260911.md:46-49 (AlphaGo architecture on a real board:
  policy = agents, value = Stockfish NNUE / KataGo, self-play distillation named; cost
  guardrail at :54) plus MASTER_INDEX_20260920.md:1217 ([OWED] stone protocol with
  "optimizer layer (AlphaGo on fleet hardware) addendum"): an unpaid AlphaGo stone OLDER
  than the journal stone. The lineage lens's jacket is mining exactly these. Falsifier:
  a byte showing :46-49 is about something other than engines-as-value on real boards.
  Move: 10 min, add the 09-11 lineage to the door card's prior-art block.
- A3: The operator's own pre-banked kill line sits in the Part B the lens skipped:
  NNUE_SIDECAR_BRIEF_20260904.md:121-123 ("If the sidecar does not beat 'just prompt the
  7B with a longer scratchpad' at equal wall time, STOP"), plus :115-116 (ship only
  Elo-like wins at fixed latency) and :157 (the rejector row in the landscape table).
  The kill-criterion section should inherit the brief's STOP as a second, older,
  operator-banked kill line. Falsifier: a reading of :121-123 that yields no STOP
  condition. Move: 5 min, one sentence in the kill criterion.
- A4: The S1 weld map already has a working draft:
  watch/inbox/hermes_burn/H247_A3_QUEEN_WELD_MAP_DRAFT.md, marked DRAFT-FOR-RACTOR-FOLD
  (five component-to-organ mappings, each with a falsifier; three priority tests; meta
  falsifier at :37). The ractor should fold it, not re-derive the weld map. Falsifier:
  the draft missing one of the receipt's five components. Move: 15 min fold.
- A5: Evidentiary caveat not carried: the QUEEN numbers (900 Elo, 1782-to-2697,
  beats-frontier) are the paper's own claims read off an abstract card image; arXiv id
  and repo URL remain OWED (watch/inbox/QUEEN_CHESS_LM_20261006.md:6, :35; :36 admits
  not re-measured). Any door design banking those numbers inherits an unverified
  external. Falsifier: the receipt gaining a fetched arXiv id plus first-hand bytes.
  Move: 10 min, stamp the caveat on any door card that cites the Elo curve.
- A6: The trigger's receipt path is wrong: watch/inbox/receipt_watch/QUEEN_CHESS_LM_20261006.md
  does not exist; the receipt is at watch/inbox/QUEEN_CHESS_LM_20261006.md (my find
  returned exactly one QUEEN_CHESS hit repo-wide). The lens silently used the correct
  path. Falsifier: a receipt_watch/ copy appearing. Move: 0 min, note only.

## Kill criterion

The lineage kill (no lossless-actability test on one real episode = metaphor door, dies
before any bout) survives this pass. Amendment from A1 and A3: the test already exists
(ENGINES_IN_CHARGE_20260916.md:28-29) and the STOP line already exists
(NNUE_SIDECAR_BRIEF_20260904.md:123). The door dies if it neither plays stone one nor
honors the STOP, regardless of new card text.

## OWED

- The corpus/ portion of the project-stockfish-doctrine reference census did not complete
  at bank time (grep stopped; scope named in F2). Completed scope: memory/, watch/, docs/,
  state/, queue/. The exact-name find over the full tree (zero hits) and the completed
  pointer-only census carry the finding.
- No test suite run (none named in the ask); all checks above are the named instruments.
