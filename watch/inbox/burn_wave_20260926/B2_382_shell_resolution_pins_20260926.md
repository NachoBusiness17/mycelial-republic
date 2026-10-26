# B2-382 receipt (2026-09-26)

## Verdict

LANDED. The B2-85 mag-side resolutions are now pytest-pinned: tests/test_b285_enum_resolution_pins.py holds 4 pins (3 forced-ImportError branches + 1 clean-path site), all passing, each asserting the System32 arm is taken (argv[0] is the absolute path, not a bare literal) and the canned process row parses clean (zero error rows). The brief's falsifier is closed: reverting any branch to the bare ["powershell"] literal now fails its pin on argv[0].

## Evidence file:line quotes

- The pinned branches (read at land time): mag/legacy_audit.py _enum_procs (160-199; fallback at 181: `ps_exe = shutil.which("powershell") or shutil.which("powershell.exe")` then the `if not ps_exe and sys.platform == "win32": ps_exe = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"` arm); mag/platform_kill.py _enum_host_pids (49-88, same shape at 65); mag/loop_breaker.py _enum (68+, same shape at 99). Flow-probe-only verification was the gap: B2_85_flow_probe all_ok 10/10, no pytest on these branches, and B2-376's pin self-feed scoped only its four straggler sites (tools/shell.py et al, tests/test_shell_powershell_resolution.py).
- tests/test_b285_enum_resolution_pins.py (4 pins, 4 passed): sys.modules["psutil"]=None forces the ImportError branch; shutil.which monkeypatched to None so the System32 arm is the only answer; subprocess.run spied (the modules import subprocess locally, so the patch lands on the shared stdlib module; monkeypatch restores), argv recorded, stdout canned; asserts calls == 1, calls[0][0] == the absolute System32 path, "-NoProfile" present, and the canned row parsed (out[0].pid == 4242, no error keys).
- Clean-path pin: mag/legacy_audit._enum_procs with psutil importable records ZERO subprocess spawns and returns a list, so a refactor that starts spawning on the clean path also fails.
- Two of my own first-cut defects caught by the pins before landing (class-scope closure bug in the spy; canned CommandLine not matching platform_kill's MAG_CMD_MARKERS / loop_breaker's _MAG filters, which had silently filtered my row to []), fixed in the test, module bytes untouched.

## Work done

1. Read all three branches plus the B2-353 pattern test; confirmed no existing pytest touched them.
2. Landed the pin file with the marker-aligned canned outputs and deterministic spy (no real PowerShell spawn; the resolution LOGIC is what is pinned).
3. 4 passed; ratchet not re-run for this file (tests/ outside scan roots, consistent with earlier lanes).

## Falsifier

The brief's falsifier: "revert mag/legacy_audit.py:181 to the bare ['powershell'] literal and no test fails today". Now: revert it and test_legacy_audit_enum_procs_takes_system32_arm fails (argv[0] == "powershell", not the System32 absolute); same for the platform_kill and loop_breaker branches. The clean-path pin fails any refactor that spawns from the psutil branch. Standing limit, named: the pins assert the resolution + argv shape and the parse of canned output, not a live Get-CimInstance return shape (that is the flow probe's job, unchanged).

## Bibliography closed

- mag/legacy_audit.py, mag/platform_kill.py, mag/loop_breaker.py (branches read, UNMODIFIED: pins only, per the brief)
- tests/test_b285_enum_resolution_pins.py (new, 4 pins); tests/test_shell_powershell_resolution.py (pattern source)
- watch/inbox/burn_wave_20260926/B2_85_powershell_fix_20260926.md; B2_353_shell_pin_20260926.md
- Board event: the B2-382 queue row was removed from QUEUE.md by the ~21:02Z compaction/restore while this work was in flight (the row carried [x] with no receipt; the repair pass dropped checked rows); landing note filed on the board instead of a flip; durable pointer lives in memory/burns/LEDGER.jsonl and this receipt.
