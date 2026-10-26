# P3 port receipt: tag-digest pinning + thinking-default read (port wave 2026-10-07)

Lane: day-7 mine fold, port-order P3. Operator laws held: `.venv\Scripts\python.exe` only,
no em/en-dashes in new bytes, no git commit.

## Proofs the build rides on (read first, both cards)

- Tags are mutable pointers: the reddit card's seat re-fetched the qwen3 registry manifests
  on 2026-10-07 and `4b` vs `4b-thinking` are byte-identical (steal 1,
  `watch/inbox/frontier_olm_2026-10-07/steal/open-local-language-models via reddit.md:14`,
  re-verification block at `:20-28`, artifacts `manifest_qwen3_4b.json` and
  `manifest_qwen3_4b-thinking.json` in the same dir). So a pin needs a digest column.
- The daemon advertises per-model thinking defaults (steal 2,
  `watch/inbox/frontier_olm_2026-10-07/steal/open-local-language-models.md:14-23`): three
  measured shapes, and the absent-key shape defaults to assume-ON, never OFF. Estate
  fixtures: `sweep/show_resp_gemma4.json:1` (structured), `sweep/show_resp_dsr1_15b.json:1`
  (capability without defaults), qwen2.5:7b absent (card line 21).

## Build 1: digest pinning (`mag/ollama_policy.py`)

- Pin surfaces unchanged (`mag/ollama_policy.py:16-18`); new beside them:
  `pin_digests()` reads `MAG_PIN_DIGESTS` as `tag=hex,tag=hex` at call time (sha256 prefix
  tolerated), `pinned_model_names()` = janitor + desk default + KEEP_ALIVE members,
  `list_tags()` maps GET /api/tags to tag and digest (digest parse at `:96`),
  `verify_pins()` at `:132` is the gate.
- Refusal shape: a pinned digest that differs from the installed digest, or a pinned tag
  missing from the daemon, lands in `refused` carrying tag, expected, actual, reason, and
  the gate returns ok false. Daemon-down with digest pins present fail-closes (a pinned
  identity must be provable); daemon-down with zero digest pins stays open.
- Migration path: with no digest pinned the gate is a warn-once stderr listing of the
  unpinned pins (once per unique set per process, `_warn_unpinned_once`), never a refusal.
- Modes: boot hook rides warm boot's existing verify branch
  (`mag/hermes_warm_boot.py:213-218` stamps `pin_verify` beside the AG5 chain gate); the
  enforcing gate with exit 1 is `python -m mag.ollama_policy --verify` (`main` at
  `mag/ollama_policy.py:331`).

## Build 2: thinking-default read

- `thinking_condition(model)` at `mag/ollama_policy.py:180` POSTs /api/show and normalizes
  all three shapes: structured (bool default to on/off, string level passthrough,
  unparseable default assumes ON), capability_only (assume ON), absent (assume ON);
  transport failure and HTTP errors also land on assume-ON. `thinking_conditions()` at
  `:227` is the per-pin ledger read.
- Consumption point patched: `resolve()` at `mag/agent_state_router.py:116` now routes
  through `_apply_daemon_thinking()` at `:85`. A state whose model is a pinned local tag
  gets its thinking_level from the daemon plus the full condition row; remote models keep
  the hand-curated value. Either way `thinking_source` is stamped (daemon,
  daemon_unreachable_assume_on, or hand) so verdict rows record provenance. The spec copy
  never mutates the state table. Downstream consumers (`mag/self_drive.py:177`,
  `mag/session_route.py:70`) read thinking_level as before, no change needed there.

## Live daemon check (real run this round, 0.34.3)

`python -m mag.ollama_policy --verify` exited 0 with all three pins listed unpinned
(gemma:2b, gemma4-desk, qwen-desk) and the warn printed once. `--thinking` read the ledger:
gemma4-desk structured default true (matches the sweep fixture byte-for-byte in shape),
gemma:2b and qwen-desk both absent-key assume-ON. That is the migration path working on
the live fleet; pinning digests is now one env line per tag.

## Tests

`tests/test_pin_digest_thinking.py` (new, 276 lines, 17 tests, all daemon HTTP mocked):
three shape fixtures plus the off and string-level arms of structured, the mismatch
refusal with tag, expected, actual asserted, sha256-prefix normalization, not-installed
refusal, daemon-down fail-closed, unpinned warn-once (stderr counted via capsys), CLI exit
codes 1 and 0, the three consumption-point cases, and table-mutation guard.

## Gates

- Scoped run: 17 new tests plus the neighboring suites
  (`tests/test_local_gpu_probes.py`, `tests/test_ag5_tip_verify.py`,
  `tests/test_ah5_warmboot.py`, `tests/test_t1w1_ractor_fixes.py`) = 65 passed; consumer
  suites (session_route, desk, local_scheduler, local_pulse, ghost, frontier advisor and
  council) = 97 passed.
- Ratchet `tools/violation_ratchet.py check --changed`: zero hits in the four lane files
  (ollama_policy, agent_state_router, hermes_warm_boot, the new test file). The run reports
  NEW=4 but all four sit in `mag/contamination_tripwire.py` and `tools/code_execution.py`,
  sibling-lane working-tree debt from other seats, not this lane's; accepting or fixing
  those is an operator call, not folded here. Full-suite result appended below when the
  background run lands.
- Full suite: see the APPEND line at the bottom.

## OWED / migration

- No digest is pinned yet on the fleet (the live run above is the proof); the operator
  pins via `MAG_PIN_DIGESTS="gemma:2b=<hex>,..."` using the digests /api/tags reports.
- Other tag surfaces named by the card (`mag/lanes.py:45,48`, `mag/task_router.py:38,147`)
  still consume bare tag strings; they route through the same pin names, so the gate
  covers them transitively, but they hold no digest column of their own (P-lane overlap,
  left to the operator's fold order).
- Boot wiring covers `--verify` boots; the plain (non-verify) boot path still does not
  gate, by design, so a daemon-less box boots.
