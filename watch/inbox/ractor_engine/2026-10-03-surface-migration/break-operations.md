# break-operations: hostile byte-check of the operations lens (2026-10-03)

Pass: break-operations (hostile second pass). Lens under test: operations.md in this directory, four findings + five blind spots. Every check below ran in this sitting against the working tree; census moments 20:31-20:38Z 2026-10-03 unless named otherwise. The hermes_burn ledger and memory/attention.md are LIVE files (alarms still appending at 20:29Z), so every count, in the lens and here, is a moment on a moving tree (census denominator law: instrument, moment, delta).

Instruments (exact): wc -l, grep -c, head/tail on the ledgers and attention.md; a ./.venv/Scripts/python.exe JSON census over memory/runs/hermes_burn/usage.jsonl (row / doubled flag / cost split / id-prefix attribution); grep -n pattern checks on tools/*.py; find -newermt over watch/inbox/playground; git log; ls/cat on ./nul; a timeout-bounded grep over ~/.zcode.

## Verdicts

### F1 "identity-collision re-fire is 61 percent of today's hermes-ledger spend": CONFIRMED (money math and mechanism byte-reproduce; one framing caveat, two cite corrections)

Reproduction, my census 20:31Z: memory/runs/hermes_burn/usage.jsonl holds 1,236 rows (first 2026-10-01T13:11:41Z, last 2026-10-03T20:29:44Z); today rows 995; doubled_key true 850 rows costing $15.28 vs 145 clean rows costing $10.07 (total $25.35, doubled share 60.3 percent). The lens read 1,152 / 809 / $15.26 / $9.85 / 61 percent at an earlier moment on the same live file; direction and ratio reproduce within live-file drift. Attribution holds exactly: all 850 doubled rows are TAVERN (595) or DND0 (255) prefixed, zero other prefixes; 145 distinct ids today.

Mechanism byte-checks:
- tools/tavern.py:157 banks f"TAVERN_r{rnd}_{p['name']}", tavern.py:174 f"TAVERN_r{rnd}_JUDGE": no session component. tavern.py:10's own docstring promises id TAVERN_<run>_r<round>_<actor>: the run component was designed and never implemented.
- tools/dungeon.py:197 f"DND0_beat{self.turn}_dm", :271 f"DND0_beat{self.turn}_{actor}", :320 "DND0_S0_dm": turn-scoped only, no session component.
- Run dirs are second-stamped per fire (tavern.py:81-84, dungeon.py:140-142), so the per-run-dir DONE law (tavern.py:18 docstring; DONE written at tavern.py:214 and dungeon.py:349) can never trigger across fires: two fires minutes apart get different dirs.
- Guard absence: grep -n 'instance_guard|claim_ask|guard_or_exit' over tools/tavern.py tools/dungeon.py tools/arena_gwap.py returned zero matches, exit 1.
- Timing: the cure landed 2026-10-02 09:00:08 -0400 (commit 56449c53b, DOGFOOD-48H EXECUTED, sweeping instance_guard to 5 surfaces); tavern.py and dungeon.py both landed the NEXT day (commits b5dac8d83 and a7d7d313d, both 2026-10-03). First doubled row today 11:51:05Z, last 20:29:15Z, still firing at census.
- tools/instance_guard.py:4-10 founding incident quoted accurately by the lens ($25.53 of $37.76 re-fire excess, unwired-organ law).

Caveat attached to the verdict: the dollars are proven MISLABELED, not proven WASTED. Every fire stamps a fresh run dir with fresh transcripts (tavern.py:83, dungeon.py:141), so each flagged row is a new session's call under a colliding id; the bytes prove the id-collision class re-opened and carries 60 percent of today's spend, they do not prove any two dollars bought the same deliverable. 175 of the 850 doubled rows are ok:false costing $0.01 total (void beats). The lens's own falsifier (share collapsing under ~5 percent after id-prefixing; doubling persisting while no sessions fire) stands unchanged.

Cite corrections:
- "The guard sweep never reached them" is true for the claim guards and false if read as all of instance_guard: tavern.py:37 imports _bank from tools.hermes_burn and hermes_burn.py:153 runs doubled_key_check inside _bank. That inheritance is exactly why the alarm wall exists at all. What never reached the carriers: claim_process / claim_ask / guard_or_exit and any cross-fire DONE check.
- The move's "run stamp already exists at tavern.py:81-83 and dungeon.py:180" is half right: the stamp is at tavern.py:81-83 (confirmed) and at dungeon.py:140-141; dungeon.py:180 is the PRICING lookup line.

### F2 "the one escalation channel is flooded, pre-acknowledged, and never stops the behavior": CONFIRMED (sharpened: the consumer the lens feared exists, is unwired, and would not cover this class anyway)

- Counts at my moment: memory/attention.md = 1,178 lines; grep -c 'doubled-key alarm' = 850 (lens read 809/815 earlier on the same live file); the tail shows the wall still appending 20:23-20:29Z at one alarm per 5-10 seconds, same ids cycling (DND0_beat1_dm re-fires at 20:23:50, 20:25:41, 20:27:41).
- Pre-acknowledged by its own emitter: instance_guard.py:203-205 writes the "- [x] INSTANCE-GUARD doubled-key alarm" line itself. Confirmed in source.
- Test leakage into the same file: grep -c 'pytest-tmp' = 94 lines; attention.md:15-17 carry provider_probe alarms into agents/pytest-tmp-54164/...; :18-20 carry suite-burn paths (C:/Users/foste/AppData/Local/Temp/suite-burn-w5-full-basetemp/...); the trees exist on disk (agents/pytest-tmp, pytest-tmp-10012, -1004, -10040, -10084 and more).
- Consumer check (the lens's own falsifier): tools/attention_dam.py EXISTS (Mickey17 W3, 2026-09-30) and is the only mover-class tool. grep -rn 'attention_dam' over tools/ scripts/ mag/ returns only the tool's own lines (attention_dam.py:2, 30, 31, 242): zero callers, and no registration script in scripts/ references it. It would not help anyway: its archivable noise class is ONLY the session-record boilerplate (attention_dam.py:50 heading regex, :123-136 signal-by-default rule), so doubled-key alarm lines would be kept as signal even on a running dam. memory/attention_archive_20260930.md exists (a dam pass ran once, 09-30); grep -c 'attention-dam:' in today's attention.md = 0 (no pointer: the file has been rewritten since).
- "None of them stopped the paying behavior": code-confirmed. doubled_key_check (instance_guard.py:191-213) flags, alarms, and returns the row; hermes_burn.py:153-156 banks the flagged row; the paid call completed before _bank ran. No cancel path exists. Alarms kept firing through 20:29Z while TAVERN/DND0 kept paying.
- Shorthand flag: "the estate's ONE headless escalation channel" is shorthand, not a census. instance_guard.py:193-195 names attention.md the estate alarm surface and AGENTS.md:114 routes FTS alerts there, but other channels exist (watch/inbox INDEX, queue/handoff, gate_canary appends). What is uniquely true and migration-relevant: attention.md is on every specialist seat's boot-read list (AGENTS.md:57), so 850 junk alarms tax every seat's boot context.

### F3 "the one front door has no production traffic and no re-fire protection": CONFIRMED (one precision hit, one addition)

- cat memory/runs/route_chat/usage.jsonl read whole: exactly 6 rows, all 2026-10-03, ts 16:44:46Z to 18:49:36Z, goals 'route_chat smoke' x2, 'route_chat smoke v2' x2, 'route_chat smoke v3', 'nous failover smoke'. Zero production goals. Exact match.
- mag/route_chat.py:82-85 is the plain-append _bank; the module imports (route_chat.py:29-37) carry no instance_guard, and the file (read whole, 177 lines) contains no doubled_key_check. Confirmed.
- queue/STANDING_RAILS.md:46-48 ("tavern/dungeon/hermes_burn/grok_burn still self-call; each migrates to route_chat or documents its reason ... one per sitting, no batch rewrite") and watch/inbox/mag_rails_plugin_spec_20261003.md:10-12 ("The default model-call tool"): exact matches (the lens cited spec lines 10-13; the sentence ends at 12).
- Precision hit: "claim/landed-skip semantics live ONLY in the hermes_burn ask flow" is false by one file: grep -rln 'landed_skip|claim_ask' over tools/ mag/ scripts/ also hits tools/model_garden.py. The route_chat conclusion (the door itself carries none) is unaffected.
- Addition found while byte-checking: route_chat._bank banks NO cost_usd (route_chat.py:150-155 bank fields: ts, lane, model, goal, key_env, prompt_tokens, completion_tokens, ok), and configs/providers.yaml carries no pricing fields (grep pricing|price_in|price_out|cost returns only comments at :388 and :440). The one front door cannot price its own calls. See Addition A2.

### F4 "win32 headless traps are live debris": CONFIRMED and UPGRADED (the lens's specific cite was already stale when re-read; the generator is live and the reappearance is commit-proven)

- ./nul exists at repo root: my check (20:32Z) reads 122 bytes, mtime Oct 3 16:27; the lens read 127 bytes, mtime Oct 3 14:41. Content changed between the two moments: cat ./nul now prints "dir: cannot access '/b'" and "dir: cannot access 'watchinboxreplay_flash'", a cmd-style `dir /b watch\inbox\replay_flash` mangled through bash with a 2> nul redirect (watch/inbox/replay_flash/ exists, holding BARFIGHT_spec.md, DND_module.md). The file changing content twice in one day RESOLVES the lens's own falsifier: a live generator exists now, not hypothetically after the next cleanup.
- Reappearance is commit-proven: commit 56449c53b (2026-10-02 09:00:08 -0400) message records "root nul junk file removed (158B shell-error misredirect that blocked the index)". Removed yesterday, back today with new bytes.
- tools/estate_cleanup.py:19-26 documents exactly this class: reserved-name nul needs cmd /c del device-path deletion, and existence checks go through scandir, never os.path.exists. Exact match (lens cited 19-24; the scandir rule runs to 26).
- pytest tmp leakage confirmed: agents/pytest-tmp* trees on disk (at least five); 94 pytest-tmp lines in attention.md.
- Generator not in-repo: grep -rn "2> nul" and "dir /b" over tools/ scripts/ mag/ queue/ docs/ returned zero hits. The mangle comes from a live session surface typing cmd syntax into a bash shell, outside the repo's scripts: exactly the unwatched-multiplier class the finding names for an opencode-style headless surface.

## Additions (what the lens missed)

### A1: the late-day arena fire is a void-restart loop: near-zero dollars, maximum flood
Evidence: 175 of 850 doubled rows today are ok:false costing $0.01 total; the last ledger row is DND0_beat13_dm ok:false, 0 tokens, $0.00 at 20:29:44Z; playground dir stamps show three dnd0 sessions launched 11-15 seconds apart (dnd0_20261003T202147Z, T202158Z, T202213Z) with alarms continuing every 5-10 seconds to 20:29Z. dungeon.py:166-176 retries a content_filter beat 3x then voids and banks ok:false (:182-186); three concurrent sessions in 26 seconds is the missing claim_process guard made visible.
Falsifier: if the next scheduled fire produces ok:true rows and the ok:false share collapses, the loop was transient provider noise; if beat1_dm ok:false rows keep cycling past the next fire, the loop is stuck and pays attention-tax at ~6 alarms/minute for zero deliverable.
Move: add a consecutive-void circuit breaker in dungeon._paid (3 consecutive ok:false beats end the session with a DONE:VOID marker and one counted alarm), ~20 min.

### A2: the front door cannot meter dollars
Evidence: route_chat.py:150-155 banks no cost_usd while hermes_burn rows carry it (usage.jsonl schema); configs/providers.yaml has no pricing fields (grep: comments only at :388, :440); dungeon.py:179 shows a PRICING dict exists in-repo to port.
Falsifier: a cost_usd field appearing in route_chat ledger rows after the port kills this finding; if per-model lane pricing is genuinely unavailable, every per-deliverable-dollar comparison in the migration stays hermes_burn-only and inherits that blind spot.
Move: port the PRICING table into configs/providers.yaml lanes and bank cost_usd in route_chat._bank, ~30 min.

### A3: the interrupts leg of headless steering went unexamined
Evidence: queue/STANDING_RAILS.md:16-18 (law 3: "Interrupts never cancel ... an operator interrupt steers, it does not kill", dated 2026-10-03) and :49-50 ("30/50 lanes landed, ~20 killed by the interrupt before the no-cancel law landed"). None of the lens's four findings touches interrupts, yet the ask names the 50-wide judge wave dying mid-turn as the law's founding incident.
Falsifier: a headless run that absorbs an operator interrupt as a mid-run revision (the turn2_only revision shape, hermes_burn.py:216-223) without dying proves the law generalizes to the new surface; a second wave dying on interrupt kills it.
Move: wire a file-watch on the ask dir's revision.md so an interrupt lands as a revision instead of a kill, ~1 h.

### A4: the automation id is now citable in-repo, but the definition bytes remain unfound and "hourly" is contradicted by dir stamps
Evidence: my untruncated grep for b1ce1342 over memory/ queue/ watch/inbox/ state/ docs/ configs/ tools/ mag/ scripts/ hits memory/trajectory/steps.jsonl, watch/inbox/parable_day_one_20261003.md, and the sibling lens reports in this directory (the lens's zero-hit grep predates those bankings). The definition itself stays OWED: timeout 90 grep -rln b1ce1342 over ~/.zcode/workspace ~/.zcode/v2 ~/.zcode/tmp exited 124 (killed for time, truncated, same fate as the lens's attempt). Dir stamps contradict a strict hourly cadence: tavern dir names span 11:39Z-19:03Z with burst clusters (11:51, 11:53, 11:57 within six minutes), and three dnd0 dirs landed in 26 seconds at 20:21-20:22Z.
Falsifier: the automation definition bytes naming schedule and cap, wherever they live; or a session log tying each burst to a cron fire.
Move: dump the automation definition to watch/inbox as a receipt so "8 cycles today" becomes byte-backed, ~10 min (blocked on locating the definition).

### A5: the estate already built the flood-control organ for this failure class, and it is unwired
Evidence: tools/attention_dam.py (2026-09-30) classifies and archives attention.md noise; zero callers in tools/, scripts/, mag/ (grep: self-references only at attention_dam.py:2, 30, 31, 242); its noise class (attention_dam.py:50, :123-136) would keep doubled-key alarms as signal anyway; memory/attention_archive_20260930.md shows it ran once.
Falsifier: a scheduled dam pass whose after-stats show the alarm wall collapsed while [priority] signal survives cures this; a dam that archives doubled-key alarms (breaking instance_guard's alarm contract) is the counter-failure.
Move: register the dam on the daily patrol schedule AND give it a collapse rule (N repeats of one (ledger,id) alarm become one counted row per hour) before the plugin surface multiplies emitters, ~45 min.

## Still OWED (not asserted; instruments named)
- "8 cycles today" for automation-b1ce1342: definition bytes unfound in-repo and in a time-killed ~/.zcode grep (exit 124); the figure rides on the ask's word.
- Whether any two of the 850 flagged rows bought the same deliverable: not established; dir-level evidence says each fire built fresh sessions.
- Estate-wide re-fire share beyond the hermes_burn ledger: route_chat's 6 rows are near-zero; memory/runs/grok_burn and memory/runs/xai_grok exist and were not censused here.
