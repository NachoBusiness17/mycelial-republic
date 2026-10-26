# GSTD REPUBLIC COOKBOOK - Lane C, incorporation + enhancement - 2026-10-09

Inputs eaten: A = GSTD_CODEBASE_AUDIT.md, B = GSTD_TOKENOMICS_AUDIT.md,
D = GAPS_AND_PEOPLE.md, DF = DOGFOOD_DATA.md, VOCAB = ROUTER_VOCAB_LANDED.md,
3B = THREE_BODY_MAP.md, CONST = mycelial-republic CONSTITUTION.md Art 1/7/15,
DIST = gstd_distribution_thesis_20260109.md, RIB = RIB_NOT_EVEN_ME_20261009.

STANDING RULE ON VOLUME (Lane B, binds every spec): live routing is
net-emission-subsidizing - fees 0.001/task vs payouts 0.002-0.0095, no fee
counterparty on uptime, 91% of emissions on the operator's own address
(B sec 1, 3). Until the signed lane lands (P2.1), ALL estate usage is
settlement-surface experiments at LOW VOLUME, the dogfood shape of ~1 req
per 10-15 s (DF sec 2, 4). Rails throughout: fork equality (CONST Art
1.4; A gap (e)); their wallet, opt-in support (CONST 15.1, RIB clause 1);
T0/T1 never leave - only T2 public bytes ride GSTD prompts (CONST Art 7).

## PART 1 - INCORPORATION BUILD SPECS (estate side, ranked)

### 1.1 Router tier daily lane (LANDED - now make it a habit)
- WHAT/WHY: config.gstd.json + 14 garden providers, tier gstd first, 4
  evidence-gated verdict rows banked (VOCAB sec 3-4); remaining work is
  the DAILY LANE, not the wiring.
- FIRST BYTE: scheduled keep-alive, one warm summarize ask per day via
  pace_run.py (VOCAB sec 3), one verdict row per run.
- WIRES: tools/gps_mcp/config.gstd.json, gps_ledger.db3, receipts.jsonl;
  a registered daily task (the fts/census pattern, AGENTS.md).
- FALSIFIER: router stops choosing gstd, or tunnel dead while platform
  last_seen stays fresh - refresh via /tmp/gstd_tunnel_url.txt (3B
  collision 3); zero new verdict rows in a week = dark tier.

### 1.2 Earnings row on the estate smith
- WHAT/WHY: a gstd organ in tools/estate_smith_chart.py charting
  gstd_earned, reputation, tasks daily from the public nodes API (B); rep
  is unobservable (D G3), ours DECAYED 59 -> 49 while earning (B sec 2),
  and the smith's law says a dark meter is a finding (its docstring).
- FIRST BYTE: logs/gstd_census.jsonl - daily GET appending one row (ts,
  node_id, gstd_earned, reputation, tasks_completed, price).
- WIRES: small .venv fetcher, one organ_lanes() row, a daily task;
  snapshot side in state/gstd/.
- FALSIFIER: a day gap in the jsonl = organ DARK; counter moves with zero
  task receipts on our side = settlement theater visible by bytes (B sec 1).

### 1.3 Mesh bridge: mesh_delta over the tailnet + P2 fleet
- WHAT/WHY: mesh_delta serve on the desktop bound to the tailnet IP, pull
  on bob/pixel (sha-verified chunks), then P2 = bob + pixel node-lite,
  each with its OWN fresh wallet (3B collision 4; P1 P2-owed;
  GSTD_POOL_SETUP_20260101.md) - the single-volume cure.
- FIRST BYTE: desktop `serve --bind <tailnet IP>`, then bob `pull
  --peer ...` sha-verified dry-report.
- WIRES: tools/mesh_delta.py both ends; upstream gstdbot is READ-ONLY -
  we run containers, we do not fork yet.
- GUARD: node-lite is a whole-Ollama open proxy via an unauthenticated
  tunnel (A finding 9) - each device sits behind Cloudflare Access
  service tokens + path allowlist BEFORE any node_url registration (D C9).
- FALSIFIER: peers=0 past P2, or census capability count collapses when
  gstd-desktop goes dark (3B collision 4); second device earns from zero,
  retired vault address stays dark (3B (e)).

### 1.4 Installer step: the Article-15 screen (demo 2026-10-30)
- WHAT/WHY: one wizard screen in the CLI/Electron installer - (a)
  generate ed25519 device key, show its did:key string (D C12, ranking
  3); (b) the Article-15 choice screen, "route X pct of rewards to the
  project", default OFF, revocable, never a condition of function (CONST
  15.1, DIST); (c) optional wallet paste, theirs alone (DIST).
- FIRST BYTE: keygen module + registration carrying node_pubkey (the
  field exists upstream, platform-link.ts:120 per A gap (c)).
- WIRES: installer repo dwfrun-acfbe081 (DIST), consent copy drafted in
  DIST; license surface clean pre-demo (DIST).
- FALSIFIER: any default-on founder routing surviving review is
  clause-void (RIB falsifier); demo conversion measured, not claimed.

### 1.5 GWAP payload wire: replay receipt as task evidence class
- WHAT/WHY: the arena replay receipt (sha256 + cost row) IS the unit -
  verdict -> local ledger -> one low-volume GSTD settle; one hand, two
  layers (3B (d); FOLD: 202/202 frozen-tape replay proven).
- FIRST BYTE: one replay receipt serialized to the evidence_hash shape
  plus ONE ledger row keyed on the settlement event (PROBE2 sect 6, 3B
  (b)).
- WIRES: agent_arena replay output -> evidence record -> the 1.1 lane at
  dogfood pace; the gps_ledger row names the settlement event id.
- FALSIFIER: replay cannot verify = no mint (3B (d)); a settle with no
  ledger row = poetry, not plumbing (3B (f)).

## PART 2 - ENHANCEMENT PROPOSALS BACK TO THE BONES

### 2.1 Signed settlement spine (first - everything waits on it)
- GAP: production lanes unsigned (A finding 12: push server.ts:4604-4617,
  poll platform-link.ts:287-297); the signed lane targets PHANTOM methods
  - verifyQuorum/SettleTaskWithProof grep ZERO in contracts (B seal
  verdict); SettleTask trusts gateway fields (SettlementMaster.tact:128). D G1.
- MECHANISM: push + poll carry node_sig exactly as the swarm lane does
  (agent.ts:991-995), platform verifies vs the registered node_pubkey
  (platform-link.ts:120; D ranking 1); then bind prompt_hash + params +
  result_hash into the signed message (attestation.ts:46-51 omits the
  prompt, A design-questions); land verifyQuorum or strike the reference.
- SIZE: first PR PR-sized, machinery exists (A verdict rank 1); the
  contract method spec-sized (A gap (a)).
- FIRST PR: sign push + poll completions; volume scales only after it
  lands and is observed.

### 2.2 ton_proof node identity (the D-lane steal)
- GAP: node identity is a knowable string, not key possession - claim
  authenticates with X-Wallet-Address only (A finding 11, server.ts:2511-
  2534); "earnings custody reduces to knowing a string" (B sec 3). D G2.
- MECHANISM: wallet signs app payload (domain + timestamp + nonce) at
  register/heartbeat/claim; gstd already depends on @ton/crypto (D C6,
  best steal of the census); promote requirePeerAuth (server.ts:203-240)
  to the platform lane, PeerId-shaped (D C7).
- SIZE: PR-sized node-side, bundled with 2.1 in D ranking 1.
- FIRST PR: /api/wallet/claim + register carry and verify the signature.

### 2.3 Offline queue-settle ledger
- GAP: offline = standalone chatbot, no earning, no settlement (A gap
  (d), CENTRAL_DEPENDENCIES.md:8-13); queues cover reports, not task
  acquisition (agent.ts:789-871; B PARTIAL verdict). D G6.
- MECHANISM: extend pending persistence across restarts to cover
  settlement state; append-only local ledger, replay on reconnect (eltoo
  defer-settle D C10; automerge merge D C11); only the net delta settles.
- SIZE: spec-sized (A gap (d)); first PR PR-sized.
- FIRST PR: persist + replay the settlement queue; verify with an
  airplane-mode dogfood (D ranking 2).

### 2.4 Replay-verified settlement - OUR contribution
- GAP: the genesis seal "supply grows only with verified work"
  (state/gstd/genesis.json) has NO enforcement site (B seal verdict); D
  O1 BUILD-OURSELVES - nobody binds "this answer served this ask,
  provably by re-execution from a frozen tape" (A gap (a)).
- MECHANISM: settlement accepts an optional evidence_hash (tape pointer +
  cost row); the platform SAMPLES then RE-EXECUTES the frozen tape
  (Livepeer, D C4), disputes escalate bisection-style with our tape as
  challenger (OP Stack, D C3); zkML/TEE prove math or environment, not
  the binding (D C2, C5); only we keep tapes + replay (202/202, FOLD).
- SIZE: spec on the platform side; our side the receipt exists (1.5).
- FIRST PR: evidence_hash field on the task record + one replay-verified
  settle demoed end to end.

### 2.5 Fairness runbook - the co-founder's homework list
Said as allies, all byte-cited (DIST: honesty is the moat).
- (1) EMISSION CONCENTRATION DISCLOSURE: 91% of visible emissions went
  to the operator's own address (B sec 3) - one honest published
  paragraph beats discovery by a third party. First PR: that page.
- (2) DAO-TRANSFER COMPLETION: SettlementMaster.owner is STILL admin,
  phase2_todo open since deploy 2026-07-08; the kill switch + baked
  PLATFORM_PUBKEY_HEX let one wallet silence every node (B sec 3; A gap
  (e)). Size: one owner tx; the fork-equality unlock (CONST Art 1).
- (3) PUBLISHED REPUTATION SEMANTICS: no formula anywhere; our score
  moved 59 -> 49 while earning (B sec 2; A gap (b): "without it every
  payout is faith"). Render-style published tiers is the honest shape (D
  C8). Size: a spec page + a node-side logging PR.

## THE SEQUENCED ROAD

THIS WEEK: (1) earnings row on the estate smith - 1.2, pure estate. (2)
spine first PR upstream + our node on the signed lane - 2.1 (A verdict
rank 1). (3) mesh_delta serve over the tailnet + bob pull dry-run - 1.3.

THIS MONTH: (1) installer wizard screen with device-key + Article-15
choice - 1.4 (D ranking 3). (2) ton_proof identity + offline queue-settle
first PRs - 2.2 + 2.3. (3) GWAP payload wire live at dogfood pace + the
replay-verified settlement spec filed upstream - 1.5 + 2.4.

BY THE CONF DEMO (2026-10-30): (1) the installer GSTD screen demoed end
to end, support toggle default OFF, conversion measured not claimed -
1.4. (2) one replay receipt carried as a GSTD task payload, settled,
with its ledger row - the seal made true once, on stage - 1.5 + 2.4.

Thesis: GSTD is a measurement instrument with a settlement rail, not a
market (3B) - we incorporate it as our low-volume settlement surface
while selling it the one bone only we keep: proof by re-execution.
