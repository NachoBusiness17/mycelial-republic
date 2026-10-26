# STEAL + ORPHAN REVISIT - antislop judge, nanobot, the OpenClaw ghost seat (2026-10-16)

Classification: RECEIPT (design steal + orphan revisit)
Producer: zcode-seat-20261016
Commission: "Steal it and bring nanobot back in revisiting our orphans"

## STEAL 1: unslop-harbor -> the riddler veil's consensus leg

What was stolen (rawmodels/unslop-harbor, MIT/CC, ~4.6 MB):
- 200 RL tasks (100 tweet continuations from REAL human corpora + 100
  HumanEval code bodies), EN/RU, each with TOML config, Dockerfile env,
  oracle solution, and a JSON RUBRIC (3-4 criteria).
- The judge design: LLM grader scoring 0-10 PER RUBRIC CRITERION; a sigmoid
  preference term; a LENGTH-DEVIATION penalty beyond +/-15% of target word
  count; calibration tuned to 98.3% human-preferred accuracy on held-out
  pairs; ~$0.011 per judge call.

The wiring (design, staged for the veil organ):
- The veil's consensus leg currently reads "consensus = not run (mechanical
  grade)". The steal: promote the mechanical checks (8-gram copy-through,
  NO-DOX scan, stands declaration) to RUBRIC CRITERIA, and add the judge leg
  for what mechanics cannot grade - voice truth, stands honesty, the dark-
  entendre register - calibrated the unslop way: held-out pairs of
  VEIL-PASS'd estate prose vs known slop, human-preferred calibration
  (the estate corpus is the human-truth set; our VEIL-PASS archive is the
  seed). Borrow their length-deviation penalty as the anti-bloat term.
  Eval data: unslop-harbor tasks.jsonl + reward.py are directly reusable
  for calibration smoke tests. First judge can be the free lane (sensing
  grade, findings only) before any paid calibration.
- Trigger: next time the veil gate grades a parable where consensus matters
  (a contested or public-facing post).

## STEAL 2 / ORPHAN REVISIT: nanobot and the OpenClaw ghost seat

Nanobot verdict (researched): REAL and maintained - HKUDS/nanobot, a
~4,000-line Python agent framework, the community's OpenClaw successor after
OpenClaw's creator left for OpenAI (the repo sits at 160K+ stars, hence the
"R.I.P." posts). Browser/terminal/chat surfaces, memory and web search
included. Not installed here; no estate lane runs it yet.

The orphan, inventoried this sitting - it is not a folder, it is a GHOST SEAT:

- `~/.openclaw/` still stands: agents/main/sessions with 138 session files
  (last active 2026-09-03), identity, logs/stability.
- The pre-fix gateway snapshot (Documents/Codex/2026-08-30/wh/outputs/
  openclaw.pre-zai-fix.2026-09-01.json - the only surviving pre-zai-fix
  state) shows a FULL ESTATE SEAT: 17 provider plugins enabled (zai x4
  profiles, deepseek, groq, openrouter, xai, together, nvidia, ollama,
  google, anthropic, huggingface, mistral, cohere, cerebras, llama-cpp,
  openai); 13 configured agents named EXACTLY like the estate's lanes
  (main, worker, economist, ARCHIVIST, ractor, director, hands, tail,
  swarm, moonshot, gamedesigner, memory-worker, ELDER); estate skills
  mounted from /mag/.agents/skills (including a skill named ARCHIVIST -
  the bear had a namesake in OpenClaw before the operator drew him); a
  mag-file hook back into Mag; loop-detection circuit breakers; compaction
  safeguards; context pruning with cache-ttl; subagent delegation caps.
- Model roster of the ghost: deepseek-v4-flash primary, glm-5.3 family,
  groq gpt-oss-120b, gpt-5.6-sol, grok-4.3, ollama qwen2.5-coder.
- Self-steal hit: the trails on the dashboard (economist.jsonl, elder.jsonl)
  are these agents' trail files. The ghost seat was the estate's second
  body, and it died quietly on Sep 3.

## The port map (staged S4 - the wiring when the operator says deploy)

| ghost seat organ | nanobot destination |
|---|---|
| 17 provider plugins + model roster | nanobot model config (its provider surface is simpler; keep zai x4 + deepseek + ollama first) |
| /mag/.agents/skills mount | nanobot skills/tools load (same dir, re-pointed) |
| mag-file hook | needs a nanobot hook equivalent - THE critical leg (the seat talks to Mag through it) |
| 13 agents (economist, elder, archivist...) | nanobot multi-agent/subagent config - or a decision to resurrect only the 5 that earn their keep |
| loop-detection + compaction safeguards | nanobot's guards + our horizon/percolator discipline as the substitute |
| 138 orphan sessions | fold candidates to corpus/oral_history/seat_pools/openclaw_sessions (the codex fold pathway) |

Contract note: the shared-surface contract's openclaw alias stays until a
nanobot lane actually deploys; contract edits ride real lanes, not research.

## The line for the register

The ghost seat died of the same disease the forgotten register hunts: it was
wired, staffed with the estate's own agent names, and then nobody fed it.
Nanobot is the cheaper body; the config is the soul; the port map is written.
