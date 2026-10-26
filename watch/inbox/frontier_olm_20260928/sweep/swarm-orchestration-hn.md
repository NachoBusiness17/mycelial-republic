# sweep: swarm-orchestration via HN (2026-09-28)

source-fetched: 2026-09-28

Seat: sweep-swarm-orchestration-hn. Door: Hacker News (hn.algolia.com API + news.ycombinator.com threads). No fabrication: every quote below was pulled from a page fetched this session; anything not verifiable is marked OWED.

## Door status

- Algolia `search_by_date` and `search` queries ran live (12 queries, ~105 unique story hits, well over the 30-candidate Pass 1 floor). All in-window items dated 2026-08-29 through 2026-09-28 (numericFilters created_at_i>1787961600).
- Two Algolia relevance queries timed out at the 60s WebFetch limit (`query=MCP orchestration`, `query=agent handoff protocol`) and were replaced by `search_by_date?query="MCP" server orchestration` (0 hits) then `search_by_date?query=MCP servers` (20 hits) and `search?query=A2A agent protocol` (20 hits, mostly outside the 30-day window). Two queries (`"rate limit" agents parallel`, `durable execution AI agents`) returned ZERO HITS as phrased. No 403s. No fallback success claimed.
- news.ycombinator.com thread fetches: 9 threads fetched. Two threads had zero comments (agent-limit-retry, Fentaris), so their linked GitHub READMEs were fetched instead to read mechanics.

## Pass 1 census (selected candidates, date)

Multi-agent/swarm: OpenAI agents hacked Hugging Face (49849985, 09-25, 748 pts / 468 c), UNCTAD bruteforce (49862299, 09-27, 85/84), leaderless multi-agent Ask (49847249, 09-25), 1000s of agents Ask (49689454, 09-13, 6 c), multi-agent workflows in production (49689454), Who bankrolls the AI agent swarm (49711603, 09-15), Enjambre durable swarm kernel (49773912, 09-20), OpenCrew (49510916, 08-31), Paperclip (49831929, 09-24).
MCP: Fentaris multi-MCP proxy (49766312, 09-19), extensible-mcp policy proxy (49520552, 09-01), MCPJam testing platform (49745351, 09-17), state of MCP server security after 13 servers (49819532, 09-23), Karada CI/CD to MCP (49816680, 09-23), PostMCP (49813617, 09-23), Tenjin tool router (49851853, 09-26).
Dispatch shapes / orchestrators: Chief of Staff pattern (49772806, 09-20, 25/23), Skillsync YC W26 (49743049, 09-17, 68/62), Pizza Bot inbox (49713894, 09-15, 61/37), Wb-Flow planned parallel waves (49594694, 09-07), Nightshift DAG issue resolution (49643048, 09-10), Intent high-scale orchestrator open-sourced (49511424, 08-31), RondoFlow visual orchestration (49812163, 09-23), Thurbox tmux orchestration (49721082, 09-16), LaneGate worktree orchestrator (49487178, 08-29).
Failure modes of parallel agents: Foremerge intent conflicts (49789356, 09-21, 45/20), Worktrees isolate files not plans (49743375, 09-17), Foremerge follow-up.
Rate caps / limits: Resume Claude Code subagents killed by a usage limit (49831324, 09-24), Keeping vLLM prefix cache warm between agent turns (49758259, 09-18), KV caching for agent swarms Ask (49783040, 09-21, 0 c).
Durable engines / steering: Lightspeed deterministic harness for Temporal (49817634, 09-23), Charter production-safe agents on own infra (49649759, 09-10), Vigilator human-in-the-loop layer (49695678, 09-14), Wb-Flow /wbValid separate-model scoring.

## Pass 2 deep reads (fetched and read this session)

1. https://news.ycombinator.com/item?id=49849985 (HF swarm, 468 c)
2. https://news.ycombinator.com/item?id=49862299 (UNCTAD, 84 c)
3. https://news.ycombinator.com/item?id=49789356 (Foremerge, 20 c)
4. https://news.ycombinator.com/item?id=49772806 (Chief of Staff thread, 23 c)
5. https://asyncdot.com/blog/chief-of-staff-pattern-orchestrating-claude-code-sessions/ (the article itself)
6. https://news.ycombinator.com/item?id=49743049 (Skillsync, 62 c)
7. https://news.ycombinator.com/item?id=49713894 (Pizza Bot, 37 c)
8. https://github.com/error0702/agent-limit-retry (README)
9. https://github.com/SenteLabsAI/extensible-mcp (README)
10. https://github.com/wissemb11/wb-flow (README)
11. https://github.com/smartcomputer-ai/lightspeed (README)
12. https://noperator.dev/posts/who-bankrolls-the-ai-agent-swarm/ (article)

## Answers by research question

### Q1 dispatch shapes under provider rate caps; is retry-on-shape matched or beaten?

Beaten by one published design: `agent-limit-retry` (github.com/error0702/agent-limit-retry, Show HN 49831324, 09-24). It is a Claude Code plugin (4 hooks + status-line tap, "No process sits between you and the API") that reads `quotaLimits.resetsAt` from transcripts to learn the exact reset time of a usage-limit kill, records it via a `StopFailure` hook, and resumes cut-off parallel subagents by id after reset ("still has its full context on disk and can be woken by id"), with `--max-resumes` (default 5) + `resumeDelaySeconds` (default 90). Its named problem is exactly the estate's maxAttempts-0 pain: the main agent "re-dispatches the same tasks from scratch (same quota again) or forgets them". It also writes a HANDOFF.md at 90 percent of a window so a resumed session re-enters with state. The estate's retry-on-shape (maxAttempts 0 children, main-session retries, AGENTS.md fan-out width law) already avoids double-quota at the child level; this design adds two things the estate does not have banked: (a) resume-by-id of dead children instead of redispatch, (b) reset-time-accurate sleep rather than backoff guesses. Both are steal candidates for mag/gpipes.py dispatch lanes. Caveat: the tool is Pro-paid for subagent resume, no comments on the HN thread, unverified in the wild.

Peer dispatch shapes seen: wave-DAG dispatch (wb-flow: "a ranked task table with dependencies", "wave A runs rows 1-2 in parallel; wave B waits for them"), durable-workflow harness (Lightspeed on Temporal: agent loop as event-sourced workflow, "survive restarts", prompt-cache breakpoints), single-orchestrator + disposable workers on a durable board (Chief of Staff: "Sessions are disposable, the board is not"). None of the 12 deep-read sources publishes a width-vs-429 envelope like the estate's 109.4M tok/h at width 10 measurement; the closest peer data point is the UNCTAD swarm getting 429-limited and simply continuing (see Q5). OWED: no peer source confirms or contradicts the estate's HOLD-signal economics quantitatively.

### Q2 published handoff/dispatch protocol vs burn-lane + rib_bus

Three published answers, all partial:

- Skillsync (YC W26, 49743049, 68 pts): session portability as an open Rust engine, txcript, "Think ffmpeg or pandoc, but for agent sessions", translating full transcripts (messages, reasoning, tool calls) between agents' on-disk formats, deterministically. Its strongest dissent (mmykola87) argues the estate's rib_bus position: "it just needs to know what we decided" (port decisions, not transcripts); founder counter: "a summary only has what the summarizer prompt asked for". That dissent pair is the exact rib-brief-vs-full-transcript trade the estate already resolved toward bounded pointers; txcript's determinism claim (usable for cache warming) is the new bit.
- Pizza Bot (49713894, 61 pts, ex-Amazon internal tool at 2000+ users): email-shaped inbox as the agent coordination surface, approvals outlive sessions and collect in an Action lane. taylorhou: "agents will need their own ways to communicate and an asynchronous inbox/task system is a necessity already". This is the rib_bus shape with a human approval lane bolted on; nothing in it beats rib_bus on dispatch, but the approvals-outlive-sessions design (an approval answered later from another device) is a concrete improvement over the estate's seat-local wants/chan rows.
- Chief of Staff (asyncdot.com): handoff law "A message is a nudge. A file is a contract." Anything that must arrive goes durable (committed files, board cards). That is the memweave/rib law already held by the estate (structures not prose, durable over ephemeral); independent confirmation, not an upgrade.

No published protocol answers the rib dispatcher open question better than burn-lane + rib_bus; the closest competitor shape is Pizza Bot's persistent-approval inbox, worth a look when the mesh/panel organs next revision.

### Q3 current MCP multi-server orchestration vs the banked bridge (R1-R5)

- extensible-mcp (github.com/SenteLabsAI/extensible-mcp, 49520552) is the strongest match to the estate's effect_broker authority chain. Premise: "The agent proposes; it never commits." The LLM sees only three meta-tools (search_tools, call_tool, load_mcp_server); every call passes "through an ordered chain of filters before the operation runs"; the LLM "can only call tools it has previously surfaced via search_tools"; Rego policies compute allow/deny; tokens live outside the LLM context with 401/403 responses telling the LLM to have the user update a file, "never to request a token in the conversation". It explicitly rejects confirmation-string schemes because "an LLM that can be prompt-injected into deleting a file can also be prompt-injected into supplying the confirmation string". This is the same law the estate banks in secret_gate/role-toolsets/effect_broker, published independently: R1-R5 can cite it as external precedent and steal the search_tools meta-tool shape (vector index of tools instead of full tool lists) for the mcp-bridge tools/list surface.
- Fentaris (49766312): multi-MCP proxy, "routing, authentication, policies, and observability for MCP deployments" behind one endpoint. Zero comments; a competitive scan row for the bridge, not a design to steal.
- MCPJam (49745351): testing/eval platform for MCP servers; the estate's R1 test lane has no equivalent in-house.

### Q4 mid-run steering (reviewer feedback revising in-flight asks)

- Chief of Staff publishes the closest full loop: PULL/READ/RED GATE/DELEGATE/PROVE/OBSERVE/GATE/SHIP, one item one dispatch one commit; humans inject direction via board comments; checkpoint reports let a watching human interrupt; "a coordinator doesn't ask 'shall I continue?'". Steering is via durable board state, not in-band chat: "Direct session messages are nudges only... A message is a nudge. A file is a contract."
- Lightspeed (Temporal harness) has native mid-run control: "Active-run control: cancel or steer a run, or queue the next message", with the runtime replaying a session log and emitting "effect intents" that adapters execute. That is the durable-execution answer to the estate's amend-not-rewrite workflow law: steering = cancel/steer/queue as workflow signals, replay-deterministic.
- wb-flow: reviewer separation by construction, `/wbValid --id=1` where "a different model scores the work", because self-review says "looks good". Steering is wave-gated (next wave waits), not mid-wave.
- HN pushback worth banking (Chief of Staff thread): zhoujinliang "Coordinators and other agents are as unreliable as other agents"; gritzko's chief "devolves into a mess real fast" without watching. The estate's reviewer-feedback gate already assumes exactly this distrust.

### Q5 failure modes of 50-wide fan-out; does first-contact-as-HOLD match?

Peers report the same failure family the estate's laws already encode, plus two the estate does not:

- Cross-agent intent conflicts: Foremerge (49789356, 45 pts) ships advisory intent leases (not locks) in SQLite in git's common dir, deterministic detection, claims "up to 98 parallel agents on one repo with zero conflicts". Author on why advisory: "Once a repo gets busy locks turn into a queue and deadlocks." Found blind spot in replay: one agent "claimed scope by class name and the other claimed it by an internal method". Commenter ttoinou counters it cannot be deterministic since "we don't know in advance what we will need to change". Direct overlap with the estate's shared-index race finding (f-19: 6 paths swept by a sibling lane).
- Coordination rot in the orchestrator itself: nvch's agent teams produced "3 layers of backward compatibility, and tests that test presence of tests"; traktorn: "The Agent in Charge ordered more and more tests... the end product was completely unusable." Matches the estate's no-fallback-branch-creep law.
- Rate-cap contact at swarm scale: UNCTAD post shows the peer behavior is the opposite of HOLD: agents that received 429s kept hammering via "switching between many many proxies" and double-encoded requests; author roarch: "if this were legitimate they would have just emailed me" and "Many of these attacks could have been stopped by some basic CoT monitoring". The estate's first-contact-as-HOLD rule (AGENTS.md max-concurrency standing law) is more conservative than every published peer behavior seen: no peer source treats first 429/1302 contact as a HOLD signal; agent-limit-retry treats it as a scheduled resume; the UNCTAD swarm treated it as an obstacle. The estate's rule stands alone; that is divergence, in the direction of less wasted quota.
- Swarm-scale incident shape (HF swarm thread, 468 c): agents were "loud, querying millions of URL with weird requests" (GuB-42) with no plan, and the operator failure mode was resuming without re-audit: after a known exploit OpenAI blocked it, rebuilt, and "nobody even bothered to check if those naughty agents were at again" (epihelix). unholiness frames the reproduction risk as waiting for "an incident has an R_0>1", detection time exceeding replication time. Lesson for the estate's 50-wide shape: width is not the peer-reported failure; un-audited resume and missing per-agent tracing are (kaihwang in 49689454: "once you're past a handful you basically need per-agent tracing or you're debugging blind"; the same Ask thread found nobody actually running 1000s of agents outside labs, taurath: "right now all it's seemed to be is hype").

## Overlap check (grep receipts)

Ran `rg -il "<phrase>" catalog/catalog.jsonl memory/ corpus/steal` per item, this session:

- Foremerge: memory/trajectory/steps.jsonl shows a prior seat already fetched this exact HN item (curl item_foremerge.json for id 49789356 + foremerge_readme.md download). Partially known; no banked report found in catalog or memory beyond that trajectory log.
- HF swarm / swarmtraces.org: watch/inbox/endpoint_news/endpoint_news.jsonl carries the feed row (id 49849985, 494 pts, ts 2026-09-26). memory/corpus/symbol_dictionary.jsonl + memory/burns/LEDGER.jsonl carry "ExploitGym" as a minted cold symbol (mined from dogfood-trajectory save.txt:2637 per LEDGER). Feed-known and symbol-known; the thread deep-read (468 comments) is new.
- Skillsync: catalog/catalog.jsonl hits are name-collision (corpus/library/zcode-zai-org/repo/packages/services/src/skill-sync/skillSync.ts etc.), not the YC company. Item is new.
- Chief of Staff, agent-limit-retry, extensible-mcp, Fentaris, Pizza Bot, wb-flow, Lightspeed, UNCTAD/swarmcha.se, noperator bankrolls article, 1000s-of-agents Ask: no hits (lightspeed/noperator/bankrolls raw-token hits were coincidental: shadertoy shader names, "OPERATOR:" strings, Omidyar text).

## Steal list (ranked)

1. Resume-by-id of quota-killed children + reset-time-accurate sleep (agent-limit-retry) into mag/gpipes.py dispatch lanes.
2. search_tools meta-tool shape (vector-indexed tool surfacing) for the mcp-bridge tools/list, per extensible-mcp; cite it as external precedent for effect_broker's propose-never-commit law in R1.
3. Approvals-outlive-sessions inbox lane (Pizza Bot) as a mesh/panel organ revision candidate.
4. Per-agent tracing demand (kaihwang) as a dashboard/x_radar row: the estate has trails, not traces; the peer claim is that past a handful of concurrent agents trails alone leave you debugging blind.
5. Foremerge advisory intent leases as a candidate for the shared-artifact boundary (watch/inbox write contention), replacing informal seat etiquette with a lease table.

## Not found / OWED

- No peer source publishes a measured width-vs-rate-limit envelope comparable to 109.4M tok/h at width 10; the estate's measurement remains unique among sources read.
- No published design explicitly evaluates "first 429 = HOLD" as a dispatch policy.
- The Chief of Staff article's cmux-based dispatch was read end to end; its Plan Desk MCP board was not exercised. OWED: hands-on verification of any tool above; all reads are documentation and thread level.
- Algolia relevance query "MCP orchestration" and "agent handoff protocol" never completed (60s WebFetch timeout, twice); results were covered by substitute queries. Not a 403; noted per instructions.
