# RECEIPT: mcp-bridge R1 landed (2026-09-29, lane mcp-bridge-r1, division B)

## What landed

Bridge R1 from `watch/inbox/burn_reset_20260927/flash50/mcp-bridge.md`: the
estate's five verbs are live on the house MCP surface. One tool per verb
(design law, mcp-bridge.md section 3), so the ask's itemization names six
tools under the "five verbs" headline; the count is reconciled here, not
argued around:

| tool | wraps | class |
|---|---|---|
| estate_water_graph_tick | mag/water_graph.py WaterGraph.tick + from_spec/to_spec | read/deterministic |
| estate_dirac_scan | mag/dirac_loop.py scan | read |
| estate_dirac_rank | mag/dirac_loop.py rank | read |
| estate_chain_verify | tools/chain_repair.py repair(dry=True) ONLY | read (dry) |
| estate_thought_compile | tools/thought_quantizer.py compile_packs, OUT_DIR-pinned | mutating |
| estate_driver_status | tools/stealth_driver.py heartbeat + off flag + work state, redacted | read |

NEVER exposed (per-tool rulings): chain repair (verkle blast radius,
mcp-bridge.md 3.4), dirac bank (mutating, broker envelope is R4),
thought_check, dirac spectrum, driver stop/start/once control words, driver
work lanes and any key (mcp-bridge.md 3.6).

## Files changed (all this lane owns or the work needed)

- NEW `mag/estate_bridge.py`: the six wrappers + `BRIDGE_INPUT_SCHEMAS`
  (hand-written JSON Schema: scope enum, ticks/sizes bounds) + `_redact`
  (credential-named fields and key-shaped strings masked on driver status).
- `tools/__init__.py`: six static TOOL_MAP entries + six _FN entries + four
  _ARG_ALIASES groups (graph->spec, steps->ticks, graph_scope->scope,
  lines/n->tail). Static, not the ephemeral overlay (standing organs,
  mcp-bridge.md section 3).
- `mag/mcp_server.py`: ROLE_TOOLSETS["bridge"] (exactly the six),
  ROLE_DESCRIPTIONS["bridge"], effect-class set memberships, `_input_schema`
  hook (bridge tools get explicit schemas keyed on the estate_ prefix; every
  existing tool's schema byte-stable, so no existing pin drifts), header note.
- NEW `tests/test_mcp_bridge_r1.py`: 19 tests (surface projection, effect
  classes, live round trips, determinism, isError shapes, OUT_DIR pin +
  refusal, SystemExit conversion, redaction, dark-surface ok, never-exposed
  list, alias normalization).

## Evidence (all raw output byte-saved)

`watch/inbox/gala_20260925/ball-20260929/lanes/mcp-bridge-r1.check.txt`:

- SECTION 1: live stdio MCP session (real client, `python -m mag.mcp_server
  --profile bridge`, probe script `_bridge_r1_stdio_probe.py` in the same
  lanes dir): initialize OK; tools/list shows EXACTLY the six estate tools;
  live tools/call per tool returned real output (tick moved 2 units and
  echoed the new spec; dirac scan betti1=8, 6 closed loops, 0 open; rank
  n=41 m=21 c=28 beta1=8; chain verify "CHAIN-REPAIR: nothing to do (chain
  consistent (8390 leaves))" exit_code 0; compile 401 in / 377 kept, packs
  written to the pinned OUT_DIR; driver status off=false with live
  work_state); bad-input calls all rode in-band isError (empty spec, scope
  "internet", caller-supplied out path refused with the bridge-pin message,
  unknown tool). PROBE-SUMMARY: 0 failures.
- SECTION 2: pytest bridge + 3 mcp files: 38 passed, exit 0.
- SECTION 3: blast radius, all 19 test files that import the tools registry:
  218 passed, exit 0.
- SECTION 4: tests/test_transport_precheck.py alone: 6 passed, exit 0 (in a
  20-file batch it threw Permission errors; alone it is green, so batch-env,
  not a functional break).
- SECTION 5: ratchet `check --changed` exit 1. ALL NEW hits are sibling
  files: mag/corpus_acquire.py (file-too-long + except-pass) and
  tools/abliterate_p1_probe.py (file-too-long, growing between runs: another
  lane is writing it now). This lane's four files contribute zero NEW
  violations; mag/mcp_server.py's size debt is pre-registered in
  configs/violation_baseline.json.

Pin organ: the two real connects pinned all six tools into
state/mcp_pins.jsonl (rows 85-92, identical hashes across connects =
PINNED, no drift alarm).

Full suite NOT run (2,436 collected per the 09-29 census): the blast radius
of this change is the tools registry consumer set, which is exactly what
sections 2-4 cover; the shared tree has sibling lanes mid-flight.

## Restraint taken

- The live compile in the probe rewrote memory/corpus/quantized_thought/
  packs; they were snapshotted before and restored after (report back to its
  2026-09-28T16:19 compile; verified the probe timestamp is gone). Evidence
  of the compile lives in the check file, not in a repo mutation.
- No em-dash in anything this lane wrote (pre-existing em-dashes in shared
  files left untouched).

## Observations banked (not this lane's fixes)

1. DEFECT (water_graph owner): `WaterGraph.to_spec` (mag/water_graph.py
   250-258) serializes elev/kind/volume/steam but NOT a sill node's `sill`
   threshold, while `from_spec` (:267) reads it. A sill-gated graph
   round-trips through the bridge tick tool with its gate silently lost.
   One-line fix owed to the module owner: add `"sill": v.sill` to the node
   dict + a round-trip test. Not fixed here (sibling module owns its
   regression suite).
2. SENSING (driver owner): driver status shows heartbeat_tail empty (no
   rows read from state/fuel/stealth_driver.jsonl at 14:56Z) and live
   lane_errors: nous:3 HTTP 402 Payment Required, llm7:5 HTTP 400,
   nous:4 timeout, openrouter:4 HTTP 403, openrouter:1 empty content,
   openrouter:2 HTTP 429. Free-lane rot, worth a look by the stealth lane.
3. RATCHET (fold owner): the two corpus_acquire.py debts named in the wave5
   commit message as "registered at fold" surface as NEW in today's ratchet
   run; the baseline registration has not landed on this branch. Owner lane
   owes the baseline-update by name or the fix.

## Decision ledger

Closes mcp-bridge R1 (the flash50 owed item): estate compute went from zero
tools on the live MCP surface to five verbs / six tools, callable by any MCP
client over stdio, with repair/bank/control-words/keys affirmatively
excluded and every tool's authority pre-declared in its manifest _meta.
R2 (scenario cards), R3 (per-seat tokens), R4 (broker-gated mutating calls),
R5 (operator-GO tunnel) remain unstarted, per the design's rollout order.
