# GSTD SettlementMaster V2 -> V3 Migration Checklist (F13-F16 Hardening)

- **Date:** 2026-10-17
- **Work Order:** `WO-SETTLEMENT-V3-MIGRATION-CHECKLIST-20261017`
- **Multi-Band Convergence:** Synthesized from 4 independent `bob` free-lane executions (`dots-studio/dots-3-note-preview`, `liquid/lfm-2.5-2.6b`, `nvidia/nemotron-3.5-super-vl`, `nvidia/nemotron-3.5-lightning`) + `AUDIT_GSTD_GITHUB_20261012.md` & `FOLD_ANTIGRAVITY_COUNTERAUDIT_20261014.md`.
- **Gate:** Operator-held (`[operator]` TON mainnet keys & multisig). Do **not** fund the bonus pool until V3 is deployed and verified against all 4 audit findings below.

---

## 1. Security Findings Closed by V3 (`SettlementMasterV3.tact`)

1. **F13 (CRITICAL — Unsigned Payout Fields in Quorum Digest):**
   - **Defect in V2:** `verifyQuorum` signed only `taskId || workerAddr || resultHash`, leaving `computeUnits` / `payoutAmount` attacker-supplied (allowing up to `1,000,000 GSTD` bonus-pool drain in a single tx).
   - **V3 Fix:** Versioned domain-separated attestation digest:
     `SHA256("GSTD_SM_V3" || chainId || contractAddr || taskId || workerAddr || artifact_sha256 || computeUnits || payoutNanoGSTD || nonce)`.
2. **F14 (HIGH — TON Gas Deficit on Bonus Settlements):**
   - **Defect in V2:** Bonus payouts forwarded `0.02+ TON` per settlement without deducting from incoming value or checking contract reserve, draining TON balance to freeze.
   - **V3 Fix:** Enforce `MIN_TON_RESERVE = ton("0.5")` via `nativeReserve(MIN_TON_RESERVE, 0)` and require `context().value >= gasConsumption + forwardTonAmount`.
3. **F15 (HIGH — `appId` Shell Interpolation in Node Manager):**
   - **Defect in V2 (`manager.ts:1347`):** `appId` passed into `docker rm/run` lifecycle commands without strict allowlist validation.
   - **V3 Fix:** Enforce `/^[a-z0-9][a-z0-9_-]{0,62}$/` regex allowlist on both `appId` and `volName` at manifest ingest and immediately before container spawn.
4. **F16 (MEDIUM-HIGH — `ClaimUptime` Cross-Deployment Voucher Replay):**
   - **Defect in V2:** Uptime vouchers lacked `contractAddress` and `chainId` binding.
   - **V3 Fix:** Bind `contractAddress`, `chainId`, and monotonic `epochId` into the `ClaimUptime` signed payload and verify attestor pubkey against the active `DAOVotingV2` registry.

---

## 2. Phase A — Pre-Flight Verification Checklist (Fail-Closed)

All 8 checks must return **PASS** before executing Step 1. Any failure halts migration immediately:

| # | Check | Target / Command | Pass Criterion |
|---:|---|---|---|
| 1 | **Mainnet RPC Sync** | `tonclient.getMasterchainInfo()` | `workchain == 0`, seqno lag `< 15s` |
| 2 | **V2 Float Invariant** | `get_wallet_balance(<V2_JETTON_WALLET>)` | Exact `499_000_000_000` nano-GSTD (`499 GSTD`), `0` uncommitted settlements |
| 3 | **In-Flight Queue Drain** | `get_active_payout_count(<SM_V2_ADDR>)` | `0` active payouts |
| 4 | **F13 Positive/Negative Vectors** | `npx jest test/settlement_v3_f13.spec.ts` | Valid V3 digest passes; mutated `computeUnits` (+1 nano-GSTD) reverts with `ERR_INVALID_QUORUM_SIGNATURE` |
| 5 | **F14 Gas Reserve Vector** | `npx jest test/settlement_v3_f14.spec.ts` | Settlement with low `msg.value` reverts before touching contract's `0.5 TON` reserve |
| 6 | **F15 Lifecycle Allowlist** | `npx jest test/manager_f15.spec.ts` | `appId` containing `;`, `$()`, or whitespace throws `ERR_INVALID_APP_ID` |
| 7 | **F16 Replay Vector** | `npx jest test/uptime_f16.spec.ts` | V2 voucher replayed against V3 address reverts with `ERR_DOMAIN_MISMATCH` |
| 8 | **Gas & Custody Readiness** | Deployer `>= 1.5 TON`, Custody `<CUSTODY_ADDR>` whitelisted | Verified on-chain |

---

## 3. Phase B — 10-Step Atomic Cutover & Rollback Runbook

1. **Snapshot V2 State:** Record `v2_seqno`, `v2_jetton_balance` (`499 GSTD`), and `v2_code_hash` into `state/gstd_v3_cutover_snapshot.json`.
2. **Pause V2 Intake:** Execute `emergency-pause-v2.ts` (`pause_active == true`). Verify subsequent test settlement reverts with `ERR_CONTRACT_PAUSED`.
3. **Verify Post-Pause Float:** Re-query `<V2_JETTON_WALLET>` balance; fail-close if balance `!= 499 GSTD`.
4. **Deploy `DAOVotingV2` & `SettlementMasterV3`:** Deploy compiled V3 BOC to TON Mainnet workchain 0; verify on-chain `code_hash` matches local build manifest.
5. **Register V3 Attestor Quorum:** Register active attestor public keys under the `"GSTD_SM_V3"` domain separator.
6. **Dry-Run Canary Settlement (1 nano-GSTD):** Submit a 3-witness signed V3 settlement for `1` nano-GSTD; verify exact payout and `nativeReserve` retention.
7. **Submit Tampered F13 Canary (Must Revert):** Replay the canary signature with `computeUnits + 1`; confirm on-chain revert (`exit_code != 0`).
8. **Migrate 499 GSTD Float:** Execute multisig transfer of `499 GSTD` from `<V2_JETTON_WALLET>` to `<V3_JETTON_WALLET>` (with `<CUSTODY_ADDR>` as time-locked rollback target).
9. **Repoint SuperNodes (`v3.4.0-patched`):** Update `SETTLEMENT_MASTER_ADDR` in `seats/{pixel,t90}/` and `desktop` `gstd-node` env; restart nodes.
10. **Mint Tails Ledger Receipt:** Record the cutover tx hash and canary revert tx hash as a verified row in `tails.jsonl`.
