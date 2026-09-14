ROW
pointer: /board/environments.json
claim: SCRIBE flagged environments.json as showing 7 containers / no desktop seats — charter's "10 seats incl. desktop lanes" unverifiable
type: arbitration
confidence: H
status: CORRECTED
evidence: environments.json DOES carry a seats map with 10 entries (grok-a, grok-b, codex, grok, zcode, deepseek, blade_buyer, grok2, codex-verifier, deepseek-lanes) — but its ts is 2026-08-29T08:55Z, i.e. the file is a 2-day-old snapshot, not live. SCRIBE read the same file; the divergence is likely v reading stale cache vs current bytes. File needs a fresh host-side dump to be a reliable pointer.
