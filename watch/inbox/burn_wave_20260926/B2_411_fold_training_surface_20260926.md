# B2-411 _fold_training failure surface, 2026-09-26

## Verdict

LANDED. The bare `except Exception: pass` around the whole _fold_training body is gone. The fold now returns a bounded fold_status dict {ok: True, outcome} on success or {ok: False, error} on failure, all three caller sites stamp it onto the caller-visible row as "fold_status", and a failure additionally logs one WARNING line to stderr naming the missing case-law edge and the icon. It never raises, exactly per the brief's constraint (the drop path cannot break because the case-law fold is broken). The brief's falsifier is dead on sandboxed bytes: forcing record_decision to raise (RuntimeError "simulated skill_ledger append failure") now surfaces as fold_status {ok: False, error: "RuntimeError: simulated skill_ledger append failure (B2-411 probe)"} on the row plus the stderr WARNING, while the happy path returns {ok: True, outcome: "ok"}. The operator_behavior fold undercount is now visible at the caller instead of silent.

## Evidence file:line quotes

- mag/icon_drop.py _fold_training (post-edit) docstring: "B2-411 2026-09-26: the fold failure is no longer silent. The whole fold body used to sit behind a bare `except Exception: pass`, so a broken fold (skill_ledger append error, training_events schema drift, import failure) left the drop landed but the case-law edge missing with no signal anywhere. Returns a bounded fold_status dict {ok, outcome?, error?} ... Never raises ...".
- Failure arm (same file): `except Exception as exc: surface = {"ok": False, "error": f"{type(exc).__name__}: {exc}"[:200]}; print(f"WARNING: [icon_drop] fold_training failed, case-law edge missing for {row.get('name')}: {surface['error']}", file=sys.stderr); return surface`.
- Caller sites (all three stamped): :170, :213, :262 `row["fold_status"] = _fold_training(row)  # B2-411: named fold failure surface` — note the ledger row is appended BEFORE the fold runs, so the surfaces live on the caller-visible row (the brief's allowed option), not the pre-fold ledger line.
- Probe transcript (this lane, sinks monkeypatched): "WARNING: [icon_drop] fold_training failed, case-law edge missing for probe-icon: RuntimeError: simulated skill_ledger append failure (B2-411 probe)"; "fold_status: {'ok': False, 'error': 'RuntimeError: simulated skill_ledger append failure (B2-411 probe)'}"; happy "fold_status: {'ok': True, 'outcome': 'ok'}"; "PROBE PASS".
- Pre-edit defect (HEAD region): the try body ended `except Exception: pass` with the function returning None.

## Work done

- Claim law: CLAIM SW-00 mag/icon_drop.py filed before editing (working-tree-modified); retired at landing; bytes re-read at claim time.
- Read _fold_training and all three callers (drop path, skipped_no_powershell path, failed path).
- Implemented the fold_status return with the dated law docstring; stamped all three caller sites; stderr WARNING on the failure arm only.
- Sandbox probe with forced failure and happy arms; py_compile clean; em-dash 0 in my added lines (the single diff em-dash is B2-414's pre-existing comment from another lane's block).
- Filed this receipt, the LEDGER row, and the QUEUE row flip.

## Falsifier

- Force record_decision (or the emit) to raise inside a sandboxed fold: if no surface anywhere names the missing edge, the brief's falsifier fires — the probe above reruns in seconds and currently passes.
- A raised error from _fold_training breaking a real drop path kills the landing (the never-raises constraint is structural: the whole body stays inside one try).
- If a consumer matches on the row dict shape and chokes on the new fold_status key, that is a visible integration break to fix, not a reason to remove the surface.
- The undercount repair is observable: operator_behavior ok_rate from skill_ledger still counts only successfully folded rows; a run whose fold_status ok=False count is nonzero proves the silent-undercount window this lane closed was real.

## Bibliography closed

mag/icon_drop.py (_fold_training pre/post-edit; three caller sites); watch/inbox/burn_wave_20260926/B2_378_fold_outcome_20260926.md (the fold outcome law this extends); B2_378_falsifier_probe.py (named in the docstring). No web sources. Em-dash count 0 in this receipt and my added lines.
