# GSTD DOGFOOD DATA - first real usage through our node - 2026-10-09

DOGFOOD lane of the GSTD basecamp all-night workflow. Mission: "dogfoods it
through our systems" - generate the FIRST REAL USAGE DATA through our own
node. Raw bytes: `watch/inbox/gstd_basecamp_20260109/dogfood_matrix_raw.json`
(all 20 rows + warmups + counters, machine-written, nothing hand-copied).

Arms: GSTD = tunnel `https://procurement-unto-porcelain-baghdad.trycloudflare.com`
POST `/v1/chat/completions` (sovereign router path, model gemma:2b). BASE =
direct `http://localhost:11434/v1/chat/completions`, same model, same body.
Both arms share ONE engine: the container's OLLAMA_URL is
`host.docker.internal:11434` (override verified), so BASE is the same Ollama
the gateway proxies to. gemma:2b was warm before the matrix (kill-test task ran
it minutes earlier; BASE warmup answered in 185 ms; no cold load in any row).

## 1. The 20-row table (10 tasks x 2 arms)

Task material, all real estate bytes, read from disk by the harness script:
- S1/S2/S3 summarize: first 400 chars of `watch/inbox/disk_audit_20261009/OPERATOR_CORRECTION_GROWTH_CLAIMS.md`, `CRON_FREEZE_20261009.md`, `CHECKPOINT.md`
- C1/C2/C3/C4 classify: last 4 titled entries of `watch/inbox/LINKS.jsonl` (EmbeddingGemma 2 announcement, GPS VECTOR-KEY WIRE queue, GPS-EMBED falsifier verdict, OLM MINE day-7 fold), classified against the 17-animal vocabulary from `watch/inbox/ml_moonshot_20261007/ml3_route_table.json`
- E1/E2/E3 extract: last 3 raw lines of `memory/burns/LEDGER.jsonl` (keys ts, verdict, slug; truth: 18:30 steal, 19:00 steal, 19:30 green, all slug doctrine-owed-chase)

Quality is a 1-5 eyeball against the source bytes (rubric: 5 = fully accurate
and in-shape, 3 = right subject with factual slips, 1 = wrong or unusable).

| task | kind | GSTD ms | GSTD ch | GSTD q | GSTD note | BASE ms | BASE ch | BASE q | BASE note |
|---|---|---|---|---|---|---|---|---|---|
| S1 | summarize | 3758 | 137 | 4 | retry after 429; accurate retraction summary | 678 | 179 | 4 | accurate, 1 sentence not 2 |
| S2 | summarize | 7407 | 187 | 3 | retry 2 after 429; swaps the 2-paused/3-disabled numbers | 896 | 260 | 5 | both facts right |
| S3 | summarize | 5094 | 248 | 3 | invents "for 10 days", "verdict is positive" | 852 | 258 | 5 | accurate |
| C1 | classify | 3119 | 120 | 2 | honest refusal, no vocab member named | 370 | 97 | 1 | echoes the title, no member |
| C2 | classify | 303 | 120 | 1 | tier=cache: served C1's answer (collision) | 495 | 108 | 1 | echoes the title, no member |
| C3 | classify | 283 | 120 | 1 | tier=cache: served C1's answer (collision) | 240 | 33 | 1 | "embeddingGe", not in vocab |
| C4 | classify | 311 | 120 | 1 | tier=cache: served C1's answer (collision) | 322 | 35 | 3 | "qwen3.7-flash" = valid member, weak fit |
| E1 | extract | 2988 | 51 | 1 | retry after 429; key NAMES only, no values | 1113 | 126 | 5 | all 3 values exact |
| E2 | extract | 2889 | 72 | 1 | retry 2 after 429; key NAMES only, no values | 1076 | 110 | 5 | all 3 values exact |
| E3 | extract | 2983 | 91 | 5 | retry after 429; all 3 values exact | 928 | 120 | 5 | all 3 values exact |

Arm summaries:
- GSTD: first pass 4/10 served (2 queue tier + 3 cache), 6/11 tunnel requests
  429'd (5 rows + the warmup), all 5 recovered on paced retry (35 s backoff).
  Queue-tier latency mean 4034 ms on its 7 real-inference rows.
- BASE: 10/10 served, zero errors, all-10 mean 697 ms (min 240, max 1113).
- Head to head on the 7 tasks where GSTD did real inference: GSTD 4034 ms vs
  BASE 845 ms = 4.8x. Cache tier mean 299 ms but 3/3 wrong content (below).
- Quality means: GSTD 2.2/10 rows, BASE 3.5/10 rows. Per kind: extract BASE
  5/5/5 vs GSTD 1/1/5; summarize BASE 4/5/5 vs GSTD 4/3/3; classify both fail
  (GSTD 2/1/1/1 vs BASE 1/1/1/3) - that one is model-limited, not tier-limited.

## 2. Findings (byte-backed)

1. RATE-BUCKET COLLAPSE QUANTIFIED: 6 of my 11 tunnel requests 429ed
   ("Too many requests. Try again in 1 minute") at a self-rate of roughly
   16/min, far under the 120/min cap. Every host-originated and
   cloudflared-forwarded request shares one bucket keyed on the docker bridge
   IP 172.20.0.1 (gateway reads socket IP, no proxy-header trust), and
   unattributed external tunnel traffic eats it. Known from buildout receipt
   section 7; now measured: sustained usable throughput through the tunnel is
   ~1 req per 10-15 s with retries, not the nominal 120/min.
2. L1 CACHE COLLISION ON SHARED PREFIXES: `router.ts:147-150` keys the cache
   on the first 200 lowercased chars of the last user message. All four
   classify prompts share a 430+ char vocabulary prefix, so C2/C3/C4 were
   served C1's cached refusal at cache speed (299 ms mean) - wrong answers,
   fast. Any prompt family sharing a 200-char boilerplate prefix (route
   tables, vocab lists, fixed preambles) cross-contaminates. Do not send
   templated prompts through /v1/chat/completions.
3. PARAM DROP: the /v1/chat/completions handler destructures only model,
   messages, stream (`server.ts:878`); temperature and max_tokens are dropped.
   The queue-path worker call also sends neither (`platform-link.ts`
   pollAndProcess body: model, messages, stream). BASE honored temperature 0;
   the GSTD arm sampled. The E1/E2 "key names only" outputs vs BASE's 3/3
   exact is this param drop plus gemma:2b variance.
4. POLL CADENCE: this build's node polls the platform every 5 s (boot log
   "fallback poll every 5s"), not the 30 s code default in platform-link.ts;
   the push lane stays primary, and every router L2 call mints a real
   fee-bearing platform task.
5. FEE LEDGER (observed deltas, not over-attributed): submit charges 0.001
   GSTD (fee_tier basic) and the kill-test completion paid the node +0.002.
   Node totals tonight: tasks_completed 1 -> 9, gstd_earned 0.027056 ->
   0.091556, reputation 51 -> 59, avg_response_ms now 1698 (Pi earner:
   288 tasks, 34536 ms avg - our desktop wins the poll race by ~20x).

## 3. Settlement kill-test: PASSED (self-dispatch through the platform's own public endpoint)

Code read first: gateway push lane `server.ts:4568` (platform -> node), and
`router.ts routeViaTaskQueue` which calls `POST {platform}/api/v1/tasks/submit`
- a real, public, no-auth demand-side endpoint the router itself uses for
every chat call. That is a legitimate self-dispatch path: no auth improvised,
no fabricated task ids. (My first probe had 404ed on the wrong path
/api/v1/tasks; the live path is /api/v1/tasks/submit. The gateway's own
unauthenticated /api/v1/tasks/push COULD forge completions for made-up
task_ids; deliberately NOT exercised - that would be faking settlement.
Named here as an upstream risk.)

Execution, all bytes in the raw JSON and docker logs:
1. Baseline: gstd-desktop tasks_completed 1 (it had ALREADY moved 0 -> 1
   overnight on a real platform-dispatched task, `task-1791519460143-sn4aoi`,
   9 chars on gemma:2b, per docker log; the buildout receipt had recorded 0).
2. Submitted ONE task: `task-1791520415505-p9o8x4`, fee 0.001 basic, model
   gemma:2b, prompt "Reply with exactly: DOGFOOD SETTLEMENT PROBE OK",
   submit round trip 348 ms.
3. Our node claimed it on the 5 s poll, ran it, task record shows status
   completed, node_id gstd-desktop, resp_ms 5000, response byte-exact
   "DOGFOOD SETTLEMENT PROBE OK".
4. Platform nodes API: tasks_completed 1 -> 2, gstd_earned 0.027056 ->
   0.029056. Counter moved, earnings moved, no re-registration needed.

The matrix then kept the lane warm: 7 more queue-tier completions all won by
gstd-desktop (docker log names each task id and char count; counters ended at
9 tasks). The dogfood itself became real paid usage on the platform.

## 4. What the data says about the gstd tier (router evidence rows)

ROUTE TO GSTD (tunnel /v1/chat/completions) WHEN:
- The point of the call is settlement/earning, not raw inference quality:
  every queue-tier call minted a real fee-bearing task and our node won every
  race tonight (5 s poll, 1.7 s avg response vs the Pi's 34.5 s).
- Traffic is low-rate (about 1 req per 10-15 s sustained with 35 s backoff on
  429) and the latency budget is 3-8 s per call.
- Prompts are unique in their first 200 chars (no template families).

DO NOT ROUTE WHEN:
- Prompts share a long common prefix (cache serves a sibling's answer; the
  C2/C3/C4 collision is the proof row).
- Determinism or output caps matter: temperature and max_tokens are dropped
  by the gateway, extraction went 1/3 exact through GSTD vs 3/3 on BASE at
  temperature 0.
- Latency under ~2 s matters: queue tier measured 4.8x BASE (4034 vs 845 ms
  mean on identical tasks; submit + 2 s router poll + 5 s node poll + platform
  writes are the floor).
- Burst above ~2-3 quick requests: the shared 172.20.0.1 rate bucket collapses
  (6/11 dead at ~16/min self-rate).

TIER VERDICT: tonight the gstd tier's value is the SETTLEMENT SURFACE (9
tasks, 0.091556 GSTD earned, reputation +8), not inference quality. For estate
janitor micro-tasks on this box, direct localhost:11434 remains the right
lane: 0 errors, 697 ms mean, better outputs on the same model. gemma:2b is
fit for summarize-lite on both arms, unfit for 17-way classification on both
arms (it is not even a member of the 17-animal vocabulary; the local member is
qwen2.5:7b), and unreliable for exact extraction when sampling is on.

## 5. Untested / owed

- Named-tunnel persistence and the 429 bucket fix (proxy-header trust) are
  upstream-code decisions, deliberately not improvised here.
- Push lane (/api/v1/tasks/push) exercised only by code read + the platform's
  own overnight dispatch, never by us (forgery risk above).
- tasks/poll at 5 s under load, swarm/P2P lanes, NAAS stay off per buildout
  receipt section 4.

Receipts: raw matrix `dogfood_matrix_raw.json` (this dir), buildout
`watch/inbox/gstd_desktop_buildout_20260109.md`, docker log lines quoted
above (gstd-node, --since 45m, 9 "completed (gemma:2b" lines).
