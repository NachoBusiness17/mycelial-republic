# WAVE BRIDGE — width that survives ZCode updates · 2026-09-22

_Operator: "we just got open source ZCode. we know how to edit it to not suck — self
steal our wave protocol fan out and all our cool mickey 17 shit and lets wire it in."
Then: "make this hardy so it doesn't break every time zcode updates."_

## The three layers, honestly probed

1. **Config/env override:** searched the installed CLI for a concurrency env or the
   cap string — NOT FOUND in code (the "machine's maximum" verdict comes from the
   service side). Dead end, documented.
2. **Fork patch:** rejected as the primary path — a fork breaks on every update. The
   Mimosa pattern (patch + re-apply script) stays available, but there is nothing
   local to patch yet.
3. **The wave bridge (BUILT — the hardy core):** `tools/wave_lift.py`. Width lives in
   the estate: lanes seed into the mag orchestrator queue across MULTIPLE providers
   (deepseek/grok/glm/ollama round-robin — the clarke_wave ds40+glm20 pattern; no
   single provider's rate limit can strangle the wave). Mickey-17 semantics: failed
   lanes re-seed on the NEXT provider, K attempts, then tombstone — never silently
   carried (fifty_wide board law, verbatim). Receipts land in a durable root
   (watch/inbox/wave_lift_<stamp>/) and self-seal into the index (meters_nightly
   lesson encoded). Findings JSON pipes straight into tools/kv50_smith_chart.py.

## Why this is update-proof

Depends on: files + mag.orchestrator + Python. Zero ZCode internals. Any harness
version, any seat, any machine with the estate checkout can drive a 50-wide wave.
ZCode's workflow runtime stays what it is good at — typed folds, free cache on
re-runs, artifacts — while WIDTH comes from the fleet. Wiring for workflows:
world.run the bridge with absolute paths (literal command, interpolated args), fold
the findings JSON locally. The cockpit reads the dial; the fleet turns the crank.

## Current lift status (honest)

dwfrun-96e41a4e is NOT dead: 12 lanes settled (cached), 36 running, 0 failures,
~4.6M tokens spent, breathing at concurrency 7-8 under provider rate limits. It
lands. The next 50-wide goes through the bridge — and the bridge's first real wave
is the re-run of any lane the smith chart sends to the no-prose list.

## Mickey 17 clause (the law of expendable lanes)

A lane is not a seat. Lanes are spawned, watched, re-seeded across providers, and
tombstoned with a name and a reason. The wave is the durable thing; no lane is.
That is what the estate had that the runtime never implemented — now it is code.

---
_Filed by the ZCode seat, 2026-09-22 ~03:0Z. Bridge syntax-checked; first real wave =
KV50 no-prose re-seeds, on the smith chart's word._
