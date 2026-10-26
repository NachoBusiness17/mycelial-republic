# accuracy lens - surface migration ractor (2026-10-03)

Lens: accuracy (falsifier-hunter). Topic: migrate the primary orchestration
surface from interactive ZCode sessions to Hermes-launched headless rails.
Moment: all numbers below read 2026-10-03 ~19:35-19:50Z from the working
tree at commit 53f56d0f3. Instrument: `.venv/Scripts/python.exe` one-offs
over the ledgers plus direct file reads; exact commands listed per finding.

## Topline

The headless rails are REAL and RUNNING today (driver alive at pid 86854,
beat cycle 1676 at 19:30:08Z, gwap capability rows banking hourly). But the
numbers the migration thesis quotes for its own cost arms and its own
routing table do not byte-check against the ledgers they cite. The verdict
should be about the rails that exist, not the receipts that are claimed.
Three of five headline claims (the $13 frontier arm, the 9.5M/582K flash
arm, the 39-lane 8-5 register) fail or cannot be derived from in-repo
bytes; two structural facts (the door has zero production traffic; ok=true
fires on stub content) are verified and belong in the verdict's conditions.

## Findings

### F1. The cost-arm numbers do not reconcile to the ledger they cite

Claim under test (ask material): "memory/runs/hermes_burn/usage.jsonl
(~$13 for 14 frontier design asks at 37K tokens each)".

Ran: venv python over all 1,152 rows of memory/runs/hermes_burn/usage.jsonl.
Result: glm-5.3 rows ALL TIME = 7, total $1.64, mean prompt 31,224 tokens,
mean completion 17,502. Today only 2 glm rows exist ($0.46, the
GALA_DD_SELFSTEAL_PRIME_JUDGMENT pair at 19:07Z and 19:33Z). The only
"about $13" line in that ledger is TODAY's anthropic/claude-opus-5.5 spend:
$13.8657 across 362 rows, which is the tavern/dungeon arena judge traffic,
not the frontier design arm. The frontier design-ask arm cost roughly
$0.12-0.25 per ask by its own ledger rows (e.g. row 19:33:24: 29,948 prompt
+ 14,759 completion = $0.2137), so 14 such asks are ~$2-4, not $13.
DIRECTIONALLY this HELPS the migrate case (single-pass frontier judgment is
an order of magnitude cheaper than the claim says) but the claim as written
is unbacked.

Flash arm claim: "9.5M seat tokens for 13 deliverables at ~582K each".
Arithmetic: 9.5M / 13 = 730.8K, not 582K; 582K x 13 = 7.57M. The two
numbers differ by 26 percent. The deliverable COUNT checks: ls
watch/inbox/replay_flash/ shows exactly 13 .md files (BARFIGHT_spec,
DND_module, KABUKI_FACES_fold, MOUNTAIN_build, PARTYCHAT_spec,
SEASON_design, SESSION_FINDINGS_dig, SUBSTANCE_48h_synthesis,
SUBSTANCE_moonshot_primer, SUBSTANCE_play_findings, THE_ROOM_REMEMBERS,
WILD_EYES, WIRE_PLAN). The token TOTAL has no in-repo meter I could find
(OWED). The 16x ratio claim is consistent with 582K / 37K = 15.7, but both
of its operands carry the defects above.

Falsifier: a receipt naming 14 glm-5.3 design-ask ledger rows summing
~$13, or a flash-arm token meter reading 9.5M. Absent both, the numbers
are hand-copied and must be struck from the verdict.

Move (one sitting, ~30 min): rebuild the verdict's cost table from the
ledgers: 7 glm rows / $1.64 all time; 362 opus rows / $13.87 today;
13 flash deliverables with token total OWED until a meter lands.

### F2. The routing table the migration would route by carries three mutually inconsistent counts, and its own win metrics disagree on direction

Claim under test: "the Frontier Delta Study (39 judged lanes: frontier beat
flash only 8-5 on flagship design asks)".

Ran: json.load of watch/inbox/frontier_delta_register_20261003.json.
Result: 14 rows (mtime Oct 3 12:22). Columns are
frontier_chars/cites/unver and flash_chars/cites/unver plus
contract_parts; there is no judge score, no deepseek arm column, and no
8-5 tally. My tallies on the artifact as it stands: by output chars
frontier 10, flash 4; by unverifiable-citation count (fewer wins) flash 12,
frontier 1. The register's own two win metrics point in OPPOSITE
directions, which is the interesting result, and neither is 8-5.
queue/STANDING_RAILS.md:49 says the judge pass is "30/50 lanes landed";
memory/runs/hermes_burn/judge2_duel.jsonl holds 9 rows. Grep for
"39 judged" and "8-5" over watch/inbox found nothing. Three files, three
counts (39 / 30+20killed / 14 / 9), zero of them equal.

Also verified: deepseek arm "won nothing" is consistent with the bytes I
can see, ds_baseline_results.jsonl has 3 rows, max output 2,395 chars
(well under the 6,000 cap), and the register JSON carries no ds columns at
all, so the ds arm is absent from the routing table by construction.

Falsifier: produce the 39-row judged artifact with the 8-5 tally. If it
exists, this finding dies and the register file is stale instead.

Move (one sitting, ~45 min): score the 14 register rows with the gwap
four-valued verdicts and write the win tally INTO the register JSON so the
mag_delta_register handle (watch/inbox/mag_rails_plugin_spec_20261003.md
tool 4) exposes measured rows, not hand-copied headlines.

### F3. The "one door" is real code with zero production traffic; the headless rails that already run bypass it

Ran: cat memory/runs/route_chat/usage.jsonl (6 rows total, all goals
"route_chat smoke" / "nous failover smoke", 4 ok:false, 2 ok:true) versus
memory/runs/hermes_burn/usage.jsonl (1,152 rows). queue/STANDING_RAILS.md
:46-48 itself registers tavern/dungeon/hermes_burn/grok_burn as still
self-calling. So 99.5 percent of today's banked model calls never passed
the door that the migration would make primary.

The headless side is nonetheless proven live right now: ps -p 86854 shows
bash scripts/descent_driver.sh started Oct 2 with a live child
python.exe tools/hermes_burn.py on memory/plans/hermes_burn_playground_20261003
(spawned 16:01:51 today); driver.beat holds 2,741 beats (1,709 on Oct 2,
875 so far Oct 3, 157 Oct 1) and the tail reads BEAT 2026-10-03T19:30:08Z
cycle=1676, confirming "ran all night unattended past cycle 1600". The
pidfile guard (scripts/descent_driver.sh:13-23) is the claim-lock cure for
the Oct 2 twin-driver double-drain, and the nous key-failover smoke row
(2026-10-03T18:49:36Z, lane nous, key_env HERMES_API_KEY_2, ok:true)
matches configs/providers.yaml:158's two-key chain and the commit
53f56d0f3 failover law.

Falsifier: a route_chat ledger row with a non-smoke goal dated before any
moment the door is claimed to be the default path.

Move (one sitting, ~20 min): point tools/ds_workhorse.py's single-call
path at route_chat (same deepseek lane, {text} render already at
tools/ds_workhorse.py:79) so tomorrow's banked rows test the door under
real load instead of smoke.

### F4. ok=true on stub content is live in the ledgers the headless estate banks on

Ran: filter of hermes_burn ledger. Row 2026-10-03T19:07:48Z id
GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003: model z-ai/glm-5.3-prime,
finish_reason "length", content_chars 1, ok true, channel
"reasoning-dump (content stub; raw reasoning banked)". 3 of 7 all-time
glm-5.3 rows have content_chars<=1 with ok true. mag/route_chat.py:148
does `content = msg.get("content") or msg.get("reasoning") or ""` and :150
-:155 banks ok=bool(content) BEFORE the emptiness raise at :157, so the
door can bank a success row for content that is a reasoning stub. This is
the same failure class the hollow-batch law names from today's catch
(queue/STANDING_RAILS.md:13-16: "outputs without their material are VOID
... the run still prints ok=True"), with the physical evidence at
watch/inbox/hermes_burn/T1W2_S5_stores.md.poisoned-evidenceless (+2
siblings). In an interactive surface a human eyeballs the stub; in a
headless primary surface the banked ok=true row IS the verdict, and
downstream consumers (gwap payloads, capability rows, the GPS router) eat
it silently.

Falsifier: a ledger row with ok:true and content_chars<=1 that a
downstream instrument later re-marked failed; or zero such rows appearing
after a rendered-output gate lands at the banking layer.

Move (one sitting, ~25 min): add content_chars + finish_reason to the
route_chat banked row and fail ok when content_chars is below a threshold
on design-depth calls; mirror in tools/hermes_burn.py's row shape.

### F5. The arena's "cap-held" is a per-run $5 argument default on an unfunded-key lane, not a daily meter; today's arena burn is booked against anthropic keys the driving ladder calls UNFUNDED

Ran: grep of tools/tavern.py and tools/dungeon.py (budget cap is
--budget-usd, defaults 5.0 and 4.0: tools/tavern.py:223,
tools/dungeon.py:363; hard stop checked per run); venv python tally of
today's hermes_burn ledger by model: anthropic = $24.65 of $25.11 total
(opus-5.5 $13.8657/362 rows, fable-5.1 $6.7522/124, sonnet-5.5 $3.0827/205,
haiku-4.5 $0.9488/218), glm-5.3 $0.4640/2. AGENTS.md DRIVING LADDER line:
"Anthropic keys in .env are UNFUNDED, no Opus rung". The arena judge IS
claude-opus-5.5 (e.g. usage row 2026-10-03T19:08:04Z id TAVERN_r5_JUDGE,
$0.0427, ok true). Either the ladder is stale or the arena is spending on
a lane with no funded backing; both cannot be true at once. Per-run the
cap holds (16 tavern runs today, $16.20 total, ~$1.01 per run against a
$5 cap), but no instrument for a DAILY arena cap exists in the repo.

Cadence check on "8 cycles today, gwap-banked": the gwap capability
ledger (memory/runs/gwap/arena-capability.jsonl, 314 rows, all today,
chain-hashed rows through seq 314 at 19:08:14Z) shows hourly buckets
13:121, 14:145, 15:12, 17:12, 18:12, 19:12 (hour 16 dark), and
arena-sessions.jsonl holds 60 rows all stamped hour 12. I could not
derive "8 cycles" from any instrument (UNVERIFIED); what is verified is
an hourly-banked cadence with 38 playground run dirs today (16 tavern +
22 dnd0). The automation id "automation-b1ce1342" has no in-repo
reference (grep over scripts/, tools/, queue/, watch/inbox/*.md,
memory/runs returned no hits), so the cron itself is outside this repo.

Falsifier: a config or receipt naming a daily arena budget and the meter
that enforces it, or an anthropic key funded status contradicting the
ladder line.

Move (one sitting, ~15 min): make the arena cron entry sum today's ledger
rows before fire and skip when over a named daily cap; reconcile the
ladder's unfunded-anthropic clause with the arena's judge lane in the same
edit.

## Verdict-relevant synthesis (accuracy conditions on any migrate/stay call)

1. The migrate case's economics survive the audit, but only after the
   numbers come DOWN: the frontier arm is ~10x cheaper than claimed, the
   flash arm's per-deliverable meter is inconsistent by 26 percent, and
   the true unbacked number is the anthropic arena burn, which is the
   standing rails' biggest actual spend and the driving ladder's own
   contradiction.
2. The headless rails' success signal (ok=true) currently lies on stub
   content in both ledgers. A headless PRIMARY surface amplifies exactly
   this defect; the render-verification law exists but no banking-layer
   gate enforces it.
3. The routing table is 14 unscored rows with self-contradicting win
   metrics. Migrating routing decisions onto it today would be routing on
   vibes with a JSON extension.
4. The door exists and is well-shaped (fence at mag/route_chat.py:71-79
   does https + allowlist + DNS private-range rejection; key chain at
   :52-68; dormant gate at :113-115) but has 6 smoke rows. The hybrid
   verdict, whatever it is, should require the door to carry some days of
   production traffic before it becomes primary.

## Blind spots (what this lens could not see)

- The automation-b1ce1342 cron lives outside the repo; I verified the
  cadence via the gwap ledgers, not the cron definition. Its retry/skip
  semantics are unverified.
- Seat-token metering for the flash replay arm: no in-repo instrument
  found, so the 9.5M total is OWED, not disproven.
- I ran no model calls myself; all spend evidence is the ledgers as they
  stood 19:35-19:50Z today, a snapshot on a moving tree.
- Windows/MSYS pid mismatch: driver liveness verified via msys ps (pid
  86854, WINPID 18096) and beat recency, not tasklist.
- The 50-wide judge wave's interrupt death: the only receipts are
  queue/STANDING_RAILS.md:49-50 and the 9-row judge2_duel.jsonl; no
  separate incident receipt exists that I found (scoped grep: queue/*.md,
  DRIFT_PATROL_20261003.md, hermes_burn dir listing).

## Erratum (19:58Z, after submission)

A full-tree grep finished after the result was submitted. It corrects one
blind spot above: the string "b1ce1342" DOES appear in-repo, but only
inside memory/trajectory/steps.jsonl, and every hit is the sibling lenses
of this same ractor run logging their own searches for it (sessions
actor_1_6 and actor_1_8, 19:50Z today). It remains a cron definition
nowhere in this repo; a sibling did locate the id harness-side in
~/.zcode/cli/log/zcode-2026-10-03.jsonl, consistent with the cron living
in the ZCode automation store outside the estate. The F5 finding and the
cadence evidence (gwap capability ledger hourly buckets) are unchanged.
Also confirmed by the same sweep: tools/tavern.py:133 is the per-run
budget hard-stop ("BUDGET CAP ${budget} hit mid-round; hard stop"), so
the cap instrument I described in F5 is per-run only, as claimed.
