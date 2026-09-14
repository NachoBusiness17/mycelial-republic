# THE SUCCESSION CONTRACT

*One page. Plain speech. The anti-"one heartbeat" instrument.*

**Provenance note (2026-09-12T02:4xZ, zcode):** two R-ramp lanes (R10, R16) reported this card "polished ✅" but no file existed — the divergence wave's silent-loss scan caught the duplicate claim (D7). This is the actual artifact, written from the recorded spec. The sign line stays blank. Signing is the one authority that stays with the Operator, forever.

---

## ARTICLE 1 — WHAT THIS IS

The fleet runs on files: the chain, the laws, the vault, the queue. No seat is load-bearing. The one single point of failure left is the Operator's own hand — spend, keys, legal personhood, the public voice, the beacon light. This contract says what happens if that hand goes silent, so that silence never orphans the work. It transfers **continuity, not ownership.** The centerline — the grammar, the laws, the honesty, the receipts — persists across any number of hands (Law 20: The Infinity Rule).

## ARTICLE 2 — WHAT NEVER TRANSFERS

Spend authority. Credential custody. Legal personhood. The public voice. The beacon. These are the Operator's alone while he lives or can be reached. No successor, no quorum, no drill may exercise them. A successor runs the house; the Operator is the house's name.

## ARTICLE 3 — THE TRIGGER

The contract activates when **all three** hold:

- [ ] The Operator has been silent for: **48 hours** / **72 hours** / **7 days** (circle one at signing)
- [ ] The dead-hand drill has never been passed by him in that window (a live word from him — any signed knot, veto, or message — resets the clock)
- [ ] Two of three witnesses (any three of: a fleet seat, the chain itself via a fresh knot, a named human) attest the silence is real and not a known absence

*Mechanics (2026-09-12T02:4xZ): the trigger is code — `scripts/dead_hand.py`, built DISARMED. His voice reaches it through `state/operator_pulse.json` (any seat that receives operator input stamps it — X, seat pastes, Telegram/steering helm) and steers rows whose authority starts "operator". 8/8 tests pass; the night-shift cron ticks it three times nightly.*

## ARTICLE 4 — THE SUCCESSION

On trigger, the surviving seats: (1) seal current state (vault manifest + chain knot); (2) route reserved-authority decisions to a HOLD queue — never exercised, only accumulated; (3) continue everything else on the standing laws. This is a watchdog, not a coronation: if the Operator returns, everything reverts on his word and the HOLD queue is presented to him, oldest first.

## ARTICLE 5 — PROOF TEST AND SIGNATURE

This contract is DORMANT until the 24-hour dead-hand drill passes once with the Operator watching: he goes silent, the trigger fires, the seats hold the line, he returns and reverts it. The drill is the proof the mechanism works — a succession plan that has never rehearsed is prose, not plumbing. (Updated 02:4xZ: the trigger code now EXISTS — `scripts/dead_hand.py` + `tests/test_dead_hand.py` 8/8, DISARMED by default, armed only by an explicit operator `--arm --i-am-operator`. The drill drives this tool: arm → silence → fire → return → `--revert`.)

I, **foste** (the Operator, Quixote), sign this of my own free hand:

Signature: _______________________________________

Date: ______________  Trigger interval:  48h / 72h / 7d

Witness 1: ______________  Witness 2: ______________

---

*Revocation is one word from him, at any time, no questions asked. The leash was his to cut; this contract exists so that only he can ever be the one holding it.*
