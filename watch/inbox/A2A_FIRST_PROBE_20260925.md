# A2A FIRST PROBE - 2026-09-25/26

Seat: a2a-probe (MICKEY-17 wave). Ask: install a2a cli into the estate .venv,
fetch one public agent card, record the interop receipt. Budget: $0 (no API
money spent; all targets are free public endpoints).

## Verdict: PASS

First live A2A interop receipt is on disk. The official Google a2a-sdk client
resolved a real public agent card from the wire and decoded it into the
official `a2a_pb2.AgentCard` proto. Full evidence filed next to this receipt.

## 1. Install receipts (estate .venv, Python 3.11.15)

Ran: `C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe -m pip index versions a2a-cli a2a-sdk`
- `a2a-cli` exists on PyPI: latest 0.2 (plus 0.1.x line)
- `a2a-sdk` exists on PyPI: latest 1.1.5 (official Google SDK, author "Google LLC", home a2a-protocol.org)

Ran: `pip install a2a-sdk` -> installed `a2a-sdk-1.1.5` (+ google-auth, json-rpc, etc.)
Ran: `pip install a2a-cli` -> installed `a2a-cli-0.2` + `a2a-json-rpc-0.4`
Ran: `pip install "a2a-json-rpc==0.3.0"` -> pin applied (see finding A)

## 2. Findings

### A. a2a-cli 0.2 is shipped broken against its own dep (upstream defect)

First run of `.venv/Scripts/a2a-cli.exe --help` crashed:
`ImportError: cannot import name 'TaskSendParams' from 'a2a_json_rpc.spec'`
(a2a_cli/cli.py:43). Cause: `a2a-json-rpc` 0.4 removed names the CLI 0.2
imports; the CLI does not pin its dep. Downgrading to `a2a-json-rpc==0.3.0`
made the CLI import and show commands (send/get/cancel/watch/chat/stdio).
Second defect: with the pin, `a2a-cli --server https://sheyda-a2a-server.hf.space send "hello"`
crashes inside the tool at `a2a_cli/cli.py:199` (`asyncio.run` called inside an
already-running loop). Conclusion: the CLI is not a working interop lane yet;
the SDK path is.

### B. Soft-404 wall: copilot.microsoft.com

`GET https://copilot.microsoft.com/.well-known/agent-card.json` returns
`HTTP 200`, `content-type: text/html; charset=utf-8`, ~68 KB of SPA HTML - a
catch-all page, not a card. The official resolver correctly rejects it:
`a2a.client.errors.AgentCardResolutionError: Failed to parse JSON for agent
card` (a2a/client/card_resolver.py:189 -> :204). Lesson recorded for the
fleet: HTTP 200 at the well-known path proves nothing; require
`content-type: application/json` + JSON parse before calling it a card.
Raw HTML evidence: `A2A_FIRST_PROBE_20260925.copilot_soft404.html`
(gemini.google.com, anthropic.com, chat.openai.com, api.githubcopilot.com
all plain 404 at the well-known path; not filed, status codes only).

### C. Live public card found (the receipt)

`GET https://sheyda-a2a-server.hf.space/.well-known/agent-card.json`
-> `HTTP 200 OK`, `content-type: application/json`, 533 bytes. Public HF Space
`sheyda/a2a-server`, zero-auth. Found by probing the Hugging Face Spaces
`?search=a2a` list (most a2a spaces there are sleeping/paused; this one is up).

Raw wire card (filed: `A2A_FIRST_PROBE_20260925.card.raw.json`):
- name: `HF A2A Agent`
- protocolVersion: `0.3.0`, preferredTransport: `JSONRPC`
- url: `https://sheyda-a2a-server.hf.space/`, version `1.0.0`
- capabilities: streaming false; modes: text/plain + application/json both ways
- 1 skill: id `hello`, "Say Hello", tags [hello, demo]

### D. Interop decode (the actual probe pass)

Ran: `.venv/Scripts/python.exe watch/inbox/A2A_FIRST_PROBE_20260925.fetch.py`
Output: `RESOLVER RETURN TYPE: a2a_pb2.AgentCard` then
`RESOLVER OK: card decoded into official a2a_pb2.AgentCard proto`.

Schema mapping worth knowing (a2a-sdk 1.1.5 uses the v1.x internal card
schema): the 0.3.0 wire card's top-level `url` + `protocolVersion` +
`preferredTransport` are remapped by the SDK into
`supported_interfaces: [{url: "https://sheyda-a2a-server.hf.space/",
protocol_binding: "JSONRPC", protocol_version: "0.3.0"}]`. Lossless decode
across schema generations; filed as
`A2A_FIRST_PROBE_20260925.card.resolved.json`.

### E. Bonus round-trip: transport interop confirmed, server agent broken

Ran: `.venv/Scripts/python.exe watch/inbox/A2A_FIRST_PROBE_20260925.hello.py`
(sends `a2a_pb2.SendMessageRequest` with role USER, one text Part "hello",
via `ClientFactory` over the JSONRPC 0.3.0 transport).

Result: our full client stack (card resolve -> factory -> JSONRPC send)
worked end to end; the SERVER returned a spec-compliant JSON-RPC
`InternalError: 'HelloWorldAgentExecutor' object has no attribute 'execute'` -
the Space's executor is written against an older a2a-sdk Executor API. So:
protocol-layer interop is confirmed live (both sides spoke A2A 0.3.0
JSONRPC correctly); the application layer on that server is broken upstream.
No fix possible from our side; noted for the next seat wanting a task-completion
round-trip: need a server with a working executor (or stand one up locally).

## 3. Evidence files (this directory)

| file | what it is |
|---|---|
| `A2A_FIRST_PROBE_20260925.fetch.py` | reproducible card-fetch probe (raw GET + official resolver decode) |
| `A2A_FIRST_PROBE_20260925.card.raw.json` | exact bytes served at the well-known path (533 B) |
| `A2A_FIRST_PROBE_20260925.card.resolved.json` | card as decoded into official AgentCard proto |
| `A2A_FIRST_PROBE_20260925.hello.py` | JSONRPC message round-trip probe |
| `A2A_FIRST_PROBE_20260925.copilot_soft404.html` | the 200-but-HTML wall, raw |
| `A2A_FIRST_PROBE_20260925.md` | this receipt |

## 4. Environment state left behind (estate .venv)

- `a2a-sdk==1.1.5` (official Google SDK; imports as package `a2a`, not `a2a_sdk`)
- `a2a-cli==0.2` with `a2a-json-rpc==0.3.0` pin (0.4 breaks its import)
- httpx already present; nothing else removed or bumped

## 5. Not run / open

- No authenticated or paid endpoints probed (Google Cloud Agent Registry needs
  a GCP project; IBM/Spotfire registries are self-hosted).
- `a2a-cli chat/watch/get` commands not exercised (send path crashes, see A).
- Task-completion round-trip blocked by the server-side defect (see E).
