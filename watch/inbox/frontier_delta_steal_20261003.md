# FRONTIER DELTA STEAL - what others did around our findings (2026-10-03)

Operator order: "this is gold, steal what others have done around these
findings." The findings: three-arm replay (frontier/flash/deepseek) of real
production asks, scored for a capability-per-cost routing table.

## THE FIELD (external steal, first pass)

- **RouteLLM** (LMSYS): learned router trained on preference data; headline
  result 85% cost reduction on chat benchmarks while retaining 95% of
  response quality. The "20% Problem" writeup (tianpan.co, May 2026) maps
  the hard cases where routing fails - exactly our falsifier-other-half law:
  a cheap MATCH means the ask was sub-frontier.
- **FrugalGPT** (Stanford): cascading - cheap model first, escalate on a
  quality gate. The ancestor of our judge-owed CHALLENGE rows.
- **Confidence-driven routers** (ResearchGate, Feb 2025): uncertainty
  estimation as the escalation trigger - decide when the weak model is
  "confident enough."
- **CRE-Router** (arXiv 2026): clustering-based pre-generation routing
  composed with a quality-estimation cascade, blending latency cost metrics.
- **LLM Shepherding** (arXiv, Jan 2026): learned a-priori routing per query.

## WHAT WE HAVE THAT THEY DON'T (the estate's delta)

1. They route on PREDICTED quality (learned preference routers, confidence
   estimators). We route on MEASURED capability: chain-verified,
   anti-cheat-scored agreement payloads from real production asks. Our
   verdicts carry cryptographic receipts; theirs carry benchmark scores.
2. They benchmark on static evals. We REPLAY the fleet's actual asks - the
   routing table regenerates from real work continuously, at $0.14 per deepseek
   arm and seat tokens per flash arm.
3. Their escalation trigger is a confidence estimate. Ours ALREADY EXISTS in
   the gwap engine's four-valued verdicts: VERIFIED_AGREE routes cheap,
   DISPUTE escalates, CHALLENGE is judge-owed - the confidence signal the
   2025 papers build whole frameworks for falls out of our scoring for free.
4. Their blind spot is adversarial: none verify that the cheap model's
   output actually engaged the material. Our hollow-batch incident (the
   {text} law: fabricated gap rows when evidence never rendered) is the
   failure class their confidence estimators miss and our agreement engine
   catches by construction.

## ADOPT (babysteps)

1. Their vocabulary in the Delta Register: win-rate per arm, cost-adjusted
   quality, escalation rate. Same ideas, our instruments.
2. Their cascade as the routing rule: ds first, flash judge gate, frontier
   on CHALLENGE - the gwap verdicts are the gate.
3. Their 20%-problem lens: our register must name the ask classes where
   cheap-and-good FAILS, not just where it wins (the frontier-only class is
   the map of what $141 buys).

Sources: search results named RouteLLM (LMSYS), FrugalGPT (Stanford,
arXiv 2305.05176 family), the 20% Problem article (tianpan.co, May 2026),
CRE-Router (arXiv 2026), LLM Shepherding (arXiv, Jan 2026), and a
confidence-driven router paper (ResearchGate, Feb 2025). Links were not
fully surfaced by the search tool; treat un-linked items as named-not-fetched.
