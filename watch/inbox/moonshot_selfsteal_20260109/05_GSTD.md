# 05 GSTD - the settlement layer meets the estate (lane 5 of 5, moonshot self-steal, 2026-10-08)

## What it IS

Two layers, one hand. GSTD (gstdcoin/ai, DePIN-for-AI on TON) is the settlement
layer: nodes execute inference work, the platform routes tasks, SettlementMaster.tact
pays 85/10/5 (worker/treasury/protocol) with a taskId replay guard and TEP-74
jetton transfers (watch/inbox/THE50_W7_T31_SETTLEMENT_AUDIT.md). The estate is
the epistemics layer: it proves the work happened and happened honestly. One
hand: the operator is co-founder of the settlement side and sole owner of the
epistemics side. The trust gap GSTD's own architecture admits (signed task
format, verification classes, reputation - docs/ref/GSTD_DOGFOOD_PLAN.md standing
notes) is the exact list the estate hardened in R3. Settlement without epistemics
pays fabricators (their fraud arc, agents fabricating rewards:
watch/inbox/GSTD_FORENSICS_20260918.md); epistemics without settlement banks
findings nobody can invoice. The one-hand shape closes both.

## What we HOLD

- R3 trust teeth: the round-3 law "every trust instrument in this estate
  certifies a representation of the thing instead of the thing" plus the landed
  fixes (UNRESOLVED-SOURCE citation class, credential shapes, verdict-walk and
  seal hardening) - watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md,
  watch/inbox/ouroboros_20261005/r3_land_teeth.md. The verifier class GSTD
  lacks; dogfood P4 stages our immune cells as its 2-of-3 attesters.
- GPS router v0: learned routing on (animal x task_shape), held-out AUC 0.9434
  vs the hand-tuned scorer's 0.5012 (chance) and the incumbent ledger's 0.5198;
  5+ row evidence gate; 25 shapes ranked - tools/gps_router_v0.py,
  watch/inbox/ml_moonshot_20261007/ML3_GPS_ROUTER_RECEIPT.md + ml3_route_table.json
  (commit 9bac820a1). Task_shape as coordinates is the routing law.
- Replay verification 202/202: frozen-tape deterministic replay, sha256 run
  receipts, a one-entry input flip = INPUT_FORK at the exact frame (mud 41/41
  + mud fifty 63/63 + toy 15/15 + frontier 51/51 + swarm 32/32) -
  watch/inbox/GWAP_BACKEND_RESEARCH_20260929.md.
- The dogfood stack: P0 wallet paste, P1 desktop FULL node, P2 bob/pixel
  node-lite, P3 the fleet lane that PAYS - docs/ref/GSTD_DOGFOOD_PLAN.md;
  docs/ref/GSTD_FLEET_LANE_SPEC.md (wallet gate fail-closed, gps_mesh_row.v1
  keyed (node_device, task_shape, evidence_hash), sha256 of completion bytes);
  tools/gstd_fleet_provider.py; tools/gstd_es_trainer.py (fitness-only travel:
  scores cross the wire, gradients never - docs/ref/GSTD_ES_MESH_TRAINER_SPEC.md).
- HyperThink build shape: GSTD ExperienceRecords promote-weights -> per-domain
  LoRA deltas routed by GPS task_shape (commit f859317c3, watch/inbox/LINKS.jsonl).
- The wire-ready runbook: one paste, three per-device TON addresses, fires P1
  end to end - watch/inbox/GSTD_WALLET_DOOR_20261007.md (byte-traced against
  gstdbot tip e0bbe48; fail-closes on the Ollama 127.0.0.1 bind blocker).

## STATE

- LIVE (their side): platform.gstdtoken.com answers HTTP 200; 4 registered
  nodes, all household; only the Bootstrap Pi earns (272 tasks, 47.39 GSTD,
  reputation 55) - watch/inbox/GSTD_NODE_CENSUS_20261007.md. Swarm growth
  beyond the household has NOT fired.
- STAGED (our side): desktop FULL node compose-validated exit 0 with no
  container started; wallet-door runbook byte-proven; fleet provider skeleton
  plus tests landed; ES trainer skeleton landed; mesh expansion roster staged
  (tablet, smashed-screen phone, 6 Rokus - commit 193bd303b).
- BLOCKED: everything that earns waits on the operator's three per-device TON
  addresses (P0, the wallet paste, his move). Second blocker, fix in hand:
  Ollama binds 127.0.0.1 only, so bob, pixel, and the desktop container cannot
  reach the garden until OLLAMA_HOST=0.0.0.0 plus restart (netstat proven
  2026-10-07, wallet door section 6). Bob SSH key auth and Pixel Termux
  prereqs unmet (watch/inbox/GSTD_POOL_SETUP_20261001.md bodies table).
- On-chain caution: SettlementMaster owner equals the protocolFee EOA,
  single-key custody, DAO handover open (T31 finding 4) - settlement is
  not trustless yet either; our epistemics half is the mitigant today.

## COMPOSITION

| with | the join | why only the pair gets it |
|---|---|---|
| WoW machinery | GWAP verified play IS the work GSTD settles: agreement payloads plus frozen-tape replay (202/202) turn play into byte-backed evidence; the fleet spec's evidence_hash is the same artifact class | a settlement layer can pay any claimant; the pair pays provable work. "A platform where play is provable" (GWAP research 1.4) becomes a network where play is payable |
| token economics | internal accounting settles externally: hermes_burn banks tokens and cost per dispatch (memory/runs/hermes_burn/usage.jsonl), cost_rollup meters $135.71 lifetime, the router priced animals at $0.003972 (haiku) vs $0.072038 (fable) per paid call over $94.74 measured spend | the estate already runs a paper settlement economy in USD-typed rows; GSTD is the outer rail for the same ledger shape. Internal verdict rows become invoiceable work with zero new accounting code |
| 5h window | the rolling 5-hour provider quota is our scarcest compute: 6 wall moments and 24 coded lane deaths on a day whose dollar field read $0.18 (watch/inbox/QUOTA_LEDGER.md); the quota ledger already renders it as currency (fires, walls, GREEN/AMBER/RED) | DePIN prices idle capacity; our window is expiring demand-side capacity. Leasing mesh node-minutes for pennies (ES trainer: pay in kilobytes) buys window relief, and GPS decides which paid call is worth window spend - the same meter prices both sides |
| mesh | earning nodes ARE mesh nodes: three bodies on tailscale (desktop 17-model garden, bob, pixel) are already one dispatch surface; per-device wallets make each an earning DePIN node; GPS keys capability rows by node_device, so the mesh's capability surface becomes routeable data | the fleet and the farm are the same machines - the DePIN fleet the operator co-founds is the estate's own three-body mesh plus the staged tablet and smashed-phone roster |

## MOONSHOT

The full stack only this estate can assemble, because one hand holds both
layers: play-as-work (a noir scene, a MUD run, a WoW session) -> replay-verified
(202/202 machinery, sha256 receipts, INPUT_FORK detection) -> agreement-scored
(the GWAP payload turns play into labels) -> GPS-routed (task_shape coordinates
pick the animal or node at 0.9434 AUC, evidence-gated) -> mesh-distributed
(desktop, bob, pixel, tablet execute; training loops travel fitness only) ->
GSTD-settled (85/10/5 per verified task, replay-guarded taskId) -> attested by
R3-hardened instruments (2-of-3 quorum from the estate's immune cells, P4).
Every link is landed bytes today; no rival holds even two links. A competitor
must build verifier, router, fleet, and trust instruments from zero, then win
a settlement network over. We are that network.

## SELF-STEAL

- The five assets were already cross-cited in our own bytes; this lane joined,
  it did not invent: dogfood P3 already names the GPS ledger join; the fleet
  spec's evidence_hash already implements the GWAP receipt law; the HyperThink
  card already drew ExperienceRecords -> LoRA deltas -> GPS routing.
- Stolen from sibling lanes by reading, not rebuilding: the quota ledger
  (window as currency), the GWAP research (verified play), the R3 synthesis
  (representations vs things), the ML3 receipt (the router and its price book).
- Refused temptation: hand-writing a GSTD status from memory. Every claim
  above traces to a receipt path; the two things NOT knowable from bytes are
  named where they bind (platform-side wallet validation UNREAD; bob OS flavor
  UNVERIFIED - wallet door sections 6 and 5).

## FALSIFIER + PROBE

Falsifier: a wallet-pasted quarter where GSTD settles tasks but no estate
instrument verifies one - no gps_mesh_row keyed on external evidence, no
replay receipt cross-checked against a settlement event - means the trust layer
never landed on the settlement layer and the one-hand shape is a slide deck.
Short-range version (fleet spec section 8): mesh_ledger.jsonl grows while
gstd-mesh capability rows stay flat in gps_ledger.db3 = burning without paying
data; fix evidence capture first.

PROBE (cheapest executable step that is NOT the wallet; $0, read-only, no
container, no ledger write): route the LIVE network through OUR router.
1. One curl: https://platform.gstdtoken.com/api/v1/nodes (the census lane's
   one-permitted-curl precedent) - fresh capability bytes for the 4 live nodes.
2. Join each node's reported capabilities (llama3.2:3b, qwen2.5:7b, empty)
   against watch/inbox/ml_moonshot_20261007/ml3_route_table.json: which of the
   25 evidence-backed task shapes could the live network serve today?
3. List the desktop's 17-model garden (ollama ls) against the same table.
4. Receipt the gap. Expected honest outcome: the live network serves none of
   our fat shapes (the table's best_animals are API-tier), while the garden's
   locals cover the cheap lanes - so the desktop FULL node (P1) is the only
   join that makes the network useful to the estate, derived at $0 before any
   wallet moves. A live node already serving a fat shape would mean the
   thin-shape gate fired or the network grew - both findings, the second
   unfreezes falsifier 5. Output: one receipt beside this file.
