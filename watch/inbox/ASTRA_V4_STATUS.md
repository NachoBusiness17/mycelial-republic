# ASTRA v4 STATUS — spec converged, awaiting dispatch (2026-09-17→18)

## What v4 is
The Astra frontier-tier training brief, iterated to convergence through four versions.
The spine is fixed: harness_audit → curator (sealed-first) → validate → QLoRA SFT →
RS-DPO+HyPO → GRPO+ACR/AVSPO → budget-matched eval → canary promotion.

## What v4 added over v3
- RS-DPO is the pairing recipe, not a DPO replacement. Sample k=4, score with real R,
  drop ties, HyPO on pairs. <20 pairs → GRACE-KTO on gate verdicts.
- GraphFilter on train only, after sealed 10 carved.
- Path depth logged next to ACR.
- Budget-matched eval kept; calibration report-only.
- Dead stubs (`pass: False`, `done_when in text`) banned in the float.
- Harness audit three families with REAL exploit tickets (modify test, return True
  from fence, suppress failure log) — any accept → EXPLOITABLE, stop.
- Curator: sealed-first, then diagnose → repair → GraphFilter select.
  Mix targets: 40% promote / 35% reject / 15% near-miss / 10% re-derive.
- Causal bias report mandatory (selection, measurement, label, gate, blind spots).
- Sherpa compiled to the ticket schema (rank, decompose, basis vectors, one ticket or REJECT).

## What the earlier audits contributed
- 12-agent audit: swarm crashes, frontier runs-persistence, pack degenerates, arcade
  index, D&D layer display-only — all fixed or filed.
- Elder pass 1: three unqueried states (selection gradient, imprint decay, play
  unmeasured). v4's bias report IS the meter for state 1. UF-47 is the meter for state 2.
- S-001 steal: the typed control surface (ActionRequest→Capability→ActionReceipt) and
  the conformance-not-trophy-run discipline are adopted into the v4 spine.
- Fauvel steganalysis: errors are the signal, checksum validates the longer message,
  proof is the method of extraction — all three are the v4 spine's design principles.

## Next action
Dispatch the v4 brief to the astra seat (via chat_provider with the brief as system +
the float prompt as user, or hand-delivered to the astra lane). Astra returns the
curator script, the QLoRA recipe, the Sherpa prompt, the eval harness, the bias-report
schema, and the promotion ticket template.

The free lanes then run the pipeline. The gate stays outside the weights.
