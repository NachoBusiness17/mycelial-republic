# hermes docs b2 wing 07 (docs/relay-connector-contract.md)

via seat-b1 beat ext-4910c608a7 folded=True

REPORT: watch/hermes_wings/b1_docs/b2doc_07.md (Relay ↔ Connector Contract v1)

1. WHAT IT DOES
Defines the wire contract between the Python Hermes gateway and a Node/TypeScript connector: the gateway dials out to the connector's /relay WebSocket, handshakes for a CapabilityDescriptor, then exchanges normalized inbound MessageEvents and outbound actions (send, edit, prompt, react, thread ops) over that single socket. The gateway stays platform-agnostic and holds no platform secrets; the connector verifies/decrypts at the edge, strips credentials, and owns tenant/session routing.

2. DESIGN PATTERNS
- Capability negotiation: descriptor supported_ops/supports_* flags gate new ops; legacy connectors degrade to defaults.
- Single choke point: RelayAdapter._apply_slack_thread_anchor resolves thread anchors for every send lane.
- Additive-only versioning: contract_version gates changes; unknown descriptor fields ignored for forward-compat.

3. RISKS
- Single point of failure: one authenticated WS carries inbound, outbound, interrupts, and passthrough; the connector's Redis RelayBus is the sole cross-instance hop. A wrong scope_id collides two Discord servers into one session (flagged as the #1 High-severity risk).
- Hidden shared-state mutation: SessionSource.to_dict() mirrors legacy guild_id into scope_id; prompt_response rewrites text to "/{option_id}" so older gateways route the press as a typed reply.
- Duplicate scheduler: none found; the doc explicitly bars a "parallel relay-only idle path," deferring suspend decisions to a future behaviour layer.
