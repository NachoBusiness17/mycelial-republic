"""s2-15 steering pipeline census - one-shot store reader. Read-only.

Banked copy: lives in flash50, so ROOT is fixed to the repo root
(four levels up from watch/inbox/burn_reset_20260927/flash50/).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
out = {}

def rows(p: Path):
    if not p.is_file():
        return []
    out_rows = []
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out_rows.append(json.loads(ln))
        except Exception:
            out_rows.append({"_unparseable": True})
    return out_rows

# 1. WINDOW_STEER bus (mag/steer.py)
sd = ROOT / "memory" / "runs" / "steer"
steers = sorted(sd.glob("*.json")) if sd.is_dir() else []
unconsumed = []
for f in steers:
    try:
        rec = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        if not rec.get("consumed"):
            unconsumed.append(f.name)
    except Exception:
        unconsumed.append(f.name + " (unreadable)")
out["steer_bus"] = {"n_files": len(steers), "n_unconsumed": len(unconsumed),
                    "unconsumed": unconsumed[:10],
                    "trail_lines": len(rows(sd / "trail.jsonl"))}

# 2. operator_inbox
ib = ROOT / "memory" / "operator_inbox.json"
if ib.is_file():
    d = json.loads(ib.read_text(encoding="utf-8", errors="replace"))
    c = d.get("committed") or []
    out["operator_inbox"] = {
        "committed_n": len(c),
        "pending_n": sum(1 for x in c if x.get("status") == "pending"),
        "processed_n": len(d.get("processed") or []),
        "sources": sorted({str(x.get("source")) for x in c})[:12],
    }
else:
    out["operator_inbox"] = "MISSING"

# 3. steer_router pins
pp = ROOT / "memory" / "runs" / "steer_router" / "pins.json"
pins = json.loads(pp.read_text(encoding="utf-8", errors="replace")) if pp.is_file() else []
out["pins"] = {"n": len(pins), "resumed": sum(1 for p in pins if p.get("resumed"))}

# 4. behavioral corpus
bc = ROOT / "memory" / "pile" / "behavioral_corpus.jsonl"
r = rows(bc)
out["behavioral_corpus"] = {"n": len(r),
                            "modes": {m: sum(1 for x in r if x.get("mode") == m)
                                      for m in sorted({str(x.get("mode")) for x in r})}}

# 5. steer_bus receipts
sr = rows(ROOT / "watch" / "steer_bus_receipts.jsonl")
out["steer_bus_receipts"] = {"n": len(sr),
                             "applied_false": sum(1 for x in sr if x.get("applied") is False)}

# 6. phone relay log
pr = rows(ROOT / "watch" / "inbox" / "phone_relay_log.jsonl")
out["phone_relay"] = {"n": len(pr),
                      "kinds": {k: sum(1 for x in pr if x.get("kind") == k)
                                for k in sorted({str(x.get("kind")) for x in pr})},
                      "decisions": {k: sum(1 for x in pr if x.get("decision") == k)
                                    for k in sorted({str(x.get("decision")) for x in pr})}}

# 7. interrupt pipeline
stack = ROOT / "memory" / "runs" / "interrupt_pipeline" / "interrupt_stack.json"
st = json.loads(stack.read_text(encoding="utf-8", errors="replace")) if stack.is_file() else []
out["interrupt_pipeline"] = {"stack_n": len(st),
                             "batches_rows": len(rows(ROOT / "memory" / "runs" / "interrupt_pipeline" / "batches.jsonl"))}

# 8. steer bridge seen + drop file
seen = ROOT / "memory" / "working" / "steer_bridge_seen.json"
if seen.is_file():
    d = json.loads(seen.read_text(encoding="utf-8", errors="replace"))
    out["steer_bridge"] = {"n_seen": len(d.get("seen") or []), "updated": d.get("updated")}
else:
    out["steer_bridge"] = "NO SEEN STATE"
drop = ROOT / "queue" / "steer_agent.md"
out["steer_bridge"]["drop_file_lines"] = (len([l for l in drop.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]) if drop.is_file() else 0)

# 9. mailboxes
md = ROOT / "memory" / "mail"
if md.is_dir():
    dirs = [d for d in md.iterdir() if d.is_dir()]
    inboxes = list(md.glob("*/inbox.txt"))
    nonempty = [p for p in inboxes if p.read_text(encoding="utf-8", errors="replace").strip()]
    out["mailboxes"] = {"n_task_dirs": len(dirs), "n_inbox_txt": len(inboxes),
                        "n_nonempty_inbox": len(nonempty)}
else:
    out["mailboxes"] = "NO memory/mail"

# 10. hermes dispatch log
hd = rows(ROOT / "memory" / "runs" / "hermes_dispatch_log.jsonl")
out["hermes"] = {"n": len(hd),
                 "kinds": {k: sum(1 for x in hd if x.get("kind") == k)
                           for k in sorted({str(x.get("kind")) for x in hd})}}

# 11. seat_steer reports
ss = list((ROOT / "memory" / "runs" / "seat_steer").glob("*.json")) if (ROOT / "memory" / "runs" / "seat_steer").is_dir() else []
out["seat_steer_reports"] = len(ss)

# 12. steer telemetry stores
out["steer_engine_telemetry"] = len(rows(ROOT / "memory" / "steer_engine" / "telemetry.jsonl"))
out["steer_telemetry_jsonl"] = len(rows(ROOT / "memory" / "steer_telemetry.jsonl"))

# 13. queue/lanes
lanes = {}
ld = ROOT / "queue" / "lanes"
if ld.is_dir():
    for lane in sorted(d for d in ld.iterdir() if d.is_dir()):
        ib2 = rows(lane / "inbox.jsonl")
        tr = rows(lane / "trail.jsonl")
        lanes[lane.name] = {"inbox_rows": len(ib2), "trail_rows": len(tr)}
out["queue_lanes"] = lanes

# 14. orchestrator tasks + queue
tdir = ROOT / "memory" / "runs" / "orchestrator" / "tasks"
qdir = ROOT / "memory" / "runs" / "orchestrator" / "queue"
statuses = {}
if tdir.is_dir():
    for f in tdir.glob("*.json"):
        try:
            s = str(json.loads(f.read_text(encoding="utf-8", errors="replace")).get("status"))
        except Exception:
            s = "unreadable"
        statuses[s] = statuses.get(s, 0) + 1
out["orchestrator"] = {"task_files": sum(statuses.values()), "statuses": statuses,
                       "queue_files": len(list(qdir.glob("*.json"))) if qdir.is_dir() else 0,
                       "trail_rows": len(rows(ROOT / "memory" / "runs" / "orchestrator_trail.jsonl"))}

# 15. receipt wire lag
rc = (ROOT / "watch" / "steer_bus_receipts.jsonl")
ws = (ROOT / "watch" / "steer_receipt_wire.state")
if rc.is_file() and ws.is_file():
    out["receipt_wire"] = {"receipts_bytes": rc.stat().st_size,
                           "wire_offset": int(ws.read_text(encoding="utf-8").strip() or 0),
                           "unwired_bytes": rc.stat().st_size - int(ws.read_text(encoding="utf-8").strip() or 0)}

# 16. usage log size (lane banking)
ul = ROOT / "logs" / "usage.jsonl"
out["usage_log"] = {"bytes": ul.stat().st_size, "rows_approx": sum(1 for _ in ul.open(encoding="utf-8", errors="ignore"))} if ul.is_file() else "MISSING"

print(json.dumps(out, indent=1, default=str))
