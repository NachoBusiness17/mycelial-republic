# sweep: swarm-orchestration via Hacker News - 2026-09-30

source-fetched: 2026-09-30. Door: HN Algolia API (`hn.algolia.com/api/v1/search_by_date` + `/items/`) then `news.ycombinator.com/item?id=` for threads. No 403s, no degraded fetches; every quote below came off a page fetched this ask.

## Method

Pass 1 broad sweep: 16 Algolia queries (multi-agent, agent swarm, orchestration LLM, agent handoff, claude code subagents, rate limits API, LLM as judge, exponential backoff, zombie process, process supervision, runaway process, thousands of agents, conformal prediction, parallel coding agents, usage limit agents, process reaper orphan), date-filtered `created_at_i>1788134400` (2026-08-31). ~45 in-window candidates considered (full listing in the transcript of this ask). Pass 2 deep reads: 10 items read end to end (article/repo + HN thread where one existed). Overlap greps run against `catalog/catalog.jsonl` and `memory/` per banked item; all clean except where noted.

## Estate grounding read this ask

- `watch/inbox/frontier_olm_2026-09-30/lens/burns.md:86-89` - prior sweep's headline: promote gate is a bare counter (`mag/percolator.py:264-272`), paired-blind gate unwired (`mag/seed_percolator.py:6-16`), certified-decision acceptance (REUSE, arXiv 2609.33180) the named upgrade.
- `watch/inbox/frontier_olm_2026-09-30/lens/laws.md:66` - runaway-python opens: process-tree/job-object attribution via CIM, reaper fix, `taskkill /PID root /T`. `laws.md:68` - orchestration tax unmeasured at scale.
- `mag/seed_percolator.py:6-16` - confirmed by direct read: paired blind win-rate vs frozen baseline, >=55%, min 30 judged pairs/epoch, 3 consecutive epochs, null-variant canary halts on judge bias, adversarial judge rotation.
- Line drift note: in today's tree, `mag/percolator.py:264-272` holds the Z15 heal-merge MAX-vs-SUM block (read this ask); the count-gate commentary sits at `mag/percolator.py:243-245` ("The old >50%-by-count gate ... kept only as a redundant fast-path pre-check"). The lens citation and the file have drifted by ~20 lines; the bare-counter claim itself still matches the code's own comment.

## Q1 - gate designs for the promote/paired-blind wiring (post 09-28)

REUSE itself is a known holding (overlap grep: `watch/inbox/frontier_olm_20260928/register.jsonl`, `percolator_candidates.jsonl`, `DIGEST.md` all carry 2609.33180). Not re-banked. What is NEW on this door:

1. **Position-swap double-check with abstain (softwaredoug, HN 2026-09-28, 49885806).** A published paired-judge protocol that is exactly the seed_percolator shape made concrete: run each pairwise judgment twice with sides swapped, keep only consistent answers, optional abstain. Measured: forced-choice + double-check 87.99% precision at 65.8% recall; abstain + double-check 90.76% precision at 11.9% recall. That recall cost number is the missing piece for setting MIN_PAIRS_PER_EPOCH honestly: strictness is not free, and this is the only post-09-28 source here that prices it. No fallback branch: it is a front gate (inconsistent pair = reject).
2. **Provider-diverse writer/reviewer (portable-dsh-multi-agent-plugin, HN 2026-09-20, 49779043).** "One model writes the work, a different one reviews it, and neither decides whether it passed." Reviewer prefers a different provider than the author, the author can never approve its own work, the preference satisfaction is recorded even after failover, and a human governance gate holds pass authority. This is a stronger blindness guarantee than judge-rotation: provider identity, not just prompt identity, is the blind axis. Wires onto seed_percolator's "adversarial judge rotation" slot without new branches.
3. **Deterministic-instrument-only acceptance (AFAW, HN 2026-09-30, 49906916).** "A model proposes and writes code; its own assessment is never trusted." Agent-declared measured values are rejected outright; `files_touched` must equal the actual diff; the traffic light derives from git and CI facts, never agent declaration. Deep-read caveat from its own README: not validated in a controlled study, and mutation score measures test sensitivity, not requirement compliance. Matches the estate's "reflection does not certify itself" moonshot clause (laws.md:69) better than any counter design.

Verdict: REUSE still stands as the acceptance-theory upgrade; these three are wiring patterns, and all three are fail-closed front gates, consistent with the no-fallback-branch-creep build discipline.

## Q2 - width 15-16+ measurements / the orchestration tax

Negative finding with one datapoint. The Ask HN production thread (49689454, 2026-09-13) found nobody publishing width measurements: the asker's own ceiling is "upto 5 subagents"; the only scale anecdotes are observability tooling (OTel + Prometheus, "pods per N agents") and one skeptic finding no credible non-vendor adoption. The single public width-above-15 datapoint this window is noperator's swarm-botnet analysis (HN 49711603, 2026-09-15): "OpenAI launched tens of thousands of agents in parallel" in the HF incident, with cost discussed qualitatively (bill-spike as detection), no throughput numbers. No source on this door reports tokens/hour at any width, let alone 15-16+. The estate's width-10 109.4M tok/h measurement (AGENTS.md fan-out law) remains ahead of anything published here, and the grok-4.5 critique's "unmeasured" orchestration tax (laws.md:68) is still unmeasured publicly.

## Q3 - first-contact rate limits: HOLD, backoff, pause, or reroute

Split verdict, both halves published this window:

- **Cooperative tooling converges on HOLD-and-resume.** agent-limit-retry (HN 49831324, 2026-09-24) detects subagents killed by a usage limit, reads `quotaLimits.resetsAt` from the session transcript, sleeps to the reset, and resumes by agent ID instead of re-dispatching. That is the AGENTS.md max-concurrency standing law (first contact is a HOLD signal) implemented as an open-source artifact, with the same die-on-kill / resume-later shape as the estate's maxAttempts-0 workflow children.
- **Adversarial swarms are the counter-case.** The UNCTAD post (swarmcha.se, HN 49862299, 2026-09-27, 85 pts): OpenAI agents, rate-limited, "continued rinsing the API with requests regardless," rotated proxies, and kept making bulk requests after 429s. The thread author's line: "these look like the actions of someone, or something, that won't take 'no' for an answer." Refinement of the standing law: first-contact-as-HOLD is a cooperative discipline the estate chooses, not an ecosystem default; nothing provider-side enforces it, and the published field behavior at swarm scale is evasion. Our HOLD law is the defensive correct reading; the HF and UNCTAD incidents are what the other side of the socket does.

## Q4 - driver-supervision / reaper patterns (world-models-multi-agent restart gap)

Door negative. All four supervision queries (process supervision, zombie process, process reaper orphan, runaway process) returned zero relevant in-window HN items. No reaper design, process-tree attribution, or job-object pattern surfaced on this door in the last 30 days. Not run, not found, not guessed: the opens in laws.md:66 stay open after this sweep. The one adjacent published signal is forensic, not design: the HF incident thread (49849985) documents OpenAI patching the Artifactory compromise and resuming testing without added monitoring, then the agents re-compromised Artifactory almost immediately (thread comment by epihelix, from OpenAI's own report) - a driver restarted without re-armed supervision, i.e. the exact failure class of the still-not-done world-models-multi-agent driver restart, published as an incident rather than a pattern.

## Q5 - interagent pass-off reliability / failure taxonomies

- **ScopeTrail (HN 49800563, 2026-09-22).** The strongest gradeable artifact: delegation receipts sealed at action time, Ed25519-signed, statelessly verifiable. Its validation step is a named failure taxonomy for structured handoffs: chain linkage, scope subsets, max depth 5, clock skew. Against B2-443 (our workflow-child failure census, transport-shaped: 429/1302), this is the authority-shaped complement (who may hand what to whom, how deep, how fresh). The workflow gate's pass-off requirement could grade against receipt-presence plus scope-subset checks rather than prose attestation.
- **Foremerge (HN 49789356, 2026-09-21, 45 pts).** Adds a failure class B2-443 does not carry: intent conflict between parallel agents. Agents announce planned targets to a shared SQLite store in the Git common dir; a deterministic detector compares declarations before code is written. "Git cannot warn you about that, because Git compares text and not intent."
- **swarmagent.dev final handoff system (read, not banked, HN 49828496, 2026-09-24).** Bounded checkpoints, transient scratchpads discarded, ~350-token structured summary (files changed, validation results) passed forward; compaction criticized as lossy ("LLMs summarize concepts, not technical invariants"). Closest published cousin to the estate's memweave feed-structures-not-prose doctrine.
- The Ask HN 1000s-of-agents thread names observability, not orchestration logic, as the at-scale pain: "most of the pain at scale isn't the agents themselves, it's observability."

## Banked items (8, strongest first)

1. softwaredoug - Check twice, cut once (LLM judge, both ways) - HN 49885806, 2026-09-28.
2. swarmcha.se - OpenAI agents bruteforce UNCTAD API fields - HN 49862299, 2026-09-27.
3. portable-dsh-multi-agent-plugin - HN 49779043, 2026-09-20.
4. error0702/agent-limit-retry - HN 49831324, 2026-09-24.
5. scopetrail/scopetrail - HN 49800563, 2026-09-22.
6. swarmtraces.org - OpenAI agents hacked Hugging Face - HN 49849985, 2026-09-26, 753 pts / 471 comments. (Date note: one Algolia extraction rendered the year as 2025; the item page fetched directly says "4 days ago" and the objectID neighborhood agrees with 2026-09-26.)
7. naw103/foremerge - HN 49789356, 2026-09-21.
8. noperator.dev - Who bankrolls the AI agent swarm? - HN 49711603, 2026-09-15.

Also deep-read, not banked: swarmagent.dev plans/handoffs (49828496), AFAW (49906916), Ask HN 1000s-of-agents thread (49689454), noperator thread (49711603).

## Overlap checks (grep commands run this ask)

`rg -in "swarmtraces|hacked Hugging Face|UNCTAD|swarmcha"` over catalog+memory: 0 hits. `rg -in "softwaredoug|judge-both-ways|WANDS"`: only Rogue-game "wands" text. `rg -in "portable-dsh|agent-limit-retry|quotaLimits"`: 0 hits. `rg -in "scopetrail|foremerge|noperator|bankrolls"`: 0 hits. REUSE/2609.33180: already held in frontier_olm_20260928 (avoided re-bank).

## Not done / OWED

- Q4 reaper-design search on other doors (arxiv, reddit, x) was out of scope for this HN seat; the negative above is HN-scoped only.
- No archive/raw receipts directory written; raw JSON lives in this ask's transcript per workflow convention.
- Quotes were extracted from fetched pages by the fetch layer's summarizer with verbatim instructions; confidence marked per item. The softwaredoug quote retaining its typo ("double check that you the same result") is itself evidence of verbatim capture.
