# UNION FULLSEND — season 1 — 24/7 standing full-width drive

*queue_digest `569f548531feb600` · done 20/42 · dead 0 · runs 3 · lanes: or-union-alpha 18ok/0fail, zai-lite 2ok/0fail · lite credits spent (guard ledger) 5110 · generated 2026-09-17T14:43:59.780211Z*

> **These are LEADS and DRAFTS, not facts.** Model output from free windows (union-alpha stealth window + Lite glm-5.3-flash under law 15). A lead is promoted > only by a byte check; a parable is a draft until the operator says otherwise. > Failures are listed, never hidden.

## corpus

### UF-30 — primary-docs hunt: ancient games + wargames
*class corpus · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## doctrine

### UF-14 — attack the Amendment Obligation
*class doctrine · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 48492 ms · ok*

“Exactly one amendment” conflicts with the permitted no-amendment tide. Also, “a later reader would accept” supplies neither a designated reader nor an acceptance criterion.

| Claim | Status |
|---|---|
| Hash-chained lineage proves an amendment improved anything | Unproven |
| Cosmetic edits can satisfy the amendment quota | Supported |
| Splitting one change into daily fragments can manufacture compliance | Supported |
| Selecting irrelevant rules can manufacture defensible “stands” | Supported |
| A friendly reader can prevent self-voiding by accepting trivial changes | Supported |
| Three genuinely justified decisions to retain rules demonstrate ritual burden | Disputed |

The present falsifier tests reader approval, not usefulness. It can punish stability while rewarding churn.

### Proposed replacement amendment

> **Each daily tide must append exactly one review disposition: AMEND or STAND. The review obligation persists; amendment manufacture is not required.**
>
> **Selection:** Examine the oldest unresolved rule implicated by a logged failure, near-miss, or explicit contradiction. If none exists, examine the next rule in a published rotation covering all fleet rules. Append selection evidence. Changing the rotation requires a separate, visible lineage entry and cannot change that tide’s selection.
>
> **AMEND:** Append the parent hash, exact delta, defect addressed, and a concrete distinguishing case: what action, permission, verification result, or materially relevant interpretation changes between parent and proposed version. State the observable result that would defeat the claimed benefit. Cosmetic changes remain permissible housekeeping but cannot constitute an AMEND disposition. Changes sharing one defect and distinguishing case count as one amendment, regardless of fragmentation.
>
> **STAND:** Append the examined rule, a concrete attempted counterexample, and why the existing rule handles it. Repeated reasoning must identify either new evidence or an untested case; otherwise mark the review **unsubstantiated**, not compliant.
>
> **Witness:** A reviewer designated before the tide checks these published conditions. Append the verdict and reasons; preserve disagreements and corrections as descendants. These are admissibility judgments, not scores. Neither proposal nor admission automatically enacts a rule change.

**Falsifier of this replacement:** Trial it for 30 tides. It fails if independent replay of the ledger finds **two compliant dispositions** that evade selection, lack their required distinguishing case/counterexample, or count fragments separately—or if **three tides** require invented novelty despite documented exhaustion of distinct cases. Failure reopens this amendment; it does not erase history or automatically abolish daily review.

### UF-15 — FX5 counter-case
*class doctrine · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 69915 ms · ok*

The false premise is that some artifact class inherently **must** flow backward. None does. Generation confers no authority. The legitimate exception is **explicit promotion of a derived candidate into authoritative state**, not reverse synchronization.

| Claim | Status |
|---|---|
| Generated code or docs must overwrite their canonical inputs | Disputed |
| Checked-in generated code/docs may be required repository artifacts without becoming canonical inputs | Supported |
| A generated lockfile may become authoritative for subsequent dependency resolution after acceptance | Supported |
| A checksum manifest may become an authoritative release record after acceptance; checksums alone establish neither correctness nor approval | Supported |
| The direction inversion and drift guard prevent further rollbacks in this fleet | Unproven |
| An append-only hash chain proves that recorded content was correct or authorized | Disputed |

### Decision rule

Backflow is required **only when an explicit authority policy requires accepting computed results as a new canonical decision or record**. Otherwise, derivation remains one-way.

Permit that promotion only if:

1. **Authority is scoped:** policy identifies the fields/artifacts eligible for promotion and the authorized approver or automated acceptance rule.
2. **Provenance is bound:** the candidate identifies its canonical input revisions and generation context.
3. **Freshness is checked atomically:** acceptance verifies the relevant inputs and destination still match the candidate’s declared baseline; changed state requires regeneration or explicit reconciliation.
4. **The change is intentional:** the accepted diff is recorded as a canonical transition, including any deliberately authorized rollback—not disguised as “sync.”
5. **History survives:** the ledger appends the transition, its authorization, and its predecessor; it does not rewrite earlier entries.

**Falsifier for this rule:** a stale or unauthorized candidate can overwrite current canonical content while satisfying all five conditions. That would show the conditions or their authority scope are insufficient.

The reported rollback case was an artifact’s existence being treated as overwrite authority. A drift guard helps, but does not itself establish authorization.

### Amended FX5

> Canonical authority flows to derived artifacts. Derived artifacts shall not overwrite canonical state merely because they were generated, checked in, or found different. A derived candidate may become canonical only through an explicitly authorized, provenance-bound, atomic promotion against a verified baseline, recorded as a new ledger transition. Where canonical acceptance policy requires that promotion, it must occur through that path—not reverse synchronization.

**Falsifier for the amendment’s enforcement:** a build or sync operation changes canonical state without the required promotion record, or accepts a candidate against a mismatched baseline.

### UF-16 — receipts-before-work threshold
*class doctrine · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 71270 ms · ok*

No universal crossover is established. Task duration measures overhead poorly and audit value worse: a ten-second action can create irreversible liability.

| Claim | Status |
|---|---|
| Minutes, calls, or lanes alone establish when receipts cost more than they protect | Unproven |
| The threshold below identifies an economic optimum | Unproven |
| A bounded lightweight tier preserves “receipts before work” and “falsifiers before data” | Supported, if enforced as written |

**Proposed amendment — provisional threshold**

> A lightweight receipt MAY replace a full receipt only when **all** conditions hold:
> - Work is bounded to **five elapsed minutes** after receipt commitment.
> - At most **one external, read-only call** is permitted.
> - Exactly **one declared lane** is touched.
> - Work makes no persistent change except ledger records and isolated draft artifacts; it creates no external commitment and involves no restricted data, permission change, or irreversible action.
>
> Before work or data access, the actor MUST append a hash-chained receipt containing: task and actor identifiers, declared scope, applicable limits, intended output, and a task-specific falsifier with its evaluation rule.
>
> Before crossing any limit, the actor MUST stop and commit a full receipt. Discovering restricted scope likewise requires stopping; retrospective upgrade does not cure unauthorized work.
>
> Completion MUST append elapsed time, actual calls and lanes, output/evidence references, and the falsifier result. Neither receipt may be overwritten.

**Falsifiers**

| Proposal or rationale | What would prove it wrong |
|---|---|
| This tier supplies sufficient audit evidence | One eligible task produces a material error or scope breach that a full receipt would have exposed, but the lightweight record cannot reconstruct or attribute. |
| Five minutes / one call / one lane is economically preferable | A matched trial shows receipt-cost savings are no greater than added investigation cost plus expected loss from reduced detection. Include completion and upgrade costs. |
| These bounds are enforceable | One task crosses a bound before its upgrade is committed. That falsifies the enforcement claim, even without damage. |

Measure both tiers on comparable tasks, with independently recorded outcomes. **Trial falsifier:** unequal task-risk distributions or missing outcomes invalidate the comparison.

Until those measurements exist, call this a **testable eligibility boundary**, not the point where overhead exceeds audit value.

### UF-17 — tide three questions, outsider answers
*class doctrine · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 86880 ms · ok*

“Never amended,” “a stranger would adopt,” and “the fleet did not send” are not established by this record. You supplied descriptions, not independently replayable evidence.

### 1. What is it believing without having tested?

| Claim | Status |
|---|---|
| Five green harnesses establish competence beyond those harnesses. | **Unproven.** Passing can validate implementations while leaving the underlying assumptions untouched. |
| A hash-chained ledger makes the fleet’s account true or complete. | **Unproven.** Hashes establish linkage; without independently retained checkpoints, they do not establish a unique history. They never establish truthful inputs. |
| Hash-committing the blind-set key establishes a fair blind evaluation. | **Unproven.** It does not alone establish absence of leakage, representative selection, or frozen scoring. |
| A tested referee chain is an operational referee. | **Unproven.** The two clicks remain a discretionary boundary. Who withholds them, under what conditions, with what recorded consequence? |
| The favorite theory was conditionally refuted. | **Supported**, as reported. Whether rho +0.327 warrants that verdict independently remains **Unproven** without the registered criterion and analysis. |

The central untested belief: **that internal procedural discipline survives external replay and inconvenient operator decisions.**

### 2. Which rule has never once been amended?

| Claim | Status |
|---|---|
| Any particular rule has never been amended. | **Unproven.** No complete rule history was supplied. |
| Append-only means rules cannot change. | **Disputed.** A later entry can supersede a rule without deleting its predecessor. |
| Operator authorization is an enduring constitutional rule. | **Unproven.** It is the visible current gate, not a demonstrated historical invariant. |

Evidence that would settle this: genesis rules, every subsequent rule change, and the interpretation governing supersession. One valid amendment falsifies “never.”

### 3. What should travel first—and what is missing?

| Claim | Status |
|---|---|
| A stranger would adopt a particular component first. | **Unproven.** Adoption requires observing strangers, not imagining them. |
| The first export should be a **standalone falsification receipt**: frozen claim, kill criterion, inputs, executable scorer, result, and ledger verification. | **Unproven proposal.** Falsifier: an unaffiliated operator cannot reproduce the verdict without fleet assistance. |

What this account **did not supply**: that runnable receipt, including the evidence behind the favorite theory’s defeat. Whether the fleet sent it elsewhere is unknown.

Ship the reproducible loss before the institutional story.

### UF-19 — board half-life law
*class doctrine · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 136204 ms · ok*

The gate does not determine a half-life. Receipt coverage is not necessarily completion, and a deadline threshold is not a decay law.

| Claim | Status |
|---|---|
| More than 10 receiptless tasks at day 2 triggers re-seeding or tombstoning of the remainder | Supported |
| Passing that gate means at least 80% are complete | Unproven: depends on what receipts certify |
| One operator, seven lanes, and free model lanes determine throughput | Unproven |
| These facts identify a uniquely right half-life | Unproven |

### First principles

For the original seeded cohort of \(N\) tasks, define
\[
F_N(t)=\frac{\text{tasks completed by }t}{N}.
\]
The completion half-life is the time when \(F_N(t)=1/2\). Tombstoning is **not** completion; re-seeding must not erase the original denominator.

Determining \(F_N\) requires service times, operator attention, dependencies, and concurrency effectiveness—not merely lane counts.

### Conditional exponential law

**Assume** receipts certify completion and every unfinished task has constant completion hazard \(\lambda\):
\[
F_N(t)=1-e^{-\lambda t},\qquad h=\frac{\ln2}{\lambda}.
\]

Calibrating to the gate’s **boundary**, not an observed outcome:
\[
F_{50}(2)=0.8
\Rightarrow \lambda=\frac{\ln5}{2},
\qquad h=\frac{2\ln2}{\ln5}\approx0.861\text{ days}.
\]

Under this model, passing the gate requires \(h\le0.861\) days. **Falsifier:** repeated cohort measurements showing nonconstant log-unfinished slopes, beyond sampling variation.

### Why board-size predictions remain conditional

An equally boundary-compatible, fixed-throughput model is
\[
F_N(t)=\min(20t/N,1),\qquad h_N=N/40.
\]
**Falsifier:** measured completion increments systematically incompatible with 20 tasks/day while work remains available.

| Board size | Constant-hazard model: half-life; done at day 2 | Fixed-throughput model: half-life; done at day 2 |
|---|---|---|
| 20 | 0.861 days; 80% (16 expected) | 0.5 days; 100% (20) |
| 50 | 0.861 days; 80% (40 expected) | 1.25 days; 80% (40) |
| 100 | 0.861 days; 80% (80 expected) | 2.5 days; 40% (40) |

### Tombstone criterion

At seed time \(+2\) days, count valid receiptless tasks \(M\). If \(M>10\), the stated rule requires re-seeding **or** tombstoning the remainder. It does not specify which disposition to choose. **Compliance falsifier:** a triggered cohort left without either disposition.

Neither a proportional threshold for other board sizes nor a unique completion law follows from the 50-task rule.

### UF-23 — WEAVE next-5 rubric
*class doctrine · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## engine

### UF-24 — ractor falsifier test stubs
*class engine · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-38 — engine/content contract exemplars
*class engine · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## game-canon

### UF-11 — the -GO line postmortems
*class game-canon · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 92315 ms · ok*

- **Bibliographic limit:** I can’t verify exact talk titles or article URLs without browsing. These are retrieval links, **not a verified bibliography**:
  - [GDC Vault: Hitman GO](https://www.gdcvault.com/search.php#&keyword=Hitman%20GO) — search **Daniel Lutz**, its game director.
  - [GDC Vault: Lara Croft GO](https://www.gdcvault.com/search.php#&keyword=Lara%20Croft%20GO).
  - [Game Developer/Gamasutra postmortem search](https://www.google.com/search?q=site%3Agamedeveloper.com+%22Hitman+GO%22+postmortem).
  - [Deus Ex GO design-interview search](https://www.google.com/search?q=%22Deus+Ex+GO%22+%22interview%22+design).

- **Mechanics to distinguish when checking those sources—not attributed interview claims:**
  - **Difficulty:** *Hitman GO* combines completing the route with optional objectives, including move limits; objectives need not all be achieved in one run. *Lara Croft GO* progressively introduces enemies, terrain interactions, and combinations.
  - **Hints:** These games offer solution assistance, not merely environmental clues. Exact free allowances, prices, and behaviour need checking against the **specific release/platform**.
  - **“One-move-at-a-time law”:** Player actions advance discrete simulation turns. That does **not** mean every enemy moves one square every turn; enemy-specific activation and timing rules matter.

- I cannot substantiate **“one-move-at-a-time law”** as the developers’ published terminology, or responsibly supply exact talk names from memory.

### UF-12 — step-clock puzzlers since 2016
*class game-canon · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 94291 ms · ok*

- **Test:** logical state advances only on accepted actions; animations do not count. Static Sokoban-style puzzles qualify, but they lack the *autonomous actors advancing one tick* found in stricter step-clock designs.

| Shipped | Game + designer | Fit / published material |
|---|---|---|
| **2016-04-18** | **Stephen’s Sausage Roll — Stephen Lavelle** | Deterministic movement, pushing, rolling and cooking; no real-time deadline. [Official](https://www.increpare.com/game/stephens-sausage-roll.html). No substantial first-party design postmortem I can confidently identify. |
| **2020-09-10** | **A Monster’s Expedition — Alan Hazelden / Draknek & Friends** | Deterministic movement and log manipulation; spatial rather than autonomous-world clock. [Official](https://www.monsterexpedition.com/). |
| **2022-03-29** | **Patrick’s Parabox — Patrick Traynor** | Deterministic recursive pushing; action-gated state, not a continuously simulated world. [Official](https://www.patricksparabox.com/); [developer posts](https://patricktraynor.itch.io/patricks-parabox/devlog). |
| **2019-03-13** | **Baba Is You — Arvi Teikari** | Genuine move-triggered world updates, **but not universally deterministic:** multiple TELE destinations introduce randomness. [First-party development archive](https://www.hempuli.com/blog/). |

- **Buys:** unlimited deliberation, reproducible solutions, legible causality; cheap undo/replay *if state is captured completely*.
- **Costs:** update-order edge cases, explicit collision precedence, potentially enormous search spaces; environmental urgency must come from move budgets or consequences—not elapsed time.
- **Exclude SUPERHOT:** time slows while idle; it does not strictly stop.

### UF-21 — Isfahan 1197 lock dungeon
*class game-canon · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-22 — squid-maze trial season
*class game-canon · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## hosting

### UF-34 — DDoS economics 2026
*class hosting · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-35 — SRP6 vs modern auth
*class hosting · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-36 — server governance constitutions
*class hosting · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-37 — Evennia 2026
*class hosting · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## law

### UF-05 — post-yuzu litigation update
*class law · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 75846 ms · ok*

- **Coverage limit:** I cannot verify a complete 2025–2026 docket update here; “no new server-emulator cases” would be unsupported.

- **Yuzu — February 26/March 4, 2024:** *Nintendo v. Tropic Haze*, **2:24-cv-00082 (D.R.I.)**: complaint, then announced **$2.4 million** settlement and permanent-injunction terms. Settlement—not a merits ruling that all emulation violates §1201.

- **Yuzu forks — May 2024:** Nintendo’s GitHub takedown reached **8,535 repositories**, including forks. Notices: [github/dmca](https://github.com/github/dmca). Repository removal is not a judicial finding against each implementation.

- **Suyu — March 21, 2024:** GitLab removed its repository following a DMCA notice. Nintendo’s authorship of that particular notice was not publicly established; distinguish reported removal from confirmed Nintendo litigation.

- **Ryujinx — October 1, 2024:** Development/downloads stopped after Nintendo contacted developer **gdkchan**, according to the team. No publicly disclosed complaint or judgment accompanied that announcement. Ryujinx was independent, not Yuzu-derived.

- **Server reimplementations:** No new 2024–2026 server-specific action I can reliably identify. Relevant precedents remain *Davidson v. Jung*, **422 F.3d 630 (8th Cir. 2005)**—**bnetd**—and *MDY v. Blizzard*, **629 F.3d 928 (9th Cir. 2010)**.

- **Practical §1201 posture:** Clean-room development helps copyright defenses, not automatic circumvention immunity. **§1201(f)** provides conditional interoperability protection; bypassing authentication/access controls or distributing circumvention tools remains separately risky. Preservation exemptions are narrow, not general public-server authorization.

### UF-06 — deterministic replay in servers
*class law · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 39275 ms · ok*

- **2026 caveat:** I cannot verify 2026 releases or announcements live; these are established implementations, not an exhaustive current census.
- **Factorio:** deterministic lockstep; clients execute the simulation from synchronized player actions. Replay requires matching game/mod versions and initial state. [Documentation](https://wiki.factorio.com/Replay_system).
- **Supreme Commander: Forged Alliance / FAF:** shipped RTS with deterministic simulation and command-stream replays; desynchronization and version compatibility remain practical constraints. [FAF game code](https://github.com/FAForever/fa).
- **OpenRA:** released open-source RTS engine; synchronized orders, deterministic simulation, replay recording, synchronization checks. [Source](https://github.com/OpenRA/OpenRA).
- **Spring / Beyond All Reason:** synchronized simulation, recorded demos, desync diagnostics; separates synchronized gameplay from unsynchronized UI/rendering. [BAR engine](https://github.com/beyond-all-reason/spring).
- **Age of Empires II / Warcraft III:** shipped lockstep RTS implementations with action-based recorded games/replays; not portable recordings across arbitrary engine patches.
- **Techniques:** record initial snapshot, tick-indexed inputs, external events, exact executable/content versions, and RNG seeds/state. Periodically hash canonical simulation state **including RNG state**; RNG-only hashes miss other divergence. Stable entity iteration, deterministic job ordering, and controlled script execution matter.
- **Float traps:** x87 versus SSE precision, FMA contraction, compiler reassociation, platform math libraries, unordered reductions. [Concrete analysis](https://gafferongames.com/post/floating_point_determinism/).
- **MMO scale:** no verified public full-world tick-replay implementation to name confidently. **EVE Online** and **Hadean/CCP Aether Wars** demonstrate large authoritative simulations—not evidence of deterministic input-only replay.

## parable

### UF-25 — the dozen cubes existence parable
*class parable · lane `any` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-26 — the second lantern parable
*class parable · lane `lite` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## physics

### UF-18 — past-bit box failure modes
*class physics · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 102903 ms · ok*

The key law is **conditional**, not unconditional: biased or deterministic past bits are harmless only if future targets are independent, fair bits **conditional on the committed record and all information used to select runs**.

| Claim | Status |
|---|---|
| Fixed past bits versus independent fair future bits gives \(K\sim\mathrm{Binomial}(1024,1/2)\) | Supported |
| \(K\ge563\) has one-sided \(p<0.001\) under that null | Supported |
| The box’s actual targets satisfy that null | Unproven |
| A hash alone proves commitment preceded target generation | Disputed |

Costs below are incremental estimates using existing phones/computers. “Falsifier” means an observation defeating the stated safeguard.

| Failure | How it fakes a pass | Cheapest hardening / falsifier | Cost |
|---|---|---|---|
| Custodian collusion | Custodian backdates receipt or substitutes a favorable record after seeing targets. | Send the complete, canonically encoded record to two separately controlled witnesses before target generation; publicly anchor its digest. **Falsifier:** inconsistent copies, missing independent receipt, or shared control. | $0–10 |
| Hash-does-not-prove-timing | A valid digest is published after targets exist; local timestamps or ledger history are rewritten. | Obtain an independently timestamped, externally retained digest receipt before the recorded target-generation session. **Falsifier:** receipt postdates generation or exists only locally. | $0 |
| Coin bias | Biased targets preferentially match biased past bits; all-one past bits exploit a heads bias. | Preregister paired-toss extraction: HT→0, TH→1; discard HH/TT. This removes fixed bias **only for independent, identically distributed tosses**. **Falsifier:** within-pair bias differences or dependence. | $0; extra tosses |
| Coin dependence/manipulation | Correlation inflates tail probabilities; an informed tosser steers outcomes. | Blind tossers to past bits; preregister toss, landing, invalid-toss and recording rules; retain continuous video. **Falsifier:** information leakage, selective retosses, or detected serial dependence. Tests cannot certify independence. | $0; labor |
| Sensor drift | **Alone, it cannot.** Post-target shifts, exclusions or threshold changes can manufacture alignment. | Commit final bits, indices and preprocessing rules—not merely raw readings. **Falsifier:** any scored bit or alignment differs. | $0 |
| Analysis peeking | Optional stopping or trying multiple scoring rules increases false-pass probability. | Fix length, score and rejection rule; run one locked script. **Falsifier:** unregistered stopping or alternate analyses counted as confirmatory. | $0 |
| Run-level selection | Many attempts are made; only winners enter the ledger or report. | Publicly register every run before acquisition; log aborts; allocate a total error budget across attempts. **Falsifier:** missing run IDs, unlogged attempts or budget overruns. | $0; administration |

## scout

### UF-09 — BenchLM leaderboard read
*class scout · lane `zai-lite` · glm-5.3-flash · attempt 1 · 44049 ms · ok*

**Caveat first: I can't verify any leaderboard called exactly "BenchLM."** Possibly you mean one of these — no leaderboard I know of carries that name:

- **Hugging Face Open LLM Leaderboard** (hf.co/spaces/open-llm-leaderboard; run by HF + community on EleutherAI's lm-evaluation-harness). V2 metrics (launched June 2024, submissions frozen ~March 2025): MMLU-Pro, GPQA (diamond), **MuSR (multistep soft reasoning)**, MATH lvl-5, IFEval, BBH — normalized 0–100 average. No Elo, no chat-vibe component.
- **BenchLLM** (github.com/superlinear-ai/benchllm) — a Python LLM-app testing library, not a leaderboard.

**For 2B-class models on structured multi-step tasks**, the relevant board is **Berkeley Function-Calling Leaderboard (BFCL)**, UC Berkeley Sky Lab (gorilla.cs.berkeley.edu): AST-match + executable verification across simple, multiple-choice, parallel, multi-turn (v3), agentic (v4) categories. 2B-class models score far below 7B-class there; exact per-release scores vary by BFCL version.

**Usefulness verdict:** Open LLM Leaderboard averages for 2B-class (Gemma-2-2B, Qwen2.5-1.5B, SmolLM2-1.7B) sit roughly 15–25 points below 7B-class, but I'm not confident enough in exact per-model numbers to quote them — pull them from the live board. Chat-Elo (LMArena) and benchmark scores diverge most at 2B scale.

### UF-10 — open remakes completeness
*class scout · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 96066 ms · ok*

**Not a verified 2026 audit:** I cannot inspect live repositories. This provisional ranking uses demonstrated playability, not stars; licenses below cover code, not original game assets.

Source: [radek-sprta/awesome-game-remakes](https://github.com/radek-sprta/awesome-game-remakes).

| Rank | Repository | Completeness | License |
|---:|---|---|---|
| 1 | [OpenTTD/OpenTTD](https://github.com/OpenTTD/OpenTTD) | Playable; complete transport simulation | GPLv2 |
| 2 | [OpenRCT2/OpenRCT2](https://github.com/OpenRCT2/OpenRCT2) | Playable; full park-management game | GPLv3 |
| 3 | [dhewm/dhewm3](https://github.com/dhewm/dhewm3) | Playable Doom 3 source port | GPLv3 |
| 4 | [CorsixTH/CorsixTH](https://github.com/CorsixTH/CorsixTH) | Playable Theme Hospital campaigns | MIT |
| 5 | [ihhub/fheroes2](https://github.com/ihhub/fheroes2) | Playable Heroes II campaigns | GPLv2 |
| 6 | [OpenMW/openmw](https://github.com/OpenMW/openmw) | Morrowind completable | GPLv3 |
| 7 | [OpenRA/OpenRA](https://github.com/OpenRA/OpenRA) | Playable RTS multiplayer; not exact originals | GPLv3 |
| 8 | [vcmi/vcmi](https://github.com/vcmi/vcmi) | Playable Heroes III; compatibility gaps | GPLv2 |
| 9 | [OpenLoco/OpenLoco](https://github.com/OpenLoco/OpenLoco) | Playable Locomotion reimplementation | MIT |
| 10 | [ACEmulator/ACE](https://github.com/ACEmulator/ACE) | Playable Asheron’s Call **server**; needs client | AGPLv3 |

- **Unfinished, not merely skeleton:** [xoreos/xoreos](https://github.com/xoreos/xoreos), GPLv3; exploration/engine framework, not complete campaigns.
- **Dead:** no defensible 2026 classification without checking archives, maintainer notices and successor forks. Old releases alone do not establish abandonment.

### UF-39 — game-datasets for AI
*class scout · lane `lite` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-40 — free-model market 30-day delta
*class scout · lane `lite` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## self-steal

### UF-27 — steal from the session record
*class self-steal · lane `any` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-28 — steal from THE SCALE
*class self-steal · lane `any` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-29 — steal from the tide card
*class self-steal · lane `any` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## wow-extension

### UF-01 — playerbot modules 2026
*class wow-extension · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 30107 ms · ok*

- **2026 maintenance:** Unverified; I cannot inspect live commits or releases.

- **mod-playerbots**
  - Repository: https://github.com/mod-playerbots/mod-playerbots
  - Companion core: https://github.com/mod-playerbots/azerothcore-wotlk
  - Function: AI-controlled player characters; autonomous population, questing, parties, dungeons, battlegrounds.
  - **100 bots, one realm:** No verified RAM/CPU benchmark available to me.
  - Compatibility: Uses the playerbots core fork; do not assume compatibility with stock AzerothCore.
  - Named module conflicts: No verified, version-specific conflict list available to me.

- **NPCBots — related alternative, not a drop-in module**
  - Repository/documentation: https://github.com/trickerer/Trinity-Bots
  - Integrated AzerothCore: https://github.com/trickerer/AzerothCore-wotlk-with-NPCBots
  - Function: Recruitable NPC combat companions; not autonomous player accounts.
  - **100 bots, one realm:** No verified RAM/CPU benchmark available to me.
  - Compatibility: Core modifications required; compatibility with the separate playerbots fork is unverified.

- **BotsParty**
  - Public repository, implementation, 2026 maintenance, resource measurements, and conflicts: **Unverified**. I cannot confidently identify an AzerothCore module under this exact name.

- **Others:** No additional actively maintained 2026 player-bot modules I can substantiate.

### UF-02 — mod-eluna lua scripting state
*class wow-extension · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 75443 ms · ok*

- **2026 status:** I cannot verify live HEAD, compatibility, or archival status. Check [azerothcore/mod-eluna](https://github.com/azerothcore/mod-eluna) against your AzerothCore commit; don’t assume compatibility from the module name.

- **Exposed surface:** [Eluna API reference](https://elunaluaengine.github.io/): `RegisterPlayerEvent`, `RegisterCreatureEvent`, `RegisterCreatureGossipEvent`, `RegisterServerEvent`; `Player:AddItem`, `Player:Teleport`, `Unit:CastSpell`, `WorldObject:SpawnCreature`; `WorldDBQuery`/`WorldDBExecute`. Availability depends on compiled bindings—not every C++ method is exposed.

- **Pure-Lua example:** `lua_scripts/broodlord.lua` adds periodic Frostbolts to existing creature template **12017**, Broodlord Lashlayer:
  ```lua
  local function bolt(_, _, _, c)
      local victim = c:GetVictim()
      if victim then c:CastSpell(victim, 116, true) end
  end
  RegisterCreatureEvent(12017, 1, function(_, c)
      c:RegisterEvent(bolt, 8000, 0)
  end)
  local function stop(_, c) c:RemoveEvents() end
  RegisterCreatureEvent(12017, 2, stop)
  RegisterCreatureEvent(12017, 4, stop)
  ```
  Existing template/spell required; no C++ or database changes. This augments—not replaces—existing AI.

- **Performance ceiling:** No defensible universal NPC count. Profile your build. Blocking queries and high-frequency callbacks consume server-update time; Lua is not an asynchronous job system.

- **Still C++:** Unexposed hooks/methods, packet handling changes, pathfinding internals, combat-formula changes: implement C++ modules/core patches or extend bindings. New static templates generally require SQL; new client-visible assets require client changes, not merely C++.

### UF-03 — cmangos vMaNGOS status
*class wow-extension · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 38192 ms · ok*

- **2026 release dates and active-maintainer counts:** I cannot verify these without live repository access. Historical contributor totals are **not** active-maintainer counts; release tags and latest commits are also different measures.
  - CMaNGOS Classic: [releases](https://github.com/cmangos/mangos-classic/releases), [activity](https://github.com/cmangos/mangos-classic/pulse).
  - vMaNGOS: [releases](https://github.com/vmangos/core/releases), [activity](https://github.com/vmangos/core/pulse).
  - CMaNGOS comprises separate **Classic, TBC, and WotLK** cores—not one project-wide release.

- **vMaNGOS’s authenticity advantage:** [vMaNGOS](https://github.com/vmangos/core) targets original **Vanilla WoW**, including **1.12.1, build 5875**, with historical patch progression and Vanilla-specific mechanics/content work. This means original-client behavior rather than recreating Vanilla content inside a later expansion.
  - [AzerothCore](https://github.com/azerothcore/azerothcore-wotlk) targets **3.3.5a, build 12340**.
  - [TrinityCore](https://github.com/TrinityCore/TrinityCore)’s **3.3.5 branch** likewise targets WotLK; its mainline targets later retail. Neither is a drop-in original-Vanilla equivalent.
  - That advantage is **specialization**, not proof every encounter is more accurate.

- **New small realm:** Both are technically plausible original-Vanilla foundations. Shortlist **vMaNGOS for historical progression** and **[CMaNGOS Classic](https://github.com/cmangos/mangos-classic) with [ClassicDB](https://github.com/cmangos/classic-db)** for another established Vanilla stack. Calling either actively maintained in **2026** requires checking recent merges, database updates, issue responses, and build success.

### UF-04 — realm hardware 2026 refresh
*class wow-extension · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 34983 ms · ok*

- **Assumption:** $500/$1,500/$5,000 are **upfront hardware budgets**, USD, excluding colocation. These are planning estimates, **not verified 2026 quotes**. Hardware alone cannot guarantee 1,000 concurrent players.

- **$500:** used Ryzen **5 5600/5600X**, **32GB DDR4**, **1TB NVMe**, consumer motherboard/case/PSU. Plausible budget build; least headroom for crowded hubs, scripts, and database activity.

- **$1,500:** Ryzen **7 9700X**, **64GB DDR5**, **2TB TLC NVMe**, good cooling. Best-balanced tier; prioritize sustained single-thread performance over additional cores.

- **$5,000:** Ryzen **9 9950X**, **128GB DDR5**, **2×2TB NVMe mirrored**, UPS, plus backup/spare hardware. Extra cores help auxiliary workloads—not proportional realm capacity. Mirroring isn’t backup.

- **Bandwidth:** provision **1Gbps**, DDoS protection, and substantial transfer allowance. Assuming—not measuring—**5–20KB/s outbound/player**, 1,000 continuously connected players produce **40–160Mbps**, approximately **13–52TB/month**. Measure your actual workload.

- **Cloud comparison:** historical AWS **us-east-1 Linux m7i.2xlarge**, **8 vCPU/32GiB**, **$0.4032/hour ≈ $294/month**; **1TiB gp3 ≈ $82/month**. Internet egress at **$0.09/GB** implies roughly **$1,170–$4,680/month before tiers/free allowances**. Shared vCPUs aren’t equivalent to dedicated physical cores.

- **Changed in 2026?** I cannot verify this year’s changes. At sustained occupancy, metered egress remains a major dedicated-host advantage. Check [EC2](https://aws.amazon.com/ec2/pricing/on-demand/), [EBS](https://aws.amazon.com/ebs/pricing/), [Hetzner](https://www.hetzner.com/dedicated-rootserver/), and [AzerothCore](https://github.com/azerothcore/azerothcore-wotlk).

### UF-07 — small-realm anticheat
*class wow-extension · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 44475 ms · ok*

- **2026 caveat:** I can identify public implementations, not verify which small realms currently deploy them. These examples concern **WoW 3.3.5a, client build 12340**, not every expansion.

- **AzerothCore:** [`azerothcore/mod-anticheat`](https://github.com/azerothcore/mod-anticheat) is a concrete server-side option. Its documented checks include **speed, flight, water-walking, jumping, teleport-plane and climbing**. “Teleport-plane” is a specific heuristic—not proof that arbitrary teleportation is comprehensively blocked. Check the selected revision’s [`conf/`](https://github.com/azerothcore/mod-anticheat/tree/master/conf) for exact switches; forks differ.

- **Warden:** Both [AzerothCore](https://github.com/azerothcore/azerothcore-wotlk) and [TrinityCore’s 3.3.5 branch](https://github.com/TrinityCore/TrinityCore/tree/3.3.5) include Warden infrastructure. Relevant `worldserver.conf` knobs include:
  - `Warden.Enabled`
  - `Warden.NumMemChecks`, `Warden.NumOtherChecks`
  - `Warden.ClientResponseDelay`, `Warden.ClientCheckHoldOff`
  - `Warden.ClientCheckFailAction`, `Warden.BanDuration`

- **Important distinction:** Warden performs client-integrity checks; it is **not** server-authoritative movement validation. Effective coverage depends on configured checks, client/platform support and enforcement settings. Movement handling also must accommodate legitimate teleports, transports, knockbacks and latency.

- **Opposing tools:** **WoWEmuHacker**, **Cheat Engine** and **WPE Pro** are historical names associated with private-server cheating or manipulation. They are not interchangeable, universally effective Warden bypasses. I cannot substantiate working **2026 versions** or realm-specific bypass claims.

### UF-08 — one-click repacks 2026
*class wow-extension · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 33013 ms · ok*

- **2026 maintenance / last-commit ages:** I cannot verify live GitHub activity here. I cannot reliably label any downloadable “solo repack” actively maintained in 2026. These are **checkable upstream projects, not endorsements of repack binaries**:

| Project | What it provides | Last-commit age |
|---|---|---|
| [azerothcore/azerothcore-wotlk](https://github.com/azerothcore/azerothcore-wotlk) | WoW **3.3.5a** server; configurable XP/drop rates; bots are not standard bundled features | Unverified |
| [mod-playerbots/azerothcore-wotlk](https://github.com/mod-playerbots/azerothcore-wotlk) + [mod-playerbots/mod-playerbots](https://github.com/mod-playerbots/mod-playerbots) | Playerbots-compatible core and module; not a one-click repack | Unverified |
| [azerothcore/mod-ah-bot](https://github.com/azerothcore/mod-ah-bot) | Auction-house automation, **not** adventuring playerbots | Unverified |
| [azerothcore/mod-autobalance](https://github.com/azerothcore/mod-autobalance) | Creature/dungeon scaling for smaller groups | Unverified |

- **Boosted rates:** configuration choices, not proof of a distinct maintained distribution. Check supplied configuration and release manifests.
- **Docker Compose:** upstream has [documented Docker installation](https://www.azerothcore.org/wiki/install-with-docker). That does **not** establish that a particular repack’s Compose build includes working playerbots, AHBot, or current images.
- **Legal posture:** AzerothCore is **AGPL-3.0**; redistribution/modification carries source obligations. Its licence does not license Blizzard’s client/assets. “Free” or “private” is not blanket immunity. Relevant precedent: *Davidson & Associates v. Jung*, **422 F.3d 630 (8th Cir. 2005)**—not an AzerothCore-specific ruling.

### UF-31 — SmartAI deep dive
*class wow-extension · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-32 — top AC modules by usage
*class wow-extension · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-33 — map extraction costs
*class wow-extension · lane `union` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

## x-play

### UF-13 — self-threading reply for the pamphlet
*class x-play · lane `or-union-alpha` · stealth/union-alpha · attempt 1 · 45930 ms · ok*

The supplied observations do not establish that speed or brevity causes a top-reply slot.

| Claim | Status |
|---|---|
| +0–2s self-replies reliably win | Unproven |
| Under-80-character text matches image-only performance | Unproven |

### Candidates
Each is one line, under 80 characters.

1. `19 rows. Follow the moves to the names the count leaves out.`
2. `Every farm bought the scale. Check what disappeared from the lists.`
3. `The lists get shorter. The keeper still calls each sheep by name.`
4. `Read the kifu. Compare the count with the names.`
5. `The scale has buyers. The keeper has names. Audit the 19 rows.`

| Verdict | Status |
|---|---|
| These lines frame a parable, not verified events | Poetry |
| **Winner: 1**, for combining the artifact, decoding action, and missing-name hook | Unproven |

**Falsifier for all five:** Across comparable pinned drops with matched timing and exposure, another reply pattern consistently earns more likes at the same measurement window.

**Winner’s specific falsifier:** An image-only reply showing one legible kifu fragment beside its decoded missing-name line consistently beats candidate 1. That would favor a visible receipt over an invitation to inspect.

### UF-20 — x-radar missed patterns
*class x-play · lane `zai-lite` · glm-5.3-flash · attempt 1 · 86006 ms · ok*

**Presupposition flag first:** one day, 8 threads, top-replies-by-likes = survivorship sample. Likes are downstream of visibility (position, follower pings), not merit. Every "pattern" is a prior awaiting execution, none is a finding.

| # | Claim | Status |
|---|---|---|
| 1 | Self-replies land +0-2s, farm crown | Supported mechanically; "farming" is unproven — first position + follower ping is structure, not skill |
| 2 | Product→one-liner/15m; safety→excerpt/45-90m | Unproven (n=8, one day) |
| 3 | Winners <80 chars | Unproven — survivorship; brevity is a platform-wide base rate |
| 4 | Usage-limit asks = invariant hijack | Unproven; also negative-EV for a parable brand (reputational cost unmodeled by likes) |
| 5 | Self-threading = like monopoly | Disputed as stated — monopolizes reply crowns on *own posts* only |

**Three missed patterns**
- **M1 Branch position:** likes cluster on replies-to-hot-replies, not root replies. Your radar sampled roots only.
- **M2 Reciprocal velocity:** small-account winners get their first 5–10 likes from own mutuals in minutes. Speed is graph-owned, not content-owned. (Organic reciprocity is the free version of buying.)
- **M3 Serial presence:** the same handle appearing across threads compounds; one-shot timing models miss cumulative recognition.

**Calendar** — P = own post, R = reply lane. Max two patterns/day.

| Day | Lane | Patterns | Falsifier |
|---|---|---|---|
| 1 | P-pamphlet | 1 + 3: instant self-reply, <80-char coda | Own reply not top reply by likes at +2h → kill 1 |
| 2 | R-product | 2 + M1: one-liner ask ≤15m, hot-branch attached | 0 asks acknowledged in 15m across 3 targets → kill 2a |
| 3 | P-receipt-thread | M2 + 5: post, then self-thread a receipt | Self-thread not top-2 replies at +3h → kill 5 |
| 4 | R-safety |

### UF-41 — Astra persona leak to fleet probes
*class x-play · lane `lite` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*

### UF-42 — Claude merge contrarian takes
*class x-play · lane `lite` ·  · attempt ? · ? ms · FAILED: not run*

*(pending)*
