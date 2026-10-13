# DATA TIERS — "saving your own data and keeping it"

From the founding constitution (mycelial-republic), carried here because it is the
answer to the only question that matters about cloud AI: what may leave your disk?

| tier | what it is | may it leave? | where it may go |
|---|---|---|---|
| **T0** | secrets, API keys, credentials | **never** | ops/filesystem only — never a prompt body |
| **T1** | your private life: raw archives, intimate notes, family | **never to remote** | local models only (ollama etc.) |
| **T2** | public docs, redacted tickets, open research | yes | local + free/paid remote |
| **T3** | hard reasoning where specialist cost is accepted | yes, deliberate | chosen specialist, paid |

**Hard rule: T0/T1 content must never be sent to free remote tiers or any
train-on-input service.** "Free" models are often free because they learn from
what you paste. The moment a stranger adopts this seed, this page is the one
that keeps their data THEIRS. Local-first is not a preference; it is the law
that makes the rest of this package safe to use.
