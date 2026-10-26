# STEALTH DRIVER 24/7 — landed 2026-09-28 00:10 (operator: "driving our stealth lanes 24/7 usefully")

Built on the boot-trigger law (Startup logon, never clocks; stoppable on
the operator's single word) and no-bulk-self-processing (every topic feeds
a real organ).

## What landed

- tools/stealth_driver.py: 7-topic rotation, 15-min cadence, staggered,
  fail-open, heartbeat per cycle to state/fuel/stealth_driver.jsonl:
  probe20 drift cycle (llama warm :8080) - rumor drill watch - fossil check -
  chain verify-dry - roster churn (allowlisted hosts, diff vs last) -
  FKB pressure top-sigs - backlog census (B2 board + queue index).
- SSRF boundary enforced in code (Mimosa-guarded twice): exact URL
  allowlist, scheme check, resolved-IP public policy for remote hosts,
  redirects disabled. Loopback allowed only for the fixed health probe.
- scripts/run_stealth_driver.py: headless launcher; routes prints to
  logs/stealth_driver_stdout.log (pythonw None-stdout trap found live:
  the first two launches died silently on print(flush=True) - venv shim +
  real-interpreter PIDs read as "duplicates" and my dedupe kill made it
  worse; the working lesson is in the transcript).
- Boot lane line 0 added (mag_boot_lane.cmd): detached start BEFORE the
  blocking Arm C line, so 24/7 never waits on the queue.
- STOP = create state/stealth_driver.off. One file, one word, gone.

## First live cycles (heartbeat bytes)

probe20 appends real drift rows every pass; rumor 4.4h ALL HELD; fossil
0 WARN; chain consistent (8,076 leaves); roster llm7=64 openrouter=458
groq=403 (free-key /models rejection, matches the redo-sweep finding -
degrades gracefully); FKB pressure: amd_window_guard x18, run_shell x11;
backlog: queue open 37, B2 board drained.

## Known quirks (honest)

- groq roster 403 with the current free key: churn detection for groq is
  degraded to the 403 signal itself until a cached-token auth pass.
- fkb topic reads memory/failure_kb/signatures.json (the real shape:
  {schema, signatures:{sig:{count,...}}}) - first version guessed a jsonl
  path and an empty result; fixed same hour.
- Fleet-doctor integration (liveness of this driver in the 08:30 pass) is
  the next small wire - the heartbeat ledger is the evidence it would read.
