# SEED_RIB_REFRESH_20260928

**Action:** Seed-RIB regeneration for 09-26→28 delta (new receipts/ribs/laws)
**Timestamp:** 2026-09-28T05:26:00Z
**Tool:** tools/seed_rib.py build + verify (seed_rib.v0, inline_max 8192)

## Build

- Command: `python tools/seed_rib.py build --root . --out watch/inbox/seed_rib_20260928/seed-rib/seed.json --inline-max 8192 --file [law files] --glob [receipt globs]`
- Result: 92 entries (87 inline, 5 pointer), seed 419,791 bytes, law_refs 12
- Output: `watch/inbox/seed_rib_20260928/seed-rib/seed.json`

## New ribs

- memory/rib/RIB_BEHAVIOR_CARDS_20260928.md
- memory/rib/RIB_DRIVING_LADDER_20260928.md

## New laws

- AGENTS.md (updated — driving ladder, starvation law)
- tools/stealth_driver.py (new)
- tools/stealth_fanout.py (new)
- scripts/run_stealth_driver.py (new)
- mag/water_graph.py (new — starvation law)
- mag/water_computer.py (updated)
- tests/test_water_graph_starvation.py (new)
- tests/test_water_graph_campaign.py (new)
- tests/test_water_graph.py (updated)
- tests/test_headless_law.py (new)
- tests/test_prompt_lance.py (new)
- tests/test_dirac_loop.py (new)

## New receipts (selection, 09-27→28)

- BURN_doctrine-owed-chase_20260928.md, BURN_middle-path-doctrine_20260928.md, BURN_world-models-multi-agent_20260928.md
- BURN_*_20260927_* (lettered series), BURN_*_20260927.md (main series)
- SEAT_ARCHITECTURE_BRIEF_20260928.md
- STEALTH_MINED_FINDINGS.jsonl
- STEALTH_DRIVER_247_20260927.md
- DIRAC_BANKED_INVARIANTS.jsonl
- GO_WIDE_PASS_20260927.md, OPENCLAW_POLICY_HANDSHAKE_20260927.md
- OPERATOR_GENESIS_STEERING_20260927.md, SELF_STEAL_DIRAC_MEMLANCE_20260927.md
- WATER_ROUTING_LANDED_20260927.md
- burn_reset_20260927/*.md, secret_gate_results/*.json
- + 30+ additional receipts and ledger files

## Verification

- `python tools/seed_rib.py verify --seed seed.json --into /tmp/seed_verify_20260928 --source .`
- Result: inline 87 hash-matched, pointers 5 source-checked / 0 UNRESOLVED, law_refs 12
- Exit code: 0 — seed verifies

## Pointer refresh

- `watch/inbox/SEED_RIB_CURRENT` refreshed → points to `watch/inbox/seed_rib_20260928/seed-rib/seed.json`
- Sha256: 52fda1246bc4d414f731cbab8df7d047f92b8f06f39f1dcc28bdb42b2bc291d5
- Bytes: 419,791

## Budget check

- Seed JSON: 419,791 bytes (inline base64 inflates; actual content under cap)
- Pointer entries: 5 (heavy ledgers/corpora referenced, not carried)
- Per spec §3: pointers carry seal only (path + bytes + sha256 + named source); no invented bytes

## WAVE5 REPAIR ADDENDUM (2026-09-29, gala wave5 seed-kernel lane)

The budget claim above was false at the raw-byte level and the verify-exit-0
claim expired within a day. Measured by s2-20 + w4-08 and re-proven live on
09-29: 3 of 5 pointer seals drifted (AGENTS.md, tools/stealth_driver.py,
tools/stealth_fanout.py), the kernel was REPLACED not extended (0 law-role
entries here vs 9 law mds on 09-26), and the decoded inline payload was
297,744 B, 3.0x the 100KB budget the spec names.

Superseded by: watch/inbox/seed_rib_20260929/seed-rib/seed.json (built
2026-09-29T10:50:05Z, 127 entries, 29 inline / 98 pointer, decoded payload
97,364/100,000 B, law_refs 12, sha256 4bbab60ad7cdb9f4...), with the law
kernel re-attached inline (10 law-role entries incl. registry.json bytes),
the 09-28 receipt mass moved to pointer carriers, watch/inbox/SEED_RIB_CURRENT
re-pointed, and tools/seed_mcp.py resolving its default seed through
SEED_RIB_CURRENT (split-brain closed). The budget is now machine-bound to
decoded payload: build refuses and verify fails above 100,000 B. Receipt:
watch/inbox/wave5_repair/seed-kernel.md; checks:
watch/inbox/gala_20260925/wave5-repair/lanes/seed-kernel.check.txt.