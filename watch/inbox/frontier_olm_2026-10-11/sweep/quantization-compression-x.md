# SWEEP: quantization-compression via x (2026-10-11)

source-fetched: 2026-10-11

Area: quantization-compression. Seat: sweep-quantization-compression-x (frontier_olm_2026-10-11 daily).
Window: 2026-09-11 .. 2026-10-11 (last 30 days). Anti-rebank ground read this sitting (in full):
watch/inbox/frontier_olm_2026-10-10/sweep/quantization-compression-x.md, watch/inbox/frontier_olm_adhoc/
sweep/quantization-compression-x.md, watch/inbox/frontier_olm_adhoc/DIGEST.md, watch/inbox/
frontier_olm_2026-10-09/sweep/quantization-compression-x.md (banked-items sections), today's lens dir
(burns/corpus/doors/graph), and memory/research_polished/kv_cache_compaction.md (14,520 bytes, mtime
2026-10-11 03:29:23, stat read this sitting).

## 0. Doors, honestly

- WebSearch `site:x.com`: DEGRADED, same class as day-8/9/10 recorded. The backend drops the
  `site:x.com` operator to general web on every query shape; two queries died in 60 s timeouts
  (1302-class storms) and were re-run successfully on retry. Zero in-window status URLs surfaced
  by search.
- Status-ID discovery: SIX status URLs surfaced across 10+ queries, ALL out of window by
  snowflake triage run this sitting with `.venv/Scripts/python.exe` (`(id >> 22) + 1288834974657`):
  UnslothAI/2056369392666194108 = 2026-05-18, danielhanchen/2054537306732941412 = 2026-05-13,
  danielhanchen/2055274688025378854 = 2026-05-15, UnslothAI/2075566124687892597 = 2026-07-10,
  UnslothAI/2087177146662072546 = 2026-08-11, UnslothAI/2092639558815060281 = 2026-08-22. Window
  floor computed = id 2098199843435446272 (2026-09-11), ceiling 2109071479403446272 (2026-10-11).
- fxtwitter per-status door: GREEN from this seat. One resolve: api.fxtwitter.com/UnslothAI/status/
  2092639558815060281 returned code 200 with full tweet JSON ("Qwen3.8-Flash can now be run
  locally! ... Run on 75GB RAM via Unsloth GGUFs. Qwen3.8-Flash-Next enables CPU RAM / unified mem
  setups to deliver near VRAM speeds."). Out-of-window (Aug 22), used as door health + a lead, NOT
  banked as an item; the GSQ-RCO quant recipe on the same model family is already held (adhoc bank).
- X profile pages via the web-reader tool: WORK without login for timeline TEXT with dates
  (x.com/UnslothAI and x.com/danielhanchen both read this sitting), but the render carries NO
  status permalinks (links truncated), so it is a text door, not an ID door. In-window X-native
  items below banked from it are marked profile-read; the Laya post's permalink was not
  discoverable through any door this sitting.
- HF API + raw README via curl: green. unsloth.ai blog: 403 to WebFetch, JS shell to curl;
  their docs corpus (unsloth.ai/docs/llms-full.txt, 1,846,632 bytes) fetched clean and is the
  primary for the AMD update below.

## 1. Research-question verdicts (the ask's four estate questions)

### 1.1 Why zero confirmed rows across three sweeps while lmcache-src holds 2,331 rows?

NOT wrong doors and NOT a mined-out topic: the sweeps banked plenty (8 items in the 10-10 x-sweep,
29 adhoc items, full quantization-compression-x lanes on 10-08/09/10), and the strongest quant
artifacts kept appearing all window (Dynamic 3.0, ShapeLearn, GLM-5.3-Flash UD ladder). The
confirmation bar was never applied to the area: the adhoc fold's confirmation pass covered only
4 of 8 areas (swarm 6, finetuning 8, open-local 7, kv-cache 2 = 23 finds) and its own honest gap 1
names quantization-compression among the four areas whose "120 banked items carry sweep-level
overlap checks only" (watch/inbox/frontier_olm_adhoc/DIGEST.md:9, :12). Worse for the count: the
one confirmed quant artifact of the window (GSQ-RCO, register row 10) was FILED under
open-local-language-models (DIGEST.md:77), so even a confirmed quant find does not land in the
quantization-compression row count. Corollary: "zero confirmed" is a fold-coverage and
area-filing artifact, not evidence the area is dry; lmcache-src's 2,331 rows
(frontier_olm_2026-10-11/lens/corpus.md:15) are serving-side prior art the sweeps never needed to
re-derive. The fix named by the digest stands: run the uncovered-areas confirmation pass
(backlog owner OWED there, DIGEST.md:98).

### 1.2 What does kv_cache_compaction.md claim, and does the owed re-audit validate or strike it?

Re-audit RUN this sitting (this discharges the "kv-cache provenance re-audit" owed row carried at
watch/inbox/frontier_olm_2026-10-11/lens/burns.md:242, to the extent code checks can). VALIDATED:
- Cache telemetry capture: models/providers.py:562 and :847 both read
  `ch = int(usage.get("prompt_cache_hit_tokens") or details.get("cached_tokens") or 0)` inside the
  doc's cited ranges :558-570 and :847-868 (sed reads this sitting).
- Spike instrument: mag/cost_learn.py:132 (`"spikes": _detect_spikes(win, rates)`), :140
  (`MISS_SPIKE_THRESHOLD = 100_000`), :144 (`def _detect_spikes`), :162 (ratio gate), :261
  (`log_behavioral_event(kind="cache_miss_spike", ...)`), exactly as the doc's finding 4 and the
  verified list claim.
- Telemetry live: logs/provider_usage.jsonl read this sitting = 77,800 rows, hit 974,669,131 /
  miss 36,054,998 = ratio 0.9643, newest cache-bearing row ts 2026-10-11T13:15:14Z (matches the
  doc's "~96-97% hit rows" claim).
- Modules exist: mag/session_maze.py 11,200 B; mag/cache_router.py 10,398 B; mag/cache_map.py
  18,913 B; mag/context_pack.py 87,657 B (ls this sitting).
STRUCK (one stale owed row): doc line 23 claims "`freeze_system_prompt()` and the socratic
tail-buffer never built - repack still rebuilds the pack per turn (grep: absent repo-wide), the
#1 cache killer still live". FALSE as of 2026-09-25: `def freeze_system_prompt` is at
mag/context_pack.py:948 (with `evolving_tail` at :984), wired at mag/agent_cli.py:1061, imported
mag/agent_cli.py:29, tested by tests/test_context_freeze.py, landed in commit 3752abae2
(2026-09-25 23:42 -0400, git log -S "def freeze_system_prompt" -- mag/context_pack.py this
sitting). The doc's next-action 2 is therefore DONE; the doc's verified section was
citation-corrected 2026-10-11 by the adhoc kv-cache steal card (doc line 11) but this owed row was
not refreshed. RULE for the bank: anything citing the doc's "Unverified/owed" list must strike the
freeze_system_prompt row first; the retention-window probe (doc next-action 1) stays owed.

### 1.3 Is the deliberate-ask quantize target (AGENTS.md:30) still right for the funded animals?

The question's premise is a category error, and the answer is NO re-measure row needed. "Quantize
target" in the deliberate-ask law is an OUTPUT-COMPRESSION doctrine, not a model or roster pin:
memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md:64-69 defines it as "Compress toward: the rails above,
the record laws, the current board (what is live, what is owed). Everything conversational is
heat; only the frozen spec persists." It names no model and no quantization format, so Lightning
going FULLY DEAD and DeepSeek going inference-PROVEN (frontier_olm_2026-10-11/lens/burns.md:59-60)
cannot stale it. Roster truth lives one line down in the DRIVING LADDER (AGENTS.md:33-34, amended
2026-09-28/29), which is the surface the roster changes belong to. Third sense for completeness:
mag/distill.py's `quantize(s)` primitive (hash-collapse many-to-one, mag/distill.py:16) is yet
another, unrelated use of the word. No law text conflates them; nothing to re-measure.

### 1.4 Can the distill-don't-dump island be wired, and is distillation practiced in mag/?

Wirable NOW, and the wiring shows distillation is PRACTICED IN CODE, not only recorded. The graph
holds `doctrine:distill don t dump` as a zero-edge node
(frontier_olm_2026-10-11/lens/graph.md:31) while the implementing modules sit one relation away:
mag/distill.py:1-2 opens "distill - the LIQUID-INTELLIGENCE distillation machine ... Makes the
doctrine REAL" and implements boil/quantize/distill/trace/cycle standing wave sw59-62;
mag/max_distill.py:4-7 defines the SkillCandidate v1 experiment "what fraction of a frontier
model's verified advantage can be recovered as an automatically-extracted, mechanically-applicable
policy executed by a cheap model" (the doctrine in one sentence); mag/max_distill_arms.py holds
the arms harness. Both modules already carry module->invariant edges (distill.v1, max_distill.v1;
knowledge_graph.json read this sitting) but the graph has NO relation type for
doctrine-governs-module (graph.md:32), which is why the island exists. Proposed edges:
doctrine:distill-don't-dump -governs-> module:distill.py, module:max_distill.py,
module:max_distill_arms.py, plus a process-level edge to the percolator distill lane. Verdict:
practice is real (three modules), the graph builder is the gap.

## 2. Pass 1 census (35 candidates considered, 2026-09-11..2026-10-11 window triaged)

In-window: UnslothAI Sep 28 Laya post (profile-read); UnslothAI Sep 23 500M-downloads post
(profile-read, names Qwen3.8-27B GGUF as Unsloth's #1 most-downloaded ever); UnslothAI Sep 22
Qwen-Image-2.1 GGUF/FP8 post (profile-read); UnslothAI Sep 17 Docker/RDNA1 post (profile-read);
danielhanchen ~Oct 6 Laya real-time packing demo (profile-read); Dynamic 3.0 GGUFs docs (unsloth.ai);
unsloth/GLM-5.3-Flash-GGUF repo (HF API, lastModified 2026-10-05); byteshape/Qwen3.8-27B-GGUF
(HF API, lastModified 2026-09-18); AMD RDNA1 Docker update 2026-09-17 (docs corpus); Laya
decision-laya docs; Muse Glimmer 30B UD-Q4-K-XL Microsoft Store add-on (Sep 11, considered, weak);
thakicloud Qwen3.8-27B Dynamic-3.0 menu piece (surfaced, not read).
Out-of-window (snowflake-dated, marked): the six status IDs in section 0; llama.cpp MTP support
and the 96.4 tok/s reply (May 19); Unsloth DeepSeek-R1 1.58-bit heritage (2025); ByteShape blog
"30B Qwen on a Raspberry Pi" (Jan 5); Nemotron-3-Nano-Omni NVFP4 (Apr 28); QuantTrio-vs-NVFP4
NVIDIA forum thread (Aug 27, 15 days out; kept as a lead); research.nvidia.com KV-compression
infra post (Jun); blog.lmcache.ai "Stop Calling It KV Cache" (Apr); weka KV guide (evergreen);
GGUF-vs-AWQ-vs-GPTQ piece (Jun); HF/ggml GGUF spec docs (evergreen).
Unresolvable this sitting: the danielhanchen GLM-5.3-Flash GGUF tweet ("most-liked GGUF post"
per a daily.dev aggregation; no status URL); ByteShape "Bonsai" X announcements (the adhoc run's
named OWED; still unindexed - the artifact itself is banked at 4.5 below, which partially
discharges that OWED); AINews October editions (news.smol.ai/issues index ends at Sep 10, read
this sitting - the sibling's OWED stands confirmed, not cured).

## 3. Pass 2 deep reads (fetched and read this sitting)

1. unsloth.ai/docs/basics/dynamic-3.0-ggufs (WebFetch, full extraction).
2. unsloth.ai/docs/llms-full.txt (curl, 1,846,632 bytes; RDNA1/Docker update blocks grepped and
   context-extracted).
3. huggingface.co/byteshape/Qwen3.8-27B-GGUF model card (WebFetch, full extraction) + HF API
   metadata (curl: lastModified 2026-09-18T16:06:20Z, 1,291,514 downloads, 163 likes).
4. unsloth/GLM-5.3-Flash-GGUF: HF API metadata (lastModified 2026-10-05T22:23:39Z, 954,431
   downloads, 466 likes) + recursive tree (70 GGUF files, per-variant GiB sums computed) + raw
   README (curl).
5. unsloth.ai/docs/models/decision-laya (WebFetch, full extraction) + the Sep 28 post text on
   x.com/UnslothAI (web-reader fetch).
6. api.fxtwitter.com/UnslothAI/status/2092639558815060281 (curl, HTTP 200, door health +
   out-of-window detail).

## 4. Banked items (6, strongest first; quotes verbatim from pages fetched this sitting)

### 4.1 Unsloth Dynamic 3.0 GGUFs - the window's flagship quant release, primary page now read
https://unsloth.ai/docs/basics/dynamic-3.0-ggufs (page undated; window anchor Sep 23: the
Sep 23 profile post names "Qwen3.8-27B GGUF" as Unsloth's most-downloaded model ever at the
500M mark, read on the profile page this sitting). Verbatim: "Our dynamic 4bit version is 2GB
smaller whilst having +1% extra accuracy vs the QAT version!" (Gemma 3 27B 5-shot MMLU table:
Unsloth Q4_K_XL 71.47% @ 15.64GB vs Google QAT 70.64% @ 17.2GB). Page claims: ">10% top-1
better accuracy at the same size compared to every other provider"; UD-IQ1_S 6.2GB retains
"around 72% top-1 accuracy yet being 89% smaller"; divergence-300 @32 cliff between UD-Q2_K_XL
(~25%) and UD-IQ2_S (<8-10%); pure PTQ ("no QAT, QAD, or training on the calibration data");
held-out eval sets (300 prompts from Terminal-Bench 2.1, DeepSWE, Harbor, MathArena 2025-26);
MTP module removed at UD-Q2_K_XL and below (~500MB saved); 5.1M Qwen3.8 downloads in 5 days.
ESTATE MOVE: this answers the 10-10 sweep's RQ2 line (QAT-vs-PTQ cell) with the vendor's own
measured table, and extends the held Quesma floor law (see overlap) with the QAT arm and the
held-out methodology the estate's run_ab successor should copy.
Overlap: catalog.jsonl streaming grep (1,136,889 rows): "Dynamic 3.0" 0, "dynamic-3.0" 0,
"UD-Q2_K_XL" 0, "UD-IQ1_S" 0. memory/: the UD-Q2_K_XL term DOES hit
memory/percolator/candidates.jsonl (row ts 2026-10-02T04:17:43Z, status candidate, source
https://quesma.com/blog/qwen38-27b-quantizations-benchmarked): the Quesma third-party ladder
(Q4_K_M matches full on Terminal-Bench 2.1; UD-Q2_K_XL 10.7GB = IF floor; 1-bit collapse) is
HELD. My bank is the primary docs page + the QAT comparison + the held-out-set methodology,
which that row does not carry; it is an upgrade, not a re-bank.

### 4.2 Unsloth adds RDNA1+2 to the Docker lane (2026-09-17 update, verbatim in the docs corpus)
https://unsloth.ai/docs/llms-full.txt (fetched this sitting; update block dated 2026-09-17
titled "Docker + MultiUser + AMD Support"). Verbatim: "We're releasing our new updated Docker
image along with multi-user accounts, RDNA1+2, FP8/INT8 diffusion support, ARM64 CUDA Windows
support and many training, GRPO and inference improvements", highlight bullet "AMD RDNA1 and
RDNA2 support", and the Docker requirement line "Built against ROCm 7.2, covers RDNA1 and newer,
plus CDNA." The AMD guide page also carries "RX 5000-9000 GPUs" in the support range line
(en-dash in the source range normalized to a plain hyphen per seat law). ESTATE MOVE: the estate
box IS RDNA1 (RX 5600 XT, gfx1010; memory/rib/RIB_GPU_LADDER_20261001.md:5), so the GPU-ladder
gate 4 (software) gains a vendor-supported inference/Docker path that did not exist when the rib
was written; the 10-10 sweep's "RX 5600 XT below every tested path" datum was true of the buun
CUDA/ROCm KV-quant fork specifically and is no longer true of the Unsloth lane generally.
TENSION, carried not resolved: memory/corpus/LINKS.jsonl (ts 2026-10-01, gala lane
nonnvidia-stacks) holds "Unsloth's official matrix marks RDNA1 RX 5000 Vulkan-inference-only
while RDNA2/3/3.5/4 and CDNA get full train support" - my fetched update adds RDNA1 to the
Docker/inference surface but does NOT prove RDNA1 TRAINING; the 10-01 reading may still stand
for the training matrix. Probe: run the Unsloth ROCm Docker on the estate box, $0, and record
what actually lights.
Overlap: catalog "RDNA1"/"RDNA 1" 0 hits; memory/ rdna1 hits: memory/corpus/LINKS.jsonl (the
10-01 gala row above) + memory/plans/premium_autopsy/gemma4/DG1/ask.json (hardware context in a
DG1 plan, not the Unsloth update). The dated 2026-09-17 update text is unheld; the matrix
reading is held. Upgrade + tension, disclosed.

### 4.3 unsloth/GLM-5.3-Flash-GGUF: a full 1-bit-to-BF16 UD ladder for the estate's own model family
https://huggingface.co/unsloth/GLM-5.3-Flash-GGUF (HF API lastModified 2026-10-05T22:23:39Z,
IN window; 954,431 downloads, 466 likes; MIT). Raw README (curl) verbatim: "Unsloth Dynamic 3.0
achieves superior accuracy & outperforms other leading quants." and "You can now run
GLM-5.3-Flash in our Unsloth Desktop UI." My measured per-variant sums from the HF tree API
(70 GGUF files): UD-IQ1_S 86.7 GiB, UD-IQ1_M 90.9 GiB, UD-IQ2_XXS 94.9 GiB, UD-Q2_K_XL 101.3 GiB,
UD-Q4_K_XL 186.0 GiB, Q8_0 317.6 GiB, BF16 597.6 GiB (mmproj 1.1 GiB each). ESTATE MOVE: the
estate serves GLM-5.3-Flash via the z.ai API today; a local-serve cell for a 320B/18B-active MoE
at ~87 GiB (UD-IQ1_S, CPU-RAM class) is now a downloadable artifact rather than a research
project - the same "RAM-rich, VRAM-poor" recipe class the GSQ-RCO bank demonstrated. No tok/s
or accuracy numbers for these specific files were read (the README links a llama.cpp PR for
support); feasibility on estate hardware is UNMEASURED and not asserted.
Overlap: catalog "GLM-5.3-Flash-GGUF" 0; memory/ grep: 0 hits. NEW.

### 4.4 Laya Decision models served locally through a Jev-compatible API (Sep 28)
X post (profile-read, x.com/UnslothAI, dated Sep 28 on the fetched page; status permalink NOT
discoverable through any door this sitting) + https://unsloth.ai/docs/models/decision-laya
(WebFetch). Docs verbatim: the Unsloth GUI can "expose Laya and Clef through a TypeSafe-compatible
Jev API, so existing Jev integrations can work by pointing them at your local server" (endpoint
http://localhost:8888/v1/systemone; model alias `jev-latest`). Sizes: Multilingual 678 MB / 4 GB
RAM, 100+ languages, 1024-token context; English and Typed-decisions variants 846 MB / 5 GB;
answers yes/no (`noul`), `choice`, and `score` questions with calibrated probabilities; "requests
take well under a second on most CPUs". ESTATE MOVE: this is the janitor scut class (structured
routing/filtering/tagging decisions) served from a 678 MB artifact with calibrated probabilities -
a candidate beside gemma:2b for the structured-decision slice of the janitor lane, and it speaks
the Jev API the estate's own compaction doctrine already references (LiteLLM "Jev-threshold
compaction", kv_cache_compaction.md finding 5). No accuracy benchmarks on the docs page.
Overlap: catalog "decision-laya"/"jev-latest"/"systemone" 0 ("Laya" 29 = Sentry C++ header
substring noise, path-checked). memory/: the term `systemone` DOES hit
memory/agent_sessions/orc-t39817fa14e.json - a sibling seat was already curl-probing
api.typesafe.ai/v1/systemone and grepping .env for "type|hermes|systemone|jev". CREDIT: the
hosted Jev API surface is known to a sibling lane; my increment is the LOCAL serving surface
(Unsloth Desktop endpoint + Laya model sizes), which that session does not carry.

### 4.5 byteshape/Qwen3.8-27B-GGUF (ShapeLearn): third independent per-tensor-sensitivity instance
https://huggingface.co/byteshape/Qwen3.8-27B-GGUF (HF API lastModified 2026-09-18T16:06:20Z,
IN window; 1,291,514 downloads, 163 likes; Apache-2.0). Card verbatim: ShapeLearn "learns the
optimal datatype per tensor to maintain high quality even at very low bitlengths"; labels are
nominal - "We do not use the conventional quantization profiles as defined in llama.cpp"
(IQ4_XS marks "the closest size class and average bit length"). Ladder: IQ2_XXS 2.56 bpw ~8.8 GB
up to IQ4_XS 3.84 bpw ~13.1 GB, vision-capable, mmproj-bf16 included. Eval set named on the card:
GSM8K, IFEval, MMLU, LiveCodeBench V6, Multi-IF, ACEBench, HumanEval, BFCL V4, vs BF16, with
quality-vs-TPS charts (RTX 5090, 94-119 TPS plain, up to 176 with DFlash2). ESTATE MOVE: (a) the
per-tensor sensitivity law now has three independent 2026 instances (GSQ-RCO held, VeriLoop
composition held, ShapeLearn new); (b) the card's eval set puts tool-calling/agentic axes
(ACEBench, BFCL V4) INSIDE a quant eval - the exact shape the estate's quant A/B successor owes;
(c) partially discharges the adhoc run's "ByteShape Bonsai announcements" OWED: the artifact is
located and read; the word "Bonsai" appears nowhere on the card, and the X-native announcement
remains unindexed (OWED stands, narrowed).
Overlap: catalog "ShapeLearn" 0, "byteshape" 0; memory/ grep: 0 hits. NEW.

### 4.6 Qwen-Image-2.1 GGUF + Dynamic FP8 quants (Sep 22) - diffusion-side, marked
X post, profile-read (x.com/UnslothAI, dated Sep 22 on the fetched page; no permalink). Verbatim
from the fetched page: "Qwen-Image-2.1 can now run locally on 12GB VRAM with Unsloth GGUFs! The
7B model performs on par with Nano Banana 2.0. For higher quality, you can also run Dynamic FP8
on just 6GB of VRAM via offloading." SCOPE: image-diffusion quant, not LLM agents; banked as the
X-door's in-window diffusion-quant datum and a lead for the game/wow art lane. GGUF/FP8 repos
not opened this sitting.
Overlap: catalog "Qwen-Image" 6 substring hits (none the Unsloth GGUF release); memory/ hits are
unrelated run manifests (compaction_eval steps, corpus_selfsteal INDEX, file_dogfood manifest).
Likely-new; confidence capped for scope.

## 5. Instrument log (commands actually run this sitting)

stat on memory/research_polished/kv_cache_compaction.md; sed reads of models/providers.py
(550-575, 843-872), mag/cost_learn.py (128-170, 255-272), mag/context_pack.py (948-1024),
AGENTS.md (25-34), RIB_DEEPSEEK_WINDOW_20261007.md (55-95); grep -n line pins on cost_learn.py
and providers.py; repo-wide grep -rn "freeze_system_prompt" (11 hits, mag/agent_cli.py:29,:1019,
:1061, mag/context_pack.py:948, tests/test_context_freeze.py x5); git log -S
"def freeze_system_prompt" -- mag/context_pack.py (commit 3752abae2, 2026-09-25) and git log -1
-- tests/test_context_freeze.py; venv python streaming tallies over logs/provider_usage.jsonl
(77,800 rows) and catalog/catalog.jsonl (15 patterns); knowledge_graph.json read via venv python
(node/edge dump for "distill"); snowflake triage python over 6 IDs + window floors; curl: HF
API x4 (byteshape, GLM tree x2, GLM README), unsloth.ai/docs/llms-full.txt (1,846,632 bytes),
fxtwitter 2092639558815060281 (200), unsloth.ai/blog/amd (403/JS shell); WebFetch: dynamic-3.0
docs, byteshape card, decision-laya docs, amd-gpus docs (redirect + 404 paths), news.smol.ai/
issues; web-reader: x.com/UnslothAI, x.com/danielhanchen (with_links variant errored MCP -500,
plain variant green); WebSearch: 12+ queries (2 timed out at 60 s, retried clean). Overlap
greps: catalog streaming (section 4 items), recursive memory/ grep x2 (terms list in section 4),
RIB_GPU_LADDER grep (RDNA1 at :5 only, no unsloth/vulkan mentions).

## 6. Falsifier / caveats / OWED

- X status-ID discovery stayed walled: every in-window X-native item is banked profile-read or
  docs-read with the permalink hole stated; the x-history miner (named cure, commit e8eedd8eb)
  remains the structural fix. Nothing here is snippet-invented; every quote traces to a fetched
  page named in section 5.
- The Dynamic 3.0 accuracy claims are vendor self-reported (like the 10-10 Unsloth QAT bank);
  the held Quesma row is the independent third-party check on the same ladder and agrees on the
  floor shape.
- RDNA1 TRAINING on the estate box is unproven; only the Docker/inference support text is
  verified verbatim. The LINKS.jsonl 10-01 matrix reading is newer on that specific question.
- GLM-5.3-Flash local serve: sizes measured from the HF tree API; hardware feasibility, tok/s,
  and accuracy of the UD files unread. No assertion made.
- No pytest run (mining lane; not applicable); no lane config changed; no probe executed - all
  probes named here are $0 follow-ups for an owner to claim.
- The AINews October hole (index ends Sep 10) and the ByteShape "Bonsai" X-post hole are
  confirmed still open; both were OWED by the adhoc fold and remain so.
