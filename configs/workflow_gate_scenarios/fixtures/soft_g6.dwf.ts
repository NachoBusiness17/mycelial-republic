/* scenario fixture G6 soft case: receipt mention present, dated stamp absent.
   Under t69 semantics G6-receipts is a soft WARN (row ok=false, soft=true,
   excluded from the failed set): overall PASS, exit 0. Minted 2026-09-26 for
   the LAW-12 genesis clause (watch/inbox/BURN_rsi-harness_20260926.md
   falsifier), which requires a scenario record for every soft-warn. Not a
   real workflow: regression input only. Laws carried in asks: no em-dashes,
   never fabricate, never synthesize. */
const briefs = ["alpha", "beta"];
for (const b of briefs) {
  const gopher = agent("dig-" + b, "read and quote " + b);
  report(gopher);
  const pack = head + first.text;
  const ask2 = "Reviewer reported these issues: " + rev.notes;
  await artifact.markdown("out/" + b + ".md", pack);
}
return { conclusion: "g6 soft fixture", receipt: "watch/inbox/BURN_example.md" };
// judge-model: groq/compound-mini (B2-206 cross-family firing contract; facade has no per-subagent model)
