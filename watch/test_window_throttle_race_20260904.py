#!/usr/bin/env python3
"""4-way contention race test for mag/window_throttle.py — 2026-09-04, builder lane.

Model: watch/CLAIM_ORGAN_RACE_TEST_20260904.py (the harness that caught the
claim organ's FINDING 1 split-brain). This one races the WINDOW THROTTLE organ
the same way: REAL subprocesses (not threads), READY-file arming + GO-file gate
(sub-ms skew), every byte asserted.

All claim state lives in a tempfile.mkdtemp root passed as root= to every call.
The live watch/windows/ root is NEVER touched (no default-root call anywhere).

Tests:
  A  fresh race        4 procs x 10 rounds, same window -> exactly 1 winner,
                       3 clean losers, claim file == winner, 0 tmp litter
  B  takeover race     forged EXPIRED claim; 4 procs x 4 rounds (dead-pid and
                       live-pid flavors) -> exactly 1 winner, no unexpired
                       claim ever tombed
  B2 lease law         (regression from harness run 1) dead-pid UNEXPIRED
                       claim -> 4 racers all LOSE: the lease outlives the
                       claiming process (short-lived CLI claimants)
  C  release guard     wrong token refused (file kept); right token releases
  D  live primary      fresh unexpired claim held; 4 racers -> 0 winners
  E  dead/expired      dead-pid UNEXPIRED lease HOLDS (racer loses);
                       expired lease taken by a single racer
  F  sweep hygiene     expired claim + old tmp/tomb + old unreadable swept;
                       unexpired claims (any pid) + fresh unreadable kept

Run-1 receipt: the first run FAILED (2-3 winners/round) because the organ
inherited bay_organs' pid-death-release; racer children claim and exit in
milliseconds, so every claim read stale and got stolen. Fix = LEASE LAW
(expiry-only; see mag/window_throttle.py docstring); B2 is its regression
test. Re-run: python watch/test_window_throttle_race_20260904.py (exit 0 = PASS)
stdlib only, $0, no LLM calls.
"""

import json
import os
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
import mag.window_throttle as wt  # noqa: E402

PY = sys.executable
HARNESS = os.path.abspath(__file__)

FAILURES = []
CHECKS = [0]


def check(cond, msg):
    CHECKS[0] += 1
    if not cond:
        FAILURES.append(msg)
        print("  FAIL: %s" % msg)
    return cond


def child_cmd(root, window, holder, purpose, ready, go, result, ttl):
    return [PY, HARNESS, "--child", "--root", root, "--window", window,
            "--holder", holder, "--purpose", purpose, "--ready", ready,
            "--go", go, "--result", result, "--ttl", str(ttl)]


def run_racers(root, window, holders, ttl=60, timeout=60):
    """Spawn len(holders) real subprocesses gated on one GO file; return their
    result dicts (won/token/pid) or None entries for crashed children."""
    d = tempfile.mkdtemp(prefix="wt_racers_", dir=root)
    go = os.path.join(d, "GO")
    ready_files, result_files, procs = [], [], []
    for i, h in enumerate(holders):
        ready = os.path.join(d, "ready_%d" % i)
        result = os.path.join(d, "result_%d.json" % i)
        ready_files.append(ready)
        result_files.append(result)
        procs.append(subprocess.Popen(
            child_cmd(root, window, h, "race", ready, go, result, ttl),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    deadline = time.time() + 10
    while not all(os.path.exists(r) for r in ready_files):
        if time.time() > deadline:
            break
        time.sleep(0.005)
    with open(go, "w") as f:
        f.write("1")
    for p in procs:
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
    out = []
    for rf in result_files:
        try:
            with open(rf, "r", encoding="utf-8") as f:
                out.append(json.load(f))
        except (OSError, ValueError):
            out.append(None)
    return out


def _dead_pid():
    p = subprocess.Popen([PY, "-c", "pass"])
    p.wait(timeout=30)
    return p.pid


def forge(root, window, pid, expires_epoch, token="forged-token"):
    """Write a claim file by hand (the 'other seat' that died or aged out)."""
    path = wt.window_path(window, root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    claim = {"schema": wt.SCHEMA, "window": window, "holder": "the_old_seat",
             "purpose": "forged", "pid": pid, "ts": wt.now_iso(),
             "ttl_s": 3600,
             "expires_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                         time.gmtime(expires_epoch)),
             "token": token}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(claim, f)
    return claim


def litter(root, name, age_s):
    p = os.path.join(root, name)
    with open(p, "w") as f:
        f.write("x")
    past = time.time() - age_s
    os.utime(p, (past, past))
    return p


def main():
    root = tempfile.mkdtemp(prefix="window_throttle_race_20260904_")
    print("claims root: %s" % root)
    window = "night_window"

    # ── TEST A: fresh race, 4 real subprocesses x 10 rounds ──────────
    print("TEST A — fresh race (4 procs x 10 rounds)")
    for rnd in range(10):
        holders = ["seat_%d_r%d" % (i, rnd) for i in range(4)]
        results = run_racers(root, window, holders)
        wins = [r for r in results if r and r.get("won")]
        crashes = [r for r in results if r is None]
        check(len(crashes) == 0, "A rnd %d: crashed children %d" % (rnd, len(crashes)))
        check(len(wins) == 1, "A rnd %d: winners=%d (want 1) results=%s"
              % (rnd, len(wins), results))
        losers = [r for r in results if r and not r.get("won")]
        check(len(losers) == 3, "A rnd %d: clean losers=%d (want 3)" % (rnd, len(losers)))
        if len(wins) != 1:
            continue
        w = wins[0]
        c = wt._read_claim(wt.window_path(window, root))
        check(c is not None, "A rnd %d: claim file missing" % rnd)
        if c:
            check(c.get("token") == w.get("token"),
                  "A rnd %d: file token != winner token" % rnd)
            check(c.get("pid") == w.get("pid"),
                  "A rnd %d: file pid %r != winner pid %r" % (rnd, c.get("pid"), w.get("pid")))
            check(c.get("holder") == w.get("holder"),
                  "A rnd %d: file holder != winner" % rnd)
            check(wt.claim_is_active(c), "A rnd %d: winner claim not active" % rnd)
        st = wt.status(window, root=root)["windows"][window]
        check(st.get("state") == "held_active", "A rnd %d: status=%r" % (rnd, st.get("state")))
        tmps = [n for n in os.listdir(root) if n.startswith(".tmp-")]
        check(len(tmps) == 0, "A rnd %d: tmp litter %r" % (rnd, tmps))
        ok = wt.release(window, w["token"], root=root)
        check(ok, "A rnd %d: winner release failed" % rnd)
    print("  rounds done")

    # ── TEST B: takeover race on a forged EXPIRED claim ──────────────
    print("TEST B — takeover race (4 procs x 4 rounds, expired leases)")
    dead = _dead_pid()
    for rnd in range(4):
        if rnd < 2:
            forge(root, window, dead, time.time() - 10,
                  token="stale-dead-%d" % rnd)          # dead pid + expired ts
        else:
            forge(root, window, os.getpid(), time.time() - 10,
                  token="stale-exp-%d" % rnd)           # live pid + expired ts
        holders = ["taker_%d_r%d" % (i, rnd) for i in range(4)]
        results = run_racers(root, window, holders)
        wins = [r for r in results if r and r.get("won")]
        check(len(wins) == 1, "B rnd %d: winners=%d (want 1) results=%s"
              % (rnd, len(wins), results))
        c = wt._read_claim(wt.window_path(window, root))
        if len(wins) == 1 and c:
            check(c.get("token") == wins[0]["token"],
                  "B rnd %d: file token != takeover winner" % rnd)
            check(wt.claim_is_active(c), "B rnd %d: new claim not active" % rnd)
        # no live claim was tombed: every tombstone must hold the FORGED token
        tombs = [n for n in os.listdir(root) if n.startswith(".expired-")]
        for t in tombs:
            tc = wt._read_claim(os.path.join(root, t))
            check(tc is not None and str(tc.get("token", "")).startswith("stale-"),
                  "B rnd %d: tomb %s holds a LIVE claim (token=%r)"
                  % (rnd, t, tc and tc.get("token")))
        wt.release(window, wins[0]["token"], root=root) if len(wins) == 1 else None
        for t in tombs:
            os.remove(os.path.join(root, t))
    print("  rounds done")

    # ── TEST B2 (regression from run 1): the lease outlives the claimant ──
    print("TEST B2 — dead-pid UNEXPIRED lease is NOT stealable (lease law)")
    forge(root, window, dead, time.time() + 3600, token="b2-held")
    results = run_racers(root, window, ["thief_%d" % i for i in range(4)], ttl=60)
    wins = [r for r in results if r and r.get("won")]
    check(len(wins) == 0,
          "B2: %d racers stole a dead-pid UNEXPIRED lease (run-1 bug alive)" % len(wins))
    check(len([r for r in results if r and not r.get("won")]) == 4,
          "B2: not all racers lost cleanly")
    c2 = wt._read_claim(wt.window_path(window, root))
    check(c2 is not None and c2.get("token") == "b2-held",
          "B2: held claim file changed under attack")
    st = wt.status(window, root=root)["windows"][window]
    check(st.get("state") == "held_active",
          "B2: dead-pid unexpired claim state=%r (want held_active)" % st.get("state"))
    check(st.get("pid_alive") is False,
          "B2: status should report pid_alive=False (informational)")
    os.remove(wt.window_path(window, root))

    # ── TEST C: release guard ────────────────────────────────────────
    print("TEST C — release discipline")
    c = wt.claim(window, "builder", "test C", ttl_s=60, root=root)
    check(c is not None, "C: parent claim failed on free window")
    check(wt.release(window, "bogus-token", root=root) is False,
          "C: wrong token released the window")
    check(os.path.isfile(wt.window_path(window, root)),
          "C: file vanished on refused release")
    check(wt.release(window, c["token"], root=root) is True,
          "C: right token failed to release")
    check(not os.path.isfile(wt.window_path(window, root)),
          "C: file still present after release")
    st = wt.status(window, root=root)["windows"][window]
    check(st.get("state") == "free", "C: status after release=%r" % st.get("state"))

    # ── TEST D: a fresh LIVE primary is never stolen ─────────────────
    print("TEST D — live primary protection (4 racers)")
    c = wt.claim(window, "the_primary", "night burns", ttl_s=600, root=root)
    check(c is not None, "D: parent claim failed")
    results = run_racers(root, window, ["racer_%d" % i for i in range(4)], ttl=60)
    wins = [r for r in results if r and r.get("won")]
    check(len(wins) == 0, "D: %d racers stole a LIVE primary (want 0)" % len(wins))
    check(len([r for r in results if r and not r.get("won")]) == 4,
          "D: not all racers lost cleanly")
    c2 = wt._read_claim(wt.window_path(window, root))
    check(c2 and c2.get("token") == c["token"],
          "D: live claim file changed under contention")
    st = wt.status(window, root=root)["windows"][window]
    check(st.get("holder") == "the_primary", "D: status holder=%r" % st.get("holder"))
    wt.release(window, c["token"], root=root)

    # ── TEST E: dead-holder lease HOLDS; expired lease is taken ──────
    print("TEST E — dead-holder lease HOLDS; expired lease is taken")
    forge(root, window, dead, time.time() + 3600, token="e1-dead")
    r = run_racers(root, window, ["lonely_taker_1"], ttl=60)
    check(bool(r and r[0] and not r[0].get("won")),
          "E: dead-pid UNEXPIRED lease was stolen (lease law broken)")
    c2 = wt._read_claim(wt.window_path(window, root))
    check(c2 is not None and c2.get("token") == "e1-dead",
          "E: dead-holder claim file changed")
    forge(root, window, os.getpid(), time.time() - 1, token="e2-expired")
    r = run_racers(root, window, ["lonely_taker_2"], ttl=60)
    check(bool(r and r[0] and r[0].get("won")),
          "E: expired claim not taken by single racer")
    if r and r[0] and r[0].get("won"):
        wt.release(window, r[0]["token"], root=root)

    # ── TEST F: sweep hygiene ────────────────────────────────────────
    print("TEST F — sweep hygiene")
    live = wt.claim(window, "live_seat", "must survive sweep", ttl_s=600, root=root)
    check(live is not None, "F: live claim failed")
    forge(root, "dead_window", dead, time.time() + 3600, token="f-dead")
    forge(root, "expired_window", os.getpid(), time.time() - 10, token="f-exp")
    litter(root, ".tmp-crash.json", age_s=400)
    litter(root, ".expired-old.json", age_s=4000)
    unreadable = litter(root, "unreadable_window.json", age_s=400)
    fresh_unreadable = os.path.join(root, "fresh_unreadable_window.json")
    with open(fresh_unreadable, "w") as f:
        f.write("{not json")
    removed = wt.sweep(root=root)
    check(os.path.isfile(wt.window_path("dead_window", root)),
          "F: UNEXPIRED dead-pid claim swept (lease law broken in sweep)")
    check(not os.path.isfile(wt.window_path("expired_window", root)),
          "F: expired claim not swept")
    check(os.path.isfile(wt.window_path(window, root)),
          "F: LIVE claim was swept")
    check(wt._read_claim(wt.window_path(window, root))["token"] == live["token"],
          "F: live claim token changed")
    check(not os.path.isfile(os.path.join(root, ".tmp-crash.json")),
          "F: old tmp debris not swept")
    check(not os.path.isfile(os.path.join(root, ".expired-old.json")),
          "F: old tombstone not swept")
    check(not os.path.isfile(unreadable), "F: old unreadable claim not swept")
    check(os.path.isfile(fresh_unreadable),
          "F: FRESH unreadable swept too early (must wait out UNREADABLE_S)")
    wt.release(window, live["token"], root=root)

    # ── verdict ──────────────────────────────────────────────────────
    print()
    print("checks: %d, failures: %d" % (CHECKS[0], len(FAILURES)))
    if FAILURES:
        for f in FAILURES:
            print("  FAILED: %s" % f)
        print("VERDICT: FAIL")
        return 1
    print("VERDICT: PASS")
    return 0


def _child(args):
    """Racer child: arm READY, wait for GO, fire one claim, report the bytes."""
    open(args.ready, "w").write("1")
    deadline = time.time() + 30
    while not os.path.exists(args.go):
        if time.time() > deadline:
            break
        time.sleep(0.001)
    c = wt.claim(args.window, args.holder, args.purpose,
                 ttl_s=args.ttl, root=args.root)
    out = {"holder": args.holder, "pid": os.getpid(),
           "won": c is not None,
           "token": (c or {}).get("token"),
           "claim_pid": (c or {}).get("pid")}
    with open(args.result, "w", encoding="utf-8") as f:
        json.dump(out, f)
    sys.exit(0 if c is not None else 3)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--child", action="store_true")
    ap.add_argument("--root"); ap.add_argument("--window")
    ap.add_argument("--holder"); ap.add_argument("--purpose")
    ap.add_argument("--ready"); ap.add_argument("--go"); ap.add_argument("--result")
    ap.add_argument("--ttl", type=int, default=60)
    a = ap.parse_args()
    if a.child:
        _child(a)
    sys.exit(main())
