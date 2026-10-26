# operator-laws.md - lens 5 (2026-10-04 reboot-patches run)

Source: .agents/skills/operator-corrections/SKILL.md (law 11 one supervisor) plus the
boot-lane law quoted in Startup\mag_boot_lane.cmd:2-5 (no timed schedules; every job
stoppable on one word) and the receipts habit.

L1 One supervisor: PASS. No patch starts a process or a loop. The janitor stays inside the
existing ghost daemon under mag_launch; the governor is a library plus a CLI.
L2 No timed tasks: PASS. No scheduler, no new scheduled task. The daily cap is a counter
keyed on the UTC date; the 1 h note throttle and the 6 h pending fallback are guards
inside an existing loop, not timers that fire work.
L3 Stop files: PASS. 01 adds state\janitor.off (and MAG_JANITOR_DISABLED). 04 keeps
state\knot_at_close.off. 02's Linux live kill is env-gated (MAG_REAPER_LINUX_LIVE=1),
not stop-file gated; acceptable because the default is refusal. Caveat (H1): the stop file
only binds code that has 01 loaded, hence the restart step.
L4 Receipts: PASS with a gap. 01 writes janitor_governor / janitor_settled rows to
autonomous_trail.jsonl; 02 logs reaper-live-refused; 04 keeps its knot_at_close.v1
receipt. 05 writes no receipt for a lock break (pre-existing; owed).
L5 Act-before-consult: the restart in step 5 is an operator call and is marked so.

No em-dash bytes.
