# AG7 — census refresh + seed seal verdict (2026-09-30)

Executor: ZCode lane (audit findings #13-14). Ownership honored: touched ONLY the AGENTS.md
census bullet, seed/MANIFEST.sha256, and this receipt.

## 1. Census refresh

- **Instrument:** `.venv/Scripts/python.exe -m pytest --collect-only -q -p no:cacheprovider tests`
- **Moment:** run started 2026-09-30T11:46:05Z; tail `3220 tests collected in 9.34s`, zero
  collection errors. Item-bearing files in that pass: **433** (unique node-id files).
- **Carrier now reads:** `3,220 tests collected / 433 files (2026-09-30 census` — B2-249 clause
  grammar preserved. Patrol proof: `python tools/census_drift_patrol.py` → exit 0
  (`census 2026-09-30 (3220 collected / 433 files)`); `parse_carrier` → 2026-09-30 / 3220 / 433.
- **Drift attributed** (prior carrier 2,436 / 371, 2026-09-29, receipt
  `watch/inbox/wave5_repair/patrol-fix.md`): +784 collected / +62 files across the 09-29-evening
  and 09-30 last-mile waves —
  - MICKEY17 `328896fcb` → tests/test_server_v0.py
  - THE COORDINATOR COMMIT `84811acb7` → +17 test files (test_brief_reaper, test_census_zero_collect,
    test_chain_contract, test_duel_harness, test_gap_sentinel, test_gate_canary, test_gwap_to_gps,
    test_inbox_consume, test_ledger_registry, test_protocol_table, test_realign,
    test_receipt_xref_gate, test_regen_front_door, test_room, test_scarless_preflight,
    test_skill_fired + the entrypoint 2,757-collect fix)
  - TIE-IT-ALL `579109f44` → +12 (test_attention_dam, test_eid_dedup, test_enqueue_law,
    test_gods_number, test_graph_heal, test_lane_budget, test_legality_dataset, test_oral_dedupe,
    test_refold_gate_run, test_reprint, test_skill_permissions, test_verkle_dangling)
  - WAVE X + X1 hydrology `f8452e01a` + `6caa8ef3e` → test_dem_to_board, test_hydrology,
    test_motion_rows, test_verdict_feed, test_propagator
  - Y11 `e74021078` → test_verkle_restore_prep
  - V-WAVE `ff1c02822` + `ac17d5da8` → test_realmd_client, test_anticheat, test_chat,
    test_field_flow, test_innkeeper, test_ldt_lattice, test_ldt_train, test_percolator_z15,
    test_rollup_delta, test_section_stream, test_server_persist
  - full-stack W3/W4/LW4 `00daf9103` + `d389326f0` + `70b781e84` → test_k8s_water, test_worldgen,
    test_river
  - AC14 `7f3ed70e8` → test_estate_cleanup; AD/AF `63f82eb12` → test_env_contract
  - plus items landed inside existing files (file-growth-blind per B2-244).
- **Audit interim 3,192** predates the 09-30 morning landings; 3,192 → 3,220 (+28) is those
  landings (AC/AD, LW/W/V completions listed above).
- **Denominator law note (B2-216):** a ~12:05Z probe of the still-moving tree read
  `3217 tests collected, 7 errors`; zero-collect gap 8 = 7 transient mid-landing import errors
  (test_agent_live, test_agent_repack, test_context_freeze, test_prompt_steering,
  test_repack_integration, test_resume_contract, test_seat_crash_guard) + the standing
  tests/test_selffeed_integration.py. Disk candidates read 435 at 12:05Z, 436 at receipt time —
  lanes still landing; the filed claim is the clean 11:46Z snapshot. Tomorrow's 08:30
  MagCensusPatrolDaily `--collect` run owns the follow-up on the settled tree.
- **Full gained list** (`git diff --name-only --diff-filter=A dbe5f682c..HEAD -- tests/`, 63 files;
  dbe5f682c = the wave5-repair commit that carried the 09-29 carrier refresh, so the few wave5
  in-flight files inside it were already counted by the 09-29 claim):
  test_anticheat, test_attention_dam, test_attention_feedback_ledger, test_brief_reaper,
  test_census_zero_collect, test_chain_contract, test_chat, test_corpus_acquire, test_dem_to_board,
  test_duel_harness, test_eid_dedup, test_enqueue_law, test_env_contract, test_estate_cleanup,
  test_field_flow, test_gap_sentinel, test_gate_canary, test_gods_number, test_graph_heal,
  test_gwap_mud, test_gwap_payload, test_gwap_to_gps, test_hydrology, test_inbox_consume,
  test_innkeeper, test_k8s_water, test_lane_budget, test_ldt_lattice, test_ldt_train,
  test_ledger_registry, test_legality_dataset, test_mcp_bridge_r1, test_mcp_pin_wire,
  test_motion_rows, test_oral_dedupe, test_percolator_z15, test_propagator, test_protocol_table,
  test_ractor_falsifier_stubs, test_realign, test_realmd_client, test_receipt_xref_gate,
  test_refold_gate_run, test_regen_front_door, test_reprint, test_river, test_rollup_delta,
  test_room, test_scarless_preflight, test_section_stream, test_selffeed_integration,
  test_server_persist, test_server_v0, test_skill_fired, test_skill_permissions,
  test_stealth_driver_prompt_lance, test_stealth_driver_v2, test_stealth_tools_wave5_repair,
  test_surface_rebuild, test_verdict_feed, test_verkle_dangling, test_verkle_restore_prep,
  test_worldgen (all under tests/).

## 2. Seed seal — verdict: LEGITIMATE LANDING, mis-stamped manifest; re-stamped

- **Symptom:** `seed/verify_seal.py` → `DRIFT engines/key_law.py`, 56/57 verified.
- **Bytes:** manifest line recorded `71f95e2d…`; working tree AND HEAD blob hash
  `fd2a0b27…`; `git status seed/` clean (the drift was committed, not a local edit).
- **The landing:** commit `383fed94f` (2026-09-27 10:01, "gate-fix + lens window close") is the
  last commit to touch seed/engines/key_law.py. Its entire diff to the file is the module
  docstring's CLI examples:
  `-  python engines/key_law.py --audit/--status` → `+  python -m tools.key_law --audit/--status`.
  Module reviewed in full: coherent key-law loader (one canonical manifest, single `get()` door,
  `audit()` orphan/empty checks, standalone dotenv bootstrap that never logs values). No logic
  change, no corruption, no secret material. Pre-landing seal was intact (383fed94f~1 blob
  `79b07f31…` == that revision's manifest line).
- **The mis-stamp:** the same commit rewrote the manifest line to `71f95e2d…`, which matches NO
  committed or derivable state — tested: old blob `79b07f31`, new blob `fd2a0b27`, CRLF
  `3511094c`, CR-only `1e82c4c6`, BOM `e00732d0`, no-trailing-newline `b89b649c`. The stamp was
  taken over intermediate working-tree bytes that were never committed (wrong-at-birth).
- **Action taken:** manifest rebuilt for the drifted row via byte-exact single-line re-stamp
  `71f95e2d… → fd2a0b27…`. `seed/engines/build_seed.py` was NOT run, on review: it is the frozen
  2026-09-25 v1 builder (hardcoded 12-engine ENGINES list, rewrites THE_METHOD/FIRST_BOOT/
  HANDOFF, seals ~16 files) while the package is SEED 3.3.0 with 57 sealed rows incl
  configs/templates/tests; running it would collapse the seal to ~16 rows and overwrite frozen
  engines from live `mag/`+`tools/` sources (mag/key_law.py exists and has diverged from the
  seed's standalone copy). The single-line amend is the byte-minimal rebuild for a 1-row drift.
- **CRLF side-fix:** the working-tree MANIFEST.sha256 was all-CRLF (4,940 B) against an LF-only
  blob (4,883 B) — a pre-existing Windows flip masked by the git stat cache until this touch.
  Normalized back to LF per the seed's own law ("LF seal passes stock sha256sum", SEED V2
  `662c25a9b`); `git diff seed/MANIFEST.sha256` is now exactly one line. Same flip hit AGENTS.md
  when the carrier edit rewrote it (working CRLF vs LF blob); normalized to LF the same way —
  `git diff AGENTS.md` is exactly one line (the census bullet).
- **Proof:** `seed/verify_seal.py` → `57/57 verified, 0 drifted, 0 missing`, exit 0.
