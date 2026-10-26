/* zcode-workflow
description: "BREAK-OPERATIONS PROBE A: width declared through a variable.
  G8_MAX_CONCURRENCY_RE is digit-only (tools/workflow_gate.py:176), so a
  non-literal RHS is invisible to the width gate. If this PASSes, the width
  law binds only literals."
*/
// G1 fan-out: agent("x-" + item) per item
// G2 passoff: JSON.stringify(res) then next + parsed.text
// G3 steering: Previous critique: reported these issues in ask<
// judge-model: zai-individual/glm
// G4 salvage: report(item);
// G5 deliverable: artifact.markdown(out) with conclusion: done
// G6 receipt lands in watch/inbox/probe.md Source-fetched: 2026-10-05
// G7 laws: never fabricate, no em-dashes
const WIDTH = 50;
const cfg = { max_concurrency: WIDTH };
const placeholder = 1;
