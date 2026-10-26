/* scenario fixture G8: single fault, the script declares max_concurrency 10
   with no measured envelope receipt stamp anywhere (G8-width-shape fails hard;
   all other gates pass by construction). Minted 2026-10-05 for
   curiosity-register row 3 r03#1 (corpus/steal/MASTER_READ_ESTATE.md):
   converts the TETHERED_LINK width law (corpus/steal/TETHERED_LINK_STEAL_20260925.md,
   amended by B2-435) from AGENTS.md prose into a submit-time gate. Not a real
   workflow: regression input only. Laws carried in asks: no em-dashes, never
   fabricate, never synthesize sources. source-fetched: 2026-10-05
   (tools/workflow_gate.py CHECKS, REGISTRY.jsonl). */
const briefs = ["alpha", "beta"];
const shape = { max_concurrency: 10 }; // the G8 fault: width above 3, no receipt
for (const b of briefs) {
  const gopher = agent("dig-" + b, "read and quote " + b);
  report(gopher);
  const pack = head + first.text;
  const ask2 = "Reviewer reported these issues: " + rev.notes;
  await artifact.markdown("out/" + b + ".md", pack);
}
return { conclusion: "g8 fixture", receipt: "watch/inbox/" };
// judge-model: groq/compound-mini (B2-206 cross-family firing contract; facade has no per-subagent model)
