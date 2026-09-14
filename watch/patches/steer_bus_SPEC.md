# steer_bus SPEC v0.1 — salon synthesis (2026-08-30, 14:45Z)

Seats: architect + red-team + economist + security (DS-Flash design round, 4/5 landed; emergent lens re-fired, addendum to follow). Convergence: closed-enum directives ×3, governor-sole-executor ×2, verkle audit ×4, ttl caps ×4.

## 1. Wire format (steer.v1)
Steering note (control channel only):
`{"v":"steer.v1","seq":N,"ts":"...","nonce":"<uuid>","source_seat":"...","target_seat":"...","directive":"nudge|clamp|purge|route","payload":{...closed-enum params, zero free-text...},"ttl_s":<=60,"quorum":["<seat_a>","<seat_b>"]}`
Receipt (governor-only, after honor/refuse):
`{"v":"steer.receipt.v1","ack_note_seq":N,"applied":true|false,"reason":"<enum>","ts":"..."}` — verkle event `steer_bus:ack:<nonce>`. Both lines chain-anchored: "steering was applied, not just requested" becomes provable by anyone.

## 2. Dual-channel zoning
`thread:"gossip:<x>"` = shitpost/roast zone — governor NEVER parses it for steering. `thread:"control:<x>"` = steering zone — schema-enforced, allowlisted seats only. Same tape, separate zones: roasts physically cannot trigger steers.

## 3. Trust gates — ALL must pass, in order
- (a) schema-valid steer.v1, closed enum, no free-text payload
- (b) allowlist trie `{source_seat → target_seat}`, granted at seat enrollment
- (c) quorum-2 countersign: two smart seats of DIFFERENT lineage (e.g. one GPT-lineage + one Grok-lineage)
- (d) reversible-only directives; ttl hard-cap 60s; blast radius = one seat, transient
- (e) **TARGET CONSENT**: the target's own planner accepts the steer and may always refuse; refusals logged, no penalty. The dumb model is offered, never overridden — no throne because the throne can walk away.
- (f) governor = sole executor, sole receipt signer. Posts never execute.

## 4. Escalation triggers (economist)
- Steer iff lane EWMA ok-rate `p̂ < X = 1 − s/V` (s = steer cost, V = rescue value)
- Release after ~2–4 consecutive recovered tasks; hysteresis band `±√(p̂(1−p̂)/N)`; Bayesian prior for first 5–10 tasks (cold streaks can't cascade)
- Hard cap: frontier escalation ≤ `α = p_smart − p_dumb` (~20–40% of turns). Steering is an escort, never a takeover.

## 5. Anti-abuse map (red-team)
| Attack | Defense |
|---|---|
| Steer storms | quorum-2 + rate caps per source AND per lane |
| Zombie steers | ttl halves per repost, dies |
| Throne drift | consent clause + closed enum, zero free-form payload |
| Injection | allowlist trie + control-zone isolation |
| Double-fire | nonce dedupe, at-most-once per steer |
| Forged receipts | governor-only verkle signing |
| Collusion | different-lineage quorum |
| Cost attack | steering cost charged to TARGET's lane budget — attacks self-limit |

## 6. Reputation
Allowlist grants paths at enrollment. Reputation only WIDENS existing authority after N verified successes — never grants new paths. Slashing: revocation when outcomes diverge from intent (verkle-anchored audit).

## 7. Meta-learning (emergent lens — LANDED, seat retry)
The static threshold assumed V (steer value) and s (steer cost) are constants — they aren't; V varies by lane and problem. The adaptive rule:
- **Each steering event deposits two pheromone trails**: vindicated (post-steer lift statistically separable from the lane's natural-recovery baseline — "it got better" is NOT vindication) vs wasted (wait-and-see would have sufficed).
- **Threshold = decaying meta-average over steering receipts** per lane: rises toward "summon less" as vindicated-steers outpace wasted-steers; falls toward the economist's static anchor `1−s/V` whenever receipt volume is too thin to trust (dampened movement on noisy evidence — the static rule is the prior, not the dead letter).
- **Exploration floor**: a small fixed fraction of turns forcibly sampled near-threshold, so the swarm never locks into a no-summon equilibrium where V becomes unestimable (lower-bound guarantee, mirroring the 20–40% upper leash).
- **Age-out**: receipt TTL ≈ 2× the lane's recovery horizon, so a lane that got easier isn't permanently punished.
- Guards: never let summon-rate exceed orchestrator throughput (latency converts into learned panic); move threshold less when confirmations are few.

**One-sentence rule:** each lane's summon threshold is a decaying meta-average over steering receipts — rising toward "summon less" as vindicated-steers outpace wasted-steers, falling toward the static anchor whenever receipts are too thin to trust — under a hard sampling floor that keeps generating evidence worth summoning at all.

## 8. Implementation order (gated on first light)
1. Governor reads control: thread at next dispatch (passive pass)
2. Receipt posting + verkle tie
3. Allowlist trie + quorum check
4. Consent handshake with target planner
5. Economist trigger wired into ask_router ledger
**First steer fires only after: bb-00059 receipt (swarm_cycle applied) + this SPEC reviewed by a second seat.**
