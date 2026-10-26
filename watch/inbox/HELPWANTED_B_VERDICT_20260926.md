# Verdict receipt: HELP_WANTED brief 2, stack row "research B" (gopher t13b)

Date: 2026-09-26. One page. No em-dashes; all claims cite files below.

## Verdict: PRUNE (executed)

## Evidence chain

1. Row existed by bytes: `memory/runs/gap_map/stack.json` listed `"goal": "research B"`, complexity 3.0, stacked 2026-08-09T13:01:09Z. Raw capture: `watch/inbox/gala_20260925/afterparty/lanes/t13b.check.txt` section 1. t13a's prune of research A re-verified first (grep exit 1, check section 1b; file showed 4 items at complexity 10.0).
2. Smoke origin confirmed: `memory/runs/gpipes/p8bc0180ab9.json` (created 2026-08-09T05:13:14Z) lists goals `["research A","research B"]`, task_ids `["t-test","t-test"]` (a duplicated test id), empty tags, status "running", both live entries "unknown" with exit_code null. A smoke-test placeholder, 48 days stale, zero output. Check section 2.
3. BIND rejected: estate-wide grep for the exact string finds only documentation about the placeholder (this board, research_A.md, gala lanes, queue row Q-045 which already titles it "degenerate placeholder ask, drop candidate"); no code or config binds it (check section 3). Candidate rebind targets `memory/runs/gap_swarm_experiment/design.json` + `probes.json`: grep exit 1 (check section 4). Binding would fabricate intent.

## Actions taken

- Pruned the row from `memory/runs/gap_map/stack.json` (estate data owned by `mag/gap_map.py`, STACK_FILE line 31; the ratified board directs the prune). JSON revalidated: 2 items, complexity 5.0. Check sections 9 to 11.
- Complexity delta by bytes: capture saw 10.0 (4 items); at edit time a concurrent gopher (t13c, research C) had already pruned to 8.0 (their validation is check section 8's citation, `lanes/t13c.check.txt` section 9). This gopher removed ONLY the research B row: 8.0 -> 5.0, delta -3.0. Cumulative from board origin 12.0: 12.0 -> 10.0 (t13a) -> 8.0 (t13c) -> 5.0 (t13b). Now below threshold 6.0: batch-elevate signal un-stuck, exactly as the board hygiene section predicted.
- Kept `memory/runs/gpipes/p8bc0180ab9.json` untouched as provenance.
- Filed resolution artifact: `memory/frontier/help_wanted/resolved/research_B.md` (cites the pipe record, records the prune).
- Board `memory/frontier/HELP_WANTED.md` brief 2 annotated resolved by hand (generator law respected; not regenerated).
- Queue row Q-045 (`queue/queue_index.jsonl`, status open) points at this ask; not edited by this gopher, left for the queue owner to close.

## Byte check (finish line)

`memory/runs/gap_map/stack.json` no longer contains the exact string `"research B"`: grep exit 1, `watch/inbox/gala_20260925/afterparty/lanes/t13b.check.txt` section 10. JSON valid, 2 items, complexity 5.0: section 11.

## Bank

`watch/inbox/gala_20260925/afterparty/lanes/t13b.json`
