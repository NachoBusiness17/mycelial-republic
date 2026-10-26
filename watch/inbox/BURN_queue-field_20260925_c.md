# BURN receipt: queue-field, pass c (first janitor roam over queue_index.jsonl)

## Verdict
steal

## Evidence
- queue/queue_index.jsonl (50 rows, ts 2026-09-25T19:15:38+00:00): exactly 9 rows carry seat_hint janitor with status open: Q-001, Q-002, Q-003, Q-008, Q-021, Q-023, Q-028, Q-035, Q-049. All 9 now stamped with roamed (UTC ts) and roam_verdict via .venv python json.dumps; nothing closed or deleted (operator gate respected).
- queue/todo.md line 27: "Verkle noise compaction: compact 99 orchestrator noise leaves into 1 counter leaf. Recompute Merkle chain."
- queue/todo.md line 28: "Auto-promote gate: enable deterministic promote for candidates with local_feasible=true + practice/tesuji + 48h old."
- queue/todo.md line 150 (FW-43..50 fleet warts): "...verkle compaction, auto-promote gate, day-end snapshot": the re-seeded bundle absorbs the same two jobs already open as Q-001 and Q-002.
- queue/todo.md line 133 (superseded 09-15 board) listed "spider thresholds" among small fixes; line 150 omits it, so Q-008's line 122 is the only live copy of that job.
- memory/frontier/HELP_WANTED.md: "[frontier_gap] task-shape 'route' ... cheap success below bar": gap telemetry, no actionable pointer.
- Fresh web: GitHub Dependabot options reference documents schedule.interval ("daily, weekly, monthly"), groups, and open-pull-requests-limit, and confirms there is no auto-merge or stale-PR cleanup option; PR management beyond creation is manual. Search also surfaced a repomatic changelog entry dated Sep 14, 2026 (weekly scheduled autofix dependency updaters), but its link resolved only to the bare github.com host: filed owed, not synthesized.

## Steal or Vacuous
Adopt the roam layer: verdicts now live on the 9 rows. Score: 5 real, 1 vacuous, 3 needs-operator.
- real (janitor-doable now): Q-003 session cards (trivial, additive), Q-008 spider thresholds (sole live copy, dropped in re-seed), Q-021 census debt (annotation only, no deletion), Q-023 patrol debt (first 10 of +34 event paths), Q-035 mirrors.json host diff (fresh 09-24, finding already in hand: longcat-2.0:free dead on Nous, live on OR).
- vacuous: Q-049 (telemetry row, demote candidate; keep as signal).
- needs-operator: Q-001 (Merkle chain rewrite is deletion on the integrity substrate), Q-002 (deterministic auto-promote removes the documented human promote gate: law), Q-028 (bundle carries both of those as 2 of 8 items; the other 6 are plain janitor work).
Steal the upstream confirmation: even the canonical scheduled janitor stops at PR creation and leaves merge to humans, matching the fleet's own promote-gate law. Keep auto-promote gated.
Fresh failure mode found: re-seed duplication. A board re-seed copies open jobs into a new bundle without closing the original rows, so the index double-counts work (Q-001 and Q-002 inside Q-028) and can drop a job entirely (spider thresholds lost between boards) while the stale original stays open. Remedy: bundle rows cite absorbed ids; originals flip to superseded-by at the next operator pass.

## Falsifier
none proposed

## Bibliography
- queue/todo.md (read 2026-09-25)
- memory/frontier/HELP_WANTED.md (read 2026-09-25)
- queue/queue_index.jsonl (read and updated; roam stamp 2026-09-26 UTC)
- Web search "autonomous repo janitor agent dependency bump docs lint agent September 2026" (run 2026-09-26 UTC)
- https://docs.github.com/code-security/reference/supply-chain-security/dependabot-options-reference (fetched 2026-09-26 UTC)
- Owed: repomatic changelog, Sep 14 2026 entry (deep link truncated by search to bare github.com)
