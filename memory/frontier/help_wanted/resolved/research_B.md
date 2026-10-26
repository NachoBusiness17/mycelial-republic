# Resolution: HELP_WANTED brief 2, stack row "research B"

- Resolved: 2026-09-26 by gopher t13b. Verdict: PRUNE (executed). Complexity of the row: 3.0, stacked 2026-08-09T13:01:09.568295Z.
- Raw evidence: `watch/inbox/gala_20260925/afterparty/lanes/t13b.check.txt` (sections cited below). Receipt: `watch/inbox/HELPWANTED_B_VERDICT_20260926.md`.

## Why PRUNE, not BIND

1. The row existed by bytes: `memory/runs/gap_map/stack.json` listed `"goal": "research B"`, complexity 3.0 (check section 1).
2. Smoke origin confirmed: `memory/runs/gpipes/p8bc0180ab9.json` (created 2026-08-09T05:13:14Z) lists goals `["research A","research B"]` with task_ids `["t-test","t-test"]` (a duplicated test id), empty tags, status "running", both live entries "unknown" with exit_code null. 48 days stale, zero output: a smoke-test label, not a research question (check section 2).
3. BIND rejected: estate-wide grep for the exact string "research B" finds only documentation ABOUT the placeholder (this board, resolved/research_A.md, gala lanes, and queue row Q-045, which itself titles it "degenerate placeholder ask, drop candidate"). No code, config, or script binds it (check section 3).
4. Candidate rebind targets checked: `memory/runs/gap_swarm_experiment/design.json` + `probes.json` contain no occurrence of "research B" (grep exit 1, check section 4). Binding would fabricate intent.

## Action

- Row pruned from `memory/runs/gap_map/stack.json` (data owned by `mag/gap_map.py`, STACK_FILE at mag/gap_map.py line 31; the ratified board directs the prune). JSON revalidated: 2 items, complexity 5.0 (check sections 9 to 11).
- Complexity trajectory by bytes: 12.0 origin -> 10.0 (t13a, research A) -> 8.0 (concurrent gopher, research C) -> 5.0 (this prune, research B, delta -3.0). Now below threshold 6.0: batch-elevate signal un-stuck, matching the board hygiene note in `memory/frontier/HELP_WANTED.md`.
- `memory/runs/gpipes/p8bc0180ab9.json` left untouched as provenance.
- Byte check (finish line): `memory/runs/gap_map/stack.json` no longer contains `"research B"` (grep exit 1, check section 10).
- Queue row Q-045 (status open, `queue/queue_index.jsonl`) is the queue owner's pointer to this ask; not edited by this gopher, flagged for closure by whoever owns the queue.
