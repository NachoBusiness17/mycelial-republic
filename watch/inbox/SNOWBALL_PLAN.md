# THE SNOWBALL PLAN — the tandem flywheel (2026-10-01, operator order)

Operator: "driving our free lanes in tandem to dogfood our systems... working
together intelligently and emergently... this many agents and our systems have
to have some sort of snowball effect."

## The law of the flywheel

Every organ CONSUMES at least one estate instrument and PRODUCES at least one
instrument input, every cycle. No organ runs on its own loop. The cycle is
daily (the mates' 08:00 cadence is the heartbeat).

## The loop (what feeds what)

```
STEALTH FLEET (24/7, free) ──mines──> STEALTH_MINED_FINDINGS
        │                                  │
        │                            [B13 triage law: auto, not manual]
        │                                  v
        │                            CYCLE BRIEF (the morning composer)
        │                                  ^
        │     MATES (08:00, coding plan) ──┤ receipts + findings
        │         │                        │
        │         │ (missions seeded from  │
        │         │  yesterday's brief)    │
        │         v                        v
        │     IMPROVE CYCLE <──── meters: gps ledger, duel table,
        │         │              anomaly flagger, quota ledger, census
        │         v                        │
        │     SKILL BEADS (verdict-gated)  │
        │         │                        v
        └─────────┴────────────> THE INSTRUMENTS get exercised ->
                                  their defects surface ->
                                  their fixes become mate missions ->
                                  SNOWBALL
```

## The couplings (what gets wired, in order)

C1. CYCLE BRIEF (tools/cycle_brief.py, built tonight): composes the morning
    brief from overnight outputs - stealth findings tail, gate digest, meter
    states, yesterday's mate receipts, quota ledger shape. This brief seeds
    (a) the mates' hunting grounds, (b) the improve scout's focus,
    (c) the orchestrator's first read. THE HANDOFF REGISTER: one file, every
    cycle, what-produced-what-consumes.

C2. MATES DRAW FROM THE ASK-BANK: mate missions that need judgment asks draw
    from tools/ask_bank.py (the hidden split) and LOG to the gps ledger -
    the mates become the meter's organic traffic (Aj1's dream: the meter
    fed by the fleet's own work).

C3. STEALTH TRIAGE GOES AUTO: B13's manual triage becomes a cycle_brief stage
    (top-5 actionable findings per day, loud rib-contradictions flagged to
    attention.md). The stealth fleet stops being write-only.

C4. IMPROVE PROMOTES VERDICT-GATED ONLY (AJ8's fix made law): beads carry
    run verdicts; the cycle brief lists promote-ready candidates WITH their
    verdict tables - the operator gate stays, the pipeline feeds it.

C5. THE DROP LEDGER CLOSES THE LOOP: every cycle-brief item carries its
    source row; every landed work updates its row. The register IS the
    flywheel's memory of itself.

C6. QUOTA SHAPE RIDES THE BRIEF: the quota ledger's HOLD/GO verdict heads
    every brief - the fleet sees its own fuel state and self-throttles
    (the measured law: 8-12 staggered green, 16+ trailing red).

## What runs it (the wall-free estate, now)

- The account's agent spawns: dead til 10-05. Irrelevant to C1-C6 - all
  couplings are local python on scheduled tasks + the mates' own quota.
- Mates 08:00 daily (coding plan) - they become the flywheel's hands.
- Stealth 24/7 (free) - the fleet's sensing surface.
- My hands + local compute - the architect's bench.
- On 10-05 (or the aimed 24h fullsend): the PAID lanes join the same loop
  as a fifth organ - same brief, same register, same dogfood law.

## The snowball metric (how we know it's working)

N=1 today. The flywheel works when: a defect found by instrument A on day N
is fixed by organ B on day N+1 and verified by instrument C on day N+2 -
UNPROMPTED, no orchestrator touch. First target: the stealth fleet's
ling:free cached_tokens=0 contradiction (B13's flag) gets resolved by a
mate mission, verified by the next triage. That's one full turn of the
wheel. Then it compounds.
