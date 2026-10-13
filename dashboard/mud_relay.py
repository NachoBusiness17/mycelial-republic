#!/usr/bin/env python
'''mud_relay.py — the second lantern. Presence relay for MUD (v1 + ws spike).

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
  GET  /mud/state                                        -> {"ok":true,"now":...,"expire":6.0,
                                                              "players":[fresh lanterns],"stale":N,
                                                              "seen_total":N}
  GET  /mud/ws   Upgrade: websocket                      -> RFC6455 push socket

/mud/state is the spectator lens: read-only snapshot of the room. "players"
holds every lantern seen within EXPIRE (6s) with its age in seconds;
"stale" counts known-but-expired ids still awaiting the 24s sweep.

Players expire 6s after their last /seen (clients resend ~4/s).

WS spike (FW-37, 2026-09-28 — spec written before the behavior it owns):
a lantern may open `/mud/ws` and send the same presence JSON as /seen as
text frames; the relay broadcasts `{"ok":true,"type":"others","others":[...]}`
to every open socket ~8Hz (BCAST_HZ), excluding the receiver's own id. The
poll pair (/seen + /others at 250ms) stays for lanterns without the socket.
Closing the socket drops that lantern immediately — no 6s ghost. Still
presence-only: the socket carries no authority the HTTP path didn't.
Why a socket: the poll pair was two HTTP round trips per lantern per 250ms
and "others" could only be as fresh as the last poll; the push halves the
requests and triples the others-refresh rate. Evidence: receipt
watch/inbox/burn_reset_20260927/queue/Q-027.md (FW-37).

Run:  ./.venv/Scripts/python.exe dashboard/mud_relay.py [port] [bind]
Default: port 8766, bind 127.0.0.1.
'''
import base64
import hashlib
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PLAYERS = {}
LOCK = threading.Lock()
EXPIRE = 6.0
SEEN_TOTAL = 0  # every accepted /seen (HTTP or ws frame), lifetime of the process (spectator counter)
BIND = '127.0.0.1'
PORT = 8766

# ---- ws spike state (FW-37) ----
WS_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
BCAST_HZ = 8
BCAST_PERIOD = 1.0 / BCAST_HZ
WS_SESSIONS = {}  # conn -> {'pid': id-or-None}; one entry per open /mud/ws socket
_bcaster_started = False


def _guard():
    u = urlparse('http://' + BIND)
    if u.hostname not in ('127.0.0.1', 'localhost') and u.hostname != '0.0.0.0':
        raise SystemExit('refusing: relay binds must be loopback or explicit 0.0.0.0')
    if u.scheme != 'http':
        raise SystemExit('refusing: relay scheme must be http')


def _recvn(conn, n):
    '''Read exactly n bytes (TCP recv may return short reads).'''
    buf = b''
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def _ws_read_frame(conn):
    '''One RFC6455 client frame -> (opcode, payload bytes) or None on close/error.
    Client frames are always masked; length forms 7/16/64-bit all parsed.'''
    hdr = _recvn(conn, 2)
    if hdr is None:
        return None
    op = hdr[0] & 0x0F
    masked = bool(hdr[1] & 0x80)
    ln = hdr[1] & 0x7F
    if ln == 126:
        ext = _recvn(conn, 2)
        if ext is None:
            return None
        ln = int.from_bytes(ext, 'big')
    elif ln == 127:
        ext = _recvn(conn, 8)
        if ext is None:
            return None
        ln = int.from_bytes(ext, 'big')
    if ln > 1 << 20:
        return None   # spike cap: presence frames are tiny; refuse monsters
    mask = _recvn(conn, 4) if masked else b'\x00\x00\x00\x00'
    if mask is None:
        return None
    data = _recvn(conn, ln) if ln else b''
    if data is None:
        return None
    if masked:
        data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    return op, data


def _ws_send_frame(conn, payload, op=0x1):
    '''Server->client frames are unmasked (RFC6455 5.1).'''
    ln = len(payload)
    hdr = bytearray([0x80 | op])
    if ln < 126:
        hdr.append(ln)
    elif ln < 65536:
        hdr.append(126)
        hdr += ln.to_bytes(2, 'big')
    else:
        hdr.append(127)
        hdr += ln.to_bytes(8, 'big')
    conn.sendall(bytes(hdr) + payload)


def _register_seen(row):
    '''Shared presence store write for both /seen and ws frames.'''
    global SEEN_TOTAL
    with LOCK:
        now = time.time()
        SEEN_TOTAL += 1
        PLAYERS[row['id']] = {
            'id': row['id'],
            'name': str(row.get('name') or row['id'])[:24],
            'x': round(float(row.get('x') or 0), 1),
            'y': round(float(row.get('y') or 0), 1),
            'hp': round(float(row.get('hp') or 0), 1),
            'max_hp': round(float(row.get('max_hp') or 0), 1),
            'state': str(row.get('state') or 'play')[:12],
            'ts': now,
        }
        for k in [k for k, p in PLAYERS.items() if now - p['ts'] > EXPIRE * 4]:
            PLAYERS.pop(k, None)


def _fresh_players():
    now = time.time()
    with LOCK:
        return {pid: {k: p[k] for k in ('id', 'name', 'x', 'y', 'hp', 'max_hp', 'state')}
                for pid, p in PLAYERS.items() if now - p['ts'] <= EXPIRE}


def _ws_drop(conn):
    with LOCK:
        sess = WS_SESSIONS.pop(conn, None)
    if sess and sess.get('pid'):
        with LOCK:
            PLAYERS.pop(sess['pid'], None)   # socket closed -> the lantern is gone now, no 6s ghost
    try:
        conn.close()
    except OSError:
        pass


def _ws_broadcaster():
    '''Push `others` snapshots to every open socket ~BCAST_HZ. One thread for the room.'''
    while True:
        time.sleep(BCAST_PERIOD)
        fresh = _fresh_players()
        with LOCK:
            sessions = list(WS_SESSIONS.items())
        for conn, sess in sessions:
            pid = sess.get('pid')
            if not pid:
                continue   # not yet announced — nothing to address it to
            others = [v for k, v in fresh.items() if k != pid]
            try:
                _ws_send_frame(conn, json.dumps(
                    {'ok': True, 'type': 'others', 'now': round(time.time(), 3),
                     'others': others}).encode('utf-8'))
            except OSError:
                _ws_drop(conn)


def _start_broadcaster():
    global _bcaster_started
    with LOCK:
        if _bcaster_started:
            return
        _bcaster_started = True
    threading.Thread(target=_ws_broadcaster, daemon=True).start()


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

    def _ws_session(self):
        '''FW-37: the connection is now a websocket. Read client frames; presence
        frames register like /seen; close/ping handled per RFC6455. Returns on
        socket end — the handler thread dies with the socket.'''
        conn = self.connection
        with LOCK:
            WS_SESSIONS[conn] = {'pid': None}
        _start_broadcaster()
        try:
            while True:
                frame = _ws_read_frame(conn)
                if frame is None:
                    return
                op, data = frame
                if op == 0x8:                       # close
                    try:
                        _ws_send_frame(conn, data[:2], op=0x8)
                    except OSError:
                        pass
                    return
                if op == 0x9:                       # ping -> pong
                    _ws_send_frame(conn, data, op=0xA)
                    continue
                if op != 0x1:                       # spike: text frames only
                    continue
                try:
                    row = json.loads(data.decode('utf-8'))
                except (ValueError, UnicodeDecodeError):
                    continue
                pid = str(row.get('id') or '').strip()
                if not pid:
                    continue
                with LOCK:
                    WS_SESSIONS[conn]['pid'] = pid
                _register_seen(row)
        finally:
            _ws_drop(conn)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/mud/ws':
            if (self.headers.get('Upgrade') or '').lower() != 'websocket':
                self._send(400, {'ok': False, 'error': 'websocket upgrade required'})
                return
            key = self.headers.get('Sec-WebSocket-Key')
            if not key:
                self._send(400, {'ok': False, 'error': 'missing Sec-WebSocket-Key'})
                return
            accept = base64.b64encode(hashlib.sha1(
                (key + WS_GUID).encode('utf-8')).digest()).decode('ascii')
            self.send_response(101, 'Switching Protocols')
            self.send_header('Upgrade', 'websocket')
            self.send_header('Connection', 'Upgrade')
            self.send_header('Sec-WebSocket-Accept', accept)
            self.end_headers()
            self._ws_session()
            return
        if path == '/mud/ping':
            with LOCK:
                now = time.time()
                alive = [p for p in PLAYERS.values() if now - p['ts'] <= EXPIRE]
            self._send(200, {'ok': True, 'players': len(alive)})
            return
        if path == '/mud/state':
            now = time.time()
            with LOCK:
                fresh, stale = [], 0
                for p in PLAYERS.values():
                    age = now - p['ts']
                    if age <= EXPIRE:
                        row = {k: p[k] for k in ('id', 'name', 'x', 'y', 'hp', 'max_hp', 'state')}
                        row['age'] = round(age, 2)
                        fresh.append(row)
                    else:
                        stale += 1
                total = SEEN_TOTAL
            self._send(200, {'ok': True, 'now': round(now, 3), 'expire': EXPIRE,
                             'players': fresh, 'stale': stale, 'seen_total': total})
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
        _register_seen(b)
        self._send(200, {'ok': True, 'id': pid})


def main():
    _guard()
    _start_broadcaster()
    httpd = ThreadingHTTPServer((BIND, PORT), Handler)
    print(f'mud_relay: room open at http://{BIND}:{PORT}  (LAN-only unless you forwarded it)')
    print(f'mud_relay: ws push at ws://{BIND}:{PORT}/mud/ws  ({BCAST_HZ}Hz others, FW-37 spike)')
    httpd.serve_forever()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    if len(sys.argv) > 2:
        BIND = sys.argv[2]
    main()
