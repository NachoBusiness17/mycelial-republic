# LANE 7 — PARENT VERIFICATION AND CORRECTION
## 2026-09-26 — the skeleton receipt's headline was right; one number was understated

*Lane 7 wrote a 50-line skeleton: headline findings plus four empty sections
(`PART A`–`PART D` marked `(filled from the observed run)` and never filled).
I re-verified all four headline claims myself rather than accept or discard them.*

---

## The headline holds. All four claims independently reproduced.

### Claim 1 — `config_seal` is RED on the real repo. **VERIFIED, and worse than reported.**

Lane 7 said "3 MODIFIED, 4 UNSEALED". Actual:

```
$ .venv\Scripts\python.exe tools/config_seal.py verify
CONFIG-SEAL verify: sealed=49 live=53 modified=6 missing=0 unsealed=4
  MODIFIED  improve.yaml  keys.json  lanes.yaml  providers.yaml
            spend_overlay.yaml  violation_baseline.json
  UNSEALED  links_kind_baseline.json  links_sha_ratchet_baseline.json
            sanctioned_scheduled_tasks.yaml  workflow_registry_baseline.json
CONFIG-SEAL: FAIL   exit=1
```

**10 problems, not 7.** Six modified seals and four unsealed configs.

**And this gate is wired into the pre-push hook with `|| exit 1`:**

```
githooks/pre-push:12
  .venv/Scripts/python.exe tools/config_seal.py verify || exit 1
```

**Consequence: the repo is currently UNPUSHABLE.** Any `git push` right now
fails at gate 2 of the hook. This is not a latent risk — it is an active block,
and it is the same failure family as F1: a gate that is correct, armed, wired,
and telling the truth, that nobody has run.

### Claim 2 — three gates have zero test coverage. **VERIFIED.**

| gate | test files referencing it |
|---|---:|
| `tools/config_seal.py` | **0** |
| `tools/checkbox_receipt_gate.py` | **0** |
| `tools/prepush_paths_changed.py` | **0** |
| `tools/violation_ratchet.py` | 4 (but see claim 4) |

All three exist as real files (`prepush_paths_changed.py`, 6,428 bytes) and all
three run inside `githooks/pre-push`. **The three gates that decide whether a
push lands are the three with no tests.**

### Claim 3 — mutation disarms the ratchet. **VERIFIED BY MY OWN RUN.**

I did not take lane 7's word. I copied `tools/violation_ratchet.py` to a temp
file, flipped the blocking `return 1` → `return 0`, and ran the ratchet's own
tests against it:

```
patched blocking return: True
.......                                                                  [100%]
7 passed in 0.82s
```

**A ratchet that can no longer fail passes all 7 of its tests.** Root cause is
visible in the test file — every assertion is on the success path:

```
tests/test_violation_ratchet.py:74    assert vr.cmd_prune() == 0
tests/test_violation_ratchet.py:97    assert vr.cmd_prune() == 0
tests/test_violation_ratchet.py:143   assert vr.cmd_baseline_update(...) == 0
tests/test_violation_ratchet.py:161   assert vr.cmd_check(changed_only=False) == 0
tests/test_violation_ratchet.py:179   assert vr.cmd_check(changed_only=False) == 0
```

Five assertions, all `== 0`. **Not one asserts `== 1`.** The ratchet's entire
purpose is the exit-1 path, and that path is untested. Cleanup verified: no
stray files in `tools/`, zero git entries.

### Claim 4 — the checkbox gate is deliberately non-blocking. **VERIFIED, and it is `|| true`.**

```
githooks/pre-push:112-116
  if [ -f tools/checkbox_receipt_gate.py ] && [ -f watch/inbox/burn_wave_20260926/QUEUE.md ]; then
    gate_out=$(.venv/Scripts/python.exe tools/checkbox_receipt_gate.py 2>&1) || true
  else
    echo "PUSH-GATE: checkbox_receipt_gate skipped (checker or queue missing)"
```

The `|| true` **is** the finding. This gate is currently RED — lane 2 measured
it: *"405 checked Open rows, 69 baseline-attached, 1 offenders. NEW DEBT:
B2-142: checked Open row names no receipt path resolving on disk."* — and the
hook swallows it. A gate that reports and cannot block is a dashboard, not a
gate. Note the two branches are asymmetric: the ratchet and config_seal use
`|| exit 1`, this one uses `|| true`.

---

## The synthesis this forces

Two categories, and they are opposite:

**Gates that block and are honest:** `violation_ratchet` (exit 1, 6 NEW),
`config_seal` (exit 1, 10 problems), `census_drift_patrol` (exit 1, +378),
`transport_precheck` and `config_seal` fail-closed on malformed input (verified
by lane 2 in a sandbox).

**Gates that cannot fail:**
- `checkbox_receipt_gate` — `|| true` in the hook, 0 tests, currently RED
- `violation_ratchet`'s *exit-1 path* — 0 tests assert it; mutation survives
- all three push-deciding gates — `config_seal`, `checkbox_receipt_gate`,
  `prepush_paths_changed` — have zero tests between them

**The pattern worth naming:** this fleet tests that its instruments *run*, and
almost never tests that they *block*. A gate's value is entirely in the branch
that says no, and that branch is the untested one in every case measured.

## Correction to the lane's own framing

Lane 7 reported the census at 2,288 collected and left PART A empty rather than
publishing a pass/fail count it had not finished measuring. **That was the right
call** — the repo's own census-denominator law demands a named instrument and
moment, and an unmeasured run reported as complete is exactly the failure that
produced the 1,910 headline. The empty section is more honest than a filled-in
guess. I am not treating the missing PART A as a defect.
