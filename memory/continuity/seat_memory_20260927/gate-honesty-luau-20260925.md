---
name: gate-honesty-luau-20260925
description: FEEDBACK 9/25 — the gate lied twice and got fixed; commit went out
  before a green gate (process failure); luau-lsp parse output is the only
  authoritative syntax verdict; python block-balance lint is advisory only;
  PARSE_FAILS regex must match ANY SyntaxError line
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_d7f6f4b6-0b61-484e-8bea-0408db77ca4f
---

During the DF-wiki build the generated ArtifactLore.luau shipped with invalid
Luau (`ArtifactLore.DWARVEN: { Word } =` — field type annotations like that
are not valid; use locals + assignment), init.server had a multiline print
hitting Lua's ambiguous-call rule (`"str"\n\t:format(...)`), GalleryZone had a
tuple type annotation (`{ { string, string, number } }` — Luau has no tuple
types), and the commit went out BEFORE the gate was green. Worse, the gate had
said PASS: its PARSE_FAILS regex missed the `Expected ')'` error class, and
the python block-balance lint false-positives on keyword-looking words inside
strings (flagged clean files, missed nothing real).

**Why:** a gate that can lie is worse than no gate — it launders broken code
through "GATE PASS" language.

**How to apply:** (1) never commit before the gate is green, no matter how
mechanical the fix seems; (2) luau-lsp analyze output is the ONLY authoritative
syntax verdict — the python block-count heuristic in tools/luau_lint.py is
advisory; (3) fail the gate on ANY "SyntaxError" line in raw analyze output,
not a hand-enumerated subclass (the `Expected ')'` class escaped a narrow
regex); (4) when the gate and the lint disagree, trust the parser; (5) verify
against raw output (`/tmp/mountain_analyze.txt`), not the filtered summary.
All fixed in tools/mountain_check + commits 65c4af34a..b939e45ba.

**Third lie, same session (fixed fa268fcbd):** the redirect `2>&1 > file`
sends the analyzer's stderr to the TERMINAL and only stdout to the counted
file — parse errors never entered the tally and the gate said PASS with a
live SyntaxError. Order must be `> file 2>&1`. And the field-annotation bug
(`Foo.BAR: { T } =` instead of `local BAR: { T }` + assignment) was repeated
in Worldgen.luau minutes after being fixed in ArtifactLore — same mistake
twice in one session means the lesson goes in memory, not just the moment.

Related: [[mountain-headless-polish-20260925]], [[no-fabrication-law-20260919]]
