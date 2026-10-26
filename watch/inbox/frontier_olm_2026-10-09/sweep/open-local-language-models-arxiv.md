# SWEEP: open-local-language-models via arxiv - 2026-10-09

source-fetched: 2026-10-09

Area: open-local-language-models. Feeds: model garden lanes, local Ollama janitor tier
(gemma:2b scut, gemma4 short worker), model-grid census rib, T0/T1 local-first consent boundary.

## Doors used and their condition

- Pass 1 broad sweep (7 fetches): export.arxiv.org/api/query sorted by submittedDate on
  "open-source large language model" (40 rows), "small language model" cs.CL (40 rows),
  quantization+LLM cs.CL (30 rows), "open weights" cs.CL (25 rows), on-device+language model
  (25 rows), Qwen+release (20 rows), plus arxiv.org/list/cs.CL/recent (one page). All doors
  healthy; no 403s. Candidate pool: 70+ items inside the 2026-09-09 to 2026-10-09 window
  (requirement was 30).
- Pass 2 deep reads (9 items, each fetched and read by this seat): 2610.10827, 2610.00954,
  2609.18005, 2609.24799, 2609.11716, 2609.10016, 2609.23742, 2609.27284, 2609.35833.
- Degradation: arxiv.org/abs/2609.35833 timed out twice (60s each); the recipe fallback
  export.arxiv.org/api/query?id_list=2609.35833 returned the full abstract. Fallback verified,
  not fabricated.
- Local-tools note: the first catalog grep attempt (find /c /v under the bash-shaped shell) was
  interpreted as GNU find and walked C:, writing a 4.5 GB stdout log; log deleted, command
  re-run with .venv\Scripts\python.exe and a python heredoc (exit 0). Counts below come from
  that rerun. A later heredoc probe received 0 bytes on stdin, so the bank file is written via
  this temp script instead.

## Overlap method (run this session)

.venv\Scripts\python.exe grep over catalog/catalog.jsonl (384,088,978 bytes per os.path.getsize)
and a full memory/ walk, 22 patterns. Results:
- Already in catalog (abstract rows under state/arxiv/YYYY-MM-DD/, 06:30Z ingest mtimes):
  2609.10016 MetroLLM-Bench (row mtime 2026-09-10T06:30:57Z), 2609.18005 Calibrated Instrument
  (2026-09-17T06:30:53Z), 2609.11716 Why-Does-PTQ-Work (2026-09-11T06:30:26Z), 2609.23742
  Constrained Decoding (+3 memory hits: memory/runs/corpus_gap_research/ARXIV_REGISTER.json,
  MAP_BACKFILL.json, MAP_BACKFILL.md), 2609.24799 EAQuant, 2609.27581 Step Law, 2609.25611
  Qwen3.8-Omni. Zero hits: 2609.35833, 2609.27284, 2610.00954, 2610.10827 (genuinely new).
- 2609.07370 CPU-MCP sub-2B already has a FULL-TEXT pull in intake:
  watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.07370.txt (48,765 bytes) - the 09-28
  sweep already read it; excluded from the top-8 for that reason.
- MiMo-V2.6 already censused by the estate: watch/inbox/last_mile_20260930/AC3_MIMO.md
  ("AC3 - XiaomiMiMo/MiMo-V2.6-RL-oss census").
- Estate verdict context confirmed on disk:
  watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md lines 1-5 (qwen2.5:7b Q4_K_M vs q8_0 A/B
  is SPEC AMEND ONLY, the owed A/B stays UN-RUN; probe 5 named at
  watch/inbox/frontier_olm_2026-10-03/lens/burns.md lines 118-123 per the amend's own lines
  9-13), and memory/rib/RIB_MODEL_GARDEN_ROUTING.md line 1 (full-grid routing table rib,
  2026-10-01).

## Answers to the four research questions

### RQ1 - releases since 2026-10-01 justifying a janitor-tier replacement

No. Nothing in the window shows an October open release that beats the incumbent janitor tier at
its own job. October releases seen: MiMo-V2.6 (2610.11959) - abstract states no parameter counts
and no weights license, and the estate already censused MiMo-V2.6-RL-oss on 09-30 (AC3_MIMO.md);
no other small-open October release surfaced in six sorted queries. In the wider 30-day window:
Hunyuan-A13B (2609.27284, 80B total / 13B active MoE, dual-mode CoT) is a real release but is a
local-specialist candidate, not a janitor replacement at 13B active; it has ZERO catalog rows
(verified: id-string count 0), so it is a release-watch add. Qwen3.8-Omni (2609.25611) already
has its abstract row.

The decisive signal is the opposite of a base swap: internalize scut into fine-tunes of the
current tier. Evidence, all read this session:
- 2610.10827: a deployed 0.8B fine-tune beats prompted GPT-5.4/GPT-5.6 at ~16x lower serving
  cost.
- 2609.10016: PEFT gain SHRINKS with size (+7.03 points at 2B, -0.91 at 27B) - small bases absorb
  fine-tunes better than big ones, so the 2b-4b class is the right fine-tuning substrate.
- 2610.00954: an SLM ensemble with an SLM judge hits 97.34% IFEval strict, beating gpt-5.4 by
  5.81 points at lower cost - scale the tier by orchestration, not by parameter count.
- Reliability rails are the actual gap: 2609.07370 (full text already in catalog) found only 5 of
  1,000 raw sub-2B responses directly parseable as JSON - recovery parsers did the work;
  2609.23742 shows constrained decoding (Outlines/XGrammar) takes schema validity from
  78.6-92.9% to 100% but the semantic gap is scale-dependent and CD-resistant for multi-step
  function calling. Wire constrained decoding into the janitor lane before buying any new model.

### RQ2 - does the qwen2.5:7b Q4-vs-q8 TIE AT CEILING generalize across UNMEASURED cells?

Not as stated. Four independent reads converge on "the tie is conditional":
1. Domain axis: 2609.18005 measured 4-bit indistinguishable from 16-bit at +/-0.3-point
   resolution on prose and Chinese, but 3-bit costs -0.5 (prose) / -0.9 (Chinese) / -1.1 (math),
   and early-exit costs -2.5 on math (19/27 to 6/27 solved). The ceiling is per-task, not global.
2. Family axis: the SAME quantizer cost Meta's model 1.8 points vs Alibaba's 0.7 (2609.18005).
   The ceiling moves with architecture - directly answering LENS 2's open question.
3. Metric axis: 2609.24799 (EAQuant) shows accuracy-preserving W4A4KV4 PTQ still "substantially
   weakens answer-supporting rationales" - an accuracy tie can hide evidence-channel damage.
   Our A/B must score more than task accuracy if janitors ever produce rationales.
4. Mechanism: 2609.11716 identifies PTQ robustness as a PRETRAINED property (counteracting
   residual errors between layers + LM-head geometry preserving top-ranked tokens) that
   "develops during pretraining" - so quantization robustness is expected to differ per
   architecture/training run by construction.
Meanwhile the estate's own A/B remains UN-RUN by design (QUANT_AB_SPEC_AMEND.md lines 3-5) - the
instrument was amended precisely so the run cannot manufacture a verdict. These four reads say:
keep it un-run until its scorecard includes a second axis (evidence/rationale quality) and at
least one non-Qwen family cell, and adopt the Calibrated Instrument's judge-calibration +
null-condition methodology for the whole UNMEASURED grid.

### RQ3 - wire the green arXiv door into model-garden intake

The abstract half of the pipe ALREADY EXISTS: catalog rows land daily at ~06:30Z under
state/arxiv/YYYY-MM-DD/ (three independent mtimes observed: 06:30:57Z, 06:30:53Z, 06:30:26Z),
and the sweep zone already lands full-text pulls as intake rows
(watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.07370.txt). What is missing is the
TRIGGER between them: on abstract ingest, regex title+abstract for
release|small language model|quantiz|on-device|edge|open (source|weights) and auto-enqueue an
export.arxiv.org full-text fetch into the mine shelf (LENS 1: 97,867 mine rows, agent_platform
72,329) before a sweep needs it. Every query used this session is machine-readable Atom from the
same door the abstract ingest already rides - no new infrastructure, one scheduler hop.

### RQ4 - which shelves already document small-model serving, which cells need fresh pulls

On disk today: corpus/library/lmcache-src/ (LMCache serving docs, including recipes/gemma4.po -
cache-side serving for our own short worker), plus the ask's LENS 1 counts (ms-genai 12,142
rows, openai-cookbook 3,120 rows). Cells needing fresh pulls, in priority order:
1. EAQuant full text (github.com/dut0817/EAQuant) - per-family quantization evidence axes.
2. Calibrated Instrument code (github.com/jerrykaplan/Calibrated-Instrument) - the grid
   measurement harness, judge calibration + null condition, ready to port onto the model-grid
   census rib.
3. MetroLLM-Bench harness (github.com/continker/metrollm-bench, CC BY 4.0) - a worked example of
   measuring a PEFT-tuned 4B student against remote tiers under Q4_K_M serving.
4. Constrained-decoding comparison (Outlines vs XGrammar on 0.6B-4B) full text - janitor lane
   rails.
The abstract rows for all of these exist; the pulls above are the full-text upgrades.

## The nine deep reads (one line each)

- 2609.18005 A Calibrated Instrument... - 4-bit indistinguishable at +/-0.3; costs are
  domain-shaped and family-shaped; code released.
- 2610.10827 Grammar Concept Annotation at Scale - deployed 0.8B beats prompted frontier, ~16x
  cheaper; engagement +15.8%.
- 2609.24799 When Quantization Preserves Accuracy but Not Evidence - W4A4KV4 keeps accuracy,
  breaks rationales; EAQuant objective.
- 2610.00954 Beyond Leaderboards: Tokenomics of Agentic SLM Ensembles - 97.34% IFEval strict,
  +5.81 over gpt-5.4, lower cost; tokenomics framing matches our per-token ledger habits.
- 2609.11716 Why Does Post-Training Quantization Work? - two pretrained-in mechanisms; 45pp.
- 2609.10016 MetroLLM-Bench - 4B Qwen 3.5 student 91.3 Tier 1 vs GPT-5.6 90.6/90.0; 2.6 GB
  Q4_K_M; serving config alone shifts 2.7 points.
- 2609.23742 Constrained Decoding Eliminates Structural Failures... - CD to 100% schema validity;
  instruction-semantic failures remain CD-resistant.
- 2609.35833 Neurosymbolic Routing... - Raspberry Pi 4B, L*-learned DFA router: 98.3% overall,
  8.8x faster / 2.8x more energy-efficient than Program-of-Thought.
- 2609.27284 Hunyuan-A13B Technical Report - 80B/13B-active MoE, dual-mode CoT; release-watch
  add, zero catalog rows (not a janitor candidate).

## OWED / follow-ups

1. Release-watch add for Hunyuan-A13B (2609.27284) - zero catalog rows as of this sweep.
2. QUANT A/B scorecard amendment: add an evidence-quality axis + one non-Qwen family cell before
   firing (grounded in 2609.24799 + 2609.18005).
3. Model-garden intake trigger (RQ3 wiring) - proposal above, one scheduler hop.
4. Full-text pulls 1-4 in RQ4.
