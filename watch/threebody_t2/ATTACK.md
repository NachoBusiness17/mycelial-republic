# ATTACK — T2 (ONI, attack lane)

## Claim 1 — `--record` has zero callers — **KEEP (re-run, evidence correct by luck)**
`--record` at ask_router.py:210 routes to `cmd_record` (:214, body 181-199: stdin JSON → ledger.jsonl → verkle). Global grep `--record|cmd_record` (excluding ask_router.py) → **empty**. Verdict holds.
**AMEND the Sancho "5 importers" framing:** 4 named files are FALSE POSITIVES — bard.py:727,782, corpus_wave.py:60, doctor.py:116, doctor_agent.py:96 all match the substring `task_router`, a different module. Real ask_router importers: afk_cadence.py:112/186 (`route(...,dry=True)`), dogfood_audit.py:192 (`route`), organ_map.py:294 (metadata). Two read-path importers, ZERO write-path callers.

## Claim 2 — "no wire, sequencing≠composition" — **KEEP (survives steelman)**
Steelman: lanes POST outcome via existing API. Refuted. api_gateway.py:204-222 `/v1/chat` is an "Epoch 1 placeholder": requires `body.text` (prompt string), no `{lane,ok,cost_usd}` schema, never reaches cmd_record. seat_dispatch.py:158 + 171-172 folds to `work_register.record` (different ledger). Closing the loop needs new wiring. PROPOSER's sequencing framing was right.

## Weakest sentence
§1 "no file in /mag/mag calls it" — true but conflates import with invocation; the task_router false-positive grep would make a checker doubt it.
