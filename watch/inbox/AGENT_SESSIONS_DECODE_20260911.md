# AGENT_SESSIONS_DECODE — the memory/agent_sessions/ pool

Decoded 2026-09-09 by a fleet research worker. READ-ONLY pass; this file is the only write.
Directory: `memory/agent_sessions/` — found by the estate index, never catalogued until now.

## 1. Anatomy of the pool

| Metric | Value |
|---|---|
| Total entries | 2,660 (13 files + `.gitkeep` outside the pool proper) |
| orc-t session files | **2,646** (`orc-t<10 hex>.json`) |
| Named-seat files | 13 (`cli`, `deepseek`, `desk-deepseek`, `desk-deepseek-test`, `cursor-bridge-test`, `cursor-phase1-cursor-verify`, `local`, `smoke`, `tablet-ipad`, `ui-test3`, `ui-test4`, `orc-diag-spawn-01`) |
| Pointer | `LATEST.txt` = newest session id (resume pointer) |
| Total size | **63.7 MB** |
| Parse errors | 0 / 2,646 — every file is clean JSON |
| Size range | 9,163 B → 1,714,939 B; median 12,658 B; mean 24,057 B |
| Span (internal `updated`) | **2026-08-03T05:07Z → 2026-09-09T15:47Z** |
| Span (named seats) | earliest file overall is `smoke.json`, updated **2026-08-02T14:36Z** |

### What a record is

One file = **one Mag agent CLI worker session transcript** (orc = the orchestrator's spawn,
`t*` = task-token sessions). Stable schema across the whole span:

```
{ session_id, provider, model, messages: [{role, content}], last_answer, updated }
```

- `session_id` — matches the filename (`orc-t4b6719bacc`).
- `provider` — ollama 1,906 (72.0%), deepseek 694 (26.2%), grok 16, deepseek_overmind 15,
  xai 8, z_ai 5, nvidia 1, frontier 1.
- `messages` — full rolling transcript: system prompt + every task turn. Long-lived workers
  accumulate thousands of turns (largest: 3,481 messages, 1.7 MB, a grok-handoff pre-scope
  day, 2026-08-09).
- `last_answer` — the worker's final word for the session.

### What the sessions are (archetypes)

| Archetype | Count | Share |
|---|---|---|
| Handshake probes (≤3 msgs, "Reply with only READY/done") | 2,204 | 83.3% |
| Task transcripts, no tool messages | 237 | 9.0% |
| **Tool-using transcripts** (real `tool` role turns) | **205** | **7.7%** |

Message-count buckets: 2,422 sessions ≤10 msgs; 124 sessions carry 50+ messages (the
long-lived workers). System prompt is versioned inside each transcript and grew
**5,239 → 19,719 chars** across the span — the worker brain's lineage is archived here.

## 2. Files-per-day histogram (internal `updated`)

```
2026-08-03  27  ######
2026-08-04  16  ####
2026-08-05   1  #
2026-08-06  39  ########
2026-08-07  14  ###
2026-08-08 122  #########################
2026-08-09 139  ############################
2026-08-10 446  ############################################################
2026-08-11 455  ############################################################
2026-08-12 193  #######################################
2026-08-13 333  ############################################################
2026-08-14 187  ######################################
2026-08-15  29  ######
2026-08-16  20  #####
2026-08-17 130  ###########################
2026-08-18   4  #
2026-08-19   0
2026-08-20   0
2026-08-21   0
2026-08-22   0
2026-08-23  14  ###
2026-08-24   3  #
2026-08-25   1  #
2026-08-26   1  #
2026-08-27   5  ##
2026-08-28   1  #
2026-08-29   3  #
2026-08-30  69  ##############
2026-08-31 156  ################
2026-09-01  11  ###
2026-09-02  18  ####
2026-09-03 101  #####################
2026-09-04  39  ########
2026-09-05  12  ###
2026-09-06  11  ###
2026-09-07  32  #######
2026-09-08   8  ##
2026-09-09   6  ##
```

**The "Aug 16-31 silence" is really Aug 19-22:** four days of zero worker sessions (Aug 18
has 4, then nothing until Aug 23). Peak load was Aug 10-13 (1,231 files — the
republic_os/grind wave). The estate index's wider window framing is DISPUTED by this
measurement; the precise gap is Aug 19-22.

## 3. The orc-knot correspondence — SUPPORTED, near-total

Family atlas claim: mag-agent-orc family = 2,575 chain knots (34.9% of chain).

Measured against `memory/biography/verkle_chain.jsonl` (7,377 rows):

- Chain knots use `session_id = "mag-agent-orc-" + tXXXXXXXXXX`; disk files use
  `orc-tXXXXXXXXXX.json` — **same token, different prefix decoration.** Stripping the
  decoration, the join is exact.
- **2,562 of 2,646 disk sessions (96.8%) have ≥1 chain knot**, 1:1 (no session carries
  multiple knots).
- **100.0% of chain orc-t tokens have a session file** (2,563 tokens incl. the variant
  `diag-spawn-01` → file `orc-diag-spawn-01.json`).
- 84 disk sessions are unknoted: 46 dated Sep 7-9 (knotter lag tail — recent, not lost)
  + 38 stragglers scattered Aug 8-31 (likely failed/aborted runs, 2.1 MB total).
- Knot ts span: 2026-08-10 → 2026-09-06 (sessions began Aug 3; knotting started Aug 10).
- Atlas says 2,575; measured unique tokens today: 2,563. Delta 12 (~0.5%) — chain has grown
  and amended since the atlas was computed. DISPUTED at the margin, SUPPORTED in substance.

**Verdict on the claim: the session files ARE the source transcripts behind the mag-agent-orc
chain knots.** The chain holds the digest; this pool holds the full bodies.

## 4. Secret exposure scan (patterns classified, nothing echoed)

- 26 files match an `api_key|secret|token|password =` pattern; on inspection 13 are prose
  ("meta-token: …" inside memory-language invariants), the rest are code-snippet examples
  with placeholder/env-var values (e.g. `<your DeepSeek API Key>`, `os.environ[...]` shapes).
- 1 file mentions the literal `X-API-Key` header name (the mag MCP door) — a name, not a value.
- **Zero real credential-shaped values found.** Three config-shaped snippets deserve a spot
  check before any external publication of pool excerpts, but the pool is clean by design
  (the worker law "Never read or echo .env secrets" is baked into every system prompt).

## 5. Samples read (full reads, no secrets)

| File | Date | Provider | Shape |
|---|---|---|---|
| `orc-t4b6719bacc.json` (earliest) | 2026-08-03 | deepseek | 3 msgs; READY handshake; sys prompt 8.8K |
| `orc-t104a28803c.json` (latest) | 2026-09-09 | ollama | verkle backfill task; honest network-error answer |
| `orc-t185c765db0.json` (Aug 16-31 window) | 2026-08-16 | deepseek v4-flash | 57 msgs, 31 tool turns — a real republic_os round (12 tasks dispatched, W0.3 gate surfaced) |
| `orc-t31873a68f8.json` (largest, 1.7 MB) | 2026-08-09 | deepseek v4-flash | 3,481 msgs; grok-handoff pre-scope; escalated a false-success guard to overmind |
| `orc-t0d7be03ef3.json` (smallest) | 2026-08-03 | deepseek | 3 msgs; "done" probe |

## 6. Recovery-value verdict

**SUPPORTED: the pool is the largest untapped primary record of fleet worker behavior —
but 83% of it is heartbeat, the treasure is the 442 real transcripts.**

1. **Recoverable now, high value** — the 205 tool-using transcripts + 237 non-tool task
   transcripts: actual worker decision trails (dispatch, escalation, honest failure answers,
   false-success guards). This is trajectory-lens raw material already in the envelope shape
   {input → tool_result → output} — pre-sealed steps, seven weeks of them.
2. **Recoverable now, medium value** — the versioned system prompts (5.2K→19.7K chars) are a
   complete lineage of the worker brain's evolution, retrievable without touching any repo
   history.
3. **Structural value** — 96.8% knot coverage means the pool can be indexed by joining
   chain ts/theme metadata onto transcripts; the 84 unknoted files need no join at all.
4. **Not worth mining** — the 2,204 handshake probes (they do prove worker cadence and the
   Aug 19-22 outage window, then should be filtered out of any future corpus).
5. **Cost** — 63.7 MB, zero parse errors, stable schema: a one-pass indexer is trivial;
   route it to a free lane.

**Recommendation:** catalogue the pool as `worker-transcripts/orc` in the estate index;
index the 442 real transcripts (session_id, updated, provider, msg count, task head, chain
knot leaf_hash) onto a topic-index lane; keep the probes out of the corpus.
