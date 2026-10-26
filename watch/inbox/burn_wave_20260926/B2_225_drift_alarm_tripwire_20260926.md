# B2-225 Streak and staleness tripwire, 2026-09-26

## Verdict

LANDED. tools/drift_dashboard.py now has `--alarm` (spec docs/DRIFT_BOARD_SPEC.md section 4b, filed before the code): it recomputes the drift table and fires when a DRIFTING streak crosses 14 days or a live referent age crosses 30 days, writing ONE dated inbox row watch/inbox/DRIFT_ALARM_<YYYY-MM-DD>.md naming every breaching pair and exiting 2; quiet exits 0 and writes nothing. Live run this lane: "alarm: quiet (no streak >= 14d, no referent >= 30d)", exit 0, no file. Quiet is honest, not the disease persisting: the motivating T4 case (referent 51d stale, gates.jsonl ended 2026-08-06) was cured by the B2-65 revival and today's stamping, live rows read this lane show T1/T3 streaks 7d, T4/T5 referent age 0d (newest 2026-09-26), T2 age 8d, nothing over threshold. The breach path is proven on a synthetic row (streak 17d + referent 51d fires; n/a referent never fires), so the tripwire is armed for the next decay while the current tree is clean.

## Evidence file:line quotes

- docs/DRIFT_BOARD_SPEC.md section 4b (post-edit): "`--alarm` reuses the same table computation and fires when either threshold is crossed ... DRIFTING streak at or above 14 days ... live referent age at or above 30 days ... On any breach it writes ONE dated inbox row, `watch/inbox/DRIFT_ALARM_<YYYY-MM-DD>.md` (same-day rerun overwrites, never duplicate-spam) ... and exits 2 ... Quiet exits 0 and writes nothing. The alarm row is a proposal surface only: model text proposes, the switchboard/effect broker authorizes effects".
- tools/drift_dashboard.py (post-edit): alarm_breaches `if streak >= 14 or (age is not None and age >= 30)`; _ref_age_days docstring "parse \"51d\" -> 51; n/a or unparseable never fires"; run_alarm writes `ROOT / "watch" / "inbox" / f"DRIFT_ALARM_{today.isoformat()}.md"` and returns 2 on breach, 0 quiet; main dispatch `if "--alarm" in argv: return run_alarm(rows, today, generated_at)` placed before the --check and build arms so the alarm never writes the panel.
- Live run (2026-09-26 20:1xZ): stdout "alarm: quiet (no streak >= 14d, no referent >= 30d)", exit 0, `ls watch/inbox/DRIFT_ALARM_*.md` finds nothing.
- Live table read this lane: "T1 DRIFTING streak 7 age 0d newest 2026-09-26 / T2 ALIGNED streak 0 age 8d newest 2026-09-18 / T3 DRIFTING streak 7 age 0d / T4 DRIFTING streak 0 age 0d / T5 DRIFTING streak 0 age 0d / T6 ALIGNED streak 0 age 0d".
- Synthetic proof (in-process, no inbox write): alarm_breaches(rows + fake streak 17d ref 51d) = ["T-FAKE"]; alarm_breaches([n/a referent row]) = [].
- B2-31 pointer receipt (watch/inbox/burn_wave_20260926/B2_31_poll_tripwire_20260926.md): its tripwire pattern (spec section filed before code, advisory channel, no new noise on the cured tree) is the shape this lane followed.

## Work done

- Read tools/drift_dashboard.py whole (drifting_days, referent_age, build_table, main) and docs/DRIFT_BOARD_SPEC.md whole; read the B2-31 receipt for the house tripwire pattern.
- Claim law: CLAIM SW-00 lines filed for both untracked shared files (tools/drift_dashboard.py, docs/DRIFT_BOARD_SPEC.md) before editing; both retired at landing.
- Spec first: added section 4b to the owning spec (thresholds, one dated row, overwrite-not-append, exit codes, proposal-surface law) before the code, same lane.
- Code: _ref_age_days (guarded parse, n/a never fires), alarm_breaches (streak >= 14 or age >= 30), run_alarm (breach rows to the dated inbox file + stdout, exit 2; quiet no-write, exit 0), --alarm dispatch in main before --check/build. Docstring usage updated.
- Ran live (quiet, exit 0, no file) and proved the breach arm on synthetic rows in-process; py_compile clean; em-dash 0 in added lines, the spec, generated output text, and this receipt.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- A pair whose streak crosses 14d or referent crosses 30d that --alarm leaves quiet kills the tripwire (rerun --alarm the day any table row shows >= threshold).
- An alarm run that mutates the ledger or the panel, or appends duplicate same-day rows, violates section 4b and voids this landing.
- A referent age string that stops ending in "d" would parse to None and never fire; if referent_age's format ever changes, _ref_age_days must change with it or the 30d arm dies silently.
- If the quiet verdict were hiding breaches, the live table read above would be lying; the per-pair numbers are quoted for recheck.

## Bibliography closed

tools/drift_dashboard.py (whole pre-edit, post-edit alarm block); docs/DRIFT_BOARD_SPEC.md (sections 3, 4, 4b, 5); watch/inbox/burn_wave_20260926/B2_31_poll_tripwire_20260926.md (whole); memory/runs/adv_arc_50/teleo_drift_stamps.jsonl via the tool's own loader (live rows quoted). No web sources. Em-dash count 0.
