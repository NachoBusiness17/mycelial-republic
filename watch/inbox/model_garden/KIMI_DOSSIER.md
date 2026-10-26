# KIMI DOSSIER (lane 5, KIMI TESUJI) - model garden 2026-10-01

Class: RECEIPT (web research, no signup, no key created, no spend).
Writer: zcode seat, model-garden lane 5. All prices checked live 2026-10-01
(platform.kimi.ai docs fetch + openrouter.ai/api/v1/models JSON pull).
Budget before battery: zero. This dossier aims the probes; it fires none.

## LINEUP

Moonshot AI sells the Kimi family through an OpenAI-compatible REST API at
`https://api.moonshot.ai/v1` (chat/completions, tools, reasoning_effort;
Anthropic-style messages API and a Batch API also exist). The docs console is
platform.kimi.ai (platform.moonshot.ai 301-redirects there). Current ladder,
flagship first:

| Model ID | Ctx | Direct price per M (in miss / in hit / out) | OpenRouter price per M (in / out) | Notes |
|---|---|---|---|---|
| kimi-k3 | 1,048,576 | $3.00 / $0.30 / $15.00 | $0.415 / $10.00 | 2.8T param open-weight MoE (Stable LatentMoE, 896 experts, 16 activated, ~104B active per token), Kimi Delta Attention, native vision, thinking always on (reasoning_effort low/high/max, default max), dynamic tool loading, official /tools + /fibers. Weights open (blog: full weights by 2026-07-27) |
| kimi-k2.7-code (+ -highspeed) | 262,144 | $0.95 / $0.19 / $4.00 (highspeed $1.90 / $0.38 / $8.00) | $0.671 / $3.35 | Coding-focused end-to-end agent model, MIT license per release coverage; released June 12 (2026) |
| kimi-k2.6 | 262,144 | $0.95 / $0.16 / $4.00 | $0.434 / $1.828 (cache-read $0.073) | K2-line agentic flagship, thinking mode, 1T MoE ~32B active, positioned for multi-agent coding (300-agent swarm demos) |
| kimi-k2.5 | 262,144 | - | $0.45 / $2.25 | Native multimodal, "visual agentic intelligence", agent-swarm paradigm |
| kimi-k2-thinking (k2-0905) | 262,144 | - | $0.60 / $2.50 | Reasoning variant; 71.3% SWE-bench Verified at release, topped the official SWE-bench leaderboard (Nov 2025) |
| kimi-k2 (Jul 2025) | 131,072 | - | $0.57 / $2.30 | The original: 1T MoE, 32B active, 65.8% SWE-bench Verified |

Notable platform extras: file APIs (extraction + storage) are "temporarily
free" on the direct platform; $web_search tool has separate billing. No
`:free` Kimi variant exists anywhere in the live OpenRouter listing (checked
in the models JSON this session).

## PUBLIC-VERDICTS (cited)

Strengths:
- K2.6 agentic scores: SWE-bench Verified 80.2%, SWE-Bench Pro 58.6% (up from
  50.7 on K2.5), Terminal-Bench 2.0 66.7% (up from 50.8), Toolathlon 50.0,
  MCPMark 55.9, tau2-Bench Telecom ~96%, Artificial Analysis GDPval-AA Elo
  1520, ranked leading open-weights model (aggregator kimi-k25.com/blog/kimi-k2-6-benchmark
  + Artificial Analysis; third-party aggregator numbers, directionally
  consistent with Moonshot claims).
- K3 (official blog kimi.ai/blog/kimi-k3, tech report arXiv:2607.24653):
  DeepSWE v1.1 67.3 (mini-SWE-agent); BrowseComp 90.4 using the full 1M
  window with no context management; autonomous 48-hour chip design +
  verification run (Nangate 45nm, 1.46M cells); reproduced I-Love-Q
  computational-astrophysics relations in ~2h from 20+ papers.
- K2 base paper (arXiv:2507.20534): tau2-bench 66.1, SWE-bench Verified 65.8,
  i.e. the whole K2 line has been tool-use-shaped since day one.
- Price:capability: K2.6 on OpenRouter at $0.434 in / $1.828 out undercuts
  every frontier judgment model by an order of magnitude per output token.

Weaknesses (cited):
- Tool selection degrades when the tool set is large: documented in a Trilogy
  AI review of the K2.5/K2.6 line. Directly relevant to our fat-tool-surface
  harness asks.
- Business/knowledge work weaker than frontier closed models (Ethan Mollick's
  hands-on notes on K2.5).
- K3's OWN stated limitations (kimi.ai/blog/kimi-k3): (1) thinking-history
  sensitivity, unstable output if the harness omits historical thinking or a
  session switches models mid-stream; (2) excessive proactiveness, improvises
  decisions on ambiguous intent unless the system prompt constrains it;
  (3) "a noticeable gap in user experience compared with Claude Fable 5 and
  GPT 5.6 Sol", i.e. it trails the top proprietary models overall.
- K2.5 shipped without a formal safety report (independent arXiv safety
  evaluation noted the absence).

## ESTATE-FIT

Box: 6GB AMD, no CUDA. Self-host is zero-option: original K2 is 1T params
(32B active), K3 is 2.8T with a >=64-accelerator recommended deployment; no
quantization puts any Kimi inside 6GB. Kimi is REMOTE-ONLY for this estate,
which matches the doctrine (local janitors stay gemma; specialists are scarce
remote). No local-lane displacement.

Stack: OpenAI-compatible REST at api.moonshot.ai/v1 = drop-in for our httpx
call shape and existing OpenAI-compat adapters (same door pattern as the xAI
SD account). The OpenRouter route is one base-URL swap (api.openrouter.ai/v1).

Jobs:
- Duel judging: serial low-RPM cadence. Moonshot direct Tier0 (1 concurrency,
  3 RPM, 500K TPM, 1.5M tokens/day) technically fits a judge loop, but see
  ACQUISITION-DOOR for why direct is the wrong door for us. K2.6 at
  $0.434/$1.828 is the cheapest credible judge-graded verdict in the garden.
- Code fixes: k2.6 / k2.7-code, 80.2% SWE-bench Verified class.
- Extraction: 262K ctx swallows our largest single receipts; direct platform
  file APIs are temporarily free (direct only, not OpenRouter).
- Agentic harness work: the signature. tau2-class tool discipline plus
  dynamic tool loading is the one axis where Kimi measurably leads every
  open-weight peer and pressures the closed frontier.

Harness caution: K3's thinking-history sensitivity collides with multi-turn
harnesses that strip reasoning between turns. Our duel/effect-broker loops
reuse prompt scaffolds across turns and would trip exactly that. K2.6 (thinking
as a mode, not a mandatory preserved channel) is the safe arm; if K3 is ever
armed, the harness must preserve thinking history verbatim.

THE CANDIDATE: kimi-k2.6 via OpenRouter. Top open-weight agentic scores
without K3's thinking-history fragility, 256K window, cheapest capable output
line in the family ($1.828/M out, 5.5x under K3's $10), and cache-read at
$0.073/M rewards our repeated-scaffold judging/audit prompts.

## ACQUISITION-DOOR

Direct (platform.kimi.ai) - documented, NOT executed (no signup per mission):
1. platform.kimi.ai console, email or Google sign-in.
2. No free trial credits documented anywhere in the billing FAQ.
3. Hard gate: recharge at least $1 to unlock API use at all (Tier0: 1
   concurrency, 3 RPM, 500K TPM, 1.5M tokens/day).
4. Individual top-up rails are WeChat Pay and Alipay QR codes (China-focused;
   painful from this operator's US seat). Business path = sales team / bank
   transfer. Tier ladder is cumulative recharge ($10 = Tier1, 15 concurrency
   and 100 RPM; up to $3,000 = Tier5). Vouchers do not count toward tiers.

Aggregator (OpenRouter) - the recommended door for this estate:
- Live 2026-10-01 from openrouter.ai/api/v1/models: moonshotai/kimi-k2.6 at
  $0.434/M in, $1.828/M out, 262,144 ctx, cache-read $0.073/M; kimi-k3
  $0.415/$10.00, 1M ctx; kimi-k2.7-code $0.671/$3.35; kimi-k2.5 $0.45/$2.25;
  kimi-k2-thinking $0.60/$2.50; kimi-k2 $0.57/$2.30.
- No :free Kimi variant in the live listing. Standard OpenRouter account with
  prepaid USD credits (card/crypto), which we already know how to operate.
- OpenRouter also sidesteps the China payment rails AND the concurrency tier
  ladder entirely.

Free-key verdict: NO. Direct needs $1 minimum plus WeChat/Alipay; OpenRouter
has no free Kimi listing. Cheapest real entry is a few dollars of OpenRouter
credits pointed at kimi-k2.6.

## THE TESUJI

Arm kimi-k2.6 through OpenRouter as the estate's designated audit-chain
agent: the effect-broker verification walk (read receipt, verify sha256
against INDEX.json, cross-check the shared-surface contract, then
authorize/deny the effect) plus the STEALTH_MINED_FINDINGS.jsonl triage
(241,657 bytes, fits whole inside its 262K window) on the same dispatch,
replaying the contract + index scaffolds every turn at cache-read $0.073/M,
so the judgment primes stop burning premium tokens on mechanical multi-tool
walks that Kimi does better and cheaper (tau2-class discipline, 5.5x cheaper
output) while judgment itself stays exactly where the driving ladder put it.
That is the move our current stable cannot make: glm-5.3-prime, qwen3.8-max
and grok-4.7 are judgment seats; none of them is a measured open-weight-best
tool-walker, and the estate's own law says model text proposes while the
switchboard authorizes, which is precisely a tau2-shaped job description.

## Sources

- platform.kimi.ai/docs/pricing/chat (model table, cache pricing)
- platform.kimi.ai/docs/pricing/limits (tier ladder, $1 gate)
- platform.kimi.ai/docs/guide/account-and-payments (no free credits, WeChat/Alipay)
- platform.kimi.ai/docs/guide/kimi-k3-quickstart (base URL, OpenAI-compat, reasoning_effort)
- openrouter.ai/api/v1/models (live JSON pull 2026-10-01, prices + ctx + no :free)
- kimi.ai/blog/kimi-k3 (K3 arch, benchmarks, stated limitations)
- arXiv:2607.24653 (K3 tech report: 896 experts, 16 activated)
- arXiv:2507.20534 (K2 paper: tau2 66.1, SWE-bench Verified 65.8)
- kimi-k25.com/blog/kimi-k2-6-benchmark + Artificial Analysis (K2.6 scores, third-party)
- Trilogy AI review (large-tool-set weakness); Ethan Mollick (business-task weakness)
