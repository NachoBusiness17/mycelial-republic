/* scenario fixture: all-pass control for the LAW-12 genesis clause
   (watch/inbox/BURN_rsi-harness_20260926.md falsifier). Minted 2026-09-26.
   Not a real workflow: regression input for tools/workflow_gate.py
   check --scenarios. Laws carried in asks: no em-dashes, never fabricate,
   never synthesize sources. source-fetched: 2026-09-26 (gate source and
   REGISTRY.jsonl rows cited in the scenario cards). */
const briefs = ["alpha", "beta"];
for (const b of briefs) {
  const gopher = agent("dig-" + b, "read and quote " + b);
  report(gopher);
  const pack = head + first.text;
  const ask2 = "Reviewer reported these issues: " + rev.notes;
  await artifact.markdown("out/" + b + ".md", pack);
}
return { conclusion: "control green", receipt: "watch/inbox/" };
// judge-model: groq/compound-mini (B2-206 cross-family firing contract; facade has no per-subagent model)
