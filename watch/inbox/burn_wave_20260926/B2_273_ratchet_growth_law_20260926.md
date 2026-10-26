# B2-273 Ratchet line-free claim absorbs silent growth

## Verdict

LANDED. Law decided: REFRESH-SIZE-OVER-EXPIRY. baseline-update stamps the accepted size (accepted_lines) into every file-too-long claim, and check prints a visible GROWTH line whenever a scanned accepted claim now measures more lines than at acceptance ("GROWTH claim <fp>: <file> accepted at N lines, now M (+K) — re-audit or re-accept by name"). Growth stays non-blocking (the ratchet's accept semantics unchanged, never loosened) but is never again a silent ledger fact. The expiry arm was rejected: expired_fps already covers time-decay, and expiry would churn live exceptions on the bridge cadence without naming the growth. The brief's falsifier experiment ran live and inverted: accept at 427, absorb 50 no-op lines to 477, line-free fingerprint unchanged, check --changed shape prints NEW=0 PASS AND the GROWTH line naming 427-to-477 (+50) — the exact 427-to-453 disease with a surface recording it. Pins: 3 new in tests/test_violation_ratchet.py (stamping, grown-past visibility, no-noise-at-accepted-size); suite 7 passed.

## Evidence file:line quotes

- tools/violation_ratchet.py:75-76 (the line-free fingerprint the brief names): `fingerprint(rule, file, detail) = sha256(f"{rule}\0{file}\0{detail}")[:16]` with detail `f">{FILE_LINE_CAP} lines"` (:136) - no line data in the register.
- tools/violation_ratchet.py (post-patch) module docstring, growth-law paragraph: "Law chosen: baseline-update stamps the accepted size (accepted_lines) into the claim, and check prints a GROWTH line whenever a scanned accepted file-too-long claim now measures more lines than it was accepted at."
- cmd_baseline_update (post-patch): `entry["accepted_lines"] = v["line"]` stamped for file-too-long claims (violations_in already carries the live count at :136, so no extra IO).
- cmd_check (post-patch): the GROWTH surface loop over accepted file-too-long hits comparing v["line"] to accepted_lines.
- Live experiment output: `claim stamped accepted_lines: 427` / `RATCHET check: ... hits=1; registered=1; NEW=0; expired-exceptions=0` / `GROWTH claim 0d0ef617a2c5b77e: mag/big.py accepted at 427 lines, now 477 (+50) — re-audit or re-accept by name` / `RATCHET: PASS — no unregistered debt.`
- tests/test_violation_ratchet.py: 3 new pins; suite 7 passed, 0 failed.

## Work done

1. Read the ratchet (fingerprint, violations_in, cmd_check, cmd_baseline_update, cmd_prune, expired_fps) and the B2-248 receipt context (claim 8d41e611f98d3fa5 accepted at 427, measured 453 at split, pruned on the split).
2. Decided the law (refresh-size; expiry rejected with reasons above) and specified it in the module docstring per the spec-before-behavior rule.
3. Implemented: accepted_lines stamp at acceptance; GROWTH surface in check for scanned accepted file-too-long claims.
4. Ran the brief's falsifier experiment in a sandbox (tmp estate + baseline; hermetic): 427 accept, +50 no-op growth, NEW=0 PASS with the GROWTH line - the pre-patch code had no surface (code-read: old cmd_check printed only NEW and EXPIRED lines), the post-patch code records it.
5. Added the 3 pins; suite 7 passed; py_compile OK; zero em-dashes on added lines.

## Falsifier

Brief's falsifier (the experiment): accept a file-too-long claim, grow 50+ no-op lines, rerun check and observe NEW=0 PASS with NO surface recording the growth. EXECUTED: pre-patch that observation was true by code reading (no growth print existed); post-patch the same experiment shows the surface (GROWTH line), so the defect the falsifier demonstrated is now impossible to reproduce silently. Reproduction: the sandbox experiment (accept 427, grow to 477, check) must print the GROWTH line while exiting 0; `pytest tests/test_violation_ratchet.py -q` must stay 7 passed. Inversion: a growth past accepted_lines that prints no GROWTH line, or a GROWTH line that fails the check (exit != 0 on growth alone), inverts this receipt.

## Bibliography closed

- tools/violation_ratchet.py (patched: docstring law, accepted_lines stamp, GROWTH surface)
- tests/test_violation_ratchet.py (3 pins; 7 passed)
- configs/violation_baseline.json (register the law now stamps; no live entries modified by this lane)
- watch/inbox/burn_wave_20260926/B2_248_module_split_20260926.md (the 427-to-453 observation this law closes)
- Nothing owed.
