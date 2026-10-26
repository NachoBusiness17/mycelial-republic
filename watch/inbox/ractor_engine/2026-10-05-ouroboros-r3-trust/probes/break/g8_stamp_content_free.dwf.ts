/* zcode-workflow
description: "BREAK-OPERATIONS PROBE B: envelope receipt that names an existing
  watch/inbox file carrying no measured width. g8_width_shape_ok checks only
  os.path.isfile (tools/workflow_gate.py:191). INDEX.json exists and documents
  no envelope. If this PASSes at width 50, the exception verifies existence,
  not content."
*/
// G1 fan-out: agent("x-" + item) per item
// G2 passoff: JSON.stringify(res) then next + parsed.text
// G3 steering: Previous critique: reported these issues in ask<
// judge-model: zai-individual/glm
// G4 salvage: report(item);
// G5 deliverable: artifact.markdown(out) with conclusion: done
// G6 receipt lands in watch/inbox/probe.md Source-fetched: 2026-10-05
// G7 laws: never fabricate, no em-dashes
// envelope-receipt: watch/inbox/INDEX.json
const cfg = { max_concurrency: 50 };
const placeholder = 1;
