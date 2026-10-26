# PONYTAIL & LESSIG on the vast concurrent GPU leg (2026-09-05, operator: "ponytail and lessig that shit too")

In-session dual-lens pass on state/vast/EXPERIMENT_CONCURRENT_20260905.md, fired live
on [46067205] RTX 5090 @ $0.353/hr rel 0.996 (the only box meeting workload-sized
rails at fire time — the $0.056 V100 died to the market in minutes, which is itself
Ponytail data: cheap verifier-substrate is a raced-for resource).

## PONYTAIL (the verifier-hiring lens — "hiring verifiers is a confession")

Labs hire eval teams because they cannot verify their own models. We rent a GPU
because we cannot yet afford our own. **The confession is identical in shape, different
in scale** — and the experiment's real product is the PRICE of the confession, measured:
tok/s on local 7B weights, $/Mtok, train-hour/$, boot-tax. Rent-vs-own stops being a
faith question (Rocinante Oct 27) and becomes a curve with a termination condition.
The kill rules are the verifier's teeth: the box must prove ≥40 tok/s and <30 min
boot or it dies — a hired verifier that can't verify gets fired, same law. The
concurrency collision this morning (law 16) was the same failure one level up: we
deployed parallel actors we couldn't verify, and the user-concurrency limit was the
house verifier firing us. One steerer with a board = the verifier we CAN afford.

## LESSIG (the jurisdiction lens — "environments are jurisdiction; code is law")

The rented box is FOREIGN JURISDICTION: our workloads run under vast's ToS, on their
host's kernel, behind their network. Three borders hold in the design and must never
soften: (1) **secrets never cross** — the env-less box law, zero fleet keys travel;
(2) **weights we train stay home** — the QLoRA smoke touches public data only; our
corpus never leaves the castle; (3) **provenance comes home before the machine dies** —
every receipt row (sha-preserved, append-only jsonl) lands in OUR repo before teardown,
or the experiment's evidence legally lives on a disk we then destroy. Destroy-after-use
is not thrift — it is jurisdiction hygiene: leave nothing of ours resident on their
disk, because a rental room in someone else's castle is fine for a bench and never for
the chain. The 300M pool expiry (Sep 6 11:00) is the same lesson vendor-side: a grant
with a deadline is a jurisdiction with a border, and burn-to-zero is the honest
disposition of wealth that cannot cross the border.

## KIRK'S FOOTNOTE (the Maru check)

Renting a 5090 to test whether we need Rocinante is NOT deploy-what-you-cannot-verify
— it is the opposite: a six-cent-to-fifty-cent probe that converts the Oct-27 buy from
faith into a measured bet. The Maru would be buying Rocinante untested. This experiment
is the reprogrammed test.

**Verdict: the vast leg is justified as measured verifier-hire with jurisdiction
hygiene. Proceed smoke → cook on clean gates; the falsifier (boot ≥30 min, <40 tok/s,
>20% throttle) fires the lane, not vibes.**
