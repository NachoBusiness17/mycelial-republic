#!/usr/bin/env python3
"""tools/redboard.py - one boot-time screen of what is red, for how long, and whose fix it is.

DFHack-style named tool (verb: redboard). Change #4 of
watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md: 8 scheduled tasks red, no
action logged, and memory/attention.md drowned by one alarm class.

  state/REDBOARD.md              the board (meter line first)
  state/REDBOARD.json            same rows, machine form (--json)
  memory/runs/redboard/runs.jsonl one receipt row per run

Sections:
  1. Scheduled tasks named Mag* / Estate* / mag-* (Get-ScheduledTask +
     Get-ScheduledTaskInfo, read-only). Health rule is the census patrol's
     fleet task doctor (scripts/census_patrol_daily.ps1): 0 ok, 267009
     running, 267011 never ran, anything else on an enabled task is red.
     Streak = consecutive red run-days from the task's own log ("END exit=N"
     style lines, else dated FAIL/ERROR lines). Cause = last error-looking
     log line, secrets redacted. Owner = operator when the cause is a missing
     CLI / token / scope / credential / quota, else seat.
  2. memory/attention.md collapsed to counted unique alarm types (top 10).
  3. Stealth driver dead routes: per-topic error rate over the last 200
     ticks of state/fuel/stealth_driver.jsonl.

Self-steal: health codes from the census task doctor; powershell resolution
from scripts/lattice_check.py _ps_exe; noise class from tools/attention_dam.py
(SESSION_HEADING_RE); secret patterns from mag/mind_window.py.
Read-only on everything except its own outputs. Never touches a task.
Stop: create state/redboard.off.

  .venv/Scripts/python.exe tools/redboard.py [--json]
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT_MD = ROOT / "state" / "REDBOARD.md"
OUT_JSON = ROOT / "state" / "REDBOARD.json"
RUNS = ROOT / "memory" / "runs" / "redboard" / "runs.jsonl"
STOP = ROOT / "state" / "redboard.off"
ATTENTION = ROOT / "memory" / "attention.md"
STEALTH = ROOT / "state" / "fuel" / "stealth_driver.jsonl"
OK_CODES = {0: "ok", 267009: "running", 267011: "never ran"}  # census task doctor rule
NAME_RE = r"^(Mag|Estate|mag-)"

try:
    from mag.mind_window import _SECRET_PATTERNS, _is_content_hash  # type: ignore
except Exception:  # noqa: BLE001
    _SECRET_PATTERNS = [(r"sk-[A-Za-z0-9_-]{16,}", "key")]
    _is_content_hash = lambda tok: False  # noqa: E731
_SECRET_RES = [re.compile(p) for p, _ in _SECRET_PATTERNS]
try:
    from tools.attention_dam import SESSION_HEADING_RE  # type: ignore
except Exception:  # noqa: BLE001
    SESSION_HEADING_RE = re.compile(r"^### Session record ready")


def redact(s: str) -> str:
    s = re.sub("[\u2013\u2014\ufffd]+", "-", s)  # no em-dashes law; mojibake collapses too
    for pat in _SECRET_RES:
        s = pat.sub(lambda m: m.group(0) if _is_content_hash(m.group(0).strip()) else "[redacted]", s)
    return s


def ps_exe() -> str:
    try:
        spec = importlib.util.spec_from_file_location("_lattice", ROOT / "scripts" / "lattice_check.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod._ps_exe()
    except Exception:  # noqa: BLE001
        return shutil.which("powershell") or r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"


def get_tasks() -> list[dict]:
    cmd = ("Get-ScheduledTask | Where-Object { $_.TaskName -match '" + NAME_RE + "' } | ForEach-Object { "
           "$i = $_ | Get-ScheduledTaskInfo; $a = $_.Actions | Select-Object -First 1; "
           "[pscustomobject]@{ name=$_.TaskName; state=[string]$_.State; last=[int64]$i.LastTaskResult; "
           "lastrun=$(if($i.LastRunTime){$i.LastRunTime.ToString('s')}else{''}); "
           "exe=[string]$a.Execute; args=[string]$a.Arguments } } | ConvertTo-Json -Compress")
    r = subprocess.run([ps_exe(), "-NoProfile", "-NonInteractive", "-Command", cmd],
                       capture_output=True, text=True, timeout=90,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    raw = (r.stdout or "").strip()
    if not raw:
        return []
    d = json.loads(raw)
    return d if isinstance(d, list) else [d]


def find_log(task: dict) -> list[Path]:
    blob = f"{task.get('exe', '')} {task.get('args', '')}"
    m = re.search(r"([A-Za-z]:\\[^\"\s]+?\.(?:ps1|py))(?=[\"\s]|$)|([\w\\/.-]+\.(?:ps1|py))(?=[\"\s]|$)", blob)
    script = None
    if m:
        p = Path(m.group(1) or m.group(2))
        script = p if p.is_absolute() else ROOT / p
    elif "-m " in blob:
        mod = blob.split("-m ", 1)[1].split()[0]
        script = ROOT / (mod.replace(".", "/") + ".py")
    names: list[str] = []
    if script and script.is_file():
        txt = script.read_text(encoding="utf-8", errors="replace")
        # dated per-day logs, e.g. logs/mates/dispatcher_<YYYYMMDD>.log
        for d, prefix in re.findall(r"logs[\\/](\w+)[\\/](\w+?)_(?:<\w+>|\{)", txt):
            hits = sorted((ROOT / "logs" / d).glob(f"{prefix}_*.log"))
            if hits:
                return hits[-10:]
        names += re.findall(r"logs[\\/]([\w.-]+\.log)", txt)
        names += re.findall(r"Join-Path\s+\$LogDir\s+[\"']([\w.-]+\.log)", txt)
    if script:
        stem = script.stem
        names += [f"{stem}.log", f"{re.sub(r'_(daily|nightly|weekly)$', '', stem)}.log"]
    for n in names:
        p = ROOT / "logs" / n
        if p.is_file():
            return [p]
    return []


def read_tail(p: Path, max_bytes: int = 400_000) -> list[str]:
    with p.open("rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - max_bytes))
        data = f.read()
    return data.replace(b"\x00", b"").decode("utf-8", errors="replace").splitlines()


DATED = re.compile(r"^\[(\d{4}-\d{2}-\d{2})[ T]\d{2}:\d{2}")
END_RE = re.compile(r"\bEND\b(.*)$")
ERR_RE = re.compile(r"FAIL|ERROR|\w*Error\b|Traceback|Exception:|[Cc]annot|[Mm]issing|[Dd]enied|[Ff]orbidden|"
                    r"HTTP [45]\d\d|exit=[1-9]|exit [1-9]|DRIFT|DEAD|[1-9]\d* HARD|seal=[1-9]|"
                    r"\b[A-Z][A-Z0-9-]{3,}: (?!PASS|OK)[A-Z][A-Z-]{3,}(?![A-Za-z:-])")
SKIP_CAUSE = re.compile(r"\bEND\b|ALERT appended|^\s*$|START ")
OPERATOR_RE = re.compile(r"missing .*(cli|\.exe|bin)|missing grok|token|scope\b(?!=)|\bPAT\b|credential|"
                         r"by NAME|--by WHO|"
                         r"\b40[13]\b|permission|login|auth|api[ _-]?key|quota|billing|credit|"
                         r"subscription|password", re.I)


def day_status(lines: list[str]) -> dict[str, bool]:
    """date -> red? Uses END lines when the log has them, else dated error lines."""
    ends: dict[str, bool] = {}
    errs: dict[str, bool] = {}
    for ln in lines:
        m = DATED.match(ln)
        if not m:
            continue
        day = m.group(1)
        e = END_RE.search(ln)
        if e:
            nums = [int(x) for x in re.findall(r"=\s*(-?\d+)", e.group(1))]
            ends[day] = any(n != 0 for n in nums)
        else:
            errs[day] = errs.get(day, False) or bool(ERR_RE.search(ln))
    return ends if ends else errs


def streak(days: dict[str, bool]) -> tuple[int, str | None, str | None]:
    """(consecutive red run-days, first red date of the streak, last green date)."""
    n, first = 0, None
    last_green = None
    for d in sorted(days, reverse=True):
        if days[d]:
            if last_green is None:
                n, first = n + 1, d
        else:
            last_green = d
            break
    return n, first, last_green


def cause_of(lines: list[str]) -> str:
    for ln in reversed(lines[-400:]):
        if SKIP_CAUSE.search(ln):
            continue
        if ERR_RE.search(ln):
            s = " ".join(ln.split())
            return redact(s[:170] + ("..." if len(s) > 170 else ""))
    return ""


def task_rows() -> list[dict]:
    rows = []
    for t in get_tasks():
        code = int(t.get("last") or 0) & 0xFFFFFFFF
        disabled = t.get("state") == "Disabled"
        red = (not disabled) and code not in OK_CODES
        row = {"task": t["name"], "state": t.get("state"), "last_result": code,
               "last_result_hex": f"0x{code:X}", "last_run": t.get("lastrun") or "",
               "red": red, "streak_days": 0, "red_since": None, "last_green": None,
               "cause": "", "owner": "", "log": None}
        logs = find_log(t)
        lines = [ln for lg in logs for ln in read_tail(lg)]
        log = logs[-1] if logs else None
        if log:
            row["log"] = log.relative_to(ROOT).as_posix()
        if red:
            n, first, green = streak(day_status(lines))
            if n == 0:  # no log evidence: count from the last run itself
                n, first = 1, (row["last_run"] or "")[:10] or None
            row.update(streak_days=n, red_since=first, last_green=green)
            c = cause_of(lines)
            if code == 0xC000013A:
                c = c or "0xC000013A: process killed (Ctrl-C / shutdown / logoff) mid-run"
            row["cause"] = c or ("no log found; check the task action" if not log else "no error line in log tail")
            row["owner"] = "operator" if OPERATOR_RE.search(row["cause"]) else "seat"
        rows.append(row)
    rows.sort(key=lambda r: (not r["red"], -r["streak_days"], r["task"]))
    return rows


def alarm_types(top: int = 10) -> tuple[list[dict], int, int]:
    if not ATTENTION.is_file():
        return [], 0, 0
    counts: Counter = Counter()
    last: dict[str, str] = {}
    total = 0
    date_re = re.compile(r"20\d\d-\d\d-\d\d(?:[ T]\d\d:\d\d)?")
    cur_head, head_dates = None, []
    lines = ATTENTION.read_text(encoding="utf-8", errors="replace").splitlines()

    def flush():
        if cur_head:
            if head_dates:
                last[cur_head] = max(last.get(cur_head, ""), max(head_dates))

    for ln in lines:
        if ln.startswith("### "):
            flush()
            head_dates = []
            if SESSION_HEADING_RE.match(ln):
                cur_head = None
                continue
            key = "### " + re.sub(r"\s*\(.*$", "", ln[4:]).strip()
            key = re.sub(r"\d+", "#", key)
            counts[key] += 1
            total += 1
            cur_head = key
            head_dates = date_re.findall(ln)
            continue
        if cur_head:
            head_dates += date_re.findall(ln)
        m = re.match(r"^- (\[[^\]]+\](?:\[[^\]]+\])*)\s*(.*)$", ln)
        if m:
            body = m.group(2).split(" -> ")[0]
            body = re.sub(r"\(run [^)]*\)", "", body)
            body = re.sub(r"20\d\d-\d\d-\d\dT[\d:.]+Z?", "<ts>", body)
            body = re.sub(r"\d+", "#", " ".join(body.split()[:8]))
            key = f"{m.group(1)} {body}".strip()
            counts[key] += 1
            total += 1
            ds = date_re.findall(ln)
            if ds:
                last[key] = max(last.get(key, ""), max(ds))
    flush()
    rows = [{"type": redact(k[:120]), "count": n, "last_seen": last.get(k, "?")}
            for k, n in counts.most_common(top)]
    return rows, len(counts), total


def stealth_routes(n: int = 200) -> list[dict]:
    if not STEALTH.is_file():
        return []
    ticks = []
    for ln in read_tail(STEALTH, 2_000_000)[-n:]:
        try:
            ticks.append(json.loads(ln))
        except Exception:  # noqa: BLE001
            continue
    bad = re.compile(r"\brc=[1-9]|\berror\b|exception|traceback|timed? ?out|\bFAIL|not up|\bdown\b|\bdead\b", re.I)
    tot: Counter = Counter()
    err: Counter = Counter()
    sample: dict[str, str] = {}
    for t in ticks:
        for k, v in (t.get("topics") or {}).items():
            tot[k] += 1
            if bad.search(str(v)):
                err[k] += 1
                sample[k] = " ".join(str(v).split())[:110]
    rows = [{"route": k, "ticks": tot[k], "errors": err[k], "error_rate": round(err[k] / tot[k], 2),
             "dead": err[k] / tot[k] >= 0.9, "last_error": redact(sample.get(k, ""))}
            for k in tot if err[k]]
    rows.sort(key=lambda r: -r["error_rate"])
    return rows


def render(tasks, alarms, n_types, n_lines, routes, now) -> tuple[str, str]:
    red = [t for t in tasks if t["red"]]
    worst = max(red, key=lambda t: t["streak_days"], default=None)
    seat = sum(1 for t in red if t["owner"] == "seat")
    dead = [r for r in routes if r["dead"]]
    meter = (f"METER {len(red)} red | worst streak {worst['streak_days'] if worst else 0}d"
             f"{' (' + worst['task'] + ')' if worst else ''} | {seat} seat-fixable | "
             f"{len(red) - seat} operator-needed | alarms {n_types} types / {n_lines} lines | "
             f"stealth dead routes {len(dead)}")
    L = [meter, "", f"# REDBOARD {now} ET", "",
         "_tools/redboard.py at logon, read-only. Stop: state/redboard.off. JSON: state/REDBOARD.json._", "",
         "## Red scheduled tasks", "",
         "| Task | Last | Streak | Since | Owner | Probable cause | Log |", "|---|---|---|---|---|---|---|"]
    for t in red:
        L.append(f"| {t['task']} | {t['last_result_hex']} | {t['streak_days']}d | {t['red_since'] or '?'} | "
                 f"{t['owner']} | {t['cause'].replace('|', '/')} | {t['log'] or '-'} |")
    if not red:
        L.append("| (none red) | | | | | | |")
    others = [t for t in tasks if not t["red"]]
    L += ["", f"Not red ({len(others)}): " + ", ".join(
        f"{t['task']}={'disabled' if t['state'] == 'Disabled' else OK_CODES.get(t['last_result'], t['last_result_hex'])}"
        for t in others), "",
          f"## attention.md alarm types (top 10 of {n_types}, {n_lines} alarm lines)", "",
          "| Count | Last seen | Alarm type |", "|---|---|---|"]
    L += [f"| {a['count']} | {a['last_seen']} | {a['type'].replace('|', '/')} |" for a in alarms]
    L += ["", "## Stealth driver routes with errors (last 200 ticks)", "",
          "| Route | Error rate | Errors/ticks | Dead | Last error |", "|---|---|---|---|---|"]
    L += [f"| {r['route']} | {r['error_rate']:.0%} | {r['errors']}/{r['ticks']} | {'DEAD' if r['dead'] else ''} | "
          f"{r['last_error'].replace('|', '/')} |" for r in routes] or ["| (no erroring routes) | | | | |"]
    return meter, "\n".join(L) + "\n"


def receipt(row: dict) -> None:
    RUNS.parent.mkdir(parents=True, exist_ok=True)
    with RUNS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="also write state/REDBOARD.json")
    a = ap.parse_args(argv)
    ts = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if STOP.exists():
        print("redboard: stop file state/redboard.off present, exiting")
        receipt({"ts": ts, "tool": "redboard", "status": "stopped", "stop_file": "state/redboard.off"})
        return 0
    now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    try:
        tasks = task_rows()
        task_err = None
    except Exception as e:  # noqa: BLE001 - a broken task read must not blind the other sections
        tasks, task_err = [], f"{type(e).__name__}: {str(e)[:120]}"
    alarms, n_types, n_lines = alarm_types()
    routes = stealth_routes()
    meter, md = render(tasks, alarms, n_types, n_lines, routes, now)
    if task_err:
        md += f"\nTASK READ ERROR: {task_err}\n"
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")
    if a.json:
        OUT_JSON.write_text(json.dumps({"ts": ts, "meter": meter, "tasks": tasks, "alarms": alarms,
                                        "alarm_types": n_types, "alarm_lines": n_lines,
                                        "stealth_routes": routes, "task_error": task_err},
                                       indent=1), encoding="utf-8")
    receipt({"ts": ts, "tool": "redboard", "status": "ok" if not task_err else "partial",
             "meter": meter, "red": [t["task"] for t in tasks if t["red"]]})
    print(meter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
