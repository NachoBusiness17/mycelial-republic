# STEAL — Runaway Python → Source (process-tree source attribution)

**Source lesson (2026-08-10):** ghost sensed a window-storm existed but was blind to WHERE
it came from — it counted processes but never reported the SOURCE. The operator's words:
"ghost sense runaway python to source" + "look at the hundred plus python windows."

**Steal target (external contracts):**
- **supervisord** — attributes each child to its source by an INHERITED env marker
  (`SUPERVISOR_PROCESS_NAME` / `SUPERVISOR_GROUP_NAME`), not by ppid-guessing. Restart
  policy `startretries` + backoff → `FATAL` (already stolen as crashLoopBackOff).
- **systemd** — the unit cgroup IS the source attribution; killing the unit kills the tree.
- **pm2** — named slots + `pm2 list` shows the source script; kill the whole tree.

**Adapted mechanism (deterministic, $0, works without psutil):**
1. Every framework spawner stamps children with `MAG_SLOT` / `MAG_SOURCE` env
   (supervisord-marker analog) — `mag_launch._spawn`, `mag/headless.py`.
2. `mag/source_trace.py`:
   - `sense()` — duplicate singleton slots / one-parent cascade / multi-boot detection,
     with verdict `clean | multi_boot | runaway`.
   - `trace_source(pid)` — walk ppid ancestry (CIM `ParentProcessId`, reliable when psutil
     is absent) up to the ROOT spawner.
   - `break_source(root)` — taskkill `/T` on the source (systemd kill-unit analog), dry by default.
   - `_enum()` — psutil preferred, else the fixed single-quoted CIM `Where-Object` fallback
     (the old nested-quote `-Filter "Name='python.exe'..."` form was PowerShell-mangled →
     silently 0 procs → ghost blind).
3. Wired: ghost.cycle adds `source_trace` to the trail + failure_kb; loop_breaker.break_loop
   reports the source chain.

**Live verification (2026-08-10):** `verdict: runaway`, 20 python procs, 5 distinct boot
roots; duplicates (scribe/lab/mirror/ghost slots) traced to `power start --browser` pid 16316
→ `mag_launch` → ghost daemon (duplicate autorun_loop) + a 2nd windowed boot stacking the same
slots. This is the "hundred plus python windows" source: repeated boots, each windowed at the top.

**Lesson:** a process-governance layer must report the SOURCE, not just the count. Attribution
by inherited marker + ancestry-walk-to-root beats 1-level ppid guessing and beats a global
process-count threshold.
