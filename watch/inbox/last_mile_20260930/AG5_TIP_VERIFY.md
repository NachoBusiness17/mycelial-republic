# AG5 — TIP VERIFY (audit finding #3) · 2026-09-30

**Lane:** last_mile AG5 · **Files:** `mag/verkle_knot.py`, `mag/context_pack.py`, `mag/hermes_warm_boot.py` + `tests/test_ag5_tip_verify.py` (new, 13 tests)
**Law kept:** the chain file itself was NOT rewritten by this lane — only the tip pointer writes, launch-path reads, and field names changed.

## A — main-path tip writes are atomic now

`_append_verkle_knot_unlocked` wrote the tip with plain `TIP.write_text` at the main append (old L753) and inside the CHAIN_RACE_REPAIR heal branch (old L792) while `_write_tip_atomic` (tmp + `os.replace`, L587) existed for exactly the torn-write disease documented at the consolidate call (old L375-377). Both writes now go through `_write_tip_atomic`. Pinned by monkeypatch spies: `test_append_path_writes_tip_atomically` (spy called once, tip on disk matches returned root) and `test_heal_path_writes_tip_atomically` (poisoned append root + forced post-append verify failure drives the heal; spy called twice, healed tip = recomputed-from-disk root, not the poisoned one).

## B — launch path verifies the chain

`context_pack.build_context_pack` rendered the tip badge as a raw read (old L746-767). New `_verify_tip_chain(timeout_s=2.0)` runs `mag.verkle_knot._verify_chain_consistent` on a daemon thread: tamper → `(False, reason)`; raise → `(False, "verify raised: …")`; >2s → `(False, "verify timeout >2s")`. Boot is never blocked. The badge carries `verified` + `verify_reason`; `format_context_pack_text` and `format_agent_preamble` render **`tip: UNVERIFIED (<reason>)`** when the verdict is False (the confident root/leaves badge is suppressed on that line). Tests: UNVERIFIED render, normal render, preamble, tamper-flag, clean-pass, timeout, raise, and badge-carries-verdict on a live pack build.

## C — hermes_warm_boot field names + real --verify

`_chain_tip` reported keys `leaves`/`tag` that chain rows never carry (rows use `n_leaves`/`dominant_theme`) — live `memory/warm_state.json` proved it (`"leaves": ""`). Fixed to `n_leaves`/`dominant_theme` (AG5 docstring names the cause). `--verify` used to echo a flag; `warm_boot(verify=True)` now calls `_verify_chain_consistent` into `state["chain_verify"]`, `main()` prints it and exits 1 on a failed verify.

## Evidence

- `pytest tests/test_ag5_tip_verify.py -q` → **13 passed** (2026-09-30)
- `pytest tests/ -q -k "verkle or context_pack or ag5"` → **83 passed, 0 failed** (2026-09-30)
- Live: `python -m mag.hermes_warm_boot --verify` → `chain_verify: ok=True reason=chain consistent (8645 leaves)`, exit 0
- Live: janitor pack badge `verified: True | chain consistent (8645 leaves)`; tip line renders the normal badge
