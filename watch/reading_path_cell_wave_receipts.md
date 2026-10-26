# Reading path — wave_receipts (outsider guide)

## Finding
The wave_receipts domain is a single-file, stdin/stdout organ that emits append-only receipts for every lane-level event. It is the machine’s consumption meter and the falsifier’s ledger: what was written vs what was read.

## Evidence
- Entry file: `watch/steer_bus_receipts.jsonl` (append-only, schema steer.receipt.v1)
- Three things to check: (1) schema version (`v` field), (2) `applied` flag (true=actioned), (3) `verkle_event` hash (chain linkage)
- The organ: `mag/steer_receipt_wire.py` (resume-safe byte-offset reader → event_stream.emit)
- Falsifier ledger: `watch/GROUNDING_WAVE.jsonl` rows 2–3 (receipts wired into the hash chain)
- One trap: `applied=false` rows are authorized requests awaiting governor; falsifiers must ignore them unless the governor row follows.

## Risk if wrong
If the examiner misses the `applied=false` state, they will miscount authorized vs executed actions, breaking the audit’s falsifiability for governance decisions.

## The act
Create `watch/reading_path_cell_wave_receipts.md` with the above three lines and the single trap. Do not invent files; cite only repo shapes.

## Falsifier
A reviewer proves this wrong by showing a row where `applied=false` is treated as executed or where the `verkle_event` hash does not match the chain tip.
