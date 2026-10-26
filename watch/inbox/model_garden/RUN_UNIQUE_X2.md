# RUN UNIQUE X2 - lane X2 (UNIQUE INPUTS, cheap-first) of the cross-model program

**Schema:** run.garden-v1-unique.v1 . **ts:** 2026-10-01T23:23-23:55Z UTC
**Seat:** ZCode subagent, model-garden lane X2. **Spend:** $0.999 real / $3.00 cap
(banked in ledger $0.8417; kimi+glm bank $0.0 unpriced on Nous credits).

MISSION: "not wasting their unique inputs" - one ask per family shaped to its
PROVEN edge, on estate material, through the gated carriers. All fires ran
tools/model_garden.py over memory/plans/garden_battery/unique/ with the
mag/inference_budget.py recipes planning every call. Scores + checks + shas
landed in GRID_unique.json; this receipt carries the run story.

## Fire order (cheap-first) and outcomes

| # | family / SKU (Nous) | ask | outcome | real $ |
|---|---|---|---|---|
| 1 | glm-5.3-flash | census cross-index | LANDED 4/5 | 0.0016 |
| 2 | kimi-k2.6 | register triage whole | DNF transport (900s x2) | 0.0 |
| 2b | kimi-k2 (family recovery, changed param) | same bytes | LANDED 4/6 | 0.0 |
| 3 | claude-sonnet-5.5 | rooms+room adversarial | LANDED 6/6 | 0.1556 |
| 4 | claude-fable-5.1 | B1 retry at 24k floor | LANDED 5/5 | 0.8417 |

## (1) KIMI: the 239KB register whole in one window

- kimi-k2.6 arm: whole-response 900s read timeout x2 (~30 min wall), zero
  bytes back, no ledger row, $0 banked. Transport finding (banked as a
  transport observation): this SKU cannot carry a 61k-token input over the
  carrier's whole-response transport; streaming or a smaller window only.
- kimi-k2 arm (lawful changed-param recovery inside the family): LANDED.
  85,573 prompt tokens = the whole 600-row register + contract in ONE window,
  676-token reply, content channel, $0.
- Verdict 4/6, the split IS the finding: block retrieval 10/10 (it found
  exactly the stealth-fanout-wave2 10-findings run: all 10 work ids, both
  models, the 10/10 scores, in order) but every ROW cite is off by 9 (cited
  rows 69-78, truth 78-87). Content from an 85k-token window: excellent.
  Row NUMBERS from a 600-line window: systematically shifted, unusable
  without re-alignment. Contradictions 1/3 byte-exact, and the one that
  lands is real: rows 4 vs 7, same answer_file, cached_tokens 149 vs 152,
  same finish=stop = the register's double-banking signal.

## (2) SONNET: the surfaces it had NOT seen (server/rooms.py + server/room.py)

6/6 with KNOWN-A (unbounded peer queues on the live path) and KNOWN-B (bare
ticks) named and excluded in the contract. What ELSE it found, all three
operator byte-verified against the frozen copies:

1. _tick_loop (rooms.py:202-208) catches ONLY CancelledError: any raise from
   world.tick()/innkeeper.pump()/stage() kills the pump task silently while
   self._pump stays non-None, so pumping still reads True and ensure_pump()
   never restarts. The room freezes until process restart. Only on_tick is
   guarded (the Z1 weld law moved with the pump; the loop body did not).
2. Room creation is unbounded and never reaped (get_or_create 276-285,
   drop_peer only stops the pump): every well-formed hello id builds a
   MountainWorld + log + innkeeper memories forever, and room_of_sid scans
   them all per action.
3. join_peer (115-121) never unseats the peer from its old room before
   overwriting peer["room"]: a cross-room re-hello leaves the peer in two
   peers dicts = both rooms' ticks, ghost seat, isolation law broken
   (caller-dependent; server.py honestly flagged UNVERIFIED).
DIFFERENT-BUILD independently re-derived the wiring-debt census row 1 fix
(fan out through transport Room.publish) = confirmatory convergence with
filed prior art.

## (3) FABLE: ONE retry of the B1 carrier review with the recipe

The animal lands when the harness fits: 0/5 at 12k (fable1 B1: 12000/12000
reasoning tokens, content channel empty, $0.68 burn) to 5/5 at the 24k
review floor ($0.84, finish=stop, 14141 reasoning + 939 content). The floor
is CONFIRMED as the minimum viable cap (rail observation banked). It still
burns 94 pct of output on reasoning; the recipe just leaves room to land.
Three NEW carrier defects, each operator byte-verified in the frozen
hermes_burn.py, each arriving with its own falsifier:

1. turn2_only revision asks re-open forever (210-215): nothing records the
   REVISION already landed, so every cycle appends another turn-2 block.
2. _call re-POSTs the identical body after TimeoutError AND after 4xx
   HTTPError (113-126): a request the server already billed is paid twice
   and only the second response is banked.
3. the plain-empty raise (330-345) skips _bank: the paid pin/pout vanish
   from usage.jsonl and the main total (the refusal path banks; this one
   does not).

## (4) GLM-FLASH: the full defect-list cross-index

4/5. 56 surfaces, ZERO invented (every one literally in the census bytes),
rows-column exact on 52/56 against per-row ground truth, SELF-TOTAL exact.
RECALL-90 missed at 82 pct (56/68): it dropped the proposed-not-yet-existing
surfaces (mag/fetch_util.py, tools/wiring_sweep.py,
tools/standing_task_liveness.py, mag/usage_bank.py) and the bare data-file
names (REGISTRY.jsonl, index_events.jsonl, usage.jsonl), plus mag/scrum.py,
mag/research_fanout.py, mag/scale_salon.py, logs/census_patrol.log, mag.cmd.
Also: glm-5.3-flash on Nous accepted the z.ai recipe (thinking enabled +
reasoning_effort low + uncapped) unmodified, first try.

## Instrument notes (grader honesty)

- The glm grader's first two drafts had instrument bugs I fixed BEFORE
  banking the cell: json|jsonl alternation order truncated .jsonl tokens
  (glm's correct effects.jsonl read as "invented"), and bare server.py vs
  server/server.py double-counted one file. Final rules: longest-first
  extension alternation, brace-group whitespace collapse, bare-name suffix
  collapse (scripts/tmp_grade_unique.py).
- Law 2 freezes (the live surfaces moved DURING staging): the live
  watch/inbox/STEALTH_MINED_FINDINGS.jsonl grew 316 bytes mid-staging
  (245335 -> 245651); frozen copy X2_stealth_findings_frozen.jsonl is the
  triaged truth. tools/hermes_burn.py drifted from the original B1 staging
  sha 9c8a0c1a5637ff82 to 91453258538db098 (same sha cheapgrid1 saw);
  fable's retry cites the frozen copy, contract otherwise byte-identical.
- Outputs: watch/inbox/model_garden/garden-v1-unique-{glm,kimi2,sonnet,fable}.md
- Ledger: memory/runs/model_garden/usage.jsonl (5 new rows incl the kimi-k2.6
  DNF banking nothing).
- Grader + staging scripts kept: scripts/tmp_grade_unique.py,
  scripts/tmp_stage_unique_asks.py, scripts/tmp_land_grid_unique.py.

## The one-line verdicts

- KIMI: window yes (85.5k tokens whole, $0), line numbers no (off-by-9 cite
  shift; re-align before trusting any row cite).
- SONNET: three new real defects on an unseen surface in one ask, $0.16.
- FABLE: the recipe is the cure (0/5 -> 5/5, $0.84); reasoning burn is the
  animal's nature, the floor is the harness's job.
- GLM-FLASH: extraction king confirmed at $0.0016 (0 invented, 82 pct
  recall); feed it only existing surfaces if you want full recall.

Paid most: SONNET - the only ask that returned three new, byte-verified,
promotable defects on material no model had seen, at $0.16.
