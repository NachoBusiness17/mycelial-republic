# AD3 — env contract landed (MiMo steal #1, AC8)

**Date:** 2026-09-29 · **Seat:** ZCode subagent (AD3) · **Owns:** `tools/env_contract.py`, `tests/test_env_contract.py`, this receipt · **No commit** (per mission).
**Steal:** MiMo-V2.6-RL-oss ships every env as `manifest.json` + rollout-time `reward.json` (AC3_MIMO.md); AC8_MIMO_VS_ESTATE.md names it steal #1. This landing re-expresses that contract for the estate's legality environments with the estate's physics: no docker, no wall clock, exact oracle.

## The format (the spec this tool owns)

`manifest.json` — schema `env_manifest.v1`, one per environment family (default family: `legality-water-graph-mountain-v1`):

| field | value / law |
|---|---|
| `env_id` | family name |
| `engine` / `engine_path` | `water_graph` / `mag/water_graph.py` (the real engine) |
| `engine_version` | git describe of the last commit touching the engine file (`d389326f0` at landing; tagless repo → `--always` abbrev) |
| `engine_sha256` | the byte pin — the ONLY field the drift check trusts (trust bytes, not reports) |
| `verifier` / `verifier_path` / `verifier_sha256` | `propagator` / `tools/legality_propagator.py`, pinned too (agreement law: propagator drift silently changes verdict semantics) |
| `task_shape` | `legality-water-graph-v1` — the gps capability key |
| `reward_style` | `rule` (MiMo's uniform style; ours is exact) |
| `timeout_sec` | `0` — the declared advantage: exact + instant, their 1800s verifier budget becomes no budget |
| `determinism` | `seeded` |
| `label_set` | the exact 5-way legality vocabulary |

`reward.json` — JSONL, schema `env_reward.v1`, one row per judged case: `case_id`, `task_shape`, `verdict` (binary 1/0 — exactly `CapabilityLedger.record_verdict`'s shape), `label` (the exact 5-way nuance gps's binary cannot carry), `evidence_hash` (64-hex, audit-walks the source like gwap's `row_sha256`). Canonical sorted-key bytes, no wall clock: identical calls → identical bytes.

## Laws enforced (fail-closed, reason-coded `EnvContractError`)

- **Freshness law:** `validate_manifest` recomputes live engine AND verifier sha256; `ENGINE_DRIFT` / `VERIFIER_DRIFT` / `*_MISSING` raise (CLI exit 1), never warn. The version string is never consulted.
- **No-guess feed law:** `feed_reward_file` is two-pass like `mag/gwap_to_gps.py` — every row validated + key-mapped (`model_id` or `case_to_model`, else `NO_KEY_MAP` / `UNMAPPED_CASE`) BEFORE the first `record_verdict`; any refusal leaves the gps ledger untouched (zero capability, zero verdict_log rows).
- **Row honesty:** `BAD_VERDICT` (non-binary; the 5-way label rides `label`), `BAD_EVIDENCE_HASH` (not 64-hex), `BAD_REWARD_ROW` (foreign shape), `BAD_MANIFEST` (foreign schema / missing field / `timeout_sec: true` — bool is an int subclass and still a lie).

## Evidence

`pytest -q tests/test_env_contract.py tests/test_gwap_to_gps.py` → **22 passed** (7 owned + 15 adjacent, untouched, 2026-09-29 ~HH:MM EDT run; 2.58s). Round-trip pins live bytes of `mag/water_graph.py` + `tools/legality_propagator.py`; drift test mutates copies and proves both refusal codes; gps-feed test lands 2/3 pass_rate via `record_verdict` and proves refusal atomicity. CLI exercised live: emit → validate exit 0; drifted engine copy → `REFUSED ENGINE_DRIFT`, exit 1.

## Findings while landing

- `git describe -- <path>` does not exist (describe reads object names, not pathspecs; rc 128 "Not a valid object name"). The file pin is two-step: `git log -1 --format=%H -- <file>`, then `describe --tags --always <sha>`. `--dirty` is also unusable with a commit-ish. Cause-and-evidence in `_git_describe`'s docstring.
- Live-repo note: both pinned files were mid-edit by sibling lanes during this window (`M mag/water_graph.py`, `M tools/legality_propagator.py`); pins capture working-tree bytes — the bytes that will actually run — so a re-emit mid-edit picks the newer bytes. That is the freshness law working, not a defect.
- Pins are byte-deterministic given identical engine bytes; `engine_version` is repo-state-dependent (tags/dirty) and human-facing only.

## Wiring

Nothing production depends on it yet — this is the format landing (per mission). Adoption seam: `tools/legality_dataset.py` could emit the manifest beside its `MANIFEST.json`, and any rollout harness could append `emit_reward` rows; `feed_reward_file` is the gps bridge. Wiring is a later window's call.

## Next-attempt design (if re-run needed)

Nothing to re-run; the landing is green. If extended: per-case `case_to_model` maps for multi-model legality rollouts, and a `--collect`-style patrol that re-validates every emitted manifest in `logs/` against live bytes on a schedule.
