#!/usr/bin/env python3
"""cockpit -- one deterministic readout of the estate, plus the one next action.

Hermes seat, 2026-10-21, operator order: "help me drive the estate better...
everything else seems to stutter... this is hermes as a cockpit."

The estate already has every organ (commit_sweeper, fossil_check, percolator
audit, falsifier lint, multi-smoke, verkle chain, schtasks). What it lacked was
ONE call that answers, in ten seconds: what is true, what is stuck, what is
next. This composes the organs; it invents no monitor and writes nothing.

    python tools/cockpit.py            # human readout + next action
    python tools/cockpit.py --json     # machine receipt
    python tools/cockpit.py --html out.html

Exit ladder: 0 all green, 1 attention needed, 2 cannot verify (never a guess).

Stutter model (what we are actually detecting):
  - the index is locked by a dead or wedged writer        -> git lock age
  - the sweeper has not landed anything while work exists  -> dirty vs last commit
  - a scheduled cycle is silently failing                  -> last task exit
  - a promoted invariant has been falsified                -> falsifier lint
  - the daily health check went stale                      -> smoke age
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "Scripts" / "python.exe"
PY = PY if PY.exists() else Path(sys.executable)

STALE_LOCK_S = 600        # an index.lock older than this with no commit moving is wedged
STALL_MIN = 30            # dirty work older than this with no commit = sweeper stalled
SMOKE_FRESH_H = 26
CHAIN_FRESH_H = 6


def _ts(value) -> datetime | None:
    if not value:
        return None
    try:
        raw = str(value).replace("Z", "+00:00")
        # schtasks writes 7 fractional digits ("...13.1399123-04:00"); fromisoformat
        # accepts 3 or 6, and a silent None made the sweeper read "0m ago" forever.
        raw = re.sub(r"\.(\d{6})\d+", r".\1", raw)
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _age_h(stamp: datetime | None) -> float | None:
    if stamp is None:
        return None
    return (datetime.now(timezone.utc) - stamp).total_seconds() / 3600.0


def sh(args: list[str], cwd: Path = ROOT, timeout: int = 60) -> tuple[int, str]:
    try:
        p = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as exc:  # noqa: BLE001 - a signal, never a crash
        return 127, str(exc)


CACHE = ROOT / "state" / "cockpit_cache.json"
CACHE_TTL = {"git": 15, "sweeper": 5, "chain": 10, "fossil": 900,
             "percolator": 180, "falsifier": 180, "smoke": 10, "tasks": 60}
_REFRESH = False


def _load_cache() -> dict:
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def _save_cache(cache: dict) -> None:
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps(cache), encoding="utf-8")
        tmp.replace(CACHE)
    except OSError:
        pass


def cached(name: str, fn) -> dict:
    """Slow organs are cached by TTL so the cockpit is a glance, not a wait.

    Measured 2026-10-21: fossil_check 21s, percolator audit 14s, falsifier 10s,
    git status 5s. A cockpit you avoid opening is not a cockpit.
    """
    global _REFRESH
    cache = _load_cache()
    ttl = CACHE_TTL.get(name, 60)
    hit = cache.get(name)
    if hit and not _REFRESH and (time.time() - hit.get("ts", 0)) < ttl:
        sig_ = dict(hit["sig"])
        sig_["measured_ago_s"] = round(time.time() - hit["ts"])
        return sig_
    sig_ = fn()
    cache[name] = {"ts": time.time(), "sig": sig_}
    _save_cache(cache)
    sig_["measured_ago_s"] = 0
    return sig_


def sig(name: str, status: str, detail: str, **extra) -> dict:
    return {"name": name, "status": status, "detail": detail, **extra}


# ── signals ---------------------------------------------------------------

def git_signal() -> dict:
    rc, out = sh(["git", "status", "--porcelain"])
    if rc != 0:
        return sig("git", "red", f"git status failed: {out.strip()[:80]}")
    dirty = len([ln for ln in out.splitlines() if ln.strip()])
    rc, tip = sh(["git", "log", "-1", "--format=%ct|%h|%s"])
    last_commit = None
    subject = ""
    if rc == 0 and "|" in tip:
        parts = tip.strip().split("|", 2)
        last_commit = datetime.fromtimestamp(int(parts[0]), tz=timezone.utc)
        subject = parts[2][:70] if len(parts) > 2 else ""
    lock = ROOT / ".git" / "index.lock"
    lock_age = (time.time() - lock.stat().st_mtime) if lock.exists() else None
    commit_age_min = (_age_h(last_commit) or 0) * 60
    status = "ok"
    why = f"{dirty} dirty, last commit {commit_age_min:.0f}m ago"
    if lock_age is not None and lock_age > STALE_LOCK_S and commit_age_min > STALL_MIN:
        status = "red"
        why = f"index.lock {lock_age/60:.0f}m old with no commit for {commit_age_min:.0f}m"
    elif dirty and commit_age_min > STALL_MIN:
        status = "red"
        why = f"{dirty} files uncommitted, no commit for {commit_age_min:.0f}m (sweeper stalled)"
    elif dirty:
        status = "warn"
        why = f"{dirty} files waiting on the next sweep (last commit {commit_age_min:.0f}m)"
    return sig("git", status, why, dirty=dirty, last_commit=subject,
               commit_age_min=round(commit_age_min, 1),
               lock_age_s=None if lock_age is None else round(lock_age))


def sweeper_signal() -> dict:
    log = ROOT / "logs" / "commit_sweeper_task.log"
    if not log.is_file():
        return sig("sweeper", "warn", "no task log (never ran under schtasks)")
    text = log.read_text(encoding="utf-8", errors="replace").replace("\x00", "")
    exits = re.findall(r"sweep exit (-?\d+)", text)
    starts = re.findall(r"===\s*(\S+)\s+sweep start", text)
    last_start = _ts(starts[-1]) if starts else None
    last_exit = exits[-1] if exits else "?"
    age_min = (_age_h(last_start) or 0) * 60
    status = "ok" if last_exit == "0" else "warn"
    if last_start and age_min > 25:
        status = "red"
    return sig("sweeper", status,
               f"last start {age_min:.0f}m ago, exit {last_exit}",
               last_exit=last_exit, age_min=round(age_min, 1))


def chain_signal() -> dict:
    chain = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
    if not chain.is_file():
        return sig("chain", "warn", "no chain file")
    try:
        with chain.open("rb") as fh:
            fh.seek(0, 2)
            size = fh.tell()
            fh.seek(max(0, size - 4096))
            tail = fh.read().decode("utf-8", "replace")
        line = [ln for ln in tail.splitlines() if ln.strip()][-1]
        row = json.loads(line)
        stamp = _ts(row.get("ts") or row.get("timestamp"))
        age = _age_h(stamp)
        status = "ok" if (age is None or age <= CHAIN_FRESH_H) else "warn"
        return sig("chain", status,
                   f"leaf {row.get('index', '?')} root {str(row.get('verkle_root', ''))[:12]}… "
                   f"{'?' if age is None else f'{age:.1f}h'} old",
                   index=row.get("index"))
    except Exception as exc:  # noqa: BLE001
        return sig("chain", "warn", f"chain tail unreadable: {str(exc)[:60]}")


def fossil_signal() -> dict:
    rc, out = sh([str(PY), "tools/fossil_check.py"], timeout=90)
    hard = len(re.findall(r"^\s*-\s*FOSSIL-CHECK: HARD", out, re.M))
    warn = len(re.findall(r"^\s*-\s*FOSSIL-CHECK: WARN", out, re.M))
    if rc == 127:
        return sig("fossil", "warn", "fossil_check unavailable")
    status = "red" if hard else ("warn" if warn else "ok")
    return sig("fossil", status, f"{warn} WARN, {hard} HARD", warn=warn, hard=hard)


def percolator_signal() -> dict:
    rc, out = sh([str(PY), "tools/invariant_percolator_audit.py", "--promoted-only", "--json"],
                 timeout=90)
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return sig("percolator", "warn", "audit unreadable")
    gates = {g["id"]: g["ok"] for g in data.get("gates", [])}
    failed = [g for g, ok in gates.items() if not ok]
    stats = data.get("stats", {})
    status = "ok" if not failed else ("warn" if failed == ["I5"] else "red")
    detail = f"{len(gates) - len(failed)}/{len(gates)} gates; live {stats.get('explore_live', '?')}/{stats.get('explore_rows', '?')}"
    if failed:
        detail += f"; failing {', '.join(failed)}"
    return sig("percolator", status, detail, failed=failed, stats=stats)


def falsifier_signal() -> dict:
    rc, out = sh([str(PY), "tools/falsifier_lint.py", "--json"], timeout=90)
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return sig("falsifier", "warn", "lint unreadable")
    c = data.get("counts", {})
    status = "red" if c.get("FAIL") else "ok"
    return sig("falsifier", status,
               f"{c.get('PASS', 0)} PASS / {c.get('FAIL', 0)} FAIL / "
               f"{c.get('UNMEASURED', 0)} UNMEASURED", counts=c)


def smoke_signal() -> dict:
    path = ROOT / "logs" / "multi_smoke_latest.json"
    if not path.is_file():
        return sig("smoke", "warn", "no smoke on disk")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return sig("smoke", "warn", "smoke unreadable")
    stamp = _ts(data.get("ts"))
    age = _age_h(stamp)
    ok = bool(data.get("ok"))
    status = "ok" if ok and (age or 0) <= SMOKE_FRESH_H else ("warn" if ok else "red")
    return sig("smoke", status,
               f"{'PASS' if ok else 'FAIL'}, {'?' if age is None else f'{age:.1f}h'} old",
               ok=ok, age_h=None if age is None else round(age, 1))


def task_signal() -> dict:
    rc, out = sh(["schtasks", "/query", "/tn", "MagCommitSweeper", "/fo", "LIST", "/v"],
                 timeout=45)
    if rc != 0:
        return sig("tasks", "warn", "MagCommitSweeper not queryable")
    state = re.search(r"Scheduled Task State:\s*(\w+)", out)
    status = "ok" if state and state.group(1).lower() == "enabled" else "warn"
    return sig("tasks", status, f"MagCommitSweeper {state.group(1) if state else '?'}")


SIGNALS = [git_signal, sweeper_signal, chain_signal, fossil_signal,
           percolator_signal, falsifier_signal, smoke_signal, task_signal]


# ── the one next action ---------------------------------------------------

def next_action(signals: dict[str, dict]) -> dict:
    g = signals.get("git", {})
    if g.get("status") == "red" and "index.lock" in g.get("detail", ""):
        return {"id": "clear-stale-lock", "why": g["detail"],
                "do": "python tools/commit_sweeper.py sweep  (after confirming no git.exe holds it)"}
    if g.get("status") == "red":
        return {"id": "unstick-sweeper", "why": g["detail"],
                "do": "python tools/commit_sweeper.py sweep; check logs/commit_sweeper.log tail"}
    if signals.get("falsifier", {}).get("status") == "red":
        return {"id": "falsified-invariant", "why": signals["falsifier"]["detail"],
                "do": "python tools/falsifier_lint.py  (trace the row to its producer before acting)"}
    if signals.get("smoke", {}).get("status") == "red":
        return {"id": "smoke-red", "why": signals["smoke"]["detail"],
                "do": "python main.py multi-smoke"}
    if signals.get("fossil", {}).get("hard"):
        return {"id": "fossil-hard", "why": signals["fossil"]["detail"],
                "do": "python tools/fossil_check.py  (recompile or tombstone per registry)"}
    perc = signals.get("percolator", {})
    if "I5" in (perc.get("failed") or []):
        return {"id": "i5-leaf-gate", "why": "promoted invariants are a leaf set; I5 asks for graph edges",
                "do": "redesign I5 as leaf-or-declared (wave 7), not '10% must declare'"}
    live = (perc.get("stats") or {}).get("explore_live") or 0
    if live > 1000:
        return {"id": "explore-consumer", "why": f"{live} live explore rows with no consumer",
                "do": "build the explore consumer (cluster live rows -> candidates)"}
    if signals.get("smoke", {}).get("status") == "warn":
        return {"id": "smoke-stale", "why": signals["smoke"]["detail"],
                "do": "python main.py multi-smoke"}
    return {"id": "clear", "why": "no blockers", "do": "pick the field brief's top ticket"}


def collect() -> dict:
    signals = {}
    for fn in SIGNALS:
        s = cached(fn.__name__.replace("_signal", ""), fn)
        signals[s["name"]] = s
    worst = "ok"
    for s in signals.values():
        if s["status"] == "red":
            worst = "red"
            break
        if s["status"] == "warn":
            worst = "warn"
    return {"schema": "cockpit.v1", "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": worst, "next": next_action(signals), "signals": signals}


def render_text(state: dict) -> str:
    icon = {"ok": "OK  ", "warn": "WARN", "red": "RED "}
    lines = [f"ESTATE {state['ts']}  status={state['status'].upper()}"]
    for s in state["signals"].values():
        lines.append(f"  {icon[s['status']]} {s['name']:11s} {s['detail']}")
    n = state["next"]
    lines.append(f"NEXT  [{n['id']}] {n['why']}")
    lines.append(f"      {n['do']}")
    return "\n".join(lines)


HTML = """<!doctype html><html><head><meta charset="utf-8"><title>cockpit</title>
<style>body{font:13px/1.45 ui-monospace,Menlo,monospace;color:var(--foreground,#e6e6e6);margin:0}
h1{font-size:14px;margin:0 0 10px;letter-spacing:.08em;text-transform:uppercase}
.row{display:grid;grid-template-columns:64px 110px 1fr;gap:8px;padding:4px 0;border-bottom:1px solid var(--border,#2a2a2a)}
.ok{color:#4ade80}.warn{color:#fbbf24}.red{color:#f87171}
.next{margin-top:12px;padding:10px;border:1px solid var(--border,#2a2a2a);border-radius:6px}
code{color:var(--muted-foreground,#9ca3af)}</style></head><body>
<h1>estate cockpit</h1><div id="rows"></div><div class="next" id="next"></div>
<script>
const d=__DATA__;
document.getElementById('rows').innerHTML=Object.values(d.signals).map(s=>
 `<div class="row"><span class="${s.status}">${s.status.toUpperCase()}</span><span>${s.name}</span><span>${s.detail}</span></div>`).join('');
document.getElementById('next').innerHTML=
 `<div><strong>NEXT</strong> [${d.next.id}] ${d.next.why}</div><div><code>${d.next.do}</code></div>`;
</script></body></html>"""


def render_html(state: dict) -> str:
    return HTML.replace("__DATA__", json.dumps(state))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="One deterministic estate readout + next action")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--html", default=None, metavar="PATH")
    ap.add_argument("--quiet", action="store_true", help="exit code only")
    ap.add_argument("--refresh", action="store_true",
                    help="ignore the TTL cache (fossil/percolator/falsifier are slow)")
    args = ap.parse_args(argv)

    global _REFRESH
    _REFRESH = args.refresh
    state = collect()
    if args.html:
        Path(args.html).write_text(render_html(state), encoding="utf-8")
    if args.json:
        print(json.dumps(state, indent=2))
    elif not args.quiet:
        print(render_text(state))
    return 0 if state["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
