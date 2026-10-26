# B2-438 receipt (2026-09-26)

## Verdict

LANDED. All four runner-driven scripts now refuse repo-external inputs at the entry point: scripts/wave_driver.py validates every writable path argument against the repo root (SystemExit 2, named refusal) before any dispatch; scripts/desk_baseline_probe.py gates both GET helpers on a BASE-host allowlist (127.0.0.1/localhost) so a refused URL never reaches urlopen; scripts/hunger_ledger.py and scripts/m12_pairing.py assert their canonical write paths stay repo-derived before running. 6 fixture pins pass (tests/test_scripts_path_pins.py), each one proving the brief's falsifier shape: an external path or URL produces a named refusal, no write, no request.

## Evidence file:line quotes

- The triage this closes: watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md must-fix set (17 occurrences in 4 files), with the drivers named: configs/coding_session_loop.yaml + mag/coding_session_loop.py (CONFIG_PATH = ROOT / "configs" / "coding_session_loop.yaml") and mag/governor_autorun.py execute desk_baseline_probe.py; mag/lane_runner.py runs scripts/hunger_ledger.py as its canonical fallback (lane_runner ~:699-701 runs watch/cage_bin then scripts/).
- scripts/path_pin.py (new): pin_under_root(path, root, what) joins relative paths under root, refuses anything resolving outside with a named stderr line + SystemExit(2); sole escape MAG_ALLOW_EXTERNAL_PATH=1 (named env, for selftests).
- scripts/wave_driver.py: new module-level validate_path_args(args, root) covering board/steers/key/kb/telemetry/ground/state/lanes_root, called in main() right after argparse before any dispatch; the defaults were already ROOT-derived (lines 78-85), the fix closes the override surface.
- scripts/desk_baseline_probe.py: ALLOWED_HOSTS = {"127.0.0.1", "localhost"} derived beside BASE (:26-28 region); _url_allowed(); both _http_get_json and _http_get_text return "refused: <url> not in desk probe allowlist" BEFORE building a request. The POST sites (:218/:231 before this lane) use the API/DESK_API constants only, which the allowlist covers by construction.
- scripts/hunger_ledger.py main() head: refuses to run if abspath(LEDGER) is not under abspath(REPO) (the LEDGER = WATCH/HUNGER_LEDGER.md derivation is repo-anchored at lines 37-40 and lane_runner executes this script directly).
- scripts/m12_pairing.py main() head: same repo-pin on RUN_DEFAULT (line 51, REPO / "state" / m12_pairing_run.json); the :391-438 writes are selftest-internal tempdir fixtures (no CLI path input exists to pin, named in the receipt).
- tests/test_scripts_path_pins.py: 6 pins, 6 passed. Refusal arm: external board (a sibling directory of the repo) raises SystemExit 2 with nothing written; GET helpers refuse http://evil.example/steal with urlopen patched to explode if called; localhost target still passes the gate with a fake response. Escape arm: MAG_ALLOW_EXTERNAL_PATH=1 lets the same external path through (the named selftest escape). Derivation arms: hunger LEDGER under REPO; m12 RUN_DEFAULT under repo.

## Work done

1. Read the four scripts and their driver call sites; separated real input surfaces (wave_driver CLI overrides, desk probe caller URLs) from already-fixed derivations (hunger/m12 constants), then fixed accordingly.
2. Landed the shared pin helper plus the four integration points.
3. Diagnostic finding while pinning: this box's pytest tmp root is redirected INSIDE the repo (agents/pytest-tmp-*), which is why tmp_path landed "internal" (the pin correctly allowed it) and why the long-running tmp PermissionError flake exists (concurrent lanes sweeping a shared in-repo tmp root). The refusal test therefore uses a true repo sibling; the finding is fed for whichever lane owns the tmp-dir disease.
4. 6 pins pass; wave_driver --selftest still PASS (board write via the pinned path); all 5 touched scripts py_compile clean.

## Falsifier

The brief's falsifier: "a test that passes a repo-external path or URL to any of the four entry points still lands a write or a request after the fix". Each pin IS that test, and all assert the negative: external URL -> refusal string, urlopen never called; external board -> SystemExit 2, no file created; derivation drift -> exit before any write. Re-arm conditions: a new writable CLI flag added to wave_driver without joining validate_path_args, or a new GET/POST helper in desk_baseline_probe bypassing _url_allowed, or a driver setting MAG_ALLOW_EXTERNAL_PATH=1 in production config (that env in a driver process is itself the violation to file).

## Bibliography closed

- scripts/path_pin.py (new); scripts/wave_driver.py (validate_path_args + main call); scripts/desk_baseline_probe.py (ALLOWED_HOSTS + gates); scripts/hunger_ledger.py (main pin); scripts/m12_pairing.py (main pin)
- tests/test_scripts_path_pins.py (new, 6 passed)
- watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md (the must-fix set); configs/coding_session_loop.yaml; mag/coding_session_loop.py:18; mag/governor_autorun.py; mag/lane_runner.py:699-701
- Diagnostic fed: pytest tmp root redirected to agents/pytest-tmp-* inside the repo (PermissionError flake family, B2-288/B2-416 receipts name symptoms)
