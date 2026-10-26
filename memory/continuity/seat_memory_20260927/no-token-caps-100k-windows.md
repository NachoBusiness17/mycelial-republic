---
name: no-token-caps-100k-windows
description: operator correction 2026-09-17 — "100k+ context windows, stop being
  retarded; self steal, most of these are solved problems"; never ration max_tokens on
  reasoning models — the reasoning channel eats the cap and content comes back EMPTY
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Operator correction (2026-09-17, blunt): "this whole budget thing is fucking nonsense. WE
have like 100k+ context windows, stop being retarded. self steal — most of these are solved
problems." Delivered while I was laddering max_tokens 2600→16000 fighting empty_content on
the build lane.

**Why:** reasoning-channel models (glm-5.3-flash via OpenRouter, gpt-oss family) spend
freely in reasoning BEFORE content; any cap you set gets consumed by reasoning and the
answer comes back empty with finish=length. The repo's own receipts had already documented
this (research_fanout docstring "max_tokens is generous because..."; TT3's big uncapped
answers; the operator's pasted deep-research transcript itself showed "Thought for 52s"
then deep content).

**How to apply:** omit max_tokens (or set it at/above the model's true output max) on any
generation call to reasoning models; never ladder caps incrementally — check finish_reason
on empties (finish=length = cap bug, finish=stop + empty = different problem); before
fighting a transport problem, sweep the fleet's own prior receipts — the operator expects
self-steal FIRST ("most of these are solved problems").

**Byte conviction (2026-09-17 receipts):** under the old caps, qwen and ministral returned
out_max of EXACTLY 900 tokens (pinned at provider defaults, nuance clipped); uncapped
union-alpha averaged 1,760 out tokens at finish=stop. Same day a second correction landed:
"you kill them before nuance can be obtained — the whole idea of our game was to let AI
emergently find novel solutions." The build-lane gate is a FITNESS FUNCTION, not a bouncer:
feed the model its own failed output plus the validator verdict verbatim and let it iterate
(6 generations per brief), never kill the search at generation one. Also: mine the prompt
cache — byte-stable fat CONTEXT prefixes (engine laws + verified examples + failure
glossary) get provider sticky-cached (z.ai receipts show cached=9247 on this exact shape;
TT3 pattern = context pack + growing turns).

**It was already fleet law, twice over:** (1) `models/providers.py::chat_provider` defaults
to max_tokens=65,536 with the 08-29 comment "mine the ceiling by default — callers opt DOWN
(JSON verbs, probes); never up from crumbs"; (2) the fleet's own no-cap mechanism predates
my re-derivation — see [[dogfood-canonical-machinery-20260917]]. And the fitness-function
approach was vindicated same night: the evolution loop promoted 2/2 briefs on generation
ONE after one-shot drafting went 0/8 ([[ruins-go-shipped-20260917]]).

Related: [[ox-alpha-was-glm53-flash]], [[self-steal-deep-thinking-invocation]], [[ruins-go-shipped-20260917]].
