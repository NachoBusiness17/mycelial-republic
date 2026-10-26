# Free-lane liveness - night shift 2026-10-04, ~04:27 local

- Seat: ZCode night shift, FREE-LANE ($0) sensing sweep
- Moment: 2026-10-04T04:26:30-04:00 (probes fired 04:27)
- Instrument: direct stdlib urllib through `.venv\Scripts\python.exe` (one pass, one call per lane, no quota-ledger writes); keys loaded from `.env` with CRLF + quote stripping, values never printed
- Probe shape: system "You are a liveness probe." / user "Reply with exactly one word: pong" / max_tokens 1 (precedent: `scripts/provider_liveness.py`, the 2026-08-26 instrument)
- Cost: $0. OpenRouter probe pinned to `cohere/north-mini-code:free` (the B2-61 verified repoint) instead of `openrouter/auto` so the call is guaranteed $0 even though `OPENROUTER_API_KEY` is the funded account-1 key. z_ai got exactly ONE probe (operator's own working lane), thinking disabled, 8s timeout per providers.yaml.
- Paid keys (DEEPSEEK, XAI, HERMES) untouched, unread, out of scope.

## Results

| lane | model | ok | latency | error class |
|---|---|---|---|---|
| ollama (local) | - (GET /api/version) | yes | 8 ms | none - ollama 0.34.3 |
| ollama (local) | qwen2.5:7b | yes | 16,410 ms | none - but 16.4s for 1 token: the model was cold, not warm as briefed (lane itself answers instantly on version) |
| groq | openai/gpt-oss-120b | yes | 325 ms | none - HTTP 200, empty content + finish_reason=length: the 1-token budget was eaten by reasoning (alive, auth + quota fine) |
| openrouter | cohere/north-mini-code:free | yes | 396 ms | none - HTTP 200, empty content + finish_reason=length (alive, auth fine) |
| z_ai (raw /paas/v4) | glm-4.7-flash | no | 582 ms | HTTP 429 code 1305 "service may be temporarily overloaded" - the documented overload cadence (B2-62 measured ~1-in-3); single shot, not retried per the one-probe constraint |

## Verdict - what the night shift can lean on

1. **ollama** - alive, unlimited, free. Version answers in 8 ms. Caveat: assume a cold model load (~16 s) on first touch of a non-loaded model; budget wall-time accordingly or pin to the models already resident.
2. **groq** - alive and fast (325 ms round trip). Auth + quota good on GROQ_API_KEY. Real-content work needs more than 1 token of budget (reasoning models), which is the known lane property, not a fault.
3. **openrouter** - alive (396 ms) on a `:free` id through the funded key. The free-lane capacity (the 2026-09-26 gate-verified `:free` roster in providers.yaml) is reachable tonight.

Bottom line: the night shift has three working free lanes (ollama + groq + openrouter). That matches the estate's effective `mag/fuel_feed.py` FREE_LANES roster after the dormant gate (ox, openrouter-a1, openrouter-a2, groq) minus ox, which was not in tonight's probe scope.

## Dead-but-believed-alive

- **None hard-dead in tonight's scope.** The only probe failure is z_ai raw `/paas/v4` (429/1305), and the estate does not believe that path is a fleet lane: providers.yaml marks it `opencode_only` ("raw-API use is rate-limited 1305/1302 + fence risk"), and fuel_feed pulled the coding-plan keys from rotation on 2026-08-27. The 1305 is expected behavior on that path, not new death.
- **The inverse finding is the actionable one:** the frozen 2026-08-30 snapshot in `memory/runs/janitor/provider_liveness.json` records groq AND openrouter as DEAD with `WinError 10051` (unreachable network). Tonight both answered HTTP 200 in 325/396 ms. That old DEAD verdict was a local egress artifact of 08-30, not provider death - any surface citing the 08-30 body as current liveness truth is wrong. This receipt + the new `night_sweeps` entry supersede it.
- Two briefing corrections for the record: qwen2.5:7b was not warm (16.4 s cold-load profile on the 1-token generate), and z_ai3 (Lite) is no longer a rotation lane at all (pulled 2026-10-03, receipt `watch/inbox/LITE_LANE_PULL_20261003.md`), so "z_ai free" now means either the opencode harness path or the dormant-gated z_ai2/z_ai3 coding lanes - none of which the fleet should raw-dial.

## Banking

- Rows appended to `memory/runs/janitor/provider_liveness.json` under a new additive `night_sweeps` key (schema `provider_liveness.night_sweep.v1`); the 2026-08-30 v1 snapshot body is preserved frozen above it. File re-validated as parseable JSON after the append (1 sweep entry, 5 result rows).
- No files committed. Nothing promoted on the shared surface; this receipt is the durable artifact.
