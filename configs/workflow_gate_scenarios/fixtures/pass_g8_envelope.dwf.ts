/* scenario fixture G8 exception: the same width above 3, documented with a
   measured envelope receipt (G8-width-shape passes via the receipt exception;
   all other gates pass by construction). Minted 2026-10-05 for
   curiosity-register row 3 r03#1 (corpus/steal/MASTER_READ_ESTATE.md).
   The receipt named below exists on disk (verified 2026-10-05) and carries the
   proven-width table from the gala envelope re-measure. Not a real workflow:
   regression input only. Laws carried in asks: no em-dashes, never fabricate,
   never synthesize sources. source-fetched: 2026-10-05. */
const briefs = ["alpha", "beta"];
const shape = { max_concurrency: 10 }; // over the base cap, under the measured envelope
// envelope-receipt: watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md (B2-476 proven widths)
for (const b of briefs) {
  const gopher = agent("dig-" + b, "read and quote " + b);
  report(gopher);
  const pack = head + first.text;
  const ask2 = "Reviewer reported these issues: " + rev.notes;
  await artifact.markdown("out/" + b + ".md", pack);
}
return { conclusion: "g8 exception fixture", receipt: "watch/inbox/" };
// judge-model: groq/compound-mini (B2-206 cross-family firing contract; facade has no per-subagent model)
