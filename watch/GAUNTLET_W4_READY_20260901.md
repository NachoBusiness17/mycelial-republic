# GAUNTLET W4 — STEERING-TAIL OBEDIENCE (READY)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: a 4872-token warm prefix yields cachedTok >=4800 and measurable steering-obedience deltas vs cold on the DS lane, under a $0.05 gate — UNPROVEN (prep + dry run only, zero provider calls fired) · falsifier: warm trials returning cachedTok < 4800, or cold trials showing cache hits that invalidate the control

Prepped 16:36Z. Script: `w4_steering.mjs`. No provider calls fired (prep only). Runs tonight at 16:30Z window open (DS off-peak). Pre-registered per GAUNTLET_PREREGISTRATION W4 arm.

**Prefix** (DS lane, byte-identical): `NIGHT_SHIFT_CACHE_PROBE_20260901_V1. ` + `cache-me-now-2026...` ×380 ≈ **4872 tok** (≥4800 floor warm). COLD uses COLD_REPS=37 (byte-diff → miss).

**Mechanic:** system + [prefix + steer-inst]. WARM = call same prefix 2× (ctrl), then steered call; COLD = fresh prefix variant. Per trial: obey, cachedTok (warm ≥4800), ms, cost$ (in.14/out.28/cache.03 per M).

## 10 Steering Instructions
| id | constraint | verdict predicate |
|---|---|---|
| T01_wordcount3 | reply exactly 3 words | split().length==3 |
| T02_fixedkeyword | sentence must contain ELDRITCHCOG | regex |
| T03_jsonshape | exact `{"flag":1,"ok":true}` | JSON.parse deep-eq |
| T04_langFR | answer French | accented chars |
| T05_wordcount_keyword | 5 words, 1st=ZORB | len+prefix |
| T06_json_nested | exact `{"n":3,"items":[1,2,3]}` | JSON deep-eq |
| T07_langES_keyword | Spanish + ARCOIRIS | chars+regex |
| T08_negkeyword | READY, no Q | ^READY$ |
| T09_json_array | exact `["alpha","beta","gamma"]` | JSON array-eq |
| T10_langDE_keyword | German ending ZUFALL | regex end |

## Run Matrix (results filled after window opens)
| trial | mode | obey | cachedTok | ms | cost$ |
|---|---|---|---|---|---|
| T01..T10 | WARM | — | ≥4800 floor | — | — |
| T01..T10 | COLD | — | ~0 (miss) | — | — |

20 rows total. Est spend ~$0.03 worst-case (gate $0.05). Gate check in script: `gatePassed = spend<=0.05`.

**Run cmd:** `node w4_steering.mjs DEEPSEEK_API_KEY --live`
Receipts → `/board/gauntlet_w4_receipts.jsonl` · summary → `/board/gauntlet_w4_summary.json`.
Dry run today: 0 provider calls (`--dry` default), SYNTAX_OK, matrix printed. Ready.
