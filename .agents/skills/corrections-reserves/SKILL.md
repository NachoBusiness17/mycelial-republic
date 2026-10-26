---
name: corrections-reserves
description: VET any finite-pool spend, refill, or rescue recommendation against the pool's natural refill time before proposing it (law 15). Use before recommending spend of credits, quota resets, or any strategic reserve.
when_to_use: Before any recommendation that spends or rescues a finite pool.
argument-hint: <pool-name> [spend-proposal]
---

# VET - reserves spend at measured starvation, never at impatience (law 15)

The Lite reset veto (2026-09-05): the weekly pool died and the seat
recommended spending the last quota reset that same night - when the usage
window (Aug 29 -> Sep 4) showed the pool refills naturally within hours.
Operator: "That would be wasting compute 50% of our weekly plan because
you're impatient." If `$0` (the pool) is missing, ask which pool the spend
touches before vetting.

A finite-pool rescue lever is strategic reserve: it pays out only when spent
on a real mid-week starvation with a full queue behind it; spent early it
converts reserve into nothing.

GATE (LAW-056 teeth, hard): before recommending ANY spend/refill/rescue of a
finite pool, NAME when the pool refills naturally, read from data - if
refill is under ~24h away, the recommendation is WAIT, and the fix is the
pacing guard on the lane, not the rescue lever. A spend rec without a named
refill time is a repeated failure.

Related, not overridden: law 53 SPEND THE MONEY governs funded budget
(hoarding funded budget is the drain bug in money form); law 54 COMPUTE
LADDER governs which account. This card governs FINITE pools only.

## Command

```bash
# read the pool's usage ledger before recommending anything
tail -5 memory/runs/hermes_burn/usage.jsonl
# name the refill time from provider docs/console data, then WAIT or SPEND
```

Final response: pool name, natural refill time (source cited), the queue
depth behind the ask, and the verdict - WAIT (pacing guard named) or SPEND
(starvation evidenced) - one or the other, never "maybe".
