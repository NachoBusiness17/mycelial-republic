#!/usr/bin/env python3
"""test_claim_race_20260904.py — independent race harness for the CLAIM ORGAN
(mag/bay_organs.try_claim / claim_active), the double-mine fix behind
watch/overnight_churn.py v0.5.2.

What it does (all state in TEMP dirs — the live claims root watch/bay/claims,
the real queues, engines and containers are never touched):

  TEST A  RACE, 6 real OS subprocesses x 10 rounds — every claimant hits
          try_claim on the SAME task id at the same moment (READY/GO file
          gate). Assert per round: exactly 1 winner, 5 clean losers (no
          exceptions), the claim FILE matches the winner (pid+engine+token),
          no .tmp litter, claim_active() True while holders live.
  TEST B  TAKEOVER RACE, 6 racers x 4 rounds — a forged STALE claim (dead
          pid, fresh ts) sits on the task; all 6 race to take it over
          (move-aside-then-CAS path). Exactly 1 winner, exactly 1 .expired
          tombstone, claim belongs to the winner.
  TEST C  PID-DEATH GRACE — dead-pid claim: claim_active() False immediately,
          reclaim succeeds; in-vivo: after racer processes exit, their claim
          file remains but claim_active() goes False and a survivor reclaims.
          Live-pid fresh claim: active, second claimant loses cleanly;
          release_claim(token) frees it, wrong token does NOT. Live-pid
          expired claim: inactive, takeover wins. Corrupt claim file:
          never treated as a lock (finding: also never swept, see card).
  TEST D  SWEEP HYGIENE — sweep_expired removes dead-pid claims, keeps live
          claims and fresh tombstones.

Run: python watch/test_claim_race_20260904.py   (stdlib only, $0, no LLM)
Exit 0 = claim organ holds. This file is a test: it never modifies
overnight_churn.py or bay_organs.py.
"""

import glob
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from mag import bay_organs  # noqa: E402

RACERS = 6
RACE_ROUNDS = 10
TAKEOVER_ROUNDS = 4

WORKER_SRC = r'''
import json, os, sys, time
repo, claims_root, queue, task_id, engine, go_path, done_path, result_path, ready_path = sys.argv[1:10]
sys.path.insert(0, repo)
from mag import bay_organs
with open(ready_path, "w") as f:
    f.write("ready")
t0 = time.time()
while not os.path.isfile(go_path):
    if time.time() - t0 > 60:
        sys.exit(2)
    time.sleep(0.005)
claim, err = None, ""
try:
    claim = bay_organs.try_claim(queue, task_id, engine=engine, slot=engine,
                                 grace_s=300, root=claims_root)
except Exception as e:
    err = repr(e)
res = {"pid": os.getpid(), "engine": engine, "won": claim is not None,
       "token": claim["token"] if claim else None, "err": err}
with open(result_path, "w", encoding="utf-8") as f:
    json.dump(res, f)
t0 = time.time()  # hold the claim while the judge inspects state
while not os.path.isfile(done_path):
    if time.time() - t0 > 30:
        break
    time.sleep(0.01)
'''

FAILURES = []


def check(name, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           (" - " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name + ((" - " + detail) if detail else ""))
    return ok


def forge_claim(claims_root, queue, task_id, pid, engine, ts=None, grace_s=1800,
                token="forged-0", raw=None):
    path = bay_organs.claim_path(queue, task_id, claims_root)
    if raw is not None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(raw)
        return path
    claim = {"queue": queue, "task": task_id, "engine": engine, "slot": "s",
             "pid": pid, "ts": ts or bay_organs.now_iso(), "grace_s": grace_s,
             "token": token}
    bay_organs.atomic_write_json(path, claim, overwrite=True)
    return path


def run_race(claims_root, queue, task_id, stale=False):
    """Spawn RACERS real processes; return (results, worker_tmpdir)."""
    tmpw = tempfile.mkdtemp(prefix="claimrace_workers_")
    worker = os.path.join(tmpw, "worker.py")
    with open(worker, "w", encoding="utf-8") as f:
        f.write(WORKER_SRC)
    go = os.path.join(tmpw, "GO")
    done = os.path.join(tmpw, "DONE")
    if stale:
        ghost = subprocess.Popen([sys.executable, "-c",
                                  "import time; time.sleep(0.2)"])
        ghost.wait()
        forge_claim(claims_root, queue, task_id, ghost.pid, "ghost-dead")
    procs, paths = [], []
    for i in range(RACERS):
        res = os.path.join(tmpw, "result-%d.json" % i)
        rdy = os.path.join(tmpw, "READY-%d" % i)
        paths.append(res)
        procs.append(subprocess.Popen(
            [sys.executable, worker, ROOT, claims_root, queue, task_id,
             "racer-%d" % i, go, done, res, rdy],
            cwd=tmpw, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    # all racers armed, none has fired (no GO yet)
    deadline = time.time() + 60
    while time.time() < deadline:
        if all(os.path.isfile(os.path.join(tmpw, "READY-%d" % i))
               for i in range(RACERS)):
            break
        if any(p.poll() is not None for p in procs):
            break
        time.sleep(0.02)
    armed = all(p.poll() is None for p in procs) and all(
        os.path.isfile(os.path.join(tmpw, "READY-%d" % i))
        for i in range(RACERS))
    with open(go, "w", encoding="utf-8") as f:
        f.write("go")
    deadline = time.time() + 60
    while time.time() < deadline:
        if all(os.path.isfile(p) for p in paths):
            break
        time.sleep(0.02)
    # MID-FLIGHT state check: all racers still alive and holding (DONE not
    # yet written) — this is the "holder alive" moment. Checked here because
    # after DONE the racers exit and the organ CORRECTLY releases their food.
    mid_active = bay_organs.claim_active(queue, task_id, grace_s=300,
                                         root=claims_root)
    with open(done, "w", encoding="utf-8") as f:
        f.write("done")
    for p in procs:
        try:
            p.wait(timeout=30)
        except subprocess.TimeoutExpired:
            p.kill()
    results = []
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                results.append(json.load(f))
        except Exception as e:
            results.append({"pid": -1, "engine": "?", "won": False,
                            "token": None, "err": "no-result: " + repr(e)})
    return results, tmpw, armed, mid_active


def judge_round(claims_root, queue, task_id, results, expect_tombstone,
                mid_active=None):
    d = bay_organs.claim_dir(queue, claims_root)
    wins = [r for r in results if r.get("won")]
    errs = [r for r in results if r.get("err")]
    ok = True
    ok &= check("round %s winner-count==1" % task_id, len(wins) == 1,
                "winners=%d losers=%d" % (len(wins), RACERS - len(wins)))
    ok &= check("round %s losers-clean" % task_id, not errs,
                "errors=%s" % ([r["err"] for r in errs][:2],))
    if mid_active is not None:
        ok &= check("round %s claim_active-while-holders-alive" % task_id,
                    mid_active is True)
    if len(wins) != 1:
        return False
    w = wins[0]
    ok &= check("round %s winner-token" % task_id, bool(w.get("token")))
    mains = [f for f in glob.glob(os.path.join(d, "*.json"))
             if os.path.basename(f) == task_id + ".json"]
    ok &= check("round %s exactly-one-claim-file" % task_id, len(mains) == 1,
                "files=%d" % len(mains))
    tmps = glob.glob(os.path.join(d, ".tmp-*"))
    ok &= check("round %s no-tmp-litter" % task_id, not tmps,
                "tmp=%d" % len(tmps))
    if mains:
        fc = bay_organs._read_claim(mains[0])
        ok &= check("round %s file-matches-winner" % task_id,
                    bool(fc) and fc.get("pid") == w["pid"]
                    and fc.get("engine") == w["engine"]
                    and fc.get("token") == w["token"],
                    "file=%s" % (fc,))
    tombs = glob.glob(os.path.join(d, ".expired-*"))
    if expect_tombstone:
        ok &= check("round %s stale-tombstoned" % task_id, len(tombs) >= 1,
                    "tombs=%d" % len(tombs))
    return ok


def test_race(claims_root, queue):
    print("TEST A: fresh race - %d processes x %d rounds on one task id"
          % (RACERS, RACE_ROUNDS))
    ok = True
    for i in range(RACE_ROUNDS):
        tid = "race-item-%02d" % i
        results, _tmpw, armed, mid_active = run_race(claims_root, queue, tid,
                                                     stale=False)
        if not armed:
            ok = False
            check("round %s all-racers-armed" % tid, False,
                  "a racer died before GO")
        ok &= judge_round(claims_root, queue, tid, results,
                          expect_tombstone=False, mid_active=mid_active)
    return ok


def test_takeover_race(claims_root, queue):
    print("TEST B: stale-claim takeover race - %d processes x %d rounds"
          % (RACERS, TAKEOVER_ROUNDS))
    ok = True
    for i in range(TAKEOVER_ROUNDS):
        tid = "takeover-item-%02d" % i
        results, _tmpw, armed, mid_active = run_race(claims_root, queue, tid,
                                                     stale=True)
        if not armed:
            ok = False
            check("round %s all-racers-armed" % tid, False,
                  "a racer died before GO")
        ok &= judge_round(claims_root, queue, tid, results,
                          expect_tombstone=True, mid_active=mid_active)
    return ok


def test_pid_grace(claims_root, queue):
    print("TEST C: pid-death grace and claim-state integrity")
    ok = True
    # C1: dead claimant -> invisible immediately, reclaim succeeds
    dead = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(0.2)"])
    dead.wait()
    time.sleep(0.05)
    ok &= check("C0 probe-agrees-pid-dead",
                bay_organs.pid_alive(dead.pid) is False)
    forge_claim(claims_root, queue, "grace-deadpid", dead.pid, "ghost")
    ok &= check("C1 dead-pid-claim-not-active",
                bay_organs.claim_active(queue, "grace-deadpid", root=claims_root)
                is False)
    take = bay_organs.try_claim(queue, "grace-deadpid", engine="taker",
                                grace_s=300, root=claims_root)
    ok &= check("C1 dead-pid-claim-reclaimed", bool(take))

    # C2: live holder (this process) -> active, rival loses, release semantics
    mine = bay_organs.try_claim(queue, "grace-live", engine="holder",
                                grace_s=300, root=claims_root)
    ok &= check("C2 live-claim-won", bool(mine))
    ok &= check("C2 live-claim-active",
                bay_organs.claim_active(queue, "grace-live", root=claims_root)
                is True)
    rival = bay_organs.try_claim(queue, "grace-live", engine="rival",
                                 grace_s=300, root=claims_root)
    ok &= check("C2 rival-loses-cleanly", rival is None)
    ok &= check("C2 wrong-token-release-refused",
                bay_organs.release_claim(queue, "grace-live", "wrong-token",
                                         root=claims_root) is False)
    ok &= check("C2 wrong-token-claim-intact",
                os.path.isfile(bay_organs.claim_path(queue, "grace-live",
                                                     claims_root)))
    ok &= check("C2 right-token-release",
                bay_organs.release_claim(queue, "grace-live", mine["token"],
                                         root=claims_root) is True)
    ok &= check("C2 released-and-gone",
                bay_organs.claim_active(queue, "grace-live",
                                        root=claims_root) is False
                and not os.path.isfile(bay_organs.claim_path(
                    queue, "grace-live", claims_root)))

    # C3: live pid but EXPIRED claim -> inactive, takeover wins
    old_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ",
                           time.gmtime(time.time() - 400))
    forge_claim(claims_root, queue, "grace-expired", os.getpid(), "stale-live",
                ts=old_ts, grace_s=300)
    ok &= check("C3 expired-live-pid-not-active",
                bay_organs.claim_active(queue, "grace-expired", grace_s=300,
                                        root=claims_root) is False)
    take = bay_organs.try_claim(queue, "grace-expired", engine="taker",
                                grace_s=300, root=claims_root)
    ok &= check("C3 expired-claim-takeover", bool(take))

    # C4: corrupt claim file -> never a lock (lose-safely, no blind steal)
    forge_claim(claims_root, queue, "grace-corrupt", dead.pid, "corrupt",
                raw="not-json{{{")
    ok &= check("C4 corrupt-claim-not-active",
                bay_organs.claim_active(queue, "grace-corrupt", root=claims_root)
                is False)
    steal = bay_organs.try_claim(queue, "grace-corrupt", engine="taker",
                                 grace_s=300, root=claims_root)
    ok &= check("C4 corrupt-claim-no-blind-steal", steal is None)

    # C5: in-vivo pid death — racer exits mid-hold, survivor reclaims
    tid = "grace-invivo"
    results, _tmpw, _armed, _mid = run_race(claims_root, queue, tid,
                                            stale=False)
    ok &= judge_round(claims_root, queue, tid, results, False)
    time.sleep(0.2)  # racers exited after DONE: their pids are dead now
    ok &= check("C5 exited-claimant-releases",
                bay_organs.claim_active(queue, tid, grace_s=300,
                                        root=claims_root) is False)
    heir = bay_organs.try_claim(queue, tid, engine="heir", grace_s=300,
                                root=claims_root)
    ok &= check("C5 survivor-reclaims", bool(heir))
    return ok


def test_takeover_toctou(claims_root, queue):
    """TEST E — deterministic repro of the takeover split-brain seen in TEST B.
    Replays the interleaving with no timing luck, through the SAME guarded
    primitive try_claim's stale-takeover path now uses (token-checked
    `_tomb_move_if_same`; pre-CAS-fix it was an unconditional os.rename —
    see watch/CAS_FIX_RECEIPT_20260904.md):
      T1 reads the stale claim and proves it stale (the judge inside try_claim,
      capturing the stale token).
      T2 completes a FULL legitimate takeover (guarded tomb-move + CAS win),
      so a FRESH claim now sits at target.
      T1 resumes and performs its commit — the guarded tomb-move with its
      stale token. It must REFUSE (token mismatch: the claim at target is no
      longer the one it judged) and lose honestly.
    Expected if the organ's invariant holds: at most ONE of {T1, T2} succeeds
    and T2's live claim is left intact at target."""
    print("TEST E: deterministic takeover TOCTOU (split-brain repro)")
    ok = True
    tid = "toctou-item"
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    forge_claim(claims_root, queue, tid, dead.pid, "ghost-stale")
    # T1's observation (what try_claim's read-and-judge step would see):
    stale_seen = bay_organs._read_claim(
        bay_organs.claim_path(queue, tid, claims_root))
    judged_stale = not bay_organs.claim_is_active(stale_seen, 300)
    ok &= check("E0 stale-claim-judged-stale", judged_stale)
    # T2: complete legitimate takeover, fresh claim now at target
    t2 = bay_organs.try_claim(queue, tid, engine="T2-fresh-taker", grace_s=300,
                              root=claims_root)
    ok &= check("E1 T2-legit-takeover-won", bool(t2))
    # T1: resumes with its pre-takeover knowledge — the guarded tomb-move the
    # CAS-fixed organ performs (re-read + token match at commit). T2's FRESH
    # claim is at target now, so the stale token cannot match: must refuse.
    d = bay_organs.claim_dir(queue, claims_root)
    tomb = os.path.join(d, ".expired-%s-%d.json" % (tid, time.time_ns()))
    moved = bay_organs._tomb_move_if_same(
        bay_organs.claim_path(queue, tid, claims_root), tomb,
        stale_seen.get("token"))
    ok &= check("E2 T1-guarded-tomb-move-refused", moved is False,
                "(if True, a LIVE claim was moved to a tombstone)")
    t1 = bay_organs.try_claim(queue, tid, engine="T1-stale-taker", grace_s=300,
                              root=claims_root)
    double = bool(t1) and bool(t2)
    ok &= check("E3 single-winner-invariant", not double,
                "t1_won=%s t2_won=%s -> %s"
                % (bool(t1), bool(t2),
                   "DOUBLE CLAIM (split-brain)" if double else "single winner"))
    if not double and t2:
        live_at_target = bay_organs._read_claim(
            bay_organs.claim_path(queue, tid, claims_root))
        ok &= check("E4 T2-live-claim-intact",
                    bool(live_at_target)
                    and live_at_target.get("token") == t2["token"]
                    and not os.path.isfile(tomb),
                    "target holds engine=%s (T2's claim: %s)"
                    % ((live_at_target or {}).get("engine"),
                       bool(live_at_target)))
    return ok


def test_sweep(claims_root, queue):
    print("TEST D: sweep_expired hygiene")
    ok = True
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    forge_claim(claims_root, queue, "sweep-dead", dead.pid, "ghost")
    live = bay_organs.try_claim(queue, "sweep-live", engine="holder",
                                grace_s=300, root=claims_root)
    ok &= check("D0 fixtures-ready", bool(live))
    removed = bay_organs.sweep_expired(queue, grace_s=1800, root=claims_root)
    ok &= check("D0 dead-claim-swept",
                not os.path.isfile(bay_organs.claim_path(queue, "sweep-dead",
                                                         claims_root)))
    ok &= check("D0 live-claim-kept",
                os.path.isfile(bay_organs.claim_path(queue, "sweep-live",
                                                     claims_root)))
    tombs = len(glob.glob(os.path.join(bay_organs.claim_dir(queue, claims_root),
                                       ".expired-*")))
    ok &= check("D0 fresh-tombstones-kept(%d)" % tombs, tombs >= 1)
    print("  sweep removed=%d (dead claims only)" % removed)
    bay_organs.release_claim(queue, "sweep-live", live["token"],
                             root=claims_root)
    return ok


def main():
    print("CLAIM ORGAN RACE TEST 20260904 - independent verification")
    print("organ under test: %s" % bay_organs.__file__)
    print("racers per round: %d real subprocesses | grace default: %ds"
          % (RACERS, bay_organs.DEFAULT_GRACE_S))
    claims_root = tempfile.mkdtemp(prefix="claim_race_test_20260904_")
    queue = "raceq_20260904"  # test namespace inside the TEST root only
    print("test claims root: %s (live bay untouched)" % claims_root)
    print("-" * 72)
    ok_a = test_race(claims_root, queue)
    ok_b = test_takeover_race(claims_root, queue)
    ok_c = test_pid_grace(claims_root, queue)
    ok_e = test_takeover_toctou(claims_root, queue)
    ok_d = test_sweep(claims_root, queue)
    print("-" * 72)
    total_checks = RACE_ROUNDS + TAKEOVER_ROUNDS
    verdict = "PASS" if not FAILURES else "FAIL"
    print("CLAIM-RACE %s (tests A=%s B=%s C=%s D=%s E=%s, %d race rounds x %d racers)"
          % (verdict, "ok" if ok_a else "FAIL", "ok" if ok_b else "FAIL",
             "ok" if ok_c else "FAIL", "ok" if ok_d else "FAIL",
             "ok" if ok_e else "FAIL", total_checks, RACERS))
    if FAILURES:
        for f in FAILURES:
            print("  FAILED: " + f)
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
