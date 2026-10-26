# W1 PROTOCOL TABLE (2026-09-29)

Mickey17 Wave 1, protocol lane. Implements return 17's improvement: verbs as gated rows, not if/elif code.

## Files

- `server/protocol_table.py` (NEW, 353 lines): schema `protocol_table.v1`. Frozen table of `{verb, required_state, handler_name, reject_code}` rows + enums (`session_states` CONNECTED/AUTHED/TURN_HELD as ordered ranks, `reject_codes`, `transport_reject_codes`) + `compile_table()` (pure, fail-closed `ProtocolSpecError` on 11 malformation classes) + `ProtocolDispatch` (the gate) + `validate()`/`state_for_sid()` (world-shape contract, swap-in ready).
- `server/protocol.py` (EDIT, additive): `VERBS`, `REJECT_CODES`, `TRANSPORT_REJECT_CODES` are now re-exported from the table. Values and order byte-identical to v0; all builders, `encode`/`decode_line`, `MAX_LINE` untouched. Consumers verified before edit: `server/world.py`, `server/server.py`, `server/__init__.py`, `tests/test_server_v0.py`.
- `tests/test_protocol_table.py` (NEW).

## The digest decision

`protocol_digest = sha256(canonical_json({schema, session_states, reject_codes, transport_reject_codes, rows}))` with `sort_keys=True, separators=(",",":")`, utf-8: the same canonicalization law as `world.row_sha` and `wow_bones.bones_digest`. The digest excludes itself, so it is a pure function of the table bytes; row order is semantic (it fixes the VERBS tuple order), so reordering moves it. Pinned v0 value:

```
d41f7cba635174628cfdff928555de340258ac6f33612dfb84217ff0958179cf
```

Sessions bind to this as a hashable contract version. Any verb, state, or reject edit is a version bump by construction.

## The Dispatch decision

Reimplemented minimal in the wow_bones.Dispatch SHAPE, not by import. Justification: `wow_bones.Dispatch` speaks the WoW refusal vocabulary (UNKNOWN_OPCODE/STATUS_MISMATCH/STATUS_NEVER/STATUS_UNHANDLED), has no per-row `reject_code` column, and eats the `bones.json` fixture envelope; adapting would need a translation shim thicker than the kernel plus a mag-fixture coupling in the wire layer. Kept verbatim and pinned by a shape-equivalence test against `mag.wow_bones.Dispatch` itself: `dispatch(verb, state) -> {ok, reason, handler_ran}`, gate-before-verb ordering law, `handler_ran` False on every refusal, calls log grows only on pass.

## NOT_YOUR_TURN machinery

A `required_state` rank column. All v0 rows require AUTHED and reject with UNKNOWN_SID (an unauthed ask carries a sid the world never issued: what the wire already said). A compiled row with `required_state: TURN_HELD, reject_code: NOT_YOUR_TURN` fires the reserved code; the default table has none, so v0 still never emits it (test sweeps every verb x every state).

## Tests (real counts)

- `pytest tests/test_protocol_table.py -q`: **25 passed** (incl. 11 fail-closed parametrize cases).
- `pytest tests/test_server_v0.py -q`: **15 passed** (in-flight surface unbroken, demo subprocess included).

## v1 notes (other lanes' ownership)

`server/world.py.validate`'s if/elif ladder and `server/server.py`'s op routing were NOT touched (lane boundary). Wiring them to `ProtocolDispatch.validate`/`state_for_sid` is a one-line swap each, proven contract-compatible here. `handler_name` values (`world_boil`/`world_valve`/`world_join`/`world_tag`) name the `_apply` branches in `server/world.py:215` as the binding point.

Laws kept: em-dash count in the three authored files: 0. No git commit.
