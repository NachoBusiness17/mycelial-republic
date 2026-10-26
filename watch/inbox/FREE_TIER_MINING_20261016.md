# FREE-TIER MINING - day one yield, lessons, and the OC-days synthesis (2026-10-16)

Classification: CARD (status + design; the OC alpha-days self-steal applied to the free-lane miner)
Producer: zcode-seat-20261016

## Day one, in bytes (memory/runs/hermes_burn/usage.jsonl)

10 ledger rows, 5 landed, 5 failed, $0.00 total. Tokens: 16,018 prompt /
22,435 completion (17,327 of it reasoning - the free reasoning model thinks
more than it writes). Landed: register triage, STUDY A instrument, STUDY B
coverage-receipt design, A2A pattern card, interpretive triangulation.
Failure classes, in order of discovery: 403 wrong-path (endpoint shape,
fixed), length/empty-reasoning (reasoning-mode model burned the whole budget,
fixed by family switch), 429 rate limit (NEW - rolling window, needs
minutes-scale backoff, wired this sitting).

## What we learned on day one

1. Yield is real: five usable sensing-grade deliverables per day at $0, from
   ONE host, ONE key, ONE serial lane, fed by six asks.
2. Free reasoning models eat budgets: 73% of completion tokens were
   reasoning; an unpriced SKU with a reasoning habit needs the family-switch
   reflex, not bigger max_tokens.
3. Endpoint shape is part of the config: the /api/v1 vs /v1 lesson (Cloudflare
   1010) means provider quirks are code-level facts, not config trivia.
4. Free tiers rate-limit per model+key on rolling windows: the 429 is a HOLD
   signal - the exact finding the OC width law predicted.
5. Everything landed is SENSING-grade: the triage invented commands, the
   triangulation echoed its evidence. The verification leg is not optional.

## SELF STEAL: the OC alpha-days swarm research, mapped

What those windows actually established (Aug-Sep, the 24-agent refreshes, the
50-lane experiments, the envelope measurements):

| OC-days finding | application to the free-lane miner |
|---|---|
| width envelope law: Task agents clean at 3/6/10/12 wide, 10-wide = 109.4M tok/h; workflow children die on first 429 (maxAttempts 0); after a burst even 12 takes 1302s to decay | the miner is SERIAL today; width is available and free to experiment with ($0 retries) - go 3-wide, measure the 429 rate, widen per measurement |
| first 429 = HOLD signal, not a width cut | the 429 backoff fix (wired this sitting: 120s on 429 vs 20s generic) |
| the 50-lane experiments STARVED: "we burned next to nothing", "why aren't we keeping 50" - width without feed is idle | the miner's feed is the standing information queue (oracle verifications, task-bank literature, GSTD-adjacent research) + preregistered studies; seed it or the width is theater |
| the ghost seat's guardrails: loop-detection circuit breakers (warn 8 / critical 15 / global 24), context pruning (cache-ttl, soft trim 25% / hard clear 50%), compaction safeguard, message queue (cap 6, drop=summarize) | the miner needs the SAME breaker class: the empty-reasoning failure is a loop the breaker should catch at the ledger level (reasoning >> completion and empty channel -> instant family switch, not a minted ask-id) |
| 13 persona agents (economist, elder, archivist, ractor...) | persona-tag the queue: ask classes route to model families (design -> gemma-class, long-context -> nemotron, triage -> lightning) |
| Z15 self-emission cap: the swarm must not prey on itself | the miner never mines its own outputs as input without the review pass |

## Make it useful to our ends - three wires

1. BACKOFF (wired this sitting): 429 -> 120s, per the HOLD law.
2. WIDTH (staged, ~30 lines): a --width flag firing the queue N-parallel,
   start 3, measure, widen - the envelope law's method, on free rails where
   experiments cost nothing.
3. FEED (staged): seed the standing queue as persona-tagged ask dirs - the OC
   swarm revived on free rails, pointed at the surfaces map's standing
   information queue. Then the evaluator: FDE-Gym-style penalty scoring
   (customer metric + message/trial/time costs) so mined findings carry a
   QUALITY number, closing the sensing-to-certified gap honestly.

## Falsifier

If widening to 10 parallel raises the 429 rate without raising the landed
rate, the free tier's envelope is narrower than the paid rails were - the
width law gets a free-tier annex with the measured number, and the miner
stays at the measured width. If a week of mined asks lands without any being
folded into an organ, this is mining theater - kill the miner, keep the feed.

## EVENING ADDENDUM: the Gemini lanes (operator push: "are you burning anything")

- The surfaces map row is STALE: gemini-2.0-flash on the old key is DEAD
  (404, "no longer available"). The daily retest finally won:
  **gemini-3.8-flash is LIVE** on the old key via native generateContent
  (the free-keys probe wanted this lane on 10/14; it was 503 then).
- Caveat: the OpenAI-compat POST path HANGS on this key (GET models works,
  native generateContent works) - so the carrier cannot drive it until a
  small native-shape adapter exists. Staged.
- First estate ask landed the same hour: the falsifier-default law draft
  (G3 of the shapes card) at
  `watch/inbox/hermes_burn/GEMINI38_FALSIFIER_DEFAULT_LAW.md` - 1,740
  tokens, $0.00, sensing-grade.
- "Argon" decoded: google/gemini-4-argon exists on OpenRouter but is PAID
  ($2/M prompt; :batch variant $1/M - the wide-mining shape if keys
  ever carry credit). Not a free lane.
- Burn accounting for the day, all lanes: openrouter free 38.5K tokens
  (5 landed / 5 failed, $0.00), z.ai 8-token ping, gemini-3.8 1,740 tokens
  (first work ask), gemini web/desktop not driven this sitting. Argon
  unburned (paid).

## NIGHT ADDENDUM: the GEMINI CLI LANE (installed, authed, warm-booted)

- @google/gemini-cli 0.64.0 installed via npm (node v22 present). The
  ghost-era `scripts/gemini_warm_pack.ps1` clipboard script is OBSOLETE:
  the CLI reads the repo directly.
- Auth: GEMINI_API_KEY (free tier - 5 RPM thin, today's burns ate the
  window). The UPGRADE is the operator's one browser click per account:
  "Login with Google" as sf Pro and nacho Pro = elevated limits x 2
  accounts. Workspace trust: GEMINI_CLI_TRUST_WORKSPACE=true (or trust the
  dir interactively once).
- WARM BOOT PROVEN same hour: `gemini -p` read README.md (the standing
  wave) and answered the boot triad (position / live lane / owed) from
  bytes. The CLI respects .gitignore - state/ files are invisible to it
  (beacon content rides in tracked files: README.md, the receipts).
- Fleet shape: `gemini -p "<ask>"` one-shots are the drivable unit - the
  miner, the queues, and the persona palaces can all fire through this
  lane. The two Pro accounts make it TWO lanes with elevated limits.
- Provenance: the lane was proposed by GEMINI ITSELF (the web session
  drafted its own induction: npm install, warm-boot patterns, the python
  wrapper option declined as redundant). Self-steal confirmed: the
  ghost-era warm-pack script and the surfaces-map Gemini rows already
  held every piece; the CLI is the missing renderer.
