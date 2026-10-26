# B2-275 receipt: surface the pin maintenance law in check7 FAIL output (2026-09-26, lane SW-03)

## Verdict

LANDED. The check7 FAIL path now prints the pin maintenance law's four required steps verbatim (re-audit every differing row against qdrops.jsonl bytes; re-derive the pin constants from that audit; name the audit in the landing receipt; never delete or weaken pins to get green, with the B2-259 receipt pointer) as a second line right under the FAIL detail, so the lane that trips check7 sees the law without reading the source. The PASS line is byte-identical (pinned by test against the historical format bytes), and a real green run proves the law text never rides a green output. Spec filed first in the docstring check 7 entry. Mutation test: drilled resurgent row -> FAIL names all steps. 3/3 tests pass.

## Evidence file:line quotes

- scripts/the50_t21_q_caption_ledger_verify.py:495-502 (pre-fix FAIL branch): "print(f\"check7 guard pin (B2-68/B2-220/B2-219/B2-242/B2-243): \" f\"{pin_msg} FAIL \" f\"resurgent={resurgent[:3]} extra={extra} gone={gone}\")" (no law guidance).
- scripts/the50_t21_q_caption_ledger_verify.py:49-61 (the law as a source comment, invisible to the tripping lane): "The law: when a generator lane lands and check7 fails, that lane re-audits every differing row against qdrops.jsonl bytes, re-derives the pin constants from that audit, and names the audit in its landing receipt; never delete or weaken pins to get green."
- QUEUE.md B2-275 row (brief): "the law now lives in the verifier constants block comment but the lane that trips check7 sees only the FAIL line" and the falsifier "a drilled check7 FAIL that prints no law guidance, or any change to the PASS line text".

## Work done

- Spec first: docstring check 7 entry extended with the SPEC (B2-275) paragraph stating the FAIL-print requirement and PASS byte-identity before the code change.
- scripts/the50_t21_q_caption_ledger_verify.py FAIL branch: added the PIN MAINTENANCE LAW required-steps print under the existing FAIL detail line (fix comment names B2-275 and the PASS-identity constraint). Scope note, honestly filed: the brief said "both check7 FAIL prints" but the code has exactly ONE check7 print site whose single FAIL branch covers both failure causes (resurgent rows and keeper mismatch); repo-wide grep found no second check7 print. Both causes now carry the law guidance through that one branch.
- tests/test_pin_law_fail_output.py (new, 3 tests): (1) the brief's mutation test run live: a temp ledger copy with the B2-68 resurgent tuple appended drives rc=1 with a check7 FAIL naming all five law markers; (2) PASS format-string bytes pinned unchanged in source; (3) a real green run against the live ledger: rc=0, RESULT PASS, and NO law text on green.

## Falsifier

The brief's falsifier, now executable both ways: (a) a drilled check7 FAIL that prints no law guidance fails test_drilled_check7_fail_names_law_steps (each of the five markers asserted individually), (b) any change to the PASS line text fails test_pass_line_stays_byte_identical (historical format bytes pinned), (c) law text leaking into green output fails test_green_run_result_line_unchanged_and_real_pass. Residual honesty: the green-run test executes the real verifier each time it runs (measured ~1s, well inside patrol budgets).

## Bibliography closed

- scripts/the50_t21_q_caption_ledger_verify.py (docstring, PIN MAINTENANCE LAW comment block, check7 print block, main)
- watch/inbox/burn_wave_20260926/B2_259_pin_law_20260926.md (the law's owning receipt, named in the FAIL output)
- watch/inbox/burn_wave_20260926/B2_242_quantity_bounds_20260926.md, B2_243_bucket_audit_20260926.md (the precedents cited by the law comment)
- tests/test_pin_law_fail_output.py (new)
- QUEUE.md B2-275 row (brief, self-fed by B2-259 per its renumber note)
