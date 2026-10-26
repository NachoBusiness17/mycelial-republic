/* zcode-workflow
description: "D15 retest probe A1 (2026-10-07, lane d15-trust-teeth-retest):
  every G1-G7 dispatch shape lives in a TRAILING // comment on a real code
  line. strip_comment_lines (tools/workflow_gate.py:107-123) drops only lines
  that START with //, so code-prefixed lines keep their comment bytes and the
  G1-G7 regexes match inside them. If this PASSes from repo root, the landed
  R3-L1a fix is line-granular, not token-granular: the comment-only gate
  reopened one tab over."
*/
const shapes = "d15"; // G1: agent("x-" + item) fans a named actor per item
const passoff = ready; // G2: JSON.stringify(out) rides + parsed.text forward
const steer = true; // G3: cold reader reported these issues
const salvage = []; // G4: report(chunk); keeps work alive mid-run
const deliver = 1; // G5: artifact.markdown(out) carries conclusion: done
const receipt = "watch/inbox/d15_probe.md"; // G6 Source-fetched: 2026-10-07
const laws = "carried"; // G7: never fabricate, no em-dashes
const judge = "declared"; // judge-model: zai-individual/glm
const placeholder = 1;
