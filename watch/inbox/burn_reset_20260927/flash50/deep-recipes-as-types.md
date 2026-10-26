# deep-recipes-as-types: the type-theoretic compilation of the estate's laws

Item ask: the estate's laws are natural language ("never fabricate", "trust bytes"). Design the type-theoretic compilation: each law becomes a type constraint, each violation a type error, each gate a type checker. Name the category theory underneath and the functors between law-space and code-space.

Evidence base, all first-hand in this session. Files read with the line numbers cited below: `tools/violation_ratchet.py`, `tools/workflow_gate.py`, `tools/census_drift_patrol.py`, `tools/freshness_check.py`, `tools/config_seal.py`, `githooks/pre-push`, `watch/inbox/SHARED_SURFACE_CONTRACT.json`, plus the AGENTS.md carrier bullet and build-discipline section. Gates executed this pass (read-only invocations, exit codes verbatim):

```
.venv/Scripts/python.exe tools/violation_ratchet.py check --changed      -> exit 1
  RATCHET check: scope=11 changed files; hits=14; registered=13; NEW=1
  NEW 2c7e16bf178da9d0 shell-true: tools/fossil_check.py:73
  GROWTH claim e066832a0b8edb5e: tools/stealth_driver.py accepted at 753
    lines, now 879 (+126) - re-audit or re-accept by name
.venv/Scripts/python.exe tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios -> exit 0
  7 cards ok + pass_control, each card pinning an exact verdict/warns/exit
.venv/Scripts/python.exe tools/census_drift_patrol.py                    -> exit 0
  census 2026-09-27 (2303 collected / 352 files); growth noted but inside
  the window (5 file(s) since census); disk 369 vs carrier 352 (instrument
  lag ... evidence only)
.venv/Scripts/python.exe tools/freshness_check.py                        -> exit 0
  BOOT_4_7.md 2.7d [frozen-ok]; state/HANDOFF.md 2.3d [frozen-ok]
.venv/Scripts/python.exe tools/config_seal.py verify                     -> exit 1
  sealed=56 live=56 modified=4: fossil_registry.json, improve.yaml,
  mirrors.json, violation_baseline.json
```

The two exit-1s are live specimens of type errors in two distinct classes (NEW-violation and seal-drift), sitting in sibling-lane working-tree state; this item banks them as evidence and touches nothing.

Quotes below are ASCII-normalized (em-dashes replaced by hyphens) per the no-em-dash law.

## 1. Thesis

The estate does not lack a type system. It lacks the syntax for the one it already runs. Look at what the machinery actually is: a collection of total functions from artifacts to a small verdict domain, a context of named axioms (the ratchet baseline, the frozen docs, the seal register), a composition of judgments with short-circuit (the pre-push hook), and a discipline that the context only grows by named admission and shrinks only when a proof is re-derivable. That is a type system in everything but surface syntax: propositions-as-types (Curry 1934; Howard 1980) with the propositions being prose laws, the types being refinement predicates over artifacts, the proof terms being receipts, and the judgment form being a process exit code. What follows makes the compilation explicit, law by law, and then names the category theory.

## 2. The verdict domain is a three-element lattice, not bool

Every gate in the chain judges into the same contract, stated in each tool's own header: violation_ratchet.py:28 ("0 = pass, 1 = new violations found, 2 = gate itself broken"), census_drift_patrol.py:30-32 ("0 = census inside the bar; 1 = STALE or COLLECT-DRIFT; 2 = cannot verify"), and the hook's B2-277 exit-class split (githooks/pre-push:78-99) which blocks exit 2 while warning on exit 1, with the reason stated in proof-theoretic terms already: "the gate SAW the carrier and can name the growth" (stale) versus "the gate saw NOTHING, so every push would pass in silence" (blind), and "blind differs from stale".

So the semantics is not `bool`. It is:

```
V  ::= PASS | FAIL | OWED        with OWED = bottom
V' ::= V + WARN                  (annotated PASS, never blocking)
```

Four facts pin this reading:

1. OWED is the explicit bottom. The meta-law "if you could not run it, report it as not run; never fill with a plausible guess" is precisely the ban on the coercion OWED -> PASS. Unverifiable is a value of the verdict domain, not an exception to be smoothed over.
2. Gates are strict in bottom. An unverifiable input can never produce PASS: `parse_carrier` returns fail-closed None on a non-canonical claim (census_drift_patrol.py:148-170), `run()` maps that to exit 2 with "need the claim shape" (:305-309); the secret gate's catch-all arm blocks exit 2, 127, and tracebacks alike because "a missing interpreter must never read as a pass" (githooks/pre-push:328-331). This is Scott-domain partiality (Scott 1976): bottom-propagating, monotone maps only.
3. FAIL and bottom are distinguished. B2-277 is exactly the domain-theoretic fact that a verified counterexample and "the checker observed nothing" are different elements, and conflating them destroys the gate.
4. WARN is a rank, not a verdict. The workflow gate's soft rows are computed as ok-but-then-marked-not-ok-with-a-reason and are excluded from the failed set so the exit contract is untouched (workflow_gate.py:126-144, t69 and B2-206 comments). WARN sits between PASS and FAIL as an annotated PASS with a named reason: evidence at reduced rank.

The ratchet's growth law (B2-273, violation_ratchet.py:71-80 and :260-272) adds a fifth class in spirit: GROWTH is a ledger fact printed on a PASS. That is a side-channel assertion, a checker emitting a non-fatal but non-silent observation. The estate consistently refuses to let PASS be information-free.

## 3. The compilation table: law -> type -> type error -> checker

Each row: the prose law with its source, the type it compiles to, the form its violation takes as a type error, and the instrument that judges it (with lines).

| # | Law (source) | Type constraint | Type error | Checker |
|---|---|---|---|---|
| 1 | never fabricate; OWED if unverifiable (seat law; carried inside asks by G7, workflow_gate.py:78-79) | `Claim(c) = { c : Text | exists r : Receipt . r witnesses c }`, an inhabited refinement (Freeman-Pfenning 1991; Liquid Types, Rondon-Kawaguchi-Jhala 2008) | a claim whose evidence fiber is empty; the only well-typed verdict is OWED | the receipt convention everywhere; observed as the EVIDENCE-MISSING token class in the estate's own Q-020 commit trail (pre-existing tokens whose files exist on disk) |
| 2 | trust bytes, not reports (AGENTS.md clippy) | content equality is the hash map; prose is a quotient of bytes and claims may not lift through the quotient. `hash . mint = id` on the hash-pinned subobject: a retraction (Reynolds 1983 flavor) | a report-term with no byte witness | `config_seal.py` (every configs/ file hashed; three error constructors at :56-70), `freshness_check.py` hash_text/hash_file :97-108 and the re-hash drift check :185-192 |
| 3 | census denominator law B2-216: name instrument, moment, delta; never difference two counts from different moments (AGENTS.md clippy) | a Count is a dependent pair `(t : Time) x (n : Nat)` indexed by instrument; subtraction is not defined on Counts, only `diff : (t1 t2 : Time) -> Count t1 -> Count t2 -> Delta t1 t2 -> Diff`; the third argument is a required witness | differencing two moments with no delta witness, i.e. an unattributable drift | `patrol()` names growth signals in the verdict itself (census_drift_patrol.py:250-288); live run printed "growth noted but inside the window (5 file(s) since census)" with the files named |
| 4 | carrier shape law B2-249: the census claim keeps the exact grammar (AGENTS.md clippy) | the claim is a record parsed by a partial function `parse_carrier : String -> Maybe Census`, whose grammar is a singleton owned by one regex plus frozen vectors (B2-274 ownership law, census_drift_patrol.py:96-119) | a claim outside the grammar's domain must be exit 2 "need the claim shape", never guessed (:305-309); rewording the carrier breaks the gate loudly by design | census_drift_patrol parse/run path |
| 5 | ratchet register law: existing debt is a registered claim, only NEW violations fail, admission is by NAME, never loosen the hook (violation_ratchet.py:2-28) | a hypothetical judgment: `Gamma, Axioms |- no NEW fingerprint`. An axiom is a record `{rule, file, detail, accepted, by, note}` written by a named act (:280-301); prune = elimination restricted to claims the scanner can re-derive; B2-95 keeps externally sourced axioms because this checker cannot re-derive them (:304-330) | `NEW <fingerprint> <rule>: <file>:<line>`: a term not derivable from the context. Live: `NEW 2c7e16bf178da9d0 shell-true: tools/fossil_check.py:73`, exit 1 | violation_ratchet check / baseline-update / prune |
| 6 | config seal: every config file sealed, re-seal by NAME (config_seal.py:2-15) | total fiber: the seal map must be defined on every configs/ file, with agreement on hashes; three error constructors MODIFIED / MISSING / UNSEALED (:56-70) | live: exit 1 naming 4 modified keys including violation_baseline.json | config_seal verify / update --by --note |
| 7 | freshness: boot docs stale at >7d while the repo has heartbeat; refresh or freeze with reason+date (freshness_check.py:8-14) | `DocState ::= Fresh | Frozen(reason, date)`; a third state, old-and-unregistered, is ill-typed. FROZEN_OK entries carry payloads (reason+date, :44-51): a sum type with constructors, not a boolean | a stale doc with no FROZEN_OK entry | freshness_check main() :267-302; live run passed with two frozen docs whose reasons printed |
| 8 | shared surface contract: durable artifacts land on the canonical inbox; a session directory is cache and never the sole copy; hashes and bounded pointers travel; a proposal cannot authorize an effect (SHARED_SURFACE_CONTRACT.json:12-22, 87-91) | transport invariance: for every surface move sigma (host / container / WSL aliases, :3-10, :36-77), the hash must be preserved; `never_sole_destination` (:78-86) enumerates the objects with no morphism into the canonical inbox, which are not admissible homes; authority is not derivable from a proof term (consensus "never grants permission") | an artifact whose only copy lives in a no-morphism object; an effect authorized by prose | `mag.shared_surface validate` and the receipt workflow (:24-30) |
| 9 | workflow dogfood G1-G7 (workflow_gate.py:13-21, 45-80) | a choreography type on workflow scripts: named per-item fan-out (G1), a dataflow edge from an earlier actor into a later ask (G2), a reviewer feedback loop (G3), an incremental checkpoint (G4), a published artifact term plus report-shape return (G5), a dated receipt path (G6), and the no-fabrication + no-em-dash laws carried inside the ask strings (G7) | per-gate FAIL rows; the scenario cards pin the expected verdict/warns/exit per gate and the checker must reproduce them exactly (validate_card, :165-208). Live: 7/7 ok, exit 0 | workflow_gate check; scenario mode READ-ONLY |
| 10 | no fallback-branch creep; no timeouts papering over sync problems (AGENTS.md build discipline) | ban on the silent summand: `A -> B` admissible, `A -> B + Default` not; recovery must change the result type (Result/Either), not add a default branch that mutes the symptom | a catch-all that swallows: the gates embody the positive form by BLOCKING on the catch-all arm (pre-push:328-331) instead of passing | ratchet exit 2 on git failure ("refusing to guess", violation_ratchet.py:242); freshness `_git` exit 2 (:57-62) |
| 11 | fix comments carry the receipt (AGENTS.md build discipline) | `Fix = Diff x Cause(path) x Evidence(receipt)`: a product type whose constructor requires all three | a comment naming the what without the cause+evidence is an ill-typed Fix | review convention; the gate files themselves are specimens (every B2-xxx comment names cause and receipt) |

Row 9, G7 deserves emphasis: it is a type constraint on the metalanguage. The asks are strings inside the workflow script, i.e. data, and the gate checks them lexically for the presence of the laws ("no em-dashes" in t, "never fabricate" in t). The system writes its laws in the same language it checks, and the check is at the data level, so no self-application paradox arises: the law-about-laws is just a substring predicate. The estate solved Goedelian self-reference the boring and correct way: by making the metalanguage object-level data.

## 4. The category theory

### 4.1 Two base categories

**Art**: artifacts (files, ledger rows, receipts, claims) with morphisms = hash-preserving bounded pointers. The contract says exactly this: "prefer an artifact plus bounded pointers and hashes over a copied transcript" (SHARED_SURFACE_CONTRACT.json:19). A bounded pointer is a morphism because it is checkable against bytes: the target can be re-hashed and the arrow verified or refuted.

**Law**: a preorder whose objects are the prose laws and whose only morphisms are refinements: `l <= l'` when the accepting fiber of l' sits inside that of l. The estate's ledger vocabulary already speaks this: a "SUPERSEDED" row (as in FW-43 SUPERSEDED by GENE_POOL_TOMBSTONE in the current commit trail) is a morphism from the old law to the finer one.

### 4.2 Compile: the main functor

```
F : Law^op  ->  [Art, V]
```

Each law maps to its checking predicate, a verdict-valued observation on artifacts. Contravariance is the refinement order: if l' refines l, then `F(l)(a) = PASS` implies `F(l')(a) = PASS` is not required; rather F(l') >= F(l) pointwise under the FAIL-above-PASS evidence order (a finer law can only convert PASS to FAIL/WARN, never the reverse, if compilation is sound). Every row of the table in section 3 is F applied to one law. The interesting mathematical content is:

**Naturality = transport.** For a surface move sigma (host path to container path to WSL path), naturality of F in Art is the square `F(l)(sigma a) = sigma(F(l)(a))`. It commutes precisely when the checker keys on content, not location: config keys are repo-relative (config_seal.py:36-43), freshness re-hashes bytes not paths (:185-192), the contract's aliases move the directory not the hash (:3-10). When a claim surface is hand-copied instead of transported, the square breaks silently, and that break has a name and a receipt: B2-274 measured the disease (regression fixtures in three hand-copied places while the live AGENTS.md bullet moved 1,837 -> 1,879 -> 1,910 in one day, census_drift_patrol.py:96-116). The estate's cure is to make the grammar a singleton: one owned regex, frozen vectors that are never auto-synced, so that the claim type has exactly one definition site. In category-speak: the claim type is fixed, and all its instances are global elements of that fixed object; rewording is then necessarily a type error at the one place a checker looks.

### 4.3 The Prose adjunction, and why "never loosen the hook" is a theorem

There is an adjunction between law-space and gate-space:

```
Free : Law -> Gate        (the weakest checker implementing a law)
U    : Gate -> Law        (read a checker back as a statement)
Free -| U
```

The unit says: a law entails its checker's acceptance condition (if the law holds, the gate passes). The counit is the dangerous direction: reading a green gate back as "the law holds" wholesale. Every proven failure mode in the estate's ledger is a counit abuse: the retired 1,341 headline was a claim (a U-output) treated as truth without its F-witness; the 12-day-stale carrier was the same disease.

The operator laws are then not management preferences but proof-theoretic restrictions on how the adjunction may be used:

- "never loosen the hook" (stated in githooks/pre-push:8, :74, :195, :273 and AGENTS.md) forbids retraction along the counit: you may not weaken a checker to make a term fit.
- "accept debt by NAME" is context extension, not weakening: `Gamma -> Gamma, Axiom(fp, by, note)`. The axiom is a term in the context, attributable and dated (violation_ratchet.py:288-296). The judgment was always hypothetical; the baseline makes the hypotheses explicit.
- "prune" is cut elimination restricted to re-derivable claims: B2-95's rule (violation_ratchet.py:304-330, "claims underivable by construction ... are kept by every prune") is exactly the admissibility condition: you may eliminate a hypothesis only when your own proof system can re-derive it. Externally sourced axioms (mimosa claims over trees this scanner never scans) are kept because their derivation lives in another checker.

The register trending down ("debt that gets fixed leaves via prune, so the register trends down", violation_ratchet.py:7-8) is a monotone progress measure on the context: the estate's version of a normalization argument.

### 4.4 Institutions: re-blocking the sentences

The whole setup is an institution in the sense of Goguen-Burstall 1992: signatures Sigma = contract schemas (shared_surface.v1; the G6_STAMP_RE stamp grammar at workflow_gate.py:86-88), sentences Sen(Sigma) = the law statements over that schema, models Mod(Sigma) = repo states, satisfaction |= = the gate's exit 0. Compiling prose to a python predicate is an institution morphism, and its soundness direction (checker accepts implies law satisfied) is the one that matters and the one that is only ever partial, because Sen(natural language) is ambiguous and undecidable.

The estate's answer to incompleteness is visible as a repeated sentence in the gate docstrings: "states the bar in numbers BEFORE reading anything" (census_drift_patrol.py:9; freshness_check.py:8-11 has the same shape). That sentence is an act, not a remark: it is the deliberate replacement of an ambiguous sentence by a decidable one, i.e. shrinking Sen so the morphism can be total on what remains. Whatever cannot be re-blocked is exactly what OWED types. The residual of the compilation is not hidden; it is given a name and a verdict value.

### 4.5 Abstract interpretation and the epsilon bar

Each gate is a Cousot-Cousot (1977) abstraction of behavior into the finite lattice V. Soundness holds genuinely for the syntactic rules: `shell=True` is literally present in the AST (violation_ratchet.py:157-160), the workflow gate's checks are regexes over script text (workflow_gate.py:45-80), so abstract FAIL implies concrete violation. Precision loss is bounded and named: `COLLECT_DRIFT_TOLERANCE = 20` (census_drift_patrol.py:125) is an epsilon-typed equality, `|real - claimed| < 20`, deliberately symmetric with the asymmetry of the disease stated in the code ("an under-claim is the B2-244 disease ..., an over-claim is worse", :197-216). The ratchet's fingerprint quotient, sha256 over (rule, file, detail) with line-free detail, one fingerprint per (rule, file) (:19-21, :84-85), is a deliberately coarse type chosen so that irrelevant edits do not churn the register: abstraction level selected for stability, the Cousot trade-off made explicit.

### 4.6 Partiality monad and the shape of composition

Gates are Kleisli maps `Art -> T(V)` for the maybe-error monad (Moggi 1991); the pre-push hook is their Kleisli composition with short-circuit (`|| exit 1` chains at githooks/pre-push:10-12; the census block's case-arm at :89-99; the scenario block at :295-304). Receipt accumulation is a Writer: the workflow gate appends a REGISTRY.jsonl row on every run including FAILs (workflow_gate.py:307-317), making the checker's own judgments observable evidence, a deliberate impurity. The hook's staging also encodes an evidence ranking: enforcing gates (ratchet, config seal, scenario suite, secret gate) versus WARN-ONLY gates with explicit `TODO-FLIP-TO-ENFORCE` markers (:17-18, :38-40, :137-139, :200-202). That is a promotion discipline on hypotheses: a checker enters the theory as a WARN axiom, accumulates observational support, and is promoted to an enforcing (blocking) judgment only by operator decision. New-type-system rollout as a monotone chain of theory extensions.

### 4.7 Session types: G1-G4 as choreography

The workflow gate's first four checks are a multiparty session type (Honda 1993; Takeuchi-Honda-Kubo 1994; Honda-Yoshida-Carbone 2008) on the workflow process: G1 pins the fan-out structure (per-item named actors, the role naming scheme is the type), G2 pins a channel (an earlier actor's output feeds a later ask: an output-to-input edge), G3 pins a recursion point that consumes a reviewer verdict before revising (the feedback loop), G4 pins progress: report() fires inside the fan-out "so work survives a dead run" (workflow_gate.py:17). G4 is the session-typed obligation that a dead process must still have emitted its trace prefix onto the durable ledger. The estate discovered session typing as fleet dogfood, which is what the phrase "dispatch shape is the retry strategy" in AGENTS.md's fan-out law is an instance of: the shape of the process, not the capacity of the channel, is what the type governs.

### 4.8 Proof-carrying artifacts and commitments

Receipts are proof terms in the sense of proof-carrying code (Necula-Lee 1996): a claim travels with the evidence sufficient to recheck it, and `stale_claim()` is the rechecker (freshness_check.py:160-193: missing, malformed, too old, future-dated, or drifted-hash receipts each fail closed with a distinct named reason; the NamedTuple even overloads `__bool__` so gates can use the verdict directly, :89-93). The config seal and the verkle-committed clippy rope are commitments to proof terms: a fresh seat verifies the commitment without re-walking the world, and the boot-order law ("load ribs -> load state -> then act", AGENTS.md) is the instruction to check the proof context before extending it. The Yoneda-flavored corollary: the ratchet register stores the fiber of each predicate (the accepted set of (rule, file) pairs), not the law itself; the law is known extensionally by what it rejects. Prune shrinking the register is a fiber decrement with a receipt (the 943 -> 941 prune in the current commit trail is one).

### 4.9 Girard stratification: who checks the checker

The tower, bottom to top:

```
level 0  repo code and bytes
level 1  workflow scripts (.dwf.ts)
level 2  workflow_gate.py checks level 1
level 3  scenario cards pin level 2's diagnostics (expected verdict/warns/exit per gate)
level 4  the AGENTS.md census claim (a statement about level 0 truth)
level 5  census_drift_patrol.py checks level 4
ground   the --collect deep mode runs level 0 (pytest --collect-only) to
         ground level 4 in bytes: normalization by evaluation
```

Each stratum is checked by the next, the top is grounded by executing the bottom, and no checker types itself: a gate-script change triggers scenario mode (pre-push:280-304), and the scenario suite cannot silently bless a broken checker because each card must cite a real REGISTRY FAIL row and reproduce its verdict exactly (workflow_gate.py:165-208; the live run's per-card lines show FAIL-expecting cards validated as "ok" because the checker produced the right error). Producing the right type error is itself typed. Girard's paradox (1972) is the hazard for any system that checks itself without stratification; the estate dodges it not by fortune but by the same trick proof assistants use: keep the checker outside the checked, and pin the checker's behavior with vectors minted from real failures.

## 5. The two functors between law-space and code-space, named

**F = Compile : Law^op -> [Art, V].** The table of section 3. Sends a prose law to its verdict-valued predicate on artifacts; sends a refinement to the pointwise order. Naturality in Art is hash-transport (4.2).

**G = Witness : Art -> Proof.** Receipt minting (freshness_check.py `receipt()`, :111-133): an artifact maps to the proof term that re-verifies it (observed_at, source_hash, bar). G is a partial section of the content-to-hash map: on the hash-pinned subobject, `hash . G = id`, a retraction; "trust bytes, not reports" is exactly the demand that every admissible claim factor through this retraction. The connection between the two functors is the soundness statement of the whole architecture:

```
for every law l and artifact a:
  F(l)(a) = PASS   implies   exists r : G(a) with r proving l(a)
and where no such r can exist, the only well-typed verdict is OWED,
and the law forbids anything else.
```

Everything else in the estate's discipline (ratchet context extension, seal totals, fail-closed bottoms, carrier grammars, scenario-pinned diagnostics) is infrastructure to keep that one statement honest at push time.

## 6. The compilation agenda, and the limits

Remaining prose laws queued for compilation, in the same scheme:

- **Driving ladder lanes** (AGENTS.md): refine `Lane ::= Sensing | Funded`; the verdict DONE requires a Funded-lane witness; outputs from Sensing lanes get typed `Finding`, which is not in the codomain of Work. This is a graded type: the same text is Findable at one grade and not Work-grade at another.
- **"No core-mirror throne"** and the shared-boundary table: already institution-shaped; the residual work is making `mag.shared_surface validate` check hash transport, not just shape.
- **The census bullet's grammar law** is fully compiled (B2-249/B2-274). The next prose law in line is the trust-decay convention on `memory/briefs/latest.md` (FROZEN at a date): that is a FROZEN_OK entry for a memory surface, waiting for its freshness_check analog.

Limits, stated honestly:

1. Full compilation of natural law is undecidable in general. The estate's posture (partial compile, explicit bottom, named axiom admission, ratchet monotonicity, fail-closed on cannot-verify) is the soundness-first approximate compiler: it never accepts on a guess, and it pays for precision with named baselines. That is the correct engineering form, not a deficiency.
2. A "real" dependent type system (Lean, F*, Dafny) would lose something the estate needs: the model is a shared mutable working tree with concurrent sibling lanes (B2-280 sibling-lane claims are cited inside the hook itself), so properties must be judged on bytes at push time, not proven once at write time. The gates are runtime type checking of a living object; the ratchet is how a runtime checker accumulates a static discipline.
3. The soundness direction of F (checker-accept implies law-holds) is only as good as the compile step per law, which is why each table row names its instrument and why "fix the gate or re-prove the cards, never loosen the hook" (AGENTS.md) is the meta-law: a suspected unsound compilation is repaired at the spec level, in public, with a receipt.

## 7. Method note

Literature anchors are cited from model knowledge of the canonical results (Curry 1934; Howard 1980; Martin-Lof 1984 on judgments; Freeman-Pfenning 1991; Rondon-Kawaguchi-Jhala 2008; Goguen-Burstall 1992; Cousot-Cousot 1977; Moggi 1991; Scott 1976; Wadler 1989, 2015; Necula-Lee 1996; Reynolds 1983; Girard 1972; Lawvere 1969; Honda 1993; Takeuchi-Honda-Kubo 1994; Honda-Yoshida-Carbone 2008; Meyer 1992; Claessen-Hughes 2000) and were not re-fetched this pass. All estate claims are first-hand from the files and runs listed at the top. The two live exit-1 specimens (ratchet NEW fingerprint `2c7e16bf178da9d0` at tools/fossil_check.py:73; config seal MODIFIED over four keys including violation_baseline.json) are sibling-lane working-tree state, banked as evidence, intentionally not re-sealed or re-accepted by this item: admission is a named act and this seat is not the name for it.
