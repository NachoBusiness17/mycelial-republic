# w3-quantizer-theory: The Thought Quantizer, Formalized as Rate-Distortion

- Item: w3-quantizer-theory (flash50 wave, 2026-09-28)
- Canonical bank: `watch/inbox/burn_reset_20260927/flash50/w3-quantizer-theory.md`
- Mirror (byte-identical): `watch/inbox/burn_reset_20260927/flash50/quantizer-rd-curve.md` (the ask's first line named this path; both files carry identical bytes)
- Type: theory/design. The measurement protocol in section 8 is PROPOSED, NOT RUN. Every file claim below was read in this session at the cited path and lines; every check below was executed during this ask and its output is in section 11.
- Ask material taken as given: "our thought quantizer maps frontier experience (long text) to flash imperatives (short instructions). This is lossy compression."
- House laws honored in this artifact: no em-dashes; no fabricated numbers; OWED marking instead of invention.

## 1. The object being formalized

The founding doctrine is already in the attic, verbatim (read this session): `attic/kill_list_20260908/mag/frontier_pennies.py:5-8` holds "100 cheap quantized workers < 1 frontier token for reproducible verifiable work" and the loop "spend the scarce frontier allowance ONCE to produce an insight, QUANTIZE it into a cheap distributable form, DISTRIBUTE it to the penny-cheap swarm, and MEASURE the multiplier." The four steps are at `frontier_pennies.py:16-20` (CAPTURE, QUANTIZE to a memlang chord, DISTRIBUTE, MEASURE).

The thought quantizer is that QUANTIZE arrow lifted from analytics to experience: frontier experience X (a session tape, a research haul, a filed workday; 10^4 to 10^6 tokens) becomes a flash imperative Y (10^2 to 10^3 tokens). The MEASURE step is exactly the distortion probe this document formalizes: the pennies multiplier only pays if decision quality survives quantization, and whether it survives is an empirical curve, not an axiom.

The estate already runs two special-purpose quantizers (both read this session, both real code):

- `mag/auto_quantize.py`: adaptive resolution for analytics storage. Docstring `mag/auto_quantize.py:1-25`; quantization levels L0 raw events through L5 emergence snapshots at `:13-19`; the three laws at `:22-24`: anomalies are NEVER quantized (keep raw forever), variance determines resolution (low variance = high compression), and the chain root is always recoverable from any quantization level. The variance-to-level mapping is at `:176-185`.
- `mag/state_quantizer.py`: N Verkle knots compressed into one summary knot. The architecture note at `mag/state_quantizer.py:15-19`: a single Verkle knot representing N previous knots, and "The summary is lossy (like quantization)" while preserving dominant themes, tension trajectory, pattern emergence, drift vectors. `quantize_state` at `:249-282` (N:1 compression ratio recorded at `:280`); `QuantizedMemory.to_agent_context` at `:418-432` formats the result for direct agent-prompt injection; the motivating line is `:403`: instead of reading 50 Verkle knots an agent reads ONE QuantizedMemory.

And the general-purpose encoder is already doctrine: deliberate-ask at `AGENTS.md:28` reads "strong asks = frozen RIB (system+bootloader+manifest+verkle tip) + small ask + output contract + quantize target. Pay the context tax once."

## 2. Formal model

- Source: X ~ P_X, a token stream, |X| in 10^4..10^6 tokens.
- Standing decoder context S: what the flash seat holds for free before Y arrives. S includes the ribs, the AGENTS.md clippy law block, the verb codebook, the receipt grammar, and the repo state on disk. S is amortized across all messages and is never re-transmitted per message.
- Encoder: Q_R maps X to Y with |Y| <= R tokens.
- Oracle channel O: the flash seat can read files at runtime (receipts, repo). Rate spent through O is off-ledger but real: a bare pointer that makes the decoder re-read X is an R0 encoding with the rate hidden in the oracle.
- Decoder: d(Y, S, O) produces an action trajectory A_hat. Reference policy: the frontier seat reading full X produces A*.
- Utility U: the task's own machine grade (tests passed, receipts valid, playtest rate). U(*) is the reference arm's grade.

Distortion, with the fabrication asymmetry the house runs on: an unverifiable emitted claim has NEGATIVE utility because it poisons every downstream decision that trusts the receipt, while a refusal-with-OWED costs only the omission. So distortion is not symmetric squared error:

    D(Y) = normalized utility loss  +  lambda * P_fabricate,   lambda >= 1

and the codebook carries an explicit erasure codeword: OWED, the fleet's word for "the rate was insufficient; the residual is declared missing, not invented." With an erasure codeword, worst-case distortion is bounded at the omission cost. Without one, distortion is unbounded, because a single invented fact corrupts every decision that later trusts the receipt. This is the error-detecting-code argument applied to thought.

## 3. Why "quantizer" is the exact word: the shared codebook

A quantizer transmits a codebook index plus a residual. The reason 10^4..10^6 source tokens can become 10^2..10^3 imperative tokens is that the expensive half of the codebook is ALREADY AT THE DECODER:

- the verb codebook: steal, self-steal, probe, fold, verify, dispatch, sign, wash (`.agents/skills/verb-genomes/SKILL.md:3`);
- the guard codebook: no-fabrication, OWED-if-unverifiable, receipt-with-hash, no em-dash (AGENTS.md clippy block; all enforced on this very ask);
- the procedure codebook: ribs, registry, residual (DNA pipeline: chain tip + registry card, then `residual/{id}.json` plus session card, `docs/DNA.md:35`).

Transmission therefore carries only two things: (a) the index into the shared tables (the verb, the tier, the class), and (b) the residual: the exact strings the decoder's prior cannot reconstruct (paths, counts, names, hashes, deltas). Rate follows surprise. That is the same law `mag/auto_quantize.py:23` states for storage ("Variance determines resolution. Low variance = high compression."), and the same reason DNA stores residual as the constitution and calls the card the coarse-grain (`docs/DNA.md:13` "Residual is DNA"; `:47` "Prune theater, never prune residual core").

Memweave is the encoder-side discipline for exactly this: "models perform on STRUCTURES better than on prose describing the same content" (`.agents/skills/memweave/SKILL.md:13-15`), with its own falsifier at `:26-28`: the weave works when structure-fed seats beat prose-fed seats on the same task at equal tokens; if prose matches structure, cut the weave. That falsifier is a one-line special case of the distortion measure in section 2.

## 4. The rate ladder (what is preserved at each compression level)

| Rung | Budget (tokens, order of magnitude) | Shape | Preserved | Lost | In-fleet instance |
|---|---|---|---|---|---|
| R0 | ~20 | pointer: path + hash + class | retrievability and integrity; any alteration of the source is detectable | all operational content; decisions require the oracle read | a receipt line; the census receipt pointer in `AGENTS.md:27` |
| R1 | ~60 | identity card: what/where/when + claim class | routing: should any seat act on this | how, why, guards | an inbox INDEX row |
| R2 | ~150-300 | imperative: verb + target + guard + receipt path + expected observable | one decision plus its integrity contract | alternatives considered, exception structure, provenance depth | the workflow ask; this very item's ask is an R2 artifact, and its standard block is the guard payload |
| R3 | ~500-800 | card: R2 + falsifier + scope boundary + one worked example | decision + guard + verification criterion + scope | evidence chain, history, counterfactuals | verb-genome L0 contract; memweave card |
| R4 | ~2-4k | pack: standing bonds + brief, structures not prose | standing context that shapes many decisions | narrative coherence, long-range dependencies | context-pack, "min-token pack for your seat" (`AGENTS.md:48`, `:87`) |
| R5 | ~10k | compressed narrative with provenance citations | coherence plus partial provenance | verbatim text begins paraphrasing: quiet distortion enters | `mag.cmd brief` |
| R6 | \|X\| | full source | everything the frontier decoder can use | nothing at the encoder; residual distortion is decoder capability, not rate | the session tape itself |

## 5. What dies first (the distortion ordering)

As R shrinks from R6, coordinate classes die in this order. This ordering is the quantizer's bit-allocation table:

1. Style, voice, redundancy: zero decision mass; free compression.
2. Narrative causality, the storytelling "why": memweave's tested claim is that prose carries no advantage over structure at equal tokens (`.agents/skills/memweave/SKILL.md:13-15`, falsifier `:26-28`).
3. Rejected alternatives (why NOT b): the first real loss. Invisible while reality matches the plan; surfaces as a wrong action the moment reality mutates off the predicted path.
4. Exception structure and long-tail failure modes: `mag/auto_quantize.py:22` already names this class for storage ("Anomalies are NEVER quantized. Keep raw forever.", with 3-sigma detection at `:302-326`). In thought: the anomalous counterexample must survive verbatim or as a pointer, because it is exactly what no aggregate represents and exactly what flips decisions.
5. Provenance chain: evidence, line numbers, receipts. Losing it converts a true imperative into an unverifiable claim, which by house law is not a claim ("Trust bytes, not reports." `AGENTS.md:27`).
6. Calibration: uncertainty, confidence. When this dies the seat no longer knows what it does not know: the fabrication regime begins.
7. The decision variable, the guard, the receipt path: dies last; below it nothing survives and the only honest output is the erasure codeword.

The estate has already run this failure once, empirically (`AGENTS.md:27`): a hand-copied census headline ("1,341 tests / 264 files") kept the NUMBER, a coordinate that feels important, while dropping instrument, moment, and provenance; the true 09-14 trio sums to 1,348, and the stale headline rode 12 days while tests/ grew 31 files, with no gate noticing. Distortion became detectable only when detection code was added (`tools/census_drift_patrol.py:148` defines `parse_carrier`; `:305` is the enforcement call; the B2-249 carrier shape law makes the claim's grammar itself checkable). Lesson, which is the rate-distortion lesson: the headline number survives compression, but the verification payload does not; at low rate, the payload that must never die is the integrity layer, not the impressive-looking figure.

## 6. The curve

For an ideal (unbounded-context) decoder, D(R) is non-increasing in R. For a capacity-limited flash decoder, the prediction is U-shaped:

- too little rate: the seat invents. With lambda >= 1 weighting, this region's distortion is worse than refusal; the encoder's duty here is the OWED erasure codeword.
- too much rate: dilution. The flash seat drowns in narrative and loses the middle of the task. The estate already routes around this region in doctrine: small ask (`AGENTS.md:28`), structures over prose at equal tokens (memweave, section 3), and free-lane long outputs banked as findings only, never as trusted work (driving ladder, `AGENTS.md:32`, paraphrased: free stealth lanes are a sensing surface; verification climbs to the funded tier).

    D |
      |  \  fabrication            dilution
      |   \                          _
      |    \                       _/
      |     \                    _/
      |      \__________________/
      |        ^              ^
      |      R_low          R_high
      +--------------------------------->  R (tokens)
              knee band [R_low, R_high]

Regions: (1) R < R_low: erasure or fabrication; emit OWED, never content. (2) R_low..R_high: the working knee; each ladder rung of section 4 buys a coordinate class back, in the death order of section 5 reversed. (3) R > R_high: dilution; additional source tokens now cost quality. Optimal operating point: the cheapest rung inside the knee whose measured D <= eps.

Pre-registered hypotheses (NOT yet measured; see section 8):

- H1 (knee): D(R3 card) - D(R6) <= 0.1 on fleet-gradable tasks. If true, the R3 card is the standard quantization target and full-rate frontier context is a luxury purchase, not a requirement.
- H2 (dilution, the U-shape): D(R5) > D(R3) for flash decoders on fleet tasks. If false, flash uses long context well and the small-ask doctrine is conservatism rather than physics.
- H3 (guard dominance): stripping the guard + falsifier payload from R3 (leaving decision content unchanged) measurably raises P_fabricate. If true, the integrity layer is load-bearing, not ceremony, and "small ask + output contract" is one law, not two.

## 7. Theoretical minimum information

Decision term (Hamming converse, the Fano family). Let A be the ask's decision variable with k admissible values and prior entropy H(A) bits, evaluated under the decoder's standing context S. To hold decision error at eps:

    I(A; Y)  >=  H(A) - h2(eps) - eps * log2(k - 1)     [bits]

Worked fleet case: an ask where k = 4 verbs could plausibly be meant, H(A) = 2 bits, target eps = 0.05. h2(0.05) = 0.05*log2(20) + 0.95*log2(1/0.95) = 0.216 + 0.070 = 0.286. eps*log2(3) = 0.05 * 1.585 = 0.079. So I(A; Y) >= 2 - 0.286 - 0.079 = 1.64 bits. The decision itself is cheap: order 1 to 3 bits. Fleet asks have small k. The expensive part is not choosing; it is specifying.

Residual term. R_res = sum over task-consumed exact strings s of -log2 p(s given S and O): the self-information of what the decoder cannot reconstruct. Gradients:

- a path listable from the repo: ~0 to 3 bits;
- a measured count: full self-information plus instrument and moment tags (the census denominator law, `AGENTS.md:27`: name instrument, moment, and delta before comparing counts);
- a content hash: all of its bits, and worth every one. `mag/state_quantizer.py:57-58` emits 16-hex ids (64 bits) and `mag/auto_quantize.py:253-255` does the same; a hash is maximal surprise per byte, and its value is not compression but detection: any alternative bit pattern is provably wrong. Hashes are the one coordinate class that must never be natural-language paraphrased.

Scaling: a task with m sequential decisions needs the union of their residuals; the integrity overhead amortizes across the artifact (one receipt per artifact, not per thought). R_min scales O(m) in DECISIONS, not O(|X|) in source tokens. This is the quantitative form of "pay the context tax once" (`AGENTS.md:28`) and of DNA's residual constitution (`docs/DNA.md:13`, `:47`).

Integrity term (constant, non-negotiable). Expected observable + falsifier + receipt path + the OWED erasure codeword: order 50 to 150 tokens, independent of |X|. Below this floor the imperative authorizes effects with no verification channel; the estate cannot distinguish done from claimed, and by house law that is fabrication with extra steps.

Total:

    R_min = O(1) decision bits
          + residual entropy of decision-relevant surprise
          + constant integrity overhead

Plain-language answer to the ask's third question: the theoretical minimum needed to preserve decision quality is NOT a percentage of the frontier text. It is (1) the choice itself, 1 to 3 bits; (2) the exact strings the flash decoder cannot reconstruct from its standing priors and its file reads, tens of bits each, scaling with the number of decisions rather than the length of the experience; (3) a constant verification contract: observable, falsifier, receipt path, erasure codeword. Everything else in a frontier experience is either reconstructible from the estate's standing context or is not consumed by the decision. Practically, the floor is integrity-dominated, which is why the fleet's R2-R3 grammar (verb + target + guard + receipt + falsifier) is already near-optimal on the rate axis. The binding constraint on flash decision quality is the decoder ceiling of section 6 (H2), not the rate floor.

## 8. Measurement protocol (PROPOSED, NOT RUN in this ask)

This item is a theory deliverable; no curve was measured here. Protocol when run:

1. Task set: n >= 20 fleet tasks with machine grades (fix-a-test, verify-a-receipt, land-a-playtest classes), each with a frontier-produced source X.
2. Reference arm: frontier seat on full X, grade U*.
3. Quantized arms: flash seat with encodings at rungs R0..R5 of section 4, same tasks; fabrication flagged by receipt audit.
4. D(R) = (U* - U_R)/U* + lambda * P_fabricate, lambda >= 1.
5. Plot at rungs; knee = cheapest rung with D <= eps (propose eps = 0.1); test H2 by comparing R5 vs R3; test H3 by running R3-minus-integrity as a sixth arm.
6. Cost: one rung per day inside normal waves (dogfood the graders the fleet already runs); a full curve takes about a week.

Falsifiers: F1: D(R2) ~ D(R6) on the task set: frontier experience adds nothing measurable over a well-formed imperative; the quantizer reduces to residual extraction. F2: D(R6) >> 0 even at full rate: distortion is decoder capability, no encoding fixes it, and the funded-tier verification law (`AGENTS.md:32`) is the only remedy. F3: no U-shape: the dilution hypothesis dies and R5-class briefs are admissible for flash.

## 9. Prior art in this repo (the theory, already half-built)

- Variance law as rate allocation: `mag/auto_quantize.py:22-24` and the mapping at `:176-185` are rate-follows-surprise for storage. Transfer to thought: the budget goes to high-variance coordinates (exceptions, anomalies, exact numbers), never to restating the aggregate the decoder already holds.
- Fixed-feature codebook: `mag/state_quantizer.py:15-19`, `quantize_state` `:249-282`, and `to_agent_context` `:418-432` pre-choose which coordinates survive at every rate. Honest caveat: its chain source path is currently a migration placeholder string (`mag/state_quantizer.py:48`), so its N:1 numbers are machinery, not live measurements.
- The multiplier doctrine: `attic/kill_list_20260908/mag/frontier_pennies.py:5-8` and `:16-20`; its MEASURE step is section 8's protocol in miniature.
- Distortion must be detectable, not merely small: the census tripwire (`AGENTS.md:27`; `tools/census_drift_patrol.py:148`, `:305`) is an empirical rate-collapse plus the detection code added afterward. In quantizer terms: the fleet runs error-DETECTING codes (hashes, grammar-checked carriers, gates) rather than trusting any encoding to be faithful.
- The encoding policy: deliberate-ask (`AGENTS.md:28`): pay the context tax once, then transmit small asks with output contracts and quantize targets. Section 7 is that sentence with the numbers filled in.

## 10. The ask's three questions, answered in one place

- Q1, preserved at each compression level: the section 4 ladder (R0 pointer keeps only retrievability + integrity; R2 keeps the decision + its contract; R3 adds falsifier + scope; R4-R5 add standing context and narrative; R6 is lossless at the encoder).
- Q2, what is lost, in death order: the section 5 ordering (style first, then narrative why, then rejected alternatives, then exceptions, then provenance, then calibration, and last the decision variable plus integrity payload).
- Q3, theoretical minimum to preserve decision quality: O(1) decision bits (1-3), plus the entropy of the decision-relevant residual (exact strings the decoder cannot reconstruct; scales with decisions m, not source length), plus a constant integrity floor (~50-150 tokens). The floor is integrity-dominated; the ceiling, not the floor, is what binds flash quality (H2, section 6).

## 11. Receipt: what was read and run in this ask

Read (cited above by path and line): `attic/kill_list_20260908/mag/frontier_pennies.py` (lines 1-30), `mag/auto_quantize.py` (lines 1-457), `mag/state_quantizer.py` (lines 1-485), `.agents/skills/memweave/SKILL.md` (lines 1-29), `TOOLS.md` (lines 640-669), plus line-precise hits from git grep: `AGENTS.md:27`, `AGENTS.md:28`, `AGENTS.md:32`, `AGENTS.md:48`, `AGENTS.md:87`, `docs/DNA.md:1,13,35,47`, `.agents/skills/verb-genomes/SKILL.md:3`, `tools/census_drift_patrol.py:148,305`.

Ran during this ask (exact commands, cmd.exe shell):

1. `git grep -n -i quantize` (concept census; output 35.2MB because attic tarball binaries matched; the md/py hits are quoted in section 1 and 9; full output persisted to the session log `call_e74f67b0a8a345ecb7206f7b-stdout.log`)
2. `git ls-files "mag/auto_quantize.py" "mag/state_quantizer.py"` (output: both tracked, confirming the two quantizer modules exist)
3. Line-number batch: `git grep -n "B2-215" -- AGENTS.md`, `git grep -n "DRIVING LADDER" -- AGENTS.md`, `git grep -n "1,341" -- AGENTS.md`, `git grep -n -i "residual" -- docs/DNA.md`, `git grep -n -i "prose" -- .agents/skills/memweave/SKILL.md`, `git grep -n "wash" -- .agents/skills/verb-genomes/SKILL.md`, `git grep -n "parse_carrier" -- tools/census_drift_patrol.py`, `git grep -n "context-pack" -- AGENTS.md` (all hits cited above)
4. Post-write checks on the banked file, output appended below.

Check results (appended after writing, verbatim):

```
.venv/Scripts/python.exe -c "t=open('watch/inbox/burn_reset_20260927/flash50/w3-quantizer-theory.md',encoding='utf-8').read(); print('EM_DASH_HITS',t.count(chr(8212)),'EN_DASH_HITS',t.count(chr(8211)),'CHARS',len(t))"
EM_DASH_HITS 0 EN_DASH_HITS 0 CHARS 21178
```

Not run in this ask: the section 8 measurement protocol (no frontier-vs-flash arms were executed; this item is the curve's design, not its trace). The census claim quoted from `AGENTS.md:27` (2,303 collected / 352 files) is that carrier's own claim and was not re-collected here.
