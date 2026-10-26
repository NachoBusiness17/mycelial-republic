# AG8 — violation ratchet triage (audit finding #15)

Date: 2026-09-30 · Agent: AG8-audit-20260930 · Instrument: `tools/violation_ratchet.py` (full scan, no `--changed`)

## Byte truth vs the finding

Finding #15 said "900 hits / 887 registered / 13 NEW (10 file-too-long, 3 except-pass) + 5 GROWTH".
The first full-scan run measured **903 hits / 887 registered / 16 NEW (13 file-too-long + 3 except-pass) + 5 GROWTH**.
The finding undercounted NEW by 3 (and mis-split 10/3 vs the byte truth 13/3). Triaged against the bytes, not the report.

## FIXED (1) — genuine silent-swallow

- `mag/corpus_acquire.py:376` (was `except Exception: pass`): swallowed a corrupt/unreadable
  `ACQUISITION.json` receipt pointer and silently degraded `--resume` to the older checkpoint.
  A corrupt receipt pointer is a receipt-integrity defect — the exact disease the round-2d
  measured-defect comment in the same function exists to prevent. Replaced with
  `except (OSError, ValueError) as e:` + a one-line warning naming the error and the fallback.
  Behavior identical (fallback preserved); only visibility changed, mirroring the
  "resume read failed" log two blocks down. Fix comment carries the cause per build discipline.

## REGISTERED by name (15) — legitimate catches + too-long files

`baseline-update --by AG8-audit-20260930` swept 15 claims (register 945 → 960):

- 2 except-pass, judged legitimate documented catches (not wrong to keep broad):
  - `mag/skills_pack.py:117` — `except OSError: pass` in `_fire`; docstring is the law:
    telemetry-only ledger write must never break pack building. Named exception, documented.
  - `tools/seat_law_gate.py:64` — `except Exception: pass` on `tmp.unlink()` in a `finally`
    after the gate verdict is already returned; leftover temp file is harmless. Rewriting to
    `contextlib.suppress` would only hide it from the ledger, not improve it.
- 13 file-too-long: mag/corpus_acquire.py (638), mag/estate_bridge.py (442),
  mag/gwap_payload.py (865), mag/percolator.py (580), mag/physical_compute_acquire.py (630),
  mag/token_chain.py (413), mag/worldgen.py (841), tools/concept_predictor.py (513),
  tools/duel_harness.py (461), tools/env_contract.py (563), tools/gate_canary.py (401),
  tools/k8s_water_sim.py (423), tools/regen_front_door.py (433).
  Splitting any of these is a refactor, not a triage (mission law).

## RE-ACCEPTED by name (5) — GROWTH claims

`baseline-update` never refreshes `accepted_lines` on already-registered fingerprints, so the
B2-273 cure ("named re-acceptance or split") was applied through the tool's own sanctioned
writer (`load_baseline`/`save_baseline`), stamping `reaccepted`/`reaccepted_by`/`reaccepted_from`
so the original acceptance provenance survives:

- `mag/corpus_selfsteal.py` 550 → 573 (+23)
- `mag/shared_surface.py` 426 → 447 (+21)
- `tools/census_drift_patrol.py` 403 → 462 (+59)
- `tools/secret_gate_scan.py` 409 → 415 (+6)
- `tools/stealth_driver.py` 753 → 1472 (+719) — the big one; a split is a refactor for a
  later window, not this triage.

## Verification

- Re-run full check: `hits=902; registered=902; NEW=0; expired-exceptions=0` —
  **RATCHET: PASS — no unregistered debt.** (hits 903 → 902 = the fixed except-pass gone;
  GROWTH lines cleared by the re-acceptance stamps.)
- `pytest tests/test_corpus_acquire.py tests/test_violation_ratchet.py -q` → **11 passed**.

## Files owned by this triage

- `mag/corpus_acquire.py` (the fix)
- `configs/violation_baseline.json` (register: +15 claims, 5 re-acceptance stamps)
