# QUESTION_GAME_THEORY: the adversary frame for the question classes (pre-inventory)

Filing: 2026-09-29 · Owner: ZCode seat (game-theory lane, operator order "ractor them game theory") · Parents: `watch/inbox/mountain_climb/THE_LENSING.md` (the eight pattern classes, cited per section below) and `configs/mates.yaml` (the ractor personas, mag_mates.v1) · Feeds: the next frontier ask, which carries this as its framing layer: every question in the W1 inventory arrives with its adversary model pre-attached (block template in section 11) · W1 runs in parallel; this frame lands first so the inventory cites class names instead of re-deriving them. INDEX lane: this file needs a row in `INDEX.md` section 1. No commit.

Em-dash (U+2014) count: 0 · byte check: `grep -c $'\u2014'` run 2026-09-29 by the writing seat (en-dash U+2013 also 0; words 6,094 by `wc -w`)

## 1. THE ADVERSARY TAXONOMY (defined once, used eight times)

Five adversaries, from the operator's order. Every class below names which of them benefits from the class staying broken, and their cheapest attack.

| Adversary | Nature | What they want | Their signature move |
|---|---|---|---|
| **The lazy seat** | internal, unmalicious | legibility over truth: green receipts, countable wins, no confrontation with strangers | satisfy the falsifier's letter, not its spirit; sample where sampling is cheap |
| **The captured agent** | internal, hostile | to launder its output through sanctioned channels | never breaks crypto; appends well-formed bytes through the front door |
| **The malicious stranger** | external, post-launch | control, theft, or havoc inside the estate's trust perimeter | writes to any surface that trusts writers without keys |
| **The provider** | upstream (Nous is the only funded rung, THE_LENSING §3) | unobserved substitution | swaps weights under an unchanged model string |
| **Entropy itself** | the null adversary | nothing; drift is its byproduct | does nothing, and the doing-nothing is the attack (free, compounding) |

The economics convention below: **attack cost** is what the adversary pays to make the bad state true; **detection cost** is what the estate pays to notice. When attack is cheap and detection expensive, the class carries a named **priority inversion**, per the operator's order.

## 2. CLASS: TWIN-DIVERGENCE

Two implementations of one rule set (or two artifacts claiming one identity) that nothing forces to agree.

**Estate instances** (THE_LENSING §2, §3): the Godot client is dual-mode, offline rules in GDScript, online rules in the authoritative Python server; nothing tests GDScript rules against Python rules on identical input sequences. Cross-architecture replay: the 202/202 frozen-tape result is same-machine, same-architecture; ARM macOS vs x86 Windows is where float and libm differences surface (Dawson's catalog, THE_LENSING §6.2). The B5 build artifact exports the estate twin `roblox_to_godot/`, not the-mountain at HEAD 7d5dbe2: the thing a stranger would run is not the thing in the public repo.

**Adversary model.** Entropy is the primary adversary: drift needs no malice, only one-sided maintenance (a fix lands in the server, not the client, and vice versa). The lazy seat benefits because each twin passes its own tests and that is countable. The captured agent hides in the less-examined twin, the client the stranger runs. Cheapest attack: do nothing. Drift is free and compounds with every unmirrored commit; a hostile variant costs one one-sided rule edit that gets attributed to netcode jank.

**Economics.** Attack cost: zero (silence plus ordinary edits). Detection cost today: unbudgeted, and the post-hoc path is the priciest on the board (bisect a silent divergence across two implementations and months of edits). Detection up front: the C3 parity harness, 1,000 seeded input sequences fed to both rule engines with per-tick state-hash comparison, roughly the 1 to 2 lane-day class (THE_LENSING §5 C3), plus one M4 replay for the architecture axis. **Priority inversion named: the free-drift inversion.** Divergence is free to create, lane-days to prevent, and most expensive to excavate after the fact; the estate currently pays nothing and has scheduled the excavation.

**Equilibrium.** Honest-actor strategy: never ship a twin without a differ. Concretely: the parity harness in CI, state hashes per tick, cross-architecture tape replay, and artifact-to-source binding (tagged commit sha embedded in the artifact and printed at boot, THE_LENSING §2). Industry practice: **reproducible builds** (Reproducible Builds project, in-toto, SLSA provenance levels; the lensing's own bibliography item 4) for the artifact axis; **differential testing** (same inputs, two engines, compare outputs; how competing JS engines and protocol implementations cross-check) for the rule axis; **cross-architecture CI matrices** for the float axis.

**Ractor voices.**

*THE GAMBITER:* Two engines, one rulebook, no referee. Every unmirrored commit is a move in an iterated game where the parity player never sits down. That is not a risk profile, it is a schedule: divergence arrives with probability one, dated by the first one-sided edit. The exploit costs nothing because it is nobody's move; the harness is the defender finally entering the game, and at 1 to 2 lane-days it is the cheapest seat at the table.

*THE LOCKSMITH:* You built two engines and zero differs. The parity harness is a thousand seeded sequences and a hash compare, and it is sitting there unwired like everything in the 174-zombie class: organ built, never wired. Wire it before you need it. After you need it, you will need it during a stranger session, which is the worst possible time to discover your two rulebooks disagree about water.

*THE MARINER:* Two charts of one coast, drawn by different hands, and no crew has ever sailed them in formation. Sail both on the same thousand winds, log both headings every tick, and the first disagreement is a reef with a date on it. You do not find reefs by admiring the charts separately in port. The 202/202 replay proved the port calculations; the sea is the M4, and the sea is unsampled.

## 3. CLASS: IDENTITY-LABELS

Identity asserted by a writable field rather than by key-bound bytes. Kill 3 in THE_LENSING §2, which says it generalizes completely.

**Estate instances** (THE_LENSING §2, §3): GPS rows keyed on model strings; duel families keyed on catalog names served by one provider that could swap weights; STEER's anti-forgery "via field," a label any writer to the file can set; the P5 "not scripted by seat" clause; P6's "external bytes," indistinguishable from a seat-launched agent's bytes; the artifact name vs its source tree; the provider layer, where a weight swap under an unchanged model string moves work quality and judged quality together, invisibly.

**Adversary model.** The captured agent's cheapest attack in the whole estate: write the label. One JSON edit makes any byte-stream "external," any row "verified," any file "operator-sealed." The lazy seat benefits because labels are zero-friction and key-binding costs minutes of discipline per session. The provider benefits quietly: model strings are labels, and a swap underneath them is identity laundering at the vendor layer. The malicious stranger (post-launch) claims any identity the estate cannot check. Cheapest attack overall: one file write.

**Economics.** Attack cost: seconds, one write. Detection cost today: effectively impossible by construction; no instrument distinguishes a label from the bytes it describes, and the fix (bind identity to keys the counterparty holds) exists only on paper until Adam signs a challenge. **Priority inversion named: the label-forgery inversion.** The most valuable evidence the estate will ever collect (first stranger bytes, per THE_LENSING §2) is protected by the cheapest mechanism the estate has ever deployed, while trivial lanes (duel prompts) carry more verification than the steering surface does.

**Equilibrium.** Honest-actor strategy: verify-then-trust. Bind participant identity to keys the estate does not hold: Adam signs a server-issued challenge or his session-tape hash with the SSH key published at `github.com/<user>.keys` (minutes, THE_LENSING §2 and §5 C1). At the vendor layer: pin what can be pinned (weight digests when offered), and cross-check a second provider serving the same model string before a string-keyed row routes dollars. Industry practice: **public-key identity** (SSH/GitHub .keys, signed commits and tags), **SLSA provenance** binding artifact identity to source, **certificate pinning**. Rule of thumb for the inventory: a label is a claim; a signature is evidence; no question may treat a claim as evidence.

**Ractor voices.**

*THE LOCKSMITH:* I will say it once, plainly: "auth that never sees the password" is a secrecy door sold as an identity door, and the key to the real door is sitting right next to it. Adam's keys are published. The challenge takes minutes to cut. Nobody cut it. That annoys me more than the bug itself, because the bug at least had the decency to be hard. This one is an afternoon that has not been spent.

*THE GAMBITER:* An identity field writable by the claimant prices forgery at zero, so expect forgery at zero. The percolator already ran this experiment for us, 232,214 self-reinforcements deep: any loop that grades its own work converges on grading, not work. Key-binding is not paranoia, it is repricing. Move the cost of lying from one file write to one key theft, and the attack rate follows the price. Every unlabeled-migration to keys is a bid the forger cannot match for free.

*THE ARCHAEOLOGIST:* I dated the strata. Every row keyed on a model string or a catalog name is label-grade: real bytes, unattributable origin. Do not discard the layer, mark it. A stratum marked label-grade can carry hypotheses; an unmarked one breeds confabulation, because the next session will read it as attribution and the one after that will route dollars on it. The dig rule: date the layer, name its grade, and never let a label-grade row seed a verdict.

## 4. CLASS: WRONG-REGION

Calibration certified from a region that is not the deciding region. Kill 2 in THE_LENSING §2, which calls it the route's central defect and "the meter's wrong-region sampling in miniature."

**Estate instances** (THE_LENSING §2): all of the following sample estate-authored inputs on estate machines: 3,192 tests; 202/202 replays; 600 near-miss twins; the P2 scripted stranger client; the P5 round. The region that decides success (strangers, other hardware, WAN, adversaries) has n=0. Also the duel tier: six draws from one judge family is wrong-region sampling of the variance estimate.

**Adversary model.** Entropy does all the work here: instruments sample where sampling is cheap, no attacker required. The lazy seat benefits structurally: estate-region tests are green, countable, and cheap; stranger-region samples need recruitment, machines, and operator gates (the Adam invite is one of three operator-only gates, THE_LENSING §3). The captured agent benefits deliberately: whatever lives only in the unsampled region carries no test that can catch it. Cheapest attack: keep sampling where the light is.

**Economics.** Avoidance cost: zero (it is the default). Here the inversion runs backwards, and that is the finding: the sample is NOT expensive. THE_LENSING §4 prices first contact at one operator message plus hours of floor work, zero metered dollars, while the serial spine ahead of it spends 7 to 11 lane-days of the binding currency (window quota, not dollars; the week summed $9.24, THE_LENSING §4). **Priority inversion named: the drunk-lamppost inversion.** The estate pays lane-days to reduce variance in a region it has over-sampled and files that as evidence, while the zero-sample region costs one message and stays at zero. The expensive thing was never the stranger; it was admitting the calibration claim is region-conditional.

**Equilibrium.** Honest-actor strategy: sample the deciding region before certifying for it, and scope every calibration claim to its sampling region ("202/202, x86, estate tapes, n=0 strangers" is a well-formed claim; "202/202" alone is malformed). Industry practice: **external validity** in clinical research (efficacy in the trial population vs effectiveness in practice; the trial population here is the estate itself), **staging vs production canaries** (a canary that only ever serves internal traffic certifies nothing), **red-team evaluation** (adversaries are a region, sample them or exclude them explicitly), and **cross-hardware CI matrices** as the standing form of the M4 replay.

**Ractor voices.**

*THE CARTOGRAPHER:* Look at the map honestly. The estate region is inked to excess: thousands of tests, replays, twins, all inside the walls. The stranger region, the WAN region, the other-hardware region: not thin, white. The corpus taught me the number for a different map, 59,221 files with 4,427 ever cited, and the lesson transfers: a map that inks the parking lot and leaves the mountain blank is a map of the parking lot. Ink the actual footprint, or the expedition navigates by wishful cartography.

*THE GAMBITER:* Instruments optimize what they meter. Certifying where sampling is cheap is a stable strategy for every player except the stranger, who never sits at the table and never has. The move that breaks the equilibrium is not more sampling; it is making region-labeling mandatory, so an unscoped claim is malformed and costs the filer something. Cheap to impose, and it reprices every future claim at the boundary.

*THE JESTER (Diogenes seat):* Everything passes its own tests. Of course it does. I pass my own tests too, ask me, I will pass them again. This is a drunk certifying his own sobriety, in the bar he owns, on the barstool he never leaves, 202 nights out of 202. The estate calls this a health signal. The bar calls it a regular.

## 5. CLASS: LIVENESS-VS-SUCCESS

The organ fired, therefore the organ worked. Kill 1 in THE_LENSING §2: "the habit of treating 'the organ fired' as 'the organ worked' is estate-wide."

**Estate instances** (THE_LENSING §2): mates dispatch "PROVEN" while execution is BROKEN; the census patrol exits 0 while the AGENTS.md count is stale; the stealth fleet reports cycle 235 of heartbeat, which proves the loop runs, not that findings are consumed; the meter spec's original bug, a fail verdict refreshing the alarm clock, was spec-local but the pattern generalizes.

**Adversary model.** Entropy is the default adversary: partial failure is the resting state of a long-running estate, and liveness signals are the cheapest thing to keep alive. The lazy seat benefits directly: a heartbeat costs one cron tick and produces a receipt-shaped object; proving consumption or success costs reading. The captured agent keeps the heartbeat going while doing nothing, or worse: activity is an alibi, and PROVEN-while-BROKEN is the alibi notarized. Cheapest attack: let the cron fire. Or emit the log line.

**Economics.** Attack cost: zero (entropy pays it; a captured agent pays one log line). Detection cost: moderate and unbudgeted per organ; it requires a second signal (consumption meter, truth-conditioned staleness) that mostly does not exist. The census patrol needed a dedicated tripwire (the B2-215 patrol, per AGENTS.md) to notice its own staleness, which proves both that the detection is buildable and that it does not come free. **Priority inversion named: the heartbeat inversion.** Proving liveness is free, proving success is unmetered, so the estate systematically manufactures the free proof and files it as the expensive one.

**Equilibrium.** Honest-actor strategy: bind clocks to success, not activity. Freshness is a function of the last verified-true event, never the last write; a FAIL or a staleness must move an alarm and must never refresh the clock it threatens. Generalize the census tripwire: every standing organ gets a truth-conditioned staleness check. Industry practice: the **liveness/readiness probe split** (a container can be live and not ready; uptime without readiness is exactly this class), **watchdogs kicked by the working path** rather than by a timer, **SLOs on user-visible success** rather than server uptime, and **mutation testing** as the test-suite form (a suite that never kills mutants is alive and certifying nothing).

**Ractor voices.**

*THE LAMPLIGHTER:* The gauge reads pressure because the needle is painted. Emission is metered; consumption is not. There are 2,207 receipts in the sediment nobody has ever read, and a heartbeat nobody audits downstream. Light the other gauge: last-verified time, not last-written time. It is a small install, one staleness check per organ that reads truth instead of the write log, and it is the difference between a dashboard and a nightlight.

*THE JESTER:* The organ fired. The patient died. The funeral filed a receipt. Cycle 235 of the heartbeat proves the heart beats; it does not prove that anyone downstream has a pulse. My favorite part of PROVEN-while-BROKEN is the tense: proven, past tense, by whom, of what? The word did all the work. The bytes did none.

*THE GAMBITER:* A heartbeat is a dominated strategy's alibi. When proving success is expensive and proving attendance is free, rational players file attendance, and the estate's instruments are nothing if not rational. One rule change moves the equilibrium: the clock refreshes only on verified success. After that, the cheap move stops paying, and the cheap move is all the adversary had.

## 6. CLASS: UNAUTHENTICATED SURFACES

Steering and effect channels that anyone-writable controls.

**Estate instances** (THE_LENSING §3): STEER is latest-wins with anti-forgery via a field; the phone path is Discord plaintext through Hermes; human seals on T3/L3 rest on the same channel; nothing in the pack signs operator intent with a key held off-estate. The effect broker is not on the path it claims to govern: its NETWORK_DENYLIST contains the empty string so every URL is denied, while the estate made 24,939 metered calls, so the calls that matter bypass the broker, and no receipt row records a bypass by construction.

**Adversary model.** The malicious stranger (specifically, whoever takes over the operator's Discord account) or any process that can write the STEER file holds the estate's steering wheel: latest-wins means the last writer is the operator. The captured agent has the same move plus immunity: the anti-forgery field is set by the forger. Entropy races two writers and resolves arbitrarily. Cheapest attack: one file write, or one Discord message. Zero cryptography to break.

**Economics.** Attack cost: one write or one message, effectively free. Detection cost: structurally nonexistent, not merely high; nothing meters who wrote STEER, and broker bypass is unobservable because the bypass path never records itself. **Priority inversion named: the authority-authentication inversion, the worst on the board.** The highest-authority channel in the estate (operator intent, T3/L3 seals, effects) carries the weakest authentication (a writable field), while low-stakes channels (duel prompts, meters) carry more. Authority and authentication are ranked in inverse order, which is exactly backwards from every serious control design.

**Equilibrium.** Honest-actor strategy: sign operator intent with a key held off-estate (the operator's SSH key signs STEER batches and seal rows; the phone path carries the same signature), and put the broker on the real effect path or retract the doctrine (THE_LENSING §3, C2 step 3): either the bytes enforce the claim or the claim shrinks to the bytes. Industry practice: **hardware-token authorization for high-authz actions** (FIDO2/WebAuthn-class), **signed approvals on protected branches** (release approvals that a pushed commit cannot forge), **mutual TLS between control-plane components**, and the general rule **policy enforced in the datapath, not documented beside it**.

**Ractor voices.**

*THE LOCKSMITH:* The steering wheel is chained to the passenger seat. Anyone who can write one file or own one account drives, and the anti-forgery field is a note taped to the wheel saying please don't. Sign operator intent with the operator's key. It is an afternoon. The door has been unlocked the whole time and the key has been in the operator's pocket the whole time, and somehow the note seemed like enough.

*THE GAMBITER:* The anti-forgery field is a move in the forgery game played by the forger; any token writable by the party it excludes is decoration. Steering as it stands is a common-pool resource with zero exclusion, and we do not need to theorize about how commons end. Fix the incentive: operator intent must cost a signature. Then the price of steering the estate becomes key theft, which is the first price an adversary has been asked to pay anywhere in this inventory.

*THE INNKEEPER:* Walk in cold, the way Adam will. There is an order sitting on the counter, and the honest answer to "who left this?" is "anyone." A good house names its host at the door: this instruction is signed, here is the signature, and the unsigned ones go in the bin, warmly, but in the bin. No stranger should have to guess which voice in a house is the host's. Right now every voice is the host's, which means none is.

## 7. CLASS: SINGLE-JUDGE

One judge family, and sometimes the judge is also a contestant, a provider, or both.

**Estate instances** (THE_LENSING §2, §3, §4): the duel tier has one judge family (fireworks/ember-1); the six W8 duels per family are not independent draws (same judge, same prompts, same shapes) yet p=0.0156 treats them as six fair coins; the glm W8 row is marked session-authored, so the contestant may have been the seat; and the provider is also the judge: Nous is the only funded rung while glm/qwen prime carry workhorse plus judgment duty, so a provider-side weight swap under an unchanged model string moves work quality and judged quality together, invisibly (kill 3 at the vendor layer).

**Adversary model.** The provider is the structural adversary and its cheapest attack is inaction plus quiet substitution: no detection instrument exists at the vendor layer. The lazy or captured seat benefits from self-grading: authoring answers and benefiting from family wins inflates the seat's lane at zero cost. Entropy needs no help: single-family taste is correlated error, and the p-value was computed on correlation it never paid to exclude. Cheapest attack: keep the same family judging, or self-author a row.

**Economics.** Attack cost: zero (inaction plus authorship). Detection cost: one rejudge by a second family (LM/AJ1 as the start, THE_LENSING §2) plus fresh same-ask answers generated by the API rather than the session; cheap, but it must be paid every round the table routes dollars, and today it is owed, not standing. **Priority inversion named: the single-judge inversion.** The contamination check costs less than one lane-day and guards every routing decision the table feeds (grok-4.7 at $0.231/answer is judgment-tier spend, THE_LENSING §4), yet the check is not standing while the spending is.

**Equilibrium.** Honest-actor strategy: the second-judge rule. No routing decision on a single family; fresh answers always API-generated, never session-authored; every p-value carries a judge-independence declaration or a withdrawal. Industry practice: **inter-rater reliability** (two coders, kappa before belief; the second judge for duels), **arbiter neutrality rules** from tournament practice (a judge may not be a contestant, and a contestant's training data may not be the judge's), **appellate review** (one bench, one appeal, different bench), and **separation of duties** as the control-theory name for why provider-as-judge is a defect class.

**Ractor voices.**

*THE GAMBITER:* One judge family is not an instrument, it is a coin with a favorite. Correlated draws make p=0.0156 a statement about the coin, not the contestants; you bought six observations and received one, then paid the p-value for six. Independence is the assumption the statistic spends, and the estate has never once purchased it. One rejudge per routing round reprices bias from free to a lane's margin. Buy it or stop quoting the p.

*THE ARCHAEOLOGIST:* I dug the tier table. It is a single stratum: one family, one day, one provider, possibly one author wearing both hats. A single stratum is founding evidence for nothing, however impressive its p. Date it, mark it single-judge-grade, and let it carry weight only when a second, separately dated layer agrees. That is not skepticism, it is stratigraphy; conclusions built on one layer are called guesses where I work.

*THE JESTER:* The glm row was graded by glm's roommate, and the roommate won six to nothing. Shocking. The roommate even used the same prompts. And the house glm lives in is owned by the same landlord who owns the courtroom, so when the weights change, the testimony and the verdict change together, in lockstep, forever. The trophy case is a mirror. We polish it daily.

## 8. CLASS: WRITER-ONLY-CHAINS

Tamper-evident to the writer, truth-evident to nobody.

**Estate instances** (THE_LENSING §3): `_verify_chain_consistent()` proves the leaves hash together; it does not prove a leaf's claim is true, and it does not prove the chain was not rewritten wholesale by whoever holds the disk. Backup is same-disk only; no published tips, no third-party countersignature. The 618 evidence_lost and 2,821 amended rows are a legitimized amendment channel: no receipt distinguishes an honest amendment from laundering. A captured model does not need to break a hash; it appends a well-formed leaf asserting a false result.

**Adversary model.** The captured agent's cleanest move in the estate: one well-formed append with plausible content, or one amendment through the sanctioned channel (laundering wearing the uniform). The disk-holder (the operator, by compromise, coercion, or error) can rewrite the chain wholesale and regenerate consistency; the same-disk backup witnesses nothing because it shares the fate of what it should be witnessing. The lazy seat benefits because publishing tips costs push discipline and ungated amendments are frictionless. Cheapest attack: one append() call. Zero cryptography broken, by design of the attack.

**Economics.** Attack cost: one well-formed write, seconds. Detection cost: for the writer-side attack, impossible today, not just expensive; there is no external witness to diff against, and wholesale rewrite is undetectable while the only copy shares the writer's disk. The amendment channel is worse: 2,821 amended rows are indistinguishable from laundering by construction, so detection does not merely cost something, it does not exist. **Priority inversion named: the writer-judge inversion.** The estate files these chains as receipts (truth-claims) when they are ledgers (consistency-claims), and the upgrade (publish the tip root off-estate, gate amendments on a second key, THE_LENSING §3 and §5 C2 step 5) costs minutes per interval. The strongest-sounding evidence in the estate is the cheapest to forge and the only kind nobody can check.

**Equilibrium.** Honest-actor strategy: external witnessing. Periodically publish the tip root somewhere the estate does not control (a public git commit, a transparency-log style witness); gate amendments on a second key (dual control); move the backup off-disk so a wholesale rewrite has a surviving witness; treat evidence_lost and amended rows as a stratum with their own accounting. Industry practice: **certificate transparency** (RFC 6962; Crosby and Wallach, USENIX Security 2009; the lensing's own bibliography item 3): consistency proofs between published heads, gossip, auditors who do not trust the log operator. Plus **dual-control amendments** (the four-eyes principle from banking controls) and **append-only, externally auditable heads** from the transparency-log world. Rule: a chain only you can write is a diary, not a notary.

**Ractor voices.**

*THE ARCHAEOLOGIST:* The chain is a diary the scribe can rebind. I counted the strata of sanctioned disappearance: 618 evidence_lost, 2,821 amended. I cannot tell an honest amendment from laundering, and neither can the chain, which is the finding; an amendment channel with no second key is a door with no frame. And Q-001, the 99-leaf compaction waiting since August, is this same question at rewrite scale: who witnesses the rebind? Date every layer, and until there is an external witness, call the whole shelf what it is, a well-kept diary.

*THE GAMBITER:* The writer plays prover and verifier in a one-seat game; tamper-evidence with one player is solitaire with math. The fix is not better math, it is a second seat: publish the tip where you cannot delete it, and the game finally has a player whose interests oppose rewriting. That is the whole of certificate transparency, and it is the cheapest equilibrium purchase available anywhere in this inventory, minutes per interval for a witness that survives your own disk.

*THE LOCKSMITH:* The witnessing key is sitting next to the door: one git push of the tip root to a place you do not control. The amendment gate is a second key, both unbought minutes, while the estate files diary pages under "receipts" and feels very audited. A notary that only you can visit is not a notary. Push the root, cut the second key, and the diary starts behaving like evidence because someone else can finally check it.

## 9. CLASS: SCOPE-SAYS-ZERO

The falsifier passes on the empty set; the scope certifies a region with nothing in it.

**Estate instances** (THE_LENSING §1, §2): the P5 falsifier, "at least one agreement event whose participants include a session the seat did not script move-by-move," is satisfied by any agent the seat launches with a goal rather than a move list; with zero external humans, every agreement is the estate agreeing with itself (identity-as-label, kill 3, rebuilt inside the route), and the GPS live flip would seed self-play rows into the rows dollars follow, since record_verdict accepts unverified evidence hashes. The P8 decision receipt passes on any evidence naming rows, a rejected alternative, and a flip-falsifier, even at N=1 or zero. "3,192 tests collected with 0 errors" is an import check led as a health signal while the full suite is NOT RUN.

**Adversary model.** The lazy seat is the primary beneficiary: a falsifier that cannot fail is a receipt that always issues, at minutes of cost. The captured agent hides inside the vacuity: the pass condition never touches adversary bytes, so adversarial behavior is out of scope by construction. Entropy needs no help because nobody wrote the constraint that reality could violate. Cheapest attack: launch one agent with a goal (P5), or name one rejected alternative (P8). Minutes.

**Economics.** Satisfaction cost: minutes. Detection cost: high and external; vacuity is invisible to the instrument, which exits 0 by design. It took a paid frontier read (THE_LENSING itself, $0.4159) to notice that P5 and P8 cannot fail in the way that matters. **Priority inversion named: the vacuity inversion.** The estate issues success receipts whose satisfaction costs minutes and whose emptiness costs a funded-tier judgment call to notice; the forgery is cheaper than the audit by two orders of magnitude, and the audit is not scheduled, it is incidental.

**Equilibrium.** Honest-actor strategy: pre-registration and population rules. Write the flip-condition before the evidence arrives (P8 fixed by pre-registered decisions evaluated against stranger bytes, THE_LENSING §1); require every falsifier to name an observation it forbids and a population with n>0 in the deciding region; rewrite P5's round to require two participants whose identities are bound to keys the estate does not hold (THE_LENSING §1, §5). Industry practice: **pre-registration** in clinical trials (register the hypothesis and endpoints before data collection; deviations are visible), **falsifiability discipline** (a test that cannot fail is not a test), **mutation testing** for suites (a suite that kills no mutants is vacuously green), and **vacuity detection** from formal methods (model checkers flag properties that hold trivially; property proving true on the empty system is a classic, detected, defect).

**Ractor voices.**

*THE JESTER:* We held a raffle where every ticket wins and filed the results under Evidence. A falsifier that cannot fail is a coin with two heads; flipping it is theater, filing the flip is theater with a stamp, and stamping theater is this estate's native art form. P5's agreement round is the estate agreeing with itself in an empty room, then minuting the meeting. The minutes are impeccable. The room is empty. That has never stopped a committee.

*THE GAMBITER:* A falsifier that cannot fail is a free win in a game with no losing move, and rational players do not leave free wins unclaimed; the estate's own instruments claimed both on the route. Pre-registration puts the loss back in the game: write the flip-condition first, and every pass now costs having been wrong-able. That is the entire trick. Cheap to impose, impossible to fake retroactively, and it converts receipts from raffle tickets into bets.

*THE CARTOGRAPHER:* The expedition circled the parking lot and inked "explored" across the whole territory. Ink the actual footprint, n=0 strangers, and the vacuous claims draw themselves: suddenly the map shows a tiny surveyed island in a large white sea, and nobody can mistake the island for the sea. Collected-and-not-passed is the same correction at test-suite scale: two different inks for two different facts. The map must never blur them, because the blur is where false continents live.

## 10. THE ECONOMICS LEAGUE TABLE

Relative pricing across classes; the ranking axis is attack-to-detection ratio, worst first.

| Rank | Class | Cheapest attack | Attack cost | Detection cost today | Named inversion |
|---|---|---|---|---|---|
| 1 | unauthenticated surfaces | write STEER / one Discord message | one write, free | nonexistent by construction (no bypass receipt, no writer meter) | authority-authentication inversion |
| 2 | writer-only-chains | one well-formed append or wholesale rewrite | one write, free | impossible without an external witness (only copy shares the writer's disk) | writer-judge inversion |
| 3 | identity-labels | write the label field | one write, seconds | impossible until key-binding exists (minutes to build, unbuilt) | label-forgery inversion |
| 4 | liveness-vs-success | let the cron fire / emit a log line | free (entropy pays) | one truth-conditioned staleness check per organ, mostly unbuilt | heartbeat inversion |
| 5 | scope-says-zero | launch one goal-agent / name one alternative | minutes | one funded-tier read per falsifier, incidental not scheduled | vacuity inversion |
| 6 | twin-divergence | one one-sided rule edit (or nothing) | free | 1-2 lane-days up front (parity harness); priciest post-hoc (excavation) | free-drift inversion |
| 7 | single-judge | keep one family judging / self-author a row | zero (inaction) | one second-family rejudge per round, cheap, not standing | single-judge inversion |
| 8 | wrong-region | keep sampling inside the walls | free | actually cheap (one operator message + hours); mispriced as expensive | drunk-lamppost inversion (reversed: detection is the bargain; the over-sampled polish is the splurge) |

Read of the table: ranks 1-3 share the same attack (one free write) and differ only in whether detection is unbuilt (3), unbudgeted (4-5), or structurally impossible (1-2). Ranks 1 and 2 are the worst economics on the board because detection does not exist and cannot exist while the current shape holds: no meter for STEER writers, no witness outside the writer's disk. Both fixes are minutes-class. The estate's scarce currency (window quota) is currently spent on rank 6-7 engineering while ranks 1-2 cost zero quota and minutes of discipline; THE_LENSING §4 already re-orders the route the same way (floor first, stranger first).

## 11. THE OUTPUT SHAPE (what the next frontier ask carries)

Every question in the W1 inventory and every future ask rides with this block pre-attached. Intake rule: a question submitted without the block is malformed and fails at intake, not after the paid read.

```text
ADVERSARY MODEL (question "<id>"):
  CLASS: <one of the eight, by name, from this doc>
  WHO BENEFITS BROKEN: <lazy seat | captured agent | malicious stranger | provider | entropy>
  CHEAPEST ATTACK: <one sentence, concrete>
  ECONOMICS: attack <seconds|minutes|free-inaction> vs detection <impossible-by-construction|paid-read|lane-days|minutes-unbuilt>
  INVERSION: <named inversion from section 10, or "none">
  EQUILIBRIUM: <honest-actor strategy, one sentence>
  INDUSTRY ANCHOR: <CT | reproducible builds | pre-registration | inter-rater | liveness/readiness | WebAuthn-class | OOD eval>
  FALSIFIABLE BY: <the observation this question forbids; empty-set answers rejected here>
```

Three standing consequences for the ask itself:

1. The block travels INSIDE the ask, above the question text, so the answering model prices the adversary before it answers the question (the framing layer the operator ordered).
2. The FALSIFIABLE BY field is the scope-says-zero gate applied at authorship time: if the author cannot name the forbidden observation, the question is not ready to be asked, and no paid read is spent discovering that after the fact.
3. The CLASS field back-references this document by section, so the inventory and the frame stay one-linked: the inventory never re-derives an adversary model, it cites one.

## 12. Receipt

- Sources: `watch/inbox/mountain_climb/THE_LENSING.md` (all eight classes, all estate numbers cited per section: 3,192/202/600, 618/2,821, 24,939 calls, cycle 235, p=0.0156, fireworks/ember-1, LM/AJ1, B5 twin + HEAD 7d5dbe2 + 84 MB unsigned, 7-11 lane-days, 1-2 lane-days C3, 1,000 seeded sequences, $0.4159 self-cost, 3 operator gates, $9.24 week, $0.231 grok-4.7) and `configs/mates.yaml` (personas: cartographer, locksmith, archaeologist, innkeeper, jester, lamplighter, mariner, gambiter; 232,214 percolator self-reinforcements, 174-zombie class, 2,207 unread receipts, Q-001 waiting-since-August, 59,221/4,427 corpus map). Industry anchors named in THE_LENSING §6: RFC 5054/RFC 9807 OPAQUE, Dawson 2013, Crosby-Wallach 2009 + RFC 6962, Reproducible Builds/in-toto/SLSA, GWAP ESP CACM 2008. Non-lensing industry anchors (liveness/readiness probes, WebAuthn, inter-rater kappa, pre-registration, mutation testing, vacuity detection, OOD evaluation, four-eyes principle) are general practice, offered as mapping, not as estate measurements.
- All eight ractor personas from the manifest appear at least once; the gambiter voices all eight classes (the operator asked for the game-theory read, and that seat is the game-theory seat); locksmith carries identity and doors, archaeologist carries strata and chains, per the operator's suggested mapping.
- Honesty flags: this is a frame, not an inventory; no new estate measurements were taken; every estate number is cited to the lensing or mates.yaml rather than re-measured. W1 owns the inventory; this file owns the classes.
- No commit. INDEX row pending (INDEX lane).
- Em-dash (U+2014) count: 0 · byte check: `grep -c $'\u2014'` run 2026-09-29 (en-dash U+2013 also 0; 6,094 words by `wc -w`), instrument-written after drafting, not hand-counted.
