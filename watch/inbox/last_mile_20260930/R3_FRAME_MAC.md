# R3 — FRAME MACs: POST-AUTH INTEGRITY ON THE LINE-JSON WIRE (2026-09-30)

Lane: last-mile wave, the frontier's top security kill (mission: V2ASK1 verdict landed at `watch/inbox/frontier_asks/volley2/results/V2ASK1.md`; Q03 "frame integrity"). No commit (operator's fence).

The kill: post-auth frames carried no integrity — the `sid` field inside the JSON was the ONLY thing binding a move to its author, so one flipped byte on the wire reattributed a forged move to a real identity. Now every frame after a successful `srp_proof` carries a K-derived HMAC the server verifies BEFORE any op runs. Without K the attacker cannot produce an accepted tag; attribution stops being a claimable field and becomes a provable property.

## What landed

| File | Change |
|---|---|
| `server/frame_mac.py` | NEW. `derive`/`derive_from_wire` (HKDF per RFC 5869 over HMAC-SHA256, V2ASK1 formulas verbatim: `prk = HMAC(SHA256(A_le‖B_le), K)`; expands `k_c2s`/`k_s2c`/`mac_id` under `"mesh-frame-v1 …"` infos); `seal`/`check`/`compute_tag`/`frame_body` (tag = `HMAC(k_dir, "mac1-v1 " ‖ dir ‖ 0x00 ‖ canonical body)[:16]`; body = frame minus its own `mac` field, the `world.row_sha` law); `FrameMacState` (expected c2s seq, s2c seq, sticky `mac_mode`, `integrity` view); `FRAME_MAC_TABLE` (BAD_MAC rides a NEW contract version's transport vocabulary). CLI self-check `python -m server.frame_mac` |
| `server/protocol.py` | The wire law in the docstring (spec-first: the doc owns the behavior) + `with_mac(msg, keys, seq)` builder + `MAC_SEQ_FIELD`/`MAC_FIELD` constants |
| `server/server.py` | The enforcement point: `require_frame_mac` flag (ctor + `--require-frame-mac`, default False = migration window); `srp_challenge` stashes the handshake publics (wire hex A/B); `srp_proof` success arms `peer["mac_state"]` (keys derive from the SAME (K, A, B) the client holds); the read loop gains the gate at decode → MAC → op-ladder order; `_on_mac_tamper` = one `kind:mac_tamper` row in the room world's hash chain (the whisper precedent: receipt-time audit row outside the tick, no clock/RNG) then disconnect; `_reply` seals direct replies s2c; `stats()` gains `mac_sessions`/`mac_tampers` |
| `tests/test_frame_mac.py` | NEW. 16 tests. The client side derives keys from the same handshake `tools.realmd_client.client_session` computed, so a passing roundtrip certifies both ends agree on K-derived material byte for byte |

## The laws

**Verify before processing.** Gate order on an armed session is decode → MAC → nonce gate → world. Proven by test: a replayed sealed action (whose `n` would alone reject STALE_NONCE) rejects **BAD_MAC** — the MAC gate demonstrably ran first.

**Tamper = disconnect + chain event.** Bad tag, replayed/gapped seq, malformed mac field, bare frame after sticky (downgrade strip), or bare frame under the flag — all one code `BAD_MAC` (which check failed is not the attacker's business), one `kind:mac_tamper` row (`user`, `sid`, `peer`, `code`, `integrity`, current `tick`; chain stays verifiable; row is durable on disk), then the connection dies. Never resync, never downgrade within a session.

**Seq law.** Per-direction counters from 0; `seq` lives INSIDE the MACed body, so an old frame cannot be retagged with a new seq; constant-time compare (`hmac.compare_digest`); `type(seq) is int` (a bool is a verdict, not a sequence number — the X9/LW7 law).

**Migration, not breakage.** `require_frame_mac=False` (default): an old SRP6 client that never sends `mac` fields keeps working byte-compat (integrity `"none"` — the chain records what it cannot see, the spec's laundering fix); frames that DO carry a mac are verified and a bad one is tamper regardless of the flag. `True`: the first bare frame after proof is tamper. The plaintext hello door carries no K and stays bare either way (byte-identical v0 welcome, pinned by test).

**Direction and session binding.** `dir` is in the MAC (reflection: a sealed welcome fed back rejects); keys are per-handshake (fresh `b` ⇒ fresh K ⇒ fresh keys — splice across sessions rejects).

## Named deviations from the V2ASK1 wire format (the mission chose the hmac-field-in-JSON shape; deviations follow the estate naming law)

- **Canonical body, not exact transmitted bytes.** An in-JSON field cannot contain a tag over the bytes that contain it, so the tag covers the decoded frame recanonicalized in the house form (sorted keys, compact). The parse-differential class the spec warned about is bounded by `protocol.encode` being the only producer on this wire.
- **Hex tag, not base64url** (32 lowercase hex chars = the spec's 16 tag bytes) — the SRP6 material convention.
- **No caps/caps_tag negotiation.** The sealed welcome (s2c seq 0) IS the capability announcement; the first valid MAC-bearing client frame (c2s seq 0) is the opt-in (the spec's sticky rule).
- **Broadcast ticks stay bare.** Encode-once fan-out is the determinism law (`rooms.broadcast`); s2c sealing covers direct replies only. Full s2c broadcast sealing is owed to the TLS-phase lane (V2ASK1 Phase 2), as is the GDScript client port (`client/net/frame_mac.gd`) with the F3.5 cross-language vector table.

## Concurrent-lane note (byte truth)

R5 (RFC 5054 dialects in `server/auth_srp6.py`) landed STAGED mid-lane: the module changed under me after my first read. My surface is dialect-agnostic — it keys on the wire hex A/B and the session key, identical on both ends whatever math minted them — so no rework was needed; my tests register accounts under the mangos-256 compat dialect because the handshake is driven by the proven realmd client math (R5's own differential path). R5's test-file update has NOT landed: `tests/test_auth_srp6.py` on disk still calls `register(salt_le=…)` and fails 10/12 against their staged module — pre-existing, their fence, not touched by me. R8 (int-domain in `mag/water_graph.py`, staged) rides the same standing 5 `tests/test_server_persist.py` failures B4's receipt already attributed to the physics lane. One operational hazard named: `.git/index.lock` is held intermittently by sibling lanes — git stash during this window fails; I proved my non-involvement by import graph instead (the persist tests import only `server.persistence` + `server.world`, neither mine).

## Digests (trust bytes)

- `PROTOCOL_DIGEST d41f7cba635174628cfdff928555de340258ac6f33612dfb84217ff0958179cf` — DEFAULT byte-identical, unmoved (matches B4's pinned value; `tests/test_protocol_table.py` green).
- `FRAME_MAC_DIGEST f3b3e79a1af50d75e1112bd87582c79602847484ce5c1398336c335f16f90917` — a NEW contract version (the X9/LW6/LW7/B4 law; no edit of an old one).
- Siblings, unchanged by this lane: `SRP6_AUTH_DIGEST 4981f23ebdda10fb27d8dac23cbe64da1367ff50ad98b19ed9cf52c5f2033556`, `CHAT_DIGEST 3ce934f5a2ab56623b685f6ec6b7aab830ab05122a2372f92f2296d86b367574`, `ANTICHEAT_DIGEST 5702c4d82dc17aa03720f8c66b94a2ffe206d7e00e9c07a54a99735de68f0bbd`.

## Tests (real counts, this tree, this moment)

`tests/test_frame_mac.py`: 16 collected (`--collect-only -q`), 16 passed (`pytest -q`, one run) — unit: derive determinism/directionality/session-uniqueness, exhaustive single-bit body flips (every byte × every bit) + every tag-hex flip + field-level forgeries, reflection, cross-session splice, seq gap/shape laws, admit migration/sticky/flag matrix, table law, `with_mac` sugar; wire: sealed roundtrip (welcome verified s2c, two sealed actions ack across a pumped tick, bare broadcast tick, BAD_JSON still fires below the gate), flipped-byte tamper (BAD_MAC + disconnect + chained `mac_tamper` row, durable on disk), replay (BAD_MAC beats STALE_NONCE — gate-order proof), reflection over the wire, no-MAC client on the flag path both ways, sticky no-downgrade, hello door stays bare.

Adjacent surface, one command, this tree at this moment: `pytest tests/test_server_v0.py tests/test_protocol_table.py tests/test_anticheat.py tests/test_chat.py tests/test_cast_server.py tests/test_identity_binding.py -q` → **115 passed**. Demo verified live: `python -m server.server --demo --ticks 12` → WIN at tick 4, exit 0, stats carrying `mac_sessions`/`mac_tampers`.

Out of scope, pre-existing, NOT this lane: `tests/test_auth_srp6.py` 10 failed (R5's staged module vs their not-yet-landed test rewrite); `tests/test_server_persist.py` 5 failed (R8's staged `mag/water_graph.py`; the same 5 B4's receipt attributed to the physics lane). Both reproduce with this lane's files outside their import graph.

## Owed next (not this lane)

GDScript client port + F3.5 cross-language vectors; s2c broadcast sealing (TLS phase, with pinned TLS per V2ASK1 Q04); a re-login's fresh state re-arming counters needs a Godot-side client law note; flip `require_frame_mac` default when MAC-bearing clients have soaked.
