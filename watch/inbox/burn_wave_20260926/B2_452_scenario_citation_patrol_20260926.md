# B2-452 Patrol scenario-card registry citations, 2026-09-26

## Verdict

LANDED. Scenario-card citation liveness now rides on every improve --status read: mag/improve.py status_summary carries a workflow_scenarios block {_scenario_citation_liveness(): ok, cards_checked, orphaned, registry}, so a REGISTRY.jsonl rewrite/prune/renumber that orphans a card's cited FAIL row is named at every status read instead of only when tools/workflow_gate.py itself changes (the gate's --scenarios run is the only other validator and is gate-edit-gated, exactly the gap the brief names). Live production read: {"ok": true, "cards_checked": 7, "orphaned": []} — all seven cards' cited (ts, digest) rows live and verdict FAIL. The brief's falsifier is proven on a sandboxed copy: a GHOST.card.json citing a nonexistent (ts, digest) with a missing registry path returns ok false naming "GHOST.card.json: cited FAIL row (ts=..., digest=deadbeefdead..) not in REGISTRY". Scope is citation liveness only (the brief's named need); the full fixture replay stays in the gate's --scenarios mode. Production REGISTRY.jsonl and the cards were never mutated. This closes the brief as the recurring-surface arm; the "register the gap with a reason" fallback arm is therefore not needed.

## Evidence file:line quotes

- mag/improve.py _scenario_citation_liveness (post-edit) docstring: "B2-452 (2026-09-26): scenario-card citation liveness on a recurring surface. The seven gate cards validate their cited_fail_row (ts, digest) against memory/workflows/REGISTRY.jsonl only inside the gate's --scenarios run, which fires only when tools/workflow_gate.py itself changes ... This check names orphans on every improve --status read. Citation liveness only ... Read-only; parameters injectable so the falsifier can run against sandboxed copies."
- Same file, status_summary wiring: "workflow_scenarios": _scenario_citation_liveness() with the B2-452 comment.
- Live production run (this lane): "workflow_scenarios: {'ok': True, 'cards_checked': 7, 'orphaned': [], 'registry': '...REGISTRY.jsonl'}".
- Falsifier probe (sandboxed): card GHOST.card.json + missing registry -> {"ok": false, "cards_checked": 1, "orphaned": ["GHOST.card.json: cited FAIL row (ts=2026-09-26T00:00:00Z, digest=deadbeefdead..) not in REGISTRY"]}; clean arm re-run against production -> ok true, 7 cards.
- tools/workflow_gate.py:146 load_registry_index (the (ts, digest) keying this check mirrors) and :164 validate_card (the full validator whose heavy fixture replay stays gate-side).
- tests after the edit: tests/test_improve_status_scheduled_task.py + tests/test_improve_provider_probe.py = 21 passed (status_summary consumers unbroken).

## Work done

- Claim law: mag/improve.py was already claimed by this lane for the B2-361/B2-493 pair; this edit extends the same claim window (same file, same lane, no concurrent foreign claim on the status_summary region; QUEUE re-read per the law before the edit).
- Implemented _scenario_citation_liveness(cards_dir, registry_path=None) with injectable parameters (production defaults; sandbox for the falsifier), read-only over the cards and REGISTRY, mirroring the gate's (ts, digest) keying; wired into status_summary as workflow_scenarios.
- Proved both arms live: production 7/7 clean; sandboxed orphan named; status consumers' tests green (21 passed); py_compile clean; em-dash 0 in my added lines.
- Filed this receipt, the LEDGER row, and the QUEUE row flip.

## Falsifier

- The brief's falsifier, executed on a copy: remove (or point away from) a cited FAIL row and the recurring surface names the orphaned card — proven above; rerun by deleting a REGISTRY row on a copy and passing its path in.
- Production falsifier check: after any future REGISTRY prune/renumber, improve --status must show workflow_scenarios.ok false naming the card, or this landing is dead.
- The check is citation-liveness only: a card whose cited row exists but whose FIXTURE no longer reproduces is out of scope here and remains the gate's --scenarios run's job (named so the scope gap is visible, not hidden).
- An unreadable card is counted as orphaned (loud), never skipped silently.

## Bibliography closed

tools/workflow_gate.py (load_registry_index, validate_card, --scenarios mode docstring); configs/workflow_gate_scenarios/*.card.json (7 cards); memory/workflows/REGISTRY.jsonl (read-only index source); mag/improve.py (status_summary pre/post-edit, new helper); tests/test_improve_status_scheduled_task.py, tests/test_improve_provider_probe.py. No web sources. Em-dash count 0.
