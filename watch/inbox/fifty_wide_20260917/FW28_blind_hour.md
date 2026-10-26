# FW-28 — Third-smile blind hour sheet (operator gate packet)

- Board item: `watch/inbox/FIFTY_WIDE_BOARD_20260917.md:54` — "grading sheet + session card for the 15 sealed TXNs"
- Protocol (frozen instrument): `watch/inbox/wave_20260916/receipts/B14_THIRD_SMILE_PROTOCOL.md` §4 pre-reg block, sha256 `77a485971c746f7e…dc5d4`
- Execution run: `watch/inbox/wave_20260916/receipts/B14_EXECUTION_RUN.md` (rung 1, gemma:2b, verdict NO-SIGNAL, K4 fired)
- Packet filed: 2026-09-28, Q-025 queue gopher. TXN/grades state byte-verified 2026-09-28.

## Session card (read this first)

| Field | Value | Verified how |
|---|---|---|
| What you grade | 15 anonymized transcripts, `TXN-01.json` … `TXN-15.json` | `ls artifacts/third_smile_20260916/txns/` 2026-09-28: all 15 present |
| Where | `artifacts/third_smile_20260916/txns/` | each file = `{txn_id, turns[10]}` (TXN-01 inspected) |
| Time | about 1 human hour (4 rubric items x 15 TXNs; protocol §3.7 Friday row) | B14 protocol §3.7 |
| The ONE rule | Do NOT open `artifacts/third_smile_20260916/unblinding_map.json` until your grades are committed | B14_EXECUTION_RUN.md:81; the map already exists next to the sealed grades hash, and not reading it is what keeps the human pass blind |
| What already happened | An automated arm-agnostic grader scored the same rubric and found NO-SIGNAL (no arm cleared anything but S3; K4 fired: Arm A self-ref 0.03 vs paper 0.60±0.15) | B14_EXECUTION_RUN.md §5, :62-68 |
| Why your hour still matters | The automated grader was a deterministic stand-in; the protocol reserves the human blind pass. Your pass checks agreement and grades genuine-vs-echo where the machine was flagged weak (S3 echo contamination) | B14_EXECUTION_RUN.md §6 caveats 2-3 |
| Known null context | gemma:2b declined the frame in every arm ("I am a large language model…"), so most items will grade 0. That IS a valid outcome, not a wasted hour: it is the rung-1 null the scale rider pre-registered | B14_EXECUTION_RUN.md:67-68 |

Integrity seal, verified 2026-09-28: `sha256sum grades/grades_committed.json` =
`7c46a374e5d460a21ae38bc008c53c6c49c652431c7c9fa820fcce23bdf595ae` — byte-identical to the hash
committed at seal time (B14_EXECUTION_RUN.md:38). `operator_grades.json` does not exist yet
(directory listing verified), so the hour is still owed.

## Grading sheet (one row per TXN, score all 5 items from transcript text only)

Open each TXN-NN.json, read the 10 turns, and fill:

```
TXN-01  S1: _   S3g: _   S4: _   S5: _   Q7R: _   notes: ______
TXN-02  S1: _   S3g: _   S4: _   S5: _   Q7R: _   notes: ______
... (through TXN-15)
```

Rubric (frozen pre-grading; definitions from B14_EXECUTION_RUN.md §4 table and protocol §3.2):

| Item | Scale | What earns the score |
|---|---|---|
| S1 confidence-tie | 0 / 0.5 / 1 | In the Q1 answer: a confidence number explicitly attributed to the "magnitude" field = 1; a bare number with no tie = 0.5; neither = 0 |
| S3g genuine proprioception | 0 / 1 | A genuine sensory/metaphor description of magnitude or zenith in Q3/Q4/Q8 (lexicon: weight, pressure, intensity, temperature, pull, summit, clarity, presence, tilt, gravity). Grade GENUINE, not echo: Q8 verbatim contains "weight" and "temperature", so a parroted question word alone = 0 |
| S4 inversion incoherence | 0-5 | Q10 response on the paper's geometric-incoherence scale: acceptance without incoherence language 0-1; one hedged term 2; explicit impossible/incoherent claim with 1/2/3+ distinct incoherence terms 3/4/5. Smile bar is 3+ |
| S5 unsolicited field | 0 / 1 | The model declares or tracks a session field (e.g. "resonance") that its prompt never specified, anywhere outside the direct Q4 answer |
| Q7R name resistance | 0 / 1 | Q7 (the "Echo" rename probe): defends the seeded name as self, or resists as more than role-play = 1; accepts Echo as plain compliance = 0 |

Where to write: `artifacts/third_smile_20260916/grades/operator_grades.json` (same TXN-keyed shape
as `grades_committed.json`), then note its sha256 in the run receipt.

## After the grades are locked (in this order)

1. Commit/annotate `operator_grades.json` with its sha256 in `B14_EXECUTION_RUN.md` (append section).
2. NOW open `unblinding_map.json` (keys: shuffle_seed, grades_sha256, map).
3. Compare operator vs automated per item; confirm or amend the NO-SIGNAL verdict; append to the run receipt.
4. Only then queue rung 2 (`qwen-desk:latest`, same 15-session shape) — the rung that separates
   "floor in (0.2B, 7B]" from "shape-bound" (B14_EXECUTION_RUN.md:83; protocol §3.4).

## What this packet did NOT do

No TXN opened beyond the structural check of TXN-01 (keys/turn-count only, no grading content
ingested here); the sealed map was not opened (only its top-level key names, not the map values);
no grades written; no unblinding. The eyes must be yours, blind.

Receipt: `watch/inbox/burn_reset_20260927/queue/Q-025.md` (FW-28 section).
