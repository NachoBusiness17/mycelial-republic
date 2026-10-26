# THE 50 RELAUNCH — CORRECTED VERDICT (2026-09-25)

**Verdict: 44/44 claimable artifacts verified on disk by absolute-path recount. The in-run verifier's "0 of 45" was a verifier bug, not builder failure.**

- Relaunch run: dwfrun-4c7ad095 (the-50.dwf.ts fired with completed=[]), 45 open tasks (T41 operator-gated, skipped by design).
- Builders: 44 returned ok with artifact paths; 1 honest gate-fail (T39: the operator-voice 9/17 page jpg does not exist in watch/inbox/operator_voice/ — re-runs when the operator delivers it; gate held exactly as written).
- **The in-run verifier claimed 0/44 on disk — WRONG.** It checked the tasks' RELATIVE finish-line paths against its own workspace cwd (the documented stray-path disease, verifier-side this time). Builders wrote correctly to the repo root.
- Corrected recount (this seat, absolute estate paths, byte-size-checked): **44/44 present, zero missing** — every watch/inbox/THE50_* doc, every tools/*.py (scs, duty_fuzz, drift_pairs_stamp, oracle_calibration, verb_anchor), every research pack, prose piece, and the50 run JSONL/JSON.

## Laws re-confirmed the hard way

1. **ABSOLUTE-PATHS applies to verifiers too** — a verifier that resolves claims relative to its own cwd manufactures a 100% failure rate out of thin air. Verifier asks must carry absolute paths or recompute them from the repo root.
2. **Fold-by-script / verify-by-disk beats both self-report AND single-verifier claims** — the correction came from a second, absolute-path recount, not from trusting either the builders or the first verifier.
3. Two verification passes disagreeing = check the checker before mourning the work.

## Still open from the program

- T39 (operator hand: provide the 9/17 page jpg), T41 (operator-gated: Cerebras key).
- Spot-quality review of the 44 artifacts is a next-wave item — this verdict claims EXISTENCE on disk, not quality; the fold's quality tiers apply next.
