# MCP RETRO / DOCTRINE (ractor50 lane mcp, division B, banked 2026-10-01T01:2xZ)

Owed work: write the estate's MCP doctrine from its own waves - what tools belong
on the bridge, what never crosses, the metering rule, the next bridge organs
(R2-R4 priority), the missing-tools list (estate needs on MCP that neither house
nor provider surfaces offer), and the one-sitting build spec for the top missing
tool. Every claim below cites a file read or a command run THIS session; raw
output lives in
`watch/inbox/gala_20260925/ractor50/lanes/mcp.check.txt` (the check transcript;
9 sections). No em-dashes anywhere in this file.

## 0. Headline

The estate's MCP layer went from one experimental server (2026-08-31) to five
live or half-live MCP surfaces plus a doctrine-grade receipt base in 30 days,
and tonight the newest organ (the pin gate) caught its first real intruder: a
bridge tool whose schema drifted after its pin is WITHHELD from the served
surface right now, alarm on stderr, until an operator repins. The retro's
verdict: the architecture is sound (transport, pin, isError, effect-class
meta all proved live), the gap is not organs but PARITY and LOOP-CLOSURE -
the docker surface serves a stale manifest, and a bridge client still cannot
file the receipt that the estate's own workflow gate demands of every wave.

## 1. The MCP estate tonight (all counts live-run this session, transcript section numbers)

| surface | transport | serves tonight | evidence |
|---|---|---|---|
| house stdio (`python -m mag.mcp_server`) | stdio JSON-RPC 2.0, protocol 2025-06-18 | full profile: 41 tools; bridge profile: 6 declared, **5 served** | transcript S1-S2 |
| house HTTP (`POST /mcp` on gateway 127.0.0.1:8001, X-API-Key) | stateless streamable + batch | same manifest, gated by `mag/mcp_http.py:31` pin pass-through | `watch/inbox/wave5_repair/mcp-pin-wire.md` |
| docker `mag-mcp` on 127.0.0.1:8766 | TCP bridge over stdio (one server proc per conn) | **STALE: 17 archivist tools, zero estate_ tools**; container created 2026-09-26T20:38Z, a rebuilt image exists (2026-09-30 18:38 EDT) but the container was never recreated | transcript S6 |
| seed MCP (`tools/seed_mcp.py`, separate server) | stdio | 3 resources + 4 tools (rebuild_subtree, verify_hash, fetch_bounded_pointer, join_protocol); cold-join falsifier PASSED 2026-09-26 | `watch/inbox/burn_wave_20260926/B2_181_seed_mcp_20260926.md` |
| GPS router facade (`tools/gps_mcp/server.py`) | stdio, MCP-shaped not MCP-wired | ask/cascade/report_capability/record_verdict, 28 tests pass; "MCP mapping documented ... so real-MCP wiring later is mechanical" | `watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md` |
| provider surfaces (this seat's host) | hosted MCP plugins | 121 live provider tools counted 2026-09-28 (87 external + 34 house); registry declares 25 of them | `watch/inbox/burn_reset_20260927/flash50/mcp-patterns.md` section 5; validator green tonight: 25 checks passed, renders free 8 / funded 22 / operator 25 (transcript S4) |

The "6 estate tools live" claim in the ask is TRUE at the registration layer
(6 static TOOL_MAP entries + ROLE_TOOLSETS["bridge"], `tools/__init__.py:56-62`,
`mag/mcp_server.py:117-121`) and 5-of-6 at the SERVING layer tonight, because
the pin gate withholds `estate_thought_compile` (see section 2). Both numbers
are reported; neither is rounded to the other.

## 2. First live fire of the rug-pull gate (new estate fact, 2026-10-01)

`check_drift` was wired at every connect surface on 2026-09-29
(`mag/mcp_server.py:338-340` inside `pin_gate_filter`, called from `serve()` at
boot and per tools/list; first call sites outside `tools/mcp_pin.py`;
transcript S7). Tonight a real client connect produced:

```
[mcp_pin] DRIFT ALARM: tool 'estate_thought_compile' schema changed since pin
(first_seen 2026-09-29T14:56:18.608622+00:00); WITHHELD from served surface.
Accept after review: python -m mag.mcp_server --list > tools_list.json &&
python tools/mcp_pin.py --repin tools_list.json --reason "reviewed"
[mcp_pin] serving 5 of 6 bridge tools; drifted tools withheld until repin
```

(transcript S1, STDERR section). Root cause, byte-proven: the pin was taken at
2026-09-29T14:56Z during the R1 probe; commit f7768cd10 (2026-09-29 11:49 EDT =
15:49Z) added `mag/estate_bridge.py` with a schema block whose bytes differ from
what was pinned (description hash UNCHANGED, schema hash CHANGED:
pinned `18cc8d67...` vs live `3db75964...`; description hash identical at
`9bb1b4c0...`; transcript S3). The wire-level contract held exactly as
designed: the drifted tool never reached the model, the other five served, the
alarm named the exact repin command. Ledger census: 397 records in
`state/mcp_pins.jsonl` (transcript S3; 68 at wiring time per pin-wire.md -
growth is touch records from repeated connects, the known append-only cost).

**Law MCP-1 (schema-edit-repin):** a commit that changes a pinned tool's
description or inputSchema bytes MUST carry the repin (with reason) in the same
commit or the very next operator action. Tonight's drift is the counterexample
that makes the law: 53 minutes between pin and unrepinned schema change, tool
dark for a day. NOT DONE by this lane: the repin (operator review action; the
alarm stands as evidence).

## 3. What the 30 days of waves taught (the mined history)

- **2026-08-31, quantized dogfood** (`watch/inbox/MCP_QUANTIZED_DOGFOOD_RECEIPT_20260831.json`):
  20 tools, profile projections pass, stdio protocol pass. Taught: a profile is
  a projection, not a permission set - the sentence that every later organ
  reuses.
- **2026-09-16, U9 union server** (`watch/inbox/wave_20260916/receipts/U9_UNION_MCP_SERVER.md`):
  a SECOND estate codebase (ractor-salon) got a real stdio MCP server with 3
  tools. Taught: the JSON-RPC/stdio pattern is portable, dependency-free, and
  reproducible outside this repo.
- **2026-09-26, B2-181 seed MCP**: a cold session rebuilt a working subtree
  from MCP alone (10/10 cold-join checks, hash-verified). Taught: MCP can carry
  the estate's continuity, not just its compute.
- **2026-09-26, B2-291 docker**: the MCP server became an always-on service via
  a TCP bridge; 17 read-only tools; two concurrent sessions proven. Taught: the
  transport stack, and also - unintentionally - that an always-on surface goes
  STALE silently (section 5 below).
- **2026-09-28, flash50 arc** (six banked items in `watch/inbox/burn_reset_20260927/flash50/`):
  security census (10 gaps, R1-R6 ranked), bridge design (R1-R5 rollout),
  composition proofs (isError contract, refs-are-params, fan-in), registry
  design (two-axis tier/mode, six cost classes, 25-row validator-green sample),
  Mapbox dogfood (13 calls, P1-P8 patterns), Together map (six families,
  REST-shaped, MCP-introspection OWED).
- **2026-09-29, R1 + pin-wire + GPS_V0 + queue_closes**: bridge R1 landed (6
  tools live, 19 new tests, per-tool never-cross rulings); the dormant
  check_drift gate got its wire; the GPS router was built as an MCP-shaped
  facade; a 7th estate_ tool (`estate_queue_closes`) entered TOOL_MAP OUTSIDE
  the bridge profile (`tools/__init__.py:62`, not in ROLE_TOOLSETS["bridge"]).
- **2026-10-01 (tonight)**: first gate fire; docker surface parity break found;
  this doctrine.

## 4. DOCTRINE: what tools belong on the bridge

A tool joins ROLE_TOOLSETS["bridge"] iff it passes ALL seven:

1. **One verb, one wrapper.** Never a generic run/proxy tool (design law,
   mcp-bridge.md section 3). One tool per verb is what let the R1 count
   reconcile as six-under-five-verbs instead of becoming a kitchen sink.
2. **Stateless or caller-held state.** The water_graph shape: caller holds the
   spec (`to_spec`/`from_spec`), server holds the physics. No server-side
   session store (mcp-bridge.md 3.1).
3. **Effect class declared in `_meta` before the call** (effect_class, risk,
   authority, cost_kind, exhaustion; `mag/mcp_server.py:121-157`). The caller
   pre-flights authority without a round trip.
4. **Bounded output, bounded time.** Truncation or cap on every list; timeout
   per tool (mcp-bridge.md 3.7 table).
5. **$0 marginal or registry-metered.** cost_kind `deterministic_local` for
   reads; anything billing rides the registry's cost class (section 6).
6. **Pin-stable.** Survives the pin gate: description + schema hashes stable
   across connects; drift = withheld until operator repin (MCP-1).
7. **Never-crosses clean** (section 5). A tool whose blast radius cannot be
   bounded by schema + authority does not get a wrapper; it gets a finding
   path.

## 5. DOCTRINE: what never crosses (the chain-repair precedent, enumerated)

The precedent set at R1, now doctrine - each row names its judge:

1. **Chain REPAIR (real).** `estate_chain_verify` is dry-only; the live call
   tonight returned `{"dry": true, "exit_code": 0, "verdict": "CHAIN-REPAIR:
   nothing to do (chain consistent (8694 leaves))"}` (transcript S1). Verbatim
   design ruling: "chain_repair(real) is NOT exposed to external agents in v1.
   It stays a seat-internal + operator verb." (`watch/inbox/burn_reset_20260927/flash50/mcp-bridge.md:136-137`).
   The general form: **the estate's integrity spine accepts verify from anyone
   and repair from no one through the wire; repair is file-a-finding, funded
   seat executes.**
2. **Dirac BANK until R4.** Mutating append to the invariant bank requires a
   broker authority envelope; the `receipt` argument is mandatory because the
   no-receipt bank is the fabrication smell (mcp-bridge.md 3.3).
3. **Driver control words, work lanes, and any key.** stop/start/once stay the
   operator's single word; lanes carry live provider keys; status crosses
   redacted, control never crosses (mcp-bridge.md 3.6; tonight's live call
   shows `off: false` with redaction note, transcript S1).
4. **Caller-supplied write paths.** The writer is pinned: thought compile
   refuses any out path (proved live at R1 with the bridge-pin refusal, and the
   BRIDGE_INPUT_SCHEMAS description says "caller-supplied in/out paths are
   refused", `mag/estate_bridge.py:97-98`).
5. **Model text as authority.** A proposal cannot authorize an effect - only
   the switchboard/effect broker does (`watch/inbox/SHARED_SURFACE_CONTRACT.json`
   laws; mcp-bridge.md 5.3).
6. **Secrets in either direction.** No elicitation form-mode, no free-text
   channel destined for a third-party API on the bridge profile, until param
   DLP exists (mcp-security.md gap 4 / R2 - still unbuilt, verified tonight:
   no COMBINED-rule consumer over tool arguments exists outside the file scanner).

## 6. DOCTRINE: the metering rule

Four clauses, each with a receipt:

1. **Unknown cost is a denial, not a free pass.** Registry rows carry a cost
   class; unmetered rows are operator-admit only, and the manifest spec's gate
   "REFUSES the call (fail-close; unknown cost is a denial, not a free pass)"
   (`docs/ref/MCP_MANIFEST_SPEC.md:96-97`; validator invariant
   `unmetered_operator_only` green tonight, transcript S4).
2. **The broker receipt stream IS the meter.** Do not add per-tool quotas to
   cheap deterministic reads; every mutating call already commits a broker
   receipt - count receipts, refuse on exhaustion, never soft-degrade
   (mcp-bridge.md 6.4 and 6.2).
3. **The caller pays the provider side.** External provider tools ride the
   caller's quota and its backoff law (429/1302 envelope, retry at 15s/30s,
   2 attempts max - the law reproduced at the tool layer during the flash50
   composition item). Estate-side budget joins the registry: the pack prices,
   the lane pays (mcp-patterns.md section 6, budget_join).
4. **The pin ledger is a meter too.** Every clean connect appends 2N touch
   records (2 x 34 = 68 on the full profile; ledger now at 397 records,
   transcript S3). Append-only stays the forensics contract; compaction is
   named future work, not a license to prune (pin-wire.md honest limits).

## 7. DOCTRINE: next bridge organs, R2-R4 priority (reordered by tonight's evidence)

The flash50 design's rollout (R2 scenario cards, R3 tokens, R4 broker wiring,
R5 tunnel) stands, but tonight's checks insert two organs ahead of the original
R2 and one between it and R3:

- **R2.0 (NEW, tonight, one sitting): surface parity.** The docker mag-mcp
  container serves the 2026-09-26 manifest (17 tools, zero estate_) while the
  host venv serves 41; a rebuilt image exists but the container predates it
  (transcript S6). Fix is one `docker compose up -d --force-recreate mcp` after
  the image lands, plus a parity check (compare manifest count for the same
  profile across stdio, HTTP, docker; fail loud on divergence). Law MCP-2:
  **an always-on MCP surface without a parity check is a stale surface with a
  green heartbeat** - the healthcheck probes the port, not the truth.
- **R2 (as designed, plus tonight's cleanup): bridge scenario cards + the
  repin.** configs/workflow_gate_scenarios/ holds the seven LAW-12 cards and
  ZERO bridge cards (transcript S8) - cards owed for: unauthorized call,
  expired authority, budget exhaustion, lease timeout, sensed-vs-done grammar,
  pin-drift withholding (tonight's fire is the fixture). And the operator repin
  of `estate_thought_compile` with reason (MCP-1).
- **R2.5 (NEW, this doctrine section 9): the receipt verb.** The workflow gate
  requires "receipt landing in watch/inbox/" of every workflow; a bridge client
  today has no write verb that satisfies the shared-surface contract. Close the
  loop with `estate_receipt_append` (spec below).
- **R3 (unchanged): per-seat bridge tokens** before any Shape B; `?key=` off
  for bridge routes; sha256 token table; rotation vault (mcp-bridge.md 5.2).
- **R4 (unchanged, slightly reshaped): broker envelopes for mutating verbs.**
  dirac bank gets switchboard-issued authority; receipt_append upgrades from
  canned authority to real envelopes; the GPS ask/cascade pair joins as
  read-only routing advice.
- **R5: tunnel, operator GO, never precedes R3.**

## 8. DOCTRINE: the missing-tools list (neither house nor provider surfaces offer)

Provider tools (121, mcp-patterns census) offer maps, search, readers, scanners
- none of them know the estate. The house surfaces know the estate but are
missing, verified tonight (TOOL_MAP grep + manifest census, transcript S2/S7;
each row names who needs it and where the need was felt):

1. **estate_receipt_append** - the write path under the shared-surface
   contract (spec, section 9). Needed by: every dogfood/dig lane that ends
   with "file the receipt"; the workflow gate's own receipts card.
2. **estate_pin_status** - read-only pin ledger query (what is pinned, what
   drifted, first_seen, the repin command). Tonight the drift was visible only
   as stderr inside a probe; a status tool makes gate state data, not console
   noise. Needed by: every client that must know why a tool vanished.
3. **seed_fetch** - read-only bounded-pointer fetch into TOOL_MAP. FILED OWED
   by B2-291: "no seed tool exists in TOOL_MAP to call ... adding a read-only
   seed_fetch tool is the follow-up" (`watch/inbox/burn_wave_20260926/B2_291_estate_mcp_docker_20260926.md`).
   The logic already exists in tools/seed_mcp.py (fetch_bounded_pointer with
   seal-check and refusal arms).
4. **estate_corpus_search on the bridge profile** - exists in the archivist/
   full surface (and docker), absent from the bridge: an external agent gets
   estate compute but not estate memory. Composition gap, not a new tool.
5. **estate_budget_read** - broker receipt stream + spend_overlay reader; the
   metering rule made queryable. Needed by: any funded lane told to "spend"
   (driving ladder) that cannot see what it has spent.
6. **estate_gps_ask / estate_gps_cascade** - wire tools/gps_mcp's ask/cascade
   into TOOL_MAP (read-only advice class; ledger writes stay local). The V0
   receipt names the wiring as mechanical.
7. **estate_queue_read** - queue/todo.md + QUEUE.md open rows with claim-law
   fields. Needed by: cold seats that must FIND. FILE. LOAD without shell.

Not missing (checked before listing): corpus FTS (exists, archivist surface),
water/dirac/chain/driver/compile (bridge R1), receipt READING (files are
already readable via archivist fs tools) - the gap is the WRITE path only.

## 9. One-sitting build spec: estate_receipt_append (top missing tool)

The estate's own gate demands receipts in watch/inbox/ (AGENTS.md workflow-gate
section); this is the verb that lets an MCP-only client comply. Pattern copy:
the thought_compile OUT_DIR pin (proven live at R1) at single-file granularity.

- **Where:** `mag/estate_bridge.py` new section (same file as the other six
  wrappers; ~70 lines with tests in `tests/test_mcp_bridge_r1.py`).
- **Wrapper:** `receipt_append(*, wave: str, name: str, payload: str) -> dict`.
  - `wave`: new subdirectory under `watch/inbox/`, regex
    `^[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}$`, no separators, no `..`.
  - `name`: receipt filename, same charset, must end `.json` or `.md`.
  - `payload`: UTF-8 text, hard cap 65536 bytes (larger = isError naming the cap).
- **Guards (all isError, never crashes):**
  1. Resolved target must be inside `watch/inbox/` (resolve + prefix check;
     same shape as the compile refusal at `mag/estate_bridge.py:100-104`).
  2. Refuse overwrite: if target exists, write `<name>.bak_<utc-ts>` first and
     report both paths (append-only forensics, the pin-ledger habit).
  3. Auto-create `<wave>/` only under `watch/inbox/`; never touch INDEX.json
     (that is the promotion flow's job, contract says leave a receipt, not
     self-promote).
- **Return:** `{"ok": true, "path": ..., "sha256": ..., "bytes": ...}` - the
  hash is the receipt the caller can cite.
- **Effect class:** `mutating_or_executing`, authority `canned_broker` (the
  thought_compile class: one-directory allowlist; mcp-bridge.md 3.5 precedent),
  cost_kind `deterministic_local`, exhaustion `retry_or_defer`.
- **Wiring:** TOOL_MAP + _FN + one alias group (`file`->`name`, `text`->`payload`);
  ROLE_TOOLSETS["bridge"] gains exactly this one name; ROLE_DESCRIPTIONS
  updated; BRIDGE_INPUT_SCHEMAS entry with the regex constraints.
- **Tests (7):** happy path hash equality; overwrite rotates to .bak; `../`
  escape refused; absolute path refused; oversize payload refused; bad charset
  wave refused; unknown-tool-isError discipline untouched.
- **Pin law MCP-1 applies to itself:** the landing commit carries the pin row
  (the ledger pins at first connect) and the repin if any schema byte changes
  in review.
- **Falsifier:** if a caller-supplied path ending outside watch/inbox/ is NOT
  refused with isError, or the sha256 returned does not match the bytes on
  disk, the spec is wrong - amend, do not argue around (bridge design
  section 9 convention).

## 10. Composition addenda (what the provider dogfood proved, kept as bridge law)

- **isError is the conditional-composition carrier.** In-band failure is what
  lets the model branch; the estate's call_tool implements it everywhere
  (`mag/mcp_server.py:309-329`, unknown-tool probe live tonight, transcript S1).
  Bridge tools never convert tool failure into protocol errors.
- **Refs are params, not artifacts.** The Mapbox render-ref mechanism
  (selfFetch = serialized original call params) is the pattern to copy if
  bridge outputs ever need fan-in replay; the estate twin is: bank the bytes,
  never just the pointer (mcp-mapbox.md P2).
- **Anti-composition clauses belong in descriptions.** ground_location's
  "FIRST and ONLY" and render's monopoly are how overlap is policed without a
  registry row; the bridge's verify-vs-scan overlap should carry the same
  clause text at the next manifest touch.

## 11. Checks run this session (transcript: watch/inbox/gala_20260925/ractor50/lanes/mcp.check.txt)

1. S1 live stdio client session (real subprocess, 8 checks, PROBE-SUMMARY: 0
   failures, exit 0): initialize, gated tools/list (5 of 6), deterministic
   tick, dry chain verify, redacted driver status, unknown-tool isError,
   DRIFT ALARM on stderr.
2. S2 manifest counts: full 41, bridge 6, estate_-prefixed in full = 7.
3. S3 pin-vs-live hash diff: description UNCHANGED, schema CHANGED (the drift).
4. S4 registry validator: 25/25 checks passed, exit 0.
5. S5 pin self-test: 9 passed / 0 failed, exit 0.
6. S6 docker parity: container 2026-09-26 image serving 17 tools, zero
   estate_; host image rebuilt 2026-09-30 18:38 EDT, container not recreated.
7. S7 check_drift caller census (wired at mag/mcp_server.py:338-340).
8. S8 scenario cards census: 7 LAW-12 cards, zero bridge cards.
9. S9 + ratchet: `tools/violation_ratchet.py check --changed` TRUE exit 1 -
   NEW=2, both sibling-lane untracked files (tools/flock_parity.py,
   tools/reverse_map.py); this lane wrote only watch/inbox/ files.

NOT run this session: secret-gate param DLP probe (organ does not exist -
that absence IS the finding), HTTP-transport live call through the gateway
(the stdio arm was the finish line; mcp_http pin pass-through cited from its
receipt), Together MCP introspection (no together tools on this seat; the
flash50 map's OWED stands), the repin (operator action).

## 12. Decision ledger

Closes the mcp retro owed item (gala ractor50 division B). Changes three
decisions: (1) bridge rollout order gains R2.0 surface-parity and R2.5
receipt-verb ahead of the original R2/R3 sequence; (2) the "6 estate tools
live" fact base is corrected to 6 declared / 5 served until the operator repin
(MCP-1); (3) docker mag-mcp is declared stale-until-recreated, not healthy-
meaning-current (MCP-2). New laws proposed: MCP-1 schema-edit-repin, MCP-2
always-on-surface-parity.
