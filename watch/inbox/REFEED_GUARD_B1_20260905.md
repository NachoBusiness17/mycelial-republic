# REFEED GUARD — B1 (2026-09-05, worker: refeed)

**Verdict: REFEED_HEAVY.** The tax is real and now measured by a repeatable guard.
Gate line: **Lite re-arm Sep 8 02:19Z is gated on this receipt existing + verdict.**

## What the refeed tax is

The burn pool loses quota to re-fed context: every turn ships the whole prior
history (tool outputs, pastes, system framing) back to the model. Operator
measurement 09-05: **122M input tokens → 0.5M output** in one weekend pool.
Input is billed (or burns quota) on every request; output — the actual work —
is a rounding error next to it. Re-arm without a guard re-opens an unmonitored
firehose.

## What the guard measures

`ROOT/mag/refeed_guard.py` — CLI `python -m mag.refeed_guard measure [--days N]
[--threshold R]`. Opens the ZCode session DB (`~/.zcode/cli/db/db.sqlite`)
**READ-ONLY** (`file:...?mode=ro`), no network, no daemons, exit code 0 always.

Per session, an honest **CHAR PROXY (chars, not tokens)**:
- input side = user text chars + tool/tool_result part chars (state.input +
  state.output) — the body that gets re-fed;
- output side = assistant text chars. (assistant reasoning chars counted
  separately, excluded from the ratio.)

Secondary cross-check, real provider tokens straight from `step-finish` parts:
`tok_in / tok_out / tok_cache_read` — labeled, kept out of the proxy math.

Outputs: per-session table (id prefix, redacted title prefix, in/out chars,
ratio), daily aggregates, flagged list (ratio > threshold with an input floor
of 100K chars to skip micro-sessions), machine JSON at
`ROOT/state/refeed_guard_latest.json` with guard `VERDICT: CLEAN | REFEED_HEAVY`
plus top offenders.

## Measured numbers (run 2026-09-05, `measure --days 3`)

- **307 sessions in 3 days.** Char proxy: **in 45,204,514 : out 3,404,259
  chars — ratio 13.3:1**.
- **Real tokens (step-finish, cross-check): in 3,018,477,598 : out 7,780,601 —
  ~388:1**, of which **2,837,080,451 are cache reads = 94% of input is re-fed
  context**. Fresh input ≈ 181M tokens/3d. This independently confirms the
  operator's 122M weekend-pool measurement: same shape, worse.
- **Proxy understates the tax by design**: stored chars count once; every turn
  re-feeds them. The step-finish token sums carry the turn-multiplied truth.
  Both are in the JSON so nobody has to trust the proxy.
- Daily: 09-03 → 11.3M/0.79M (70 sess); 09-04 → 25.3M/1.66M (142 sess);
  09-05 → 8.6M/0.95M (95 sess). Sep-4 was the heaviest refeed day.
- **Worst offender: `sess_sub` at 301:1** (elder-lane agent batch). All 4
  flagged sessions are `sess_sub*` sub-agent batch runs, 204–301:1.

## Threshold: in:out > 200:1 (input floor 100K chars)

Flagged sub-agent sessions cluster 204–301:1; normal interactive sessions sit
far below (fleet-wide ratio 13.3:1 chars). The operator's own measured tax
(122M:0.5M = 244:1 tokens) lands inside the flagged band. 200:1 cleanly
separates batch context-mining from work-with-output — a session that ships
200 chars of context per char of answer is a miner, and miners belong on the
free lanes, not the burn pool.

## Falsifier

- **Determinism: PASS.** Two back-to-back runs → canonical JSON (all fields
  except `generated_at`) byte-identical (`diff` clean). Ran while this very
  session was live-writing to the DB and still held.
- **Threshold sanity: PASS.** `--threshold 5` run completes and flags more
  sessions; canonical `--days 3` run re-emitted REFEED_HEAVY afterward and is
  the JSON now on disk.

## Known gaps (tri-state honesty)

- Paste/file attachment parts hold a path, not inline text — paste-heavy
  sessions have input UNDERCOUNTED in the proxy (their real tokens still show
  in tok_*). SUPPORTED by DB schema (part type `file`, `url` field).
- Daily aggregates bucket by session `time_updated` (UTC), not per-part time —
  UNPROVEN whether per-part bucketing changes the day shape materially.
- Cache-read share measured on this machine only; pool-wide share UNPROVEN.

## Files

- Guard: `ROOT/mag/refeed_guard.py`
- Machine receipt: `ROOT/state/refeed_guard_latest.json` (regenerate anytime:
  `python -m mag.refeed_guard measure --days 3`)
- DB access: read-only URI, mirrors `ROOT/watch/live_feed.py` DB constant.

**Gate:** Lite re-arm Sep 8 02:19Z is gated on this receipt existing + verdict.
