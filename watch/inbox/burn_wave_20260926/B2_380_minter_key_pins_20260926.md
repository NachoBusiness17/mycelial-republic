# B2-380 pin the fold minters' key sets against the registry 2026-09-26

## Verdict

LANDED. Two pins in tests/test_index_fold_host.py (test_add_minter_keys_are_registered, test_invalidate_minter_keys_are_registered) run the REAL fold script via the file's _run/_mk_inbox helpers, execute an add and an invalidate, read the appended event rows from the events log, and assert every emitted top-level key is a subset of the configs/events_key_schema.json closed vocabulary. The pre-registered falsifier was fired live: injecting `ev.probe = 1` into the add minter made test_add_minter_keys_are_registered FAIL naming the unregistered key; reverting the injection returned both pins green. The unknown-key appendOp path now has a tripwire that names the minter instead of never firing.

## Evidence file:line quotes

- scripts/index_fold_host.mjs add arm (pre-injection, line ~738): `appendOp(ev);` minting {seq, ts, op, file, sha256, class, purpose, writer, nonce, [living, size, seal]}; invalidate arm (~762): {seq, ts, op, file, reason, writer, nonce}.
- configs/events_key_schema.json keys[]: closed vocabulary including seq, ts, op, file, sha256, class, purpose, writer, nonce, reason, living, size, seal, ... (30 registered keys).
- Falsifier transcript: probe injected -> "1 failed" (test_add_minter_keys_are_registered asserts not unknown with the unregistered key names in the message); probe reverted (grep ev.probe count 0) -> minter pins 2 passed; total file state 4 failed / 23 passed where the 4 failures are the pre-existing B2-342/343 lane in-flight work that failed identically before this lane's first edit (observed in the B2-486 refold run before any B2-380 edit).

## Work done

1. Claim law: tests/test_index_fold_host.py is untracked (B2-342/147 lanes), CLAIM B2-380 (21:36:13Z) before the append; existing pins untouched.
2. Appended _schema_keys() + the two minter pins using the file's own subprocess helpers.
3. Falsifier executed live: injected ev.probe = 1 into the add minter, pin failed naming it; reverted byte-exact; full pin run returned to the pre-lane state (same 4 pre-existing failures, none mine).
4. Registered receipt + LEDGER row; board flip.

## Falsifier

Dies if: (a) a minter emits ev.probe (or any unregistered key) and the pins pass; (b) the schema registry gains a key and the pins do not track it via the same file (the pins read the registry file, not a copy, so drift is impossible without editing both); (c) a NEW minter (e.g. a third CLI op) lands with unregistered keys and no pin covers it (extend the pins with the third op in the same landing as the minter).

## Bibliography closed

Read whole: scripts/index_fold_host.mjs (add/invalidate minters, appendOp, writer guard), configs/events_key_schema.json (vocabulary + census + drift note), tests/test_index_fold_host.py (helpers + existing pins). Bytes: falsifier injection/revert observed live; 2/2 minter pins green on the reverted tree. Nothing synthesized.
