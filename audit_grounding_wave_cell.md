## Finding — what your cell yields
The grounding_wave is a tri-state falsification ledger where SUPPORTED claims require dual witness verification — 11/113 posts are witnessed SUPPORTED, 46 legacy/unwitnessed SUPPORTED (auto-demoted to UNPROVEN), creating a two-tiered truth hierarchy. The system's strongest claim is its own operational consistency: every claim carries an evidence pointer that must resolve, and the hash-chain integrity is mathematically verifiable.

## Evidence — what in the repo supports it (file/shape, no invention)
- `mag/grounding_wave.py` (267 lines): Implements v3 truth-gate requiring second witness for SUPPORTED claims (lines 126-132), evidence path validation (lines 153-170), and hash-chain verification (lines 173-194)
- `watch/GROUNDING_WAVE.jsonl` (113 posts): 11 witnessed SUPPORTED posts, 46 legacy/unwitnessed SUPPORTED posts with "auto-demoted from SUPPORTED: no second witness (v3 truth-gate)" notes
- `dashboard/static/grounding_wave.md`: Human-readable rendering of the ledger showing the two-tiered structure
- `watch/inbox/ASTRA_ASK_FOLD_20260913.md`: Reading path compilation that positions grounding_wave as the "ledger discipline" after chain and fanout

## Risk if wrong — what the audit breaks on if this is missed
Matthew Steiniger's EUT theory views the chain as a "single scalar line" — he will likely test the mathematical consistency of the hash-chain integrity and the witness-supply mechanism. Missing the dual-witness requirement would make the SUPPORTED tier appear fraudulent when he discovers the 46 legacy claims lack proper verification. The evidence path validation is also critical — dead evidence paths would break his reproducibility requirement.

## The act — the concrete prep step (file/spec/number)
Create a witness ledger companion file: `watch/grounding_wave_witnesses.jsonl` containing only the 11 witnessed SUPPORTED claims with their witness identities, and a separate README explaining the v3 truth-gate mechanics. Number: 11 witnessed claims to verify, 46 legacy claims requiring witness upgrade.

## Falsifier — what would prove this wrong
A witnessed SUPPORTED claim with dead evidence path, or a hash-chain integrity failure during verification. The system's own `verify()` function would catch both — currently returns FAIL due to 4 missing evidence files (rows 75, 76, 86, 105), requiring either restoration or evidence pointer correction.