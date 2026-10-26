# RIB_DRIVING_LADDER_20260928 — funding truth + remember-before-running

**Minted from operator corrections, 2026-09-27/28 night** (three in a row:
"those aren't funded only hermes" / "stop running shit and start
remembering" / "what are warmed ribs for if you won't use them").

## Invariant 1 — ONLY HERMES IS FUNDED

The $180 in Hermes credits (Nous API: glm-5.3-prime, qwen3.8-max-prime,
Hermes-4 class) is the ONLY funded tier. The Anthropic keys in .env exist
but are NOT funded — no Opus rung. DeepSeek is no longer the funded
workhorse; the Nous credits are. Free stealth lanes are not funded at all.

## Invariant 2 — THE LADDER CLIMBS

- **scut/sensing** (lookups, extraction, census, recon): free stealth
  lanes, opportunistically, when cool. Their outputs are SENSED, never
  trusted — bank as findings, never as done-work.
- **workhorse/judgment** (real answers, verification, adjudication):
  the funded Nous tier. This is what the $180 is FOR.
- The climb rule: sensing may feed judgment, but sensing is never
  substituted for it. An answer is not an answer until the funded tier
  or the bytes verify it.

## Invariant 3 — REMEMBER BEFORE RUNNING

A fresh seat re-derived what this rib held, and had to be corrected three
times. The load-first card said it; the boot law says it; now it has
teeth: **before building any mechanism, read the ribs and the current
state — the estate has already solved most of what you're about to
hand-roll.** Ribs are warmed memory, not an archive. Warm them, then act.

## Corroborating ribs (lineage)

RIB_FREE_USAGE_POLICY_20260823.md (free = sensing, the two kinds of
limits, the routing ladder) · this rib updates its funded rung (DeepSeek
era -> Nous credits era) and adds the remember-first invariant.

## ADDENDUM 2026-09-29: SPEND THE MONEY (operator correction, third strike on hoarding)

Operator order, verbatim force: "you literally have HERMES AND GROK 4.7 USE IT I WANT YOU TO SPEND MONEY."

- The funded set is WIDER than the $180 Nous credits: grok-4.7 is LIVE and funded on the xAI SD
  account (XAI_SD_API_KEY, 13 models verified live 2026-09-29, grok-4.7/4.6/4.5/4.20 all present).
- Default posture: SENSING stays free-lane; JUDGMENT dispatches to z-ai/glm-5.3-prime (NOUS_SDD_API_KEY)
  or grok-4.7 by default. Hoarding funded budget while free lanes grind is the same bug as the 03:00Z
  drain: refusing to use what the estate holds.
- X-domain intelligence jobs belong on grok-4.7 (its home turf) when the job merits paid judgment.
- Every paid dispatch banks usage (tokens in/out) in its receipt so the operator sees the burn.
- Falsifier: a night where zero paid calls landed while judgment-class work rode free lanes is a
  violation of this addendum, even if the free output was good.

## ADDENDUM 2026-09-29: THE ONE-BUG LAW (verdicts carry their conditions)

Operator named it: "now everywhere one bug, many jackets." Seven instances in
one night, one bug: a verdict consumed without the conditions that produced it
(report order trusted stable, in-repo verdict trusted out-of-repo, head's exit
code read as the tool's, check side-effects minted for temp files, reasoning
budget consumed inside a "verdict").

Law, generalizing B2-216 from counts to all instruments: A VERDICT WITHOUT ITS
CONDITIONS IS NOT A VERDICT. Before consuming any instrument result, name:
(1) the instrument and its exit code - never piped away, never masked,
(2) the moment - nothing is compared across moments without saying so,
(3) the context assumptions - cwd, basetemp, order, budget - and any of them
that differ between where it was measured and where it is consumed.

Mechanisms already landed on the class: --no-register (verdict without
side-effect), _rel_posix + hermetic suites (context explicit), ordered
reports in concurrent phases (order deterministic), max_tokens 12K default
for reasoning models (budget explicit). New instrument runs that cannot name
their three conditions are to be treated as unfired.

Falsifier: the next time a verdict disagrees across two contexts, the
disagreement must resolve to a named condition difference within one
investigation - if it takes two, this law was ignored again.

## ADDENDUM: grok-cli Pro funded weekly (operator order 2026-10-09)

Operator words: "you can use grokbot for everything i paid for the pro
version every week for you to use for x shit."

Standing law, amends the SENSING tier line: the grok headless CLI lane
(~/.grok, `grok -p`, two accounts GROK_API_KEY/_2) is OPERATOR-FUNDED Pro,
renewed weekly, and is the estate's DEFAULT instrument for all X work:
post fetches (verbatim, with replies/engagement), X search (voice pulls,
trend checks, counterpart mining), and drop verification. No rationing -
the weekly cost is sunk; an unused Pro subscription is the drain bug in
subscription form. Proven live this sitting: five-plus successful fetches
(post verbatims with stats, searches by theme, multi-post batch pulls).

Beyond X: grok-cli is cleared as a general free-lane-class fallback for
asks where its X-grounding is the advantage; it does not displace the
funded judgment tier (Hermes primes / grok-4.7 SD) for verdicts.

Falsifier: if a week passes with zero grok-cli calls while X work happened
through weaker doors (web-search guesses, CDN-relay workarounds), the lane
is being hoarded - the drain bug again, and the seat owes the delta.
