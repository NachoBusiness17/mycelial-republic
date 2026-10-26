# GAPS AND PEOPLE - Lane D, the gap register + the people who filled them - 2026-10-09

Inputs: GSTD_CODEBASE_AUDIT.md (Lane A), DOGFOOD_DATA.md, PLATFORM_SURFACE_MAP.md,
gstd_distribution_thesis_20260109.md, mycelial-republic CONSTITUTION.md Articles 1/7/15.
Method: every census card web-verified 2026-10-09; URLs from live search results;
unverifiable claims marked OWED. Gaps are quoted from the inputs, none invented.

## 1. Gap register

GSTD-side (evidence cites are Lane A byte anchors):

| id | gap | evidence | who fills it |
|---|---|---|---|
| G1 | results not bound to asks: signed lane exists, production lanes unsigned; result_hash omits prompt+params | agent.ts:989-1009 vs platform-link.ts:287-297, server.ts:4604-4617; attestation.ts:46-51; dogfood rode the unsigned lane | C1-C5 |
| G2 | node = knowable string, not key possession; push endpoint unauthenticated; baked platform pubkey crowns every fork | finding 11 platform-link.ts:107-130; findings 3/5 server.ts:4568; platform-auth.ts:5-10; Art 1 violated by construction | C6, C7 (+ Solana key classes) |
| G3 | reputation formula unobservable; zero node-side reputation code | gap (b); ARCHITECTURE.md:189 "No quality signal"; dogfood +8 on 9 tasks, opaque | C8 |
| G4 | shared-IP rate bucket, no proxy-header trust; in-memory limiter clears on restart | finding 4 server.ts:453-480; dogfood 6/11 requests dead at ~16/min | nobody needed: standard trust-proxy practice; fastify.ts:23 already proves the fix in-repo |
| G5 | node-lite = whole Ollama API through an unauthenticated quick tunnel, CORS * | finding 9 node-lite/index.ts:100-144 | C9 |
| G6 | offline = no earning, no settlement; queue-settle covers reports, not task acquisition | gap (d); CENTRAL_DEPENDENCIES.md:8-13; agent.ts:789-871 partial | C10, C11 |

Our-side needs:

| id | need | why (input) | who fills it |
|---|---|---|---|
| O1 | settlement-grade work verification we can PRODUCE from our replay machinery | dogfood tier verdict: settlement is the gstd tier's value; frozen-tape replay is the half nobody else has | closest C1-C5; verdict BUILD-OURSELVES |
| O2 | installer-grade key UX for normies, one wizard screen | distribution thesis: node-by-default in the Electron installer; Art 15 choice screen | C12 |
| O3 | mesh bridge economics: rewards across our mesh + gstd, support-pct routing | thesis: honest support channel, default OFF, revocable | C13 |
| O4 | task routing quality: shape-keyed matching on honest capabilities | dogfood cache-collision rows; self-declared peers.ts:249-296 | C14 |
| O5 | per-device identity at scale, fork-equal, no privileged registry | thesis: every seat is supply AND demand; Art 1.4 bans a one-party registry | C7, C15 |

## 2. People census (verdicts: STEAL / WATCH / PARTNER / BUILD-OURSELVES)

C1 GENSYN (G1) - WATCH
- BUILT: RL Swarm p2p testnet, nodes earn on-chain identity tracking verified contributions; proof-of-compute for ML
- SOURCES: https://docs.gensyn.ai/testnet | https://github.com/gensyn-ai/rl-swarm
- WHY: same thesis, training-loop shaped, not chat-task shaped

C2 EZKL (G1) - WATCH
- BUILT: ONNX model to Halo2 zk circuit; proves inference of a fixed model
- SOURCES: https://docs.ezkl.xyz | https://github.com/zkonduit/ezkl
- WHY: proves model math, cannot prove "this answer served this ask"; too heavy per 0.002 GSTD task

C3 OP STACK FAULT PROOFS (G1/O1) - STEAL
- BUILT: permissionless dispute game: claim, challenger bisection, one-step proof settles
- SOURCES: https://docs.optimism.io/op-stack/fault-proofs | https://docs.optimism.io/op-stack/fault-proofs/explainer
- WHY: the bisection-on-diff pattern ports to task disputes; our replay tape plays the challenger

C4 LIVEPEER + TRUEBIT (G1/O1) - STEAL
- BUILT: probabilistic verification: sample outputs of deterministic transcode and re-run to compare; disputes escalate to Truebit's on-chain verification game
- SOURCES: https://forum.livepeer.org/t/transcoding-verification-improvements-fast-full-verification/1499 | https://medium.com/truebit/truebit-the-marketplace-for-verifiable-computation-f51d1726798f | https://arxiv.org/pdf/1908.04756
- WHY: sample-then-reverify is the exact economics for replay-checked settlement

C5 PHALA (G1) - PARTNER
- BUILT: TDX/GPU-TEE confidential AI: attestation reports + signed receipts via OpenAI-compatible API
- SOURCES: https://docs.phala.com/phala-cloud/confidential-ai/overview | https://phala.com/solutions/ai-agents
- WHY: renting attested inference beats building TEE plumbing; does not cover local nodes

C6 TON TON_PROOF (G2) - STEAL, best steal of the census
- BUILT: wallet signs app payload (domain + timestamp + nonce); backend verifies key possession, auth without a new identity system
- SOURCES: https://docs.ton.org/applications/ton-connect/how-to/ton-proof | https://docs.tonconsole.com/academy/sign-data
- WHY: gstd already depends on @ton/crypto; heartbeat/complete/claim should carry this signature shape

C7 LIBP2P PEERID (G2/O5) - STEAL
- BUILT: peer identity = multihash of the ed25519 pubkey; the key IS the id, signatures verify from the id alone
- SOURCES: https://github.com/libp2p/specs/blob/master/peer-ids/peer-ids.md | https://github.com/libp2p/js-libp2p/discussions/2379
- WHY: already inside gstd p2p; the requirePeerAuth pattern (server.ts:203-240) is this, promote it to the platform lane

C8 RENDER NETWORK (G3) - WATCH
- BUILT: published reputation-tier pricing (Trusted/Priority/Economy) with OctaneBench scoring driving assignment
- SOURCES: https://rendernetwork.com/pricing | https://messari.io/report/understanding-the-render-network-a-comprehensive-overview
- WHY: the honest shape for G3, publish the formula and benchmark-gate tiers; assignment stays centralized

C9 CLOUDFLARE ACCESS + THE PROBLLAMA RECORD (G5) - STEAL
- BUILT: service-token zero-trust wall in front of cloudflared origins (CF-Access-Client-Id/Secret); Wiz/Oligo documented what naked Ollama exposure costs (CVE-2024-37032 RCE + follow-ups)
- SOURCES: https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/ | https://www.wiz.io/blog/probllama-ollama-vulnerability-cve-2024-37032 | https://www.oligo.security/blog/more-models-more-probllms
- WHY: node-lite tunnel behind Access + path allowlist is a config change, not a build

C10 ELTOO / LIGHTNING (G6/O3) - WATCH
- BUILT: state channels where later states supersede earlier ones; on-chain settlement deferred to the final state only
- SOURCES: https://blockstream.com/eltoo.pdf | https://blog.blockstream.com/en-eltoo-next-lightning
- WHY: the defer-settlement LOGIC is our queue-settle shape; the Bitcoin plumbing is not reusable on TON

C11 AUTOMERGE / INK & SWITCH (G6/O1) - STEAL
- BUILT: CRDT sync engine: local-first edits, conflict-free merge after long offline, replay changes elsewhere
- SOURCES: https://automerge.org | https://www.inkandswitch.com | https://automerge.org/blog/automerge-2
- WHY: the local settlement ledger: append completions offline, merge/replay on reconnect; frozen-tape replay proves the re-execution half

C12 DID:KEY + PASSKEY WALLETS (O2) - STEAL (did:key) / WATCH (passkeys)
- BUILT: did:key derives a DID from one pubkey, no registry, fork-equal by construction; Coinbase Smart Wallet kills the seed phrase with WebAuthn passkeys on ERC-4337
- SOURCES: https://w3c-ccg.github.io/did-key-spec | https://github.com/coinbase/smart-wallet | https://www.coinbase.com/blog/state-of-wallets-2
- WHY: did:key is the per-install identity string a wizard can show in one screen; passkey UX is EVM-shaped, no TON standard yet

C13 ALTHEA (O3) - STEAL
- BUILT: mesh routers pay per-hop price-per-megabyte over bidirectional payment channels; routing follows the price vector; empty balance degrades service, never disconnects
- SOURCES: https://updates.althea.net/Althea-Whitepaper-v2.0.pdf | https://staging.altheamesh.com/how-it-works
- WHY: per-hop price-vector routing is the economics grammar for bridge fees + the support-pct routing table

C14 AKASH (O4) - STEAL
- BUILT: reverse-auction compute marketplace: tenant SDL declares attributes, providers bid, lease forms on match
- SOURCES: https://akash.network/docs/learn/core-concepts/providers-leases | https://akash.network/docs/providers/operations/provider-attributes
- WHY: attribute-declared capabilities + bid/lease replaces self-declared peers (peers.ts) with the matching shape GPS task_shape routing already needs

C15 IOID / IOTEX + IO.NET (O5) - STEAL (DID layer only)
- BUILT: W3C-DID device identity minted as ERC-721 Device NFTs; firmware SDK registers real hardware; deployed at io.net scale
- SOURCES: https://docs.iotex.io/ioid | https://docs.iotex.io/ioid/technical-specification/system-architecture | https://iotex.io/blog/ioid-on-chain-device-identity-for-verifiable-depins
- WHY: steal the DID-per-device layer, skip the chain registry to honor Art 1.4

Register note (no card): Solana validator key classes (identity / vote / withdrawer, rotation
playbook) are the pattern for separating device key from earning wallet from payout authority:
https://docs.anza.xyz/operations/guides/vote-accounts

## 3. Ranking - top 3 fills by value per engineering hour

1. SIGNED + AUTHENTICATED SETTLEMENT SPINE (G1+G2, C6+C7). One ed25519 device key per node
   (PeerId pattern, already in-repo), wallet-linked once at registration via a ton_proof-shaped
   signature; every completion lane binds prompt_hash + params + result_hash under node_sig.
   First PR: push + poll lanes include node_sig exactly as the swarm lane does (agent.ts:991-995);
   platform verifies against the node_pubkey field the register call already carries
   (platform-link.ts:120).
2. OFFLINE QUEUE-SETTLE LOCAL LEDGER (G6, C10+C11). Append-only local ledger of
   completed-unsettled tasks, CRDT-merge on reconnect; eltoo logic says only the net delta
   settles. First PR: extend pending-report persistence (agent.ts:789-871) across restarts to
   cover settlement state, replay to platform on reconnect; verify with an airplane-mode dogfood.
3. PER-DEVICE IDENTITY AT INSTALL (O5+O2, C12+C15). Wizard screen 1: generate ed25519 device
   key, show its did:key string; screen 2: optional wallet paste + the Article 15 choice screen
   (support pct, default OFF, revocable); register node_pubkey. First PR: keygen + registration
   field; consent-screen copy is already drafted in the distribution thesis.

BUILD-OURSELVES, nobody has it: replay-verified task settlement (O1). zkML proves model math
(C2), TEE proves environment (C5), fault games prove execution steps (C3/C4); nobody binds
"this answer served this ask, provably by re-execution from a frozen tape" because only our
estate keeps frozen tapes plus replay machinery. Livepeer PVS (C4) is the ancestor to adapt.

## OWED
- Oasis ROFL (other TEE class named in the brief): not verified this pass, OWED.
- GSTD platform reputation formula: unobservable per Lane A, no external source can exist.
- Stacks/Blockstack auth class: superseded by the passkey pattern, not carded.
