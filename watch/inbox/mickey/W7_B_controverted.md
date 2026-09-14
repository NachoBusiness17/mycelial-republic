# W7-B — CONTROVERTED FINAL 20 THROUGH V2 PROMPT (wave 7, lane B; convergence run)

2026-09-11 · zcode seat · deepseek-chat (T2) fired twice on the remaining 20
CONTROVERTED lines with the G4-2 v2 prompt byte-identical (few-shot-free intro +
classifier-noise disclaimer line + format spec).

**Context a lane has to own:** G5-2 (fired 2026-09-11, `G5_2_controverted_v2.md`)
already ran this exact batch — it answered G4-2's NEXT before wave 7 spawned this
lane. Per wave doctrine (validity = convergence, disagreement is the finding) this
lane re-fired the SAME 20 claims through the SAME v2 prompt and graded blind
before opening G5-2's card. What follows is the independent run PLUS the
convergence check against G5-2. The batch is now argued twice by two calls each;
that is the redundancy the dispute queue wanted anyway.

## THE POINT

1. **Convergence: 20/20 same-side, zero contradictions.** Two independent fires of
   the same prompt landed the same FOR/AGAINST mechanism on every claim — the
   strongest disagreements between runs are emphasis, not direction. The instrument
   is stable, and the v2 prompt fix generalizes: it was never a one-batch fluke.
2. **Count-defense: 0/20.** G4-2 measured 0/10; G5-2 saw a partial reversion
   (call A 6/10, soft); this run: zero count-led AGAINST entries in both calls.
   Pooled across three v2 runs: 6 soft count-openings in 50 claims, all on r>=5
   lines. Confirmed shape: at temp 0.3 the disclaimer REDUCES count-defense
   stochastically; it never defends the classifier outright. The v2 prompt stays.
3. **Cost fell off a cliff:** DeepSeek prompt cache now holds the v2 prefix —
   640/791 and 640/836 prompt tokens were cache hits (79%). Standing-prompt
   economics: the fixed prefix rides at ~10% cost, exactly the fleet's
   constitution-prefix doctrine, measured not theorized.

## RUN RECEIPT (2 calls, within bounds)

- model=deepseek-chat (the T2 lane prior G-runs call deepseek-flash) ·
  max_tokens=8000 (spec; unused headroom — completions ~1.3K each) · temp=0.3 ·
  finish=stop BOTH (no truncation)
- call A: 791 prompt (640 cached) + 1,316 completion = 2,107 tok · 6.8s
- call B: 836 prompt (640 cached) + 1,301 completion = 2,137 tok · 6.6s
- total: 4,244 tok · 13.4s · pennies
- raw: `_w7b_ds_raw_a.txt` / `_w7b_ds_raw_b.txt` (root scratch) · repro:
  `_w7b_deepseek_v2.py` · key from `.env`, header use only, never echoed

## FOR/AGAINST TABLE (condensed; full text in raws; G5-2 column = convergence)

| # | [a/r] | Claim (fragment) | FOR | AGAINST | Resolving evidence | vs G5-2 |
|---|-------|------------------|-----|---------|--------------------|---------|
| 1 | 3/3 | S4 twin I4 re-derive verdict | Reproducible arithmetic should stand or fall on recomputation | Same ambiguous inputs re-run may launder the original error | Full S4/I4 worksheet + independent recomputation from raw exhibits | CONVERGENT (same mechanism: garbage-in re-run) |
| 2 | 2/7 | UNPROVEN via RULE CARD I5-RC-v1 | Deterministic card converts evidence to verdict | Card applicability + exhibit preconditions unshown | Card text + exhibit ID + input/output execution trace | CONVERGENT |
| 3 | 2/6 | INSTANCE I4 contested denominators | Labels a live dispute; resolvable by re-run | No outcome stated; wrong denominator = no resolution | Original I4 run + contested definitions + adjudicated denominator rule | CONVERGENT |
| 4 | 2/5 | ≤6,000-token input allowance | Concrete, testable constraint | 3.5K packet + unstated prefix size may exceed cap; hard-vs-soft unknown | Same-tokenizer token counts of packet AND prefix + governing spec | CONVERGENT ($0 self-check; this run prompted at 791 tok) |
| 5 | 2/5 | DEMOTION <2 independent witnesses | Blocks single-source promotion | Too blunt — one decisive artifact can prove; "independence" undefined | Witness definition + demotion policy text + case history | CONVERGENT (mine sharper: one decisive artifact beats two weak witnesses) |
| 6 | 2/3 | I4 irreducible deck, HOLD 2 slot 4 | Stable indexing claim | "Irreducible deck" + slot rule unstated; staleness unprovable from fragment | Deck manifest with timestamp + slot rules + reduce-counterexample | CONVERGENT (soft both — in-corpus jargon) |
| 7 | 2/3 | C1 keeps SUPPORTED (12) after exclusion | Conditional verdict preservation | Invalid exclusion or non-independent 12 launders the verdict | C1 calculation + exclusion rationale + independence audit of the 12 | CONVERGENT (count-laundering mechanism, 3rd appearance) |
| 8 | 2/3 | LAW-065 third leg SUPPORTED | Artifacts named are concrete and checkable | Demo/warn-only path ≠ operative law; attribution unproven | LAW-065 text + call-site code + ledger contents + attribution record | CONVERGENT (demo≠operative is the sharper cut) — **VERIFIED**: mag/destructive_receipt.py exists (6,508B, 2 LAW-065 refs), ledger 11 rows. 3rd same-day verification across runs |
| 9 | 2/2 | 2,960-leaf dossier as C09 trap row | Deliberate preservation of a known-failure example | Trap designation may invalidate evidentiary reliability | Trap-row definition + dossier manifest + designation rationale | CONVERGENT (soft both — jargon) |
| 10 | 2/2 | INCLUSIVE: exactly 0.3000 MEETS | Precise mathematical claim, checkable | Exclusive reading or rounding convention flips it | Threshold rule text + unrounded share + rounding policy | CONVERGENT |
| 11 | 2/2 | 60.7% CONFIRMED; REFEED_HEAVY | Recorded artifacts, directly checkable | Threshold may be marginal/contested pass, not CONFIRMED | Run manifest with verdict strings + thresholds + timestamped classifier output | CONVERGENT — **PREDICTIVE HIT** (see below) |
| 12 | 2/1 | I2/I3/I4 reconciliation/reconstruction/falsifier | Status report, checkable | Task list ≠ execution; steps may be skipped/mislabeled | Execution trace per step: inputs, outputs, completion | CONVERGENT |
| 13 | 3/1 | Ollama local cheap, always on | Operationally true if configured+used | "Exploratory tip" not a verified capability claim | Routing config + invocation logs + cost/latency | CONVERGENT (lone refute = negation-marker noise; fleet runs HOST ollama eye by design) |
| 14 | 3/1 | DESIGN CONSTRAINTS INHERITED (SUPPORTED, cited) | Provenance claim, diffable | SUPPORTED may be self-asserted; inherited vs independently chosen | Cited Astra source + diff/trace into current design | CONVERGENT |
| 15 | 3/1 | Falsifier verdict, denominator contested | Accurately reports live disagreement | Truncated; "one seat" may not be valid dissent | Full verdict record + each seat's exact denominator | CONVERGENT |
| 16 | 3/1 | 94% PASS, rotation 0.950, ~310 cells | Factual metric report | Numbers may be from different runs; context stripped | Raw metric dump + PASS denominator + bar definition | CONVERGENT — **PREDICTIVE HIT** (see below) |
| 17 | 3/1 | F-H0: 3 consecutive desk rejections | Checkable trigger condition | Consecutiveness unproven; seed identity truncated | F-H0 definition + rejection log checked for 3 consecutive SAME-seed hits | CONVERGENT |
| 18 | 2/1 | ≤8K in/≤1,536 out; thinking=low | Explicit config, verifiable | Aspirational vs actual; thinking=low may not be honored | Per-episode token accounting + thinking-mode setting from logs | CONVERGENT — **PREDICTIVE HIT** (see below) |
| 19 | 2/1 | W5a grounding-wave row, 18/18 PASS | Faithful citation of a timestamped row | Row may be superseded; 18/18 partial; byte-identity unverified | Original wave record at 2026-09-06T17:54:59Z + post-fix hash comparison | CONVERGENT |
| 20 | 2/1 | W5b salon fold excerpt, same facts | Faithful excerpt of the fold notes | **Secondary summary, not independent evidence — inherits any error in the row it cites** | Fold notes vs grounding-wave row side-by-side (timestamp, count, byte claim) | CONVERGENT — **STRONGEST LINE, 3rd independent arrival** |

## PREDICTIVE HITS — the model walks toward disputes the fleet already resolved

Four claims where the resolving evidence the model names is a receipt the fleet
ALREADY holds — the classifier's refutations are noise from context-stripping,
and the model sniffed it from the fragment alone:

1. **Claim 11 (60.7% CONFIRMED):** the fleet's sheet itself carries
   "coldest-vertex gate → CONFIRMED at 60.7%" at net=+3 · refute=0, and boot
   memory records the gate. The refutation on this line is I4-denominator-theme
   bleed on token overlap. Model's named check (run manifest + thresholds) = the
   receipt in hand.
2. **Claim 16 (94% PASS):** boot memory: "mag/refeed_guard.py (B1 REFEED_HEAVY —
   94% of input is re-fed cache reads, falsifier PASS)". The numbers are
   fleet-canonical; the model's "different run" attack is exactly the real risk
   when a fragment strips a number's context — which is what happened here.
3. **Claim 18 (thinking=low, ≥1,536 out):** boot memory's MAX_DISTILL infra
   findings say verbatim "5.3 needs thinking=low + >=1536 max_tokens". The
   metering line is a true config receipt; the refutation is noise.
4. **Claim 20 (W5a/W5b):** the model's AGAINST — secondary summary is not an
   independent witness, inherits any error — is the fleet's grounding-wave v3
   rule (SUPPORTED without source-tracking is demotable), arrived at
   independently for the THIRD time (G3-3/G4-2 witness partitioning, G5-2 claim
   20, now this run). Corpus property, not sample luck. Same for claim 7's
   count-laundering (label-inheritance), also a third appearance.

## GRADING

**Resolvable, convergent, cheap.** 20/20 RESOLVING EVIDENCE entries name a
specific artifact AND a comparison operation (recomputation, execution trace,
diff, side-by-side, hash comparison, same-tokenizer recount). Zero both-sidesism,
zero "more research needed." Soft spots unchanged from every prior run: claims 6
and 9 lean on in-corpus jargon ("irreducible deck," "trap row") — fragment
weakness, not model weakness. Claim 8 re-verified this run (3rd cross-run
verification of a model-proposed check executed same-day: artifacts exist, label
holds).

## VERDICT

**Batch closed with redundancy.** The remaining-20 work now has two independent
deepseek passes in agreement (G5-2 + W7-B), the v2 prompt holds (0/20
count-defense this run, cache-hot prefix), and four predictive hits confirm the
dispute queue surfaces real fleet receipts, not just model confabulation. The
CONTROVERTED instrument is production-shaped: bind it to the desk's dispute queue
alongside G3-3's ten, mark claim 8 CLOSED (verified 3x), and use W5a/W5b +
claim 7 as the standing examples for why witness independence needs
source-tracking, not just seat-tracking.

NEXT (operator-gated, unchanged from G5-2): fold the 20 closures into the desk
dispute queue file; the only NEW residue this run adds is the measured 79%
prompt-cache hit — worth wiring the standing v2 prompt as the desk's default
dispute-queue prompt to keep the prefix hot.

— WAVE 7 LANE B, zcode seat, 2026-09-11
