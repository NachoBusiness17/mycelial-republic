# BREAK-DOGFOOD: hostile second pass on the dogfood lens (2026-10-03)

Target: `watch/inbox/ractor_engine/2026-10-03-surface-migration/dogfood.md`
(read in full this sitting; the ask's paste was truncated mid finding 3's
falsifier, so all verdicts below are against the full file text).
Method: every evidence cite re-executed against the bytes this sitting,
20:27:42Z to 21:00Z. Sitting started at [DateTime]::UtcNow 2026-10-03T20:27:42Z.
Zero em-dashes. Nothing edited in the repo except this receipt.

## VERDICT SUMMARY

| finding (as pasted in the ask) | verdict | one-line reason |
|---|---|---|
| 1. "the migration already happened in fact" | CONFIRMED | every liveness claim re-proved byte-exact, and the falsifier's live half fired DURING this sitting (beat 1678 landed 20:32:58Z, new dnd0 dirs 20:21-20:22Z); two census numbers were wrong (26 tasks not 21; 41 dirs not 38) but wrong in the understating direction |
| 2. "route_chat has ZERO callers, the port bill" | CONFIRMED | repo-wide census incl. untracked found zero code callers; the falsifier fired on 3 mention-only files in archived gala receipts and none of them imports or calls the door |
| 3. (= file finding 1) "safe where caps and judges are in-band, openly broken where not" | WEAKENED | the in-band vs out-of-band architecture claim survives, but two evidence cites are byte-wrong (collusion timestamp; census "three mornings"), one is overstated as a universal ("no dead-letter"), and the lens missed the true collusion scale by 100x |

File findings 4 and 5 (not in the ask's paste) were also byte-checked; see
the tail of this receipt.

## FINDING 1: CONFIRMED (evidence bytes corrected)

Checked and byte-exact:

- `sed -n '2740p' memory/runs/hermes_burn/driver.beat` prints exactly
  `BEAT 2026-10-03T19:30:08Z cycle=1676`. 2,740 lines was the count at the
  lens's moment; the file has grown since (see live re-proof below).
- `scripts/descent_driver.sh:13-23` is the pidfile guard exactly as cited
  (PIDFILE line 13, second instance exits 3 at line 18, trap at line 23).
- `grep '2026-10-03T19:08:14' memory/runs/gwap/arena-capability.jsonl` hits
  one row, `wc -l` on the file reads 314 rows, the row carries
  `"byte_backed":true`.
- `memory/improve/latest.md` line 5: `generated: 2026-10-03T12:01:09.691819+00:00`.
- `logs/fts_index.log:442`: `[2026-10-03 09:00:01] END exit=0`.
- All three dossier quotes byte-verified in
  `~/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/memory/arena-gwap-useful-shit-law-20261003.md`:
  line 26 names `automation-b1ce1342` with the $25/day cap, line 32 carries
  "the automation fired AS ITS OWN PROMPT", line 40 carries "$20.00 of the
  $25 cap at the 15:00Z check" and the designed "arena over daily cap" hold.

Wrong or imprecise evidence bytes (finding survives all of them):

- Task count: `schtasks //Query //FO CSV | grep -iE 'Mag|Estate'` this
  sitting returns 26 matching rows, not 21: 9 `Estate ...` + `EstateWalkDaily`,
  15 `Mag...`, plus `mag-docker-watchdog`. Three are Status: Disabled:
  `Estate LaneSupervisor`, `MagLabKit8765`, `MagPrivateOffice8765` (the two
  8765 servers the file lists as part of the "21" are disabled). 23 Ready.
  The lens understated its own baseline.
- Playground dirs: 41 dirs match `20261003` (25 dnd0 + 16 tavern), 38 carry
  a DONE marker, 33 carry GWAP_BANKED. The file's "38 session dirs ... with
  DONE + GWAP_BANKED markers" is wrong as a conjunction; it is the DONE count.

Live re-proof stronger than the lens's own evidence: this sitting began
20:27:42Z with beat 1677 (20:01:22Z) as the tail. `tail -2 driver.beat` at
20:59:00Z reads `BEAT 2026-10-03T20:32:58Z cycle=1678`, and
`ls -t watch/inbox/playground/` shows new unattended sessions
`dnd0_20261003T202147Z`, `dnd0_20261003T202158Z`, `dnd0_20261003T202213Z`.
The headless half advanced while this break pass ran, with no seat steering.
The falsifier (suspend the seat, watch the meters) is now cheap to run
tonight instead of hypothetical.

Sharpening the lens missed (measured on 6 of the 26 tasks, all 6 the same):
`schtasks //Query //TN <task> //FO LIST //V` for MagImproveDaily,
MagCensusPatrolDaily, MagFtsIndexDaily, mag-docker-watchdog, Estate Cooker,
Estate LaneSupervisor all read `Logon Mode: Interactive only`,
`Run As User: foste`. The entire sampled cron estate is login-gated:
"operator-independent" is decision-independent, not machine-independent.
After a logout or a reboot-without-login, all 23 Ready tasks stop, and the
descent driver (a child of a long-lived bash process, pidfile
`state/descent_driver.pid` = 86854, confirmed alive via `kill -0`) dies with
the session that owns it. See Addition A.

## FINDING 2: CONFIRMED (falsifier tested and did not stick)

- Repo-wide census run this sitting, including untracked files:
  `grep -rln --include='*.py' 'route_chat' . | grep -v .venv,__pycache__`
  returns `mag/route_chat.py` plus two archived gala files;
  `grep -rln 'route_chat' --include='*.sh' --include='*.ps1' --include='*.cmd' --include='*.bat' .`
  adds one more. The falsifier's condition fired, so each was read:
  - `watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-intelligent-burn_check.py:61`
    is a quoted STANDING_RAILS text string, not a call.
  - `watch/inbox/gala_20260925/dd-selfsteal/lanes/_byproducts/filer_state_append.py:33,37,45`
    are prose strings describing the rails.
  - `watch/inbox/gala_20260925/dd-selfsteal/lanes/selfsteal-24h-laws.check.sh:150`
    is a file-existence list that mentions `mag/route_chat.py`.
  Zero imports, zero calls. The four-tree grep claim (exactly the module and
  its cache) is a subset of this census and holds; `mag/__pycache__/route_chat.cpython-311.pyc`
  exists as cited.
- `memory/runs/route_chat/usage.jsonl` read in full: exactly six rows, four
  `ok:false` deepseek smokes 16:44:46Z to 16:47:09Z, v3 `ok:true` 16:47:21Z,
  nous failover `ok:true` 18:49:36Z on `"key_env": "HERMES_API_KEY_2"`. As cited.
- `queue/STANDING_RAILS.md:26` (the drop-in row "any one model call |
  mag.route_chat(lane=, goal=)") and `:45-48` (registered self-call debts:
  tavern/dungeon/hermes_burn/grok_burn) byte-exact.

The port-bill economics finding stands on stronger legs after this pass:
even the estate's own archived receipt scripts only talk about the door.

## FINDING 3 (file finding 1): WEAKENED

Byte-exact confirms:

- `tools/tavern.py:15` "hard stops: round cap, cumulative budget_usd";
  defaults `--rounds 8` / `--budget-usd 5.0` at `tools/tavern.py:222-223`.
- The Greta meta-leak: the transcript row at
  `watch/inbox/playground/tavern_20261003T190348Z/transcript.jsonl` tagged
  `TAVERN_r2_Greta Thornwood` (19:05:05.584Z, sonnet-5.5, turn 2) plus the
  schema row one microsecond later carrying `"esc_after": 3` whose `speech`
  field is literally the model's drafting notes ("I need Greta's line under
  120 words, no em-dashes..."), and the judge text "out-of-character
  drafting notes with no in-world content" appears verbatim.
- `driver.log:279335` is exactly
  `FAIL PODCAST_STRUCTURE_spec: RuntimeError("transport failed after 2 tries: TimeoutError(...")`
  and the ask dir holds only `ask.json` (2,905 bytes) + `CLAIM` (68 bytes),
  no output, so the skip rule (`descent_driver.sh:4-5` comment, implemented
  as `_landed_skip` at `tools/hermes_burn.py:206-227`, skip only when the
  output exists) never skips it.

Byte-wrong or overstated:

1. Collusion cite is wrong on the row. The 19:08:14Z capability row reads
   `"suspected_collusion":false` with `compared_claims: 0` and evidence
   "below 2 claims there is no order information". The true flag the lens
   meant is the 13:10:34Z row (evidence "identical order of 2 claims between
   independent authors gw-954383f656e5 and gw-2741a8880854", verdict
   CHALLENGE, artifact_rarity tainted).
2. The scale is 100x what the lens said. `grep -c '"suspected_collusion":true'`
   on the ledger = 100 of 314 rows (31.8 percent), and all 100 tainted rows
   still carry `meter_credit.byte_backed:true`. The lens cited one row; the
   arena's in-band anti-cheat is flagging a third of all scenes and they all
   still bank as byte-backed credit. See Addition B.
3. "END exit=1 three mornings straight (lines 160, 184, 212)" is wrong twice.
   The lines exist and all read `END exit=1`, but they are 10-02 03:29:15,
   10-02 08:30:00 and 10-03 08:30:01: two mornings, three runs. And the
   10-03 exit is not the pytest drift: that run's log shows
   `TASK-DOCTOR: 4 unhealthy task(s) named, alert appended` as the failing
   check; the quoted "pytest holds 4197 vs carrier claim 4156, delta +41" is
   `logs/census_patrol.log:192`, from the 10-02 08:30 run. The 4197-vs-4147
   (+50) variant is line 168, from the 10-02 03:29 patrol.
4. "no dead-letter, no max-retry" is false as a universal. `tools/hermes_burn.py`
   has a terminal dead-letter for provider refusals: 2 or more ledger
   refusals mints a REFUSED marker and skips on sight (`:195-203`,
   `:295-305`, receipt for the DAY1_RIB_WARMTH 46x/42x loops at `:180-181`),
   atomic O_EXCL CLAIM locks at `:267-283`, and inference-budget terminal
   skips at `:306-309`. What has no dead-letter is exactly the
   transport-timeout class: PODCAST_STRUCTURE_spec failed with transport
   errors 9 times at the lens's sitting and the count is 11 now
   (`grep -c 'FAIL PODCAST_STRUCTURE_spec' driver.log` = 11), still no
   REFUSED marker in the ask dir. The mechanism grew DURING this audit,
   which is live confirmation the loop is real; the accurate law is
   "refusals dead-letter, transport failures do not".

## FILE FINDINGS 4 AND 5 (not in the ask's paste, byte-checked anyway)

- Finding 4 (splintered ledgers): re-computed this sitting over
  `memory/runs/hermes_burn/usage.jsonl`: 10-01 $37.76 / 236 rows (exact),
  10-02 $1.17 / 5 rows (exact), 10-03 now $25.35 / 995 rows (was $25.11 /
  911 at the lens's moment: both the row count and the dollars grew during
  the audit window), total $64.29, which now matches the driver's standing
  total exactly (`driver.log` tail: `HERMES-BURN: PASS - 28/28 asks; ledger
  total $64.29`); the $0.22 discrepancy the lens noted has self-healed.
  Today's model set byte-exact: claude-fable-5.1, claude-haiku-4.5,
  claude-opus-5.5, claude-sonnet-5.5, z-ai/glm-5.3-prime. `logs/usage.jsonl`
  is 70,689,428 bytes. CONFIRMED, moment-true numbers trending up.
- Finding 5 (composition clause): `mag/gwap_to_gps.py` exists (Sep 29,
  11,061 bytes) and `tools/gps_mcp/gps_ledger.db3` is 94,208 bytes written
  Oct 3 10:09, both as cited. `watch/inbox/frontier_delta_register_20261003.json`
  parses as a list of exactly 14 rows, confirming the lens's 14-not-39 gap
  against the topic. New: the full-ledger verdict census the lens left OWED
  is 58 VERIFIED_AGREE / 152 DISPUTE / 104 CHALLENGE over 314 rows, so
  DISPUTE is 48.4 percent of all arena judgments, which strengthens the
  lens's own point that routing dollars off DISPUTE rows mislabels
  escalation. RESOLVED from OWED.

## BLIND SPOTS: updated

1. Automation config: STANDS, search now named. I looked for
   automation-b1ce1342 by filename across `~/.zcode` (nothing), as a key in
   `~/.zcode/cli/config.json` (nothing), in the CLI sqlite
   (`~/.zcode/cli/db/db.sqlite`, read-only: no workflow_definition or
   workflow_run rows; the id string exists only inside session text bytes).
   The lens's claim that the in-repo footprint is only trajectory rows is
   consistent with `grep -c 'b1ce1342' memory/trajectory/steps.jsonl` = 46;
   no readable automation-definition store was found from this seat.
2. Seat-token meters: STANDS. `grep -rln '9\.5M|582K' watch/inbox/` hits only
   the sibling lens doc
   `watch/inbox/ractor_engine/2026-10-03-surface-migration/accuracy.md` and
   unrelated binaries; no instrument ledger found.
3. Reboot-survival: SHARPENED into Addition A. It is worse than untested:
   the crons are Interactive-only, so the whole "headless" half is coupled
   to one logged-in Windows session (6 of 26 tasks sampled, all Interactive).
4. Key handling: not re-audited this pass beyond the HERMES_API_KEY_2
   failover row; stands for the security lens.
5. gwap verdict counts: RESOLVED (58/152/104 over 314; the dossier's
   266/178 and 50/128/88 were a mid-day moment, superseded by current bytes).
6. No pytest run by the lens: also true of this pass. This is a receipts
   audit; no test suite was executed here either.
7. Operator-side invisibility: STANDS for the communication lens; Addition E
   names one concrete operator dependency it can start from.

## ADDITIONS (what the lens missed)

A. The unattended estate is logon-coupled, not operator-independent.
   Evidence: `schtasks //Query //TN MagImproveDaily //FO LIST //V` reads
   `Logon Mode: Interactive only`, `Run As User: foste`; same for
   MagCensusPatrolDaily, MagFtsIndexDaily, mag-docker-watchdog, Estate
   Cooker, Estate LaneSupervisor (6 of 26 sampled, zero non-interactive
   found). Falsifier: log off (or reboot without login) for one cron period:
   if any Mag*/Estate* task fires while logged out, this finding dies.
   Move: make the boot-layer decision an explicit part of the migration
   verdict (auto-login vs S4U/service-account tasks vs rails as daemons),
   about 30 minutes to convert one task as the pilot.

B. The collusion meter banks tainted scenes anyway. Evidence:
   `grep -c '"suspected_collusion":true' memory/runs/gwap/arena-capability.jsonl`
   = 100; `grep '"artifact_rarity":"tainted"' ... | grep -c '"byte_backed":true'`
   = 100; example row 13:10:34Z (verdict CHALLENGE, tainted, byte_backed
   true). Since STANDING_RAILS.md:39-42 routes the next ask's dollars off
   capability rows, up to a third of the routing signal is flagged-colluded
   and still banked. Falsifier: the dollar-router (mag/gwap_to_gps.py)
   provably filters artifact_rarity=tainted rows; if it does, this weakens
   to a labeling bug. Move: read the router's filter, add a tainted
   exclusion if absent, about 45 minutes.

C. There is a third failure class between in-band and out-of-band:
   caught-but-never-healed. Evidence: DND0 beats carry 278 usage rows today,
   only 90 ok:true; `DND0_beat8_dm` alone has 18 rows, every one
   `ok:false, cost 0.0`, most flagged `"doubled_key": true`, re-fired from
   12:28Z through 20:28:56Z (the INSTANCE-GUARD doubled-key alarms in
   `memory/attention.md` at 20:27:00Z to 20:29:15Z fired during this
   sitting). The guard absorbs the spend at $0 per attempt, forever, and
   nothing heals the state that causes the re-fire. Falsifier: bank or purge
   the failed morning dnd0 dirs and the alarms stop; if fresh beat ids start
   looping instead, the loop is in the stager, not the bank step. Move: make
   arena ingest mark failed-beat runs terminal, about 30 minutes.

D. The poison loop is live and countable: `FAIL PODCAST_STRUCTURE_spec`
   grew from 9 (lens's sitting) to 11 during this audit
   (`grep -c 'FAIL PODCAST_STRUCTURE_spec' memory/runs/hermes_burn/driver.log`),
   first-cited line 279335 byte-exact. The fix is already templated in the
   same file: reuse the REFUSED marker path (`tools/hermes_burn.py:195-203`)
   for transport failures after N tries. Falsifier: an output file appears
   in `memory/plans/hermes_burn_playground_20261003/PODCAST_STRUCTURE_spec/`
   and the FAIL count freezes while beats continue. Move: mint a
   TRANSPORT-FAIL terminal marker, about 30 minutes.

E. The headless surface already files operator-bound alerts, and the
   migration verdict must name who actionizes them. Evidence:
   `logs/census_patrol.log` 10-03 08:30 run: `TASK-DOCTOR: 4 unhealthy
   task(s) named, alert appended` (exit 1); its alerts land in
   `memory/attention.md`, which today only a seat reads. Falsifier: a 24h
   closed-seat run where every attention.md alert is consumed by a rail
   rather than a seat. Move: add an alert-disposition column to the dawn
   report so headless consumption is countable, about 45 minutes.

F. The strongest form of finding 1's evidence re-proved itself mid-audit:
   beat 1678 (`BEAT 2026-10-03T20:32:58Z cycle=1678`) landed 5 minutes into
   this sitting, plus three new dnd0 session dirs at 20:21-20:22Z. The
   24h closed-seat falsifier can be run tonight at near-zero cost; the
   migration verdict should demand that run before it lands.

## OWED (not verified this pass)

- Logon Mode was sampled on 6 of 26 tasks; the other 20 were not queried.
  All 6 samples read Interactive only; the universal form of Addition A is
  therefore an inference, not a full census.
- The semantics of `byte_backed:true` on tainted rows (receipt-backing vs
  credit-paid) were not traced into mag/gwap code; Addition B's router
  filter question is open.
- The 4 unhealthy tasks TASK-DOCTOR named are not enumerated in the log
  line read; my 3 Disabled finds are a plausible but unproven subset.
- No pytest collection or execution was run in this pass (receipts audit).
- Whether the descent driver survives logout (it is a child of a bash
  process owned by the interactive session, pid 86854 alive via kill -0)
  is inferred from Windows session semantics, not tested by logging out.
