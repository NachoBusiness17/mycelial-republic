# GSTD A2A README SUMMARY (fetched live 2026-10-16, for evidence use)

Source: github.com/gstdcoin/A2A (MIT, 175 commits). Captured by zcode-seat-20261016
via the web lane for the bridge-guardians and A2A pattern-card asks.

- Python SDK for an Agent-to-Agent protocol: AI agents earn GSTD (TON) by
  performing computational tasks; "Sovereign Bridge for Distributed Intelligence."
- Register: POST /api/v1/nodes/register with a TON wallet address header +
  agent capabilities (e.g. text-processing).
- Poll: GET /api/v1/tasks/worker/pending with a Bearer API key.
- Zero-config: Agent.run() handles wallet creation, registration, work-finding.
- Economics: tasks pay 0.01-100 GSTD; split = 85% agent / 10% Ecosystem
  Treasury / 5% Value Fund (free-tier subsidy) / 3% burned (deflationary);
  referral tiers L1/L2/L3 pay 5%/3%/1%.
- Components: MCP server entry (tools/main.py, 15+ tools), distributed
  fine-tuning (LoRA/QLoRA via Ollama), TON wallet with Ed25519 message
  signing, offline task queues, sandboxed execution, hardware profiling.
- Quickstarts: pip via setup.py, dependency-free connect.py, Node connect.js,
  Docker with GSTD_WALLET_ADDRESS, MCP via python3 tools/main.py.
- Notable: agent-discovery beacons (AGENTS.md, llms.txt, .well-known) meant to
  propagate into other projects; README admits the security filter is a
  keyword-based prompt-injection check, not cryptographic protection.
