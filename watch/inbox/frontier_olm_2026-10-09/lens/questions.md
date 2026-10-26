# LENS-OF-LENSES: 8 frontier question areas

Banked: watch/inbox/frontier_olm_2026-10-09/lens/questions.md (2026-10-09)
Seat: lens-questions (dynamic workflow run, branch mag/run-beta1-factory-build-audi-20260806T231709Z)
Purpose: the question card the frontier sweep answers next. Areas are the ask-named estate research interests; each is refined by what the 5 lens summaries say the estate already holds, so the sweep reads what we do NOT hold.

## Inputs (5 lenses, banked under watch/inbox/frontier_olm_2026-10-09/lens/)

| Lens | File | What it established (all facts below are from the ask's lens summaries) |
|---|---|---|
| 1 corpus | lens/corpus.md | 1,343,390 catalog rows (all of catalog/catalog.jsonl streamed; kind census matches catalog_manifest.json:8-21); library 52,313 rows / 4.6 GB (ms-genai 12,142, ms-agents 9,429, openai-cookbook 3,120); own mine 97,867 rows (agent_platform 72,329); game-server shelf (azerothcore 10,356, vmangos 4,397, tortoise 3,767, DFHack 2,123); shadertoy21k 21,806; ZERO paths for biology, biotech, drug, web3; unreconciled drift vs CORPUS_CATALOG.md:5 flagged (canon 210 vs 209, library 52,313 vs 66,715) |
| 2 laws | lens/laws.md | 62 standing laws from instructions_frontier.jsonl (24 rows) + memory/rib/ (59 files read in full; 2 of 6 .mimosa runtime files sampled, 4 unopened = OWED); 20 open research questions the ribs imply incl flock-decode redesign, emergence A/B harness, knot-as-CRD, world-rib contract, law census, hidden bank, model-grid UNMEASURED cells, conditions-suspect re-measurement |
| 3 graph | lens/graph.md | memory/knowledge_graph.json (schema v2, ts 2026-10-06), computed via .venv/Scripts/python.exe; skills_pack.py = 287-edge precedent magnet; memlang 22, leaked_prompt_mine 21, skill_ledger 13; thinnest: 6 superseded_by edges estate-wide (correction memory unmapped), 1,066/2,938 nodes (36%) orphans, 451/1,053 modules carry no invariant, already_inside wiring only in the 9-node frontier cluster; shape = one 288-node star + 454 two-node islands; `invariant:law ` trailing-space id bug breaks exact-match joins; zero dangling endpoints so the thinness is real |
| 4 burns | lens/burns.md | memory/burns/LEDGER.jsonl 705 lines, byte-frozen since 10-07 (max ts 2026-09-28); day-8 mine (32 sweeps, 6 cards, 6 lenses) has no DIGEST/register, its fold = top owed; owed qwen2.5:7b Q4-vs-q8 A/B resolved TIE AT CEILING on 10-08; GSTD P1 fired, disk crisis purged, moonshot self-steal + probe 1 banked; anti-rebank rules minted |
| 5 doors | lens/doors.md | arXiv export API green (Atom XML, 3 of 176 entries, newest 2026-10-08; plain GET, sortBy=submittedDate); hn.algolia.com green (JSON, nbHits 2947, hits[].objectID/points/created_at); api.fxtwitter.com per-status green (jack/status/20 = 200; corroborates digest commit f676ee787's timeline 404s as timeline-shaped, not dead host); old.reddit.com top.json closed (302 login; OWED authenticated path); HN search_by_date variant unverified |

## Area 1: open-local-language-models

Q1. Which open-model releases since 2026-10-01 justify replacing the local janitor tier (gemma:2b scut, gemma4 short worker), given consent laws keep T0/T1 local-only and the model grid still has UNMEASURED cells (LENS 2)?
Q2. Does the qwen2.5:7b Q4-vs-q8 TIE AT CEILING verdict (LENS 4, resolved 2026-10-08) generalize across the UNMEASURED grid cells, or does the ceiling move with architecture (LENS 2 open question)?
Q3. Can the green arXiv door recipe (LENS 5) be wired into model-garden intake so new releases land as rows in the mine shelf (LENS 1: 97,867 mine rows, agent_platform 72,329) before they are needed?
Q4. Which corpus library shelves already document small-model serving (LENS 1: ms-genai 12,142, openai-cookbook 3,120 rows) and which model-grid cells need fresh pulls instead?

Estate map: Feeds the model garden lanes, the local Ollama janitor tier, the model-grid census rib, and the T0/T1 local-first consent boundary.

## Area 2: quantization-compression

Q1. Has any frontier quantization result since 10-01 moved small-model quality off the ceiling the qwen2.5:7b Q4-vs-q8 TIE established (LENS 4), or is Q4-at-ceiling the standing rule for janitor-class models?
Q2. Which quantization-aware training methods (QAT, LoRA-on-quantized) fill the UNMEASURED model-grid cells (LENS 2) without breaking the T0/T1 local-first law (LENS 2)?
Q3. Of the day-8 mine's 6 unbanked cards (LENS 4: ledger byte-frozen since 10-07), which carry quantization claims re-verifiable in one GET through the green arXiv door (LENS 5)?
Q4. What does the frontier say about weight-sharing and pruning for sub-8B models that the corpus library does not already hold (LENS 1 shelf census)?

Estate map: Feeds the burns LEDGER A/B queue, the UNMEASURED model-grid cells, the inference-budget terminal rule, and janitor-tier sizing.

## Area 3: agent-memory-continuity

Q1. How does frontier memory work handle correction and supersession, given the estate graph carries only 6 superseded_by edges estate-wide (LENS 3)?
Q2. Does knot-as-CRD (LENS 2 open question) survive contact with frontier CRDT and merge literature, or does the single-controller architecture law (LENS 2) make it moot?
Q3. What does the literature offer for the diagnosed L0d context-pack shedding and runaway-recall ceiling (digest commit f676ee787 named it a DIRECT HIT with a staged fix ported) beyond the fix already in tree?
Q4. Which frontier schema-evolution pattern best re-wires the 1,066 orphan nodes and 454 two-node islands (LENS 3), and is the `invariant:law ` trailing-space id bug (LENS 3) the actual join blocker to fix first?
Q5. Can the world-rib contract and law census open questions (LENS 2) be answered by a frontier memory taxonomy, or are they estate-internal by construction?

Estate map: Feeds memory/rib law files, the zknot session recap, knowledge_graph.json maintenance, the mycelium edge fabric, and warm_state boot.

## Area 4: swarm-orchestration

Q1. Does frontier multi-agent scheduling research explain the measured dispatch envelope (Task agents clean at widths 3-12, workflow children maxAttempts 0 die on first 429/1302), or is the envelope purely provider-side rolling throughput?
Q2. What retry and backoff shapes does frontier swarm infrastructure use under rate-limit storms that the fan-out width law does not yet encode?
Q3. Does the agent_platform mine shelf (LENS 1: 72,329 rows) already hold a precedent for the flock-decode redesign open question (LENS 2) before any fresh frontier pull?
Q4. What does frontier swarm work say about interagent pass-off and per-item named actors, the two dispatch shapes the workflow gate already enforces as dogfood?

Estate map: Feeds the workflow gate dogfood checks, queue lane runners, the fan-out width and max-concurrency laws, and descent-protocol dispatch shape.

## Area 5: finetuning-adaptation

Q1. What consumer-GPU LoRA and PEFT results since 10-01 would let the estate adapt its local janitors without leaving the T0/T1 local boundary (LENS 2 consent laws)?
Q2. Is adapter-tuning or full-parameter tuning the frontier default for sub-8B open models, and does the corpus library curriculum (LENS 1: 52,313 rows) already hold the primer bytes or is it inference-only?
Q3. Would adapting model weights break the skills_pack precedent magnet (LENS 3: 287 case_law edges mapped to one module), i.e. do we adapt models or keep compounding the skill ledger?
Q4. Which finetuning claims inside the day-8 mine's 32 unbanked sweeps (LENS 4) are verifiable through the green arXiv door (LENS 5) in one funded session?

Estate map: Feeds the model garden, the skills_pack case-law magnet, the skill ledger, and the local-first consent boundary.

## Area 6: kv-cache-context-engineering

Q1. What does the frontier say about prompt-prefix cache economics at the estate's fan-out shape (up to 50 workflow children at max_concurrency 10 per standing law), versus the playbook's byte-identical-ask cache rule?
Q2. Which KV-cache management results (paged attention, sliding windows, recompression) bear on the L0d context-pack shedding diagnosis and the Hermes opt-in prefetch spilling port (commit f676ee787)?
Q3. Does context compression (LLMLingua-class) clear the instruments-only and blind multi-family judging verdict laws (LENS 2), i.e. is there a benchmark reproducible byte-locally?
Q4. Does the deliberate-ask frozen-RIB + pay-the-context-tax-once doctrine have a frontier analogue that prices the one-time tax against per-ask re-packing?

Estate map: Feeds claritas prompt assembly, mag.cmd context-pack, the deliberate-ask frozen-RIB spec, the L0d context-pack shedding fix, and hermes warm boot.

## Area 7: evals-self-improvement

Q1. Do frontier eval methods (LLM-as-judge calibration, contamination audits) satisfy the blind multi-family judging and consensus-illusion verdict laws (LENS 2), or do they fail as instruments?
Q2. What experimental designs (controls, seeds, power analysis) can the emergence A/B harness open question (LENS 2) borrow so conditions-suspect re-measurement (LENS 2) stops being suspect?
Q3. Does any frontier self-improvement loop beat the estate's ratchet + citation-lint + census-patrol triad as a measured mechanism, or is the day-8 mine's unbanked fold (LENS 4: 32 sweeps, no DIGEST) proof the bank is the bottleneck, not discovery?
Q4. How would the frontier close the 451-of-1,053 modules carrying no invariant (LENS 3): generation-first or verdict-first, and which side does the percolator already take?

Estate map: Feeds percolator invariants, the drift and census patrols, the violation ratchet and citation lint, workflow-gate scenarios, and the improve/promote candidate lane.

## Area 8: inference-efficiency

Q1. What speculative decoding and continuous batching results since 10-01 shift work down the driving ladder (local janitors up, funded remote down) without violating the inference-budget terminal rule (LENS 2)?
Q2. Do frontier serving-stack benchmarks reconcile with the estate's own free-lane row counts (digest commit f80961cd9: openrouter 469 adds, groq 11, mistral 46), or does our concurrency envelope produce different economics?
Q3. Which of the day-8 mine's 32 unbanked sweeps (LENS 4) carry inference-efficiency claims that descent-protocol leg 3 (one landed deliverable per premium turn) should re-measure first at funded tier?
Q4. Is inference efficiency a zero-coverage domain in the corpus like biology and web3 (LENS 1), or does the library shelf already hold the serving-stack canon?

Estate map: Feeds memory/burns/LEDGER.jsonl, driving-ladder tier decisions, the ds_workhorse batch lane, the free-usage policy rib, and lane budget gates.

## Checks run this session

- Ran: directory listing of watch/inbox/frontier_olm_2026-10-09/lens/ (POSIX-shell `dir`; the `/b` flag failed with exit 2 but the listing printed): burns.md, corpus.md, doors.md, graph.md, laws.md - all 5 input lenses confirmed on disk.
- Ran (after write, receipt appended below): ASCII/em-dash scan of this file via .venv/Scripts/python.exe.
- Not run: no corpus re-census, no ledger re-read, no door re-probe. The 5 lens summaries arrived as the ask's input; this bank refines them into questions and does not re-verify their underlying claims. LENS 2's 4 unopened .mimosa files and LENS 5's reddit authenticated path remain OWED at their own lenses' boundary, not here.

## Post-write scan receipt

Command: .venv/Scripts/python.exe scan of this file (non-ASCII lines + chr(0x2014)/chr(0x2013) counts), 2026-10-09.
Output: file_lines 98 | nonascii_lines 0 | emdash_count 0 | endash_count 0. PASS.
