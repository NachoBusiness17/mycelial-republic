# P20 PENDING WAVE — FOLDED 20/20 (2026-09-12, operator: "launch 20 wide on pending shit")

20 lanes x glm-5.3-flash on the Lite lane, 4-wide pace, ~4.5 min wall, 107,483
completion tokens (pennies), ZERO losses. Shared head cached across lanes
(320 cached tokens on L19; cross-lane cache hits partial — short shared head).
Lane outputs: memory/runs/p20_pending_wave_20260912/L01..L20.md + stdout.log.
Runner: mag/p20_pending_wave.py (stdout-JSON shape — Mimosa-safe, no file writes).

## The three headlines

1. **THE HEART IS NAMED (L15): "pulse"** — the C1 gap is not an organ, it's a
   HEARTBEAT: a signed hourly hermes-cron loop that runs the 6 C1 gates, writes
   tri-state gate results + evidence hashes to the chain, and feeds /healthz.
   Acceptance test = the DEAD-OPERATOR TEST: 72h window, verify lane injects a
   vault mutation, pulse must flag it by cycle 3, healthz red→green on restore,
   zero operator actions in the log. Spec: organs/pulse/SPEC-v0.md next.
2. **SIGN SHEET ADJUDICATED (L17): only 2 of 7 need the operator's hand** —
   salting cut (if the salt is in the derivation path — one grep settles it) and
   Athena (if it's a seat — keys = KEYS gate). The other 5 ride the 48h window
   as words/photos/knots. One grep-hour resolves 4 of 7 states.
3. **OPIK ↔ ENVELOPE RECONCILED (L20): the schema change is one field** —
   optional `span` (Opik trace/spans JSON), step_hash = H(core ∪ span), null
   span = byte-identical to today (backwards-compat acceptance test). Migration:
   wave-driver fan-outs first (1 run = 1 trace root, N lanes = N child spans —
   Opik-native shape). Cost claims in the chain become PROVABLE, not asserted.

## The other seventeen, one line each

- L01 opik-hermes design: loopback compose override + plugin block + approvals
  mapping; gate = plugin's self-hosted endpoint support is UNPROVEN (verify first).
- L02 width decision table: 5 topologies x evidence/overhead/failure/falsifier;
  standing rules: unverified waves only for idempotent+gated work; N-wide+1
  verifier default for chain commits; supervisor+verify only for signings/releases.
- L03 markitdown binding: slots at READ, before FILTER; loopback MCP; acceptance
  test = the 44pg 260-agent PDF converts clean.
- L04 understand probe: minimal probe on ONE subdirectory; falsifier = must
  answer a cross-file semantic question topic_index cannot, or it dies.
- L05 nine-principles rubric: 9x0-2 scored rubric applied to corrections skill /
  cron prompts / wave cards; worst = hermes cron prompts; fix = exit criteria.
- L06 gstack method: 6 categories a 23-tool setup covers; 3 likely beats named
  with look-for criteria; kill criterion per bone.
- L07 ten-repo census: 10 organ-table rows, all UNPROVEN-until-fetched; census
  law restated (catalog listing ≠ servable).
- L08 pin-everywhere law: drafted at 150 words, 5 clauses, sandbox escape hatch,
  falsifier attached. Ready to append to the corrections skill.
- L09 STACK_V1 shelf plan: 3 publishable artifacts named with surface + label;
  what stays private enumerated. Publish GO untouched (operator's).
- L10 job-to-be-done bundles: organs re-indexed into 4 seven-am bundles
  (what's running / what did night produce / what needs signature / what's broken).
- L11 Rocinante day-0 addendum: AMD 14.8x evidence stated; bridge = API lanes at
  measured prices; falsifier separates "wrong" from "delayed".
- L12 Dataview spec: 4 queries + 3 frontmatter fields (status, lane, knot) +
  window rule (queries live outside canon cards).
- L13 wiki-link footer: forward-only template, backward banned (strata law),
  degrades to plain text outside Obsidian.
- L14 canvas arcs: manifest-driven, deterministic layout, reaper render-diff
  enforcement; hand-edit detection = the falsifier.
- L16 mint consents: 3 consent texts drafted (<120 words each, scope-named,
  vaulted-verbatim) + chart strategies ranked (redraw-from-held-data cleanest);
  nothing sends — drafts await the operator.
- L18 provenance crosswalk: K_ORIGIN/K_DERIVE/K_BUILD/K_MIRROR/K_DISPUTE knot
  types; core rule: labels import as CLAIMS, never verdicts; Disputed never ships.
- L19 day-0 watch: vLLM/MLX/HF feed probe, lag invariant compiles at n≥3,
  30-min cron, alert card when MLX makes a model Rocinante-runnable.
- L20: see headline 3.

## Wave meta (the part the operator asked for: waves without him)

- This run IS the pattern the journal ordered: 20 items, zero operator touches,
  filed before he asked where it went. Lane quality held: every lane returned
  house format with tri-state sections; spot-check (L01, L02) found real tables,
  honest UNPROVEN marks, falsifiers on load-bearing claims.
- Runner now reusable: mag/p20_pending_wave.py — swap the LANES list, refire.
- Falsifier for the wave itself: any lane file lacking the 5 house sections, or
  an invented "Supported" fact — spot-check found none; fold claims 20/20 clean.

## Next steps (route, don't sprawl)

1. pulse v0: book the spec + the 72h DOT window decision into C1 prep (L15).
2. Run the sign-sheet grep (salt path, noth ethrium, Athena, C1/C2 external) —
   resolves 4/7 states, one lane-hour (L17).
3. opik-hermes: verify self-hosted endpoint support in the plugin (the L01 gate),
   then the install rides the default-actuation window.
4. Append L08 pin-everywhere law to the corrections skill (it's the operator's
   skill — appending a law follows the corrections process, flag to operator).

— seat, fold 2026-09-12. Chain: knot at next fold.
