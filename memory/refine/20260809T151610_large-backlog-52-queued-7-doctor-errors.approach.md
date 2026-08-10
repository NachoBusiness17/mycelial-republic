# Frontier Approach — large backlog 52 queued; 7 doctor errors; FKB heat run_shell:c73866f2f1b5 x68

**ts:** 2026-08-09T15:16:10.992389+00:00
**transport:** grok-3 / deep
**path:** inline

---

**Coding Approach**

**Files**  
- `core/queue.py`  
- `doctor/sanity.py`  
- `exec/run_shell.py` + `exec/run_python.py`  
- `fkb/heat.py`  
- `tasks/chain.py`

**Functions**  
- `queue.drain_backlog(max=20, priority="chain")`  
- `sanity.fix_chain_discipline()` (targets 5 issues)  
- `sanity.check_provider_inbox()`  
- `fkb.suppress(sig, threshold=50)` + `fkb.record()`  
- `exec.safe_run(cmd, retries=1, circuit=True)`  
- `chain.enforce_order(task_id, prev_id)`

**Invariants**  
- `queued <= 20` after drain  
- `chain_discipline.issues == 0`  
- `run_shell:c73866f2f1b5.count < 10` post-fix  
- `provider_sanity.ok && inbox_sanity.ok`

**Order of operations**  
1. `fkb.suppress` on top-2 sigs (immediate heat cut).  
2. `sanity.fix_chain_discipline()` + `check_provider_inbox()`.  
3. `queue.drain_backlog()` (process 32 tasks, skip heat sigs).  
4. Wrap `run_shell`/`run_python` with `safe_run`.  
5. Re-run doctor probe; assert `errors==0`.

**SUMMARY**  
Target repeated FKB heat + chain/inbox failures + backlog via suppression, targeted sanity repair, bounded drain, and guarded exec.

**DELIVERABLE**  
Patch set: 5 files, 7 functions, 4 invariants. Ready for deepseek-v4-flash execution.
