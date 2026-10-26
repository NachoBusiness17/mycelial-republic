# SWEEP - swarm-orchestration via x - 2026-10-04

source-fetched: 2026-10-04
Seat: sweep-swarm-orchestration-x (dwf sess_dwf-dwfrun-ab8d406e, actor 3_16)
Area: swarm/multi-agent orchestration, flock-shaped generation, playerbot-to-lane transfer, retry-as-orchestration, width-vs-throughput curves.

## Door status (read this first)

The X door DEGRADED this run: 8+ `site:x.com` / `site:twitter.com` searches (WebSearch backend)
returned either zero X results or bare-domain `https://x.com` URLs with **no status IDs**, so the
fxtwitter resolution step (`https://api.fxtwitter.com/<user>/status/<id>`) had **nothing to
resolve and was never attempted against a real ID**. No X post was deep-read. Per the recipe
fallback, search-result snippets are banked as degraded-URL items with lowered confidence and
the degradation named; the deep reads came from the literature the same sweep surfaced (arXiv,
OpenReview API, Google Research blog, GitHub). One search call also surfaced the backend's own
1302 rate-limit error mid-sweep. Never treated as a fallback success.

## Pass 1 (broad sweep, 30+ candidates)

36+ candidates collected from the sweep queries: x.com snippets (capability-token safety post
2026-09-14; "Agent-First full stack" 2026-06-10; "14-step roadmap prompter to loop designer"
2026-06-09 - both June items OUTSIDE the 30-day window), plus literature: Revisiting Boids
(OpenReview), Towards a science of scaling agent systems (Google, 2026-01-28, arXiv 2512.08296),
W&D parallel tool calling (arXiv 2602.07359), WideSeek-R1 (arXiv 2602.04634), WideSeek
(arXiv 2602.02636), PspMAS prospect-state propagation (arXiv 2609.08033, 2026-09-07, in window),
TokenDance KV-cache sharing (arXiv, 2026-04, outside window), RL-for-MAS orchestration traces
(arXiv 2605.02801), Alan Turing Institute Agent-Scaling-Orchestration repo, LangChain forum
failure-diagnosis thread (2026-03-27), Towards AI retries (2026-04-06, URL unrecoverable),
Galileo multi-agent failure census (2025-12-21), AWS/Credal/TrueFoundry orchestration guides,
Diagrid concurrency backpressure, Mastra parallel CLI agents, learnaivisually production
harness retry/jitter article (URL not found on landing page; not banked), durable-agent
step-level retry issue (GitHub, 2026-08-26, in window), codebridge/dev.to/theagiclock swarm
think-pieces, Kimi 300-agent swarm coverage (2026-06-02, outside window).

## Pass 2 (deep reads, 6 end-to-end)

Fetched and read: W&D arXiv abs page; WideSeek-R1 arXiv abs page; Google Research blog post in
full; Boids paper abstract via the OpenReview API (`api2.openreview.net/notes/search` - the
forum page itself sits behind a browser-verification interstitial and could NOT be read; noted);
PspMAS abstract via the arXiv export API; durable-agent issue #2 on GitHub.

## RQ1 - flock-shaped generation: does any published result match?

**No. Nothing published decodes a leaderless flock consensus into verifiable task answers.** The
estate's flock shape (memory/rib/RIB_EMERGENT_FLOCK_ON_K8S_20260810.md:17) is leaderless
particles in an invariant field phi steered by boid terms, and its own eval already proved the
catch: flock consensus is valid only for open-ended sampling, never as a verifiable answer
generator (watch/inbox/frontier_olm_2026-10-04/lens/laws.md:43), with the decode redesign named
ribs-open at laws.md:73 ("the decode must map to the actual task output space (numbers/text),
not surrogate territory actions").

Closest published, ranked:

1. **Revisiting Boids for Emergent Intelligence via Multi-Agent Collaborative Tool-Building**
   (Xisen Wang, Qi Zhang, SEA @ NeurIPS 2025 poster, OpenReview forum 46LJ81Yqm2). Agents follow
   an observe-reflect-build loop guided "only by three Boids-inspired primitives: separation,
   alignment, and cohesion," and collectively "invent, adopt, and refine tools." The
   coordination layer matches our flock_field almost term for term - our rib already encodes
   separation/alignment/cohesion - but their emergent product is a shared tool library, not a
   decoded answer. Steal: the tool-building loop as the flock's convergence PRODUCT (what the
   flock folds into knots could be tools, not just verdicts).
2. **W&D (arXiv 2602.07359, 2026-02-07)**: width via parallel tool calls INSIDE one reasoning
   step - the decode is real (task answers), but the swarm is intra-agent. Steal: their result
   (62.2% BrowseComp GPT-5-Medium > 54.9% GPT-5-High, fewer turns) says parallel sampling with a
   verifier-shaped decode beats a bigger model - the nearest published cousin to "flock answers
   that are verifiable."
3. **Google scaling science (2026-01-28, 180 configs)**: independent (leaderless) architectures
   "amplified errors by 17.2x" vs 4.4x centralized - quantitative backing for laws.md:43's
   consensus-illusion finding, and a warning: the flock needs a verification seat, not more
   voices.
4. **WideSeek-R1 (arXiv 2602.04634)**: width scaling works but via a TRAINED lead agent (MARL)
   over parallel subagents - a hierarchy, not a flock; "consistent performance gains as the
   number of parallel subagents increases" (4B matching DeepSeek-R1-671B at 40.0% item F1).
5. **PspMAS (arXiv 2609.08033, 2026-09-07, in window)**: finds "agent heterogeneity gradually
   decreases during simulation" and splits state into a compact Prospect State + Semantic State
   to keep cheap agents useful at scale - directly relevant to flock pods drifting into
   sameness; steal the heterogeneity-preservation propagator for long flock runs.

## RQ2 - playerbot coordination mechanisms vs lane runners (local, byte-checked)

Corpus confirmed in catalog: 5,033 rows matching "playerbot", 10,360 matching "azerothcore"
(`grep -ci` over catalog/catalog.jsonl; ask cited 25,413-row corpus, azerothcore 10,356,
mod-playerbots 5,019 - catalog rows include near-duplicates by path prefix; the corpus.md file
itself was not found in this run, `find -maxdepth 3 -name corpus.md` returned nothing, so the
25,413 figure stays ask-sourced, not byte-verified here).

Mechanism inventory (corpus side, `corpus/library/mod-playerbots/src/modules/Bots/playerbot/`):

- **Formation keeping** - `strategy/values/Formations.h:23-46`: FollowFormation / MoveFormation
  with `MoveLine`/`MoveSingleLine` computing per-slot offsets from a center + orientation +
  follow angle. Transfer shape: slot geometry anchored to a lead. NOT in the lane runners.
- **Leader (election-shaped)** - `PlayerbotMgr.cpp:262-263`: `if (master->GetGroup() &&
  !master->GetGroup()->IsLeader(masterGuid)) master->GetGroup()->ChangeLeader(masterGuid);` -
  leader-by-ownership assertion, not an election protocol. Lane analog EXISTS:
  create-by-rename CAS, "when two engines race on one item, exactly one rename" wins
  (`mag/bay_organs.py:9-16`), used by `mag/lane_runner.py:130-146` (atomic tmp+replace,
  Errno-22 cure, "the lock is external and transient, not code-side"). Same primitive family
  (single-winner claim), already reimplemented - knowingly, via CAS, not election.
- **Role assignment** - `strategy/values/PvpValues.h:19-22`: `BgRoleValue : ManualSetValue<uint32>`
  ("bg role") - a stored per-bot role slot. Lane analog EXISTS: static lane identities
  (builder/day_work/research/night) plus the gate's judge seats and cascade
  (`mag/lane_runner.py:272-278`, `configs/lanes.yaml` gate_verdict_v2). Reimplemented as
  static roles; the playerbot version is dynamic per-context (BG role set at join).
- **Threat tables** - `strategy/values/AttackersValue.h:8-11`:
  `AttackersValue : ObjectGuidListCalculatedValue` (recalculated attacker list) plus
  `AttackerCountValues.cpp` - priority-by-danger read each tick. NOT in the lane runners:
  lane INBOXes are FIFO drops (`mag/lane_runner.py:984,1079`), no danger-scored target
  ranking. Steal candidate: threat-style scoring for INBOX prioritization (danger = cost /
  blast radius / deadline), the one mechanism with no lane analog yet.

Verdict: 2 of 4 mechanisms (single-winner claim, role slots) are already in the lane runners in
weaker static forms; formation geometry and threat-table prioritization are genuinely
unreimplemented transfers.

## RQ3 - retry-as-orchestration vs retry-as-transport

The sharpest published articulation found is **jatinsethi98/durable-agent issue #2
(2026-08-26, in window)**: the engine owns nothing - "They own retries, rate limiting and
authentication - the engine does none of that"; a transient tool failure "fails the whole run
back to the host queue" because "the host can only retry the run, not the step. Every consumer
rebuilds the same machinery"; and safety requires "Retryable-vs-terminal classification must be
explicit and conservative" plus "A retry must reuse the same effect_id."

That is exactly the estate's proven split, restated from the other side: workflow children ride
maxAttempts 0 (zero adapter retries, die on the first 429/1302 - the fan-out width law),
Task agents ride the main-session retry path (maxAttempts 11 + driver backoff). The published
consensus adds one mechanism the estate should bank formally: retry-as-orchestration is safe
only with an idempotency key carried across attempts - durable-agent's effect_id is the same
animal as the estate's corr_id joins (estate_query corr_id joins landed 2026-09-30). No
framework published "children die on first 429, parent owns the retry" as a named doctrine; the
estate's dispatch-shape law remains the sharper statement of it.

## RQ4 - published width curves vs the 109.4M tok/h @ width 10 envelope

**No published tok/h-versus-width curve exists in anything this sweep read.** Published curves
are quality-vs-width: WideSeek-R1 ("consistent performance gains as the number of parallel
subagents increases"), W&D (width improves accuracy while REDUCING turns; 62.2% vs 54.9%
BrowseComp), Google 180 configs (+80.9% centralized over single agent on parallelizable work;
every multi-agent variant degraded sequential tasks 39-70%; error amplification 17.2x
independent vs 4.4x centralized; coordination tax rises disproportionately past ~16 tools;
predictive model R2=0.513 picks the optimal architecture for 87% of unseen configs). Under a
shared rate-limit budget, added width buys sublinear quality while error amplification and the
tool-coordination tax grow - so the untested 15-16 rung should be estimated as: hold tok/h
fixed at the measured envelope, expect diminishing quality return per rung, and treat first
429/1302 contact as the HOLD signal per the max-concurrency standing law. The thundering-herd
mechanism (synchronized retry waves without jitter - the learnaivisually harness article's
"200 clients all retry at T" framing) is the specific failure shape a naive 15-16 rung invites
on workflow children, which carry no adapter retries at all. The rung must be measured by the
estate itself; the literature supplies priors, not the curve.

## Banked items (7, strongest first - mirrors SweepResult)

1. Revisiting Boids (OpenReview 46LJ81Yqm2) - RQ1, flock primitives match, tool-building steal.
2. Towards a science of scaling agent systems (Google, 2026-01-28) - RQ4/RQ1, the numbers.
3. W&D parallel tool calling (arXiv 2602.07359) - RQ4/RQ1, width-beats-depth decode.
4. WideSeek-R1 (arXiv 2602.04634) - RQ4, subagent width gain curve.
5. PspMAS (arXiv 2609.08033, 2026-09-07) - RQ1/RQ4, heterogeneity decay + state split.
6. durable-agent issue #2 (GitHub, 2026-08-26) - RQ3, run-vs-step retry ownership + effect_id.
7. X capability-token post (2026-09-14, UNRESOLVED - bare x.com URL, snippet-only, confidence
   0.35; the fxtwitter door had no status ID to resolve).

## Not banked (checked, rejected)

- learnaivisually production-harness article: subject page does not contain the article; quote
  unverifiable. OpenReview forum page: verification interstitial. Towards AI retries article,
  Diagrid, Mastra, Galileo, AWS, TrueFoundry, codebridge, dev.to 34-agent swarm, Kimi coverage:
  URLs bare-domain or outside window; not read end to end. TokenDance (2026-04) and WideSeek
  (2026-02): outside the 30-day window and weaker than the banked four for the four RQs.
