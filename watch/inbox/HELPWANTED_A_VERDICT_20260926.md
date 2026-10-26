# Verdict receipt: HELP_WANTED brief 1, stack row "research A" (gopher t13a)

Date: 2026-09-26. One page. No em-dashes; all claims cite files below.

## Verdict: PRUNE (executed)

## Evidence chain

1. Row existed by bytes: `memory/runs/gap_map/stack.json` line 4, `"goal": "research A"`, complexity 2.0, stacked 2026-08-09T13:01:09Z. Raw capture: `watch/inbox/gala_20260925/afterparty/lanes/t13a.check.txt` section 1.
2. Smoke origin confirmed: `memory/runs/gpipes/p8bc0180ab9.json` (created 2026-08-09T05:13:14Z) lists goals `["research A","research B"]`, task_ids `["t-test","t-test"]`, empty tags, status "running" with both live entries "unknown" and exit_code null. A duplicated test-task placeholder, 48 days stale, zero output. Check section 2.
3. BIND rejected: no code, config, or script references the exact string (check section 4, grep exit 1); candidate rebind targets `memory/runs/gap_swarm_experiment/design.json` + `probes.json` carry 5 named research questions with zero linkage to "research A" (check section 3, grep exit 1). Binding would fabricate intent.

## Actions taken

- Pruned the row from `memory/runs/gap_map/stack.json` (estate data owned by this repo's `mag/gap_map.py`; the ratified board directs the prune), complexity 12.0 -> 10.0, JSON revalidated: 4 items, 10.0. Check sections 7 to 9.
- Kept `memory/runs/gpipes/p8bc0180ab9.json` untouched as provenance (it also backs brief 2, research B).
- Filed resolution artifact: `memory/frontier/help_wanted/resolved/research_A.md` (cites the pipe record, records the prune).
- Board `memory/frontier/HELP_WANTED.md` brief 1 annotated resolved by hand (generator law respected; not regenerated).

## Byte check (finish line)

`memory/runs/gap_map/stack.json` no longer contains the exact string `"research A"`: grep exit 1, `watch/inbox/gala_20260925/afterparty/lanes/t13a.check.txt` section 7.

## Bank

`watch/inbox/gala_20260925/afterparty/lanes/t13a.json`
