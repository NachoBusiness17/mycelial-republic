# break.md - hostile pass (2026-10-04 reboot-patches run)

Verdicts: confirmed / weakened / killed, per lens finding, then the attacks.
correctness: C1 confirmed (fixed), C2 confirmed, C3 confirmed, C4 weakened (bounded),
C5 confirmed, C6 confirmed, C7 confirmed, C8 confirmed (fixed).
container-host: H1 confirmed (order fixed), H2 confirmed, H3 confirmed (measured),
H4 confirmed (measured), H5 confirmed.
concurrency: K1 confirmed (fixed), K2 confirmed pre-existing, K3 confirmed, K4 weakened
(single process, small window), K5 confirmed unchanged.
rollback: R1-R5 confirmed. operator-laws: L1-L3 confirmed, L4 weakened (05 no receipt),
L5 confirmed.
Count: confirmed 25, weakened 3, killed 0.

## Attacks, per patch

01 janitor limits
B1 apply time: clean on live worktree (--ignore-whitespace, loops_registry CRLF). Lands
inert until the ghost daemon restarts (H1).
B2 silent change: count>=10 quests go to qwen2.5-coder:7b; read_only children cannot write
the output file, so done-without-output counts as failure and sigs go STUCK after 3.
Intended safe state (APPLY_ORDER Risks).
B3 untested before this pass: died/stalled terminal statuses (C1). Now tested.
B4 untested, accepted: PAID_PROVIDERS is a deny-list (fail-open for a new provider name);
only "deepseek" is used by janitor quests today. Owed: flip to an allow-list of local
providers.

02 lazy CAGE_DOCTOR + reaper Linux
B5 silent change: the cage reaper goes from blind to seeing 6 false leaks (H3); ghost
writes a leak_report.jsonl row per cycle. Report-only. Do not arm live kill.
B6 untested: the Linux classifier itself (tests only cover enumeration and the live
refusal). Owed before MAG_REAPER_LINUX_LIVE is ever set.
B7 apply time: must go after the restart (H1). Fixed in APPLY_ORDER.

03 knot on success
B8 tests cover failed, done-empty, done-with-output and spawn-time; they do not cover a
pending task when the governor errors between spawn and save_state (task untracked, no
knot ever). Fail-closed direction; accepted.
B9 silent change: subscribers of CH_TASK "autonomous_task_completed" now see only real
completions (about 5 janitor dones in 14 d vs every spawn before). Intended.

04 knot_at_close filter
B10 silent change: --seed-sweep also skips dwf children now (shared _db_rows). Fine for
recovery seeds; noted.
B11 untested: a real-db timing check for the per-session JOIN on part. Overnight real-db
run (2,948 sessions) completed; accepted.

05 namespace lock
B12 break found: double-break race (K1). Fixed and tested.
B13 apply time: new markers are 3-field; old long-lived writers misjudge them (K3). Covered
by the restart step.
B14 untested: Windows PID reuse makes a dead holder look alive (psutil) and falls back to
900 s. Safe direction.

## Engine fixes applied
Cross-lens contradiction gate: H1/R2/L3 agree (the stop file binds only loaded code);
K1/C8 same finding. Unresolved contradictions: 0. Quantifier lint: "6 leaks" is one
measurement at 2026-10-04 ~08:20 ET; "died 85" is the 14-day mtime window census.

No em-dash bytes in prose (diff files quote pre-existing source lines that carry them).
