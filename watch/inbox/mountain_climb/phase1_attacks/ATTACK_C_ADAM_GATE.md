# Phase 1 attack (c) — Adam-as-B4-gate with 72h anonymous fallback (P6)

Date: 2026-10-20 · Attacker: Beam/DeepSeek (free lane) · Target: ROUTE_V0.md §P6 + §3 serialization · Lane: provider-chat, read-only.
Source of truth: ROUTE_V0.md as written 2026-09-30. No code was run; this is a doc-level adversarial read.

## Attack

1. **N=1 friend is not a valid existence proof for "usable without estate help."** A friend's feedback is confounded by relational context (they know you, your intent, your history), so it demonstrates a usable path, not estate-independent usability. Whether friendship and usability are separable here is unknown from the route doc alone.

2. **The 72h fallback likely produces a different kind of friend, not a true stranger.** Someone arriving from an external surface with prior context is a "contextual stranger," so the fallback may not test the anonymous-stranger condition it claims to. Whether any genuinely context-free stranger is reachable via that surface is unknown from the doc.

3. **Honest falsifier.** If Adam-gated B5 outcomes are statistically indistinguishable from "publish and count" outcomes (same downstream error/confusion rate, same informed-choice quality), then the gate adds no signal and should be dropped to publish-and-count. Whether that comparison is even measurable at N=1 is unknown from the route doc alone.

## Verdict

- Assumption (c) is currently Unproven: the gate's value depends on whether friendship-context confounds the feedback, which the route does not address. The fallback does not obviously solve the problem it claims to solve.

## Amendment proposed (for ROUTE_V1)

- Redefine B4's gate as "first non-estate identity to complete the acceptance test, regardless of source," and log the identity's prior-context level (friend / contextual stranger / anonymous) as a covariate. If the gate shows no signal difference across levels, collapse to publish-and-count.
