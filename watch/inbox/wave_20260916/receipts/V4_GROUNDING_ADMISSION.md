# V4_GROUNDING_ADMISSION — grounding_wave v4 evidence-admission boundary

- Date: 2026-09-16
- Wave: wave_20260916, seat: implementer (Codex packet "most useful next synthesis")
- Design source: `A2_EPISTEMOLOGY_ENGINE.md` (read fully before code)
- Target: `mag/grounding_wave.py` v3 → v4 + `tests/` new v4 suite

## Log (append as I go)

- [x] Read A2 design fully — stone 1 row law, status ladder, VOID procedure, two-eyes law, §5 build spec
- [x] Read grounding_wave v3 current shape — sha256_12 `1ce1ea1cafe8` matches the hash cited in the A2 receipt (built on the exact file the design targeted)
- [x] Compat sweep before code: `scripts/wave_driver.py` hashes v3 key sets against `mag.grounding_wave._row_hash` (test asserts exact match — v4 dispatch must key off `kind` presence so v3 rows hash identically); `mag/perturbation_battery.py` swaps `gw.LEDGER` and greps `EVIDENCE-MISSING` in `verify()` output — signature `(ok, msg)` and token preserved
- [x] G1/G2/G3 gate hardening — `_admit()` runs inside the append lock on EVERY verb: MALFORMED_ROW (missing/short hash or prev), HASH_MISMATCH, PREV_MISMATCH (vs admission tip), UNSUPPORTED_UNSEEDED (SUPPORTED with no seat refused outright), EVIDENCE_DEAD (dead path-shaped evidence refused at post, v3 checked at verify), EVIDENCE_MUTABLE (`*_latest` refused for SUPPORTED). Row-122's bypass path is physically impossible through the write path
- [x] Verbs: void / contest / witness / view (+ `--warrant` on post, `--dry` everywhere)
- [x] Status ladder RECORDED → CORROBORATED → CONTESTED → VOID in `view()` + ADMISSION summary in `verify()`
- [x] No auto-migration — v1/v2/v3 key sets hash byte-identically (test-pinned); live row 122 untouched; un-voided legacy defects still FAIL verify exactly as before
- [x] v4 test suite — 24 tests: row-122 shape refused at write, void cross-signature (refuse + count-only-when-signed), tamper detection, evidence mutation (identity), G3 warrant exit codes, full ladder in view, planted-failure propagation (child-of-void + witness-of-void, chain-visible), no-migration, §5.4-style void+re-anchor repair on a synthetic twin, void-of-void reversal
- [x] Full grounding test run (old + new): 67 collected, **65 passed / 2 failed** — both failures PRE-EXISTING and data/banner-drift, not v4 (details in §Findings below)
- [x] Row-122 void staged as PROPOSAL (dry-run only, nothing appended) — see §Operator hand-actions

## Findings during build

- **The v3 `render()` crashes on the live tape today** (KeyError: row 122 has no `verdict`/`hash` keys), so any v3 `post()` to the live ledger has been dying at render time since 09-16 04:17. v4 render/view are defensive (`.get` everywhere) — `post` to the live tape works again, which is also what makes the operator's void executable when he decides.
- **`shlex` posix-mode trap**: on Windows, `shlex.split(..., posix=False)` keeps quote characters inside tokens, so a quoted interpreter path in a warrant can never spawn. v4 warrants are split with `posix=True` and use forward slashes (canonical A2 form).
- **Tip collapse edge**: when every claim on a tape is voided, the admission tip would collapse to GENESIS mid-tape; a later void-of-void (reversal) re-validates earlier rows and strands them. Fix: admission tip falls back to the physical tip when no live claim exists. Pinned by the reversal test.
- **Live tape still FAILs verify at row 122** — by design. No migration: the fail→pass transition happens only through the operator's cross-signed void (proposals staged below).
- Two pre-existing failures in the old suite, untouched by this lane: `test_falsifier_ledger` (asserts every live-tape row has `evidence` — row 122's fragment never had it, failing since 09-16 04:17) and `test_wave_driver::test_tick_appends_chain_valid_row` (expects banner `WAVE_DRIVER v0 TICK`; the untouched driver prints `v1` — the driver's ground-row hash contract test `test_hash_matches_canonical_module` PASSES against v4).

## TEST COUNTS (verbatim, final run 2026-09-17T01:29Z)

- Grounding/wave selector (old + new, 67 collected):

  ```
  2 failed, 65 passed, 1428 deselected, 2 warnings in 14.04s
  FAILED tests/test_falsifier_ledger.py::test_grounding_jsonl_chain_and_schema        (pre-existing: live row 122 has no 'evidence' key)
  FAILED tests/test_wave_driver.py::TestSingleTickSubprocess::test_tick_appends_chain_valid_row  (pre-existing: driver prints "v1 TICK", test wants "v0"; hash contract test passes)
  ```

- v4 suite alone:

  ```
  26 passed, 1469 deselected, 2 warnings in 6.89s
  ```

- Live tape: `python -m mag.grounding_wave verify` → `FAIL row 122: MALFORMED_ROW (missing/short hash — v4 refuses this at write; contain it: void --row #122 --reason-code MALFORMED)` — honest failure preserved, exit 1, 124 rows, bytes untouched.

## THE V4 VERB SURFACE (all through the append lock + `_admit` G1 gate; refusals are typed `GATE-<CODE>` on stderr, exit 2)

| Verb | Form | Gate teeth |
|---|---|---|
| `post` | `post --claim … --verdict … --evidence … [--note] [--seat] [--witness] [--warrant "cmd"] [--dry]` | MALFORMED_ROW · HASH_MISMATCH · PREV_MISMATCH · UNSUPPORTED_UNSEEDED (SUPPORTED w/o seat refused, not demoted) · EVIDENCE_DEAD (dead path refused at post) · EVIDENCE_MUTABLE (`*_latest` refused for SUPPORTED) · BAD_VERDICT; records `src_sha256_12` per evidence token at post time (G2); `warrant` text hashed into the row (G3) |
| `void` | `void --row <hash-prefix\|#line> --reason-code <enum> --reason "…" --witness <second-seat> [--seat] [--evidence] [--dry]` | BAD_REASON_CODE (enum: MALFORMED · FORGED · EVIDENCE_DEAD · EVIDENCE_MUTATED · WARRANT_FAILED · DUPLICATE · SUPERSEDED · CONTEST_SUSTAINED) · VOID_UNSIGNED (no named second seat ≠ poster) · ALREADY_VOIDED · NOT_FOUND/AMBIGUOUS; void lands PENDING and COUNTS only when the named seat's `kind:"witness"` row signs it in-chain (two-eyes law) |
| `contest` | `contest --row <hash-prefix\|#line> --reason "…" [--seat] [--evidence] [--dry]` | holds target at CONTESTED; view stamps pending / STALE(>7d) (closure counter, A2 §4.3) / SUSTAINED |
| `witness` | `witness --row <hash-prefix> [--seat] [--dry]` | SELF_SIGNED (witness seat must differ from the signed row's seat); records `checks {g1 hash-recompute, g2 evidence re-hash vs src_sha256_12, g3_exit warrant run by THIS hand}` |
| `view` | `view` | effective ledger with ladder status per row + witnesses + voids (effective/PENDING) + contests (pending/STALE/SUSTAINED) + propagation (child-of-void / witness-of-void) |
| `verify` | `verify` | LINKAGE over physical tape (contained defects reported, uncontained FAIL) + G2 identity audit (EVIDENCE-MUTATED/DEAD FAIL) + truth-gate counts + `ADMISSION: V voided, C contested, R corroborated, P pending voids, N propagation-flagged` |
| `render` | `render` | md views, now void/ladder-aware and crash-proof against malformed legacy rows |

Status ladder: **RECORDED** (G1 pass) → **CORROBORATED** (≥2 witness rows, distinct seats, neither the author, checks pass) → **CONTESTED** (effective contest row) → **VOID** (effective cross-signed void row). Void-of-void is the same verb (reversal, test-pinned). §2 re-anchor: rows chained past a voided stretch are accepted by the reader and noted; new writes chain to the admission tip.

## FILES TOUCHED (worktree only — NO commits, per lane law)

- `mag/grounding_wave.py` — v3 (`1ce1ea1cafe8`) → v4; full backward-compatible surface (`_row_hash` versioned dispatch pinned by `test_v3_hash_compat_with_legacy_key_sets` and the wave_driver schema test)
- `tests/test_grounding_wave_v4.py` — new, 26 tests
- `watch/inbox/wave_20260916/receipts/V4_GROUNDING_ADMISSION.md` — this receipt

## WHAT THE OPERATOR MUST STILL DO BY HAND

**The row-122 void decision is his** (A2 caveat: the author is inside the machine too — and this seat is the author of v4, so it stages, does not execute). The two void rows below are **PROPOSALS**, dry-run only, nothing appended. The dry JSON is the *shape* — `ts`/`prev`/`hash` recompute at execution time.

1. **Read the proposals, then name his second seat.** Each void needs a cross-signature from a hand that is not the poster: `--witness <second-seat>` at void time, then a `witness` row from that seat signing the void's hash before it counts.
2. **Execute (or reject) void #122** — `voids: "line:122"` (it has no hash; line-addressing is the only honest pointer to a hashless row):
   `python -m mag.grounding_wave void --row "#122" --reason-code MALFORMED --reason "…" --seat <his-seat> --witness <second-seat>` then the second seat: `python -m mag.grounding_wave witness --row <void-hash-12> --seat <second-seat>`
3. **Same decision for row 123** (`d2c81c2dc98a…`, empty prev, unseeded SUPPORTED hand-written past the v3 gate): without voiding it too, the tape stays FAIL (its prev chains to nothing); with it voided, row 124 stands on the direct physical chain and `verify` returns `LINKAGE-PASS` with `contained by void` notes + `ADMISSION: 2 voided`. Rows 1–121 and 124 are untouched either way.
4. **Aftermath bookkeeping this seat deliberately did NOT do:** `test_falsifier_ledger` will still fail post-void (it asserts raw `evidence` presence on every physical row — it does not yet read the admission view); the perturbation battery's twin-A probe inherits the same live-tape break. Both need their own small void-aware pass, by another hand, with the operator's nod.
5. **Standing law going forward:** every new row carries v4 semantics automatically; nothing to migrate. The falsifier of this stone stays the A2 §5.5 stranger replay: `verify` + `view` on the tape alone from a second machine must reconstruct this admission view identically.

