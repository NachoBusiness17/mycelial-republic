# Steal card: open-and-local-language-models via x (round 2 revision)

Area: open-and-local-language-models via x. Round 1 drafted 2026-09-29; this
round-2 revision folds the reviewer's six conditions and three missing items
same day. Eight confirmed finds, delivered with the ask (dates 2026-08-14
through 2026-09-10; one correction below moves find 3's tweet to 2026-09-01).
Recovery doors per the ask's source field: WebSearch on site:x.com ran
degraded, finds were recovered via smol.ai AINews issues plus the fxtwitter
door https://api.fxtwitter.com/<user>/status/<id>; X articles via the mcp
web_reader. Confidence: the ask re-carries these at 1, but the run's register
scale is 0.9-0.95 (register.jsonl rows), so this card carries every find at
0.9 and raises to 0.95 only where this session landed raw bytes (finds 3, 4,
8). The round-1 OWED "external facts not re-fetched" is largely closed: this
session ran six of the eight probes and banked seven raw receipts. Every
repo-side claim was re-verified here with named commands; anything still
unverified is marked OWED. No em-dashes anywhere in this card.

## Find 1: Vals Index externally corroborates the K3 leg, refutes the #1 leg as of today

Source: https://x.com/ValsAI/status/2098125164072554545 (2026-09-10).

Claim from the find: "DeepSeek V4.1 Flash is the new #1 open-weight model on
the Vals Index. It beats Kimi K3 while costing $0.30 a test, the cheapest
model in the open-weight top 10."

Round-2 headline fix: this card no longer says the find "closes" the desk row.
The desk row closes only on the desk's own terms (watch/inbox/
DESK_DSV41FLASH_20260911.md:47 "our own benches, our surfaces"); an external
board supports at most.

Probe RAN this session, and it cut the find into pieces (this is the probe
working, not the find failing silently):
- Fetched https://www.vals.ai/ (HTTP 200, 1,297,267 bytes, saved to sweep/
  _raw/vals_home_20260929.html) and https://www.vals.ai/models/
  deepseek_deepseek-v4.1-flash (HTTP 200, 305,311 bytes, saved to sweep/
  _raw/vals_model_v41flash.html).
- K3 leg SUPPORTED by saved bytes: DeepSeek V4.1 Flash accuracy 51.32 vs
  Kimi K3 50.70, and V4.1 Flash sits directly above K3 in both embedded
  homepage tables (positions 19 vs 21 of 37 overall; 4 vs 5 among open
  weights).
- "#1 open-weight" REFUTED as of the fetch (2026-09-29): the open-weight
  table reads 1 MiMo V2.6 Pro 55.20, 2 GLM 5.3 53.51, 3 MiMo V2.6 Flash
  53.23, 4 DeepSeek V4.1 Flash 51.32, 5 Kimi K3 50.70. V4.1 Flash is #4
  open, #19 overall. The 09-10 tweet may describe the board as it stood on
  09-10; today's bytes cannot confirm or deny that. Board movement and tweet
  error are indistinguishable from this artifact.
- Price leg SUPPORTED: the model page carries "$0.30 per test" twice ("per
  test versus $6.47" against the closed comparison, and "the next
  open-weight model" framing consistent with cheapest-open).

Estate grounding: the desk's UNPROVEN row is at watch/inbox/
DESK_DSV41FLASH_20260911.md:46-47 with the next-steps echo at :69; V4.1-Flash
is the held item (catalog grep "v4.1 flash": 11 hyphenated + 3 spaced rows,
this session).

Estate map: feeds the SOVEREIGN MIRROR (substrate ranking) and CONTEXT PACK
secondarily (the cache-floor read at desk :60-61). Port move EXECUTED this
session, per the round-1 condition that the desk line lands only after the
probe saves bytes: two dated bullets appended to the desk tri-state (VALS
CORROBORATION + PARTIAL REFUTATION, and the find-7 OLLAMA CLOUD bullet), with
the own-bench probe at :47 explicitly left open. Receipt: the desk file's
tri-state section, this session's Edit.

## Find 2: Hugging Face acquired by NVIDIA; the weight supply chain is measurable, so measure it

Source: https://x.com/ggerganov/status/2095897173376618881 (2026-09-04).

Claim from the find: "Hugging Face has been acquired by NVIDIA ... Going
forward, llama.cpp/ggml will stick to its founding principles. One of the most
important qualities of the project is to be hardware-agnost[ic]."

Verified this session: the weight path transits HF at runtime. The live local
Ollama server answers `curl -s http://127.0.0.1:11434/api/tags` with an
hf.co/-prefixed GGUF present ("hf.co/prism-ml/Ternary-Bonsai-2-27B-gguf:PTQ1_0",
both session checks). In-repo HF touchpoints: mag/frontier_scout.py:287,
tools/pricing_diff.py:48, mag/hf_space.py:12. Catalog grep "Gerganov": 0.

Round-2 count fix (the critique caught the census disease): the tag list is
read at probe time, never hardcoded. Instrument named: `curl -s
http://127.0.0.1:11434/api/tags | grep -o '"name":"[^"]*"' | wc -l`. It
returned 14 at the round-1 drafting moment and 16 at this round's re-run
(gemma4-hermes:latest and nomic-embed-text:latest among the additions); both
are moment snapshots under the B2-216 same-row-every-moment discipline, and
the probe below reads the list fresh when it runs.

Estate map: feeds the SOVEREIGN MIRROR (supply chain) and the PERCOLATOR.
Round-2 merge per the review: the sibling card's percolator candidate row 4
(watch/inbox/frontier_olm_20260928/percolator_candidates.jsonl, the
license-tier ledger wired from watch/MODEL_VAULT_MANIFEST_20260831.md:11-12)
and this find's provenance need are ONE per-model register, not two parallel
config scans: per live tag, record license {tier, name, source_url} (row 4's
fields) plus pull source and second source (this find's fields). A merged
candidate row is appended this session citing both cards.

Probe (falsifiable, cheap; receipt path named): read the tag list at probe
time, resolve each tag's pull source and second source, land the register at
watch/inbox/frontier_olm_20260928/sweep/_raw/weight_provenance_register.json.
Falsifier: if every janitor-critical tag has a usable non-HF re-fetch path,
the single-vendor dependency is overstated and no mirror backlog row is
filed; if any critical tag resolves to hf.co only, the register row becomes a
real backlog item with the tag list as evidence.

## Find 3: RWKV-7 G1j, 100% RNN, Apache-2.0, weights stamped 20260831

Source: https://x.com/BlinkDL_AI/status/2094785763129151677. Date correction
from the review, verified this session: the fx raw
(sweep/_raw/fx_BlinkDL_AI_status_2094785763129151677.json) carries created_at
"Tue Sep 01 13:53:39 +0000 2026", so the announcement tweet is 2026-09-01,
not 2026-08-31 as the ask's date field and round-1 card had it. The 08-31
date survives in a different place: the weight filenames themselves
(rwkv7-g1j-*-20260831-*.pth), which is presumably where the recovery dating
came from. Both facts now cited to their artifacts.

Probe RAN this session: the missing raw the sweep named at sweep/
open-and-local-language-models-x.md:256 now exists. `curl -s
"https://huggingface.co/api/models/BlinkDL/rwkv7-g1"` landed sweep/_raw/
hf_rwkv7g1.json (2,508 bytes): license apache-2.0, downloads 22,917 (the
find's number, confirmed), and four G1j weight files, all ctx16384, all
stamped 20260831: rwkv7-g1j-1.5b, -2.9b, -7.2b, -13.3b (.pth). The find's
"1.5B/2.9B sizes" confirmed and extended. Repo-side: catalog grep "rwkv7-g1":
0 rows; the 4 bare "rwkv" rows are incidental code, including the in-tree
WKV7 GGML kernel watch/organs/kimodo/kimodo.cpp/ggml/src/ggml-et/et-kernels/
src/rwkv_wkv7_f32.c (kimodo.cpp's own README: a text-to-motion GGML
implementation, so a kernel dig site, not a serving path). The live Ollama
tag list carries no RWKV model.

Estate map: feeds the GOPHER FLEET (janitor doctrine at configs/lanes.yaml:6
and :31-36; gemma:2b and gemma4:latest in the live tags). RNN means O(1)
per-token memory: long janitor sessions stop paying KV rent if the
agent/coding claim survives re-ranking. Round-2 instrument fix per the
review: the re-rank rides the estate's EXISTING janitor battery, not a new
prompt set - watch/inbox/ball2/abliterate-p1.md (20 fleet-shape prompts,
sources at mag/afk_loop.py:41-47 and mag/ghost.py:2905-2911 per its battery
provenance table, 3 runs each = 60 inferences on gemma:2b, script
tools/abliterate_p1_probe.py, banked sidecar
watch/inbox/ball2/abliterate_p1_runs_banked.json; the same 60-inference
battery the round-1 card could not locate and the review found banked
2026-09-29).

Probe (remaining leg; receipt path named): serving-path check - search the
Ollama library and the installed stack for anything that loads RWKV-7 text,
landing the answer at sweep/_raw/rwkv7_serving_path.txt. Falsifier: no
serving path found (expected) means the O(1)-memory janitor stays paper until
someone wires the WKV7 kernel dig into a runner, and the probe's output is
that go/no-go; a found path flips it to building the battery run.

## Find 4: Nemotron 3.5 Lightning fine-tune recipe, now captured verbatim

Source: https://x.com/i/article/2088303137182679378 (2026-08-14, OUT OF
WINDOW on date, stated by the find). Round-2 authorship correction from the
capture: the article is by Fastino Labs (their Fine-tuning agent did the
work) about NVIDIA's Nemotron 3.5 Lightning; page canonical URL is
x.com/fastinoAI/article/2088303137182679378.

Round-2 fix for the provenance hole: the article is now captured verbatim at
sweep/_raw/nemotron35_fastino_article.md (mcp web_reader re-read this
session; metadata matches the sweep's: wordCount 4,978, published
2026-08-14T16:34:01Z). Every number the card banks is rerunnable from the
repo, quoted verbatim in the capture: "27,542 real-harness trajectories with
rank 32, a 2e-4 learning rate, and two epochs. Corrected internal evaluation
moved overall performance from 48.00% to 71.18%. Single-turn performance rose
from 51.42% to 81.88%, while multi-turn changed by less than half a point."
Capture also fixes two round-1 imprecisions: Recipe I's 2e-4 is a deliberate
override of the article's stated ~1e-4 default (Lesson 4), and the adapters
are the two Fastino HF repos under Apache 2.0 (named in the capture), which
answers the find's "adapters released Apache 2.0" line.

Estate grounding: the estate's one touch of this model rode a lane now dead -
catalog row 1c05449cb808, watch/salon_responses/astra_smoke_12/
astra_smoke_12__or-nemotron.md ("lane or-nemotron
(nvidia/nemotron-3.5-lightning:free) - OK - 147399ms", 2026-09-16), and
configs/providers.yaml:19-23 records the B2-61 purge ("nvidia 410 EOL + 404
for-account", receipt watch/inbox/burn_wave_20260926/
B2_61_roster_purge_20260926.md). The recipe is the transferable part; the
model's own lane is gone.

Estate map: feeds the QUANTIZER and the GOPHER FLEET. The quantizer organ is
the standing compiler for tiered instruction packs (tools/thought_quantizer.py:1-2).
The capture's own words are the law: "The adapter taught the model the
interface, not the state discipline. Multi-turn competence needs real
multi-turn trajectories, and synthetic pairs did not move it." The estate's
session tapes are the corpus, so the port is a selection rule: weight
multi-turn seat tapes over synthetic single-turn pairs when compiling
fine-tune curricula. The review confirmed this rule has no existing holding
in the quantizer tree (grep multi-turn over memory/corpus/quantized_thought/
and tools/thought_quantizer.py: 0), so it is genuinely new there.

Probe (falsifiable, cheap, re-targeted per the review at the estate's own
battery; receipt path named): run the abliterate-p1 battery unchanged
(tools/abliterate_p1_probe.py, same 20 fleet-shape prompts, same 3-run shape)
against a second janitor-class tag from the live list (qwen2.5:3b-instruct,
the cache-identity primary at mag/cache_identity.py:78-80), landing the
sidecar at watch/inbox/ball2/abliterate_p1_runs_qwen25-3b.json. Score the
single-turn prompts against the multi-step prompts (the battery's provenance
table distinguishes task shapes) and test the Nemotron asymmetry: interface
gaps close faster than multi-step state gaps. Falsifier: if the two gap
classes come out equal or inverted, the curriculum law has no purchase on
this stack and the card records the non-transfer. Cost: 60 local CPU-class
calls, the same envelope the banked gemma:2b run already paid.

## Find 5: Qwen3.8-Flash-Next at Agent Arena #7 open, banked as a fact (probe cut)

Source: https://x.com/arena/status/2094785763129151677 sibling find, URL
https://x.com/arena/status/2094566204488962483 (2026-08-31, fx raw verbatim
on disk; catalog grep "Agent Arena" and "Qwen3.8-Flash-Next": 0 rows).

Claim from the find: "#7 among open models (#24 overall) with +2.4% net
improvement across 8.7K+ real-world agentic sessions", no VRAM class, no
tool-call JSON accuracy published.

Round-2 fix per the review: the round-1 A/B probe was inert (10 funded-tier
calls to produce "a routing-prior row in the fleet notes, not a roster
change" - a no-op on a pairing the RIB already fixed). Cut. The rank banks as
a fact against the decision point that already exists: the estate is
already warm on exactly this comparison at
memory/runs/fleet_round/burn2b_pack.md:7299 (verified this session), the WARM
entry asking "How is GLM-5.3 Flash compared to Qwen3.8-Flash-Next and
DeepSeek-V4-Flash-0731?" with a practitioner answer. When the estate next
answers that question on the funded lane, this Arena rank is one stored
input; no new spend is authorized for it.

Estate map: feeds the GOPHER FLEET as a stored routing prior, subordinate to
memory/rib/RIB_DRIVING_LADDER_20260928.md:9-12 (ONLY HERMES IS FUNDED;
glm-5.3-prime and qwen3.8-max-prime are the funded pair) and :16-23
(sensing never substitutes for judgment). One cross-check from this session's
own bytes, not the find: on the fetched Vals open-weight table, GLM 5.3 sits
#2 at 53.51, above Qwen 3.8 Max at #6 48.27 - a different leaderboard, but
the same direction the RIB's pairing already picked.

## Find 6: Jetson Unsloth QLoRA-to-GGUF-to-llama.cpp tutorial: zero-port pointer, probe ran

Source: https://x.com/NVIDIARobotics/status/2094480283135316182 (2026-08-31).

Round-2 demotion per the review: round-1's "Port move: none now" was a
disqualifying shape. This find is now a zero-port named-recipe pointer whose
only claims are the URL and what the fetched page verifiably says; no port is
claimed, and the Qwen3.5-4B OWED is resolved one level.

Probe RAN this session: WebSearch located the tutorial at
https://www.jetson-ai-lab.com/tutorials/unsloth-on-jetson; direct fetch
landed HTTP 200, 92,055 bytes, saved to sweep/_raw/
jetson_unsloth_on_jetson.html (the round-1 guessed URL and the site root
both 404'd or carried no unsloth content - the pointer names the URL that
actually served bytes). The page confirms the pipeline verbatim in its
section anchors (#convert-a-model-to-gguf, #run-the-gguf-with-llamacpp, 44
qlora/gguf/llama.cpp hits) and names BOTH find models: "Qwen3.5-4B on Jetson
Orin Nano" and "Nemotron 3.5 Lightning 30B-A3B on Jetson AGX Thor". Two
resolutions: Qwen3.5-4B's existence is now vendor-page-confirmed (its HF
model card remains unpulled, OWED downgraded), and Nemotron 3.5 Lightning's
shape is stated as 30B-A3B (30B total, ~3B active), consistent with the
find-4 capture's "30B-A3B" description from an independent artifact.

Estate map: GOPHER FLEET edge-tier notes only. Honest organ note kept from
round 1: this is a weights pipeline, not the estate's thought quantizer
(tools/thought_quantizer.py compiles instruction packs from invariants); the
mapping is adjacency, named as such. Banked as the named recipe for a future
on-box janitor fine-tune, when one is earned. No port move.

## Find 7: DeepSeek-V4.1-Flash on Ollama cloud: rollout fact probed and landed

Source: https://x.com/ollama/status/2098188014119985406 (2026-09-10, fx raw
verbatim on disk).

Claim from the find: rolled out "starting with Max and Team accounts", more
capacity coming for all subscribers.

Probe RAN this session, both legs:
- Classic registry: `curl -s
  https://registry.ollama.ai/v2/library/deepseek-v4.1-flash/manifests/latest`
  returned HTTP 404 with body {"errors":[{"code":"MANIFEST_UNKNOWN",...}]},
  saved to sweep/_raw/ollama_registry_v41flash.txt. Not pullable from the
  classic registry.
- Library page: https://ollama.com/library/deepseek-v4.1-flash served HTTP
  200 (89,522 bytes, saved to sweep/_raw/ollama_lib_v41flash.html) and the
  page's run line is `run deepseek-v4.1-flash:cloud`. The cloud tier gate is
  real and visible in saved bytes.
- Local grounding: no deepseek-v4.1-flash tag in the live /api/tags list
  (both session counts).

Estate map: feeds the SOVEREIGN MIRROR's Oct 27 decision (desk :7, :66).
Port move EXECUTED this session: the desk's tri-state now carries the OLLAMA
CLOUD ROLLOUT bullet with both receipt paths, feeding the local-weights-vs-
Ollama-cloud leg. This also warms the desk's second UNPROVEN row (:48-49,
API pricing/availability) without closing it: the cloud gate is confirmed,
the price and lane behavior still need a live endpoint.

## Find 8: DeepSeek V4 Flash Vision weights open, MIT confirmed

Source: https://x.com/zizhpan/status/2094386230675062836 (2026-08-31, fx raw
verbatim on disk).

Claim from the find: "Weights open:
https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp".

Probe RAN this session: `curl -s
"https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp"`
landed sweep/_raw/hf_v4flashvision.json (5,883 bytes): license **mit**, id
confirmed. The checkpoint is genuinely open under a permissive license.
Catalog grep "V4-Flash-Vision": 0 rows.

Estate map: feeds the SOVEREIGN MIRROR's vision lane. The target lane exists
and its gap is real: watch/inbox/v41_paces/LANE5_vision.md (head read round
1) establishes V4.1-Flash's ViT is native and trained on screen captures and
computer-use trajectories, and that the model card documents NO image formats
or transport on the API surface; the desk's :65 line ("no separate ollama
eye") names the prize; the live local eye today is qwen2.5vl:3b (in both
session tag counts). Vision-Exp, separately checkpointed and now
MIT-confirmed, is the diff target. Port move: append the MIT confirmation and
raw path to LANE5_vision.md's API-gap section at next lane touch (left for
the lane owner; not done this session).

## Probe receipt register (round-2 addition)

Every probe now names its landing path:
- Find 1: sweep/_raw/vals_home_20260929.html (1,297,267 B) +
  vals_model_v41flash.html (305,311 B) - LANDED; desk bullet appended.
- Find 2: sweep/_raw/weight_provenance_register.json - TO RUN (register built
  at probe time against the live tag list).
- Find 3: sweep/_raw/hf_rwkv7g1.json (2,508 B) - LANDED; serving-path leg
  lands at sweep/_raw/rwkv7_serving_path.txt - TO RUN.
- Find 4: sweep/_raw/nemotron35_fastino_article.md - LANDED; battery rerun
  lands at watch/inbox/ball2/abliterate_p1_runs_qwen25-3b.json - TO RUN.
- Find 5: probe cut per review; the fact banks against
  memory/runs/fleet_round/burn2b_pack.md:7299.
- Find 6: sweep/_raw/jetson_unsloth_on_jetson.html (92,055 B) - LANDED.
- Find 7: sweep/_raw/ollama_registry_v41flash.txt (404 body) +
  ollama_lib_v41flash.html (89,522 B) - LANDED; desk bullet appended.
- Find 8: sweep/_raw/hf_v4flashvision.json (5,883 B) - LANDED.

## Organ ledger (honest summary)

- SOVEREIGN MIRROR: finds 1, 2, 7, 8 (substrate ranking with today's
  falsification recorded; merged per-model weight register; cloud tier gate
  landed in the desk; MIT vision checkpoint diff target).
- GOPHER FLEET: finds 3, 4, 5, 6 (O(1)-memory janitor candidate on the
  abliterate battery instrument; single-vs-multi-turn curriculum rule with
  the same battery as its test rig; Arena rank banked as a stored input to
  the warm burn2b comparison; Jetson recipe pointer, zero-port).
- QUANTIZER: find 4's tape-selection law, confirmed new to the quantizer tree
  by the review's grep.
- CONTEXT PACK: find 1 secondary (corpus-as-context rides the cache floor,
  desk :60-61).
- PERCOLATOR: merged register candidate appended this session (find 2's
  pull-source fields + sibling row 4's license-tier fields, one register).
- WATER GRAPH: declined for all 8, as round 1. mag/water_computer.py:1-9
  defines water as the campaign hydraulics keep (tank heights, valves,
  pours); none of these finds pours water.

## Novelty recheck (round 2, with corrections)

All run this session as grep -ci over catalog/catalog.jsonl: rwkv7-g1 0,
Gerganov 0, "Agent Arena" 0, "V4-Flash-Vision" 0, "Qwen3.8-Flash-Next" 0,
"vals index" 0. Bare "rwkv": 4 rows, all incidental code (FastChat adapter,
kimodo WKV6/WKV7 kernels, one stealth intake note). Bare "nemotron": 18 rows,
exactly 1 mentioning 3.5/lightning (the astra smoke lane receipt). "v4.1
flash": 14 (11 hyphenated + 3 spaced). The review's re-bank audit stands:
nothing here is a straight re-bank; the sweep's own discipline caught Muse
Glimmer (already at
memory/runs/mickey17_v2/lanes/meta-fair-agents.json) and cross-referenced
FunctionGemma to register row 2609.25373 instead of re-banking; find 4's
curriculum rule and find 2's merged register are the two genuinely new
holdings this card adds.

## OWED (round 2, updated)

- Vals "#1 open-weight as of 09-10": unverifiable from today's bytes (the
  board moves); today's refutation of #1 and confirmation of the K3 leg are
  both dated 2026-09-29. The desk's own-bench probe at :47 stays open.
- Find 3's serving-path leg: Ollama library search for RWKV-7 text models
  not yet run; lands at sweep/_raw/rwkv7_serving_path.txt.
- Qwen3.5-4B: existence vendor-page-confirmed this session; HF model card
  still unpulled.
- Find 8's LANE5_vision.md append: left for the lane owner, not done here.
- The review's LINKS.jsonl:194 line-ref did not reproduce at this session's
  read: line 194 carries an unrelated 09-17 row; the OBLITERATUS row naming
  the P1 census / P2 port map sits at watch/inbox/LINKS.jsonl:379 (ts
  2026-09-29T09:55:00Z). The battery itself is verified at
  watch/inbox/ball2/abliterate-p1.md regardless; line refs in jsonl files
  move as rows append (the B2-216 lesson again).
- The "60-inference battery" OWED from round 1 is RESOLVED: it is the
  abliterate-p1 battery (watch/inbox/ball2/abliterate-p1.md,
  tools/abliterate_p1_probe.py, abliterate_p1_runs_banked.json), now the
  named instrument for finds 3 and 4.

## Landing (round 2)

- Register rows: 8 rows appended to
  watch/inbox/frontier_olm_20260928/register.jsonl this session (one per
  find, confidence 0.9 except 0.95 for finds 3, 4, 8 where raw bytes landed).
- Percolator: 1 merged-register candidate row appended to
  watch/inbox/frontier_olm_20260928/percolator_candidates.jsonl this session,
  referencing sibling row 4.
- Desk: 2 bullets appended to watch/inbox/DESK_DSV41FLASH_20260911.md
  tri-state this session (finds 1 and 7), both gated on probe bytes that
  landed first.
- Receipt for this card: this file, plus the raw receipts listed above.

## Citations

- Ask material: the eight confirmed finds as delivered to rounds 1 and 2.
- watch/inbox/DESK_DSV41FLASH_20260911.md:7,46-49,60-66,69 + the two 09-29
  appended bullets (Read round 1; Edit this session)
- watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-x.md:21-22,256-258
- watch/inbox/frontier_olm_20260928/register.jsonl (23 rows read; +8 appended)
- watch/inbox/frontier_olm_20260928/percolator_candidates.jsonl row 4 (read)
- watch/inbox/ball2/abliterate-p1.md:1-25 (battery, provenance table, sidecars)
- tools/abliterate_p1_probe.py (exists), watch/inbox/ball2/
  abliterate_p1_runs_banked.json (exists)
- watch/inbox/LINKS.jsonl:123,379 (grep -n abliterate, this session)
- memory/runs/fleet_round/burn2b_pack.md:7295-7304 (ItsmeAjayKV entry)
- configs/lanes.yaml:6,31-36; configs/providers.yaml:19-23
- mag/cache_identity.py:78-80; mag/water_computer.py:1-9;
  mag/frontier_scout.py:287; mag/hf_space.py:12; tools/pricing_diff.py:48;
  tools/thought_quantizer.py:1-2
- memory/rib/RIB_DRIVING_LADDER_20260928.md:7-23
- catalog/catalog.jsonl (grep counts as listed)
- sweep/_raw/: fx_BlinkDL_AI_status_2094785763129151677.json (created_at),
  hf_rwkv7g1.json, hf_v4flashvision.json, vals_home_20260929.html,
  vals_model_v41flash.html, ollama_registry_v41flash.txt,
  ollama_lib_v41flash.html, jetson_unsloth_on_jetson.html,
  nemotron35_fastino_article.md (all landed this session)
- Local Ollama: curl -s http://127.0.0.1:11434/api/tags (both sessions;
  14 tags at round-1 moment, 16 at this round's re-run)
- External: https://www.vals.ai/, https://www.vals.ai/models/
  deepseek_deepseek-v4.1-flash, https://huggingface.co/api/models/BlinkDL/
  rwkv7-g1, https://huggingface.co/api/models/deepseek-ai/
  DeepSeek-V4-Flash-Vision-Exp, https://registry.ollama.ai/v2/library/
  deepseek-v4.1-flash/manifests/latest, https://ollama.com/library/
  deepseek-v4.1-flash, https://www.jetson-ai-lab.com/tutorials/
  unsloth-on-jetson, https://x.com/i/article/2088303137182679378 via mcp
  web_reader (all this session)
