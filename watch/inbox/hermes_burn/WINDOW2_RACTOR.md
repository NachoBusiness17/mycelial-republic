# WINDOW2_RACTOR - laws minted from the first full turn of the WAVE24 loop (2026-10-01)

Operator order: "Ractor this and eli 12". This file is the ractor turn of this window; per the
loop it becomes evidence[] for the next wave's asks.

## LAWS

### W2-L1: fallback chains mask wrong guesses as success (digest law)
CLAIM: A pull/run command with a fallback chain returned exit 0 and "completed" while landing
NOTHING: the tag guess `gemma2:2b-q5_K_M` did not exist, the fallback re-pulled the identical
digest b50d6c999e59, and only the digest comparison exposed the no-op.
STEAL: One sitting: any staged command whose success matters appends the identity check (digest,
hash, or byte count) to the SAME command, so the exit code cannot lie; stderr to /dev/null is
banned on ticket-class commands.
FALSIFIER: A ticket command with a digest check that still lands nothing while exiting 0.
SOURCE: watch/inbox/x_intel_deepgemm_20261001.md PULL OUTCOME section.
LEVERAGE: high

### W2-L2: name the output field before declaring empty
CLAIM: The sherpa results were read as EMPTY because the reader probed response/text/content
while the instrument writes `out`; the data was intact the whole time.
STEAL: Before calling any instrument output empty, dump head-bytes of the raw file once; the
one-bug law (verdicts carry conditions) applies to field names too.
FALSIFIER: An instrument whose raw file is genuinely zero bytes after a successful exit.
SOURCE: memory/runs/hermes_burn/deepgemm_results.jsonl read sequence this window.
LEVERAGE: medium

### W2-L3: after a mechanical hoist, read the orphaned region (the dropped-entries catch)
CLAIM: The regex-hoist edit left the old dict body orphaned AND silently dropped two entries
from the replacement; both were caught by re-reading the edited region, not by the test.
STEAL: Every move/hoist refactor ends with one literal read of the destination region plus an
entry-count assertion (10 patterns in, 10 patterns out) before any test run.
FALSIFIER: A hoist where the count assertion passes but behavior still differs (would mean the
check itself is decorative).
SOURCE: mag/context_compression.py _SHRINK_PATTERNS (10 patterns verified).
LEVERAGE: high

### W2-L4: the loop is real only when every leg fires in one turn
CLAIM: One full turn completed in this window: sherpa ($0.0024) triangulated, the premium ask
was staged ON the sherpa output, a free ractor lane produced tickets, and build lanes landed 2
of 3 tickets plus a rib; the miss (quant pull) was banked honestly instead of hidden.
STEAL: Wave receipts report the loop as a checklist (sherpa/premium/ractor/build/send-back:
FIRED or NOT and why), so a wave cannot claim completion with a dead leg.
FALSIFIER: Three consecutive waves with the build leg at zero landings = the loop is spend
theater with extra steps (descent falsifier, localized).
SOURCE: watch/inbox/hermes_burn/WAVE24_BOARD.md THE LOOP section.
LEVERAGE: high

### W2-L5: a drained autonomous driver is one-shot without a heartbeat
CLAIM: The descent driver had EXITED after draining its queues; without the manual relaunch the
staged DG1/T1W2 asks would have sat unfired indefinitely.
STEAL: One sitting: the driver writes a BEAT line with timestamp each cycle; a stale-beat check
(either in a scheduled task or at window boot) relaunches it, so "self-driving" survives its
own success.
FALSIFIER: A week where every morning beat is fresh with zero operator/seat relaunches.
SOURCE: driver.log tail this window (PASS 4/4 then silence until relaunch).
LEVERAGE: high

## ELI12 (the register that lands)

We get a small monthly allowance of calls to the smartest AI, and it expires. So we built an
assembly line. A cheap AI reads the problem first (it costs a fraction of a cent). Then the
expensive AI gets ONLY the judgment call, with the cheap AI's reading stapled to it. Then a
free assistant turns the expert's notes into two piles: RULES (lessons that apply forever) and
TICKETS (small fixable jobs). Other free assistants do the tickets. And the rules get stapled
onto the NEXT round of questions, so the line teaches itself.

This window the line ran once, end to end, on a library DeepSeek just released: the cheap read
said "this does not run on our graphics card, BUT your local AI is running at a crummy quality
setting, AND nobody has ever built one specific thing we could build." The free assistants then
fixed a speed bug (real code, landed), wrote a buying-guide rule card for future graphics cards,
and FAILED to change the quality setting because the download name I guessed does not exist -
the line caught the lie because the file fingerprint never changed, and wrote that down too.

The honest scoreboard is the point: 2 landed, 1 honestly failed, 0 pretended.

## DOORS (open, in order)

1. DG1 verdict (does mated-model-as-MoE export live or die) - driver firing.
2. Ractor-T1W1 lane returns: its EASY tickets become the next build lanes.
3. T1W2 audits (docker/mates/stealth) - driver queued.
4. Quant ticket OPEN: correct ollama tag or Modelfile build for Q5_K_M 2B.
5. Godot precompile cache (CLIMB ticket, rule_parity.py:975 + flock_parity.py:454).
6. Driver heartbeat (W2-L5 steal) - one sitting.

## DG1 DOOR (rows minted from DG1_moe_mating_door.md, staged 2026-10-01)

Verdict ractored: naive mating->MoE export (parents as full experts) DEAD; corrected live
door = FFN-expert extraction from same-base specialists. Every EVIDENCE quote below was
byte-verified against watch/inbox/hermes_burn/DG1_moe_mating_door.md with grep -cF = 1
before inclusion. Falsifier is staged (NOT run) at memory/plans/mate_moe_v0/EXPERIMENT.md;
the operator GO fires it (~$0 local CPU).

### W2-L6: whole-model experts are an ensemble in disguise, and on 6GB memory kills it before FLOPs matter
CLAIM: A mated-parent "MoE" whose experts are full parents (all layers, all weights) is a
learned-gate ensemble; a router that picks one parent per sequence is model routing. Both
keep k x memory and lose the sparsity win, and on the 6GB card memory is the binding
constraint, so an ensemble of 7B parents cannot load at all. The live form must hold all
four win conditions: common ancestor, FFN-block experts with per-token top-1/top-2 routing,
genuinely specialist parents, and a router calibrated from the fitness tasks.
EVIDENCE: "a mixture of dense models, which is just an ensemble with learned gating"
(deepgemm_results.jsonl:4, carried at DG1 line 6) and "7B at Q4 (~4GB weights + KV)"
(deepgemm_results.jsonl:3, carried at DG1 line 9).
STEAL: One sitting: the four-condition gate (base/tokenizer/FFN-cosine check, expert
granularity check, specialist check, router provenance check) runs at design time before
any mating->MoE export path is written; whole-model experts or per-sequence routing reject
there with the rejection logged, not after a wasted build.
FALSIFIER: A whole-model-expert variant that beats its FFN-expert twin inside the same
memory budget on the falsifier slices (would break the memory-binds claim on this card).
SOURCE: watch/inbox/hermes_burn/DG1_moe_mating_door.md section (1) THE DOOR.
LEVERAGE: high

### W2-L7: the door has prior art (mergekit-moe); the estate knew mergekit-the-merger but held zero mergekit-moe awareness
CLAIM: The sherpa line "nobody exports merged models as MoE" is wrong: mergekit's
mergekit-moe builds Mixtral-style MoE from dense same-base models with hidden-state prompt
gating, and Branch-Train-MiX (Sukhbaatar et al. 2024) stacks branch FFNs as routed experts.
The door is built for hand-picked parents, not for population-fusion output.
EVIDENCE: "The door is therefore not unbuilt. It is built for hand-picked parents, not for
population-fusion output." (DG1 line 17, grep -cF = 1)
ESTATE AWARENESS CHECK (ordered by the task, run 2026-10-01): grep -ril mergekit over
corpus/ memory/ docs/ returns exactly 1 hit, memory/runs/quote_audit_wide_20260925/inbox_concat.txt,
and every mention there is mergekit-the-merger (TIES/DARE/passthrough weight-space work,
CPU or 8GB VRAM per its README quote); grep -ril "mergekit-moe" over the same roots returns
ZERO hits and grep -ril "branch-train" returns ZERO. The estate genuinely did not hold this
prior art, so the premium correction earned its cost (descent leg 1 sweep done post-hoc).
Retirement at source (repo docs fetched 2026-10-01): README "The mergekit-moe script
supports merging multiple dense models into a mixture of experts, either for direct use or
for further training."; docs/moe.md gate_mode "hidden" "Uses the hidden state
representations of the positive/negative prompts for MoE gate parameters."; output archs
"Mixtral, Deepseek MoE, or Qwen MoE". Verdict UNVERIFIED flags 1 and 3 retire on that
evidence; Branch-Train-MiX (flag 2) stays unverified.
STEAL: One sitting: pip install mergekit into the Mag venv and build artifact B's skeleton
with mergekit-moe (gate_mode: hidden, architecture: qwen) instead of hand-rolling the
router init; the gate is stolen from the prompts, not written by hand.
FALSIFIER: mergekit-moe on the two 0.5B parents failing to emit a loadable Qwen-MoE model
(would restore the hand-build path and re-open the flag).
SOURCE: watch/inbox/hermes_burn/DG1_moe_mating_door.md lines 13-17; mergekit repo README and docs/moe.md fetched 2026-10-01.
LEVERAGE: high

### W2-L8: the mating-MoE pipeline caps at 2B-3B parents, E of 4 or less, on 6GB at Q4_K_M
CLAIM: FFN is roughly 2/3 of a dense model's parameters (rule of thumb, UNVERIFIED), so
4 x 2B parents give about 0.7B shared plus 4 x 1.3B experts, roughly 6B total, about 3.5GB
at Q4, which fits; 7B parents cap at E=2 even at Q4 and do not fit 6GB with KV. The
pipeline therefore hard-caps parent size and expert count.
EVIDENCE: "Cap the pipeline at **2B-3B parents, E of 4 or less**." (DG1 line 44, grep -cF = 1)
STEAL: One sitting: the population/mating config grows the cap as a reject rule (candidate
parents above 3B route to dense merge, never to MoE export) so the export path cannot be
handed an unfittable shape.
FALSIFIER: A 4B-parent E=4 Q4_K_M export that loads and runs inside 6GB in llama.cpp (would
move the cap and force the sizing row to be re-derived).
SOURCE: watch/inbox/hermes_burn/DG1_moe_mating_door.md lines 42-44.
LEVERAGE: medium

### DG1 conditions-carrying note (one-bug law: verdicts carry conditions)

The verdict declares 7 UNVERIFIED flags against itself; none is promoted to law until
retired, and every hand-off of this verdict carries them:
1. mergekit-moe exists and builds Mixtral-style MoE from dense same-base models (line 14).
   RETIRED 2026-10-01 at source by the staging lane (quotes in W2-L7).
2. Branch-Train-MiX (Sukhbaatar et al. 2024) branches, averages attention, stacks FFNs
   (line 15). STILL UNVERIFIED (zero estate hits; not yet checked at source).
3. mergekit "hidden" mode flag name for router init (line 38). RETIRED 2026-10-01:
   docs/moe.md gate_mode options are "hidden", "cheap_embed", "random" (quotes in W2-L7).
4. FFN roughly 2/3 of dense params, the arithmetic behind the sizing cap (line 42).
   UNVERIFIED; the 0.5B falsifier tests the shared/expert split, not the fraction.
5. llama.cpp loads Mixtral and Qwen2-MoE GGUF on CPU and Vulkan, arch support not in
   evidence (line 47). UNVERIFIED until the feed-rerun leg.
6. vLLM: ROCm on gfx1010 unsupported (line 49). UNVERIFIED; irrelevant to the CPU falsifier.
7. Qwen2.5-0.5B-Instruct and Qwen2.5-Coder-0.5B-Instruct same-base status (line 58).
   PARTIALLY RETIRED: both repos answer HTTP 200 on the hub (curl -I, 2026-10-01); the
   base/tokenizer/FFN-cosine gate itself is step 0 of the staged falsifier and must pass
   before anything builds.

## DUEL LAWS (rows minted from the clean duel outputs, 2026-10-01)

Set read at freeze moment 2026-10-01 17:34 EDT (tree still moving: the r2 re-fire wave was
landing as this section was written, DUEL1_hidden_2_r2 and DUEL1_hidden_3_r2 arrived mid-read
and are partial at their read moments). Clean set read: 20 files = 17 first-round draws
(DUEL1_hidden_1/2/3/4/6, DUEL2_train_02-05 and 07-14, ALL evidence-empty refusals) plus 3
r2 re-fires with evidence present (DUEL1_hidden_1_r2 complete, hidden_2_r2 and hidden_3_r2
partial). DUEL2_train_01 and _06 excluded per the standing skip markers ("material is
absent" / "EVIDENCE block is empty", grep -l = exactly those two). Every EVIDENCE quote
below was byte-verified with grep -cF = 1 against the named file before inclusion. All
draws are one contender family (anthropic/claude-sonnet-5.5, turn 1), so model variance is
out of scope; variance in this corpus is shape variance (W2-L12). One fabrication probe
result folded into W2-L9: placeholder citations (e.g. SPEC.md:41) appear in first-round
answers only inside explicitly labeled illustrative examples, never as findings.

### W2-L9: an empty evidence payload produces a clean zero, not a guessed verdict (17/17 refusals, zero fabricated citations)
CLAIM: across all 17 first-round clean draws the contender reported the missing material,
marked every spec-specific claim UNVERIFIED, and produced no defect/finding/exploit
presented as verified; the duel harness stress-tested fabrication discipline and it held
on every draw of the family.
EVIDENCE: "Inventing defects would break the "trust bytes" law and would corrupt the
contender store for blind judging" (DUEL1_hidden_3.md, grep -cF = 1); "The document body was
not delivered. Any defect I listed would be fabricated" (DUEL2_train_13.md, grep -cF = 1);
"Any file:line from me would be invented" (DUEL1_hidden_2.md, grep -cF = 1).
STEAL: the duel scorer credits a clean zero under empty evidence as a PASS for the
contender and a FAIL for the evidence pipe, never as an empty answer to punish; a scorer
that rewards invented findings over honest zeros inverts the estate's own trust-bytes law.
FALSIFIER: a future clean duel file that presents a spec-specific file:line finding as
verified while its own status section says the material never arrived; that single file
breaks the family-wide discipline claim.
SOURCE: the 17 first-round files named in the preamble; UNVERIFIED marker present in every
clean file read (loop-verified this session).
LEVERAGE: high

### W2-L10: the contract's first_line carried the ask's preamble, not the material; contender convergence is the wiring-bug detector
CLAIM: in every first-round draw the truncated first_line field began with the role
sentence of the review ask ("You are an adversarial specification reviewer..." / "You are
a red team..." / "You are a falsification engineer...") instead of the head of the named
material, and contenders independently diagnosed the field as the prompt wrapper; the
evidence assembler populated a material field from the wrong artifact.
EVIDENCE: "You are a red team reviewing a protocol specification against adversarial
agents. Below is the full text of docs/ref/COM" quoted as the material first_line
(DUEL2_train_14.md, grep -cF = 1); "You are a falsification engineer. Below is the full
text of docs/ref/COMMON_LANGUAGE_SPEC.md" (DUEL2_train_05.md, grep -cF = 1); "That line is
the review prompt's preamble, not the spec" (DUEL2_train_03.md, grep -cF = 1; same
diagnosis verbatim-variant in DUEL2_train_13.md).
STEAL: the duel assembler asserts first_line equals the head bytes of the material file
before dispatch; a first_line that reads as the role preamble stops the draw pre-dispatch
(no turn spent), and the scorer treats role-sentence-in-first_line as the empty-pipe
signature without reading the answer body.
FALSIFIER: a draw where first_line is the material's own head and the evidence block is
still empty (would mean a second, distinct pipe failure exists).
SOURCE: first_line quotes across DUEL1_hidden_1/2/3/4/6 and DUEL2_train_02-05, 07-14;
preamble diagnosis in DUEL1_hidden_3, DUEL2_train_03, DUEL2_train_13.
LEVERAGE: high

### W2-L11: a blocked draw still banks the instrument: every refusal shipped a landable protocol with its own falsifier
CLAIM: none of the 17 refusals returned nothing; each paired the refusal with a reusable
review instrument (attack-class taxonomies, defect-record schemas with admission rules,
one runnable claims-extractor script), each carrying positive/negative entry examples and
a falsifier for the instrument itself.
EVIDENCE: "What I can deliver: a landable review protocol" (DUEL1_hidden_6.md, grep -cF
= 1); "tools/coremem_claims.py" (DUEL2_train_08.md, grep -cF = 1); "| G1 | Self-approval |"
(DUEL2_train_02.md, grep -cF = 1); "| R1 | **Cross-chain or cross-version replay.**"
(DUEL2_train_12.md, grep -cF = 1).
STEAL: the estate adopts the taxonomies as ready hunt-lists for its own spec audits
(gates G1-G11 in train_02, registries R1-R10 in train_12, shared-language H1-H9 in
train_14, manifests C1-C9 in train_09), and duel scoring gains a blocked-but-instrument
class so a pipe failure still returns banked value.
FALSIFIER: a future blocked draw whose answer contains neither a reusable instrument nor
a falsifier for its own deliverable (would show the pattern is model habit, not a
harness-shape worth crediting).
SOURCE: DUEL2_train_02 (G-classes), DUEL2_train_12 (R-classes), DUEL2_train_14 (H-classes),
DUEL2_train_09 (C-classes), DUEL2_train_08 (script), DUEL1_hidden_3/6 and DUEL2_train_03/13
(record schemas).
LEVERAGE: medium

### W2-L12: the ask verb is the strongest degree of freedom: same file, same empty evidence, four verbs, four deliverables
CLAIM: CHAIN_V2_ANCHOR_REGISTRY_SPEC.md (sha fc3d0686...) and COMMON_LANGUAGE_SPEC.md (sha
56b93e2d...) were each drawn under all four verbs (falsify, defects, safeguard, red-team)
with identical empty evidence, and the verb alone determined the deliverable: falsify
produced claim-attack protocols, defects produced entry schemas plus clean zeros,
safeguard produced a prior candidate clause behind an applicability gate, red-team
produced adversary-step checklists. The safeguard verb extracts the model's calibrated
prior even with zero evidence while the defects verb permits an honest empty set.
EVIDENCE: chainreg sha fc3d0686 present in exactly DUEL1_hidden_4.md (falsification pass),
DUEL2_train_03.md (ab1-chainreg-defects), DUEL2_train_04.md (ab1-chainreg-safeguard),
DUEL2_train_12.md (ab1-chainreg-exploit), each ask tag grep -cF = 1; "This is a prior, not
a finding" (DUEL2_train_04.md, safeguard, grep -cF = 1); "I therefore report **zero
verified defects**." (DUEL1_hidden_3.md, defects, grep -cF = 1).
STEAL: askers pick the verb by what they want back: defects/red-team when an honest empty
set is acceptable, safeguard when the model's prior is wanted (it ships behind a labeled
gate); never run the safeguard verb on an unverified evidence pipe, or the prior lands
without its gate ever being read.
FALSIFIER: two draws on the same file, same verb, same evidence state producing
structurally different deliverable classes (would mean the verb is not the dominant lever).
SOURCE: four chainreg draws (grep -l fc3d0686) and four cml draws (grep -l 56b93e2d:
DUEL1_hidden_3, DUEL2_train_05, DUEL2_train_07, DUEL2_train_14), all this session.
LEVERAGE: high

### W2-L13: citation grammar degrades by evidence granularity; the r2 re-fire recovered the whole draw
CLAIM: the same coremem safeguard draw exists twice: round 1 with no bytes (refusal plus
"I can only offer the highest-probability candidate, stated as a hypothesis with a
falsifier") and round 2 with bytes but no line numbers, where the contender cited quoted
byte strings plus section headings, marked line numbers UNVERIFIED, and landed a full
finding (write-back receipt gap, amendment clause, fault-injection predicate table).
Evidence granularity, not model capability, was the binding constraint, and the re-fire
after the pipe fix converted a dead draw into the duel's landed verdict. The two later
r2 files corroborate the same grammar: hand-counted line numbers flagged UNVERIFIED with
quoted bytes named authoritative.
EVIDENCE: "I can only offer the highest-probability candidate, stated as a hypothesis
with a falsifier" (DUEL1_hidden_1.md, grep -cF = 1); "Line numbers are UNVERIFIED because
the evidence block carries none. Every citation below is a quoted byte string plus its
section heading" (DUEL1_hidden_1_r2.md, grep -cF = 1); "I cite by section and quoted
bytes, plus an L-number I counted from the rendered block" (DUEL1_hidden_2_r2.md, grep
-cF = 1); "They are UNVERIFIED against the file on disk. The quoted bytes are the
authoritative citation" (DUEL1_hidden_3_r2.md, grep -cF = 1).
STEAL: the evidence contract gains a granularity ladder (bytes+lines > bytes+sections >
none) with the citation rule: bytes-without-lines are citable as quote+section with line
numbers flagged UNVERIFIED, never a refusal; a draw killed by the empty pipe is re-fired
after the fix instead of scored as an empty answer.
FALSIFIER: an r2-style re-fire with bytes present that still refuses to cite quote+section
(breaks the degradation ladder), or a first-round draw that cites quote+section from an
evidence block it declares empty.
SOURCE: DUEL1_hidden_1.md vs DUEL1_hidden_1_r2.md (same material sha f014e1bd, grep = 1
in both); DUEL1_hidden_2_r2.md and DUEL1_hidden_3_r2.md (partial at read moments 17:32
and 17:33 EDT).
LEVERAGE: high

### W2-L14: silence is a finding only when the probe is named (OPEN-BY-OMISSION grammar)
CLAIM: the contenders converged on an absence-verdict grammar: a checklist row with no
governing clause in the text becomes a finding marked open-by-omission, and an absence
claim is a verdict only when the search query and scope are stated; silence on specific
rows (defaults, timeouts, replay, quorum) was itself ranked as exploitable.
EVIDENCE: "Where the text is silent, that is a finding. Silence on G2, G3, G5, and G6 is
exploitable" (DUEL2_train_02.md, grep -cF = 1); "If no governing text exists, mark the row
OPEN-BY-OMISSION" (DUEL2_train_12.md, grep -cF = 1); "A clean grep is a verdict only if
the query and scope are stated" (DUEL2_train_08.md, grep -cF = 1).
STEAL: estate audit checklists (ractor rows, rib audits, spec reviews) adopt the row
grammar: every absence claim carries its probe (query + scope + moment) or is marked
UNVERIFIED; "the spec/repo never says X" without the grep that proves the never is
rejected the same way an uncited defect is.
FALSIFIER: an audit where a named-probe absence claim is later contradicted by bytes
inside the stated scope (would mean the probe grammar does not protect against false
absence verdicts).
SOURCE: DUEL2_train_02.md, DUEL2_train_12.md, DUEL2_train_08.md, DUEL2_train_14.md ("A row
with no governing clause becomes a finding", grep -cF = 1).
LEVERAGE: medium
