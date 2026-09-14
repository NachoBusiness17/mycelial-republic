# ENV INVENTORY + GAPS + WORK PLAN — 2026-09-01 14:35Z (retry-kick delivery)
Consolidates tonight's receipts: key-matrix probes, WATER_NETWORK_SPEC census, DUMB_AGENT_GPS map,
ECONOMIST_ROUTE capacity table. Writer pause respected — board appends only, no knot/trajectory writes.

## 1. ENV INVENTORY — every key, what it's good for (probe-verified 2026-09-01)
| key | family/endpoint | protocol | state | good for |
|---|---|---|---|---|
| ZAI_API_KEY (slot1, 3254ac…) | intl PAYG @ paas/v4 | OpenAI Bearer | **DELETED console-side** (was E5-live 99.7% cache) | was: cache-mined cash lane; restore = new intl-console key |
| ZAI_API_KEY_2 (088650…, env) | none — 401 everywhere | — | **DEAD garbage** | purge at next container recreation |
| MAG (ZAI_API_KEY_3, bafc5c…) | coding-plan @ anthropic-compat | x-api-key /v1/messages | LIVE; shared weekly pool **WALLED to 09-02 12:52:28Z** (1310) | plan-quota work post-reset; probe battery staged |
| Cache (e3c505…, /mag/.env L29) | coding-plan @ anthropic-compat | x-api-key | LIVE; same shared pool, walled same | backup lane post-reset |
| ZAI_API_KEY_PRO (e18faf…) | coding-plan @ anthropic-compat | x-api-key | **LIVE 200** (zcode's key) | zcode primary; plan-quota work |
| ZAI_API_KEY_LITE (4f8ac5…) | Lite @ anthropic-compat | x-api-key | **LIVE 200**, own bucket: 2K/5h, 10K/wk (13% used, pace alarm → ISOLATION GATE) | Lite law: zcode primary; fleet ≤ tiny sequential probes only |
| deepseek (direct) | paas | OpenAI Bearer | LIVE, $24.13 invoiced, 98% cache, off-peak ½ | driver + gophers; conservation-lane backbone |
| together | serverless | OpenAI | LIVE, E6 100% cache proven | cache-mined scut arm #2 |
| cerebras | free tier | OpenAI | LIVE, 1M TPD | scut reservoir (full) |
| groq | free tier | OpenAI | LIVE, 200K TPD, 87% fuel | scut reservoir |
| nvidia/others | credits | — | unprobed | backlog |
| ollama | local | local | LIVE $0 | T0 janitor, electricity-only |
| **DOCTRINE:** z.ai key families are endpoint-scoped — coding-plan console keys speak Anthropic protocol ONLY; intl-console keys speak OpenAI paas. Match family to protocol or 401 forever. |

## 2. FUNCTIONALITY GAPS vs what we hold
**Infrastructure:**
- G-INF1: slot1 PAYG lane dark (E5 cache-mining channel offline) — needs new intl-console key.
- G-INF2: no closed economist→router actuator (route table computed, nothing rewires lanes automatically).
- G-INF3: 11/12 water reservoirs lack per-burn meter rows (M0 cron now live; history shallow).
- G-INF4: memory_search down (fts-only fix staged, needs operator config command).
- G-INF5: container env fossilized — dead 088650 string un-purgeable until recreation; /mag/.env not read by container.
**Fleet capability (from DUMB_AGENT_GPS map):**
- G-NAV1: no self-locate-on-cold (fresh seat can't compute its rung) — unblocks 3 gaps when built.
- G-NAV2: no steer heartbeat — ignored steers are silent misses; 26/26 D-lerp claim is brief-level, unreceipted.
- G-NAV3: no heading vectors (cascade order without direction), dumb→dumb routing, goal-bind persistence, exit vectors.
**Governance/process:**
- G-GOV1: writer-id collisions (two sessions as `sancho` pre-hardening; codex malformed log lines — tolerance patched, writers need schema discipline).
- G-GOV2: arena/harness infra unbuilt (Wargames spec frozen, smoke verdict filed).
- G-GOV3: provider endpoint patch + roster patch applied but provider endpoint patch (PROVIDER_ENDPOINT_PATCH) still pending host apply.

## 3. HOW-BEST-TO-WORK PLAN (the ladder, in order)
**Now → 12:52Z tomorrow (conservation window):**
1. DeepSeek + free lanes only; Lite reserved for zcode (ISOLATION GATE enforced — fleet probes ≤6-call sequential).
2. Water v1 gate enforcement: every lane decision cites its gate; M0 meter fills reservoir levels daily.
3. Carve #1 (self-locate-on-cold connector) — smallest shape, unblocks 3 GPS gaps; spec'd in DUMB_AGENT_GPS_MAP.
4. Phase-change boundary probe (steering position-variance, 6 LITE calls) — staged, fires on operator word.
**Rain day (09-02 12:52Z):**
5. MAG/Cache/PRO refill → invariant probe battery re-runs → steering-transfer verdict from real quota.
6. New intl-console key (operator) → E5 PAYG channel reopens → API BUFFER goes live (dumb-window overflow).
**This week:**
7. Carve #2 steer heartbeat (receipts the 26/26 class; closes silent-miss).
8. Headings, goal-bind, dumb→dumb routing in babystep order; ask_router reads water levels (closed loop).
9. Provider endpoint patch host-apply; memory_search fix; salvage-lane host runs (verkle tie-ins).
**Standing law:** board appends only under writer pause · pointer-law lanes (procedure in files, prompts are
pointers) · every organ judged by force multiplication · receipts before claims.
