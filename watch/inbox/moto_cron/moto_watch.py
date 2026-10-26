#!/usr/bin/env python3
"""PC-side watcher / job submitter for moto-cron (SSH over Tailscale)."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLAGS_PATH = HERE / "moto_flags.json"
INBOX_JSONL = HERE / "inbox.jsonl"
STATE_PATH = HERE / ".moto_watch_state.json"

DEFAULT_HOST = "100.102.34.118"
DEFAULT_PORT = 8022
DEFAULT_IDENTITY = str(Path.home() / ".ssh" / "id_ed25519")
STALE_MINUTES = 20
REMOTE_ROOT = "~/moto-cron"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def load_flags() -> dict:
    with FLAGS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def ssh_base(args: argparse.Namespace, *, use_jump: bool = False) -> list[str]:
    cmd = [
        "ssh",
        "-p",
        str(args.port),
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=10",
        "-o",
        "StrictHostKeyChecking=accept-new",
    ]
    jump = getattr(args, "jump", None) or os.environ.get("MOTO_JUMP", "")
    if use_jump and jump:
        # Host alias from PC ~/.ssh/config (e.g. "bob" -> etfag@100.125.103.60)
        cmd += ["-o", f"ProxyJump={jump}"]
    if args.identity:
        cmd += ["-i", args.identity, "-o", "IdentitiesOnly=yes"]
    if args.user:
        target = f"{args.user}@{args.host}"
    else:
        target = args.host
    return cmd, target


def _ssh_failed(p: subprocess.CompletedProcess) -> bool:
    if p.returncode == 0:
        return False
    err = ((p.stderr or "") + (p.stdout or "")).lower()
    # retry jump on reachability / auth / timeout style failures
    needles = ("permission denied", "connection timed out", "connection refused",
               "no route to host", "network is unreachable", "connection reset",
               "timed out", "could not resolve")
    return any(n in err for n in needles) or p.returncode != 0


def run_ssh(args: argparse.Namespace, remote: str, check: bool = False) -> subprocess.CompletedProcess:
    base, target = ssh_base(args, use_jump=False)
    p = subprocess.run(base + [target, remote], capture_output=True, text=True, check=False)
    jump = getattr(args, "jump", None) or os.environ.get("MOTO_JUMP", "bob")
    if _ssh_failed(p) and jump:
        base2, target2 = ssh_base(args, use_jump=True)
        # ensure jump flag is set for ssh_base
        if not getattr(args, "jump", None) and not os.environ.get("MOTO_JUMP"):
            args.jump = jump
            base2, target2 = ssh_base(args, use_jump=True)
        p2 = subprocess.run(base2 + [target2, remote], capture_output=True, text=True, check=False)
        if p2.returncode == 0:
            p2.stderr = (p2.stderr or "") + "\n[moto_watch] used ProxyJump=" + jump
            return p2
    if check and p.returncode != 0:
        p.check_returncode()
    return p


def run_scp_to(args: argparse.Namespace, local: Path, remote_path: str) -> subprocess.CompletedProcess:
    def _scp(use_jump: bool) -> subprocess.CompletedProcess:
        cmd = [
            "scp",
            "-P",
            str(args.port),
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=10",
            "-o",
            "StrictHostKeyChecking=accept-new",
        ]
        jump = getattr(args, "jump", None) or os.environ.get("MOTO_JUMP", "bob")
        if use_jump and jump:
            cmd += ["-o", f"ProxyJump={jump}"]
        if args.identity:
            cmd += ["-i", args.identity, "-o", "IdentitiesOnly=yes"]
        if args.user:
            target = f"{args.user}@{args.host}"
        else:
            target = args.host
        cmd += [str(local), f"{target}:{remote_path}"]
        return subprocess.run(cmd, capture_output=True, text=True)

    p = _scp(False)
    if p.returncode != 0:
        p2 = _scp(True)
        if p2.returncode == 0:
            return p2
    return p


def tailscale_reachable(host: str) -> tuple[bool, str]:
    try:
        p = subprocess.run(
            ["tailscale", "ping", "-c", "1", host],
            capture_output=True,
            text=True,
            timeout=20,
        )
        out = (p.stdout or "") + (p.stderr or "")
        ok = p.returncode == 0 and "pong" in out.lower()
        return ok, out.strip().splitlines()[0] if out.strip() else f"exit={p.returncode}"
    except FileNotFoundError:
        return False, "tailscale CLI not found"
    except Exception as e:
        return False, f"tailscale error: {e}"


def parse_heartbeat(text: str) -> dict:
    data = {}
    for line in text.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data


def heartbeat_age_minutes(hb: dict) -> float | None:
    ts = hb.get("ts")
    if not ts:
        return None
    try:
        # support ...Z
        if ts.endswith("Z"):
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (utc_now() - dt).total_seconds() / 60.0
    except Exception:
        return None


def append_inbox(record: dict) -> None:
    with INBOX_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def cmd_check(args: argparse.Namespace) -> int:
    flags = load_flags()
    ts_ok, ts_msg = tailscale_reachable(args.host)
    print(f"tailscale: {'ok' if ts_ok else 'FAIL'} — {ts_msg}")
    if not ts_ok:
        append_inbox(
            {
                "kind": "alert",
                "notify": "ghost",
                "source": "moto_watch",
                "ts": utc_now().isoformat().replace("+00:00", "Z"),
                "alert": "tailscale_unreachable",
                "detail": ts_msg,
            }
        )
        return 2

    p = run_ssh(args, f"cat {REMOTE_ROOT}/heartbeat 2>/dev/null || echo MISSING")
    if p.returncode != 0:
        err = (p.stderr or p.stdout or "").strip()
        print(f"ssh heartbeat: FAIL — {err}")
        append_inbox(
            {
                "kind": "alert",
                "notify": "ghost",
                "source": "moto_watch",
                "ts": utc_now().isoformat().replace("+00:00", "Z"),
                "alert": "ssh_failed",
                "detail": err[:500],
            }
        )
        return 3

    text = p.stdout or ""
    if "MISSING" in text and "ts=" not in text:
        print("heartbeat: missing")
        append_inbox(
            {
                "kind": "alert",
                "notify": "ghost",
                "source": "moto_watch",
                "ts": utc_now().isoformat().replace("+00:00", "Z"),
                "alert": "heartbeat_missing",
            }
        )
        return 4

    hb = parse_heartbeat(text)
    age = heartbeat_age_minutes(hb)
    print(f"heartbeat: {hb.get('ts')} age_min={age} uptime_sec={hb.get('uptime_sec')} battery={hb.get('battery', '')[:80]}")
    if age is None or age > STALE_MINUTES:
        append_inbox(
            {
                "kind": "alert",
                "notify": "ghost",
                "source": "moto_watch",
                "ts": utc_now().isoformat().replace("+00:00", "Z"),
                "alert": "heartbeat_stale",
                "age_min": age,
                "heartbeat": hb,
            }
        )
        print(f"ALERT: heartbeat stale (>{STALE_MINUTES} min)")
        return 5
    print("heartbeat: fresh")
    # unused but available for tagging
    _ = flags
    return 0


def cmd_pull(args: argparse.Namespace) -> int:
    flags = load_flags()
    state = load_state()
    seen_results = set(state.get("seen_results", []))
    outbox_offset = int(state.get("outbox_offset", 0))

    # list done results
    p = run_ssh(args, f"ls -1 {REMOTE_ROOT}/done/*.result 2>/dev/null || true")
    if p.returncode != 0:
        print("ssh pull list failed:", (p.stderr or "").strip())
        return 3

    new_count = 0
    for line in (p.stdout or "").splitlines():
        remote = line.strip()
        if not remote or remote in seen_results:
            continue
        r = run_ssh(args, f"cat {remote}")
        if r.returncode != 0:
            continue
        body = r.stdout or ""
        meta = {}
        for ln in body.splitlines():
            if ln.startswith("----"):
                break
            if "=" in ln:
                k, v = ln.split("=", 1)
                meta[k.strip()] = v.strip()
        flag = meta.get("flag", "")
        notify = meta.get("notify") or flags.get(flag, "ghost")
        append_inbox(
            {
                "kind": "result",
                "notify": notify,
                "source": "moto_cron",
                "ts": utc_now().isoformat().replace("+00:00", "Z"),
                "remote_path": remote,
                "flag": flag,
                "id": meta.get("id"),
                "exit": meta.get("exit"),
                "summary": meta.get("summary"),
                "start": meta.get("start"),
                "end": meta.get("end"),
                "body": body[:8000],
            }
        )
        seen_results.add(remote)
        new_count += 1
        print(f"pulled result {remote} -> notify={notify}")

    # outbox.log new lines
    o = run_ssh(args, f"wc -c < {REMOTE_ROOT}/outbox.log 2>/dev/null || echo 0")
    try:
        size = int((o.stdout or "0").strip() or "0")
    except ValueError:
        size = 0
    if size > outbox_offset:
        # fetch from offset via dd/tail — simple: cat and slice by prior line count stored
        # We store byte offset; use dd if available
        chunk = run_ssh(
            args,
            f"dd if={REMOTE_ROOT}/outbox.log bs=1 skip={outbox_offset} 2>/dev/null || tail -c +{outbox_offset + 1} {REMOTE_ROOT}/outbox.log",
        )
        data = chunk.stdout or ""
        for ln in data.splitlines():
            parts = ln.split(" ", 5)
            if len(parts) < 5:
                continue
            # ts notify flag id status [summary...]
            notify = parts[1]
            flag = parts[2]
            jid = parts[3]
            status = parts[4]
            summary = parts[5] if len(parts) > 5 else ""
            if not notify or notify == "none":
                notify = flags.get(flag, "ghost")
            append_inbox(
                {
                    "kind": "outbox",
                    "notify": notify,
                    "source": "moto_cron",
                    "ts": parts[0],
                    "flag": flag,
                    "id": jid,
                    "status": status,
                    "summary": summary,
                }
            )
            print(f"outbox {parts[0]} {notify} {flag} {jid} {status}")
        outbox_offset = size

    state["seen_results"] = sorted(seen_results)
    state["outbox_offset"] = outbox_offset
    state["last_pull"] = utc_now().isoformat().replace("+00:00", "Z")
    save_state(state)
    print(f"pull done: {new_count} new results; outbox_offset={outbox_offset}")
    return 0


def submit_job(args: argparse.Namespace, flag: str, payload: str, notify: str | None, job_id: str | None) -> int:
    flags = load_flags()
    if flag not in flags:
        print(f"unknown flag {flag}; known={list(flags)}")
        return 1
    notify = notify or flags[flag]
    job_id = job_id or uuid.uuid4().hex[:12]
    manifest = f"FLAG={flag}\nPAYLOAD={payload}\nNOTIFY={notify}\nID={job_id}\n"
    tmp = HERE / f".submit_{job_id}.job"
    tmp.write_text(manifest, encoding="utf-8", newline="\n")
    remote = f"{REMOTE_ROOT}/jobs/{flag}__{job_id}.job"
    try:
        p = run_scp_to(args, tmp, remote)
        if p.returncode != 0:
            print("scp failed:", (p.stderr or p.stdout or "").strip())
            return 3
        print(f"submitted {remote} notify={notify} id={job_id}")
        append_inbox(
            {
                "kind": "submit",
                "notify": notify,
                "source": "moto_watch",
                "ts": utc_now().isoformat().replace("+00:00", "Z"),
                "flag": flag,
                "id": job_id,
                "payload": payload,
                "remote": remote,
            }
        )
        return 0
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass


def cmd_watch(args: argparse.Namespace) -> int:
    """One-shot check + pull (for schtasks)."""
    rc = cmd_check(args)
    # still attempt pull if ssh worked somehow; check returns non-zero on alerts
    pull_rc = cmd_pull(args)
    # prefer alert rc if any
    if rc != 0:
        return rc
    return pull_rc


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="moto-cron PC watcher")
    p.add_argument("--host", default=os.environ.get("MOTO_HOST", DEFAULT_HOST))
    p.add_argument("--port", type=int, default=int(os.environ.get("MOTO_PORT", DEFAULT_PORT)))
    p.add_argument("--user", default=os.environ.get("MOTO_USER", ""), help="Termux username (whoami on phone)")
    p.add_argument("--identity", default=os.environ.get("MOTO_IDENTITY", DEFAULT_IDENTITY))
    p.add_argument("--jump", default=os.environ.get("MOTO_JUMP", "bob"),
                   help="ssh ProxyJump host alias if direct fails (default: bob; empty to disable)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="heartbeat + tailscale freshness")
    sub.add_parser("pull", help="pull done/*.result and outbox into inbox.jsonl")
    sub.add_parser("watch", help="check then pull (schtasks target)")

    s = sub.add_parser("submit", help="scp a job manifest into jobs/")
    s.add_argument("flag", help="FLAG_FETCH|FLAG_PROBE|FLAG_RENDER|FLAG_SHELL")
    s.add_argument("payload", help="url or command")
    s.add_argument("--notify", default=None)
    s.add_argument("--id", default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "check":
        return cmd_check(args)
    if args.cmd == "pull":
        return cmd_pull(args)
    if args.cmd == "watch":
        return cmd_watch(args)
    if args.cmd == "submit":
        return submit_job(args, args.flag, args.payload, args.notify, args.id)
    return 1


if __name__ == "__main__":
    sys.exit(main())
