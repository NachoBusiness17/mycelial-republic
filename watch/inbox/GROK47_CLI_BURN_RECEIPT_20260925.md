# GROK 4.7 CLI OVERFLOW BURN RECEIPT - one real chore through the CLI harness seat (2026-09-25, filed 2026-09-26T01:1xZ)

Task: grok-overflow. FINISH LINE: one real fan-out-suitable chore executed through the
grok CLI harness seat with a cost/latency receipt in the cheap-lane ledger. EXECUTED.

## Which path was actually taken (the brief's pricing question, answered)

The nous-week row (watch/inbox/QUIET_RADAR_20260921.md:269-286) says Nous Portal
resells Grok 4.7 at 50% off for one week, ends ~09-28, accessed via Nous's Hermes
Agent product. That discount did NOT ride this run. Path taken:

- Seat found: `harness/grok_cli.py` (`find_grok()` at :23 resolves the `grok` binary;
  present at C:\Users\foste\.grok\bin\grok.exe, version 1.0.41).
- Binary auth: auth.x.ai OIDC session (account nachobusinesscorp, team-scoped), NOT
  the estate XAI_API_KEY and NOT Nous Portal keys. Model catalog fetched from
  https://cli-chat-proxy.grok.com/v1/models; `-m grok-4.7` resolves to surface model
  id `grok-4.7-build` on that proxy (reported in each call's modelUsage).
- Cost basis: the proxy self-reports `total_cost_usd` per call; those numbers are the
  receipt's cost figures. Exact per-token pricing of the build proxy surface is not
  documented where I looked (docs.x.ai pricing page covers api.x.ai, $2/$6 <200k per
  the 09-25 repoint receipt); implied blended rate from my two priced calls is BELOW
  the api.x.ai card (roughly $0.7-0.8/M in, ~$2/M out, inferred from self-reported
  cost over measured tokens, NOT a verified rate card).
- So: Portal-tier 50% pricing does not apply via the CLI. This run burned the
  estate's own xAI account session on the Grok Build surface. The Nous 50% window
  remains usable only through the Hermes/Nous key lane, which is a different seat.

## The chore (real, fan-out-suitable)

BOOT_LANE_INTERFERENCE_BURN_20260925.md Stone 5.1: adversarial pass on the frozen
interference-replication pre-registration (+ Amendment 1) BEFORE Arms A/C run
(watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md,
watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md). No seat had
filed this pass yet as of this run (inbox check this session). Same chore shape fans
out across prereg docs, which is what makes it fan-out-suitable.

## What ran (exact commands)

1. Smoke probe, raw binary, `grok-4.7 --output-format json`, prompt "Reply with
   exactly one word: ok": HTTP-shaped ok, 19.8s, self-reported cost $0.01726316,
   24,609 in / 110 out. This verified auth + cost capture before spending on the
   real chore.
2. Attempt 1 via the seat: `./.venv/Scripts/python.exe _grok47_chore_run.py`
   (calls harness.grok_cli.escalate_via_harness, output_format json, model grok-4.7).
   FAILED HONESTLY: exit 1, stop_reason cancelled at 225s, $0.03970384 spent, 10,414
   reasoning tokens burned because the model tried to read the filed prereg from disk
   (tool use) instead of answering from the pasted text. Ledger row appended, ok:false.
3. Attempt 2, same driver with tool use explicitly forbidden and
   `reasoning_effort="low"`: OK. exit 0, end_turn, latency 120,125ms, cost
   $0.02908224, usage 26,830 in (1,280 cache-read) / 5,206 out (4,110 reasoning),
   model grok-4.7-build. Total spend all three calls: $0.08604924.

## Seat patch (durable, in repo)

`harness/grok_cli.py`: added optional `model` and `reasoning_effort` params (model
pin + billed-reasoning lever), wall-latency capture (`latency_ms` on success, timeout
and error paths), and when `output_format="json"` the proxy cost accounting is lifted
into the result dict (`usage`, `cost_usd`, `model_used`, `session_id`,
`stop_reason`) with `deliverable` set to the parsed text. Backward compatible:
default `output_format="plain"` behaves exactly as before.

## Cheap-lane ledger (finish-line receipt)

`logs/provider_usage.jsonl`, two rows appended via json.dumps, session_id
`20260925-grok47-prereg-adversarial`, provider xai, model grok-4.7-build:

- 2026-09-26T01:03:47Z ok:false cost_usd 0.03970384 latency_ms 225000 tokens 38558
- 2026-09-26T01:07:33Z ok:true  cost_usd 0.02908224 latency_ms 120125 tokens 33316

Ledger choice stated openly: this file is one of the two burn meters the boot lane's
Sunday checklist names ("logs/provider_usage.jsonl + state/fuel/stealth_ledger.jsonl
prove the burn", BOOT_LANE:109); stealth_ledger is the openrouter stealth-probe
shape, so provider_usage is the cost/latency home here. Verified by re-reading the
tail this session.

## Deliverable

watch/inbox/INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md: verbatim grok-4.7
adversarial review, 5 objections (saturated-regime 200 bar, amendment-reinterpreted
50 bar, dual-budget second-life risk, unfrozen Arm C decoding/prompt, post-hoc
skip risk), each with quote + risk + bar-preserving fix, ending VERDICT: UNSOUND.
Raw result also in queue/results/20260925-grok47-prereg-adversarial.json.

## Honest limits

- Two attempts were needed; the failed one is receipted, not hidden. Total grok spend
  this task $0.086, above a strict few-cents reading, justified by the brief naming
  the overflow burn and the boot lane's Grok pool; reported to the cent.
- The proxy's per-token price is opaque; cost figures are the proxy's own accounting,
  trusted as authoritative for the receipt but not independently verifiable.
- grok-4.7-build is the build-surface variant, not the raw api.x.ai grok-4.7 id; a
  same-window raw-API check belongs to the operator-gated xai cash lane (grok_route.v1),
  untouched here per operator-gate law.
- The UNSOUND verdict is one model's review of the design, filed as a chore product.
  Whether to accept its fixes is a judgment for the seats running Arms A/C, not
  settled by this receipt.
- config seal untouched: no writes under configs/ by this seat (pre-existing
  lanes.yaml seal drift noted by XAI_GROK47_REPOINT_20260925.md remains another
  seat's named act).

## Read trail

watch/inbox/QUIET_RADAR_20260921.md:269-298; watch/inbox/BOOT_LANE_INTERFERENCE_BURN_20260925.md
(pools table, Stone 5, Sunday checklist); watch/XAI_GROK47_REPOINT_20260925.md;
watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md + AMENDMENT1;
harness/grok_cli.py; _grok47_chore_run.py; ~/.grok/auth.json + models_cache.json +
config.toml (metadata read only); logs/provider_usage.jsonl tail; smoke + two seat
runs executed this session.
