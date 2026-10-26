# Phase 1 attack (b) — build-rail-before-wire ordering (P3 before P4)

Date: 2026-10-20 · Attacker: Beam/DeepSeek (free lane) · Target: ROUTE_V0.md §P3 + §3 serialization · Lane: provider-chat, read-only.
Source of truth: ROUTE_V0.md as written 2026-09-30. No code was run; this is a doc-level adversarial read.

## Attack

1. **A build without the online leg is a real deliverable only if the stranger's first need is "does it run at all" (install/launch/export sanity); otherwise it is a dead toy.** Whether the stranger values runnability over connectivity is unknown from the route doc alone.

2. **The stranger most likely needs a runnable artifact first** (a working online session is meaningless if the client will not launch), but if the route's stranger is defined as a remote peer expecting to connect, the priority flips. The doc does not pin the stranger's definition, so unknown.

3. **Honest falsifier.** If a stranger given only the P3 build cannot reach any meaningful next step without the wire (i.e., the artifact yields no observable value until P4 lands), then P4-before-P3 is correct; conversely if the P3 build alone satisfies the stranger's stated acceptance test, ordering stands.

## Verdict

- Assumption (b) is currently Unproven: the route's "rail is the deliverable" claim is plausible but depends on an unpinned stranger definition. The ordering is defensible only if the stranger's acceptance test is runnability-first.

## Amendment proposed (for ROUTE_V1)

- Pin the stranger's acceptance test in P3's falsifier: "stranger can launch, reach the water board, play one move, exit" is the P3 gate. If that test passes, P3-first stands; if the stranger reports "I expected to connect to someone," P4 moves ahead.
