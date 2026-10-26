# B2-494 Probe alarms stop at the candidates ledger

## Verdict

LANDED. Chosen path (ONE mouth, per the brief): alarm-class probe results append EXACTLY ONE "[priority][probe-alarm] provider_probe <classes> (run <day>) -> <snapshot ref>" line to memory/attention.md at probe time; a quiet run writes nothing; a failed surface write is best-effort and never breaks the probe (the candidates row still lands). The doctor issue surface stays silent on this path (two alarm mouths is the fan-out disease). Falsifier executed in-suite: a fixture ALARM_RESULT run gains exactly one line naming the lane (provider_probe) and the classes (DOWN, QUOTA-DEAD) with the snapshot ref; the QUIET_RESULT run gains nothing; an OSError-throwing surface leaves the risk row intact. 3 new pins, suite 17 passed.

## Evidence file:line quotes

- mag/improve.py run_provider_probe (post-patch), after append_candidates: "B2-494 (2026-09-26): the alarm surface. Alarm-class probe results no longer stop at the candidates ledger: the run appends EXACTLY ONE [priority] line to memory/attention.md naming the lane, the alarm classes and the snapshot ref. Chosen path: attention.md (the doctor issue surface stays silent here; two alarm mouths is the fan-out disease). A quiet run writes nothing." with `if alarms:` writing "- [priority][probe-alarm] provider_probe %s (run %s) -> %s".
- mag/improve.py new constant: ATTENTION_PATH = ROOT / "memory" / "attention.md" (module constant so tests can inject it, the surface-fixture shape).
- tests/test_improve_provider_probe.py TestAlarmSurfaceB2_494: exactly-one-line assertion naming DOWN + QUOTA-DEAD + the provider_health snapshot ref; quiet-run no-write assertion; OSError best-effort assertion.
- Suite: 17 passed (14 prior pins from B2-106 + 3 new), 0 failed; py_compile OK.

## Work done

1. Read run_provider_probe (B2-106 landing) and the two named surfaces (memory/attention.md, the doctor issue surface); chose attention.md as the single alarm mouth.
2. Wired the surface: one [priority] line per alarm-class run naming lane + classes + snapshot ref; ATTENTION_PATH as an injectable module constant.
3. Added the three pins covering the falsifier plus the failure-isolation arm.
4. py_compile OK; suite 17 passed; real memory/attention.md untouched by tests (injected to tmp).
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Brief's falsifier: "run run_provider_probe with a fixture ALARM_RESULT and the chosen surface must gain exactly one line naming the lane and class within the same run." EXECUTED: TestAlarmSurfaceB2_494.test_alarm_run_gains_exactly_one_priority_line runs the real function with the suite's ALARM_RESULT fixture and asserts exactly one line naming provider_probe + DOWN + QUOTA-DEAD + the snapshot path; the quiet arm and the write-failure arm are pinned alongside. Reproduction: pytest tests/test_improve_provider_probe.py -q (17 passed). Inversion: zero or 2+ lines after an alarm run, a line on a quiet run, or a probe failure caused by the surface write inverts this receipt.

## Bibliography closed

- mag/improve.py (run_provider_probe, ATTENTION_PATH)
- tests/test_improve_provider_probe.py (3 pins; 17 passed)
- memory/attention.md (the chosen operator surface; real bytes untouched by tests)
- watch/inbox/burn_wave_20260926/B2_106_probe_cadence_20260926.md (the cadence this surfaces)
- watch/inbox/burn_wave_20260926/B2_106_cadence_live.json (the ollama DOWN case that motivated the brief)
- Nothing owed.
