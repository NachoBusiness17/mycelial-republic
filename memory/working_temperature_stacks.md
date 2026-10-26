# Temperature stacks + pointer knots + organic gap track (2026-08-06)

## Config (adjust timings/heat here)
configs/temperature_stacks.yaml — loops + cold/warm/hot/scarce/improve/pointer

## Code
mag/temperature_stack.py — OO TemperatureStack, TimingProfile, PointerKnot, gap track
Wired: orchestrator.timeout_for_goal, mag_launch intervals, lifecycle auto_reconcile → track_lifecycle_into_improve
Training patterns: lifecycle_gap, pointer_knot, temperature_route

## REST
GET/POST /api/v1/temperature-stacks
  resolve: {action, goal}
  pointer: {action: pointer, ref, kind}
  track_gap / track_lifecycle

## Organic loop
Missing/waste pieces → memory/training/loop_gaps.jsonl + improve candidates + optional pointer knot
