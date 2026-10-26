# X INTEL DIG: ai-engineering-from-scratch + agentmemory (2026-10-04)

Operator drop: "https://x.com/RoundtableSpace/status/2106704634584903895 dig deep on this"

## The tweet, verified

@RoundtableSpace (Mario Nawfal's Crypto & AI org account, 265.9K followers),
2026-10-04 11:15 UTC, 23.7K views at fetch: promoting
github.com/rohitg00/ai-engineering-from-scratch - "523 lessons. 342 hours.
from the math all the way up to agent swarms, and every lesson ships something
real." 63K stars claimed, costs $0.

## Byte verification (cloned, corpus/library, MIT)

- 523 lessons: EXACT (523 dirs with docs/en.md under phases/00-19). 1,813
  commits, tip 3be078b 2026-10-02 (two days old - live repo).
- 63.5K stars / 10.9K forks confirmed at fetch. 114,584 readers, 181,995 page
  views/30d (their own counter, 2026-08-29).
- The 342-hour claim is an UNDERCOUNT: 515/523 lessons carry a Time field and
  they sum to ~1,160 hours - the curriculum is ~3.4x bigger than advertised
  (342h is presumably a core path, not the whole ladder).
- Quiz coverage: 373/523 lessons carry quiz.json (71%); the agent phase is
  54/54 fully quizzed.

## What it actually is: a Primer running in production

The curriculum is agents-native (AGENTS.md operating manual, .claude/skills,
10 tutor skills installable via `npx skills add rohitg00/...`) and implements
the full Primer loop for humans-with-agents:

| Primer property | Their organ |
|---|---|
| Adaptive front (right-size to learner) | find-your-level skill + learning-paths |
| Teach through wanted interaction | learn skill: section-by-section, "never just scroll", works hostless over raw.githubusercontent.com |
| Verification ractive | check-understanding skill + quiz.json contract |
| Progress memory | LEARNING.md progress file |
| Certification | claude-certification + mcpa-certification tracks |

The lesson contract has estate-grade gates baked in: quiz.json = exactly 6
questions (1 pre + 3 check + 2 post), zero-indexed answers, bias-checked
distractor lengths; CI runs audit_lessons.py and blocks PRs; code must run
end-to-end, self-terminate, 5+ stdlib-runner tests; scenario runners/scorers
instead of fake API code; dependency allowlists (Rust stdlib only; Python
numpy/torch/h5py/zstandard/safetensors). Every lesson ships a reusable
artifact: a prompt, a skill, an agent, or an MCP server - convert-yield as
curriculum law.

## THE CONVERGENCE FIND: the estate's laws, written by a stranger as lessons

Phase 14 (agent-engineering, 54 lessons) lessons 43-54 are not framework
lessons - they are the estate's operating law as a teachable ladder:

| their lesson | estate organ |
|---|---|
| 37 runtime-feedback-loops | lane runner_state feedback |
| 38 verification-gates | ratchet / citation-lint / workflow-gate |
| 40 multi-session-handoff | next-window-handoff.md |
| 43 frame-the-task-before-code | spec-before-behavior-change |
| 44 plan-from-evidence | trust bytes, not reports |
| 46 turn-feedback-into-system | social_rsi |
| 47 outcomes-before-output | convert-yield-not-sing |
| 50 choose-the-smallest-testable-slice | checkpoint climbs |
| 54 build-the-feedback-ratchet | violation_ratchet.py |

Independent convergent evolution: a UK DevRel engineer (Rohit Ghumare, GDE,
Docker Captain, ex-Cloudera/Oracle/Solo.io) derived the same law-list the
estate bled for. Two implications: (a) the estate's laws are the actual
curriculum of production agent engineering, not local superstition; (b) their
54-lesson ladder is a free self-audit surface - sweep it against estate
organs for gaps (FIPA-ACL heritage, theory-of-mind coordination, BFT/consensus
lessons in phase 16 are mesh territory the estate should cross-check).

Phase 16 (multi-agent-and-swarms, 25 lessons): supervisor patterns, debate
topologies, negotiation, agent economies, swarm optimization, MARL, groupthink
failure modes, 2026 SOTA case studies. Phase 15 autonomous-systems: 22 more.

## Second target surfaced: agentmemory (29.1K stars, MIT)

Same author, persistent memory for AI coding agents, TypeScript MCP server,
tip commit TODAY (c51bf3f 2026-10-04: embedding key precedence, structured
SessionStart context). Claims: 95.2% retrieval R@5, 92% fewer tokens, 54 MCP
tools, 12 auto hooks, 0 external DBs, 1,674+ tests. Extends "Karpathy's LLM
Wiki pattern with confidence scoring, lifecycle, knowledge graphs, and hybrid
search" (design doc: a 1.6K-star gist).

THE DIRECT HIT: its supported-agents list names **Hermes and OpenClaw** - both
estate surfaces - plus Claude Code, Codex, Cursor, OpenCode, any MCP client.
This is prior art landing exactly on the estate's MCP-lattice vision
(memory/mcp-lattice spec-seed: local MCP server serving right-sized context
from the hot lattice, PULL OVER DUMP). A 29K-star implementation with
confidence scoring + lifecycle + knowledge graph + hybrid search is shipping
now. The lattice spec owes a reconciliation pass against it (adopt/steal/watch
doors like image-blaster) BEFORE any lattice building starts - the wire-don't-
build law. Cloned to corpus/library/agentmemory for that pass.

## Steal doors (named, ordered by leverage)

1. quiz.json contract as the estate skill-card verification ractive: every
   .agents/skills card gains a check-understanding section - a skill that
   cannot quiz its holder cannot verify it transferred. Pairs with gwap.
2. six-beat lesson contract (Motto, Problem, Concept, Build It, Use It, Ship
   It) for social_rsi synthesis packets - the drafted errno22 card re-cast
   into the six beats becomes a teachable primer lesson, not just a cure.
3. `npx skills add` distribution: estate .agents/skills become installable by
   other seats/hosts (the skills-are-distribution play this repo proves).
4. find-your-level: the context-pack quantizer pattern applied to seats - a
   new seat takes a level probe instead of drinking the whole AGENTS.md.
5. agentmemory reconciliation on the MCP-lattice leg (prior art, wire-don't-
   build; integration door already names Hermes/OpenClaw).
6. their phases 14-16 as a free self-audit: run the estate's organs against
   their 101 agent/swarm lesson objectives and file the gaps.

## Evidence

- corpus/library/ai-engineering-from-scratch @ 3be078b (shallow clone, 107MB,
  gitignored per library pattern)
- agentmemory @ c51bf3f parked OUTSIDE the repo tree at
  ../library_parked/agentmemory (sibling of the repo, 60MB). Why parked: the
  Mimosa commit gate force-blocked on its vendored contents (73 high findings,
  all inside the clone: SSRF-class patterns in their cli.ts URL-fetch paths
  at :1020/:2411/:2816/:2834/:2876/:4079, hardcoded credentials in their
  test/cli-doctor-fixes.test.ts, code injection in their
  viewer-dashboard-reliability.test.ts). Third-party code, never executed by
  the estate, inventory only - but the finding classes are themselves the
  reconciliation caveat: door 5's pass must NOT run their CLI against
  untrusted input without review; the SSRF surface is real in their code.
- tweet fetch via api.fxtwitter.com 2026-10-04 ~12:00 UTC

No paid doors used; all $0. Nothing executed from either repo (inventory only;
any adoption of agentmemory code is operator-gated like image-blaster keys).

Writer: zcode-53-strategy-window
