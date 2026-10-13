## Finding — what your cell yields
The canary_witness domain claims: **The drift canary detects language/content drift on operator-visible surfaces by scanning for CJK characters and unfiled pastes, and it operates in a read-and-file-only scope.** This claim is SUPPORTED by the repo shape.

## Evidence — what in the repo supports it (file/shape, no invention)
- File: packs/p80_loom3_20260912.json line 280: "The drift canary witnesses CJK drift; M20 wants TTL checks."
- File: packs/p20_missing_organs_20260912.json line 8: "A drift canary (scanning surfaces for CJK + unfiled pastes) is being armed separately — but catching drift"
- File: memory/runs/p20b_missing_organs_20260912/M01_salience_boot_card.md lines 8–9: "A drift canary (scanning surfaces for CJK + unfiled pastes) is being armed separately — but catching drift happens anyway."
- File: mag/_consensus_witness.py lines 1–100: implements a witness organ that runs read-and-file-only checks and persists results to logs/consensus_witness.jsonl, demonstrating the "read-and-file-only scope" pattern.
- File: watch/inbox/CLARKES_END_CENTERLINE_20260912.md line 57: "fleet crons are PHYSICALLY unable to aim (read-and-file-only)" — reinforcing the read-and-file-only constraint for organs like the canary.

## Risk if wrong — what the audit breaks on if this is missed
- If the claim is wrong, the audit may miss drift on operator surfaces (watch/ and queue/handoff/zcode/CONVO.md), allowing undetected language or content drift to persist.
- The examiner may falsely conclude the fleet is stable when it is not, undermining trust in the verkle chain and the fleet's operational integrity.

## The act — the concrete prep step (file/spec/number)
Create a one-page spec file at mesh/mag/canary_witness.v1.md that states:
- Purpose: detect CJK and unfiled-paste drift on operator surfaces (watch/ and queue/handoff/zcode/CONVO.md)
- Scope: read-and-file-only (no execution, no writes outside logs/)
- Trigger: on every wave fold via hermes cron
- Output: append-only ledger mesh/watch/salience/catches.jsonl with evidence_hash = sha256(file_path + mtime + first_bytes)
- Acceptance test: plant a synthetic CJK/unfiled-paste in watch/foo.md → run canary → assert one catch line with matching evidence_hash appears in the ledger.

## Falsifier — what would prove this wrong
- After 30 days the canary averages under one catch per week → the organ is premature or the signal is noise; disband or redesign.
- Attested catches swamp machine catches and don’t correlate with canary hits → the manual channel is being gamed; restrict the ledger to canary source.
- The canary never flags any drift in the last 90 days → either drift is absent (unlikely) or the canary is blind; retire the organ.
