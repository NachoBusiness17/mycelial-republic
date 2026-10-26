# SWEEP: open-local-language-models via arxiv (2026-10-11)

source-fetched: 2026-10-11. Seat: sweep-open-local-language-models-arxiv gopher.
Doors used this session, all ANSWERED with real data: arXiv export API (Atom XML, 8
queries), hn.algolia.com (search_by_date + search). The Reddit door was blocked on
2026-10-11 per the doors lens (lens/doors.md:13, :27) and was not attempted by this seat;
nothing below rests on Reddit. No door degraded during this sweep. ascii only, no em or
en dashes; house quote-normalization noted where the source carried an en dash.

## Method (every count from this session's fetches and greps)

- Pass 1, arXiv export API, 8 queries, sortBy=submittedDate desc: all:"open-weight"
  (40 entries), abs:"open weights" AND cat:cs.CL (40), abs:"open-source" AND
  abs:"large language model" AND cat:cs.CL (38), ti model-family query
  ti:"Qwen" OR ti:"Kimi" OR ti:"GLM" OR ti:"DeepSeek" (21), cat:cs.CL (50),
  cat:cs.LG (30), abs:"local llm" OR abs:"on-device" AND cat:cs.CL (30),
  abs:"we release" AND cat:cs.CL (30). Union of distinct candidates considered:
  well over 60 rows; 30+ distinct LLM-release / serving / gating / quantization
  candidates evaluated for the OLM area.
- Pass 2, deep reads end to end (8): 2610.11451 SAIL, 2610.11959 MiMo-V2.6,
  2610.05343 MemStrata, 2610.03124 Trigger-Tag, 2610.09033 Quad-State,
  2609.15030 GLM-5.3-Flash hybrid-state cache recovery, blokhin.us GridCore note,
  data4sci.com vLLM-at-scale post. Only end-to-end-read items are banked.
- HN door, search_by_date query "local llm" hitsPerPage 30 (newest 2026-10-11) and
  search "llama.cpp serving" numericFilters created_at_i>1759276800 (13 rows).
- Overlap greps run this session: ls of state/arxiv dated dirs; grep -c over
  catalog/catalog.jsonl for 2610.11451 / 2610.11959 / 2610.05343 / 2610.03124 /
  2610.09033 / 2609.15030 / MiMo-V2 / GridCore / MemStrata / Kolibri / Kisoku /
  SRA-RiskGate / Qwen3.5-35B-A3B / vLLM; bounded memory grep (memory/lattice,
  memory/research_packs, memory/frontier, memory/corpus, memory/burns,
  watch/inbox/frontier_olm_adhoc, watch/inbox/frontier_olm_2026-10-10). A full
  memory/ recursive grep was started and killed for time (the biography subtree is
  ~577k rows); its partial output (MemStrata, MiMo-V2.6 rows only) is folded in and
  the stop is disclosed per item below.

## Q1. Post-edge releases and the frozen ledger

- The arXiv edge has not moved past the corpus: the cat:cs.CL and cat:cs.LG API
  sorts, both taken 2026-10-11, top out at 2026-10-08T17:59:50Z; the cs.LG fetch
  explicitly reported "No entries were published on 2026-10-09 or later". The
  state/arxiv dated dirs for 2026-10-10 and 2026-10-11 each hold ONE file,
  digest.jsonl, and both are 0 bytes (wc -c), while content-bearing days carry
  ~510 KB digests plus ~240-252 raw txts (2026-10-05: 255 files / 513,787 B;
  2026-10-09: 252 files). So the newest content-bearing sweep day is 2026-10-09,
  and its 300-row digest holds ZERO titles matching qwen|kimi|glm|deepseek|
  open-weight|moe|llama|technical report (grep, 0 hits). No NEW open-weight
  release after the sweep edge existed on arXiv at fetch moment. The empty 10-10
  and 10-11 digests are a sweep-instrument degradation, not a quiet weekend being
  misread: the digest writer ran (files exist) and wrote nothing.
- Roster-class releases AT the edge (2026-10-08): SAIL (2610.11451, "open model
  with 35B total and 3B active parameters", the exact small-ACTIVE-MoE class the
  adhoc Kolibri find named) and MiMo-V2.6 (2610.11959, omni-modal family,
  hybrid-SWA, MoE router frozen during RL). Both are already held as raw sweep
  bytes (catalog rows exist) and neither is a confirmed funded-roster entry:
  SAIL's abs page comments field carries no weights link ("16 pages, technical
  report"), and MiMo-V2.6's abstract open-sources "the training dynamics, RL
  environments, and RL framework" without naming model weights. Weights
  availability on a funded carrier (Nous catalog / xAI SD) is UNVERIFIED: OWED.
- The adhoc run's 7 confirmed finds (watch/inbox/frontier_olm_adhoc/register.jsonl,
  open-local-language-models rows, read this session) ALREADY name three
  open-weight releases the frozen ledger cannot record: Kolibri (2026-10-03,
  78.1B-total / 3.46B-active MoE, Apache 2.0), Kisoku 1.6B (2026-10-08, Apache 2.0,
  GGUF published), Qwen3.8-Flash-Next GSQ GGUF (2026-09-14). The ledger is
  byte-frozen: my own stat this session reads memory/burns/LEDGER.jsonl at
  571,821 bytes, mtime 2026-10-07 08:09:26 local, last content ts
  2026-09-28T19:30:00Z (matches lens/burns.md:49-50, the fifth consecutive frozen
  read), and no writer instrument exists (lens/burns.md:73-76). Every one of those
  releases postdates the ledger's last row, so YES: the frozen ledger cannot
  record them, and the DIGEST/RECEIPT + git commit remains the only mining record
  until a writer is minted.

## Q2. RIB_MODEL_GATES gates + routing-battery cells before a paid call

Gates that must be measured on a new animal FIRST (memory/rib/
RIB_MODEL_GATES_20261001.md, read this session; lens/laws.md:38 is the distill):

1. Per-animal harness profile: transport (streaming-SSE-only on opus, :14-19;
   streaming on grok-4.7, :33-35), rails (max_tokens floors per ask shape, :16-18),
   failure modes and proven shapes. "Never assume the last animal's harness fits
   the next one" (:8-9). A fingerprint change is a NEW animal, cold start, no
   inherited trust (:64-67).
2. Thinking/reasoning control on the wire: the off state must be SENT explicitly
   (omission is a measured ON state on deepseek; RIB_INFERENCE_BUDGET_20261001.md
   :119-131, folded into the gates rib's 2026-10-04 amendment :119-131).
3. mag/inference_budget.py plan_call + guard_terminal on every fire (:76-79):
   EMPTY_REASONING classification (empty content + finish=length + burn evidence)
   is TERMINAL, one marker, never refire the same params (:46-66 via lens/laws.md:39).
4. Paid asks on operator GO (the AA1 gate, :19).
5. Judging independence: never the animal judging itself (glm-on-glm
   contamination caveat, :23-25); ember-1 never the sole judge on a
   dollar-routing verdict (:51-53); second judge family owed.

Battery cells (memory/rib/RIB_MODEL_GARDEN_ROUTING.md:70-193, read this session):
8 columns (code-writing, analysis, extraction, judgment, creative,
adversarial-review, schema-design, planning) x 7 fields (verdict,
price-per-quality, condition, measured-by, moment). Laws: INSTRUMENTS ONLY, a cell
fills from estate instruments, vendor numbers are PLANNING inputs that never
masquerade as verdicts (:47-53); rows carry a moment and EXPIRE at 30 days or a
family event (:54-62); funding and reachability gate which families may fire but
never fill cells (:66-68).

Cheapest LEGAL first call, minimal battery: (a) one plan_call harness probe
(transport + explicit thinking control + max_tokens floor, one cheap ask);
(b) ONE mini-task cell at the F4 census shape (extraction or code-writing, strict
JSON auto-validated) - the measured precedent puts mini-task cells at
$0.0001-0.0002/answer on the flash tier (routing rib :76-78), the cheapest cell
class in the grid; (c) a blind second-family judge on that cell (the F4 shape
used a gemini blind judge, :76-83). Bank the raw row to logs/duel/duels.jsonl or a
model_garden receipt and fill the cell FROM the receipt the same session
(:202-209). Anything that will route dollars later additionally needs the
adversarial-review cell with a second judge family before any verdict is consumed.

## Q3. The HN 'local llm' pool vs estate tooling gaps

The doors lens confirmed 2,957 total hits on the HN 'local llm' pool
(lens/doors.md:12). This session's search_by_date page (30 newest, top dated
2026-10-11) surfaces, in the serving/gating class: GridCore (GPU-sharing
scheduler, MIT, w512/GridCore), "Local LLM Inference at Scale with vLLM"
(data4sci, 10-09/10-10), SRA-RiskGate-4B (HF model for stablecoin risk gating,
10-05/10-10), "Gauze fixes (some) open-weight LLM deficiencies" (github,
10-08, 1 point, NOT read this session), GMKtec EVO-X3 128GB AMD mini-PC review
(10-11), and an "Ask HN: Best Local LLM Box?" (10-11).

Honest overlap finding: the two strongest (GridCore, data4sci vLLM) were ALREADY
deep-mined by the 10-10 run: watch/inbox/frontier_olm_2026-10-10/sweep/
open-local-models-x.md:21 (full GridCore card with the same measured numbers I
re-read: RTX 4060 Ti 16GB, 4 models at 15.5/16GB, interactive p50 3.4s) and
watch/inbox/frontier_olm_2026-10-10/sweep/inference-efficiency-arxiv.md:17 (full
vLLM digest: DGX Spark GB10, 34 tok/s single to 284 tok/s at 256 concurrency, 69
percent prefix-cache hit). They are mined material, not new finds; both were my
deep reads this session and the numbers matched.

What the estate still LACKS (instrument truth, lens/corpus.md:29 gap holds):
(a) no GPU-sharing scheduler is RUN on the janitor lane (gemma:2b scut +
gemma4 worker co-residency is managed by ollama FIFO, exactly the incumbent
GridCore indicts); (b) the vLLM-class batching win is Linux-only - the 10-10 note
records vLLM "was built from the ground up for Linux", so the Windows fleet
cannot inherit it without a WSL/Linux bridge; (c) safety-venue cross-check
material: corpus holds no ML-benchmark or safety-venue material (lens/corpus.md:29),
and this sweep read two items of exactly that class - Quad-State (NeurIPS 2026
workshop-accepted safety eval of open-weight models) and Trigger-Tag (misuse
detection gating that fails under attack) - neither processed beyond the raw
sweep drop. SRA-RiskGate-4B sits in the adhoc raw hn_localllm.json only
(grep hit); Gauze is unread and unclaimed.

## Q4. GPU-ladder five gates after the 10-10/10-11 carrier waves

Gates per memory/rib/RIB_GPU_LADDER_20261001.md:11-23 (read this session):
1 ARCH SM90/SM100/SM120, 2 VRAM 24GB min / 32 preferred, 3 PRICE (24GB+ Blackwell
under ~$1200, or 5090-class under ~$1700, or used H100 under ~$4000), 4 SOFTWARE
(CUDA 12.8+ NVRTC via cuda-python, plus vLLM or SGLang FP8 in a dogfoodable
container), 5 WORKLOAD (real FP8/MoE QPS demand or the mating->MoE export door).

Verdict: ALL FIVE STILL FALSE. Nothing in the 10-10/10-11 carrier waves moved a
gate input. The only adjacent card is gstd_perimeter_design_20261010/CARD.md
(read this session): its Arm 1 rents "entry GPU like 3090" instances (:34-35) -
RTX 3090 is Ampere SM86, fails gate 1 outright; its prices are self-declared
ESTIMATE-CLASS because "vast.ai pricing page is dynamically loaded" (:6-9), so no
measured Blackwell/5090/H100 price under the gate-3 triggers exists; its purpose
is K gstd-node containers per instance at 1-2GB each (:50-54), not FP8/MoE
serving, so gates 4 and 5 see no new demand; no hardware was acquired, so gate 2
is unmoved and the estate box is still the AMD RX 5600 XT (gfx1010, rib :5-6).
The data4sci DGX Spark (GB10 Blackwell) post is external reading, not an estate
card, and names no purchasable price. The one soft input that DID move:
rental-structure intel (interruptible 50 percent+ cheaper, reserved up to 50
percent off, per-second billing, CARD.md:7-9) - planning-class only, per the
instruments-only law it fills no gate.

## Banked items (all deep-read this session; overlap greps as cited)

See the six items in the submitted register: MemStrata, Quad-State Safety
Evaluation, Trigger-Tag Fragility, SAIL, MiMo-V2.6, GLM-5.3-Flash hybrid-state
cache recovery. Anti-rebank exclusions this session: GridCore and the data4sci
vLLM post (mined 10-10, cited above), Kolibri + Kisoku + the other five adhoc
finds (frontier_olm_adhoc/register.jsonl), Qwen3.8-Flash-Next LoRA-over-GGUF
(adhoc find 1), HuatuoGPT-3 / Project Greenhouse / T-Search / ApexQuant
(listing-seen only, not deep-read, so not banked).

## OWED (named, not asserted)

- SAIL weights: does a public checkpoint exist (HF), and does any funded carrier
  serve it? Not verified this session.
- MiMo-V2.6: weights vs framework-only open-sourcing; note the family already
  runs as a FREE lane (memory/lattice/latest.md:14 "mimo-v2.6-flash-free"), so a
  roster move would be a free-lane upgrade question, not a new animal.
- Sweep digest degradation: 2026-10-10 and 2026-10-11 digest.jsonl are 0 bytes;
  an owner should heal the sweep writer or name the pause.
- Ledger writer: fifth-plus-one frozen read; nothing in this sweep changes that
  debt (lens/burns.md:73-76).
- Gauze (github.com/ggeorgovassilis/llm-gauze) and SRA-RiskGate-4B: surfaced by
  the HN door, not read this session; next seat claims or drops them.
