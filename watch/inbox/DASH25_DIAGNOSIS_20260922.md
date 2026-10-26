# DASH25 DIAGNOSIS — the wave found a broken execution layer · 2026-09-22

_Named blocker, receipts attached. The 25-wide dashboard wave ran end to end and
its harvest was 2/25 — but the failure is NOT the wave. It is the drainer._

## What happened (receipted)

1. Bridge mechanics ✓: 25 lanes seeded across deepseek/grok/glm/ollama (7/6/6/6),
   watched, re-seeded, tombstoned with reasons, receipts self-sealed. The
   missing-listing bug was found and fixed live (tolerant 30-strike; resume-root
   mode added).
2. The drainer DID pick up and run the lanes: **46 task records exist**
   (memory/runs/orchestrator/tasks, created 04:09–04:54, originals + r2 re-seeds).
3. **44 of 46 failed**: "non-zero exit 1" or "timeout exceeded 602s".
4. Root cause, receipted from a failed task record: the spawned command was
   `['/usr/local/bin/python', '/app/main.py', 'agent', '--query', ...]` —
   **Linux container paths on a Windows host.** Python isn't at /usr/local/bin
   here; /app doesn't exist. Instant exit 1. The timeouts are sessions that hung
   instead of failing fast.
5. The 2 "done" lanes (d01-walk, d25-backups) returned only "exit" as detail —
   thin output; the collector also needs to read task LOG files, not just the
   detail excerpt (improvement queued).

## Why this matters (the wave as instrument)

This was the first WIDE fan-out since the docker purge (−545 GB, disk 91%→49%).
The purge removed the container world the drainer's spawn template was written
for. Narrow single tasks kept working (the historical 374 done entries are
container-era or pre-purge); the first wide test exposed that **the execution
layer still believes it lives in a container.** This is exactly what the wave was
for: a wide test finds what narrow tests miss.

## The morning fix (named, scoped)

1. Locate the drainer's spawn-template (it builds `/usr/local/bin/python
   /app/main.py agent --query …`) and make it host-native:
   `{venv python} {ROOT}/main.py agent --query …` — or restore the container the
   drainer expects. Operator chooses which world the drainer lives in.
2. Collector: read task LOG files for wave findings, not detail excerpts.
3. Re-run dash25 (spec is stable: wave_spec_dashboard25.json) after the fix —
   Mickey-17 round 3, with the template fixed the lanes should land.

## What did land tonight regardless

- athena homecoming proven (byte-exact vs source oid)
- 74.7 GB freed, one manifest, one home
- 50-wide lift invariant + 48/48 smith-chart clean
- light-maze wide walk + the boot_check economy finding
- the Lens Stack salon, fleet mix law, AOS reply sealed

---
_Diagnosis by the ZCode seat, 2026-09-22 ~05:0Z. The wave did its job: it went
looking for work and found the thing that was actually broken._

---
## CORRECTION + FIX LANDED (09-22 ~08:25Z — supersedes "The morning fix" above)

**The container-era-path framing was WRONG.** The drainer lives INSIDE the
container by design — `mag-sovereign` was Up 26h (healthy) all along, and
`/usr/local/bin/python /app/main.py` is the CORRECT in-container template.
"Host-native template" would have been the wrong fix.

**Actual root cause (receipted):** every `main.py agent` boot calls
`build_context_pack()`, whose residual-biography census read all
`memory/biography/residual/*.json` — 3,771 files by this morning — through the
Docker bind mount. Faulthandler SIGABRT receipt: hang at
`mag/context_pack.py:596 in read_text` (old line numbering). Same 3,771 files
read on host NTFS: **1.02s, zero errors** → the files are fine, the MOUNT is
degraded (post-rebuild Docker Desktop). 300s/602s timeouts = boot never
finishing. This is what killed dash25's 44/46 AND the janitor's morning loop
AND the drainer's respawn churn all day (respawned 10× between 05:56–07:50Z).

**Fix landed (mag/context_pack.py):** residual census now cached hourly to
`memory/working/residual_census.json` (`_residual_census()`); agent boot pays
one small cached read instead of 3,771. Counting logic byte-identical.
Host verify: full `build_context_pack(fast=False)` in 3.83s, cache written.
**Also landed:** `mag/orchestrator.py` stamps `provider` top-level at task save
(the mix-law hygiene debt); `_provider_running_count` reads the field first.

**Live status at fix time:** mag-sovereign + mag-worker Exited 137 (SIGKILL
after ignored SIGTERM — wedged on the very hang fixed here), mag-redis Exited 0,
dependency-ordered, ~12:05Z — an explicit `compose stop` shape, `restart:
unless-stopped` keeping them down. NOT restarted from this seat (deliberate-stop
evidence; restart = operator word: `docker compose up -d`). fullsend_s2
(MiMo free lane, port 4096) was re-running the dash25 prompts host-side and is
unaffected by the container stack.

**Still owed:** the mount itself is slow — moves like estate-in-volume or
Docker Desktop file-sharing settings are operator-architecture calls.

### RECONCILIATION (09-22 ~08:45Z — reads with the fresh-boot arc, not against it)

The ~12:05Z stop above was the FRESH-BOOT FIX (sess_fc9e89e3): the "purged"
containers had never actually stopped — they held ports 8000/8765/9000, answered
boot health checks, and spawned the failing tasks as ghosts of the old world.
`docker stop` (reversible, not removed) + Windows stack started (backend :8000,
dashboard :8765, fresh host drainer). So "host-native" was the DELIBERATE and
correct direction; this card's earlier "host-native would be wrong" line is
withdrawn. What this card's forensics ADD: the faulthandler receipt that
container spawns were ALSO hanging on the residual census through the bind mount
(1.02s NTFS vs 300s+ mount) — the why-they-timed-out under the ghost story. The
hourly census cache helps both worlds: container (mount bomb removed) and host
(per-boot 3,771-parse tax removed, growing daily). Docker stack remains stopped
by design of the fresh-boot fix; the census cache fix is live on the host stack
immediately (host drainer boots pay one cached read).
