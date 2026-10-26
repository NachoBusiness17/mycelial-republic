# hermes docs b2 wing 11 (docs/design/multiplexing-gateway.md)

via seat-b1 beat ext-5ea2099806 folded=True

Multiplexing Gateway Design (watch/hermes_wings/b1_docs/b2doc_11.md) — a design rationale doc, not source; findings are from its described code.

1. WHAT IT DOES
Documents one gateway process serving many profiles: routes inbound platform events to a profile, then installs that profile's HERMES_HOME and secret scope via contextvars so config, state.db, sessions, and credentials resolve per profile. When isolation is impossible it fails closed (raises, drops) or is listed as a known process-global limitation.

2. DESIGN PATTERNS
- Fail-closed guard: `get_secret()` raises `UnscopedSecretError` under multiplexing instead of falling back to `os.environ`.
- Context-local override: `_profile_runtime_scope` sets contextvars, propagated via `copy_context()`, unwound in `finally`.
- Lazy handle resolution: `SessionStore` binds no DB at construction; resolves per-call to the active home's `state.db`.
- Single chokepoint: `profiles_to_serve()` is the only gate on the served set.
- Hybrid overlay registries: globals plus per-home `hermes_home_key()` overlays.

3. RISKS
- SPOF: one HTTP listener, relay ingress, and process lock owned by the default profile; secondaries may not bind ports (fatal).
- Hidden shared state: `_MULTIPLEX_ACTIVE` is a plain module global; MCP/tool discovery is first-profile-wins.
- Duplicate scheduler: external `cron.provider` silently falls back to the built-in ticker.
