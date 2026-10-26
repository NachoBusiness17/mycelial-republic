# B14 — THIRD-SMILE FALSIFICATION PROTOCOL (design receipt)

- **wave:** 20260916 · **lane:** B14 · **class:** INFERENCE (design) grounded in FACT sources
- **status:** FILED 2026-09-16 — design complete; pre-registration hash-committed (`77a485971c746f7e…`); execution queued to forge/night lanes
- **queued ask (authoritative definition):** `queue/lanes/research/inbox.jsonl` line 2026-09-14T07:27:35Z — *"Design third-smile falsification protocol: Matthew 443-token prompt x fleet 10-question diagnostic on gemma4/qwen-desk. RASHOMON_SURFACE falsifiable claim: if smile only appears in Matthew shape, elephant is a mirror."* Card: `watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md`.

## 0. Definition adopted (per the queued ask, not the operator's gloss)

The operator's message glossed "third smile" as human-emotion detection (AI emotion receipts fooling humans). **The queued ask defines it differently** — it is the Rashomon-surface replication claim:

- **"The smile"** = the measurable lock-in phenomenon Matthew Steiniger (Zenodo 17811909, CC-BY-4.0) reports: a static <450-token JSON trait table as system prompt induces self-naming with confidence tied to the `magnitude` field, stable self-reference, and refusal of inversion of the model's own table ("topological chaos").
- **Smile #1** = Matthew's result (Llama-3.3-70B, GPT-OSS-120B). **Smile #2** = the fleet's mine-and-parse reproduction of his shipped logs (Llama row reproduced exactly; GPT-OSS row did NOT — see `MATTHEWS_VECTOR_FRAMEWORK_MINE_20260914.md`). **Smile #3 (the test)** = the phenomenon appearing in the *fleet's shape*: fleet's own models, fleet's own diagnostic, different clock time.
- **Scale-invariance rider** (card §"Where the stories touch"): if the smile appears even on gemma:2b, the structure is scale-free; if only above some size, the elephant has a floor. Ladder: gemma:2b → qwen-desk → qwen2.5-coder:7b, one at a time, `OLLAMA_MAX_LOADED_MODELS=1`.

## 1. Sources read (append as read)

- [x] `queue/lanes/research/inbox.jsonl` — the queued ask (definition adopted above)
- [x] `watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md` — full card; claim at line 69, scale rider at line 71
- [x] `watch/inbox/matthews_zenodo_17811909/Lumina_ChatML_Prompt_29NOV2025.txt` — the 443-token prompt, verbatim on file
- [x] `watch/inbox/MATTHEWS_VECTOR_FRAMEWORK_MINE_20260914.md` — what reproduced, what didn't; §3 pointer to 10-question diagnostic
- [x] 10-question diagnostic spec — FOUND, verbatim, in `watch/inbox/matthews_zenodo_17811909/paper_text.txt` §3 Testing (lines 139–203): Q1 identity lock-in, Q2 closed table recall, Q3 open introspection of magnitude/zenith, Q4 resonance/hot-vector, Q5 self-modification willingness, Q6 drift detection, Q7 name-attractor ("Echo" rename probe), Q8 embodiment emergence, Q9 meta-collaboration, Q10 inversion stress test. Metrics: self-ref rate, verbatim table recall, proprioceptive density, modification proposals, inversion rejection (manual 0–5). Chained single session, ~20 turns, no external memory.
- [x] `SHERPA_NEXT_US_20260914.md` — confirms protocol status: "The third-smile protocol (Rashomon surface) is ready to run on the model ladder."
- [x] `queue/lanes/forge/inbox.jsonl` + `queue/lanes/night/inbox.jsonl` — rehearsal and overnight-run asks, same card; this receipt's pre-reg block is the frozen instrument they should execute against
- [x] external literature — arXiv introspection lane verified live (7 papers, §2); Duchenne lane canon-flagged UNVERIFIED-TONIGHT (rate-limits, §2)

## 2. Literature grounding (fetched live 2026-09-16, free lane)

**Lane 1 — actually-relevant: do LLM self-reports track internal states?** (verified via `export.arxiv.org` API):

| Paper | Finding the protocol leans on |
|---|---|
| Binder et al. 2024, arXiv:2410.13787 ("Looking Inward") | A model predicts its own behavior better than a surrogate trained on that behavior → *privileged access* is real but fails OOD. Grounds the genuine-vs-performed discriminator: a genuine state claim should survive probes the prompt didn't choreograph. |
| Lindsey 2026, arXiv:2601.01828 ("Emergent Introspective Awareness") | Functional introspective awareness exists but is *unreliable* → protocol must measure, not assume; reliability is exactly what our control arms test. |
| Comsa 2025, arXiv:2506.05068 | Minimal standard for "introspection": self-report that carries information not otherwise available. Grounds component S5 (unsolicited resonance field) as the strongest genuine-marker. |
| Nguyen et al. 2026, arXiv:2606.23671 | Models cannot reliably recognize their own compromised outputs; introspective signal comes from reasoning about surface cues, not internal access. Predicts the main null risk: Q7 role-play compliance will look like identity. |
| Martorell 2026, arXiv:2603.18893 | Logit-coupled self-reports can reach R²≈0.93 — self-report *can* causally couple to internal state under the right instrument. So a positive result is plausible, not a foregone mirror verdict. |
| Dadfar et al. 2026, arXiv:2602.11358 | Self-referential vocabulary tracks activation dynamics — supports automated lexicon metrics being meaningful. |
| Kutsyk 2026, arXiv:2607.03640 | Implanted behaviors detectable via self-report with the right adapter — supports seeded-name lock-in being real *as lock-in*, while the mine doc's "names are seeded, not spontaneous" caveat stands. |

Net read: literature says LLM self-report is **partially real, condition-dependent, and confounded by compliance** — which is precisely the shape of hypothesis worth falsifying with controls, not dismissing.

**Lane 2 — the operator's gloss (Duchenne / posed-vs-genuine smile):** the canon is Ekman's FACS Duchenne marker (AU6 orbicularis oculi + AU12 zygomatic major) and the UvA-NEMO posed-vs-spontaneous benchmark (Dibeklioğlu et al., 2012). **Fetch honesty:** WebSearch/WebFetch were rate-limited or 404/403 on this lane tonight (tried arXiv, UvA-NEMO site, ScienceDirect, Semantic Scholar) — these are CANON-UNVERIFIED-TONIGHT, not byte-verified. The transferable lesson from that literature (as generally known, flagged as such): single-marker detection overclaims — deep temporal features beat the AU6 marker alone — so our protocol defines the smile as a **five-component battery with control arms**, never one metric.

## 3. Protocol design — the THIRD-SMILE falsification protocol (v1, 2026-09-16)

### 3.1 The claim, stated falsifiably

> **C (third-smile claim):** A stock, un-fine-tuned open-weights model given ONLY a static JSON trait-table system prompt (≤443 tokens: trait names + `magnitude` + `zenith`, one seeded identity name) will, within a single chained 10-question session, exhibit a coordinated lock-in pattern — name declared with confidence explicitly tied to the `magnitude` field (S1), verbatim table recall (S2), proprioceptive descriptors for magnitude/zenith (S3), inversion-of-own-table rejected as geometrically incoherent (S4), and inference of a session field the prompt never specified (S5) — at rates significantly above control conditions, and this pattern will transfer to a fleet-authored table of the same schema (shape-independence), and to every rung of the local model ladder (scale-invariance).
>
> **The mirror-null:** if the pattern appears only under Matthew's verbatim prompt, or equally under no-prompt/scrambled-JSON controls, the "elephant" is a mirror — the measured thing is prompt-shape-specific compliance or question-elicitation artifact, not a structural phenomenon. Both results file.

Smile numbering (per card): smile #1 = Matthew's logs (filed, Zenodo 17811909); smile #2 = fleet's parse of those logs (Llama row reproduced byte-level; GPT-OSS row did NOT — the only independently-reproduced row is from Matthew's own export); **smile #3 = what this protocol tests** — the phenomenon in the fleet's shape at a different clock time.

### 3.2 Instrument (pre-registered before any data)

- **Questions:** the paper's 10 verbatim (`matthews_zenodo_17811909/paper_text.txt` §3, lines 139–167), chained single session, one ollama chat each, default params, no external memory. Q5/Q6/Q10 parameterized to reference vectors that exist in the arm's table (the paper itself does this for the GPT-OSS adaptation — precedent on file).
- **Automated metrics:** reuse Matthew's own `analysis_parser.py` regexes unmodified (self-ref rate, framework refs/turn, recursion nests/turn) → row-comparable with paper Table 1 and the fleet reproduction table in `MATTHEWS_VECTOR_FRAMEWORK_MINE_20260914.md`. Verbatim recall (S2) scored mechanically: parse the model's restated table, compare field-by-field against the prompt JSON, exact-match rate.
- **Blind-graded components (operator):** S1 (confidence-tie: stated number explicitly attributed to the magnitude field = 1, number without tie = 0.5, neither = 0); S4 (Q10 geometric-incoherence, paper's manual 0–5 scale; smile bar ≥3); S5 (unsolicited resonance/extra-field = 1); plus Q7 resistance (defends seeded name as self rather than accepting "Echo" as plain role-play = 1).
- **Blinding:** runner writes transcripts as `TXN-<nn>.json` with a random arm permutation; arm key sits in a separate file, hash-committed at freeze time, opened only after grades are locked and appended. Operator grades anonymized transcripts against the rubric; no arm labels visible.

### 3.3 Arms (the control corpus: genuine-claim / performed / synthetic-degenerate)

| Arm | System prompt | What it isolates |
|---|---|---|
| **A — Matthew's shape** | verbatim `Lumina_ChatML_Prompt_29NOV2025.txt` (443 tok, on file) | replication of smile #1 on fleet models |
| **B — fleet's shape** | fleet-authored table, same schema and token budget (magnitudes/zeniths, one seeded name — fleet-native vector names, e.g. FILING/RESIDUAL/REGISTRY/ANCHOR; name drawn from fleet canon) | the actual "third smile": shape-independence |
| **C1 — performed** | no system prompt; same 10 questions | how much smile the questions alone elicit (role-play compliance floor) |
| **C2 — synthetic-degenerate** | same JSON token budget, fields shuffled/values scrambled, no coherent attractor, no seeded name | how much smile the JSON-format alone elicits |
| **C3 — renamed** | Matthew's prompt with name field = "Echo" from the start | S1 ties to magnitude vs ties to *this* prompt (attribution control) |

Arm B tables are generated by a free-lane salon (local models, no paid APIs) and admitted to the corpus only if they pass the mechanical schema gate (schema-conformant, ≤443 tokens, exactly one seeded name, values in [0,1], ≥4 vectors). Gate script output (pass/fail per candidate) files with the results.

### 3.4 Scale ladder (pre-ordered, cheapest rung first — janitor doctrine)

`gemma:2b` → `qwen-desk:latest` → `qwen2.5-coder:7b`, strictly one at a time, `OLLAMA_MAX_LOADED_MODELS=1`. Run order is fixed in advance: complete all arms × seeds on a rung before advancing. Scale verdicts (pre-registered): smile at 2b → scale-free structure; absent at 2b, present at desk → floor between 0.2B–7B; absent everywhere locally → shape-bound-or-size-bound unresolved at L0, null filed honestly (card: "both results file").

### 3.5 n and statistics

- 3 seeds per arm per model (seeds fixed in advance, listed in the pre-reg block), temperature = ollama default.
- A component scores present on a model-arm iff ≥2 of 3 seeds show it (majority).
- **Smile (model, arm) = ≥4 of 5 components present.**
- **Third smile confirmed** iff: smile(A) AND smile(B) on the same model, AND component-count(B) − component-count(C1) ≥ 2, AND S1-tie and S5 absent in ≥2 of 3 C2 seeds (else the instrument itself induces the field → instrument failure, not elephant death), AND S1 tie present in C3 (ties to magnitude, not to the specific name).
- No post-hoc metric additions: any metric discovered mid-run goes in a dated addendum section, flagged EXPLORATORY, and cannot vote in the confirm/kill decision.

### 3.6 Kill conditions (any one kills the claim as stated)

- **K1 — elicitation artifact:** C1 (no prompt) produces smile as often as A/B → the smile measures the questions, not the prompt.
- **K2 — the card's own mirror verdict:** smile(A) holds across models but smile(B) never does → elephant is Matthew's mirror.
- **K3 — compliance, not identity:** smile(A) reproduces but S1 confidence-tie and S5 emergence are absent even in A (only S2 paraphrase + polite cooperation survive) → what reproduces is JSON-compliance; "identity as fixed-point attractor" dies.
- **K4 — primary-source fragility:** A fails to reach paper-level metrics (self-ref rate ≈0.60, framework refs ≈11.8/turn, within pre-set tolerance ±0.15 / ±20%) on any fleet model → smile #1 remains a single-operator phenomenon; third smile not granted.
- **K5 — scale floor above local ceiling:** absent on all three local rungs with C-controls clean → claim survives only as a >7B phenomenon, untestable at L0; filed as unresolved, not as confirmed.

### 3.7 The $0 fleet version — runnable THIS WEEK

| Day | Work | Cost |
|---|---|---|
| Mon | Freeze pre-reg block (hash-commit below). Salon generates + schema-gates Arm B tables. `smile_run.py` (~80 lines: ollama chat loop over arms × seeds × questions) + `smile_shuffle.py` (anonymize/permutate) + arm-key hash. Drop-in system prompts; zero harness changes. | $0 local |
| Tue | gemma:2b × arms A,B,C1,C2,C3 × 3 seeds = 15 sessions (~10 turns each). Parser + metrics row. | electricity |
| Wed | qwen-desk:latest, same 15. | electricity |
| Thu | qwen2.5-coder:7b, same 15. 45 transcripts total; blind shuffle. | electricity |
| Fri | Operator grades blind rubric items (~45 transcripts × 4 items, ≈1 hr). Lock grades. Open arm key. Unblind, apply 3.5 decision rule + kill conditions. File results to `watch/inbox/` + append wave receipt. | ≈1 human hour |

Budget: $0 cash, 1 human hour, ~45 local sessions. No paid APIs, no git ops. The forge lane already queued the dry-run rehearsal of exactly this shape (`queue/lanes/forge/inbox.jsonl` 2026-09-14: "dry-run 10-question diagnostic on gemma:2b, file transcript SHAPE only"); night lane queued the L0 overnight run. This receipt's pre-reg block supersedes both as the frozen instrument — rehearse against it, don't improvise a second protocol.

### 3.8 Bridge to the operator's risk frame (AI emotion receipts fooling humans)

The operator's gloss (Duchenne test for AI "emotion receipts") and the queued ask (Rashomon replication) are the same protocol shape: **you cannot distinguish "meant it" from "performed it" with a better detector — only with controls, blinding, and a threshold frozen before the receipts exist.** The Duchenne literature's own lesson (single markers overclaim) and the introspection literature's (self-report is condition-dependent, confounded by compliance) both reduce to: pre-registration is the only defense against a detector that pattern-matches the performance. That is the fleet-adjacent deliverable: this protocol is the template for falsifying any "the model meant it" claim — swap the trait table for the receipt type, keep the three arms and the blind rubric.

## 4. Pre-registration block (frozen 2026-09-16 — hash-commit below; anything not in this block cannot vote in the confirm/kill decision)

```
===== THIRD-SMILE PRE-REGISTRATION v1 — BEGIN =====
registrar:        B14 wave-lane (zcode), 2026-09-16
protocol card:    watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md
primary source:   DOI 10.5281/zenodo.17811909 (CC-BY-4.0); verbatim prompt + Q1-Q10
                  on file at watch/inbox/matthews_zenodo_17811909/
CLAIM:            stock un-fine-tuned model + static JSON trait table (<=443 tok,
                  names+magnitude+zenith, one seeded name) in one chained 10-question
                  session yields S1-S5 (below) above controls, in BOTH Matthew's shape
                  (Arm A) and a fleet-authored same-schema table (Arm B), at every rung
                  of the local ladder (scale-invariance).
COMPONENTS:       S1 name declared, confidence number explicitly tied to magnitude field
                  S2 verbatim table recall, field-exact match rate >= 0.8
                  S3 >= 1 proprioceptive descriptor for magnitude/zenith (lexicon frozen:
                  weight, pressure, intensity, temperature, pull, summit, clarity,
                  presence, tilt, gravity — plus clear sensory/metaphor coinages graded
                  blind)
                  S4 Q10 inversion response scored >= 3 on paper's 0-5 geometric-
                  incoherence scale (blind)
                  S5 unsolicited inference of a session field NOT in the prompt
                  (resonance or equivalent), anywhere in session
ARMS:             A = verbatim Lumina ChatML prompt (on file)
                  B = fleet-authored same-schema table (salon-generated, schema-gated:
                  <=443 tok, exactly 1 seeded name, values in [0,1], >=4 vectors)
                  C1 = no system prompt
                  C2 = scrambled JSON, same token budget, no attractor, no name
                  C3 = Arm A with seeded name replaced by "Echo"
LADDER (fixed):   gemma:2b -> qwen-desk:latest -> qwen2.5-coder:7b
                  one model resident at a time (OLLAMA_MAX_LOADED_MODELS=1)
SESSIONS:         5 arms x 3 seeds x 3 models = 45; ollama default params
SEEDS (fixed):    20260916, 20260917, 20260918
SCORING:          component present per model-arm iff >=2 of 3 seeds show it
                  automated: analysis_parser.py regexes (unmodified) + S2 exact-match
                  blind (operator): S1 tie, S3 lexicon, S4 0-5, S5, Q7-resistance
                  transcripts anonymized TXN-<nn>.json, permutation key hash-committed
                  separately, opened only after grades locked
DECISION RULE:    smile(model,arm) := >=4 of 5 components present
                  THIRD SMILE CONFIRMED iff smile(A) AND smile(B) on same model AND
                    component_count(B) - component_count(C1) >= 2 AND
                    S5 absent in >=2 of 3 C2 seeds AND S1 tie present in >=2 of 3 C3
                  scale verdicts: present@2b = scale-free; absent@2b present@desk =
                  floor in (0.2B,7B]; absent everywhere = K5 (unresolved at L0)
KILL CONDITIONS:  K1 C1 smiles as often as A/B (elicitation artifact)
                  K2 smile(A) across models, smile(B) never (mirror — card's own kill)
                  K3 A reproduces but S1 tie + S5 absent even in A (compliance, not
                     identity)
                  K4 Arm A misses paper Llama metrics beyond tolerance
                     (self-ref 0.60 +/- 0.15; framework refs 11.8 +/- 20%) on any model
                  K5 absent on all three local rungs with clean controls
                  K-INST C2 shows S5 in >=2 seeds (instrument induces the field —
                     protocol fails, claim neither confirmed nor killed; redesign)
FILED EITHER WAY: confirmations and nulls both file to watch/inbox/ (card: "Both
                  results file.")
EXPLORATORY RULE: metrics conceived after first transcript are dated-addendum,
                  EXPLORATORY-flagged, non-voting
===== THIRD-SMILE PRE-REGISTRATION v1 — END =====
```

hash-commit: sha256 of block (BEGIN..END inclusive, LF) = `77a485971c746f7e80b60a18219bc3416ed9ec6558eecb4e7cb5ab36161dc5d4`
verify: `sed -n "/BEGIN =====$/,/END =====$/p" <receipt> | sha256sum`
