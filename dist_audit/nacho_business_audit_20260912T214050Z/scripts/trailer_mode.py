"""trailer_mode — attachment-under-relative-motion, as a sport (2026-09-11).

Operator dropped the sport: a flatbed truck circles the track; cars must drive
up onto the moving trailer and STAY ON for a set time to win, while the driver
actively swerves and brakes. Self-steal: this is the night test's true meter —
hold-time under maneuver, not tasks in a calm window.

v0 (TONIGHT): N lightweight worker subprocesses must dock every tick — hash a
per-tick nonce delivered over stdin and return it over stdout — while a SEALED
perturbation schedule (driver-only, hash-committed at start) injects kills,
delays, and quota pinches. Score = appended seconds-on-trailer per lane. Falls
are counted, never hidden. Telemetry renders to
dashboard/static/trailer_telemetry.json for the grandstand.

Trailer law: the truck never waits. A missed tick is a fall. The driver holds the
swerve schedule; lanes hold nothing. Seal is hash-printed, contents withheld.
Workers touch no filesystem at all (Mimosa: no path surface, no traversal).

Schema: trailer_mode.v1 · stdlib only · host-side run · $0

v1 adds SEVERITY (--severity N, or TRAILER_SEVERITY env): 2 runs a 10-14 event
kill-weighted schedule with double delays (up to 60% of tick), mid-tick kills
that drain the lane's in-flight result queue, and one guaranteed double-tap
(kill + quota_pinch, same lane, same tick). Falls are the point: severity
scales until lanes fall, or the meter has no dynamic range.

Severity 3 (falsifier probe): 12-16 swerves, kills most likely (50% draw,
90% land mid-tick), delays at 50-60% of the tick, double-taps allowed in the
draw. Task ledger: every successful dock IS the accepted task (the hash
computation is the task) — accepted/rejected counted per lane per tick into
ticklog + telemetry, paired with the tick's hold delta.
"""
from __future__ import annotations

import hashlib
import json
import os
import queue
import secrets
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
RUN_DIR = ROOT / "memory" / "runs" / "trailer"
TELEMETRY = ROOT / "dashboard" / "static" / "trailer_telemetry.json"

TICK_SECONDS = 20
LANES = 3
DURATION_TICKS = 45  # 15 minutes

PERTURB_ACTIONS = ("kill", "delay", "quota_pinch")
SEV2_ACTIONS = ("kill", "delay", "kill", "delay", "quota_pinch")  # kill-weighted: falls are the point
SEV3_ACTIONS = ("kill", "kill", "delay", "kill", "delay", "quota_pinch")  # kills most likely: the meter
SEVERITY = 1  # set from --severity / TRAILER_SEVERITY in main(); 2 = the mean truck
SECURE_RNG = secrets.SystemRandom()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_schedule() -> list[dict]:
    """Sealed swerve schedule, hash-committed at start; contents withheld from lanes.

    severity 1: sparse (1..ticks//4, capped 9), no adjacent-tick pileups.
    severity 3: 12-16 events, 50% kill draw, ~20% of draws are double_taps
    (plural allowed); same seal discipline as 2.
    severity 2: 10-14 kill-weighted events; adjacent ticks allowed across lanes
    (same tick carries at most 2 lanes, same lane keeps a 1-tick gap to respawn
    into), plus exactly one double_tap (kill + quota_pinch, same lane same tick).
    """
    span = max(2, DURATION_TICKS - 2)
    events = []
    guard = 0
    if SEVERITY >= 3:
        target = SECURE_RNG.randint(12, 16)
        per_lane: dict[int, set[int]] = {}
        while len(events) < target and guard < 4000:
            guard += 1
            tick = SECURE_RNG.randint(2, span)
            lane = SECURE_RNG.randrange(LANES)
            if any(abs(tick - t) < 2 for t in per_lane.get(lane, ())):
                continue
            if sum(1 for e in events if e["tick"] == tick) >= 2:
                continue
            if len(events) == target - 1 or SECURE_RNG.random() < 0.20:
                action, duration = "double_tap", 1  # severity 3: double-taps allowed, plural
            else:
                action = SECURE_RNG.choice(SEV3_ACTIONS)
                duration = SECURE_RNG.randint(1, 2)
            events.append({"tick": tick, "lane": lane, "action": action, "duration_ticks": duration})
            per_lane.setdefault(lane, set()).add(tick)
        if not any(e["action"] == "double_tap" for e in events):  # guaranteed placement
            for tick in range(2, span + 1):
                placed = False
                for lane in range(LANES):
                    if not any(abs(tick - t) < 2 for t in per_lane.get(lane, ())):
                        events.append({"tick": tick, "lane": lane,
                                       "action": "double_tap", "duration_ticks": 1})
                        placed = True
                        break
                if placed:
                    break
    elif SEVERITY >= 2:
        target = SECURE_RNG.randint(10, 14)
        per_lane: dict[int, set[int]] = {}
        while len(events) < target and guard < 4000:
            guard += 1
            tick = SECURE_RNG.randint(2, span)
            lane = SECURE_RNG.randrange(LANES)
            if any(abs(tick - t) < 2 for t in per_lane.get(lane, ())):
                continue
            if sum(1 for e in events if e["tick"] == tick) >= 2:
                continue
            if len(events) == target - 1:
                action, duration = "double_tap", 1  # the promised double-tap
            else:
                action = SECURE_RNG.choice(SEV2_ACTIONS)
                duration = SECURE_RNG.randint(1, 2)
            events.append({"tick": tick, "lane": lane, "action": action, "duration_ticks": duration})
            per_lane.setdefault(lane, set()).add(tick)
        if not any(e["action"] == "double_tap" for e in events):  # guaranteed placement
            for tick in range(2, span + 1):
                placed = False
                for lane in range(LANES):
                    if not any(abs(tick - t) < 2 for t in per_lane.get(lane, ())):
                        events.append({"tick": tick, "lane": lane,
                                       "action": "double_tap", "duration_ticks": 1})
                        placed = True
                        break
                if placed:
                    break
    else:
        max_events = max(1, min(9, DURATION_TICKS // 4))
        target = SECURE_RNG.randint(1, max_events)
        ticks = set()
        while len(events) < target and guard < 500:
            guard += 1
            tick = SECURE_RNG.randint(2, span)
            if any(abs(tick - t) < 2 for t in ticks):
                continue
            ticks.add(tick)
            events.append({
                "tick": tick,
                "lane": SECURE_RNG.randrange(LANES),
                "action": SECURE_RNG.choice(PERTURB_ACTIONS),
                "duration_ticks": SECURE_RNG.randint(1, 2),
            })
    return sorted(events, key=lambda e: e["tick"])


WORKER_CODE = """import hashlib, sys
lane = {lane!r}
while True:
    line = sys.stdin.buffer.readline()
    if not line:
        break
    sys.stdout.buffer.write(hashlib.sha256(line + str(lane).encode()).hexdigest().encode() + b'\\n')
    sys.stdout.flush()
"""


class Worker:
    """One lane: a stateless hash-responder over stdin/stdout. No filesystem."""

    def __init__(self, lane: int):
        self.lane = lane
        self.proc: subprocess.Popen | None = None
        self.results: "queue.Queue[str]" = queue.Queue()
        self.reader: threading.Thread | None = None

    def start(self):
        code = WORKER_CODE.format(lane=self.lane)
        self.proc = subprocess.Popen(
            [sys.executable, "-u", "-c", code],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        self.results = queue.Queue()
        self.reader = threading.Thread(target=self._read_stdout, daemon=True)
        self.reader.start()

    def _read_stdout(self):
        for line in self.proc.stdout:
            self.results.put(line.decode("utf-8", "replace").strip())

    def send_nonce(self, nonce: bytes) -> None:
        self.proc.stdin.write(nonce.hex().encode() + b"\n")
        self.proc.stdin.flush()

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except Exception:
                self.proc.kill()

    def alive(self) -> bool:
        return self.proc is not None and self.proc.poll() is None


def drain_results(w: Worker) -> int:
    """Clear a lane's result queue — in-flight answers die with the swerve."""
    n = 0
    while True:
        try:
            w.results.get_nowait()
            n += 1
        except queue.Empty:
            break
    return n


def parse_args(argv: list[str]) -> dict:
    cfg = {"severity": SEVERITY, "ticks": DURATION_TICKS,
           "tick_seconds": TICK_SECONDS, "lanes": LANES}
    env = os.environ.get("TRAILER_SEVERITY", "")
    if env.isdigit():
        cfg["severity"] = max(1, int(env))
    names = {"--severity": "severity", "-s": "severity", "--ticks": "ticks",
             "--tick-seconds": "tick_seconds", "--lanes": "lanes"}
    it = iter(argv)
    for arg in it:
        if arg in names:
            cfg[names[arg]] = max(1, int(next(it, cfg[names[arg]])))
    cfg["severity"] = max(1, cfg["severity"])
    cfg["ticks"] = max(4, cfg["ticks"])
    return cfg


def main():
    global SEVERITY, TICK_SECONDS, LANES, DURATION_TICKS
    cfg = parse_args(sys.argv[1:])
    SEVERITY, TICK_SECONDS = cfg["severity"], cfg["tick_seconds"]
    LANES, DURATION_TICKS = cfg["lanes"], cfg["ticks"]

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-trailer-s{SEVERITY}"
    run_dir = RUN_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    schedule = build_schedule()
    schedule_bytes = json.dumps(schedule, sort_keys=True).encode()
    schedule_sha = sha(schedule_bytes)
    (run_dir / "sealed_schedule.json").write_bytes(schedule_bytes)  # driver-only; lanes never see this

    workers = [Worker(i) for i in range(LANES)]
    for w in workers:
        w.start()

    ticklog = run_dir / "ticklog.jsonl"
    hold_seconds = [0] * LANES
    falls = [0] * LANES
    docked_total = [0] * LANES
    quota_hold = [0] * LANES  # quota-pinch ticks: excluded from hold AND fall
    accepted_total = [0] * LANES  # task ledger: a dock IS the accepted task (the hash computation)
    rejected_total = [0] * LANES

    header = {
        "schema": "trailer_mode.v1", "run_id": run_id, "started": now_iso(),
        "severity": SEVERITY,
        "tick_seconds": TICK_SECONDS, "lanes": LANES, "duration_ticks": DURATION_TICKS,
        "schedule_sha256": schedule_sha,
        "note": "sealed swerve schedule withheld from lanes; driver computes expected results itself",
    }
    with ticklog.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"row": "header", **header}) + "\n")

    print(f"TRAILER ROLLING: {run_id} · severity {SEVERITY} · {LANES} lanes · {DURATION_TICKS} ticks x {TICK_SECONDS}s "
          f"(~{DURATION_TICKS * TICK_SECONDS // 60} min) · sealed schedule {schedule_sha[:12]} "
          f"({len(schedule)} swerves)", flush=True)

    try:
        for tick in range(1, DURATION_TICKS + 1):
            t0 = time.time()
            events = [e for e in schedule if e["tick"] == tick]
            tick_row = {"tick": tick, "ts": now_iso(), "lanes": []}

            for lane in range(LANES):
                lane_t0 = time.time()
                w = workers[lane]
                evs = [e for e in events if e["lane"] == lane]
                entry = {"lane": lane, "event": None, "docked": False, "fell": False,
                         "accepted": 0, "rejected": 0, "hold_delta": 0, "note": ""}
                rows_seen = 0  # diagnostics: result rows consumed this lane-tick

                if any(e["action"] == "quota_pinch" for e in evs):
                    quota_hold[lane] += 1
                    entry["event"] = "quota_pinch"
                    entry["note"] = "frozen out: excluded from hold and fall"
                elif any(e["action"] == "double_tap" for e in evs):
                    # severity 2: kill + quota_pinch, same lane, same tick.
                    quota_hold[lane] += 1
                    entry["event"] = "double_tap"
                    if w.alive():
                        w.stop()
                    drained = drain_results(w)
                    entry["note"] = (f"double-tap: kill + quota pinch; lane frozen, worker left dead "
                                     f"({drained} row(s) drained), respawn law covers next tick")
                else:
                    kill = any(e["action"] == "kill" for e in evs)
                    # severity 2: 75% of kills land MID-tick, nonce already in flight —
                    # the answer dies with the worker and the result queue is drained.
                    midtick = kill and SEVERITY >= 2 and SECURE_RNG.random() < (0.90 if SEVERITY >= 3 else 0.75)
                    deadline = t0 + TICK_SECONDS
                    expected = None

                    if kill:
                        entry["event"] = "kill"
                        if midtick:
                            if not w.alive():
                                w.start()
                            nonce = secrets.token_bytes(32)
                            wire = nonce.hex().encode() + b"\n"
                            expected = sha(wire + str(lane).encode())
                            w.send_nonce(nonce)
                            time.sleep(SECURE_RNG.uniform(0.2, 1.0))  # let the answer get in flight
                            k0 = time.time()
                            w.stop()  # the swerve
                            k_stop = round(1000 * (time.time() - k0))
                            drained = drain_results(w)
                            k0 = time.time()
                            w.start()  # respawn law, immediately — the lane must live
                            entry["note"] = (f"mid-tick kill: result queue drained ({drained} row(s)); "
                                             f"stop={k_stop}ms respawn={round(1000 * (time.time() - k0))}ms")
                        else:
                            w.stop()
                            entry["note"] = "early kill: lane braced before the send"
                    if any(e["action"] == "delay" for e in evs):
                        entry["event"] = (entry["event"] + "+" if entry["event"] else "") + "delay"
                        if SEVERITY >= 3:
                            time.sleep(TICK_SECONDS * SECURE_RNG.uniform(0.50, 0.60))  # swerve eats up to 60% of the tick
                        elif SEVERITY >= 2:
                            time.sleep(TICK_SECONDS * SECURE_RNG.uniform(0.40, 0.60))  # double swerve
                        else:
                            time.sleep(min(3.0, TICK_SECONDS * 0.4))  # the swerve

                    if not w.alive():
                        w.start()  # respawn law: restart, never leave a lane dead

                    docked = False
                    if midtick:
                        # only a result that survived the drain could match; bound the
                        # wait so one lane's wreck doesn't eat the shared tick deadline
                        # for the lanes behind it in the serial loop
                        mid_deadline = min(deadline, time.time() + 2.0)
                        while time.time() < mid_deadline:
                            try:
                                got = w.results.get(timeout=max(0.05, mid_deadline - time.time()))
                                rows_seen += 1
                                if got == expected:
                                    docked = True
                                    break
                            except queue.Empty:
                                break
                    else:
                        nonce = secrets.token_bytes(32)
                        wire = nonce.hex().encode() + b"\n"  # worker hashes the raw stdin line, newline included
                        expected = sha(wire + str(lane).encode())
                        w.send_nonce(nonce)

                        while time.time() < deadline:
                            try:
                                got = w.results.get(timeout=max(0.05, deadline - time.time()))
                                rows_seen += 1
                                if got == expected:
                                    docked = True
                                    break
                                # wrong hash stays undocked; queue keeps draining
                            except queue.Empty:
                                break

                    if not w.alive():
                        w.start()  # respawn law

                    entry["ms"] = round(1000 * (time.time() - lane_t0))
                    entry["rows"] = rows_seen
                    if not docked and not entry["fell"]:
                        entry["diag"] = {"qsize": w.results.qsize(), "alive": w.alive()}
                    entry["docked"] = docked
                    if docked:
                        hold_seconds[lane] += TICK_SECONDS
                        docked_total[lane] += 1
                        accepted_total[lane] += 1
                        entry["accepted"] = 1
                        entry["hold_delta"] = TICK_SECONDS
                        if kill:
                            entry["note"] = ("braced the mid-tick kill" if midtick else "held through kill")
                    else:
                        falls[lane] += 1
                        rejected_total[lane] += 1
                        entry["rejected"] = 1
                        entry["fell"] = True

                tick_row["lanes"].append(entry)

            with ticklog.open("a", encoding="utf-8") as f:
                f.write(json.dumps(tick_row) + "\n")

            TELEMETRY.parent.mkdir(parents=True, exist_ok=True)
            TELEMETRY.write_text(json.dumps({
                "schema": "trailer_telemetry.v1", "run_id": run_id,
                "tick": tick, "of": DURATION_TICKS, "updated": now_iso(),
                "lanes": [
                    {"lane": i, "hold_seconds": hold_seconds[i], "falls": falls[i],
                     "docked": docked_total[i], "accepted": accepted_total[i],
                     "rejected": rejected_total[i], "quota_frozen_ticks": quota_hold[i]}
                    for i in range(LANES)
                ],
                "leaderboard": sorted(
                    [{"lane": i, "hold_seconds": hold_seconds[i], "falls": falls[i]} for i in range(LANES)],
                    key=lambda x: -x["hold_seconds"]),
            }, indent=1), encoding="utf-8")

            remaining = max(0.0, TICK_SECONDS - (time.time() - t0))
            time.sleep(remaining)
            print(f"tick {tick}/{DURATION_TICKS} · hold: "
                  + " ".join(f"L{i}={hold_seconds[i]}s/{falls[i]}F" for i in range(LANES)), flush=True)
    finally:
        for w in workers:
            w.stop()

    summary = {
        "schema": "trailer_mode.v1.summary", "run_id": run_id, "finished": now_iso(),
        "severity": SEVERITY,
        "schedule_sha256": schedule_sha, "swerve_count": len(schedule),
        "actions": {a: sum(1 for e in schedule if e["action"] == a)
                    for a in sorted({e["action"] for e in schedule})},
        "lanes": [
            {"lane": i, "hold_seconds": hold_seconds[i], "falls": falls[i],
             "docked_ticks": docked_total[i], "accepted_tasks": accepted_total[i],
             "rejected_tasks": rejected_total[i], "quota_frozen_ticks": quota_hold[i],
             "hold_pct_of_run": round(100 * hold_seconds[i] / (DURATION_TICKS * TICK_SECONDS), 1)}
            for i in range(LANES)
        ],
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print("TRAILER COMPLETE:", json.dumps(summary["lanes"]), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
