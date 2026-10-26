# SW03 sw-econ-2

lane model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-09-29T00:18:18.808438+00:00
dt: 9.0s

---

I can’t verify several current-policy details precisely enough to cite them as fact, so I’m marking those **OWED**.

### What I can state with reasonable confidence
- **No free tier is SLA-backed.** All three (Gemini API free, OpenRouter community `:free` models, Groq free) reserve the right to change limits, models, or access without notice. Production means you cannot depend on uptime or rate-limit stability.
- **Data terms vary by provider and change.** Whether free-tier calls are used for training is a contractual point, not a technical one, and Google/OpenRouter/Groq have updated these clauses multiple times. I don’t have a verified current snapshot of the exact Gemini free-tier training clause, OpenRouter’s data flow for `:free` models, or Groq’s latest free-tier commercial-use language.
- **Silent routing/downgrades.** OpenRouter’s `:free` models are especially opaque here—providers can retire or replace a free endpoint without notice. Gemini and Groq are more likely to throttle than silently swap models, but I cannot verify a specific “silent downgrade” policy for any of them.

### OWED (verify against current docs)
- **Gemini API free tier**: current rate limits, whether API key calls areopt-in/opt-out of training, and exact Google AI Studio vs. Gemini API difference.
- **OpenRouter `:free` models**: per-model provider ToS, data residency, and whether OpenRouter itself has a unified free-tier data policy (it doesn’t—it’s inherited from the upstream model owner).
- **Groq free tier**: current RPM/TPM, commercial-use permission, and data-training clause.

### Practical boundary where free stops being safe for production
Treat free tiers as **prototyping only** when any of these are true:
1. The call affects revenue, user-facing latency, or compliance data.
2. You need a guaranteed request ceiling or uptime SLA.
3. You cannot tolerate a model/endpoint disappearing or a silent policy change.
4. You need a data-processing agreement (DPA) or training opt-out guarantee.

If you want, I can help you write a “free-tier risk checklist” you can attach to your deployment runbook, or draft the specific ToS-verification queries to send to each provider’s support.
