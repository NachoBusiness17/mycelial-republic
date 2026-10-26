# LW7 — ANTI-CHEAT V1: RATE_CAP + STALE_NONCE + THE GWAP DISPUTE CALL SITE (2026-09-30)

Lane: last-mile wave (S20's design, `watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md` S20; compounds DAY_SYNTHESIS_20260929 T4 "anti-cheat v1"). No commit (operator's fence).

S20's diagnosis, verbatim from the ledger: server-authoritative water kills position/velocity cheats BY CONSTRUCTION; the real surfaces are action spam (the demo logged 30 tags/30 ticks from one client), replay abuse (winning tapes re-earning credit), and collusion. This lane lands the first two as executable law and stubs the third's call site.

## What landed

| File | Change |
|---|---|
| `server/protocol_table.py` | `ANTICHEAT_SPEC`/`ANTICHEAT_TABLE`/`ANTICHEAT_DIGEST` (DEFAULT rows + `RATE_CAP`,`STALE_NONCE` in the closed vocabulary) and `ReceiptGate` — the executable law (`admit_nonce` / `admit_cap` / `commit`, `NO_NONCE` sentinel) |
| `server/server.py` | The enforcement point: `_admit_action` (nonce law → world validation → rate cap → stage), `_route_tag_dispute` (the GWAP stub), `anticheat_rejects` + `tag_disputes` state, new `stats()` keys, demo nonce dogfood |
| `tests/test_anticheat.py` | NEW. 14 tests: table contract, gate unit laws, cap-on-second-action, never-stages, first-action-per-tick, per-sid budgets, DRY_POOL-does-not-spend, replay rejected, tape-cannot-re-earn, burn-at-receipt, malformed-id-no-bind, legacy nonce-less, dispute routing x2 |
| `tests/test_server_v0.py` | One test adjusted to the law (see below); every other line untouched |

## The laws

**RATE_CAP (spam).** Per-sid, per-tick staged-action budget of 1. The tick bucket is the tick the action would apply at (`world.tick_count + 1` — the receipt window between ticks). A second action in the same bucket rejects `RATE_CAP` at receipt and never stages. Only an ACK spends the budget: a world-rejected action (DRY_POOL, BAD_TEXT) leaves it untouched. Whisper (LW6) acks outside the tick but an ack is an ack — it spends the window. The FIRST action of every tick is always legal; budgets are per-sid.

**STALE_NONCE (replay).** Per-session monotonic action ids: the client includes `"n"` in each action. First id BINDS the session; afterwards every action must carry `type(n) is int` (bools are verdicts, not ids — the X9 u8 law) strictly above the high-water. Ids BURN AT RECEIPT, not at staging: a rate-capped or world-rejected action still spends its id. A bound session can never go nonce-less (tape-n-stripping foreclosed). Replayed/lower/equal/malformed ids reject `STALE_NONCE` at receipt. Tapes verify (the hash-chained world log still holds) but cannot re-earn: every taped id sits at or below the high-water, so a verbatim replay stages nothing.

**Why the codes ride the vocabulary, not rows.** A second action in a tick is illegal whichever verb it carries; a replayed id is stale on every verb alike. No row may own these laws. Enforced ordering at the receipt point: nonce law → world validation → rate cap → stage. Semantic rejects keep their codes (LW6's `BAD_TEXT` still beats the cap — proven by `tests/test_chat.py` passing untouched).

**GWAP dispute stub.** `"dispute": true` on a tag routes through the agreement engine (`mag/gwap_payload`, real calls: `agreement_score` + `decide_verdict`): the tagger's claim is the intent side, the cop report is OWED, so a fresh dispute scores 0.0 and verdicts DISPUTE — the row a judge queue consumes (`server.tag_disputes`, `stats()["tag_disputes"]`, `ack["gwap"]`). The dispute routes, it does not veto: the tag still applies. Only staging tags route (a DRY_POOL tag or a disputed boil does not). Round machinery — participants, ed25519 signatures, SessionLedger, collusion fingerprint (needs the independent author) — is the owed next lane.

## The one existing test the law moved

`tests/test_server_v0.py::test_join_tag_and_valve_apply_at_tick` staged join+tag+valve from ONE sid in ONE tick — three budget slots. It now rides three sids (all "ben": events carry the USER, the budget is per-SID), so what it proves is unchanged: the three verbs apply at the same tick, in arrival order, with identical events and physics. No other test in the repo needed touching; LW6's chat suite passes byte-untouched.

## Concurrent-lane note (byte truth)

LW6 (chat) landed `server/world.py` say/whisper + `CHAT_TABLE` in the shared working tree DURING this lane (one edit collided mid-flight; re-read, re-anchored, no clobber). `server/server.py` itself was untouched by LW6 (their receipt names server.py as the next fence). Interop verified live: `pytest tests/test_chat.py` 17/17 against the anticheat ladder.

## Digests (trust bytes)

- `PROTOCOL_DIGEST d41f7cba635174628cfdff928555de340258ac6f33612dfb84217ff0958179cf` — DEFAULT byte-identical, unmoved (pinned by `tests/test_protocol_table.py`).
- `ANTICHEAT_DIGEST 5702c4d82dc17aa03720f8c66b94a2ffe206d7e00e9c07a54a99735de68f0bbd` — a NEW contract version (the X9/LW6 law; no edit of an old one).
- Siblings, unchanged by this lane: `CHAT_DIGEST 3ce934f5...`, `MOTION_DIGEST ce259465...`.

## Tests (real counts, this tree, this moment)

- `pytest tests/test_anticheat.py -q` → **14 passed** (1.82s)
- `pytest tests/test_server_v0.py tests/test_chat.py tests/test_protocol_table.py tests/test_motion_rows.py tests/test_verdict_feed.py tests/test_room.py tests/test_anticheat.py -q` → **141 passed** (10.55s)
- All twelve server-importing suites (adding gods_number, healthz_status, ledger_registry, legality_dataset, chain_contract) → **158 passed, 1 failed, 3 errors** (25.58s); `tests/test_server_persist.py` (a sibling lane's suite, mid-landing during my run) → **7 passed** at the settled tree.
- FULL SUITE `pytest -q --ignore=tests/test_behavioral_awareness.py` (run 05:20-06:05, mid-wave with siblings landing concurrently): **10 failed, 3108 passed, 12 skipped, 3 errors in 2692.60s**. Attribution of every red I could reproduce at the settled tree (census-denominator law: name instrument, moment, delta — the tree moved underneath this run):
  - `test_healthz_status` (1 failed + 3 errors): expects `server.app`, an attribute no commit of `server/__init__.py` ever defined. Pre-existing, owed by the dashboard-health lane; outside LW7's effect path.
  - `test_gods_number::test_mountain_gods_number_golden`: BFS golden 339,840 vs 183,360. Tool and golden both last touched in 579109f44; the water physics moved after it (X3 "water weld", f8452e01a) and LW6 added chat verbs to `world.validate`. LW7 touched no verb, board, or physics byte — `PROTOCOL_DIGEST`/`CHAT_DIGEST` compile byte-identical with and without my edit (proof in the digests section) — so this drift is the physics/chat lanes' debt, not LW7's.
  - `tests/test_behavioral_awareness.py`: excluded — unresolved merge conflict (UU, SyntaxError), another lane's pre-existing state.
  - The remaining visible failures (`test_server_persist` x3 in that run's tail) belong to a suite that was landing mid-run and passes 7/7 at the settled tree.
- Demo (nonce dogfood live, first nonce-bearing client): `python -m server.server --demo --tick-ms 20 --ticks 30` → WIN at tick 4, `rate_capped: 0, stale_nonce: 0` — one action per sid per tick is the demo's existing shape, so the cap costs it nothing.

## Commit note (byte truth)

This lane made NO commit (the mission's fence). The coordinator's wave commits (ff1c02822 and after, "40+ lanes landed") swept the shared working tree — including this lane's files — while the full suite was running; `git status` shows zero dirty server/ files at close. The bytes on disk are the bytes tested above.

## Owed (named, not hidden)

1. The GWAP round machinery behind the stub: cop report intake, participants, signatures, `SessionLedger` rows, collusion fingerprint — the judge queue S20 priced as adversarial audit.
2. Whisper server-side routing to the client outbox queue (LW6's named next lane, not mine).
3. Nonce persistence across server restarts (v1 ids are per-session in memory; the world log is the durable witness — replay across a restart needs the ledger binding).
