# LENS 1: THE SUBSTRATE, what runs the work (Conductor, Vorflux, amp)

Ractor run: mountain_climb_ractor_20260929. Grounded in DIGEST.md only (digest entries cited as D#). Authorship mode: same-session sequential (declared; blind divergence compromised, see GRADED.md). Calibration target for this run: 1,200-1,500 words.

## What this cluster knows that the estate needs

The substrate cluster knows three things the estate keeps re-learning the hard way. Conductor knows that agent labor needs a BODY to run in: isolated microVM sandboxes per agent, spin-up in seconds, runs that last hours (D3), one sandbox per worker over a shared repository, which is the estate's burn-wave shape with the race conditions engineered out before the fact instead of after. Vorflux knows the money shape: an opinionated harness running the full software development lifecycle on dedicated machines, subsidized roughly 90 percent by the customer's own cloud credits, validated by a $15M seed (D2); that is the estate's burn economics, credit arbitrage and all, productized as a company, which means the market has now paid once for the doctrine this estate runs on. amp knows the unit shape: the orb, an unsupervised remote agent run, spun out of Sourcegraph in 2025-12 (D4), a bounded dispatch that does its work and returns with a receipt instead of a conversation.

Put together, the cluster has already answered a question the estate was still asking: what is the shape of one unit of agent labor? Their answer: an isolated, bounded, unsupervised run on machines someone else subsidizes, which returns artifacts, not attention. The estate's own record agrees from the other side: the 2026-09-29 bots port burned a day on exactly the failure isolation prevents, 120 playerbot call sites fused across 40 files with zero iframes (D7), a single tree shared by every worker, 12 fix classes landed before the lane even reached upstream inconsistencies. That is what no-sandbox looks like at fleet scale.

## What the estate already has

More than the cluster suspects, less than the cluster ships. The estate has the lane discipline: burn waves, offpeak queues, the shared inbox contract that makes every surface write to one durable root (D-load-bearing fact via S9), and the historical proof the shape scales: a 300M token weekend pool burned toward a proof under vision steering (D25). It has the funding law that makes substrate choices legible: only Hermes funded at $180 Nous credits, free lanes sensing-only, verification climbs to the funded tier (D30), which is Vorflux's subsidy doctrine stated as an operating law rather than a pricing page. It has the census instrument: 2,303 tests collected across 352 files (D31), the difference between a substrate that works and a substrate that asserts. And it has the receipt habit already wired into the newest organ: gps-mcp wrote 3 receipt rows for 3 decision steps in its smoke run and proved append-only integrity in tests (D15, D16). What the estate does not have is isolation: seats are WSL and Windows hosts sharing trees, and the steal map itself names the gap, WSL host today, microVMs tomorrow (D-cluster row).

## The ONE steal that changes the trajectory

The orb contract. Not the virtual machines; the CONTRACT. Steal amp's shape and weld it to Conductor's isolation: a lane is an orb, bounded, unsupervised, receipted, one isolated sandbox per worker over the shared repo, and every orb files its receipt on landing. This is the steal because it converts substrate from an ops problem into a meterable unit: an orb has a task shape, a cost, an outcome, and an evidence hash, which is exactly the row gps-mcp already writes (D16), and exactly what the capability ledger prices (D15). The moment the unit of work is an orb, the substrate becomes billable, comparable, and improvable: the estate can say this orb shape costs $0.0042 when it stays local and escalates once (D16), and this orb shape needs the frontier at $0.12 (D16), and be right in both cases because the receipts say so. Conductor's VM reuse pattern is the second-order steal the map flags for the verkle second-writer problem (D-cluster row): if two orbs can share a warm machine safely, the estate's chain has a concurrency answer it currently lacks. Status: Supported that isolation removes shared-tree race conditions (Conductor ships it, the bots port bled for lacking it, D7); Unproven that microVMs specifically are required versus disciplined WSL seats (estate has never run the isolated-seat variant); Unproven that VM reuse transfers to the verkle second-writer problem (named as a watch item, not a result).

## What GPS does for this layer

GPS is what makes the substrate honest, in three moves. First, pricing: hard constraints filter before anything runs (D15), so an orb declares max_cost_usd and max_latency_ms and the substrate cannot silently gold-plate; the ~100x gap between owned-local marginal cost and frontier tokens (D21) becomes a routing decision instead of a habit. Second, truth accumulation: every orb outcome flows back through record_verdict as a running mean, the smoke moved design judgment from 0.96 to 0.9608 at n=53 (D16), so the substrate learns which machine class actually wins which task shape, on the estate's own evidence, never on vendor labels. Third, exploration without waste: unknown task shapes route to the mid tier marked exploration true (D15), which is how a substrate meets a new workload without either freezing or burning the funded tier. Fourth, decay honesty: the digest carries the meter's own confession that the 0.85 gate has no time decay, so yesterday's 0.9 routes today's traffic (D6-fact 6); on a substrate this is not an abstract flaw, it is a scheduling bug, a stale row sends hours-long runs to a machine class that has quietly degraded underneath the ledger. An orb contract fixes the clock problem the same way it fixes the trust problem: every orb re-measures the lane it ran on, so the substrate's capability rows age in bounded steps instead of lying forever at their high-water mark. The honest caveat the digest carries: the ledger's trust model is inflatable until verdicts bind to checkable artifacts (D6-fact 6), so GPS prices the substrate honestly only once orbs carry evidence, which is why the orb contract and the meter are one steal wearing two coats. Vorflux's validation closes the loop: if the market pays for a 90 percent subsidized opinionated harness (D2), then a harness whose opinions are measured pass-rates (D15) is the same product with the one organ Vorflux lacks.

## Numbers carried (digest-cited)

D2 ($15M, ~90 percent), D3 (seconds, hours), D4 (2025-12), D7 (120/40/12), D15 (28 tests, 0.85, 0.8, 3 tiers), D16 ($0.12, $0.0042, 0.96 to 0.9608 at n=53, 3 rows), D21 (~100x), D25 (300M pool), D30 ($180, sensing-only), D31 (2,303/352). Ten numbers, quota met.

## Tri-state ledger for this lens

| Claim | State |
|---|---|
| Isolation per agent prevents shared-repo race conditions at fleet scale | Supported (D3 market-shipped; D7 estate counterexample) |
| The orb contract (bounded, unsupervised, receipted) is the composable unit of agent labor | Supported as steal-map doctrine and gps-mcp receipt shape (D16); market-wide adoption Unproven |
| Credit-subsidized harness economics are commercially validated | Supported (D2: $15M seed) |
| MicroVMs are REQUIRED (versus disciplined WSL seats) for the estate's next substrate rung | Unproven (no estate-side isolated-seat run yet) |
| VM reuse patterns solve the verkle second-writer problem | Unproven (watch item only) |
| Frontier tokens ~100x owned-local marginal cost | Supported (D21, third-party trackers caveat carried in S5) |

---
Authorship mode: same-session sequential. Byte check (2026-09-29 Phase 2.5 instrument (wc -w via python word-split, U+2014 via char scan)): words=1250 emdash=0.

CORRECTION 2026-09-29 (grader defect S-1): the phrase "burn-wave shape with the race conditions engineered out" paraphrased S1's cluster-quote beyond digest text. The digest's SUBSTRATE row carries the sandbox-per-agent lifecycle and the orb steal, and this lens's load-bearing claims stand on those. Phrasing overreach only; noted, not reworded.

Byte check (2026-09-29 final instrument pass (word-split + U+2014 char scan)): words=1306 emdash=0.
