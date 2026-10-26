# INTAKE CARD — @yohakujpn free-model list (2026-09-04)

**Paste**: https://x.com/yohakujpn/status/2095493136990527977
**Score**: 19/25 — **BUILD WINDOWED** (lanes receipted ALIVE; fuel_feed registration
routes to the driver, backup-first)
**Probed live from this seat** (own OpenRouter key from the shelf, $0, 3 calls):

| Lane (tweet claim) | Probe result |
|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | **ALIVE** — responded (thinking model, 550B-A55B MoE) |
| `minimax/minimax-m3` | **ALIVE** — responded via AtlasCloud; thinking model (reasoning field ate 16-token budget, finish=length; needs >=256 max_tokens) |
| `poolside/laguna-s-2.1:free` | EXISTS but **429 saturated** at probe time — classic OpenRouter free-lane congestion, retry later |

Chat doors named in the tweet (no API, REMEMBER lines only): DeepSeek V4 Pro
(chat.deepseek.com), Qwen 3.8 (chat.qwen.ai), GLM-5.3 (chat.z.ai — already our
house), Kimi K3 (kimi.com), Gemini 3.6 (gemini.google.com).

## Why it scores 19
- **FIT 4**: fuel_feed FREE_LANES exists; these bolt straight on (Calcifer
  precedent: z_ai3 relit into FREE_LANES pinned by model).
- **PULL 3**: 16 days to the Sep-20 wall + tranche-gated bay = free lanes are
  exactly the capacity class we want. A free 550B-A55B MoE is a real body for
  pennies-lane judgment jobs, not just sweeps.
- **COST 5**: $0, three probe calls.
- **WINDOW 4**: queue depth hungry now; night window is the build slot.
- **NOVELTY 3**: Nemotron-3-Ultra, MiniMax-M3, Laguna-S all absent from
  corpus/lane map.

## Routing (three verbs)
1. **BUILD WINDOWED** — register the two ALIVE lanes into fuel_feed
   FREE_LANES (pinned by model, backup-first, night window, driver owns the
   surgery — research window does not touch the fuel router). Laguna S goes
   on a re-probe schedule (429 = exists, not dead).
2. **REMEMBER** — Nemotron 3 Ultra 550B free = biggest free body on the
   board; candidate for dumb-judgment batches and salon N-posts where
   deepseek pennies currently go.
3. **REMEMBER** — MiniMax M3 quirk: reasoning-first output shape (content
   null until thinking completes) — same class as our 5.3 thinking law;
   max_tokens floor applies.

## Tri-state
- Lane aliveness: **Supported** (probe receipts above, bytes read).
- "Free forever": **Unproven** — OpenRouter :free tiers are quota/congestion
  bound and vendor-revocable (genre rule: repeat-promo = REMEMBER, never plan
  on stranger generosity).
- Chat-door model names (V4 Pro, 3.8, K3, 3.6): **Unproven** — not probed,
  marketing names until a byte touches one.
