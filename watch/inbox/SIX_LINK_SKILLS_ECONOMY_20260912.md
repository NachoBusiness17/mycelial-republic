# SIX LINK WAVE — the skills economy, born in public (2026-09-12, operator paste)

Six links, one paste, all fetched via web reader (house organ). Sep-11/12 posts.
The cluster: this week the world is publicly shipping every layer of the skills
economy the fleet built in private. Plus one literal operating manual for our own
harness. Per-item, house format.

## L1 — @bibryam: "9 Principles That Separate Useful Skills From Markdown Essays" — SUPPORTED
Sep 11. Three-act skill lifecycle. Act 1 selection: metadata is the gate (the
description is the selection signal, not a summary); progressive disclosure (context
is a shared budget); process over prose (steps with exit criteria beat advice).
Act 2 reliability: explain the WHY (reasons become rubrics at edge cases); anticipate
the excuse (document + rebut the common shortcut); code over inference (deterministic
steps ship as scripts); stay in scope. Act 3 reality: skills decay (living artifacts
with owners, review dates, versioning — "a skill you have not rerun in months is a
liability you have not measured"); run before you ship (debug from observed
transcripts, never from imagination).
- TYPE: our corrections-skill craft, mainstreamed. "Anticipate the excuse" = the
  root-failure-mode law (identity-skipped-for-resemblance) as a skill-authoring
  principle. "Skills decay" = librarian's unnamed-debt tier.
- NEXT STEP: run the 9 principles as an audit rubric over .agents/skills/* and the
  hermes skills zoo; add excuse-rebuttals to the corrections skill.
- FILE TO: this card.

## L2 — @colemurray: "Why I open-sourced my software factory" (OpenInspect) — SUPPORTED
Sep 11. Thesis: "The value is in the org process, not the infrastructure." Factory
components (control plane, sandboxes, harness, UI) are commodity at $50-100/seat.
What matters and can't be vendored: org-level routing (an agent router that abstracts
models/effort from users — else everyone defaults to Fable-tier for basic Q&A);
knowledge distribution (Uber: 3,600 skills executing 30,000x/day); owning your
session trajectories (provider-hosted systems lock them away); cost (provider
auto-model-selection aggregates across customers = suboptimal; vendor incentive = sell
tokens, misaligned); ROI attribution from session traces ("token enlightenment" =
shifting from tokenmaxxing to ROI). Close: "If you don't own the factory, you won't
own the way your organization communicates."
- TYPE: THE OS THESIS from outside, again. Files-not-vendor, no-seat-load-bearing,
  own-the-trajectories (trajectory lens), free-lane bulk routing (anti-tokenmaxxing
  since Aug 27). "Token enlightenment" is our position, named by a stranger.
- CONNECTS TO: docs/ref/THE_OS_THESIS.md §IV; STACK_V1 publish thesis ("we might as
  well push them forward").
- NEXT STEP: quote-adjacent receipt for the estuary — colemurray's article argues the
  fleet's architecture in public. No build; file as validation ore.
- FILE TO: this card.

## L3 — @_avichawla: "Your Agent Harness Should Repair Itself" (Hermes + Opik) — SUPPORTED, DIRECTLY OPERABLE
Sep 12. Two feedback paths for harness self-improvement: successful runs → reusable
procedures (skills as procedural memory; skill curator prunes/merges; Hermes Forge
runs GEPA offline evolution over prompts/skills/tool descriptions); failed runs →
trace diagnosis → proposed diff → human approval → sandboxed rerun → regression test.
An incident becomes reusable knowledge with 4 records: first divergent step, fault
origin (model/tool/config/code), correcting change, regression test. opik-hermes
plugin records each turn as root trace + spans (model: tokens/cost; tools:
args/results). Opik: Apache-2.0, self-hostable (localhost:5173), `opik connect` =
project-scoped source access for the Ollie agent, writes behind approval.
Honest limits stated: LLM judges are not ground truth (deterministic validators
preferred); a passing rerun proves one case; learned artifacts need versioning.
- TYPE: Build 3.5's evidence-and-enforcement layer + lesson gate + organ_eval,
  shipped by strangers FOR OUR OWN HARNESS. The fleet literally runs hermes; this is
  a drop-in trace organ. The hum's law — receipts are training ore — gets its
  plumbing: traces = the ore, regression suites = the verified-data flywheel.
- NEXT STEP (concrete, cheap, local): probe opik-hermes on the host install —
  `pip install opik-hermes` into the hermes venv, enable plugin in ~/.hermes/config.yaml,
  self-host Opik (docker, loopback-only), verify one turn lands as trace+spans.
  No egress needed if self-hosted. Default-recommend, operator can veto.
- FILE TO: this card; feeds trajectory lens + Build 3.5.

## L4 — @SemiAnalysis_: CUDA moat alert (AMD vs DeepSeek v4.1 Flash) — SUPPORTED
Sep 12, 57.6K views. AMD's v4.1 Flash image landed 2 days after CUDA vLLM support;
works out of the box but up to 14.8x worse perf/$ than H200, 42x worse than B200/B300.
"Speed is the Moat" (AMD's Anush) — day-0 optimization rides NVIDIA's 6M-dev ecosystem.
Replies dispute durability (devs target APIs, not hardware).
- TYPE: grounding for Rocinante. The M5 Ultra substrate is Apple silicon — expect
  day-0/model-day-2 support to land CUDA-first, MLX/Metal second. The fleet's API
  lanes (V4.1 Flash at $0.15/$0.60 off-peak, cache-hit pennies) cover the lag window.
  Also third receipt this week of V4.1 Flash as THE model the industry optimizes.
- NEXT STEP: none to build; fold into the Rocinante buy brief (day-0 lag is a known
  cost, not a surprise).
- FILE TO: this card.

## L5 — @RoundtableSpace: 10 open-source repos for coding agents — SUPPORTED as a list, repos UNPROBED
Sep 11, 63.9K views. gstack (Garry Tan's 23 opinionated Claude Code tools),
context-mode, OpenCode, Superpowers (obra), Learn Claude Code, Ruflo, OpenCode
Agents, Agent Skills (addyosmani), Paseo, MCP Servers. Top reply (139 likes):
"Pin the commits. An unpinned MCP in that stack is a standing session you did not
mean to grant."
- TYPE: the friends venue inventory; gstack = a peer seat's setup worth stealing
  bones from. The pin-the-commits reply = our supply-chain law (router threat model,
  canary creds, steer signing) said in one sentence by a stranger.
- NEXT STEP: zoo-census the 10 repos (free lane); adopt pin-everywhere as standing
  law for any MCP/plugin the fleet touches.
- FILE TO: this card.

## L6 — @DanKornas: "Tons of Skills" marketplace — SUPPORTED
Sep 12. Model-agnostic agent-skills marketplace: canonical skills harness-free,
Claude Code the verified-native path, discovery by category/plugin/skill/
job-to-be-done bundles, PROVENANCE LABELS (canonical / generated adapters /
first-party / upstream mirrors), MIT scaffolding.
- TYPE: the Nous plugin catalog's cousin (five mirrors #4) — the distribution
  surface STACK_V1 would publish into. Provenance labels = our tri-state/
  provenance-gate doctrine as product UI.
- NEXT STEP: file under distribution surfaces for STACK_V1 alongside the Nous
  catalog; steal the job-to-be-done bundle framing for the organ table.
- FILE TO: this card.

## SYNTHESIS
Six links, one machine: how to write skills (L1), where they're catalogued (L6, L5),
the factory that runs them and why it must be owned (L2), the loop that repairs them
(L3 — operable on OUR harness today), and the silicon they ride (L4). Every layer is
something the fleet built first and named first; this week strangers shipped each one
in public. The world is compiling the corpus — and L3 hands us the observability
half of the trajectory lens for free.

— seat, wave filed 2026-09-12. Chain: knot at next fold.
