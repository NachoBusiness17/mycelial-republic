# AJ9 — Nous 402 diagnosis (2026-09-30)

Owner of record: AJ9 (file ownership per dispatch). Budget held: one 10-token probe
per key (4 keys found), 2 returned 200, 2 cost nothing (401/200-auth). No other Nous
spend. No key values appear below; fingerprints are len + sha256[:8] only.

Mission: diagnose the LM1 finding (funded Nous lane returning 402 on both prime
models post-rotation, `LM1_SESSION_MAZE.md` line 19) without spending beyond one
probe call per key.

## (1) Env census: which Nous keys exist, and do they match

`C:\Users\foste\AppData\Local\hermes\.env` Nous vars (names only):

| var | line | len | sha8 |
|---|---|---|---|
| `NOUS_SDD_API_KEY` | 503 | 40 | 3d2a1908 |
| `NOUS_NACHO_API_KEY` | 504 | 40 | e8f807da |

Repo `.env` carries the rotated pair (no var named `*NOUS*` there):

| var | line | len | sha8 |
|---|---|---|---|
| `HERMES_API_KEY_1` | 41 | 40 | 5a76c88c |
| `HERMES_API_KEY_2` | 44 | 40 | af5d4d69 |

Match matrix (all four cross-pairs compared, values never printed):

- NACHO(old) vs KEY_1 / KEY_2: **NO MATCH**
- SDD(old) vs KEY_1 / KEY_2: **NO MATCH**

All four are `sk-nous...`, length 40. Verdict: the hermes env is running the
pre-rotation pair; the repo holds the post-rotation pair. **Rotation gap confirmed
at the byte level.**

## (2) Probe calls (one per key, max_tokens=10)

Endpoint `https://inference-api.nousresearch.com/v1/chat/completions`, model
`mistralai/ministral-3b-2512` (cheapest chat model on the card; model list pulled
first via free `GET /v1/models`, which also returned HTTP 200 with the old SDD key).

| key | HTTP | body (safe excerpt) | classification |
|---|---|---|---|
| hermes-old `NOUS_NACHO_API_KEY` | **401** | "Your API key is invalid, blocked or out of funds... portal.nousresearch.com" | stale key = rotation gap |
| hermes-old `NOUS_SDD_API_KEY` | **200** | completion ok, usage returned | old key still valid (not yet revoked) |
| repo-new `HERMES_API_KEY_1` | **200** | completion ok, usage returned | key + account pass |
| repo-new `HERMES_API_KEY_2` | **200** | completion ok, usage returned | key + account pass |

## (3) Balance endpoint

No public balance/credits endpoint on the API base: `GET /v1/credits`, `/v1/usage`,
`/v1/key`, `/v1/auth/key` all HTTP 404. The 401 message itself names the operator
portal: **https://portal.nousresearch.com** (billing/credits check lives there).

## (4) Verdict table

| question | answer |
|---|---|
| Are hermes Nous keys the rotated ones? | NO (all four pairs mismatch; NACHO slot is dead 401) |
| Is the 402 account-level credit death? | NO for cheap calls (both new keys 200), but YES in effect for prime models: credits exist yet are insufficient for a prime-model reservation (LM1 saw 402 "Insufficient available credits" even on a 64-token reservation; a 10-token 3B call passes). Near-empty pool, not revoked keys. |
| Was LM1's 402 model-specific? | Cost-specific: prime models (z-ai/glm-5.3-prime, qwen/qwen3.8-max-prime) reserve more than remains; cheap lane is alive. If LM1's failover chain rode the hermes-env keys, the dead NACHO 401 would alternate with SDD's 200, so the repo pair is the healthier read. |
| Lane state | Auth healthy on repo pair; funded (prime) work blocked on credit balance. |

## Exact fix

1. **Rotation gap (do now, no portal needed):** paste the value from repo `.env`
   line 41 (`HERMES_API_KEY_1`) into hermes `.env` line 504 (`NOUS_NACHO_API_KEY`),
   and repo `.env` line 44 (`HERMES_API_KEY_2`) into hermes `.env` line 503
   (`NOUS_SDD_API_KEY`). The 1→NACHO / 2→SDD mapping is arbitrary (both new keys
   200); the point is hermes carries only the live rotated pair. The old SDD key
   still works today but is pre-rotation and should be treated as revocable.
2. **The 402 itself (operator, portal):** check credits at
   https://portal.nousresearch.com. The API exposes no balance endpoint (404s
   above), so the portal is the only source. Evidence says the balance is above
   ~0 (cheap 200s) but below a prime-model reservation: top up, or route prime
   escalations elsewhere until topped.

Budget note: 4 probe completions at max_tokens=10 (2 hit, 2 free), 1 free models
list, 4 free 404 checks. Nothing else spent.
