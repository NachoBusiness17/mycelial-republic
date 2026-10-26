# CHAIN_HARDEN_ITER2_20261020

Applied 2026-10-20 (America/New_York). Iteration after ~22h of the 2026-10-19 five fixes.
No git commit. No push. Live chain not rewritten or truncated.
Working baseline today: n=13138, full sha256 33311208952768dab48d2ff3cea397e02b3494cf17c741915b0d296de2b74d92.
Sealed 10/16 prefix stays history. No correction/restore rows. Checkpoint only after a clean week.

## 1. Proof result (item 1)

| Check | Result |
|-------|--------|
| Yesterday full-file sha (2026-10-19 fixes) | d887ccc223c97b311da2c91a4f08ad0252a754ebed0daddd605e665654f522b3 |
| Today full-file sha | 33311208952768dab48d2ff3cea397e02b3494cf17c741915b0d296de2b74d92 |
| Rows today | 13138 (= 13135 + 3 appends) |
| Byte-prefix sha of first 13135 rows | d887ccc223c97b311da2c91a4f08ad0252a754ebed0daddd605e665654f522b3 |
| Match yesterday full file | YES (append-only growth; no rewrite of rows 1..13135) |
| Row 13135 leaf prefix | f6cb5e7b... (matches spot check) |

Proof JSON: %TEMP%\magfix20261020\PROOF_CHAIN_20261020.json

## Per-item status

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Full proof vs yesterday | done | prefix of 13135 rows == yesterday full sha; +3 appends only |
| 2 | Stuck-red prefix check | done | chain_prefix_seal_check now HISTORICAL_RECORD_ONLY (exit 0). Rolling tools/chain_no_rewrite_check.py seeded at today tip; red only on new rewrite. Hooked in ratchet_daily.ps1 |
| 3 | Env-bit bypass | done | MAG_ALLOW_CHAIN_REWRITE=1 AND fresh state/chain_rewrite_approval.json (expires_utc) or held chain:biography lease. Audit line to memory/biography/chain_rewrite_audit.jsonl. Flag scan + redboard section via chain_harden_patrol |
| 4 | ACL SIDs | partial | Identified: CodexSandboxUsers = CodexSandboxOffline/Online (sandbox seats). 5x S-1-5-21-* = UNRESOLVED foreign SIDs (not this PC domain 717218263), inherited from biography dir; icacls cannot map them; Set-Acl needs SeSecurityPrivilege (denied). Soft DENY WD + RX,AD applied for foste + CodexSandboxUsers. SYSTEM/Admins untouched. DENY DELETE not applied (breaks Python open; noted). os.replace still bypasses file ACL |
| 5 | Lab /proc patrol | done | chain_harden_patrol uses docker exec /proc/*/cmdline (+ docker top fallback). lab_ok=True, MAG_DISABLE_LAB=1. In ratchet_daily |
| 6 | Other writers | done/listed | Gated: diary_node (append not rewrite), merkle_sized.migrate, repair_verkle_chain.apply, chain_repair dual gate, verkle_compaction/_rewrite_chain already gated. Listed read-mostly: verify_verkle_full, knot_rehash_patrol, chain_guard, usage_digest amend path uses _rewrite_chain (gated) |

## Fork and rehydration

### Prior art (dated, verified at HEAD 2026-10-20)

| Artifact | Date | At HEAD | Role |
|----------|------|---------|------|
| watch/inbox/CHAIN_RESTORE_20261015.md Option A | 2026-10-15/16 | yes (mtime 2026-10-16) | Restored 12016 = backup 11218 + 411 lost-window from knot files + 387 post-overwrite; candidate in %TEMP%\magrestore; historically swapped under lock |
| /workspace/mag-archaeology-oct/restore/build_candidate.py | 2026-10-14/15 | archaeology copy | Builds candidate chain in TEMP only; never touches live |
| scripts/verify_verkle_full.py | 2026-10-03 | yes | Read-only leaf recompute from knots + merkle roots |
| mag/bintree_v2.shadow_append | 2026-10-17 | yes | Parallel shadow strand; not the live law |
| mag/verkle_knot.py PURE APPEND / Option A incremental | 2026-08-16 note in code | yes | Append does not require full rewrite |
| tools/superseded_wire.py + operator-corrections supersede | 2026-10-03..07 | yes | Supersede as append/graph fact, not swap |
| F13_fork_demo.json (rib_fork.v1) | 2026-10-01 | yes | Fork demo pattern (rib, not chain) |

Ponytail: existing verifier + build_candidate already do most of fork-in-TEMP + knot rehydration. Oct 15 Option A ended in a SWAP; this iteration reframes rejoin as APPEND-only weave (never swap).

### Reused vs new

| Item | Reused/New | Staleness |
|------|------------|-----------|
| verify_verkle_full leaf recipes | reused | 2026-10-03 HEAD |
| build_candidate TEMP-only law | reused (pattern) | archaeology; not in repo tree |
| bintree shadow parallel strand | reused (concept) | chain_v2_shadow still false in compose path |
| tools/chain_fork_rehydrate.py | NEW | thin weave: fork jsonl in %TEMP%/magfork_*, divergence.json; RO on live |
| tools/chain_no_rewrite_check.py | NEW | rolling baseline state/chain_no_rewrite_baseline.json |
| tools/chain_harden_patrol.py | NEW | lab /proc + flag scan -> state/chain_harden_alerts.json |
| Dual gate in verkle_knot | extended | approval file + audit |
| ratchet_daily hooks | extended | no new schedule |

### Smoke

- fork --limit 50: leaf_ok=50 dangling=0 divergences=0 out=%TEMP%\magfork_20261020_smoke
- NO-REWRITE: SEEDED at 13138 / 33311208...
- PREFIX: HISTORICAL_RECORD_ONLY (exit 0)
- HARDEN-PATROL: red=False lab_ok=True flag_hits=0

### Hostile pass (fork/rehydrate)

1. Fork tool keeps dangling rows' live leaf_hash (does not invent). A hostile knot rewrite that matches stored leaf_hash is invisible until recipe mismatch.
2. Weave report is not yet on a schedule (by design: no new daemon); operator runs tools/chain_fork_rehydrate.py or hooks later.
3. Rejoin-by-append is documented law only; no automatic correction rows (matches user: do not fix shit that breaks over and over).
4. Full-chain fork of 13k+ rows is slow; --limit for smoke. Production weave should resume/checkpoint.

## Tests

34 passed: test_chain_harden_iter2_20261020 + test_chain_rewrite_gate_20261019 + test_ah19_append_leaves + test_chain_byte_exact_io + test_verkle_lock_heartbeat.

## Remaining holes (hostile)

1. Orphan foreign SIDs still (M) on the chain file; cannot DENY without SeSecurityPrivilege / resolvable accounts. App dual-gate is the real rail.
2. os.replace / container-as-root still bypass NTFS soft ACL.
3. Approval file is a single JSON under state/; theft of a fresh approval + env flag = rewrite. Keep expiry short; audit jsonl is append-only but not ACL-hardened.
4. usage_digest / verkle_compaction still call _rewrite_chain (now dual-gated) - operator must not leave a long-lived approval.
5. ratchet will fail closed if harden patrol cannot docker exec (lab check error -> ok=False). Accept or add allowlist later.
6. No week-long checkpoint yet (intentionally deferred).

## Backups / rollback

- Backups: %TEMP%\magfix20261020\ + BACKUP_SHA256.txt + ACL saves + PROOF_CHAIN_20261020.json
- Rollback: powershell -File %TEMP%\magfix20261020\rollback.ps1

## Receipt paths

- watch\inbox\CHAIN_HARDEN_ITER2_20261020.md
- /workspace/mag-audit-20261019/CHAIN_HARDEN_ITER2_20261020.md
