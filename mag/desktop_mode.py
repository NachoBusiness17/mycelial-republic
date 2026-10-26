"""desktop_mode - the operator one-liner that freezes the desktop for a game
window and thaws it after.

gene: memory/runs/genetic_burn/20261018/G0/lanes/g03-mode-organ.md (spec, the
parent) + memory/runs/genetic_burn/20261018/G0/GENOME.md (i06 assignment).
Ground truth the moves encode: watch/inbox/DESKTOP_PAUSE_20261017.md (pause
semantics, RESUMED append, crons note, mag-worker unpauser anomaly) and
watch/inbox/DESKTOP_POPUP_QUIET_20261018.md (the three popup sources and the
hidden-launcher contract).

CLI (main.py wiring is a named follow-up; this module is runnable directly):

    python -m mag.desktop_mode game  [--until 4h] [--sweep]
                                     [--seat S --token T] [--no-lease] [--dry]
    python -m mag.desktop_mode burn  [--seat S --token T] [--no-lease] [--dry]
    python -m mag.desktop_mode status [--strict]

`game`  = ONE `docker pause mag-sovereign mag-worker` + operator_mode paused
          (scope all_agents, --until self-heal) + headed-surface scan (sweep
          only with --sweep) + auto receipt watch/inbox/MODE_GAME_<ts>.md
          (schema mode_receipt.v1) + one +60s unpauser-anomaly recheck.
`burn`  = find the open receipt, ONE `docker unpause ...`, health verify (90s
          budget / 10s interval - one healthcheck interval scale), then
          operator_mode.resume, then `## RESUMED` append to the same file.
`status`= the read-only no-headed-surface check: Startup folder + schtasks
          task-XML launcher audit (never edits anything). --strict exits 1 on
          any FLAG.

Exit codes (lab_ctl convention): 0 ok, 1 docker failed, 2 usage, 3 lease
refused.

LEASE PREREQUISITE (fail-closed, named debt): configs/restricted_leases.json
has NO `proc:desktop` resource row yet, so every gated call refuses with the
named error below until the operator lands the row (enforce conflict,
default_ttl_s 7200, max_ttl_s 86400; g03-mode-organ.md section 1). G1 is
forbidden from touching configs, so this module ships fail-closed on purpose.
--no-lease is the OPERATOR-GATED escape: it skips the lease check entirely and
says so in the receipt and the machine log. Never pass it in automation.

CHARTER AMENDED 2026-10-18 (operator: "it needs to be able to pause and resume
cleanly no matter where"): the game-night CPU tasks (MagBoxBurnNightly,
MagProbeCadence) are now PART of the ritual - game disables them, burn re-enables
them, both recorded in the receipt. Still never restarts containers and never
edits a launcher. Control card: watch/inbox/CONTROL_CARD_20261018.md.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from mag import docker_ops
from mag import operator_mode

ROOT = Path(__file__).resolve().parents[1]

TWIN = ("mag-sovereign", "mag-worker")
LEASE_RESOURCE = "proc:desktop"
LEASE_CONFIG = ROOT / "configs" / "restricted_leases.json"
RECEIPT_DIR = ROOT / "watch" / "inbox"
RECEIPT_GLOB = "MODE_GAME_*.md"
RECEIPT_SCHEMA = "mode_receipt.v1"
LEFT_RUNNING = ("gstd-node, tortoise-db, mag-mcp, mag-redis, cluster-factorio, "
                "host ollama, llama-server, scheduled tasks (hidden-wrapped)")

HEALTH_FMT = "{{.State.Health.Status}}"
HEALTH_BUDGET_S = 90
HEALTH_INTERVAL_S = 10
ANOMALY_RECHECK_S = 60
PAUSE_TIMEOUT_S = 60

STATUS_ARGV = ["ps", "-a", "--filter", f"name=^({'|'.join(TWIN)})$",
               "--format", "{{.Names}}\t{{.Status}}"]

EXIT_OK = 0
EXIT_DOCKER = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3

MISSING_ROW_MSG = (
    "FAIL-CLOSED: configs/restricted_leases.json has no 'proc:desktop' resource "
    "row - desktop_mode refuses every gated call until the operator lands it "
    "(resource proc:desktop, enforce conflict, default_ttl_s 7200, max_ttl_s "
    "86400; spec memory/runs/genetic_burn/20261018/G0/lanes/g03-mode-organ.md "
    "section 1). --no-lease is the operator-gated escape and is recorded as "
    "ungated in the receipt; never use it from automation."
)

# ── Part A detection rules (parent ground truth, g03 section 5) ─────────────
VBS_STYLE0_RE = re.compile(r"\.Run\([^)]*,\s*0\s*[,)]")
CMD_DETACHED_RE = re.compile(r'^\s*start\s+""\s+/b(\s|$)', re.IGNORECASE)
CMD_COMMENT_RE = re.compile(r"(?i)^(rem(\s|$)|::|#)")
TASK_FILTER_RE = re.compile(r"(?i)^\\?(mag|mag-)")
CONSOLE_BINARIES = {"powershell.exe", "pwsh.exe", "cmd.exe", "python.exe", "pythonw.exe"}


# ══════════════════════════════ lease ═══════════════════════════════════════

def lease_row_exists(config: Path | None = None) -> bool:
    """True only when the proc:desktop row is live in the restricted list.

    An unreadable config counts as missing: fail closed, never fail open.
    """
    cfg = Path(config) if config else LEASE_CONFIG
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and LEASE_RESOURCE in (data.get("resources") or {})


def _lease_guard(op: str, *, seat: str | None = None, token: str | None = None,
                 no_lease: bool = False) -> dict[str, Any]:
    """The one lease door. Fail-closed on the missing proc:desktop row (a
    missing row is NAMED debt, not a warn-through); conflict-tier otherwise:
    refuses only when ANOTHER seat holds a live lease (g03 section 1)."""
    if no_lease:
        return {"allowed": True, "op": op, "no_lease": True,
                "reason": "operator-gated --no-lease escape: proceeding with no lease check"}
    if not lease_row_exists():
        return {"allowed": False, "refused": True, "op": op, "reason": MISSING_ROW_MSG}
    try:
        from mag.leases import guard
        return guard(LEASE_RESOURCE, op, enforce="conflict", seat=seat, lease_token=token)
    except Exception as e:  # noqa: BLE001 - a broken lease organ must not fail open
        return {"allowed": False, "refused": True, "op": op,
                "reason": f"FAIL-CLOSED: lease guard {LEASE_RESOURCE}/{op} unusable "
                          f"({type(e).__name__}: {e}); configs/restricted_leases.json "
                          f"proc:desktop row required"}


def _seat_name(seat: str | None) -> str:
    return seat or os.environ.get("MAG_LEASE_SEAT") or "operator"


def _lease_summary(g: dict[str, Any]) -> dict[str, Any]:
    return {"resource": LEASE_RESOURCE, "holder": g.get("holder"),
            "until": g.get("until"), "no_lease": bool(g.get("no_lease"))}


def _seat_line(g: dict[str, Any], seat: str) -> str:
    if g.get("no_lease"):
        return f"seat: {seat}  lease: {LEASE_RESOURCE} NONE (--no-lease operator-gated escape)"
    return (f"seat: {seat}  lease: {LEASE_RESOURCE} "
            f"holder={g.get('holder') or seat} until={g.get('until') or '(n/a)'}")


# ══════════════════════════════ docker helpers ══════════════════════════════

def twin_status() -> dict[str, str | None]:
    """Verbatim `docker ps` Status per twin; None where the container is absent."""
    r = docker_ops._run(STATUS_ARGV, timeout=30)
    st: dict[str, str | None] = {n: None for n in TWIN}
    if r.get("ok"):
        for line in (r.get("out") or "").splitlines():
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0] in st:
                st[parts[0]] = parts[1].strip()
    return st


def parse_until(spec: str) -> str:
    """`4h` / `90m` / `3600s` or an ISO timestamp -> ISO-Z UTC deadline."""
    s = (spec or "").strip()
    m = re.fullmatch(r"(\d+)\s*([hms])", s, re.IGNORECASE)
    if m:
        n, unit = int(m.group(1)), m.group(2).lower()
        delta = {"h": timedelta(hours=n), "m": timedelta(minutes=n),
                 "s": timedelta(seconds=n)}[unit]
        return (datetime.now(timezone.utc) + delta).isoformat().replace("+00:00", "Z")
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _poll_health(*, sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic) -> tuple[dict[str, int], dict[str, str], bool]:
    """Poll per-container health AFTER unpause (never while Paused - stale is
    the pause, not a failure). Returns ({name: seconds-to-healthy}, last_seen,
    timed_out)."""
    t0 = clock()
    healthy: dict[str, int] = {}
    last: dict[str, str] = {}
    while True:
        for n in TWIN:
            if n in healthy:
                continue
            r = docker_ops._run(["inspect", "--format", HEALTH_FMT, n], timeout=30)
            val = (r.get("out") or "").strip()
            if not val:
                val = ((r.get("err") or "inspect-failed").splitlines() or ["inspect-failed"])[0][:60]
            last[n] = val
            if val == "healthy":
                healthy[n] = int(clock() - t0)
        if len(healthy) == len(TWIN):
            return healthy, last, False
        if clock() - t0 >= HEALTH_BUDGET_S:
            return healthy, last, True
        sleep(HEALTH_INTERVAL_S)


# ══════════════════════ Part A: launcher audit (read-only) ══════════════════

def _run_tool(argv: list[str], timeout: int = 60) -> str:
    """Run a non-docker tool (schtasks/powershell/taskkill) windowless; stdout only."""
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, creationflags=flags)
    return r.stdout or ""


def audit_vbs(text: str) -> dict[str, str]:
    """PASS iff a `.Run(` carries the literal window-style 0 (run_hidden.vbs:16,
    docker_watchdog.vbs:2 shape). Style 1+ or absent = FLAG."""
    if VBS_STYLE0_RE.search(text or ""):
        return {"verdict": "pass", "reason": ".Run window-style literal 0 (hidden launch)"}
    return {"verdict": "flag", "reason": "no .Run(..., 0, ...) window-style-0 launch found"}


def audit_cmd(text: str) -> dict[str, str]:
    """Every non-comment executable line must launch detached with `start "" /b`
    (mag_boot_lane.cmd convention). A foreground line is the armC console-leak
    disease. Fix comments pass nothing: behavior is what is checked."""
    flagged: list[str] = []
    launches = 0
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line or CMD_COMMENT_RE.match(line):
            continue
        if CMD_DETACHED_RE.match(raw):
            launches += 1
        else:
            flagged.append(line[:120])
    if launches and not flagged:
        return {"verdict": "pass",
                "reason": f"{launches} launch line(s), all `start \"\" /b` detached"}
    if flagged:
        return {"verdict": "flag", "reason": "foreground launch line(s): " + " | ".join(flagged[:3])}
    return {"verdict": "manual", "reason": "no launch lines found; manual review"}


def audit_lnk(name: str) -> dict[str, str]:
    return {"verdict": "manual",
            "reason": ".lnk binary target parse out of scope for v1; manual review"}


def _exec_verdict(cmd: str | None, args_text: str | None) -> dict[str, Any]:
    base = (cmd or "").strip().replace("/", "\\").rsplit("\\", 1)[-1].lower()
    args_l = (args_text or "").lower()
    if base == "wscript.exe":
        if "run_hidden.vbs" in args_l:
            return {"verdict": "pass", "reason": "wscript + run_hidden.vbs hidden wrapper"}
        m = re.search(r'[^\s"]+\.vbs', args_text or "", re.IGNORECASE)
        if not m:
            return {"verdict": "manual", "reason": "wscript without a .vbs reference; manual review"}
        vbs = Path(m.group(0))
        try:
            text = vbs.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return {"verdict": "manual", "reason": f"referenced {vbs} unreadable; manual review"}
        if VBS_STYLE0_RE.search(text):
            return {"verdict": "pass", "reason": f"referenced {vbs.name} launches window-style 0"}
        return {"verdict": "flag", "reason": f"referenced {vbs.name} does not use window-style 0"}
    if base in CONSOLE_BINARIES:
        return {"verdict": "flag",
                "reason": f"{base} runs directly in the task: the console-flash-per-fire "
                          f"disease run_hidden.vbs exists to cure"}
    return {"verdict": "flag",
            "reason": f"command {base or '(none)'} is not the wscript hidden-wrapper shape"}


def audit_task_xml(xml_text: str) -> dict[str, Any]:
    """Parse one schtasks /XML document: enabled flag + per-Exec verdict rows."""
    try:
        root = ET.fromstring(xml_text or "")
    except ET.ParseError as e:
        return {"enabled": True, "rows": [{"command": None, "arguments": None,
                "verdict": "manual", "reason": f"task XML unparseable: {e}"}]}
    enabled = True
    for el in root.iter():
        if el.tag.endswith("Enabled") and (el.text or "").strip().lower() == "false":
            enabled = False
    rows: list[dict[str, Any]] = []
    for ex in (el for el in root.iter() if el.tag.endswith("Exec")):
        cmd = args_text = None
        for child in ex:
            if child.tag.endswith("Command"):
                cmd = (child.text or "").strip()
            elif child.tag.endswith("Arguments"):
                args_text = (child.text or "").strip()
        rows.append({"command": cmd, "arguments": args_text, **_exec_verdict(cmd, args_text)})
    return {"enabled": enabled, "rows": rows}


def parse_task_csv(text: str) -> list[dict[str, str]]:
    """`schtasks /Query /FO CSV /NH` rows: TaskName, Next Run Time, Status."""
    out: list[dict[str, str]] = []
    for row in csv.reader(io.StringIO(text or "")):
        if not row or not row[0].strip():
            continue
        out.append({"name": row[0].strip(),
                    "next_run": row[1].strip() if len(row) > 1 else "",
                    "status": row[2].strip() if len(row) > 2 else ""})
    return out


def list_mag_tasks() -> list[dict[str, str]]:
    try:
        out = _run_tool(["schtasks", "/Query", "/FO", "CSV", "/NH"], timeout=120)
    except Exception:  # noqa: BLE001 - the audit reports, it never raises
        return []
    return [r for r in parse_task_csv(out) if TASK_FILTER_RE.match(r["name"])]


def task_xml(name: str) -> str:
    try:
        return _run_tool(["schtasks", "/Query", "/TN", name, "/XML"], timeout=60)
    except Exception:  # noqa: BLE001
        return ""


def _startup_dirs() -> list[Path]:
    dirs = []
    appdata = os.environ.get("APPDATA")
    programdata = os.environ.get("PROGRAMDATA")
    if appdata:
        dirs.append(Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")
    if programdata:
        dirs.append(Path(programdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "StartUp")
    return [d for d in dirs if d.is_dir()]


def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def launcher_audit(*, startup_dirs: list[Path] | None = None,
                   tasks: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """The no-headed-surface config audit. JSON rows, never edits anything.
    `tasks` rows: {name, status?, enabled?, xml?}; None discovers via schtasks."""
    rows: list[dict[str, Any]] = []
    dirs = startup_dirs if startup_dirs is not None else _startup_dirs()
    for d in dirs:
        for f in sorted(Path(d).iterdir()):
            low = f.name.lower()
            if low.endswith(".disabled") or ".bak" in low:
                continue
            row: dict[str, Any] = {"surface": f"startup:{Path(d).name}", "name": f.name,
                                   "command": str(f)}
            if f.suffix.lower() == ".vbs":
                row.update(audit_vbs(_read_text(f)))
            elif f.suffix.lower() in {".cmd", ".bat"}:
                row.update(audit_cmd(_read_text(f)))
            elif f.suffix.lower() == ".lnk":
                row.update(audit_lnk(f.name))
            else:
                row.update({"verdict": "manual", "reason": "unrecognized startup surface"})
            rows.append(row)
    for t in (tasks if tasks is not None else list_mag_tasks()):
        name = t["name"]
        row = {"surface": "schtasks", "name": name, "command": None}
        if (t.get("status") or "").lower() == "disabled" or t.get("enabled") is False:
            row.update({"verdict": "skipped", "reason": "task is disabled; skipped with a note"})
            rows.append(row)
            continue
        xml_text = t.get("xml")
        if xml_text is None:
            xml_text = task_xml(name)
        parsed = audit_task_xml(xml_text or "")
        if not parsed["enabled"]:
            row.update({"verdict": "skipped", "reason": "task XML says Enabled=false; skipped with a note"})
            rows.append(row)
            continue
        for r in parsed["rows"]:
            rows.append({"surface": "schtasks", "name": name, "command": r.get("command"),
                         "arguments": r.get("arguments"),
                         "verdict": r["verdict"], "reason": r["reason"]})
    return rows


# ══════════════════════ Part B: live popup scan ═════════════════════════════

def classify_surface(row: dict[str, Any]) -> dict[str, str]:
    """Pure classification of one MainWindowTitle row (the 10-18 popup patterns)."""
    name_l = str(row.get("name") or "").lower()
    cmd = str(row.get("cmdline") or "").lower()
    title = str(row.get("title") or "")
    if "chrome" in name_l or "msedge" in name_l:
        if "--headless" in cmd or "--remote-debugging-port=9222" in cmd:
            return {"verdict": "pass", "action": "left",
                    "reason": "headless burner (9222/headless), never touched"}
        return {"verdict": "flag", "action": "kill-candidate",
                "reason": "headed browser window (the 2026-10-18 fullscreen thief, pid 32204 pattern)"}
    if name_l.startswith("cua.agentcursoroverlay"):
        return {"verdict": "flag", "action": "minimize-candidate",
                "reason": "cua-driver overlay, expect ELEVATED (ACCESS DENIED precedent); "
                          "escalate-or-reboot for true cure"}
    if title and (name_l in {"cmd", "conhost"} or name_l.startswith("powershell")
                  or name_l.startswith("python")):
        return {"verdict": "flag", "action": "review",
                "reason": "console-window leak candidate; cross-check the launcher audit before any kill"}
    return {"verdict": "pass", "action": "left", "reason": "no popup pattern"}


def _protected(row: dict[str, Any]) -> str | None:
    cmd = str(row.get("cmdline") or "").lower()
    name_l = str(row.get("name") or "").lower()
    if "--remote-debugging-port=9222" in cmd or "run_hidden.vbs" in cmd:
        return "protected: 9222 burner / scheduled-task wrapper chain"
    for pfx in ("gstd", "factorio", "tortoise"):
        if name_l.startswith(pfx):
            return f"protected allowlist: {pfx}"
    return None


def _ps_surface_scan() -> list[dict[str, Any]]:
    script = ("$ErrorActionPreference='SilentlyContinue';"
              "$out = Get-Process | Where-Object { $_.MainWindowTitle } | ForEach-Object {"
              " $c = Get-CimInstance Win32_Process -Filter \"ProcessId=$($_.Id)\";"
              " [pscustomobject]@{ name=$_.ProcessName; pid=$_.Id; title=$_.MainWindowTitle;"
              " ppid=$c.ParentProcessId; cmdline=$c.CommandLine } };"
              "$out | ConvertTo-Json -Compress")
    try:
        out = _run_tool(["powershell", "-NoProfile", "-Command", script], timeout=120)
        data = json.loads(out) if out.strip() else []
    except Exception as e:  # noqa: BLE001 - a failed scan is a receipt row, not a crash
        return [{"name": "scan-error", "pid": 0, "title": "", "ppid": "",
                 "cmdline": f"{type(e).__name__}: {str(e)[:120]}"}]
    if isinstance(data, dict):
        data = [data]
    return data


def _sweep_action(row: dict[str, Any], runner: Callable[..., str] | None) -> str:
    """--sweep only. taskkill /F non-elevated headed browsers; ShowWindow(6)
    minimize for elevated overlays. Never the protected set. Record refusals."""
    prot = _protected(row)
    if prot:
        return f"left ({prot})"
    plan = row.get("plan")
    pid = row.get("pid")
    run = runner or _run_tool
    try:
        if plan == "kill-candidate":
            run(["taskkill", "/PID", str(pid), "/F"], timeout=30)
            return "killed"
        if plan == "minimize-candidate":
            script = ("$p=Get-Process -Id {pid};"
                      "$sig='[DllImport(\"user32.dll\")] public static extern bool "
                      "ShowWindow(IntPtr hWnd, int nCmdShow);';"
                      "$t=Add-Type -MemberDefinition $sig -Name W -Namespace N -PassThru;"
                      "[void]$t::ShowWindow($p.MainWindowHandle, 6)").format(pid=pid)
            run(["powershell", "-NoProfile", "-Command", script], timeout=30)
            return "minimized"
    except Exception as e:  # noqa: BLE001 - ACCESS DENIED lands verbatim in the receipt
        return f"left (action failed: {type(e).__name__}: {str(e)[:80]})"
    return "left"


def surface_scan(*, sweep: bool = False, ps_rows: list[dict[str, Any]] | None = None,
                 runner: Callable[..., str] | None = None) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for row in (ps_rows if ps_rows is not None else _ps_surface_scan()):
        cls = classify_surface(row)
        f = {**row, "verdict": cls["verdict"], "plan": cls["action"], "reason": cls["reason"],
             "action": "left"}
        if sweep and os.name == "nt":
            f["action"] = _sweep_action(f, runner)
        findings.append(f)
    return {"count": len(findings), "findings": findings}


# ══════════════════════════════ receipts ════════════════════════════════════

def _local_stamp(dt: datetime | None = None) -> str:
    ts = (dt or datetime.now().astimezone())
    return f"{ts:%Y-%m-%d %H:%M} {ts.strftime('%Z') or ts.strftime('%z')}".strip()


def receipt_path_for(stamp: datetime) -> Path:
    return RECEIPT_DIR / f"MODE_GAME_{stamp:%Y%m%d_%H%M}.md"


def find_open_receipt() -> Path | None:
    """Newest MODE_GAME_*.md by mtime, but ONLY if it still lacks `## RESUMED`
    (the open-session marker). A closed newest receipt means no open session."""
    if not RECEIPT_DIR.is_dir():
        return None
    files = sorted(RECEIPT_DIR.glob(RECEIPT_GLOB),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return None
    newest = files[0]
    try:
        text = newest.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return None if "## RESUMED" in text else newest


def _append_receipt(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as h:
        h.write("\n".join(lines).rstrip("\n") + "\n")


def _finding_bullet(f: dict[str, Any]) -> str:
    parent = f.get("ppid") if f.get("ppid") not in (None, "", 0) else "exited"
    return (f"  - {f.get('name')} pid {f.get('pid')} window \"{f.get('title')}\" "
            f"parent {parent} -> {f.get('action')} ({f.get('reason')})")


def _surface_lines(prefix: str, surf: dict[str, Any]) -> list[str]:
    out = [f"{prefix}: {surf['count']} findings"]
    out.extend(_finding_bullet(f) for f in surf.get("findings") or [])
    return out


_NEXT_RUN_FORMATS = ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S")


def _parse_next_run(raw: str) -> datetime | None:
    for fmt in _NEXT_RUN_FORMATS:
        try:
            return datetime.strptime((raw or "").strip(), fmt).astimezone()
        except ValueError:
            continue
    return None


def crons_in_window(start: datetime, end: datetime,
                    tasks: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    tasks = tasks if tasks is not None else list_mag_tasks()
    inside = []
    for t in tasks:
        dt = _parse_next_run(t.get("next_run") or "")
        if dt is not None and start <= dt <= end:
            inside.append({"name": t["name"].lstrip("\\"), "next_run": t["next_run"],
                           "hour": dt.hour})
    return inside


def _crons_note(started: datetime, until_iso: str,
                tasks: list[dict[str, str]] | None = None) -> str:
    try:
        end = datetime.fromisoformat(until_iso.replace("Z", "+00:00")).astimezone()
    except ValueError:
        end = started
    inside = crons_in_window(started.astimezone(), end, tasks=tasks)
    if not inside:
        return "none inside window"
    note = "; ".join(f"{t['name']} @ {t['next_run']}" for t in inside)
    if any(t["hour"] in (7, 8, 9) for t in inside):
        note += " - drain/improve no-op expected, self-heal next cycle"
    return note


# ══════════════════════════════ mode game ═══════════════════════════════════

def _software_pause(until_iso: str) -> dict[str, Any]:
    try:
        return operator_mode.set_paused(reason="game session", scope="all_agents",
                                        until=until_iso)
    except Exception as e:  # noqa: BLE001 - the receipt must record the failure
        return {"mode": "error", "until": until_iso, "error": f"{type(e).__name__}: {e}"}


def _anomaly_recheck(sleep: Callable[[float], None]) -> str:
    """+60s after the freeze: the mag-worker unpauser (DESKTOP_PAUSE lines
    33-39). Found unpaused -> re-pause ONCE, record; still unpaused -> surface,
    never loop (a fight with an unknown healer must surface, not escalate)."""
    sleep(ANOMALY_RECHECK_S)
    st = twin_status()
    unpaused = [n for n in TWIN if st.get(n) and "(Paused)" not in st[n]]
    if not unpaused:
        return "none observed at +60s recheck"
    docker_ops._run(["pause", *unpaused], timeout=PAUSE_TIMEOUT_S)
    st2 = twin_status()
    still = [n for n in unpaused if st2.get(n) and "(Paused)" not in st2[n]]
    docker_ops._log("mode-game-anomaly", containers=unpaused, still_unpaused=still)
    msg = f"unpauser anomaly: {', '.join(unpaused)} found unpaused at +60s; re-paused ONCE"
    if still:
        msg += (f"; STILL unpaused after the re-pause ({', '.join(still)}) - surfacing, "
                "not fighting; stream `docker events --since` during the next window")
    return msg


# ══════════════════════════ the eye (ollama on a CPU-only host) ═════════════
# DESKTOP_PAUSE_20261017.md addendum: this host has no CUDA GPU, so ollama
# loads models into RAM and infers on CPU - any lane touching the eye hitches
# a game. game = eye down (stealth driver flag + ollama stop); burn = eye up.
STEALTH_FLAG = ROOT / "state" / "stealth_driver.off"


def _ollama_exe() -> Path:
    local = os.environ.get("LOCALAPPDATA", "")
    return Path(local) / "Programs" / "Ollama" / "ollama.exe"


def _eye_down() -> str:
    notes: list[str] = []
    try:
        STEALTH_FLAG.parent.mkdir(parents=True, exist_ok=True)
        STEALTH_FLAG.write_text("", encoding="utf-8")
        notes.append("stealth_driver.off set")
    except OSError as e:  # noqa: BLE001
        notes.append(f"stealth flag FAILED ({e})")
    r = _run_tool(["taskkill", "/F", "/IM", "ollama.exe"])
    out = (r or "")
    notes.append("ollama stopped" if "SUCCESS" in out else f"ollama: {out[:60] or 'already down'}")
    # zombie sweep: orphaned probes (killed sessions leave python children running
    # `ollama run <model>` - the 10/19 churn: a "stopped" athena probe respawned
    # the stack for an hour). Kill anything still holding an ollama command line.
    z = _run_tool(["powershell", "-NoProfile", "-Command",
                   "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine "
                   "-match 'ollama run|llama-server' } | ForEach-Object { "
                   "Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"])
    notes.append("zombie sweep: " + ("clean" if z is not None else "failed"))
    return "; ".join(notes)


def _eye_up() -> str:
    notes: list[str] = []
    try:
        if STEALTH_FLAG.exists():
            STEALTH_FLAG.unlink()
            notes.append("stealth_driver.off cleared")
        else:
            notes.append("stealth flag already clear")
    except OSError as e:  # noqa: BLE001
        notes.append(f"stealth clear FAILED ({e})")
    exe = _ollama_exe()
    if exe.exists():
        flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        subprocess.Popen([str(exe), "serve"], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, creationflags=flags)
        notes.append("ollama serve relaunched (detached, boot-lane path)")
    else:
        notes.append("ollama.exe not found; boot lane restores it at next logon")
    return "; ".join(notes)


GAME_NIGHT_TASKS = ["MagBoxBurnNightly", "MagProbeCadence"]


def _flip_tasks(op: str) -> list[str]:
    """Disable (game) or enable (burn) the game-night CPU tasks. Returns the
    flipped names; failures are named, never silent (the pause must stay clean
    no matter where it is asked from)."""
    flipped = []
    for t in GAME_NIGHT_TASKS:
        r = _run_tool(["schtasks", "/Change", "/TN", t, op])
        if r and "SUCCESS" in r:
            flipped.append(t)
    return flipped


def mode_game(*, until: str = "4h", sweep: bool = False, seat: str | None = None,
              token: str | None = None, no_lease: bool = False, dry: bool = False,
              sleep: Callable[[float], None] = time.sleep,
              crons_tasks: list[dict[str, str]] | None = None,
              ps_rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """`crons_tasks=None` discovers the schtasks CSV live; tests pass []."""
    """Pause the desktop twin for a game window. Never restarts anything."""
    g = _lease_guard("mode.game", seat=seat, token=token, no_lease=no_lease)
    if not g.get("allowed"):
        return {"ok": False, "action": "game", "exit_code": EXIT_REFUSED, "refused": True,
                "reason": g.get("reason"), "how": g.get("how"), "lease": _lease_summary(g)}
    seat_name = _seat_name(seat)
    until_iso = parse_until(until)
    pause_argv = ["pause", *TWIN]
    if dry:
        return {"ok": True, "action": "game", "exit_code": EXIT_OK, "dry": True,
                "plan": {"docker": [pause_argv],
                         "software": f"operator_mode.set_paused(reason='game session', "
                                     f"scope='all_agents', until={until_iso})",
                         "sweep": bool(sweep)},
                "lease": _lease_summary(g)}
    started = datetime.now()
    path = receipt_path_for(started)
    result: dict[str, Any] = {"ok": False, "action": "game", "exit_code": EXIT_DOCKER,
                              "receipt": str(path), "lease": _lease_summary(g)}
    body: list[str] = []

    def seal(exit_code: int, ok: bool) -> None:
        # The receipt lands even on partial failure: a pause that half-worked is
        # exactly when the record matters most.
        result["exit_code"] = exit_code
        result["ok"] = ok
        _append_receipt(path, body)
        result["receipt"] = str(path)
        if ok:
            docker_ops._log("mode-game-done", ok=True, seat=seat_name, receipt=str(path))

    body.append(f"# MODE GAME - {_local_stamp(started)} (operator ask)")
    body.append(f"schema: {RECEIPT_SCHEMA}")
    body.append(_seat_line(g, seat_name))
    if not docker_ops.engine_reachable():
        body.append("engine: not reachable; ensure_engine attempt")
        eng = docker_ops.ensure_engine()
        if not eng.get("engine_reachable"):
            body.append(f"engine: STILL DOWN after ensure_engine ({eng.get('waited_s')}s); abort")
            seal(EXIT_DOCKER, False)
            return result
    body.append("engine: reachable")
    pre = twin_status()
    missing = [n for n in TWIN if pre.get(n) is None]
    if missing:
        body.append(f"containers: MISSING {', '.join(missing)} - a pause of a half-twin "
                    "is a half desktop; abort")
        seal(EXIT_DOCKER, False)
        return result
    for n in TWIN:
        body.append(f"  {n + ':':<15}{pre[n]} -> Paused")
    r = docker_ops._run(pause_argv, timeout=PAUSE_TIMEOUT_S)
    docker_ops._log("mode-game-pause", ok=bool(r.get("ok")), containers=list(TWIN),
                    seat=seat_name, receipt=str(path))
    if not r.get("ok"):
        body.append(f"freeze: FAILED - {(r.get('err') or r.get('out') or 'unknown')[:200]}")
        seal(EXIT_DOCKER, False)
        return result
    body.append("freeze: ONE `docker pause mag-sovereign mag-worker` ok "
                "(SIGSTOP semantics; no restart, no port rebind)")
    software = _software_pause(until_iso)
    body.append(f"software: operator_mode paused scope=all_agents until={software.get('until')}")
    body.append(f"eye: {_eye_down()}")
    flipped = _flip_tasks("/DISABLE")
    body.append("crons disabled: " + (", ".join(flipped) if flipped else "none (already off)"))
    result["crons_disabled"] = flipped
    surf = surface_scan(sweep=sweep, ps_rows=ps_rows)
    body.extend(_surface_lines("surface", surf))
    body.append(f"left_running: {LEFT_RUNNING}")
    crons = _crons_note(started, software.get("until") or until_iso, tasks=crons_tasks)
    body.append(f"crons in window: {crons}")
    body.append(f"anomaly: {_anomaly_recheck(sleep)}")
    result["containers"] = {n: f"{pre[n]} -> Paused" for n in TWIN}
    result["surface"] = surf["count"]
    result["software"] = {"scope": "all_agents", "until": software.get("until")}
    result["crons"] = crons
    seal(EXIT_OK, True)
    return result


# ══════════════════════════════ mode burn ═══════════════════════════════════

def mode_burn(*, seat: str | None = None, token: str | None = None,
              no_lease: bool = False, dry: bool = False,
              sleep: Callable[[float], None] = time.sleep,
              clock: Callable[[], float] = time.monotonic,
              ps_rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Unpause, health-verify (one healthcheck-interval scale), then resume the
    software pause and append `## RESUMED` to the open receipt. Idempotent."""
    g = _lease_guard("mode.burn", seat=seat, token=token, no_lease=no_lease)
    if not g.get("allowed"):
        return {"ok": False, "action": "burn", "exit_code": EXIT_REFUSED, "refused": True,
                "reason": g.get("reason"), "how": g.get("how"), "lease": _lease_summary(g)}
    seat_name = _seat_name(seat)
    unpause_argv = ["unpause", *TWIN]
    if dry:
        return {"ok": True, "action": "burn", "exit_code": EXIT_OK, "dry": True,
                "plan": {"docker": [unpause_argv],
                         "health": f"poll to {HEALTH_BUDGET_S}s every {HEALTH_INTERVAL_S}s, "
                                   f"then operator_mode.resume",
                         "receipt": "append ## RESUMED to the open MODE_GAME_*.md"},
                "lease": _lease_summary(g)}
    receipt = find_open_receipt()
    if receipt is None:
        return {"ok": False, "action": "burn", "exit_code": EXIT_USAGE,
                "reason": f"no open game-session receipt (a {RECEIPT_GLOB} without a "
                          f"`## RESUMED` marker) under {RECEIPT_DIR}"}
    result: dict[str, Any] = {"ok": False, "action": "burn", "exit_code": EXIT_DOCKER,
                              "receipt": str(receipt), "lease": _lease_summary(g)}
    pre = twin_status()
    missing = [n for n in TWIN if pre.get(n) is None]
    if missing:
        result["reason"] = f"missing containers: {', '.join(missing)}"
        return result
    body = [f"## RESUMED - {_local_stamp()}"]
    r = docker_ops._run(unpause_argv, timeout=PAUSE_TIMEOUT_S)
    docker_ops._log("mode-burn-unpause", ok=bool(r.get("ok")), containers=list(TWIN),
                    seat=seat_name, receipt=str(receipt))
    if not r.get("ok"):
        body.append(f"unpause FAILED - {(r.get('err') or 'unknown')[:200]}")
        _append_receipt(receipt, body)
        result["reason"] = "unpause failed"
        return result
    body.append("unpause ok")
    already = [n for n in TWIN if "(Paused)" not in (pre[n] or "")]
    if already:
        body.append(f"note: {', '.join(already)} was already Running (not Paused) on entry "
                    "(idempotent resume; unpauser-anomaly watch)")
    healthy, last, timed_out = _poll_health(sleep=sleep, clock=clock)
    if timed_out:
        body.append(f"health: NOT healthy within {HEALTH_BUDGET_S}s - "
                    + "; ".join(f"{n}={last.get(n)}" for n in TWIN)
                    + " (operator: docker logs; this command never restarts anything)")
        _append_receipt(receipt, body)
        result["health"] = last
        result["reason"] = "health verify timed out"
        return result
    body.append("health: " + "; ".join(f"{n} healthy in {healthy[n]}s" for n in TWIN))
    try:
        operator_mode.resume(reason="game session over")
        body.append("software: operator_mode resumed")
        result["software"] = "resumed"
    except Exception as e:  # noqa: BLE001 - the operator must see this in the receipt
        body.append(f"software: operator_mode RESUME FAILED ({type(e).__name__}: {e})")
        result["software"] = "resume-failed"
    body.append(f"eye: {_eye_up()}")
    flipped = _flip_tasks("/ENABLE")
    body.append("crons re-enabled: " + (", ".join(flipped) if flipped else "none"))
    result["crons_re_enabled"] = flipped
    surf = surface_scan(sweep=False, ps_rows=ps_rows)
    body.extend(_surface_lines("surface after", surf))
    _append_receipt(receipt, body)
    result["health"] = healthy
    result["surface"] = surf["count"]
    result["exit_code"] = EXIT_OK
    result["ok"] = True
    docker_ops._log("mode-burn-done", ok=True, seat=seat_name, receipt=str(receipt))
    return result


# ══════════════════════════════ mode status ═════════════════════════════════

def mode_status(*, strict: bool = False, startup_dirs: list[Path] | None = None,
                tasks: list[dict[str, Any]] | None = None,
                statuses: dict[str, str | None] | None = None) -> dict[str, Any]:
    """Read-only: operator mode + twin statuses + the no-headed-surface audit.
    No lease. --strict exits 1 when any FLAG is standing (redboard alarm seed)."""
    rows = launcher_audit(startup_dirs=startup_dirs, tasks=tasks)
    flags = sum(1 for r in rows if r.get("verdict") == "flag")
    out: dict[str, Any] = {"ok": True, "action": "status", "exit_code": EXIT_OK,
                           "operator_mode": operator_mode.read(),
                           "containers": statuses if statuses is not None else twin_status(),
                           "surfaces": rows, "flag_count": flags}
    if strict and flags:
        out["exit_code"] = EXIT_DOCKER
        out["reason"] = f"{flags} FLAG row(s) under --strict"
    return out


# ══════════════════════════════ CLI ═════════════════════════════════════════

def _print_surface_table(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    print()
    print(f"{'surface':<22} {'name':<28} {'verdict':<8} reason")
    for r in rows:
        print(f"{str(r.get('surface')):<22} {str(r.get('name')):<28} "
              f"{str(r.get('verdict')):<8} {str(r.get('reason'))[:100]}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="desktop_mode",
                                 description="pause the desktop twin for a game window and restore it")
    sub = ap.add_subparsers(dest="mode", required=True)
    pg = sub.add_parser("game", help="docker pause the twin + software pause + surface report + receipt")
    pg.add_argument("--until", default="4h",
                    help="software-pause TTL, e.g. 4h / 90m (abandoned windows self-heal)")
    pg.add_argument("--sweep", action="store_true",
                    help="act on popup findings (default: report-only)")
    pg.add_argument("--seat", default=None, help="default env MAG_LEASE_SEAT")
    pg.add_argument("--token", default=None, help="default env MAG_LEASE_TOKEN")
    pg.add_argument("--no-lease", action="store_true",
                    help="OPERATOR-GATED escape: skip the proc:desktop lease check entirely")
    pg.add_argument("--dry", action="store_true", help="lease-check, print the plan, run nothing")
    pb = sub.add_parser("burn", help="unpause + health verify + software resume + RESUMED append")
    pb.add_argument("--seat", default=None)
    pb.add_argument("--token", default=None)
    pb.add_argument("--no-lease", action="store_true",
                    help="OPERATOR-GATED escape: skip the proc:desktop lease check entirely")
    pb.add_argument("--dry", action="store_true", help="lease-check, print the plan, run nothing")
    pst = sub.add_parser("status", help="read-only no-headed-surface audit (no lease)")
    pst.add_argument("--strict", action="store_true", help="exit 1 on any FLAG row")
    a = ap.parse_args(argv)
    if a.mode == "game":
        out = mode_game(until=a.until, sweep=a.sweep, seat=a.seat, token=a.token,
                        no_lease=a.no_lease, dry=a.dry)
    elif a.mode == "burn":
        out = mode_burn(seat=a.seat, token=a.token, no_lease=a.no_lease, dry=a.dry)
    else:
        out = mode_status(strict=a.strict)
    print(json.dumps(out, indent=1, default=str))
    if a.mode == "status":
        _print_surface_table(out.get("surfaces") or [])
    return int(out.get("exit_code", EXIT_DOCKER))


if __name__ == "__main__":
    raise SystemExit(main())
