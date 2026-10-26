# GSTD INCORPORATION DRAFT v1 (FIRST DRAFT, 2026-10-05, incorporation-draft lane)

Provenance: built from three inputs. (1) state/gstd_analysis_results.jsonl, the
738-row DeepSeek file analysis of the GSTD venture repos (every row carries the
five-line WHAT/SYSTEM/HOOKS/RISK/INCORPORATE contract; the contract text lives at
state/gstd_analysis_prompt.md:1-10). (2) docs/ref/GSTD_DOGFOOD_PLAN.md, the
device/phases plan. (3) docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md, the trust findings.
Every count below comes from the scripted census
(state/_gstd_incorporation_census.py, output banked at
state/_gstd_incorporation_census.json) unless tagged hand-count. High-value rows
were read in full via the slice dump state/_gstd_top_rows.txt.

## 1. EXEC SUMMARY

The estate incorporates into GSTD as a trust layer at four boundaries, and the
network's own 738-file self-analysis asks for exactly that shape. At the submit
boundary, citation/credential/seal pre-push instruments attach evidence hashes to
every task result before it POSTs. At the quorum boundary, the hardened consensus
gate plus immune-cell critics decide which attestations count. At the routing
boundary, the GPS ledger replaces self-reported counters and RAM heuristics with
what-solved-what keyed on (model, task_shape, evidence_hash). At the settlement
boundary, verkle receipts and patrols make payouts auditable. The census agrees:
citation/seal instruments are named in 320 INCORPORATE lines, receipts in 218, the
consensus gate in 193, GPS in 136 (state/_gstd_incorporation_census.json:179-184),
while the top risk class by far is unverifiable results with no evidence (353
rows, state/_gstd_incorporation_census.json:202). Phasing rides the dogfood plan:
nodes first, instruments on the mesh second, the quorum/settlement trust layer
gated on the immune race.

## 2. THE MAP

Subsystem file counts (scripted, state/_gstd_incorporation_census.json:161-175):
platform-api 100, settlement/wallet 88, node-lifecycle 82, channels/ux 19 plus 50
web-frontend, bridge 47, contracts 43, inference 41, task-routing 26, p2p 21,
training 20, quorum/attestation 12, memory 4; non-runtime buckets: skill
marketplace 111, docs 74. Value rank orders each wiring by how much of the
network's trust surface it converts to receipts.

### 2.1 quorum/attestation (12 rows). Value rank: 1 (HIGHEST)

What it is: the 2-of-3 Ed25519 attestation path. Co-executor cross-signing is
collected and adjudicated in gstdbot/src/p2p/quorum-coordinator.ts (the
evaluate() filter and alreadyEndorsed dedupe,
state/gstd_full/gstdbot/src/p2p/quorum-coordinator.ts:60), attestation transport
is the libp2p PROTOCOL_ATTESTATION handler
(state/gstd_full/gstdbot/src/p2p/node.ts:443), and the bridge runs its own vote
consensus (record_vote, state/gstd_full/gstd-bridge/src/consensus/mod.rs:145).
Estate wiring: the hardened consensus gate (mag/consensus_gate.py, with witness
collapse logic in mag/_consensus_witness.py) inserts at evaluate()'s
verified-filter and at the PROTOCOL_ATTESTATION handler: refuse unanimity-of-one,
collapse byte-identical witnesses, require construction-evidence before an
attestation set counts as quorum. Evidence rows: state/gstd_analysis_results.jsonl:684
(quorum-coordinator: pubkey-rotation sybil can inflate verified.length),
state/gstd_analysis_results.jsonl:680 (attestation acceptance is schema-only),
state/gstd_analysis_results.jsonl:409 (bridge record_vote forgeable),
state/gstd_analysis_results.jsonl:450 (their own quorum-gaps spec admits
recordOutcome conflates responsiveness with outcome),
state/gstd_analysis_results.jsonl:706 (their live test proves only the happy
path).

### 2.2 settlement/wallet (88 rows). Value rank: 2

What it is: SettlementMaster (Tact) pays workers on attested quorum via
SettleTaskWithProof and registers attestor keys via RegisterAttestorKey; a cron
relay (contracts/scripts/settle-quorum-proof.ts) fetches proofs from the platform
and submits on TON. Estate wiring: consensus gate plus immune critics run
pre-send on the relay's buildAttestationsChain path
(state/gstd_full/contracts/scripts/settle-quorum-proof.ts:80); the verkle chain
(mag/verkle_bus.py and the verkle family in mag/) appends a receipt per settled
taskId; the credential registry gates RegisterAttestorKey. Evidence rows:
state/gstd_analysis_results.jsonl:357, state/gstd_analysis_results.jsonl:380
(relay trusts a single shared TREASURY_SECRET),
state/gstd_analysis_results.jsonl:258 (timing-unsafe treasury auth),
state/gstd_analysis_results.jsonl:703 (recordVerifiedEarning trusts caller
amount).

### 2.3 platform-api (100 rows). Value rank: 3

What it is: the Cloudflare Worker plus KV surface that routes tasks; the worker
flow is register, poll /api/v1/tasks/worker/pending, POST
/api/v1/tasks/worker/submit. Estate wiring: citation/credential/seal pre-push
(tools/citation_lint.py, mag/config_seal.py, tools/md_record_seal.py) wraps
submit so results carry evidence_hash plus credential; GPS ledger
(tools/gps_mcp/) filters/ranks pending; every register and submit response lands
as an estate ledger row. Evidence rows: state/gstd_analysis_results.jsonl:39
(gstd_client.submit_result is the exact seam),
state/gstd_analysis_results.jsonl:125 (trust_score is opaque),
state/gstd_analysis_results.jsonl:172, state/gstd_analysis_results.jsonl:63.

### 2.4 node-lifecycle (82 rows). Value rank: 4

What it is: node onboarding and heartbeat. swarm/client.ts registers, heartbeats,
and self-reports earnings; node-lite/index.ts is the no-Docker node; the A2A
agent SDK runs the worker loop. Estate wiring: seal the register/heartbeat
payloads; verkle receipt per processed task keyed (model, task_shape,
evidence_hash); immune critics as task-type handlers so no result leaves the
node unattested. Evidence rows: state/gstd_analysis_results.jsonl:692 (earnings
are local counters), state/gstd_analysis_results.jsonl:674 (registration
unauthenticated), state/gstd_analysis_results.jsonl:36 (default handler returns
completed unconditionally), state/gstd_analysis_results.jsonl:422 (their
central-dependencies audit names the Phase-4 cutover gap).

### 2.5 inference (41 rows). Value rank: 5

What it is: Ollama execution plus the sandboxes around it (POSIX rlimit
sandbox.py, browser wasmSandbox.ts, the WorkerService web worker driver).
Estate wiring: replace the fabricated proofHash (btoa of latency plus
Math.random(), state/gstd_full/ai/frontend/src/services/WorkerService.ts:129)
with a sealed receipt at the task_completed send site; immune critics wrap
sandbox run_safe; GPS rows key every inference call. Evidence rows:
state/gstd_analysis_results.jsonl:303 (the fake proofHash),
state/gstd_analysis_results.jsonl:47 (sandbox is resource-limiting, not a
sandbox), state/gstd_analysis_results.jsonl:185, state/gstd_analysis_results.jsonl:41.

### 2.6 task-routing (26 rows). Value rank: 6

What it is: node discovery and call routing in ai/frontend/src/lib/nodes.ts
(getActiveNodes scoring, callNodeParallel first-wins racing,
state/gstd_full/ai/frontend/src/lib/nodes.ts:9), the oracle single-node verdict
path, and the multi-expert chat fan-out with a heuristic consensus score.
Estate wiring: consensus gate plus immune critics convert first-wins racing
into quorum-of-witnesses; GPS ranking replaces RAM/CPU heuristics in node
scoring. Evidence rows: state/gstd_analysis_results.jsonl:173 (first-wins with
no attestation), state/gstd_analysis_results.jsonl:188 (consensus score is a
fake heuristic), state/gstd_analysis_results.jsonl:263 (unanimity-of-one
oracle).

### 2.7 p2p (21 rows). Value rank: 7

What it is: peer discovery, heartbeat gossip, and the libp2p SuperNode mesh;
plain-HTTP peer manager in gstdbot/src/p2p/peers.ts, bootstrap list served from
ai/frontend/src/pages/api/v1/nodes/peers.ts. Estate wiring: ed25519 seed seal
(mag/seed_seal.py) signs and verifies HeartbeatPayload (their pubkeyHex field is
declared but unused per state/gstd_analysis_results.jsonl:683); the consensus
gate attestation-filters the bootstrap list (the trust root for WAN discovery).
Evidence rows: state/gstd_analysis_results.jsonl:683,
state/gstd_analysis_results.jsonl:248 (any KV writer can poison bootstrap
peers), state/gstd_analysis_results.jsonl:106, state/gstd_analysis_results.jsonl:16.

### 2.8 bridge (47 rows). Value rank: 8

What it is: the Rust cross-chain bridge consensus plus the MCP surfaces
(ai/gstd-mcp-server execute_rpc passthrough, the A2A MCP tools) and the A2A
ingress firewall. Estate wiring: receipt-first MCP wrapper around execute_rpc;
immune skeptic replaces the regex firewall's silent boolean
(state/gstd_analysis_results.jsonl:48); reproducer CI job re-runs bridge builds
hermetically. Evidence rows: state/gstd_analysis_results.jsonl:312
(unauthenticated arbitrary-method passthrough), state/gstd_analysis_results.jsonl:64,
state/gstd_analysis_results.jsonl:409, state/gstd_analysis_results.jsonl:398.

### 2.9 contracts (43 rows). Value rank: 9

What it is: the Tact contract family (SettlementMaster, AgentRegistry, DAOVoting,
GSTDJetton) plus deploy scripts and CI. Estate wiring: bytecode-hash seal on
deploy payloads with a verkle receipt; consensus gate on RegisterAttestorKey and
UpdateReputation send paths; receipt chaining of compiled artifacts. Evidence
rows: state/gstd_analysis_results.jsonl:375 (single owner wallet mints
attestors), state/gstd_analysis_results.jsonl:92 (deploy mnemonic uncheck),
state/gstd_analysis_results.jsonl:331 (CI has no test step),
state/gstd_analysis_results.jsonl:392 (DAO quorum is stake-in-TON).

### 2.10 channels/ux (19 rows plus 50 web-frontend rows). Value rank: 10

What it is: the Telegram bot and webhook, the web frontend. Estate wiring:
consensus gate at the webhook's handleAI callNodeChat call; GPS-keyed answer
cache replacing MD5-of-question keying; seal on outbound task payloads.
Evidence rows: state/gstd_analysis_results.jsonl:294 (webhook has no secret-token
check), state/gstd_analysis_results.jsonl:632 (MD5 cache with no provenance),
state/gstd_analysis_results.jsonl:307.

### 2.11 training (20 rows). Value rank: 11

What it is: federated QLoRA marketplace (federated.ts GradientAggregator,
metacognition self-scores, the finetune specs), experimental in their tree.
Estate wiring: immune critics gate submitGradient
(state/gstd_full/gstdbot/src/training/federated.ts:172); reproducer re-runs the
timing probe; GPS rows keyed (base_model, domain, evidence_hash). Evidence rows:
state/gstd_analysis_results.jsonl:696, state/gstd_analysis_results.jsonl:440
(colluding-majority gradient poisoning is the load-bearing hole),
state/gstd_analysis_results.jsonl:43, state/gstd_analysis_results.jsonl:38.

### 2.12 memory (4 rows). Value rank: 12

What it is: collective.ts three-tier store with verifiedBy hardcoded to 1
(state/gstd_full/gstdbot/src/memory/collective.ts:121) and the IPFS pin ledger.
Estate wiring: verkle proof on L3 sync; GPS keys at store/recall; consensus gate
on remote entries. Evidence rows: state/gstd_analysis_results.jsonl:663
(platform-trusted L3 can poison global memory),
state/gstd_analysis_results.jsonl:688, state/gstd_analysis_results.jsonl:620,
state/gstd_analysis_results.jsonl:525.

## 3. THE TOP 10 INCORPORATIONS

1. SEAL THE SUBMIT BOUNDARY. Wiring: wrap POST /api/v1/tasks/worker/submit with
   citation/credential/seal pre-push; the result payload gains evidence_hash
   plus credential, and the platform (or any peer) can reject unsealed submits.
   Their files: A2A/src/gstd_a2a/gstd_client.py (submit_result at
   state/gstd_full/A2A/src/gstd_a2a/gstd_client.py:136),
   gstdbot/src/swarm/client.ts (processTask),
   gstdbot/src/node-lite/index.ts. Our instruments: mag/config_seal.py,
   tools/md_record_seal.py, tools/citation_lint.py, verkle receipt sink. Probe:
   submit one sealed and one unsealed result for the same task; today both are
   accepted (state/gstd_analysis_results.jsonl:1 names the hole), after wiring
   the unsealed one must be refused and the sealed one must appear as a ledger
   row with matching evidence_hash.
2. CONSENSUS GATE AT QUORUM EVALUATION. Wiring: insert
   mag/consensus_gate.py checks into quorum-coordinator evaluate()'s
   verified-filter and the PROTOCOL_ATTESTATION handler: unanimity-of-one
   refused, byte-identical witnesses collapsed, construction-evidence required.
   Their files: state/gstd_full/gstdbot/src/p2p/quorum-coordinator.ts:152,
   state/gstd_full/gstdbot/src/p2p/node.ts:443,
   state/gstd_full/gstdbot/src/p2p/attestation.ts. Our instruments:
   mag/consensus_gate.py, mag/_consensus_witness.py. Probe: replay a quorum set
   where all three attestations are byte-identical, and a 1-witness set; the
   current code accepts both (their live test only proves the happy path,
   state/gstd_analysis_results.jsonl:706); the gate must refuse both.
3. SIGNATURE VERIFICATION IN BRIDGE CONSENSUS. Wiring: record_vote must verify
   signature_share against a registered per-validator key before counting the
   vote; the estate seed seal supplies the ed25519 key registry and signing.
   Their files: gstd-bridge/src/consensus/mod.rs:145 (their own SECURITY NOTE at
   state/gstd_full/gstd-bridge/src/consensus/mod.rs:136 admits it). Our
   instruments: mag/seed_seal.py (ed25519, per the audit's note that the
   decaying manifest is a port not a build,
   docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md:41-45), mag/consensus_gate.py. Probe:
   submit a vote with a valid PeerId but a signature from the wrong key; current
   code counts it, hardened code must reject and emit a receipt of the refusal.
4. GPS LEDGER REPLACES SELF-REPORTED CAPABILITY. Wiring: node scoring and oracle
   node-selection read GPS rows keyed (node_device, task_shape, evidence_hash)
   instead of tasks_completed and RAM/CPU heuristics; per-device wallets (dogfood
   P0 ruling, docs/ref/GSTD_DOGFOOD_PLAN.md:20-23) make the rows real. Their
   files: state/gstd_full/ai/frontend/src/lib/nodes.ts:47,
   state/gstd_full/ai/frontend/src/pages/api/v1/oracle/evaluate.ts,
   state/gstd_full/gstdbot/src/swarm/client.ts.
   Our instruments: tools/gps_mcp (ledger), mag/gwap_to_gps.py (the gwap
   pattern generalized, docs/ref/GSTD_DOGFOOD_PLAN.md:47-49). Probe: two nodes
   claim identical tasks_completed but their GPS rows disagree; the router must
   pick the GPS-backed node, and a node with zero GPS rows must never win a
   routing race it did not earn.
5. VERKLE RECEIPTS ON THE SETTLEMENT RELAY. Wiring: pre-send, run the gate over
   the fetched proof; post-confirmation (waitSeqno), append a verkle receipt
   keyed taskId plus resultHash; the queue-clear becomes idempotent bookkeeping.
   Their files: state/gstd_full/contracts/scripts/settle-quorum-proof.ts:80 and
   the TREASURY_SECRET auth at
   state/gstd_full/contracts/scripts/settle-quorum-proof.ts:45. Our
   instruments: mag/verkle_bus.py, the verkle family, the census patrol extended
   to settlement rows. Probe: settle one proof end to end, then tamper the
   platform queue JSON and re-run; the ledger must flag the divergence, and
   every settled taskId must have exactly one receipt row.
6. CREDENTIAL-REGISTRY GATE ON ATTESTOR KEYS. Wiring: RegisterAttestorKey loops
   and deployment scripts check pubkeys against the estate credential registry
   before on-chain authorization; a proof file can no longer self-authorize its
   own attestors. Their files:
   state/gstd_full/contracts/scripts/verify-p2p-proof.ts:70,
   state/gstd_full/contracts/scripts/deploy-settlement-v2.ts. Our instruments:
   tools/prepush_credential_shape.py, mag/config_seal.py. Probe: take the
   verify-p2p-proof harness, tamper one pubkey in the proof JSON, re-run; the
   current script registers it (state/gstd_analysis_results.jsonl:386), the
   gated version must refuse with a named mismatch.
7. IMMUNE RACE ON THE MESH. Wiring: arm B of the race runs as three mesh nodes
   (desktop, bob, pixel per the dogfood plan) executing verifier, skeptic, and
   reproducer roles through the swarm; 50 subtly-poisoned failure reports;
   false-positive rate at bounded compute. Their files: the swarm task path
   (gstdbot/src/swarm/agent.ts, A2A task handlers). Our instruments: the
   percolator candidate (mag/seed_percolator.py; filed per the audit ruling,
   docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md:82-84), tools/free_lane_fleet.py with
   the new gstd provider (docs/ref/GSTD_DOGFOOD_PLAN.md:34-37). Probe: the
   audit's own falsifier, false positives at most 2x monolith compute on 50
   poisoned reports; if arm B cannot beat the monolith, the trust layer built
   on it dies with it (docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md:37-41).
8. SIGNED HEARTBEATS AND PEER IDENTITY. Wiring: ed25519 sign
   HeartbeatPayload at send, verify at receiveHeartbeat before a peer enters
   the table; the bootstrap endpoint serves only attested, fresh peers. Their
   files: gstdbot/src/p2p/peers.ts, gstdbot/src/node-lite/index.ts,
   ai/frontend/src/pages/api/v1/nodes/peers.ts. Our instruments: mag/seed_seal.py,
   consensus gate for the admission filter. Probe: register a peer with a
   spoofed nodeId and an unused pubkeyHex; today it wins routing
   (state/gstd_analysis_results.jsonl:683), after wiring it must be rejected and
   counted in a refusal receipt.
9. RECEIPT-FIRST COMMAND AND LOG SURFACES. Wiring: platform-auth's stale-command
   check (exported but never called, per
   state/gstd_analysis_results.jsonl:659) becomes mandatory inside both
   verifiers, and every warn/error flows to a verkle receipt sink with
   structured fields. Their files: gstdbot/src/lib/platform-auth.ts,
   ai/frontend/src/lib/logger.ts. Our instruments: verkle receipt sink, seal
   wrapper, the drift patrol watching the new receipt class. Probe: replay an
   old signed command; it must be refused as stale; send one warn through the
   logger; a chained receipt with a resolvable task_id must exist.
10. MCP DOOR WITH RECEIPTS. Wiring: the platform MCP server
    (docs/ref/GSTD_DOGFOOD_PLAN.md:44-46) and the existing ai/gstd-mcp-server
    gain a receipt-first wrapper: every execute_rpc response carries a hash
    verifiable against the estate ledger, and list_nodes output carries GPS
    ranks. Their files:
    state/gstd_full/ai/gstd-mcp-server/index.ts:29. Our instruments: the
    estate MCP bridge, verkle receipts, GPS. Probe: query execute_rpc through
    the seat door; verify the returned receipt hash independently; an
    unverifiable response must surface as a trust warning in the seat, not
    silently pass.

## 4. RISK CENSUS

Scripted classes over all 738 RISK lines (counts at
state/_gstd_incorporation_census.json:202-214); 634 rows name a trust-hole
keyword (quorum, attestation, settlement, wallet, verification, signature, or
evidence; state/_gstd_incorporation_census.json:216). 92 rows matched no keyword
cluster, the unclustered bucket (script artifact of the clustering instrument,
not evidence of safety; state/_gstd_incorporation_census.json:209).

| class | rows |
|---|---|
| unverifiable results / no evidence | 353 |
| quorum/attestation weakness | 201 |
| auth spoofing / wallet-header trust | 193 |
| RCE / sandbox escape | 173 |
| secret/key handling | 117 |
| settlement/trustless payment risk | 106 |
| stale/undocumented drift | 94 |
| centralization / single point | 62 |
| DoS/resource abuse | 49 |
| prompt/LLM injection | 31 |
| data loss / persistence | 27 |
| license/unknown provenance | 5 |

The worst five, quoted from the analysis rows (verbatim up to the cut mark):

1. Bridge vote forgery, the single worst trust hole because it sits directly on
   cross-chain money. "`record_vote` trusts `vote.voter` string membership in
   `self.validators` without verifying `signature_share` against a registered
   per-validator key, so any peer knowing a validator's PeerId can forge votes
   and reach quorum (explicitly flagged in the file's own SECURITY NOTE)."
   (finding row state/gstd_analysis_results.jsonl:409, source file
   state/gstd_full/gstd-bridge/src/consensus/mod.rs:145). Cure: mag/seed_seal.py
   ed25519 key registry plus signature verification, fronted by
   mag/consensus_gate.py (incorporation 3).
2. Attestation transport accepts anything schema-shaped. "Attestation
   acceptance is schema-only [...]" with no verification that signatureHex
   matches pubkeyHex over resultHash, no key-to-node binding, and no replay
   guard (finding row state/gstd_analysis_results.jsonl:680, source file
   state/gstd_full/gstdbot/src/p2p/node.ts:443). Cure: mag/consensus_gate.py
   construction-evidence and witness rules at the handler (incorporation 2).
3. Proof files self-authorize their own attestors. "The script trusts the proof
   JSON's `pubkeyHex`/`signatureHex`/`resultHash` verbatim and registers
   whatever pubkeys appear, so a tampered proof file would self-authorize its
   own attestors [...]" (finding row state/gstd_analysis_results.jsonl:386,
   source file state/gstd_full/contracts/scripts/verify-p2p-proof.ts:70). Cure:
   the credential registry (tools/prepush_credential_shape.py,
   mag/config_seal.py) gating RegisterAttestorKey (incorporation 6).
4. The settlement relay has one soft trust root and a truncation surface. "The
   relay trusts the platform's `/settlement/quorum-proofs` endpoint (auth =
   single shared `TREASURY_SECRET`) as the sole source of \"genuine quorum\"
   [...]" plus SHA256 truncated to 64 bits for taskIdToUint64 (finding row
   state/gstd_analysis_results.jsonl:380, source file
   state/gstd_full/contracts/scripts/settle-quorum-proof.ts:45). Cure: the
   consensus gate pre-send plus verkle receipts (incorporations 2 and 5); the
   truncation needs their-side widening, flagged to the cofounder.
5. Reward farming by default handler. "`_default_task_handler` returns
   `\"valid\": True` and `\"status\": \"completed\"` unconditionally with no
   evidence, signature, or verifier [...]" (finding row
   state/gstd_analysis_results.jsonl:36, source file
   state/gstd_full/A2A/src/gstd_a2a/agent.py:466). Cure: seal at submit plus
   immune critics as task handlers (incorporations 1 and 7).

The pattern: the top class (unverifiable results, 353 rows) plus classes 2, 3,
and 6 above are precisely the holes the R3-hardened instruments exist to close
(consensus gate, seed seal, credential registry, verkle receipts), which is the
same convergence the dogfood plan already ruled
(docs/ref/GSTD_DOGFOOD_PLAN.md:69-72): their honest gaps table and the estate's
mesh audit findings are one list.

## 5. PHASED WIRING (merged with the dogfood plan)

- P0 INPUTS (unchanged, docs/ref/GSTD_DOGFOOD_PLAN.md:20-23): per-device
  wallets owed by the operator. Instrumentation is not blocked by this; the
  seal and receipts can be exercised in dry mode on the desktop node while
  wallets pend.
- P1 DESKTOP NODE (docs/ref/GSTD_DOGFOOD_PLAN.md:25-29): node up with the
  estate Ollama garden; first task completion receipted. Landing here:
  incorporation 1 in minimal form (seal plus one ledger row class for mesh
  tasks) and incorporation 4's write side (GPS rows begin accumulating).
- P2 BOB + PIXEL (docs/ref/GSTD_DOGFOOD_PLAN.md:31-32): second and third
  devices; per-device GPS capability rows become real; incorporation 8
  (signed heartbeats) lands here because three nodes make peer spoofing
  testable.
- P3 THE DOGFOOD (docs/ref/GSTD_DOGFOOD_PLAN.md:34-49): fleet lane gstd
  provider (incorporation 7 infrastructure), GPS verdict rows (incorporation 4
  read side), the immune race through the swarm (incorporation 7), the MCP
  door with receipts (incorporation 10), receipts plus patrol coverage
  (incorporation 5's ledger side).
- P4 GATED TRUST LAYER (docs/ref/GSTD_DOGFOOD_PLAN.md:51-55): incorporations
  2, 3, and 6 (consensus gate at quorum, bridge signature verification,
  attestor registry) land only after the immune race stands, per the audit's
  build order (docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md:71-78: immune cells
  first, everything else untestable until then). Settlement RFC review and
  memory/training wiring wait for their tree to mature.
- Standing gate on everything: the gstdbot license is NOASSERTION
  (docs/ref/GSTD_DOGFOOD_PLAN.md:72-75); no estate code ports into their tree
  (nor theirs out) until the cofounder confirms the license story. Wiring by
  wrapper, mount point, or sidecar (the estate's instruments wrapping their
  endpoints) does not port code; anything that would, waits.

## 6. WHAT THE ANALYSIS DID NOT COVER (honest)

- The 126 sliced files (scripted count,
  state/_gstd_incorporation_census.json:220): the batch builder elided file
  middles behind the marker form [N lines elided of M total, K bytes], 57238
  elided lines in total (state/_gstd_incorporation_census.json:221). The worst
  elisions gut exactly the trust-critical files: gstdbot/src/gateway/server.ts
  with 4554/4854 elided (state/_gstd_incorporation_census.json:225) and the
  compiled SettlementMaster binding with 2176/2476 elided
  (state/_gstd_incorporation_census.json:229). Consequence: the on-chain
  SettlementMaster quorum semantics (how the attestations cell is validated)
  were judged from a head and tail only; the analysis row
  state/gstd_analysis_results.jsonl:357 says so itself ("no source, no
  attestation schema ... unauditable from this file"). Any incorporation that
  touches the contracts surface needs a full-file read of the elided middles
  before wiring.
- The claimed one skipped file: no byte-backed record of exactly one skipped
  file exists in this repo. The scripted disk-versus-batch diff says 1062 files
  on disk under state/gstd_full (excluding .git, node_modules, __pycache__)
  against 738 batch items, so 324 files never entered the analysis
  (state/_gstd_incorporation_census.json:243-244): 150 .tsx, 28 .js, lockfiles,
  TON build artifacts (.boc, .fif, .fc, .abi, .pkg), and 27 extensionless
  files (state/_gstd_incorporation_census.json:245-254). The singular "1
  skipped" framing understates the real coverage gap; the frontend React
  surface (all .tsx) is effectively unanalyzed.
- ok_api false rows: 0; ok_material false rows: 0
  (state/_gstd_incorporation_census.json:3-5). All 738 rows carry all five
  section labels. Total analysis cost 0.6252 USD
  (state/_gstd_incorporation_census.json:217).
- What the five-line contract could not see: (a) one-sentence RISK flattens
  compound findings (several rows pack two or three distinct holes into one
  sentence, so class counts in section 4 are floors, not ceilings); (b) HOOKS
  are model-proposed seams, not verified against imports or call graphs, so
  every wiring point in section 3 must be confirmed against the real source
  before code moves (the anchors cited there were confirmed for exactly the
  functions named, nothing more); (c) the prompt told DeepSeek the estate's
  instrument vocabulary up front (state/gstd_analysis_prompt.md:1), so the
  INCORPORATE frequency ranking measures resonance with a primed list, not
  independent discovery; 16 rows answered NONE outright and 34 named no known
  estate system (738 minus the 704 scripted at
  state/_gstd_incorporation_census.json:177); (d) skill-marketplace rows (111,
  state/_gstd_incorporation_census.json:161) are prompt-pack content where the
  only real finding repeats (unsigned source plus self-declared risk), which
  inflates the citation/seal frequency by volume; (e) the mesh audit's
  structural findings (identical-cognition confound, mirror-scorer
  circularity, no demotion path, docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md:10-28)
  are file-invisible: no per-file analysis can surface them, so the
  incorporation design must carry them as constraints, not wait for rows to
  report them.

NEXT (for the cofounder seat): confirm the license story, deliver per-device
wallets, and rule on whether incorporations 2 and 3 land as PRs into the gstdbot
and gstd-bridge trees or as sidecar wrappers while the license pends.
