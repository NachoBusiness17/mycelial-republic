# container-host.md - lens 2 (2026-10-04 reboot-patches run)

H1 TRUE, the headline. mag-sovereign runs ghost as a long-lived mag_launch child (cage pid
12, ppid 1; container StartedAt 2026-10-03 16:41 ET). The janitor loop lives in that
process. 02 fixes health.py for NEW processes the moment it lands (./mag bind mount), so
the old in-memory loop's children would start to succeed while that loop still runs the
pre-01 code: no governor, stop file ignored, deepseek tier for count>=10, the verkle --fix
quest, spawn-time knots. The old APPLY_ORDER kept "janitor off" as the guard, but the
stop file only exists for code that has 01 loaded. FIXED in APPLY_ORDER: 02 moved last,
after an operator `docker compose restart mag` and an in-cage governor status check.
H2 TRUE. state/ and memory/ are bind-mounted (docker-compose.yml:46-50), so
state\janitor.off and memory/runs/ghost/janitor_governor.json are shared host/cage. The
MAG_JANITOR_* env switches reach the cage only through the container env (documented).
H3 TRUE, measured. Staged process_reaper piped into the cage read-only (stdin, nothing
written): buckets dashboard 2, known-supervised 1, leak 6. The 6 "leaks" are the
mag_launch roster: backend.server, main.py api, mag.ghost, lane_runner, main.py autorun,
monitor_lane. Report-only by default, so harmless today; ghost will write a
leak_report.jsonl row per cycle claiming ~5 leaks (it skips itself). A ppid==1 rule is NOT
a safe fix: orphans reparent to pid 1 in the cage. Left as a law: never set
MAG_REAPER_LINUX_LIVE=1 until the classifier knows the roster.
H4 TRUE. Cage identity measured: hostname a51cb0130308, pid ns pid:[4026532674]; psutil is
absent in the cage, so 05 uses the POSIX os.kill(pid, 0) probe there (a real probe on
Linux). Host identity is "<host>|win". A container restart changes the ns inode, so a
pre-restart cage marker is foreign and waits for the 900 s mtime rule (safe direction).
H5 TRUE. 04 runs host-only (Startup\mag_boot_lane.cmd:37 calls mag\knot_at_close.py
--backfill --skip-subagents --min-messages 5 --since 2026-09-11 --skip-knot-backup);
argv-compatible with the new main(argv=None).

No em-dash bytes.
