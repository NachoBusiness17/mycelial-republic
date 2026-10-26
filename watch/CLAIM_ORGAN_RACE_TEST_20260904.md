# CLAIM ORGAN RACE TEST — 2026-09-04

Verified by zcode seat (independent harness, not the builder's `mag/race_harness.py`).
Economist's ruling honored: the claim is tested at the bytes, not taken from code comments.

**Objects under test (READ-ONLY, unmodified):**
- `mag/bay_organs.py` — `try_claim` / `claim_active` / `claim_is_active` / `pid_alive` / `release_claim` / `sweep_expired`
- `watch/overnight_churn.py` v0.5.2 — the CLAIM ORGAN integration (lines 169-182, 277)

**Harness:** `watch/test_claim_race_20260904.py` (stdlib only, $0, no LLM calls)

---

## HARNESS

All state lives in a `tempfile.mkdtemp` claims root (`claim_race_test_20260904_*`).
The live bay (`watch/bay/claims`), the real queues, engines and containers are never
touched. Every `bay_organs` call passes `root=<tempdir>` explicitly.

- **TEST A — fresh race:** 6 REAL OS subprocesses (not threads) x 10 rounds, all
  claiming the SAME task id at the same moment (READY-file arming, then a GO-file
  gate, sub-ms skew). Winners hold until judged. Asserts per round: exactly 1
  winner, 5 clean losers, exactly one claim FILE whose pid+engine+token match the
  winner, zero `.tmp` litter, `claim_active()` True while holders are alive.
- **TEST B — takeover race:** a forged STALE claim (dead pid, fresh ts, grace 1800)
  sits on the task; 6 racers x 4 rounds race `try_claim` to take it over — this is
  the move-aside-then-CAS path. Same single-winner + tombstone asserts.
- **TEST C — pid-death grace:** win32 `OpenProcess` probe agrees on a dead pid;
  dead-pid claim is invisible immediately and reclaimable; live-pid fresh claim is
  active and a rival loses cleanly; `release_claim` refuses a wrong token and keeps
  the file, honors the right token; expired-ts live-pid claim is stealable; corrupt
  claim file is never treated as a lock (and never stolen blind); in-vivo: racers
  that exit mid-hold release their food and a survivor reclaims.
- **TEST E — deterministic takeover TOCTOU repro:** replays the exact interleaving
  TEST B hit, with zero timing luck (see FINDING 1).
- **TEST D — sweep hygiene:** `sweep_expired` removes dead-pid claims, keeps live
  claims and fresh tombstones.

## RESULT

**FAIL — 3 of 5 test groups pass; the takeover path violates the single-winner invariant.**

| Test | Result | Numbers |
|---|---|---|
| A fresh race (6 procs x 10 rounds) | PASS | 10/10 rounds exactly 1 winner, 5 clean losers; 0 double-claims, 0 zero-winner, 0 tmp-litter, file==winner every round |
| B takeover race (6 procs x 4 rounds) | **FAIL** | 4/4 rounds MULTIPLE winners: 2, 2, 3, 2 winners out of 6; losers all clean (no exceptions) |
| C pid-death grace (21 checks) | PASS | 21/21 incl. dead-pid instant release, token-guarded release, in-vivo exit-release |
| D sweep hygiene | PASS | dead claims swept, live kept, fresh tombstones kept |
| E TOCTOU repro | **FAIL** | `t1_won=True t2_won=True -> DOUBLE CLAIM`; the tombstone holds T2's fresh live claim |

Full transcript in session log; re-run: `python watch/test_claim_race_20260904.py` (exit 0 = all pass; currently exits 1).

## VERDICT

**The claim organ does NOT yet satisfy Leg-1.**

- The **fresh-claim path** (the CAS itself) is proven sound: 60 concurrent
  subprocess claimants across 10 rounds produced exactly one winner every time,
  with byte-level file agreement. The `os.rename` create-by-rename CAS works.
- The **pid-death grace** is proven sound and genuinely win32-correct (the
  `OpenProcess` probe is honest where `os.kill(pid,0)` was a no-op).
- The **stale-takeover path is split-brain under contention** — and this is a path
  the fleet hits in NORMAL operation: whenever a claim goes stale (engine crash or
  `BAY_CLAIM_GRACE_S` expiry) multiple engines see the task as pending on the same
  cycle and race the takeover. Measured: up to 3 of 6 racers all returned success.
  That is the double-mining class (sp_83204700) the organ exists to kill,
  reintroduced through the takeover door.

The builder's own gate (`mag/race_harness.py`) cannot see this: its TEST 1 races
only 2 claimants on a FRESH item, and its TEST 2 grace checks are sequential —
the takeover path is never raced.

## FINDINGS (filed, not patched — bay_organs.py untouched per ground rules)

**FINDING 1 (blocking): unconditional tomb-move TOCTOU in `try_claim`.**
`mag/bay_organs.py` ~lines 243-249: after a taker proves the claim it READ is
stale, it does `os.rename(target, tomb)` with NO re-check that target still holds
the claim it judged. Interleaving: T1 reads stale claim S and proves it stale;
T2 completes a full legitimate takeover (its tomb-move + CAS win) putting a FRESH
claim at target; T1 resumes and its tomb-move moves T2's LIVE claim to a
`.expired-` tombstone; T1's CAS then wins the freed name. Both T1 and T2 return
success. TEST E reproduces this deterministically; TEST B shows it fires
naturally under 6-way contention (4/4 rounds). Cascade effect: each mis-tombed
live claim can itself be re-stolen, which is how 3 winners appeared in one round.
Fix shape (for the owner, not applied here): after the staleness proof, re-read
target and tomb-move only if it is still THE SAME claim (match on token), or
replace move-aside entirely with an overwrite-CAS that embeds the judged-stale
token in the new claim file (write-new-then-rename still single-winner).

**FINDING 2 (minor): corrupt claim files are unsweepable permanent locks.**
A claim file with unparseable JSON is correctly never treated as a lock
(`claim_is_active` -> False), but `sweep_expired` skips it (`if c and ...`) and
`try_claim` loses-safely forever (3 CAS rounds, returns None). In
overnight_churn the task is then skipped every cycle as "claimed elsewhere
mid-pick" until a human deletes the file. Probability low (temp-write + fsync +
rename makes half-written targets unlikely; win32 filter locks are re-read and
transient), but if it happens it is permanent. Fix shape: sweep unreadable
`.json` files older than some mtime threshold.

**FINDING 3 (observation): no orphan-claim leak.** Racers that win and then exit
leave their claim file behind, but it is correctly invisible (`pid_alive` False)
and reclamation is instant — measured in-vivo (C5). `sweep_expired` cleans them.

## TRI-STATE

| Claim | State | Evidence |
|---|---|---|
| "Before dispatch, an engine atomically claims the task; two engines can never both hold a fresh item" (fresh path) | **Supported** | 10 rounds x 6 subprocesses, 60 claim attempts, exactly 1 winner + matching claim file every round |
| "Claims expire on grace or claimant pid death and are reclaimed" | **Supported** | 21/21 grace checks incl. win32 probe, in-vivo exit-release, survivor reclaim |
| "Takeover of stale claims stays single-winner" | **Disputed** | 4/4 contended takeover rounds multi-winner (2-3 of 6); deterministic TOCTOU repro produced a double claim and tombstoned a live claim |
| "Every interleaving of two takers yields exactly one winner" (bay_organs docstring) | **Disputed** | contradicted by TEST E interleaving; the invariant holds only when no tomb-move occurs |
| "Corrupt claim state cannot wedge a task" | **Unproven** | corrupt file never locks (proven) but is never swept and blocks `try_claim` indefinitely (proven) — wedge severity depends on operational frequency of corruption, not measured here |

## RULES COMPLIANCE

Live queue files: untouched. Engines/containers: not restarted. `overnight_churn.py`
and `bay_organs.py`: read-only (findings filed above, no patches). Harness: stdlib
only, all claim state in temp dirs, explicit `root=` on every call.

---

## CLOSURE (2026-09-05, zcode seat — the throttle is dead)

**FINDING 1 FIX LANDED + VERIFIED 2x.** `bay_organs.py` mtime 09-04 10:31 — `_tomb_move_if_same`
(CAS tomb-move: re-read + token match at commit, rename-CAS) replaced the unconditional tomb-move,
exactly the fix-shape FINDING 1 named. Post-fix rerun same hour, both harnesses, $0, tempdir-isolated:

- **Independent harness (this file's own): PASS, exit 0** — A=ok B=ok C=ok D=ok E=ok.
  The two FAILs are dead: TEST B takeover race single-winner holds; TEST E deterministic
  TOCTOU shows t1_won=False t2_won=True, guarded tomb-move refused, T2's live claim intact.
- **Builder harness (mag/race_harness.py): 3/3 PASS — "GATE OPEN"** (race 20x2 double-claims=0).

One builds, one verifies. Leg-1 condition satisfied; tranche scale-up UNBLOCKED at the organ
level (execution still waits: drain-engine revival + pools reset Sep 8). Residual notes stay
open (corrupt-claim = permanent lock was TEST-C-passing; keep the sweep hygiene).
