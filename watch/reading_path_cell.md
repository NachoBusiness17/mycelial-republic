## Finding — what your cell yields
The grounding_wave organ is the tri-state ground ledger: it records every claim as Supported/Disputed/Unproven, with a hash-chained witness and evidence path. Its purpose is to surface what the house has grounded (or not) so an outsider can read the fleet’s truth state without prior knowledge.

## Evidence — what in the repo supports it (file/shape, no invention)
- Entry file: watch/GROUNDING_WAVE.jsonl (112 rows, append-only, hash-chained via "prev" field; each row has ts, claim, verdict, evidence, note, hash).
- The organ that maintains it: mag/grounding_wave.py (single-file stdin/stdout Python; stdin = new claim JSON, stdout = updated ledger JSONL; verify() method enforces linkage and evidence paths).
- The tri-state rule: v3 rows require a second witness to stay Supported; otherwise they auto-demote to Unproven. The organ enforces this via verify() returning LINKAGE-PASS separately from admission audit.
- Witness supply: every row carries a "witness" field naming the human/seat that signed the row; Astra witness #5 (codex_seat) and operator are common witnesses.
- The 16h dark window: claims made during the dark window are UNRECORDED, not Unproven; they are backfilled by blast-radius worklist after the window closes.

## Risk if wrong — what the audit breaks on if this is missed
- If the outsider misses that rows without a second witness auto-demote, they will treat Disputed rows as Supported, breaking the tri-state contract and misrepresenting the fleet’s truth state.
- If the outsider does not know about the 16h dark window, they will misclassify UNRECORDED rows as Unproven, causing false alarms.
- If the outsider does not read the evidence path, they cannot verify the claim’s grounding, undermining the falsifier’s requirement for reproducibility.

## The act — the concrete prep step (file/spec/number)
Create the outsider’s reading guide as a concise markdown file at watch/reading_path_cell.md with exactly the headers specified in the OUTPUT CONTRACT, referencing only the repo’s concrete files and shapes.

## Falsifier — what would prove this wrong
- A row in GROUNDING_WAVE.jsonl that claims Supported without a second witness field.
- A row whose evidence path does not resolve to an existing file in the repo.
- A row timestamped within a documented dark window that is recorded as Unproven instead of UNRECORDED.
