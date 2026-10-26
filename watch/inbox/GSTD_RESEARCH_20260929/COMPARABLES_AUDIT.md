# GSTD COMPARABLES AUDIT (2026-09-29)

Half 2 of the GSTD research project. Companion to `watch/inbox/GSTD_FORENSICS_20260918.md`
(read first). Question answered here: **where does GSTD's development complexity rank
against comparable tokens, including scam-grade controls?**

Method: mechanism-inventory rubric derived from the forensics findings, GSTD scored from
the local clone (file receipts named per score), 12 comparables scored on the same rubric
from fetched public pages (URL per claim), matrix + rank + tri-state verdict.

Evidence boundary, stated up front:

- Local side: `reference/gstdcoin/` clones are 1-commit squash clones (each repo's git log
  shows exactly 1 commit, last dated 2026-07-23; contracts record a "Phase 1 mainnet
  deployment" commit dated 2026-07-08). Upstream contributor counts and commit history are
  NOT recoverable locally; the development census is files + LOC only.
- Live side: two explorer point-checks on 2026-09-29 via tonviewer.com (URLs below).
- The forensics file's "last upstream push 2026-03-31" predates these clone heads; the
  clone is fresher than the forensics note assumed.

## Part 1: The rubric

Twelve mechanisms, derived from the forensics inventory. Scores: **0** = absent;
**0.5** = written (code exists, unverified in production) or thin/claimed-only;
**1.0** = live with public evidence (deployed contract, running network, shipped artifact).
Max 12.0. Two axes are reported: **breadth** (total) and **depth** (share of rows at 1.0).
Depth is the honesty axis: a paper machine scores breadth and fails depth.

| # | Mechanism | What earns 1.0 |
|---|---|---|
| R1 | Identity / verification layer | On-chain attestation of what a node IS |
| R2 | Peer policing | Participants report each other with evidence |
| R3 | Slashing economics | Escalating enforced penalties on stake |
| R4 | Settlement economics | Payment flow contract, live |
| R5 | Buyback / burn | Programmatic value-accrual sink, documented |
| R6 | DAO governance | Token-holder voting with real authority |
| R7 | Treasury architecture | Dedicated treasury instrument |
| R8 | Escrow | Dispute-safe task payment path |
| R9 | Bridge | Cross-chain transfer, live |
| R10 | Autonomy / agent engine | Self-bootstrapping agent population or framework |
| R11 | Client / tooling | SDK, CLI, bot, web, MCP surface |
| R12 | Operational polish | Tests, audits, deployment records, honest status docs |

## Part 2: GSTD scored from the local clone

Local census (excludes node_modules, .git, lockfiles; `wc -l` over code/config/doc text):

| Repo | Files | LOC |
|---|---|---|
| A2A | 82 | ~11,725 |
| ai (platform: backend, frontend, gstd-mcp-server, agents, docker, nginx) | 877 | ~53,536 |
| contracts (Tact) | 89 | ~25,909 |
| gstd-bridge | 27 | ~333 |
| gstdbot | 270 | ~72,657 |
| web | 64 | ~6,590 |
| **Total** | **1,409** | **~170,750** |

Tact contracts (13): AgentRegistry, DAOVoting, EcosystemTreasury, GSTDJetton,
SettlementMaster, SettlementRouter, SovereignVault, TreasuryGold, escrow, escrow_complete,
naas/ProviderRegistry, naas/SlashMechanics, bridge/ton/GstdBridge.

Deployment truth (`reference/gstdcoin/contracts/deployment-mainnet.json`, phase 1,
2026-07-08): GSTDJetton, EcosystemTreasury, SettlementMaster, Escrow deployed.
phase2_todo explicitly lists: Deploy DAOVoting, Deploy AgentRegistry, transfer
SettlementMaster.owner and EcosystemTreasury.owner to DAOVoting, deploy TreasuryGold.
phase3_todo: GstdBridge, ProviderRegistry ("fix Jetton integration first"),
SlashMechanics ("fix message type mismatch first"). Two addresses explorer-verified on
2026-09-29: SettlementMaster Active with balance 0.0992 GRAM (~$0.15)
(https://tonviewer.com/EQAhuR_cEaIkRqs4gvgXSD-Qw2FRUkkBUZQkTBrFT5n-ZrSS); GSTDJetton
Active, name "Gold Standard", symbol GSTD, max supply 1,000,000,000, 206 holders, price
$0.00005, contract balance 4.24 GRAM (~$6.59)
(https://tonviewer.com/EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO). Implied fully
diluted valuation at that price: ~$50,000.

| Row | Score | Evidence (local file receipt) |
|---|---|---|
| R1 identity | 0.5 | Genesis Lock, SHA-256 of binary manifest, owner-set hash: `contracts/AgentRegistry.tact`. Written, compiled (build artifacts present). Not deployed (phase2_todo). |
| R2 peer policing | 0.5 | ReportGenesisViolation with evidenceHash, reputation deltas: `contracts/AgentRegistry.tact`. Not deployed. |
| R3 slashing | 0.5 | Full ladder, downtime 0.1% / 1h 1% / wrong-RPC 2% (10% challenger, 90% burned) / 24h 5% + downgrade / proven fraud 100%: `contracts/naas/SlashMechanics.tact` (header comment). phase3, known message-type bug. |
| R4 settlement | 1.0 | 85/10/5 split, gateway-authoritative quality scores, EmergencyPause: `contracts/SettlementMaster.tact` (workerShare=85 at line 106). Deployed 2026-07-08 and explorer-Active. Caveat: near-zero balance says the economy is idle; the contract is live, the flow is not evidenced. |
| R5 buyback/burn | 0.5 | 5% path sends "buyback" to protocolFee address in the deployed `contracts/SettlementMaster.tact` (line 183 onward). Sink contract TreasuryGold written but undeployed (phase2). |
| R6 DAO | 0.5 | `contracts/DAOVoting.tact` + compiled Proposal/DAOVoting build docs. Undeployed; owner transfers to it are phase2_todo, not done. |
| R7 treasury | 0.5 | EcosystemTreasury deployed + Active (~$0.15 balance). TreasuryGold (the substantive half) undeployed. Half the architecture exists on chain. |
| R8 escrow | 0.5 | `contracts/escrow.tact`, `contracts/escrow_complete.tact` (two iterations); Escrow listed in the phase-1 record. Address not independently explorer-verified by this audit. |
| R9 bridge | 0.5 | `contracts/bridge/ton/GstdBridge.tact` written; `gstd-bridge/` is 27 files / 333 LOC of status docs; phase3, self-declared deferred. |
| R10 autonomy engine | 0.5 | `A2A/src/gstd_a2a/sovereign_autonomy.py`, starter kit, CLI (`A2A/tools/gstd-cli.py`), OpenClaw bridge, swarm client: ~11.7k LOC. No evidence of a live agent population in the clone. |
| R11 client/tooling | 1.0 | gstdbot ~72.7k LOC (auth-gated destructive endpoints per its 2026-07-23 git log), ai/ platform with MCP server + backend + frontend + docker + nginx (~53.5k LOC), web ~6.6k LOC. Shipped artifact class. |
| R12 polish | 0.5 | SECURITY.md, STATUS.md, honest status disclaimers (gstd-bridge git log 2026-07-23), deployment record, CI config. Against: **zero committed contract tests** (`contracts/` has only `scripts/deploy-testnet.ts`; CLAUDE.md claims `npx blueprint test` exists but no test files are in the tree), phase2/3 unfinished, 1-commit squash history. |

**GSTD total: 6.5 / 12. Depth: 2 of 12 rows at 1.0 (17%).**

## Part 3: The comparables

Retrieval caveat: the search backend rate-limited repeatedly during this audit; every score
below rests only on the fetched pages cited, or on clearly attributed Wikipedia articles.
Where public docs were thin, the row is scored at what the fetched page supports and the
thinness is named. The intended "TON-native AI-agent token" slot found no well-documented
candidate in retrievable public sources (docs.ton.org's AI-in-TON page returned 404 on
fetch); Toncoin is included as the L1 context row instead.

### Class A: AI-agent protocol tokens

**Virtuals Protocol (VIRTUAL)**, Base. Agent launchpad and "society of AI agents": agents
with identity, wallets, payroll (EconomyOS), agent-hires-agent commerce (ACP), tokenized
agents, VIRTUAL staking (veVIRTUAL), AI Council governance described as upcoming
(https://virtuals.io/). Third-party summaries describe fee-funded buyback-and-burn and a
59/100 "BB" tokenomics rating, but the fetched page itself is silent on buyback mechanics
and the audit URL was not retrievable, so R5 is scored at 0.5 flagged thin. Scored:
R1 0.5 (credentials claimed in EconomyOS), R4 0.5 (trading fees, ACP commerce), R5 0.5
(thin), R6 0.5 (AI Council upcoming), R7 0.5, R9 0.5, R10 1.0, R11 1.0 (launchpad,
capital markets), R12 1.0. **Total 6.0. Depth 3/12.**

**elizaOS (ELIZA, ex ai16z)**, Solana. The framework is the most-developed agent artifact
in the set: 25,230+ commits, 19.5k stars, TypeScript monorepo, model-agnostic runtime,
plugins, desktop/mobile bridges, local inference, non-custodial wallets with approval
boundaries (https://github.com/elizaOS/eliza). The README contains NO token and NO DAO;
press summaries report the successor token at a ~97% drawdown with founder statements
depegging it (search-summary attribution only, no citable URL retrieved). The code is the
product; the token is a sticker. Scored: R1 0.5 (wallet approval boundaries), R10 1.0,
R11 1.0, R12 1.0. **Total 3.5. Depth 3/12.**

**Fetch.ai / ASI (FET)**. Autonomous economic agents at scale: "2.7 million agents",
uAgents framework, Agentverse marketplace, ASI:One, brand verification path (Fetch
Business "get verified") (https://fetch.ai/). Token mechanics (staking, payments) are not
detailed on the fetched page. Scored: R1 0.5 (agent verification), R4 0.5 (marketplace
implied), R6 0.5, R9 0.5, R10 1.0, R11 1.0, R12 1.0. **Total 5.0. Depth 3/12.**

**Bittensor (TAO)**. Scored strictly from the whitepaper
(https://bittensor.com/whitepaper): peers rank each other, Yuma consensus aggregates
scores into emissions, bonds track trust, dishonest subgraphs "decay to irrelevance" by
superlinear stake gradient, consensus peg detects off-consensus inflation. This is the
purest peer-policing design in the set, and it has no buyback, treasury, escrow, or bridge
in the cited text. Scored: R1 0.5, R2 1.0, R3 0.5 (economic decay, not slashing), R4 0.5
(emissions), R6 0.5, R10 0.5, R11 1.0 (SDK/subnet ecosystem, outside the fetched text but
non-controversial public artifact), R12 1.0. **Total 5.5. Depth 2/12.**

### Class B: Established infra (the high bar)

**Akash (AKT)**, Cosmos L1. From https://akash.network/token/: AKT governs, secures, and
settles; staking "verifies host provider configurations" (R1 0.5); on-chain governance
(R6 1.0); AEP-76 burn-mint settlement of provider payments with "built-in circuit
breakers" (R4 1.0, R5 1.0); validator slashing is standard Cosmos-SDK (R3 1.0, parameter
detail from search summary, not the fetched page); lease escrow not detailed on the page
(R8 0.5); community pool thin (R7 0.5); IBC not detailed on page (R9 0.5); tooling and
polish (R11 1.0, R12 1.0). **Total 9.0. Depth 7/12 (58%). This is what delivered looks
like on this rubric.**

**Chainlink (LINK)**. From https://chain.link/economics/: 1B fixed supply, 748M+
circulating, Chainlink Reserve (5M+ LINK) programmatically converting revenue into LINK
(R5 1.0, R7 1.0), staking 42M+ LINK with slashing for missed performance requirements
(R3 0.5: existence stated, enforcement detail thin), Payment Abstraction (R4 0.5), $34T+
transaction value enabled, 904K+ holders. No peer policing, identity, escrow, or on-chain
DAO on the fetched page. **Total 5.5. Depth 3/12.** Note: the rubric measures token-state
machinery, not oracle scale; LINK's raw impact dwarfs everything here and its rubric score
still lands mid-table because it concentrates its machinery in Reserve + staking.

**Helium (HNT)**. From https://docs.helium.com/helium-tokens/hnt/: burn-and-mint
equilibrium (DC only created by burning HNT, R5 1.0), HIP-20 halvings and HRP 2025-03
smoothing pool (R6 1.0, R7 0.5), DC settlement of data transfer (R4 0.5), Net Emissions
re-mint capped at 1% of epoch (R7 0.5, overlapping), no penalties for bad hotspots on the
page (R3 0). **Total 5.5. Depth 3/12.**

**Toncoin (TON)**, context row, class mismatch noted. From
https://en.wikipedia.org/wiki/Toncoin: $1.7B SAFT raise, SEC halt, Telegram abandonment
and $18.5M penalty, independent relaunch, Telegram wallet integration, 2024 native USDT,
2026 rename to Gram. Foundation governance (R6 0.5), L1 settlement (R4 1.0), tooling and
polish (R11 1.0, R12 1.0). **Total 4.5. Depth 3/12.** An L1 base scores mid-table on a
token-statecraft rubric; this is the yardstick showing the rubric is not measuring
network size.

### Class C: Scam-grade controls (documented post-mortems)

**Squid Game token (SQUID)**, 2021. Contract had no sell function; buyers could not
resell; price ran to $2,861 then collapsed in minutes; developers drained ~$3.38M through
Tornado Cash; site "riddled with errors" (https://en.wikipedia.org/wiki/2021_Squid_Game_cryptocurrency_scam).
Scored: R11 0.5 (a website and game page existed). **Total 0.5.**

**Save the Kids (KIDS)**, 2021. Charity token promoted by FaZe Clan members and YouTubers;
advertised anti-whale limit (20% per 24h) was altered at launch to a 60-second window,
letting insiders dump; Coffeezilla traced the sells; price fell ~99%
(https://en.wikipedia.org/wiki/Save_the_Kids_token). Note the pattern: the ONE piece of
machinery scammers write is a fee/limit splitter, and it is sabotaged at birth. Scored:
R4 0.5 (fee splitter written, then corrupted). **Total 1.0.**

**HAWK (Hawk Tuah)**, Solana, Dec 2024. Bubblemaps' forensic series "HAWK: Anatomy of a
Celebrity Rug" (https://blog.bubblemaps.io/hawk-anatomy-of-a-celebrity-rug/, "From Wallet
Leak to Courtroom") traces interconnected insider wallets at launch; press summaries of
the analysis report ~96% of supply in a connected cluster (Binance Square case study;
retrieved only as a search summary, treat the 96% as press-reported). Launchpad token, no
machinery of its own. Scored: R11 0.5 (launchpad-provided). **Total 0.5.**

**$LIBRA**, Argentina, Feb 2025. Presidential promotion, insiders held 70% of supply,
~$87M extracted by founding accounts while ~74,000 investors lost money and total losses
reached $251M; Hayden Davis admitted profiting $113M; the same liquidity strategy was used
on $MELANIA; asset freezes and a congressional commission followed
(https://en.wikipedia.org/wiki/$Libra_cryptocurrency_scandal). The largest documented
extraction in this entire sample ran on zero machinery. Scored: R4 0.5 (launchpad fee
plumbing), R11 0.5. **Total 1.0.**

## Part 4: The matrix

| Token | Class | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 | R12 | Total | Depth |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Akash | infra | 0.5 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0.5 | 0.5 | 0.5 | 0 | 1.0 | 1.0 | **9.0** | 58% |
| GSTD | agent-econ | 0.5 | 0.5 | 0.5 | 1.0 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 0.5 | **6.5** | 17% |
| Virtuals | agent | 0.5 | 0 | 0 | 0.5 | 0.5 | 0.5 | 0.5 | 0 | 0.5 | 1.0 | 1.0 | 1.0 | **6.0** | 25% |
| Bittensor | agent/AI | 0.5 | 1.0 | 0.5 | 0.5 | 0 | 0.5 | 0 | 0 | 0 | 0.5 | 1.0 | 1.0 | **5.5** | 17% |
| Chainlink | infra | 0 | 0 | 0.5 | 0.5 | 1.0 | 0 | 1.0 | 0 | 0.5 | 0 | 1.0 | 1.0 | **5.5** | 25% |
| Helium | infra | 0 | 0 | 0 | 0.5 | 1.0 | 1.0 | 0.5 | 0 | 0.5 | 0 | 1.0 | 1.0 | **5.5** | 25% |
| Fetch.ai | agent | 0.5 | 0 | 0 | 0.5 | 0 | 0.5 | 0 | 0 | 0.5 | 1.0 | 1.0 | 1.0 | **5.0** | 25% |
| Toncoin | L1 ctx | 0 | 0 | 0 | 1.0 | 0 | 0.5 | 0.5 | 0 | 0.5 | 0 | 1.0 | 1.0 | **4.5** | 25% |
| elizaOS | agent | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.0 | 1.0 | 1.0 | **3.5** | 25% |
| Save the Kids | control | 0 | 0 | 0 | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0.5 | 0 | **1.0** | 0% |
| LIBRA | control | 0 | 0 | 0 | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0.5 | 0 | **1.0** | 0% |
| SQUID | control | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.5 | 0 | **0.5** | 0% |
| HAWK | control | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.5 | 0 | **0.5** | 0% |

## Part 5: Findings

**Where GSTD sits.** Second on breadth (6.5), behind only Akash (9.0), ahead of every
AI-agent comparable including Virtuals (6.0) and Bittensor (5.5). Near the bottom on
depth (17%) among the honest cohort, tied with Bittensor and above nothing but the
controls' 0%. GSTD's profile is maximal-breadth, minimal-depth: it is the only token in
the sample that has written at least a half-score on every single mechanism. Nobody else
did that, including Chainlink and Akash.

**The median for its class.** AI-agent protocol class (Virtuals, elizaOS, Fetch.ai,
Bittensor): totals 6.0, 3.5, 5.0, 5.5, class median 5.25, and the class is dominated by
R10/R11/R12 (agents + tooling + polish) with near-zero statecraft rows. GSTD at 6.5 is
above its class median, and it wins on exactly the rows the class skips (identity,
policing, slashing, treasury, escrow). Infra class median: 5.5. GSTD sits slightly above
that too, on breadth alone.

**What scam-grade actually looks like on this rubric.** Total 0.5 to 1.0 out of 12. The
controls wrote essentially one mechanism between them, a payment splitter or honeypot
gate, and in the one documented case where it had a protective design (KIDS anti-whale
window) it was altered at launch (24h to 60s,
https://en.wikipedia.org/wiki/Save_the_Kids_token). SQUID's signature was the ABSENCE of
a sell path (https://en.wikipedia.org/wiki/2021_Squid_Game_cryptocurrency_scam). LIBRA,
the biggest extraction ($87M+ founders per
https://en.wikipedia.org/wiki/$Libra_cryptocurrency_scandal), needed no contract
machinery at all beyond the launchpad. Scam-grade on this rubric is not bad machinery; it
is NO machinery, plus trusted distribution.

**Is the complexity grift-plausible?** Graded tri-state at the end, but the economics
first: a rug's revenue is a function of hype distribution at launch, not of contract
count. Every control demonstrates extraction at near-zero build cost, and the biggest one
(LIBRA) out-earned any plausible machinery-heavy scam by orders of magnitude while
building nothing. Machinery adds build cost and audit surface without adding extraction
capacity, EXCEPT as trust camouflage. So the camouflage theory requires the machinery to
be trust-marketing; but the specific machinery written (slash ladders that fine the
operator's own validators, evidence-hash peer reports, genesis locks that pin every node
to a manifest, a burn sink that destroys the treasury's own upside) is machinery whose
entire function is to constrain the operator. A camouflager writes honeypots and fee
splitters; neither SQUID nor KIDS nor HAWK wrote a self-punishing contract. Meanwhile the
economy the machinery secures is, on 2026-09-29 evidence, 206 holders at ~$50k FDV with
an idle settlement contract. If this is camouflage, it is camouflage that has so far
earned approximately nothing, which is the least profitable grift in the sample.

The caveat that keeps this from being a clean pass: the AUTHORITY SPINE from the
forensics still binds. The gateway is owner-set, SettlementMaster.owner transfer to
DAOVoting is listed in phase2_todo and NOT done, and whoever holds those keys is the
sovereign of the deployed economy regardless of how much anti-grift machinery is written
but undeployed (`contracts/deployment-mainnet.json`). The complexity is real; the
decentralization it promises is still pending in the project's own checklist.

## Part 6: Verdict (tri-state)

Operator hypothesis: "the pay grift is camouflage; the development is the real tell."

**Verdict: LEAN SUPPORTED, on complexity evidence alone, at WRITTEN status; UNPROVEN at
DELIVERED status.** The development is real (170k LOC, 13 contracts, deployment record),
anomalous for its economy (no other token in the sample carries this machinery-to-economy
ratio; the controls carry zero), and of the anti-grift kind (self-punishing mechanisms,
which no documented rug writes). Scam-grade is decisively excluded: 0.5 to 1.0 rubric
totals against GSTD's 6.5. What the complexity evidence cannot confirm is delivery and
authority-dispersal: 10 of 12 rows are written-not-live, the owner transfers are pending
in the project's own phase2_todo, and no on-chain usage exists in evidence. The tell is
currently a blueprint tell.

**What evidence would settle it:**

1. **On-chain slash events.** SlashMechanics is phase3 and undeployed, so no slash can
   exist yet. First SlashExecute on TON mainnet with a real provider stake would convert
   R3 from 0.5 to 1.0 and prove the policing loop runs.
2. **Gateway settlement logs.** SettlementMaster is Active at ~$0.15 balance. A stream of
   85/10/5 settlements with GSTD bonus mints, or their long absence against claimed
   agent population, is the single cleanest live/dead discriminator for the economy.
3. **Genesis manifest version timing.** AgentRegistry is undeployed, so no genesis lock
   exists on chain. Its deployment, then the cadence of owner-set manifest updates versus
   agent registrations, plus ReportGenesisViolation events with evidenceHashes, would
   show whether the trap harvests real fabricators or is decorative.
4. **The phase2 owner transfers.** SettlementMaster.owner and EcosystemTreasury.owner
   moving to a deployed DAOVoting is the project's own checklist item and the one
   falsifiable good-faith act available. If it never happens, the authority-spine reading
   (forensics: "the crown before the council") strengthens regardless of machinery.

## Sources

Local: `watch/inbox/GSTD_FORENSICS_20260918.md`; `reference/gstdcoin/{A2A,ai,contracts,gstd-bridge,gstdbot,web}`;
`reference/gstdcoin/contracts/deployment-mainnet.json`; `reference/gstdcoin/contracts/SettlementMaster.tact`;
`reference/gstdcoin/contracts/AgentRegistry.tact`; `reference/gstdcoin/contracts/naas/SlashMechanics.tact`;
`reference/gstdcoin/contracts/bridge/ton/GstdBridge.tact`; `reference/gstdcoin/contracts/README.md`;
`reference/gstdcoin/contracts/CLAUDE.md`.

Explorer (2026-09-29 point checks):
- https://tonviewer.com/EQAhuR_cEaIkRqs4gvgXSD-Qw2FRUkkBUZQkTBrFT5n-ZrSS (SettlementMaster, Active, 0.0992 GRAM)
- https://tonviewer.com/EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO (GSTD Jetton, Gold Standard, 206 holders, $0.00005)

Comparables:
- Akash: https://akash.network/token/
- Bittensor: https://bittensor.com/whitepaper
- Chainlink: https://chain.link/economics
- Helium: https://docs.helium.com/helium-tokens/hnt/
- Fetch.ai: https://fetch.ai/
- Virtuals: https://virtuals.io/
- elizaOS: https://github.com/elizaOS/eliza
- Toncoin: https://en.wikipedia.org/wiki/Toncoin
- SQUID: https://en.wikipedia.org/wiki/2021_Squid_Game_cryptocurrency_scam
- Save the Kids: https://en.wikipedia.org/wiki/Save_the_Kids_token
- HAWK: https://blog.bubblemaps.io/hawk-anatomy-of-a-celebrity-rug/
- LIBRA: https://en.wikipedia.org/wiki/$Libra_cryptocurrency_scandal

Unretrievable-but-reported (flagged, not scored without a URL): Virtuals buyback-and-burn
third-party audit (8blocks, 59/100); HAWK 96% insider-cluster figure (Binance Square
summary of the Bubblemaps analysis); elizaOS founder token statements (KuCoin News).
