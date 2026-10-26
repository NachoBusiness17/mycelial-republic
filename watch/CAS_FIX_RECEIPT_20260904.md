# CAS FIX RECEIPT — claim-organ stale-takeover split-brain — 2026-09-04

Builder: zcode seat (background gopher, salon-unanimous GO #1).
Bug under surgery: `mag/bay_organs.py` `try_claim` FINDING 1 from
`watch/CLAIM_ORGAN_RACE_TEST_20260904.md` — the stale-takeover tomb-move was
an UNCONDITIONAL `os.rename(target, tomb)` after the staleness proof, with no
re-check that the target still held the claim that was judged. Under 6-way
contention: 2-3 simultaneous winners in 4/4 rounds; deterministic TOCTOU repro
tombed a rival's LIVE claim.

## VERDICT

**PASS — all paths.** Split-brain closed: contended takeover now yields
EXACTLY 1 winner per round; losers lose honestly (return None, no write, no
exception). Harness exit 0, twice in a row (contended paths re-run for
stability). Builder's own gate `mag/race_harness.py` still 3/3 PASS (no
regression).

| Path | Before (card, 2026-09-04) | After (this fix) | Verdict |
|---|---|---|---|
| A fresh race (6 procs x 10 rounds) | PASS 10/10 exactly 1 winner | PASS 10/10 exactly 1 winner, 5 clean losers, file==winner, 0 tmp-litter, active-while-alive | **PASS** (unchanged path) |
| B stale-takeover race (6 procs x 4 rounds) | **FAIL** 4/4 multi-winner (2,2,3,2 of 6) | PASS 4/4 exactly 1 winner, losers clean, exactly one new `.expired-` tombstone per round, file==winner | **PASS** |
| C pid-death grace (21 checks) | PASS 21/21 | PASS 21/21 (dead-pid instant release, token-guarded release, expired-steal, corrupt-no-blind-steal, in-vivo exit-release + survivor reclaim) | **PASS** |
| D sweep hygiene | PASS | PASS (dead swept, live kept, tombstones kept) | **PASS** |
| E deterministic TOCTOU | **FAIL** double claim, live claim tombed | PASS guarded move REFUSED, t1_won=False t2_won=True single winner, T2's live claim intact at target, no tomb | **PASS** |

Re-run: `python watch/test_claim_race_20260904.py` (exit 0). Full transcript
in session log. Second confirmation run: also exit 0, all groups.

## THE FIX (mag/bay_organs.py)

Compare-and-swap on the claim's identity token, exactly the fleet-agreed
shape: capture the judged-stale claim's `token` at decision time; at the
commit moment re-read the target and tomb-move ONLY if the token still
matches; on mismatch LOSE HONESTLY (no write; the 3-round loop re-reads and
re-judges whatever now sits at target — a fresh live claim → return None).

New helper `_tomb_move_if_same(target, tomb, judged_token)` (stdlib, 18 lines):
re-read → token match? → rename; any race (target gone, unreadable, re-taken,
or rename lost) returns False with zero writes beyond a failed rename attempt.
`try_claim`'s stale-takeover block becomes a single call:
`_tomb_move_if_same(target, tomb, existing.get("token"))`.

Unified diff, `mag/bay_organs.py.bak-20260904-pre-cas` → `mag/bay_organs.py`:

```diff
@@ -11,9 +11,10 @@
    an atomic test-and-set: when two engines race on one item, exactly one rename
    wins. Claimed items are invisible to other claimants until grace expiry
    (default 30 min, env BAY_CLAIM_GRACE_S) or until the claimant's pid dies.
-   Expired/dead claims are taken over by move-aside-then-recreate, which stays
-   single-winner because the final creation is always a rename-CAS onto the one
-   fixed target name.
+   Expired/dead claims are taken over by token-checked move-aside (the
+   tomb-move fires only if the target still holds the EXACT claim that was
+   proven stale) then rename-CAS onto the freed name — single-winner under
+   contention.
@@ -176,6 +177,25 @@
+def _tomb_move_if_same(target, tomb, judged_token):
+    """CAS tomb-move for the stale-takeover path: only move the claim at
+    target aside if it is STILL the exact claim the taker proved stale
+    (token match at commit time). Kills the takeover split-brain
+    (watch/CLAIM_ORGAN_RACE_TEST_20260904.md FINDING 1): the old
+    unconditional tomb-move could move aside a RIVAL'S fresh live claim that
+    landed between the staleness proof and the move — two winners. Returns
+    True only if THIS taker's rename won; on any race (target gone,
+    unreadable, or re-taken) False and NO write: lose honestly."""
+    current = _read_claim(target)
+    if current is None or current.get("token") != judged_token:
+        return False  # raced away or re-taken by another taker: refuse
+    try:
+        os.rename(target, tomb)
+        return True
+    except OSError:
+        return False  # another taker's rename beat ours to the source
+
@@ -202,13 +222,16 @@
-    Takeover of stale claims (expired or dead pid) is move-aside-then-CAS, and
+    Takeover of stale claims (expired or dead pid) is judge-then-CAS, and
     NEVER blind: we only tomb-move a claim we could actually read AND prove
-    stale. [...]
+    stale, and at the commit moment we re-read and tomb-move ONLY if the
+    target still holds that exact claim (token match) — otherwise we lost
+    the takeover race and lose honestly, no write. [...]
@@ -241,12 +264,13 @@
             # POSITIVE staleness proven (parseable + expired or dead pid):
-            # move the stale claim aside, then CAS onto the freed name.
+            # commit the takeover by compare-and-swap — re-read the target
+            # and tomb-move ONLY if it still holds the exact claim we judged
+            # stale (token match). A mismatch means another taker won the
+            # takeover after our read: we lose honestly and the loop's next
+            # round re-reads and re-judges whatever now sits at target.
             tomb = os.path.join(d, ".expired-%s-%d-%d.json" % (task_id, time.time_ns(), os.getpid()))
-            try:
-                os.rename(target, tomb)         # only ONE taker can win this move
-            except OSError:
-                pass                            # another taker moved it first
+            _tomb_move_if_same(target, tomb, existing.get("token"))
```

(Full-context diff regenerable: `diff -u mag/bay_organs.py.bak-20260904-pre-cas mag/bay_organs.py`)

## HARNESS CHANGE (disclosed, watch/test_claim_race_20260904.py)

TEST E's deterministic replay manually performed the OLD unconditional
`os.rename` — post-fix that would test dead behavior and fail spuriously.
The replay now performs T1's commit through the SAME guarded primitive the
fixed organ uses (`bay_organs._tomb_move_if_same` with T1's stale token),
which is the honest way to force the exact interleaving: the TOCTOU window
lives INSIDE try_claim between judge and commit, so the interleaving cannot
be driven through the public API without the manual step. Assertions
STRENGTHENED, not weakened: E2 now requires the guarded move to REFUSE;
E4 (previously only ran on double-claim, to autopsy it) now asserts T2's live
claim is INTACT at target and no tomb exists. Expectations for A/B/C/D
untouched. The card's before-numbers were produced by the original harness;
both files' pre-surgery state is preserved in `.bak-20260904-pre-cas` copies.

## WHY THE GUARD HOLDS UNDER CONTENTION (mechanics, not hope)

- N takers all judge the SAME stale claim → all capture the SAME token. The
  first rename wins the source; every later guarded move either re-reads
  None (target gone) or loses the rename (FileNotFoundError → OSError →
  False). At most ONE tomb per claim generation — measured: exactly one new
  `.expired-` tombstone per TEST B round (tombs=1,2,3,4 across 4 rounds).
- The old kill-chain (mis-tombed LIVE claim re-stealable → 3 winners) is
  dead: a rival's fresh claim carries a different token → guarded move
  refuses → refusing taker's next loop round sees fresh+active → returns
  None honestly.
- TEST E proves the exact card interleaving now refuses: T1 judged stale,
  T2 fully took over, T1's commit sees T2's token ≠ stale token → no move,
  T1's subsequent try_claim loses cleanly against T2's live claim.

## RESIDUAL WINDOW (honest accounting — new race searched, one micro-window remains)

Between `_tomb_move_if_same`'s re-read and its rename there is still a
microsecond-scale TOCTOU: another taker could complete a full takeover in
that gap and our rename would move its fresh claim. Assessment: not
reachable as split-brain in practice — for the gap to fire, a rival must
judge the same stale claim, pass ITS token check, rename it to a tomb, and
CAS a fresh claim onto the freed name, ALL between our read and our rename;
and the old window spanned the entire staleness proof (pid probe + time
parse) plus 3-round re-read loops with 20ms sleeps, which is why TEST B hit
it 4/4 naturally while this one needs an adversary inside a syscall gap.
Verdict: residual risk real but vanishingly narrow, single-winner invariant
now enforced at both commits (tomb-move + create); no new multi-winner
observed in 2 full harness runs + builder gate. Stdlib offers no
content-checked rename; closing the last gap would need a lock file or
OS-level transactional rename — not warranted for this organ's threat model.

FINDING 2 from the card (corrupt claim files unsweepable → permanent skip)
remains OPEN and untouched — separate fix, separate card (this surgery was
scoped to FINDING 1 only).

## RULES COMPLIANCE

- Backup BEFORE any edit: `mag/bay_organs.py.bak-20260904-pre-cas`,
  `watch/test_claim_race_20260904.py.bak-20260904-pre-cas` (both verified on
  disk).
- Minimal diff: 1 helper + 1 call-site + 2 docstring corrections in the
  organ; TEST E replay + assertions in the harness. stdlib only, zero new
  deps. No API keys touched or echoed.
- Other organs untouched; callers audited (`overnight_churn.py`,
  `march_228.py`, `mag/race_harness.py`) — all use the public claim-or-None
  contract, unchanged for them except the now-honest contended case.
- No containers restarted; live bay `watch/bay/claims` never touched (all
  harness state in `tempfile.mkdtemp`).
