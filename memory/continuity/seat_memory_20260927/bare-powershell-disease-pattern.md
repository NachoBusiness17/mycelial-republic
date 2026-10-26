---
name: bare-powershell-disease-pattern
description: Bare powershell argv disease — 13+ sites across mag/ tools/ scripts/ fail Errno 2 under stripped PATH; fixed with shutil.which + System32 fallback pattern; falsifier runs both directions
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

The bare-powershell disease: 13+ call sites across mag/, tools/, and scripts/ call `["powershell", ...]` directly, which fails with `[Errno 2] No such file` whenever the spawning context has a stripped or empty PATH (test runners, daemon threads, scheduled tasks, service contexts). 7,964+ production failure events accumulated in the FKB before the root cause was identified.

**The fix pattern** (from `mag/process_reaper.py:82-90`): `shutil.which("powershell")` first, then `powershell.exe` bare, then the System32 absolute path as final fallback. Receipt comment at each site naming the disease class sig.

**Lanes that landed fixes:**
- B2-85: root writer `tools/shell.py:40-56` (the actual `run_shell`), plus 8 mag/ modules (gpu_ghost, legacy_audit, icon_drop, offerings, platform_kill, loop_breaker, saelis_room, power) — 10 sites total, flows re-run green live (gpu_ghost reads real AMD Radeon RX 5600 XT via amd-cim)
- B2-352: 5 straggler sites in mag/source_trace.py, tools/box_burn_watch.py, scripts/lattice_check.py x2, mag/tts.py (multi-line Popen literal invisible to single-line grep falsifier)
- B2-353: tests/test_shell_powershell_resolution.py pins the resolution — 3 tests, falsifier runs both directions on the real file (revert to bare literal → all 3 fail in under a second)

**Multi-line literal gap**: the B2-352 grep falsifier (`["powershell"` single-line match) missed `mag/tts.py`'s multi-line Popen literal. The broader bare-token grep catches it. Lesson: grep falsifiers need both single-line and multi-line patterns.

**Honesty note**: a planned self-feed brief about a "blind single-hunter check" was refuted by its own probe before filing (both `-Filter` and `Where-Object` forms count the same 15 pythons). The brief was never filed — feeding a refuted claim would have been fabrication.

**Why:** the disease spans three directories and two scopes (mag/ runs as services, scripts/ runs as one-shots), so no single-lane fix catches all sites. The pattern fix must propagate to every caller, and the falsifier must cover both grep shapes.

**How to apply:** when any `[executable, ...]` argv literal appears in production code, immediately apply the which+fallback pattern and add a resolution pin test. The bare literal is a latent production failure waiting for a stripped PATH context.
