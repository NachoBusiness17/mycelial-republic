/* scenario fixture G3: single fault, no reviewer verdict carried into a
   revision ask (G3-steering fails, all other gates pass by construction).
   Minted 2026-09-26 for the LAW-12 genesis clause (watch/inbox/BURN_rsi-
   harness_20260926.md falsifier). Not a real workflow: regression input only.
   Laws carried in asks: no em-dashes, never fabricate, never synthesize.
   source-fetched: 2026-09-26 (tools/workflow_gate.py CHECKS, REGISTRY.jsonl). */
const briefs = ["alpha", "beta"];
for (const b of briefs) {
  const gopher = agent("dig-" + b, "read and quote " + b);
  report(gopher);
  const pack = head + first.text;
  const ask2 = "Reviewer notes carried into the redraft: " + rev.notes;
  await artifact.markdown("out/" + b + ".md", pack);
}
return { conclusion: "g3 fixture", receipt: "watch/inbox/" };
