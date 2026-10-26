# Steal card: open-and-local-language-models via reddit (round 1 draft)

Area: open-and-local-language-models via reddit. Drafted 2026-09-29 by the
steal gopher for this area. Two confirmed finds (confidence 0.9 each, from the
run's frontier intake; doors used per the ask: pullpush archive API and
safereddit redlib mirror after all direct reddit doors returned blocks). Every
repo claim below was re-verified in this session; anything not verified here
is marked OWED, never asserted.

## Find 1: tool-calling judgment head-to-head re-ranks the janitor slots

Source: https://www.reddit.com/r/LocalLLaMA/comments/1r4ie8z/i_tested_21_small_llms_on_toolcalling_judgment/
(r/LocalLLaMA, 2026-02-14, u/MikeNonect, score 89, 42 comments per this run's
session tape, memory/trajectory/steps.jsonl:34457).

Claim from the find: the Qwen3 family ranking is non-monotonic
(0.6B > 4B > 1.7B); qwen3:0.6b ties lfm2.5:1.2b first at 0.880 Agent Score in
Round 2 while gemma3:1b lands 19 of 21 at 0.550 and granite3.3:2b is 20th at
0.480. Harness: github.com/MikeVeerman/tool-calling-benchmark, 12 prompts,
CPU-class calls.

Verified this session:
- The repo is live: full_name MikeVeerman/tool-calling-benchmark, default
  branch master, 124 stars, pushed_at 2026-08-15T21:26:57Z (GitHub API
  HTTP 200, recorded on this run's tape at memory/trajectory/steps.jsonl:34462;
  the raw README fetch under main/ 404'd because master is the default branch,
  same tape line).
- The harness supports Ollama natively: backends "ollama" and "ollama_raw";
  runner is `python bench.py` after `pip install ollama requests`, with a
  `--num-runs 3` quick mode; Agent Score = Action x 0.4 + Restraint x 0.3 +
  Wrong-Tool-Avoidance x 0.3 where WTA = (3 - wrong_tool_count) / 3 (WebFetch
  of the repo README, this session).
- The live README score table has moved to a Round 3 (20 runs) table that no
  longer matches the find's Round 2 numbers: qwen3:0.6b 0.880, lfm2.5:1.2b
  0.920, gemma3:1b 0.690, granite3.3:2b 0.520, overall winner qwen3:1.7b at
  0.960 (same WebFetch). Non-monotonicity across Qwen3 sizes survives both
  rounds, but the drift between Round 2 and Round 3 is itself the argument
  for a local rerun instead of trusting any one table.

Estate grounding (the janitor doctrine is pinned in machine config, not
folklore):
- configs/lanes.yaml:6: "Doctrine: gemma:2b = scut; gemma4 = short worker
  bursts; specialist = judgment."
- configs/lanes.yaml:31-33: clerk, router, and orchestrator seats all ride
  gemma:2b (voice too, lane 36).
- configs/improve.yaml:299-300 and 316: brief clerk is gemma:2b ("janitor
  gemma:2b only"), worker is gemma4 short bursts.
- configs/seat_playbook.yaml:16-19: ollama_gemma4 seat, default_model
  gemma4:latest.
- Local endpoint: mag/cache_identity.py:78 OLLAMA = "http://127.0.0.1:11434";
  mag/afk_loop.py:98-112 already speaks /api/tags and /api/chat locally.

Estate map: feeds the GOPHER FLEET (the janitor slots clerk/router/
orchestrator/voice) and secondarily the SOVEREIGN MIRROR (more scut held
local instead of climbing the ladder, whose funded rung is Hermes/Nous only
per memory/rib/RIB_DRIVING_LADDER_20260928.md:7-23). Port move: clone the
harness, point bench.py at 127.0.0.1:11434, run gemma:2b, gemma4:latest,
qwen3:0.6b, lfm2.5:1.2b at --num-runs 3; if the Reddit ranking reproduces,
swap the clerk/scut slot in configs/lanes.yaml and file a percolator
invariant candidate ("janitor slots are assigned by measured Agent Score,
re-run quarterly", target memory/percolator/invariants.json); if it does not,
record the non-transfer and keep the fleet as-is.

Probe (falsifiable, cheap): the four-model local rerun above. Falsifier: if
gemma:2b or gemma4 matches or beats qwen3:0.6b on the same 12 prompts, the
Reddit ranking does not transfer to this box and no swap happens; if qwen3:0.6b
reproduces its edge (0.33 over gemma3-class in Round 2, 0.19 in Round 3), the
swap is earned. Cost: 12 prompts x 4 small models x 3 runs, CPU-class, well
under an hour. Any Windows wrapper process that spawns bench.py carries
creationflags=CREATE_NO_WINDOW per house law.

OWED for find 1: the scores are the poster's and the README's, not locally
reproduced yet; whether qwen3:0.6b and lfm2.5:1.2b pull clean on this box's
Ollama is unverified; the README's assumed clone dir (local-agent-bench) vs
the repo name (tool-calling-benchmark) is not reconciled against a real clone.

## Find 2: free rungs go dark without comms (Mistral)

Source: https://www.reddit.com/r/MistralAI/comments/1whurp8/so_does_anyone_actually_know_when_the_free_tier/
(r/MistralAI, 2026-09-16).

Claim from the find: the provider's free tier had been dark over a week with
no ETA comms, a commenter notes it was pulled from the incident page, and the
community advice is to keep a fallback free provider because free tiers get
revoked.

Estate grounding, both sides of the same event:
- configs/providers.yaml:19-21: "2026-09-26 roster purge (B2-61): nvidia,
  mistral, gemini REMOVED from the ..." with "mistral limit-0 + 403 tier" as
  the recorded cause. The estate independently observed the same dark rung
  ten days after the thread and purged mistral from the roster.
- memory/rib/RIB_DRIVING_LADDER_20260928.md:12 ("Free stealth lanes are not
  funded at all") and lines 14-23 (the ladder climbs; free stealth lanes are
  sensing-only, outputs banked as findings, never done-work): the policy this
  find corroborates from outside, in-window.

Estate map: feeds the RIB CORPUS and the PROVIDERS ROSTER (lane economics).
It does NOT map to the water graph: mag/water_computer.py:1-9 shows water is
the campaign hydraulics keep, so I decline to stretch a provider-liveness
steal onto that organ. Port move: fold the Reddit URL into the rib lineage
(the Corroborating ribs section of RIB_DRIVING_LADDER_20260928.md or the
RIB_FREE_USAGE_POLICY_20260823 lineage it updates) as a dated external
confirmation, and leave a pointer next to configs/providers.yaml:19-21 that
the B2-61 purge matches the community-reported outage window.

Probe (falsifiable, cheap): a 7-day daily HEAD to one live free stealth lane
endpoint (roster witness: configs/providers.yaml:181, stealth/space-bunny-alpha,
which self-describes as expiring "when stealth ends"), logged to a dated file.
Falsifier: if the lane stays lit all week, "revocation without comms" does
not generalize from Mistral and the rib needs no reinforcement; if it goes
dark and the log catches the day, the sensing-only law gains a dated internal
plus external receipt pair.

OWED for find 2: which endpoints the harness currently dials for free stealth
lanes was not read in this ask (only the roster comment at
configs/providers.yaml:181 was verified); configs/spend_overlay.yaml:93-94
still lists MISTRAL keys, and whether that overlay row is stale debris after
the B2-61 purge is unverified (candidate cleanup, owner owed).

## Novelty recheck (honest note on the ask's zero-overlap claim)

The ask reports a zero-hit grep for the find terms. My wider recheck ran:
rg -n -m 10 "MikeVeerman|FunctionGemma|qwen3:0.6b|lfm2.5|tool-calling-benchmark|tool-calling judgment"
over catalog memory mag configs docs tools. Result: hits only in (a) this
run's own session tape (memory/trajectory/steps.jsonl:33697 onward, sibling
actors fetching the same thread today, 2026-09-29), (b) one same-run sweep
intake row (catalog/catalog.jsonl:674068, a FunctionGemma paper title under
watch/inbox/frontier_olm_20260928/sweep/_raw/, mtime 2026-09-29T02:59:44Z),
and (c) an unrelated 2026-08-28 thinking trace mentioning qwen3:0.6b as a
CPU-inference idea (memory/thinking/app_reasoning.jsonl:2165). No curated
memory or knowledge artifact overlaps the finds. Novelty holds for curated
estate knowledge; the tape and sweep hits are this run's own exhaust.

## Citations

- Ask material: the two confirmed finds as delivered to this round (quotes,
  confidence 0.9, dates 2026-02-14 and 2026-09-16).
- https://github.com/MikeVeerman/tool-calling-benchmark (WebFetch this session)
- https://www.reddit.com/r/LocalLLaMA/comments/1r4ie8z/i_tested_21_small_llms_on_toolcalling_judgment/
- https://www.reddit.com/r/MistralAI/comments/1whurp8/so_does_anyone_actually_know_when_the_free_tier/
- configs/lanes.yaml:6,31-36; configs/improve.yaml:299-300,316;
  configs/seat_playbook.yaml:16-19; mag/cache_identity.py:78;
  mag/afk_loop.py:98-112; configs/providers.yaml:19-21,181;
  configs/spend_overlay.yaml:93-94; memory/rib/RIB_DRIVING_LADDER_20260928.md:7-23;
  mag/water_computer.py:1-9; memory/trajectory/steps.jsonl:33697,33744,34457,34460-34462;
  catalog/catalog.jsonl:674068; memory/thinking/app_reasoning.jsonl:2165
