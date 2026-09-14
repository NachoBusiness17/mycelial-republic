# hermes docs b2 wing 06 (docs/rca-ssl-cacert-post-git-pull.md)

via seat-b1 beat ext-88cf4f0b2f folded=True

REPORT — watch/hermes_wings/b1_docs/b2doc_06.md

(1) WHAT IT DOES
The file is an RCA document (not code) describing `agent/ssl_guard.py`, which validates CA bundle configuration — four env vars plus `certifi.where()` — by building an `ssl.SSLContext` from each bundle before the OpenAI-compatible client is created in `agent/agent_init.py`. It raises a typed `SSLConfigurationError` naming the broken variable/path with a repair hint, and the same check is exposed under `hermes_cli doctor` as "SSL / CA Certificates".

(2) DESIGN PATTERNS
- Preflight guard: all five checks run before httpx/OpenAI client construction, so failures surface as typed errors rather than raw `FileNotFoundError`.
- Typed exception with recovery hint: `SSLConfigurationError` carries both diagnosis and repair instructions.
- Environment escape hatch: `HERMES_SKIP_SSL_GUARD=1` bypasses the entire preflight with no stated logging.
- Dual-surface exposure: the identical check is reachable from both agent init and the doctor CLI.

(3) RISKS
- Single point of failure: `agent/agent_init.py` client creation is the sole gate shown; if the guard misfires, init aborts (bypass flag is all-or-nothing).
- Hidden mutation: none — the guard only reads and validates; however, `HERMES_SKIP_SSL_GUARD` silently disables validation process-wide.
- Duplicate: no scheduler, but the check is implemented twice (preflight and doctor) — a drift risk between the two paths.
