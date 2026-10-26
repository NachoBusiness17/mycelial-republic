# DOGFOOD LENS - surface migration raction (2026-10-03)

Lens question: which standing rails already run headless today without the
interactive seat? Method: every number below was read or computed in this
sitting; commands named inline. Zero em-dashes.

## THE HEADLINE

The migration is not a proposal, it is a description. The estate already runs
headless by default, and the interactive seat's residual unique work is
staging, judging, and steering. Today's (2026-10-03) unattended receipts:

- 21 Windows scheduled tasks named Mag*/Estate* (census patrol, FTS index,
  improve, endpoint news, gate canary, secret scan, vision nightly, X radar,
  tip witness, ratchet, LaneSupervisor, Librarian, Gopher, KeyAudit, StealthSweep,
  FullScan, Cooker, Spine Index, EstateWalkDaily, LeaveProtocol, docker watchdog,
  two 8765 servers). Instrument: `schtasks //Query //FO LIST` grep, this sitting.
- The descent driver alive unattended: `memory/runs/hermes_burn/driver.beat`
  line 2740 reads `BEAT 2026-10-03T19:30:08Z cycle=1676`, 2,740 beat lines
  append-only across restarts; pidfile guard at `scripts/descent_driver.sh:13-23`
  (second launch exits 3, proof per `state/CURRENT.md:23-24`).
- The hourly arena: 38 session dirs dated 20261003 under
  `watch/inbox/playground/` (tavern + dnd0), latest with DONE + GWAP_BANKED
  markers; gwap capability row minted 2026-10-03T19:08:14Z in
  `memory/runs/gwap/arena-capability.jsonl`, byte_backed true.
- MagImproveDaily green 08:00 (`memory/improve/latest.md`, generated
  2026-10-03T12:01:09Z); FTS 09:00 exit=0 (`logs/fts_index.log` END line).
- The arena cron fires AS ITS OWN PROMPT: the ZCode-side dossier
  (`~/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/
  memory/arena-gwap-useful-shit-law-20261003.md`, read this sitting) records
  "by the 14:00Z cycle the automation fired AS ITS OWN PROMPT into the
  session... The cadence is operator-independent", and cycle 4 hit $20.00 of
  the $25/day arena cap at the 15:00Z check with the next fire designed to
  hold ("arena over daily cap").

## FINDINGS

1. Headless rails are safe exactly where the failure class has an in-band
   terminal state, and the unattended loop is real for exactly the class that
   has none. (Corrected per the hostile second pass, re-checked this sitting.)
   In-band terminal states exist and work: tools/hermes_burn.py:195-203 mints
   a terminal REFUSED marker at >=2 provider refusals, :295-305 skips such
   asks on sight, :306-309 skips terminally burned asks, :206-227 blocks
   re-burning landed deliverables, :267-283 closes the twin-race window with
   an atomic O_EXCL CLAIM. The arena's instruments ran at scale: 100 of 314
   rows in `memory/runs/gwap/arena-capability.jsonl` carry
   suspected_collusion:true, all 100 byte_backed:true, first batch banked
   13:10:34Z - but every true row is a dungeon scene (dm/players report
   identical dice quadruples, compared_claims 2), so the flag is structural
   for the dungeon shape, not fraud: the instrument catches the pattern and
   the pipeline has no shape-awareness to separate designed agreement from
   actual collusion. The precise gap class: transport timeouts produce no
   output, no REFUSED, no budget skip, so PODCAST_STRUCTURE_spec re-fires
   every driver cycle - its FAIL count grew 9 -> 12 across this sitting
   (grep -c on driver.log, rerun) while its ask dir still holds only ask.json
   (`memory/plans/hermes_burn_playground_20261003/PODCAST_STRUCTURE_spec/`).
   Census patrol correction: my "three mornings straight" was wrong. END
   lines in `logs/census_patrol.log` show failures on 09-28 17:20, 09-29
   08:30, 09-30 08:30, 10-02 03:29, 10-02 08:30, 10-03 08:30 - five of the
   last six scheduled runs failed, and 10-01 has no END line in this log
   (dark or rotated, not verified). The 10-03 run (START line 185) failed on
   three findings: COLLECT-DRIFT +41 (line 192, 4197 vs carrier 4156 - this
   line belongs to the 10-03 run, not the 10-02 run), ZERO-COLLECT
   tests/test_selffeed_integration.py (line 193), and TASK-DOCTOR 4 unhealthy
   tasks (line 204); the printed cures (lines 194-196) all route to manual
   operator action.

2. The migration's named front door is a door with zero footsteps. An
   untruncated census, `grep -rln route_chat` over mag/, tools/, scripts/,
   tests/ (full trees), returns exactly two hits: `mag/route_chat.py` and its
   .pyc cache. Zero callers. The five carrier tools named in the registered
   debts contain no route_chat reference (same grep), so
   `queue/STANDING_RAILS.md:26` "any one model call -> mag.route_chat" is
   aspirational. The door itself works: `memory/runs/route_chat/usage.jsonl`
   shows four failed deepseek smokes (16:44-16:47Z ok:false), a passing v3,
   and a passing nous failover smoke on HERMES_API_KEY_2 at 18:49Z. So the
   real cost of "migrate to the rails" is a port bill: every rail still
   self-calls its own urllib path.

3. The wide-wave fabric lives in the interactive seat, and that is the one
   thing headless would re-lose. Wave 2 of the fifty-wide protocol ran 50/50
   with zero transport failures today (`watch/inbox/burn_claims_50wide_20261003.md:9`)
   but on the main-session retry path and seat tokens: "~1.5M subagent tokens,
   $0 cash (seat tier)" (same receipt line 40) - the exact window meter the
   operator's thesis calls scarce. The Delta Register judge pass lost ~20
   lanes to a mid-turn interrupt before the no-cancel law existed
   (`queue/STANDING_RAILS.md:49-50`); the law (:17-18) is written but not yet
   mechanically proven headless.

4. Headless spend is already material and splintered across at least four
   ledgers, so the migration's economics are unqueryable from one meter.
   Computed this sitting over `memory/runs/hermes_burn/usage.jsonl`:
   2026-10-01 $37.76 / 236 rows, 10-02 $1.17 / 5 rows, 10-03 $25.11 / 911
   rows, total $64.05 (driver.log's standing total reads $63.83). Today's
   rows span anthropic/claude-opus-5.5, sonnet-5.5, haiku-4.5, fable-5.1 and
   z-ai/glm-5.3-prime - the unattended arena pays premium judgment prices
   hourly, while route_chat banks separately, tavern banks into transcripts
   plus hermes_burn, and logs/usage.jsonl (70 MB) is a fifth bank.

5. The composition clause has a consumer after all, and the register is
   behind the talk. Correcting my own first pass: the oro loop IS wired -
   `mag/gwap_to_gps.py` exists (Sep 29) and `tools/gps_mcp/gps_ledger.db3`
   (94 KB) was written today 10:09Z; the arena capability ledger grew to 314
   rows by 19:08:14Z (`memory/runs/gwap/arena-capability.jsonl`), and the
   ZCode dossier claims 266 rows / 178 verdicts (50 VERIFIED_AGREE, 128
   DISPUTE, 88 CHALLENGE) fed across all four funded models at cycle 3. The
   unwired part is finer: tavern DISPUTE rows are structural (no law-referee
   layer) yet feed as agreement fails, per the dossier's own "honest
   refinements owed" - routing dollars off them today mislabels escalation
   as incompetence. Meanwhile the frontier Delta Register on disk holds 14
   rows (`watch/inbox/frontier_delta_register_20261003.json`), not the 39
   judged lanes the raction topic cites - the routing table is behind the
   routing talk.

## WHAT THIS MEANS FOR THE VERDICT (lens input, not verdict)

Stay-vs-migrate is the wrong axis. The dogfood bytes say the estate is
already a headless executor with an interactive staging surface bolted on.
The honest next-primary-surface question is: does the seat's residual work
(staging ask dirs, judging, wide-wave steering, interrupt-with-intent) move
into Hermes-launched headless surfaces (opencode-style) or stay? The port
bill for the headless half is concrete and small (route_chat adoption per
rail, dead-letter rule, one meter), and the plugin spec
(`watch/inbox/mag_rails_plugin_spec_20261003.md:35-47`, "wraps an existing
function, no new model-call logic") is the correct ordering: handles before
doors, doors before migration.

## OWED (not verified this sitting)

- RESOLVED mid-sitting: automation-b1ce1342 is a ZCode-side hourly automation;
  its dossier lives OUTSIDE the repo in the ZCode memories dir
  (`~/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/
  memory/arena-gwap-useful-shit-law-20261003.md`); the in-repo footprint is
  only sibling-lens command rows in `memory/trajectory/steps.jsonl`. Cap-held
  and operator-independent behavior is confirmed by that dossier plus my
  byte census (38 dirs, capability rows hourly, latest 19:08:14Z), not by
  reading the automation itself - I cannot see ZCode's automation config.
- Seat-token meters (9.5M flash arm, ~582K per deliverable): ask-given, no
  in-repo ledger verified.
- Whether the descent driver survives a machine reboot (it survives session
  death; no schtasks autostart for it was found).
- The 39-lane judge census behind the topic's Frontier Delta Study number
  (register on disk: 14 rows).
- The gwap_to_gps verdict counts (266/178) are the dossier's claim; I
  verified the file and db3 exist and the ledger grew to 314 rows, not the
  verdict breakdown itself.
