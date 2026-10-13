"""test_server_reprint: the log IS the reprint (W1, MICKEY17 wave 1, 2026-09-29).

Runnable harness (not pytest): same shape as scripts/test_mud_replay.js, a
main that prints PASS/FAIL lanes and exits 1 on any red. Grading target is
server/world.py (MountainWorld), read-only: this file only DRIVES the world.

Why it exists (ledger return 21): server/README claims more than the pytest
suite grades. tests/test_server_v0.py proves same-sequence determinism only:
it never replays from a SAVED TAPE and never grades an ACTION_FORK. Lanes:

  lane group REPRINT: record a world under a frozen action tape, dump its
    hash-chained log to JSONL, then build a FRESH world and feed ONLY what
    the dumped log says (action rows become staged actions in seq order,
    tick rows become ticks, preserving the (action, tick) interleaving).
    Assert per-tick node volumes byte-identical, the fresh chain verifies,
    and the fresh log is row-for-row byte-identical to the tape it replayed.
    Every saved tape becomes a grader; the log is the reprint.

  lane group ACTION_FORK: flip ONE verb in the tape read back from the log
    (boil -> valve, target held), replay, and assert divergence first fires
    at the EXACT tick where the flipped action applies (tick 3), with the
    tick number and the first differing nodes named. The one boiled unit was
    the win: the record wins at tick 5, the fork never wins.

  lane group CHAIN_CONTINUITY: append to a reopened log path: seq and prev
    resume from the file's last row, the appended rows verify, and the file
    on disk grows by exactly the appended rows.

Tape facts (verified by running, not hand-copied): 9 stages, all acks,
6 ticks; siphon primes at tick 2, gate1 XOR-holds at tick 3, siphon breaks
at tick 4, WIN at tick 5 (crown 4, sticky), tick 6 boils the crown itself.
Physics note: the record run ends with spring at -1 (deferred gate inflow
plus the siphon draw in the same tick both debit spring; deterministic and
already blessed by tests/test_server_v0.py determinism laws).

Run:
    .venv\\Scripts\\python.exe scripts\\test_server_reprint.py

Not a pytest module: nothing executes at import (an explicit
`pytest scripts/test_server_reprint.py` collects zero tests instead of
running the harness inside the collector).

Laws honored: em-dash 0 (this file is ASCII), no fabricated results (every
expectation below was produced by a real run before it was frozen).
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.world import MountainWorld, load_log_rows, verify_log_rows  # noqa: E402

# ------------------------------------------------------------ lane frame ----
RESULTS: list[tuple[int, str, bool, str]] = []
LANE_N = 0


def lane(name, fn):
    global LANE_N
    LANE_N += 1
    try:
        fn()
        RESULTS.append((LANE_N, name, True, ""))
    except AssertionError as e:
        RESULTS.append((LANE_N, name, False, str(e)))
    except Exception as e:  # a crash is a red lane, not a broken harness
        RESULTS.append((LANE_N, name, False, f"{type(e).__name__}: {e}"))


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg or "assertion failed")


def eq(a, b, msg):
    if a != b:
        raise AssertionError(f"{msg or 'eq'}: got {a!r} want {b!r}")


# ------------------------------------------------------------ the frozen ----
# tape: (action, tick) interleaving. Staged actions apply at the START of the
# next tick, before the physics (the determinism law in server/world.py).
TAPE = [
    ("stage", "s1", "boil", "spring"),      # applies at tick 1
    ("tick",),
    ("stage", "s2", "tag", "hollow"),       # applies at tick 2
    ("stage", "s1", "valve", "p_bypass"),   # opens the siphon
    ("tick",),
    ("stage", "s1", "boil", "spring"),      # applies at tick 3  <- FORK ENTRY
    ("stage", "s2", "join", "terrace"),
    ("tick",),
    ("stage", "s1", "boil", "gate1"),
    ("tick",),
    ("stage", "s2", "tag", "crown"),
    ("stage", "s1", "boil", "gate1"),
    ("tick",),
    ("stage", "s1", "boil", "crown"),       # steam condenses back at the crown
    ("tick",),
]

FORK_TICK = 3    # the flipped action is staged for tick 3: divergence is due THERE
WIN_TICK = 5     # the record reaches crown 4 at tick 5; the fork never does

# replay steps come from log rows, which carry users not sids
USER_SID = {"ada": "s1", "ben": "s2"}


def run_steps(steps, log_path=None):
    """Fresh world, sessions, then the steps in order. Returns per-tick
    volume lines (canonical JSON), winner flags, stage replies, the world.
    Step actor field accepts either a sid (frozen tape) or a user name
    (steps parsed back from log rows)."""
    w = MountainWorld(log_path=log_path)
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    vols, winners, replies = [], [], []
    for st in steps:
        if st[0] == "stage":
            _, actor, verb, target = st
            sid = actor if actor in ("s1", "s2", "s3") else USER_SID[actor]
            r = w.stage(sid, verb, target)
            tag = r["op"] if r["op"] == "ack" else f"reject:{r.get('why')}"
            replies.append((actor, verb, target, tag))
        else:
            w.tick()
            vols.append(json.dumps(w.node_volumes(), sort_keys=True))
            winners.append(w.winner)
    return {"vols": vols, "winners": winners, "replies": replies, "w": w}


def steps_from_log(rows):
    """The reprint: action rows become staged actions (seq order), tick rows
    become ticks. Same (action, tick) interleaving the record lived."""
    steps = []
    for row in rows:
        if row["kind"] == "action":
            steps.append(("stage", row["user"], row["verb"], row["target"]))
        elif row["kind"] == "tick":
            steps.append(("tick",))
        else:
            raise AssertionError(f"unknown row kind in tape: {row['kind']}")
    return steps


def flipped_boil_to_valve(steps):
    """Flip the ONE boil staged for FORK_TICK to a valve (target held: a node
    target under the valve verb is a typed UNKNOWN_TARGET reject at stage
    time, so the boil simply never happens in the fork run)."""
    out, tick_no, flipped = [], 0, None
    for st in steps:
        if st[0] == "tick":
            tick_no += 1
            out.append(st)
            continue
        _, actor, verb, target = st
        if verb == "boil" and tick_no + 1 == FORK_TICK:
            flipped = (actor, target)
            out.append(("stage", actor, "valve", target))
        else:
            out.append(st)
    ok(flipped is not None, f"no boil staged for tick {FORK_TICK} in the tape")
    return out, flipped


def first_vol_diff(rec_vols, fork_vols):
    for i, (a, b) in enumerate(zip(rec_vols, fork_vols), start=1):
        if a != b:
            return i, json.loads(a), json.loads(b)
    return None, None, None


# ---------------------------------------------------------------- shared ----
REC: dict = {}          # the record run, set in main() before lanes fire
TAPE_FILE = None        # the dumped record log (the tape)
FRESH_FILE = None       # the reprint run's own log
TMP = None


def _events_joined():
    """the record's tick rows already carry the broadcast event lists"""
    rows = REC["w"].rows
    return "\n".join("\n".join(r["events"]) for r in rows if r["kind"] == "tick")


# =========================================================== LANE GROUP 1 ===
# REPRINT: record, dump, rebuild from the dump, byte-identical


def lane_record_lived():
    """the tape actually lived: 9 acks, 6 ticks, all four verbs, siphon +
    XOR events, WIN at tick 5"""
    eq(len(REC["vols"]), 6, "tick count")
    eq(len(REC["replies"]), 9, "stage count")
    for actor, verb, target, tag in REC["replies"]:
        eq(tag, "ack", f"stage {actor}/{verb}/{target} was not accepted")
    verbs = {r[1] for r in REC["replies"]}
    eq(verbs, {"boil", "valve", "tag", "join"}, "verbs exercised")
    joined = _events_joined()
    ok("Siphon p_bypass primes at crest (2)." in joined, "siphon never primed")
    ok("Junction gate1 holds 2 below gate (2 inlets); pooling." in joined,
       "XOR hold never fired")
    ok("Siphon p_bypass breaks (intake dry)." in joined, "siphon never broke")
    eq(REC["winners"], [False, False, False, False, True, True], "winner flags")
    eq(REC["vols"][4], '{"crown": 4, "gate1": 0, "hollow": 0, "spring": -1, '
                       '"terrace": 0, "waste": 0}', "tick 5 volumes")


def lane_dump_is_the_tape():
    """close the record, read the JSONL back: chain verifies, disk == memory,
    and it parses into exactly the 9 stages + 6 ticks that were run"""
    REC["w"].close()
    rows = load_log_rows(TAPE_FILE)          # verifies the chain or raises
    eq(rows, REC["w"].rows, "disk rows differ from memory rows")
    eq(verify_log_rows(rows), True, "chain does not verify")
    steps = steps_from_log(rows)
    eq(sum(1 for s in steps if s[0] == "tick"), 6, "tick rows in tape")
    eq(sum(1 for s in steps if s[0] == "stage"), 9, "action rows in tape")


def lane_reprint_byte_identical():
    """FRESH world fed ONLY the dumped log: per-tick node volumes byte-identical"""
    steps = steps_from_log(load_log_rows(TAPE_FILE))
    rep = run_steps(steps, log_path=FRESH_FILE)
    rep["w"].close()
    eq(len(rep["vols"]), len(REC["vols"]), "reprint tick count")
    for i, (a, b) in enumerate(zip(REC["vols"], rep["vols"]), start=1):
        eq(b, a, f"per-tick volumes diverge at tick {i}")
    eq(rep["winners"], REC["winners"], "winner flags diverge")


def lane_reprint_log_byte_identical():
    """the reprint's own log is byte-identical to the tape it replayed, chain
    included: nothing in the replay invented or dropped a row"""
    eq(FRESH_FILE.read_bytes(), TAPE_FILE.read_bytes(),
       "reprint log bytes differ from the tape file")
    rows = load_log_rows(FRESH_FILE)
    eq(verify_log_rows(rows), True, "fresh chain does not verify")
    eq([r["seq"] for r in rows], list(range(1, len(rows) + 1)), "seq numbering")


# =========================================================== LANE GROUP 2 ===
# ACTION_FORK: flip one verb in the tape read back from the log


def lane_fork_named_at_tick():
    """flip boil -> valve on the action staged for tick 3: ticks 1-2 stay
    byte-identical, divergence fires AT tick 3, nodes named"""
    steps = steps_from_log(load_log_rows(TAPE_FILE))
    fork_steps, (actor, target) = flipped_boil_to_valve(steps)
    frk = run_steps(fork_steps)
    n, rec_nodes, frk_nodes = first_vol_diff(REC["vols"], frk["vols"])
    ok(n is not None, "the flipped verb changed nothing (fork is vacuous)")
    eq(n, FORK_TICK, f"ACTION_FORK fired at tick {n}, expected {FORK_TICK}")
    diff_nodes = [k for k in rec_nodes if rec_nodes[k] != frk_nodes[k]]
    ok(diff_nodes, "no differing node at the fork tick (impossible)")
    # the flipped stage was honestly refused: valve + node target is typed.
    # (The tape's own tick-2 valve p_bypass is still an ack; match the
    # flip's target, not just the verb.)
    flipped_reply = [r for r in frk["replies"]
                     if r[1] == "valve" and r[2] == target]
    eq(len(flipped_reply), 1, "flip locator matched more than one stage")
    eq(flipped_reply[0][3], "reject:UNKNOWN_TARGET", "flipped stage verdict")
    print(f"    ACTION_FORK @ tick {n}: {actor} boil {target} -> valve {target} "
          f"(typed UNKNOWN_TARGET); nodes diverge: "
          + ", ".join(f"{k} {rec_nodes[k]}->{frk_nodes[k]}" for k in diff_nodes))


def lane_fork_costs_the_win():
    """the one boiled unit was the win: record wins at tick 5 (sticky), the
    fork never wins (crown stuck at 3)"""
    steps = steps_from_log(load_log_rows(TAPE_FILE))
    fork_steps, _ = flipped_boil_to_valve(steps)
    frk = run_steps(fork_steps)
    eq(REC["winners"][WIN_TICK - 1], True, "record does not win at tick 5")
    eq(frk["winners"], [False] * 6, "the fork run won anyway")
    eq(json.loads(frk["vols"][-1])["crown"], 3, "fork crown at final tick")
    eq(json.loads(REC["vols"][-1])["crown"], 4, "record crown at final tick")
    print(f"    consequence: crown {json.loads(REC['vols'][-1])['crown']} vs "
          f"{json.loads(frk['vols'][-1])['crown']}; winner True vs "
          f"{frk['winners'][-1]} at tick 6 (win delayed past the tape end)")


# =========================================================== LANE GROUP 3 ===
# CHAIN_CONTINUITY: append to a reopened log


def lane_chain_continuity():
    """a fresh world on the SAME log path appends, it does not restart: seq
    resumes at last+1, prev links to the file's last sha, and the grown file
    verifies end to end"""
    log = Path(TMP.name) / "chain_continue.jsonl"
    first = run_steps(TAPE, log_path=log)
    first["w"].close()
    old = load_log_rows(log)
    eq(verify_log_rows(old), True, "first segment does not verify")

    w2 = MountainWorld(log_path=log)        # reopen: continues the chain
    w2.register_session("s3", "cy")
    ack = w2.stage("s3", "boil", "spring")  # fresh state: spring is 6 again
    eq(ack["op"], "ack", "reopened world refused a valid stage")
    w2.tick()
    w2.close()

    grown = load_log_rows(log)              # verifies or raises
    eq(len(grown), len(old) + 2, "append count (one action row + one tick row)")
    first_new = grown[len(old)]
    eq(first_new["seq"], old[-1]["seq"] + 1, "seq did not resume")
    eq(first_new["prev"], old[-1]["sha"], "prev did not link to the file tip")
    eq(grown[-1]["kind"], "tick", "appended segment ends on a tick row")
    print(f"    reopened log: seq resumed at {first_new['seq']}, prev linked "
          f"to file tip; {len(old)} rows -> {len(grown)} rows, chain verifies")


# ------------------------------------------------------------------ main ----
def main() -> int:
    global TMP, TAPE_FILE, FRESH_FILE
    TMP = tempfile.TemporaryDirectory(prefix="server_reprint_")
    TAPE_FILE = Path(TMP.name) / "tape_record.jsonl"
    FRESH_FILE = Path(TMP.name) / "tape_reprint.jsonl"
    REC.update(run_steps(TAPE, log_path=TAPE_FILE))

    lane("R1: the tape lived (9 acks, 6 ticks, 4 verbs, siphon + XOR + WIN @ 5)",
         lane_record_lived)
    lane("R2: dump is the tape (JSONL reloads, chain verifies, disk == memory)",
         lane_dump_is_the_tape)
    lane("R3: REPRINT from the dump: fresh world, per-tick volumes byte-identical",
         lane_reprint_byte_identical)
    lane("R4: REPRINT log byte-identical to its tape + fresh chain verifies",
         lane_reprint_log_byte_identical)
    lane("F1: ACTION_FORK boil->valve: divergence at EXACTLY tick 3, nodes named",
         lane_fork_named_at_tick)
    lane("F2: the fork costs the win (record WIN @ 5 sticky, fork never wins)",
         lane_fork_costs_the_win)
    lane("C1: CHAIN_CONTINUITY: reopened log appends (seq resumes, prev links)",
         lane_chain_continuity)

    fails = [r for r in RESULTS if not r[2]]
    for n, name, good, err in RESULTS:
        print(f"{'PASS' if good else 'FAIL'} {str(n).rjust(2)} {name}"
              + ("" if good else f"  -> {err}"))
    print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} lanes green"
          + (f", {len(fails)} RED" if fails else ""))
    print(f"reprint harness: tape 15 rows (9 actions + 6 ticks), "
          f"fork tick {FORK_TICK}, win tick {WIN_TICK}")
    # Windows law: close every log handle before the temp dir goes away, and
    # do not let a cleanup race turn a green run red.
    REC["w"].close()
    TMP.cleanup()
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
