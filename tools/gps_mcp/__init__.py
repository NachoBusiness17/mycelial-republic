"""gps-mcp v0: the capability-ledger router facade.

Routes asks to model endpoints by MEASURED pass-rate from a SQLite
capability ledger, not by marketing labels. Every routing decision
emits an append-only JSONL receipt. Ships with an in-process test-double
provider mode so the whole system runs offline for $0.

Modules:
  ledger.py     SQLite capability ledger + fixtures
  providers.py  provider config (JSON/YAML), test double, real endpoints
  router.py     ask() / cascade() routing with receipts
  server.py     stdlib JSON-RPC stdin/stdout loop exposing the tools
"""

__version__ = "0.1.0"
