# Lens of lenses: 8 frontier question areas (frontier_olm 2026-10-08)

- Compiled 2026-10-08 by the lens-questions seat of the frontier_olm run.
- Instruments this sitting: `Read` on all five banked lens files in this directory in full:
  `corpus.md` (76 lines), `laws.md` (216), `graph.md` (36), `burns.md` (244), `doors.md` (89).
  No estate tooling was run beyond the em-dash grep recorded in the receipt below; this is a
  read-only compile, not a re-census. Every cite is path:line into a lens file read this
  sitting, or into the underlying record that lens names (secondhand where marked via).
- Method: the eight areas are the estate's standing research interests named in the ask.
  Each question is refined by what the lenses say we already hold, and the anti-rebank rules
  of `burns.md` section 5 are applied: nothing here asks to re-confirm a banked or closed
  finding; owed items are fired before new seams (`burns.md:234-235`).
- Doors state at compile: 3 of 4 frontier doors open to WebFetch today (`doors.md:9-16`);
  reddit walled-for-WebFetch with the curl+UA bypass OWED (`doors.md:56-64`); HN
  search_by_date sibling not re-verified (`doors.md:54`); fxtwitter media shape unverified
  (`doors.md:83`); arXiv works only in the minimal no-sort query shape (`doors.md:39`).

## 1. open-local-models

Holds: gemma:2b janitor / gemma4 short worker are the local fleet; the 0.5B-8B band is
UNMEASURED on public evidence and on the estate battery, meter n=0 (`burns.md:85-86`, day-7
DIGEST.md:15); harness/serving stack dominates small-model outcomes (Mingbird 0.405 to 0.886
LRAB, tool-call fidelity a serving-layer property, `burns.md:88-89`); tag-digest aliasing
proved live (qwen3 4b vs 4b-thinking byte-identical sha256, `burns.md:102-103`), P3 boot
pinning landed; per-animal gates law (`laws.md:60-63`); champion-cell contamination suspect
(`laws.md:159-161`) and fable-5.1 recipe-conditional zeros (`laws.md:162-164`) both open.

Questions:
1. Which open-weight models released since 2026-09 land in the estate's 0.5B-8B janitor and
   worker band and beat gemma:2b on the lanes' actual scut, given the band is UNMEASURED
   (day-7 DIGEST.md:15 via `burns.md:86`) and the decision meter is invalid at n=0
   (mag/verb.py:493 via `burns.md:86`)?
2. Does the day-7 confirmed harness-dominates-small-models finding (arXiv 2610.07781,
   `burns.md:88-89`) replicate on the estate's own stack: how much of gemma:2b's janitor
   pass-rate is Ollama/llama.cpp serving choice versus weights?
3. Tag-digest aliasing proved live (`burns.md:102-103`): which alias classes survive P3
   boot-time digest pinning, and which local Ollama tags still alias to byte-identical
   weights today?
4. Do the grok-4.7 champion cell re-measure (Q5, RIB_MODEL_GARDEN_ROUTING.md:115-119 via
   `laws.md:159-161`) and the fable-5.1 plan_call-recipe re-measure (Q6, `laws.md:162-164`)
   confirm their suspect cells, or do dollars re-route under the per-animal gates law?
5. With reddit JSON walled to WebFetch and the curl+UA bypass OWED (`doors.md:56-64`), does
   the hn.algolia.com-first mix (plus HN search_by_date once re-verified, `doors.md:54`)
   surface new open-model releases fast enough to keep the garden's 30-day row expiry
   (`laws.md:67-69`) fed from estate instruments only?

estate_map: Feeds the model garden routing grid (estate-instrument cells only,
RIB_MODEL_GARDEN_ROUTING.md:46-68), the local janitor fleet seats (gemma:2b and gemma4
across queue/lanes/*), and per-animal gate ribs in memory/rib/.

## 2. quantization-compression

Holds: the qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B is OWED, spec amended by port-wave P6
to four pinned choices (`burns.md:205-208`, spec watch/inbox/port_wave_20261007/
QUANT_AB_SPEC_AMEND.md); day-6 banked the per-artifact task-graded bit-ladder subject
(`burns.md:70-71`); matched-task quant deltas reportedly swing -50 to +35 at exactly the
owed pair (commit c7d364ab6 message); corpus has only 82 arXiv PDFs (`corpus.md:43`), so
paper mass must arrive through the doors; GPU-ladder price triggers unfired
(`laws.md:189-191`); ml7 quantizer bridge banked in the ML moonshot (`burns.md:136-137`).

Questions:
1. Run the amended four-pinned-choices qwen2.5:7b Q4_K_M vs q8_0 A/B end to end (spec
   watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md, un-run per `burns.md:205-208`) and
   bank which janitor and lane tasks flip verdict between quants.
2. Which of the four pinned choices are load-bearing for comparability, given matched-task
   deltas swing -50 to +35 at exactly this pair (commit c7d364ab6), and what minimal pin
   contract keeps future quant A/Bs reproducible on this box?
3. Does a per-role quant ladder (janitor scut vs short worker vs judgment-adjacent draft)
   beat one global quant choice under the estate's measured latency and cost envelope,
   extending the day-6 per-artifact bit-ladder subject (`burns.md:70-71`)?
4. Has any GPU-ladder price trigger fired on 2026-10 market data (24GB+ Blackwell under
   ~$1200 or used H100 under ~$4000, RIB_GPU_LADDER_20261001.md:14-23 via `laws.md:189-191`),
   and if so does quant-versus-card economics flip for the AMD box?
5. Which 2026-10 quantization and compression releases (via the arXiv export API minimal
   shape, `doors.md:20-39`) carry claims that contradict or sharpen the four-pinned-choices
   A/B design before it fires?

estate_map: Feeds the owed A/B queue anchored at watch/inbox/port_wave_20261007/
QUANT_AB_SPEC_AMEND.md, the model garden quant cells, and the GPU-ladder rib; results land
as register rows plus a burn receipt before any lane changes its quant.

## 3. agent-memory-continuity

Holds: the knowledge graph is a catalog, not a web: 1,687 components, 36 percent zero-degree
nodes (`graph.md:11`); knots 379/400 isolated with 162 sharing the label autonomous_janitor
(`graph.md:25`); doctrine 190/217 and steal 122/140 isolated (`graph.md:26-27`); invariants
never cross-link (`graph.md:29`); the burns LEDGER is byte-frozen since 2026-10-07 08:09:26
with max ts 2026-09-28, a standing no-writer incident two windows running
(`burns.md:31-38, 236-240`); day-6 banked write-time/use-time memory contracts
(`burns.md:71-72`); ReFold reversible sheds with a proved 4,290-char restore door
(`burns.md:118-120`); GPS-embed killed by its pre-registered falsifier (`burns.md:129-131`).

Questions:
1. What is the cheapest instrument that promotes isolated priors (379/400 knots, 190/217
   doctrine, 122/140 steal, `graph.md:25-27`) into verified edges, reusing the P1
   cite-allowlist gate's whole-repo path verification (`burns.md:115-116`) as the linker?
2. 162 of 400 knots share one label and are indistinguishable in the graph (`graph.md:25`):
   what identity key (corr_id, session id, digest) makes knot labels collision-free, and
   does the estate_query corr_id join machinery already carry it?
3. Build or retire: does the record support minting a minimal append-only LEDGER writer
   consistent with amend-never-rewrite (RIB_MD_RECORD_20260921.md:6-26 via `laws.md:33-34`)
   for the byte-frozen ledger (`burns.md:31-38`), or does the incident go to the operator as
   a retire decision with evidence either way?
4. Which estate memory writes (zknot, warm_state, world_state) violate their own read
   contracts today, and does the proved ReFold restore door (`burns.md:118-120`) serve as
   the continuity primitive under compaction, closing the day-6 write-time/use-time
   contract subject (`burns.md:71-72`)?
5. GPS-embed died on its falsifier (string keys 100.0 percent vs embedding-kNN 99.05,
   McNemar p=0.5, 60x over latency budget, `burns.md:129-131`): name one agent-memory
   retrieval job on this estate where embeddings beat keyed lookup, or retire the class.

estate_map: Feeds memory/knowledge_graph.json weaving, the burns-ledger writer incident
(memory/burns/LEDGER.jsonl), the ReFold reversible sheds, and the write-time contracts of
warm_state, zknot and world_state.

## 4. swarm-orchestration

Holds: fan-out width law and max-concurrency standing law fix the dispatch shapes on this
account (AGENTS.md; measured envelope 5 gated workflows x 10); consensus illusion measured
(0/3 wrong-at-high-strength, `laws.md:81-84`); ArcticSwarm premature consensus 82.6 vs
40-run majority 63.5 and probe monitors 97-99 percent recall vs judge 9, kappa 0.15
(`burns.md:95-96`, day-7 DIGEST.md:19); flock decode redesign owed (`laws.md:176-178`);
pheromone bus plus Merkle cure shipped with ONE unconfirmed p1a L0d (`burns.md:145-147`);
blind-sweep placement law at WARN in the gate (`burns.md:120-121`); the day-6 11.7M-request
dispatch-shape counter-evidence is gated on a width A/B never run (`burns.md:72-74`).

Questions:
1. Run the width A/B the day-6 dispatch-shape counter-evidence is gated on
   (frontier_olm_2026-10-06/DIGEST.md:17,:43 via `burns.md:72-74`) at the two proven shapes
   (workflow max_concurrency 3 vs Task agents 10-12), then amend or retire that row.
2. What flock decode maps consensus onto the actual task output space (Q10,
   `laws.md:176-178`) so consensus strength stops being an anti-signal (0/3
   wrong-at-high-strength, `laws.md:81-84`), and can it be dogfooded on the next sweep's own
   review pass given ArcticSwarm's 82.6 vs 63.5 counter-evidence (`burns.md:95-96`)?
3. Can probe-first verification (97-99 percent recall vs judge 9, kappa 0.15,
   `burns.md:95-96`) replace the paid judge as first pass on register rows, keeping judge2
   re-judge (second family, Q7, `laws.md:165-169`) only for probe-flagged disagreements?
4. Confirm or kill the pheromone bus's ONE unconfirmed p1a L0d at the next natural swarm
   run (`burns.md:145-147`), and record whether MAG_POSITION_BOUND_LEAVES flipped the
   [a,b,c] vs [a,b,c,c] falsifier on-box.
5. Does enforcing the G2 blind-sweep placement law (currently WARN, `burns.md:120-121`)
   measurably improve sweep outcome quality, or only add gate latency, measured across two
   runs of the same scenario cards?

estate_map: Feeds the fan-out width law and the max-concurrency standing law (dispatch
shapes on this account), tools/pheromone.py and the flock instruments, and the workflow_gate
scenario cards at configs/workflow_gate_scenarios.

## 5. finetuning-adaptation

Holds: reasoning-marker penalization is doubly specified (the estate's own held thread bytes
carry the RL mechanism the HF card omits, commit c7d364ab6) and P6 shipped a marker-penalty
logit_bias profile OFF by default (`burns.md:120-121`); the serving-layer finding
(`burns.md:88-89`) implies adaptation may be dominated by harness work for the 0.5-8B band;
ReFold's sha-addressed reversible shed pattern is proved for context folds
(`burns.md:118-120`); corpus/library holds 52,313 curriculum rows (`corpus.md:35`);
EmbeddingGemma 2 banked under models/ (`burns.md:132`); five-gate hardware adoption law
(`laws.md:98-99`).

Questions:
1. Does toggling the P6 marker-penalty logit_bias profile (OFF by default, `burns.md:120-121`)
   measurably change gemma:2b janitor accuracy, and is a sampler-level profile the right
   adapter substitute where a local finetune is out of reach?
2. Is any LoRA or PEFT pass on the janitor fleet ever justified under the five-gate hardware
   law (RIB_GPU_LADDER_20261001.md:10-23 via `laws.md:98-99`), given the confirmed finding
   that serving-layer choices dominate small-model outcomes (`burns.md:88-89`)?
3. Does ReFold's reversible sha-addressed shed pattern (`burns.md:118-120`) transfer from
   context folds to adapter and checkpoint deltas (per-seat LoRA or sampler deltas stored as
   restorable sheds), and what breaks the restore door there?
4. Catalog which adaptation techniques (LoRA, PEFT, distillation, prompt-tuning) appear in
   the 52,313 taught curriculum rows (`corpus.md:35`) but have zero estate instruments, as
   the eliminate-before-frontier map any future adaptation ask must carry (`laws.md:88-91`).
5. With GPS-embed dead (`burns.md:129-131`) and EmbeddingGemma 2 banked under models/
   (`burns.md:132`): what non-router use justifies keeping an embedding model resident on
   the box, against the RAM-cache residency law (RIB_RAM_CACHE_STALE_SNAPSHOT_20260825.md
   :8-41 via `laws.md:103-105`)?

estate_map: Feeds sampler profile defaults (the marker-penalty logit_bias profile, OFF by
default), ReFold shed storage patterns, and the eliminate-before-frontier prior-art map for
any future adaptation ask.

## 6. kv-cache-context-engineering

Holds: deliberate-ask law freezes a cache-shared prefix (raw_count 27,
instructions_frontier.jsonl:22 via `laws.md:75-77`); xAI full-history cache grammar
(edit/remove/reorder breaks prefix, reasoning_content omission the top miss cause, commit
c7d364ab6); the P3 thinking-default reader landed (`burns.md:117`); omission-is-measured-ON
law (`laws.md:28-30`); the day-7 OpenAI caching-doc claim was CONTRADICTED by the fetched
page and stayed unbanked (`burns.md:105-108`); BreadthKV and BARQ steals from day-6
(`burns.md:73-74`) and the lmcache-src mirror at 2,331 rows (`corpus.md:38`);
context_compression.py is the graph's top family target at degree 7 (`graph.md:22`) yet
invariants never cross-link (`graph.md:29`); b11465-b11475 runtime deltas proved
Metal-specific (`burns.md:93-94`).

Questions:
1. Which estate ask paths (warm_state, briefs, world_state injections) mutate the frozen
   cache-shared prefix between asks today, and what does a prefix-stable boot block save in
   measured tokens under the deliberate-ask law (`laws.md:75-77`) plus the xAI prefix-break
   grammar?
2. Do the P3 thinking-default reader (`burns.md:117`) and the omission-is-measured-ON law
   (`laws.md:28-30`) close the reasoning_content-omission miss mode for DeepSeek, or does
   one of the six unwired carriers still drop reasoning on replay (Q4, `laws.md:154-158`)?
3. Re-derive per-family cache grammars (xAI, DeepSeek, Nous primes, Anthropic unfunded) from
   primary vendor pages, superseding the day-7 OpenAI caching-doc claim the fetched page
   contradicted (`burns.md:105-108`), and bank the rows in the garden.
4. Do any of BreadthKV, BARQ (`burns.md:73-74`) or the lmcache-src mirror (`corpus.md:38`)
   run on llama.cpp/Ollama on Windows/Vulkan, given b11465-b11475 deltas proved Metal-only
   (`burns.md:93-94`), or is KV offload here a non-steal on this box?
5. Write the falsifiable invariant set for context_compression.py, honoring the RAM-cache
   mtime-fingerprint law (`laws.md:103-105`), before any new compaction carrier lands: what
   would a red test even look like, given its invariants never cross-link today
   (`graph.md:29`)?

estate_map: Feeds deliberate-ask frozen-prefix carriers, the P3 thinking-default reader,
context_compression.py invariants in memory/percolator/invariants.json, and per-family cache
grammar rows in the model garden.

## 7. evals-and-self-improvement

Holds: the decision-rung bar (>=0.880 on n>=40 vs beat-embeddings) is cleared by nothing
read; semantic-entropy tops at 0.871 AUROC and nimble 86.9 straddles the gate
(`burns.md:90-92`); the meter is invalid at n=0 (`burns.md:86`); the hidden ask-bank is thin
at 20 asks (Q8, `laws.md:170-172`); ember-1 is the sole judge family and the judge2 re-judge
of the ~300-ask duel ledger is proposed not run (Q7, `laws.md:165-169`); the whole-corpus
law census is proposed not run (Q9, `laws.md:173-175`); duty_fuzz contamination tripwire
landed with the first pair gemma:2b 0.9167/0.8333 (`burns.md:116-117`); judge-agreement-is-
the-wrong-target banked three independent ways (`burns.md:104`); recurring uncured gate
tics: colon reveal 25/28 (`burns.md:127-128`) and lyrics-verbatim repeat offense
(`burns.md:139-140`).

Questions:
1. Manufacture the n>=40 fleet-labeled rows (day-7 probe queue, DIGEST.md:97-108 via
   `burns.md:209-211`) so the decision meter ever reads valid, then re-run the decision-rung
   bar: does anything clear 0.880 on the estate battery, or does semantic-entropy's 0.871
   AUROC stand as the measured ceiling (`burns.md:90-92`)?
2. Grow the hidden ask-bank from 20 to 100+ contamination-safe asks (Q8, `laws.md:170-172`)
   using duty_fuzz twin-minting as the dedup gate (delta >= 0.15 lands risk rows,
   `burns.md:116-117`), and measure whether the ask generator itself mints phrasing twins.
3. Run the judge2 re-judge of the ~300-ask historical duel ledger with a second family (Q7,
   `laws.md:165-169`) and count how many dollar-routing verdicts flip; a nontrivial flip
   rate makes the ember-1-only judge a standing incident.
4. Run the whole-corpus law census (~2000 asks, est $2-8, Q9, `laws.md:173-175`): does it
   surface law-collision rows (same law filed twice) at a rate that makes it a recurring
   percolator input rather than a one-off, and does it catch the graph's duplicate-label
   disease (`graph.md:25`)?
5. Which gate findings recurred 3+ times without a cure (colon reveal 25/28,
   `burns.md:127-128`; lyrics-verbatim repeat offense, `burns.md:139-140`), and which
   belong promoted from WARN patrol to percolator invariants under fix-the-cause law
   (`laws.md:100-102`)?

estate_map: Feeds the mag/verb.py decision meter, the hidden ask-bank, the judge2 duel
ledger, the duty_fuzz contamination tripwire, percolator invariants, and the pre-push gates
(violation ratchet, citation lint, census patrol).

## 8. inference-efficiency

Holds: DeepSeek off-peak proven and the Lightning lane dead with Chutes/SiliconFlow/Scaleway
(ledger lines 681, 692, 701 via `burns.md:46-49`); every pre-2026-10-04 DeepSeek per-pass
economics row rode thinking-ON by omission and is conditions-suspect (Q3,
`laws.md:149-153`); the inference-budget guard is wired in two carriers, six fire surfaces
still hand-roll params (Q4, `laws.md:154-158`); EMPTY_REASONING terminal law
(`laws.md:64-66`); mesh matched or beat premium on 14/17 evidence-readable asks at 2-4
percent of dollars, 0/5 on runtime-simulation (`laws.md:41-45`); the Hermes 402 wall was hit
2026-10-07 (`burns.md:181`) while the SPEND amendment orders budget spent
(`laws.md:49-51`); the Featherless full-dump left 28.6k unserved rows (`burns.md:214-215`).

Questions:
1. Re-measure the conditions-suspect DeepSeek economics rows (the $0.0024 triangulations,
   $0.005 assembly, $0.00077/ask, Q3, `laws.md:149-153`) with thinking explicitly OFF vs ON
   in the d4 three-arm shape (`laws.md:28-30`), and append superseding rows per
   amend-never-rewrite.
2. Wire the inference-budget guard into the six hand-rolling fire surfaces (stealth_driver,
   duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire, Q4, `laws.md:154-158`) or
   record per-carrier exemption, and name today's highest token-bleed surface with a
   measured number.
3. Post-402-wall (2026-10-07, `burns.md:181`), what is the funded tier's actual
   cost-per-blind-point this week under the SPEND amendment (`laws.md:49-51`), and does the
   routing-class table (14/17 at 2-4 percent of dollars, `laws.md:41-45`) still hold?
4. Does the Featherless paged re-pull close the 28.6k unserved-row roster gap
   (`burns.md:214-215`), and does the fuller roster change the cool-pool SENSING
   composition now that the Lightning lane and its substitutes are dead (`burns.md:46-49`)?
5. Measure EMPTY_REASONING's 2026-10 incidence across funded and free lanes
   (`laws.md:64-66`): does the drip-not-burst free-lane finding (`laws.md:52-54`) transfer
   to paid-lane burst handling, and which lane is bleeding retrial tokens on refired
   params today?

estate_map: Feeds the inference-budget guard and its six unwired carriers, the routing-class
table, the free-lane queue drain path, and the burn ledgers (memory/runs/hermes_burn/
usage.jsonl).

## Machine-readable echo

```json
[
  {"area": "open-local-models", "questions": ["Which open-weight models released since 2026-09 land in the estate's 0.5B-8B janitor and worker band and beat gemma:2b on the lanes' actual scut, given the band is UNMEASURED (day-7 DIGEST.md:15 via lens/burns.md:86) and the decision meter is invalid at n=0 (mag/verb.py:493 via lens/burns.md:86)?", "Does the day-7 confirmed harness-dominates-small-models finding (arXiv 2610.07781, lens/burns.md:88-89) replicate on the estate's own stack: how much of gemma:2b's janitor pass-rate is Ollama/llama.cpp serving choice versus weights?", "Tag-digest aliasing proved live (lens/burns.md:102-103): which alias classes survive P3 boot-time digest pinning, and which local Ollama tags still alias to byte-identical weights today?", "Do the grok-4.7 champion cell re-measure (Q5, lens/laws.md:159-161) and the fable-5.1 plan_call-recipe re-measure (Q6, lens/laws.md:162-164) confirm their suspect cells, or do dollars re-route under the per-animal gates law?", "With reddit JSON walled to WebFetch and the curl+UA bypass OWED (lens/doors.md:56-64), does the hn.algolia.com-first mix (plus HN search_by_date once re-verified, lens/doors.md:54) surface new open-model releases fast enough to keep the garden's 30-day row expiry (lens/laws.md:67-69) fed from estate instruments only?"], "estate_map": "Feeds the model garden routing grid (estate-instrument cells only, RIB_MODEL_GARDEN_ROUTING.md:46-68), the local janitor fleet seats (gemma:2b and gemma4 across queue/lanes/*), and per-animal gate ribs in memory/rib/."},
  {"area": "quantization-compression", "questions": ["Run the amended four-pinned-choices qwen2.5:7b Q4_K_M vs q8_0 A/B end to end (spec watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md, un-run per lens/burns.md:205-208) and bank which janitor and lane tasks flip verdict between quants.", "Which of the four pinned choices are load-bearing for comparability, given matched-task deltas swing -50 to +35 at exactly this pair (commit c7d364ab6), and what minimal pin contract keeps future quant A/Bs reproducible on this box?", "Does a per-role quant ladder (janitor scut vs short worker vs judgment-adjacent draft) beat one global quant choice under the estate's measured latency and cost envelope, extending the day-6 per-artifact bit-ladder subject (lens/burns.md:70-71)?", "Has any GPU-ladder price trigger fired on 2026-10 market data (24GB+ Blackwell under ~$1200 or used H100 under ~$4000, lens/laws.md:189-191), and if so does quant-versus-card economics flip for the AMD box?", "Which 2026-10 quantization and compression releases (via the arXiv export API minimal shape, lens/doors.md:20-39) carry claims that contradict or sharpen the four-pinned-choices A/B design before it fires?"], "estate_map": "Feeds the owed A/B queue anchored at watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md, the model garden quant cells, and the GPU-ladder rib; results land as register rows plus a burn receipt before any lane changes its quant."},
  {"area": "agent-memory-continuity", "questions": ["What is the cheapest instrument that promotes isolated priors (379/400 knots, 190/217 doctrine, 122/140 steal, lens/graph.md:25-27) into verified edges, reusing the P1 cite-allowlist gate's whole-repo path verification (lens/burns.md:115-116) as the linker?", "162 of 400 knots share one label and are indistinguishable in the graph (lens/graph.md:25): what identity key (corr_id, session id, digest) makes knot labels collision-free, and does the estate_query corr_id join machinery already carry it?", "Build or retire: does the record support minting a minimal append-only LEDGER writer consistent with amend-never-rewrite (RIB_MD_RECORD_20260921.md:6-26 via lens/laws.md:33-34) for the byte-frozen ledger (lens/burns.md:31-38), or does the incident go to the operator as a retire decision with evidence either way?", "Which estate memory writes (zknot, warm_state, world_state) violate their own read contracts today, and does the proved ReFold restore door (lens/burns.md:118-120) serve as the continuity primitive under compaction, closing the day-6 write-time/use-time contract subject (lens/burns.md:71-72)?", "GPS-embed died on its falsifier (string keys 100.0 percent vs embedding-kNN 99.05, McNemar p=0.5, 60x over latency budget, lens/burns.md:129-131): name one agent-memory retrieval job on this estate where embeddings beat keyed lookup, or retire the class."], "estate_map": "Feeds memory/knowledge_graph.json weaving, the burns-ledger writer incident (memory/burns/LEDGER.jsonl), the ReFold reversible sheds, and the write-time contracts of warm_state, zknot and world_state."},
  {"area": "swarm-orchestration", "questions": ["Run the width A/B the day-6 dispatch-shape counter-evidence is gated on (frontier_olm_2026-10-06/DIGEST.md:17,:43 via lens/burns.md:72-74) at the two proven shapes (workflow max_concurrency 3 vs Task agents 10-12), then amend or retire that row.", "What flock decode maps consensus onto the actual task output space (Q10, lens/laws.md:176-178) so consensus strength stops being an anti-signal (0/3 wrong-at-high-strength, lens/laws.md:81-84), and can it be dogfooded on the next sweep's own review pass given ArcticSwarm's 82.6 vs 63.5 counter-evidence (lens/burns.md:95-96)?", "Can probe-first verification (97-99 percent recall vs judge 9, kappa 0.15, lens/burns.md:95-96) replace the paid judge as first pass on register rows, keeping judge2 re-judge (second family, Q7, lens/laws.md:165-169) only for probe-flagged disagreements?", "Confirm or kill the pheromone bus's ONE unconfirmed p1a L0d at the next natural swarm run (lens/burns.md:145-147), and record whether MAG_POSITION_BOUND_LEAVES flipped the [a,b,c] vs [a,b,c,c] falsifier on-box.", "Does enforcing the G2 blind-sweep placement law (currently WARN, lens/burns.md:120-121) measurably improve sweep outcome quality, or only add gate latency, measured across two runs of the same scenario cards?"], "estate_map": "Feeds the fan-out width law and the max-concurrency standing law (dispatch shapes on this account), tools/pheromone.py and the flock instruments, and the workflow_gate scenario cards at configs/workflow_gate_scenarios."},
  {"area": "finetuning-adaptation", "questions": ["Does toggling the P6 marker-penalty logit_bias profile (OFF by default, lens/burns.md:120-121) measurably change gemma:2b janitor accuracy, and is a sampler-level profile the right adapter substitute where a local finetune is out of reach?", "Is any LoRA or PEFT pass on the janitor fleet ever justified under the five-gate hardware law (RIB_GPU_LADDER_20261001.md:10-23 via lens/laws.md:98-99), given the confirmed finding that serving-layer choices dominate small-model outcomes (lens/burns.md:88-89)?", "Does ReFold's reversible sha-addressed shed pattern (lens/burns.md:118-120) transfer from context folds to adapter and checkpoint deltas (per-seat LoRA or sampler deltas stored as restorable sheds), and what breaks the restore door there?", "Catalog which adaptation techniques (LoRA, PEFT, distillation, prompt-tuning) appear in the 52,313 taught curriculum rows (lens/corpus.md:35) but have zero estate instruments, as the eliminate-before-frontier map any future adaptation ask must carry (lens/laws.md:88-91).", "With GPS-embed dead (lens/burns.md:129-131) and EmbeddingGemma 2 banked under models/ (lens/burns.md:132): what non-router use justifies keeping an embedding model resident on the box, against the RAM-cache residency law (RIB_RAM_CACHE_STALE_SNAPSHOT_20260825.md:8-41 via lens/laws.md:103-105)?"], "estate_map": "Feeds sampler profile defaults (the marker-penalty logit_bias profile, OFF by default), ReFold shed storage patterns, and the eliminate-before-frontier prior-art map for any future adaptation ask."},
  {"area": "kv-cache-context-engineering", "questions": ["Which estate ask paths (warm_state, briefs, world_state injections) mutate the frozen cache-shared prefix between asks today, and what does a prefix-stable boot block save in measured tokens under the deliberate-ask law (lens/laws.md:75-77) plus the xAI prefix-break grammar?", "Do the P3 thinking-default reader (lens/burns.md:117) and the omission-is-measured-ON law (lens/laws.md:28-30) close the reasoning_content-omission miss mode for DeepSeek, or does one of the six unwired carriers still drop reasoning on replay (Q4, lens/laws.md:154-158)?", "Re-derive per-family cache grammars (xAI, DeepSeek, Nous primes, Anthropic unfunded) from primary vendor pages, superseding the day-7 OpenAI caching-doc claim the fetched page contradicted (lens/burns.md:105-108), and bank the rows in the garden.", "Do any of BreadthKV, BARQ (lens/burns.md:73-74) or the lmcache-src mirror (lens/corpus.md:38) run on llama.cpp/Ollama on Windows/Vulkan, given b11465-b11475 deltas proved Metal-only (lens/burns.md:93-94), or is KV offload here a non-steal on this box?", "Write the falsifiable invariant set for context_compression.py, honoring the RAM-cache mtime-fingerprint law (lens/laws.md:103-105), before any new compaction carrier lands: what would a red test even look like, given its invariants never cross-link today (lens/graph.md:29)?"], "estate_map": "Feeds deliberate-ask frozen-prefix carriers, the P3 thinking-default reader, context_compression.py invariants in memory/percolator/invariants.json, and per-family cache grammar rows in the model garden."},
  {"area": "evals-and-self-improvement", "questions": ["Manufacture the n>=40 fleet-labeled rows (day-7 probe queue, DIGEST.md:97-108 via lens/burns.md:209-211) so the decision meter ever reads valid, then re-run the decision-rung bar: does anything clear 0.880 on the estate battery, or does semantic-entropy's 0.871 AUROC stand as the measured ceiling (lens/burns.md:90-92)?", "Grow the hidden ask-bank from 20 to 100+ contamination-safe asks (Q8, lens/laws.md:170-172) using duty_fuzz twin-minting as the dedup gate (delta >= 0.15 lands risk rows, lens/burns.md:116-117), and measure whether the ask generator itself mints phrasing twins.", "Run the judge2 re-judge of the ~300-ask historical duel ledger with a second family (Q7, lens/laws.md:165-169) and count how many dollar-routing verdicts flip; a nontrivial flip rate makes the ember-1-only judge a standing incident.", "Run the whole-corpus law census (~2000 asks, est $2-8, Q9, lens/laws.md:173-175): does it surface law-collision rows (same law filed twice) at a rate that makes it a recurring percolator input rather than a one-off, and does it catch the graph's duplicate-label disease (lens/graph.md:25)?", "Which gate findings recurred 3+ times without a cure (colon reveal 25/28, lens/burns.md:127-128; lyrics-verbatim repeat offense, lens/burns.md:139-140), and which belong promoted from WARN patrol to percolator invariants under fix-the-cause law (lens/laws.md:100-102)?"], "estate_map": "Feeds the mag/verb.py decision meter, the hidden ask-bank, the judge2 duel ledger, the duty_fuzz contamination tripwire, percolator invariants, and the pre-push gates (violation ratchet, citation lint, census patrol)."},
  {"area": "inference-efficiency", "questions": ["Re-measure the conditions-suspect DeepSeek economics rows (the $0.0024 triangulations, $0.005 assembly, $0.00077/ask, Q3, lens/laws.md:149-153) with thinking explicitly OFF vs ON in the d4 three-arm shape (lens/laws.md:28-30), and append superseding rows per amend-never-rewrite.", "Wire the inference-budget guard into the six hand-rolling fire surfaces (stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire, Q4, lens/laws.md:154-158) or record per-carrier exemption, and name today's highest token-bleed surface with a measured number.", "Post-402-wall (2026-10-07, lens/burns.md:181), what is the funded tier's actual cost-per-blind-point this week under the SPEND amendment (lens/laws.md:49-51), and does the routing-class table (14/17 at 2-4 percent of dollars, lens/laws.md:41-45) still hold?", "Does the Featherless paged re-pull close the 28.6k unserved-row roster gap (lens/burns.md:214-215), and does the fuller roster change the cool-pool SENSING composition now that the Lightning lane and its substitutes are dead (lens/burns.md:46-49)?", "Measure EMPTY_REASONING's 2026-10 incidence across funded and free lanes (lens/laws.md:64-66): does the drip-not-burst free-lane finding (lens/laws.md:52-54) transfer to paid-lane burst handling, and which lane is bleeding retrial tokens on refired params today?"], "estate_map": "Feeds the inference-budget guard and its six unwired carriers, the routing-class table, the free-lane queue drain path, and the burn ledgers (memory/runs/hermes_burn/usage.jsonl)."}
]
```

## RECEIPT

- Read this sitting: the five lens files named in the header, in full, via the Read tool.
  No lens content was re-derived from primary records this sitting; underlying paths cited
  in questions are pointers the sweep must verify before acting, exactly as the lens files
  carry them.
- Not run this sitting: any pytest, any census, any door re-probe, any ledger read beyond
  the lens files. This file folds; it does not confirm.
- Em-dash law: verified by grep after writing (see submitted receipt in the run result).
