# THE 50 / W7 / T31 - SettlementMaster full contract audit

Filed: 2026-09-25 by the T31 seat (re-audit). Supersedes the 2026-09-19 filing at this same path; corrections to that filing are listed in section 9. Task: "SettlementMaster full contract audit", `watch/inbox/THE_50_PROGRAM_20260918.md:50` (W7 GSTD / EXTERNAL).

Every command, greps, hashes, build and on-chain call below was executed during this ask (2026-09-25). All paths repo-relative unless marked on-chain. No em-dashes.

## 1. Subject map (what I read)

| Piece | Path |
|---|---|
| Contract source (new generation) | `reference/gstdcoin/contracts/SettlementMaster.tact` (320 lines) |
| Contract source (old generation) | `reference/gstdcoin/ai/contracts/SettlementMaster.tact` (279 lines) |
| Build artifact (new gen only) | `reference/gstdcoin/contracts/build/SettlementMaster/` |
| Deployment record | `reference/gstdcoin/contracts/deployment-mainnet.json` |
| Root ops scripts | `reference/gstdcoin/contracts/scripts/` (`deploy-mainnet.js`, `settle-rewards.ts`) |
| Old-gen deploy tree | `reference/gstdcoin/ai/contracts/` (scripts + tact.config.json, NO build dir) |
| Go client stub | `reference/gstdcoin/ai/backend/internal/settlement/client.go` |
| On-chain settlement service | `reference/gstdcoin/ai/backend/internal/services/onchain_settlement_service.go` |
| DB settlement service | `reference/gstdcoin/ai/backend/internal/services/settlement_service.go` |
| Simulated router service | `reference/gstdcoin/ai/backend/internal/services/settlement_router_service.go` |
| Routes | `reference/gstdcoin/ai/backend/internal/api/routes.go`, `routes_settlement.go` |
| Config defaults | `reference/gstdcoin/ai/backend/internal/config/config.go:103-104` |
| Frontend contract config | `reference/gstdcoin/ai/frontend/src/lib/config.ts:75` |
| Frontend settlement API | `reference/gstdcoin/ai/frontend/src/pages/api/v1/settlement/{batch,pending,clear}.ts` |
| A2A protocol | `reference/gstdcoin/A2A/src/gstd_a2a/protocols.py:41,75` |
| Verification doc (stale) | `reference/gstdcoin/ai/docs/CONTRACTS_VERIFICATION.md` |

Coverage check: full-repo grep for "SettlementMaster" over .md/.py/.json/.js/.ts ran to completion this ask (background grep, exit 0). The file set above covers every code hit; the remaining hits are fleet memory files and this program's own workflow definitions.

## 2. Contract source findings (new generation, the audited variant)

Splits verified sound: worker 85 / treasury 10 / protocol 5 with floor rounding, remainder to protocol (`SettlementMaster.tact:143-145`); `UpdateShares` requires sum == 100 and worker >= 50 (lines 239-240); replay guard on taskId map (lines 133-135); bonus capped by `baseRate * min(computeUnits, 1e9)` (lines 148-154); pause honored (line 130); zero-address worker rejected (line 131). TEP-74 transfer body (lines 201-210) is well formed: opcode 0xf8a7ea5, queryId, coins, dest, response_dest, payload bit, forward_ton, forward bit. Gas-reserve arithmetic (lines 138-140) is internally consistent (value > 0.1 TON, remainder >= minPayment 0.05). These are the good parts.

Findings, each with evidence:

1. **GATE (high) - stats overcount before sends.** `self.totalGSTDMinted += actualBonus` at line 158 runs before the sends; the bonus send (lines 195-212) uses `SendIgnoreErrors` with fixed `value: ton("0.12")` paid from contract balance. If the balance cannot fund it, the send is silently dropped while stats still count it. No correction path.
2. **GATE (medium) - WorkerPayment announces the uncapped bonus.** Line 170 carries `bonusGSTD: msg.gstdBonusAmount` while the capped `actualBonus` (lines 152-154) is what the jetton transfer moves. Worker-visible amount diverges from delivered amount.
3. **GATE (medium) - SetBaseRate has no upper bound.** Line 258 requires only `rate > 0`. A compromised owner key sets baseRate astronomically; the only real limit on bonuses is the pool wallet balance.
4. **GATE (high) - single-key custody, and the 5% leg pays the owner's own EOA.** `init` sets `gateway = owner` (line 101). Owner can reroute shares to 50/50/0 (UpdateShares), retarget treasury/protocol (UpdateAddresses, lines 248-253), and drain the pre-funded GSTD pool via SettleTask bonuses to any address. Verified live in section 5: on-chain `owner` and `protocolFee` cells decode to the identical hash `0:a45c594d...4a61a9`, which is exactly the `admin` address `UQCkXFlN...qQED` from `deployment-mainnet.json:6`. `phase2_todo` "Transfer SettlementMaster.owner to DAOVoting" is still open (deployment-mainnet.json:17).
5. **GATE (low) - observability holes.** Getters (lines 269-297) expose only stats, split, addresses, paused. No getter for `gateway`, `settledTasks`, `ownJettonWallet`, `minPayment`. Off-chain cannot precheck replay or read the current gateway (I could not verify on-chain whether SetGateway was ever called; see section 8).
6. **GATE (low) - bonus leg unfixable by bounce.** Jetton transfer sent with `bounce: false` (line 200); a mis-set `SetOwnJettonWallet` burns 0.12 TON per settle with no record. The worker TON leg has `bounce: true` plus a `bounced` handler (lines 216-226) - that part is correct.
7. **GATE (low) - dead message.** `MintWorkerReward` defined at lines 42-46 has no `receive(msg: MintWorkerReward)` anywhere in the file. Vestige of the old generation, misleading to integrators.
8. Naming: `totalGSTDMinted` (line 82) contradicts its own comment "from pool, not minted".

## 3. Two source generations, and three-way bytecode divergence

`diff reference/gstdcoin/contracts/SettlementMaster.tact reference/gstdcoin/ai/contracts/SettlementMaster.tact` = 94 diff lines (ran this ask). The old generation (`ai/contracts/`) has NO replay guard, NO bonus cap, NO computeUnits cap, NO zero-address worker check, NO ownJettonWallet; minPayment 0.1 TON (line 107); `totalGSTDMinted += msg.gstdBonusAmount` uncapped (line 132); step 4 mints the bonus by sending `MintWorkerReward` to the jetton master (lines 166-179). Both generations expose the same four getters and embed the same `bounced_worker_payment` string, so getter probes alone do not discriminate which generation is deployed.

**GATE (high) - the audited source builds to bytecode that matches neither the committed artifact nor the chain.** Ran `npm ci` (lockfile pins `@tact-lang/compiler` 1.6.13, `package-lock.json:152-154`; `package.json:13` floats `^1.5.0`) plus `npx tact --config tact.config.json --project SettlementMaster` on a copy of the contracts tree. Results, all computed this ask:

| Artifact | sha256 | size |
|---|---|---|
| Fresh build from audited source (tact 1.6.13) | `415867fa796868c3fca61e20218b0f223c74fcd102ceb916453c47e7e0ee8868` | 2728 B |
| In-tree `build/.../SettlementMaster.code.boc` (mtime 2026-08-05) | `d51f79b58b311793bc80ff00ff0947ed5459350a127fe8906de862beaeabd583` | 2342 B |
| On-chain code (toncenter, 2026-09-25) | `f3751997da9935b04b4df2506a3a55e6eae2a51f00d69af162a64201014371b3` | 2732 B |

Three divergent bytecodes, three sources of truth. The deploy predates the committed artifact by 28 days (2026-07-08 vs 2026-08-05), and the old-gen tree (`ai/contracts/`) has no build dir at all, so today `ai/contracts/scripts/deploy-mainnet.js` would abort at `loadContract` ("Contract bytecode not found", deploy-mainnet.js:46-53). No in-tree artifact can be tied to the deployed contract. Until a locked, tagged rebuild matches the chain, the deployed bytecode's guards are unverified: if the chain holds the old generation, there is no replay guard and no bonus cap on mainnet.

## 4. Backend findings (Go stack and API vs contract)

1. **GATE (critical) - the backend never sends SettleTask, and the one repo sender that exists cannot succeed.** Grep for `SettleTask` across `reference/gstdcoin/ai/backend` returns exactly one hit, a comment (`onchain_settlement_service.go:23`). The only backend client is `internal/settlement/client.go`, whose `Settle()` says "In production: submit TON transaction ... For now: track locally" (lines 132-133) and fabricates a tx hash `fmt.Sprintf("tx_%s_%d", ...)` (line 140). CORRECTION to the prior filing: a real sender does exist out of tree lane, `reference/gstdcoin/contracts/scripts/settle-rewards.ts:91-102`, which sends `SettleTask` from the deployer wallet. But it attaches `value: toNano('0.05')` (line 93), and the new generation requires `context().value > ton("0.1")` (`SettlementMaster.tact:138`); the old generation subtracts the same 0.1 reserve before a `minPayment` check of 0.1 (old line 107), so `0.05 - 0.1 < 0` fails there too. Also `computeUnits: BigInt(1)` and `taskId = BigInt(Date.now() + i)` (lines 84, 100): one CU per wallet per day. The only SettleTask path in the repo is dead on arrival against either generation.
2. **GATE (critical) - default contract address is not SettlementMaster.** `config.go:103` defaults `TON_CONTRACT_ADDRESS` to `EQDO0ab4mJsRn_aM7gVxaMnxtVsMKFJmuO9X55SbUqAj31g5`; the deployment record says SettlementMaster is `EQAhuR_cEaIkRqs4gvgXSD-Qw2FRUkkBUZQkTBrFT5n-ZrSS` (`deployment-mainnet.json:11`). Probed the default live this ask: active, balance 0, 1234-byte code, and `runGetMethod get_settlement_stats` returns exit_code 11 with stack error `0x11197` (getter absent). Meanwhile the frontend defaults to the correct address (`ai/frontend/src/lib/config.ts:75`). Frontend and backend point settlement at different contracts out of the box.
3. **GATE (high) - advertised withdraw flow does not exist in the contract.** `routes.go:487` publishes "Worker signs Withdraw message -> contract sends earnings"; `routes.go:538` instructs "Sign this Withdraw message in TonConnect to claim your earnings from the contract". The contract's entire message set (`SettlementMaster.tact:16-62`) contains no Withdraw and there is no per-user balance ledger. A worker who follows the instruction sends GSTD to the contract and can only recover it if the owner routes it back as a "bonus" (finding 2.4).
4. **GATE (high) - advertised deposit crediting does not exist.** `onchain_settlement_service.go:18` claims "User -> sends GSTD Jetton -> SettlementMaster contract -> balance credited". The contract has no deposit receiver and no balances map; it implements no jetton-notification receive at all. Deposits land in SettlementMaster's computed jetton wallet with no per-user record anywhere.
5. **GATE (high) - unauthenticated mint-shaped endpoint.** `SetupSettlementRoutes(v1, ...)` at `routes.go:1478` mounts POST `/bridge/settlement/route` (`routes_settlement.go:13-15`) on the public v1 group (`v1 := api.Group("/v1")` at `routes.go:410`; only `APIVersionMiddleware` is attached, line 408; the session/auth routes live on separate `protected`/`admin` groups). `settlement_router_service.go:80-95` "simulates" a STON.fi swap at hardcoded rates (USDT 2.0, TON 12.0), and `distributeReward` (lines 164-171) credits `user_balances` in Postgres, returning Status "completed_and_validated" (line 76). Anyone who can reach the endpoint prints GSTD balances.
6. **GATE (medium) - DB marked settled with no chain event.** `processBatch` inserts batches with status 'settled' and no tx hash (`onchain_settlement_service.go:318-332`); `GetStats` hardcodes `Mode: "contract_settle"` (line 368) although this path never touches the chain. The public `/monitor/onchain-settlement` endpoint (`routes.go:480-492`) therefore reports contract settlement that never happened.
7. **GATE (medium) - DB split drifts from contract split.** `settlement_service.go` boosts worker share above 85% under "Eternal Flame" (lines 99-124), routes platform-consumer payments 70/30 instead of 10/5 (lines 105-109), and skims 0.01 GSTD per payout for "Genesis Sync" repayment (lines 127-142). None of these exist in the contract; DB ledger and chain can never reconcile.
8. **GATE (low) - config mislabels SettlementMaster as the escrow.** `routes.go:381-382` returns `"escrow_contract": tonConfig.ContractAddress` with the comment "Escrow is the main contract", while `deployment-mainnet.json:14` lists a separate Escrow address.
9. **GATE (low) - frontend settlement API is a closed accrual loop.** `batch.ts` records KV accrual with node-registration and wallet-match checks and a 50 GSTD per-event cap (reasonable); `pending.ts:17-21` requires `x-admin-secret`; `clear.ts` clears balances. The comment says Phase 2 flushes on-chain "via /api/v1/settlement/trigger" - `trigger.ts` does not exist in the directory (listed this ask). The loop has no chain exit, consistent with finding 1.
10. **A2A note:** `protocols.py` registers `InvoiceTask` under `"settlement-invoice"` (lines 41, 75); grep over `A2A/src` shows no other reference. Dead protocol at the A2A layer.
11. Minor: deposit/withdraw payload handlers parse amount with `fmt.Sscanf` ignoring the error (`routes.go`, deposit and withdraw handlers around lines 507 and 533) - "1.5abc" parses as 1.5; "abc" yields 0 and is rejected by the positivity check. Cosmetic.

## 5. On-chain verification (all run this ask, 2026-09-25)

Contract under audit, from `deployment-mainnet.json:11`: `EQAhuR_cEaIkRqs4gvgXSD-Qw2FRUkkBUZQkTBrFT5n-ZrSS`, deployed 2026-07-08T12:12:06Z (79 days ago today).

| Check | Command | Result |
|---|---|---|
| Account state | `curl toncenter.com/api/v2/getAddressInformation?address=EQAhuR...` | state=active, balance=99261969 nanoTON (0.0992 TON), code present, 2732 B |
| Code lineage | decode code BOC (39 cells, 2586 raw bytes, node + @ton/core), substring search | contains `bounced_worker_payment`, `deposit`, `buyback` - same lineage as source |
| Stats getter | `curl -X POST .../runGetMethod` method=get_settlement_stats | exit_code 0, stack [0x0, 0x0, 0x0, 0xf4240]: totalSettled=0, totalGSTDMinted=0, taskCount=0, baseRate=1,000,000 (0.001 GSTD/CU, matches source line 110) |
| Split getter | same, method=get_revenue_split | [0x55, 0xa, 0x5] = 85/10/5 (matches source lines 106-108) |
| Pause getter | same, method=is_paused | 0x0 (not paused) |
| Addresses getter | same, method=get_addresses; cells decoded with @ton/core (tag=2 addr_std, wc=0) | gstdJetton `0:efe9c616...b59b2` = record's `EQDv6cYW...skTO`; treasury `0:1bb530ac...8affc` = record's `EQAbtTCs...Ii_`; protocolFee and owner byte-identical cells, hash `0:a45c594d...4a61a9` = record admin `UQCkXFlN...qQED` (converted and compared this ask) |
| Backend default address | `curl getAddressInformation?address=EQDO0ab4...` + runGetMethod get_settlement_stats | active, balance 0, 1234 B code, getter exit_code 11 - not a SettlementMaster |

Transport events this ask: none. All 8 toncenter calls returned `ok:true` on first attempt; no 429s were observed (the 2026-09-19 filing recorded one 429; it did not recur).

## 6. Triage: gate vs transport

**GATE (fix before real value flows, in order):**

1. Default `TON_CONTRACT_ADDRESS` points at a non-settlement contract and the frontend disagrees with the backend (4.2). One constant away from settling against the wrong code.
2. No working sender exists: the Go backend is a stub with fabricated tx hashes; the only repo SettleTask script attaches 0.05 TON against a > 0.1 TON requirement and dies on both generations; the DB marks batches settled with no chain event (4.1, 4.6).
3. Bytecode provenance: fresh locked build, committed artifact, and chain are three different bytecodes (section 3). Rebuild from a pinned compiler, diff against chain, then redeploy if unresolved. Until then, assume the deployed contract may be the unguarded old generation.
4. Withdraw and deposit-credit flows advertised to users have no contract counterpart; a worker who follows the public instructions donates GSTD to the contract (4.3, 4.4).
5. Unauthenticated `/bridge/settlement/route` mints DB balances at hardcoded rates (4.5).
6. Ownership: owner == gateway-at-init == protocolFee == admin EOA; the 5% "buyback and burn" leg pays the operator's own wallet until the phase2 DAO transfer (2.4, section 5).
7. Contract hardening: stats-before-sends overcount, uncapped SetBaseRate, uncapped bonus announced in WorkerPayment, dead MintWorkerReward message (2.1-2.3, 2.7).

**TRANSPORT (environment and ops, not code verdicts):**

1. Contract balance is 0.0992 TON, below the 0.12 TON the bonus leg tries to send per settle (source line 198). Even a correct SettleTask today would silently drop the bonus. Needs an admin refuel; the silent-drop shape itself is gate finding 2.1.
2. Dormancy: taskCount=0 and totalSettled=0, 79 days after deploy. There is no mainnet settlement history to forensically audit; the chain state corroborates the stub architecture rather than contradicting it.
3. toncenter public API rate limiting (429 observed by the prior filing, not this one). Monitoring needs an API key plus backoff. Not a code verdict.

## 7. Compile and toolchain checks actually run

- `npm ci` in a copy of `reference/gstdcoin/contracts` + `npx tact --config tact.config.json --project SettlementMaster`: SUCCESS (exit 0), producing sha256 `415867fa...` above. The copy lived outside the repo so the in-tree evidence boc was not overwritten.
- `go version`: "go: command not found" on this seat. No Go compilation or vet was possible; all Go findings are from source reading.

## 8. Not run, and why (honest skips)

- On-chain gateway identity: SettlementMaster has no gateway getter (source lines 269-297), so whether `SetGateway` was ever called is unverifiable from here. Init value is `owner` (line 101); treat the gateway as the owner EOA until proven otherwise.
- Transaction history pull for the contract address (toncenter getTransactions): not run; with taskCount=0 and last lt unchanged since the 2026-09-19 audit's balance observation, the audit value is nil. Last transaction lt `88831304000025` was observed in this ask's getAddressInformation for the record.
- gstdbot swarm (265 tree files): out of lane, that is task 34 (its receipt is `watch/inbox/THE50_W7_T34_GSTDBOT_AUDIT.md`, 2026-09-25 re-verification). TON explorer depth and alternate endpoints: task 32.
- Escrow contracts (`escrow.tact`, `escrow_complete.tact`): read only via config references; flagged in 4.8, not audited.

## 9. Corrections to the 2026-09-19 filing at this path

1. "Nothing ever sends SettleTask" is refined: `reference/gstdcoin/contracts/scripts/settle-rewards.ts` does send it, but with a value that fails both generations (section 4.1). The gate stands; the statement was too absolute.
2. `npx tact build` was listed as not run; this ask ran it against the locked 1.6.13 compiler and it materially changed the provenance picture from "deployed != repo artifact" to a three-way divergence including the audited source itself (section 3).
3. The old generation was attributed to `ai/contracts/` with a claim that its deploy script was the likely deployer; that tree has no build dir, so the deploy could not be reproduced from it today. Attribution of the deployed bytecode remains open.
4. Frontend layer added to the map: `config.ts:75` (correct default address) and the batch/pending/clear KV loop with a missing trigger endpoint (4.9). The prior filing did not cover it.
5. Dormancy figure updated from 73 to 79 days; no transport events this ask.
6. Line-count cites corrected 321 -> 320 and 280 -> 279 (wc -l on 2026-09-26, b2-01-the50-punch; T35's counts were already right). deployment-mainnet.json cite :18 -> :17 (line 17 is "Transfer SettlementMaster.owner to DAOVoting"; line 18 is the EcosystemTreasury item). Cause: wave-2 quality audit batch 6.1 (`watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md`).
7. gstdbot cross-reference corrected 267 files -> 265 tree files and "filed 2026-09-19" -> 2026-09-25 re-verification; find recount this date: 270 excl .git, 265 excl .git+.mimosa. Same audit cause, batch 6.1 stale-crossref defect.

## 10. Verdict

The audited contract source is a reasonable 85/10/5 settlement machine with real replay and cap guards, and the live deployment matches the configured economics on every getter I could read (85/10/5, baseRate 1e6, not paused, jetton and treasury addresses matching the deployment record). But the system around it does not connect to it: the backend defaults to a different address that is not SettlementMaster, no working code path sends SettleTask, the two user-facing flows the API advertises have no contract counterpart, the router endpoint mints database balances to anyone who asks, and the deployed bytecode can be attributed to neither in-tree source generation. The measured chain truth - taskCount=0, totalSettled=0, 79 days of dormancy, 0.0992 TON balance - is exactly what the stub architecture predicts. No real value should be routed through SettlementMaster until gate items 1 through 6 of section 6 are fixed.
