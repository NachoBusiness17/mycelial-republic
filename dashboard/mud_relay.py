#!/usr/bin/env python
'''mud_relay.py — the second lantern. Presence relay for MUD (v1).

Two or more browsers pointing at the same MUD register here; each sees the
others as embers in its dark. v1 is presence-only: positions and vitals,
no authority — each client's world is its own, and the relay is the room
they share. The authoritative version (server-side sim) is the next stone.

LAN-only by intent: bind 127.0.0.1 and forward via lan_proxy, or bind
0.0.0.0 if you accept the same perimeter as the dashboard (no auth).

API (all JSON):
  POST /mud/seen   {id, name, x, y, hp, max_hp, state}  -> {"ok":true}
  GET  /mud/others?id=X                                  -> {"ok":true,"others":[...]}
  GET  /mud/ping                                         -> {"ok":true,"players":N}

Players expire 6s after their last /seen (clients resend ~4/s).

Run:  ./.venv/Scripts/python.exe dashboard/mud_relay.py [port] [bind]
Default: port 8766, bind 127.0.0.1.
'''
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PLAYERS = {}
LOCK = threading.Lock()
EXPIRE = 6.0
BIND = '127.0.0.1'
PORT = 8766


def _guard():
    u = urlparse('http://' + BIND)
    if u.hostname not in ('127.0.0.1', 'localhost') and u.hostname != '0.0.0.0':
        raise SystemExit('refusing: relay binds must be loopback or explicit 0.0.0.0')
    if u.scheme != 'http':
        raise SystemExit('refusing: relay scheme must be http')


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        try:
            n = int(self.headers.get('Content-Length') or 0)
            return json.loads(self.rfile.read(n).decode('utf-8') or '{}')
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/mud/ping':
            with LOCK:
                now = time.time()
                alive = [p for p in PLAYERS.values() if now - p['ts'] <= EXPIRE]
            self._send(200, {'ok': True, 'players': len(alive)})
            return
        if path == '/mud/others':
            q = parse_qs(urlparse(self.path).query)
            me = (q.get('id') or [''])[0]
            now = time.time()
            with LOCK:
                others = [{k: p[k] for k in ('id', 'name', 'x', 'y', 'hp', 'max_hp', 'state')}
                          for pid, p in list(PLAYERS.items())
                          if pid != me and now - p['ts'] <= EXPIRE]
            self._send(200, {'ok': True, 'others': others})
            return
        self._send(404, {'ok': False, 'error': 'not found'})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != '/mud/seen':
            self._send(404, {'ok': False, 'error': 'not found'})
            return
        b = self._body()
        pid = str(b.get('id') or '').strip()
        if not pid:
            self._send(400, {'ok': False, 'error': 'missing id'})
            return
        with LOCK:
            now = time.time()
            PLAYERS[pid] = {
                'id': pid,
                'name': str(b.get('name') or pid)[:24],
                'x': round(float(b.get('x') or 0), 1),
                'y': round(float(b.get('y') or 0), 1),
                'hp': round(float(b.get('hp') or 0), 1),
                'max_hp': round(float(b.get('max_hp') or 0), 1),
                'state': str(b.get('state') or 'play')[:12],
                'ts': now,
            }
            for k in [k for k, p in PLAYERS.items() if now - p['ts'] > EXPIRE * 4]:
                PLAYERS.pop(k, None)
        self._send(200, {'ok': True, 'id': pid})


def main():
    _guard()
    httpd = ThreadingHTTPServer((BIND, PORT), Handler)
    print(f'mud_relay: room open at http://{BIND}:{PORT}  (LAN-only unless you forwarded it)')
    httpd.serve_forever()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    if len(sys.argv) > 2:
        BIND = sys.argv[2]
    main()
