# B4 — SRP6 PORTED HOME: THE ACCOUNT SYSTEM v1 (2026-09-30)

Lane: last-mile wave, missing mile #1 (mission: SRP6 proven against mangos realmd in `tools/realmd_client.py` (LW4) but UNPORTED to our own server; MC3 named the v0 auth honest-plaintext). No commit (operator's fence).

The port: the exact handshake that wire-verified against the live CMaNGOS realmd on 2026-09-30 now runs as OUR account system on the line-JSON TCP wire. The math is not re-typed — `server/auth_srp6.py` imports every formula (N/g/k, x, v, B, u, S, K-interleave, M1, M2) from `tools/realmd_client` itself, so the little-endian operand law has ONE source of truth, the one the realmd vectors pin. The login handshake never carries the password; the server stores only salt + verifier; the session key falls out of the exchange; the sid mints from handshake material (K), so it is unforgeable without completing the proof.

## What landed

| File | Change |
|---|---|
| `server/auth_srp6.py` | NEW. `SrpStore` (JSON `{user: {salt, verifier}}`; password touched once at register, never stored) + `Srp6AuthService` (`register` / `begin_challenge` / `verify_proof`): fresh `b` per challenge, M1 compared constant-time over the full 20 bytes (the mangos memcmp over-read edge is NOT ported), M2 + session key + sid on success; pending handshakes are SINGLE-USE, keyed by connection, burned at proof receipt; unknown users get a well-formed DECOY challenge (no enumeration). CLI `python -m server.auth_srp6 <file> add <user>` |
| `server/protocol_table.py` | `SRP6_AUTH_SPEC`/`SRP6_AUTH_TABLE`/`SRP6_AUTH_DIGEST`/`SRP6_AUTH_DISPATCH`: the three verbs as frozen data rows (`srp_register`/`srp_challenge`/`srp_proof`, required_state CONNECTED, handlers `auth_srp_*`); `BAD_PROOF` + `STALE_CHALLENGE` ride the closed reject vocabulary (LW6/LW7 law — no row owns them) |
| `server/protocol.py` | Builders `srp_register`/`srp_challenge`/`srp_proof`/`srp_challenge_ok`/`srp_registered`/`srp_welcome` + wire-shape docstring (integers lowercase hex, little-endian operands everywhere) |
| `server/server.py` | The enforcement point: three new ops in the ladder, each GATED through `SRP6_AUTH_DISPATCH` before its handler (gate before verb); `_grant_session` is the one session-grant path (both doors, one shape); `allow_plaintext_hello` fallback flag (ctor + `--no-plaintext-hello`); `_serve` wires `SrpStore(server/srp_users.json)`; pending handshakes drop with their connection; `stats()` gains `srp_sessions`/`bad_proof`/`stale_challenge` |
| `tests/test_auth_srp6.py` | NEW. 12 tests (below). The CLIENT side of every handshake is `tools.realmd_client.client_session` — the proven math — so a passing roundtrip certifies our server speaks realmd's own dialect |

## The laws

**Register.** `{"op":"srp_register","user","pass"}` → salt (32 bytes, `secrets`) + v = g^x mod N stored; the password crosses the wire exactly once (the enrollment moment SRP6 cannot avoid; mangos pays it via the admin SQL INSERT) and is never stored. Identity+password are uppercased before hashing (mangos law); usernames colon-free (the sha1(I:P) ambiguity law).

**Handshake.** challenge (A) → salt+B reply → proof (M1) → `welcome{sid, m2, auth:"srp6", world, room}`. M1 verified constant-time; M2 returned for the client's mutual check; sid = sha256("srp6-sid:" + user + ":" + K40) — 64-hex, the v0 shape, unique per handshake (fresh b ⇒ fresh K).

**Nonce law (replay).** Pending challenges are single-use and BURN AT RECEIPT (the ReceiptGate idiom): a replayed proof — success-replay or failure-replay — finds no pending and rejects `STALE_CHALLENGE`; replaying the whole challenge+proof pair earns a fresh B, and M1 covers B, so the old proof rejects `BAD_PROOF`. Tapes cannot re-earn a session. A dead connection's pending dies with it.

**No enumeration.** Unknown users get a decoy challenge (deterministic sha256 salt + decoy verifier, byte-shape identical to a real one) whose proof can only reject `BAD_PROOF` — the SAME code as wrong-password, so the wire never reveals whether an account exists. Stronger than mangos (which answers 0x04 UNKNOWN_ACCOUNT at proof); our v0 BAD_AUTH one-code promise does not regress.

**The fallback flag.** `allow_plaintext_hello=True` is the default (the no-regression law: the v0 wire stays byte-identical, `tests/test_server_v0.py` passes untouched); `False` (or `--no-plaintext-hello`) refuses hello with BAD_AUTH and SRP6 is the only door. Flip the default when SRP6 has soaked; the flag IS the fallback.

**Why required_state is CONNECTED.** The auth verbs run pre-auth by definition, so their floor is the lowest rank — the row's reject_code slot is a reserved never-fires slot, exactly the v0 NOT_YOUR_TURN precedent. The dialect's real laws (BAD_PROOF, STALE_CHALLENGE) ride the closed vocabulary and fire in the service layer, the LW6/LW7 shape.

## Named deviations (fix comments carry the receipt)

- **`secrets` for salt and b** — breaks the v0 no-RNG estate law knowingly: SRP6 is broken without unpredictable b (a repeated b replays the session key), and auth.py itself named its clock+counter salts "would NOT be fine for production". The determinism law governs the WORLD LOG (byte-identical replays); auth material never enters the world log.
- **ROOM_FULL check on the SRP6 door** — refused BEFORE the proof is consumed (nothing granted, nothing burned). The SRP6 door lands in the DEFAULT room; room selection on this door is the owed follow-up once rooms + SRP6 have both soaked.

## Concurrent-lane note (byte truth)

B15 (rooms: `server/rooms.py`, GameRoom/RoomBook) landed in `server/server.py` DURING this lane — the shared file changed under me twice. Re-read, re-anchored, no clobber: my SRP handlers merged clean with their room machinery, `_grant_session` gained the room param (both doors walk it), the SRP6 welcome carries B15's `room` key (one welcome shape), and the SRP6 door pays B15's capacity law. Interop verified live: `tests/test_room.py`, `tests/test_innkeeper.py`, `tests/test_room_tags.py` all pass against the merged tree.

## Digests (trust bytes)

- `PROTOCOL_DIGEST d41f7cba635174628cfdff928555de340258ac6f33612dfb84217ff0958179cf` — DEFAULT byte-identical, unmoved (matches LW7's pinned value; `tests/test_protocol_table.py` green).
- `SRP6_AUTH_DIGEST 4981f23ebdda10fb27d8dac23cbe64da1367ff50ad98b19ed9cf52c5f2033556` — a NEW contract version (the X9/LW6/LW7 law; no edit of an old one).
- Siblings, unchanged by this lane: `CHAT_DIGEST 3ce934f5a2ab56623b685f6ec6b7aab830ab05122a2372f92f2296d86b367574`, `ANTICHEAT_DIGEST 5702c4d82dc17aa03720f8c66b94a2ffe206d7e00e9c07a54a99735de68f0bbd`, `MOTION_DIGEST ce259465f063f09dfb3187140c1c0781943be6bebb62c3cc86a13f182c61d637`.

## Tests (real counts, this tree, this moment)

`tests/test_auth_srp6.py`: 12 collected, 12 passed — store laws (salt+verifier, no password on disk, rotation, identity refusal) x2; service math differential vs the proven client; single-use/drop laws; TCP roundtrip (register → handshake → welcome(m2) → boil ack → tick event, stats); wrong-password BAD_PROOF then burn-then-recover; replay x2 (STALE_CHALLENGE + fresh-B BAD_PROOF, no re-earned session); decoy no-enumeration; malformed wire values typed; fallback flag both ways; frozen-rows table law + gate-before-verb.

Full server surface, one command, this tree at this moment: `pytest tests/test_auth_srp6.py tests/test_server_v0.py tests/test_protocol_table.py tests/test_anticheat.py tests/test_chat.py tests/test_realmd_client.py tests/test_room.py tests/test_innkeeper.py tests/test_room_tags.py -q` → **123 passed** (collected = executed, one run, no skips firing).

Out of scope, pre-existing, NOT this lane: `tests/test_server_persist.py` shows 5 failures that reproduce with this lane's edits fully removed (bisected: `git stash` of `server/protocol_table.py` + `server/protocol.py`, `server/auth_srp6.py` moved aside → still 5 failed). The failure traces through `server/world.py` → `mag.water_graph.py`, which another lane has modified in the shared tree ("snapshot row disagrees with replayed state", `server/persistence.py:209`). Named here so the drift is attributable; the owner of that lane owes the heal.

## Owed next (not this lane)

Room selection on the SRP6 door; flip `allow_plaintext_hello` default to False when soaked; session-key use beyond the sid (channel encryption is the SRP6 dividend still uncollected); SRP6 lockout/throttle surface.
