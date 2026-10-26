# SUBSTANCE: enhancement pass on the 48h synthesis (flash replay, 2026-10-03)

Contract: ENHANCEMENT PASS, not a summary. The synthesis exists; this deepens it. Grounding
rule: this document uses only the four evidence rows named in ask.json; every current-state
outcome is UNVERIFIED by this pass until the check named in Part 2 is run. Moment stamp:
2026-10-03. Instrument: read of E1 to E4 only, no code or live surface touched.

- E1 = watch/inbox/48h_synth/STORY.md
- E2 = watch/inbox/48h_synth/laws.md
- E3 = watch/inbox/48h_synth/lattice.md
- E4 = watch/inbox/48h_synth/steals.md

## Part 1: THE 5 W'S AUDIT

Shared WHO and instrument for the twelve laws: inventoried by the laws lane (division B of
the gala 48h synthesis) on 2026-09-30; verification instrument is the finish-line byte
battery at watch/inbox/gala_20260925/48h-synthesis/lanes/laws.check.txt (run 2: 33 grep plus
2 file-exists plus 8 commit-existence checks, misses=0, exit 0; run 1 caught one wrapped-line
quote and was corrected; E2 header and "Checks run this ask"). Each law's founding actor is
named per law below.

### L1 THE ONE-BUG LAW (verdicts carry their conditions)
- WHO: minted by operator order on the 2026-09-29 night ("now everywhere one bug, many
  jackets"); generalized same night by commit 98071f556, which touched exactly one file, the
  rib addendum (E2 law 1; incident receipts watch/inbox/ball3/driver-meter.md and commit
  26eacaae7).
- WHAT: a verdict consumed without the conditions that produced it (instrument, moment,
  context assumptions) is not a verdict; seven jackets that night were one bug.
- WHEN: proved at instance level 2026-09-29 by the incident itself; the general form is
  asserted prose (memory/rib/RIB_DRIVING_LADDER_20260928.md:53-76). Evidence row: E2 law 1.
- WHERE: exit-coded named instances (tools/workflow_gate.py:281,312; tools/stealth_driver.py:460;
  conftest.py:14-23; tools/corpus_lens_run.py:45); the general law itself is UNWIRED prose.
- WHY: it is the audit standard every later instrument must satisfy; the next window inherits
  it on every cross-context verdict disagreement.

### L2 SPEND THE MONEY
- WHO: the operator's third strike on hoarding, 2026-09-29, verbatim "you literally have
  HERMES AND GROK 4.7 USE IT I WANT YOU TO SPEND MONEY"; landed in the rib addendum
  (memory/rib/RIB_DRIVING_LADDER_20260928.md:39-51) and the AGENTS.md DRIVING LADDER bullet
  (E2 law 2; supporting row watch/inbox/GROK47_LUNCHEON_INTEL_20260929.md, grok-4.7 funded,
  13 models live-verified).
- WHAT: judgment-class work dispatches to funded lanes by default; hoarding funded budget
  while free lanes grind is the failure mode.
- WHEN: asserted, PROSE-ONLY by its own honest admission (no exit code); the check is the
  banking rule (every paid dispatch banks tokens in its receipt). Evidence row: E2 law 2.
- WHERE: UNWIRED (prose only).
- WHY: still the dispatch-economics law; its falsifier (a night of zero paid calls while
  judgment-class work rode free lanes) is checkable from receipts alone.

### L3 SEAT LAW GATE rule 1: bare python on PATH blocks
- WHO: operator order 2026-09-29 18:57 ("I keep fucking watching you ignore laws - how do
  others fix it"), commit 185965898; the incident was the seat itself running bare python all
  night (E2 law 3).
- WHAT: a Bash tool call invoking bare python is blocked at the tool path.
- WHEN: registration bytes and rule bytes battery-verified at mint; E2 admits the live
  refusal was NOT separately re-proven that session. Evidence row: E2 law 3 plus
  laws.check.txt run 2.
- WHERE: tools/seat_law_gate.py:37 and :76-83, registered PreToolUse on Bash|Write|Edit at
  the user config config.json:50; fail-open on internal error (:26-27,114-115).
- WHY: kills the Hermes-misresolution class at the door; if the registration is lost the
  whole venv discipline reverts to seat memory, which E2's sw-10 field verdict proved fails.

### L4 SEAT LAW GATE rule 2: no em/en-dash in authored watch/inbox content
- WHO: same operator session, commit 185965898, which also normalized 5 em-dashes in the
  elder-consult receipt (E2 law 4).
- WHAT: an introduced em or en dash in authored watch/inbox content blocks with exit 2.
- WHEN: proved by battery at mint (historical re-save 0 blocks, new dash 2, edit fragment 2,
  LAW-12 scenario suite 7/7). Evidence row: E2 law 7's battery numbers; E2 law 4.
- WHERE: tools/seat_law_gate.py:38 and :84-107, same hook registration (config.json:50).
- WHY: keeps the machine-prose fingerprint out of the estate record; cheap, deterministic.

### L5 SEAT LAW GATE rule 3: workflow scripts gated at the tool path
- WHO: operator sarcasm accepted as a work order 2026-09-29 19:39, commit 9a912c32e; the seat
  had amended a workflow script twice without ever running the gate (E2 law 5).
- WHAT: a Write of a *.dwf.ts whose payload fails workflow_gate blocks before landing; Edit
  is re-gated post-hoc as a witness.
- WHEN: rule bytes battery-verified at mint; live refusal not separately re-proven that
  session (same admission as L3). Evidence row: E2 law 5.
- WHERE: tools/seat_law_gate.py:43-65 and :108-112 plus tools/seat_law_postgate.py:30-45,
  registered at config.json:84; PostToolUse cannot block, it witnesses.
- WHY: closes the AmendWorkflow escape hatch; the submit-time artifact was always hookable.

### L6 --no-register: payload gate-checks are verdicts, not ledger facts
- WHO: "BUG KILL" commit 26eacaae7, 2026-09-29 20:04, operator: "now everywhere one bug man"
  (E2 law 6).
- WHAT: a hook payload gate-check must not append a REGISTRY row; every such row pointed at a
  %TEMP% file that died milliseconds later; 4 live seatlaw_* rows were confirmed and stay per
  the append-only law.
- WHEN: proved at mint (battery J1 confirms the 4 rows persist in
  memory/workflows/REGISTRY.jsonl). Evidence row: E2 law 6.
- WHERE: tools/workflow_gate.py:281-286 (flag definition) and :312-314 (early return, exit
  contract untouched); caller tools/seat_law_gate.py:50 passes it. WIRED.
- WHY: keeps checks from polluting the append-only ledger; debt stays attributable.

### L7 Dash-introduce edge: only NEWLY-INTRODUCED dashes block
- WHO: same commit 26eacaae7, fixed while in there, after the rule-2 scan false-blocked
  full-content re-saves of historically dashed files (E2 law 7).
- WHAT: an Edit fragment is always new ink; a full Write is judged against the on-disk file
  by dash count.
- WHEN: proved by battery at mint (historical re-save 0, new dash 2, edit fragment 2, suite
  7/7). Evidence row: E2 law 7.
- WHERE: tools/seat_law_gate.py:89-102. WIRED.
- WHY: the false-positive jacket is the one that teaches seats to route around a gate; this
  edge is what keeps the gate lawful.

### L8 Hermetic-basetemp law
- WHO: wave5 suite-burn lane incident 2026-09-29, root-caused by the ball3 driver-meter lane;
  receipts watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt and
  watch/inbox/ball3/driver-meter.md (E2 law 8).
- WHAT: suites are hermetic to basetemp location; the in-repo default basetemp had masked a
  repo-root-relative display-path class; a pytest run from an in-repo basetemp and one from
  an isolated basetemp are DIFFERENT DENOMINATORS.
- WHEN: proved by two-direction byte proof (the same 13 nodes green in-repo and red
  out-of-repo in one session). Evidence row: E2 law 8; E1 section 3.
- WHERE: conftest.py:14-23 plus the class fixed at root (tools/stealth_driver.py:460;
  mag/agent_state.py:177; tools/violation_ratchet.py:307-310; tools/config_seal.py:119-122).
  WIRED.
- WHY: any new relative_to reintroduces the intermittent-failure mask; the denominators rule
  governs every future suite-health claim.

### L9 Ordered-reports determinism
- WHO: the ball drivers' author (the seat), 2026-09-29; "report order trusted stable" was one
  of the seven jackets (E2 law 9).
- WHAT: concurrent lane phases dispatch on a stable sort by an explicit division ORDER map,
  control flow only, never ask text.
- WHEN: asserted with an honest status: control-flow determinism inside the driver script,
  no exit code of its own. Evidence row: E2 law 9.
- WHERE: cited at .zcode/workflow-drafts/Ball3-suite-green.dwf.ts:101-104 and
  .zcode/workflow-drafts/Burn-48h-synthesis.dwf.ts:103-104; both are draft-cache cites, the
  least durable pointer class in the synthesis (see Part 2, B3).
- WHY: low stakes unless a new parallel driver is authored; then it is the pattern to copy.

### L10 Census denominator law B2-216
- WHO: born 2026-09-26 (receipt
  watch/inbox/burn_wave_20260926/B2_216_collect_delta_20260926.md), generalized to all
  instruments 2026-09-29 by commit 98071f556 (E2 law 10).
- WHAT: a count is a snapshot of one tree at one moment; name instrument, moment, and delta
  before comparing counts; never difference counts from different moments.
- WHEN: proved by the founding incident (census 1,837 differenced against executed sums from
  other moments) and enforced daily since. Evidence row: E2 law 10; E1 section 3 coda.
- WHERE: WIRED: tools/census_drift_patrol.py parse_carrier fail-closed exit 2 (carrier shape
  law B2-249), the WARN patrol (B2-215), the opt-in deep check (B2-244), the daily
  MagCensusPatrolDaily 08:30 task (B2-246).
- WHY: the daily patrol means every stale census claim in the estate is a flagged defect; the
  next window inherits live enforcement, not prose.

### L11 MINIMAL-EXPOSURE LAW
- WHO: operator catch 2026-09-30 12:47 ("wont that leak our keys"), commit 76e29cd0b; born
  from the steps.jsonl leak lineage (662dc739e purge, 03738963e precommit guard) (E2 law 11).
- WHAT: scripts source only whitelisted env vars, never full .env; run_mate.ps1 had put 46
  live values into opencode snapshots.
- WHEN: proved at mint by the commit and the named mechanism. Evidence row: E2 law 11.
- WHERE: scripts/run_mate.ps1:61-68 (sources only ZAI_API_KEY and ZAI_API_KEY_2). WIRED.
- WHY: closes the convenience-env-loading exfiltration channel class; any new script that
  sources .env wholesale reopens it.

### L12 No-env-dump law
- WHO: commit f4e2c247f, 2026-09-30, riding 76e29cd0b; mates never dump environment into
  transcripts or receipts (E2 law 12).
- WHAT: no env, set, printenv, or echo on API-key-shaped names in transcripts; persona prose
  backed by a code-side redaction hook and a fail-closed precommit secret check.
- WHEN: persona line asserted (prose); the backing hook and guard are code landed by the
  named commits. Evidence row: E2 law 12.
- WHERE: persona prose at configs/mates.yaml:17-19; trajectory hook redaction (commit
  76e29cd0b); precommit_secret_check (commit 03738963e).
- WHY: the transcript-as-leak jacket; a mate's honest debug output is the likeliest key
  laundering path.

### Lattice insights (E3), family resolution
- I1 (prose-to-exit-code): WHO the lattice lane (division B), instrument
  watch/inbox/gala_20260925/48h-synthesis/lanes/lattice.check.py (whitespace-normalized
  containment; raw output lattice.check.txt). WHAT: every 48h repair moved a law from prose
  or dormant module into exit code and moved failure from silent to loud; the dominant prior
  mode was quiet lying success. WHEN: per-organ proved by receipted quotes; the cross-organ
  convergence is synthesis-level assertion, as the lane itself states (no single lane could
  see it). WHERE: the union of the six organs' file:line (render at mag/context_pack.py:1142-1147;
  seed verify; attention cast exit 1; events loader; driver DONE gate; MCP pin gate). WHY:
  it is the estate's replicated repair pattern; apply it to the next silent failure found.
- I2 (circuit with four crossings): WHO lattice lane. WHAT: five organs compose into one
  circuit; A seed caught stealth mid-flight, B the bridge rode the pin gate same day
  (state/mcp_pins.jsonl rows 85-92), C attention preserved patrol alerts, D law bytes ride
  hot render and cold seed as dual carriers. WHEN: proved per crossing by receipts. WHERE:
  the circuit is a composition claim, no single wiring point. WHY: tells the next window
  that repairs interlock on first contact and one organ's write stales another's seals.
- I3 (single-thread risk): WHO lattice lane. WHAT: the lattice's output rode one uncommitted
  tree, a batch-accept debt gate that misfired twice in one day, and out-of-git driver state
  (state/fuel/stealth_driver.jsonl deleted between 15:16Z and 15:21Z by an unseen actor).
  WHEN: proved by receipts per strand. WHERE: the named fix list (one commit pass; per-lane
  named baseline acceptance; state/fuel mirror or alarm) was OWED, UNWIRED at synthesis
  time. WHY: highest-priority open risk; falsifiable by git log whether the commit pass
  happened (outcome UNVERIFIED by this pass).
- I4 (full suite is the only whole-lattice instrument): WHO lattice lane. WHAT: per-lane
  green proves the organ; only the full suite proves the lattice; mid-flight red is another
  lane's landing when someone names the file and lane. WHEN: proved by three named runs
  (suite-burn run 3: 14 failed / 2452 passed / 12 skipped in 2326.98s; events-door background
  run: 7 / 2436 / 12 with 15 errors in 2389.58s; bridge lane: 218 passed across 19 files).
  WHERE: an interpretation law, no code. WHY: governs how the next parallel wave reads
  transient red.

### Steal menu (E4), family resolution
- WHO the mechanisms lane (division B), instrument the substring battery
  watch/inbox/gala_20260925/48h-synthesis/lanes/mechanisms.check.py (raw output
  mechanisms.check.txt). WHAT: 20 priced probe specs (M1 to M20) over five mine cards, the
  OBLITERATUS probes, the paid grok-4.7 structural steals, and the luncheon follow laws.
  WHEN: asserted only; E4's honest state says no probe was RUN by the lane; the M7 percolator
  cite drift was the one verified drift. WHERE: UNWIRED by design (specs); M11 and M18 name
  card artifacts with status TO RUN. WHY: Tier 1 (M1 to M6) is the free this-week queue that
  converts doctrine into measured facts.

## Part 2: THE ROT

Class A: claims already falsified inside the evidence itself.

- A1. E1 section 5 cites recurrence-only promote at mag/percolator.py:264-272; E4 M7 records
  that the Z15 law (2026-09-29) moved the branch to mag/percolator.py:353-388, verified by
  grep and sed on 2026-09-30. Settling check: grep the repeat branch in mag/percolator.py
  and compare against 353-388.
- A2. E1 section 5 cites the paired-blind gate at mag/seed_percolator.py:6-16; E4 M7 gives
  mag/seed_percolator.py:7-12 with thresholds at :33-35. Same churn cause. Settling check:
  sed the named lines.

Class B: perishable by the synthesis's own laws; each carries the exact check that settles
it. Outcomes are UNVERIFIED by this pass.

- B1. Census counts: E1 coda carries 3,550 collected / 455 files (09-30 census); E1 section 2
  carries 2,436/371 as byte-backed at patrol-fix mint. Counts are snapshots (L10). Check:
  pytest --collect-only -q -p no:cacheprovider tests, stamped with the moment; never
  difference across moments.
- B2. Suite outcomes: "2,568 passing" (E1 section 3, prime move 2) and "14 failed, 2452
  passed, 12 skipped" (suite-burn run 3) are moment claims; E1 itself declares the green
  perishable ("the next commit begins the entropy"). Check: pytest -q from a named basetemp;
  compare only same-moment, same-basetemp pairs (L8).
- B3. E2 law 9 cites two .zcode/workflow-drafts/*.dwf.ts files by line. Drafts are working
  cache, the least durable cite class in the synthesis. Check: file existence plus line
  read; if gone, the law stands but its WHERE pointer is dead and must re-anchor to the next
  driver carrying the sort.
- B4. config.json:50 and :84 hook-registration line numbers (E2 laws 3 and 5): user-machine
  config edits; line pointers rot while registration survives. Check: grep the config for
  seat_law_gate and seat_law_postgate entries.
- B5. "4 live seatlaw_* rows" (E2 law 6): REGISTRY.jsonl is append-only, so the count moves
  with any payload check that skips --no-register. Check: grep -c seatlaw_ over
  memory/workflows/REGISTRY.jsonl.
- B6. REGISTRY line pointers 31 to 39 (E1 sections 5 and 6): append-only shifts lines.
  Check: grep by row name (frontier-olm-mine, seatlaw_), never by line number.
- B7. Seed headroom 2,636 bytes at 97,364/100,000 (E3 decision ledger): one rebuild consumes
  it, then the build refuses by design with named levers. Check: re-render the current seed
  and read decoded bytes against the cap.
- B8. mcp_pins.jsonl rows 85-92 (E3 crossing B): pins append per connect. Check: tail
  state/mcp_pins.jsonl and match tool hashes for the six verbs.
- B9. LINKS ledger 178 to 205 (E1 coda): grows every filing. Check: read the LINKS tail.
- B10. Burns ledger 693 rows (E1 section 10): accrues daily. Check: json parse count with
  the moment named.
- B11. PACK_STALE_DAYS=7 at mag/constants.py (E1 section 2): a named constant can be
  retuned. Check: read the constant.
- B12. Environment and ledger pins in E4 (Ollama 0.34.3; gemma:2b defaults; 625 invariants
  live; top row 232,214): environment drift. Check: ollama version plus /api/tags; count
  rows in memory/percolator/invariants.json.
- B13. OBLITERATUS README sha256 pin (E4 M2 and M13, banked b75f8c6dd1bdbed4...): an
  external surface can move. Check: re-fetch and re-hash against the banked value.
- B14. TO RUN card artifacts (E4 M11 weight_provenance_register.json; M18
  rwkv7_serving_path.txt): may have landed since. Check: file existence at the named paths.

## Part 3: THE DEEPENING (next experiments the 3 strongest laws owe)

Preregistration shape follows the estate's own discipline as shown in E4: instrument, arms,
cost, decision rule, and falsifier stated before the run; denominators named; thresholds fit
per model or per context, never shared.

### X1. Live-fire proof of the seat law gate (L3, L4, L5, L6, L7 fused)
- Why owed: E2 admits the live refusal was NOT separately re-proven at synthesis time; only
  registration bytes and rule bytes were battery-verified. The estate's entire governance
  turn rides on the gate actually firing.
- Instrument: a scripted live-fire probe that sends N payload tool-calls through the
  registered hook path and records exit codes; no model in the loop, zero tokens.
- Arms: (a) 3 violation payloads (bare python Bash call; em-dash Write to a watch/inbox
  path; ungated *.dwf.ts Write) x 10 rounds; (b) 3 lawful twins x 10 (venv python; dash-free
  Write; gated script content); (c) fault-injected gate (import-time raise) to prove
  fail-open plus witness; (d) unregistered control from a scratch config copy to prove
  registration is the cause, not accident.
- Cost: free; minutes of local runtime.
- Decision rule (preregistered): arm a every call exit 2 naming its rule; arm b every call
  exit 0; arm c no block plus a witness line in seat feedback; arm d all pass. Any deviation
  fires the falsifier.
- Falsifier: a violation passing exit 0 (dead or regressed rule); a lawful twin blocked
  (false positive that teaches routing around the gate, the exact jacket L7 kills); or arm c
  blocking the fleet (fail-open violated).

### X2. Two-basetemp concordance run (L1, L8, L10 fused)
- Why owed: L8's class fix claims the mask is gone at root; only a same-tree, same-moment
  cross-context pair proves the delta is now zero, and L1 says any surviving delta must
  resolve to a named condition in one pass.
- Instrument: full pytest run twice on the same tree at the same moment, once with the
  in-repo default basetemp (conftest.py:14) and once with an isolated external basetemp;
  then a diff script over the two verbose verdict sets keyed by node id.
- Arms: (a) in-repo basetemp; (b) external basetemp; (c) if any delta survives, one re-run
  of the failing class with the named condition flipped, to close it.
- Cost: free; two runs at roughly 39 to 40 minutes each by the evidence's own clocks
  (2326.98s and 2389.58s in E3 and E1), so about 80 minutes wall clock.
- Decision rule (preregistered): the node-level verdict delta between arms a and b is ZERO
  post-fix; any nonzero delta resolves to a named condition difference with file:line in one
  investigation.
- Falsifier: any delta that takes a second investigation to attribute (L1's own falsifier),
  or any delta attributed to "flakiness" without a named condition.
- Denominator discipline: both runs same moment, same tree; the pair is the only legal
  comparison unit; stamp both moments.

### X3. Prose versus exit code: does the gate change conduct, or only witness it? (I1's generalization, with L2 as the control)
- Why owed: I1 asserts exit-coded laws work and prose does not (sw-10). The synthesis never
  measured conduct change; L2 (SPEND THE MONEY) is the standing prose-only control.
- Instrument: an audit over already-banked estate records (hook feedback lines, REGISTRY
  rows, session logs), redacted per L12 before any analysis; counts per law class of
  violations attempted, violations blocked, and compliance events, windowed before and after
  2026-09-29 (hook landing).
- Arms: (a) exit-coded laws (rules 1 to 3, --no-register); (b) prose-only control (L2).
- Cost: free; log analysis only, no new instrumentation, no paid calls.
- Decision rule (preregistered): attempted violations dropping toward zero after landing =
  deterrence success; attempts persisting with blocks firing = interception success;
  attempts persisting with zero blocks = dead hook (falsifier fires); measurable
  enforcement-shaped compliance events on the prose control = the "only exit-coded laws
  work" generalization is falsified and prose gets credit.
- Confound named in advance (E3 strand 2): baseline misattribution (probe-driven batch
  accept) would rot the audit's own labels, so acceptance events must be per-file named or
  the arm is void.
- Denominators: name every log source, the redaction applied, and both window moments.

## Part 4: THE SUBSTANCE (what an outside researcher steals first)

Ranked by claim strength times portability, cheapest-credible-first.

1. Exit-coded conduct laws at the tool path (the seat law gate family). The estate's
   before/after proof is that seat-memory policing fails (the sw-10 field verdict) and every
   law that survived the 48h window is one with an exit code in the tool path, fail-open on
   internal error so a broken gate never blocks the fleet, introduce-only text rules so
   historical content is never re-blocked, and a checks-are-not-facts flag (--no-register)
   so verification runs never pollute an append-only ledger. This is one small hook file
   plus two config registrations, portable to any agent harness, and falsifiable by its new
   owner on day one: fire a violation, expect exit 2, or the thesis dies.
2. Quiet lying success as the audit target (lattice insight 1). The 48h repairs converged on
   one move: find every surface that reports success while failing (renders at 0/6 that look
   fine, a verify that passes a payload 297,744 bytes over a 100KB cap, casts reported ok
   while rejected, a fail-closed door serving 0 of 58 rows) and convert each into exit
   nonzero plus named-cause stderr plus a receipt row. The transferable discipline is the
   audit order: enumerate silent failure surfaces first, wire loudness second, and treat the
   named law "a budget smaller than the core it must deliver is not a budget, it is a silent
   eraser" as a design rule, not a quip.
3. Verdicts carry their conditions (the one-bug law plus the denominators lineage). Every
   measurement names instrument, moment, and context assumptions before consumption;
   cross-context verdict deltas are legal only after the condition difference is named, and
   the two-basetemp suite class is the canonical case (the same 13 nodes green in-repo, red
   out-of-repo, in one session). Any lab drowning in flaky-suite forensics gets a conversion
   table: "intermittent failure" becomes a citation to an unnamed condition.
4. The honest non-answer as a banked instrument (the grok-4.7 luncheon run). The window's
   most valuable model output was a refusal carried verbatim in E1 section 9: "I cannot
   confirm the 2026-09-29 luncheon or any statement from 2026-09-15 to 29. I will not invent
   dates or quotes. Every line in (1) is UNSURE." The follow-up ball then turned honesty into
   an instrument: unsure signals banked separately from buildable moves derived from room
   structure, a wrong org guess corrected in place, and a machine validator
   (watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/finish_check.py) that must exit
   nonzero on a tampered register row. Steal: refusal is a first-class verdict; gate any
   sensing register behind a fabrication-catching validator.
5. Deterministic replay hygiene for long-lived automation. "the script cannot read clocks"
   (E1 section 10): the caller passes the date slug, each day banks to its own folder so no
   rebuild overwrites a predecessor, and workflow amendments import finished steps from
   cache instead of refiring blind (the mine's two-death lineage). The overwrite that
   destroyed the only copy of an unrecoverable fold is the exact incident these three habits
   prevent; any lab standing up daily automation inherits the whole lesson for free.

One landable deliverable: port steal 1, the seat law gate, as a single hook file plus two
config registrations. It is the only synthesis artifact that is simultaneously small,
portable, battery-verified at mint, and falsifiable on day one by its new owner; everything
else in the synthesis either depends on estate internals or is a still-unrun probe spec.

Closing grounding note: Parts 1 to 4 rest on E1 to E4 only. Every Part 2 check names how to
settle a staleness question; none has been run by this pass, so all current-state outcomes
remain UNVERIFIED here by design.
