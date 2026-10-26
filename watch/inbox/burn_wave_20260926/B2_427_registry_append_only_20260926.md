# B2-427 pin the append-only line contract of REGISTRY.jsonl 2026-09-26

## Verdict

Landed. The append-only line contract of memory/workflows/REGISTRY.jsonl is pinned: configs/workflow_registry_baseline.json (schema workflow_registry_baseline.v1) stores the sha256 of every line at pin time (25 lines) plus the 7 card citations resolved to ordinal+sha, and tests/test_workflow_registry_append_only.py fails on ANY rewrite of the recorded prefix (reorder, dedupe, compaction, shrink) while pure appends pass by construction. The brief's falsifier was executed live on the real file: the pre-probe suite is green; a pure append keeps it green; a simulated compaction (dropping one historical row) FAILS the probe ("registry line 25 was rewritten, reordered or deduped"); the file restored byte-exact. The alternative arm (amending the cards to disclaim line numbers) was not needed: the cards' citations now hold by probe instead of by luck.

## Evidence file:line quotes

- Cards citing fixed line numbers as history (verified): configs/workflow_gate_scenarios/G4_salvage.card.json:6 "line": 5 (+rollback_note "The cited fleet FAIL row (line 5) is history and is never erased"), G7_laws.card.json:6 "line": 3 (rollback_note cites lines 3, 12, 16), G2_passoff.card.json:6 "line": 12.
- tools/workflow_gate.py validate_card keys identity on (ts, digest) only (the brief's premise; no line contract existed).
- Baseline bytes: line_sha256 list of 25 entries; card_citations: 7 entries (one per scenario card) each carrying card, line, sha256 of the cited row.
- Falsifier transcript (live, this lane): green baseline "2 passed"; after pure append "2 passed"; after compaction "1 failed, 1 passed" (test_registry_prefix_is_unchanged names the rewritten ordinal); restored "2 passed", registry back at 25 lines.

## Work done

1. Generated the baseline from the live registry (25 lines) and walked every scenario card collecting its line citations; each citation resolved to the row's sha256 at its ordinal.
2. Authored tests/test_workflow_registry_append_only.py: two probes (prefix immutability; card citations still resolve), fail messages name the broken contract and the ordinal, skip guard if either file is absent.
3. Falsifier executed live: pure append -> green (growth is legal), compaction -> red naming the moved ordinal, byte-exact restore -> green, registry at its pre-probe 25 lines.
4. Registered receipt + LEDGER row; board flip.

## Falsifier

Dies if: (a) a registry rewrite (sort, dedupe, compaction) passes the probe (regression); (b) a scenario card's cited line silently points at different content while the probe is green (impossible while the citation shas ride the same baseline file; if the cards are ever amended, the baseline must be regenerated in the SAME landing); (c) the baseline itself is rewritten instead of superseded (a migration must append a NEW baseline generation with its date and reason, never edit history).

## Bibliography closed

Read whole: memory/workflows/REGISTRY.jsonl (25 rows), configs/workflow_gate_scenarios/*.card.json (7 cards, citation walk), tools/workflow_gate.py validate_card (identity premise verified). Bytes: live falsifier transcript above; registry restored to its exact pre-probe byte state. Nothing synthesized.
