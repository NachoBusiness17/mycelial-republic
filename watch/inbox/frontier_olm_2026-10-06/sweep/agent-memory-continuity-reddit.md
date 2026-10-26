# Sweep: agent-memory-continuity via reddit (2026-10-06)

source-fetched: 2026-10-06. Area: agent-memory-continuity. Seat: sweep gopher, frontier_olm_2026-10-06.
Every quote below is verbatim from a page I fetched this sitting (raw files under
`watch/inbox/frontier_olm_2026-10-06/sweep/raw/thread_*.txt`). Laws held: no fabrication,
ascii only in my own prose, every claim cites its fetch.

## Doors (what actually worked, this sitting)

- Recipe's primary door DEAD, confirmed again: `old.reddit.com/r/*/top.json` returns an HTML
  "Welcome to Reddit / Log in" interstitial to both WebFetch and the web_reader MCP
  (`sweep/doors/` evidence; the same interstitial a sibling lane recorded today at
  `lens/doors.md:46-62`); `www.reddit.com/r/LocalLLaMA/top/.json` returns HTTP 403;
  `api.reddit.com/comments/1rxywnf` returns HTTP 403. A sibling's JSON fetcher with a scripted
  UA got HTTP 404 on all four subs (`sweep/doors/*.json.err`, status=404).
- Recipe's fallback (WebSearch site:reddit.com) degraded but usable: intermittent z.ai 1302
  rate limits, retries succeeded; it supplied candidate URLs (1rxywnf, 1rejuyw, 1sk656i,
  1rj18h4, 1sna5kb) but no fetchable pages. Recorded as the degraded door.
- WORKING door this sitting: reddit Atom RSS with a browser UA, paced 8-12 s with 429
  backoff. Top-month feeds: `r/{sub}/top/.rss?t=month` for LocalLLaMA (25 entries),
  MachineLearning (24), LocalLLM (17), ollama (17) - LocalLLM and ollama needed one retry
  each after 429s. Search feeds: `r/{sub}/search/.rss?q=...&restrict_sr=1&sort=relevance&t=month`
  over 8 memory-topic queries = 148 entries (`sweep/doors/memsearch_candidates.json`).
  Deep-read door: per-thread comments RSS `r/{sub}/comments/{id}/.rss`, which serves the
  post plus every comment entry. This extends the day-5 mine's RSS listing recipe
  (credit: frontier_olm_2026-10-05 register, "r/LocalLLaMA RSS-door recipe") to full thread
  bodies; day-5 never deep-read the threads below except 1wl3828.
- Fetcher scripts: `sweep/doors/mem_search_fetch.py` + `sweep/doors/thread_read.py`
  (host allowlist, DOCTYPE/ENTITY XML guard per the Mimosa entity-expansion finding,
  CREATE_NO_WINDOW subprocess on win32, output paths asserted inside the sweep dir).

## Pass 1 / Pass 2 census

- Pass 1: 85 top-month entries + 148 search entries + WebSearch results = 200+ candidates
  considered (ask asked for 30+), dated 2026-09-05..2026-10-06, listed in `sweep/doors/`.
- Pass 2: 8 threads fetched end to end and read in full (entry counts: 96, 4, 12, 21, 14,
  20, 20, 8). A 9th (1wqqott, SQLite memory layer) rendered post-only (1 entry, no body) -
  fetched, not readable, not banked as a read.

## Overlap checks (run this sitting)

- `rg "1wl3828"` over catalog/, memory/, frontier_olm_2026-10-05/: hits only in day-5's own
  DIGEST.md, RECEIPT.md, sweep file, and raw harvest. Day-5 recorded this thread UNCONFIRMED
  ("2 of 7 sub-claims absent from the fetchable render", DIGEST.md:69, carried at
  lens/burns.md:100-105).
- `rg -il "supersession|superseded"`: day-4's sweep
  (`frontier_olm_2026-10-04/sweep/agent-memory-and-continuity-reddit.md` lines 45, 55,
  113) and day-5's sweep (lines 59-67) already bank the supersession law, the mem0
  0.53/n=30 revival measurement, the Delhi-to-Mumbai identity schema, and the 77%->94%
  owner+conflict measurement. NOT re-banked here; my new items are threads neither day
  deep-read.
- `rg -il "mengram|memfmt"`: raw post text already sits in the Arctic Shift archive
  (`corpus/social_archive/reddit_20261001/as_ollama_mem.json`) but zero register rows or
  sweep findings name it; day-4 harvested the thread id (`_amc_reddit_harvest.jsonl`) and
  banked nothing from it.
- `rg -il "silence was the bug|zero memory calls"`: only my own raw file. New.
- `rg -il "dynamic context pruning|opencode-dcp"`: zero hits. New.
- `rg -l "1wz3xnf|1wai0iv|1wlbqnl|1wd4tcw|1wqa5da"` over day-4/day-5 sweep + registers:
  ids appear only in day-4's raw harvest jsonl (pass-1 candidate lists), zero banked rows.
- V2ASK3.md hit for "source of truth" is a Godot/Roblox parity harness paid ask; unrelated.

## Items (strongest first)

### 1. VERDICT UPGRADE: r/LocalLLaMA 1wl3828's two unconfirmed sub-claims confirmed on a deeper render (2026-09-20)
Day-5's only unconfirmed item resolves. The comments RSS serves 96 entries (day-5's render
was thinner). C57 (/u/redtortuga19) verbatim from my render
(`raw/thread_1wl3828.txt` entry 57): "The database has entities, groups, values, notes, and
*relationships. Relationships point from entity to entity like 'fancy checkout button' ->
calls -> 'this class' -> triggered by -> blah blah. This basically allows the agent to have a
simple graph database inside SQLite." C70 (/u/FutureStriking283) entry 70: "I wonder if
there's a clue to be had from the prior decades data engineering handbook for Hot, warm &
cold. That's what I'm circling ..". Both were recorded absent at DIGEST.md:69; both are
byte-present in a fetch I ran. The thread's other 94 entries also carry the supersession
law and the 0.53 measurement (already banked day-5; overlap credited, not re-banked).

### 2. r/ollama 1wai0iv (mengram, 2026-09-08): extracted memory cannot tell plans from history - 35 of 37 "procedures" were never run (belief-retirement depth, RQ5/RQ4)
OP moved agent memory into a folder of Markdown (entities, episodes, procedures with
per-step success/fail records); after a failed run the agent is asked "what belief broke"
and writes the next workflow version; search/recall/the run-gate are plain code. The
thread's crux is OP's own admission after an AI reviewer's methodological hit (entry 11:
attach source spans, count supported/duplicate/unsupported against a hand-checked reference,
"not Sonnet's output as ground truth"): "I went looking in my own folder after reading this:
35 of 37 extracted 'procedures' are plans from conversations - launch checklists, build
plans - not sequences anyone ever run..." verbatim: "So the extractor does exactly what you
describe: it cannot tell 'here is what we will do' from 'here is what we do', and both land
as reusable workflows with the same shape." That is the estate's belief-retirement disease
at write time: intent lands in the same shape as history, so nothing downstream can
distinguish a cured belief from a proposal. Secondary payload: a local extraction bench
(entry 10: llama3.1:8b, qwen2.5:7b, qwen3:8b, qwen3:4b vs sonnet-5 reference; all 4/4
first-try valid JSON at num_ctx 16384 with format:json; qwen3:4b found both workflows Sonnet
found; Ollama's ~4k default context silently cut his prompt until the tool sent num_ctx
itself). Repo: github.com/alibaizhanov/mengram, bench at benchmark/local-extraction.

### 3. r/LocalLLaMA 1wlbqnl (2026-09-20): "The silence was the bug" - 40% of sessions made zero memory calls; self-graded memories confirm planted ones (propagation clock, RQ1/RQ5)
Asly97 (entry 8) measured the failure the estate's propagation clock is named after:
"Something like 40% of sessions had zero memory calls and everything looked perfectly
normal. The silence was the bug." His countermeasures: lookup as step one of instructions,
one shared store, last-write-wins, and the admission that "no philosophy on earth fixes a
model that treats the call as optional when it's feeling lazy." Danculus (entry 16) adds
the verifier law: "In my tests an agent that graded its own memories also confirmed a
planted one, so I ended up trusting only memories whose outcome something outside the agent
had confirmed." Map: a propagation-clock instrument must count per-seat-class whether the
boot pack's law rows were actually LOADED and USED per session (the estate analog: per-seat
boot receipts citing rib digests), because silent skip is the dominant failure, and belief
retirement needs an outcome verifier outside the seat that holds the belief. KenOtwell
(entry 7) contributes the paging frame: "evict raw text and keep formatted summaries. When
gets tighter, just keep keyword sets and look up keys" - placement tiers, not one-shot
compaction.

### 4. r/LocalLLaMA 1w7wb0n (2026-09-05, one day outside the strict 30-day window, kept for RQ2): boot-pack presence is not enforcement; the law stack has a load-cost tiering (two-law-stack merge)
The LLVM AGENTS.md debate's sharpest line, feng_sg (entry 11) verbatim: "Putting 'don't
access .env' in AGENTS.md is a sticky note on a door with no lock. The model has to read it,
remember it, and choose to comply. Until those directives map to actual sandbox or
tool-permission checks at runtime, they're suggestions dressed up as policy." That is the
terminal leg of the propagation clock: a law row can land in every boot pack and still not
be propagated if nothing at runtime enforces it. RLutz (entry 6) supplies the merge
contract's cost axis: "Every token in CLAUDE.md is loaded on every single turn... CLAUDE.md
only for things that are important enough to justify including on every single turn",
skills ride frontmatter-only until invoked, pointers fetch docs on demand - i.e. the AGENTS
stack should be merged into always-loaded / lazy-loaded / pointer tiers by per-turn cost,
not by provenance. Commenter cites arxiv 2602.11988 on AGENTS.md failure modes (not fetched
this sitting: OWED).

### 5. r/LocalLLaMA 1wz3xnf (2026-10-06): recall collapse at 13% context use - a cliff BELOW the summarization layer (compaction cliff, RQ3)
A repetition-loop report at 13% context utilization resolves to two model-side causes, not
context overflow: KV cache quantization (`--cache-type-k q8_0 --cache-type-v q8_0`) and
low-context finetunes. Emotional-Package-91 (entry 17) verbatim: "even when the base arch
supports more context the model effectively gets 'lobotomized' or usually stuck in
repetition loops once you surpass certain context length (trained on)". Edenar (entry 20):
"Do not quant kv cache for long context (use 16bit)". Map: the estate's placement-vs-
compaction question needs a floor measurement - any summary/placement scheme sits on a
model whose effective recall horizon can be 4-16k regardless of window size; the estate's
own q8_0 KV rows (B4 sweep) and gemma:2b janitors live near this cliff. Not a summary
failure: no summarizer can fix it, and it can masquerade as one.

### 6. r/ollama 1wd4tcw (2026-09-11): the multi-writer shared-memory contract (two-law-stack merge, RQ2)
OP states the exact hazard of several seats writing one memory: "If each assistant writes
its own summary back into shared memory, a mistaken compression can become authoritative
for every later session." The proposed contract: small Markdown records with stable IDs,
timestamps, source links, explicit supersession, append-only decisions; embeddings and
model-specific summaries are disposable indexes; writes pass a narrow process that prevents
two assistants from silently replacing the same fact. and_pf (entry 1) adds the key rule:
"append-only with explicit supersession, so a mistaken automated 'compression' can never
silently become the authoritative version." Map: this is the merge contract shape for the
estate's AGENTS.md + rib-vault two-stack problem - one stack must be canonical append-only
records, the other a disposable compiled index, and no automated compile may overwrite
canonical rows (the freshness-theater cure at the write leg). Overlap: day-4's line-45
schema covers single-writer fact identity; the multi-writer narrow-write-process contract
is new.

### 7. r/LocalLLaMA 1wyt020 (Memoria 1.0.0, 2026-10-06): an ablatable temporal axis + LongMemEval tooling on a 3.7 GiB box (propagation clock instrument shape, RQ1)
Fresh 1.0.0 release, model-agnostic and local-first (benchmark host: Celeron N4020,
1.10 GHz, 3.7 GiB RAM, no GPU). Author numbers (unreplicated): LongMemEval-S Recall@1 89.8%,
Recall@5 97.9%, Recall@10 98.9%, session NDCG@10 0.9257, peak RSS 2.65 GiB. Six parallel
retrievers (FAISS, BM25, graph, phrase, attribute, temporal) fused by multi-signal ranking.
The instrument shape is the steal, verbatim: "Temporal retrieval is independently
implemented too, so I can measure it and ablate it instead of having it baked into the base
retrieval path." Ablatable recency is exactly what a propagation clock needs: measure how
much recall depends on the timestamp axis per seat class. Honest propagation gap in the
release itself: a commenter asked where the docs teach an agent to use Memoria and the
author answered "No you aren't" - the memory layer shipped before the boot-pack row that
would make a seat use it.

### 8. r/LocalLLaMA 1wqa5da (2026-09-25): the offload-reload check is the expensive leg; DCP named (compaction, RQ3)
Against "offload to memory.md" as the compaction cure, sburel (entry 9) names the cost
leg verbatim: "The offload part is easy. The 'quick check every request' is where it gets
expensive or wrong: either a second model call per turn to decide what to reload, or a
cheap keyword match that misses the one thing you needed." DinoAmino (entry 2):
"Compacting isn't for reducing context. It is a workaround for having insufficient context
to finish a session." Atretador (entry 7) links opencode-dynamic-context-pruning
(github.com/Opencode-DCP/opencode-dynamic-context-pruning), not previously in the estate
(zero grep hits). Overlap: day-4 banked the compaction consensus (77%/0.2% decision/command
split, natural-stop handoffs); this adds the reload-check economics and the DCP pointer.

## Fix-design seeds for the estate (from what was read, not invented)

1. Propagation clock instrument (RQ1): per-seat-class boot receipt that counts (a) rib rows
   carried, (b) law rows actually consulted in-session (tool-call accounting like Asly97's
   40%-zero-calls census), (c) runtime enforcement hooks wired (feng_sg's no-lock law).
   A row is propagated only when all three are true for the seat class; otherwise it is
   compile coverage, not propagation. Memoria's ablatable temporal axis shows the
   measurement shape for the recency leg.
2. Two-law-stack merge contract (RQ2): canonical stack = append-only records with stable
   ids, timestamps, source links, explicit supersession, narrow multi-writer write path
   (1wd4tcw); the compiled AGENTS.md/boot-pack = disposable index that may never overwrite
   canonical rows; merge tiers by per-turn load cost: always-loaded / lazy skill / pointer
   (RLutz); every law that matters gets a runtime check, not prose (feng_sg).
3. Belief retirement (RQ5): on write, tag records as plan vs history (mengram's 35/37
   disease) - an extract that cannot tell intent from event must not land as outcome;
   retirement propagates only when an outcome verifier OUTSIDE the holding seat confirms
   the new state (Danculus's planted-memory test); supersession already banked day-4/5.
4. Compaction cliff floor (RQ3): before benchmarking summarize-vs-place on zknot archives,
   measure the model-side recall horizon (KV quant state, finetune context horizon) so a
   repetition-loop collapse is not misread as a summary failure (1wz3xnf); price the
   reload-check leg per turn (1wqa5da).

## Honest gaps

- 1wqqott (SQLite memory layer) rendered post-only through the RSS door (1 entry, empty
  body): fetched, unreadable, not banked.
- The 1rxywnf / 1rejuyw / 1rj18h4 / 1sna5kb threads surfaced by the degraded WebSearch door
  were not fetched this sitting (budget went to deep reads); they remain candidates.
- Memoria numbers, mengram bench numbers, and the 40% zero-calls figure are author-reported,
  unreplicated (L14: conditions named, not estate-verified).
- arxiv 2602.11988 (AGENTS.md failure modes) cited by a commenter, not fetched: OWED.
- JSON-door closure re-confirmed with three distinct clients this sitting; the sibling
  Anubis-HTML path (325 KB shells) also yields nothing parseable.
