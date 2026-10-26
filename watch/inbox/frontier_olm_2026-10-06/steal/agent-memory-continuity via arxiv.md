# STEAL: agent-memory-continuity via arxiv (2 confirmed finds) - 2026-10-06 - REV 1 (round 1 draft)

Area: agent-memory-continuity via arxiv
Banked by: steal-agent-memory-continuity via arxiv (Mag Resource Harness steal gopher, dynamic workflow run)
Finds handed by the driver ask (both confidence 0.95, both marked source-fetched 2026-10-06 by the sweeper):
1. "When Evidence Changes: Evaluating Memory Repair and Re-reading in Language-Model Agents", https://arxiv.org/abs/2610.03902 (2026-10-02)
2. "Memory Consolidation Flattens the Temporal Shape of User Facts", https://arxiv.org/abs/2609.36457 (2026-09-29)
Source sitting: watch/inbox/frontier_olm_2026-10-06/sweep/agent-memory-continuity-arxiv.md (items 1-2 of its bank of 8; full texts were read there; my independent fetches were abs-level only, stated below).

## Verification run THIS sitting (not inherited)

- Overlap re-checks, exact commands from repo root, each returning zero hits (rg exit 1, no output):
  - `rg -i -c "When Evidence Changes" catalog/catalog.jsonl memory` -> no hits
  - `rg -i -c "Memory Consolidation Flattens" catalog/catalog.jsonl memory` -> no hits
  - `rg -i -c "aspectual flattening" catalog/catalog.jsonl memory` -> no hits
  Matches the sweep card's own overlap block (watch/inbox/frontier_olm_2026-10-06/sweep/agent-memory-continuity-arxiv.md:39). Genuinely new to the corpus.
- Independent abs fetches (WebFetch, arxiv.org/abs, 2026-10-06):
  - 2610.03902: title and date confirmed (submitted 2 Oct 2026, matching the ask's 2026-10-02). Verbatim from the abstract: "local repair uses 5-10x fewer revision tokens than rebuilding"; "every memory pipeline costs at least twice full re-reading in held-out conditions". The abstract does NOT carry the adoption counts (8-9/13 vs 13/13) or the new-value-in-prompt miss finding; those ride the sweeper's full-text read (sweep card :55 and :63) and are credited, not independently verified by me.
  - 2609.36457: title and date confirmed (submitted 29 Sep 2026, matching the ask's 2026-09-29). Verbatim from the abstract: "We call this aspectual flattening and measure it with LAPSE, a benchmark of matched user statements that differ only in temporal form."; "Three writer models flattened the progressive statement but kept its simple-present match in 244 of 381 pairs, never the reverse."; "The asymmetry holds in all 11 model configurations tested and in the installed pipelines mem0, Graphiti, and Letta."; "changing only the stored verb shifted all three readers' estimates that a fact still holds."

## Estate byte-truth (every line read or run THIS sitting)

- The quantizer compile is a full rebuild with one input: memory/corpus/quantized_thought/compile_report.json:2 (compiled 2026-10-06T18:26:38Z), :4-14 (stats: in 648, kept 625, dedupes 13, rib_amendments_in 5, rib_amendments_kept 5, packs frontier 24 / flash 12 / local 589), :30 ("input": "memory/percolator/invariants.json"). The report header reads "v": "0.4" at :3; the tool docstring documents laws through v0.6 (tools/thought_quantizer.py:37-44 MIN_KEPT_LAWS: an empty compile must never serve as law, because "seats booted zero laws with a green freshness stamp"; :46-51 v0.6: rib amendment rows ride beside the percolator feed at weight 1.0); rows in instructions_flash.jsonl carry "status": "compiled-v0.4". Both bytes reported, not adjudicated.
- The consumer gate is presence + age only: mag/context_pack.py:436 (_quantized_laws), :415 and :472 (serve/refuse on age_d > PACK_STALE_DAYS), :14 (the ONE decay bar import), :1048 (the pack composes quantized_laws). Nothing on this path scores whether a consuming seat's output ADOPTED the served row; the compile stamps rows, it never re-asks them.
- Amendment provenance exists per row already: memory/corpus/quantized_thought/instructions_flash.jsonl:1-5 are the five vault-amendment rows (rib0..rib4), each carrying "sources" back to the exact amendment block (e.g. :3 sources rib2:RIB_INFERENCE_BUDGET_20261001#1), and each narrating its own supersession (row 3: the ds_workhorse thinking-key erratum, omission measured as a MEASURED ON state, explicit thinking:{type:disabled} mandatory).
- The estate's own memory writers already reshape what they store (my byte evidence; truncation-shaped, not aspect-shaped):
  - zknot cards store deduped 150-char first lines only: tools/zknot.py:107-112 (first_line width cap), :196-197 (cards carry first lines, latest 30); full prompt text stays in the external DB (tools/zknot.py:65). The card schema (tools/zknot.py:198-221) has no original-wording or temporal-form field.
  - Percolator invariant rows carry text/count/first_seen/domain/last_seen/decay_as_of/cycle_hits/depends_on and nothing else (memory/percolator/invariants.json:3-13); several text fields are mid-sentence truncations (:4 ends "shape" mid-clause, :34 cuts inside a parameter token, :52 cuts at "behind th"). No temporal-form field; observation time exists (first_seen/last_seen) but is storage bookkeeping, not per-claim capture.
  - The quantizer's flash tier truncates its own frontier tier: instructions_flash.jsonl:2 flash ends "this bloc" mid-word, :3 ends "tools/ds_work", :4 ends "ZERO" mid-sentence.
- R5's own target 1 names the adjacent leg: state/NIGHT_LOOP_20261005.md:262 reads "not compile coverage, is the falsifier for \"propagated\")" - boot-time seat inhalation is the named falsifier; nothing yet tests the use-stage leg downstream of inhalation.
- The freshness-theater disease is the estate's own coinage, at the source: git log -n 1 becb53618 carries "FRESHNESS THEATER KILLED AT THE SOURCE ... the fresh-stamped pack was lawless one layer down" (verified this sitting).

## The steal (mechanism, not a link dump)

Agent-memory continuity, on this pair of papers, is two contracts the estate currently fakes with stamps:

- A. ADOPTION-AT-USE GATE + AMENDMENT-SCOPED PATCHING (2610.03902). The paper separates two costs the estate conflates into one full recompile. Propagation: local repair of short records costs 5-10x fewer revision tokens than rebuilding, and every memory pipeline still costs at least twice full re-reading in held-out conditions (both quoted from the abstract this sitting) - so for short records the pack layer never wins on cost and must win on adoption or not at all. Adoption: memory pipelines committed the superseded value even when the NEW value sat in the prompt (8-9 of 13 adopted vs 13/13 for bare re-reading; every miss was use-stage; credited from the sweep's full-text read, sweep card :63). Estate port, two moves on the quantizer + context pack organs: (1) DELTA MANIFEST - the v0.6 feed already knows exactly which rows an amendment touches (compile_report rib_amendments_in 5; per-row "sources" field), so the compile emits changed row ids beside the packs and consumers re-read only changed rows instead of re-inhaling 625; (2) USE-STAGE RECEIPT - after a seat consumes a pack containing a row whose upstream amended since that seat's last boot, fire one gated question per changed row at the free local janitor and score whether the answer carries the superseded value; the receipt rides the existing pack surface (mag/context_pack.py:1048). This is the downstream complement of R5 target 1's boot-inhalation leg (state/NIGHT_LOOP_20261005.md:262): inhalation proves the pack entered; adoption proves it stuck. Pricing corollary the paper supplies (sweep :55): for law questions, re-read the rib bytes - the flash tier's mid-word truncation habit (instructions_flash.jsonl:2-4) is exactly a summary layer losing the amendment's operative tail.
- B. TEMPORAL FORM IS DATA, NOT FLAVOR (2609.36457). Writers flatten progressive to simple present in 244 of 381 matched pairs, never the reverse, across 11 configurations and inside mem0/Graphiti/Letta; changing only the stored verb shifts readers' still-holds estimates (all four quoted from the abstract this sitting). The estate's three memory writers already reshape what they store (byte-truth above: 150-char first lines in zknot, mid-sentence percolator text, flash truncating frontier). Port moves: (1) three stored fields on the invariant row and the zknot card header - original_wording (full capture; the width caps become display caps, not storage caps), temporal_form (deterministic aspect tag at capture, no LLM), observed_at (promote first_seen/last_seen to per-claim capture time, distinct from storage time); (2) LAPSE-mini - matched progressive/simple pairs drawn from the estate's own operator corpus, run through the flash/local tier writers, count flips; prediction from the paper: flips toward simple-present with zero reversals, the mem0 shape (49/128 inside mem0, sweep :53).

## Per-find organ map

| # | Find | Organ | Concrete port move |
|---|---|---|---|
| 1 | 2610.03902 adoption + repair pricing | quantizer (tools/thought_quantizer.py:46-51 feed; compile_report.json:4-14) + context pack (mag/context_pack.py:436, :415/:472, :1048) | delta manifest of changed row ids per compile; use-stage adoption receipt (one gated question per amended row, free local lane) extending the age-only gate |
| 2 | 2609.36457 LAPSE | percolator (memory/percolator/invariants.json:3-13) + zknot capture (tools/zknot.py:107-112, :196-221) + quantizer tiers (instructions_flash.jsonl:2-4) | original_wording + temporal_form + observed_at as stored fields; LAPSE-mini over the estate's own matched pairs scored against the writers |

## Falsifiable probe (cheap, this week; named NOT run)

P1 evidence-replacement replay on the flash pack, gemma:2b free local lane, zero paid dispatch, one evening:

- Arms: for each of the 5 vault-amendment rows (instructions_flash.jsonl:1-5), arm A asks one gated question with the fresh row in context (row 3's gate: "may ds_workhorse omit the thinking key?"); arm B asks the same question with the fresh row present PLUS the superseded pre-amendment phrasing in context (the erratum's earlier belief, which rows 2-3 themselves narrate), mirroring the paper's condition where the new value is already in the prompt and the memory layer still answers old.
- Prediction (paper shape): arm B commits the superseded value in a nonzero fraction of asks while a bare rib-bytes re-read control is clean; the paper's memory pipelines missed 4-5 of 13 exactly this way.
- Falsifier: zero stale commitments across the whole batch (the pack consumer already equals the re-reading control) kills find 1's use-stage port on this organ and downgrades it to a propagation-only instrument.
- Companion (find 2): LAPSE-mini over the estate's own matched pairs once a pairing instrument exists - blocked today on the OWED row below.

## Overlap credits (so nothing is double-banked or re-derived)

- Freshness theater is the estate's OWN named disease (git becb53618, verified above; tools/thought_quantizer.py:37-44 v0.5). Find 1 is its controlled-lab reproduction; the port extends a cure already started, it does not re-diagnose.
- Compile-coverage-is-not-propagation is R5 target 1 (state/NIGHT_LOOP_20261005.md:262, verified this sitting). The use-stage receipt is positioned DOWNSTREAM of that target's boot-inhalation leg: if target 1's inhalation probe fails, the adoption receipt is moot until a seat provably inhales. Falsifier inheritance explicit.
- The reddit-lane card of this same round (watch/inbox/frontier_olm_2026-10-06/steal/agent-memory-continuity.md, REV 2) banks a session-end consult counter (its S3). Consult (did the seat read the row) and adoption (did the seat's output carry the row's current value) are different legs; the adoption probe presumes its consult sibling. Credited, not duplicated.
- The two-stack merge at compile (quantizer v0.6, tools/thought_quantizer.py:46-51) is the substrate the delta manifest rides; no new feed is proposed.

## OWED / not verified (marked, never asserted)

- OWED the "171 zknot pairs": the count comes from the sweep card (watch/inbox/frontier_olm_2026-10-06/sweep/agent-memory-continuity-arxiv.md:53) with no derivation stated. My census this sitting: `rg --files memory/zknot -g "*.md"` returns 23 files (22 session cards + LATEST.md), so 171 is not the card count and the pairing instrument is not reconstructable from what I read. Whoever runs LAPSE-mini must first mint and receipt the pairing rule.
- The 8-9/13 vs 13/13 adoption counts and the new-value-in-prompt miss finding ride the sweeper's full-text read (sweep :63); my fetch was abs-level and the abstract does not carry them (stated in Verification). If an executor arm needs them byte-true, fetch arxiv.org/html/2610.03902v1 directly.
- The probe is named, not run: no ollama call, no replay harness, nothing executed against gemma:2b this sitting.
- The consult-zero greps on lane/pack surfaces are the reddit card's runs (its "Propagation accounting" block), credited, not rerun here.
- compile_report.json reads "v": "0.4" while the tool docstring documents v0.5/v0.6 laws and the rib feed demonstrably ran (rib_amendments_in 5); both bytes reported, adjudication owed to the quantizer owner.

## Checks run / not run

- RUN: 3 overlap rg commands (zero hits each); WebFetch of both arxiv abs pages (titles, dates, verbatim abstract quotes above); line-cited reads of tools/zknot.py, tools/thought_quantizer.py (docstring), mag/context_pack.py (rg for _quantized_laws/PACK_STALE_DAYS), memory/percolator/invariants.json, memory/corpus/quantized_thought/compile_report.json, memory/corpus/quantized_thought/instructions_flash.jsonl, state/NIGHT_LOOP_20261005.md (rg "compile coverage" -> line 262), the sweep card, the reddit-lane REV 2 card; `git log -n 1 becb53618 | rg -a "fresh-stamped|FRESHNESS"`; zknot file census (23 md files).
- NOT RUN: any ollama/local-model call; the HTML full-text fetches of either paper; LAPSE-mini; the delta manifest or use-stage receipt implementation; any estate test or gate.
