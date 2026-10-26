#!/usr/bin/env python3
"""overnight_churn v0.5.2 — RESIDENT STEERED WORKERS + GATE V2 + CLAIM ORGAN.

New in v0.5.2 (Leg-1 queue plumbing, SHERPA_ROUTE v2 + ECONOMIST_AUDIT guards):
  * CLAIM ORGAN: before dispatch the engine claims the task atomically
    (temp-write + same-volume rename, mag/bay_organs). Claimed items are
    invisible to other engines until grace expiry (BAY_CLAIM_GRACE_S, default
    30 min) or until the claimant's pid dies. Kills the double-mine class
    (sp_83204700). Rejected/blocked beats KEEP their claim: the task requeues
    only after grace — no instant-fail loops (the 737 lines/sec scar).
  * PARK IDEMPOTENCY VIA STATE, not output bytes: a parked task gets a marker
    in the state file (st["parked"]); the pending filter and maybe_park both
    honor it, so a parked task can never re-park or re-log, even if its THIN
    output file is deleted. Park logs exactly once (guard (b), live-tested via
    `--park-test`, grepped by mag/race_harness.py).
  * LOCKFILE PID: the child writes {pid, seat, ts} to its own lockfile at
    startup (CHURN_LOCK, set by the reconciler per launch; hand-launched
    engines default to watch/bay/locks/writers/hand-<queue>.lock). Writers of
    the board/queues are attributable now.
  * (carried) GATE V2, LIGHT-TO-LIGHT SHARE, contract-once, steer tails,
    env-overridable engines, sun-up stop.
"""
import json, os, subprocess, sys, time, datetime

ROOT = os.path.realpath(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from mag import bay_organs  # noqa: E402  (stdlib-only, $0 — no LLM calls)

QUEUE = os.environ.get("CHURN_QUEUE", os.path.join(ROOT, "watch", "overnight_queue.jsonl"))
BOARD = os.path.join(ROOT, "dashboard", "data", "ractor_board.jsonl")
LOG = os.environ.get("CHURN_LOG", os.path.join(ROOT, "watch", "overnight_churn.log"))
STATE = os.environ.get("CHURN_STATE", os.path.join(ROOT, "watch", "churn_state.json"))
SHARE = os.environ.get("CHURN_SHARE", os.path.join(ROOT, "watch", "bay_share.jsonl"))
LOCK = os.environ.get("CHURN_LOCK", "")  # engine lockfile (pid+seat+ts), set by reconciler
SLEEP_S = int(os.environ.get("CHURN_SLEEP", "200"))
END_HOUR = 8
SESS = os.environ.get("CHURN_SESS", "g1,g2,g3,g4").split(",")
MODEL = os.environ.get("CHURN_MODEL", "zai/glm-4.7-flash")
SEAT = os.environ.get("CHURN_SEAT", "openclaw")
RESIDENT = os.environ.get("CHURN_RESIDENT", "1") == "1"
ORGAN = os.environ.get("CHURN_ORGAN", "cage")
QUEUE_NAME = os.path.splitext(os.path.basename(QUEUE))[0]          # claim namespace
CLAIMS_ROOT = os.environ.get("CHURN_CLAIMS_ROOT", "") or None      # bay/claims default
CLAIM_GRACE_S = int(os.environ.get("BAY_CLAIM_GRACE_S", str(bay_organs.DEFAULT_GRACE_S)))
PARK_ATTEMPTS = int(os.environ.get("CHURN_PARK_ATTEMPTS", "2"))

CONTRACT = ("You are a code archaeologist (resident session; this contract persists). "
            "Each future message names one source file. For each: report under 200 words, "
            "plain text: (1) what it does in two sentences, from the code only; "
            "(2) three notable design patterns, one line each, named from the code itself "
            "- do not guess intent beyond the file; (3) any single-point-of-failure, hidden "
            "mutation of shared state, or duplicate scheduler. Do not use vocabulary from "
            "this contract when describing the code. Output only the report. "
            "Confirm by replying CONTRACT ACK.")

def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(ts() + " " + m + "\n")

def board_row(organ, kind, title, detail, status, evidence):
    row = {"organ": organ, "kind": kind, "title": title, "detail": detail[:200],
           "status": status, "evidence": evidence, "ts": ts()}
    with open(BOARD, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def tasks():
    out = []
    if not os.path.isfile(QUEUE):
        return out
    with open(QUEUE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out

def state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"contracted": [], "next_sess": 0, "attempts": {}, "parked": {}}

def save_state(s):
    # atomic overwrite (temp + same-volume replace) — the park marker and the
    # attempts ledger must never be caught half-written by a sibling engine.
    bay_organs.atomic_write_json(STATE, s, overwrite=True)

def maybe_park(t, st):
    """Park a task that exhausted its attempts. IDEMPOTENT VIA STATE MARKER:
    once st['parked'][id] exists the task is parked forever — no output-byte
    re-derivation, no re-write, no second log line (the 1.84M-line park ghost
    buried here; guard (b) demands the live test, see --park-test).
    Returns True when the task is parked (caller skips it), False to proceed."""
    if st.setdefault("parked", {}).get(t["id"]):
        return True
    if st.get("attempts", {}).get(t["id"], 0) < PARK_ATTEMPTS:
        return False
    st["parked"][t["id"]] = bay_organs.now_iso()
    save_state(st)  # marker FIRST: crash here = parked-without-file, never re-park loop
    op = os.path.join(ROOT, t["output"])
    with open(op, "w", encoding="utf-8") as f:
        f.write("# " + t["title"] + "\n\nTHIN: failed substance gate twice. Morning retry advised.\n")
    board_row(ORGAN, "task.receipt", "overnight: " + t["title"],
              "THIN after %d attempts - morning retry" % PARK_ATTEMPTS, "THIN", t["output"])
    log(t["id"] + " parked as THIN")  # exactly once per task, ever
    return True

def clean(detail):
    if detail and detail.startswith("EMBEDDED FALLBACK:"):
        return detail.split("\n", 1)[-1] if "\n" in detail else detail
    return detail

def is_boilerplate(detail):
    if not detail:
        return True
    heads = ("I'll help", "I'm sorry", "I cannot", "I can't", "EMBEDDED FALLBACK",
             "I've done everything", "It seems there are multiple issues")
    return any(detail.strip().startswith(h) for h in heads)

def dispatch(goal, sess, model=MODEL):
    tag = sess[5:] if sess.startswith("seat-") else sess
    r = subprocess.run(
        [sys.executable, "-m", "mag.seat_dispatch", "task", goal,
         "--seat", SEAT, "--tag", tag, "--model", model],
        cwd=ROOT, capture_output=True, text=True, timeout=300)
    body = r.stdout.strip()
    try:
        parsed = json.loads(body)
        return clean(parsed.get("detail") or body), parsed.get("folded", False), parsed.get("task_id", "?")
    except json.JSONDecodeError:
        return body[:1500], False, "?"

def main():
    log("churn v0.5.2 awake - sessions " + ",".join(SESS) + " on " + MODEL + " (claims + state-park)")
    # LOCKFILE PID organ: the child owns its identity — pid + seat + ts in the
    # lockfile, written by the child itself (sidesteps the launch-side path
    # scanner; makes this writer of queues/board attributable).
    lock_path_used = LOCK or os.path.join(
        ROOT, "watch", "bay", "locks", "writers", "hand-%s.lock" % QUEUE_NAME)
    try:
        bay_organs.write_writer_lock(lock_path_used, SEAT)
        log("writer lock " + lock_path_used)
    except Exception as e:
        log("writer lock FAILED (continuing, unattributed): " + str(e)[:120])
    st = state()
    st.setdefault("attempts", {})
    st.setdefault("parked", {})
    claim = None  # current {token,...} for the in-flight task
    while True:
        now = datetime.datetime.now()
        if 8 <= now.hour < 12:
            log("sun is up - stopping")
            break
        pending = []
        for t in tasks():
            if t["id"] in st["parked"]:
                continue  # parked marker lives in STATE — never re-derived from bytes
            op = os.path.join(ROOT, t["output"])
            if os.path.isfile(op):
                head = open(op, encoding="utf-8", errors="ignore").read(120)
                if "THIN:" in head:
                    continue  # belt: THIN output present (state marker is the suspenders)
                if os.path.getsize(op) >= 150:
                    continue
            if bay_organs.claim_active(QUEUE_NAME, t["id"], grace_s=CLAIM_GRACE_S, root=CLAIMS_ROOT):
                continue  # CLAIM ORGAN: held by a live engine — invisible until grace expiry
            pending.append(t)
        if not pending:
            log("queue empty - engine complete")
            break
        t = pending[min(int(os.environ.get("CHURN_PICK_OFFSET", "0")), len(pending) - 1)]
        if maybe_park(t, st):
            continue
        claim = bay_organs.try_claim(QUEUE_NAME, t["id"], engine=ORGAN, slot=SESS[0],
                                     grace_s=CLAIM_GRACE_S, root=CLAIMS_ROOT)
        if claim is None:
            log(t["id"] + " claimed elsewhere mid-pick - skipping")
            continue
        sess = SESS[st["next_sess"] % len(SESS)]
        st["next_sess"] += 1
        if sess not in st["contracted"]:
            if RESIDENT:
                log(sess + " contract turn")
                try:
                    ack, folded, tid = dispatch(CONTRACT, sess)
                except Exception as e:
                    log(sess + " contract dispatch error: " + str(e)[:120])
                    time.sleep(90)
                    break
                if not folded:
                    log(sess + " contract not folded: " + (ack or "")[:120])
                    time.sleep(90)
                    continue
            st["contracted"].append(sess)
            save_state(st)
            log(sess + " contracted" + ("" if RESIDENT else " (non-resident: contract inlined per beat)"))
        if RESIDENT:
            goal = "NEXT WING: read the file " + t["source"] + " - same report contract."
        else:
            # non-resident seats see ONE turn: task-shaped, format inline, no
            # session contract (contract preambles make agent CLIs wait for a
            # next message instead of acting — proven at the bytes tonight).
            goal = ("You are a code archaeologist. Read the file " + t["source"]
                    + " and write a report under 200 words, plain text: "
                    "(1) what it does in two sentences, from the code only; "
                    "(2) three notable design patterns, one line each, named from the code itself "
                    "- do not guess intent beyond the file; (3) any single-point-of-failure, "
                    "hidden mutation of shared state, or duplicate scheduler. "
                    "Read the file now and output only the report.")
        try:
            shares = [l for l in open(SHARE, encoding="utf-8").read().splitlines() if l.strip()][-2:]
            if shares:
                tops = []
                for l in shares:
                    try:
                        top = json.loads(l).get("top", "")[:180]
                    except Exception:
                        continue
                    if top.startswith("[") or "failed before producing" in top:
                        continue  # failure noise, not a finding
                    tops.append(top)
                if tops:
                    goal += "\n\nRECENT FINDINGS FROM OTHER MINERS (context, may inform your report):\n- " + "\n- ".join(tops)
        except Exception:
            pass
        # FIELD STEER — the film's tail for this seat (operator pen lights + turn-fail
        # health), one line of context. Missing/short field = no-op. Never replaces
        # the wing itself.
        try:
            _fj = os.path.join(ROOT, "watch", "steer_field", "FIELD.json")
            if os.path.exists(_fj):
                _field = json.loads(open(_fj, encoding="utf-8").read())
                for _r in _field.get("seat_tails", []):
                    if _r.get("seat") == sess:
                        goal += "\n\nFIELD STEER: " + str(_r.get("tail", ""))[:160]
                        break
        except Exception:
            pass
        log(sess + " steer tail -> " + t["id"])
        try:
            detail, folded, tid = dispatch(goal, sess)
            # GATE V2: substance + no boilerplate
            if folded and (is_boilerplate(detail) or len(detail) < 150):
                folded = False
                log(sess + " GATE V2: boilerplate/thin rejected")
            if not folded:
                st["attempts"][t["id"]] = st["attempts"].get(t["id"], 0) + 1
                save_state(st)
                log(sess + " beat rejected - attempt " + str(st["attempts"].get(t["id"], "?"))
                    + " (claim kept; requeues after grace " + str(CLAIM_GRACE_S) + "s)")
                time.sleep(60)
                continue
            body = detail
            # the seat returns a 300-char summary; the full report lives in the
            # seat OUTBOX (2000-char cap). The corpus eats the full meat.
            ob = os.path.join(ROOT, "queue", "handoff", SEAT, "OUTBOX", "%s.md" % tid)
            if os.path.isfile(ob):
                txt = open(ob, encoding="utf-8", errors="ignore").read()
                if "\n## Result\n" in txt:
                    full = txt.split("\n## Result\n", 1)[1].strip()
                    if len(full) > len(body):
                        body = full
            with open(os.path.join(ROOT, t["output"]), "w", encoding="utf-8") as f:
                f.write("# " + t["title"] + "\n\nvia " + sess + " beat " + tid
                        + " folded=" + str(folded) + "\n\n" + body + "\n")
            board_row(ORGAN, "task.receipt", "overnight: " + t["title"],
                      (detail or "(empty)")[:200], "DONE", t["output"])
            with open(SHARE, "a", encoding="utf-8") as f:
                f.write(json.dumps({"from": sess, "wing": t["id"],
                                    "top": (detail or "")[:220]}, ensure_ascii=False) + "\n")
            log("done " + t["id"] + " (" + str(len(detail)) + " chars)")
            if claim:
                bay_organs.release_claim(QUEUE_NAME, t["id"], claim["token"], root=CLAIMS_ROOT)
                claim = None
        except Exception as e:
            st["attempts"][t["id"]] = st["attempts"].get(t["id"], 0) + 1
            save_state(st)
            board_row(ORGAN, "task.receipt", "overnight: " + t["title"],
                      "BLOCKED: " + str(e), "BLOCKED", t["output"])
            log("blocked " + t["id"] + ": " + str(e))
            time.sleep(60)
        time.sleep(SLEEP_S)

def park_test():
    """GUARD (b) LIVE TEST — force one park against the REAL maybe_park path,
    then re-visit it twice more (the exact flood mechanism the 18:26Z edit
    claimed to fix: a parked task re-seen by the pick loop). Scratch sinks
    only: no live queue/log/state/board is touched, no LLM dispatch happens,
    the main loop is never entered. The harness (mag/race_harness.py) runs
    this as a subprocess and greps the scratch log: exactly ONE park line."""
    import tempfile
    global QUEUE, BOARD, LOG, STATE, SHARE
    tmp = tempfile.mkdtemp(prefix="churn_parktest_")
    QUEUE = os.path.join(tmp, "queue.jsonl")
    BOARD = os.path.join(tmp, "board.jsonl")
    LOG = os.path.join(tmp, "engine.log")
    STATE = os.path.join(tmp, "state.json")
    SHARE = os.path.join(tmp, "share.jsonl")
    task = {"id": "parktest-" + ts().replace(":", ""), "title": "Park Live Test",
            "source": os.path.join(tmp, "in.py"),
            "output": os.path.join(tmp, "out.md")}  # absolute: os.path.join passes it through
    ok = True
    try:
        st = state()
        st.setdefault("attempts", {})
        st["attempts"][task["id"]] = PARK_ATTEMPTS  # attempts exhausted -> next visit parks
        # three loop passes over the same task: pre-fix code re-parked forever
        # at ~737 lines/sec; post-fix must park exactly once and stay parked.
        for i in range(3):
            maybe_park(task, st)
        parked_lines = [l for l in open(LOG, encoding="utf-8").read().splitlines()
                        if "parked as THIN" in l]
        marker = state().get("parked", {}).get(task["id"])
        thin_file = os.path.isfile(task["output"])
        if len(parked_lines) != 1:
            ok = False
        if not marker:
            ok = False
        if not thin_file:
            ok = False
        print("PARKTEST-LOG " + LOG)
        print("PARKTEST park-lines=%d marker=%s thin-file=%s" % (
            len(parked_lines), bool(marker), thin_file))
        print("PARKTEST " + ("OK - one park, one line, state marker set" if ok else "FAIL"))
        return 0 if ok else 1
    except Exception as e:
        print("PARKTEST-LOG " + LOG)
        print("PARKTEST FAIL - exception: " + repr(e))
        return 1


if __name__ == "__main__":
    if "--park-test" in sys.argv:
        sys.exit(park_test())
    main()
