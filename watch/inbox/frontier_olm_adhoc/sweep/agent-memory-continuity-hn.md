# Frontier sweep: agent-memory-continuity via Hacker News

source-fetched: adhoc
area: agent-memory-continuity
seat: sweep-agent-memory-continuity-hn (dwfrun, second pass)
moment: 2026-10-11 (HN Algolia door)

This file supersedes the 2026-10-10 sweep at this path. The 10-10 seat's 8 banked items
(funes/dacorvo recall-vs-compaction, motif, Singularity, calpaterson memoryfields,
codepointer four-systems, OKF agent-memory, StructMemEval, galahad-kv 2610.10845) remain
HELD and are not re-banked here; this pass banks only signal that is new against that set,
against the 10-04 agent-memory-and-continuity family (which held liao.gg 49945933 with a
163-comment tree read, SuperLocalMemory 2608.08253, Strata, copeca via the Novgraph
thread, cognee guide, post-graph-rag keys 09-30, routine-cleanup, boolean.ai), and
against the 10-06 Zep/Hindsight comparison capture.

## Door health

HN Algolia API clean on all 8 queries (search_by_date, created_at_i>1789084800 = 2026-09-11
onward; zero 403s, zero degradations). news.ycombinator.com item pages fetched clean:
49783133 (Mini-AGI, 80-comment thread) and 49993820 (claix, 10-comment thread). GitHub
READMEs (IHMT-MEMORY, SelMem), arxiv abstract (2502.12110), two vendor pages (claix.dev,
groundtrack.dev) and one blog (redreamality.com) all fetched clean. All quotes below are
verbatim as relayed by the fetch summarizer, hence confidence below 1.0 on every item.

## Pass 1 (broad sweep)

Queries run: "agent memory", "LLM memory", "knowledge graph memory", "vector RAG
retrieval", "graph RAG", "agent context engineering", "continual learning agent",
"agent memory benchmark". Roughly 150 raw hits; 35+ distinct in-window on-topic
candidates considered. Held or duplicate and excluded: liao.gg 49945933 (HELD 10-04 with
tree read at 163 comments; thread now shows 311 comments, delta not chased, no re-bank),
SuperLocalMemory 49950478 (HELD), Hindsight 49963587 (HELD via Zep comparison 10-06),
post-graph-rag 49743385 (keys HELD 09-30 per the 10-04 file), Novgraph 49672213/49745176
(thread mined by 10-04 for copeca), cognee guide (HELD), Aura 50010250 (read-not-banked
by 10-04), galahad 50018178 (banked by 10-10), Singularity 50004683 (banked by 10-10),
Slowave/Recalld/Memdebug/Tinyhat (cut by 10-10 as low-signal; Memdebug's memory
diff/undo would instrument the why_context drop but re-raising yesterday's cut without
new evidence is re-banking waste).

Below cut this pass, with reasons: claix.dev agentic-retrieval 49993820 (read end to
end: zero benchmarks anywhere in the post; thread's own readers flag it, see Pass 2);
Groundtrack 49908550 (read end to end: zero numbers, no integration detail, pure
marketing shape); Make0 49713789, Nexusyn 49935994, IngotDB 49878337, Past.dev 49967073
(vendor or 1-pt Show HNs, no measured claims); "Do coding agents need memory or
documentation?" 49976848 (echo of HELD liao.gg); "Agents Don't Need Another Memory API"
49996093 (medium paywalled, untested); "Ask HN: embeddings only retrieval?" 49685838
(2 comments, thin).

## Pass 2 (deep reads, 8 fetched and read end to end)

Mini-AGI thread 49783133 (80 comments, read via item page); claix.dev agentic-retrieval
post; claix HN thread 49993820 (all 10 comments); IHMT-MEMORY README; Groundtrack page;
CTWM post (redreamality.com, full); SelMem README; A-Mem arxiv abstract 2502.12110.

## Overlap checks (commands run this session)

grep -i -c over catalog/catalog.jsonl per phrase: A-Mem 0, "Agentic Memory" 0, 2502.12110
0, Mini-AGI 0, IHMT 0, CTWM 0 (searched as part of the pattern battery), SuperLocalMemory
1 (the HELD 10-04 fetch), Novgraph 0, claix 0, Groundtrack 0, SelMem 0, Nexusyn 0,
Memdebug 0, Slowave 0, Recalld 0, post-graph-rag 0. Known-set confirmation: MemCodex 1,
letta 1126, MemGPT 44 (the banked set lives in corpus folds and mined repos, not the
catalog title field). Full recursive grep over memory/ for the same battery matched 31
files; attribution pass showed every match is a substring false positive: "a-mem" inside
"cia-memo" and "letta-memrepo", "Hindsight" the plain English word. Zero real hits for
any banked item. The adhoc sibling files (agent-memory-continuity-arxiv/reddit/x.md) and
the 10-04 family files were grepped: A-Mem appears only as a LoCoMo baseline mention
(agent-memory-continuity-arxiv.md:43, "+10.1pp over A-Mem"), never banked as a design.

## RQ1 answered from repo evidence this session (the OWED settles)

The graph builder is mag/knowledge_graph.py: build() at mag/knowledge_graph.py:602
regenerates the whole graph and GRAPH_PATH.write_text at mag/knowledge_graph.py:621
overwrites memory/knowledge_graph.json. The 117 why_context edges were manual appends
by tools/graph_heal.py (HEAL_REL = "why_context" at tools/graph_heal.py:55), and the
builder's own receipt comment records the wipe measurement: "a rebuild wipes manual edges
(measured 2026-10-07 on a copy: 117 why_context edges -> 0 after build())"
(mag/knowledge_graph.py:231-236). The survival cure already exists in the same file as
precedent: the m6 supersession wire derives its superseded_by edges from a durable
register (memory/fold_history/SUPERSEDED.md) inside the builder's edge branch, "so
supersession survives the weave's own rebuild" (mag/knowledge_graph.py:234-236, the
maps_to precedent). Law: authored cross-links survive regeneration only when minted from
a durable source file the builder reads on every build; appending edges to the JSON is
raking leaves. Public-side corroboration: IHMT-MEMORY implements the identical split
(rebuild discards derived branches/catalog only, never leaf content; leaf ids derive
from content so re-ingest rewrites rather than duplicates; superseded values marked
OUTDATED/HISTORICAL with superseded_by links).

## RQ2 (verkle coherence vs vector embedding)

"On the estate's own seat tapes" is a measurement only this estate can run; no public
source answers it (OWED, unchanged). What the window adds is three zero-vector retrieval
designs with numbers plus one falsification discipline: IHMT-MEMORY navigates a tree with
BM25 beam descent (beam 3, cost beam x log_B(n)), stdlib-only, claiming 200-900 tokens
per retrieval from 50 to 50,000 entries, and measured 1,071 vs 3,613 tokens on an
8-question 55-file benchmark; CTWM allocates context by rank under a power-law budget and
measured -24.48 percent tokens on LongMemEval at accuracy parity, while honestly naming a
multi-session recall loss; held motif already banked FTS5+graph at 1186x smaller than
full history. CTWM's random-walk audit (0 percent pure-power-law pass across 54 cells;
retrieval-off drops Gini 0.698 to 0.29-0.35) is the caution that concentration-shaped
retrieval claims can be artifacts of top-k itself, exactly the class of check a verkle-
vs-vector verdict on seat tapes needs. Build cost side: IHMT is zero-dependency (no
embedding model to host), CTWM is a no-retrain layer with one knob. The claix thread's
strongest technical comment warns the anti-vector argument usually fights a strawman:
"We dropped that well over a year ago IIRC... agentic search has pretty much become the
default" (cmenge, thread 49993820).

## RQ3 (ten-minute-self falsifiers, laws.md:97)

Estate falsifiers are ours to fire; no public source runs them (OWED, unchanged). The
window supplies two instrument classes worth stealing for the runs: Mini-AGI is the
weights-tier mechanism candidate (pitfall-bypass corpus compressed into weights), and its
thread is a replication cautionary tale: an independent replicator (jmatthews) found the
effect held "only after controlling for step density" and attributed it to the known
"learn less forget less" result, i.e., a JIT fold must control exposure density before
claiming compounding, or it is distillation wearing a clock (the rib's own words for
falsifier 2). SelMem is the behavioral-divergence instrument class: its fork experiment
measured d_beh 0.80 with the book split vs 0 for all baselines (no sleep, null, last-8,
full log) over 360 days, with negative results kept in the README; that is the same
experimental shape as "fold beats prompt-only on held-out pitfalls," run long-horizon.

## RQ4 (40-day-stale fold, burns.md:151-153)

mine_recon 2026-10-11 05:19 flagged last_fold 2026-08-31; whether the fold cures recall
is estate-internal and unfired (OWED). Public-side note only: the fold-time retrieval
design choice and the RQ2 verkle-vs-vector choice are now the same decision, and the
three zero-vector designs above are the candidate shapes to fold into.

## RQ5 (published designs beyond MemCodex/TAGGRAPH/mem0/EMIR2)

Banked: A-Mem (NeurIPS 2025 submission v11; Zettelkasten note network where every memory
becomes a note carrying structured attributes and links that evolve as new memories
arrive; evidence-bearing by construction rather than name nodes), SelMem (sealed source
evidence the model never reads, with gists/affect/axioms as the recall surface),
IHMT-MEMORY (leaves carry id/timestamp/tags/parent_id/checksum/span headers; superseded
facts get timeline status instead of deletion), CTWM (per-node visit histograms and
bottom-half tail error logged beside tokens, making outcome evidence a first-class
field). Common pattern against graph.md:17-19: all four fill we_have/evidence/banked as
FIELDS derived from durable registers on existing nodes, which is the same shape as the
in-repo supersession-wire precedent (mag/knowledge_graph.py:234-236); none adds degree-0
name nodes.

## Banked items (strongest first, also in the JSON result)

1. Mini-AGI, dynamic continual learning on 8GB VRAM (HN 49783133, 2026-09-21, 277 pts,
   80 comments; github.com/volotat/mini-AGI). MoE with dynamically added/pruned experts,
   batch-1 single-stream training, LR asymmetry (slow trunk, fast experts) as the
   anti-forgetting mechanism; thread carries independent replication, the
   stability-plasticity objection (synctext), and the chess-samples teardown (seanhunter).
2. IHMT-MEMORY, long-term memory for AI coding agents as a tree of plain files
   (HN 50038733, 2026-10-11; github.com/gonzaroman/IHMT-MEMORY). Regeneration-safe by
   design: rebuild discards derived state only, never leaves; BM25 beam descent, zero
   vectors, zero dependencies; measured token costs plus an honest counter-benchmark
   (headless Claude never called the tools; forcing them cost 42-71 percent more).
3. CTWM, heavy-tailed memory traces in long-horizon agents (HN 49955466, 2026-10-04;
   redreamality.com). Rank-based power-law context budget, tail summarized not deleted;
   Graph World -5.9 percent tokens and -13.6 percent tail error, LongMemEval -24.48
   percent tokens at parity, multi-session recall weakness named; random-walk artifact
   audit separates retrieval artifacts from semantic concentration.
4. SelMem, selective reconstructive memory for LLMs (HN 49840484, 2026-09-25;
   github.com/jbsalles/Selmem). Path-dependent memory: gate/reconstruct/sleep loop,
   sealed archive, 360-day divergence experiment with baselines pinned at 0 and negative
   LoCoMo/LongMemEval results kept in the README.
5. A-Mem, agentic memory for LLM agents (arxiv 2502.12110, NeurIPS 2025 submission v11;
   HN 49877747, 2026-09-28). Zettelkasten-style note network with agent-driven link
   evolution; abstract-level numbers only ("six foundation models"), and the estate
   already holds a paper beating it by 10.1pp on LoCoMo, so it banks as design prior
   art for RQ5, not as a SOTA claim.

Nothing banked that this seat did not read itself; the two vendor pages read (claix,
Groundtrack) are recorded below-cut with their zero-measurement status stated.
