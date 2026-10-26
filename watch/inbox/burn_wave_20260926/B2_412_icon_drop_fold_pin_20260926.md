# B2-412 Port the B2-378 fold-outcome arms into a repo pin

## Verdict

LANDED. tests/test_icon_drop_fold.py pins all four fold-outcome arms (dropped->ok, failed->failed, skipped_no_powershell->skipped_no_powershell, statusless->unknown) in the throwaway probe's exact sandbox pattern (tmp_path + monkeypatch on icon_drop.LEDGER, icon_drop.desktop_folder, skill_ledger.DECISIONS_PATH, training_events.EVENTS_PATH). The brief's falsifier executed live: injecting the hardcoded outcome="ok" regression into _fold_training turns the module red on exactly the three non-dropped arms (3 failed, 1 passed), restoring the pass-through returns it green (4 passed). The icon_drop outcome pass-through is no longer pinned only by a throwaway probe. Suite: 4 passed; mag/icon_drop.py restored byte-exact after the injection (working-tree diff vs HEAD is the pre-existing uncommitted B2-378 landing, not this lane's bytes).

## Evidence file:line quotes

- mag/icon_drop.py _fold_training (current bytes): `outcome="ok" if status == "dropped" else status,` with the B2-378 cause comment naming the ok_rate counting law.
- tests/test_icon_drop_fold.py: the four arm tests + the sandbox fixture (monkeypatch on the four module write-path constants) with the module docstring naming the port and the falsifier.
- Falsifier run: injection `outcome="ok",  # B2-412 FALSIFIER INJECTION: hardcoded regression` -> `3 failed, 1 passed` (failed/skipped_no_powershell/statusless arms red, dropped arm green); restore -> `4 passed`; restore verified by the grep count of the pass-through line = 1 and the absence of the injection marker.

## Work done

1. Read mag/icon_drop.py _fold_training and the B2-378 probe's sandbox pattern.
2. Wrote tests/test_icon_drop_fold.py: sandbox fixture on the four write paths, four arm tests reading the real decisions/events jsonl rows.
3. Executed the brief's falsifier both ways (inject regression -> red on 3 non-dropped arms; restore -> green 4 passed).
4. py_compile untouched (test-only module); real ledgers untouched (all writes sandboxed; the fixture's tmp paths hold the only rows).
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Brief's falsifier: "revert _fold_training's outcome to a hardcoded 'ok' and the new module goes red on the three non-dropped arms." EXECUTED: 3 failed / 1 passed under injection, 4 passed restored. Reproduction: swap the pass-through line for outcome="ok", run pytest tests/test_icon_drop_fold.py, observe exactly test_failed_row_folds_outcome_failed, test_skipped_row_folds_verbatim_status and test_statusless_row_folds_unknown red while test_dropped_row_folds_outcome_ok stays green. A future signature change to record_decision or _fold_training that breaks an arm also goes red (the pins read real rows, not mocks of the writer).

## Bibliography closed

- mag/icon_drop.py (_fold_training; byte-restored after the injection)
- tests/test_icon_drop_fold.py (new, 4 pins)
- watch/inbox/burn_wave_20260926/B2_378_falsifier_probe.py + B2_378_fold_outcome_20260926.md (the probe this ports; the sandbox pattern source)
- mag/skill_ledger.py (DECISIONS_PATH), mag/training_events.py (EVENTS_PATH)
- Nothing owed.
