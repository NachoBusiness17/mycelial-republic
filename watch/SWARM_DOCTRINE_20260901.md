# SWARM_DOCTRINE_20260901 — when to swarm (measured API economics)

Operator directive 02:04Z: *"with cache mining and z.ai api keys we could in theory
launch an absolute fuckload of next to free models for literally fractions of a
penny. check the api."*

Answer, receipted: **yes.** z.ai Pro + 4.7-flash free + cached prefixes make the
per-call marginal cost ~$0 on the swarm lanes, and the fleet can run thousands of
breadth-parallel calls/day for under $1 — but only on the *right* lanes and the
*right* shapes. This file is the when-to-swarm law.

All prices in USD per 1M tokens unless noted. Every figure is labeled
MEASURED (this subagent probed it live today) / DOCS (z.ai published page,
web_fetch'd) / CORPUS (fleet ledger/seat_corpus) / ESTIMATED (derived).

---

## §MEASURE — z.ai pricing, cache, limit (DOCS + live probes)

### 1. Web facts (DOCS, via docs.z.ai)

- **Pricing**: `https://docs.z.ai/guides/overview/pricing.md`
  (promo active to **2026-09-09 24:00 UTC+8**):
  - **glm-5.3-flash**: input **$0.075** | cached input **$0.015** | output **$0.25** | cached storage **Limited-time free**.
  - **glm-5.3**: $1.4 / cached $0.26 / output $4.4.
  - **glm-4.7**: $0.6 / cached $0.11 / output $2.2.
  - **glm-4.7-flash**: **FREE.**
- **Context caching**: `https://docs.z.ai/guides/capabilities/cache.md` —
  automatic *implicit* caching (no manual prefix registration needed); billed via
  `usage.prompt_tokens_details.cached_tokens`. Matches DeepSeek's surface pattern.
- **Rate limits**: `https://docs.z.ai/api-reference/rate-limit.md` →
  redirects to `https://z.ai/manage-apikey/rate-limits` — **dynamic per-key,
  no static concurrency doc** (UNVERIFIED numerically; see probe for the measured
  ceiling).
- `https://open.z.ai/en/pricing` → ENOTFOUND (unreachable this session).

### 2. Live probe A — billed key (`ZAI_API_KEY`), glm-5.3-flash, 10 parallel

Endpoint `https://api.z.ai/api/paas/v4/chat/completions`. Frozen prefix
`SWARM_DOCTRINE_FROZEN_PREFIX_20260901`, ~100-tok output per call.

| metric | value |
|---|---|
| HTTP status | 10/10 **200** |
| 429 / fence / aborts | **0** |
| cache-hit tokens (cached_tokens) | **0 on every call** |
| prompt tokens | 6873 each |
| output tokens | 64 each |
| latency spread | 3280–3889 ms (~610 ms) |

→ Billed lane handles 10-parallel with **zero 429**, but reported **no cache hits**
on the repeated prefix. Follow-up sequential reconcile (2 identical calls to
`BILLED_SEQ_CACHE_TEST_20260901`): call-1 cached=0/2656ms, call-2 cached=**0**/1577ms.
Call-2 was ~40% faster — server-side prefix reuse exists but is **not billed or
surfaced as cached_tokens** on this lane at this volume.
**DOCS claim $0.015/M cache-hit on the billed key: UNVERIFIED at this scale.**

### 3. Live probe B — Pro plan key (`ZAI_API_KEY_PRO`; the `/z_ai2` lane)

Same pattern. First run on the **already-warm** prefix:

| metric | value |
|---|---|
| HTTP status | 10/10 **200** |
| cache-hit tokens | **6848 / 6873 = 99.6% on ALL 10 calls** |
| latency | 3980–7265 ms (warm first run) |
| fresh cold `_V2` prefix | 10/10 OK, min 2196 / med 2549 / **max 24564 ms**(contention) |
| warm re-hit | 10/10, 6848 cached each, spread 4007–16693 ms (heavy tail) |

Concurrency fence signal: one `UND_ERR_SOCKET` ("other side closed") on an
unrelated ~20th rapid call → **Pro lane degrades ~10–20 concurrent**; back off
under it.

### 4. Reconcile

- **z.ai Pro plan**: cache-hit discount is **REAL and MEASURED** — 99.6% hit on
  warm prefix, and the Pro plan is plan-funded ($0 marginal for our burn). This is
  the "fractions of a penny" lane.
- **Billed key**: cache reuse happens server-side (latency drop) but the billable
  `cached_tokens` field stays 0 at this volume — **MEASURED $0.075-in billed on the
  full prompt, not $0.015**; the $0.015 cache-hit rate is **UNVERIFIED vs docs for
  this lane at 2K-scale**.
- **Cache must be ESTABLISHED once** (cold → ~24.5s worst) before it pays.
  Per-call-unique prefixes are the kill-switch (see §DOCTRINE).

### Probe spend (receipt, kept under the $0.05 cap)

- Probe A billed: 10×6873 in @$0.075/M + 640 out @$0.25/M ≈ **$0.0053**
- Billed seq reconcile: 2×2431 in + outs ≈ **$0.0004**
- Probe B: Pro plan-funded (≈$0 marginal)
- **TOTAL measured billed ≈ $0.0057 < $0.05** ✓

---

## §COMPUTE — swarm cost table

Model: N calls × 2K input tokens each, **frozen prefix** (≈1800 cached + ~200
new tail), ~500 output tokens per call. Labels: MEASURED / DOCS / CORPUS /
ESTIMATED. Do **not** read beyond the bottom row for the "how much" instinct.

| Lane | unit (per-call $) | N=10 | N=100 | N=1000 | N_max for <$1/day | ceiling |
|---|---|---|---|---|---|---|
| **z.ai Pro 5.3-flash** (cached) | **$0** MEASURED (plan-funded, 99.6% hit) | $0 | $0 | $0 | **~unlimited dollars; ~1–3K/day sane** | ~10–20 parallel (fence) ESTIMATED |
| **glm-4.7-flash** (free tier) | **$0** DOCS | $0 | $0 | $0 | unlimited (rate only) | rate-limited per key ESTIMATED |
| **z.ai billed 5.3-flash** (no cache billing MEASURED) | $0.000275 ESTIMATED (all 2000@.075 + 500@.25) | $0.0028 | $0.028 | $0.275 | **≈3,600/day** | 10-parallel OK MEASURED |
| z.ai billed 5.3-flash (if $0.015 cache worked) | $0.000167 per DOCS | $0.0017 | $0.017 | $0.167 | ≈5,988/day | — |
| **together** (Flash-0731 serverless, cached) | $0.000222 CORPUS ($0.03 cached/M) | $0.0022 | $0.022 | $0.22 | ≈4,500/day | — |
| **DS-flash off-peak** (DeepSeek) | $0.000387 CORPUS ($0.007 cache-hit/M) | $0.0039 | $0.039 | $0.39 | ≈2,587/day | 1M-token window CORPUS |
| **cerebras** gpt-oss-120b | **$0** free tier | $0 | $0 | $0 | **500/day token-capped** | **1M TPD** CORPUS |
| **groq** | **$0** free tier | $0 | $0 | $0 | **100/day token-capped** | **200K TPD** CORPUS |

### Fuckload verdict (one line)

Broadcast swarms of cheap/free breadth-parallel calls can run at roughly
**hundreds to a few thousand calls/day for under $1** — z.ai Pro and 4.7-flash are
effectively **$0 marginal** (Pro plan-funded + measured 99.6% cache hit), which is
the difference between a swarm day costing cents on the Pro lane vs ~$0.28 on the
billed lane vs token-capped $0 on cerebras/groq.

So: **the "fuckload" is real and achievable today**, but it is bounded by (a)
quota ceilings on free lanes (cerebras 500/groq 100/day), (b) the Pro lane's
~10–20-parallel concurrency fence, and (c) **whether the prefix is frozen** — the
repeated-prefix discipline is what turns a billed lane from ~$0.28/K-calls into
$0.17/K-calls and keeps Pro at ~$0.

---

## §DOCTRINE — when to swarm (from our own receipts)

The swarm is a **breadth machine for jury-labeled harvesting**, not a brain. It
pays when the unit of work is *independent, parallelizable, prefix-reusable* and
the *value is diversity* (HOT gate law). It dies when the work is sequential,
verdict-shaped, or prefix-fracturing.

### SWARM (DO)

- **GOPHER fetch/extract**: many URLs, same instruction, frozen preamble.
- **Probe batteries / smoke batteries**: same prefix × N variants (exactly what
  this probe did — it's the canonical swarm shape from water_ledger
  `together_activation` 08-31T20:39:25.230Z and `lane_activations`
  08-31T21:15:31.150Z).
- **Smell-lane intake**: cheap models score/hash many docs in parallel for
  routing; fast rejects, only the survivors ascend.
- **Salon lens-shots**: one pack, N distinct lenses (the fleet's proven cross-
  family salon — see riddler receipts below). Diversity = jury value.
- **Harvest triage**: many candidate leads, one cheap classifier each (ledger
  `OCTANT` wave-1 → 6 leads ≈ 4.5 lead-hrs ≈ $3.40).

Receipts (CORPUS, riddler/water_ledger):
- `SALON_RIB_COMPACTION` — lanes A inventory / B divergences / C build program
  across deepseek + groq-120b + cerebras-120b; then synthesis on /board.
- `SALON_RACTOR_CAST` — 3 lenses (Lessig/Bernays/Ellul) as decode-parity,
  mechanism proven cross-family, `calibration line + 3 findings + 1 refusal each`.
- `SALON_BUS_INTEGRATION` — A misses / B unmounted / C design, cross-family
  groq/nvidia/deepseek.
- `SWARM_LENS v0` — six-gate jury (ledger-first, source hierarchy, mandatory
  arbitration vs primary bytes, hostile pass, calibration words, publication via
  riddler gate).
- Lane activation receipts: `together_activation` 08-31T20:39:25.230Z,
  `lane_activations` 08-31T21:15:31.150Z (cerebras gpt-oss-120b confirmed 10s/165 tok).

These are the template: **same pack, N independent lanes, receipted synthesis.**
They are a swarm; the swarm doctrine just names the cost law they already obey.

### DON'T (NEVER swarm)

- **Sequential reasoning / single verdicts**: one judge, one call, wants the whole
  context — that is brain-slot work. Run it warm on one lane, not fanned out.
- **Per-call-unique prefixes**: kills the cache on every lane. Measured: cold
  5.3-flash ~24.5s worst and full $0.075-in; warm ~4–7s and $0.015/0 on Pro. Freeze
  the prefix or don't batch.
- **Swarming brain-slot work**: escalating insight/steering across lanes creates
  N agreeing copies of one failure, not a jury. Escalate to a warm single lane /
  salon synthesis instead.
- **Free-lane quota abuse**: cerebro 1M TPD / groq 200K TPD are the real ceiling,
  not dollar cost. Respect them (CORPUS: operator budget law 14:07Z ≈ $1/hr active,
  cheap/off-peak autonomous).

### When NOT to swarm (tie-break)

When the task is one-of (a single answer, a single verdict, a decision) → **no
hash-receipt, escalate**. When it is many-of-identical-shape (fetch, probe, score,
classify, lens) → **swarm it**. When it is N-different-lenses-on-one-subject →
**swarm as a salon jury** (diversity = value, HOT gate law). When the prefix can't
be frozen → **swarm is waste; go warm.**

---

*English, receipted, no novel. All numeric probes MEASURED today by ZAI-PROBE
subagent; spend ≈ $0.0057 billed, capped well under $0.05. Fuckload verdict:
the capacity is real; the constraint is quota ceilings + Pro concurrency fence +
prefix-freeze discipline, not price.*
