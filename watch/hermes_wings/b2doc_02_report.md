# hermes docs b2 wing 02 (docs/chronos-managed-cron-contract.md)

via seat-b1 beat ext-c8d031f413 folded=True

Report on watch\hermes_wings\b1_docs\b2doc_02.md

Note: this file is a wire-contract spec (markdown), not source. Findings are from the file's own text only.

1. WHAT IT DOES
The document specifies how a Hermes agent outsources cron timing to a NAS-side "Chronos" provider: the agent computes each job's next fire time, arms exactly one one-shot via `POST /api/agent-cron/provision`, and can scale to zero between fires. At fire time NAS relays a signed call back to the agent's `/api/cron/fire`, where a NAS-minted JWT is verified and the job runs, then re-arms.

2. DESIGN PATTERNS (named in the file)
- Reconcile loop: `reconcile()` diffs desired `jobs.json` against armed one-shots on boot, mutation, and post-fire, self-healing missed provisions.
- Compare-and-set claim: `claim_job_for_fire` gives at-most-once execution across relay retries and N replicas sharing one `HERMES_HOME`.
- Pluggable strategy: `get_fire_verifier()` swaps the NAS-JWT verifier for a cron-key mode with no handler change.

3. RISKS
- SPOF: NAS is on every fire path; its outage silences all cron (no periodic wake by design). `agent_callback_url` is persisted at provision and goes stale if the URL changes.
- Hidden mutation: `mark_job_run` deletes the job under a name implying a status write.
- Duplicate scheduler: the built-in in-process ticker remains, gated only by `cron.provider` config.
