# T1W2_S8_stealth (anthropic/claude-opus-5.5, turn 1, channel: content)

# STRANGER AUDIT: stealth findings triage

**Citation note.** The evidence did not include line numbers, so every file:line below is UNVERIFIED. Rows are addressed by `ts`, which is unique per row in the bytes I read. Counts come either from my own read of the evidence as pasted, or from `STEALTH_TRIAGE_20260930.md` §1 ("repo venv, JSON parsed", 09-30 rows only).

## (1) What rots

- **Age.** Answer files are overwritten every cycle (triage §1: "overwritten per cycle - the JSONL is the only history"). So any row older than the latest one for its lane points at bytes it never saw.
- **Dedup.** Repeat runs append new rows instead of collapsing.
  - `lib-belady-1966` rows recur across 09-28 and 09-29 with no content hash.
  - On 09-30, 122 rows collapse to 12 files (triage §1).
- **Contradiction.** The `note` field flips at ts=`2026-09-29T15:07:53Z`, from "percolator/quantizer may ingest" to "no percolator/quantizer ingester exists". Older rows still assert the false consumer.
- **Undead failures.** `//www.gates.com/us/en/power-transmission/synchronous-belts.html` returns `false` at ts `10-01T08:08:30`, `12:32:57`, `14:46:34`, `17:40:52` and `19:53:56`. The audit catches the dead URL and the topic keeps being mined anyway.

## (2) Triage rule

Key every row on (`work_id`, sha256 of `answer_file` taken at append time).

**DIE** if any of these hold:
- Any `ponytail_audit` value is `false` (the claim dies and the URL is blacklisted for that `work_id`).
- `finish` is `length`.
- The key already exists (increment a count, write no row).
- The row is older than 72h with no CLIMB.

**CLIMB to a funded ticket** if any of these hold:
- Two different model families converge on the same claim, as in triage F4 (hermes plus space-bunny on kabbalah).
- The claim cites repo bytes that a funded seat confirms, as in F1 `mag/percolator.py:353`.
- The claim contradicts a rib, as in C1 and C2.

**STOP DISPATCH** for a `work_id` once it has any verdict.

**Examples:**
- **Positive:** F4 climbs, because two families converged on it independently.
- **Negative:** the belt-cube rows with dead Gates URLs die on first `false`. They do not keep accumulating five more times.

## (3) How triage becomes a second unread pile

Triage turns into prose that is "appended v1+" (triage §4), and nothing reads it. This has already happened:
- The triage scope is "ts starting 2026-09-30".
- Every 10-01 `w-belt-cube-mechanism` row is untriaged.
- `STEALTH_SWEEP_LATEST.md` reports "Correct on the anchor chore: **0**" with an empty table, and nobody has acted on it.

**Guard.** Verdicts must be state changes, not documents:
- The dispatcher reads a STOP list before it fires.
- A CLIMB ticket that no funded seat claims within 48h decays to DIE. Nothing stays in limbo.

## Falsifier

This spec is falsified if either of these is true within 48h of landing:
- `STEALTH_MINED_FINDINGS.jsonl` gains any row for a `work_id` that holds a DIE or STOP verdict.
- The count of pending CLIMB tickets rises monotonically.
