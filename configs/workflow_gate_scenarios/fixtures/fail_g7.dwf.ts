/* scenario fixture G7: single fault, the asks do not carry the em-dash law
   (G7-laws fails; the no-fabrication half is present, all other gates pass
   by construction). Minted 2026-09-26 for the LAW-12 genesis clause
   (watch/inbox/BURN_rsi-harness_20260926.md falsifier). Not a real workflow:
   regression input only. Laws carried in asks: never synthesize sources.
   source-fetched: 2026-09-26 (tools/workflow_gate.py CHECKS, REGISTRY.jsonl). */
const briefs = ["alpha", "beta"];
for (const b of briefs) {
  const gopher = agent("dig-" + b, "read and quote " + b);
  report(gopher);
  const pack = head + first.text;
  const ask2 = "Reviewer reported these issues: " + rev.notes;
  await artifact.markdown("out/" + b + ".md", pack);
}
return { conclusion: "g7 fixture", receipt: "watch/inbox/" };
// judge-model: groq/compound-mini (B2-206 cross-family firing contract; facade has no per-subagent model)
