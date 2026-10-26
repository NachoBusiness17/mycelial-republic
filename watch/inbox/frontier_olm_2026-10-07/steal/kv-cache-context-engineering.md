# STEAL CARD: kv-cache-context-engineering (frontier_olm 2026-10-07, round 2 REVISE applied)

Round 1 was REVISED on three defects, none touching the verified sources, quotes,
estate cites, or organ mappings (all re-verified clean by the round-2 critique and by
my own round-2 runs): (1) Probe A's falsifier observable could fire a false kill
(billed input-token COUNT cannot discriminate a cache hit that prices down while
preserving the count), so step 0 now banks the vendor-documented cached-token field
and the primary observables are cached_tokens count and COST; (2) Probe B claimed a
replay substrate the offload ledger does not hold (rows carry no assembly bytes), so
the replay now rebuilds assemblies from current organ state at forced overflow;
(3) the Steal 1 history-side tripwire now names the sanctioned-mutation boundary
(auto-repack and _clip_history legitimately mutate history on overflow). In passing:
Steal 2's restore path is made concrete (re-render from the stub's named source,
sha-checked) and the post-commit shed census is sharpened (414 rows, only the 84
full-mode-at-7200 rows evidence stale code).

Seat: steal-kv-cache-context-engineering gopher. Both source pages fetched live in
round 1 (WebFetch, 2026-10-07) and re-fetched by the critique; the xAI usage-and-pricing
page fetched live in round 2 (WebFetch, 2026-10-07). Every estate cite below was read,
grepped, or counted this session (rounds 1 + 2).

---

## Steal 1: xAI multi-turn prompt-cache canon: the whole history is the cache key, and the reasoning channel is part of the history

Source: https://docs.x.ai/developers/advanced-api-usage/prompt-caching/multi-turn

Verified quotes (live fetch 2026-10-07):
- "never edit, remove, or reorder earlier messages" (the page continues: only append
  new ones; editing, removing, or reordering any earlier message each breaks the prefix
  match, with a worked example per failure mode)
- "For reasoning models, you must include reasoning_content from previous responses"
- "omitting it is the top cause of cache misses"
- Repairs named on the page: send back the encrypted reasoning_content, or use
  previous_response_id so the provider continues the conversation statefully.
- Scope honesty: the page's code samples carry an x-grok-conv-id header with zero
  explanatory text, and the page states no cache TTL. Both details stay OWED if ever
  encoded.

Mechanism stolen: the byte-stability law the estate holds for the system PREFIX
generalizes, as vendor canon, to EVERY earlier message in a multi-turn history: any
edit, removal, or reorder of an earlier user or assistant message breaks the prefix
match; only appends preserve it; and for reasoning models the reasoning channel itself
must ride back in the history or the turn starts as a full miss.

### PRIOR HOLDINGS (reconciled; all read this session)
- Harness amend-cache law: keyed on byte-identical ask text, one wording change = cache
  miss (corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md:10-12).
- DeepSeek frozen-prefix canon: byte-identical system message across asks, 1024-token
  cache floor (memory/research_packs/20260809T021009Z_cache-aware-context-batching.answer.remote.md:11-21),
  plus the xAI prompt_cache_key + 4x cache-pricing block at :55-70 of the same pack.
  NOT held there: the edit/remove/reorder invalidation grammar over the full history,
  and the reasoning_content carry law.
- My overlap grep this session: "What Breaks Caching" or "x-grok-conv-id" over
  catalog/catalog.jsonl = 0 rows.
- The estate's own A2 freeze already embodies append-only on the PREFIX side:
  repack_messages freezes system prompt + tool schemas byte-identical per session and
  appends new instructions as TRAILING messages, "never spliced into the frozen prefix"
  (mag/agent_cli.py:1018-1029); the freeze primitive is mag/context_pack.py:615-652
  with the live-values evolving tail at :655-688.
- The reasoning_content carry law exists as a ONE-PROVIDER empirical note only:
  "kimi-k3 must preserve reasoning_content across turns (thinking-history sensitivity)"
  (mag/inference_budget.py:164, source watch/inbox/model_garden/KIMI1_RUN.md). The
  grok-4.7 FamilyTable row (:169-177) holds streaming and billing notes, NOT the carry
  law, even though grok-4.7 is the funded lane where this vendor canon is literally
  the provider's own.

### Organ fed and port move (gopher fleet, fed by the context pack's freeze machinery)
Concrete port move: (1) add the invalidation grammar + reasoning_content carry as
FamilyTable row properties beside the kimi note (mag/inference_budget.py:156-177) so
multi-turn dispatch lanes inherit the canon per provider instead of rediscovering it
per burn; (2) extend the repack_messages discipline from prefix-only to history-side:
mid-history edits, removals, and reorders become a tripwire on the message list the
same way the frozen prefix already refuses mutation (mag/agent_cli.py:1024-1029).
BOUNDARY (round 2): the tripwire covers NON-overflow mutations only. The estate's
overflow paths legitimately mutate history: auto-repack collapses it to frozen prefix
+ residual + trailing developer messages (mag/agent_cli.py:1087-1090) and _clip_history
drops the oldest messages past MAX_HISTORY_MESSAGES (mag/agent_cli.py:1093-1105); a
tripwire blind to those cries wolf on every overflow. Sanctioned compaction either
routes through a logged fold (composing with Steal 2's stub shape below) or carries an
explicit overflow marker the tripwire accepts; (3) where a lane cannot carry reasoning
bytes back, prefer the stateful-continuation shape the page names
(previous_response_id analog) over rebuilding history and paying the full miss.

---

## Steal 2: ReFold: reversible inter-turn folding with chunked prefix advance

Source: https://arxiv.org/abs/2610.07863 (abstract page fetched live this session).
Scope law: the abstract page verifies the mechanism, reversibility, 2.5x tokens, and
92% compaction claims; the benchmark list, models, k=3 cadence, and the 87% vs 23%
prefix-hit numbers come from this run's own HTML deep read banked at
watch/inbox/frontier_olm_2026-10-07/sweep/kv-cache-context-engineering-arxiv.md:24,
not from the abstract page. Paper-reported numbers, never estate truth.

Verified quotes:
- "a training-free rendering layer that preserves the underlying interaction history"
- "reduces token consumption by up to 2.5x"
- "avoids up to 92% of forced compactions"
- Reversibility confirmed on the live page: every removal is strictly reversible; a
  wrong removal costs one restore from the history rather than permanent content loss.
- From the sweep HTML read (:24): already-displayed content folds to a stub keeping
  signatures, finished turns fold to one-line notes, the cached prefix is rewritten once
  every k=3 steps so between advances the rendered context stays strictly append-only;
  prefix-cache hit 87% vs 23% for mask-style eviction; benchmarks SWE-bench
  Verified/Pro, Multi-SWE-bench, Terminal-Bench 1.0/2.1 on Qwen3.6-27B and
  Qwen3.6-35B-A3B.

Mechanism stolen: compression that never destroys. The rendered context shrinks through
stubs that point back into the untouched history (restore = one read), and the render
boundary advances on a fixed cadence rather than every step, so renders stay append-only
between advances and the prefix cache survives folding.

### WHY THIS IS LIVE HERE (bytes counted this session)
The pack shed ladder fires constantly and its drops are permanent in the render:
- watch/inbox/PACK_OFFLOAD.jsonl holds 2,405 shed rows stamped 2026-10-07 (and 1,977 on
  10-06); today's top shed sections: L4 Heat 194, L3 Task 194, L1 bonds 186, L1b/L1c
  skills + ijl + mirror/clue 170, L0d zeitgeist 170, L0 coordination 170.
- Post-commit census (round 2, my recount via .venv/Scripts/python.exe over the
  ledger): 414 rows fire AFTER the 21:11:41Z commit 633b884ad that raised full mode to
  26000 (mag/context_pack.py:161-188). Breakdown by (mode, max_chars): audit/7500 = 78,
  build/7400 = 90, full/7200 = 84, janitor/4800 = 24, plan/11000 = 84, route/5800 = 54.
  Build 7400, plan 11000, audit 7500, janitor 4800, and route 5800 all MATCH the
  current budget table (mag/context_pack.py:67,86,105,126,146), so ONLY the 84
  full-mode-at-7200 rows (last at 2026-10-07T23:05:24Z) evidence stale code on whatever
  path emits them (candidate: a renderer process older than the commit; not traced,
  OWED). That commit itself carries "ONE UNCONFIRMED (p1a L0d ... the claimed fix state
  was overwritten 12min later by a fresh render)". And the code keeps the ladder as
  "the net for other modes and future growth" (mag/context_pack.py:171-172) even where
  the rescale holds.
- A shed row is LOGGED (schema pack_offload.v1, mag/context_pack.py:35-50) but a logged
  shed is still an irreversible drop from the seat's view: nothing restores the section
  mid-session. Round 2 sharpened this premise twice: (a) ZERO consumers of the ledger
  exist anywhere in mag/ or tools/ (grep this session: every PACK_OFFLOAD reference is
  writer-side inside mag/context_pack.py), so the log is write-only telemetry;
  (b) the ledger itself holds one torn row (bytes 80 a6 + CR, a non-UTF8 partial write;
  the only unparseable line among 34,141 raw lines under my newline-split instrument),
  so even the telemetry is not durable under concurrent append. The _head_tail middle
  amputation (mag/context_pack.py:339-344) is the same lossy class.
- The defect family this answers is the estate's own: the CONTEXT-PACK-layer
  propagation gap (lens/burns.md:151; commit 04ee7066d: L0d carrier shed at stage 3,
  9471 > 7200, zero R4b/R5 mechanism bytes rendered) and the tour-guide-can-drop-pages
  question (lens/questions.md:264-266).

### Organ fed and port move (context pack)
Concrete port move: the stage-3/4 shed ladder (the code path emitting pack_offload.v1
rows, mag/context_pack.py:35-50 and the shed ladder referenced at :171-172 and :1571+
in the render) grows a ReFold-shaped operator: instead of dropping a section, emit a
one-line stub into the render (section name + source path + content sha), and let the
bytes persist where they already live: the assembly is per-render, so the stub names
the source organ/file the section was rendered from, and restore re-renders the
section from that source, sha-checked against the stub's recorded content hash. That
is the reversibility the d01 finding wants. Fold advances (which stubs exist) change only on a
cadence, so consecutive renders inside a window are byte-identical, composing with the
frozen-prefix law already in force (mag/agent_cli.py:1018-1029). The compression hub
mag/context_compression.py (degree-7 hub per lens/graph.md:22) gets the reversible
operator BEFORE any lossy summarizer: its verify_compression (:315-360) is a heuristic
similarity scorer (keyword, structure, quote, number overlap), it measures loss, it
does not undo it.

---

## Falsifiable probes (cheap, this week; named, NOT run this session)

Probe A (serves Steal 1; cents on the funded grok lane; round 2 rewrite, the round-1
falsifier could fire a false kill): fire two 2-turn grok-4.7 dispatches with
byte-identical turn 1; turn 2a only appends, turn 2b edits one earlier assistant
message. STEP 0 (mostly pre-answered this round): the vendor documents the cached-token
usage field: Chat Completions usage.prompt_tokens_details.cached_tokens, Responses API
usage.input_tokens_details.cached_tokens, with cached tokens billed at the
"substantially lower" cached prompt token price
(https://docs.x.ai/developers/advanced-api-usage/prompt-caching/usage-and-pricing,
fetched live this session); what step 0 still banks on one cheap dispatch is whether
grok-4.7 on our lane actually populates the field. PRIMARY OBSERVABLES: cached_tokens
count and COST under the cached vs regular prompt prices. Raw billed input-token COUNT
is a SECONDARY signal only: a cache hit can preserve the count while cutting the rate
(grok cache_read is a price break, research pack :55-70), so a count-equal outcome
kills nothing by itself. FALSIFIER: the append-only turn shows no higher cached_tokens
AND no lower cost than the edited turn → append-only history buys nothing measurable
on this lane and the history-side port is not worth the code. If cached_tokens is
absent or unpopulated after step 0, the probe is unrunnable as specified; bank that
absence as itself the finding (field not populated on this lane) and do not fall back
to a count-only verdict.

Probe B (serves Steal 2; $0 offline; round 2 rewrite, the round-1 text overstated its
replay substrate): the offload rows carry ts/mode/max_chars/total_chars/shed_sections/
stage/root_short ONLY (schema at mag/context_pack.py:38-47), not assembly bytes, and
the ledger has zero consumers, so there is nothing to replay row-wise. Instead REBUILD
assemblies from current organ state: render build_context_pack +
format_context_pack_text over the live memory/state inputs per mode, force overflow by
capping max_chars below the natural assembly size, and run the stub-render variant on
those current rebuilt shapes: shed section becomes a one-line pointer stub. Assert
(a) render lands under max_chars, (b) restore re-renders the section from the stub's
named source and the sha matches the stub's recorded content hash, (c) consecutive
renders inside a cadence window are byte-identical. FALSIFIER: any assertion fails on
the rebuilt shapes → reversible folding does not fit the pack's sections and the
ladder upgrade is dead. Companion live check (my round-2 recount: 414 rows fired after
the 21:11Z budget-raise commit, 84 of them full-mode still at 7200): if a week of rows
shows zero sheds post-fix AND probe B fails, the whole ladder mechanism change is
unjustified; if sheds keep firing, the rescale-alone cure is falsified and the
mechanism change is owed.

## OWED / not verified
- ReFold benchmark numbers and 87% vs 23%: paper-reported via our sweep HTML read;
  never assert as estate truth.
- k=3 cadence: from the HTML read; the abstract page says only "every few steps".
- xAI cache mechanics beyond the fetched pages: the usage-and-pricing page (round 2)
  documents the cached-token field names and the lower cached price but states NO
  minimum cacheable prefix and NO TTL (it only notes a miss "is expected on the first
  request or after cache eviction"); whether grok-4.7 populates the field on our lane
  is Probe A step 0. x-grok-conv-id semantics: recommended in the overview page's
  wording, never explained.
- Which process emits the post-commit full-mode 7200 rows: not traced; bytes +
  timestamps + the 414-row recount banked above.
- The torn ledger row (bytes 80 a6 + CR): noted, not healed; whether it came from a
  concurrent append is untested.
- Probes A and B: named, not run; the burns ledger owns firing.

## Receipts
- Round 1 live fetches: the xAI multi-turn caching page and the arXiv 2610.07863
  abstract page (WebFetch x2, 2026-10-07); quotes above. Round 2 live fetch: the xAI
  usage-and-pricing page (WebFetch, 2026-10-07; field names + cached-price sentence).
- Overlap greps (round 1): grep -c "2610.07863|ReFold" catalog/catalog.jsonl = 1
  (the raw daily mirror row only); grep -c "What Breaks Caching|x-grok-conv-id"
  catalog/catalog.jsonl = 0.
- Shed census (round 1): ts-day counts over watch/inbox/PACK_OFFLOAD.jsonl
  (10-06: 1,977 rows; 10-07: 2,405 rows); section histogram grep|sort|uniq -c.
- Shed census (round 2, .venv/Scripts/python.exe): 34,141 raw newline-split lines,
  34,139 parsed, 1 torn row (bytes 80 a6 + CR); rows with ts > 2026-10-07T21:11:41 =
  414 (audit/7500 78, build/7400 90, full/7200 84, janitor/4800 24, plan/11000 84,
  route/5800 54); last ts 2026-10-07T23:05:24.616946Z.
- Consumer grep (round 2): PACK_OFFLOAD/pack_offload over mag/ + tools/ .py = writer
  side only (mag/context_pack.py:17,35-50,1518 + comments); zero readers.
- Budget-table read (round 2): max_chars per mode at mag/context_pack.py:67 (janitor
  4800), :86 (route 5800), :105 (build 7400), :126 (audit 7500), :146 (plan 11000),
  :173 (full 26000).
- Estate cites read across rounds: mag/context_pack.py:35-50, :161-188, :339-344,
  :347-358, :615-652, :655-688; mag/agent_cli.py:1004-1029 and :1082-1111 (round 2:
  the repack return shape at :1087-1090, _clip_history at :1093-1105);
  mag/inference_budget.py:142-177; mag/context_compression.py:315-360;
  corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md:10-12;
  memory/research_packs/20260809T021009Z_cache-aware-context-batching.answer.remote.md:11-21
  and :55-70; lens/burns.md:151; lens/questions.md:255-266; lens/graph.md:22-26;
  git log 633b884ad (p1a, 2026-10-07 17:11:41 -0400) and 04ee7066d (dogfood2
  propagation-gap evidence).
