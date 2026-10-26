# SW03 sw-econ-1

lane model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-09-29T00:24:08.282792+00:00
dt: 9.1s

---

I don’t have reliably verifiable sources for the specific per-task dollar figures you asked about, so I’m marking those items **OWED** rather than guessing at citations.

**What I can’t verify (OWED)**
- **Anthropic “4× tokens vs. chat” claim:** I don’t have a confirmed published source (blog, docs, or earnings quote) for that exact multiplier. It may exist in a talk or internal slide, but I can’t cite it cleanly.
- **OpenAI / Google “agent-economics” posts:** I don’t have a verified public post from either company giving per-task $ figures for agent swarms. They publish API pricing and use-case guides, but standardized “cost per completed agent task” tables are not something I can source.
- **Production per-task $ figures:** These are almost always proprietary. Vendor blogs (e.g., Devin, Intercom, Zendesk, StackAI) sometimes share anecdotal “cost per resolution” or “cost per PR” numbers, but I can’t verify a consistent published dataset.

**What is publicly available**
- **Token price lists:** Anthropic, OpenAI, Google, and Mistral publish per-token input/output rates (e.g., Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro). Those are the starting point for any cost model.
- **Inference-cost analyses:** Firms like SemiAnalysis and Epoch AI have published per-token / per-request inference cost breakdowns, but those are usually per API call, not per “completed agent task.”
- **Estimation method:** A credible internal model is  
  `cost ≈ (input tokens + output tokens + tool-call tokens) × per-token price × retry/loop factor`.  
  Agent swarms multiply this by the number of agents and tool rounds.

If you need citable numbers, the safest path is to pull the publicly posted per-token rates and apply your own task-completion multiplier (many teams use 3–10× chat cost as a working hypothesis for agentic workloads) — but I can’t verify a specific published “4×” or per-task $ figure for you right now.
