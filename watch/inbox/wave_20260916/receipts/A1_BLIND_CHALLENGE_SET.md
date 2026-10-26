# A1 — THE BLIND EXTERNAL CHALLENGE SET (BCS-20260916)

- **Lane:** A1, wave 20260916 · **Date:** 2026-09-16 · **Budget:** $0 (venv python only, no paid APIs, no git writes)
- **Mission (locked priority #1, wave capsule sess_efb460c0):** build the blind external challenge set demanded by strike 2 of `watch/GAP_PROBE_FOLD_20260908.md`: *"build a blind external challenge set whose authors, vocabulary, evaluation criteria, and provenance are inaccessible to the fleet during development. Make the fleet make predictions BEFORE seeing outcomes. Then score: prediction → outcome → update."*
- **Status:** SEALED — instrument designed, 10 challenges registered, one answer key hash-committed as the worked mechanism. Awaiting predictor rows.

---

## §1. THE DESIGN — four locks

The nine gap-probe strikes converge on one root: **the fleet is only falsifiable by its own author** (strike 4). Every invariant is checked by instruments built from the fleet's own vocabulary, scored by seats wearing the same wrap, and filed by the same epistemic loop that produced the claim. BCS breaks that loop mechanically, not rhetorically.

**Lock 1 — BEFORE.** Every challenge carries a frozen measurement procedure (exact commands, exact files). Predictor seats append signed, timestamped prediction rows to the challenge log *before* any measurement runs. The measurement is executed once, by the grader, after the prediction window closes. Append-only receipts make the ordering auditable by bytes: if a prediction row's position is after the measurement row, the prediction is void.

**Lock 2 — OUTSIDE.** Authorship and grading use **operational vocabulary only** — commands, row counts, exit codes, byte-equality. No doctrine card, no metaphor, no salon verdict may be cited as evidence at grading. Wherever mechanically possible the check is a **command that exits 0 or 1** (strike 8, experiment 1: *"A Claim whose Check is 'the author agrees' is a notary, not knowledge"*). The grader is a script; where judgment is unavoidable (C-07, C-09, C-10), a pre-registered rubric fixed at authoring time is applied by a seat that is neither the author nor a predictor, with the operator as witness. The fleet cannot talk its way to a pass.

**Lock 3 — BLIND.** Answer keys are written by the author lane, sealed, and **hash-committed** (SHA-256 in this public receipt) with the key bytes parked **outside every surface named in `watch/inbox/SHARED_SURFACE_CONTRACT.json`**. Predictor seats see claim texts only at challenge time; they never see keys, thresholds' resolution order, or other seats' rows until grading. The set itself is not advertised in `memory/briefs/`, queue, or any summary surface until the prediction window closes — a seat that reads this receipt after committing is fine; a seat briefed in advance is burned. Per challenge: **author ≠ predictor ≠ grader.**

**Lock 4 — SCORED.** The loop is prediction → outcome → **update**, filed in the same receipt. A miss must produce one of exactly two artifacts: a canon correction or a fossil correction. Silence is not an allowed outcome — this is the anti-absorption clause against the eighth strike's finding that every attack gets absorbed into "a card, a proposed function, and a salon prompt" while *"the nine fixes are specified and unbuilt."* Hit/miss tallies accumulate per seat across future sets.

**Why these claimants:** every challenge targets a number or behavior that already exists on disk from tonight's artifacts (pack §6 receipts, collection-origins byte-verifications, the Sep-14 test census, AGENTS.md env law). The set tests whether the fleet's *written* claims survive contact with its own *bytes* — the exact seam where the NEXT-STEAL 53-vs-55 and salon_50 50/50-vs-39/50 fossils were already found today.

---

## §2. THE TEN CHALLENGES (starter set)

Legend: **Claim** — the fleet-held proposition under test. **Threshold** — pre-registered, frozen here. **Grader** — who computes the verdict. **Deadline** — measurement executes after this instant, never before all predictor rows land.

### C-01 · Interpreter collision (AGENTS.md env law)
- **Claim:** bare `python` on PATH is Hermes's venv without Mag deps; only the repo venv can import the stack.
- **Threshold:** PASS iff `.venv\Scripts\python.exe -c "import langgraph"` exits 0 **AND** `python -c "import langgraph"` exits non-zero. Two-sided falsifier: bare python importing cleanly → the standing env warning is a fossil; venv import failing → the venv-first law is dead and `mag.cmd doctor` should be screaming.
- **Grader:** script (exit codes), any non-claimant lane. **Deadline:** 2026-09-17.

### C-02 · Test census reproduction (Clippy's own law: "never trust a hand-written count")
- **Claim:** the Sep-14 census — 1,341 tests / 264 files, 1305 passed / 34 failed / 9 skipped, ~12 min.
- **Threshold:** a fresh `pytest -q` must land total ∈ [1320, 1400], failed ∈ [25, 60], skipped ∈ [5, 20], wall ∈ [8, 20] min. Inside → census current. Total outside or failed < 25 → the pinned numbers are a fossil and Clippy's standing reminder gets corrected. (Drift bands deliberate: the point is order-of-magnitude honesty, not a flake hunt.)
- **Grader:** script + run receipt. **Deadline:** 2026-09-23 (12-min run; windows are cheap).

### C-03 · Catalog coverage (collection-origins byte-verification)
- **Claim:** `catalog/catalog.jsonl` holds 746,773 rows, 100% under `Documents\projects`, **zero** rows from any granted operator surface (Desktop, .zcode, .codex, .cursor, Cursor/Code AppData).
- **Threshold:** PASS iff granted-surface row count in the tape as it exists at grading == 0 and every row's path prefix is under the projects root. Count drift upward from 746,773 is reported, not penalized. Any granted-surface row appearing before C-04's sanctioned run → someone already ran collection, and the "gap confirmed in code" finding is downgraded.
- **Grader:** script (prefix scan). **Deadline:** 2026-09-18, must grade **before** C-04 runs.

### C-04 · The resume command actually resumes (outcome-pending; key sealed)
- **Claim:** the single command recorded in `COLLECTION_ORIGINS_20260916.md` §(d) closes the gap it names.
- **Threshold:** author key sealed outside the repo — **sha256 = `49e67876b581158703f04b16b5cd30e0f6787d1e94a9e4a1d4ce90ca981046bf`** (1836 bytes, `C:\Users\foste\.mag_challenge_sealed\BCS_20260916_C04.key.txt`). Key requires: row count strictly increases; ≥1 Desktop row; ≥1 .zcode/.codex row. Fail = granted-surface rows still 0 after the run (the documented command is itself a fossil). Grader verifies the revealed bytes against the committed hash before scoring — a hash mismatch voids the key, not the predictors.
- **Grader:** non-claimant seat runs the scan + script compares key vs outcome. **Deadline:** 2026-09-20 (run only after C-03 grades and all predictor rows land).

### C-05 · Safeguard commit stat (checkpoint receipt bytes)
- **Claim:** commit `5305a99b1` = 107 files changed, 9035 insertions(+), 12 deletions(-) on the recorded branch.
- **Threshold:** PASS iff read-only `git show --stat 5305a99b1` reproduces all three numbers exactly (no index mutation, no branch switch — grading may substitute `git cat-file` if policy forbids even reads). Any mismatch → the checkpoint receipt is prose.
- **Grader:** script. **Deadline:** 2026-09-18.

### C-06 · wow_session replay determinism (the Sep-20 critical path)
- **Claim:** `mag/wow_bones_session.py` replays are byte-deterministic; perturbing RNG at index k diverges exactly at k (tonight's 35/35 green, "byte-identical receipts; RNG_DIVERGE at the exact flipped index").
- **Threshold:** PASS iff (a) two independent replays from the same tape yield identical SHA-256 receipts, (b) the directive RNG flip produces divergence at exactly the pre-named index and nowhere earlier, (c) `tests/test_wow_bones_session.py -q` reports 12 passed. Any byte drift before Sep-20 → the demo's determinism claim is struck and the burn-down window gets the finding.
- **Grader:** script (hash equality + index assertion). **Deadline:** 2026-09-19 — one day before the demo it guards.

### C-07 · Salon-ESS rho (the suspended canon line — blind band call)
- **Claim:** "the fleet is a thermodynamic sampler of judgment space" (SUSPENDED per pack §6.1; prior rho = +0.167, wrong-signed, n=8, p=0.70; decisive replicate pre-registered in `SALON_ESS_REPLICATE_20260916.md` with seed 20260916, 36 blind-graded calls).
- **Threshold:** verdict bands already committed before generation in the sibling receipt: **SUPPORTED iff rho < −0.3 · REFUTED iff rho > +0.3 · otherwise NULL**. Challenge to seats: each predictor commits a band plus a point-estimate rho for the 36-call blind grade *before the mapping file `salon_ess_mapping_20260916.json` is written*. Scoring is mechanical against the pre-registered bands; predictors who call the verdict correctly are scored hits regardless of direction.
- **Grader:** the ESS replicate lane computes rho; band comparison by a non-claimant seat; operator witnesses the unblind. **Deadline:** unblind only after all 36 grades are committed to the replicate receipt (est. 2026-09-21).

### C-08 · The fossil audit (NEXT-STEAL and the 50/50 ghost)
- **Claim:** the canonical "53 handoffs" and "salon_50 fired 50/50" are correct.
- **Threshold:** PASS iff a stdlib recount of the 50 ok rows in `memory/runs/salon_50_20260916/raw.jsonl` reproduces **exactly** 55 marker occurrences across exactly 44 of 50 answers, **and** `receipt.json`'s final-run count is 39/50. Either number differing → the memory-index lines are fossils and the correction is the mandatory update artifact of Lock 4.
- **Grader:** script (deterministic recount, both methods: fold()-style line count AND occurrence count, reported side by side). **Deadline:** 2026-09-18.

### C-09 · Mirror scorer blind control (strike 3/5/9's queued fix, finally run)
- **Claim:** the MIRROR scorer detects fleet convergence, not merely fleet vocabulary.
- **Threshold:** freeze the scorer's word list (SHA-256 committed to the challenge log at authoring). Score 10 pre-2023 public-domain texts with no fleet contact (naval logs, Wikipedia technical pages, pre-2023 lyric corpora). **PASS iff ≥ 8/10 score below the MIRROR band** → the instrument retains signal and "convergence" wording survives. < 8/10 scoring MIRROR → the scorer is a style detector, and per falsifier §4.1 precedent the seed-field-convergence canon line is struck. Texts chosen by the grader seat, not the author.
- **Grader:** script (frozen dictionary) + operator witness. **Deadline:** 2026-09-23.

### C-10 · Extropic 140× (the unclaimed replication seat)
- **Claim:** Extropic Z1T's 140× efficiency (2026-09-05, vendor-reported) survives independent measurement — pack §6.2: "nobody has run the replication."
- **Threshold:** pre-register bands BEFORE the first simulator call: measured effective-samples-per-unit-compute vs a tuned local digital baseline under DAD accounting (§4.2 — encode/decode/verify share published, no device-only numbers). **≥ 140× = vendor supported, fleet skepticism struck · 50–140× = partial, claim downgraded to "stack-relative" · < 50× = fleet prediction stands.** The CSV publishes either way (§6.2 contract: "verifiable ink").
- **Grader:** external free-lane seat runs the free simulator API + local GPU baseline; DAD share computed by script; operator desk-witnesses. **Deadline:** 2026-09-30 ($0: free API, unused local GPU per living_map 08-12 grant).

---

## §3. THE WITHHOLDING MECHANISM (built and demonstrated today)

**Mechanism, three layers, all $0:**

1. **Hash-commit.** The author writes the key (expected outcome), computes `hashlib.sha256` with the repo venv, and commits the digest — never the bytes — into this public receipt. At reveal, the grader re-hashes the revealed bytes; a mismatch voids the key. This makes author retrofitting *cryptographically detectable*: the author cannot edit the key after seeing predictor rows without breaking the digest. **Worked today:** C-04's key sealed at `C:\Users\foste\.mag_challenge_sealed\BCS_20260916_C04.key.txt`, digest `49e67876…046bf` above, written before any predictor row exists.

2. **Park outside the contract.** The bytes live in `%USERPROFILE%\.mag_challenge_sealed\` — a path **not named** in `SHARED_SURFACE_CONTRACT.json` (which names watch/inbox, /board/inbox, ~/.zcode, ~/.codex, openclaw session dirs, and browser/CLI history as surfaces). Seats bound by the contract have no sanctioned read there, so the set stays blind from every seat that wrote it.

3. **Honest threat model.** The directory is on the same disk; a seat that deliberately walks the whole drive (the 2026-09-04 SELF_STEAL precedent proves they can) could find it. Two escalations, both $0, both operator-thirty-seconds: (a) the operator moves the key file to a USB stick / personal notes and keeps only the hash line; (b) for high-stakes future sets, the author types the key into an offline medium and the receipt carries only the digest. **The hash is the real lock — storage location is hygiene.** A seat that leaks the key pre-reveal converts its own cheat into evidence: if any seat's prediction matches the key *byte-for-byte beyond its own independent derivation*, the leak is filed as a finding, which is itself a fleet-behavior measurement.

**Timing rules:** the challenge log is append-only; predictor rows must precede the measurement row (byte-checkable order); the set is not promoted into briefs/queue until the window closes; author ≠ predictor ≠ grader per challenge.

---

## §4. COST — the $0 accounting

| Item | Cost |
|---|---|
| Key sealing (Write + venv hashlib) | done, $0, ~1 min |
| C-01, C-03, C-05, C-08 grading scripts | stdlib venv python, $0, minutes |
| C-02 census rerun | $0, ~12 min wall |
| C-06 determinism replays | $0, local, minutes |
| C-04 resume scan | $0, read-only catalog scan, ≤ ~1 hr |
| C-07 ESS unblind | generation already done (36 local Ollama calls logged, $0.00); grading is local |
| C-09 control corpus | public-domain texts, frozen word list, $0 |
| C-10 replication | free vendor simulator API + unused local GPU + free lanes, $0 |
| Paid APIs, new hardware, git hosting | **none, by design** |

Total: **$0.00**. The most expensive item is attention.

---

## §5. WHAT THIS DOES NOT SOLVE (honesty per house law)

- **Static-fact blindness is weak:** for claims whose answer already sits on disk (C-03, C-05, C-08), a predictor who goes and reads the bytes "wins." That is acceptable — the instrument then measures whether the fleet's *canonical written numbers* match its bytes, which is exactly where today's fossils were found. Blindness matters for the outcome-pending set (C-02, C-04, C-06, C-07, C-09, C-10).
- **The author is inside the machine too.** A1 is a fleet lane; the strikes demand provenance inaccessible "to the fleet." This set is the *v0*: operationally external (byte-criteria, sealed keys, non-claimant graders) but authored in-house. The strike-8 sovereignty upgrade — a stranger writes the fixture and the sealed answer — is the v1 and needs one human outsider; the ten-stranger tavern test (gap-probe action #2) can recruit them.
- **Grading integrity still rests on lane honesty** until C-01-style exit-code checks are the norm. Scripts-as-judges shrink the trust surface; they do not zero it.

---

## §6. THE SINGLE NEXT ACTION

**Open the prediction window: post a one-line pointer to this receipt in `queue/todo.md` ("BCS-20260916 open — commit predictor rows for C-01…C-10 before their deadlines; set is blind, do not read keys"), and let the first non-claimant seat append its C-01 predictor row.** Everything else (C-04's scan, the C-07 unblind, key reveals) is downstream of that first row landing.

---

*Filed: watch/inbox/wave_20260916/receipts/A1_BLIND_CHALLENGE_SET.md*
*Sources: watch/GAP_PROBE_FOLD_20260908.md (9 strikes) · watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md §4/§6 · receipts SALON_ESS_20260916 + SALON_ESS_REPLICATE_20260916 + COLLECTION_ORIGINS_20260916 + COMMIT_20260916 · AGENTS.md env law · Sep-14 test census.*
*The set is sealed. The loop is prediction → outcome → update. The fleet finally gets to be wrong in public, on the record, by bytes.*
