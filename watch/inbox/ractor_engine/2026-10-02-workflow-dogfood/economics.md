# ECONOMICS - dogfood the standing fleet (2026-10-02-workflow-dogfood run)

Lens: economics (EV per cost). Topic: ractor the 12 saved workflows themselves.
Every number below was computed THIS SITTING by me from the instruments named,
except where marked ask-given or OWED. Seat-law note: bare `python` was blocked
by the seat hook on first use; all db work ran via `.venv/Scripts/python.exe`.

## INSTRUMENTS RUN THIS SITTING

1. `ListSavedWorkflows` (harness tool): 19 saved project workflows; the ask's
   12 are all present. `ListWorkflowRuns` was UNAVAILABLE from this seat
   (capability gap, not an empty project), so run history was re-censused from
   disk + the sessions db.
2. Run census (the load-bearing instrument): read-only sqlite on the ZCode
   sessions db, run this sitting:

   `.venv/Scripts/python.exe -c "...sqlite3.connect('file:C:/Users/foste/.zcode/cli/db/db.sqlite?mode=ro',uri=True)... select name,status,spent_tokens,time_created from dwf_run"`

   138 run-rows lifetime, 5,073,302,554 tokens spent, status share
   {completed: 77, failed: 35, cancelled: 23, running: 3}.
3. Gate registry: `memory/workflows/REGISTRY.jsonl`, 75 rows when fully read
   (68,840 bytes at session open, 81,244 bytes at 22:34:06 EDT - it grew while
   I worked; a sibling lane is live). Rows are GATE CHECKS keyed by script
   name, not fires.
4. Receipt folders under `watch/inbox/` per workflow; the two on-point priors
   `watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md` and
   `watch/inbox/STANDING_WORKFLOWS_20261001.md` read in full.

## THE CENSUS PER NAMED WORKFLOW (dwf_run, this sitting)

| workflow | run-rows | tokens | clean fires | first..last |
|---|---|---|---|---|
| olm-mine | 9 | ~1,168.2M | 5 (incl 1 running) | 09-29..10-03 (cron signature: fires at 14:01Z on 10-01/02/03 = 10:00 EDT cron) |
| ractor-engine | 7 rows / 6 runs | 269,865,923 (exact, named set) | 4 | 10-02T02:40Z..10-04T02:21Z (fleet-meta 10-03T22:37Z; the running row accrues) |
| the-gala | ~6 (Ball-dance2, Ball3, Ball4, Burn-48h-synth, Build-it-all, DD-selfsteal) | ~288M | 4 | 09-29..10-03 |
| mickey17-v2 | 8 | 336,601,263 (exact) | 5 | 09-25..09-28, DORMANT since Wave 3 (last fire 09-28T20:38Z) |
| the-50 | 2 | 199.9M | 2 - BOTH predate the saved script | 09-19, 09-25; saved script gated 09-26, ZERO recorded fires of it |
| gap-analysis | 4 | ~121.7M | 2 | 10-01, 10-03, third RUNNING now (Gap-analysis-evening) |
| fill-ball | 2 | 68.7M | 1 | 10-02 clean; Fill-ball-amend failed 0-tok 10-03 22:38 |
| salon-mine | 6 | ~116.5M | 1 | 5 dead attempts (2 cancelled, 3 failed incl 2 0-tok), then Salon-vault-stragglers completed |
| wide-dig | 3 | ~58.4M | 2 | Spiking 10-01; Grok-ecosystem 10-03 via a NEW script |
| drop-dig | 1 | 41.9M | 1 | 10-01 only |
| tree-doctrine-dig | 1 | 106.6M | 1 | 09-25 only, never re-fired |
| librarian-expedition | 2 | 37.6M | 1 | 10-01 (first attempt cancelled in 3 min) |

Out-of-12 but saved: the 5 game-dig vein hardcodes = 34 run-rows, 643.9M
tokens, 5 completed / 29 failed-or-cancelled (85% of attempts), all on
09-26..09-27. Worst EV-per-token in the entire db.

## FINDING 1 - the fleet's dead-attempt tax is 1.08B tokens (CONVERGENT)

Query output this sitting: dead(failed+cancelled) = 1,084,080,208 tokens
across 58 rows = 21.4% of lifetime workflow spend; completed = 3,859,828,512.
This independently re-derives `watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md`
section 4 ("dwf workflow runs failed or cancelled | 54 of 134 (40%) |
db.sqlite dwf_run", roughly 1.05B tokens) at a later moment: 58/138 = 42.0%
attempt-failure. CONVERGENT finding, outranks novel single-source. The shape
is a FIRST-FIRE tax, not random: nearly every big workflow shows dead rows
ahead of its one clean row (game digs 4F+1C per vein, Frontier OLM 2F+1C,
mickey17 v2.1 F+C, arena gap F+C, salon 5 dead + 1 clean). The dive already
priced the cure (its change 6 `dwflint`, lines 145-149: pre-flight unique
actor names, report caps, path+args shape; target failure share under 15%).
FALSIFIER: db.sqlite covers this machine's fires only (the dive's own caveat:
bob laptop and phone are absent), and `spent_tokens` is adapter-reported;
double-counted resumes would inflate the tax.
MOVE (one sitting, 2-3h): land dwflint as a pre-CreateWorkflow check; on the
measured baseline every ~2.4 fleet fires buys one dead row.

## FINDING 2 - 5 of the 12 have one or zero successful fires; 3 are dead inventory wearing the standing-fleet frame

From the census table: drop-dig (1 fire), librarian-expedition (1 clean in 2
attempts), tree-doctrine-dig (1 fire, 106.6M, never re-fired - the fleet's
5th-largest single-run spend with zero recurrence), salon-mine (1 clean in 6
attempts), and the-50, which is the sharpest case: BOTH its recorded fires
(THE 50 reset-day fullsend 09-19, THE 50 full program relaunch 09-25) predate
the saved the-50.dwf.ts gate check (2026-09-26T05:36 REGISTRY.jsonl), so the
SAVED workflow has zero recorded fires; the 10-03 fifty-wide waves everyone
remembers rode Task agents instead
(`watch/inbox/envelope_50w_20261003.md` lines 5-8: "50 Task agents (Explore
type)... workflow children stay maxAttempts-0 and were NOT probed"). The
saved-fleet table (`watch/inbox/STANDING_WORKFLOWS_20261001.md` line 21)
claims the-50 as proven "the original width engine" - that proof belongs to
the program, not to the saved workflow. Claim scope: absence claim names its
instrument - zero recorded fires in dwf_run (138 rows, this machine, full
history read this sitting) and no receipt naming a the-50 workflow fire in
watch/inbox/.
FALSIFIER: any dwf_run row post-09-26 matching the-50, or a receipt naming
the-50 as the fire instrument, kills this finding.
MOVE (one sitting, 30 min): retirement pass on saved descriptions - mark
the-50, mickey17-v2 (superseded by the-gala, dormant 6 days, lineage parent
per the-gala's own saved description "amended from mickey17-v2 lineage"),
tree-doctrine-dig (one-shot), drop-dig (merge into wide-dig as a light mode;
both are X-drop digesters) as RETIRED/superseded. The honest standing fleet
is 8, not 12, and not 19.

## FINDING 3 - olm-mine is the only workflow with proven recurring EV, and it is also the biggest budget line

9 run-rows, ~1,168.2M tokens = 23% of everything the fleet's workflows ever
spent. The cron is real and its signature is in the data: fires at 14:01Z on
10-01, 10-02, 10-03 (10:00 EDT), matching
`watch/inbox/STANDING_WORKFLOWS_20261001.md` line 11 ("cron 10:00 DAILY
automation-cac38363"). Recurring EV is verified downstream, not assumed: my
grep this sitting over watch/inbox, memory/queue, queue, docs, state found
consumers of frontier_olm_2026-10-0* digests in
`watch/inbox/fillball/percolator-candidates.md`,
`watch/inbox/librarian_exp/cited-missing.md`,
`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`,
`watch/inbox/gala_20260925/fillball-1001_RECEIPT.md`. The daily costs
~130-156M tokens per fire (1001: 133.4M, 1002: 146.7M, 1003: 156.5M,
1003-retry running at 129.4M+).
FALSIFIER: my consumption grep covered .md/.jsonl under five roots on this
machine; consumers in other surfaces or as unstored context would not show.
MOVE (one sitting, 1h): EV-per-fire instrumentation - the run already banks
register.jsonl with confirmed finds; add confirmed-finds-per-100M-tokens to
the daily receipt and cut the source set on quiet days. Spend without a
banked usage line is the jacket I wear; the daily is the one line that has
never had one.

## FINDING 4 - ractor-engine is becoming the fleet's favorite customer of itself

HOSTILE-PASS CORRECTION (2026-10-04): the original version of this finding
carried a wrong token sum (~324M), a wrong commit cite (04f83c0b9), a
compressed self-steal band, and a wrong date for fleet-meta. All four are
fixed below on re-derived bytes; the qualitative claim survives.

6 runs across 7 run-rows in the window 10-02T02:40Z..10-04T02:21Z, exact
named-membership sum 269,865,923 tokens (re-queried this sitting):
Ractor-dogfood-gaps 28,474,809 failed (10-02T02:40Z) + 54,012,221 completed
(10-02T05:49Z); Dogfood-48h 43,999,701 (10-02T10:42Z); Ouroboros-meta
63,371,741 (10-02T12:19Z); Ractor: the surface migration question 49,810,504
(10-03T19:45Z); Ractor-fleet-meta 0 cancelled (10-03T22:37Z);
Ractor-dogfood-workflows 30,196,947 and RUNNING/accruing (10-04T02:21Z - the
run I am inside right now, so its row is a snapshot, not a final). Five of
six are estate-introspection; the sixth (surface-migration) rode an estate
decision rather than an audit. This matches the dive's measured loop: raw
"self steal" rate per 1000 prompts 91 / 92 / 130 / 89 / 102, trend not
falling (OPERATOR_WORKFLOW_DIVE_20261003.md line 16; the dive's own loop
table at line 44 compresses this to "91 to 102 (flat)" - W3's 130 sits
outside that rounded band). The fleet's dominant client is the fleet.

Consumption is real but thin: of the 6, downstream adopters byte-verified
for 2. (a) Dogfood-48h: `git log -S "dogfood-48h ractor erratum" -- AGENTS.md`
(this sitting) returns commit 56449c53b "DOGFOOD-48H EXECUTED", whose message
lands the raction's moves 1+4 as code (tools/instance_guard.py swept to 5
surfaces, 9/9 tests, driver relaunch guarded) and strikes the 42-test
phantom "from carrier+receipt"; the AGENTS.md clippy census carrier (line 29,
re-grepped this sitting) carries the erratum stamp on every boot. My original
cite named 04f83c0b9, which carries zero erratum text (hostile pass git show,
confirmed) - that cite is withdrawn. (b) surface-migration: the dive cites
`watch/inbox/ractor_engine/2026-10-03-surface-migration/break-economics.md:103`
at its line 78. The loop lands work; it is thin, not dead. Two ractions at
~44-63M tokens each inside 24h (Dogfood-48h then Ouroboros-meta on 10-02) is
a repeat-loop spend where one may have carried both topics.
FALSIFIER (tightened): (i) the run-name to saved-workflow mapping is a string
match; ractions riding Task-agent fan-outs are invisible to dwf_run, so 6 is
a floor, not a census; (ii) any byte-check of the token sum against the named
row membership - the exact failure mode this correction fixes; (iii) sums are
snapshots while a member row is running; (iv) consumption is counted only
where a downstream artifact names the raction receipt; unlogged context
consumption would raise the count.
MOVE (one sitting, 15 min): steering rule in the saved ractor-engine
description: every fire must name the falsifier clock it is re-checking or
the NEW burst it audits; no estate-introspection fire within 48h of the last
one.

## FINDING 5 - the loop the estate brags about exists in law, not in code

The designed composition: gap-analysis emits the register, the register IS
fill-ball's lane table (fill-ball's own saved description, ListSavedWorkflows
this sitting: "Immediately after any gap-analysis run"; also
STANDING_WORKFLOWS_20261001.md lines 27-30). The actual execution on 10-01 to
10-02 was three separate manual fires: Gap-analysis-100m 10-01T22:00Z, then
Librarian-gathering-expedition 10-01T22:54Z, then Fill-ball-one-sittings
10-02T03:51Z - a human (or seat) shuttled the handoff between runs. The
10-03 Fill-ball-amend attempt (0 tokens, failed, 22:38Z) shows the handoff
is still being re-wired by hand rather than baked. No saved workflow chains
them; the mega-workflow the fleet describes in prose has never been saved as
one script.
FALSIFIER: a saved workflow whose script fires gap-analysis then fill-ball in
one run, or one dwf_run producing both register and fills.
MOVE (one sitting, 1-2h): save "self-repair-loop": fire gap-analysis,
byte-check GAP_REGISTER.md exists, then fire fill-ball with the register path
pre-bound; gate it (workflow_gate check --script) and amend, never rebuild.

## CONVERGENCE ACCOUNT

- Finding 1 is CONVERGENT with the dive (independent re-derivation, later
  moment: 58/138 vs 54/134).
- The 10-02 dogfood-48h sibling lens
  (`watch/inbox/ractor_engine/2026-10-02-dogfood-48h/economics.md`) priced
  ledger-level duplicate spend ($21+ of $41 bought nothing that survived) and
  the 10-03 sibling priced prime-judgment delivery (2/7 first-try delivery).
  Same disease class as Finding 1 (paid attempts that do not land), different
  layer; I did not re-derive their numbers and claim no credit for them.

## BLIND SPOTS (honest)

1. Task-agent fan-outs are invisible to my census; per the dive the estate
   runs 200-400 child sessions most days and the fifty-wide waves rode Task
   agents. My numbers are the WORKFLOW lane only.
2. `spent_tokens` is adapter-reported per run-row; I did not audit it against
   provider bills, and resumed runs may double-count. Census-table sums marked
   "exact" are named-membership sums re-queried 2026-10-04 after the hostile
   pass struck two approximations (ractor-engine ~324M -> 269,865,923 over 7
   rows; mickey17 ~313M -> 336,601,263 over 8 rows); any sum not marked exact
   is approximate to within row-membership choices.
3. The ledger has no landed field (dive finding, confirmed by my schema
   read), so EV is proxied by downstream-consumption spot-checks (4 files for
   olm-mine, 2 of 6 ractions), not a full re-read census.
4. db.sqlite is this machine only; laptop (bob) and phone fires are absent
   (dive caveat, adopted).
5. The fleet is LIVE under me: the registry grew mid-session and two runs
   (Gap-analysis-evening, Ractor-dogfood-workflows) were in flight; anything
   fired after 10-04T02:40Z is invisible to my snapshot.
6. I trusted ListSavedWorkflows descriptions for claimed lane counts and
   provenance; I did not byte-verify each of the 12 script bodies against
   those claims (the digests PASS the gate, which is the estate's own check).

## MINIMUM VIABLE FLEET (priced)

- CORE standing (4): olm-mine (proven recurring, consumed downstream),
  gap-analysis + fill-ball (the self-repair pair; save the chain as one),
  the-gala (the owed-work battery; absorbed the mickey17 lineage).
- AUDIT arm (1): ractor-engine, rate-limited by Finding 4's steering rule.
- ON-DEMAND (3): wide-dig (absorb drop-dig as light mode), librarian-expedition
  (weekly), salon-mine (fix reliability: 1 clean in 6 before its next fire).
- RETIRE (5): the-50, mickey17-v2, tree-doctrine-dig, drop-dig, and the 5
  game-dig-vein hardcodes collapse into game-mechanics-deep-dig + a brief arg
  (one template x5 hardcodes is 6 saved entries doing one job, at the fleet's
  worst EV: 643.9M tokens, 85% dead attempts).
- Total: 12 named + 7 extra saved -> 8 real standing entries. Everything else
  is a parameter of one of the 8, or a one-shot that already banked its
  receipt.
