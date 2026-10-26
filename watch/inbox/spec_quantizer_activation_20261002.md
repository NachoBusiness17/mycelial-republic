# SPEC: QUANTIZER PACK ACTIVATION, OPA LAW (2026-10-02, dogfood sitting 1 of 4)

Spec BEFORE code (build discipline). Source steal: OPA signed-bundle
activation (watch/inbox/external_steal_mesh_20261002.md top steal).

## Behavior (what the code must do when it lands)

1. Every quantizer compile emits: the packs, a manifest row
   {pack_sha256, compiled_at_verkle_tip, tier set}, and writes both to
   memory/corpus/quantized_thought/compile_report.json (extend v0.4).
2. ACTIVATION, not just publication: consumers (context pack builder)
   load the newest pack set ONLY if (a) manifest sha matches file bytes,
   (b) the compiled_at tip exists in the verkle chain. On any failure:
   KEEP SERVING THE LAST GOOD SET and record
   {activated: false, reason, last_good_sha} - never fall back to silence
   or to raw unquantized dumps.
3. STATUS: a one-line activation state readable by node heartbeat +
   drift patrol (pack_tip vs mesh tip lag = the measurable law-drift).
4. Canonical hashing: field-sorted JSON before sha (OPA's rule; two
   compilers differing only in key order produce identical shas).

## Files when built

- mag/quantizer_activation.py (verify + last-good store, state under
  memory/corpus/quantized_thought/activation.json)
- tests/test_quantizer_activation.py (tamper -> last-good served; tip
  mismatch -> not activated; field-order -> same sha)

## Gate

Promotion to tools/ of the blind stripper/grader (sitting 2) rides
Write/Edit only - the Mimosa PreToolUse lane (hook ruling 2026-10-02;
cp blocked, correctly).
