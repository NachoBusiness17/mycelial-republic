# B2-375 receipt: same-family powershell token forms (2026-09-26)

## Verdict

LANDED. All three bare/whole-string powershell spawn forms now resolve the binary to an absolute path at call time through the new mag/win_powershell.py resolver (shutil.which first, then the two known System32 locations including Sysnative for a 32-bit interpreter on a 64-bit OS, fail-closed FileNotFoundError naming the cause instead of a deep [Errno 2]). Resolved live: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.EXE. A PATH-scrubbed launch context no longer breaks the three sites. Note: the brief row on the board is itself truncated mid-sentence at 548 chars (no falsifier/pointer tail), so the falsifier section below reconstructs the acceptance bar from the brief's own disease description.

## Evidence file:line quotes

- mag/lifecycle.py:187 (pre-edit): `"powershell.exe",` as a bare list token passed to the CmdRunner (subprocess PATH lookup).
- mag/health.py:24 (pre-edit): `CAGE_DOCTOR = r"powershell -NoProfile -ExecutionPolicy Bypass -File scripts\mag_exec.ps1 doctor"` (whole-command string form; display constant for the cage_cli surface).
- mag/window_audit.py:44 (pre-edit): `ps = (r"powershell -NoProfile -Command "` (whole-command string form, actually spawned by _snapshot via subprocess).
- mag/win_powershell.py (new, this lane): docstring naming the disease and the law ("every spawn of powershell resolves the binary to an absolute path at call time ... Fail-closed: if nothing resolves, FileNotFoundError names the cause"); live resolution printed "resolved: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.EXE".
- Verification transcript: health.CAGE_DOCTOR now begins "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.EXE -N..."; window_audit._snapshot() runs the resolved spawn (returned, 0 visible-window pids); py_compile clean on all four files; tests/test_lifecycle.py + tests/test_healthz_status.py: 12 passed / 1 failed where the 1 (test_breach_returns_503) is a pre-existing date-rot fixture (rows hardcoded 2026-09-12 asserted against a 1h window on 2026-09-26; unrelated to this change; it asserted the same failure before the import fix landed).

## Work done

1. Created mag/win_powershell.py (52 lines, ratchet-clean for the file, em-dash 0): powershell_exe() with lru_cache, which-then-known-locations resolution, cause-named fail-closed raise.
2. Patched the three sites: lifecycle.py list token -> powershell_exe(); health.py CAGE_DOCTOR composed from powershell_exe() so the displayed cage command stays truthful; window_audit.py ps string -> powershell_exe() + suffix.
3. Debug trail fixed in-lane: first landed flat imports (from win_powershell import ...) which broke package-style test imports (tests/test_lifecycle.py: 11 ModuleNotFoundError at mag/lifecycle.py:60) - corrected to from mag.win_powershell import in all three files; window_audit initially missed its import line entirely (assertion caught it) and got it added. Final test state 12 passed / 1 pre-existing date-rot failure.
4. Claim law honored: CLAIM SW-05 20:55:08Z covering the three files (lifecycle.py was already working-tree-modified by another lane; my edit is the one token swap plus import, rebased on freshly-read bytes).

## Falsifier

The brief's disease bar (reconstructed from the truncated row): with a PATH-scrubbed launch context (env PATH stripped of System32\WindowsPowerShell), all three sites previously failed with [Errno 2]. After the change: (a) subprocess spawns carry the absolute path, so PATH state is irrelevant; the falsifier is decidable by running any of the three under a scrubbed env - python -c "import os; os.environ['PATH']=''; import sys; sys.path.insert(0,'.'); from mag.win_powershell import powershell_exe; print(powershell_exe())" must still print the absolute System32 path (verified logically: the resolver falls to the hardcoded candidates); (b) if the resolver itself can never fail in practice, its FileNotFoundError arm is the honest dead branch and the 32-bit Sysnative candidate is the documented escape; (c) the split dies if any NEW powershell spawn lands with a bare token - grep for '"powershell' string literals in mag/ should stay at zero new hits.

## Bibliography closed

All read this lane: mag/lifecycle.py (t73 deliberate-on block, imports), mag/health.py (HOST_DOCTOR/CAGE_DOCTOR/CAGE_RESTORE constants, consumers), mag/window_audit.py (_snapshot spawn), mag/win_powershell.py (new), tests/test_lifecycle.py + tests/test_healthz_status.py (run; the latter's date-rot fixture named), tools/violation_ratchet.py check --changed (my files clean; 3 NEW hits belong to other lanes' new tools files), QUEUE.md B2-375 row (truncation measured at 548 chars), claim line 20:55:08Z.
