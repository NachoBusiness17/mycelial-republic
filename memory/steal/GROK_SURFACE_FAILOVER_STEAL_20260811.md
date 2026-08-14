# STEAL — provider/surface failover invariant (grok dispatch fix) (2026-08-11)

## Trigger
Operator correction: "i don't have a free grok" / "deepseek and two grok keys you nuked the rest".
The 1 failing dogfood probe (`grok_free.health`) was a FALSE PREMISE (a free grok surface that doesn't
exist), but it masked a REAL bug: grok dispatch didn't fail over to the paid API.

## SELF-STEAL (the invariant we already owned)
- `mag/grok_rightsize.call_grok` already implements **key-chain failover**: iterate
  [XAI_API_KEY, XAI_API_KEY_2, GROK_API_KEY, GROK_API_KEY_2], on 401/402/403 (auth / no-credits /
  balance-exhausted) roll to the next key; abort only on other HTTP/network errors.
- The invariant to steal: **fail over to the next viable surface on failure**, never return a
  failure while a fallback surface remains.

## The bug it fixed
- `call_grok_free` preferred the CLI harness and RETURNED its failure when the harness was present
  but the call failed/timeout — it only fell back to the API when the harness was ABSENT.
- Result: 9/9 grok calls logged `surface: cli, ok: false, fallback: false` — the frontier dispatch
  path never reached the two-key API.

## EXTERNAL-STEAL (mechanism, adapted — contract only)
- LLM router / provider-failover pattern: a router tries the cheap/free surface first, and on any
  failure (not just absence) falls through to the next tier/key. This is the standard "try-then-failover"
  shape (openai-compat routers, multi-provider gateways). We adapt the CONTRACT, not DNA: any harness
  failure -> call_grok (two-key chain). Cost-safe: the API is metered but is the REAL grok surface; a
  free surface that doesn't exist should never be a terminal failure.

## Adaptation (code)
- `mag/grok_rightsize.call_grok_free` now returns the harness result ONLY on success; on harness
  absence, call error, or timeout it falls through to `call_grok`, preserving the harness error as a
  `[harness-fallback: ...]` note. `harness` field stays `false` on API path (matches `fallback` semantics).

## Folds
- Folds as a doctrine node (failover-on-failure invariant). Reprobes dogfood `grok_free.health` once a
  funded key is in `.env` (operator-only secret: XAI_API_KEY_2 slot).
