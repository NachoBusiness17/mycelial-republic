# improve-loop audit (s2-02): state of the Mag improve loop

Item: s2-02 · 2026-09-28 · census gopher run. Scope: read every file under `memory/improve/` (SEATS.md, HABIT.md, candidates.jsonl, daily/ named by the ask), map the pipeline, classify working / broken / never-fired.

Method note (instrument honesty): the tree holds 833 files / 22,577,934 bytes (walk `memory/improve`, includes the vendored `sources/ponytail-2026-08-03` clone at 185 files). Read in FULL: SEATS.md, HABIT.md, GOAL.md, MIRROR.md, state.json, latest.md, field_brief.md, playbook.md (258 lines), today's four daily-family leaves, improve_daily.ps1, improve_loop.py (328 lines), plus targeted sections of mag/improve.py (2,773 lines), configs/improve.yaml (361 lines), tools/auto_promote.py headers, mag/behavioral_synth.py header, mag/tesuji_shell.py symbols. Swept by instrument (all files opened, size + mtime + first heading captured): all 101 daily/ files, all 47 root-level notes, all subdirs censused programmatically (candidates.jsonl parsed row by row, 0 unparseable). Vendored ponytail clone, deepseek_api/ reference dumps, and per-dig deep/ leaves were opened at head level only.

## 1. The pipeline (as coded, configs/improve.yaml + mag/improve.py)

- Trigger: Windows scheduled task `MagImproveDaily`, daily 08:00, `scripts/improve_daily.ps1` -> `.venv\Scripts\python.exe main.py improve --once`, log `logs/improve_daily.log`. Verified live: `schtasks /Query /TN MagImproveDaily /V` returned Status Ready, Last Run 9/28/2026 8:00:01 AM, Last Result 0, Next Run 9/29/2026 8:00:00 AM.
- `improve_once` (mag/improve.py:2109): scout() -> run_eval() -> (since 2026-09-28) tools/auto_promote -> synthesize_field_brief().
- scout() (mag/improve.py:1180): weekday rotation over `configs/improve.yaml:19-30` (Mon github/huggingface/agent_harness, Tue reddit/ollama/openclaw/mesh_comm, Wed arxiv/anthropic/openai, Thu openrouter/deepseek/xai/steal_protocol_repos, Fri google_adk/vast/agent_harness/platform/bleeding-edge, Sat catchup, Sun digest) plus `tier_a_always: [huggingface, reddit, github, arxiv, mag_internal, agent_memory]`; fetches pages/feeds, mines mag_internal (working.md, multi-smoke, IJL beads, behavioral leaves mag/improve.py:880, tesuji leaves mag/improve.py:1105, crash log census :712), appends rows to `memory/improve/candidates.jsonl`, writes `daily/<day>.md` blocks via `_write_daily_report` (mag/improve.py:1424).
- run_eval(): multi-smoke fixture check, writes `evals/<day>.json` + eval block in daily report.
- synthesize_field_brief() (mag/improve.py:1879): heuristic rank (LLM polish disabled, `synthesis.use_llm: false` after gemma:2b nuked briefs 2026-08-02, configs/improve.yaml:299), writes `field_brief.md`, `daily/<day>-field.md`, and `latest.md` (verified byte-identical to field_brief.md by diff).
- Human gates: `promote --apply/reject` (mag/improve.py:2693/2758), practices auto-append to playbook on promote (`promote.auto_append_practices_to_playbook: true`).
- Sidecars: opt-in `--deep` dig (mag/improve.py:2202, 17 runs 07-29..08-02), deepseek_rank (:1965, last 08-07), provider probe cadence 7d (:399, `provider_health/<day>.json`, fired 09-26), `improve --status` summary (:2619).
- Parallel event-driven leaf writers, NOT the scheduled loop: `mag/tesuji_shell.py:154` rebuilds `daily/<day>-tesuji-shells.md` on each `tesuji-shell log`; `mag/behavioral_synth.py:39` rebuilds `daily/<day>-behavioral.md` for callers (improve, decision_framework, growth_cycle, pro_library, tesuji_shell). This is why leaf mtimes (today 18:19 EDT) postdate the 08:00 scout (state.json last_scout 12:00:14Z = 08:00 EDT).

## 2. Ledger census (all numbers from commands run 2026-09-28)

- candidates.jsonl: 200 rows, 0 unparseable. Status: 130 new / 50 rejected / 14 promoted / 6 hold. Kind: risk 72, (none) 50, model 37, practice 16, runtime 13, tesuji 11, census 1. Source: mag_internal 97, mag_temperature_gap 50, reddit 19, huggingface 18, github 14, openclaw 1, mag_internal_drill 1. Date span 2026-07-24..2026-09-28, 17 distinct days, 51 rows carry no `date` field at all.
- `improve --status` (run this session, repo venv) confirms the same totals: ok=true, 200 total, by_status 50/14/130/6.
- Promotions by updated-month: 37 status flips in 2026-07, 12 in 2026-08, 1 in 2026-09. The 14 promoted: 11 July practice/tesuji rows, 2 FKB risk rows 08-06, 1 tesuji 08-06. Zero September promotions.
- 50 `mag_temperature_gap` rows are schema-less test pollution (keys ts/url/kind_hint/tags, no schema/date/kind; one row annotated "test-injected (tests/test_temperature_stack.py)" per B2-86) plus 1 mag_internal_drill rumor row (2026-09-27). These sit in the same file the scout/eval/promote reads.
- evals/: 17 root JSONs, 07-24..08-07 then 09-26/27/28 (50-day hole). 09-26 eval FAIL (multi_smoke_ok false), 09-27 and 09-28 PASS ("dual-local multi-model is real"). conductor eval ran once, 08-06, score 10/10.
- daily/: 101 files. Main daily reports exist only 19 of the 67 days from 07-24 to 09-28 (48 missing, the whole 08-09..09-25 stretch). Families: 19 main, 16 field, 17 behavioral, 17 tesuji-shells, 24 cost, 4 share-unpack, 3 verkle-audit.json, 1 verkle.md.
- Subdir cadence (newest artifact mtime): field_steal 258 files, last ledger 08-15 (days 07-31, 08-05, 08-09 burst, 08-10, 08-15); deep/ 17 runs ending 08-02; pins/skills 48 files, newest 08-08; growth/ 4 files, newest 08-25, growth_trail.jsonl has exactly 1 row (08-05); weaves/ W1-W7 all 08-03; behavior/ newest 08-06; blast/ newest 08-07; releases/gates.jsonl 19 rows, 09-26; provider_health 1 snapshot, 09-26.
- Live logs: skill_ledger.jsonl 3,961 rows spanning 08-07..09-28 (53 distinct days, active today); logs/behavioral_events.jsonl 215,580 good rows + 2 bad, first 08-04, last 2026-09-28T22:30:44Z; logs/tesuji_shells.jsonl 2,392 rows over 28 distinct days, first 08-05, last 2026-09-28T22:31:52Z (peak day 08-23 with 1,025).

## 3. What's working

1. The daily loop itself is alive again. 17 scheduled starts in the log (07-24, then 07-25..08-06 daily at 08:00:01, then 09-26/27/28). Today's run: scout added 4 candidates, eval PASS, brief synthesized 12:01:21Z, field brief 2,508 bytes written to all three surfaces.
2. Multi-smoke eval gate works and tells the truth: it FAILED 09-26 and PASSED 09-27/28 (evals/2026-09-26.json vs 09-28.json).
3. The local-signal miners never stopped: behavioral_events (215k rows), tesuji shells (2,392 rows, last entry 12 minutes before this audit's leaf mtimes), skill_ledger (3,961 rows, rows logged today). The event-driven leaves are the only daily/ artifacts written every working day since August.
4. Provider-health probe (B2-106/B2-494) fired on cadence: state.json last_provider_probe 2026-09-26, 11 probes, 3 alarms, snapshot provider_health/2026-09-26.json.
5. Playbook promotion is real when it happens: playbook.md holds composed, evidence-cited practices (Socratic boundary loop 08-05; sovereign-run lessons 08-03 including the write_file shape-collapse fixes with a named regression test tests/test_tool_dispatch_shape.py).
6. The promote gate itself works end to end (14 promotions landed July/August, triage-2026-07-25.md documents a 3 promoted / 20 rejected cut).

## 4. What's broken

1. STRUCTURAL: the weekly source rotation can never fire. `_weekday_keys` (mag/improve.py:193-196) returns `tier_a_always + day_keys` in that order, and `_select_urls` (mag/improve.py:198-216) truncates at `budgets.urls_per_day: 10` (configs/improve.yaml:11). huggingface carries 5 static URLs and reddit 5, so the cap is consumed by the first two always-on sources every single day; github, arxiv feeds, agent_memory, and every tier-B rotation key are starved. Today's fetch list proves it: exactly the 5 huggingface URLs ok + the 5 reddit URLs failed, nothing else, 10 of 10 slots. The rotation keys at configs/improve.yaml:19-26 are dead config.
2. The scheduled task died for 50 days: zero START lines in logs/improve_daily.log between 2026-08-06 08:00 and 2026-09-26 08:00. The gap left no evals, no main daily reports, no scout candidates between 08-08 and 09-25 (the behavioral/tesuji leaves dated in that window are event-driven sidecars, not scout runs). The task is registered and green now, but nothing in the log or state.json would have alerted anyone to the gap; state.json keeps only last_* fields.
3. The promote pipeline seized: 1 status flip in September vs 37 in July. 130 rows sit in new + 6 hold. The field brief has ranked the same 5 tesuji tickets (c-16c057730c5c, c-b235a1ae200a, c-380bf9d1d74a, c-e93d9d9af0fc, c-e46d14ea4db4, all score 22.5, all pointing at Aug 5-8 leaves) since at least 09-26; the 09-27 and 09-28 field briefs differ only in their two timestamp lines (diff verified). The loop is now ranking its own stale internal leaves instead of fresh external signal, which is a direct consequence of break 1 plus the static mag_internal miners.
4. The ledger is polluted: 51 of 200 rows (25%) are schema-less foreign rows (50 test-injected mag_temperature_gap + 1 drill rumor). read_candidates does not filter them by schema; improve --status surfaces them as kind "?" (50).
5. Reddit lane is 100% dead: all 5 reddit URLs fail every run (today 5/5 fail; state.json failed_urls holds exactly those 5; the same set appears in the 09-26/27/28 daily reports). No alarm, no demotion, no replacement source: the loop refails them daily.
6. blast/lattice state lies: blast/status.json says `"state": "running", "thread_alive": true` with ts 2026-07-31 while the newest artifact in the subtree is verkle_tip.json at 08-07. Two months stale, still claiming a live thread.
7. The ijl counter undercounts: `n_skills = len(list(skills_dir.glob("*.json")))` (mag/improve.py:636-638) counts only the 22 .json sidecars while 26 .md beads exist; the brief's "skills=22" is the json count, not bead count.

## 5. What never fired

- Q-002 auto-promote gate: wired TODAY (commit 2ba484fc9, 2026-09-28 12:57:47 -0400, after both of today's improve runs), `memory/improve/auto_promote.jsonl` does not exist, zero firings so far. First real test is tomorrow 08:00.
- Q-049 demote route: `tools/demote_candidates.py --dry` (run this session, exit 0) scans 200 rows and flags 6 runtime rows would_demote (runtime shape success rate below bar 0.6; skipped: 43 by status, 100 by shape, 50 by kind, 1 by cheap). `memory/improve/demoted.jsonl` never created: the CLI was never run for real, and it is documented standalone (not wired into improve_once, configs/improve.yaml:283-294).
- deep dive: last run 2026-08-02 (state.json last_deep_dive; 17 run dirs 07-29..08-02; deep/latest.json = the 08-02 60-minute run, 4/4 digs ok, elapsed 16.48 min). Never since, 57 days.
- deepseek_rank: last 08-07 (state.json last_deepseek_rank_n=5). Never since.
- field_steal: 258 files but only 5 active days, nothing since 08-15; STEAL_LATEST.md still points at the 08-15 ledger (259 files scanned, 9 vendors).
- IJL bead minting: newest pins/skills file 08-08. The "one assigned graph goal a day" habit of HABIT.md has minted zero beads in 51 days, yet the daily brief keeps printing "ijl: skills=22" as if the surface were alive.
- growth_cycle: growth_trail.jsonl holds exactly 1 row ever (2026-08-05). The growth/ lane is a one-shot.
- behavior/ loop-catch seeds: 2 index rows + 2 catch leaves, all 08-06/08-07. Never caught anything since.
- weaves W1-W7: composed once, 08-03, never revisited.
- hermes_self_improve: one attempt, killed by operator after ~6 min on 07-24 (hermes_self_improve_result.json: ok=false, stopped_by operator, "no file deliverables"). The Mag CLI bash path failure documented there matches SEATS.md invariant 7.
- Mag economy ledger: economy_totals.json last updated 08-07 (lifetime_saved 3,210,265 tokens, lifetime_turns 90). The GOAL.md economy instrument stopped being fed 52 days ago.
- Conductor eval: one run ever (08-06, 10/10).
- By-design-never (correct): model-seat auto-promote (max_auto_pull_gb: 0, auto_apply_model_seats: false) and remote-LLM scout (remote_llm_for_scout: false). Zero model pulls is policy, not failure.

## 6. Verdict

The improve loop is a July artifact running on September fumes: the scheduler is back (3 consecutive green days), the local miners never stopped, but the external-scout half is structurally starved (rotation dead by ordering + budget), the promote half seized after August (1 flip in Sept), the ledger is 25% test pollution, and 7 of the loop's named instruments (deep dive, deepseek rank, field steal, IJL beads, growth, behavior catch, economy ledger) have their newest artifact in July or August. The two newest gates (Q-002 auto-promote wired 12:57 today, Q-049 demote still dry-only) are the untested repair path: auto_promote.jsonl's first row tomorrow 08:00 is the single cleanest test of whether the loop closes again.

Files: this report banks as flash50/improve-loop-audit.md and flash50/s2-02.md, byte-identical. Every number above traces to a command run in this session (find/walk over memory/improve, python parses of candidates.jsonl / skill_ledger.jsonl / evals / daily / logs, grep of logs/improve_daily.log, schtasks query, improve --status, demote --dry, git log, diff of field briefs). No em-dashes in this file.
