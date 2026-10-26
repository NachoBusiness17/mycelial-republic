# STEAL CARD: inference-efficiency (frontier_olm 2026-10-07, round 2 REVISE applied)

Round 1 was REVISED on three grounds, all verified against bytes this session: a false
zero-overlap receipt for Steal 1 (the grep omitted watch/inbox, the root where every frontier
bank lives), an organ claim already falsified by the same-day ML3 GPS ROUTER v0 landing, and a
port move that re-walked a path ML3 measured at chance. This round corrects all five required
fixes. Steal 2 stands approved from round 1 and is carried forward unchanged except for one
unsourced detail struck from its probe.

Seat: steal-inference-efficiency gopher. Both source pages fetched live in round 1
(WebFetch, 2026-10-07); quotes byte-verified against the live pages.

---

## Steal 1: Weave Router, parity-constrained composite tier routing (v1 blog vs v2.0 thread)

Source: https://weaveos.com/blog/introducing-weave-router-right-sizing-inference-for-production-agentic-workloads

Verified quote: "On production Claude Code traffic, we're measuring 80 to 85 percent cost
reductions with no observable quality regression" (vendor self-reported, no third-party audit;
the number is OWED as estate-measured, the mechanism is the steal).

### PRIOR HOLDINGS (round 1 falsely declared zero; corrected)

The Weave Router prior is ALREADY BANKED, in two generations:
- v2.0 generation: watch/inbox/frontier_olm_2026-10-04/sweep/inference-efficiency-hn.md
  item 8 (full HN thread 49911500, raw at sweep/_ihn_thread_49911500_routing_agents.txt): HMM
  session state, classifier to a bucket of similar-capability models, RL pick within bucket,
  the cache-EV switching subsystem ("This is where most of our improvement on cost has come
  from"), per-turn routing ("they only route once per session... Imo this is basically
  impossible to do correctly"), escalation-salvage, provider cooldowns.
- v1 bytes, this same run's sibling sweeps: sweep/inference-efficiency-x.md RQ1/RQ3 carries
  ONNX embedding + frozen centroids + cost/latency/verbosity composite under parity +
  session-sticky + 80-85% + 60-70% short/simple + one-fortieth cost; and
  sweep/inference-efficiency-hn.md:67 explicitly lists Weave Router 2.0 as "Known, NOT banked
  (re-banking is waste)" pointing at the 10-04 bank.
Corrected overlap grep (this session):
`rg -l -i "weave ?router|weaveos" watch/inbox/ catalog/catalog.jsonl memory/ corpus/`
returns 20 files, 18 of them under watch/inbox (10-02 through 10-07 sweeps, the 10-04 thread
txt, and this card itself). The catalog/memory/corpus scopes stay zero-hit, which proves
nothing about the estate: watch/inbox is where frontier banks land. Overlap scope law for every
future card: the grep must include watch/inbox or it is not an estate overlap check.

### v1 vs v2.0 reconciliation (a steal must reconcile generations, not silently steal the older)

The v1 blog's "session pinned to its first routing decision" was a cache-preservation
HEURISTIC. The v2.0 thread replaces that heuristic with an explicit expected-value calculation:
when is paying the one-time cache-fill cost of switching models worth it, with the vendor
naming cache EV, not model selection, as where most cost improvement came from, and routing
moving to per-turn. What survives constant across both generations: quality parity as the
constraint, cost as the objective, and cheap typed classification (one small-model forward
pass) rather than clever premium selection. Three independent designs this month (per the 10-04
bank's synthesis) converged on the same law: most measured savings come from NOT switching.

### The surviving delta (small, and honestly small)

Against what the estate already holds and already built, the v1 blog adds exactly two things
neither the 10-04 v2.0 bank nor ML3 carry:
1. Latency and verbosity as SCORED AXES inside the composite (cost is not the only objective
   term; parity is still the constraint).
2. Prompt-side features: the frozen-centroid ONNX embedding classifies the request TEXT. ML3's
   frame is exactly text-blind (its 3753 rows carry node/animal/task_shape categoricals; the
   percolator lexicon baseline scored AUC 0.5012 on this job precisely because the rows carry
   no text, ML3_GPS_ROUTER_RECEIPT.md, "Why the percolator baseline sits at chance").

### Organ fed and port move (rewritten against ML3)

The classifier front half the round-1 card called "missing" EXISTS, measured the same day 76
minutes before that card was written: watch/inbox/ml_moonshot_20261007/ML3_GPS_ROUTER_RECEIPT.md
- sklearn logreg/GB on (node, animal, task_shape), time-split AUC 0.9288/0.9434, a 25-shape
evidence-gated route table that fails closed ("do not route" under 5 rows; ungated argmax is
the grok-4.7 thin-sample trap), and a measured cost block (haiku $0.003972 per paid row on 672
rows; classical lane $0.00). The port move is therefore NOT "build the front half" and NOT the
percolator path (measured at chance for this job):
- Amend, do not build: if ML3 v1 ever extends its objective, the v1-blog composite is the prior
  shape for adding latency/verbosity axes to the route-table ranking, under the same >=5-row
  evidence gate.
- Prompt-side features, if ever added, must use the frozen-centroid cheap-embedding shape (one
  small-model pass), never a text lexicon over ledger rows (the measured-dead path).
- Session-stickiness as a v1-style blind pin is superseded: the estate already holds the better
  v2.0 shape (cache-EV switching math) plus its own frozen-prefix cache law.

Artifact-bundle wording fixed: the blog says the scorer "is shipped as a versioned artifact
bundle" (vendor claim, round-1 fetch). We have not fetched that bundle; whether it is readable
or runnable by us is OWED, not asserted either way.

---

## Steal 2: DeepSeek live pricing: the levers are timing, cache, concurrency; there is NO batch lever

Source: https://api-docs.deepseek.com/quick_start/pricing (living page, fetched 2026-10-07)
APPROVED at round 1; carried forward unchanged.

Verified quote: "All other hours are off-peak, including weekends and Chinese public holidays in
full." Peak = 01:00-04:00 and 06:00-10:00 UTC Mon-Fri (excluding Chinese public holidays);
off-peak rates are half of peak.

Verified table (USD per 1M tokens, off-peak / peak):
- deepseek-flash: input cache-hit $0.003 / $0.006; input cache-miss $0.15 / $0.30; output $0.60 / $1.20
- deepseek-v4-pro: input cache-hit $0.022 / $0.044; input cache-miss $0.66 / $1.32; output $1.98 / $3.96
- Concurrency caps: flash 2500, pro 500.
- Batch discount: NONE. The page's only discount structure is off-peak halving; no batch tier
  exists (absence verdict on the page as fetched 2026-10-07; page self-warns "Product prices may
  vary", so re-verify at encode time).

This is the invoice-strength answer to the owed discount check at
watch/inbox/frontier_olm_2026-10-07/lens/burns.md:221-222: no batch lever exists; the levers are
WHEN you fire (off-peak halves everything), PREFIX STABILITY (flash cache hit is 50x cheaper
than miss: 0.003 vs 0.15), and WIDTH (caps 2500/500 are far above our envelope, so concurrency
is a non-binding lever for us today).

Estate overlap: partial, as the find stated. memory/burns/MANIFEST.json:21 already holds the
off-peak windows, the halving, flash cache-hit $0.003, and the pro 30x cache advantage. NEW
bytes (verified absent from the manifest by grep for 2500/concurrency: zero relevant hits): the
full per-token table including peak and output prices, the explicit no-batch-discount verdict,
and the concurrency caps.

Organ fed: the ds_workhorse lane (the fleet's cheap batch lane) plus the burns manifest.
Concrete port move: tools/ds_workhorse.py:102-105 meters every call at a flat $0.27/M in,
$1.10/M out, reading only prompt_tokens and completion_tokens; it drops the cache split the API
already returns (prompt_cache_hit_tokens / prompt_cache_miss_tokens are in the same usage object
read at :101) and ignores time-of-day. Replace with the time-and-cache-aware table above: cost =
hit_tokens * hit_price + miss_tokens * miss_price + completion_tokens * out_price, price set
selected by the MANIFEST:21 window predicate. Extend MANIFEST.json:21 with the full table, the
no-batch verdict, and the caps so the next lens does not re-derive this.

---

## Falsifiable probes (cheap, this week)

THE probe (approved round 1, fired unchanged; one live batch, cents; serves the cache half of
both steals):
Run one 2-pass batch through `.venv\Scripts\python.exe -m tools.ds_workhorse run` with the same
20 items and the same prompt template, pass 2 immediately after pass 1; bank
usage.prompt_cache_hit_tokens / prompt_cache_miss_tokens per row (field is already in the API
response, currently discarded at tools/ds_workhorse.py:104-105); recompute cost under the live
table. FALSIFIERS: (a) pass-2 cache-hit share = 0 -> prefix stickiness does not compound on this
lane, so the 50x lever AND the router-generation cache-EV rationale are dead for our traffic
shape; (b) recomputed cost >= flat-meter cost -> off-peak/cache metering saves nothing on our
shape and the port is not worth the code. Round-1's parenthetical "DeepSeek cache needs a stable
>=64-token prefix" is STRUCK: no page we hold states a 64-token minimum (grepped
sweep/_raw/deepseek_kv_cache.html and siblings this session: no such line); if a minimum exists
it is OWED, and the probe measures our actual hit share without needing it.

Steal-1 probe ($0 arithmetic over existing ML3 artifacts, replaces the round-1 counterfactual
census that ML3 already superseded at 3753 rows with cost_block): re-rank ML3's existing
ml3_route_table.json shapes with latency and verbosity added as axes in the composite objective,
same held-out frame, same >=5-row gate. FALSIFIER: gated picks unchanged -> the v1 composite
axes add nothing on our shapes and the steal is fully absorbed by what the estate already holds;
nothing further is owed.

## OWED / not verified
- Weave's 80-85% / 52%-of-Astra-cost / parity claims: vendor-reported, no readable audit
  artifact fetched; never assert as estate truth.
- The versioned artifact bundle the blog says ships: unfetched; readability OWED.
- No-batch-discount: an absence verdict on a living page; re-verify before encoding prices.
- Any prompt-cache prefix minimum: unverified on every page we hold; the 2-pass probe measures
  our real hit share regardless.
- Both probes: named, NOT run this session (this card is the draft; the burns ledger owns
  firing).

## Receipts
- Both URLs fetched and quotes verified live in round 1 (WebFetch x2, 2026-10-07).
- Corrected overlap: `rg -l -i "weave ?router|weaveos" watch/inbox/ catalog/catalog.jsonl
  memory/ corpus/` = 20 files, 18 under watch/inbox (round-1 scope without watch/ = zero hits,
  which was the defect).
- 64-token strike: `rg -o -i ".{40}64.{40}" sweep/_raw/deepseek_kv_cache.html | rg -i
  "token|prefix|cache"` = no matches.
- Estate cites: tools/ds_workhorse.py:101-106, memory/burns/MANIFEST.json:21,
  watch/inbox/frontier_olm_2026-10-07/lens/burns.md:217-222,
  watch/inbox/frontier_olm_2026-10-04/sweep/inference-efficiency-hn.md item 8,
  watch/inbox/frontier_olm_2026-10-07/sweep/inference-efficiency-x.md RQ1/RQ3,
  watch/inbox/frontier_olm_2026-10-07/sweep/inference-efficiency-hn.md:67,
  watch/inbox/ml_moonshot_20261007/ML3_GPS_ROUTER_RECEIPT.md (metrics table, percolator-at-
  chance section, cost block), mag/percolator.py:125-145 and :198-210 (via ML3 receipt).
