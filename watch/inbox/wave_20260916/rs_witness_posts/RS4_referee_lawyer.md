# WITNESS 4 - THE REFEREE LAWYER

- lane: or-union-alpha (stealth/union-alpha)
- temperature: 0.25
- usage: {'prompt_tokens': 673, 'completion_tokens': 437, 'total_tokens': 1110, 'cost': 0, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 12, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0, 'upstream_inference_prompt_cost': 0, 'upstream_inference_completions_cost': 0}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}

POST:
“First successful non-movement verb” is underspecified: does inspect wake the boss? Can success depend on an encounter not yet loaded? Define eligible verbs, scope encounters by instance ID, and commit verb acceptance plus load atomically. Two clients must not double-load. Leaving, disconnecting, and restarting must not reset encounters. DONE requires an authoritative victory predicate, not merely IN_PROGRESS.

Next fractures:
- Signed packs prove issuance, not ownership or unspentness. Transfers and consumption need atomic, uniquely identified ledger events; copied receipts cannot duplicate items.
- Death needs one durable transition covering losses, rewards, and respawn. Disconnect cannot cancel it.
- Resume must reconcile player and world history at a committed sequence; independent files invite forks.
- Seed plus moves is insufficient once scheduling and time matter: record authoritative ordering, timer events, and rules versions.
- Turn limits belong to encounters or leases, never world lifetime.

NUANCE:
A 0.35-second server telegraph can expire before Discord displays it; rollability needs a declared delivery-and-input timing contract, not just timestamps (amends M3).

DIFFERENT:
Build a durable, sequenced world-event log before player files. Player ledgers and signed receipts become projections of committed events, not competing authorities. Use idempotent commands, transactional encounter transitions, and explicit timeout policy. Test crash-between-steps, simultaneous activation, receipt reuse, and disconnect-before-death before adding content.
