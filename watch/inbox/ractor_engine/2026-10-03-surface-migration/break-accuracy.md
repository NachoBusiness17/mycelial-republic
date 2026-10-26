# break-accuracy - hostile second pass on the accuracy lens (2026-10-03)

Sitting moments: 2026-10-03 20:30-20:50Z. HEAD moved under this pass twice
(a7d7d313 at ~20:31Z, e0344fe39 at ~20:47Z per git rev-parse / git log -1).
Every count below is a moment snapshot on a moving tree; lens moments were
19:35-19:50Z. Instruments: .venv/Scripts/python.exe over the jsonl ledgers,
MSYS ps, grep/find/cat as named per check. No model calls were made.

## VERDICTS

### F1 cost arms do not byte-check - CONFIRMED

Reran the census myself (memory/runs/hermes_burn/usage.jsonl): 1,236 rows at
my moment (lens read 1,152 at 19:35-19:50Z; +84 landed in between). By model:
anthropic/claude-opus-5.5 501, sonnet-5.5 316, haiku-4.5 231, fable-5.1 181,
z-ai/glm-5.3-prime 7. GLM all-time: 7 rows, $1.6379, mean prompt 31,224
(lens claimed 7 / $1.64 / 31,224 - exact to the digit). GLM today: 2 rows,
$0.464 (lens: $0.46). Opus today: 416 rows / $14.0096 at my moment (lens:
362 / $13.8657 - moment drift, same conclusion). The only ~$13 line is the
opus arm, and AGENTS.md:32 marks Anthropic keys UNFUNDED. Arithmetic: 9.5M/13
= 730.8K, 582K x 13 = 7.566M - the ask's pair is internally inconsistent
regardless of meters. watch/inbox/replay_flash/ holds exactly 13 .md files
and nothing else (ls -la; no manifest, no token counts).

Hostile check the lens skipped, and the absence survived: the plausible seat
meters it never opened all meter OTHER seats. memory/runs/seat_spend/
spend.jsonl (1,059 rows) is schema grok_seat_burner.spend.v1, seat "sd" (the
xAI SD grok seat); deepseek_bill.jsonl (11,286 rows) is deepseek cash;
memory/runs/gab_seat.jsonl's last row is 2026-08-18. No checked instrument
banks z.ai coding-seat tokens. Absence scope named: hermes_burn/usage.jsonl,
seat_spend/{spend,deepseek_bill}.jsonl, gab_seat.jsonl, plus zero hits for
"9.5M" over recursive grep of watch/inbox/, memory/runs/, queue/.

### F2 register counts mutually inconsistent; 8-5 derivable from no artifact - CONFIRMED

json.load of watch/inbox/frontier_delta_register_20261003.json (mtime Oct 3
12:22): 14 rows, columns id, frontier_chars/cites/unver, flash_chars/cites/
unver, contract_parts - no judge scores, no deepseek arm. Recomputed tallies:
chars frontier_better 10 / flash_better 4; unver flash_fewer 12 /
frontier_fewer 1 - exactly the lens's numbers. queue/STANDING_RAILS.md:49-50
reads "30/50 lanes landed, ~20 killed by the interrupt before the no-cancel
law landed" verbatim. memory/runs/hermes_burn/judge2_duel.jsonl: 9 rows
(wc -l). Recursive grep for the exact strings "39 judged" and "9.5M" over
watch/inbox/, memory/runs/, queue/: zero hits. I also read the artifact the
lens never opened, watch/inbox/frontier_delta_steal_20261003.md, in full: it
names the three-arm replay and cost units ("$0.14 per deepseek arm and seat
tokens per flash arm", line 30-31) and carries no 39, no 8-5, no totals. The
"39 judged lanes / frontier beat flash 8-5" headline in the ask is derivable
from no artifact found. Caveat: bare "8-5" matches timestamp noise, so the
absence claim is carried by the exact strings and the full read of the only
delta-study receipt on disk.

### F3 front door is real code with zero production traffic; headless rails demonstrably run - CONFIRMED

Byte-read memory/runs/route_chat/usage.jsonl: exactly 6 rows, 4 ok:false
(2x "route_chat smoke", 2x "v2"), 2 ok:true ("smoke v3", "nous failover
smoke" on key_env HERMES_API_KEY_2 - the failover chain proven live).
mag/route_chat.py:42 pins USAGE to that one file and _bank (:82-85) is the
only writer, called only after a successful HTTP response, so the ledger is
a lower bound on traffic; zero production rows stands a fortiori. Code cites
all exact: key chain :52-68 (reads .env at :63-66), endpoint fence :71-79,
dormant gate :113-115. queue/STANDING_RAILS.md:46-48 registers
tavern/dungeon/hermes_burn/grok_burn as still self-calling, byte-checked.
Liveness reproduced: MSYS ps shows pid 86854, WINPID 18096, STIME Oct 2,
"bash scripts/descent_driver.sh"; memory/runs/hermes_burn/driver.beat is now
2,742 lines (Oct 1: 157, Oct 2: 1,709, Oct 3: 876) and the cited tail exists
verbatim at driver.beat:2740 ("BEAT 2026-10-03T19:30:08Z cycle=1676"; cycles
1677-1678 landed since). Added sharpening the lens implied but did not say:
scripts/descent_driver.sh:33-38 shows the flagship carrier calling
tools/hermes_burn.py and tools/ds_workhorse.py directly, so the rails' own
law 1 (STANDING_RAILS.md:10-12, "the front door is mag.route_chat") is
violated by the rails' own primary headless carrier.

### F4 ok=true banks on 1-char stubs; success signal lies - CONFIRMED, two citation corrections

The cited row is real: id GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003,
z-ai/glm-5.3-prime, finish_reason "length", content_chars 1, ok true - but
its ts is 2026-10-03T19:25:23.803567Z, NOT 19:07:48Z as the lens cited (the
19:07:48Z ts holds an unrelated tavern sonnet row). Right row, wrong stamp.
Count verified: 3 of 7 all-time glm rows have content_chars<=1 (my filter,
same 3 rows). Code shape verified: mag/route_chat.py:148 falls back to
msg.get("reasoning") and :150-155 banks before raising with
"ok": bool(content); tools/hermes_burn.py:379 banks ok:True on any non-empty
channel with only a refusal gate at :358-375. Corrections the lens missed:
(a) watch/inbox/hermes_burn/ holds 4 poisoned-evidenceless files (S5_stores,
S6_docker, S7_mates, S8_stealth), not "1 + 2 siblings"; (b) the two Oct 2
stub rows carry self-describing annotations (note "STUB: content under
substance floor... re-ask owed"; today's row channel "reasoning-dump (content
stub; raw reasoning banked)"), so the ledger partially self-reports the
failure - but route_chat's own banked rows carry no stub annotation at all,
and any aggregator reading the ok flag still gets lied to. queue/
STANDING_RAILS.md:13-16 (law 2, the hollow-batch law, "the run still prints
ok=True") is the estate's own convergence with this finding, same day.

## BLIND-SPOT SPOT-CHECKS

- automation-b1ce1342: zero in-repo hits, reproduced. Scope: grep -rln over
  the repo excluding .git for *.md,*.json,*.jsonl,*.sh,*.ps1,*.py,*.yaml,
  *.yml. The cron's definition and retry/skip semantics stay OWED.
- Arena cadence via gwap ledgers: memory/runs/gwap/arena-capability.jsonl
  has 314 rows with created_utc on 2026-10-03 spread over hours
  13,14,15,17,18,19Z (gap at 16Z); arena-sessions.jsonl has 60 today, all in
  hour 12Z. Roughly-hourly with a gap is what the bytes show; the ask's
  "8 cycles today" is not countable from either ledger.
- MSYS ps vs tasklist instrument mismatch: reproduced (ps -p 86854 answers,
  pid alive since Oct 2).

## WHAT THE LENS MISSED (the additions)

1. THE NUL-FILE TRAP IS RECURRING AND RECEIPTED. Repo-root file `nul` (530
   bytes, mtime Oct 3 16:32 EDT) contains MSYS dir stderr with
   backslash-eaten paths (C:Usersfoste... for tools/attention_dam*,
   overmind_senses.py, instance_guard.py, cost_rollup.py) - a cmd-ism (>
   nul) run inside bash. Prior art: HEAD-1 commit 56449c53b (2026-10-02
   09:00 EDT) already removed a "158B shell-error misredirect that blocked
   the index" nul file; this is the second firing in two days. Same-minute
   co-occurrence with .mimosa/history/run-20261003T203242439Z makes the
   Mimosa scan hook the probable writer (inference, not proven). Falsifier:
   a named-process receipt showing a different writer, or proof the Oct 3
   file predates the hook run. Move: reserved-device-name guard in
   instance_guard.py plus a bash-isms sweep of the scan/lane shells (~30
   min).

2. LAW 3 (INTERRUPTS NEVER CANCEL) IS PROSE-ONLY IN THE RAILS' OWN DRIVER.
   queue/STANDING_RAILS.md:17-18 states it; scripts/descent_driver.sh:33-38
   runs hermes_burn and ds_workhorse as foreground children of its bash loop
   with no background-execution, no disown, no checkpoint-resume - the only
   mechanical protection is the pidfile claim lock (:13-23). An interrupt of
   the driver's console kills the paid child mid-turn, the exact failure the
   law was written against. Falsifier: a driver revision whose children
   survive a kill of the parent with resumable state. Move: implement law 3
   in the driver (background + per-ask resumable checkpoint), ~45 min.

3. THE LINEAGE LEG THE VERDICT MUST NAME: DESCENT-PROTOCOL LEG 4.
   AGENTS.md:35 makes "the seat steers as OPERATOR-PROXY between turns" a
   law leg, and it is interactive-only by construction. The poisoned files
   and ok:true stubs are what the rails already bank when that leg is
   absent. A migration that does not name the mechanical substitute
   (rendered-material check + judge pass gating ok:true) re-loses the
   guarantee the interactive seat provided. Falsifier: a full day of
   headless output where ok:true is gated on render+judge with zero poisoned
   artifacts - then leg 4 is substitutable. Move: write the substance gate
   into route_chat/hermes_burn banking (min content_chars, {text}-render
   check, judge on design depth), ~60 min.

4. THE ECONOMICS COMPARISON IS UNFALSIFIABLE UNTIL A SEAT METER EXISTS. The
   two arms are in different currencies (hermes_burn banks cash;
   the flash arm burns quota-license window tokens) and no checked
   instrument meters the z.ai coding seat (see F1 hostile check). Until a
   per-run seat-token ledger exists, any tokens-per-deliverable number for
   the flash arm, including the ask's 9.5M/582K, is uncheckable by
   construction. Falsifier: an in-repo meter found that already banks z.ai
   seat tokens per run. Move: one jsonl row per replay run (task, window
   tokens, deliverable chars) written by the replay driver, ~30 min.

5. THE DOGFOOD EVIDENCE IS REAL BUT THE CADENCE INSTRUMENT IS LOOSE. Arena
   gwap payloads today: 314 rows across hours 13,14,15,17,18,19Z with a 16Z
   gap; sessions all in 12Z. "Hourly cron, 8 cycles" is not countable
   in-repo; the cap-hold story is plausible but unreceipted here. Falsifier:
   the outside-repo automation log showing 8 fired cycles today. Move:
   tavern/dungeon write one DONE row per cycle to a single ledger with cycle
   count, ~15 min.

6. THE MIGRATION HAS ALREADY HAPPENED IN PRACTICE; THE VERDICT IS ABOUT
   FINISHING, NOT RE-PLATFORMING. The paid workhorse is already headless
   (driver alive since Oct 2, 2,742 beats; 1,236-row bank ledger; 314 gwap
   payloads today) while the declared front door has 6 smoke rows and the
   rails' own carriers bypass it (descent_driver.sh:33-38). The honest
   verdict space is therefore hybrid/finish-in-place: route the existing
   carriers through route_chat and gate its ok flag, rather than standing up
   a new opencode surface on unbanked economics. Falsifier: route_chat
   accumulating production rows from the carriers without a gate change and
   staying clean for a week - then the door thesis holds as-is.
