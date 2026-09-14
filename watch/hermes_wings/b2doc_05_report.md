# hermes docs b2 wing 05 (docs/profile-routing.md)

via seat-b1 beat ext-fb17aa0665 folded=True

The file is documentation (markdown), not source code, so this is read from the doc's description of the code.

(1) What it does: b2doc_05.md documents profile-based routing in a gateway, where one gateway instance serves multiple isolated profiles by matching an inbound message's origin (platform, guild_id, chat_id, thread_id) against declarative `profile_routes` to pick which profile handles it. Routing only takes effect when `gateway.multiplex_profiles: true`; otherwise behavior is identical to a single-profile gateway.

(2) Design patterns:
- Rule table with conjunctive matching and additive specificity weights (thread 8 > chat 4 > guild 2), most-specific-wins resolution.
- Injected back-reference: `BasePlatformAdapter.gateway_runner` is set on all adapters so they delegate profile resolution to the runner (dependency injection).
- Fallback chain in `_resolve_profile_home_for_source`: routed profile → active profile → `default`.
- Hierarchical matching: a thread source satisfies a route pinned to its parent channel.

(3) Risks:
- Single point of failure: one gateway process serves every routed profile — its failure takes down all communities; the single injected `gateway_runner` is the sole resolver path for all adapters.
- Hidden mutation of shared state: `_profile_name_for_source` "stamps `source.profile`" in place on the SessionSource object built by the adapter, mutating it rather than returning a resolved value.
- Duplicate scheduler: none present in this file.
