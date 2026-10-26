# quantizer-hygiene (ball-20260929, division B): the three verified quantizer losses fixed at root

**Lane:** quantizer-hygiene · **Date:** 2026-09-29 · **Owner seat:** gala lane, mag/run-beta1 branch
**Owed work:** w4-27 section 3 loss classes L1, L3, L4 (watch/inbox/burn_reset_20260927/flash50/w4-27.md) + s2-23.md (stage 4/5).
**Finish line:** fresh compile shows zero shell-error fragments in any pack; the decay constant defined exactly once and imported at all three sites; kept == packed across tiers; tests green. Raw evidence: watch/inbox/gala_20260925/ball-20260929/lanes/quantizer-hygiene.check.txt (all checks exit 0).

## L1: shell-error fragments refuse unless genuinely imperative

v0.3 kept `[Errno 2] No such file or directory: 'Get-ChildItem'` (de7eaa711459), `'type'` (d536890f0abc) and `'powershell'` (ae3af609ff99) as flash laws because "file" is an IMPERATIVE_RE keyword inside the error text and TELEMETRY_RE has no errno shape (w4-27 L1 measured 3 of 12 flash rows as fragments; re-measured live this ask, same three ids in instructions_flash.jsonl before the fix).

Fix (tools/thought_quantizer.py): `SHELL_ERROR_RE` matches the shell-error LINE itself ([errno N], no such file or directory, is not recognized as, command not found, permission denied, no module named, traceback, segmentation fault, cannot find the path/file, file not found); `classify()` now refuses such texts as machine events UNLESS the text adds normative framing beyond the quote: LAW_SHAPE_RE grammar, a NORM_MODAL_RE modal (must/shall/should/always/never/do not/don't/whenever), or a CONDITIONAL_LAW_RE conditional do-X frame ("when the gate exits 2, rerun it..." keeps; the v0.3 heal survives). IMPERATIVE_RE's verb list was hoisted into `_VERBS` so the conditional frame shares it exactly.

Live result (check.txt CHECK 1-2): fresh v0.4 compile, refused_telemetry 2 -> 5 (delta is exactly the three errno rows, verified by classify() census), all three baseline ids gone from every pack, `SHELL_ERROR_RE` scan over all 374 packed rows x all tier fields: **0 hits**.

## L3: one decay constant, defined once, imported at all three sites

Before: producer `check(max_age_hours=24.0)` (thought_quantizer), consumer `if age_d > 7.0` (mag/context_pack.py `_quantized_laws`), boot `STALE_DAYS = 7` / `HEARTBEAT_DAYS = 2` (tools/freshness_check.py): three uncoordinated TTLs on one resource (w4-27 L3; fossil_registry.json itself recorded the split, "pack bar 24h, independent of compile_report mtime").

Fix: `PACK_STALE_DAYS = 7` defined ONCE in mag/constants.py (the lazy, pathlib-only constants home), imported at:
- producer: tools/thought_quantizer.py (check() now takes days; `--max-age-days` CLI replaces `--max-age-hours`; no external caller of the old flag existed, grep-verified)
- consumer: mag/context_pack.py (`if age_d > PACK_STALE_DAYS`)
- boot: tools/freshness_check.py (`STALE_DAYS = PACK_STALE_DAYS`; run via scripts/ratchet_daily.ps1 daily, exit 0 after the change)

**Decision: the unified value is 7d, not 24h.** Direction argued from harm: the verified defect (s2-23 roll-up 10) is stale law rendered as obey-law, which loosening the producer would legalize for the whole window; 7 is also the value the estate's other freshness surfaces already shared (fossil_registry bar_hours=168 for the compile report, the boot-doc bar, the census bar) - the producer's 24h probe was the outlier. After unification the fossil arm and the render bar coincide, so the "up to 6 days of stale law shown as obey-law" window is structurally gone. HEARTBEAT_DAYS=2 stays a local constant: it is a liveness window, not a decay bar, and it has exactly one site. Live parity verified: `tq.PACK_STALE_DAYS is cp.PACK_STALE_DAYS is freshness.STALE_DAYS is DEFINED` -> True (check.txt CHECK 3).

Note left intentionally: configs/fossil_registry.json is SEALED and outside this lane's ownership; its note line ("pack bar 24h, independent of compile_report mtime") is now stale while its operative `bar_hours: 168` matches the unification. One-line operator fix when the seal next opens.

## L4: the linker law, kept == packed

Before: 307 kept, packs 24/12/12 = 60 packed, 283 laws in no pack with zero counters (s2-23 stage 4; w4-27 L4 "dead definitions").

Fix (tools/thought_quantizer.py compile_packs): tiers are now DISJOINT BANDS of the ranked list - flash (the consumer seam every seat boots, mag/context_pack.py reads instructions_flash.jsonl only) takes the top-ranked rows, frontier the next band, local the remainder; a cap <= 0 takes all remaining (new CLI default `--local 0`). The compile fails LOUD with `linker error: kept N != packed M` unless every kept law lands in exactly one tier pack. Census gains a `packed` counter; report bumped to v0.4 with the amendment stanza.

Live result (check.txt CHECK 4): kept 374 == packed 374 == sum of pack rows (frontier 24 + flash 12 + local 338); flash top-12 keeps the highest-weight laws for the boot dose.

Required companion edit outside the named ownership set, named here: mag/estate_bridge.py `estate_thought_compile` default `local` 12 -> 0 (schema minimum 1 -> 0). The old 24/12/12 default would trip the linker error on real data (48 packed vs 374 kept) and break the live MCP surface; 0 is the remainder cap and cannot wipe a tier under band semantics. tests/test_mcp_bridge_r1.py: 22 passed.

## Tests

- tests/test_thought_quantizer.py: +5 cases (three live errno fragments refuse; the 'type'/'powershell'/'is not recognized'/'command not found' shapes refuse; genuine-norm error law keeps; decay constant defined-once/three-site parity incl. spec-loaded freshness_check; linker kept==packed with disjoint-band verification; linker fails loud on undercover caps; flash-takes-top-rank), status pin updated compiled-v0.3 -> compiled-v0.4. Suite: 20 passed (with tests/test_context_pack_quantized_laws.py, which pins the render seam and stays green).
- tests/test_mcp_bridge_r1.py: 22 passed (bridge pin + new defaults).

## Not fixed, measured and registered (residuals)

1. **Probe-table echo rows (fourth loss class, outside this ask's L1 spec).** The invariants stream holds 301 `pro-xxxxxxxx -> ok (Verify with git diff...)` rows - one per probe id, so signature dedupe never collapses them; 301 of 374 kept laws are this echo, 6 sit in the flash top-12 (they were there in v0.3 too: ranks came from the same list; NOT a regression of this lane). They quote a real law and are noise rather than non-denoting fragments, so the L1 escape (which refuses only shell-error shapes) correctly does not fire on them. Owed: either percolator-side echo collapse or a signature() machine-row normalization - owner should be the percolator/quantizer dedupe law, not snuck into this lane's classify().
2. Sibling debt: `violation_ratchet.py check --changed` exit 1 with NEW hits ONLY in mag/corpus_acquire.py (:636 file-too-long, :376 except-pass) - the corpus_acquire owner lane's debt, already named at the wave5 fold ("owner lane owes fix"). ZERO ratchet hits on this lane's six files (grep of raw output: none). Raw output: watch/inbox/gala_20260925/ball-20260929/lanes/_ratchet.txt, also appended to check.txt CHECK 7.
3. mag/context_pack.py `_quantized_laws` still caps at 1800 chars and the janitor budget still clips (L2, w4-27's erasure class) - NOT in this lane's ask (L1/L3/L4 only), unchanged.

## Hygiene

Em/en dash scan of ADDED diff lines across the six lane files: 0 hits (git diff -U0 | grep, this session; the instrument's whole-file counts include pre-existing docstring dashes). Instrument kept as evidence: watch/inbox/gala_20260925/ball-20260929/lanes/_quant_hygiene_check.py (reads only; raw stdout banked at quantizer-hygiene.check.txt, all seven checks present, exit 0).

## Decision ledger

Closes the w4-27 section 5 sketch item "two TTLs on one resource fail subsumption at compile" and "a kept law unreachable from any tier pack is a linker error": both are now code (mag/constants.py PACK_STALE_DAYS with three named importers; the compile_packs linker error), not just card prose. The quantizer is v0.4.
