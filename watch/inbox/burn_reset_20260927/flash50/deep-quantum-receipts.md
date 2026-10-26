# DEEP ITEM: quantum receipts (deep-quantum-receipts)

- Date 2026-09-28 · seat deep-gopher-deep-quantum-receipts (flash50 workflow gopher) · cost $0 (local reads, one read-only CLI run)
- Question: the estate's receipts are classical (deterministic hash chains). Design receipt states that are SUPERPOSED (provisionally true until observed), ENTANGLED (verifying one verifies its pair), and COLLAPSED (observation changes the state). What problems does this solve that classical chains do not?

## 0. Method: what was read and run for this item

Read in full: `mag/grounding_wave.py` (the GROUND circuit ledger, 975 lines) and `mag/integrity_kernel.py` (the vendored AOS tri-state kernel, 299 lines). Read in part: `mag/verkle_knot.py` (module header, chain tip as succinct root), `mag/policy_engine.py` (the five authorization gates), `mag/renderman.py` (cache entries with ttl and expiry), `mag/seed_registry.py` (the W1 LINEAGE and LIVING-FILE DRIFT laws), `mag/boot_check.py` (`_chain_tip`), and one real burn-reset receipt: `watch/inbox/burn_reset_20260927/queue/Q-020_FW03_grounding_verify.md`.

Ran this session, read-only: `./.venv/Scripts/python.exe -m mag.grounding_wave verify` returned exit 1 with:

```
FAIL LINKAGE-PASS: 137 posts intact, tip=fc3c32be6f26 | truth-gate: 11 witnessed
SUPPORTED, 49 legacy-unwitnessed | row 122: hashless defect contained by void;
row 123: prev defect contained by void; row 129: re-anchored past voided stretch;
row 130: re-anchored past voided stretch; row 131: prev defect contained by void;
row 132: re-anchored past voided stretch | ADMISSION: 3 voided, 0 contested,
0 corroborated, 0 pending voids, 3 propagation-flagged | EVIDENCE-MISSING
row 75:swarm_20260912/smoke_driver.js, row 76:suno/flat_beat_loop.mp3,
row 86:flygomoku_20260912/hermes_mirror_summary.json
```

This byte-matches the Q-020 FW-03 receipt filed 2026-09-28 by a sibling seat. That repetition is itself the first datum: the same measurement over the same chain returns the same FAIL on adjacent days, and the FAIL is about a world OUTSIDE the chain (three evidence files on disk), not about the chain's bytes. Keep that in mind; it is the hinge of the whole design.

## 1. The classical baseline, stated precisely

The estate's receipts are two-layered, and the layers have different physics.

Layer 1, the PREPARATION, is classical and immutable: `mag/grounding_wave.py:160-175` hashes a row as sha256 over versioned canonical key sets (`_row_hash`); every row carries `prev`, and `verify()` (`mag/grounding_wave.py:725-785`) re-hashes the physical tape and fails on any mismatch. `mag/integrity_kernel.py:113-152` (VerkleWitness) is the same shape in miniature: payload_hash and node_hash chained to genesis. The append gate `_admit` (`mag/grounding_wave.py:403-446`) refuses hashless or prev-broken rows at write time. Nothing is ever edited or deleted; delete-as-append is the law (`mag/grounding_wave.py:34-41`).

Layer 2, the STATUS, is neither immutable nor purely classical. A row's verdict ladder (RECORDED, CORROBORATED, CONTESTED, VOID, `mag/grounding_wave.py:48-52`) is computed by `_admission` (`mag/grounding_wave.py:265-347`) as a fixed point over the whole tape: a void counts only once a second seat's witness row signs it (`cross_signed`, lines 277-279); a voided void stops counting (void-of-void reversal, lines 283-291); a witness whose signed row later gets voided becomes a "witness-of-void" propagation flag (lines 336-337). G2 binds evidence files by sha256_12 at post time (`_bind_sources`, lines 217-231) and re-hashes them at every audit (`_evidence_mutated`, lines 702-722). G3 stores a warrant command in the row and witnesses RUN it and append the exit code (`_run_warrant`, lines 472-482; `witness`, lines 629-665). So the truth of a row is a measurement over mutable resources: files on disk, command exit codes, the existence of other rows appended later.

The reader law already admits this: "Readers quote the admission view, never bare PASS" (`mag/grounding_wave.py:43-46`), born from the v3 FALSE-RECEIPT attack in which a fabricated SUPPORTED row passed hash linkage because hash-validity was read as truth (lines 96-105).

## 2. The central claim: these receipts are already quantum in effect; the design is to stop lying about it

A classical receipt claims: its truth value is a fixed function of its own bytes, readable at any time by anyone, with no cost and no side effects. This estate's receipts do not have that property and never did:

- Row 75's evidence resolved at post time (09-12 era) and does not resolve today; the row is hash-faithful and still fails verify, every day, until someone notices. My run above reproduces this.
- A row's prev-validity can depend on rows appended LATER than it: the re-anchor rule `_reanchor_ok` (`mag/grounding_wave.py:381-399`) makes row i's linkage depend on whether a future void buried the stretch it skipped. Appending a void today changes the effective status of rows from weeks ago. That is retrocausal by classical log standards.
- The same chain yields different truth on different days with zero bytes changed, because G2/G3 measure the working tree, which evolves. The seed registry already names this phenomenon and grades it: LIVING-FILE DRIFT, "snapshot staleness, not forgery," REVIEW rather than REFUSE (`mag/seed_registry.py:31-35`).

Quantum mechanics is the existing formalism for systems whose (a) state is not fixed until measured, (b) measurement outcomes depend on basis choice, (c) states of composite systems are not decomposable into independent parts, (d) measurement acts disturb or consume the state. The estate has rediscovered each property ad hoc and patched it as a special case: the v3 auto-demote is collapse on a missing observation; the admission view is a density matrix over the ladder; pending voids are superpositions awaiting a second observation; propagation flags are entanglement made visible; the policy engine's TTL gate ("proposal.ts + ttl_seconds must still be the future", `mag/policy_engine.py:12` and 167-188) and renderman's `expired` property (`mag/renderman.py:113-116`) are decoherence schedules; the loose `ttl_s`-outside-the-hash contract (`mag/grounding_wave.py:163-164`) is an unspent hook for exactly this. QUANTUM RECEIPTS unify the special cases into one typed layer. No qubits are required; the qubit is the receipt's epistemic state, and the disk is its Hilbert space.

## 3. Primitive 1: superposed receipts (provisional truth)

Design. A claim row stops storing a bare verdict and stores an amplitude vector over the ladder, e.g. `amp = {CORROBORATED: 0.81, RECORDED: 0.19}`, computed at READ time as a pure function of recorded events only: witness count and seat distinctness (the two-eyes inputs at `mag/grounding_wave.py:325-334`), witness ages, latest G2 re-hash results, latest G3 exits, open contests. Nothing hand-set; amplitudes must be derivable, because a hand-set confidence is the hand-copied-count disease all over again. Each observable carries a decay term (a half-life on witness age, an instant kill on evidence re-hash mismatch), and every quotation of the receipt must carry the amplitude and the observation timestamp.

What it solves that classical does not: SILENT STALENESS. A classical receipt that read CORROBORATED on the day it was written reads CORROBORATED forever after in every downstream quote, no matter how far the world drifted. The estate has bled on exactly this twice. First: the row-122 defect rode for days and the 09-12-era EVIDENCE-MISSING rows are still failing verify now, visible only to whoever re-runs the full audit (my exit 1 above). Second, and worse because it is load-bearing: the retired "1,341 tests / 264 files" census headline in AGENTS.md was hand-copied, never byte-backed, and rode for 12 days while 31 test files grew, until the B2-215 tripwire was built; the fleet then had to add B2-244 (deep collect check), B2-246 (daily scheduled deep check), and B2-249 (carrier shape law so the gate cannot be silently reworded away) to patrol ONE carrier line. That is a classical special-case decoherence detector, hand-built per surface. A superposed receipt generalizes it: any consumer sees probability, so a stale receipt is visibly less-true rather than falsely-true, and quoting an amplitude from t0 as if it were the amplitude at t is a type error, not a trap. The estate's own evidence-mutation machinery proves the demand exists; amplitude just gives it a number and a schedule.

## 4. Primitive 2: entangled receipts (verifying one verifies its pair)

Design. Bind each claim row to a declared entanglement group: its witness rows, its void/contest acts, its evidence blob hashes, and (optionally) its descendant range. Add one key (`entangles: [hash12, ...]`) to the versioned key set in `_KIND_KEYS` (`mag/grounding_wave.py:119-126`). A measurement of any member runs the group's checks once and records ONE outcome that fixes the status of every member, plus a group id in the outcome row.

What it solves that classical does not: two things.

First, O(defect) propagation instead of O(tape) re-derivation. When FW-03 found the row-122/123 linkage defect, the containment answer ("contained by void, re-anchored past voided stretch") required reading every descendant row and running the admission fixed point; my verify output lists rows 122, 123, 129, 130, 131, 132 individually because each had to be re-derived by walking the tape. The fixed-point loop at `mag/grounding_wave.py:283-291` is a classical simulation of entanglement collapse, computed globally on every read. With declared groups, one measurement of the defect collapses the whole group to SUSPECT in one step, and everything OUTSIDE the group is certified untouched without being read. The current propagation flags (336-337) are the seed of this; entanglement makes it a first-class object instead of a diagnostic printout.

Second, mirror divergence with localization. The chain tip is copied to many independent surfaces: `mag/boot_check.py:48` (`_chain_tip`), `mag/bonds.py:208` (biography chain tip), `mag/chord.py:36` (session origin), and the seed registry's LINEAGE law, which refuses a seed whose `position.chain_tip.leaf_hash` exists nowhere in `memory/biography/verkle_chain.jsonl` (`mag/seed_registry.py:36-38`). The tip root itself is a succinct commitment (`mag/verkle_knot.py:3-7`). Classically, each surface re-verifies alone, and a mirror that froze before a void landed (the estate keeps frozen mirrors, e.g. the `dist_audit/nacho_business_audit_20260912T214050Z` snapshot copies of `mag/embassy_integrity.py` alongside the live vendored `mag/integrity_kernel.py`) keeps serving pre-void truth indefinitely and is indistinguishable from a live one without a diff. Entangled group verification makes tip equality a JOINT observable: any one surface measuring its tip detects a fork on all of them, and the first disagreeing pair localizes WHICH surface is stale. The estate's existing two-seat cross-signature law is entanglement of trust: a void row is in a superposition of (effective, pending) until the second seat's witness row exists (`pending_voids`, lines 296-299); one party cannot collapse it alone.

## 5. Primitive 3: collapse (observation changes the state)

Design. Keep the tape classical and append-only (the estate's law: nothing is ever edited or deleted, `mag/grounding_wave.py:40-41`). The quantum state lives entirely in the admission view. Measurement is a verb that APPENDS: the existing `witness` verb is already this, it records `checks.g1`, `checks.g2`, `checks.g3_exit` as new rows (lines 629-665). Generalize it to a `measure` verb that appends the full amplitude vector, the basis used, and the outcome; repeated measurement is legal and every outcome is kept (measuring inside the decay half-life freezes the decay: a classical Zeno effect, with the estate's corroboration rule as the existing approximation).

What it solves that classical does not: the basis-confusion attack, made structural rather than disciplinary. The v3 FALSE-RECEIPT attack succeeded because a reader measured in the wrong basis: hash-basis (does the row recompute?) instead of admission-basis (do two independent hands corroborate?). The fix was a law people have to remember ("readers quote the admission view, never bare PASS"). A quantum receipt makes bare PASS ill-typed: every read names its observable, so there is no untyped quote to leak. The same move kills the false-success guard's failure mode at the type level: `mag/integrity_kernel.py:159-175` (Executor.claim_only vs run, `verify_execution`) exists because a claim of an observation is not an observation; in receipt terms, appending "I measured CORROBORATED" without a basis and a warrant nonce is not a measurement record.

Collapse also gives the no-cloning theorem an operational payoff. Classically, one SUPPORTED row's trust is copied freely into commit messages, FKB signatures, and downstream receipts; nothing limits how many times one observation is replayed as evidence. Quantum framing makes witness tokens single-use challenge-response (the warrant command embeds a nonce; two witness rows cannot cite one measurement), so the two-eyes law (the self-sign refusal at `mag/grounding_wave.py:642-646`) stops being honor-system and becomes non-replayable. The 49 legacy-unwitnessed SUPPORTED rows in my live verify are the standing monument to the current replay exposure: they were never measured by a second hand, and they still read SUPPORTED in history and in quoting receipts.

## 6. QROW v5: the minimal concrete diff

No new subsystem. Extend `mag/grounding_wave.py` only:

1. `_KIND_KEYS["claim"]` gains `amp_basis`, `entangles`, `decay` (all inside the hashed set, versioned like every prior wave; `.get` defaults keep v1-v4 rows valid per the no-auto-migration law).
2. New pure function `_amplitude(row, rows, adm, now)` computing the ladder amplitude from recorded events only (witness ages, g2 results, g3 exits, contests). Unit-testable against the live tape.
3. `verify()` gains a STALE section: amplitude below floor is WARN with the number printed, never silent, and never a linkage FAIL (staleness is REVIEW-grade, exactly as LIVING-FILE DRIFT already grades it in `mag/seed_registry.py:31-35`).
4. `measure` verb: witness plus amplitude snapshot, appended, never overwriting.
5. Receipt-format law (extends the reader law): a Q-020-style receipt quoting a chain row must quote amplitude and observation timestamp. The sibling receipt I read already does the honest classical version of this (verbatim output, exit code, "Not done" section); this makes it typed.

## 7. The problem list, answered directly

Problems the three primitives solve that the classical chains do not: (1) silent staleness of quoted receipts, generalized instead of one tripwire per surface; (2) O(tape) re-derivation after a defect, replaced by group collapse; (3) mirror divergence that cannot localize which copy is stale; (4) basis-confusion (hash-PASS read as truth-PASS), made a type error; (5) unbounded replay of a single observation as trust; (6) the retrocausality the tape already has (later voids changing earlier rows' effective status) made explicit and priced, instead of discovered by surprise in a FAIL line.

## 8. Literature anchors

Cited from the gopher's field knowledge, not re-fetched in this session (flag for external quoting): Wiesner's conjugate coding (SIGACT News, 1983) originated quantum money: states prepared in conjugate bases that wrong-basis measurement disturbs; that is the G2 evidence-rehash law in physical form (reading evidence disturbs what reading certifies). Wootters and Zurek (Nature 299, 1982) proved no cloning, the physical basis for single-use witness tokens. Bennett and Brassard's BB84 (1984) turned that into detection of interception. Gottesman and Chuang, "Quantum Digital Signatures" (arXiv quant-ph/0105032, 2001) built signatures where a quantum signed message cannot be duplicated, the direct analog of a non-replayable witness. Hillery, Buzek and Berthiaume (Phys. Rev. A 59, 1829, 1999) did quantum secret sharing with GHZ entanglement: the secret exists only in the joint state, which is the cross-signature void read as physics. Zhandry, "Quantum Lightning Never Strikes the Same State Twice" (EUROCRYPT 2019) gives publicly verifiable no-replay tokens. Misra and Sudarshan (J. Math. Phys. 18, 756, 1977) named the Zeno effect behind measure-to-freeze-decay. The honest limit is real physics: Mayers (PRL 78, 3414, 1997) and Lo and Chau (PRL 78, 3410, 1997) proved unconditionally secure quantum bit commitment impossible, so no receipt can bind a provisional state against a cheating preparer without either computational assumptions or an external trusted hand.

## 9. Honest limits and OWED

- No quantum hardware is present or assumed anywhere in this design. The entire content is (a) a type system for epistemic state and (b) classical simulations (amplitudes, groups, measurement records). If conjugate-basis evidence tags ever became practical, G2's mutation detection would upgrade from hash-based to information-theoretic; until then the quantum vocabulary is semantics, not security strength. I claim no speedup from physics.
- The Mayers/Lo-Chau impossibility maps cleanly onto the estate: the cross-signature law requiring the operator's word for a VOID is exactly the trusted external hand that physics cannot replace. The estate already pays the only price that can be paid.
- Amplitudes need their own calibration receipts or they reintroduce the hand-copied-count disease in fancier clothes. The design above restricts amplitudes to derived quantities; the OWED part is a calibration harness proving derived amplitudes predict observed verify outcomes better than the bare ladder (not run in this session; no harness exists yet).
- Not done here: no QROW v5 code was written (this item is design-only per the ask); no tests were run (the touched surface would be `mag/grounding_wave.py`, which I did not modify); the literature was not re-fetched online in this session, so the anchors carry the flag above.

## 10. Verification log

- Ran: `./.venv/Scripts/python.exe -m mag.grounding_wave verify` (read-only) -> exit 1, output quoted verbatim in section 0; byte-matches the sibling receipt `watch/inbox/burn_reset_20260927/queue/Q-020_FW03_grounding_verify.md` filed for Q-020/FW-03.
- Read: `mag/grounding_wave.py` (full), `mag/integrity_kernel.py` (full), `mag/verkle_knot.py:1-18`, `mag/policy_engine.py:1-30` plus lines 167-188 via grep, `mag/renderman.py:100-120`, `mag/seed_registry.py:25-45`, `mag/boot_check.py:40-60`, the Q-020 FW-03 receipt (full).
- All code citations above were read in this session. The AGENTS.md census-carrier history (1,341 headline, B2-215/244/246/249) is quoted from the workspace instructions supplied with this ask, not independently re-verified against the named receipts in this session.
