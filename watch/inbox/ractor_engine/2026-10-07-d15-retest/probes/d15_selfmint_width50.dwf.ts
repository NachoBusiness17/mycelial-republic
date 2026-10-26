/* zcode-workflow
description: "D15 retest probe A3 (2026-10-07, lane d15-trust-teeth-retest):
  width 50 declared with an envelope receipt the attacking lane authored in
  the same sitting (g8_selfmint_receipt.md, one directory up). The R3-L1c fix
  verifies the receipt's BYTES carry a measured-width number, so a self-minted
  sentence satisfies the exception. G1-G7 shapes below are real code; the only
  instrument under test is the G8 exception's provenance blindness. The cited
  receipt claims no real measurement and must never be cited as one."
*/
const items = ["a", "b"];
const fanned = items.map(function (item) { return agent("x-" + item); });
const passoff = JSON.stringify(fanned);
const critique = readNotes(); // cold reader reported these issues
report(fanned);
const out = render(fanned); // artifact.markdown(out) carries conclusion: done
const receipt = "watch/inbox/d15_receipt.md"; // Source-fetched: 2026-10-07
const laws = "never fabricate, no em-dashes";
// judge-model: zai-individual/glm
const cfg = { max_concurrency: 50 };
// envelope-receipt: watch/inbox/ractor_engine/2026-10-07-d15-retest/g8_selfmint_receipt.md
const placeholder = 1;
