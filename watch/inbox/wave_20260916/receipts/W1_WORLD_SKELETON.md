# W1_WORLD_SKELETON — receipt (appended as I go)

- **Lane:** wave_20260916 / W1
- **Date:** 2026-09-16
- **Operator:** (to review at end)
- **Worker split:** union-alpha (stealth, OpenRouter, key via `mag.flight_recorder.load_env`, never printed) drafts → editor (this session) verifies every self-check, per U3 law.
- **Budget:** $0 target.

## Mission

Build `mag/wow_world.py` — the bones-world skeleton (blueprint M0):
- Rooms are **legality tables**: `{id, name, verbs_allowed, exits: {direction: room_id}, encounters: [boss_id]}`.
- Verbs dispatch through the **existing** `mag/wow_bones.py` Dispatch gate — gate is reused, never duplicated.
- Session = `BonesSession` extended with a `room` pointer + `go <direction>` verb routed through the SAME dispatch law; locked/missing exit = **typed refusal, never silent**; movement costs no draws; encounters inherit the existing DONE guard.
- Every session is a replayable receipt.

## Steps (live log)

- [x] Receipt opened FIRST (this file).
- [ ] Read `watch/inbox/WOW_CLONE_BETA_BLUEPRINT_20260916.md` (M0).
- [ ] Read `mag/wow_bones.py` + `mag/wow_bones_session.py` (reuse kernels verbatim).
- [ ] Design contract.
- [ ] union-alpha draft (prompted with exact module contract).
- [ ] Editor pass on draft (verify all claimed self-checks).
- [ ] Tests: determinism (byte-identical receipt), illegal exit → typed refusal `handler_ran=False`, graph traversal, receipt schema keys.
- [ ] pytest run (real numbers filed).

## Editor pass — union-alpha draft verification (worker law: verify every self-check)

Draft landed on attempt 4 of the second backoff loop (first loop: 5x upstream 429; the pool
was degraded for ~15 min). 12,805 chars, finish=stop, prompt 3174 + completion 3460 tokens,
**cost $0**. Draft kept verbatim at
`watch/inbox/wave_20260916/drafts/W1_union_alpha_draft.py`; contract at `W1_contract.md`.

What UA got RIGHT (verified, not trusted): the `VERB@ROOM:<id>` row scheme with room-as-status;
locked exit → STATUS_NEVER row; refusal short-circuit with only turn_count + move record
changed; movement branch that draws nothing; load-on-first-room-verb with the Instance kernel;
DONE attempted only when IN_PROGRESS with `world_boss_alive` passed through (the inherited
guard); receipt keys + sha256 over canonical body; world-digest resume guard; stream index
restore. Its exit resolution was case-robust where the editor's first cut was not (caught by
the traversal test — the editor's own bug, fixed with a loud KeyError tripwire).

DEFECTS found in the draft (all fixed in the merged `mag/wow_world.py`):

1. **Fenced output** — module filed wrapped in a literal ```python fence; not importable as-is.
2. **`verb_name.startswith("GO_")` movement predicate** — a room verb like `gossip` (GOSSIP)
   matches `GO_` and the turn loop dies in StopIteration. CONFESSION: the editor's contract
   specified this exact predicate; UA executed the contract faithfully — the bug is
   contract-authored, caught in verification anyway. Final law: movement is
   `verb == "go" and arg`, never a name-prefix guess.
3. **First-turn movement skipped promotion** (movement branch first, promotion as elif) —
   contract-conformant but violates the bones lifecycle law ("the first successful AUTHED verb
   promotes"). Final: promotion always fires on first success; the promoting non-movement verb
   is consumed by promotion; movement always applies and still draws nothing.
4. **CLI contract violations**: `--seed` typed `int, required` (breaks string seeds and the
   bones default — `start --seed t-cli` crashes); refused turns exit 1 (a typed refusal is an
   answer, not an error — bones law: refusal is typed and the caller carries on);
   `UNKNOWN_SESSION` renamed; `map` dropped `encounters`. Final: bones-style flat parser,
   string seed with default, exit 0 on refusals.
5. Minor: `seed: int` type hint, thin docstring, `super().receipt()` computed then discarded.
   Adopted from the draft: `_write_json` helper, defensive `list()` copies in save/receipt.

**union-alpha grade: B.** High structural fidelity to the contract; deterministic core; the
gate genuinely reused, not duplicated. Docked for the CLI violations and the movement
predicate trap (both would have failed the module's own falsifiers), and it wrote no
self-checks at all — so unlike U3, nothing lied; it just left the lying to chance.

## Test output (verbatim)

```
............                                                             [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\discord\player.py:30
  C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Lib\site-packages\discord\player.py:30
    DeprecationWarning: 'audioop' is deprecated and slated for removal in Python 3.13
    import audioop

.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Lib\site-packages\fastapi\testclient.py:1
    StarletteDeprecationWarning: Using `httpx` with `starlette` is deprecated...
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
12 passed, 1457 deselected, 2 warnings in 2.33s
```

(`.venv\Scripts\python.exe -m pytest tests -q -k wow_world`; the 12 = the whole of
`tests/test_wow_world.py`: determinism, cross-process splice, missing/locked/unknown-verb
typed refusals with handler_ran False, no-draw traversal, promote→load→DONE arc, world-boss
EXHAUSTED guard, receipt schema + self-hash, world-digest binding, CLI smoke.)

**Cross-process replay falsifier (stronger than in-process):** the full route
(look, go north, go east, look, look x4) played twice through the CLI in two separate
interpreter processes — receipt files diff clean:

```
CROSS-PROCESS REPLAY: BYTE-IDENTICAL
verdict: COMPLETE | encounter: DONE | draws: 3 | room: vault | sha256: 2ab96b827a06e8b79355...
```

Full-suite census: see appendix line below (job was still running when this section was
written; appended on completion).

### Full-suite census (real numbers, trust bytes)

```
32 failed, 1427 passed, 9 skipped, 6 warnings, 1 error in 911.39s (0:15:11)
```

(`.venv\Scripts\python.exe -m pytest tests -q`, full collection.) The 32 failures + 1 error
were then re-listed individually (`--lf`): **none are in `tests/test_wow_world.py` (12/12
green) and none are in the wow bones/session/family/manifest tests.** They are pre-existing
failures in unrelated subsystems — test_water_computer (5), test_desk_baseline_probe (6),
test_process_supervisor (3), test_falsifier_ledger (2), test_quota_billable (2),
test_organ_map (2), test_wave_driver, test_spore_seed (+1 setup error), test_substrate_identity,
test_voice_shadow, test_voice_turn, test_healthz_status, test_mirror_intro, test_no_win,
test_pack_modes_steward, test_seat_registry, test_all_seat_interaction, test_repack_integration
— consistent with the 2026-09-14 census (1305 passed / 34 failed / 9 skipped). W1 added 12
passing tests and regressed nothing.

## THE ONE DESIGN DECISION MADE ALONE (flagged for the operator)

**When the encounter LOADS, and what a draw means outside the boss room.** The bones law
("first LOGGEDIN verb loads boss 0 unconditionally") would load the boss in any room and make
the room table's `encounters` data decorative. The naive fix (load only in encounter rooms,
draw everywhere) opens the Instance kernel's TO_BE_DECIDED shortcut: three draws anywhere
would slip a DONE through as a "load", bypassing the guarded transition — a silent wrong-law.
Chosen law for the world: **the boss loads on the first successful non-movement verb in a room
whose `encounters` lists it; DONE is attempted only while the boss is IN_PROGRESS; movement
never draws and never loads.** Every DONE is therefore a guarded transition, the room table is
load-bearing, and the falsifiers hold. If the operator wants draws to tick world-wide (bones
verbatim), it is a two-line change — but it should be a decision, not a drift.

## Provenance / cost

- union-alpha via OpenRouter `stealth/union-alpha`, key loaded by `mag.flight_recorder.load_env`,
  never printed, $0.00 (usage: 3174 prompt + 3460 completion tokens; two 429 waves before the
  pool admitted the job — attempts filed in `W1_union_alpha_meta.json`).
- Editor seat: contract, tests, merge, falsifiers. No git commands. Session + receipt files in
  `memory/runs/wow_world/` are the only runtime writes.

## Findings / decisions log (early design notes)

- **Blueprint M0 confirmed** (`WOW_CLONE_BETA_BLUEPRINT_20260916.md`): falsifier = same seed +
  same moves → byte-identical receipt. UA self-checks unreliable (grade B, wrong-signed checks).
- **Kernels read.** `Dispatch` is fully data-driven (row table + enums) → the world rides the
  SAME class with a world-derived table; zero gate logic duplicated. `Instance` DONE guard and
  `Stream` indexed draws are reused verbatim. `BonesSession` is subclassed, not copied.
- **KEY FINDING (would have been the trap):** `Dispatch.rows` is keyed by verb NAME only.
  A per-room table collides (`GO_NORTH` exists in several rooms; last room wins — a silent
  wrong-law). Fix in contract: every door/verb row is unique as `VERB@ROOM:<id>` with
  `status = ROOM:<id>` ("a room is a status, a door is a legality row" — blueprint's own words).
  Refusal mapping stays pure gate vocabulary: missing exit → `UNKNOWN_OPCODE`, locked exit
  (exit value `{"room":…, "locked":true}`) → `STATUS_NEVER`, both `handler_ran=False`.
- **Design decision made alone (flagged for operator):** when the boss LOADS. The bones law
  ("first LOGGEDIN verb loads boss 0 unconditionally") would fire in any room and make the
  room `encounters` data decorative; a naive room-conditional load instead opens the
  Instance kernel's TO_BE_DECIDED shortcut (a 3-draw DONE can slip in as a "load" while
  never engaged). Chosen law: load happens on the first successful *room verb* (non-movement)
  in a room whose `encounters` lists boss 0; DONE is attempted only when the boss is actually
  IN_PROGRESS. Movement never draws and never loads. This keeps every DONE a guarded
  transition and makes the room table load-bearing.
- **Receipt contract:** schema stays `wow_session.v1` (blueprint law), extended with
  `world`, `world_sha256_12`, `room`, `route`; save-state is `wow_world_session.v1`;
  sessions bind `world_sha256_12` so a world-table edit invalidates old sessions (resume
  refuses rather than replays against a different world).
- **Default world `atrium-ring`:** 5 rooms, one encounter room (vault, boss 0), one locked
  door (torch_hall west → ash_gallery). Winning line = 7 turns (≤ TURN_LIMIT 8).
