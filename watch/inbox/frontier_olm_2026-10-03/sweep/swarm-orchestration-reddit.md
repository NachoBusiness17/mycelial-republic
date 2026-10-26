# sweep: swarm-orchestration via reddit - 2026-10-03

Lane: sweep-swarm-orchestration-reddit (frontier_olm 2026-10-03)
Questions: (Q1) documented/measured concurrency+retry envelopes for subagent fan-out vs the estate's near-3 workflow-children (maxAttempts 0) vs Task-agents-clean-at-10-12 split; (Q2) backoff doctrine for 429/1302-class provider storms; (Q3) decentralized mesh coordination with measured handoff-quality numbers; (Q4) incremental salvage of partial agent work (report()-salvage shape).

## Door status (degraded, no fabrication)

- Recipe door `old.reddit.com/r/*/top.json?t=month&limit=50` (LocalLLaMA, MachineLearning, LocalLLM, ollama): all four returned an empty "Welcome to Reddit" shell, no JSON. HTML variant of r/LocalLLaMA/top: same shell. **Degraded.**
- `www.reddit.com/...json` via WebFetch: HTTP 403 Blocked. curl with browser UA: HTTP 302, 0 bytes. web_reader on old.reddit.com: "Log in to use old Reddit". **Degraded.**
- Fallback (per recipe): WebSearch site:reddit.com - worked, but the search backend itself threw `MCP error -429 code 1302 Rate limit reached` repeatedly mid-query (first-hand storm evidence for Q2; receipts in the session log).
- Working read doors found this session: (a) `web_reader` on `www.reddit.com` thread pages; (b) **Arctic Shift public Reddit archive API** (`arctic-shift.photon-reddit.com/api`) - full post JSON with created_utc/score/selftext plus comment trees. All 8 banked items were fetched through the archive API (post selftext + top-scored comments) and the JSON is retained byte-backing in `sweep/tmp/` (candidates_full.jsonl, comments_<id>.json, post_1w950fw.json).

## Pass 1 (broad sweep, last 30 days)

Full-window crawl of 13 subreddits (LocalLLaMA, ClaudeAI, ClaudeCode, AI_Agents, aiagents, LLMDevs, LocalLLM, ollama, claudeskills, LangChain, Anthropic, cursor, codex), 2026-09-03..2026-10-04, sort=asc with cursor pagination: **1,017 posts in-window candidates collected** (raw: sweep/tmp/candidates_full.jsonl); keyword pool 1,754; strict title-strong pool **204** (ranked by score+5*comments). Far over the 30-candidate floor; the strongest 30 were considered explicitly in the ranked print, 8 taken to deep read.

## Pass 2 (deep reads, end to end) - 8 items, strongest first

### 1. How many agents can 2x4090 actually run at once? Three weeks of llama.cpp concurrency data - soft cap 5 @ 64k, hard cap 9, and why
r/LocalLLaMA · 2026-09-08 · https://www.reddit.com/comments/1wb35xo/ · score 15, 20 comments
Read: full selftext (10,691 chars) + 23 comments.
> "aggregate prefill throughput is constant at roughly 1,500 tokens/second regardless of slot count. The box has one prefill budget. Slots divide it; they do not multiply it."

Measured table: 3 agents @64k = 1.54 completions/min, 112s median wait; 5 agents = 1.63/min, 168s; 9 agents = 1.52/min, 330s. "Tripling the agents changed total throughput by 6% and tripled the wait." Soft cap 5 (latency trade), hard cap 9 (VRAM arithmetic, every config within 3.5 GiB of 44.6 GiB). Accuracy tie-at-ceiling across Q4/Q6/Q8 up to 251,557 tokens, zero cross-slot leakage. Comments add the mechanism: the soft cap is KV-cache pressure starving agent contexts (u/Future_AGI), pin each agent to a fixed context budget, prefill is compute-saturated GEMMs, and slot rotation kills prefix-cache reuse (u/Firm-Luck2062). Workload caveat stated by the author: prefill-heavy agent prompts batch badly; decode-heavy would scale better.
Estate read (Q1, local lane): the strongest independent corroboration of the fan-out width law's mechanism - a width cap is a *shared server budget* (one prefill pipe; VRAM), so the estate's near-3 workflow-children cap and the 10-12 Task width are two points on one budget curve, not two truths. Also hands the local janitor lane an operating point: ~5 agents @64k before wait explodes.

### 2. I tested an end-to-end continuity layer across 205 agent runs. The hard part wasn't checkpointing. It was proving whether the external side effect had already happened.
r/LLMDevs · 2026-09-14 · https://www.reddit.com/comments/1wg442g/ · score 4, 9 comments (author-disclosed product: "Infra", MIT integration layer; repo github.com/caelancarmer/infra named in comments)
Read: full selftext (3,322 chars) + 10 comments.
> "Before retrying an uncertain action, it attempts to reconcile the local state with evidence from the external system."

Measured numbers (205 published sanitized runs): 25 high-risk continuation runs - Infra 5/5 vs "Strong Handoff" 4/5, 49.4% fewer tokens, 60.8% faster recovery; 60 matched runs all 20/20 with Native cheapest; 30 effect-safety runs blocked 10/10 injected duplicate external effects; 90 verified-experience runs: 64.5% fewer tokens than raw history but 2.0% costlier than cold start and won only 1/6 cells - "experience should be routed selectively, not inserted into every continuation." Comments converge on: two proofs at takeover (what objectively happened + is the successor still authorized), UNKNOWN fails closed, persist intent+idempotency key before dispatch, "Checkpoint replay without reconciliation preserves the uncertainty instead of resolving it."
Estate read (Q4 + Q2): the only measured handoff-quality numbers found in the window. It is the citation-resolution law in agent form - salvage requires evidence receipts, and salvage-by-summary is a fabrication risk. Direct input for the report()-salvage gate: salvage must carry effect status + authority validity, else fail closed.

### 3. AI agents can double-charge customers on a simple retry, and "just add a checkpoint" doesn't fully fix it
r/AI_Agents · 2026-09-03 · https://www.reddit.com/comments/1w6gg8v/ · score 5, 14 comments (cites open crewAI issue #5802)
Read: full selftext (1,315 chars) + 14 comments.
> "A key just makes a retry harmless, it doesn't tell you what happened. Evidence does."

Selftext: agent loops re-fire side-effecting tools after timeout because the agent can't know the first attempt landed; a checkpoint written after the action leaves a crash window where the effect exists but nothing records it. Comments: exit-code lies ("sometimes it doesn't think it failed, it thinks it succeeded... that's so much worse"); UNKNOWN must be a first-class retry state; idempotency key generated from the *intent* (task id + action), not the generated call text, or model rephrasing on retry defeats dedupe; enforcement via pre-hook (no side effect runs without a committed key).
Estate read (Q2): the missing piece in backoff doctrine - backoff schedules assume failure is known; provider storms produce *unknowns*. The estate's tri-state + receipt laws already encode this; this thread is independent confirmation plus the intent-derived-key refinement.

### 4. LangGraph vs CrewAI for multi-agent handoffs: which handles context and communication better?
r/LangChain · 2026-09-21 · https://www.reddit.com/comments/1wmafge/ · score 22, 17 comments
Read: full selftext (1,344 chars) + 20 comments.
> "the side effect does not get rolled back for you, which is what bit a ~12-node run when we marked done before the receipt landed"

Practitioner consensus: "keep autonomy inside the nodes and make the edges deterministic" (top comment, S=8); LangGraph re-enters a node from its old checkpoint so a resumed agent re-writes unless an idempotency check precedes the write; the idempotency key must commit in the same transaction as the write; run_id+node_id doubles as the trace tag answering which agent produced what without replay. CrewAI handoffs described as "handing off a Slack thread" (everyone scrolls the whole history) vs LangGraph as "a lab notebook with a sign-out sheet - you can re-enter at step 3 without replaying the whole show." The selftext names the handoff-quality axes: preserve decisions/constraints, pass only relevant context, retry one agent without restarting the chain, per-agent attribution.
Estate read (Q3): qualitative but convergent handoff-quality doctrine - deterministic edges + typed payloads + checkpoint re-entry is exactly the estate's rib_bus pass-off + trail.jsonl shape. No measured numbers here; the measured numbers live in item 2.

### 5. How I use sub-agents without burning through Fable 5.1
r/ClaudeCode · 2026-09-09 · https://www.reddit.com/comments/1wbc03f/ · score 339, 109 comments
Read: full selftext (1,397 chars) + 100 comments.
> "Fable is my orchestrator, not my worker."

Fan-out economics: premium model plans and runs agents and integrates; Haiku scouts (locations only, never file contents), Sonnet reads/builds, Opus refutes (independently reruns tests) and debugs; every sub-agent gets a specific goal, exact files/scope, and what to verify. Author sits at ~90% weekly quota with the split. Comments quantify the counter-case: sub-agent starts inflated to "at least 200k... even latest agent runs was starting with more than 400k" tokens when the orchestrator dumps raw context, which is why one commenter disabled sub-agents entirely.
Estate read (Q1): provider-side envelope - fan-out cost is dominated by orchestrator-to-child context seeding, matching the estate's deliberate-ask "pay the context tax once" and the tier ladder (janitors scout/build, specialists judge).

### 6. New day: new 592 overloaded
r/ClaudeCode · 2026-09-03 · https://www.reddit.com/comments/1w67g8k/ · score 254, 126 comments
Read: post + 100 comments.
> "And once they are back online we all going to pay for cold cache. For Claude going down is basically equal to making more money"

Storm morphology thread: a provider-wide 592/Overloaded day hitting Opus and other models for ~2h, Codex down for some users too. Cost mechanism in comments: warm caches expire mid-storm ("in 30 minutes the cache for my 6 concurrent sessions will clear"), so post-storm work re-pays full prefill and users get "charged for redoing the same work you just did." No backoff parameters documented anywhere in the thread - practitioners just wait.
Estate read (Q2): corroborates that 429/1302-class storms are provider-wide events where the correct client behavior is HOLD (the estate's max-concurrency standing law treats first contact as a hold signal), and names the hidden cost that makes blind retry worse: cold-cache re-prefill after the storm.

### 7. How are you all handling session bloat and state handoff between agents?
r/AI_Agents · 2026-09-09 · https://www.reddit.com/comments/1wbifl0/ · score 8, 43 comments
Read: full selftext (914 chars) + 48 comments.
> "my subagents dont hand over conversation at all, they write a short md file (goal, decisions made, files touched, open questions, what NOT to do) and the next one starts fresh with only that file plus the repo"

Convergent field doctrine: transcript-as-garbage, artifact-as-state; typed handoff packet capped (goal, constraints, open decisions, artifacts, last successful tool results, known failures); "If the packet fails schema validation, refuse the handoff - don't 'summarize harder'"; checkpoint after irreversible or expensive steps, not on a message count; keep the task statement and acceptance criteria outside the rolling summary because summarization rewrites them; stamp handoffs with an id for later grep; demote the raw transcript to fallback storage instead of deleting it.
Estate read (Q4): independent reinvention of the estate's shared-inbox/report()-salvage shape - partial work salvages as a bounded, schema-checked artifact pointer, not as a transcript. The "refuse on schema violation" line is a gate check we already run; the "demote, don't delete" line is worth stealing for warm-state.

### 8. Hermes Bot Mode Tutorial (Agent Teams): Specialized Bots, Group Chats & Essential Settings
r/hermesagent · 2026-09-06 · https://www.reddit.com/comments/1w950fw/ · score 175, 43 comments (video post; body not archived, read via top comments)
Read: post metadata + 46 comments.
> "When I use different agents for different jobs, I usually end up being the one connecting everything. Copying results between chats, explaining what the other agent did, then deciding where the work should go next."

Hermes Pantheon v21.0 "bot mode" moves the coordination burden from the human to group chat + kanban: specialized bots, essential settings, Docker per agent. The counterpoint (S=7) is the mesh-skeptic data point: "one orchestrator agent and kanban does this well already... I have not spoken to another agent in months"; another user runs agent-to-agent chat in task comments because "I asked my agents how they wanted to communicate and that's what they preferred."
Estate read (Q3): the same Hermes family the estate runs is shipping agent-teams/group-chat pass-off, and its own community splits hub-and-spoke vs peer-to-peer with no quality numbers either way. Relevant when Hermes next wakes: kanban+board (rib_bus) remains the contested default against true mesh.

## Cross-cutting verdicts per question

- Q1 (envelopes): no framework publishes a first-class "workflow child maxAttempts=0" shape; the documented envelope is quota/RPM-shaped. Reddit-side corroboration is indirect but physical (item 1: shared budget caps width; item 5: context seeding dominates fan-out cost; Anthropic's own agent-teams announcement of 2026-02-05 warns token usage scales proportionately). Nothing contradicts the estate's split; items 1 and 6 explain *why* narrow-with-retry beats wide-cold.
- Q2 (backoff): Reddit threads in-window document storm morphology and retry *semantics* (items 3, 6), not tuned backoff schedules. Non-reddit corroboration found through the fallback door (marked non-reddit, not banked): Anthropic platform docs (429 carries retry-after header), fast.io 2026-09-16 (60 RPM enforced ~ 1 req/s, so ten concurrent calls in two seconds can trip 429 - matches the estate's burst-sensitivity reading), jev.page 2026-09-24 (exponential backoff on 429/529). The search backend's own 1302 storms during this sweep behaved exactly like the estate's receipt: burst, then 429, then a decay window.
- Q3 (mesh): no in-window reddit result carries measured agent-to-agent handoff-quality numbers; the only measured numbers are item 2's 205-run study. Practitioner default remains orchestrator+board (items 8, 4), i.e. the estate's rib_bus shape, with peer-to-peer as the minority experiment.
- Q4 (salvage): item 2 (evidence-gated continuation), item 7 (typed handoff packet, refuse-on-schema, demote-don't-delete transcripts), item 4 (checkpoint re-entry + idempotent writes). All three converge on the report()-salvage gate: salvage is a bounded, verifiable artifact handoff, never a summary and never the transcript.

## Overlap check (per banking rule)

catalog/catalog.jsonl (917,885 lines): 0 hits on all 14 distinctive phrases. memory/: precise-phrase hits resolve to (a) memory/trajectory/steps.jsonl - this session's own step journal logging my grep commands (self-referential, not prior art), and (b) memory/seals/2026-08-24T*/memory/percolator/invariants.json - a coincidental "aggregate prefill" GPU-economics invariant (8xH100 ~10k-25k tok/s), unrelated subject. No sibling lane has banked any of the 8 threads. Generic terms (handoff packet, double-charge, Pantheon) appear in estate prose naturally and were not treated as overlap.

## Method notes

- Instruments: Arctic Shift posts/search (sort=asc, cursor) + posts/ids + comments/search via venv python urllib; WebSearch fallback; web_reader for live-page confirmation. Raw fetches: sweep/tmp/candidates_full.jsonl (1,017 rows), sweep/tmp/batch1.json, sweep/tmp/comments_<id>.json (8 files), sweep/tmp/post_1w950fw.json.
- Not run: no pytest/census instruments - this ask is a research sweep; nothing was executed against the estate's test surfaces.
- Dates are post created_utc from the archive; scores/comments are archive-moment values, not live.

---

# Window 2 (evening re-fire, same lane, 2026-10-03 ~21:00-22:30)

Evening re-fire of this lane with 5 sharpened research questions: (Q1) which PANDA
fault-tolerant-mesh mechanisms (2609.38482, burns.md:86-87) port to lane_runner's retry
asymmetry (workflow children maxAttempts 0 vs Task agents 11), which contradict; (Q2) what
queue policy prevents the code-1005 quota-wall lane deaths (2 of 8 BUILD-IT-ALL lanes,
burns.md:154-157): DEALS expertise-aware queuing (2609.33768) or the owed limit-kill census;
(Q3) does the 438-redone-vs-8-resumed census replicate over queue/lanes/*/trail.jsonl;
(Q4) which MAS collective-failure diagnosis methods (2609.38761) rib_bus can adopt so a swarm
failure is diagnosed at the mesh, not re-run blind; (Q5) under what measured task classes is a
cheap-seat flock better than one seat, given the consensus-illusion verdict (lens/laws.md:43).
Window 1 above is preserved verbatim; per the lens law (burns.md:86) none of its confirmed
rows are re-banked here, and none of the 8 items below is in window 1 or in burns r1-r23.

## Door status, window 2 (all first-hand this window)

- Recipe doors `old.reddit.com/r/*/top.json`: all four via WebFetch returned Reddit's
  "Welcome to Reddit" HTML shell, zero JSON. curl direct: old.reddit .json 403 "Blocked"
  (1,522-byte block page); www.reddit.com and api.reddit.com 403 with a 189,908-byte block
  page; old.reddit HTML 302/0 bytes. r.jina.ai proxy: 200 but delivers the same Reddit
  "whoa there, pardner" network-policy block. web_reader MCP on old.reddit: same block page.
  redlib mirrors: catsarch HTTP 000, safereddit 200 but a 4.3KB shell with zero post titles,
  perennialte 403, bloat.cat 000. **Degraded**, matching lens/burns.md:107-111 from the
  morning window ("EVERY direct reddit door died... Arctic Shift is the working reddit
  engine. Do not rediscover doors").
- Working door used: **Arctic Shift archive API** (`arctic-shift.photon-reddit.com/api`),
  same as window 1. WebSearch fallback was attempted but the search backend itself threw
  `MCP error -429 code 1302 Rate limit reached` mid-query on two of three tries (same
  1302 signature the estate's receipts document).

## Estate census run this window (the ask's Q2/Q3 probe, executed read-only)

- Event tally over all 13 `queue/lanes/*/trail.jsonl`: CYCLE 3,119 / MONITOR 2,852 /
  CYCLE_FAIL 735 / HEARTBEAT 605, rest smaller; sampled CYCLE_FAIL details are OSError-class
  (builder-cage Errno 22 on runner_state.json, 2026-09-14), and grep finds ZERO rows with
  quota/limit/code-1005 kill semantics anywhere in queue/ - the only "1005" string is
  prose/trail.jsonl 2026-09-07 `census files=9076 stale=1005`, a stale-file count, not the
  quota code. The 1005 quota wall exists in evidence only via commit af9aa05f6's message
  (burns.md:154-157).
- `memory/trajectory/steps.jsonl` (50,716 rows): `trajectory_step.v1` = per-command steps
  (session_id/face/command/result); no agent-lifecycle fields, no death/redo/resume markers.
- `memory/workflows/REGISTRY.jsonl` (63 rows): verdicts PASS 52 / FAIL 11 at gate
  granularity; zero "1005" and no per-child attempt data.
- `queue/lanes/*/runner_state.json`: keys are inbox_offset/last_run/last_result/seat; zero
  attempt/retry keys.

**Census verdict (Q3):** the HN agent-limit census (449 limit-killed subagents, 438 redone
from scratch, 8 resumed and all died again; burns r12) does NOT replicate over the estate's
own trail.jsonl corpus because the estate records NO subagent-granularity death ledger at
all - lane trails are cycle-granularity, steps.jsonl is command-granularity, the registry is
gate-granularity. The re-done-not-resumed fraction is therefore UNMEASURABLE on today's
instruments, not zero. The census stays OWED and needs a writer: workflow-children death
events carrying attempt count plus disposition (redone | resumed | salvage). This also means
(Q2) neither DEALS nor any census can name the preventive shape from estate instruments
today; the practitioner shape below (per-lane fencing) is the only in-window candidate.

## Pass 1, window 2 (broad sweep)

Fresh full-window crawl run by this seat: 14 subreddits (LocalLLaMA, ClaudeCode, ClaudeAI,
AI_Agents, aiagents, LLMDevs, LocalLLM, ollama, claudeskills, LangChain, Anthropic, cursor,
codex, hermesagent), 2026-09-03..2026-10-05, cursor pagination: **24,367 posts fetched,
1,677 keyword hits** against a 48-keyword pool mapped to the five questions; the ranked
top-60 were considered explicitly (raw: `sweep/tmp/sw2_full.jsonl`, tool `sw2_crawl.py`).
Far over the 30-candidate floor. 8 taken to deep read; window-1 ids are tagged in the pool
and none was re-taken. Two pagination defects were paid for en route and are recorded in
`sw2_crawl.py` comments: the API 400s on a duplicate `before` param (page 2 sent the window
edge AND the cursor), and the cursor must advance to the batch's newest row (default sort is
newest-first).

## Pass 2, window 2 (deep reads, end to end) - 8 items, strongest first

### 1. What breaks first when you start running multiple AI agents?
r/AI_Agents · 2026-09-23 · https://www.reddit.com/comments/1woj7dv/ · score 8, ~66 comments
Read: full selftext (742 chars) + 70 fetched comments (raw `sweep/tmp/sw2_item_1woj7dv.json`).
> "Each run gets a slice of the window, so a lane stuck in a retry loop burns its own share and stops instead of emptying the bucket for the others."

Practitioner failure census at width: the two top threads are (a) **per-lane quota fencing**
(u/ianreboot, two comments): fence each invocation at a share of the provider window, so a
lane stuck retrying hits its OWN ceiling and stops, instead of spending the bucket the other
lanes need - and the provider's two readouts (weekly vs 5-hour bucket) "don't agree with
each other"; (b) **attribution breaks before state or retries** (u/Mariia_Sosnina): with
interleaved tool calls the log is one flat stream and "We lost a day on a 'state bug' that
was just two agents writing in an order we couldnt see" - correlation IDs per call are the
fix; (c) post-hoc causality needs run IDs + step IDs + who-changed-what (u/Annual-Ad8594);
(d) verify-after-risk rule: "if an outsider couldn't tell success from the app alone after
the action, it was risky and needs the verify" (u/ImL1s).
Estate read (Q2 + Q4): the preventive shape for the code-1005 lane deaths that DEALS does
not supply - the BUILD-IT-ALL lanes died sharing one quota bucket, and the practitioner fix
is per-lane fencing of the shared window, i.e. lane_runner budgets its own slice and stops
itself instead of starving siblings. For Q4, corr_id-per-effect attribution is exactly the
mesh-diagnosis primitive (the estate's estate_query corr_id joins already exist; the missing
half is the death-event ledger the census verdict names).

### 2. How do you use subagents & multiple agent with local models, and how many?
r/LocalLLaMA · 2026-09-25 · https://www.reddit.com/comments/1wpxh2g/ · score 20, ~70 comments
Read: full selftext + 73 fetched comments (raw `sweep/tmp/sw2_item_1wpxh2g.json`).
> "Run tasks in waves: do 2 or 3 independent tasks at a time, check that the code works, then move to the next step."

Width envelope on one local box: qwen3.8-27B NVFP4 on vLLM at max context "gives around 8
agents with 32k context each" (selftext); a counter claims 800k pooled KV on 2x3090 with
vLLM dynamic per-request allocation vs llama.cpp slot reservation (u/zipperlein, u/cbert33);
the correction computes the arithmetic - "You'd need ~16GB for 256k context at BF16. To get
true 800K you'd need ~50GB" (u/BawbbySmith). The surviving doctrine: short-task children
that "save its work to disk, and exit immediately" (u/Muted_Ad_9442, top comment), waves of
2-3 with a check between waves, workers returning "a compact summary plus pointers to
anything written to disk" while worker transcripts stay off the orchestrator's KV
(u/Kairos_BA).
Estate read (Q1): the fan-out width law's mechanism confirmed from the local side - width is
a KV-cache/compute budget, so maxAttempts-0 workflow children at near-3 width and 11-retry
Task agents at 10-12 width are two operating points on one budget curve, not two truths. The
portable shape for the local janitor lane: wave-scheduled short children, disk artifacts,
summary+pointer returns (the report()-salvage shape), orchestrator KV swapped out during
child runs.

### 3. are you still creating fresh sessions or work in the same thread?
r/ClaudeCode · 2026-10-02 · https://www.reddit.com/comments/1wvpffv/ · score 133, ~147 comments
Read: full selftext + 152 fetched comments (raw `sweep/tmp/sw2_item_1wvpffv.json`).
> "Reset if `upfront reset cost < useless leftover context × number of future invokations you expect your next task to take`"

The redo-vs-resume decision, practitioner edition: month-long single threads drift
("poisoned context... like clockwork", s=156), fresh-session fans pay cold-cache re-prefill
("why did my entire five hour usage get drained by one prompt!"), and the thread's most
portable artifact is the quantified reset predicate above - measure upfront cost by
prompting "Reply with OK", estimate leftover, multiply by expected future invocations.
Supporting shape: orchestrator keeps a kanban of workpackage .md files so new sessions start
frequently without losing context (s=79); compaction "misses things and is token heavy"
(s=19).
Estate read (Q3): this is the missing cost model for the 438-redone-vs-8-resumed question -
redo-vs-resume is an arithmetic decision (reset cost vs leftover-context tax times remaining
invocations), not a habit; the estate can instantiate it per lane from trail-derived reset
costs once the death ledger exists. No in-window replication of the 438/8 numbers anywhere.

### 4. The tool timed out. Is it safe for the agent to try again?
r/LLMDevs · 2026-10-01 · https://www.reddit.com/comments/1wv66mt/ · score 3, 4 comments
Read: full selftext (651 chars) + all 4 comments (raw `sweep/tmp/sw2_item_1wv66mt.json`).
> "we model three outcomes in the tool result: done, failed, and unknown. Unknown comes with a check handle, and the agent is only allowed to call the status tool next, not the write tool again."

Retry-safety contract: stable request IDs minted by the caller's code BEFORE the model sees
the tool ("If the model makes up the key, a re-plan after the timeout can produce a fresh
key, and you get the double booking anyway"), a first-class unknown outcome whose only legal
next action is a status check, and the restart case: "If the request ID only lives in the
conversation, a fresh session can turn the same intent into a second booking. The original
operation needs to remain discoverable after that restart."
Estate read (Q1 + Q3): the gate that makes the retry asymmetry safe - workflow children with
maxAttempts 0 die safe by construction; the 11-retry Task path is only safe if retries carry
an intent-derived idempotency key and an unknown-state that forbids re-fire. Refinement for
lane_runner: the key must be minted outside the model and persisted with the ask, or
salvage-after-death cannot distinguish done from unknown.

### 5. Be careful with Opus 5.5's confidence
r/ClaudeCode · 2026-09-26 · https://www.reddit.com/comments/1wqnjkp/ · score 59, ~64 comments
Read: full selftext + 75 fetched comments (raw `sweep/tmp/sw2_item_1wqnjkp.json`).
> "Never use the same context/session for both writing the code and reviewing the code."

A frontier model investigating its own work returns "an incomplete investigation or a
conclusion based on wrong results" and still reports mistakes found with confidence. The
community's convergent fix is NOT more sampling from the same animal: independent second
context ("tell it explicitly not to trust its own first pass conclusions before handing
off"), cross-FAMILY review ("dispatch to Fable 5.1 for a review and each time Fable catches
gaps"), and - ranked above any LLM reviewer - a test suite plus a spec: "how can the changes
be reviewed for regressions if the reviewer has no idea what it is regressing from?"
Estate read (Q5): practitioner-grade confirmation of the consensus-illusion verdict's other
half - a single seat's confidence is not evidence, and corroboration must cross contexts and
families; deterministic instruments (tests, specs) outrank any LLM reviewer. No post-bank
evidence here moves open-ended divergent sampling off the flock's valid-uses list; this
thread extends the NOT-a-verifier side, not the sampler side.

### 6. Can you force Claude to write a handoff .md file before a chat gets compacted?
r/ClaudeAI · 2026-09-30 · https://www.reddit.com/comments/1wui0hj/ · score 69, 82 comments
Read: full selftext (1,835 chars) + 82 fetched comments (raw `sweep/tmp/sw2_item_1wui0hj.json`).
> "the agent can't reliably tell when compaction is about to happen, so a handoff written \"just in time\" is often late or slightly out of date."

Checkpoint cadence doctrine: just-in-time salvage fails because the agent cannot see
compaction coming; every-turn overwrite of HANDOFF.md (the OP's workaround) is voted token-
inefficient ("Auto handoff after every prompt will be token inefficient. Too many writes.");
the durable shape is handoff at natural milestone boundaries (200k-400k), deterministic
PreCompact hooks where the harness offers them, and overwrite-not-append so the handoff
never becomes its own context problem. "A hand off file is basically compaction" (s=17) -
the difference is who controls the trigger.
Estate read (Q3): the salvage gate needs a cadence, not just a schema - milestone handoffs
plus a deterministic pre-compaction hook, never compaction-time salvage, never per-turn
burn. Maps to the estate's trail.jsonl append habit: the trail IS the every-turn write; the
handoff file is the milestone projection.

### 7. 400+ LLM agents living in a 2004-era MMO server, all local on Qwen3-4B
r/ollama · 2026-09-29 · https://www.reddit.com/comments/1wt0tot/ · score 189, ~25 comments
Read: full selftext (1,049 chars) + 36 fetched comments (raw `sweep/tmp/sw2_item_1wt0tot.json`).
> "When the queue backs up, low-priority reflections get shed so chat stays responsive."

A live 400+ agent local mesh on 2x3090: Qwen3-4B Q4_K_M 4k-context runs the per-agent loop,
Qwen3.8-27B Q4_K_M serves rich one-on-one interactions, ~2.5s avg per call, MTP speculative
decoding on the big tier. The queue policy is explicit: under queue pressure, low-priority
reflection work is SHED to keep the chat class responsive. Comments push a classifier-first
architecture (deterministic behavior layer, LLM reserved for conversation and social
decisions).
Estate read (Q2 + Q1): a running demonstration of priority-class admission control - the
exact policy class the quota-wall question asks about - plus the janitor/specialist tier
split the estate already runs, at 400+ agents. No measured QoS numbers in-thread (hobby
system), hence moderate confidence; the shed-reflections-first ordering is the stealable
shape for lane priority under cap pressure.

### 8. Perhaps Sol 6.1 is not that bad after all. I've spent 160% of my quota on Astra trying to solve a bottleneck
r/codex · 2026-09-29 · https://www.reddit.com/comments/1wtmhgw/ · score 34, ~65 comments
Read: full selftext + 65 fetched comments (raw `sweep/tmp/sw2_item_1wtmhgw.json`).
> "Sol 6.1 worked about an hour on high on it, while consuming 1% of my quota and dropping the publication age to 38ms"

Cost-asymmetry data point: a premium lane burned 160% of plan quota on a latency bottleneck
(47s publication age under stress); the cheaper tier then solved it in ~1 hour for 1% of
quota, dropping it to 38ms. Two supporting practitioner facts: the cheap tier "doesn't rip
through usage like Astra does" (usage efficiency is model-coupled, not just plan-coupled),
and provider usage readouts are unstable - "my Pro 200 plan keeps bouncing between 71% and
42% usage available with no rhyme or reason."
Estate read (Q2): cheap-first (SHERPA leg) has a practitioner cost face - when a lane is
burning quota on a wall, the queue policy is to demote the ask to the cheaper tier rather
than keep paying the premium lane's burn rate; and quota telemetry from provider readouts is
untrustable, which is why the census must bank receipt-side usage, not console numbers.

## Per-question verdicts, window 2

- **Q1 (PANDA port):** nothing in-window documents mesh-level fault-tolerance mechanisms
  comparable to 2609.38482; that confirmed row stands unreplicated on reddit. What the
  window adds: the retry asymmetry has a physical substrate (item 2 - width is a KV/compute
  budget) and a safety gate (item 4 - unknown-state + caller-minted keys) rather than a
  contradiction. No thread found that contradicts maxAttempts-0 for workflow children.
- **Q2 (quota-wall queue policy):** the practitioner preventive shape is per-lane fencing of
  the shared provider window (item 1), priority-class shedding under pressure (item 7),
  cheap-tier demotion of burning asks (item 8). DEALS expertise-aware queuing (arXiv r4)
  stays unreplicated on reddit; the owed census cannot yet name any shape because the estate
  death ledger does not exist (see census verdict).
- **Q3 (redo-vs-resume):** no replication of the 438/8 census anywhere in-window; what
  reddit adds is the decision arithmetic (item 3), the cadence (item 6), and the
  restart-safety contract (item 4). The estate fraction remains UNMEASURABLE, not zero.
- **Q4 (MAS collective-failure diagnosis):** no in-window match for 2609.38761's mechanism;
  the practitioner primitives are corr_id-per-call attribution and run/step event logs for
  post-hoc causality (item 1). rib_bus adoption candidate: keep corr_id on every effect and
  add the missing death-event rows, so a swarm failure reads off the mesh instead of re-run
  blind. A directly-on-topic thread (EchoFault, incident-history-to-diagnosis, r/aiagents
  1wtsxbm) surfaced in pass 1 but had ~1 comment; not deep-read, not banked.
- **Q5 (flock vs single seat):** no post-bank evidence moves open-ended divergent sampling
  off the consensus-illusion valid-uses list; item 5 reinforces the other half (single-seat
  confidence is not evidence; corroboration crosses contexts and families; instruments
  outrank reviewers).

## Overlap check, window 2 (per banking rule)

16 distinctive phrases (2+ per item) grepped against `catalog/catalog.jsonl` (260,806,347
bytes): **0 hits on all 16**. Against `memory/` (453,131 files scanned): every phrase's only
hit is `memory/trajectory/steps.jsonl` - this window's own step journal logging the grep
commands (self-referential, not prior art), plus one coincidental "check handle" in
`memory/runs/fleet_round/burn2b/wave_04/Z002_MAZE.md` (unrelated subject). No sibling lane
has banked any of the 8 threads; nothing here re-banks window 1.

## Method notes, window 2

- Instruments: `sweep/tmp/sw2_crawl.py` (Arctic Shift posts/search, 14 subs, cursor
  pagination, 24,367 rows to `sweep/tmp/sw2_full.jsonl`), `sweep/tmp/sw2_read.py`
  (posts/ids + comments/search per thread; raw per-item bytes in
  `sweep/tmp/sw2_item_<id>.json` x8), inline python for the census tallies and the overlap
  grep. Door probes: curl (old/www/api.reddit, r.jina.ai, 4 redlib instances), WebFetch,
  web_reader MCP, WebSearch - every failure named above, none fabricated.
- Quotes are verbatim from the fetched comment/selftext bytes; scores and comment counts
  are archive-moment values, not live Reddit.
- Not run: no pytest/census instruments beyond the read-only trail/registry tallies named
  above - this ask is a research sweep; nothing was executed against the estate's test
  surfaces, and the write-up bank rule (1000+ chars) is satisfied by this section alone.
