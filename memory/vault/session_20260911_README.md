# Session artifact vault — 2026-09-11

Chair 1's registration-vault doctrine, applied to today's window: every hold
becomes a hash hold. Every file created or modified in the repo today
(cutoff 2026-09-11 00:00 local) is registered in
`session_20260911_MANIFEST.json` with its sha256 and byte count. If a file
changes after registration, its row stops matching — the vault is the
tamper-evident snapshot of the day's work surface.

Exclusions per doctrine: `.git`, `node_modules`, `__pycache__`, `logs/`
telemetry, `memory/runs/trailer/`, and files over 50MB (those are named
below, not hashed). Secret-pattern scan ran over every artifact; flagged
rows carry `"review": true`. **Flags today: 0.**

## Counts (total 16,500 artifacts, ~400 MB hashed)

| group  | files  | note |
|--------|--------|------|
| docs   | 40     | watch/, watch/inbox/, docs/ |
| code   | 9      | mag/, tools/, backend/, scripts/, tests/ |
| vault  | 41     | memory/vault/ (this window writes here too) |
| config | 247    | journal/, configs/, state/ hand-edits |
| other  | 16,163 | 15,941 under memory/ — see surprise #1 |

## Three largest surprises

1. **memory/ is 96.6% of everything touched today.** 15,941 of 16,500 files:
   biography/ 10,946, briefs/ 2,681, ghost/ 1,477, runs/ 542. The chain and
   biography writes ARE the fleet's workload; the code surface is nearly
   still (9 files all day).
2. **Four files blew the 50MB ceiling and are named-but-not-hashed:**
   `memory/ingest/registry.jsonl` (1.12 GB), `memory/runs/ghost/trail.jsonl`
   (324 MB), `training/events.jsonl` + `memory/training/events.jsonl`
   (168 MB each). And `memory/decisions_log.jsonl` (50.7 MB) rode in just
   under the line — one byte of growth and the decision ledger goes
   invisible to the next vault run. The 50MB doctrine line needs a policy
   (chunk or exempt-list), not a silent skip.
3. **The vault is a write surface, and the secrets law is holding.** 41
   files under memory/vault/ changed during this same window, including the
   27.9 MB `astra_v2_companions/failure-ledger-frozen-prefix.jsonl` — while
   a key-material scan over all 16,500 artifacts returned zero flags.

Registered by LANE 1 of the 2026-09-11 grounding wave. Verify by re-hashing
any row: `sha256sum <file>` against the manifest.
