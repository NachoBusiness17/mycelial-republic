# THE ENHANCEMENT STACK — 2026-09-20

*Operator commission: "Think about the ractors and our salons and our head museum and our 72-step process and teasing out. How else can we enhance our functionality here, steal from others and arXiv... we also have vs code logs, grok conversations we can mine, and literally full model weights to explore." Consolidates: tonight's builds, the verified bibliography, the arXiv steal dossier (memory/runs/gapwave/arxiv_multiactor_steals.md, 14 verified steals), the grok corpus map, and the width-ceiling receipts.*

---

## 0. THE WIDTH ANSWER (why we never see 50)

- The lane's ~50-concurrent ceiling is real and RECEIPTED by the fleet's own night lanes (RACTOR_LEGIONS card, 50-wide sustained).
- Daytime waves hit a different wall: **1302 = request-rate window**, tripped by launch bursts and by one key serving every seat at once (main session + clones + sibling + fleet automation).
- Each clone is a long multi-request session, so the agent-count ceiling sits under the request-stream ceiling regardless.
- **The three levers, in order:** (1) ramp staircase (launch 6-8, refill on landing — tonight's paced doctrine); (2) the night window (receipted); (3) more keys — doctrine math: 3 keys = ~150-wide shelf. Holdings today: one Max + one Lite.

## 1. RACTORS — typed verdicts (build: nights' work, rides tonight's scorer)

- **Steal: MiniCheck (arXiv 2404.10774)** — per-claim grounding verdicts (supports/refutes/not-enough-info) with a benchmark; the tri-state SUPPORT/OPPOSE/DISPUTED engine at ~400× lower cost.
- Build: `tools/typed_scorer.py` (already committed, discrimination-proven tonight) becomes the chair-verdict backend — decomposed Nouls per testimony claim, full generation reserved for the cross-examination phase only.
- Effect: salons widen without widening the bill; chairs fire at single-prefill cost.

## 2. SALONS — the layered fold, conformity-guarded

- **Steal: Mixture-of-Agents (arXiv 2406.04692)** — layered proposer→aggregator where each layer synthesizes the anonymized pool of the previous layer. This IS the salon's fixed-point fold; the paper proves the shape beats GPT-4o with open models. Adopt the layer formalism.
- **Steal: Conformity in LLMs (arXiv 2410.12428)** — the scientific basis + two tested interventions (Devil's Advocate, Question Distillation) for the silent-agreement-illegal rule; wire the Devil's-Advocate seat as a standing chair when consensus approaches unanimity (unanimity = contagion suspect).
- **Steal: LLMs as a Jury (arXiv 2607.10139)** — agreement structure of independent models AS the verdict signal; a principled fold for DISPUTED outcomes instead of vibes.
- Context law: salon panes run under the compaction governor's kernel/fold laws (identity kernel verbatim, fold at boundaries).

## 3. HEAD MUSEUM — a stocked, versioned persona library

- **Steal: Persona Hub (arXiv 2406.20094)** — 1B auto-curated personas driving persona-conditioned synthesis; the catalog/diversity engine for stocking museum heads beyond the current canon.
- Build: museum cards become versioned artifacts (passport: provenance, register row, cite-gate, last-fired receipt). Un-fired heads surface on the liveness spine (the shipped-dark organ_vitals — light it first).

## 4. THE 72-STEP INTAKE — fold the paste

- **Steal: MemoRAG (arXiv 2409.05591)** — KV-compressed global memory drafts clues over the WHOLE document that then steer retrieval: global-before-local treatment of heavy pastes. Exactly the 72-step's shape.
- Build: AgentFold semantics — granular-condense recent steps, deep-summarize old ones, kernel (constitution + open gates) never scored. The compaction governor IS this organ; the 72-step becomes its first consumer.

## 5. SOCRATIC TEASING-OUT — the ladder as an organ

- **Steal: Scaffolding Collapse in Socratic Tutors (arXiv 2607.19371)** — names and fixes the failure where questioning ladders cave to pressure and reveal answers (trajectory-weighted DPO + representation alignment). Keeps operator-only rungs operator-only — the exact risk tonight's ladders ran.
- Build: `tools/socratic.py` — ladder templates (docker-arc shape, substrate-salon shape, next-era shape), rung gating, terminal operator-rung invariant. Three hand-runs tonight are the test corpus.

## 6. THE NEW MINES

- **VS Code logs**: burning now — 48 lost sessions, 4/6 slices landed; unique data rescued (steer-tournament rates, sanitization-hop law, READ-THE-FILES origin).
- **Grok conversations**: located — **823 sessions, ~105 MB primary transcripts** at `~/.grok/sessions/` with a prebuilt `session_search.sqlite`; the stalled 08-09 pipeline resumes via `stage2_run.py` (topics 2-5). ONE export to request from the operator: the grok.com data export (both X accounts + partner Super Grok seat) — nothing local holds grok.com-side threads.
- **Full model weights**: the filed 5-model dissection order (saelis athena → mtp-gemma-4-31B → Qwen3.5-4B-MTP → R1-Distill-1.5B → Qwen2.5-32B), logit-lens per the labyrinth card's 434-tensor parse. NIGHT-WINDOW LANE ONLY (the GPU law: no local inference while the family is on the box).

## BUILD ORDER (cheap first, per the F-then-S bench verdict)

1. `tools/socratic.py` (corpus exists: tonight's three ladders) — $0, one session.
2. Ractor-verdict backend swap to typed_scorer — $0, one session + one salon A/B against the old verdict path.
3. Resume the grok pipeline topics 2-5 — $0, script exists.
4. MemoRAG-shape on the 72-step (compaction governor consumer) — after the eval lands (night chain).
5. Museum passports + liveness spine lighting — after the memory-index repair.
6. Weight dissection lane — night windows, scheduled.
