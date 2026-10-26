---
name: no-bulk-self-processing-law
description: CORRECTED 9/26 - operator WANTS local inference running; the
  control is his stop-or-limit word, never timed schedules; boot is the trigger.
  Original "external consumer" framing was wrong
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_71c96bdc-4107-40e1-96f8-7211934ac587
---

Operator, 2026-09-26. Two-step correction, second beats first:

1. Morning: "what the actual fuck you processed it all" + "stop being dumb self steal" - I first wrote this as "local bulk inference needs an EXTERNAL consumer."
2. Evening correction, verbatim: "external consumer is the wrong move we want local inference i just want you to stop or limit it when i tell you putting shit on schedules that are timed never works. plan it but also plan it all to happen when i boot."

**The actual law:**
- Local inference is the WANT. Keep the box loaded with it. The dumb-self-steal correction was about uncontrolled bulk churn, not about local inference being suspect.
- The control surface is the operator's word: when he says stop or limit, it stops or limits, immediately, whatever it is.
- Timed schedules NEVER work for this. No clock-triggered tasks. The trigger is BOOT: work queues fire when he boots/logon, via the Startup folder (mag_boot_lane.cmd), never /sc once /st HH:MM.

**How to apply:** Load local inference freely; wire every long-running job into the boot-lane queue (startup folder script) so it restarts with the machine and dies on his word. When he says stop, kill the process, not the plan; it relights at next boot. Never answer "when will it run" with a clock time. Related: [[law-11-credits-over-failure]], [[box-burn-90-percent-law]] (night-window guard still applies to heavy local), [[sovereignty-offense-dependence-20260920]].
