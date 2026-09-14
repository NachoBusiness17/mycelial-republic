# THE ENGINE BAY — concurrent steered engines via z.ai API (v0 design, 2026-09-02)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: a multi-engine concurrent bay (A1/B1/C1/D1) can be assembled tonight from existing parts only (resident sessions, entropy routing, queue-per-drainer) with no new engine code — UNPROVEN (design v0, no concurrency receipt in card) · falsifier: two different-model engines failing to fold concurrently without lane collision, or prefix-cache thrash under session sharing
*Operator: "GLM-4-32B-0414-128K has 15 concurrent — could we launch 15 of those and 20 of
the GLM 4 Plus? Start with one each. Launch from API, multiple engines concurrently using
our steering mechanisms for each. Find out how other people do it — we aren't the first. Steal."*

## THE STEAL (how others do it — gathered tonight)
- **KVFlow** (arXiv): tracks per-agent cache-hit history; consistently-hit prefixes treated as
  FIXED fixtures for a swarm. -> our resident sessions ARE the fixtures; steer tails preserve hits.
- **llm-d / Ray Serve prefix-aware routing**: route each request to the engine that ALREADY
  holds its prefix. -> engines own domains; the dispatcher routes by domain, not round-robin.
- **TrueFoundry**: standard load balancers break prefix locality. -> never randomize engine
  selection for the same stream. (The seat-w-<uuid> mistake, generalized.)
- **fuel_feed** (our shelf, 08-24): ENTROPY ROUTING — hard signals -> strong lanes, easy ->
  fast lanes, rotated for fairness; free-first. The dispatcher's routing law already exists.
- **blade_drain** (our shelf): partitions a backlog N-way across workers — the queue-split
  pattern for the bay.
- **swarm_worker law**: dedicated queue per drainer, single-drainer per queue, no double-exec.

## THE ENGINE MATRIX (start one each, scale to published concurrency)
| Engine | Model | Concurrency cap (console) | Key lane | Role |
|---|---|---|---|---|
| A1 (LIVE) | glm-4.7-flash | free tier ~1-5 (serial tonight) | KEY (paas v4) | fast miner |
| B1 (TONIGHT) | GLM-4-32B-0414-128K | **15** | KEY (API credits) | mid-brain, 128K ctx |
| C1 | GLM-4-Plus | **20** | KEY (API credits) | strong lane |
| D1 (LIVE) | glm-5.3-flash low-effort | plan/API | KEY | conductor/spec only |
| bench | groq / portal :free / glm-4.5-air | caps | their keys | overflow |

Scale law: one engine of each class tonight -> measure -> then multiply each to its
published concurrency with SEPARATE resident sessions per replica (session-per-replica
preserves prefix cache; a load balancer over shared sessions would thrash it).

## THE MECHANISM (all existing parts, no new engine)
1. Each ENGINE = one resident session (contract-once, steer-tails) + its own queue file
   + one key lane. Single-drainer per queue (swarm_worker law).
2. The DISPATCHER assigns tasks: entropy-routed (fuel_feed law) — hard mining -> B/C,
   bulk summaries -> A, specs/judgment -> D.
3. Steering per engine = the steer grammar (NEXT WING tails; STEER packets via steer_bus
   for behavior changes). Each engine's session is watchable verbosely in the cage.
4. Receipts: output files + board rows + event.v1. Substance gate (>150 bytes) at pickup.

## START-TONIGHT
- B1 engine: GLM-4-32B-0414-128K on KEY, own queue (docs/rfcs + design shelf mining),
  resident session engine-b1. Proof = two different-model engines folding concurrently
  (A1 on 4.7-flash + B1 on 32B) without lane collision.
- C1/D-scale: morning, after B1's receipt and a queue-quality check.
