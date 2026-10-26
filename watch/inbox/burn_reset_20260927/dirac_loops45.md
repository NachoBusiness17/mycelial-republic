# Dirac loops 4+5 closed: admission <-> OpenClaw runtime-policy handshake

Lane 9 of BURN_RESET_20260927_EVENING · 2026-09-27 · seat zcode · closed in one window

## What closed

Loops 4 and 5 of the operational Dirac scan share ONE invariant because their
label sets are identical modulo direction:

- loop 4 edge: `organ:context_admission->organ:openclaw`
- loop 5 edge: `organ:openclaw->organ:context_admission`
- shared invariant: `1992f3960400da28c3d7b3db2d539f68ef852a2634447ec0c37f82e885e6ddcf`
  (labels: context admission, Dirac loop, self audit, swarm worker, effect
  broker, switchboard, OpenClaw runtime policy)

One policy-handshake artifact therefore closes BOTH. Per the gap-reader
verdict, the detour through switchboard/effect_broker is the real authority
chain, so closure BANKED the holonomy; no direct edge was added to
mag/organ_map.py and no code changed.

## The artifact

`watch/inbox/OPENCLAW_POLICY_HANDSHAKE_20260927.md`

Honest content, read from the bytes:

- Side A (mag/context_admission.py): deterministic preflight only. Bands
  green/amber/red/black, allowed = est <= threshold, durable receipts at
  memory/runs/context_admission/receipts.jsonl. It never authorizes effects.
- Side B (deploy/openclaw/openclaw.container.json + C:\Users\foste\.openclaw\openclaw.json):
  gateway token auth, tools profile minimal + alsoAllow, explicit-ownership
  agents (main full/exec, worker coding + deny list, zcode coding),
  modelPolicy.allow, contextLimits/compaction. The internal mag-file hook
  files evidence to watch/openclaw_traj.jsonl and states "Does not govern."
- Authority chain: model text proposes; switchboard_v2 grant() runs
  policy_engine.validate_authority (TTL/budget/revocation, operator gate);
  effect_broker executes only AUTHORIZED + granted_capabilities + policy-pass.
  Admission sits upstream of dispatch with no bypass into that chain.

## The two bank rows (watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl)

1. ts 2026-09-27T23:13:13.918273Z · edge organ:context_admission->organ:openclaw
   · invariant 1992f3960400da28c3d7b3db2d539f68ef852a2634447ec0c37f82e885e6ddcf
   · receipt: watch/inbox/OPENCLAW_POLICY_HANDSHAKE_20260927.md (admission
   checks window-fit preflight only; effects route switchboard->effect_broker)
   · seat zcode
2. ts 2026-09-27T23:13:14.084033Z · edge organ:openclaw->organ:context_admission
   · invariant 1992f3960400da28c3d7b3db2d539f68ef852a2634447ec0c37f82e885e6ddcf
   · receipt: watch/inbox/OPENCLAW_POLICY_HANDSHAKE_20260927.md (container
   policy governs the cage only; the mag-file hook does not govern; Mag-side
   effects stay behind switchboard->effect_broker) · seat zcode

## New scan verdict (byte-backed, ran 2026-09-27T23:13Z)

betti1 8 · n_loops 6 · closed_solved 3 · open_gaps 3

- CLOSED: organ:verkle_knot->organ:manifest (banked earlier tonight)
- CLOSED: organ:context_admission->organ:openclaw (this lane)
- CLOSED: organ:openclaw->organ:context_admission (this lane)
- open: organ:context_pack->organ:swarm_surface
- open: organ:context_checkpoint->organ:context_pack
- open: organ:water_computer->organ:manifest (lane 8's claim, not banked at
  this scan)

Requirement CLOSED >= 3 met.
