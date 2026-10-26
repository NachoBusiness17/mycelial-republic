#!/usr/bin/env python3
"""test_claim_repair_20260905.py — corruption harness for the claim organ's
FINDING 2 (watch/CLAIM_ORGAN_RACE_TEST_20260904.md): corrupt claim files are
unsweepable permanent locks. Exercises mag/claim_repair.py (which reuses
mag/bay_organs.py primitives; the organ itself is UNMODIFIED).

All state in TEMP dirs — the live claims store watch/bay/claims, the real
queues and engines are never touched. stdlib only, $0, no LLM calls.

  TEST P  PRE-REPAIR PROOFS (the bug, live on the unmodified organ):
          P1 unparseable claim -> sweep skips it (file persists) and
             try_claim loses forever (stranded, proven twice)
          P2 valid-JSON-non-object claim -> the sweeper CHOKEs
             (AttributeError inside claim_is_active) and a claimant CRASHES
          P3 claim missing ts with a LIVE holder -> organ judges it stale and
             a rival try_claim STEALS it (double-execution hazard)
          P4 stale parseable claim -> sweep blind-DELETES it: no quarantine,
             no backup, evidence destroyed
  TEST D  REPAIR DRY-RUN — classifies all fixtures, moves nothing, store
          byte-identical, would-* receipt rows written
  TEST A  REPAIR APPLY — each fixture quarantined exactly once with evidence
          preserved (sha-verified) + full-store backup taken first;
          re-issue fired ONLY for the verifiably-not-done tranche (try_claim
          win + release proof); done / parked-thin / unverifiable refused;
          fresh tombstone and live claim untouched (FINDING 1 invariant kept)
  TEST I  IDEMPOTENCY — second apply run: 0 repairs, store byte-identical
  TEST R  REGRESSION — the EXISTING split-brain harness
          (test_claim_race_20260904.py) still passes 4/4 unmodified

Run: python watch/test_claim_repair_20260905.py
Exit 0 = FINDING 2 closed at v0.
"""

import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from mag import bay_organs  # noqa: E402
from mag import claim_repair  # noqa: E402

QUEUE = "repairq_20260905"
GRACE = 300  # tight window, mirrors the race harness

FAILURES = []


def check(name, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           (" - " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name + ((" - " + detail) if detail else ""))
    return ok


def dead_pid():
    p = subprocess.Popen([sys.executable, "-c", "pass"])
    p.wait()
    return p.pid


def write_raw(claims_root, queue, name, raw, age_s=None):
    d = bay_organs.claim_dir(queue, claims_root)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(raw)
    if age_s is not None:
        t = time.time() - age_s
        os.utime(p, (t, t))
    return p


def write_claim(claims_root, queue, task_id, obj, age_s=None):
    return write_raw(claims_root, queue, task_id + ".json",
                     json.dumps(obj), age_s=age_s)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def store_snapshot(root):
    snap = {}
    for dirpath, _dirs, files in os.walk(root):
        for n in files:
            p = os.path.join(dirpath, n)
            snap[os.path.relpath(p, root)] = sha(p)
    return snap


def old_ts(seconds):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - seconds))


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------

def build_world():
    """Temp claims store + temp work manifests (queue rows, churn state)."""
    claims_root = tempfile.mkdtemp(prefix="claim_repair_test_20260905_")
    repair_root = claims_root + "-repair"   # sibling: same volume, outside store
    work = tempfile.mkdtemp(prefix="claim_repair_work_20260905_")
    outd = tempfile.mkdtemp(prefix="claim_repair_out_20260905_")
    os.environ["CLAIM_REPAIR_QUEUE_DIR"] = work
    os.environ["CLAIM_REPAIR_STATE"] = os.path.join(work, "churn_state.json")

    # work manifests: r1 not-done, r2 done (substantive), r3 parked-THIN,
    # r4 has NO row (unverifiable)
    out = {"r1": os.path.join(outd, "r1_out.md"),
           "r2": os.path.join(outd, "r2_out.md"),
           "r3": os.path.join(outd, "r3_out.md")}
    rows = [{"id": "r1", "title": "t1", "output": out["r1"]},
            {"id": "r2", "title": "t2", "output": out["r2"]},
            {"id": "r3", "title": "t3", "output": out["r3"]}]
    with open(os.path.join(work, QUEUE + ".jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    with open(out["r2"], "w", encoding="utf-8") as f:
        f.write("# t2\n\nReal substantive work product, 340 chars of it. " * 5)
    with open(out["r3"], "w", encoding="utf-8") as f:
        f.write("# t3\n\nTHIN: failed substance gate twice. Morning retry advised.\n")
    with open(os.environ["CLAIM_REPAIR_STATE"], "w", encoding="utf-8") as f:
        json.dump({"parked": {}}, f)
    return claims_root, repair_root, work, out


def build_fixtures(claims_root):
    """The four corruption classes + the two things repair must NEVER touch."""
    dp = dead_pid()
    f = {}
    # f1 unparseable (bad JSON), work not-done
    f["f1"] = write_raw(claims_root, QUEUE, "r1.json", '{"queue": "repairq_2026')
    # f2 valid JSON, NOT an object (sweeper choke shape), work done
    f["f2"] = write_raw(claims_root, QUEUE, "r2.json", "[1, 2, 3]")
    # f3 missing-fields (no token), dead claimant, work parked-THIN
    f["f3"] = write_claim(claims_root, QUEUE, "r3",
                          {"queue": QUEUE, "task": "r3", "engine": "ghost",
                           "slot": "s", "pid": dp, "ts": old_ts(5),
                           "grace_s": GRACE})
    # f4 expired-lease (full fields, lease long past), no queue row
    f["f4"] = write_claim(claims_root, QUEUE, "r4",
                          {"queue": QUEUE, "task": "r4", "engine": "ghost",
                           "slot": "s", "pid": dp, "ts": old_ts(GRACE + 120),
                           "grace_s": GRACE, "token": "tok-r4"})
    # f5 aged corrupt tombstone, f6 aged well-formed WRONG-token tombstone,
    # f7 FRESH well-formed tombstone (the FINDING 1 CAS fix needs these kept)
    f["f5"] = write_raw(claims_root, QUEUE, ".expired-tomba-1-2.json",
                        "{oops not json", age_s=GRACE + 60)
    f["f6"] = write_raw(claims_root, QUEUE, ".expired-tombb-3-4.json",
                        json.dumps({"queue": QUEUE, "task": "tombb",
                                    "token": "WRONG-TOKEN", "pid": dp,
                                    "ts": old_ts(GRACE + 60)}),
                        age_s=GRACE + 60)
    f["f7"] = write_raw(claims_root, QUEUE, ".expired-tombfresh-5-6.json",
                        json.dumps({"queue": QUEUE, "task": "tombfresh",
                                    "token": "tok-fresh", "pid": dp,
                                    "ts": old_ts(1)}), age_s=1)
    # f8 a FRESH LIVE claim (this process) — must be skipped, never touched
    live = bay_organs.try_claim(QUEUE, "live-held", engine="repair-harness",
                                slot="harness", grace_s=GRACE, root=claims_root)
    f["f8_path"] = bay_organs.claim_path(QUEUE, "live-held", claims_root)
    f["f8_token"] = live["token"] if live else None
    return f


# --------------------------------------------------------------------------
# TEST P: pre-repair proofs against the UNMODIFIED organ
# --------------------------------------------------------------------------

def test_pre_repair(claims_root):
    print("TEST P: pre-repair proofs - the organ strands/chokes/steals/eats")
    ok = True

    # P1: unparseable claim -> sweep skips it, try_claim loses forever
    q = "strandq"
    write_raw(claims_root, q, "strand-item.json", '{"task": "strand-item"')
    removed = bay_organs.sweep_expired(q, grace_s=GRACE, root=claims_root)
    p = bay_organs.claim_path(q, "strand-item", claims_root)
    ok &= check("P1 corrupt-claim-unsweepable", os.path.isfile(p),
                "sweep removed=%d but file persisted" % removed)
    t1 = bay_organs.try_claim(q, "strand-item", engine="victim-1",
                              grace_s=GRACE, root=claims_root)
    t2 = bay_organs.try_claim(q, "strand-item", engine="victim-2",
                              grace_s=GRACE, root=claims_root)
    ok &= check("P1 try_claim-loses-forever", t1 is None and t2 is None,
                "two independent claimants both stranded")

    # P2: valid JSON non-object -> sweeper CHOKEs, claimant CRASHES
    q = "chokeq"
    write_raw(claims_root, q, "choke-item.json", "[1, 2, 3]")
    raised = None
    try:
        bay_organs.sweep_expired(q, grace_s=GRACE, root=claims_root)
    except Exception as e:
        raised = e
    ok &= check("P2 sweeper-chokes-on-non-object", raised is not None,
                "sweep_expired raised %s" % type(raised).__name__)
    raised = None
    try:
        bay_organs.try_claim(q, "choke-item", engine="victim",
                             grace_s=GRACE, root=claims_root)
    except Exception as e:
        raised = e
    ok &= check("P2 claimant-crashes-on-non-object", raised is not None,
                "try_claim raised %s" % type(raised).__name__)

    # P3: missing-ts claim with a LIVE holder -> organ steals it
    q = "stealq"
    write_claim(claims_root, q, "steal-item",
                {"queue": q, "task": "steal-item", "engine": "live-worker",
                 "slot": "s", "pid": os.getpid(), "grace_s": GRACE,
                 "token": "tok-live-worker"})
    steal = bay_organs.try_claim(q, "steal-item", engine="rival",
                                 grace_s=GRACE, root=claims_root)
    ok &= check("P3 organ-steals-from-live-holder", steal is not None,
                "half-write (ts lost) lets a rival take a LIVE worker's item"
                if steal else "organ refused (already hardened?)")

    # P4: stale parseable claim -> sweep blind-deletes, evidence gone
    q = "eatq"
    dp = dead_pid()
    write_claim(claims_root, q, "eaten-item",
                {"queue": q, "task": "eaten-item", "engine": "ghost",
                 "slot": "s", "pid": dp, "ts": old_ts(GRACE + 60),
                 "grace_s": GRACE, "token": "tok-eaten"})
    p = bay_organs.claim_path(q, "eaten-item", claims_root)
    before = sha(p)
    bay_organs.sweep_expired(q, grace_s=GRACE, root=claims_root)
    leftovers = glob.glob(os.path.join(bay_organs.claim_dir(q, claims_root),
                                       "*eaten*"))
    ok &= check("P4 sweep-blind-deletes-evidence",
                not os.path.isfile(p) and not leftovers,
                "stale claim destroyed, sha %s unrecoverable" % before[:12])
    return ok


# --------------------------------------------------------------------------
# TEST D: dry-run moves nothing
# --------------------------------------------------------------------------

def test_dry_run(claims_root, repair_root):
    print("TEST D: repair dry-run - classify all, move nothing")
    ok = True
    before = store_snapshot(claims_root)
    s = claim_repair.repair(root=claims_root, apply=False, queues=[QUEUE],
                            repair_root=repair_root, grace_s=GRACE)
    ok &= check("D dry-run-mode", s["mode"] == "dry-run")
    ok &= check("D all-six-repairable-found", s["to_repair"] == 6,
                "to_repair=%d by_class=%s" % (s["to_repair"], s["by_class"]))
    ok &= check("D classes-split-correctly",
                s["by_class"].get("unparseable") == 2
                and s["by_class"].get("missing-fields") == 1
                and s["by_class"].get("expired-lease") == 1
                and s["by_class"].get("tomb-mismatch") == 2,
                "by_class=%s" % s["by_class"])
    ok &= check("D nothing-moved", before == store_snapshot(claims_root))
    ok &= check("D no-backup-on-dry-run", s["backup"] is None)
    ok &= check("D receipt-written", os.path.isfile(s["receipt"]))
    rows = [json.loads(l) for l in open(s["receipt"], encoding="utf-8")
            if l.strip()]
    would = [r for r in rows if r.get("mode") == "dry-run"
             and r.get("kind") == "item"]
    ok &= check("D would-quarantine-rows", len(would) == 6,
                "rows=%d" % len(would))
    ws = {r["task"]: r.get("work_state") for r in would if r.get("task")}
    ok &= check("D work-states-verified",
                ws.get("r1") == "not-done" and ws.get("r2") == "done"
                and ws.get("r3") == "parked-thin"
                and ws.get("r4") == "unverifiable",
                "work_states=%s" % ws)
    return ok


# --------------------------------------------------------------------------
# TEST A: apply quarantines + re-issues exactly right
# --------------------------------------------------------------------------

def test_apply(claims_root, repair_root, fixtures):
    print("TEST A: repair apply - quarantine with evidence, re-issue once")
    ok = True
    d = bay_organs.claim_dir(QUEUE, claims_root)
    f = fixtures
    # capture pre-apply evidence hashes: after apply the originals are gone
    pre_sha = {k: sha(v) for k, v in f.items()
               if isinstance(v, str) and k != "f8_path"
               and os.path.isfile(v)}

    s = claim_repair.repair(root=claims_root, apply=True, queues=[QUEUE],
                            repair_root=repair_root, grace_s=GRACE)
    ok &= check("A apply-mode", s["mode"] == "apply")
    ok &= check("A backup-first-taken", s["backup"]
                and os.path.isdir(os.path.join(s["backup"], "claims", QUEUE)))
    ok &= check("A backup-holds-pre-state",
                os.path.isfile(os.path.join(s["backup"], "claims", QUEUE,
                                            "r1.json"))
                and sha(os.path.join(s["backup"], "claims", QUEUE,
                                     "r1.json")) == pre_sha["f1"],
                "backup copy sha-matches the original corrupt file")

    ok &= check("A six-quarantined", s["quarantined"] == 6)
    ok &= check("A one-reissued", s["reissued"] == 1,
                "reissued=%d refused=%d" % (s["reissued"],
                                            s["reissue_refused"]))
    ok &= check("A exactly-one-reissue-target",
                s["reissued"] == 1 and s["reissue_refused"] == 3,
                "r1 not-done re-issued; r2 done + r3 parked-thin + r4 "
                "unverifiable refused")

    qdir = os.path.join(repair_root, "quarantine")
    quarmed = os.listdir(qdir)
    ok &= check("A quarantine-holds-six", len(quarmed) == 6,
                "files=%d" % len(quarmed))
    names = {k: os.path.basename(v) for k, v in f.items()
             if isinstance(v, str) and k != "f8_path" and k != "f7"}
    qmap = {}
    for n in quarmed:
        for key, base in names.items():
            if n.endswith("-" + base):
                qmap[key] = os.path.join(qdir, n)
    ok &= check("A all-corrupt-evidence-preserved",
                len(qmap) == 6, "matched=%s" % sorted(qmap))
    for key in ("f1", "f2", "f3", "f4", "f5", "f6"):
        if key in qmap:
            ok &= check("A %s-sha-preserved" % key,
                        sha(qmap[key]) == pre_sha[key])
        else:
            ok &= check("A %s-quarantined" % key, False, "missing from quarantine")

    # store is clean: all six gone from the claims dir
    for key in ("f1", "f2", "f3", "f4", "f5", "f6"):
        ok &= check("A %s-gone-from-store" % key, not os.path.isfile(f[key]))

    # the two NEVER-TOUCH surfaces
    ok &= check("A fresh-tombstone-kept",
                os.path.isfile(f["f7"]),
                "FINDING 1 CAS invariant: fresh tombs are transient state")
    fc = bay_organs._read_claim(f["f8_path"])
    ok &= check("A live-claim-untouched",
                bool(fc) and fc.get("token") == f["f8_token"],
                "fresh live claim still holds the item, token unchanged")

    # re-issue proof: r1 is FREE for the fleet (repair claimed+released it)
    ok &= check("A r1-open-for-fleet",
                not os.path.isfile(bay_organs.claim_path(QUEUE, "r1",
                                                         claims_root)))
    heir = bay_organs.try_claim(QUEUE, "r1", engine="post-repair-heir",
                                grace_s=GRACE, root=claims_root)
    ok &= check("A r1-claimable-again", bool(heir))
    if heir:
        bay_organs.release_claim(QUEUE, "r1", heir["token"], root=claims_root)

    # receipt rows: one item row per repair, typed
    rows = [json.loads(l) for l in open(s["receipt"], encoding="utf-8")
            if l.strip()]
    items = [r for r in rows if r.get("kind") == "item"
             and r.get("run_id") == s["run_id"]]
    ok &= check("A receipt-item-rows", len(items) == 6)
    r1row = [r for r in items if r.get("task") == "r1"]
    ok &= check("A r1-receipt-reissued",
                bool(r1row) and r1row[0].get("reissued") is True
                and "released" in (r1row[0].get("reissue_note") or ""),
                "reissue proof recorded: %s"
                % (r1row[0].get("reissue_note") if r1row else "-"))
    cls_by_task = {r.get("task"): r.get("cls") for r in items}
    tombs = [r for r in items if r.get("cls") == "tomb-mismatch"]
    ok &= check("A receipt-classes-typed",
                cls_by_task.get("r1") == "unparseable"
                and cls_by_task.get("r2") == "unparseable"
                and len(tombs) == 2
                and cls_by_task.get("r4") == "expired-lease"
                and cls_by_task.get("r3") == "missing-fields",
                "cls_by_task=%s" % cls_by_task)
    return ok


# --------------------------------------------------------------------------
# TEST I: idempotency
# --------------------------------------------------------------------------

def test_idempotent(claims_root, repair_root):
    print("TEST I: idempotency - second apply run changes nothing")
    ok = True
    before = store_snapshot(claims_root)
    s = claim_repair.repair(root=claims_root, apply=True, queues=[QUEUE],
                            repair_root=repair_root, grace_s=GRACE)
    ok &= check("I zero-repairs-second-run",
                s["to_repair"] == 0 and s["quarantined"] == 0
                and s["reissued"] == 0,
                "to_repair=%d quarantined=%d" % (s["to_repair"],
                                                 s["quarantined"]))
    ok &= check("I store-byte-identical",
                before == store_snapshot(claims_root))
    ok &= check("I no-second-backup", s["backup"] is None)
    return ok


# --------------------------------------------------------------------------
# TEST R: regression — the existing split-brain harness must still pass
# --------------------------------------------------------------------------

def test_regression():
    print("TEST R: regression - existing claim-race harness (unmodified)")
    r = subprocess.run([sys.executable, os.path.join(HERE,
                       "test_claim_race_20260904.py")],
                       capture_output=True, text=True, timeout=600)
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    ok = check("R race-harness-exit-0", r.returncode == 0,
               "exit=%d %s" % (r.returncode, tail[0][:120]))
    ok &= check("R race-harness-verdict-PASS", "CLAIM-RACE PASS" in r.stdout,
                (r.stdout or "")[-200:])
    return ok


def main():
    print("CLAIM REPAIR TEST 20260905 - FINDING 2 closure verification")
    print("organ under repair: %s" % bay_organs.__file__)
    print("repair module:      %s" % claim_repair.__file__)
    claims_root, repair_root, work, _out = build_world()
    print("test claims root: %s (live bay untouched)" % claims_root)
    print("-" * 72)
    fixtures = build_fixtures(claims_root)
    ok_p = test_pre_repair(claims_root)
    ok_d = test_dry_run(claims_root, repair_root)
    ok_a = test_apply(claims_root, repair_root, fixtures)
    ok_i = test_idempotent(claims_root, repair_root)
    ok_r = test_regression()
    print("-" * 72)
    verdict = "PASS" if not FAILURES else "FAIL"
    print("CLAIM-REPAIR %s (P=%s D=%s A=%s I=%s R=%s)"
          % (verdict, "ok" if ok_p else "FAIL", "ok" if ok_d else "FAIL",
             "ok" if ok_a else "FAIL", "ok" if ok_i else "FAIL",
             "ok" if ok_r else "FAIL"))
    if FAILURES:
        for x in FAILURES:
            print("  FAILED: " + x)
    # temp world cleanup is skipped on failure (evidence for triage)
    if not FAILURES:
        shutil.rmtree(claims_root, ignore_errors=True)
        shutil.rmtree(repair_root, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
