#!/usr/bin/env python3
"""mcp_stdio_shim -- let a stdio-only MCP client reach the loopback TCP MCP door.

Shared surface (2026-10-17, watch/LIBRARY/SHARED_SURFACE_SELFSTEAL_20261017.md):
the always-on estate MCP runs in the mag-mcp container behind
scripts/container/mcp_tcp_bridge.py on 127.0.0.1:8766 (newline-delimited
JSON-RPC over raw TCP, one mag.mcp_server subprocess per connection). Most
MCP clients (Gemini CLI, Codex, Claude Desktop, Hermes, ZCode, Cursor) can
only SPAWN a stdio server. This shim is that server: it connects to the TCP
door and pipes bytes both ways, nothing else. It parses nothing and adds no
authority -- the profile is whatever the bridge on the other end serves.

LOOPBACK LAW: the host must be a loopback address (127.0.0.0/8, ::1,
localhost). A non-loopback host is refused unless --allow-remote is passed,
and even then this shim carries no credentials; exposure decisions belong to
the operator (see docs/SHARED_SURFACE_CLIENTS.md, "Later: beyond localhost").

Stdlib only; no dependency on the repo (point a client at this file with any
Python 3.9+).

SIGNED MODE (2026-10-17): --sign wraps every stdin line in a seat handshake
envelope (mag/seat_handshake.py) using the key at --key or env
MAG_SEAT_KEY_PATH, for a bridge running --handshake optional|required.
This imports the repo module, so it needs this file to stay in <repo>/scripts.

RUN:  python scripts/mcp_stdio_shim.py                 # 127.0.0.1:8766
      python scripts/mcp_stdio_shim.py --port 8766 --timeout 5
"""
from __future__ import annotations

import argparse
import ipaddress
import socket
import sys
import threading

CHUNK = 65536
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8766


def is_loopback(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _stdin_to_sock(src, sock: socket.socket) -> None:
    """Client stdin -> TCP; on EOF half-close so the server sees end of input."""
    try:
        while True:
            data = src.read1(CHUNK) if hasattr(src, "read1") else src.read(CHUNK)
            if not data:
                break
            sock.sendall(data)
    except OSError:
        pass
    finally:
        try:
            sock.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def _stdin_to_sock_signed(src, sock: socket.socket, key_path: str | None) -> None:
    """Like _stdin_to_sock, but each JSON-RPC line rides a signed envelope."""
    import json
    from pathlib import Path

    root = str(Path(__file__).resolve().parents[1])
    if root not in sys.path:
        sys.path.insert(0, root)
    from mag import seat_handshake as sh

    seat_id, seed = sh.load_key(key_path)
    try:
        for raw in iter(src.readline, b""):
            line = raw.decode("utf-8").strip()
            if not line:
                continue
            env = sh.wrap(line, seed=seed, seat_id=seat_id)
            sock.sendall((json.dumps(env, separators=(",", ":")) + "\n").encode("utf-8"))
    except OSError:
        pass
    finally:
        try:
            sock.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def _sock_to_stdout(sock: socket.socket, dst) -> None:
    """TCP -> client stdout, flushed per chunk so short replies are never held."""
    try:
        while True:
            data = sock.recv(CHUNK)
            if not data:
                break
            dst.write(data)
            dst.flush()
    except OSError:
        pass


def run(host: str, port: int, timeout: float, stdin=None, stdout=None,
        sign: bool = False, key_path: str | None = None) -> int:
    stdin = stdin if stdin is not None else sys.stdin.buffer
    stdout = stdout if stdout is not None else sys.stdout.buffer
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
    except OSError as e:
        sys.stderr.write(f"[mcp_stdio_shim] cannot reach {host}:{port}: {e}\n"
                         "  is the mag-mcp container up? (docker compose ps mcp)\n")
        return 2
    sock.settimeout(None)
    reader = threading.Thread(target=_sock_to_stdout, args=(sock, stdout), daemon=True)
    reader.start()
    writer = (threading.Thread(target=_stdin_to_sock_signed, args=(stdin, sock, key_path),
                               daemon=True) if sign else
              threading.Thread(target=_stdin_to_sock, args=(stdin, sock), daemon=True))
    writer.start()
    reader.join()  # the session ends when the server closes the connection
    try:
        sock.close()
    except OSError:
        pass
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="mcp_stdio_shim",
                                 description="stdio <-> loopback TCP pipe for the mag MCP door")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--timeout", type=float, default=5.0, help="connect timeout, seconds")
    ap.add_argument("--allow-remote", action="store_true",
                    help="permit a non-loopback host (operator decision; off by default)")
    ap.add_argument("--sign", action="store_true",
                    help="wrap each line in a seat handshake envelope (bridge --handshake)")
    ap.add_argument("--key", help="seat key path (default env MAG_SEAT_KEY_PATH)")
    args = ap.parse_args(argv)
    if not is_loopback(args.host) and not args.allow_remote:
        sys.stderr.write(f"[mcp_stdio_shim] refusing non-loopback host {args.host!r} "
                         "(loopback law; pass --allow-remote only on an operator decision)\n")
        return 3
    return run(args.host, args.port, args.timeout, sign=args.sign, key_path=args.key)


if __name__ == "__main__":
    sys.exit(main())
