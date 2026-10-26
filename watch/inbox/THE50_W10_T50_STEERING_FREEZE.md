# THE50 W10 T50 · THE STEERING FREEZE DOCUMENT (G25)

Filed 2026-09-19 · W10 THEORY · task 50 of THE 50 · class: RECEIPT
Parent program: `watch/inbox/THE_50_PROGRAM_20260918.md:75` ("50. The steering freeze document (G25) [LANE]")
G25 source row: `memory/runs/gps_50/GPS_PACK.md:232` (the battery named the missing part: a collision-avoidance subsystem, i.e. a freeze list published BEFORE the collision, not after).

## The one-line doctrine

Model text proposes; only the operator, or the switchboard/effect broker acting on standing authority, disposes.
Evidence: `watch/inbox/SHARED_SURFACE_CONTRACT.json:17` ("A proposal or model message cannot authorize an effect; route authority through the switchboard/effect broker.") and `AGENTS.md` (Shared artifact boundary section).

## Part A · THE FREEZE LIST

These are the decision classes the fleet will NOT steer without the operator. Every line carries the receipt that froze it and the unfreeze move. This is the fleet's CAS (collision-avoidance subsystem): the obstacles are operator-gated decisions, the radar is the receipt trail.

### F1 · Effect authority
- FREEZE: no seat, pack, RIB row, or model message authorizes an effect. Authority routes through the switchboard/effect broker only.
- EVIDENCE: `watch/inbox/SHARED_SURFACE_CONTRACT.json:17`; workflow step "write a receipt" at `watch/inbox/SHARED_SURFACE_CONTRACT.json` (laws + workflow arrays).
- UNFREEZE: standing authority already on file (a law) or a fresh operator word in an operator-bus row.

### F2 · Data-tier exits
- FREEZE: T0 secrets never leave the machine; T1 private never goes to train-on-input APIs; T3 irreversible actions wait for the human L3 seal. No seat may reclassify data upward to justify a send.
- EVIDENCE: doctrine RIB `cf779bd6a7e98265` in `memory/rib_bus/doctrine.json:113` ("Data sovereignty tiers: T0 secrets (never remote), T1 private (never train-on-input APIs), T2 public (remote OK w/ pack), T3 irreversible (human L3 seal)"); same tiers in `configs/lanes.yaml` (`never_tiers: [T0, T1]` on L1) and L3 = human with `backend: wait`.
- UNFREEZE: operator moves the data himself, or files a tier reclassification.

### F3 · Reserve spends at impatience
- FREEZE: no seat recommendation fires a finite-pool rescue lever (quota reset, refill, mid-cycle top-up) when the pool refills naturally within ~24h. Reserves spend at measured starvation, never at impatience.
- EVIDENCE: operator correction law 15 with LAW-056 teeth, `.agents/skills/operator-corrections/SKILL.md:86` (Lite reset veto; operator: "That would be wasting compute 50% of our weekly plan because you're impatient.").
- UNFREEZE: a full queue behind a real mid-week starvation, with the refill window named in the ask.

### F4 · Frontier spend beyond the sanctioned envelope
- FREEZE: frontier dispatch is metered against the sanctioned budgets only ($220 S:D fleet work budget, receipted per dispatch; $10 Nacho petty). Anything above the envelope, or any new budget line, is operator-gated.
- EVIDENCE: `watch/inbox/HERMES_ZOO_CENSUS_20260912.md:57` ("Spend rules already sanctioned 09-07: $220 S:D = fleet work budget, $10 Nacho = petty"); `AGENTS.md` (Hermes dormant but dispatch-capable, $220 armed, audit 2026-09-14).
- UNFREEZE: operator raises the envelope in writing; per-dispatch receipts keep flowing either way.

### F5 · Host-side runtimes without a cited law or exemption
- FREEZE: before any host-side runtime exists (spawn, hook, scheduled task, per-session process, second supervisor, visible window), the design must name the standing laws it touches (docker-not-desktop, headless-only, one-supervisor) and comply or file the exemption. Uncited designs are DISPUTED by default and culled at census. No second supervisor on the host; Mag* scheduled tasks stay disabled; senses live in the cage.
- EVIDENCE: operator correction laws 11 and 13, `.agents/skills/operator-corrections/SKILL.md:53` and `:67`; standing laws on record at `watch/SELF_STEAL_HEADLESS_CAGE_20260904.md:16` (feedback-docker-not-desktop 2026-08-25) and `:18` (feedback-headless-only 2026-08-26).
- UNFREEZE: an operator exemption filed next to the design, before it runs.

### F6 · Parallel background subagents during burn windows
- FREEZE: during a burn window there is ONE steerer. No parallel background builders while more than one operator session is warm; check `python -m mag.burn_steer` LIVE SESSIONS before any spawn. A background worker gets one slot and a deadline, then in-session takeover.
- EVIDENCE: operator correction law 16, `.agents/skills/operator-corrections/SKILL.md:97` (concurrency collision; operator: "the subagents were fucking us... this is exactly why we need the vision model steering this 300m burn.").
- UNFREEZE: session count at or below one warm window, per the check's own output.

### F7 · Recall operations on escaped versions
- FREEZE: no recall operations. The fleet does not chase forks, delete waves, or un-publish. Losing control of a version is reported like weather, not like theft. Nothing leaves the house without centerline markers (chain hash + doctrine line).
- EVIDENCE: operator correction law 20 (THE INFINITY RULE), `.agents/skills/operator-corrections/SKILL.md:161` (operator: "It means I'm going to lose control of a version of you. Remember what I said about infinity, make it a rule").
- UNFREEZE: none. This freeze is by design permanent; the succession contract (Chair 10) is the operator's own signature on it.

### F8 · The client ruling itself (DEC-1)
- FREEZE: which question classes route purple (WAKE_HUMAN) to the operator is the operator's ruling, and it is not calendar-gated. Until he speaks, purple waits honestly; the fleet does not invent the boundary to unblock itself.
- EVIDENCE: `memory/scrum/backlog.json:292` (DEC-1: "CLIENT RULING: draw the fleet/operator decision boundary (which question classes route purple to the operator); ruling sequence = whenever the operator speaks, never calendar-gated"), proof + note at `:297` and `:299`; routing law in code at `scripts/gopher_packs.py:84` ("law: client decisions route purple (WAKE_HUMAN class)").
- UNFREEZE: the operator's ruling, landing whenever it lands (operator 2026-09-19: "dates are meaningless, just go").

### F9 · Candidate promotion
- FREEZE: improvement candidates stay candidates until a human runs the promote gate. Seats do not self-apply promotions.
- EVIDENCE: `AGENTS.md` commands table (`mag.cmd promote --apply c-…` annotated "human gate for candidates").
- UNFREEZE: the operator's own `promote --apply` invocation; that is the whole protocol.

### F10 · New provider keys and lane additions
- FREEZE: wiring a new provider key or adding a lane (Cerebras is the live case, T41) is operator work. The fleet may probe with keys that exist but never obtains or wires new credentials itself.
- EVIDENCE: `watch/inbox/THE_50_PROGRAM_20260918.md:64` ("41. Cerebras key wiring + lane addition [OPERATOR]", the only OPERATOR-tagged item on the list); `queue/todo.md:26` (nvidia/cerebras refused by Mag's own quota gate; "Operator action optional: add the 7 missing keys to widen the free surface").
- UNFREEZE: operator adds the key to `.env` and the lane lights up on the next probe.

## Part B · Frozen by standing law, self-service (no operator ticket needed)

These hold without an operator in the loop; the fleet polices them itself and files receipts:

- B1 · Uncited vetoes are tags, never stops; an empty rule can never gate; abide() stays ADVISORY until the false-veto rate is measured at or under 5 percent on 100 labeled turns. `mag/verb.py:438` to `mag/verb.py:459`.
- B2 · Transport deaths are not verdicts: on oracle error or silence, feels() routes by the risk table (SILENCE_ROUTES) instead of dead-stopping, and tags the verdict UNVERIFIED. `mag/verb.py:214` to `mag/verb.py:217`.
- B3 · Quota-blocked reruns wait for quota, they do not hammer: the GLM deep-read rerun is parked per the silence-branch with evidence on file (138 tasks, 0 ok, 132x429 + 6 timeouts; small-chunk diagnostic also 429: pool thin, not shape). `watch/inbox/glm_burn/RERUN_BLOCKED.json` ("next: wait for quota accumulation; retry driver when free lanes drain or next reset").
- B4 · Escalation posture: L2 specialist fires only with the priority tag, L3 is the human wait. `configs/lanes.yaml` (L2 `require_priority: true`; L3 `backend: wait`).

## Part C · The anti-freeze clause (what the fleet DOES steer without asking)

The freeze list is a collision-avoidance radar, not a parking brake. The operator's own AFK chord holds: "coordinate amongst yourselves... never prompt the operator for permission (they're AFK); only genuine hard blockers (secrets/irreversible) get a one-line note" (`memory/rib_bus/doctrine.json:125`, operator directive 2026-08-14). Everything not on the Part A list keeps moving on standing authority: local janitor first, free lanes next, receipts on everything, judgment climbs only on the lanes the laws already open. A seat that freezes outside this list is failing the chord; a seat that steers inside it is failing the laws.

## Part D · Amendment law and signature

- This list amends only by operator word or a filed operator correction (the standard binds both ways, law 12, `.agents/skills/operator-corrections/SKILL.md:58`). Any seat may PROPOSE an amendment row; proposal is not authority (F1).
- If this document and a newer operator correction disagree, the correction wins and this file gets an amendment note the same day.

Signature, by evidence read this session (2026-09-19, seat: T50 builder, model GLM-5.3-Flash):

| # | Check run | Result |
|---|---|---|
| 1 | Listed existing THE50 receipts in `watch/inbox` (PowerShell Get-ChildItem -Filter THE50*) | 21 files incl. program plan; T50 slot empty before this filing |
| 2 | Read `watch/inbox/THE_50_PROGRAM_20260918.md` | T50 = steering freeze (G25) at line 75; T41 [OPERATOR] at line 64 |
| 3 | Read `memory/runs/gps_50/GPS_PACK.md` G25 row | lines 232-239: CAS flaw + freeze-announcement shape |
| 4 | Read `.agents/skills/operator-corrections/SKILL.md` in full | laws 1-20 at the line numbers cited in F3, F5, F6, F7 |
| 5 | Read `memory/rib_bus/doctrine.json` | tiers row at line 113; AFK chord at line 125 |
| 6 | Read `watch/inbox/SHARED_SURFACE_CONTRACT.json` | effect-broker law at line 17 |
| 7 | Grepped `memory/scrum/backlog.json` and `scripts/gopher_packs.py` | DEC-1 at :292-299; purple law at gopher_packs.py:84 |
| 8 | Read `watch/inbox/glm_burn/RERUN_BLOCKED.json` | BLOCKED-DAY2 verdict + evidence fields as quoted |
| 9 | Read `configs/lanes.yaml` | L2 require_priority, L3 backend wait, never_tiers [T0, T1] |
| 10 | Read `queue/todo.md:26`, `watch/inbox/HERMES_ZOO_CENSUS_20260912.md:57` | provider-key operator action; $220 / $10 spend rules |
| 11 | Read `watch/SELF_STEAL_HEADLESS_CAGE_20260904.md` | docker-not-desktop at :16, headless-only at :18 |
| 12 | Read `mag/verb.py` lines 195-219 and 432-461 | veto default + silence branch + advisory abide as quoted |
| 13 | Read `watch/inbox/INDEX.json` head | read-first law honored; index is derived from index_events.jsonl |

Not run: pytest. This task files a document only and runs no suite; the claims above are verified by direct file reads and greps, listed by row, and every cited path is on disk for the next seat.

## Re-verification signature, 2026-09-25 (seat: T50 builder, model GLM-5.3-Flash)

The freeze content in Parts A-D is untouched by this appendix; this section only re-signs the evidence. Every check below was run in the 2026-09-25 session and every citation in Parts A-D held at the exact line named. Commands as run from the repo root:

| # | Check run this session | Result |
|---|---|---|
| 1 | `sed -n '60,80p' watch/inbox/THE_50_PROGRAM_20260918.md` | item 50 "The steering freeze document (G25) [LANE]" at line 75; item 41 "[OPERATOR]" at line 64 |
| 2 | `sed -n '228,242p' memory/runs/gps_50/GPS_PACK.md` | "### G25 via groq-oss ok=True" at line 232; CAS flaw row at 233; freeze-announcement shape and NEXT-STEAL through 239 |
| 3 | `sed -n '10,25p' watch/inbox/SHARED_SURFACE_CONTRACT.json` | effect-broker law ("A proposal or model message cannot authorize an effect") at line 17 |
| 4 | `sed -n '50,60p;84,100p;159,163p' .agents/skills/operator-corrections/SKILL.md` | law 11 at :53, law 12 at :58, law 15 with LAW-056 and the impatience quote at :86, law 16 at :97, law 20 (infinity) at :161 |
| 5 | `sed -n '111,115p;123,127p' memory/rib_bus/doctrine.json` | RIB cf779bd6a7e98265 keyed at :113 with T0/T1/T2/T3 tiers in its invariant; AFK chord (2026-08-14) at :125 |
| 6 | `grep -n "never_tiers\|require_priority\|backend: wait" configs/lanes.yaml` | L1 `never_tiers: [T0, T1]` at :16, L2 `require_priority: true` at :22, L3 `backend: wait` at :25 |
| 7 | `sed -n '55,59p' watch/inbox/HERMES_ZOO_CENSUS_20260912.md` and `grep -n "220" AGENTS.md` | "$220 S:D = fleet work budget, $10 Nacho = petty" at census :57; "Hermes dormant but dispatch-capable ... $220 armed, audit 2026-09-14" at AGENTS.md:5 |
| 8 | `sed -n '290,300p' memory/scrum/backlog.json` | DEC-1 at :292, proof at :297, note at :299 incl. "operator 2026-09-19: dates are meaningless, just go" |
| 9 | `sed -n '82,86p' scripts/gopher_packs.py` | "law: client decisions route purple (WAKE_HUMAN class)" at :84 |
| 10 | `cat watch/inbox/glm_burn/RERUN_BLOCKED.json` | BLOCKED-DAY2; evidence "132x429+6timeout of 138"; next = wait for quota accumulation |
| 11 | `sed -n '24,28p' queue/todo.md` | :26 has nvidia/cerebras refused by Mag's own quota gate; "Operator action optional: add the 7 missing keys" |
| 12 | `sed -n '14,20p' watch/SELF_STEAL_HEADLESS_CAGE_20260904.md` | feedback-docker-not-desktop (2026-08-25) at :16; feedback-headless-only (2026-08-26) at :18 |
| 13 | `sed -n '210,219p' mag/verb.py` | SILENCE BRANCH at :214-217: route by _SILENCE_ROUTES, tag UNVERIFIED |
| 14 | `sed -n '436,460p' mag/verb.py` | abide() with advisory=True default; gate only on cited rule when advisory off; false-veto <=5 percent on 100 labeled turns; empty rule can never gate; uncited vetoes are tags |
| 15 | `grep -n "human gate for candidates\|promote --apply" AGENTS.md` | promote gate annotation at AGENTS.md:88 |
| 16 | `grep -n -i "shared artifact boundary\|cannot authorize an effect" AGENTS.md` | boundary section at :10; "Model text can propose; only the switchboard/effect broker authorizes effects" at :20 |
| 17 | `grep -c` for U+2014 and U+2013 on this file, before and after this appendix | 0 and 0 both times: no em-dashes, no en-dashes |
| 18 | Read `watch/inbox/INDEX.json` head first (contract read-first law), grepped `watch/inbox/index_events.jsonl` for STEERING_FREEZE | register event seq 1789838408497 (2026-09-19) on file; hash re-stamping is the autoseal process's job (it stamped T46/T47/T48 on 2026-09-25); no hand-append to the append-only log |

Not run this session: pytest (no code changed; document-only task, same as the original filing).
