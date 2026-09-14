#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lan_proxy.py -- persistent LAN TCP forwarder for the sovereign fleet (host side).

WHAT IT DOES
    192.168.86.35:8765  ->  127.0.0.1:8765   dashboard upstream
    192.168.86.35:8001  ->  127.0.0.1:8001   mag MCP gateway (X-API-Key protected)

    Pure Python stdlib, no admin rights, no netsh portproxy. Each accepted
    connection is piped bidirectionally with two threads; a dead upstream only
    kills that one connection, and a listener that loses its socket rebinds
    itself after 5s. Survives the console/agent session that started it.

HOW TO START
    dashboard\\lan_start.cmd                    (double-click, or from any shell)
    -- equivalent: python dashboard\\lan_proxy.py start
    `start` spawns a detached copy of itself (`run`) and returns immediately.
    PID is recorded in dashboard\\lan_proxy.pid; log in dashboard\\lan_proxy.log.

HOW TO STOP
    python dashboard\\lan_proxy.py stop
    -- or: dashboard\\lan_start.cmd stop
    Stop refuses to kill a PID that is not python (guards against PID reuse).

STATUS / RESTART
    python dashboard\\lan_proxy.py status
    python dashboard\\lan_proxy.py restart

SECURITY CAVEAT
    LAN-only, NOT internet. The 8765 hop has NO authentication -- anything on
    the home network can reach the dashboard through it. The 8001 MCP hop is
    only as strong as the gateway's X-API-Key check. The perimeter is the
    ROUTER'S FIREWALL: never port-forward 8765/8001 on it, treat guest Wi-Fi
    as hostile. Fleet law unchanged -- fleet services stay loopback-only in
    Docker; this host-side proxy is the single deliberate bridge and binds
    ONLY the LAN IP (never 0.0.0.0). If the LAN IP changes (DHCP), set
    LAN_PROXY_BIND_IP or let the auto-detect fallback pick the new one.
"""

import ctypes
import os
import signal
import socket
import subprocess
import sys
import threading
import time

BIND_IP = os.environ.get("LAN_PROXY_BIND_IP", "192.168.86.35")
FORWARDS = [
    (8765, "127.0.0.1", 8765, "dashboard upstream"),
    (8001, "127.0.0.1", 8001, "mag MCP gateway (X-API-Key)"),
]
HERE = os.path.dirname(os.path.abspath(__file__))
PIDFILE = os.path.join(HERE, "lan_proxy.pid")
LOGFILE = os.path.join(HERE, "lan_proxy.log")
BUF = 65536
IS_WIN = os.name == "nt"

_log_lock = threading.Lock()


def log(msg):
    line = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + msg
    print(line, flush=True)
    try:
        with _log_lock:
            if os.path.exists(LOGFILE) and os.path.getsize(LOGFILE) > 5 * 1024 * 1024:
                os.replace(LOGFILE, LOGFILE + ".1")
            with open(LOGFILE, "a", encoding="utf-8", errors="replace") as f:
                f.write(line + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------- pid helpers

def _read_pid():
    try:
        with open(PIDFILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return None


def _rm_pid():
    try:
        os.remove(PIDFILE)
    except OSError:
        pass


def _pid_alive(pid):
    if not pid or pid <= 0:
        return False
    if IS_WIN:
        k32 = ctypes.windll.kernel32
        SYNCHRONIZE = 0x00100000
        h = k32.OpenProcess(SYNCHRONIZE, False, int(pid))
        if not h:
            return False
        try:
            WAIT_TIMEOUT = 0x00000102
            return k32.WaitForSingleObject(h, 0) == WAIT_TIMEOUT
        finally:
            k32.CloseHandle(h)
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def _pid_image(pid):
    """Image name of a pid ('' if unknown) -- used to guard against PID reuse."""
    if not IS_WIN:
        return "python"
    k32 = ctypes.windll.kernel32
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
    if not h:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = ctypes.c_ulong(1024)
        if k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            return os.path.basename(buf.value).lower()
        return ""
    finally:
        k32.CloseHandle(h)


# ------------------------------------------------------------ forwarder core

def _detect_lan_ip():
    """Best-effort source IP toward the default route (sends no packets)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 53))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def _listen_ip():
    """Configured LAN IP if bindable, else the auto-detected one."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        try:
            s.bind((BIND_IP, 0))
            return BIND_IP
        except OSError:
            alt = _detect_lan_ip()
            log(f"bind probe: {BIND_IP} unavailable, falling back to {alt}")
            return alt or BIND_IP
    finally:
        s.close()


def _pipe(src, dst):
    try:
        while True:
            data = src.recv(BUF)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass
        for s in (src, dst):
            try:
                s.close()
            except OSError:
                pass


def _handle(client, dst_host, dst_port, addr):
    try:
        client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        upstream = socket.create_connection((dst_host, dst_port), timeout=10)
        upstream.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    except OSError as e:
        log(f"{addr[0]}:{addr[1]} -> {dst_port} upstream down: {e}")
        try:
            client.close()
        except OSError:
            pass
        return
    threading.Thread(target=_pipe, args=(client, upstream), daemon=True).start()
    threading.Thread(target=_pipe, args=(upstream, client), daemon=True).start()


def forwarder(listen_port, dst_host, dst_port, name, ip_holder):
    while True:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            srv.bind((ip_holder[0], listen_port))
            srv.listen(64)
            log(f"{name}: listening {ip_holder[0]}:{listen_port} -> {dst_host}:{dst_port}")
            while True:
                try:
                    client, addr = srv.accept()
                except OSError:
                    break
                threading.Thread(
                    target=_handle, args=(client, dst_host, dst_port, addr), daemon=True
                ).start()
        except OSError as e:
            log(f"{name}: listener {listen_port} error: {e}; retry in 5s")
        finally:
            try:
                srv.close()
            except OSError:
                pass
        time.sleep(5)


# ------------------------------------------------------------------ commands

def cmd_run():
    """Foreground run -- normally spawned detached by `start`."""
    old = _read_pid()
    if old and old != os.getpid() and _pid_alive(old):
        print(f"already running as pid {old}; not double-starting")
        return 1
    with open(PIDFILE, "w") as f:
        f.write(str(os.getpid()))
    ip_holder = [_listen_ip()]
    log(f"lan_proxy run pid={os.getpid()} bind={ip_holder[0]}")
    threads = [
        threading.Thread(target=forwarder, args=(lp, dh, dp, name, ip_holder), daemon=True)
        for (lp, dh, dp, name) in FORWARDS
    ]
    for t in threads:
        t.start()
    try:
        while all(t.is_alive() for t in threads):
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        log("lan_proxy exiting")
        if _read_pid() == os.getpid():
            _rm_pid()
    return 0


def cmd_start():
    old = _read_pid()
    if old and _pid_alive(old):
        print(f"already running as pid {old} ({_pid_image(old)})")
        return 0
    _rm_pid()
    exe, script = sys.executable, os.path.abspath(__file__)
    p = None
    if IS_WIN:
        DETACHED_PROCESS = 0x00000008
        NEW_GROUP = 0x00000200
        BREAKAWAY = 0x01000000
        for flags in (DETACHED_PROCESS | NEW_GROUP | BREAKAWAY,
                      DETACHED_PROCESS | NEW_GROUP):
            try:
                p = subprocess.Popen(
                    [exe, script, "run"], creationflags=flags, cwd=HERE,
                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, close_fds=True,
                )
                break
            except OSError:
                continue
    else:
        p = subprocess.Popen([exe, script, "run"], cwd=HERE, start_new_session=True)
    if p is None:
        print("failed to spawn detached process")
        return 1
    with open(PIDFILE, "w") as f:
        f.write(str(p.pid))
    time.sleep(1.2)
    if not _pid_alive(p.pid):
        print(f"child pid {p.pid} died immediately -- see {LOGFILE}")
        return 1
    print(f"started pid {p.pid}")
    for lp, _dh, _dp, name in FORWARDS:
        print(f"  {name}: target {BIND_IP}:{lp}")
    return 0


def cmd_stop():
    pid = _read_pid()
    if pid is None:
        print("not running (no pidfile)")
        return 0
    if not _pid_alive(pid):
        _rm_pid()
        print(f"stale pidfile (pid {pid}) removed")
        return 0
    img = _pid_image(pid) or "unknown"
    if "python" not in img:
        print(f"REFUSING to kill pid {pid}: image is '{img}', not python (pid reuse?)")
        return 1
    try:
        os.kill(pid, signal.SIGTERM)  # Windows: TerminateProcess
    except OSError as e:
        print(f"kill pid {pid} failed: {e}")
        return 1
    for _ in range(30):
        if not _pid_alive(pid):
            break
        time.sleep(0.1)
    _rm_pid()
    print(f"stopped pid {pid} ({img})")
    return 0


def _probe(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    try:
        s.connect((ip, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def cmd_status():
    pid = _read_pid()
    alive = pid is not None and _pid_alive(pid)
    print(f"process: pid={pid} alive={alive}")
    rc = 0 if alive else 1
    for lp, dh, dp, name in FORWARDS:
        ok = _probe(BIND_IP, lp)
        note = "LISTENING" if ok else "down"
        if not ok and BIND_IP != (_alt := _listen_ip()):
            note += f" (also tried {_alt}: {'LISTENING' if _probe(_alt, lp) else 'down'})"
        print(f"  {BIND_IP}:{lp} -> {dh}:{dp}  [{name}]: {note}")
        rc = rc or (0 if ok else 1)
    return rc


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "start"
    if cmd == "start":
        return cmd_start()
    if cmd == "run":
        return cmd_run()
    if cmd == "stop":
        return cmd_stop()
    if cmd == "restart":
        cmd_stop()
        time.sleep(0.3)
        return cmd_start()
    if cmd == "status":
        return cmd_status()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
