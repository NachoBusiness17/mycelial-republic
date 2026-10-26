# SEED-RIB gap census (s2-20, 2026-09-28)

Instrument: raw census at `watch/inbox/burn_reset_20260927/flash50/_s220_scan.py` (byte-faithful port of `tools/seed_rib.py:40-51` classify_role, no subprocess spawns) writing `_s220_raw.json` (81,789 bytes); generated 2026-09-28T23:57:56Z. Subject: `watch/inbox/seed_rib_20260928/seed-rib/seed.json` (created_ts 2026-09-28T03:57:46Z, 92 entries, 87 inline / 5 pointer carriers, 419,791 bytes, law_refs 12), the seed `watch/inbox/SEED_RIB_CURRENT` points at (built 2026-09-28T05:26:00Z per the pointer row). All numbers below come from commands run in this session; the moment matters (census denominator law): the tree moved during 09-28 and part of this report is exactly that.

## 0. The seed fails its own verifier against the live tree right now

Ran: `./.venv/Scripts/python.exe tools/seed_rib.py verify --seed watch/inbox/seed_rib_20260928/seed-rib/seed.json --into /tmp/s220_seed_verify --source .` at scan time. Output: 3x `SEAL MISMATCH (pointer vs source)`, then `inline 87 hash-matched, pointers 2 source-checked / 0 UNRESOLVED, law_refs 12`, exit code 1.

- `AGENTS.md`: seed seal `85c4e49eb9c9` vs live `eda67bca212e` (live 16,671 bytes, mtime Sep 28 14:33; sealed 16,513)
- `tools/stealth_driver.py`: `c3cc4afadb2a` vs `3db01201fcb9` (live 37,814 B, mtime 13:05; sealed 27,500)
- `tools/stealth_fanout.py`: `547116fd4e64` vs `1f360c9fac28` (live 8,559 B, mtime 09:21; sealed 8,394)
- Matched: `mag/water_graph.py`, `mag/water_computer.py`.

`watch/inbox/SEED_RIB_REFRESH_20260928.md` records verify exit 0 at 05:26Z; the estate moved under 3 of the 5 sealed pointers in the ~14-20 hours after. A cold agent holding this seed plus the live estate gets "the seed and the world disagree" (spec section 3: that is a hard fail, someone moved bytes without re-sealing). The seed is stale, not corrupt: inline seals all hold.

## 1. Headline: the 09-28 refresh replaced the kernel, it did not extend it

The prior seed `watch/inbox/SEED_RIB_CURRENT_20260926.json` (created 2026-09-26T23:33:07Z, 13 entries, roles law 9 / doctrine 1 / boot 1 / pointer 2, law_refs 11) carried the law surface: all 9 `memory/law/*.md` plus `docs/DNA.md`, `memory/briefs/latest.md`, `AGENTS.md`, `tools/seed_rib.py`. The 09-28 build (per the refresh doc, `--file [law files] --glob [receipt globs]`) landed 78 BURN_* receipts from 09-27/09-28 plus 13 delta code/RIB files plus AGENTS.md: role census of the current seed is boot 1 / pointer 13 / receipt 78, and zero law-role, zero doctrine-role, zero ledger-role entries. 12 of the 13 files the 09-26 seed carried are gone from the current seed; the survivor (AGENTS.md) is the one whose seal drifted.

Net: a cold agent handed the CURRENT seed gets 2-day burn receipts and the 09-28 delta, and zero of the boot kernel (laws, doctrine, state, contracts). A cold agent served by `tools/seed_mcp.py` gets the opposite slice (section 4). Neither gets both.

## 2. The missing census (per tools/seed_rib.py inclusion criteria)

Groups are grounded in: spec `watch/inbox/SEED_RIB_FORMAT_v0_20260926.md` (section 2 budget law: inline set = laws, registry heads, doctrine, handoff pointers; section 4 law-surface mandate; "pointers fused here" list), the AGENTS.md load-order table and clippy named files, `tools/freshness_check.py:38-41` boot-doc list, and classify_role itself. inline_max 8192 (`tools/seed_rib.py:36,91`).

| group | candidates | in seed | missing | missing inline-eligible bytes |
|---|---|---|---|---|
| A: memory/law/* (spec s4 law surface) | 11 | 0 | 11 | 14,282 |
| A: spec fused pointers (ESSENTIALS_RESTORE, TWO_MACHINE_SYNC, the format spec) | 3 | 0 | 3 | 14,890 |
| B: AGENTS.md load-order + build-discipline docs | 14 | 1 (AGENTS.md, stale seal) | 13 | 21,169 |
| B: freshness gate boot docs | 4 | 0 | 4 | 9,911 |
| B: queue/handoff/* (classify_role boot role) | 116 | 0 | 116 | 243,251 |
| C: AGENTS.md operator-named files | 8 | 1 (RIB_DRIVING_LADDER) | 7 | 14,677 |
| D: memory/rib/*.md surface | 43 | 2 | 41 | 123,603 inline-eligible (147,261 B total) |
| E: 09-26 seed coverage dropped by 09-28 | 13 | 1 | 12 | 29,610 |

The highest-cost absences for a cold agent, all verified present on disk and absent from seed entries:

1. `memory/law/registry.json` (9,849 B) and the 9 law files (14,282 B total). Spec section 4: a seed that includes memory/law/ surfaces MUST carry or reference registry.json, and a seed without a law surface must declare `law_refs: []` "honestly rather than pointing at nothing". This seed declares law_refs 12 while carrying zero law bytes. The 12 ids DO all exist in the live registry (checked both directions: `law_refs not in registry: []`, `registry ids not attested: []`), but the verifier never checks law_refs at all (`tools/seed_rib.py:161` only prints the count), so nothing catches a seed whose attested laws ride on nothing. Both the 09-26 and 09-28 seeds omit the registry bytes; `seed_mcp.py` serves it live (`seed://law-registry`) which works only while an estate exists to serve from.
2. The AGENTS.md load-order rows 1-6: `docs/FRAMEWORK_LOAD.md` (13,309), `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md` (13,132), `docs/ref/MYCELIAL_SCIENCE_MAP.md` (12,875), `docs/ref/MAG_DIRECTION_ARTIFACT_v2.md` (13,682), `docs/ref/MAG_PROJECT_PROPOSAL.md` (16,216), `docs/ref/OPERATOR_CARD.md` (4,888). The seed carries AGENTS.md only as a sealed pointer, so the cold agent holds a hash promise for the one file that tells it what to read first, and none of the files.
3. State: `state/CURRENT.md` (3,353, live truth per AGENTS.md), `BOOT_4_7.md` (3,427), `state/START_BRIEF.md` (1,616), `state/HANDOFF.md` (1,515) - the exact four files `tools/freshness_check.py:38-41` gates on. All inline-eligible, all absent. Also `queue/todo.md` (36,212) and `HANDOFF_MAG_AGENT_TODOS.md` (14,103), load-order rows.
4. Ribs: AGENTS.md boot-order law says warm the ribs, "esp. RIB_FREE_USAGE_POLICY_20260823 + RIB_DRIVING_LADDER_20260928". The seed carries only DRIVING_LADDER (inline, seal holds); `memory/rib/RIB_FREE_USAGE_POLICY_20260823.md` (2,950 B, inline-eligible) is missing. 41 of 43 rib md files are missing.
5. Machine contracts: `watch/inbox/SHARED_SURFACE_CONTRACT.json` (3,791 B, the shared artifact boundary law) and `watch/inbox/INDEX.json` (466,153 B, "read first" root; pointer-eligible) - both absent. Same for `watch/inbox/ESSENTIALS_RESTORE.md` (1,693) and `watch/inbox/TWO_MACHINE_SYNC_20260919.md` (6,722), the two files the format spec names as the seed concept's own fused pointers, and the spec itself (6,475). A seed that does not carry its own format spec makes the consumer guess.
6. `queue/handoff/*`: 116 files, zero carried (243,251 B under the inline bar; heaviest `VERKLE_RIB.json` 2,226,441 and `CODE_MAP_RIB.md` 75,131 are pointer-eligible). classify_role assigns every one the boot role via the "handoff" substring (`tools/seed_rib.py:45`).
7. Smaller named gaps: `memory/attention.md` (40,441), `memory/live_from_grok.md` (60), `memory/warm_state.json` (908), `configs/lanes.yaml` (6,968), `configs/version_roadmap.yaml` (10,416), `docs/ref/releases/VERSION_REGISTRY.md` (6,695), `docs/DNA.md` (5,798, carried by 09-26, dropped).

## 3. Budget law is exceeded and the refresh's overflow note is wrong

Spec section 2 / falsifier (d): whole-fleet seed targets < 100,000 bytes, overflow must be named. Measured: raw inline payload 297,744 bytes (87 entries), sealed pointers 96,331 bytes (5), seed file 419,791 bytes on disk. `SEED_RIB_REFRESH_20260928.md` says "inline base64 inflates; actual content under cap" - false at raw-byte level: the inline content alone is ~3x the budget before any base64 tax. 78 receipts at ~3.4 KB each are the mass; receipts are "watch/inbox evidence" (receipt role), not the spec's inline kernel (laws, registry heads, doctrine, handoff pointers).

## 4. Split-brain: the MCP cold-agent surface serves the other seed

`tools/seed_mcp.py:44`: `DEFAULT_SEED = ... / "watch/inbox/SEED_RIB_CURRENT_20260926.json"` - hardcoded to the 09-26 seed. `tools/seed_mcp_cold_client.py:17` documents the same 09-26 path. Meanwhile `watch/inbox/SEED_RIB_CURRENT` (the named "current" pointer, untracked) points at the 09-28 seed. Result: an MCP cold agent gets the law kernel but not the 09-27/28 delta or receipts; an agent hand-carrying the current seed gets receipts and the delta but no law/doctrine/state kernel. No single surface gives both halves.

## 5. Structural notes

- The 09-28 carrier is JSON-only: `watch/inbox/seed_rib_20260928/seed-rib/` contains exactly `seed.json`. The v0.1 amendment (spec lines 104-127) makes the directory carrier (MANIFEST.sha256 + POINTERS.sha256 + kernel/law.heads.json + SEED_RIB.md) the preferred form; the 09-26 directory holds 61 files including build/cold-seat outputs and `.mimosa` scratch.
- Tracking: `git ls-files` shows only `watch/inbox/SEED_RIB_CURRENT_20260926.json` tracked. The current seed, `SEED_RIB_CURRENT`, and the refresh receipt are untracked-unignored (`git check-ignore` = NOT-IGNORED), so git history holds no record of the current seed.
- Receipt-stamp inconsistency: refresh doc says built 2026-09-28T05:26:00Z; the seed's own created_ts is 2026-09-28T03:57:46Z.
- Deliberate, not a gap: `memory/briefs/latest.md` is FROZEN per AGENTS.md ("must not be consumed as live"), so dropping it is defensible, though the refresh doc does not say so. The 78-receipt fan is a chosen 2-day slice of the receipt universe, not an oversight: kernel-surface rollup (scope: memory/law, memory/rib, docs, state, queue, configs, scripts, tools, mag, githooks, tests, watch/inbox, watch/board, root files) counts 12,355 receipt-role files / 6.39 GB, and a full-tree walk is infeasible here anyway (`.mimosa` alone holds 3,193,880 files; memory/ 318,623; mine/ 98,524).

## 6. What a cold agent would actually need (minimal fix list)

Boot-order shape per AGENTS.md (ribs, then state, then act), all inline-eligible sizes verified above:

1. Rebuild with the kernel re-attached: `--file` the 9 law mds + registry.json + CONSTITUTION.md + docs/DNA.md + OPERATOR_CARD.md + state/CURRENT.md + BOOT_4_7.md + state/START_BRIEF.md + SHARED_SURFACE_CONTRACT.json + ESSENTIALS_RESTORE.md + TWO_MACHINE_SYNC_20260919.md + the format spec + RIB_FREE_USAGE_POLICY + attention.md + warm_state.json + lanes.yaml, plus `--glob "docs/ref/MAG_*.md"` and `--glob "queue/handoff/*.json"` for the handoff pointers. Kernel addition is roughly 40 KB raw - fits the budget once the 78 BURN receipts move to pointers or drop (receipts are the budget eater, ~265 KB raw).
2. Carry `memory/law/registry.json` bytes (or add a POINTERS row for it) so law_refs attest against something in the seed; ideally make `tools/seed_rib.py` verify() check law_refs against a carried registry (today it cannot fail on phantom ids, `tools/seed_rib.py:159-161`).
3. Re-point `tools/seed_mcp.py:44` at SEED_RIB_CURRENT (read the pointer file) instead of the frozen 09-26 path, so the MCP surface and the current seed stop diverging.
4. Re-seal or re-build after the 09-28 AGENTS.md / stealth_driver / stealth_fanout edits, re-run verify `--source .`, and refresh `SEED_RIB_CURRENT` + the refresh receipt with the new created_ts.
5. Commit the seed + pointer + receipt, or gitignore them deliberately; today they are untracked-unignored and invisible to history.

Raw evidence: `_s220_raw.json` (group rows with bytes, sha256, mtime, would_inline, seed-carrier/seal-match per file) + `_s220_scan.py` beside this file in flash50.
