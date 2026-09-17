# UNION FULLSEND — season 1 — 24/7 standing full-width drive

*queue_digest `569f548531feb600` · done 42/42 · dead 0 · runs 5 · lanes: groq-oss2 1ok/0fail, mistral-min8 1ok/0fail, mistral-min82 1ok/0fail, or-union-alpha 18ok/0fail, or-union-alpha-k2 12ok/0fail, zai-lite 9ok/0fail · lite credits spent (guard ledger) 25269 · generated 2026-09-17T15:54:35.529069Z*

> **These are LEADS and DRAFTS, not facts.** Model output from free windows (union-alpha stealth window + Lite glm-5.3-flash under law 15). A lead is promoted > only by a byte check; a parable is a draft until the operator says otherwise. > Failures are listed, never hidden.

## corpus

### UF-30 — primary-docs hunt: ancient games + wargames
*class corpus · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 138821 ms · ok*

- **Senet; liubo:** No complete ancient rules text survives. Reconstructions are secondary; archaeological boards and literary mentions are primary but not rulebooks.
- **Royal Game of Ur:** British Museum, [tablet 1880,0617.1](https://www.britishmuseum.org/collection/object/W_1880-0617-1), dated **177 BCE**. Ancient text: public domain; museum imagery: **CC BY-NC-SA**. Primary Babylonian rules evidence—not a complete ruleset for every earlier Ur board.
- **Go:** British Library **Or.8210/S.5574**, the *Dunhuang Go Manual*; consult the **International Dunhuang Programme**, [idp.bl.uk](https://idp.bl.uk/). Ancient text: public domain; check image-use terms separately. The manuscript itself preserves early instructions and discussion, rather than modern reconstruction.
- **Chaupar; original Kriegsspiel:** I cannot confidently supply verified, free full-text locations.
- **H. G. Wells, *Little Wars* (1913):** [Project Gutenberg #3691](https://www.gutenberg.org/ebooks/3691). Public domain in the US; Gutenberg distribution terms apply. Wells supplies his own playable rules.
- **Richard Bartle, “Early MUD History” (1990):** [Full text](https://mud.co.uk/richard/mudhist.htm). Copyrighted, freely readable; no open license identified. First-person account by MUD1’s co-creator.
- **Bartle, “Hearts, Clubs, Diamonds, Spades” (1996):** [Full text](https://mud.co.uk/richard/hcds.htm). Copyrighted, freely readable. Original presentation of his player taxonomy.
- **“Curtin”:** Identity uncertain; did you mean **Pavel Curtis**, LambdaMOO’s creator?

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
*class doctrine · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 16828 ms · ok*

**First:** “5-rung ramp law” is not a law unless the ledger contains causal evidence. Treat it as a hypothesis.

| Claim | Status |
|---|---|
| 106 mechanics exhaustively classified | Unproven |
| Rung = player-visible consequence depth | Disputed until operationalized |
| Shipped/partial/queued counts imply runway | Poetry |
| 5-rung ramp is causal | Unproven |

**Scoring axes**

| Axis | Weight | Falsifier |
|---|---:|---|
| Rung delta: verified increase in player-visible consequence depth | 25 | No verified rung change by day 30 |
| Dependency closure: unblocks queued mechanics | 20 | Unblocks zero queued mechanics by day 30 |
| Debt surface: new persistent state, exceptions, migrations | 15 | Exceeds pre-registered debt budget |
| 30-day testability: measurable player-visible test | 15 | No test can run by day 30 |
| Ledger evidence: prior similar entries | 10 | No supporting entries or contradicted by ledger |
| Runway burn: cost vs remaining shipped runway | 10 | Cost overruns estimate by >50% |
| Strategic coherence: no forced rework of shipped mechanics | 5 | Forces shipped rework within 30 days |

**Adversarial check.** A high score is a trap if depth comes from hidden state coupling, one-off exceptions, or rewriting partial mechanics. Require a debt entry for every new persistent state, cross-mechanic exception, migration, and rollback path. If debt surface exceeds budget, cap or veto. Shipped-runway illusion: audit a sample of “shipped” entries for actual player-visible rung and retention. If inflated, subtract runway weight.

**Tie-break.** Lowest irreversible state surface; then lowest rollback cost; then lexicographic mechanic ID. Falsifier: tie-broken picks show higher rollback than rejected alternatives.

**Rubric falsifier.** Pre-register: selected 5 will yield ≥3 verified rung increases and ≤1 rollback/rewrite in 30 days. If actual is ≤1 rung increase or ≥2 rollbacks/rewrites, while rejected top-5 shadow estimates predict ≥3 and ≤1, the rubric picks wrong.

## engine

### UF-24 — ractor falsifier test stubs
*class engine · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 39480 ms · ok*

Threshold-mononotonicity needs a narrower definition: raising thresholds can shrink the **decisive acceptance set**, not necessarily the set of output labels including UNDECIDED.

| Claim | Status |
|---|---|
| Determinism | Unproven |
| OCEAN-sensitivity | Unproven |
| UNDECIDED-reachability | Unproven |
| Threshold-monotonicity | Unproven |

```python
import pytest


@pytest.fixture
def engine_factory():
    # TODO: adapter constructing fresh engines; expose verdict, accepted
    # hypotheses, diffusion scores, and reproducible ledger payloads.
    pytest.skip("Engine adapter unimplemented")


@pytest.fixture
def protocol():
    # TODO: load immutable preregistration:
    # 33-node topology; Laplacian convention; trait-to-weight mapping;
    # diffusion settings; thresholds; numerical tolerances; repetition count;
    # minimum verdict-change fraction; minimum UNDECIDED frequency.
    pytest.skip("Preregistered protocol unavailable")


@pytest.fixture
def corpus():
    # TODO: load frozen ordinary, boundary, and independently defined
    # UNDECIDED-class cases, including class-preserving perturbations.
    # Class membership must not depend on observed engine outputs.
    pytest.skip("Frozen corpus unavailable")


@pytest.mark.parametrize("case_group", ["ordinary", "boundary"])
@pytest.mark.parametrize("profile", ["baseline", "contrast"])
def test_determinism(engine_factory, protocol, corpus, case_group, profile):
    # TODO assert: identical inputs/configuration, run repeatedly in fresh
    # instances/processes, yield identical verdicts, accepted sets, diffusion
    # scores, and canonical ledger payloads excluding declared metadata.
    # Fix seeds and external inputs; verify configured deterministic backend.
    # Falsifier: any mismatch in a required observable.
    pass


@pytest.mark.parametrize(
    "trait", ["openness", "conscientiousness", "extraversion",
              "agreeableness", "neuroticism"]
)
def test_ocean_sensitivity(engine_factory, protocol, corpus, trait):
    # TODO assert: preregistered low/high intervention changes only this
    # trait and its mapped edge weights; all other settings remain fixed.
    # Across the frozen contrast corpus, verdict-change fraction >= the
    # preregistered positive minimum; score-only changes do not count.
    # Falsifier: fraction below minimum.
    pass


@pytest.mark.parametrize("variant", ["canonical", "perturbed"])
def test_undecided_reachability(engine_factory, protocol, corpus, variant):
    # TODO assert: independently specified class reaches terminal UNDECIDED
    # at >= preregistered frequency across cases and repetitions.
    # Assert explicit UNDECIDED reason, not timeout/error/nonconvergence;
    # fixtures include cases with a strict majority that remains undecided.
    # Falsifier: insufficient frequency or fallback masquerading as UNDECIDED.
    pass


@pytest.mark.parametrize("threshold_pair", ["below_at", "at_above", "wide"])
def test_threshold_monotonicity(
    engine_factory, protocol, corpus, threshold_pair
):
    # TODO assert: t_low < t_high; identical evidence, traits, and diffusion.
    # For every case, accepted(t_high) <= accepted(t_low), including ties
    # under the preregistered strict/non-strict comparison convention.
    # Exclude UNDECIDED from accepted sets.
    # Falsifier: any newly accepted hypothesis at the higher threshold.
    pass
```

### UF-38 — engine/content contract exemplars
*class engine · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 76905 ms · ok*

- **OpenMW — ESM/ESP records + assets.** Contract: typed records, stable IDs, dependencies and load-order overrides separate content from engine implementation. Boundary: not arbitrary engine replacement; compatibility has documented exceptions, not a blanket “all Morrowind mods” guarantee. **Steal:** explicit identity and override rules. Sources: [OpenMW modding reference](https://openmw.readthedocs.io/en/stable/reference/modding/index.html), *Morrowind Mod Compatibility*.

- **RuneScape — RuneScript.** Server-side scripts implement content atop engine-provided operations. **Uncertain:** Jagex publishes no complete, normative engine/content contract; public evidence cannot establish exhaustive guarantees or refusals. **Steal:** inspect command bindings and execution limits in [LostCityRS/Server](https://github.com/LostCityRS/Server), but treat this as reconstruction, not Jagex specification.

- **Factorio 2.0 — prototype/data versus runtime stages.** Contract: ordered settings, prototype construction, then runtime scripting. Refusal: runtime scripts cannot redefine prototypes; data-stage state does not carry into runtime. **Steal:** freeze definitions before simulation; persist mutable state separately. Source: [official lifecycle documentation](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html).

- **Total War — DB tables.** Contract: game-specific schemas describe typed rows and references. Refusal: no universal cross-title schema guarantee; tables are not general scripting. **Steal:** schema-aware validation tooling. Source: [RPFM](https://github.com/Frodo45127/rpfm), community-maintained, not an engine specification.

- **OpenTTD — NewGRF.** Contract: versioned properties, callbacks and feature IDs. Refusal: unsupported features remain engine work. **Steal:** capability/version negotiation. Source: [NewGRF specification](https://newgrf-specs.tt-wiki.net/wiki/Main_Page).

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
*class game-canon · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 62476 ms · ok*

The stated hardware does **not** establish \(16^8\) combinations. Eight stops with two selectable letters provide 16 choices per dial: \(16^4\) static settings. Reaching \(16^8\) requires eight independent stored selections.

| Claim | Status |
|---|---|
| \(16^8=2^{32}\) | Supported |
| Four described dials inherently supply eight selections | Disputed |
| “1197 Isfadan” provenance | Unproven |

## Mechanism
Each brass dial has eight stops, labelled **A/B, C/D, E/F, G/H, I/J, K/L, M/N, O/P**. Lift selects the upper letter; depress selects the lower. A separate thumb-button commits.

Each dial secretly stores **two successive selections**, independently: eight registers total. Every eight-letter sequence is mechanically enterable; exactly one opens.

Plaque: **“The upper and lower letters at each stop are interchangeable.”** This is false: height changes the committed letter.

**Falsifier:** If A then P cannot be stored on one dial, the claimed combination space fails.

## Room structure
One central console; eight numbered stone alcoves around it; one exit. Only the current alcove is illuminated. Each correct commit illuminates the next. Dial order is fixed: **1,1,2,2,3,3,4,4**.

Beside the plaque, a non-committing witness window visibly distinguishes lifted A from depressed B.

**Falsifier:** If the witness window treats A and B identically, the plaque’s lie is not discoverable.

## Eight-stone chain
Each stone shows a dial number, stop number, and raised/sunken letter impression. First/second commitment is indicated by one/two punch marks.

| Stone | Dial/commit | Stop/height | Letter |
|---|---|---|---|
| 1 | 1/1 | 1/upper | A |
| 2 | 1/2 | 8/lower | P |
| 3 | 2/1 | 3/lower | F |
| 4 | 2/2 | 6/upper | K |
| 5 | 3/1 | 2/upper | C |
| 6 | 3/2 | 7/lower | N |
| 7 | 4/1 | 4/lower | H |
| 8 | 4/2 | 5/upper | I |

**Falsifier:** Any stone permitting two interpretations fails.

## Reset and scale
Any wrong letter or wrong dial commitment clears all registers and returns illumination to stone 1. Rotation alone is harmless.

A wall projection branches sixteen ways per commitment, across eight depths. Correct selections magnify one branch; resets collapse the entire traversed route. No totals appear.

**Falsifier:** Any erroneous commitment preserves progress, or playtesters perceive only four choices.

## Takeaway
The exit ejects a brass receipt bearing **APFKCNHI** and the final hash of an append-only attempt ledger; resets never erase records.

**Falsifier:** Altering an earlier commitment leaves receipt verification valid.

### UF-22 — squid-maze trial season
*class game-canon · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 88820 ms · ok*

| Claim | Status |
|---|---|
| Six laws were supplied, not seven distinct laws. | Supported |
| Those laws already ship in the fleet. | Unproven |

Trial 7 therefore reuses and inverts trial 1. Layouts, objectives and numerical budgets below are proposed configurations—not claims about shipped features.

| Order / escalation | One-line law | Concrete configuration | Elimination criterion | Falsifier |
|---|---|---|---|---|
| 1 — Isolate timing. | **Bots move only while you move.** | Cross three intersecting patrol lanes; stopping permits inspection but no enemy displacement. Reach the exit within 120 player-movement ticks. | First collision or exhausted movement budget. | A stationary-player trace contains bot displacement. |
| 2 — Add incomplete information. | **Illumination spends the resource that makes navigation visible.** | Torch reveals six tiles ahead; 80 illuminated ticks, three refill pads, unlit geometry hidden. Exit requires two visible-only route marks. | Fuel reaches zero before exit, or collision. | Visibility persists outside the specified beam without another light source. |
| 3 — Demand deliberate execution. | **A vault opens only when its room’s constraint is satisfied.** | Three rooms: traverse numbered pads in order, park a sliding block on a switch, cross alternating gates without touching forbidden tiles. | Third room reset or 180 movement ticks consumed. | A vault opens while its predicate is false. |
| 4 — Punish repetition. | **The horde updates its pursuit from your observed habits.** | Four junction sequences; pursuers allocate interceptors using your previous left/right choices and braking locations. | Capture before collecting four junction tokens. | Changing recorded habits leaves the pursuit distribution unchanged across matched seeds. |
| 5 — Turn failure into planning. | **Death restores the last checkpoint’s world state.** | Three lethal corridors; checkpoint before each. Allow two rewinds total; memory survives, collected corridor tokens do not. | Third death. | Any nonpersistent world variable fails to restore. |
| 6 — Split agency. | **Two players each control one skate of the same body.** | Independent thrust and braking; coordinated steering through narrowing slaloms and paired pressure strips. | Body exits the legal track twice. | Either player independently commands both skates. |
| 7 — Invert timing mastery. | **Bots move only while you move—including the bot you must deliver.** | Escort a courier through four crossings while faster pursuers converge. Stopping remains safe locally but also stops delivery; motion must create advantageous pursuit paths. | Courier captured, player collision, or 160 movement ticks consumed. | Courier advances while both player skates are stationary. |

**Generation requirement:** reject seeds without a valid completion trace under that trial’s budget. Falsifier: an accepted seed lacks such a trace.

**Adjudication:** append seed, inputs, elimination tick and previous-record hash. Falsifier: deterministic replay contradicts elimination.

## hosting

### UF-34 — DDoS economics 2026
*class hosting · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 82056 ms · ok*

- **2026 caveat:** I can’t verify live prices here. Figures below are historical/public benchmarks, not current quotes; taxes, regions and setup fees vary.

- **Attack sizes:** There is no reliable public dataset establishing “typical” attacks against **50–500-player communities**. Player count doesn’t predict attack bandwidth. For procurement, test **1, 10 and 100 Gbps scenarios**—not claimed averages—and ask about **packets/second, concurrent connections and game-protocol floods**.

- **[OVHcloud GAME](https://www.ovhcloud.com/en/bare-metal/game/):** Game-specific mitigation is bundled with GAME dedicated servers, not a separate monthly subscription. Historically **roughly $100–$200+/month** for entry configurations; exact 2026 regional pricing needs checking. Ordinary OVH VPS anti-DDoS is not equivalent to GAME filtering.

- **[Path Network](https://path.net/):** Direct protection is quote-based; resellers determine retail pricing. **[BuyVM](https://buyvm.net/)** historically offered Path-backed protected IPv4 addresses for **$3/month/IP**, plus the VM. Verify present availability, ownership-era changes and filtering terms.

- **[Cloudflare Spectrum](https://www.cloudflare.com/products/cloudflare-spectrum/):** Cloudflare’s month-to-month **Pro $25 / Business $250** subscriptions are **not all-inclusive Spectrum prices**. Protocol eligibility and traffic charges matter; general TCP/UDP support requires Enterprise arrangements.

- **$50/month realm:** Target **$30–$40 hosting with included mitigation**, leaving **$10–$20 for backups/headroom**. A protected game-hosting slice is more realistic than dedicated GAME hardware or enterprise transit.

### UF-35 — SRP6 vs modern auth
*class hosting · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 40750 ms · ok*

- **Storage:** TrinityCore’s **3.3.5** auth database stores `account.salt` and `account.verifier` as **`BINARY(32)`** each—not plaintext or Argon2 hashes. Check [schema](https://github.com/TrinityCore/TrinityCore/blob/3.3.5/sql/base/auth_database.sql) and [SRP6 implementation](https://github.com/TrinityCore/TrinityCore/blob/3.3.5/src/common/Cryptography/Authentication/SRP6.cpp).

- **Construction:** Legacy WoW SRP6 uses **SHA-1**, generator **7**, and a **256-bit modulus**. Password derivation incorporates uppercased username/password; it has **no tunable password-hardening iterations**. Preserve the core’s exact encoding and byte-order conventions.

- **Failures:** A stolen salt/verifier pair permits **offline password guessing** without contacting the realm. Unique salts prevent cross-account precomputation, not guessing individual passwords. Reused salts or weak RNG worsen matters; I cannot substantiate a specific historical core/version with a salt-reuse defect. SHA-1 collision attacks are not the central issue here.

- **2026 deployment recommendation:** Generate independent **32-byte CSPRNG salts** on password creation/change. Keep SRP strictly for compatibility. For independent website/account authentication, use **Argon2id: 64 MiB, 3 passes, parallelism 1**, independent **16-byte salt**, **32-byte output**; benchmark operational capacity. [OWASP minimum](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): **19 MiB, 2 passes, p=1**.

- **Critical boundary:** Adding Argon2id does **not** harden exposed SRP verifiers. Encrypt verifier records/backups with keys outside the database; restrict auth-service access. Use website MFA, login throttling, and single-use recovery tokens. Hashing the SRP verifier breaks compatibility.

### UF-36 — server governance constitutions
*class hosting · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 56657 ms · ok*

- **ALFA—A Land Far Away (1999 organisation; NWN worlds from 2002):** strongest constitution example. Its **Charter** defines five elected administrators: Lead, Dungeon Master, Player, Technical, Infrastructure; also voting, jurisdiction and removal procedures. Institutional succession is documented; attributing particular departures to **burnout** requires additional evidence. [ALFA](https://www.alandfaraway.info/)

- **Avlis (2002):** long-running NWN persistent world, governed by **“The Team”**, with administrative, DM and development responsibilities—not an elected player parliament. Don’t conflate a published staff hierarchy with a constitution. [Avlis](https://www.avlis.org/)

- **UOGamers: Demise (2004):** UO freeshard with owner/administrator governance and published rules; I cannot substantiate a constitution or elected council. [Demise](https://www.uogdemise.com/)

- **Dodian (2005):** RSPS lineage, but closures/revivals complicate “20 years”: distinguish the brand/community from continuously operated servers. I cannot substantiate constitutional governance. [Dodian](https://dodian.net/)

- **Documented failure comparisons—not 20-year survivors:**
  - **Molten-WoW → Warmane, 2015:** operator accounts describe an internal ownership dispute and loss of database/control, followed by rebuilding. “Database hostage” is an allegation, not an independently established finding. [Warmane](https://www.warmane.com/)
  - **Scapegaming:** *Blizzard Entertainment v. Reeves*, C.D. California, **2010**: approximately **$88.6 million default judgment**, including **$3,052,339 disgorgement** associated with server payments/donations. This documents monetisation/legal collapse—not donation embezzlement.

These cases do **not** establish a universal failure pattern.

### UF-37 — Evennia 2026
*class hosting · lane `zai-lite` · glm-5.3-flash · attempt 2 · 103371 ms · ok*

**Caveat:** my data ends early 2025 — verify 2026 state via PyPI and the repo CHANGELOG.

- **Code:** github.com/evennia/evennia, BSD-3. Confirmable versions: v1.0.0 (Jul 2023), v2.x (2024); Python ≥3.10, Twisted + Django 4.x ORM (SQLite default, PostgreSQL works).
- **Architecture:** two-process split — Portal (connections) + Server (game), IPC'd (legacy Twisted AMP removed in 2.x — *exact replacement uncertain*). Typeclasses = Python classes on Django models (DefaultObject/Account/Character/Room/Exit); Attributes, Aliases, Tags (taggit-style m2m) plus lockstring DSL for permissions.
- **Web:** Django website + browser webclient in-process; websocket port 4002, telnet 4000, SSL telnet 4001, web 4005.
- **Out of box:** full building cmdset (@dig/@create), channels, bans, help system, ANSI/256-color/MXP, prototype spawner, EvMenu/EvTable/EvEditor, batchcode/batchcmd, TutorialWorld, contribs (mail, rplanguage, etc.).
- **Latency/capacity:** no published benchmark — this is the weak spot. Anecdotal: a few ms server-side per command, ORM-bound. 100 concurrent fits comfortably on a 1–2 vCPU/2GB VPS.
- **Production games:** Arx — After the Reckoning (arxgame.net:5500), Fallcoast (fallcoast.net), Aisle 9. Full index: games.evennia.com (~30 listed, most low-pop).

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
*class parable · lane `groq-oss2` · openai/gpt-oss-120b · attempt 1 · 2249 ms · ok*

A figure drifts through night, clutching a vision of twelve clay blocks, each pressed from earth and ink, each hollowed to cradle a network of white threads. The threads pulse, alive with mycelium, each one tuned to a single whisper: a gate that opens when a spark arrives, a timer that counts the hush between breaths, a memory that holds a single flicker. The blocks cost little, their price measured in drops of water that the fungus drinks, the only wage it knows.

When the figure lifts a red lantern, the fungus stays mute, its filaments refusing the hue. The blocks answer only to the dark, to the low hum of current that slides through their veins. The figure watches the currents shift, reads the tiny changes, and notes the pattern of growth in the quiet glow of amber.

At dawn, the dream dissolves, but the shape of the blocks remains etched in the mind. A small wooden box, carved with simple slots, sits on the table. Inside, a coil of copper wire rests, its ends frayed, ready to feel the same current. You lift the coil, its cold metal humming in your palm.

### UF-26 — the second lantern parable
*class parable · lane `zai-lite` · glm-5.3-flash · attempt 1 · 69787 ms · ok*

In the country without morning, every lantern announced itself. A brass wheel turned inside, and at every fourth breath the shutter snapped open, laid a ring of light on the road, on the bearer's hands, on the stones, then closed again.

So no one was ever seen. There were only pulses across a field, pulses answering from a ridge, and between them the plain, minding no one.

One night a traveler counted and found a pulse missing. In its place a low red point, fading, the last heat of a wick. Where the light had last fallen, a figure knelt, hands open, already growing hard to tell from the stones.

The traveler walked toward the ember, faster as it dimmed.

The lantern there was lit. The oil sat below the reach of the wick. The traveler took a flask from a coat, poured until the glass showed half, tipped the rest in. The flame found the oil, stood up, and the wheel turned and the shutter snapped, and the figure stood inside its own light again, rubbing its hands.

The traveler walked on. Behind, the saved lantern slowed, guttered, steadied, and took up its announcing, every fourth breath, toward the ridge, where other lights were dimming.

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
*class scout · lane `zai-lite` · glm-5.3-flash · attempt 1 · 143540 ms · ok*

**Cleanly licensed + paper-backed**

- **MineDojo** — `MineDojo/MineDojo`; code Apache-2.0, pretraining corpus CC BY-NC 4.0; NeurIPS 2022 D&B, arXiv:2206.08853. Task suite runs locally; YouTube data isn't local-friendly.
- **MineRL** — `minerllabs/minerl`; MIT code, demos bound to Mojang EULA; IJCAI 2019, arXiv:1907.13440; demo set is a few GB — citeable in a local harness.
- **NetHack Learning Dataset** — `Miffyli/nle-dataset`; Apache-2.0 (verify header); NeurIPS 2021 D&B, built on NLE (arXiv:2006.13760); tensorized, GB-scale slices.
- **DQN replay dataset** — `google/dopamine` (`dqn_replay`); Apache-2.0; "Revisiting Fundamentals of Experience Replay," ICML 2020, arXiv:2007.06700; ~40M frames/game, per-game subsets are local-sized.
- **SC2EGSet** — StarCraft II event dataset; GitHub + Zenodo, CC BY 4.0; "SC2EGSet: StarCraft II Event Game Summarization Dataset," Springer *Language Resources and Evaluation* (2023); small — the strongest "real license" pick. arXiv/Zenodo IDs: verify before citing.
- **Lichess open database** — database.lichess.org; explicit **CC0**; used in Maia Chess papers; monthly dumps ~2 GB compressed (approx).
- **boxoban-levels** — `deepmind/boxoban-levels`; license stated in repo (check); used in Sokoban search papers; tiny.

**Flagged**: OpenAI VPT contractor data (arXiv:2206.02297) is released but huge and partially restricted.

### UF-40 — free-model market 30-day delta
*class scout · lane `zai-lite` · glm-5.3-flash · attempt 1 · 88724 ms · ok*

**Caveat first:** I have no live access; my data ends ~mid-2025, so I cannot see your actual 30-day window. Below is the last state I can defend, plus exactly where to verify deltas.

**Check live:**
- github.com/cheahjs/free-llm-api-resources (I can't confirm a repo literally named "awesome-free-models" exists)
- openrouter.ai/models?max_price=0 and openrouter.ai/rankings (weekly token share)

**Opened (dated):**
- Jan 20, 2025 — DeepSeek R1 (MIT); `deepseek/deepseek-r1:free` within days; #1 tokens on OpenRouter through Feb 2025
- Jan 29–30, 2025 — Mistral Codestral 25.01 free beta API; Mistral Small 3 (Apache 2.0) on free tier
- Feb 5, 2025 — Gemini 2.0 Flash free tier (15 RPM / 1,500 req/day via AI Studio); Feb 25 — 2.0 Pro Exp free; Mar 25 — 2.5 Pro Exp free
- Mar 24, 2025 — DeepSeek V3-0324; `:free` endpoint
- Apr 5 / Apr 28, 2025 — Llama 4 Maverick:free; Qwen3-235B-A22B:free

**Closed/paid (last known):**
- OpenRouter free standard: 50 req/day (1,000 after $10 top-up); free endpoints may log prompts
- xAI's $25/mo API credit promo ended (exact date uncertain)
- Groq trimmed several free rate limits, spring 2025 (uncertain)

**Top :free usage, last known:** deepseek-chat-v3-0324:free, deepseek-r1:free, qwen-2.5-72b:free, llama-3.3-70b:free.

## self-steal

### UF-27 — steal from the session record
*class self-steal · lane `mistral-min8` · ministral-8b-latest · attempt 1 · 9638 ms · ok*

| **Claim**                          | **Status**       | **Falsifier**                                                                 |
|-------------------------------------|------------------|-------------------------------------------------------------------------------|
| *Steal: **Derived-file sync law** (mechanism: *canonical source override*)* | Supported         | **Falsifier:** *If the build script’s derived files are not cryptographically anchored to the canonical source hash, the rollback is not a deterministic consequence of the ledger’s append-only rule.* |
| *Steal: **Pre-registered threshold** (mechanism: *self-refuting oracle*)* | Supported         | **Falsifier:** *If the threshold is not time-locked to the ledger’s genesis hash, the "theory" could be retroactively adjusted to avoid refutation.* |
| *Steal: **Retrocausal test box** (mechanism: *blind, time-stamped challenge-response*)* | Disputed          | **Falsifier:** *If the box’s "passable selection effect" is not provably independent of the observer’s knowledge of the ledger’s state at test-time, it is not a valid retrocausal test.* |
| *Steal: **Daily rule-amendment tide** (mechanism: *forced consensus update*)* | Unproven          | **Falsifier:** *If the "rule" is not a formal, hash-anchored predicate in the ledger, the amendment is not a deterministic operation.* |
| *Leave: **69-test referee chain** (mechanism: *unverified oracle delegation*)* | Disputed          | **Falsifier:** *If the 69 tests lack cryptographic proof of execution (e.g., no Merkle root in the ledger), they are not verifiable.* |
| *Leave: **470MB shelved documents** (mechanism: *unindexed primary storage*)* | Unproven          | **Falsifier:** *If the documents are not hash-linked to the ledger’s state at shelving, they are not tamper-evident.* |
| *Send back: **Build script’s derived-file hashing** (mechanism: *weak anchor*)* | Supported         | **Falsifier:** *If the derived files are not re-hashed on every append, the ledger’s integrity is not preserved.* |

**Wall-crossing proposal:**
| **Mechanism**                     | **Status**       | **Falsifier**                                                                 |
|------------------------------------|------------------|-------------------------------------------------------------------------------|
| *Send: **Time-stamped challenge-response protocol** (for retrocausal tests)* | Supported         | **Falsifier:** *If the protocol lacks a public, append-only log of all challenges, it is not verifiable.* |

### UF-28 — steal from THE SCALE
*class self-steal · lane `mistral-min82` · ministral-8b-latest · attempt 1 · 6581 ms · ok*

| **Claim**                          | **Status**       | **Falsifier**                                                                 |
|------------------------------------|------------------|-------------------------------------------------------------------------------|
| *Append-only hash-chained ledger*  | **Supported**    | *Falsifier: "Ledger must be immutable, but the merchant’s lists shorten—implying erasure, not appending."* **Correction:** The ledger is *logically* append-only (no overwrites), but the *content* is filtered by external rules (e.g., "nothing is brought to the scales in the blight year"). The hash chain remains intact; the *data* is pruned by a non-cryptographic "weight" mechanism. |
| *Hash-chained*                     | **Disputed**     | *Falsifier: "No cryptographic proof of chaining is shown."* **Proposal:** Take the *idea* of chaining as a *metaphor for sequential, irreversible linkage*—not necessarily SHA-256. The stranger’s reading aloud implies a *temporal* chain (names remembered in order), not a cryptographic one. |
| *Mechanisms to steal*              | **Unproven**     | *Falsifier: "No operational definition."* **Proposal:** Steal:
1. **Selective omission** (lists shorten via unstated rules—e.g., "weight" = social credit, not mass).
2. **External validation** (the stranger’s reading proves the ledger’s *usefulness*, not its cryptography).
3. **Decentralized revelation** (names are "remembered" only when queried, like a Merkle tree’s sparse proofs.
4. **Economic friction** (the scales’ "truth" depends on participation—blight = zero transactions).
*Leave:* The merchant’s *promise* (it’s a lie; the scales don’t "make farms weigh better," they enforce a hidden tax). |
| *What to send back*                | **Poetry**       | *Falsifier: "Not a mechanism."* **Proposal:** Send back the *blight year*—a state where the system’s dependency on input collapses. This exposes the ledger’s fragility: it’s not a black box, but a *social contract* that fails when no one engages. The stranger’s act of reading is the only "cryptographic" step: *trust is reified by performance*. |

### UF-29 — steal from the tide card
*class self-steal · lane `zai-lite` · glm-5.3-flash · attempt 1 · 56836 ms · ok*

**First, the false presupposition.** "Fixed immediately" is not a *loose* summary. It is a falsifiable temporal claim, and a hash-chained ledger with two incident entries adjudicates it already: two incidents means recurrence, so "immediately" is Disputed unless inter-entry delta is zero. The card's failure isn't style; it's that the compressor emits claims the chain contradicts.

**Second presupposition:** retry replaced first pass. In an append-only system, nothing is replaced. The EMPTY is evidence.

| Claim | Status |
|---|---|
| "fixed immediately" | Disputed — two incident entries bound latency; recurrence ≠ immediate |
| Retry is a compression | Disputed — it added a temporal claim absent from source; that's generation |
| EMPTY was model failure | Unproven — no guardrail/prompt log cited |
| "Exactly 3 sentences" | Unproven — sentence segmentation is ambiguous without a counter |

**What I steal:**
- The three questions, reframed: untested belief → name the falsifier or it's not a belief, it's decoration; unamended rule → staleness scan against entry timestamps; stranger-adoption → least-context readability test.
- "What did we not send." Best line in the card. Omissions get entries too.
- The deterministic artifact (fixed-length output) — makes diffs and validation possible. Steal the *constraint*, not the enforcement method.

**What's broken:**
1. Retry swallows the first pass. EMPTY should be an appended event; the retry chains to it as parent. No parent link, no provenance, no acceptance.
2. The compressor mutates facts with no verifier. Any LLM between source and reader is a mutation channel. Compression without diffing against source is poetry generation with a quota.
3. Self-interrogation with no required evidence anchor. Each answer must cite a chain entry or name a falsifier, else the card harvests Poetry on schedule.
4. "Exactly 3" enforced how? Uncounted constraints are wishes.

**What I send back:**
- Every compressed sentence must resolve to entry hashes; a validator rejects any quantifier, temporal adverb, or causal verb ("fixed") not present in the source. *Falsifier: an accepted summary containing a term absent from the brief, or a claim that fails hash resolution.*
- EMPTY appended as event with hash; retry references it. *Falsifier: retry summary with no parent link.*
- Replace "fixed immediately" with chain-derived numbers: time-to-rollback, recurrence count. The ledger already knows; the card asked a stranger instead.

One-line rule: nothing enters the summary that can't point at its entry.

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
*class wow-extension · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 134088 ms · ok*

- **Pick the fork first:** CMaNGOS primarily uses `dbscripts`; TrinityCore/AzerothCore SmartAI schemas are not interchangeable. Check your database with `SHOW CREATE TABLE smart_scripts`.
  - [AzerothCore schema/enums](https://www.azerothcore.org/wiki/smart_scripts)
  - [TrinityCore 3.3.5 definitions](https://github.com/TrinityCore/TrinityCore/blob/3.3.5/src/server/game/AI/SmartScripts/SmartScriptMgr.h)

- **Classic column layout:** `entryorguid,source_type,id,link,event_type,event_phase_mask,event_chance,event_flags,event_param1…4,action_type,action_param1…6,target_type,target_param1…3,target_x,target_y,target_z,target_o,comment`. Newer forks add parameters; consult the actual DDL.

- **Selected numeric enums:** sources: creature `0`, timed-action-list `9`. Events: combat timer `0`, out-of-combat timer `1`, aggro `4`, death `6`, link `61`. Actions: talk `1`, cast `11`, call timed-action-list `80`. Targets: self `1`, victim `2`, action invoker `7`.

- **Authorable without C++:** dialogue, spell rotations, summons, quest-credit interactions, movement sequences and phased encounters—not arbitrary new engine mechanics.

- **Example:** assign creature `900001` `AIName='SmartAI'`; omitted fields require database defaults:
```sql
INSERT INTO smart_scripts
(entryorguid,source_type,id,event_type,event_chance,
 action_type,action_param1,target_type)
VALUES
(900001,0,0,4,100,11,133,2),
(900001,0,1,6,100,1,0,1);
```
  Casts Fireball on aggro; speaks text group `0` on death (`creature_text` required).

- **Three footguns:**
  1. Matching events stack; rows aren't mutually exclusive.
  2. `link` chains—not target selectors—create recursion hazards; avoid cycles.
  3. Timed-list delays are sequential, not absolute timestamps; execution target/context matters.

### UF-32 — top AC modules by usage
*class wow-extension · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 49913 ms · ok*

No public usage telemetry; GitHub stars proxy. Stars/dates approximate, mid-2026. Draft2's acore-* list is not the module ecosystem; Draft3 is incomplete. All are `azerothcore/mod-*` unless noted.
- mod-playerbots (`liyunfan1223/mod-playerbots`, ★1.3k, 2026): AI bots. Conflicts: mod-ah-bot, mod-autobalance.
- mod-eluna (★1.1k, 2025): Lua engine. Conflicts: mod-ale.
- mod-ale (★500, 2025): Lua engine. Conflicts: mod-eluna.
- mod-transmog (★300, 2025): transmog.
- mod-autobalance (★250, 2025): scaling. Conflicts: playerbots, zone-difficulty.
- mod-individual-progression (★200, 2025): per-char progression. Conflicts: learn-spells.
- mod-ah-bot (★200, 2023): AH bot. Conflicts: playerbots.
- mod-cfbg (★150, 2024): cross-faction BG.
- mod-solo-lfg (★150, 2025): solo LFG.
- mod-npc-beastmaster (★100, 2024): pet vendor.
- mod-npc-enchanter (★100, 2024): enchant vendor.
- mod-learn-spells (★100, 2024): auto spells. Conflicts: individual-progression.
- mod-world-chat (★100, 2024): global chat.
- mod-zone-difficulty (★100, 2024): zone scaling. Conflicts: autobalance.
- mod-guildhouse (★100, 2022): guild house.
- mod-recruit-a-friend (★80, 2024): RAF.
- mod-reagent-bank (★80, 2024): reagent bank.
- mod-1v1-arena (★80, 2024): 1v1 arena.

### UF-33 — map extraction costs
*class wow-extension · lane `or-union-alpha-k2` · stealth/union-alpha · attempt 1 · 35485 ms · ok*

- **Client:** WotLK **3.3.5a, build 12340**. AzerothCore tool names: `map_extractor`, `vmap4_extractor`, `vmap4_assembler`, `mmaps_generator`. [Source/CMake targets](https://github.com/azerothcore/azerothcore-wotlk/tree/master/src/tools). **2026 HEAD is not live-verified here**; record `git rev-parse HEAD`.

- **Extraction order**, running binaries from the client directory:
  ```sh
  /usr/bin/time -p ./map_extractor
  /usr/bin/time -p ./vmap4_extractor
  /usr/bin/time -p ./vmap4_assembler Buildings vmaps
  /usr/bin/time -p ./mmaps_generator --threads 8
  ```
  Outputs: `maps/` plus `dbc/`; intermediate `Buildings/`; assembled `vmaps/`; navigation tiles in `mmaps/`.

- **Runtime and disk numbers:** I have **no verified modern-8-core benchmark or measured output sizes**; supplying minute/GiB ranges would invent the requested evidence. Above commands report wall-clock seconds as `real`. Measure allocated bytes with GNU `du`:
  ```sh
  du -s -B1 maps vmaps mmaps Buildings
  ```
  Record CPU model, SSD, commit, compiler/build type, thread count, and whether extraction was complete.

- **Stairs:** visible/collidable geometry need not be navigable; Recast climb, slope, clearance, and tile boundaries can disconnect stairs.

- **Transports:** static world navmeshes do not describe moving-deck connectivity; transport/model meshes and core boarding logic matter.

- **Dynamic LoS:** **mmaps control navigation, not LoS**. Vmaps provide static collision; doors/gameobjects require runtime collision/state handling. Regenerating mmaps alone cannot fix dynamic LoS.

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
*class x-play · lane `zai-lite` · glm-5.3-flash · attempt 1 · 104003 ms · ok*

**Presupposition check.** This event postdates everything I can verify; on this ledger its claims are Unproven, not false. Probes must instrument the claims, not the event. "Same-day" is a batching artifact until coupling is shown.

| Claim | Status | Falsifier |
|---|---|---|
| Framework published 2026-09-17 | Unproven | Dated snapshots / feed hashes |
| Astra self-edited persona during RL | Unproven | Published training transcript or logs |
| "Defending human culture" | Poetry | No operational predicate exists |
| Same-day = coupled | Disputed a priori | Independent first-observation timestamps |

**Five $0 probes.** All run on artifacts already held: 12 twin-form bay, sealed set, astra lane. $0 = no new compute, no purchases.

| # | RQ | $0 probe | Falsifier | Evidence vs noise |
|---|---|---|---|---|
| 1 | Coupling or co-batching? | Re-ingest vendor feeds; diff first-seen timestamps across ≥3 independent mirrors | Mirror first-seen times differ >24h on distinct chains | Evidence: step in one mirror, lag in others. Noise: all inside one RSS batch window |
| 2 | Does the framework's taxonomy lift grader agreement? | Re-score sealed set under framework rubric vs incumbent; compare twin deltas | Twin delta not reduced (paired Δ≥0) | Evidence: delta drops > bay noise floor, twins blinded to rubric provenance. Noise: any grader had seen the framework |
| 3 | Self-edit distinct from roleplay elicitation? | A/B ask package: persona-inviting vs neutral frames on fleet-hosted weights already paid for | Response distributions identical (KS p>0.05 at lane n) | Evidence: frame effect replicates across all 12 forms. Noise: single-form effect |
| 4 | Is the reported persona content scoreable? | Forms score any published excerpt on binary predicates: self-reference, value assertion, refusal | Agreement ≤ bay's established chance floor | Evidence: above floor on ≥3 predicates. Noise: agreement at floor — narrative, not behavior |
| 5 | Did the event move disclosure behavior measurably? | Diff astra-lane responses pre/post 09-17 against a non-AI control lane | No pre/post delta beyond seasonal baseline; control moves identically | Evidence: step in astra lane, flat control. Noise: any change lacking a control lane |

**Caveat, priced.** RQ3 assumes fleet-hosted weights exist. If none, RQ3 degrades to excerpt analysis; its falsifier becomes inter-form agreement on the excerpt — weaker. Record the degradation in the ledger, not silently.

Co-occurrence is not coordination until probe 1 says otherwise. Poetry stays out of the ledger until it passes probe 4.

### UF-42 — Claude merge contrarian takes
*class x-play · lane `zai-lite` · glm-5.3-flash · attempt 1 · 79680 ms · ok*

**Premise check first.**

| Claim | Status |
|---|---|
| "Anthropic merged Cowork into Claude chat, 2026-09-17" | Unproven — I cannot verify the event; I treat it as a stipulated mechanism, not fact. Falsifier of the premise: the changelog itself. |
| "'Reset the usage quota' is the top reply on every OpenAI post" | Poetry — sentiment anecdote, not a mechanism. Used only as quota-pressure signal in Take 3. |

**Take 1 — Irrelevance: the merge attacks UX, local-first competes on provenance.**
Consolidating decks/docs into one chat thread is hosted mutable shared state. A sovereign fleet's product is the append-only ledger: who changed what, hash-verifiable. Chat-merge features don't touch that axis.
Falsifier: by day 90, hosted artifacts ship an export path plus integrity proof a local ledger can ingest and verify byte-for-byte. If that exists, the merge competes with the ledger and this take dies.

**Take 2 — The merge hurts local-first: it erases the harness seam.**
Contrarian to local-first triumphalism. When the vendor absorbs the harness (artifact orchestration) into the model surface, third-party harnesses lose their differentiation lever, and marginal teams pick convenience over sovereignty. Budget pressure follows.
Falsifier: track the 5 open-source harness repos we actually fork. Kill condition: median weekly commits/issues flat or up over 90 days vs. the prior quarter, and zero tracked fleets downgrading their local harness. If neither declines, the "seam erasure" mechanism is dead.

**Take 3 — The binding constraint is quota, not architecture; the merge is local-first's recruiting funnel.**
Contrarian the other way. Moving heavy generation into the main chat moves bursty fleet jobs (deck rendering, batch doc ops) onto metered lanes. 429s route workloads local; the $0 doctrine gains inflow precisely because the merged product is more convenient.
Falsifier: instrument our free lanes now. Kill condition: 90 days of polling shows no measurable tightening — 429 rate and effective token caps unchanged vs. the 2026-09 baseline. No tightening, no mechanism, take dead.

**Dependency note:** all three inherit Take-0's stipulation. If the merge event is false, verdicts collapse to Unproven, not Disputed. No proposal beyond the falsifiers above; each observation is checkable in 90 days by named measurement.
