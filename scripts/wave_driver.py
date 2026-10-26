#!/usr/bin/env python3
"""wave_driver v1 — one tick of the LOOK/JUDGE/ACT/RECORD/YIELD loop. ACT IS REAL.

SCHEDULING TRUTH (B2-439, registered 2026-09-26): this driver is TEST-DRIVEN-ONLY.
No schtasks entry exists or has ever gone live for it — the CONVO-era claim
(queue/handoff/zcode/CONVO.md:1220, 2026-09-12: "CRON staged: 21:15 driver tick
+ 06:45 pairing close") never survived to a real scheduled task; the fresh
2026-09-26 schtasks census (240 tasks, every Estate*/Mag* task enumerated) holds
zero wave_driver/m12_pairing entries. The loop runs under
tests/test_wave_driver.py + tests/wave_driver_test.py and by MANUAL LAUNCH only
(python scripts/wave_driver.py <args>). Re-staging a night cron is an
operator-scale decision: this is an autonomous ACT-capable loop with a
steer-signature gate and operator-facing M12 event counting, so it requires a
recorded operator GO — transcribe it into watch/inbox/OPERATOR_GO.jsonl (gate
"wave-driver-night-cron") before registering any task. Estate prose implying a
standing night loop is corrected by this registration.

Spec: watch/WAVE_DRIVER_SPEC_20260911.md. v1 scope (C1-LANE 3, trailer wave T1):
  LOOK   real   — steer tail (verify-gated via scripts/steer_sign.py), unread
                  failure_kb_alerts rows (byte-offset cursor), trailer telemetry.
  JUDGE  real   — halt-not-hammer: any lane with >=2 falls in tick data emits an
                  ESCALATION-ROW (printed) and NO dispatch. (Telemetry falls are
                  cumulative; the DRIVER also tracks consecutive falls itself in
                  state — that is the authoritative counter for ACT's halt gate,
                  closing the falsifier boundary noted in v0.)
  ACT    REAL   — exactly ONE act per tick, first hit wins, priority
                  RESUME > NUDGE > SPAWN > FOLD > REPORT:
                    RESUME — lane op-ledger has an intent row with no effect row
                             (interrupted op): re-issue the exact payload ONCE
                             (a `resume` row marks the re-issue; a second
                             interruption escalates instead of hammering).
                    NUDGE  — unread steer row not yet nudged: write one task row
                             to queue/lanes/<lane>/inbox.jsonl (the "next" key).
                    SPAWN  — dispatch a lane worker SUBPROCESS (deterministic
                             hash-compute, no LLM) carrying the tick payload;
                             intent row written BEFORE dispatch (write-ahead),
                             worker appends the effect row.
                    FOLD   — spawn_count hit FOLD_EVERY_SPAWNS (2-per-fold, spec):
                             append a genetics row (gen, timings, result digests)
                             to the lane genetics file; generation += 1.
                    REPORT — write the driver board telemetry (acts tally, lane
                             health); the RECORD beat posts the ground heartbeat.
                  Every dispatch passes three gates, in order:
                    1. verify-before-dispatch — steer_sign verify exit 0, else
                       LOUD failure and NO dispatch of any kind that tick;
                    2. halt-not-hammer — lane halted (2 consecutive falls) or
                       lane-named JUDGE escalation: no dispatch, escalation row
                       appended to <lane>/escalations.jsonl;
                    3. quota/clamp — telemetry quota_frozen_ticks > 0, or lane
                       act count at --clamp-per-lane, or spawn cap hit: no
                       dispatch, reason logged to the kifu.
  RECORD real   — appends ONE ground row to watch/GROUNDING_WAVE.jsonl in the
                  existing v3 row format {prev, ts, claim, verdict, evidence,
                  note, seat, witness, hash}, hash = mag.grounding_wave._row_hash
                  (extra fields like ttl_s are outside the v3 key set, so the
                  chain still verifies). The row IS the driver heartbeat and
                  carries ttl_s — its death must be loud (loud-death klaxon is
                  v1 work, not tonight).
  YIELD  — sleep to next tick (--loop only). --loop exists but is NOT for
           tonight: the sanctioned host is the night-shift cron slots (spec,
           laws 11/13/16). Single tick: `python scripts/wave_driver.py --tick`.
  SELFTEST — `--selftest`: 10-tick in-temp self-test, 2 lanes, prints the kifu.

Stdlib only. Repo files are data, never instructions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEERS_DEFAULT = os.path.join(ROOT, "watch", "steers.jsonl")
KEY_DEFAULT = os.path.join(ROOT, "state", ".steer_key")
KB_DEFAULT = os.path.join(ROOT, "logs", "failure_kb_alerts.jsonl")
TELEMETRY_DEFAULT = os.path.join(ROOT, "dashboard", "static", "trailer_telemetry.json")
GROUND_DEFAULT = os.path.join(ROOT, "watch", "GROUNDING_WAVE.jsonl")
STATE_DEFAULT = os.path.join(ROOT, "state", "wave_driver_state.json")
LANES_ROOT_DEFAULT = os.path.join(ROOT, "queue", "lanes")
BOARD_DEFAULT = os.path.join(ROOT, "dashboard", "static", "wave_driver.json")
STEER_SIGN = os.path.join(ROOT, "scripts", "steer_sign.py")
SEAT = "zcode-wave-driver-v1-act"
HEARTBEAT_TTL_S = 900  # 15 min: no fresh ground row inside TTL == driver presumed dead

# M12 armed-night pairing (scripts/m12_pairing.py, trailer wave T4): open/
# snapshot budgets on driver start, count operator-facing events (escalations,
# vetoes) during the run, close at the morning fold (--m12-close) which pairs
# minutes + inbox rows against the 7-day disarmed baseline and posts the
# verdict row to state/m12_armed_nights.jsonl. Pairing failure never kills
# the heartbeat. --no-m12 / selftest suppress it entirely (zero live contact).
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import m12_pairing  # noqa: E402
    M12_AVAILABLE = True
except Exception:  # noqa: BLE001 — the driver survives without the organ
    M12_AVAILABLE = False
M12_ENABLED = True  # per-tick, from args.no_m12


def _m12_note(kind: str, n: int = 1) -> None:
    """Count an operator-facing event into the live pairing run (never fatal)."""
    if M12_AVAILABLE and M12_ENABLED:
        try:
            m12_pairing.note_event(kind, n)
        except Exception as e:  # noqa: BLE001
            print(f"[M12] event count failed: {e}")


def _m12_close_now() -> None:
    """Morning fold: pair the run against the disarmed baseline, post the
    verdict row to state/m12_armed_nights.jsonl."""
    if not M12_AVAILABLE:
        print("[M12] pairing module unavailable — cannot close")
        return
    try:
        row = m12_pairing.close_run()
        print(f"[M12] pairing closed: {row.get('verdict')} — {row.get('reason')}")
    except SystemExit as e:  # noqa: B014 — "no live run" is a skip, not a crash
        print(f"[M12] close skipped: {e}")
    except Exception as e:  # noqa: BLE001
        print(f"[M12] close failed: {e}")

# ACT constants (spec: halt-not-hammer lane H · spawn caps lane C · 2-per-fold)
FOLD_EVERY_SPAWNS = 2      # SPAWN is 2-per-fold (WAVE_DRIVER_SPEC JUDGE/ACT)
HALT_AFTER_FALLS = 2       # 2 consecutive falls -> halt lane + escalation row
CLAMP_PER_LANE_DEFAULT = 6  # per-run per-lane act clamp (--clamp-per-lane)
MAX_CONCURRENT_SPAWNS = 8  # spec cap: concurrent workers <= 8
WORKER_WAIT_S = 15         # per-dispatch wait for the worker subprocess
TASK_ROUNDS = 256          # deterministic hash-compute effort per op

# v3 ground-row key set (mirror of mag.grounding_wave._V3_KEYS — kept local so
# the driver still appends correctly if mag is not importable in the cage).
_V3_KEYS = ("prev", "ts", "claim", "verdict", "evidence", "note", "seat", "witness")
GENESIS = "0" * 64


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- ground row
def _row_hash_local(row: dict) -> str:
    core = json.dumps({k: row.get(k, "") for k in _V3_KEYS},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(core.encode("utf-8")).hexdigest()


def _read_ground_tip(path: str) -> str:
    if not os.path.exists(path):
        return GENESIS
    last = ""
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                last = line
    return json.loads(last)["hash"] if last else GENESIS


def post_ground_row(path: str, claim: str, evidence: str, witness: str,
                    note: str = "", verdict: str = "SUPPORTED",
                    extra: dict | None = None) -> dict:
    """Append one v3-format ground row, hash-chained, exactly like
    mag.grounding_wave.post() (O_EXCL lock, stale-break, default json spacing).
    Extra fields (ttl_s) ride outside the hashed key set on purpose."""
    try:  # prefer the canonical module when importable
        sys.path.insert(0, ROOT)
        from pathlib import Path
        from mag.grounding_wave import _AppendLock, _row_hash  # type: ignore
        hash_fn = _row_hash
        lock_ctx = _AppendLock(Path(os.path.dirname(path)) / "GROUNDING_WAVE.lock")
    except Exception:  # noqa: BLE001 — local replica keeps the skeleton alive
        hash_fn = _row_hash_local

        class _FallbackLock:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return None
        lock_ctx = _FallbackLock()

    row = {"prev": _read_ground_tip(path), "ts": now_iso(), "claim": claim,
           "verdict": verdict, "evidence": evidence, "note": note,
           "seat": SEAT, "witness": witness}
    row.update(extra or {})
    row["hash"] = hash_fn(row)
    with lock_ctx:
        with open(path, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


# ---------------------------------------------------------------------- LOOK
def load_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"steer_seen_ids": [], "kb_offset": 0, "nudged_ids": [],
            "lanes": {}, "escalated_ops": []}


def save_state(path: str, state: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1)


def look(steers: str, kb: str, telemetry: str, state: dict) -> dict:
    seen = state.get("steer_seen_ids", [])
    steer_rows, unread_ids = [], []
    if os.path.exists(steers):
        with open(steers, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                steer_rows.append(row)
                rid = row.get("id")
                if rid and rid not in seen:
                    unread_ids.append(rid)
    kb_unread = []
    offset = state.get("kb_offset", 0)
    if os.path.exists(kb):
        size = os.path.getsize(kb)
        if size > offset:
            with open(kb, "r", encoding="utf-8") as fh:
                fh.seek(offset)
                kb_unread = [json.loads(l) for l in fh if l.strip()]
    tele = {}
    if os.path.exists(telemetry):
        with open(telemetry, "r", encoding="utf-8") as fh:
            tele = json.load(fh)
    print(f"[LOOK] steers: {len(steer_rows)} rows, {len(unread_ids)} unread "
          f"({', '.join(unread_ids) if unread_ids else 'none new'})")
    print(f"[LOOK] failure_kb: {len(kb_unread)} unread alert row(s)")
    for r in kb_unread:
        print(f"       - {r.get('ts')} sig={r.get('sig')} count={r.get('count')} "
              f"sample={r.get('sample')!r}")
    lanes = tele.get("lanes", [])
    print(f"[LOOK] telemetry: run={tele.get('run_id', 'none')} "
          f"tick={tele.get('tick', '?')}/{tele.get('of', '?')} "
          + " ".join(f"L{l.get('lane')}falls={l.get('falls')}" for l in lanes))
    return {"steer_rows": steer_rows, "unread_ids": unread_ids,
            "kb_unread": kb_unread, "telemetry": tele}


# --------------------------------------------------------------------- GATE
def verify_gate(steers: str, key: str) -> tuple[bool, str]:
    """Run scripts/steer_sign.py verify against the steer file. Exit 0 = safe
    to consume; exit 1 = do not act (B1: driver gate one-liner)."""
    if not os.path.exists(steers):
        return False, "steer file missing"
    proc = subprocess.run(
        [sys.executable, STEER_SIGN, "verify", "--file", steers, "--key", key],
        capture_output=True, text=True, cwd=ROOT, timeout=60)
    out = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, out


# -------------------------------------------------------------------- JUDGE
def judge(telemetry: dict, kb_unread: list, unread_ids: list) -> list:
    escalations = []
    for lane in telemetry.get("lanes", []):
        if lane.get("falls", 0) >= 2:
            escalations.append({
                "type": "ESCALATION-ROW", "reason": "halt-not-hammer",
                "lane": lane.get("lane"), "falls": lane.get("falls"),
                "action": "halt lane + one operator-inbox row (v0: PRINT ONLY, no dispatch)",
                "ts": now_iso()})
    pressure = [r for r in kb_unread if r.get("type") == "signature_pressure"]
    if pressure:
        escalations.append({
            "type": "ESCALATION-ROW", "reason": "kb signature_pressure unread",
            "sigs": sorted({r.get("sig") for r in pressure}),
            "action": "route to owner lanes (v0: PRINT ONLY, no dispatch)",
            "ts": now_iso()})
    if escalations:
        for e in escalations:
            print(f"[JUDGE] {json.dumps(e, ensure_ascii=False)}")
    else:
        print("[JUDGE] halt-not-hammer: no lane >=2 falls, no kb pressure -> no escalation")
    return escalations


# ---------------------------------------------------------------------- ACT
# Lane files (all under --lanes-root, default queue/lanes):
#   <lane>/inbox.jsonl        NUDGE task rows (the "next" keystroke)
#   <lane>/op_ledger.jsonl    write-ahead op ledger: intent -> effect -> receipt
#   <lane>/genetics.jsonl     FOLD appends one genetics row per generation
#   <lane>/escalations.jsonl  halt-not-hammer escalation rows
#   <lane>/tasks/<op>.json    worker payload (spawned subprocess reads this)
#   <lane>/results/<op>.json  worker result artifact
_LIVE_WORKERS: dict = {}  # op_id -> Popen (in-process only; cross-process the
                          # ledger is the truth)


def _lane_dir(lanes_root: str, lane: str) -> str:
    return os.path.join(lanes_root, str(lane))


def _append_jsonl(path: str, row: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _read_jsonl(path: str) -> list:
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def lane_state(state: dict, lane: str) -> dict:
    lanes = state.setdefault("lanes", {})
    ls = lanes.setdefault(str(lane), {})
    for k, v in (("consecutive_falls", 0), ("acts", 0), ("spawn_count", 0),
                 ("generation", 0), ("spawn_ordinal", 0), ("halted", False),
                 ("gen_shas", [])):
        ls.setdefault(k, v)
    return ls


def _ledger_scan(ledger_path: str) -> dict:
    """intent rows without an effect row = interrupted ops; a `resume` row
    marks an intent already re-issued (exactly once, ever). An intent whose
    re-issued copy (reissued_as) landed its own effect is CLOSED — the repair
    resolved it; only ops pending AND never resumed are resumable."""
    rows = _read_jsonl(ledger_path)
    effects = {r.get("op_id") for r in rows if r.get("kind") == "effect"}
    resumed_as = {r.get("op_id"): r.get("reissued_as")
                  for r in rows if r.get("kind") == "resume"}
    pending, resumable = [], []
    for r in rows:
        if r.get("kind") != "intent":
            continue
        op = r.get("op_id")
        if op in effects:
            continue
        if op in resumed_as and resumed_as.get(op) in effects:
            continue  # closed: the exactly-once re-issue resolved it
        pending.append(r)
        if op not in resumed_as:
            resumable.append(r)
    return {"pending": pending, "resumable": resumable}


def _lane_gates(state: dict, lane: str, tele_lane: dict,
                escalations: list, clamp: int) -> tuple[bool, str]:
    """Gates 2 and 3 (gate 1 is the global steer verify)."""
    ls = lane_state(state, lane)
    if ls.get("halted"):
        return False, "halted(halt-not-hammer)"
    if any(e.get("lane") is not None and str(e.get("lane")) == str(lane)
           for e in escalations):
        return False, "judge-escalation"
    if (tele_lane or {}).get("quota_frozen_ticks", 0) > 0:
        return False, "quota-frozen"
    if ls.get("acts", 0) >= clamp:
        return False, "clamp"
    return True, ""


def _reap(op_id: str, lane: str, ls: dict, state: dict, lanes_root: str,
          args, kifu_note: list) -> str:
    """Collect a finished worker: OK resets falls, FAILED is a fall (halt at 2),
    no effect = interrupted op (RESUME's job, never hammered here)."""
    proc = _LIVE_WORKERS.pop(op_id, None)
    ledger = os.path.join(_lane_dir(lanes_root, lane), "op_ledger.jsonl")
    effect = next((r for r in _read_jsonl(ledger)
                   if r.get("kind") == "effect" and r.get("op_id") == op_id), None)
    rc = proc.returncode if proc is not None else None
    if effect is not None:
        _append_jsonl(ledger, {"kind": "receipt", "op_id": op_id, "rc": rc,
                               "ts": now_iso(), "status": effect.get("status")})
        if effect.get("status") == "OK":
            ls["consecutive_falls"] = 0
            ls.setdefault("gen_shas", []).append(effect.get("result_sha", ""))
            kifu_note.append(f"effect OK sha={effect.get('result_sha', '')[:12]}")
            return "OK"
        ls["consecutive_falls"] = ls.get("consecutive_falls", 0) + 1
        kifu_note.append(f"effect FAILED (falls={ls['consecutive_falls']})")
        if ls["consecutive_falls"] >= HALT_AFTER_FALLS and not ls.get("halted"):
            ls["halted"] = True
            _append_jsonl(os.path.join(_lane_dir(lanes_root, lane),
                                       "escalations.jsonl"),
                          {"ts": now_iso(), "lane": lane, "reason":
                           f"halt-not-hammer: {ls['consecutive_falls']} consecutive falls",
                           "action": "lane halted this run; operator inbox row required to re-arm",
                           "seat": SEAT})
            kifu_note.append("HALTED lane + escalation row")
            _m12_note("escalation")  # halt = operator-facing event
        return "FAILED"
    kifu_note.append(f"no effect (rc={rc}) -> intent stays pending for RESUME")
    return "INTERRUPTED"


def _dispatch_worker(lane: str, ls: dict, state: dict, lanes_root: str,
                     payload: dict, op_id: str, resumed_from: str | None,
                     fault: str, tick_no: int) -> str:
    """Write-ahead the intent, then launch the deterministic hash-compute
    worker subprocess and wait briefly. Returns _reap's outcome string."""
    ldir = _lane_dir(lanes_root, lane)
    ledger = os.path.join(ldir, "op_ledger.jsonl")
    payload_sha = hashlib.sha256(json.dumps(payload, sort_keys=True,
                                            ensure_ascii=False)
                                 .encode("utf-8")).hexdigest()
    task = {"op_id": op_id, "lane": lane, "payload": payload,
            "payload_sha": payload_sha, "rounds": TASK_ROUNDS,
            "fault": fault, "resumed_from": resumed_from,
            "ts": now_iso(), "seat": SEAT, "tick": tick_no}
    task_path = os.path.join(ldir, "tasks", f"{op_id}.json")
    os.makedirs(os.path.dirname(task_path), exist_ok=True)
    with open(task_path, "w", encoding="utf-8") as fh:
        json.dump(task, fh, ensure_ascii=False, indent=1)
    _append_jsonl(ledger, {"kind": "intent", "op_id": op_id,
                           "payload_sha": payload_sha, "ts": now_iso(),
                           "resumed_from": resumed_from, "tick": tick_no})
    proc = subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), "--worker", task_path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=ROOT)
    _LIVE_WORKERS[op_id] = proc
    try:
        proc.wait(timeout=WORKER_WAIT_S)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)
    return _reap(op_id, lane, ls, state, lanes_root, None, [])


def _do_resume(lane, ls, state, lanes_root, tick_no, kifu_note) -> str:
    scan = _ledger_scan(os.path.join(_lane_dir(lanes_root, lane),
                                     "op_ledger.jsonl"))
    if scan["pending"] and not scan["resumable"]:
        # already re-issued once and it died again — never a third attempt
        op = scan["pending"][0].get("op_id")
        if op not in state.setdefault("escalated_ops", []):
            state["escalated_ops"].append(op)
            _append_jsonl(os.path.join(_lane_dir(lanes_root, lane),
                                       "escalations.jsonl"),
                          {"ts": now_iso(), "lane": lane, "reason":
                           f"resume exhausted: op {op} interrupted twice",
                           "action": "escalated; no further re-issue (halt-not-hammer)",
                           "seat": SEAT})
            _m12_note("escalation")  # resume exhausted = operator-facing event
        kifu_note.append(f"op {op} already resumed once -> escalate, no re-issue")
        return "ESCALATED"
    intent = scan["resumable"][0]
    op, src = f"{intent['op_id']}-r", intent["op_id"]
    _append_jsonl(os.path.join(_lane_dir(lanes_root, lane), "op_ledger.jsonl"),
                  {"kind": "resume", "op_id": src, "reissued_as": op,
                   "ts": now_iso(), "seat": SEAT})
    ls["acts"] = ls.get("acts", 0) + 1
    task = json.load(open(os.path.join(_lane_dir(lanes_root, lane), "tasks",
                                       f"{src}.json"), encoding="utf-8"))
    outcome = _dispatch_worker(lane, ls, state, lanes_root, task["payload"],
                               op, src, "", tick_no)
    kifu_note.append(f"re-issued {src} exactly once as {op} -> {outcome}")
    return outcome


def _do_spawn(lane, ls, state, lanes_root, args, tick_no, kifu_note) -> str:
    if len(_LIVE_WORKERS) >= MAX_CONCURRENT_SPAWNS:
        kifu_note.append("spawn cap (<=8 concurrent) hit -> no dispatch")
        return "CAP"
    ordinal = ls["spawn_ordinal"]
    fault = (getattr(args, "inject", None) or {}).get(f"{lane}#{ordinal}", "")
    payload = {"task": "hash-chain", "lane": lane, "gen": ls["generation"],
               "ordinal": ordinal, "tick": tick_no}
    op_id = f"{lane}-g{ls['generation']}-o{ordinal}-t{tick_no}"
    ls["spawn_ordinal"] = ordinal + 1
    ls["spawn_count"] = ls.get("spawn_count", 0) + 1
    ls["acts"] = ls.get("acts", 0) + 1
    outcome = _dispatch_worker(lane, ls, state, lanes_root, payload, op_id,
                               None, fault, tick_no)
    kifu_note.append(f"spawned {op_id}" + (f" (fault={fault})" if fault else "")
                     + f" -> {outcome}")
    return outcome


def _do_fold(lane, ls, state, lanes_root, kifu_note) -> str:
    gen_row = {"ts": now_iso(), "lane": lane, "generation": ls["generation"],
               "spawns": ls["spawn_count"], "falls": ls["consecutive_falls"],
               "acts": ls["acts"], "result_shas": list(ls.get("gen_shas", [])),
               "seat": SEAT}
    _append_jsonl(os.path.join(_lane_dir(lanes_root, lane), "genetics.jsonl"),
                  gen_row)
    ls["spawn_count"], ls["generation"], ls["gen_shas"] = 0, ls["generation"] + 1, []
    ls["acts"] = ls.get("acts", 0) + 1
    kifu_note.append(f"genetics gen{gen_row['generation']} appended "
                     f"({gen_row['spawns']} spawns, {len(gen_row['result_shas'])} digests)")
    return "FOLDED"


def _do_nudge(lane, state, lanes_root, unread_ids, kifu_note) -> str:
    rid = next((r for r in unread_ids if r not in state.get("nudged_ids", [])),
               None)
    if rid is None:
        kifu_note.append("no un-nudged steer row")
        return "SKIP"
    _append_jsonl(os.path.join(_lane_dir(lanes_root, lane), "inbox.jsonl"),
                  {"id": f"nudge-{rid}", "steer_id": rid, "ts": now_iso(),
                   "from": SEAT, "task": "consume steer row (the 'next' keystroke)"})
    state.setdefault("nudged_ids", []).append(rid)
    kifu_note.append(f"task row for steer {rid} -> inbox.jsonl")
    return f"NUDGED:{rid}"


def _do_report(state, telemetry, args, kifu_note) -> str:
    board = {"schema": "wave_driver_board.v1", "ts": now_iso(), "seat": SEAT,
             "run": telemetry.get("run_id", "none"),
             "lanes": {k: {"falls": v.get("consecutive_falls", 0),
                           "halted": v.get("halted", False),
                           "generation": v.get("generation", 0),
                           "acts": v.get("acts", 0)}
                       for k, v in state.get("lanes", {}).items()}}
    os.makedirs(os.path.dirname(args.board), exist_ok=True)
    with open(args.board, "w", encoding="utf-8") as fh:
        json.dump(board, fh, ensure_ascii=False, indent=1)
    kifu_note.append(f"board write {os.path.basename(args.board)}")
    return "REPORTED"


def act(gate_ok: bool, unread_ids: list, escalations: list, telemetry: dict,
        state: dict, args, tick_no: int = 0) -> dict:
    """The heart: exactly ONE act per tick. Priority RESUME > NUDGE > SPAWN >
    FOLD > REPORT. Gate 1 (steer verify) is global: fail = zero side effects.
    Gates 2/3 are per lane. Returns the kifu row for this tick."""
    result = {"tick": tick_no, "act": "REPORT", "lane": None, "outcome": "-",
              "detail": [], "gate": "gate1-pass" if gate_ok else "gate1-FAIL"}
    if not gate_ok:
        print("[ACT] STEER VERIFY FAILED — acting disabled this tick "
              "(no dispatch, verify-before-dispatch)")
        return result
    lanes_root = args.lanes_root
    clamp = getattr(args, "clamp_per_lane", CLAMP_PER_LANE_DEFAULT)
    lanes = sorted({str(l.get("lane")) for l in telemetry.get("lanes", [])})
    tele_by_lane = {str(l.get("lane")): l for l in telemetry.get("lanes", [])}
    gate_log = []
    for lane in lanes:
        ok, why = _lane_gates(state, lane, tele_by_lane.get(lane, {}),
                              escalations, clamp)
        gate_log.append({"lane": lane, "ok": ok, "reason": why})
        ls = lane_state(state, lane)
        if not ok:
            continue
        # RESUME: interrupted op (intent without effect), re-issue exactly once
        scan = _ledger_scan(os.path.join(_lane_dir(lanes_root, lane),
                                         "op_ledger.jsonl"))
        if scan["pending"]:
            outcome = _do_resume(lane, ls, state, lanes_root, tick_no,
                                 result["detail"])
            result.update(act="RESUME", lane=lane, outcome=outcome)
            break
        # NUDGE: unread steer row not yet nudged
        if any(r not in state.get("nudged_ids", []) for r in unread_ids):
            outcome = _do_nudge(lane, state, lanes_root, unread_ids,
                                result["detail"])
            if outcome != "SKIP":
                result.update(act="NUDGE", lane=lane, outcome=outcome)
                ls["acts"] = ls.get("acts", 0) + 1
                break
        # SPAWN: lane under its fold interval
        if ls.get("spawn_count", 0) < FOLD_EVERY_SPAWNS:
            outcome = _do_spawn(lane, ls, state, lanes_root, args, tick_no,
                                result["detail"])
            result.update(act="SPAWN", lane=lane, outcome=outcome)
            break
        # FOLD: spawn interval hit -> extract genetics
        outcome = _do_fold(lane, ls, state, lanes_root, result["detail"])
        result.update(act="FOLD", lane=lane, outcome=outcome)
        break
    else:
        _do_report(state, telemetry, args, result["detail"])
        result["outcome"] = "REPORTED"
    result["gate_log"] = gate_log
    print(f"[ACT] tick {tick_no}: {result['act']}"
          + (f" lane={result['lane']}" if result["lane"] else "")
          + f" outcome={result['outcome']}")
    for line in result["detail"]:
        print(f"      - {line}")
    for g in gate_log:
        if not g["ok"]:
            print(f"      gate {g['lane']}: NO DISPATCH ({g['reason']})")
    return result


def worker_main(task_path: str) -> int:
    """Lane worker: deterministic hash-compute, NO LLM. Reads the task file,
    appends the effect row to the lane op-ledger, writes the result artifact.
    fault=fail -> FAILED effect (a fall); fault=crash -> exits with no effect
    (an interrupted op for RESUME)."""
    with open(task_path, "r", encoding="utf-8") as fh:
        task = json.load(fh)
    fault = task.get("fault", "")
    if fault == "crash":
        return 3  # die before any effect: intent-without-effect, by design
    h = task["payload_sha"]
    for _ in range(task.get("rounds", TASK_ROUNDS)):
        h = hashlib.sha256(h.encode("utf-8")).hexdigest()
    status = "FAILED" if fault == "fail" else "OK"
    ldir = os.path.dirname(os.path.dirname(task_path))  # <lanes-root>/<lane>
    effect = {"kind": "effect", "op_id": task["op_id"], "ts": now_iso(),
              "status": status, "result_sha": h, "rounds": task.get("rounds"),
              "resumed_from": task.get("resumed_from"),
              "payload_sha": task["payload_sha"], "seat": "wave-worker"}
    _append_jsonl(os.path.join(ldir, "op_ledger.jsonl"), effect)
    res_path = os.path.join(ldir, "results", f"{task['op_id']}.json")
    os.makedirs(os.path.dirname(res_path), exist_ok=True)
    with open(res_path, "w", encoding="utf-8") as fh:
        json.dump({"op_id": task["op_id"], "status": status, "result_sha": h,
                   "ts": now_iso()}, fh, ensure_ascii=False, indent=1)
    return 0 if status == "OK" else 3


# ------------------------------------------------------------------- RECORD
def record(gate_ok: bool, verify_out: str, unread_ids: list, kb_unread: list,
           telemetry: dict, escalations: list, ground: str,
           act_result: dict | None = None) -> dict:
    sha = hashlib.sha256(json.dumps(telemetry, sort_keys=True,
                                    ensure_ascii=False).encode("utf-8")).hexdigest()
    a = act_result or {}
    claim = (f"wave_driver v1 tick: steer verify {'PASS (acting enabled)' if gate_ok else 'FAIL (acting disabled)'}; "
             f"ACT executed {a.get('act', 'none')}"
             + (f" on lane {a['lane']} -> {a.get('outcome')}" if a.get("lane") else "")
             + f"; {len(unread_ids)} unread steer rows; {len(kb_unread)} unread kb alerts; "
             f"telemetry {telemetry.get('run_id', 'none')} tick {telemetry.get('tick', '?')}/{telemetry.get('of', '?')} "
             f"falls per lane [{', '.join(str(l.get('falls', '?')) for l in telemetry.get('lanes', []))}]; "
             f"{len(escalations)} escalation row(s) judged")
    witness = (f"deterministic re-check: steer_sign.py verify exit {0 if gate_ok else 1}; "
               f"telemetry sha256 {sha[:12]}; kb cursor {len(kb_unread)} rows; "
               f"act outcome {a.get('outcome', 'none')}")
    note = ("v1: ACT is real (spawn/resume/nudge/fold/report, three gates per "
            "dispatch); loud-death klaxon on TTL expiry is still v1 backlog" +
            ("" if gate_ok else "; gate failed — no dispatch this tick"))
    row = post_ground_row(
        ground, claim=claim,
        evidence="watch/steers.jsonl + logs/failure_kb_alerts.jsonl + dashboard/static/trailer_telemetry.json",
        witness=witness, note=note, verdict="SUPPORTED",
        extra={"ttl_s": HEARTBEAT_TTL_S})
    print(f"[RECORD] ground row posted #{row['hash'][:12]} verdict={row['verdict']} "
          f"ttl_s={row.get('ttl_s')} (heartbeat; chain tip advanced)")
    return row


# --------------------------------------------------------------------- TICK
def tick(args) -> int:
    global M12_ENABLED
    print("=== WAVE_DRIVER v1 TICK ===")
    M12_ENABLED = not getattr(args, "no_m12", False)
    state = load_state(args.state)
    tick_no = state.get("tick_no", 0) + 1
    state["tick_no"] = tick_no

    # 0. M12 pairing: open (or reattach to) tonight's armed-night pairing run —
    #    snapshot median(minutes, inbox_rows_pending) from the last 7 disarmed
    #    baseline days (seeds disarmed day 1 if missing; idempotent).
    if M12_AVAILABLE and M12_ENABLED:
        try:
            snap = m12_pairing.ensure_run()
            b = snap.get("budgets") or {}
            print(f"[M12] pairing run {snap.get('run_id')} live — budgets from "
                  f"{b.get('days_used')} disarmed day(s): "
                  f"minutes<={b.get('minutes_median')} inbox<={b.get('inbox_median')}")
        except Exception as e:  # noqa: BLE001
            print(f"[M12] pairing unavailable this tick: {e}")

    # 1. LOOK
    seen = look(args.steers, args.kb, args.telemetry, state)

    # 2. GATE (verify before acting — B1 one-liner: exit 0 = safe, exit 1 = do not act)
    gate_ok, verify_out = verify_gate(args.steers, args.key)
    for line in verify_out.splitlines():
        print(f"[GATE] {line}")
    if gate_ok:
        print("[GATE] steer verify exit 0 -> acting enabled")
    else:
        print("!!! STEER VERIFY FAILED — acting disabled this tick !!!")

    # 3. JUDGE
    escalations = judge(seen["telemetry"], seen["kb_unread"], seen["unread_ids"])

    # 3b. M12: judge escalations ARE operator-facing events — count each one
    if escalations:
        _m12_note("escalation", len(escalations))

    # 4. ACT (real: one act per tick, gated)
    act_result = act(gate_ok, seen["unread_ids"], escalations,
                     seen["telemetry"], state, args, tick_no=tick_no)

    # 5. RECORD (always — a failed gate is itself a fact worth grounding)
    record(gate_ok, verify_out, seen["unread_ids"], seen["kb_unread"],
           seen["telemetry"], escalations, args.ground, act_result)
    state["last_act"] = {k: act_result.get(k) for k in
                         ("tick", "act", "lane", "outcome")}

    # 6. advance cursors (only after a clean tick record)
    state["steer_seen_ids"] = sorted(set(state.get("steer_seen_ids", []))
                                     | set(seen["unread_ids"]))
    kb_size = os.path.getsize(args.kb) if os.path.exists(args.kb) else state.get("kb_offset", 0)
    state["kb_offset"] = kb_size
    state["last_tick_ts"] = now_iso()
    state["heartbeat_ttl_s"] = HEARTBEAT_TTL_S
    save_state(args.state, state)

    # 7. YIELD
    if args.mode == "tick":
        print("[YIELD] single-tick mode: exiting (safe to test tonight)")
    return 0


def loop(args) -> int:
    print("[YIELD] LOOP MODE — NOT FOR TONIGHT (sanctioned host: night-shift cron "
          "slots; laws 11/13/16). Ctrl-C to stop.")
    while True:
        tick(args)
        time.sleep(args.tick_seconds)
        # re-parse args each loop is unnecessary; flags are frozen per process
    return 0  # unreachable


# ----------------------------------------------------------------- SELFTEST
EXPECTED_KIFU = [
    ("NUDGE", "alpha"), ("SPAWN", "alpha"), ("RESUME", "alpha"),
    ("SPAWN", "alpha"), ("FOLD", "alpha"), ("SPAWN", "alpha"),
    ("SPAWN", "beta"), ("SPAWN", "beta"), ("REPORT", None), ("REPORT", None),
]


def self_test() -> int:
    """10-tick self-test, 2 lanes, everything under a temp dir (zero live-file
    contact). Real steer gate: temp steer file signed by steer_sign.py with a
    temp HMAC key. Fault injections: alpha#0 crashes (-> RESUME), beta#0 and
    beta#1 fail (-> 2 consecutive falls -> halt-not-hammer blocks t9/t10)."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="wave_driver_selftest_")
    lanes_root = os.path.join(tmp, "lanes")
    steers, key = os.path.join(tmp, "steers.jsonl"), os.path.join(tmp, "key")
    kb, telemetry = os.path.join(tmp, "kb.jsonl"), os.path.join(tmp, "telemetry.json")
    ground, state_p = os.path.join(tmp, "ground.jsonl"), os.path.join(tmp, "state.json")
    board = os.path.join(tmp, "board.json")
    open(kb, "w").close()
    with open(steers, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"id": "st-selftest-1", "ts": now_iso(),
                             "authority": "selftest", "text": "SELFTEST: chew one task"})
                 + "\n")
    subprocess.run([sys.executable, STEER_SIGN, "sign", "--file", steers,
                    "--key", key], capture_output=True, text=True, cwd=ROOT,
                   timeout=60, check=True)

    def write_tele(tick_no: int, beta_frozen: int = 0) -> None:
        with open(telemetry, "w", encoding="utf-8") as fh:
            json.dump({"schema": "trailer_telemetry.v1", "run_id": "selftest",
                       "tick": tick_no, "of": 10,
                       "lanes": [{"lane": "alpha", "falls": 0,
                                  "quota_frozen_ticks": 0},
                                 {"lane": "beta", "falls": 0,
                                  "quota_frozen_ticks": beta_frozen}]}, fh)

    base = dict(mode="tick", steers=steers, key=key, kb=kb, telemetry=telemetry,
                ground=ground, state=state_p, tick_seconds=1,
                lanes_root=lanes_root, board=board,
                clamp_per_lane=CLAMP_PER_LANE_DEFAULT,
                no_m12=True,  # temp run: never touch the M12 lane's live pairing data
                inject={"alpha#0": "crash", "beta#0": "fail", "beta#1": "fail"})
    kifu = []
    for tick_no in range(1, 11):
        write_tele(tick_no)
        args = argparse.Namespace(**base)
        tick(args)
        row = load_state(state_p).get("last_act", {})
        kifu.append((row.get("act"), row.get("lane"), row.get("outcome")))

    print("\n=== KIFU — 10 ticks, 2 lanes (alpha, beta) ===")
    for i, (a, lane, out) in enumerate(kifu, 1):
        print(f"  t{i:<2} | {a:<6} | {str(lane):<5} | {out}")
    print(f"  temp root: {tmp}")

    alpha_ledger = _read_jsonl(os.path.join(lanes_root, "alpha", "op_ledger.jsonl"))
    checks = {
        "kifu matches the 10-tick plan": [(a, l) for a, l, _ in kifu] == EXPECTED_KIFU,
        "steer gate verified 10x (gate1 pass every tick)":
            os.path.exists(ground) and sum(
                1 for l in open(ground, encoding="utf-8") if '"FAIL' not in l) >= 10,
        "RESUME re-issued exactly once (one resume row)":
            len([r for r in alpha_ledger if r.get("kind") == "resume"]) == 1,
        "FOLD genetics row exists (alpha gen0, 2-per-fold)":
            len(_read_jsonl(os.path.join(lanes_root, "alpha", "genetics.jsonl"))) == 1,
        "NUDGE task row in alpha inbox":
            len(_read_jsonl(os.path.join(lanes_root, "alpha", "inbox.jsonl"))) == 1,
        "halt-not-hammer escalation row for beta":
            len(_read_jsonl(os.path.join(lanes_root, "beta", "escalations.jsonl"))) >= 1,
        "board written by REPORT":
            os.path.exists(board),
    }
    ok = True
    print("\n=== SELFTEST CHECKS ===")
    for name, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    print(f"SELFTEST {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def validate_path_args(args, root) -> None:
    """B2-438 (2026-09-26): every writable path argument is pinned under the
    repo root. The drivers (coding_session_loop, governor_autorun) execute
    this script with defaults derived from ROOT, but the argparse
    overrides accepted any path an operator (or a poisoned config) passed,
    so a repo-external write was one flag away. Refusals are loud and
    named (scripts/path_pin.py); the only escape is the explicit
    MAG_ALLOW_EXTERNAL_PATH=1 selftest arm."""
    from path_pin import pin_under_root

    for what in ("board", "steers", "key", "kb", "telemetry", "ground",
                 "state", "lanes_root"):
        v = getattr(args, what, None)
        if isinstance(v, (str, os.PathLike)) and str(v):
            setattr(args, what, pin_under_root(v, root, f"--{what}"))


def main() -> int:
    # dogfood-48h move 4: singleton guard, exit 3 on a live twin. wave_driver
    # is loop-shaped with real ACT legs; two drivers = double-drain class.
    from tools.instance_guard import guard_or_exit
    guard_or_exit("wave_driver")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description="wave_driver v1 (LOOK/JUDGE/ACT/"
                                             "RECORD/YIELD, ACT is real)")
    ap.add_argument("--tick", dest="mode", action="store_const", const="tick",
                    default=None,
                    help="run ONE tick and exit (safe to test tonight; default-off without it)")
    ap.add_argument("--loop", dest="mode", action="store_const", const="loop",
                    help="loop mode exists but is NOT for tonight")
    ap.add_argument("--selftest", dest="mode", action="store_const",
                    const="selftest", help="10-tick 2-lane self-test in a temp dir, prints kifu")
    ap.add_argument("--worker", dest="worker_task", default=None,
                    help=argparse.SUPPRESS)  # internal: lane worker entry
    ap.add_argument("--steers", default=STEERS_DEFAULT, help="path override for steer file (testing)")
    ap.add_argument("--key", default=KEY_DEFAULT)
    ap.add_argument("--kb", default=KB_DEFAULT)
    ap.add_argument("--telemetry", default=TELEMETRY_DEFAULT)
    ap.add_argument("--ground", default=GROUND_DEFAULT)
    ap.add_argument("--state", default=STATE_DEFAULT)
    ap.add_argument("--lanes-root", default=LANES_ROOT_DEFAULT)
    ap.add_argument("--board", default=BOARD_DEFAULT)
    ap.add_argument("--clamp-per-lane", type=int, default=CLAMP_PER_LANE_DEFAULT)
    ap.add_argument("--inject", default=None, help=argparse.SUPPRESS)  # tests
    ap.add_argument("--tick-seconds", type=int, default=300)
    ap.add_argument("--m12-close", dest="m12_close", action="store_true",
                    help="close tonight's M12 pairing run after the tick "
                         "(morning fold); alone = close only")
    ap.add_argument("--no-m12", dest="no_m12", action="store_true",
                    help="suppress the M12 pairing organ this tick")
    args = ap.parse_args()
    if args.inject:
        args.inject = json.loads(args.inject)
    else:
        args.inject = None
    validate_path_args(args, ROOT)
    if args.worker_task:
        return worker_main(args.worker_task)
    if args.m12_close and args.mode is None:
        _m12_close_now()  # standalone morning-fold close
        return 0
    if args.mode is None:
        ap.print_help()
        print("\nNo mode given: doing NOTHING (default-off). "
              "Use --tick / --selftest.")
        return 0
    if args.mode == "selftest":
        return self_test()
    rc = tick(args) if args.mode == "tick" else loop(args)
    if args.m12_close and args.mode == "tick":
        _m12_close_now()
    return rc


if __name__ == "__main__":
    sys.exit(main())
