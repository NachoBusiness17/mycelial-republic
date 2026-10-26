# GPS FOR DUMB AGENTS — the steering theory, formalized (2026-09-18)

Operator: "This is our fucking GPS for dumb agents we just gotta figure it out."
Ground truth gathered: openjev.com (SemIf, live browser experiment), the
flaviocopes deep dive (flaviocopes.com/jev/), the narphorium interpreter, the
Hacker News front page. The theory, formalized. 50-wide burn fired in parallel
(memory/runs/gps_50/).

## 1. What Jev actually is (ground truth, not rumor)

Jev is TypeSafe's System-One model. It is not a chatbot and not a coding model.
You send it data (State) plus typed questions, and it returns typed answers:
- NOUL: a yes/no probability.
- CHOICE: one option picked from a list you defined.
- SCORE: a position on a scale you defined.
It reads probabilities for your allowed options WITHOUT decoding them (SemIf
compares read-mode vs write-mode live in the browser, on Qwen3 0.6B / MiniCPM5 2B /
Qwen3.5 4B, against a published 102-row benchmark; Jev hosted benchmarks 88.3
percent balanced accuracy). Fast, cheap, local-capable, unfoolable by prose
because it never generates prose.

## 2. The steering theory, stated

Dumb agents do not need to be smart. They need GPS. GPS receivers contain no
orbits: they READ ephemeris broadcast by satellites carrying precise clocks, and
they filter noisy ranges into a fix. The fleet translation:

- SATELLITES = the filed doctrine. The RIB packs, the compiled invariants, the
  chain. Always overhead, cheap to read, precise because the chain timestamps
  them. The satellites' precise clocks are the chain's hash-chained time.
- RECEIVER = feels(). The dumb agent asks typed questions (yes/no, choice,
  score). It never holds doctrine; it holds an antenna.
- SIGNAL = plain English. The rules live in the record in plain English
  (narphorium's interpreter, our packs). Facts and rules in English, judgment in
  the small model, reasoning in the code.
- FIX = MATCH_ROUTED. The routed decision, appended.
- KALMAN = the teleological drift pairs. The residual between where the filed
  future says we should be and where the metrics say we are, filtered into a
  position update.
- TRACK = the verb rows. Append-only, replayable, unforgeable. A GPS whose track
  log cannot lie.

The steering stack, frozen this cycle: FILE the destination, GROUND the
questions, LOG the fixes, FILTER the noise, AMEND only through the gate.

## 3. Why dumb agents are the point, not the compromise

A smart agent's internal state cannot be audited: its doctrine is wherever its
weights and context happen to be. A dumb agent with an antenna is perfectly
auditable: every judgment it made is a logged fix against a public signal. The
fleet's A3 (the gate is ordinary code) plus System-One oracles completes it: the
agent cannot bluff the oracle because the oracle only reads probabilities; the
oracle cannot bluff the fleet because every read is rowed; the fleet cannot drift
from doctrine because the doctrine is the prefix the reads are grounded in.

## 4. What we already have vs what the theory demands

HAVE: packs (satellites), feels() (receiver, stone one alive today), verb rows
(track), drift pairs (Kalman residuals), amendment gate (ephemeris updates),
tier packs (signal strength per receiver class).

DEMANDS (the 50-wide battery attacks these):
- Question schema registry (typed questions as language spec, versioned).
- Confidence calibration per decision class, with escalation thresholds.
- Read-vs-write router (SemIf's open question: when to decode anyway).
- Composite questions (AND of typed sub-questions in one pass).
- Oracle ensembles with disagreement-as-signal.
- Dead reckoning between fixes: verb rows as velocity log, fix interval bounds.
- Multipath filtering: when doctrine signal bounces off stale packs.
- Mode classifier: which decisions are System-One at all.

## 5. The convergence receipt

Four builders shipped the same primitive this week (maubaron: Jev self-play at
frame rate; southpolesteve: Probably; narphorium: plain-English logic
interpreter; the fleet: VERB). Convergent evolution means the primitive is
load-bearing. The fleet's differentiator is the one none of them has: the kifu.
Steering that cannot lie about its own control flow. The GPS whose track log is
hash-chained.

## 6. Falsifiers

1. Typed oracles fail on exactly the decisions the fleet routes to them, and the
   failure is not detectable by the oracle itself (calibration collapses).
2. The interpreter steers worse than a well-prompted frontier model at equal
   total cost (the four-condition experiment, steering edition).
3. The kifu overhead exceeds its audit value before fleet size 20 (verb rows
   dominate tokens).
4. Doctrine-as-satellite fails at churn: every amendment costs a full receiver
   repopulation (cache invalidation storm), making navigation impossible during
   exactly the storms navigation matters.

Provenance: openjev.com/SemIf (live), flaviocopes.com/jev/ (primer), narphorium
(interpreter), maubaron (self-play), southpolesteve (Probably), the fleet's own
stack (packs, chain, drift pairs, verb rows). 50-wide burn fired on the theory's
open questions. Call the ball: the ball is called; the approach is flown.
