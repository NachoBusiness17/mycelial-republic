# EPISTEMIC GAP SENSOR  -  designing the estate's nervous system (deep-epistemic-gap, flash50, 2026-09-28)

## 1. The diagnosis, byte-backed

The paired drops arrive in this repo as a ledger row, not as folklore. `watch/inbox/LINKS.jsonl` row seq `1790591389126114` (2026-09-28T10:29:49Z, writer `operator-drop-what-llms-are`, canonical_sha256 `089B99F9...F8A5D7C`) records the pairing: Qivshi pushes back on "we don't understand LLMs"  -  we know HOW (a multidimensional image of human language reflecting likeliest continuation), what we lack is WHY so well; it is not thought. NachoQuixotic sharpens: statistical grammars manufacturing language from language, semantics from syntax from co-occurrence, no world; **hallucination = treating a closed corpus as reality**; the medieval Kabbalah precedent (letter combination *produces* rather than *mirrors*  -  the Abulafia line of ecstatic permutation practice). The same row names the estate corroboration: "the percolator echo (203,000 phantom counts), FKB hysteresis, and the entire no-fabrication law exist because closed-corpus reflection is exactly what these machines do."

Read carefully, that diagnosis contains its own remedy. If the failure mode is *closure*  -  the model reading only what the model wrote  -  then the cure is not better prose but **scheduled contact with bytes the model did not write**, at instrumented tolerance, with an alarm when contact fails. That is a module, not a virtue. This document designs it.

## 2. The estate already built four point-instruments (all read this session)

The sensor does not start from zero. Four organs already exist, each invented reactively after a specific epistemic wound:

1. **`tools/drift.py:50-91`**  -  the metric-referent drift instrument. Born from METRIC_REFERENT_TRIANGULATION_20260918: five fleet documents measured their RATE OF CHANGE and called that orientation while the truth instrument sat unbuilt. Its core is `drift_check(metric, referent)`: Pearson correlation of the deltas, `corr(dM, dR)`, emitting verdicts VACUOUS / ALIGNED / DRIFTING / INVERTED / DEGENERATE / INSUFFICIENT. Its own law line (`tools/drift.py:90-91`): "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers 'is it moving north'."
2. **`tools/freshness_check.py`**  -  two sensors in one file. (a) The boot-doc stale-trap gate: a doc is STALE when its last commit is older than `STALE_DAYS=7` while the repo has heartbeat (`HEARTBEAT_DAYS=2`, `tools/freshness_check.py:53-54`). (b) The per-tool-result freshness receipt (`receipt()` at :111, `stale_claim()` at :160): every observation carries `observed_at` + `source_hash` + a carried bar (default 900s), and `stale_claim(rec, source_path=...)` **re-hashes the world** before letting a claim through; missing receipt, future-dated receipt, unreadable source, and drifted hash all fail closed (:171-192). This is the estate's receipt theory made executable: a receipt is *justification*; the re-hash is *truth-testing*; without the second leg you hold Gettier cases, lucky-true belief.
3. **`tools/census_drift_patrol.py:2-64`**  -  the claim-carrier tripwire (B2-215). Motivating wound, quoted from its own docstring (:4-8): the estate hand-carried the "1,341 tests / 264 files" headline for 12 days while tests/ grew 31 files, because no gate watched the carrier. Its bar is the conjunction the whole design rests on: stale = **census date older than 7 days AND world moved since that census** (:10-21). Inside the window, lag is tolerated and reported as evidence; outside it, alarm. The `--collect` deep check (B2-244) closes the file-growth blindspot: items added inside existing files are invisible to git, so the carrier can read 1,837 while reality holds 1,879 (a delta of 42 measured live on 2026-09-26, :53-56); tolerance is `COLLECT_DRIFT_TOLERANCE = 20` in either direction (:125). Exit codes are the house convention: 0 inside bar, 1 actionable drift, **2 = cannot-verify, never a guess, never a pass** (:30-32).
4. **`tools/drift_pairs_stamp.py:1-95`**  -  the teleological layer. Six pairs (T1-T6), each a fleet metric paired with a FILED referent (lane trails vs LINKS rows, training events vs release milestones, fold steps vs burn receipts), stamped weekly and idempotently to `memory/runs/adv_arc_50/teleo_drift_stamps.jsonl`. Its aging guard (B2-66, spec written before code, :51-88) is an epistemically mature move: `REFERENT_MATURE_DAYS = 7`; an ALIGNED verdict on a 2-day-old referent downgrades to FRAGILE-ALIGNED because "a correlation whose referent has less history than the stamp's own cadence is not proven, it is provisional" (:65-67).

A fifth organ is the capture side: `mag/state_snapshot.py:74-106` appends structured state summaries (deduped by state_hash) to `memory/pile/state_summaries.jsonl`  -  the estate's *internal model* stream, the thing the sensor will compare against the world.

## 3. What I ran this session (all green, outputs verbatim)

- `./.venv/Scripts/python.exe tools/freshness_check.py` → `FRESHNESS: PASS  -  boot docs inside the bar.` heartbeat 0.0d; BOOT_4_7.md and state/HANDOFF.md frozen-ok with dated reasons; EXIT 0.
- `./.venv/Scripts/python.exe tools/census_drift_patrol.py` → EXIT 0: census 2026-09-27 (2303 collected / 352 files), 5 files grown since census **each named**, disk 369 vs carrier 352 reported as instrument lag, "same-window lag, evidence only."
- `./.venv/Scripts/python.exe tools/drift_pairs_stamp.py --status` → 18 rows (3 v1 + 15 v2), weeks W38-W40 stamped; embedded `regime_trail_staleness` tripwire: 2 days since last gate, `alarm: false`.
- `./.venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check` → `index_state: fresh` (the FTS5 index vs catalog.jsonl gate: bytes+mtime cheap tier, sha256 audit tier, `tools/corpus_fts_rebuild.py:11-24`).
- A live `drift_check` demo → see section 8; it found a real blindspot in instrument #1.

## 4. The design: a claim registry measured by an observation registry

**EPISTEMIC GAP SENSOR = `tools/epistemic_gap_sensor.py` (design; not landed this pass).** One sentence: it compares the estate's *asserted model* (every durable claim the estate would act on) against *fresh observation* (re-measurement at instrumented tolerance), on a cadence ladder, with fail-closed alarm semantics.

### 4.1 What it compares

**CLAIM.** A claim is any durable assertion with five fields: `carrier` (the path it lives on: AGENTS.md census bullet, boot docs, INDEX.json fold-integrity lines, warm_state.json, state/CURRENT.md, teleo stamp verdicts), `grammar` (the regex that parses it  -  e.g. `CENSUS_CLAIM_RE`, `tools/census_drift_patrol.py:117-119`), `observed_at` (the census date / receipt stamp), `instrument` (the operator that re-measures the truth), `tolerance` (the verdict thresholds). The estate already proved claims must be grammatical to be checkable: the B2-245 fix (parser took prose numbers as the claim, :84-95) and the B2-249 carrier shape law (rewording the bullet breaks the gate instead of silently rephrasing it) mean **claim grammar is authored, not audited**  -  the sensor enforces that a claim written without its parseable shape fails at write time, not 12 days later.

**OBSERVATION.** An observation is one instrument run stamped as a freshness receipt (`observed_at`, `source_hash`, bar) in exactly the `freshness_check.py:111-133` shape, so any later consumer can re-hash before trusting. Instruments tier by cost, inheriting the two splits the estate already measured: cheap = git + disk bytes only, no venv, pre-push safe (census patrol default, :37-38; FTS bytes+mtime tier); deep = re-execution (`pytest --collect-only`, sha256 over catalog), venv required, cron-only.

**THE GAP.** Three families, each an existing verdict vocabulary, each with its own wound as precedent:

- **G1 AGE-GAP** (wound: the 12-day headline). Claim age vs world movement. Fires only on the conjunction old-AND-moved; lag inside the window is reported as named evidence, never alarm.
- **G2 VALUE-GAP** (wound: the 42-count invisible drift). Re-measure, diff, fail at tolerance in either direction. Two house laws bind it: the B2-216 denominator law (never difference counts from different instruments or moments; name instrument, moment, delta) and the attribution rule (B2-216 again): **an unattributable drift is a fabrication smell**  -  the alarm must carry the expected-vs-actual table and the named landings, or it escalates rather than resolves.
- **G3 COUPLING-GAP** (wound: the percolator echo, section 7). `corr(dM, dR)` on the teleo pairs, with the aging guard. INVERTED alarms immediately; VACUOUS alarms on a second consecutive window (a referent that has not moved yet is not yet a lie); DRIFTING alarms on trend across windows, not on a single weak corr.

### 4.2 How often (the cadence ladder)

The sensor does not add a scheduler; it hangs off the heartbeat that already exists:

| layer | cadence | hook that already exists | what runs |
|---|---|---|---|
| cheap G1 | hourly | the burn cron | git + disk bytes over all carriers, no venv |
| medium G1+G2 | daily 08:00 | drift-patrol-cron (automation-a7c71ad1, DRIFT_PATROL_20260928.md:3) | named carriers re-measured, FTS `--check`, regime staleness tripwire |
| deep G2 | daily 08:30 | MagCensusPatrolDaily (`scripts/census_patrol_daily.ps1`) | `--collect` full re-execution, tolerance 20 |
| G3 stamps | weekly | `tools/drift_pairs_stamp.py` (idempotent per ISO week, W38-W40 already stamped) | T1-T6 verdicts + aging guard |
| event | every push | ratchet hook | carrier grammar + claim co-update (B2-274 ownership law generalized: grammar changes are spec changes with receipts) |

Cost law inherited from the estate's own finding: a sensor that needs the venv never sits in the pre-push path (census_drift_patrol.py:59-61).

### 4.3 What triggers an alarm

1. **INVERTED** (corr <= -0.5): metric rises while referent falls. Immediate, exit 1.
2. **VACUOUS x2**: two consecutive windows where the referent never moved while the metric moved. The metric is measuring nothing that matters; exit 1.
3. **G1 conjunction**: carrier older than its bar AND world moved under it; exit 1 with the named growth rows.
4. **G2 tolerance breach**: re-measurement off the claim by >= tolerance in either direction; exit 1; attribution table required in the alarm payload.
5. **FRAGILE-ALIGNED unhealed**: an ALIGNED verdict still standing on a referent past maturity without re-stamp; exit 1 (the provisional form expired).
6. **CANNOT-VERIFY (exit 2) is itself the alarm**: missing carrier, unparseable grammar, git failure, future-dated claim. This is the estate's deepest convention and it is load-bearing: fail-closed is not conservatism, it is the recognition that an unverifiable claim is exactly the state in which closed-corpus reflection happens.
7. **DARK SURFACE (negative receipt)**: the 2026-09-28 patrol found the secret gate itself crashed  -  a name-rebound RecursionError that fail-closed and froze ALL pushes since e60b4e801, silently (DRIFT_PATROL_20260928.md:27-29). Lesson: every layer emits a heartbeat row when it runs *and* the absence of the row is detectable ("no START stamp for today means the surface is dark" is already law for the FTS task in AGENTS.md). The sensor's first alarm is therefore a meta-alarm: sensor did not run.

Alarm routing reuses the pile habit: exit 1/2 rows append to `memory/pile/state_summaries.jsonl` via `mag.state_snapshot.capture_summary(kind="escalation")` and surface in `memory/attention.md`; verdict flips on filed claims (REFUTED-ON-REPLICATE precedent, FW-15/FW-05) stay operator-gated  -  the sensor detects and proposes, the operator authorizes truth-status changes.

## 5. Retrodiction: the design against the estate's three known hallucination episodes

A design earns belief by explaining known wounds. Each known episode maps to one alarm class:

- **Percolator echo (2026-09-18).** The percolator's top invariant counted **203,000** (grew ~500 overnight) while `explore.jsonl` held **1,433 rows in 38 days**  -  "echo-arithmetic, not recurrence," ~142 counts per event; verdict filed as "the meter lies by multiplication" and raw counts demoted to provenance (`watch/inbox/NIGHT_FOLD_20260918.md:25-30`). Under EGS: pair metric=invariant count, referent=explore.jsonl row count; delta-M huge, delta-R ~0 → **VACUOUS in one window**, alarm class 2. The operator-authorship receipt generalizes the lesson: "drift is NOT stopped  -  it is now DETECTABLE BY THE THING ITSELF... Percolator's 203,000 phantom counts and 9.3-day fossil packs could lie for weeks; the estate now feels itself move" (`memory/continuity/seat_memory_20260927/operator-authorship-question-20260927.md:29-31`).
- **The stale headline (2026-09-14 to 09-26).** 1,341/264 riding 12 days while tests/ grew 31 files → G1 conjunction, alarm class 3, exit 1 at the first hour where both legs held. This is the case the census patrol already catches; EGS generalizes it from one carrier to the registry.
- **The gate that died silently (2026-09-28).** Secret-gate RecursionError, fail-closed, pushes frozen, nobody paged until the patrol opened the log → alarm class 7, dark-surface meta-alarm, exit 2 as incident.

## 6. The monotone blindspot: found by running the instrument this session

My demo run exposed a real hole in `drift.py`. Three synthetic pairs:

```
inverted      metric=[1,2,3,4,5,6] referent=[6,5,4,3,2,1]  -> DEGENERATE (corr None)
vacuous       metric=[1,2,3,4,5,6] referent=[3,3,3,3,3,3]  -> VACUOUS
insufficient  metric=[1,2,3]       referent=[5,5,5]         -> INSUFFICIENT
```

The first row is the finding: perfectly anti-correlated **monotone** series have zero delta variance, so Pearson is undefined and the verdict is DEGENERATE, not INVERTED (`tools/drift.py:74-76`; variance denominators at :45). But perfectly monotone divergence is precisely the nightmare case: a vanity metric climbing in lockstep while its referent decays linearly, forever, no alarm. The EGS therefore adds a rank-coupling fallback for the DEGENERATE case: Spearman rho on the deltas (rank correlation survives zero variance in *values*, though not in ranks) plus a plain sign-agreement fraction over deltas (fraction of windows where sign(dM) == sign(dR)); sign-agreement 0.0 over >= 3 windows is INVERTED by monotone evidence. Two-line fix in a wrapper module, no change to the pure core, whose "reads nothing, writes nothing" boundary (`tools/drift.py:27-28`) stays intact.

## 7. The anti-reflexivity clause: who sensors the sensor

The drops' warning applies to the EGS itself. A gap sensor is itself a producer of claims ("all carriers inside bar"), and if it becomes a closed corpus  -  reading only its own past verdicts  -  it re-creates the disease at one level up. Four defenses, all already house style:

1. **Frozen witnesses (B2-274):** the EGS's regression vectors are never auto-synced to the live carriers; a frozen wrong-looking number is the only witness that can catch a grammar break.
2. **Self-test without world-writes:** the freshness_check.py pattern (:196-264)  -  no network, no repo writes, fails on garbage input rather than inventing a receipt.
3. **No self-certification:** an EGS verdict is evidence about carriers, never about the EGS; its own accuracy is measured the way every other metric is, by a new teleo pair (T7: EGS alarms vs operator-confirmed incidents, corr(dM, dR) weekly). If alarms do not track confirmed incidents, the sensor itself goes VACUOUS or INVERTED against its referent. This closes the infinite regress the way metrology does: not with a final unverified link but with an unbroken calibration chain terminating in a human-anchored standard  -  here, the operator's testimony, the founding event the authorship receipt names.
4. **External anchors where possible:** the byte layer is not fully closed. T3's referent class ("externally anchored LINKS rows: rows carrying a src/source/author field," drift_pairs_stamp.py:19-21) and the drop-capture rows themselves (the sha256-stamped LINKS row for the drops) are contact with text the estate did not write. The estate knows its letters produce rather than mirror; so it anchors to bytes it did not write whenever the world offers them, and says so when it cannot.

## 8. Honest limits (what this design cannot do)

- **G3's referents are internal ledgers.** Coupling-gap is second-order epistemics: it detects the estate's metrics decoupling from the estate's own filed records, not from the world. The only out-of-estate ground truth the sensor can touch is the externally-anchored layer and live probes (Vercel URLs 302 through SSO and must be `curl -I`-verified per AGENTS.md  -  a standing example of a claim surface that lies without the probe).
- **Tolerance is a guess until measured.** The census patrol's 20 is calibrated against a live-measured 42; the EGS's per-carrier tolerances start there and must be re-derived from each carrier's measured landing velocity, or they are theater.
- **I did not land the module.** This ask is a design item; `tools/epistemic_gap_sensor.py` does not exist in the tree, and the ratchet/gate family plus the spec-before-behavior discipline would put its spec (this file) before its code in a later, separately-gated pass. The four existing sensors ran green this session; the seventh pair, the sign-agreement fallback, and the registry consolidation are proposed, not built.

## 9. The literature the design stands on

- **Bender & Koller 2020 (ACL), "Climbing towards NLU":** the octopus argument  -  meaning cannot be learned from form alone; a system trained on form is a "stochastic parrot" (Bender et al. 2021, FAccT). This is the academic twin of the drops' "manufacturing language from language, no world," and it says the deficit is structural, not a bug awaiting a patch.
- **Kalai & Vempala, "Calibrated Language Models Must Hallucinate" (arXiv:2311.14648; ICLR 2024):** even a perfectly calibrated LM hallucinates at a rate lower-bounded by the prevalence of singleton facts in the training corpus. Hallucination is not noise to be reduced but a structural property of closed corpora  -  the theorem-shaped version of NachoQuixotic's line. The estate's consequence follows: the goal cannot be elimination, only instrumentation. (The estate already discovered the same shape locally: the census carrier can be fully honest and still drift, because a snapshot is a snapshot.)
- **Ji et al. 2023, ACM Computing Surveys, "Survey of Hallucination in NLG":** intrinsic vs extrinsic hallucination; faithfulness-to-source vs factuality-to-world. The EGS is literally an extrinsic-factuality instrument for a non-LLM speaker: the estate's "language" is its receipts.
- **Conant & Ashby 1970, "Every good regulator of a system must be a model of that system" (Int. J. Systems Science):** the estate is a regulator; its state docs, indexes, and counts are its model; a model drifting from the system is a bad regulator by theorem. The EGS measures regulator-model adequacy.
- **Gama et al. 2014, ACM Computing Surveys, "A survey on concept drift adaptation":** drift detection families (error-rate, distribution, distance). G1/G2/G3 map cleanly: staleness detection, re-execution error detection, distribution coupling.
- **Popper, "Conjectures and Refutations" (1963):** the falsifier habit (FW-15's named falsifier, the FW-05 pre-registered mechanical rule at `artifacts/salon_ess_replicate_20260916.py:210-215` per Q-020) is Popper operationalized; the EGS extends it from single hypotheses to the standing claim registry.
- **Korzybski, "Science and Sanity" (1933):** the map-territory relation; the census carrier IS a map, the collection IS the territory, and B2-215 was a map-territory incident with a 12-day half-life.
- **The Kabbalah precedent, held correctly:** Abulafia's letter-permutation practice treated generated text as revealing rather than mirroring. The drops use it as the mirror-image warning; the estate's answer is neither to forbid generation nor to trust it, but to date-stamp it, hash it, and schedule its falsification.

## 10. Module sketch (design shape; every spawn honors the windowless law)

```python
# tools/epistemic_gap_sensor.py -- proposed surface
@dataclass
class Claim:    carrier: Path; grammar: re.Pattern; observed_at: str
                instrument: str; tolerance: float
@dataclass
class Observation: value: float; observed_at: str; source_hash: str; tier: str  # receipt shape, freshness_check.py:111

def measure(c: Claim) -> Observation: ...          # runs c.instrument, mints the freshness receipt
def gap(c: Claim, o: Observation) -> dict: ...     # G1 age-gap / G2 value-gap / G3 coupling verdict
def monotone_sign_check(metric, referent) -> dict: # section-6 fallback: sign-agreement over deltas
def alarm(reports) -> int: ...                     # 0 / 1 / 2, payload = attribution table
def heartbeat(layer: str) -> None: ...             # negative-receipt: absence is detectable
# any subprocess: subprocess.run(argv, shell=False,
#   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
```

The registry seeds with the four carriers the estate already patrols plus the teleo ledger; T7 (EGS alarms vs confirmed incidents) joins T1-T6 at the next weekly stamp; the operator gate covers verdict flips only. Nothing in the sketch writes on its own initiative; the fail-closed convention is inherited from all four parents, and the one thing it refuses to inherit is their silence.

**Transcription note:** house law bans em-dashes; the 25 em-dashes in this file's first draft (including inside verbatim quotes of estate text and tool output) are transcribed above as spaced hyphens.

**Banked:** `watch/inbox/burn_reset_20260927/flash50/deep-epistemic-gap.md` · checks run this pass: `freshness_check.py` (EXIT 0), `census_drift_patrol.py` (EXIT 0), `drift_pairs_stamp.py --status` (EXIT 0), `corpus_fts_rebuild.py --check` (EXIT 0), `drift_check` monotone demo (DEGENERATE finding). Not run: full pytest suite (ask names no suite; this is a design item, no code landed).
