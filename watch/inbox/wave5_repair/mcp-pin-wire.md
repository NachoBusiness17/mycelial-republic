# mcp-pin-wire: the dormant rug-pull gate is wired and fires

Lane: gala wave5-repair mcp-pin-wire (division B) | Banked: 2026-09-29
Owed work: `tools/mcp_pin.py check_drift` had ZERO code callers (banked as gap 1 in
`watch/inbox/burn_reset_20260927/flash50/mcp-security.md` "the rug-pull gate exists but
nothing charges it", and as the class-W wiring truth in
`watch/inbox/burn_reset_20260927/flash50/w4-41.md` section 2: "The sentence 'check_drift
detects descriptor drift' is a theorem of the module. The sentence 'the estate detects
MCP tool drift at connect time' is false"). It is now wired at every MCP connect surface,
fails loud on drift, and a test proves the wire fires.

## What changed (3 files edited, 1 file added; `tools/mcp_pin.py` itself UNTOUCHED)

1. `mag/mcp_server.py` (the connect-site file chosen, the ask's first option):
   - `pin_ledger_path()` (mag/mcp_server.py:259): resolves the gate ledger.
     `MAG_MCP_PIN_LEDGER` env override; default `state/mcp_pins.jsonl`
     (tools/mcp_pin.py DEFAULT_LEDGER); `MAG_MCP_PIN_GATE=off|0|false` is the operator
     disarm hatch and returns None.
   - `pin_gate_filter(manifest, ledger_path)` (mag/mcp_server.py:276): runs
     `tools.mcp_pin.check_drift` (lazy import keeps module import stdlib-only), writes a
     loud stderr DRIFT ALARM per drifted tool (name, kind, first_seen, exact repin
     command), and returns the manifest WITH drifted tools WITHHELD: the mutated
     description/schema never reaches a model. `repin()` is the only way a changed
     surface returns -- the pin doctrine at tools/mcp_pin.py:140-145 ("the alarm blocks
     and repin() is the only way past it"), now enforced by a caller for the first time.
   - `handle(msg, profile, pin_ledger=None)` (mag/mcp_server.py:404): the tools/list
     branch gates whenever a ledger is passed.
   - `serve(profile)` (mag/mcp_server.py:443): gates the profile surface once AT BOOT
     (alarm fires even if the client never asks tools/list) and passes the ledger into
     handle() so every tools/list response is gated. A connect therefore gates twice by
     design: boot + per-list (2 x 34 = 68 touch records per clean connect, verified).
   - Module docstring: PIN GATE paragraph added (spec-before-behavior discipline).
2. `mag/mcp_http.py:31`: the gateway adapter `_respond` passes
   `mcp_server.pin_ledger_path()` into handle(), so POST /mcp tools/list (X-API-Key +
   loopback surface) is gated identically.
3. `dashboard/server.py:830-838`: the SECOND /mcp POST surface (which called
   `tools_manifest()` directly and would have been an ungated side door) now routes
   tools/list through `pin_gate_filter` + `pin_ledger_path`.
4. `tests/test_mcp_pin_wire.py` (new, 6 tests): proves first-connect pins via handle(),
   drift is withheld + stderr alarm + zero ledger writes for the drifted tool (forensics
   contract), repin returns the tool, MAG_MCP_PIN_GATE=off is a no-write passthrough,
   serve() alarms at boot before reading any message, and the HTTP adapter passes the gate.

Semantics preserved for existing callers: direct `handle()` calls with no pin_ledger
(default None) are gate-off, so programmatic users and all pre-existing tests are
unaffected (tests/test_mcp_quantized.py + tests/test_sense_mcp.py still pass untouched).

## Safety probe run BEFORE arming

The real ledger `state/mcp_pins.jsonl` already held 68 records (34 tools, pinned
2026-09-26T00:19:43Z). Read-only drift probe (real 34-tool manifest vs a ledger COPY in a
temp dir, so no writes): `alarm False, counts {observed: 34, new: 0, pinned: 34, drift: 0,
missing: 0, invalid: 0}`. Arming is safe: the first real connect just refreshes last_seen
and serves everything. Confirmed after all runs: the real ledger still reads 68 records,
single 2026-09-26 stamp -- this session wrote only temp ledgers.

## Checks run (raw output: watch/inbox/gala_20260925/wave5-repair/lanes/mcp-pin-wire.check.txt)

1. `./.venv/Scripts/python.exe tools/mcp_pin.py --self-test` -> `passed: 9, failed: 0`,
   exit 0 (finish line: still 9/9).
2. `./.venv/Scripts/python.exe -m pytest tests/test_mcp_pin_wire.py
   tests/test_mcp_quantized.py tests/test_sense_mcp.py -q` -> `16 passed`, exit 0
   (6 new wiring tests + 10 pre-existing MCP tests, no regression). Baseline before the
   edit was `10 passed`.
3. Callers census after wiring: `git grep -n "pin_gate_filter\|pin_ledger_path" -- "*.py"`
   -> 10 hits across mag/mcp_server.py, mag/mcp_http.py, dashboard/server.py; and
   `git grep -n "check_drift" -- "*.py"` shows the first call sites outside
   tools/mcp_pin.py (mag/mcp_server.py:293 definition-call in pin_gate_filter). Before:
   only tools/mcp_pin.py (re-derived live from the mcp-security/w4-41 claim).
4. Live end-to-end stdio probe (the real `python -m mag.mcp_server` spawned as a
   subprocess, temp ledger via MAG_MCP_PIN_LEDGER): connect 1 served 34 tools and wrote
   68 ledger records (boot gate + tools/list gate), stderr silent on the clean surface;
   connect 2 served 34, ledger 136; connect 3 with MAG_MCP_PIN_GATE=off served 34 and
   wrote NO ledger. First probe run had a wrong assertion (expected 34 records on first
   connect; the designed double-gate writes 68) -- both runs kept in the raw check file.
5. `./.venv/Scripts/python.exe tools/violation_ratchet.py check --changed` -> `RATCHET:
   PASS -- no unregistered debt`, `hits=27; registered=27; NEW=0`, exit 0. (The 27 hits
   are pre-existing registered debt across the 35 files changed on this branch by other
   lanes; none are from this lane's files.)
6. ASCII/em/en-dash scan over the 105 added diff lines of this lane plus the whole new
   test file: 0 hits.

## Honest limits

- The daily-patrol alternative surface named in the ask ("or a topic in the existing
  daily patrol script") was NOT built; the connect surface was chosen. Drift on a server
  that never connects is detected at its NEXT connect, not daily. A scheduled patrol
  topic (run check_drift over a captured tools/list daily) remains open work if the
  operator wants offline detection.
- The gate covers tools/list serving. `--quantize` cartridges and the dashboard GET /mcp
  info page (names only) are projections outside the gate; cartridge drift is visible via
  its content-addressed manifest_sha256, noted here as a known boundary, not fixed.
- Ledger appends from concurrent surfaces (stdio + gateway + dashboard) can interleave in
  principle; load_pins() skips malformed lines so a torn line degrades to a skipped
  record, and the alarm path never overwrites (append-only contract unchanged).
- First real connect from any client will append 68 touch records to
  state/mcp_pins.jsonl per clean connect (34 tools x boot + list). At heavy use this
  grows; pruning/compaction of the touch log is future work and deliberately NOT added
  here (append-only is the forensics contract).
- tests/test_mcp_pin_wire.py::test_gate_disarm_is_a_passthrough initially failed because
  it expected the ledger file to not exist, forgetting the test's own setup pins it;
  fixed to compare record counts before/after. tests counted as failed during
  development: 2 (both test-side, no wiring change required).

## Decision ledger

Closes the decision "is the mcp_pin rug-pull gate load-bearing?" -- it now is. Changes
the estate's MCP connect contract from "serve whatever the signatures produce" to "serve
only what the pin ledger vouches for"; a description/schema change to any of the 34
pinned tools is now loud (stderr alarm + tool withheld) at every connect until an
operator repins with a reason. This is the first estate instance of a w4-41 class-W gap
(proved mechanism, zero callers) being closed by wiring rather than by more proof.
