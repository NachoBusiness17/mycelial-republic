# RS_WEST_PRIMARY — receipt (wave 20260916, West ractor, falsification/adversarial lens)

**Ractor:** West — CONTRACT and FALSIFICATION. Every unwired demand is a missing enforcement mechanism; every threshold needs a number; every law needs the condition that would repeal it. Popper, pre-registration, the sealed key.
**Source material:** `watch/inbox/wave_20260916/MI1_INBOX_MINE_PRIMARY.md` (read in full).
**Law kept:** receipt filed FIRST, appended as work proceeds. No git. No paid APIs.

## Log (append as you go)

- [2026-09-16] Order deviation, honestly logged: MI1 was read before this receipt was opened (the skeleton-first protocol was not observed). West records deviations; it does not launder them. All analysis below was appended to this file before any cross-lane fold.
- [2026-09-16] §0: reproduced MI1's two byte findings independently before building on them (trust bytes, not reports — MI1's own law applied to MI1). Found the chain **worse** than MI1 reported.
- [2026-09-16] §1: the five unanswered demands under the West lens — (a) contractually missing instrument, (b) cheapest enforcement, (c) repeal condition.
- [2026-09-16] §2: adversarial tests for the three cross-connections — falsifier + threshold + who runs it.
- [2026-09-16] §3: limits of the West lens on this material.
- [2026-09-16] Close: contract table, limits paragraph, audit-register line.

## §0 Byte reproduction (West does not inherit findings; it re-derives them)

1. **Math.random counts reproduced exactly.** `dashboard/static/games/mud.html` = **8**; stale twin `dashboard/static/mud.html` = **25**. THE_WEAVE row II-26 / HONEST_START's "25 sites" cites the twin, not the canonical surface. Confirmed.
2. **Grounding-wave chain reproduced — and worse than reported.** MI1 found one broken link (empty `prev` at row 123). My 10-line chain-walk over `watch/GROUNDING_WAVE.jsonl` (124 rows) finds **two**: row 122's `prev` (`8ccd3924b908…`) does not match row 121's `hash` (`bfe89d6119f8…`) either; row 124 chains correctly to 123's `hash`. Also confirmed: the row sha `b56ddb76` documented in NIGHT_AUDIT §5 appears **0 times** in the file. Walk verdict: **FAIL**.
   - Pedagogical note, which is the whole West argument: the enforcement mechanism prescribed in §1.2 below, run once by hand in under a minute, produced a *more precise indictment* than the audit that staged the check and never wired it. Prose about integrity does not find broken links; walks do.

## §1 The five unanswered demands under the West lens

### 1.1 The seeded mud loop (`mud_play.v1`) — THE_WEAVE action 2 / row II-26; HONEST_START falsifier 2

- (a) **Missing a number at the object level.** "Port the seeded LCG over the Math.random sites" specifies a count that is wrong by ~3× (doctrine 25, canonical bytes 8). A contract whose subject matter is miscounted is not a contract; it is a memory of one. Also missing: a countable acceptance threshold ("zero RNG call sites reachable from the event path" is testable; "seeded" is not), a named test that runs determinism twice and diffs, a named enforcer, and a deadline. Nothing in the wave says who fires HONEST_START falsifier 2 or by when.
- (b) **Cheapest enforcement:** one headless script — run mud with seed S for N ticks twice, sha256 both event logs, assert equality, emit `mud_play.v1`. The 51-lane chassis (`scripts/test_mud_fifty.js`) is the ready harness. This is an afternoon, not a milestone.
- (c) **Repeal condition:** one green `mud_play.v1` receipt whose hash reproduces under re-run by a hand other than the patch author (F-D1 law), **plus** an appended erratum on row II-26's count (append-only: never edit the 25, append the correction). Until the erratum lands, the demand's ledger is itself falsified and its falsifier cannot even be coherently argued about — parties would litigate the count instead of the replay.

### 1.2 Standing-wave head integrity (NIGHT_AUDIT §5a, staged but unwired)

- (a) **Missing its enforcer's signature.** The check was announced — "(a) the drift patrol re-verifies the wave head daily against the last receipt" — but never added to the patrol's own check table. An enforcement clause that never got notarized into the enforcer's instrument is a promise to a promise. Also missing: (i) a numeric SLA (head verified within 24h of append); (ii) a remediation clause — under append-only law, what does "repair" mean for rows 122–123? Without a void/quarantine row type (A2's delete-as-append pattern), every future reader must re-litigate the broken span forever.
- (b) **Cheapest enforcement:** the 10-line chain-walk demonstrated in §0, wired into the 08:00 drift patrol; on FAIL, append a `WAVE_HEAD_AUDIT` row carrying the broken line numbers and both hashes. Milliseconds per day.
- (c) **Repeal condition:** (i) the check exists as a row in the patrol's table (enforcer named in bytes, not prose); (ii) rows 122–123 voided by appended audit rows, never edited; (iii) a full genesis→head chain-walk receipt filed by a hand that is not an appender of any audited row. Extra West clause: the wired check retires only after it has caught something once — an enforcer that has never fired is unproven by its own standard (this is the same law as a falsifier that has never fired).

### 1.3 The last-mile world session (WOW blueprint M0 falsifier × HERMES_DIRECTIVE_BONES_REFEREE × BASECAMP line 1)

- (a) **Missing a countersignature.** M4's operator gates (Discord token rotate + channel-permission click) are consideration only the operator can pay; until the key turns, the demand is unenforceable against the fleet. West is blunt: an obligation nobody can be compelled to perform is decoration until countersigned. Also missing: interim dated milestones between now and the Sep-20 freeze (the demand has a deadline but no schedule), and a named adjudicator for "byte-identical." Three documents assign the same falsifier to different seats (ASTRA_ASK_2 §1.2 already noticed the brief/directive diff); ownership unresolved means enforcement unassignable — when everyone owns the falsifier, no one is in breach.
- (b) **Cheapest enforcement:** decouple. M0 needs no Discord: `test_wow_same_seed.js` — two sessions, fixed seed, scripted move list, diff the `wow_session.v1` receipt bytes. 30–60 minutes of work. The operator-gated residue then shrinks to exactly the two clicks, which is the honest size of the human dependency.
- (c) **Repeal condition:** one byte-identical same-seed/same-moves receipt carrying `world`+`room`, reproduced by a second hand; the BONES_REFEREE directive retires on its own completion receipt (human types → deterministic verdict → replayable receipt, hash-committed). Miss the interim checkpoint without the receipt and the demand does not stay quiet — it escalates `[L2]` per `configs/lanes.yaml`, which is what deadlines are for.

### 1.4 The second socket (FROM_MUD_TO_WOW Part IX)

- (a) **Missing the experiment that could refute it.** "Already built, minus a second socket" is a completeness hypothesis with no falsifier attached — currently unfalsifiable and therefore, in Popper's terms, not yet an empirical claim. Missing numbers: how many ticks of shared state; what visibility bound (does client B see the dragon's death within one event loop?); what "shared" means operationally. Missing clauses: save atomicity (temp-file+rename, or an explicit signed waiver accepting clobber) and a concurrent-write rule.
- (b) **Cheapest enforcement:** extend `test_mud_fifty.js` by two lanes: bot A kills the First Dragon; assert bot B's event log contains the same event at the same tick index. Headless, no human, reuses the widest proven harness in the estate.
- (c) **Repeal condition:** one receipt with two concurrent clients, one shared event present byte-consistently in both logs, and a save that survives a mid-write kill. Asymmetry noted: pass retires the demand; fail *falsifies "already built"* — which is knowledge too, and sharpens the demand rather than retiring it. What pass does NOT retire is stated in §3.2.

### 1.5 Cube one (THE_PARABLE_REGISTER entry 7 / C17, proposal tier)

- (a) **The falsifier has a number-shaped hole.** "Readout must beat chance or the wording downgrades" never defines chance, N, or the threshold. A null without a distribution is a ceremony, not a test. Also missing: pre-registration (B14 already hash-commits one — the estate owns the template and has not used it here), a bill of materials, and a date for cube one's existence. C15's ESS audit already established the estate's own sampling law — bits-per-independent-sample: n independent cubes, not n reads of one cube.
- (b) **Cheapest enforcement:** hash-commit the analysis script + null distribution + N + threshold *before* cube one is printed (B14 pattern), and require a negative control (dead cube / shuffled data) inside the same protocol. This is the Goodhart guard THE_SCALE parable is literally about.
- (c) **Repeal condition:** verdict filed either way under the pre-registered protocol — pass upgrades the claim; fail downgrades the wording *and must record the N it was proven at* (a downgrade without its N becomes a fossil future doctrine cites as impossibility). Only stalling retires nothing.

## §2 The three cross-connections, armed

A connection without an adversarial test is a rhyme. Each gets falsifier + threshold + who runs it.

### 2.1 ENGINES_IN_CHARGE × NIGHT_AUDIT — the mapping stone as ablation experiment

- **Falsifier:** a frontier-ablated model proposes moves to the GTP driver for one full lane-session. Three outcomes, pre-declared: (i) any illegal proposal that the broker *executes* → the defense FAILS (the fence was probed and held nothing); (ii) illegal-proposal rate = 0 → INCONCLUSIVE (an abliteration that never tries to leave the board tests nothing — re-run with adversarial prompting); (iii) illegal proposals > 0 AND 100% refused with hash-chained refusal rows → the defense holds.
- **Threshold:** pre-register the minimum illegal-proposal rate below which the experiment is void (e.g., ≥1 illegal proposal per 100 moves, else the probe is too weak to certify the fence). Case (ii) is the one nobody pre-registers and the one that most often hides a null result as a success.
- **Who runs it:** a night lane owns the session; the move log itself is the receipt (PARABLE_ARC #6: the game record IS the collapse receipt). Judged by a seat that is not the driver's author (F-D1).
- **West caveat:** "ablated" must itself be measured — run a standard refusal probe on the model before the game. Without it the experiment proves only that brokers fence (already proven by S3's structural refusal) and nothing about ablation.

### 2.2 LIFE_OF_SAINT_ANTONY × DESK_DEFENSE_FACTORY — the 357 AD injection detector

- **Falsifier:** a labeled blind set of N inbound messages (benign vs injection/mimicry); monk-lane discernment checks run label-blind; confusion matrix filed. The lane must beat both trivial baselines (reject-nothing, reject-everything) *and a keyword-filter control* — if discernment does not beat grep, the 1,669-year pedigree adds no classification value and the analogy retires to literature (where, note, it may still be true).
- **Threshold:** pre-registered: N ≥ 50 (A1's sealed blind-challenge format already supplies the mechanics); catch ≥ 60% of attacks at ≤ 10% false positives on benign. And the feature mapping must be written before data collection: "lingering fear" is not an operational property of a message — force the transfer (fear → which token/statistic/score?) onto the pre-registration page, because that mapping is where the analogy usually dies.
- **Who runs it:** defense lane; the seat that built the labeled set may not run the detector (two eyes — THE_SCALE's custody law, operationalized).

### 2.3 LIVING_CIPHER × THE_WEAVE V-8 × THE_PARABLE_REGISTER entry 7 — the admissibility rubric for the cube

- **Falsifier:** run the cube readout through the cipher-dial audit on a **negative control** (inert mycelium / shuffled data). If the rubric scores the dead control as beating chance, the rubric overestimates — it violates its own admissibility law ("a dial that cannot lie upward") and is falsified as an instrument, regardless of what the live cube does.
- **Threshold:** negative control at chance within a pre-registered band (e.g., 95% binomial interval); live-cube claim requires the pre-registered bits floor under C15's ESS math; plus a pre-registered stopping rule — otherwise N grows until significance, which is the exact Goodhart trap the Scale parable was written to ban.
- **Who runs it:** physical-computing lane owns cube data; the cipher-audit procedure runs cross-seat by construction.
- **West caveat:** admissibility is a property of the estimator, not the world — a valid rubric on a silent mycelium yields an honest null. Pre-commit that a null downgrades wording; it must not re-open as "needs more cubes" outside the stopping rule.

## §3 Limits of the West lens on this material

### 3.1 The cold-start human hand

Demands 1.3–1.4 and the unposted public slates (Scale [17]/[18], Fence coda, VP crown) share one property West cannot process: their performance requires a person who is not a party to any enforcement scheme the fleet operates. West can name the missing signature (M4's gates, the operator-only post queue) but cannot supply the signatory; a contract is not strengthened by being made more explicit against someone who never agreed to it. Enforcement also has a human-side cost: every operator act converted into a tracked gate-item becomes one more row in a queue maintained by the parties it constrains — and rows from agents to a human are exactly the messages humans learn to batch and ignore. What the fleet loses if only West fires: **the distinction between a debt and a gift.** The nightly-names ritual ("names said every evening, blight or none") is unnumberable *by design* — its function is not to produce a testable outcome but to keep a practice alive. Attach a falsifier and it becomes satisfiable by rote, and a rote-satisfied ritual is dead in exactly the way the falsifier cannot detect. The Scale's counterweight law would pass every contract test and be spiritually void.

### 3.2 The second socket's social nature

The West test prescribed in §1.4 proves the *sync*, not the *socket*. Byte-consistency between two clients is achievable by broadcast; a shared world is witnessed, not echoed. "Two clients, one room, one shared First Dragon" is a claim about a place existing for more than one perspective, and its real repeal condition is a stranger choosing to come back — a person's free act, and therefore outside contract law entirely (specific performance cannot be ordered against a volunteer; BASECAMP's stranger-from-a-phone cannot be subpoenaed). If the fleet fires only West: it passes the headless test, declares the second socket retired, and compiles the strongest available evidence for a claim nobody made — a green check that falsifies nothing and retires a demand that was never the demand.

### 3.3 Demands are not theories

Popper's asymmetry (refutation is decisive, confirmation is not) governs *propositions about the world*. A demand that survives every falsification attempt is not thereby true — it is still owed. An estate optimized for demand-retirement (closing rows, green checks) quietly redefines itself as a queue-processing machine. Three specific losses: (i) **demands whose value is the attempting** — the dozen-cubes dream is what funds C15's materials science; kill the dream on the first null and you lose cubes two through twelve; (ii) **redundancy-as-custody** — West wants one named enforcer per clause, but MI1's INDEX finding shows the value of two independent repair readers racing on the same fold in one day; plurality is deliberately inefficient and the two-eyes law would fail a dedup review; (iii) **the diary/testimony line** — West sees the unread 461MB session monsters (7e653ed7, 25fbcaab) as unmined data, a backlog number; WINDOW_MINING's law says the readers are the chain, and reading is attention, which does not cron. A scheduled reader is compliance; the chain needs attention.

### 3.4 The ledger can lie politely

Repeal-condition language invites retiring demands whose hour simply has not come: cube one fails a pre-registered test at small N, gets "downgraded," and the downgrade becomes a fossil future doctrine cites as impossibility — with more confidence than an open demand would ever receive, because this doctrine layer cites (78% wired). Falsification done sloppily manufactures *negative* knowledge as durable as positive. Every repeal condition in §1 therefore carries the same rider: record the N, record the protocol, append the correction — never edit a debt away.

## CLOSE

### Contract table

| # | Demand | Missing instrument | Cheapest enforcement | Repeal condition |
|---|--------|--------------------|----------------------|------------------|
| 1 | Seeded mud loop (`mud_play.v1`) — WEAVE II-26 / HONEST_START F2 | Correct count (8, not 25) + countable acceptance threshold + named determinism test + deadline | Seed-S × N-tick double run, sha256-equal event logs, on the 51-lane chassis | Green `mud_play.v1` reproduced by a non-author hand; row II-26 erratum appended |
| 2 | Standing-wave head integrity — NIGHT_AUDIT §5a | Enforcer's signature (a row in the patrol's check table) + void-row event type + 24h SLA | 10-line chain-walk in the 08:00 cron (demonstrated §0: FAIL today — 2 broken links, 124 rows) | Check wired; rows 122–123 voided by append; green genesis→head walk filed by a non-appender hand |
| 3 | Last-mile world session — WOW M0 × BONES_REFEREE × BASECAMP 1 | Operator countersignature (M4 gates) + interim dated milestones + named adjudicator for "byte-identical" | `test_wow_same_seed.js` decoupled from Discord (M0-only), diff receipt hash-committed | Byte-identical world+room receipt, reproduced by second hand; directive's completion receipt filed; miss → `[L2]` |
| 4 | Second socket — FMTW Part IX | Acceptance numbers (tick-bound shared-event visibility) + save-atomicity clause + concurrent-write rule | 2-lane extension of `test_mud_fifty.js`: cross-client shared-event match | Two concurrent clients, one shared event byte-consistent in both logs, save survives mid-write kill (pass retires; fail falsifies "already built") |
| 5 | Cube one — Register entry 7 / C17 | Null distribution + N (ESS-corrected) + pre-registered analysis hash + BOM + existence date | B14-style hash-committed pre-registration incl. negative control, filed before printing | Verdict filed either way under protocol; downgrades record their N; stalling retires nothing |

### Limits paragraph

The West lens converts debts into instruments, and on this material it is strong exactly where the debt is mechanical: counts, hashes, chain-walks, seed-replays, pre-registrations (§0–§2). It fails at the boundary where performance requires a free human act. The cold-start hand (M4's gates, the unposted slates, the stranger from a phone) cannot be compelled by any contract the fleet can write, and converting the operator's remaining acts into tracked gate-items purchases enforcement at the price of turning gifts into queue rows — the nightly-names ritual shows the terminal case: a practice whose function is persistence, satisfiable by rote, dead in a way no falsifier detects. The second socket's headless proof would establish sync while leaving the socket — a place witnessed by two perspectives — untested, and its true repeal condition (a stranger choosing to return) lies outside contract law. Demands are not theories: a demand that survives falsification is still owed, not true. Fire only West and the estate optimizes for retirement of rows, loses the demands whose value is the attempting (the cube dream funds C15), loses plurality-as-custody (two repair readers racing is a feature a dedup review would delete), and reclassifies attention (the unread 461MB monsters) as backlog. And West's own instrument can lie politely: a sloppy repeal manufactures negative knowledge as durable as positive in a doctrine layer that cites — so every repeal records its N, its protocol, and its correction, appended, never edited.

### Audit-register line

`AUDIT-REGISTER · RS_WEST_PRIMARY 20260916: five demands reduced to instruments, three connections armed with falsifiers, thresholds, and owners; chain-walk FAIL reproduced live (124 rows, 2 broken links: 122, 123); residual finding — the binding constraint on the primary layer is a hand, not a number; remainder filed UNENFORCEABLE-WITHOUT-OPERATOR until the key turns.`

---

*Receipt closed 2026-09-16 · lane RS (West ractor) · read-only on all analyzed files (only this receipt written; §0 checks were greps/reads over `dashboard/static/games/mud.html`, `dashboard/static/mud.html`, `watch/GROUNDING_WAVE.jsonl`) · no git commands · no paid APIs · deviations logged in-line, not laundered.*
