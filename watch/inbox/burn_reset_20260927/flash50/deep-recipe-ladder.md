# deep-recipe-ladder: The Formal Recipe Ladder (RIR, the Recipe Intermediate Representation)

Item ask: operators write laws (natural language), the seat compiles to code (Python/Lua), the code produces receipts (JSONL). Design the FORMAL recipe ladder: a typed intermediate representation between natural-language intent and executable code, with provenance tracking and reversible compilation. Grounded in estate bytes read this session; literature anchors at the end.

## 1. The informal ladder already exists in bytes (four instances read this session)

The design below is not greenfield. The estate already hand-compiles law to code to receipt in at least four places, and each one exhibits exactly the pathology a typed IR exists to kill.

**Instance A: the census carrier laws.** The natural-language law is the AGENTS.md Tests bullet (AGENTS.md:27), which carries at least eight numbered sub-laws (B2-215, B2-216, B2-244, B2-245, B2-246, B2-247, B2-249, B2-274). The compiled code is `tools/census_drift_patrol.py`: the claim grammar as `CENSUS_CLAIM_RE` (tools/census_drift_patrol.py:117-119), the parser `parse_carrier` returning dict-or-None with fail-closed semantics (:148-170), the deep-check bar `COLLECT_DRIFT_TOLERANCE = 20` (:125), and the pure verdict cores `patrol()` and `collect_patrol()` (:250-288, :197-216). The receipts are the patrol stdout and `logs/census_patrol.log`. The disease is documented in the code's own comment: the B2-274 OWNERSHIP LAW block (tools/census_drift_patrol.py:97-116) admits the grammar is hand-copied into three places (this regex, the self-test fixtures, the pytest fixtures), and that "the two frozen surfaces cannot see a live-carrier reword" while the AGENTS.md sentence is "the only surface that warns the reworder." Three hand-maintained projections of one law, kept in sync by attention. That is the missing IR, stated as a debt.

**Instance B: the workflow dogma.** The natural-language law is the operator quote preserved verbatim in the module docstring (tools/workflow_gate.py:4-7). The compiled code is the G1-G7 check table (:45-80) plus two soft-warn layers (G6 dated stamp :86-94, G3 judge-model stamp :96-114). The receipts are real FAIL/PASS rows in `memory/workflows/REGISTRY.jsonl` (rows 1-6 read this session: verdict FAIL at 2026-09-25T18:52:02Z for tree-doctrine-dig, G6 ok=false; mickey17-v2 FAIL at 20:45:15Z with G3/G4/G7 false, PASS at 20:47:59Z after amend). The scenario cards are the closest existing thing to IR clauses: `configs/workflow_gate_scenarios/G7_laws.card.json` carries `gate_id`, a `cited_fail_row` pointing at REGISTRY.jsonl by line number (lines 4-10), a typed `expected_verdict` (failed_checks, exit_code 2, lines 14-19), a `regression_criterion`, and a `rollback_note` (lines 20-21). A card is a law clause bound to a fixture and an expected receipt, with provenance. The FRL formalizes exactly that shape and generalizes it past the gate.

**Instance C: the ratchet.** Law text in the docstring (tools/violation_ratchet.py:5-8: "debt that exists today is a REGISTERED CLAIM in the baseline; only NEW violations fail"). Code: fingerprint `sha256(rule NUL file NUL detail), first 16 hex` (:84-85), the closed `SCANNER_RULES` set (:51-61), the B2-95 external-claim keep rule (:10-17, :64-68), the B2-273 accepted-lines growth law (:72-80). Receipts: `configs/violation_baseline.json` claims and the prune counts in commit messages (Q-028: "ratchet prune 943->941", commit d90bc8607, verified via `git log --oneline -3` this session).

**Instance D: a proto-IR already exists and nobody calls it one.** `memory/corpus/quantized_thought/instructions_flash.jsonl:1-4` is a typed compilation of behavioral invariants: fields `id`, `class: "law"`, `raw_count`, `count_verdict: "inflated echo - provenance only"`, `weight`, `shape: "imperative"`, `sources` (pointing at invariant ids in `memory/percolator/invariants.json`, e.g. instructions_flash.jsonl:2 `sources: ["a77444ced5abc2e7"]` = the "Trust bytes, not reports" invariant at invariants.json:66-72), and `status: "compiled-v0.3"`. That is: source provenance, a typed shape field, and a compiler version stamp. Likewise `docs/ref/lessig_1_6.md` is a hand-built ladder: a Law table (:8-17) and a separate Architecture section listing the enforcing code sites (:32-39, e.g. `mag/dispatch.py` seat gate, `mag/run_trail.py` base freeze). The law table and the architecture table are two artifacts kept consistent by hand.

The recipe ladder is therefore already load-bearing. What is missing is the middle layer that would make the compilation typed, provenance-tracked, and reversible, so the B2-274 triple-copy and the B2-215 twelve-day stale headline (tools/census_drift_patrol.py:4-7: "the estate carried the hand-copied '1,341 tests / 264 files' headline for 12 days ... because no gate watched the test-count carrier") become compiler errors instead of discovered wounds.

## 2. The observed failure modes, each a missing-IR symptom

1. **N-way hand-copy drift** (B2-274): one grammar, three frozen surfaces, sync by attention (tools/census_drift_patrol.py:97-116).
2. **Unenforced prose claims** (B2-215): a number rode 12 days stale with 31 files grown and no gate noticed (AGENTS.md:27; patrol docstring :4-7). The claim had no clause node, so nothing owned it.
3. **Order-fragile parsing** (B2-245): the first parser took the FIRST date and the FIRST "N tests" anywhere on the bullet, so prose numbers poisoned the parse; the fix anchored on the clause shape (:84-92). Without a typed Grammar node, every carrier is one reword away from this again.
4. **Mis-compiled thresholds** (Q-008, commit 4706d5a04, verified this session via `git show -s 4706d5a04`): the FKB thresholds were "flat count>=3 twice plus a [:5] rank slice", so only 5 of 15 signatures emitted while 2,502 of 3,958 real trail ticks ran at n_signals=0. A threshold is a typed value with denominators; the hand version had neither, and the mis-compile was found by a live census, not by review.
5. **Denominator confusion** (B2-216, AGENTS.md:27): "collected" and "executed" are different instruments at different moments; "never difference two counts taken at different moments" is currently a prose rule enforced by shaming.

Each of these is a type error or a provenance error in a system that has no types and no provenance graph. That is the argument for the IR.

## 3. The design: RIR, the Recipe Intermediate Representation

### 3.1 Layers

- **L0 Law source.** Immutable natural-language text, addressed by `law_id` (16-hex content-hash prefix, matching the estate's own fingerprint convention, tools/violation_ratchet.py:19-21) plus byte spans. Rewording is never an edit: it is a new epoch with retained old spans (amend-not-rewrite, tools/workflow_gate.py:9-11).
- **L1 RIR: the typed clause tree.** See 3.2.
- **L2 Lowerings.** Deterministic back-ends: Python gate code, Luau modules, prompt cards (the quantized-thought JSONL), scheduled-task registrations (scripts/census_patrol_daily.ps1 per B2-246, AGENTS.md:27). A lowering must be re-runnable from the IR alone.
- **L3 Receipts.** Append-only JSONL surfaces keyed by law_id, already the estate norm (REGISTRY.jsonl, LEDGER.jsonl, trails).

### 3.2 The clause node

Every node: `id`, `kind`, `law_ref` (law_id + byte span), `semantics` (a named operator from the closed set below), `params` (typed), `obligation` (gate | warn | ritual | sensing), `targets` (file:function:line of the lowering), `receipt_surface` (JSONL path + row schema id), `provenance` (compiler seat, model, tier, timestamp, upstream clause ids), `reverse_template` (how to render this clause back to English).

The original move is that the estate's laws already collapse into a small closed operator set. Reading the three instances, eight kinds suffice:

1. **Carrier**: a document slot that must keep a typed grammar, with a freshness bound. (B2-249 grammar + B2-215 7-day bar; code: tools/census_drift_patrol.py:117-119, :78.)
2. **Threshold**: measure, operator, bar, and DENOMINATOR. (B2-244's tolerance 20 at :125; the Q-008 FKB re-compile: ordinary kinds at count>=2, collapse/fake_success at count>=1 with severity=error.)
3. **Gate**: exit contract 0/1/2, warn-only flag, and the named owner who may flip it. (Exit-code docstrings: census_drift_patrol.py:30-32, violation_ratchet.py:28; "WARN-ONLY at pre-push, flip-to-enforce is an operator call", AGENTS.md:27.)
4. **Ratchet**: monotone register, prune-domain rule, accept-by-name, expires-rot. (violation_ratchet.py:5-17, :51-68, :70-71.)
5. **Receipt**: surface path, row schema, hash discipline. (REGISTRY.jsonl; the B2-216 receipt pointer in AGENTS.md:27.)
6. **Ritual**: human-gated step with trigger and evidence form. (B2-246's operator refresh duty, AGENTS.md:27; the v4 VOID cross-sign nomination form in Q-020, commit b34ccd3ba; FW-48 "plan-only OWED operator GO", commit d90bc8607.)
7. **Falsifier**: predicate whose firing mandates a named action. (G7 card regression_criterion, G7_laws.card.json:20; Q-022's FW-15 amendment 005 "falsifier = future EMPTY/foreign-claims/stacked section", commit f737ee453.)
8. **SoftWarn**: reason string, family, non-blocking. (workflow_gate.py:86-94 and :96-114.)

Anything a law says that maps to no operator is typed `Decorative` (explicitly unenforced prose). This is the inverse of the build-discipline rule "spec before behavior change / no orphan behavior": the IR makes orphan LAW visible too, which is precisely what the B2-215 headline was.

### 3.3 The type system: the estate's scars as compile-time distinctions

- **Count(instrument, moment).** `CountCensus(t)` does not unify with `CountExecuted(t)`. B2-216 (AGENTS.md:27: "never difference two counts taken at different moments") stops being a memo and becomes a type error: subtracting two counts is well-formed only when instrument and moment unify; otherwise the compiler must emit an explicit `Delta(instrument, t1, t2, attribution)` node naming the landings that moved the count, which is exactly what B2-246 already demands in prose ("an unattributable drift is a fabrication smell", AGENTS.md:27).
- **Grammar(shape)**: the B2-249 claim shape as a first-class value. The compiler emits the SAME Grammar node to all three surfaces (AGENTS.md bullet, patrol regex, fixtures), which structurally kills the B2-274 triple-copy: the grammar is owned once and projected, and the audit fails if any projection disagrees.
- **Freshness(days)**, **Severity(class)**, **Debt(fingerprint, accepted_by, accepted_lines, expires)** (typed directly from violation_ratchet.py:72-80), and **Tier**: per the driving ladder law (AGENTS.md:32), free stealth lanes are a sensing surface; a Tier-typed compiler restricts sensing-tier seats to emitting `sensing` obligations and to DRAFTING gate clauses, which stay `draft` until a funded-tier seat verifies them. A compile is not done until its journal row is verified.

### 3.4 Provenance

Why-provenance in the database sense (Buneman, Khanna, Tan, ICDT 2001): every receipt row can answer "which law clauses produced this row", and every clause can answer "which receipts first proved me". The estate already keeps both halves separately (the FAIL rows in REGISTRY.jsonl, the G7 card's `cited_fail_row`, the `status: compiled-v0.3` stamp in instructions_flash.jsonl:1); RIR joins them on law_id and span ids. The compile journal is `receipts/recipe/compile.jsonl`, append-only, one row per attempt: (law_id, law_sha, ir_sha, target lowering, seat, tier, verdict, diff-to-previous-ir). Rows are never edited in place; the precedent is FW-03's grounding verify: "all 137 rows hash-faithful, none edited in place" (commit b34ccd3ba, git log this session). Re-deriving a clause without a journal row is the compiler's own fabrication smell, the same rule the census patrol applies to drift without attribution.

## 4. Reversible compilation

Forward: law bytes to spans to clause tree (the compiler is a seat, tier-constrained). Backward: `render(IR)` to English. The round-trip law, borrowed from bidirectional transformations (lenses: Foster, Greenwald, Moore, Pierce, Schmitt, TOPLAS 2007): the law text is the concrete source, the IR the view; `parse(render(compile(law)))` must be law-equivalent to `law`. Equivalence is span-faithfulness, not byte equality: each rendered sentence must hash-match the span it claims to own, and the clause multiset must be unchanged. Where a human reword is legitimate, it is an AMENDMENT: new epoch, old spans retained, filed in the compile journal (the estate already does this by hand: Q-022 filed FW-15's amendment 005 as ledger row 6 with status active and a falsifier, commit f737ee453).

Because the compiler is an LLM seat and not a verified compiler, the correct verification posture is translation validation (Pnueli, Siegel, Singerman, TACAS 1998): do not prove the compiler, check each compilation. The compile journal row is a proof-carrying-code certificate in Necula and Lee's sense (1996/97): the pre-push gate re-checks the evidence cheaply instead of trusting the seat. CompCert (Leroy, CACM 2009) is the aspirational end state, not the plan.

Reversibility pays off concretely on the B2-274 surfaces: `tools/recipe_ladder.py render` regenerates the AGENTS.md census bullet from the single Grammar node and diffs it against the live bytes; `audit` walks every clause and checks (a) span coverage of the law (no sentence unmapped and unmarked Decorative), (b) target presence (every gate clause's lowering exists at the named file:line, else orphan behavior), (c) projection agreement (the three census surfaces agree byte-for-byte). Any failure is exit 2, cannot-verify, matching the patrol's fail-closed convention (census_drift_patrol.py:23-28).

## 5. What each existing organ becomes

| Existing byte | RIR reading |
|---|---|
| AGENTS.md:27 census bullet | L0 law carrier (source of truth for spans) |
| tools/census_drift_patrol.py:117-119 grammar | lowering of a Carrier clause; loses grammar ownership to the IR |
| tools/workflow_gate.py:45-80 G1-G7 | eight... seven Gate clauses + two SoftWarn clauses |
| configs/workflow_gate_scenarios/*.card.json | Falsifier clauses, already IR-shaped (cited_fail_row = provenance, expected_verdict = typed params) |
| tools/violation_ratchet.py + configs/violation_baseline.json | Ratchet operator + typed Debt register |
| memory/corpus/quantized_thought/instructions_flash.jsonl | a second lowering target (prompt-card lowering) with `status: compiled-v0.3` as its compiler version |
| docs/ref/lessig_1_6.md:8-39 | hand-written ancestor: Law table + Architecture table = the two projections RIR derives from one clause set |
| memory/rib_bus/doctrine.json entries (ts, source, target_rank) | law epochs with provenance fields already present |

## 6. Execution sketch, cheap first, all on existing rails

- **Phase 0**: `configs/recipe_ir.schema.json` + `receipts/recipe/compile.jsonl`. Seed by TRANSCRIPTION of the four instances above; no new enforcement, the bytes already exist.
- **Phase 1**: `tools/recipe_ladder.py` with `audit`, `render`, `compile-check`; wire `audit` into githooks/pre-push next to the census patrol and ratchet (self-steal of the ratchet's exit-2-only hard-block pattern, tools/workflow_gate.py:9-11).
- **Phase 2**: the compiler self-applies the workflow gate: every compile attempt registers a REGISTRY.jsonl-adjacent row so improvement is a ledger fact; a scenario card suite for the compiler itself, minted from real FAIL rows per the LAW-12 clause (workflow_gate.py:22-31).
- **Phase 3**: prove target-agnosticism with the Luau lowering. Q-032 (commit 0f75d80c8, git log this session) already ran this pipeline by hand: NL swarm mechanics, CLONED_MECHANICS spec landed first, then `shared/Flock.luau`, then a 37/37 luau.exe check with the banked sha. Under RIR, the spec IS the IR, the tuning constants (flee 95 to 14, trail 300 to 38) become typed Coefficient nodes with provenance, and the "scale law documented one place" becomes a literal single Grammar/Constant projection.

## 7. Honest limits

- Parsing English stays statistical. Spans can be wrong; the audit grades confidence and routes low-confidence spans to Ritual (operator confirm), never invents a span. A fabricated span is the one failure the whole apparatus exists to prevent.
- Judgment laws resist typing. "Keeps its lanes at max concurrency on demanded work" (AGENTS.md:34) has no measurable bar; it types as Ritual with a receipt duty, not a Gate. Mis-typing a judgment as a Gate would be the IR's own fabrication smell, and the audit should flag Gate clauses whose params contain no measurable bar.
- Reversibility is clause-level, not phrasing-level: render is faithful to clause structure; operator phrasing freedom survives only through amendments. That is a real (and intended) constraint on operator prose, and the one place the ladder pushes back on its author.
- The tier law means the compiler itself has an unresolved trust boundary: sensing-tier drafts are untrusted input to a funded-tier verifier. RIR shrinks that boundary to a single journal row per compile; it does not close it.

## 8. Literature anchors

Lessig, "Code and Other Laws of Cyberspace" (1999): the estate self-cites him (docs/ref/lessig_1_6.md:1-6, docs/DNA.md:22 "Lessig 1-6") but keeps his "law" and "architecture" modalities as two hand-maintained tables (:8-17 vs :32-39); RIR is the missing compiler between them. Knuth, "Literate Programming" (1984): one source, two projections. Lattner et al., "MLIR" (CGO 2021): multi-level IR with dialects, law-dialect lowering to python- and luau-dialects. Necula and Lee, proof-carrying code (OSDI 1996 / POPL 1997). Pnueli, Siegel, Singerman, "Translation validation" (TACAS 1998). Leroy, CompCert (CACM 2009). Foster et al., lenses (TOPLAS 2007) for the render/parse contracts. Buneman, Khanna, Tan, why-provenance (ICDT 2001). Padioleau, Lawall, Muller, Coccinelle semantic patches (2008): the nearest prior art for law-to-patch compilation with NL documentation. Rondon et al., liquid types (PLDI 2008) for the refinement-flavored Count/Grammar types.

## 9. The one-sentence version

The estate has been writing its own IR by hand all along, in regex-plus-comment blocks and scenario cards and `compiled-v0.3` stamps; RIR is the admission that those artifacts are one type system, and the audit is the tripwire that finally watches the compilers themselves.
