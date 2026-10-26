# P5 ReFold: reversible pack sheds (port-order lane P5, 2026-10-07)

Lane: day-7 mine fold, port-order P5. Steal: watch/inbox/frontier_olm_2026-10-07/steal/kv-cache-context-engineering.md (Steal 2, ReFold). Executor: P5 seat, repo venv python only, no commit. All quantities cited below are banked with their instruments in watch/inbox/port_wave_20261007/p5_refold_probe.json.

## What landed (all in mag/context_pack.py)

1. Reversible shed stubs: every shed rung (1 heat drop, 2 task compact, 3 per-block shed) files a stub into its PACK_OFFLOAD.jsonl row carrying section, source organ path, content sha256, and chars. The sha is over the exact rendered lines removed; restore re-renders from the stub's named source and refuses on sha drift. The schema string stays pack_offload.v1 as an additive-field extension, so the v1 pin in tests/test_dirac_loop.py holds unmodified.
2. Render-side fold marker: a stage-3 fold leaves ONE render line, "[SHED this fold: N sections | restore: python -m mag.context_pack sheds]". Per-section pointer bytes deliberately do NOT ride the render: measured this sitting on route, the whole sheddable tier was 775 bytes while 7 in-render stubs cost 1085 (probe json, render_stub_net_negative_measurement), so render stubs are net-negative on the tight mode budgets and tipped 4 pre-existing tests plus route/audit hard clip before the redesign. Stubs are pure functions of shed content, so consecutive renders between fold advances stay byte-identical (pinned in tests/test_context_pack_refold.py).
3. Restore machinery: restore_shed_section(section, mode, pack, sha) over a per-section recipe table mirroring the live section builders byte for byte (the mirror itself is pinned by test_recipe_mirrors_live_section_build). Restore without a pack rebuilds a fresh fast pack from the named organs; sha drift refuses the restore instead of corrupting it.
4. Ledger reader, the first PACK_OFFLOAD consumer: read_pack_offload() byte-splits, skips torn non-UTF8 rows with a note (never crashes; the live file holds exactly 1 such row, bytes 80 a6 + CR, matching the steal card), and flags rows whose (mode, max_chars) mismatches the current budget table as stale_code. list_shed_stubs() flattens rows into a restore index.
5. CLI: python -m mag.context_pack sheds [--tail N], and restore --section NAME [--mode M] [--sha HEX] with exit 1 on drift or unknown section.

## The 84 stale full-mode rows: disposition

The steal card banked 84 post-commit rows still firing full mode at 7200 after commit 633b884ad raised full to 26000 (mag/context_pack.py). Disposition this sitting:

- No dead 7200 constant exists in code on disk: the only 7200 left in mag/context_pack.py is prose inside comments; the budget table holds full at 26000. The steal card's own candidate (a renderer process older than the commit) is confirmed live: my recount reads 322 post-commit full/7200 rows (probe json, ledger_recount), still firing at 42 rows per hour, and the newest ledger row at recount time was itself full/7200 (2026-10-08T05:01:04Z per watch/inbox/PACK_OFFLOAD.jsonl).
- The emitter is the dashboard full-mode pack endpoint (h_context_pack in dashboard/rest.py renders full with no override); the dashboard port pair (8765/8766, probe json) resolves to the Docker Desktop backend on this host, a container surface that predates the commit. Bouncing it is an operator call, not a lane action; the rows are harmless telemetry under the old constant.
- Detection is now mechanical: any (mode, max_chars) mismatch against the current table is flagged stale_code by the reader, so the next stale renderer is visible from the ledger without a hand recount. Explicit max_chars override renders also mismatch and the flag note says so.

## Torn row handling

read_pack_offload decodes and parses per line: a torn non-UTF8 partial write is counted with a byte-preview note and skipped; good rows around it still parse. Pinned by test_ledger_reader_skips_torn_non_utf8_row using the live torn shape (80 a6 + CR).

## Gates (moment 2026-10-08T05:55Z, probe json gates block)

- pytest over tests/test_context_pack_refold.py + tests/test_context_pack_delivery.py + tests/test_context_pack_quantized_laws.py + tests/test_dirac_loop.py: 46 passed, 6 failed, and all 6 are stash-verified pre-existing at HEAD (git stash of mag/context_pack.py, same suites, same 6, measured before my edits): 4 test_quantized_laws_render_in_every_mode (janitor/route/build/audit) plus 2 test_render_fits_budget_without_hard_clip (build/plan). The task brief named 2 pre-existing hard-clip failures; byte truth at HEAD is 6. Cause class is live-organ growth against fixed budgets, not this port.
- Ratchet: check --changed PASS, NEW=0.
- Census instrument (pytest --collect-only -q, default testpaths): 5003 collected, zero collection errors.
- Other pack-touching suites (steward/coordination/checkpoint/v3/ag5/rib_boot_amendments): 46 passed.
- Live: mag.cmd context-pack exit 0; main.py context-pack exit 0; a live fold fired (route render 5094 chars against a 5200 budget, marker "7 sections"; watch/inbox/port_wave_20261007/p5_refold_probe.json); live restore via the new CLI sha-verified, exit 0 (L0d rib vault amendments, 4290 chars, re-rendered from memory/rib_boot.json).
- Em-dash law: no em/en dashes in added prose; the only dashes in added lines sit inside copied render literals where byte parity with the live section builders is the mechanism.

## Owed / blockers

- The stale full/7200 container renderer keeps emitting until an operator bounces the dashboard surface.
- The 6 pre-existing reds (organ growth vs fixed mode budgets) are a separate lane's cure.
- The L0f full-mounted-subchain recipe is verified in-process only; the escape-hatch mode rarely sheds and had no live fixture this sitting.
