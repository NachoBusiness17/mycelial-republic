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

RUN:  python scripts/container/mcp_tcp_bridge.py --port 8766 --profile archivist
"""
from __future__ import annotations

import argparse
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


def handle(conn: socket.socket, profile: str, quiet: bool) -> None:
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
        threading.Thread(target=_pump, args=(conn, proc.stdin), daemon=True),
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
    args = ap.parse_args()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.bind, args.port))
    srv.listen(16)
    if not args.quiet:
        print(f"[mcp_bridge] listening on {args.bind}:{args.port} "
              f"(profile={args.profile}, one mcp_server subprocess per session)",
              flush=True)
    while True:
        conn, _ = srv.accept()
        threading.Thread(target=handle,
                         args=(conn, args.profile, args.quiet), daemon=True).start()


if __name__ == "__main__":
    raise SystemExit(main())
