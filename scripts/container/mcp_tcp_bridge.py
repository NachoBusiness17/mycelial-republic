"""mcp_tcp_bridge -- serve the stdio MCP server over loopback TCP (B2-291).

Operator question (2026-09-26): "our docker can serve mcp, does that do
anything." This is the wire that makes it do something: mag/mcp_server.py
speaks MCP on stdio (one process per spawning client, stdlib-only law), which
is perfect for desktop clients but cannot be an always-on docker service.
The bridge accepts TCP connections and spawns ONE mag.mcp_server subprocess
per connection, piping bytes both ways, so every connected MCP client gets
the same isolation the stdio spawn gives and concurrency is one subprocess
per session (the falsifier shape: two client sessions, both clean).

SECURITY POSTURE (loopback law): default bind is 127.0.0.1 -- never 0.0.0.0.
Inside docker the compose service publishes "127.0.0.1:8766:8766" only, so
reachability = host-local processes + the mag_net containers (the trusted
fleet). The archivist profile is served by default: read-only tools, no
run_shell / write_file / apply_patch. The MCP registry ALREADY runs inside
this backend (dashboard /run_task dispatches the same TOOL_MAP); the bridge
is transport, not authority -- same posture as the stdio server docstring.

SEAT HANDSHAKE (2026-10-17, opt-in): --handshake optional|required (default
from env MAG_SEAT_HANDSHAKE, else off = the original raw byte pipe). In a
handshake mode every client line is checked by mag/seat_handshake.py
(signed envelope -> only the verified inner JSON-RPC line is forwarded); a
failed check, or a plain line under "required", silently closes the session.
Clients sign with scripts/mcp_stdio_shim.py --sign.

RUN:  python scripts/container/mcp_tcp_bridge.py --port 8766 --profile archivist
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import threading

CHUNK = 65536


def _pump(src, dst) -> None:
    """Copy bytes src -> dst until EOF or error; half-close dst at the end.

    dst is either a socket (sendall) or the subprocess stdin pipe
    (write+flush); both directions occur, so handle both shapes.
    """
    try:
        while True:
            # read1 (not read) for pipe sources: BufferedReader.read blocks
            # until the FULL chunk arrives, which would hold a short MCP
            # reply hostage; read1 returns whatever one raw read produced.
            data = src.recv(CHUNK) if hasattr(src, "recv") else src.read1(CHUNK)
            if not data:
                break
            if hasattr(dst, "sendall"):
                dst.sendall(data)
            else:
                dst.write(data)
                dst.flush()
    except OSError:
        pass
    finally:
        try:
            if hasattr(dst, "shutdown"):
                dst.shutdown(socket.SHUT_WR)
            else:
                dst.close()
        except OSError:
            pass


def verify_line(line: bytes, mode: str, allowlist: dict, cache) -> bytes | None:
    """One client line -> the bytes to forward, or None to drop the session."""
    from mag import seat_handshake as sh

    stripped = line.strip()
    if not stripped:
        return b""
    try:
        obj = json.loads(stripped)
    except ValueError:
        return None if mode == "required" else line
    if sh.is_envelope(obj):
        ok = sh.verify_envelope(obj, allowlist=allowlist, cache=cache)
        if ok is None or "\n" in ok[1]:
            return None
        return ok[1].encode("utf-8") + b"\n"
    return None if mode == "required" else line


def _pump_verified(conn: socket.socket, dst, mode: str, cache) -> None:
    """Client -> subprocess, line by line through the seat handshake."""
    from mag import seat_handshake as sh

    allowlist = sh.load_allowlist()
    reader = conn.makefile("rb")
    try:
        for line in reader:
            out = verify_line(line, mode, allowlist, cache)
            if out is None:  # silent drop: no reply, close the session
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                break
            if out:
                dst.write(out)
                dst.flush()
    except OSError:
        pass
    finally:
        try:
            dst.close()
        except OSError:
            pass


def handle(conn: socket.socket, profile: str, quiet: bool,
           handshake: str = "off", cache=None) -> None:
    """One connection = one MCP stdio subprocess (session isolation)."""
    peer = conn.getpeername()[0]
    if not quiet:
        print(f"[mcp_bridge] session open from {peer} (profile={profile})", flush=True)
    proc = subprocess.Popen(
        # -u: the stdio server's stdout is a pipe here, not a client's stdin
        # handle, and block buffering would hold the initialize reply forever.
        [sys.executable, "-u", "-m", "mag.mcp_server", "--profile", profile],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)
    threads = [
        (threading.Thread(target=_pump, args=(conn, proc.stdin), daemon=True)
         if handshake == "off" else
         threading.Thread(target=_pump_verified, args=(conn, proc.stdin, handshake, cache),
                          daemon=True)),
        threading.Thread(target=_pump, args=(proc.stdout, conn), daemon=True),
    ]
    for t in threads:
        t.start()
    proc.wait()
    for t in threads:
        t.join(timeout=5)
    conn.close()
    if not quiet:
        print(f"[mcp_bridge] session closed from {peer} (exit={proc.returncode})",
              flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="mcp_tcp_bridge",
        description="Loopback TCP bridge in front of mag.mcp_server (stdio)")
    ap.add_argument("--port", type=int, default=8766)
    ap.add_argument("--bind", default="127.0.0.1",
                    help="bind address. BARE-METAL law: keep 127.0.0.1. "
                         "INSIDE docker bind 0.0.0.0 -- the docker proxy dials "
                         "the container IP, not the container's loopback, so a "
                         "127.0.0.1 bind is unreachable through the published "
                         "port; the loopback guarantee there comes from the "
                         "compose mapping 127.0.0.1:8766->8766 (host side).")
    ap.add_argument("--profile", default="archivist",
                    help="mcp_server profile; archivist = read-only default")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--handshake", choices=["off", "optional", "required"],
                    default=os.environ.get("MAG_SEAT_HANDSHAKE", "off").strip().lower() or "off",
                    help="seat handshake mode (mag/seat_handshake.py); off = raw pipe")
    args = ap.parse_args()
    if args.handshake not in ("off", "optional", "required"):
        args.handshake = "required"  # unknown env value fails closed
    cache = None
    if args.handshake != "off":
        from mag import seat_handshake as sh

        cache = sh.ReplayCache()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.bind, args.port))
    srv.listen(16)
    if not args.quiet:
        print(f"[mcp_bridge] listening on {args.bind}:{args.port} "
              f"(profile={args.profile}, handshake={args.handshake}, "
              f"one mcp_server subprocess per session)",
              flush=True)
    while True:
        conn, _ = srv.accept()
        threading.Thread(target=handle,
                         args=(conn, args.profile, args.quiet, args.handshake, cache),
                         daemon=True).start()


if __name__ == "__main__":
    raise SystemExit(main())
