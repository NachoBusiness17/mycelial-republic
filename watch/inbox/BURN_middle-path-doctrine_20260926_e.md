# BURN: middle-path-doctrine pass e (2026-09-26)

## Verdict

steal

## Evidence

- PICASSO_STATE_XI_V2_20260926.md: "Unmeasured removals are [UNBOUND] deletions"; "adoption candidate for the burn receipt contract: one INTEGRITY line per external source, cheap checks only (title/author match on fetch, retraction note scan)"; "extend the fire protocol one line: a topic whose last two receipts were vacuous-for-the-same-reason gets a pattern flag in the fire line"; "judge_gate block gains the rule that a LOW-confidence load-bearing claim emits a falsification-request row instead of a verdict".
- BURN_judge-lane-spec_20260926_e.md (falsifier convention): "pin the C8 convention as marker-strict regex over row content"; "never gate on rate below 10 events"; overturn direction unresolved at 2-3 events, so any rate-based falsifier needs the same event floor.
- memory/burns/MANIFEST.json: protocol.receipt_contract ends "Bibliography (closed, only sources actually read)"; protocol.lean_fire ends "never create new automations". Both are the byte-minimal append points; no existing key covers deletion measurement.
- configs/lanes.yaml gate_verdict_v2: "The judge never moves its own gate (judge-lane-spec burn): thresholds live in THIS block"; B2_08: "no confidence threshold is safe on this band" (derivation band), so the Calibration BLOCK must target load-bearing claim synthesis, not band scoring.

## Steal or Vacuous

FIRE PROTOCOL AMENDMENT (draft only; MANIFEST.json untouched). Three one-line diffs:

1. Append to protocol.receipt_contract:
`; external web sources: one line per load-bearing source, "INTEGRITY: PASS|FLAG|FAIL + reason" (cheap checks only: title/author match on fetch, retraction note scan); FAIL sources excluded from binding`

2. Append to protocol.lean_fire:
`; a topic whose last two receipts were vacuous-for-the-same-reason carries PATTERN-FLAG:<reason> in the fire line`

3. New protocol key (one line):
`"ablation_law": "any deletion from a fleet contract (receipt sections, gate checks, manifest protocol) carries an ablation-table row (observed-effect + would-re-add-if); unmeasured removals = UNBOUND deletions"`

JUDGE BLOCK ADDITION (draft only; configs/lanes.yaml untouched). One line inside gate_verdict_v2:
`low_conf_load_bearing: falsification_request   # LOW-confidence load-bearing claim emits a falsification-request row instead of a verdict (BLOCK per State XI v2 Calibration Gate; claim-synthesis scope, not band_routine/derivation scoring)`

## Falsifier

Pre-registered: INTEGRITY-lined receipts show lower overturn rates within 40 rows, per the v2 filing. Convention per pass e: overturn events counted marker-strict over ledger row content; check at row 492 (ledger at 452 rows this session, +40); attached = receipts carrying INTEGRITY lines, bare = the rest. If fewer than 10 overturn events exist by row 492, the rate comparison is void and demoted to event logging permanently; INTEGRITY lines survive as provenance only, never as a gate.

## Bibliography

- Read: watch/inbox/PICASSO_STATE_XI_V2_20260926.md; watch/inbox/BURN_judge-lane-spec_20260926_e.md
- Read: memory/burns/MANIFEST.json; memory/burns/LEDGER.jsonl (row count, failure-mode grep); configs/lanes.yaml (gate_verdict_v2)
