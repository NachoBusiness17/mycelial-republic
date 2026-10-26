# Build script for the kv-cache-context-engineering steal card (scratch, this sitting).
# Writes the card, enforces the no-em-dash law, emits the one-line machine JSON.
import json
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
OUT = ROOT / "watch/inbox/frontier_olm_2026-10-05/steal/kv-cache-context-engineering via x.md"

BODY = """# STEAL: kv-cache-context-engineering (1 confirmed find) - 2026-10-05 - ROUND 1

Area: kv-cache-context-engineering via x
Banked by: steal-kv-cache-context-engineering (Mag Resource Harness steal gopher)
Round: 1, first draft (previous critique: none yet)

## Find provenance (verified this sitting)

- Source: https://x.com/theo/status/2100762304862384257 (@theo, 2026-09-18). Re-fetched this sitting through the fxtwitter JSON door (https://api.fxtwitter.com/theo/status/2100762304862384257): HTTP 200, full text 3,131 chars, created "Fri Sep 18 01:42:18 +0000 2026". The find's quote fragment "cache write costs go over 60%" is present verbatim. The tweet is a six-point teardown of a per-tool-call history-filtering tool; the find quoted point 5, but points 1-4 carry mechanism the estate should port too (scoping below).
- Verbatim core (point 5): "Cache writes are more expensive than cache reads. Cache writes are the biggest cost by far for agents. I often see cache write costs go over 60% of my total LLM spend in my personal use of Claude Code and Codex. Cache writes are insanely expensive when data earlier in the history is changed (because the old cache is invalidated when things change at the top). Every history edit requires a cache rewrite for ANY data past the history edit. If your history is '1,2,3,4,5,6' and you delete '2', you have to rewrite '3,4,5,6'. This is more expensive than leaving '2' in the history."
- Also ported (same tweet, this sitting's fetch): point 1 "Compaction isn't a filter. The role of compaction is to clean up history to keep the agent focused, not just deleting noise. It should be used sparingly when context gets too long, not constantly to keep context small." Point 2: a per-tool-call trimmer "doesn't even know what the result of the tool call is", and deleting tried-things dooms the model to "stupid loops". Point 3: frontier APIs share reasoning as encrypted payloads and Anthropic is stricter, "requiring you to preserve the entire history in order to get any of the reasoning data". Point 4: "Frontier Labs have been including compaction and long runs as part of the training process."

## Overlap scoping (what the estate already holds)

The find's overlap grep is confirmed with one refinement. Re-ran this sitting: grep for "cache write costs", "60% of my total LLM spend", "cache-write" over memory/ markdown (agent_sessions excluded) and the catalog: zero hits on Theo's quantification or the edit-point arithmetic. Pre-banked and adjacent (same mechanism family, not this claim):
- The frozen-prefix mechanism itself: watch/inbox/burn_reset_20260927/flash50/w3-research-cachemech.md:149-179 (A2 law citations, fleet KPI table, meter inventory).
- Cache-write storms from prefix invalidation as failure mode #1: memory/runs/salon_20260827/COMBINED.md:21 ("Cache invalidation is the first break" with "hit-rate collapse 90% to 0% per epoch, cache-write storms") and memory/runs/salon_20260827/grok_sd.md:10 (promoting a new standing prompt drops production hit-rate 90% to 0%; "cache-write storm + frozen-RIB identity change").
- Prefix-caching economics funds keep-everything: watch/inbox/frontier_olm_2026-10-01/sweep/agent-memory-continuity-x.md:33 and :48 ("97% of those tokens were cached"; "the estate's byte-identical cache law is the same bet").
- Wire-shape cache rewrites: memory/runs/quote_audit_wide_20260925/snapshot/corpus/steal/MASTER_MICKEY17_V2_20260924.md:83 (nous native wire "re-writes the previous turn's prompt cache on 14-20% of consecutive calls"; the canonical corpus/steal/ copy of that line was not re-verified this sitting).
Therefore NEW from this find: (1) the practitioner dollar baseline (write side over 60% of spend on Claude Code/Codex shapes), (2) the edit-point arithmetic as a review formula (delete "2", rewrite "3,4,5,6"), (3) compaction as a sparingly-fired focus tool, not a continuous size filter, (4) trimmer blindness (per-tool-call deletion decided without the tool result), (5) full-history preservation as the price of reasoning payloads on Anthropic-shape wires, (6) models are trained on their own compaction flows.

## Estate byte-truth (verified this sitting)

- A2 law: mag/context_pack.py:467-472, the system prompt + tool schemas "must be BYTE-IDENTICAL for the whole session - provider prompt caches key on exact prefix bytes, so a system prompt that re-renders per repack re-prices the entire context" every call. freeze_system_prompt at :489, evolving_tail at :529 (all live values ride AFTER the prefix).
- Trailing law: mag/agent_cli.py:1024-1026, new instructions "ride as TRAILING developer messages, appended at the END of the payload - never spliced into the frozen prefix, where a mid-insert would re-price everything after it" (em-dash in source normalized to hyphen per the no-em-dash law).
- Measurement stack already exists: mag/honest_cache_meter.py tracks cache_write_tokens per provider with rate cards (:144 cache_write_per_mtok, :170, :204 Anthropic cache_creation_input_tokens, :215 "OpenAI reports no separate write bucket", :256 the rate-card multiply) and its docstring vows "NEGATIVE savings on write-heavy days" (:20-21); mag/cache_watch.py standing $0 monitor; scripts/probe_cache_ab.py controlled A/B; tools/prefix_cache_sim.py deterministic prefix-cache simulator; tools/cache_kpi.py fleet hit-rate KPI (all present by ls this sitting).
- Quantizer organ: mag/state_quantizer.py:1-27 docstring: compresses N Verkle knots into one summary knot; "long-running agent conversations reference this knot as memory"; between DnD rooms the quantizer compresses and "next room loads from summary".
- Percolator: mag/percolator.py:1-27, deterministic pipeline (SIGNAL/THEATER/NOISE, repeatables compile to invariants), candidates land promoted=False behind review (the --candidates law at :24-27).
- Descent protocol legs 2 and 4: memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:34-37 (CLARITAS + LAW FACE, "the prompt itself is dogfood") and :38-40 (OPERATOR-PROXY STEER via revision.md between turns).
- Cross-link: the sibling card watch/inbox/frontier_olm_2026-10-05/steal/agent-memory-continuity.md row 7 banks "preserve failed attempts as diagnostic context" from a different frontier thread; Theo point 2 is the same law seen from the cost side.

## The steal (mechanism, not a link dump)

In a prefix-cached agent loop, cost is a function of WHERE the context mutates, not how big it is. Every token is paid at least once as a write (full price or premium); reads are the discount. An edit at position i re-prices everything after i, so deleting context to save tokens can cost more than it saves: the tokens removed were cheap reads, and the rewrite is a premium write over the whole tail. Corollaries: compaction is a sparingly-fired focus tool with a re-pricing bill, not a continuous filter; a per-tool-call trimmer is doubly self-defeating (it decides without the tool result, and every deletion re-prices the tail and hides the tried-things that prevent stupid loops); on Anthropic-shape wires, preserving full history is also the price of reasoning payloads; and hand-rolled compaction fights models already trained on their own compaction flows.

## Per-find mapping (one find, four organ feeds)

| Organ | Port move |
|---|---|
| context pack (mag/context_pack.py:467-472, :489, :529; mag/honest_cache_meter.py; mag/cache_watch.py) | The A2 law already holds the mechanism; port the METRIC. Surface write-share-of-spend as a standing KPI next to hit ratio (the meter already collects cache_write_tokens and rate cards; alarm at Theo's 60% disease signature), and adopt delete-2/rewrite-3456 as the review formula: cost of any history edit = rewrite of the tail after the edit point, usually more than the tokens saved. |
| quantizer (mag/state_quantizer.py:1-27) | Summary knots are compaction events. Law: a knot is born at a conversation/room boundary (seeds a NEW prefix) or referenced in the tail; never inline-swapped into a live conversation's earlier turns. Cadence: sparingly at boundaries, not continuously (Theo point 1). The room-boundary design in the docstring is already boundary-shaped; freeze it as a law so no lane "refreshes" a knot mid-conversation. |
| percolator (mag/percolator.py:1-27) | Any candidate that changes frozen-prefix bytes (standing doctrine text, tool-schema addition, prefix reword) carries a prefix_bytes_delta cost line in its review fields; a mid-fleet prefix promotion is the cache-write storm the estate's own salon named failure #1, and Theo adds the dollar form of that storm. |
| gopher fleet / descent protocol (memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:34-40; mag/agent_cli.py:1024-1026) | Premium-turn prompts keep the law block byte-identical across the whole climb (a re-rendered block re-prices every checkpoint turn); steering rides as appended trailing messages (already the agent_cli law). Plus two handoff laws: sensing lanes must not trim tool results before judgment dispatch (trimmer blindness), and Anthropic-shape lanes preserve full history for reasoning payloads (feeds the wire pinning noted at the MASTER_MICKEY17 snapshot :83). |

Not fed: sovereign mirror and water graph get no direct port from this find (the identity-over-frozen-bytes adjacency is the salon's pre-banked holding, not a new move).

## The falsifiable probe: WRITE-SHARE CENSUS (descriptive arm RUN at full scale this sitting)

Instrument (this sitting, read-only, stdlib, zero model calls): one-pass aggregation over logs/provider_usage.jsonl (26,062,137 bytes, mtime 2026-10-05 13:50 local), ok rows only, write proxy = prompt_tokens - cached over provider-reported fields (cache_hit_tokens / cached_tokens / cache_read_tokens / prompt_tokens_details.cached_tokens; explicit cache_miss_tokens cross-checked), moment 2026-10-05.

MEASURED, September 2026 (38,546 ok rows):
- deepseek 3.9% write share (605,625,011 prompt / 581,812,864 cached): the frozen-prefix lane is disciplined, matching the 96.1% tok_hit in the w3 receipt.
- Telemetry-carrying free lanes are write-heavy: z_ai3 91.5%, xai 95.2% (n=1), openrouter 85.8%, cerebras 84.9%, nous 58.0%, z_ai 17.5%.
- groq, together, ollama, z_ai2 report zero cached fields on every row: their "100%" is telemetry-blindness, counted as no-telemetry, never as proven writes (cache_kpi's own law).
- Fleet total 4.1% (deepseek dominates volume).

MEASURED, October-to-date (102 ok rows, small n): deepseek 37.3%, z_ai3 49.6% by proxy (the vendor's explicit miss field reads higher, 31,622 vs 13,472, denominator quirk unresolved), total 41.1%. Cross-check this sitting: tools/cache_kpi.py --since 2026-10 prints tok_hit 48.9% total (deepseek 62.7%, z_ai3 30.2%); both instruments agree the October regime is write-heavy.

The estate therefore shows TWO REGIMES: a disciplined volume lane near 4% and sensing/free lanes at 85-100% (or unmeasurable). Theo's 60% dollar figure sits between them; on lanes where reads are discounted and writes full price, the token share LOWER-BOUNDS the dollar share.

Executor arms (cheap, one-file aggregations, zero model calls):
(a) ATTRIBUTION: rows carry session_id; per session, split write tokens into first-call cold starts (structural) vs mid-session miss spikes (the delete-2 signature: miss tokens appearing after established hits within one session_id). Prediction: September deepseek's 3.9% is cold-start-dominated; any session with an in-conversation spike names the lane holding a live history-repricing bug. FALSIFIER A: if no session anywhere shows the mid-session spike pattern, the edit-point mechanism has no local instance and this card demotes to a dollar-guard law for premium turns only.
(b) DOLLAR WEIGHTING: re-run with mag/honest_cache_meter.py rate cards (:144) to convert token shares into spend shares and compare against Theo's 60%. FALSIFIER B: if dollar-weighted write share on the heaviest spend lane cannot be computed from provider-reported fields, the 60%-as-lever framing is unverifiable locally and dies to WARN (the mechanism law survives on the A2 + salon prior).

## Degradations (honest)

- Theo's 60% is a personal-use observation on Claude Code/Codex (Anthropic/OpenAI shapes where writes carry premium and reads discount), not a benchmark; the find's 0.97 confidence is about the find, not the number's universality.
- October n is small (5 days, 115 rows total) and includes this sweep's own dispatches; the regime shift is a signal to attribute, not a concluded trend.
- The write proxy is token-wise; Theo's figure is dollar-wise. On discounted-read lanes the dollar share exceeds the token share, so comparisons are directional lower bounds.
- z_ai3's vendor miss field exceeds prompt-minus-cached (31,622 vs 13,472 October); unresolved denominator quirk, disclosed.
- Telemetry-blind providers (groq, together, ollama, z_ai2) are counted as no-telemetry, not as writes.
- The x.com URL itself was not fetched directly; the fxtwitter JSON door is the standing door per the sweep's source note and returned 200 this sitting.
- The canonical corpus/steal/MASTER_MICKEY17_V2_20260924.md:83 line was verified only via the quote_audit_wide snapshot copy.
- Quotes from repo sources containing em-dashes are normalized to hyphens per the no-em-dash law; the tweet text itself contains no dashes and its quoted fragments above are verbatim from this sitting's fetch.
- Not run: the session_id attribution join, the dollar weighting, any model call.

## Machine-readable card (identical to the returned StealCard JSON; chars = the prose body above this line, measured)

"""

card = {
    "area": "kv-cache-context-engineering via x",
    "steal": "In a prefix-cached agent loop, cost is a function of WHERE context mutates, not how big it is: every token is paid at least once as a write (full price or premium), reads are the discount, and an edit at position i re-prices everything after i. Theo's arithmetic (verbatim, tweet point 5): history '1,2,3,4,5,6', delete '2', you have to rewrite '3,4,5,6', which is more expensive than leaving '2' in; practitioner baseline: cache write costs go over 60% of total LLM spend in his Claude Code and Codex use. Corollaries ported as laws: compaction is not a filter, it is a sparingly-fired focus tool that carries a re-pricing bill, not a continuous size filter; per-tool-call trimming is doubly self-defeating (the trimmer decides without knowing the tool result, and every deletion re-prices the tail and hides the tried-things, causing stupid loops); on Anthropic-shape wires full-history preservation is also the price of reasoning payloads (encrypted traces require the entire history); frontier models are trained on their own compaction flows, so hand-rolled filters fight the training. Pre-banked adjacency (not re-banked here): the frozen-prefix mechanism (w3-research-cachemech.md:149-179), cache-write storms as failure #1 (salon_20260827 COMBINED.md:21, grok_sd.md:10), prefix-caching economics (frontier_olm_2026-10-01 sweep :33,:48).",
    "source_url": "https://x.com/theo/status/2100762304862384257",
    "estate_map": "Four organ feeds. (1) CONTEXT PACK (mag/context_pack.py:467-472 A2 law, freeze_system_prompt :489, evolving_tail :529; mag/honest_cache_meter.py; mag/cache_watch.py): the mechanism is already law, port the METRIC - surface write-share-of-spend as a standing KPI beside hit ratio using the meter's existing cache_write_tokens + rate cards (:144,:170,:204,:256), alarm at Theo's 60% disease signature, and adopt delete-2/rewrite-3456 as the review formula for any pack or history edit (cost = rewrite of the tail after the edit point). (2) QUANTIZER (mag/state_quantizer.py:1-27): summary knots are compaction events; law = knots are born at conversation/room boundaries (seeding a NEW prefix) or referenced in the tail, never inline-swapped into a live conversation's earlier turns; cadence = sparingly at boundaries, never continuous. (3) PERCOLATOR (mag/percolator.py:1-27): candidates that change frozen-prefix bytes carry a prefix_bytes_delta cost line in review fields; mid-fleet prefix promotion = the salon's cache-write storm (COMBINED.md:21) now with a dollar form. (4) GOPHER FLEET / DESCENT PROTOCOL (RIB_THE_DESCENT_PROTOCOL_20261001.md:34-40; mag/agent_cli.py:1024-1026): law block byte-identical across a whole premium climb, steering rides as trailing appends; sensing lanes must not trim tool results before judgment dispatch; Anthropic-shape lanes preserve full history for reasoning payloads. Not fed: sovereign mirror, water graph.",
    "probe": "WRITE-SHARE CENSUS over logs/provider_usage.jsonl, read-only, zero model calls; descriptive arm RUN at full scale this sitting (moment 2026-10-05): September deepseek 3.9% write share (605,625,011 prompt / 581,812,864 cached, 37,893 ok rows) vs telemetry-carrying free lanes z_ai3 91.5%, openrouter 85.8%, cerebras 84.9%, nous 58.0%, xai 95.2% (n=1); groq/together/ollama/z_ai2 report no cache telemetry (counted no-telemetry, never as writes); fleet total 4.1%. October-to-date small n: deepseek 37.3%, z_ai3 49.6%, total 41.1% (cross-check tools/cache_kpi.py --since 2026-10: tok_hit 48.9%). Two regimes measured: disciplined volume lane near 4%, sensing lanes 85-100%. Executor arms, both one-file aggregations: (a) ATTRIBUTION via the session_id field on every row - split write tokens into first-call cold starts vs mid-session miss spikes (the delete-2 signature); FALSIFIER A: no session anywhere shows the mid-session spike pattern means the edit-point mechanism has no local instance and the card demotes to a dollar-guard law for premium turns; (b) DOLLAR WEIGHTING via mag/honest_cache_meter.py rate cards (:144) to compare spend share against Theo's 60%; FALSIFIER B: if the heaviest lane's dollar-weighted write share is not computable from provider-reported fields, the 60%-as-lever framing dies to WARN while the mechanism law survives on the A2 + salon prior.",
}

body_chars = len(BODY)
card["chars"] = body_chars
machine = json.dumps(card, ensure_ascii=True)
full = BODY + machine + "\n"

for bad, name in (("\u2014", "em-dash"), ("\u2013", "en-dash")):
    if bad in full:
        idx = full.index(bad)
        raise SystemExit(f"{name} found at offset {idx}: ...{full[max(0,idx-60):idx+60]}...")

OUT.write_text(full, encoding="utf-8")
print("WROTE:", OUT)
print("body_chars:", body_chars, "| total_chars:", len(full), "| machine_json_chars:", len(machine))
print("MACHINE_JSON:", machine)
