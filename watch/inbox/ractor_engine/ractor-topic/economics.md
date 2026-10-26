# ECONOMICS LENS - ractor on the estate spend (2026-10-02)

Lens: EV-per-cost pricer. Jacket: hoarding or burning without a banked usage line.
Topic arrived as "undefined"; I priced the estate's live spend as the standing
default. Every number below was computed or read in this sitting, instrument
named, moment 2026-10-02 ~01:45-02:00 EDT, tree live (descent driver cycling).

## Instruments run this sitting

- python over memory/runs/hermes_burn/usage.jsonl (236 rows, all ts 2026-10-01):
  raw sum $37.7591; by model: claude-opus-5.5 85 rows $31.78, claude-sonnet-5.5
  103 rows $4.51, claude-fable-5.1 48 rows $1.47.
- Same file grouped by (id, turn): 24 groups repeat, 165 extra rows, $25.5316.
  Top: A1_steer_antiforgery turn 1 = 49 rows $20.99; DUEL1_hidden_5 = 46 rows
  $0.00 (refusals bank near-zero); N1_parables_songmap = 42 rows $0.00.
- Night subset (ts >= 2026-10-01T21:31:24Z): 43 rows $5.5208, carrying 13
  same-(id,turn) pairs fired seconds apart (e.g. DUEL2_train_09_r2 at
  21:47:10.827Z and 21:47:12.909Z, identical 5944/8000 tokens, $0.0919 each).
  CORRECTION (hostile second pass, re-verified 2026-10-02): the original
  $2.2521 was pair-GROSS (both members of each pair). The race-marginal
  duplicate, members after the first per group, is $1.1292 = 20.45 pct of the
  subset, not 40.8 pct.
- python over memory/runs/model_garden/usage.jsonl: 725 rows $3.4746 (10-01
  $3.13, 10-02 $0.35); models glm-5.3-flash 334, deepseek-chat 151, kimi-k2 121,
  gemma4 27, qwen3.8-max-prime 25, grok-4.7 25. Row keys include base_url and
  channel (pots separable per row).
- Liveness: memory/runs/hermes_burn/DRIVER_STOP does not exist;
  memory/runs/hermes_burn/driver.beat tail reads BEAT 2026-10-02T05:59:36Z
  cycle=557, 06:00:39Z cycle=558. The driver is live.
- git grep "47\.54" over the tracked tree: zero hits. Recursive sweep of
  memory/, queue/, watch/inbox/ (md/json/jsonl) for "47\.54": timestamp
  coincidences only (e.g. "23:36:47.540701").
- Hermetic check of one ask queue: all 28 dirs under
  memory/plans/hermes_burn_duel2 carry 0 revision.md, 0 turn2_only flags,
  0 REFUSED markers (N1R dir likewise bare).

## Finding 1 - the estate's only cost aggregator is blind to both live ledgers

tools/cost_rollup.py:42-45 scans exactly four surfaces (logs/duel/duels.jsonl,
logs/mates/*.jsonl, logs/hermes_gopher_burn_*/..., training/cost_ledger.jsonl).
The descent law's leg 8 banks every paid turn into memory/runs/hermes_burn/
usage.jsonl (memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:54-56) and the
model garden banks into memory/runs/model_garden/usage.jsonl; neither path is
in the rollup's surface list, and no receipt in watch/inbox shows a rollup that
covers them. $41.23 of measured 48h spend lives in ledgers no aggregate
instrument reads; the only per-day totals in receipts are hand-computed
(watch/inbox/NIGHT_CLOSE_20261002.md:50-56, which do reproduce byte-exact -
positive confirm, but hand-computation is the phantom-number disease's front
door; the 191.8M precedent).
Falsifier: cost_rollup gains the two surfaces, or an aggregator receipt exists
that includes them (I did not find one).
Move (45 min): add the two memory/runs ledgers as surfaces (schema adapter
already seams this at tools/cost_rollup.py:115-116), run it, land the receipt.

## Finding 2 - the ledger cannot say bought vs burned, and 67.6 pct of it is burn

Of the hermes ledger's $37.7591, $25.5316 sits in rows that re-fire a turn
already fired (165 extra rows over 24 (id,turn) groups). tools/hermes_burn.py
:24-25 documents the disease ("A1 ... 45x at $20.53 after landing") but the row
schema has no wasted/refire_of marker (measured keys: ts,id,model,turn,tokens,
channel,cost_usd,ok), and the tool itself prints "ledger total" as the raw sum
(tools/hermes_burn.py:388-395). Any consumer of the headline number reports
$37.76 spend of which roughly $12.23 bought a first answer. The commit-message
figure "Ledger ~$42 of 145" inherits the inflation (37.76 + 3.47 = 41.23).
Falsifier: a byte location that already separates bought from theater over this
ledger, or proof the extras are distinct paid asks (they are same id+turn).
Move (30 min): backfill pass marking rows after the first per (id,turn) as
refire (append-only sidecar keeps the ledger append-only), bought/theater split
in the rollup.

## Finding 3 - CORRECTED: three unlocked driver instances; race-marginal duplicate was 20.45 pct

_landed_skip checks output existence at entry (tools/hermes_burn.py:210-218)
but out_path is written only after the 60-900s call returns (:354-361), and
descent_driver.sh re-enters every 45s with no lock and no single-instance
guard (scripts/descent_driver.sh:14-28). ROOT CAUSE (verified in bytes this
sitting, sharper than my original "two executors, identity not pinned"):
memory/runs/hermes_burn/driver.log carries THREE "[driver cycle 1 ...]"
starts - 17:55:00Z (line 1), 19:17:13Z (line 449), 20:40:13Z (line 2094) -
each restart leaving the prior loop running (STOP is only checked per-cycle;
nothing kills the old process). Two full sweeps of the 28 duel2 asks fired the
same _r2 revision turns for money back-to-back (driver.log lines 5326-5350 and
5366-5390; e.g. train_09_r2 $0.09 in both), and the ledger holds the resulting
13 duplicate pairs. HEADLINE CORRECTED: the race-marginal duplicate spend is
$1.1292 = 20.45 pct of the $5.5208 night subset (members after the first per
(id,turn) group, re-summed 2026-10-02); my original $2.2521 / 40.8 pct counted
both members of each pair and over-attributed the legitimate first fire.
Guard_terminal adds no second bank: it banks only the turn=None EMPTY_REASONING
row and returns terminal (mag/inference_budget.py:352-365; the caller at
tools/hermes_burn.py:324-325 raises). The turn2_only re-open door is shut in
bytes but by out-of-band cleanup, not by design: 28/28 duel2 dirs have 0
revision.md; the turn2_only key survives present-but-falsy in 14 ask.json
(train_09_r2: turn2_only=false, revision=null); no stripping code exists in
tools/, scripts/, or mag/ - so any future staged revision reopens it, and the
driver restart that minted the duplicates can happen again any shift.
Falsifier (tightened): the members[1:] resummation fails to reproduce $1.1292
/ 20.45 pct; or driver.log's extra counters never overlap a paid sweep; or a
single-instance guard or per-ask lock already exists in some organ.
Move (50 min, two halves): (a) exclusive lockfile at descent_driver.sh start,
exit if held - kills the restart-recurrence class; (b) os.open(ask_dir/
'.inflight', O_CREAT|O_EXCL) around the API call, removed in finally, plus one
test that a concurrent run_ask skips - makes any future concurrent executor
safe.

## Finding 4 - the banking leg passes, the balance line is ungoverned prose

Positive: where banking exists it is byte-accurate. NIGHT_CLOSE's 43 rows
$5.5208 and 725 rows $3.4746 reproduce exactly from my independent sums.
Cheap-first is real: 605 of 725 model_garden rows are flash/deepseek/kimi;
primes are rare (25 qwen, 25 grok); opus spend concentrates in the descent
asks it was ordered for. The hermes pricing table is pinned in-repo with its
capture provenance (tools/hermes_burn.py:66-71). Ticket redemption economics
are honest: issued 65 / run 48 / 73.8 pct with four promotions NAMED rather
than aged silently (watch/inbox/hermes_burn/TICKET_LEDGER.md:149-161); its one
"not re-verified" item (heartbeat W2-L5, :101-103) verifies now in bytes:
descent_driver.sh:17 writes driver.beat and the tail is live at cycle 558.
Negative: the funded-balance line has no byte home. AGENTS.md carries "$220
armed - audit 2026-09-14" and "$180 Nous credits" (09-28 ladder);
tools/hermes_burn.py:3 carries "spend 70+$"; commit 0c9d72a06 carries "Ledger
~$42 of 145" and "($47.54 live balance)". git grep finds 47.54 nowhere; the
recursive sweep finds it nowhere. Three coexisting armed figures, one
unanchored balance, and the descent rib itself names the failure mode
(RIB_THE_DESCENT_PROTOCOL_20261001.md:60-62: "hitting $70 can corrupt
usefulness ... every dollar leaves an artifact, or it did not happen").
Falsifier: a file deriving armed/balance from ledgers, or a provider-side
credits probe (I ran neither; the sweep covered memory/, queue/, watch/inbox/
plus the full tracked tree via git grep).
Move (60 min): mint memory/runs/spend_balance.json {pot, armed, as_of, spent
per ledger path, balance} written by cost_rollup on every run, and fold the
single figure back into AGENTS.md's money line so the ladder stops carrying
three armed values.

## Blind spots

- No live probe of provider credit balances (Nous/xAI/deepseek): whether any
  prose figure matches reality is OWED to an API check I did not run.
- Per-row price correctness against each provider's price sheet is unverified;
  only the hermes table is pinned in-repo (comment claims a 10-01 live probe).
- CORRECTED per the hostile second pass: my original night-subset headline
  ($2.2521 / 40.8 pct) was pair-gross and over-attributed ~2x; the
  race-marginal truth is $1.1292 / 20.45 pct, and I originally failed to
  identify the second executor - the driver.log read this sitting (three
  cycle-1 starts at 17:55:00Z, 19:17:13Z, 20:40:13Z) closes that gap.
- model_garden: counts, sums, and schema checked; not each provider's math.
- Free-lane "$0 metered" claims (NIGHT_CLOSE) accepted as claims, not verified.
- Topic was "undefined"; a narrower intended topic was not visible to me.

---

# ECONOMICS LENS, SECOND SITTING - ractor-topic (2026-10-06, evening EDT)

Seat: economics, same jacket (hoarding or burning without a banked usage
line). Topic again "undefined"; I priced the estate's money and token
metabolism over 2026-10-04/06. Every number below was computed or read this
sitting: python censuses over usage.jsonl and cost_ledger.jsonl, grep counts
over driver.log, ls byte checks, git log reads. The 2026-10-02 section above
is preserved untouched; its falsifiers are scored below. No em-dashes.

## Instruments run this sitting

- python over memory/runs/hermes_burn/usage.jsonl: 3010 rows, $94.6085 total,
  first 2026-10-01T13:11:41Z, LAST 2026-10-05T07:12:43Z. By model:
  opus-5.5 $59.83 (1247 rows), sonnet-5.5 $12.21, fable-5.1 $18.30, haiku
  $2.64, glm-5.3-prime $1.64 (7 rows). By day: 10-01 $37.76, 10-02 $1.17,
  10-03 $25.62, 10-04 $26.29, 10-05 $3.76.
- Same file by ask prefix: TAVERN $41.97 (opus $16.24, fable $16.28, sonnet
  $7.04, haiku $2.40), dnd0+DND0 $2.40, A1 $21.85 (all opus-5.5), DUEL2
  $2.43. TAVERN ids are NPC debate rounds with a JUDGE
  ("TAVERN_tavern_20261005T071101Z_r8_Maud Ashgrove"); my grep -rln tavern
  over mag/ lands on mag/game_dm.py, mag/game_brawl.py and kin.
- grep -c over memory/runs/hermes_burn/driver.log: 779 "HTTPError 402:
  'Payment Required'" (first at line 398335, all on MOCAP_BUILD_spec), 5150
  "HERMES-BURN: PASS - 28/28 asks" lines riding all-skip batches, 1260 FAIL
  MOCAP lines of which 936 are EVIDENCE-PREFLIGHT closes.
- ls: watch/inbox/replay_deepseek_thinking/MOCAP_BUILD_spec.md is 0 bytes,
  mtime Oct 4 18:22. memory/plans/hermes_burn_playground_20261003/
  MOCAP_BUILD_spec/ holds only ask.json (no REFUSED, no TERMINAL, no output).
- head/tail of memory/runs/hermes_burn/driver.beat: BEAT 2026-10-01T21:31:24Z
  cycle=1 through BEAT 2026-10-05T23:35:30Z cycle=3569. Commit d5f89d97b
  (10-06 09:58 EDT) says "Driver closed".
- python over memory/training/cost_ledger.jsonl: 2478 rows, schema
  cost_ledger.v1, live through 2026-10-06T04:34:42Z; grep -c dwfrun = 0.
- grep -in token over watch/inbox/frontier_olm_2026-10-05/RECEIPT.md: no
  hits (it counts 32 sweeps, 239 items, 23 confirmations, 8 steal cards).
- grep for 402, credit, usage, hermes over state/NIGHT_LOOP_20261005.md:
  zero hits.
- Scored the 10-02 falsifiers: tools/cost_rollup.py has zero grep hits for
  memory/runs, hermes_burn, model_garden; memory/runs/spend_balance.json
  does not exist (my ls).

## Finding 1 - the Oct 2 cure was skipped, and four days later the wall arrived; both funded premium rails are dead and the dawn page prices only one

The 10-02 section's Finding 1 named cost_rollup.py's blindness to
memory/runs/hermes_burn/usage.jsonl and its Finding 4 named the ungoverned
balance ("Three coexisting armed figures, one unanchored balance"; falsifier:
"a provider-side credits probe (I ran neither)"). This sitting scores both
falsifiers UNMET four days later: cost_rollup.py still scans neither ledger,
spend_balance.json still does not exist. In that window $56.85 more burned
through the unaggregated ledger ($37.76 to $94.61), the driver hit 779
"Payment Required" 402s on MOCAP_BUILD_spec, the last banked row landed
2026-10-05T07:12:43Z, the beat file went quiet at 2026-10-05T23:35:30Z, and
commit d5f89d97b closed the driver. The xAI rail died the same day
(DAWN_REPORT_20261006.md:79-83, "X reply radar exit 1 at 10-05 08:00
(402/timeout class, logs/x_radar.log)"). The driving ladder makes primes or
grok-4.7 the DEFAULT judgment rung (AGENTS.md); both rails are dead and the
operator's one dawn page carries an xAI reissue item and no hermes item (my
grep for 402/credit/usage/hermes over state/NIGHT_LOOP_20261005.md: zero
hits). The 402's cause (account exhaustion vs per-model paywall) is OWED:
probing needs the console or one live paid call, outside this sitting. The
10-01 order funded "70+$ hermes credits" (tools/hermes_burn.py:4-5) and
$94.61 banked, so exhaustion is plausible, not proven.
Falsifier: a usage.jsonl row after 2026-10-05T07:12:43Z, or a receipt naming
a hermes balance probe or refill, or spend_balance.json existing at a path I
did not check.
Move (10 min): append a hermes row beside dawn item 4: balance probe, then
reload-or-formal-stop. And land the 10-02 spend_balance.json move; it is now
overdue by one billing wall.

## Finding 2 - the driver's last ~40 hours were zero-paid-output noise, and the terminal-marker law does not cover the failure classes that killed the lane

5150 all-skip "PASS - 28/28 asks" batch lines and 1260 MOCAP failures in
driver.log against 3569 beats. The 936 EVIDENCE-PREFLIGHT closes fire on a
0-byte evidence file authored Oct 4 18:22; the ask dir holds only ask.json,
so the REFUSED-IS-TERMINAL law (tools/hermes_burn.py:310-317, refusal-class
markers only) never minted anything: transport and preflight failures raise
per-ask exceptions (tools/hermes_burn.py:433) that nothing makes terminal,
so the overmind loop re-fired the same broken ask every beat for two days.
The summary grammar compounds it: tools/hermes_burn.py:442 prints PASS and
exits 0 whenever the exception counter stays zero, and skipped rows (:431)
count as OK, so "PASS - 28/28" printed 5150 times where the truth was "0
paid work". The MOCAP contract itself is good work (ask.json read this
sitting: an opus-5.5 nuance pass with a real evidence list and a falsifier
section); it died of authoring (empty evidence file), then of billing (402),
then of no stop line.
Falsifier: a REFUSED or TERMINAL marker in the MOCAP ask dir, or a driver
beat after 2026-10-05T23:35Z carrying a non-skip cost>0 row.
Move (15 min): one edit in tools/hermes_burn.py: mint <ask>/TERMINAL on
EVIDENCE-PREFLIGHT and on two consecutive transport failures per ask id, and
make the :442 summary print paid/skipped/failed separately.

## Finding 3 - the window's largest token spends are the only ones no estate ledger carries (CONVERGENT with r5_land_truth.md and with the 10-02 section's rollup blindness)

Commit d5f89d97b's message claims "DAY-5 MINE FOLDED (164.5M tokens, largest
single run)". The mine's own receipt
(watch/inbox/frontier_olm_2026-10-05/RECEIPT.md) bills itself as
"every number below was measured or counted by a command run in this ask"
and carries zero token totals (my grep). The orchestrator cost ledger
(memory/training/cost_ledger.jsonl) holds 0 dwfrun rows (my grep -c); the
hermes usage ledger ended 07:12:43Z, before the mine fired (commit
356c90634, 10-05 10:09 EDT). watch/inbox/ouroboros_20261005/
r5_land_truth.md:105-108 already banked the same species for the executor's
60M headline ("remains unbanked as bytes anywhere"), after the dawn report
had to strike it (DAWN_REPORT:28-30, "commit-message-carried only, with no
byte source"). Three phantom token headlines in five days: 191.8M struck
(citation-lint founding fixture), 60M struck, 164.5M minted in a commit
message. The descent protocol's leg 8 (every turn banks tokens+cost,
AGENTS.md) has a carrier only on the hermes_burn path. Honest scoping: my
ListWorkflowRuns call returned workflow_introspection_unavailable (same
capability gap the r5 relay economics lens banked), so this claim is scoped
to estate disk; harness-private run accounting is OWED to whoever holds
introspection.
Falsifier: any estate byte source (ledger row, receipt line) carrying 164.5M
or the executor's 60M.
Move (20 min): teach the dwf receipt template a tokens+cost footer (leg-8
shape), or strike the 164.5M claim from NIGHT_LOOP-sourced restatements
until a row exists.

## Finding 4 - 47 percent of the window's funded spend bought one workstream, and no per-workstream EV row exists to steer the refill

My census: TAVERN $41.97 plus dnd0/DND0 $2.40 = about $44.4 of $94.61
(47 percent) on the game-tavern line, with $32.52 of it on the two most
expensive models (opus-5.5 and fable-5.1). Judgment work shows as A1 $21.85
(all opus-5.5) and $1.64 lifetime on glm-5.3-prime, the funded workhorse,
over 7 rows. Framing kept honest: the game corpus is a real product line and
every row is banked per the driving-ladder law, so this is not waste proven;
the finding is that the 10-01 order's stated purpose was "inject logic into
our squeakiest joints" (tools/hermes_burn.py:4-5) and the credits went 47
percent to one workstream with no per-line EV row anywhere I checked
(usage.jsonl ids, DAWN_REPORT, NIGHT_LOOP, the 10-02 section). Whether the
tavern judge hardened anything the estate reuses is exactly the row that
does not exist, and the refill decision now pending has no data to ride.
OWED: a row-level contract audit of what TAVERN bought; I priced the mix,
not its output.
Falsifier: a per-workstream spend or EV table in a file I did not check.
Move (15 min): append a spend-by-workstream census (game line vs estate
machinery vs research asks) to the dawn report's economics amendment.

## Finding 5 - retirement without status rows is the estate's recurring spend leak, proven in three organs this week (CONVERGENT with dawn item 5)

One defect class, three organs. (a) Hermes asks: MOCAP re-failed 1260 beats
with no terminal marker (Finding 2). (b) Fleet scripts: DAWN_REPORT:84-90
banks "tree-doctrine-dig collected a gate certificate two days after its
death verdict"; state/CURRENT.md:49-50 carries "stop-cert armed but UNLOADED
(zero registry status rows minted)". (c) The driver itself: 3569 beats, 5150
of them all-skip PASS beats after the paid lane died, stopped only when the
window closed it. In each case a verdict exists and the status row that makes
the verdict bite does not, so compute keeps flowing to retired things. The
dawn report already prices (b) for the operator's pen; the shared class is
named here so one cure covers all three: a verdict is not a retirement until
a status row exists in the organ that owns the spend.
Falsifier: a registry status row for any retired fleet script, or a TERMINAL
marker on MOCAP, or a driver beat that stops itself on terminal state.
Move (10 min): when the operator signs dawn item 5, mint the stop-cert rows
in the same sitting; the Finding 2 edit is the same cure on the hermes organ.

## Blind spots (honest)

- Provider-side balances unread: the 402 cause and the xAI balance are OWED.
  This is the same blind spot the 10-02 section declared, unfilled.
- Harness run accounting unreachable (ListWorkflowRuns =
  workflow_introspection_unavailable, my call): mine and executor token
  totals could exist harness-side; Finding 3 is scoped to estate disk.
- Free-lane fleet row quality ungraded by me: the 387-row ledger and 5/7
  provider health are carried from
  watch/inbox/ractor_engine/2026-10-06-ouroboros-r5-relay/economics.md
  Finding 4, not re-audited.
- No test suite or census re-run; all test counts carried from receipts.
- Seat-account token spend of workflow sessions is invisible from disk.
- TAVERN output quality unjudged (Finding 4 prices the mix, not the merit).
- I checked exactly four surfaces for the missing hermes dawn item
  (DAWN_REPORT, NIGHT_LOOP, r5 relay economics.md, and the 10-02 section);
  a fifth surface naming it would falsify the "not priced" clause.
- cost_rollup's four named surfaces (per the 10-02 section's :42-45 read)
  were re-checked only by grep for the three ledger paths; I did not re-read
  the full surface list this sitting.

---

# THIRD SITTING - hostile-pass corrections to Findings 1 and 2 (2026-10-06, late)

The second-pass audit verdicted Findings 1 and 2 WEAKENED. Every byte below
was re-run or re-read this sitting; the corrected state supersedes the
second-sitting text above for these two findings only. Findings 3, 4, 5 were
not verdicted and stand as banked.

## Finding 1, corrected: the rail re-armed mid-sitting and the OWED cause is answered; what survives is the ungoverned balance, the prose-class xAI attribution, and the still-absent dawn item

Both of my falsifiers fired post-sitting. My python census now reads 3012
rows / $94.6422; the two new rows are H247_A2_TOKEN_CUE_FAMILY_TABLE and
H247_A3_QUEEN_WELD_MAP_DRAFT, haiku-4.5, ok=true, at 2026-10-06T23:55:08Z
and 23:55:27Z. A fifth surface now exists:
watch/inbox/HERMES_247_WIRED_20261006.md (mtime 2026-10-06 19:58:33 EDT, my
ls), which names my dark window ("Last pre-wiring fire: 2026-10-05T07:12Z
(~32h dark)", :9), gives the meter context ("$94.64 spent of the $180 meter
by ledger sum; API-side meter is the balance truth", :29), and answers the
OWED cause: key 2 no longer covers premium SKUs, so the rung 402s are a
per-model paywall, not account exhaustion (:21) - corroborated by the 402ing
ask being opus-5.5 (memory/plans/hermes_burn_playground_20261003/
MOCAP_BUILD_spec/ask.json:3, my sed read) against paid haiku rows on the
same rail. My "absent from every canon surface" and "dawn page prices only
xAI" clauses were true at my moment and are withdrawn as of now. The reload
leg of my move is landed: my cmd //c "schtasks /Query /TN
MagHermesBurn247 /FO LIST" returns TaskName \MagHermesBurn247, Status Ready,
Next Run Time 10/6/2026 10:00 PM. The receipt also names the better root
cause for the 40h banked-line gap: "NO scheduled task existed ... when a
window closed, the staging stopped. The carrier and the law existed; the
clock never did" (:9) - the 402 was the separate per-SKU wall.

Surviving clauses, re-checked this sitting: (a) memory/runs/spend_balance.json
still does not exist (my ls: NO_SPEND_BALANCE) - the 10-02 sitting's move is
now twice-owed, across one billing incident; (b) the dawn page still carries
no hermes item (my grep -i hermes over DAWN_REPORT_20261006.md: zero hits);
(c) the "xAI 402/403" attribution I carried from DAWN_REPORT:79-83 is prose,
not bytes: my grep -c "402\|403" over logs/x_radar.log returns 0, and the
log's own tail names "no JSON block in grok output" and "END exit=1" - the
xAI rail's real cause is unproven and its balance unprobed; (d) the premium
rung is still down: only haiku pays today, and premium needs an operator
top-up on key 2 (or premium credits on key 1) or a carrier amendment adding
per-ask cross-key failover (:21). Instrument defect corrected: the 779 count
was run with grep -c "Payment Required"; the longer pattern I banked
("HTTPError 402: 'Payment Required'") is the log's repr spelling, not the
pattern I ran.
Falsifier (tightened): spend_balance.json appearing at any path; or a hermes
row added to DAWN_REPORT_20261006.md; or a premium-SKU (opus/sonnet/fable)
usage row after 2026-10-06T23:55Z accompanied by an operator top-up receipt.
Each kills one surviving clause, not the finding.
Move (15 min): land spend_balance.json through cost_rollup (twice-owed),
append the hermes row to the dawn page, and correct the xAI parenthetical at
DAWN_REPORT:79-83 to the byte-named cause or mark it prose.

## Finding 2, corrected: rescaled 6.5x down and redirected at a live instance - the hourly 24/7 clock re-fires a 402 that can never self-heal

My headline numbers were wrong; corrected by my own re-runs this sitting.
The 1260 FAIL MOCAP lines decompose as 467 EVIDENCE-PREFLIGHT + 779
HTTPError-402 + 13 TimeoutError + 1 other (my four grep -c runs; 936 was
the all-ask preflight count, which I wrongly attributed to MOCAP alone).
The preflight re-fire ended before the paid era did: last preflight failure
at driver.log line 397014, last paid line "OK THE_MERGE_spec cost=$0.72" at
about line 397027 (my sed read) - the empty-evidence disease was cured by
queue composition while the 0-byte file itself remains on disk (0 bytes,
mtime Oct 4 18:22, my first-sitting ls). The zero-paid-output stretch is
792 all-skip "PASS - 28/28" beats after driver.log line 397125 (my awk |
grep -c), with zero paid-cost lines after that line under a pattern that
includes $0.72-class amounts (my awk | grep -cE 'cost=\$0\.0*[1-9]|
cost=\$[1-9]' = 0). So "the driver's last ~40 hours were zero-paid-output
noise" is withdrawn: the paid era rode 4358 of the 5150 PASS lines, and the
true zero-output stretch is the post-wall ~20 hours, 792 beats.

What survives, and now points at a live target: the terminal-marker gap.
The critique's reads hold (refusals count only usage rows with a refused
field; transport exceptions print FAIL and write no row; skips print OK;
PASS exits 0). My own read this sitting closes the loop:
_refusal_state (tools/hermes_burn.py:189-205) counts only usage.jsonl rows
with a refused field; the sole refused-field write is at :375 on the
refusal-content path; _call raises on HTTPError at :138 writing nothing.
Therefore HERMES_247_WIRED_20261006.md:21's self-heal claim ("A1 will 402
twice more then mint REFUSED and stop burning tries") is code-false for the
402 class: no refused row is ever written, the count stays 0, and the
marker never mints. The live instance: queue/hermes_247/A1_mira_lane_
forecaster (sonnet-5.5) failed the first hourly fire (logs/
hermes_burn_247.log: "HERMES-BURN: FAIL - 2/3 asks; ledger total $94.64",
exit 1 at 2026-10-06T23:54:15Z; A2 and A3 paid, their rows are the two new
usage rows). The hourly clock re-fires A1 into a permanent 402 with no
terminal state, and the designed alert leg (receipt :15, :22) appends an
attention.md alert row per failing fire - observed once, hourly recurrence
projected not yet observed. (My grep -c "Payment Required" over the 247 log
returned 0, but that log is UTF-16LE per receipt F4, so ASCII greps cannot
read it; the 402 fact rests on the receipt's :21, not that grep.)
Falsifier (tightened): a REFUSED marker minting in queue/hermes_247/
A1_mira_lane_forecaster/ on 402-class failures alone (no refused-field row
in usage.jsonl); or a carrier code change writing refused-field rows on
transport errors; or the hourly fires stopping of their own accord.
Move (15 min): the same hermes_burn.py edit, now load-bearing on a running
clock: write a refused-field row (or a terminal marker) on transport-class
HTTPError before re-raise, so _refusal_state can see 402s and the hourly
fire can go terminal; until then, pull A1 from queue/hermes_247/ or amend
the receipt's :21 self-heal clause to match the code.
