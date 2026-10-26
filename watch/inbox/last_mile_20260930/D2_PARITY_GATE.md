# D2_PARITY_GATE — the parity proof is STANDING: rule_parity CI-shaped + wired into pre-push

2026-09-30 · seat: zcode (D2, last_mile Q01 second half) · ownership: `tools/rule_parity.py`
(extended), `githooks/pre-push` (new gate block), `tests/test_parity_gate_hook_pin.py`,
`tests/test_rule_parity.py` (extended), `tools/rule_parity_out/latest.json` (standing artifact),
this receipt. No commit by me (operator order; note below — D1's lane swept my in-flight tool+test
edits into its commit `9ed2c153f`, verified byte-present in HEAD).

## Mission

The V5 harness (receipt `V5_PARITY.md`) proved the twins can silently diverge — but a one-off
artifact is not a differentiator's proof. D2 makes it standing: CI profiles, a pre-push FAIL-blocks
gate on twin changes, a committed-adjacent last-verdict artifact, tests, and the honest bank.

## What landed

1. **`tools/rule_parity.py` CI-shaped.** `all --quick` (20 seqs / 40 ticks + 1 fracture loop,
   1,220 frames, **2.1s measured**, budget <60s machine-warned) and `all --full` (100 seqs,
   14,040 frames — byte-compatible with the V5 receipt corpus, **8.8s measured**) for nightly.
   Explicit `--seed/--n/--ticks` beat the preset; `--out-dir`, `--source` added. FIRST-LINE
   CONTRACT (B2-338 law): `PARITY: ok|FAIL|ERROR mode=…` opens stdout; exit 0/1/2. Mix law fix:
   mountain share scales with n (old code made n=20 ALL-mountain — a quick corpus blind to the
   LW5 seam it exists to watch); quick now covers all 5 families (4/5/5/1/5), pinned by test.
2. **Pre-push gate** (`githooks/pre-push`, between the scenario-suite gate and the secret gate).
   Trigger law: fires only when EITHER twin changes (`mag/water_graph.py`,
   `roblox_to_godot/systems/water_graph.gd`) — decision via the B2-272 helper
   `tools/prepush_paths_changed.py` (dirty / untracked / pushed-range arms), fail-closed on its
   exit 2 (B2-277: a blind enforcing gate is worse than none). Payload:
   `rule_parity.py all --quick --source prepush`. ENFORCING day one by D2 mission contract (not a
   t40 WARN-first break — a WARN-only parity gate repeats the disease it closes): case arm matches
   the lowercase `PARITY: ok` prefix only; FAIL, ERROR, and tracebacks all fall to `exit 1`.
   Tool writes only its own untracked out dir (B2-328 push-hook law; watch/inbox untouched).
   Twins unchanged → `skipped, twins unchanged` (verified by standalone block run).
3. **Standing artifact** `tools/rule_parity_out/latest.json` (schema `rule_parity_latest.v1`):
   every run (gate included) refreshes it — mode, params, wall, parity, exit_code,
   first_divergence, per_family, and content sha256 of BOTH twins, so a dirty tree can never hide
   behind a stale verdict. Current bank: **parity true, full depth, 100/100 sequences, 14,040
   frames, 8.8s, twins gd=35a4edeae0dc py=71203c04f088, source=manual**.
4. **Tests.** New `tests/test_parity_gate_hook_pin.py` (6 tests, B2-451 pin pattern, real hook
   bytes): twins wired as the exact trigger; enforcing + fail-closed arms; quick+source payload;
   **trigger fires on either twin (dirty py / dirty gd / untracked) and skips on clean or
   unrelated-only changes** — decided by the real helper in a real temp repo; gate payload's first
   line + latest.json agree with the exit code (honest-orbit) and replay through the hook's real
   case arm via sh; case-flip falsifier caught. Extended `tests/test_rule_parity.py` (+5): profile
   shapes (full == V5 corpus incl. 14,040 frames), flags-beat-preset, quick covers every family
   within the 1,500-frame budget, small-n family spread. **22 passed** across both files.

## The gate WOULD have caught today's bug — proven on real history

D1 landed mid-task (its staged→committed `9ed2c153f` ported the LW5 probe-time reserve), so the
gate runs GREEN now (quick 2.1s, full 8.8s, zero divergence). To prove the gate's teeth honestly I
replayed the PRE-fix twin (`9ed2c153f^`) in a throwaway project copy (no contact with the shared
tree): quick corpus → **PARITY: FAIL, exit 1** — `parity: False`, gated_siblings 4/5 diverged at
tick 1, mountain first divergence seq_002 tick 4 with the exact v0 signature
(`nodes.spring.volume: py=0 gd=-1`, `terrace py=0 gd=1`, phantom `p_bypass.primed`). Chain: twin
change ⇒ trigger fires (test-pinned) ⇒ payload FAIL exit 1 (demonstrated on real history) ⇒ case
arm blocks the push (test-pinned). **The gate would have blocked the push that shipped the v0
divergence — that is the point, banked.**

Race note for the record: my first replay attempt overwrote the worktree twin and restored it
byte-exact, but D1 committed during the 30s window — the run was invalidated by the race (not by
gate weakness), the restore landed clean (worktree == HEAD verified), and the redo used the
throwaway-copy method above. Lesson: never stage a shared-tree replay against a lane with a live
claim; copy the project instead.

## Honest bank / how to check "currently true"

```
cat tools/rule_parity_out/latest.json        # last run's verdict + twin digests + mode
.venv/Scripts/python.exe tools/rule_parity.py all --quick --source prepush   # gate path (~2s)
.venv/Scripts/python.exe tools/rule_parity.py all --full --source nightly    # nightly (~9s)
```

## Debt / census notes

- Ratchet `check --changed`: my remaining files (githooks/pre-push, tests, latest.json) carry NO
  new debt (githooks is outside the mag/+tools/ scope). `tools/rule_parity.py` is 791 lines
  (file-too-long) — now committed inside `9ed2c153f` so invisible to `--changed`, but present;
  a full `check` names it. Sibling pain_replication NEW debt (11 items) is not D2's.
- Census: +11 collected tests (6 + 5), delta under the 20-collect threshold; attribution named
  here per the census law.
- Committing `latest.json` (and the gate block) is the operator's call — the artifact is
  committed-adjacent and refreshes on every gate run regardless.
