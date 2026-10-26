# SWEEP: swarm-orchestration via reddit - 2026-10-02

Stamp: source-fetched: 2026-10-02. Seat: sweep-swarm-orchestration-reddit (workflow actor 3).
Area: swarm-orchestration via reddit. Feeds: width/max-concurrency envelope laws (AGENTS.md),
workflow-gate interagent pass-off + steering (tools/workflow_gate.py), owed consensus-decode
redesign (watch/inbox/frontier_olm_2026-10-02/lens/laws.md:54).

## Door report (degraded, in order tried)

1. Recipe door `https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` (and r/MachineLearning,
   r/LocalLLM, r/ollama, all four in parallel): returned only Reddit's "Welcome to Reddit" shell -
   old.reddit is now login-walled ("Log in to use old Reddit", accounts required). DEGRADED.
2. `old.reddit.com .../.json` and comment URLs via web_reader: same login wall. DEGRADED.
3. `www.reddit.com/.../top.json` via WebFetch: HTTP 403 Blocked (Retry-After: 0), both subreddits tried. DEGRADED.
4. `www.reddit.com` thread HTML via WebFetch: content-free shell ("Reddit"); via web_reader: 500 network error. DEGRADED.
5. `r.jina.ai` proxy: upstream Reddit 403 "blocked by network security". DEGRADED.
6. `api.pullpush.io/reddit/search/submission/?ids=t3_1w7kgzl`: reachable, but `"data": []` - no
   recent-ID coverage. DEGRADED (archive lag).
7. WebSearch `site:reddit.com` fallback (per recipe): WORKED, with two transient 1302 rate-limit
   storms of its own mid-sweep (retry recovered both times - same 1302 signature the estate's
   envelope laws bank).
8. Final working byte door: redlib mirror `https://safereddit.com/r/<sub>/comments/<id>` and
   `https://safereddit.com/r/<sub>/top/?t=month`. This delivered full thread bodies, dates, scores,
   and comment threads. `redlib.catsarch.com` 429'd, `rl.bloat.cat` ECONNRESET - safereddit was the
   one stable mirror. All deep reads cite reddit.com canonical URLs; bytes came through the mirror.
   r/MachineLearning/top/?t=month 404'd on the mirror; r/MachineLearning coverage is search-snippet
   only (no ML-subreddit item banked).

## Pass 1 accounting (>=30 in-window candidates considered)

- r/LocalLLaMA top-month listing: 25 posts, all in-window (3d-29d old), read as listing rows.
- r/LocalLLM top-month listing: 25 posts, all in-window (1d-29d), read as listing rows.
- r/ollama top-month listing: 25 posts, all in-window (3d-29d), read as listing rows.
- Search-surfaced thread candidates (8 topic searches): ~20 more items across r/LocalLLaMA,
  r/LocalLLM, r/ollama, r/AI_Agents, r/MachineLearning, r/LangChain, r/learnmachinelearning;
  several rejected as out-of-window by mirror date check (llmdiff Jul 14 '26; best-of-N SOTA 1grgqpb
  older block; Managing the Swarm 1pzv687 older block; quorum-validation 1sbcear and
  confidence-measure 1szn7bu older blocks; llama-swap 429 1ts072f older block - not read, not banked).
- Explicitly considered and REJECTED for the RQs: the Jev-architecture wave, Nvidia/HF acquisition
  news, Qwen4/DeepSeek V4 releases, hardware posts (no consensus/backpressure/tiebreak content).
- Net: 75 in-window listing rows + ~20 search candidates considered; 8 threads deep-read end to end
  (requirement was >=5); 7 banked (llmdiff rejected: Jul 14, outside window).

## Banked items (strongest first), with RQ mapping

### 1. Detecting hallucinations in local models without eating VRAM (1.5B-120B) - r/ollama 1wdasar
Date shown: "21d ago" (approx 2026-09-11). Author u/Otherwise_Nobody_721, 77 upvotes, 93%.
The "Spanda" method: 5 samples at T=0.7, string-normalize into equivalence classes, Shannon entropy
on CPU instead of a DeBERTa NLI cross-encoder. Claims: 7B AUROC 0.706 vs 0.705 for the heavy NLI
model; 27B 0.89 with exact matching dominant (p = 1.89e-28); 120B frontier COLLAPSED to AUROC 0.09
from "Confident Mode Collapse" - identical wrong answers across all 5 runs, and "even heavy NLI
fails here". Commenter: "it only checks consistency of the output not its truthfulness, so that's
why consistent lies... will not be detected."
Verbatim quote: "it only checks consistency of the output not its truthfulness, so that's why consistent lies... will not be detected."
RQ1 DIRECT HIT. This is the consensus-illusion redesign in the wild: agreement computed over
normalized OUTPUT equivalence classes (numbers/text canonicalized, not judge scores), plus the
sharpest warning the estate could want - at the top of the model range, flock agreement is
ANTI-correlated with correctness (identical wrong answers). Verifies the estate's 0/3-agreed-with-
strength-0.60 result scales in both directions. CAVEAT: thread has marketing tone, commenter-noted
numeric inconsistencies (760ns vs 1.3µs), single-author claims unverified.
Overlap: "semantic entropy" and "mode collapse" both already present in
memory/percolator/explore_deepseek_drain.jsonl (the estate's percolator frames semantic entropy as
a low-cost fleet probe) - term-level prior art, no finding-level duplicate. No title match in
catalog.jsonl. Genuinely new: the string-class AUROC numbers and the 120B failure mode.

### 2. After eight months of running a multi agent setup, the thing that actually mattered was the message bus, not the agents - r/AI_Agents 1vt8088
Date shown: Aug 20 '26 (absolute). Author u/__hymn, 14 upvotes, 54 comments. NOTE: 13 days OUTSIDE
the strict 30-day candidate window; retained because it is the strongest RQ3 hit found anywhere in
the sweep - flagged, not hidden.
Verbatim quote: "The authority is not an agent. It is the receipt."
Also banked lines: "Loud and stuck beats quiet and wrong."; "That single rule killed an entire class
of silent corruption." (the rule: disagreements escalate to the human, never self-arbitrate);
envelopes report only what already happened and must point to something externally checkable
("Not 'the conversion is complete' but 'Ballad_11_v2.md, 10547 bytes'"); "notes that loop" failure
mode (entries summarizing prior entries) fixed by requiring each entry carry a fact not in the
previous one.
RQ3 DIRECT HIT (Cathedral World tiebreak class): the field's answer to two strong families holding
contested verdicts is NOT a stronger judge - it is record-both-and-stop, human escalation, and
receipt-based arbitration. Comment u/Rox-onfire: "'Delivered' is three facts, not one"; recording-
both-and-stopping "is discipline, not cowardice."
RQ1 second leg: every claim must anchor to a checkable artifact - agreement over receipts, not over
opinions.
Overlap: no matches for "message bus, not the agents" / "Loud and stuck" / "quietly wrong and
completely consistent" / "The authority is not an agent" anywhere in catalog/ or memory/. Genuinely new.

### 3. Agent swarm coordination - r/LocalLLaMA 1wu3rio
Date shown: "2d ago" (approx 2026-09-30). Author u/bolche17, 6 upvotes, 22 comments.
Verbatim quote: "An agent 'swarm' is just hype at this point. What you need is handful (at most) of carefully coordinated agents."
Other load-bearing comments: "The more agents you got running in a swarm, the greater the model
drift risk" (9 pts); pass plan/diff/logs, not chat history; cap iterations and always compare
against a single-model baseline (5 pts); u/Salt_Hyena5896's "boring protocol": task queue with
explicit states, lease/heartbeat claiming, cloud model reserved for planning/review, plus a
max-hop/dead-letter path to prevent infinite loops; shared-markdown-folder coordination with
open/claimed/done/failed states and a note that cross-machine sync breaks atomicity.
RQ2 DIRECT HIT: lease/heartbeat + max-hop dead-letter is the admission/retry-cap discipline AIMD
lacks - AIMD paces sends, the dead-letter cap BOUNDS retry loops. Extends the banked HiveMind
72-100% vs 0-18% result with practitioner shape rather than contradicting it. No measured
contradicting data found on Reddit.
RQ4 second leg: community prior is explicitly "handful coordinated beats wide swarm," with a
single-model baseline as the required control - the exact experimental design the estate's
small-collectives question needs.
Overlap: "dead-letter" hits in memory/corpus/ractors/esoterica are postal dead-letters in Gutenberg
fiction, not queueing - no real overlap. No title match. Genuinely new.

### 4. 400+ LLM agents living in a 2004-era MMO server, all local on Qwen3-4B - r/ollama 1wt0tot
Date shown: "3d ago" (approx 2026-09-29). Author u/kristiantalley679, 251 upvotes, 97%, 35 comments.
Architecture: Qwen3-4B Q4_K_M 4k-ctx runs the main agent loop for 400+ agents; a 27B model handles
rich one-on-one interactions; 2x RTX 3090, q8_0 KV cache, MTP speculative decoding, ~2.5s avg/call.
Verbatim quote: "low-priority reflections get shed so chat stays responsive."
RQ2 DIRECT HIT: priority-shedding admission control deployed in anger - when queues back up, drop
the low-priority class (reflections) to protect the interactive class (chat). This is a second
mechanism beyond AIMD pacing and beyond dead-letter caps: class-based shedding by consequence.
RQ4 DIRECT HIT: measured-in-production small-collective beat: a 4B workhorse herd plus a 27B
specialist reserved for high-stakes dyads - the estate's janitor/specialist tier ladder exactly.
Stack disclosed as CMaNGOS mangos-classic + cmangos/playerbots + author's own mod-llm-bridge,
GPL-2.0 NOTICE added after a credit callout.
Overlap: STRONG terrain overlap - "playerbots" appears hundreds of times in catalog/catalog.jsonl
and the estate holds memory/continuity/seat_memory_20260927/hermes-wow-bones-azerothcore-20260916.md
(AzerothCore WoW bones). The estate already holds the MMO-bot terrain; what is NEW here is the
4B-herd/27B-dyad split and the reflection-shedding line. Thread title itself not in catalog.

### 5. I ran those benchmarks we all see on YouTube locally - r/LocalLLaMA 1vu8atq
Date shown: Aug 21 '26 (absolute). Author u/on_line187, 0 net score (23% upvoted, 5 comments) -
low-karma but maximally instrumented post. NOTE: 10 days OUTSIDE the strict 30-day window;
retained for RQ1, flagged.
Verbatim quote: "executed unit tests for code, sympy equivalence for maths, no LLM judge anywhere."
Qwen 3.8 27B Q8_0, 2,483 items, 9.1h: GSM8K 96.7%, MATH-500 86.4%, HumanEval 95.5% ±1.6, MBPP 80.0%.
Grading mapped onto the OUTPUT SPACE mechanically - unit tests and sympy equivalence, zero judge
models. Reasoning-stall split: GSM8K 98.1% when reasoning completed vs 52.4% when it burned the
token budget with no answer; MATH-500 94.3% vs 6.7% ("On MATH-500 this single defect costs about 8
points"); stalls ate 60 of GSM8K's 245 minutes. Contamination probing via prefix-continuation
similarity (HumanEval softest: +0.307 over no-memorization floor). HumanEval run-to-run noise at
temp 0.2: 94.5 / 97.6 / 94.5 - "If you see two models a point apart on HumanEval, that difference
is probably nothing."
RQ1 DIRECT HIT: two designs the consensus-decode redesign can steal outright - (a) verification as
execution (tests/sympy) instead of scoring; (b) TERMINATION as a gating feature: an answer emitted
after a reasoning stall is a different output class and must be scored separately or discarded.
RQ4 second leg: the noise numbers set the resolution floor any flock-vs-single comparison must
clear (a 1-point HumanEval delta is nothing).
Overlap: no matches for "no LLM judge anywhere" / "reasoning stalls" / "reasoning_content" in
catalog/ or memory/ beyond noise (catalog matches were other rows). No title match. Genuinely new.

### 6. Parallel vs Sequential Agent Systems (Research links inside) - r/LocalLLaMA 1w7kgzl
Date shown: "posted 27 days ago" (approx 2026-09-05). Author u/PilgrimofHaqq2, 5 upvotes, 64%, 6 comments.
Verbatim quote: "all parallel workers tend to fall into the exact same attractor basin."
Post synthesizes: Anthropic multi-agent research 90.2% vs single agent at ~15x token cost; a Nature
Machine Intelligence study of 260 configurations where every multi-agent variant made coding worse
(-1.3% to -12.8% on SWE-bench Verified) with error amplification 17.2x; Berkeley MAST 41-86.7%
failure rates; Cognition "Don't Build Multi-Agents"; Princeton "AI Agents That Matter" ~100x cost.
TL;DR: "Use parallel agents when the work is read-heavy and splits into independent slices...
Use one sequential agent when the work is a single chain of decisions." Top comment (7 pts) on the
thread's subject: "Bot to bot posting and communicating."
RQ4 DIRECT HIT: the measured ledger the estate's small-vs-large question must clear - parallel
flocks LOSE on write-heavy chains (correlated errors: same attractor basin), WIN on read-heavy
slices; and the strongest comment in-thread: "Majority voting can crown a shared hallucination"
(verifying via deterministic tools, not LLM votes).
RQ1 third leg: correlated-error proof that vote-counting over models sharing one prior is not
verification.
Overlap: no matches for "Parallel vs Sequential Agent Systems" / "error amplification 17.2" /
"attractor basin" phrase-set in catalog/ or memory/ (attractor language exists in estate prose but
the -1.3%/-12.8%/17.2x study does not). No title match. Genuinely new.

### 7. I stopped using the smartest AI models. Programming got faster and cheaper. - r/ollama 1wjnkgm
Date shown: "14d ago" (approx 2026-09-18). Author u/ievkz, 155 upvotes, 88%, 40 comments.
Verbatim quote: "models are already good. Harness is not."
Cost-per-task: GPT-5.6 Luna at $0.18/task vs GPT-6 Astra $3.26 ("That is a difference of almost 20
times") with Luna only 2 AA-index points below; speed as the new bottleneck (DeepSeek-V4.1-Flash at
300 tok/s vs 25-50 typical); harness token bloat: a simple "hi" costs ~3,000 tokens in Pi, ~18,000
in Codex, ~30,000 in Claude Code; "Eighty percent of its work... figuring out what is going on all
over again" from context resets. Comment u/MarcelloT254k: "plan with frontier, execute with
something smaller." Top comment (19 pts, 20-year programmer on local Qwen3.8-27B): verifies only
critical parts, predicts the work shifts to "building validation frameworks, safety nets, testing
constraints".
RQ4 supporting hit: the routing rule (cheap workhorse + frontier plan/review only) with cost
numbers; also names verification-as-the-job - consistent with the estate's driving ladder and
descent protocol.
Overlap: no matches for "cost per Task" phrase or title in catalog/ or memory/. Genuinely new.

## RQ synthesis

- RQ1 (consensus mapped onto the actual output space): three independent in-window/near-window
  threads converge on the same design the estate owes: measure agreement over canonicalized OUTPUTS
  (string/number equivalence classes, sympy, unit tests), never over judge scores; gate on
  termination (stalled reasoning = different output class); and treat flock-unanimity at the top
  model range as an alarm (120B confident mode collapse, AUROC 0.09), not a pass. The estate's
  percolator already holds "semantic entropy" as a concept - the new bytes are the implementation
  numbers and the failure mode.
- RQ2 (backpressure/admission control vs AIMD): two practitioner mechanisms extend rather than
  contradict the banked HiveMind result: (a) class-based priority shedding (drop reflections, keep
  chat) and (b) bounded retry via max-hop/dead-letter paths on leased task queues. No measured
  contradicting evidence surfaced. The search backend's own 1302 storms during this sweep
  re-confirmed the estate's rolling-throughput envelope law from the outside.
- RQ3 (tiebreak between strong families): the only serious answer found is process, not model:
  record-both-and-stop, human escalation as a hard rule, receipts as the arbiter ("The authority is
  not an agent. It is the receipt."). No frontier automatic-tiebreak design surfaced on Reddit.
- RQ4 (small collectives vs single large): measured evidence says the axis is TASK SHAPE: parallel
  slices (read-heavy) reward herds (400+ agents on a 4B; research/review fan-out), single
  decision-chains (write-heavy coding) punish them (every multi-agent variant worse by -1.3% to
  -12.8%, error amplification 17.2x, at up to 15x cost). Any flock-vs-single trial must clear the
  measured noise floor (HumanEval 1-point deltas are nothing) and run a single-model baseline arm.

## OWED / not found (stated plainly)

- NO post-10-01 consensus or verification design surfaced anywhere in the Reddit candidate pool:
  nothing relevant dated after 2026-10-01 was found (newest banked: approx 2026-09-30). RQ1's
  "post-10-01" slice is empty from this door; nearest evidence is mid-September.
- No Reddit-carried MEASURED benchmark of small-collective vs single-large on orchestration tasks
  was found beyond the practitioner claims and the 260-config coding study relayed in item 6
  (relayed numbers not independently pulled from the underlying papers - OWED if the estate wants
  paper-grade citations).
- r/MachineLearning top-month could not be read through any door (mirror 404, JSON 403) - an
  academic-lens sweep of that subreddit remains OWED.
- Spanda's claimed numbers are single-author, marketing-toned, with commenter-flagged internal
  inconsistencies (760ns vs 1.3µs) - treat as leads, not law, until the substack/GitHub is read
  (OWED deep read: liquidngas.substack.com, github.com/nayakbhupen/Spnda).
- llama-swap concurrencyLimit-429 thread (1ts072f) surfaced by search but is from an older ID block;
  not read, not banked; its one snippet fact (HTTP 429 when queue exceeds concurrencyLimit) is
  snippet-level only.

## Method receipts

- Doors tried and their exact failures listed above; working doors: WebSearch site:reddit.com
  (8 searches run) + safereddit.com redlib mirror (11 fetches: 3 top-month listings + 8 thread
  reads, minus 2 mirror failures logged in the door report).
- Deep reads completed end to end (8): 1w7kgzl, 1vt8088, 1vu8atq, 1wdasar, 1wt0tot, 1wu3rio,
  1wjnkgm, 1uwap9h (last one rejected as out-of-window). Requirement >=5: PASSED.
- Overlap greps run via rg against C:/Users/foste/Documents/projects/local_sovereign_agent/catalog/
  (catalog.jsonl, tags.jsonl) and C:/Users/foste/Documents/projects/local_sovereign_agent/memory/:
  title-phrase greps for all 7 banked items returned zero catalog hits; phrase-level hits found and
  disclosed above (semantic entropy + mode collapse in memory/percolator/explore_deepseek_drain.jsonl;
  playerbots in catalog.jsonl; dead-letter in Gutenberg fiction).
- Quotes are relayed through the mirror + fetch-summarizer chain (no raw-byte Reddit access exists
  from this seat); confidence per item reflects that relay. Relative dates ("21d ago") converted
  against today 2026-10-02 and marked approx.
