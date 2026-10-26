# GSTD CLOSED PERIMETER: vast.ai + blade design (operator ask + GB req, 2026-10-10)

Operator ask: "how could we use vast ai long term rental to do this and spin up a cheap
blade server with like a thousand". GB requirement (operator relay, same sitting): "Nodes
must confirm the ability of different models to generate a consensus answer." Context:
GB's need list (mini PCs, TON contracts, gas, reward verification). All prices below are
ESTIMATE-CLASS (vast.ai pricing page is dynamically loaded; fetched 2026-10-10, only the
discount STRUCTURE is confirmed: interruptible 50%+ cheaper, reserved up to 50% off on
1/3/6-month terms, per-second billing, 68+ GPU types, 40+ datacenters).

## The perimeter's two assertions (what the fleet proves)

A1 REWARD: for every completed task, the paying node's balance/ledger delta lands as
   claimed (GB ask #4; closes our audit's settlement-theater finding on a staging rail).
A2 CONSENSUS: the same task dispatched to K nodes running K DIFFERENT models produces a
   measurable consensus - majority/exact-match for closed-form shapes (extract,
   classify), normalized-match for short answers. Output: consensus rate per task
   shape, per-model agreement matrix, divergence cases banked as receipts.
   Dead-salmon control (arXiv 2512.18792 law): consensus must beat a label-shuffled
   baseline before it counts as signal.

This is the behavioral analog of today's unisub paper claim, qualifier restored:
disjoint models converge WITHIN SHARED ARCHITECTURES (the abstract's own qualifier,
unisub_drop_20261010/CARD.md:13-14 - do not overclaim cross-architecture). A2's
fleet runs K different models across families, so the garage measures CROSS-FAMILY
BEHAVIORAL AGREEMENT - behavioral where the paper measured spectral convergence,
across families where the paper stayed within one: a claim no cited paper makes, a
better experiment rather than a smaller one (honesty edit 2026-10-10, finding 7,
ractor_engine/2026-10-10-singing-network/SYNTHESIS.md:47 - unisub qualifier restored,
cross-family behavioral agreement headline). The GPS capability ledger already holds
the per-model half (dogfood matrix); consensus is the new aggregation view.

## Arm 1: vast.ai long-term rental (elastic, $0 capex, live tonight)

- Rent M small instances (entry GPU like 3090 or CPU-heavy listings, filter console by
  RAM), each hosting K gstd-node containers: one instance = one IP = K distinct node
  identities.
- Reserved (1/3/6-mo) for the stable perimeter core; interruptible for load-bursts
  (consensus sweeps are fault-tolerant batch: a dropped node just re-joins the sweep).
- Closed perimeter: instances join a tailnet (Tailscale/WireGuard); nodes point at the
  staging platform endpoint (GB side) via per-node tunnels. Nothing touches the public
  roster.
- IDENTITY PINNING per node (the ghost-row law): each container gets a persistent
  identity/volume, else the platform mints a thousand ghost rows (the two-nodes-on-my-
  desktop disease at scale).
- RATE-BUCKET LAW: every host-originated request from one instance shares that
  instance's IP bucket (the measured docker-bridge lesson). Spread nodes across
  instances rather than stacking all on one box; or GB whitelists the perimeter IP
  range on the staging platform (the real fix, his side).
- Estimate-class sizing: a 64-128GB instance hosts 30-60 node containers (1-2GB each
  with shared small models); ~$0.10-0.25/hr class per entry GPU instance on-demand,
  roughly half that reserved or interruptible. A 5-instance perimeter core runs tens
  of dollars per month; a thousand-node LOAD TEST is a burst: 20 instances x 50
  containers for hours, not months.

## Arm 2: the ~$1000 blade (capex, permanent, guild asset)

- Used Dell PowerEdge class (R720/R730, 2x Xeon, 256GB RAM) is $300-700 on the used
  market - literally gospaceport's garage archetype. $1000 covers the box + rails +
  a small switch.
- Runs 50-100+ node containers locally at $0 marginal cost; power ~200-400W.
- SINGLE IP limit: every node behind one pipe shares one rate bucket - fine against a
  staging platform (limits likely differ there; UNOBSERVABLE until GB confirms), fatal
  against the public platform.
- Guild play: the blade is the Garage Guild's first shared asset. Benches host
  perimeter boxes; the guild's collective test fleet earns GSTD doing GB's
  verification - the demand-side flywheel with hardware.

## Recommended shape (both arms, phased)

Phase 1 (tonight, $0): docker multi-node rig on the desktop, 3-5 nodes, distinct
models, consensus harness v0 (dispatch K, compare, assert, receipt). Proves A2 on our
bytes before any spend.
Phase 2 (this week, tens of $/mo): vast reserved core, 5 instances x 10 nodes = 50
heterogeneous nodes + tailnet perimeter + staging endpoint. Proves A1/A2 at fleet
scale; GB's mini-PC need is answered by elastic capacity instead of boxes.
Phase 3 (with GB + guild): the blade(s) as permanent guild assets; burst to ~1000
nodes via interruptible vast for the launch-scale reward test (does payout hold at
1000 participants - the number that matters to GB's thesis).

## The harness (one lane, reuses estate organs)

- Dispatcher: task bank from estate bytes (the dogfood matrix's S/C/E shapes).
- Per node: model id, answer, latency, payout delta asserted.
- Aggregator: consensus rate per shape, agreement matrix, dead-salmon control arm,
  receipts to watch/inbox/. Feeds the GPS capability ledger as consensus-contrib rows.

## GB reply addendum (one line, his register)

"perimeter's covered elastic on my side - and the test itself is the part i find
beautiful: same task to a fleet of different models, consensus measured, payout
asserted per node. it's the behavioral version of the convergence paper that dropped
today, with their qualifier kept: their convergence is within shared architectures,
ours is cross-family behavioral agreement - a claim no cited paper makes. that's a
better experiment, not a smaller claim."

(qualifier restored before this enters the GB thread, honesty edit 2026-10-10,
finding 7: the unisub claim is within shared architectures,
unisub_drop_20261010/CARD.md:13-14; this perimeter tests cross-family behavioral
agreement - ractor_engine/2026-10-10-singing-network/SYNTHESIS.md:47.)
