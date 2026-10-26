#!/usr/bin/env python3
'''Q_037_ws_probe.py — FW-37 receipt probe: the mud relay's ws push socket.

Starts dashboard/mud_relay.py on a test port and proves, over a real TCP socket:
  1. RFC6455 handshake (101 + correct Sec-WebSocket-Accept)
  2. presence text frame registers the lantern in the shared store (visible via HTTP /mud/ping)
  3. a second lantern POSTed over HTTP appears in the ws broadcast, self excluded
  4. closing the socket drops the lantern immediately (no 6s ghost)
  5. the v1 HTTP poll path still works (backward compat)

Run: ./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/queue/Q_037_ws_probe.py
'''
import base64
import hashlib
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(ROOT, 'dashboard', 'mud_relay.py')):
    nxt = os.path.dirname(ROOT)
    if nxt == ROOT:
        raise SystemExit('repo root not found: no dashboard/mud_relay.py above this file')
    ROOT = nxt
RELAY = os.path.join(ROOT, 'dashboard', 'mud_relay.py')
PORT = 8791
WS_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

results = []
def check(name, fn):
    try:
        fn()
        results.append((name, True, ''))
    except AssertionError as e:
        results.append((name, False, str(e)))
    except Exception as e:
        results.append((name, False, f'{type(e).__name__}: {e}'))

def assert_(cond, msg):
    if not cond:
        raise AssertionError(msg)

def http_json(path, payload=None):
    url = f'http://127.0.0.1:{PORT}{path}'
    if payload is None:
        with urllib.request.urlopen(url, timeout=5) as r:
            return json.loads(r.read().decode())
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode())

class WS:
    '''Minimal RFC6455 CLIENT: masked frames out, unmasked frames in.'''
    def __init__(self, port):
        self.s = socket.create_connection(('127.0.0.1', port), timeout=5)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((
            f'GET /mud/ws HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n'
            f'Upgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n'
            f'Sec-WebSocket-Version: 13\r\n\r\n').encode())
        buf = b''
        while b'\r\n\r\n' not in buf:
            buf += self.s.recv(4096)
        head, _, rest = buf.partition(b'\r\n\r\n')
        self.head = head.decode()
        self.rest = rest
        expected = base64.b64encode(hashlib.sha1((key + WS_GUID).encode()).digest()).decode()
        self.expected_accept = expected

    def recv_frame(self, timeout=5.0):
        self.s.settimeout(timeout)
        def exact(n, first=b''):
            buf, first = first, b''
            while len(buf) < n:
                chunk = self.s.recv(n - len(buf))
                if not chunk:
                    raise ConnectionError('socket closed')
                buf += chunk
            return buf
        hdr = exact(2, self.rest)
        self.rest = b''
        op = hdr[0] & 0x0F
        ln = hdr[1] & 0x7F
        if ln == 126:
            ln = int.from_bytes(exact(2), 'big')
        elif ln == 127:
            ln = int.from_bytes(exact(8), 'big')
        return op, exact(ln)

    def send_text(self, obj):
        payload = json.dumps(obj).encode()
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        hdr = bytearray([0x81])
        ln = len(payload)
        if ln < 126:
            hdr.append(0x80 | ln)
        else:
            hdr.append(0x80 | 126)
            hdr += struct.pack('>H', ln)
        self.s.sendall(bytes(hdr) + mask + masked)

    def send_close(self):
        mask = os.urandom(4)
        payload = struct.pack('>H', 1000)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.s.sendall(bytes([0x88, 0x80 | len(payload)]) + mask + masked)

    def close(self):
        try:
            self.s.close()
        except OSError:
            pass

def ws_upgraded(w):
    assert_(' 101 ' in w.head, f'expected 101, head was: {w.head!r}')
    assert_('upgrade: websocket' in w.head.lower(), f'missing Upgrade header: {w.head!r}')
    assert_(w.expected_accept in w.head, f'bad Sec-WebSocket-Accept; want {w.expected_accept} in {w.head!r}')

def recv_broadcast(w, timeout=5.0):
    '''Next others-broadcast (skip pongs).'''
    deadline = time.time() + timeout
    while time.time() < deadline:
        op, data = w.recv_frame(timeout=deadline - time.time())
        if op != 0x1:
            continue
        d = json.loads(data.decode())
        if d.get('type') == 'others':
            return d
    raise AssertionError('no broadcast within timeout')

def main():
    proc = subprocess.Popen([sys.executable, RELAY, str(PORT), '127.0.0.1'],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for _ in range(50):
            try:
                http_json('/mud/ping')
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise SystemExit('relay did not come up')

        def t1():
            w = WS(PORT)
            ws_upgraded(w)
            w.send_text({'id': 'probe-a', 'name': 'probe-a', 'x': 12.5, 'y': 40.0,
                         'hp': 80, 'max_hp': 100, 'state': 'play'})
            time.sleep(0.3)
            ping = http_json('/mud/ping')
            assert_(ping.get('players') == 1, f'expected 1 player after ws presence, got {ping}')
            w.close()
        check('1. handshake 101 + accept, ws presence frame registers lantern', t1)

        def t2():
            w = WS(PORT)
            ws_upgraded(w)
            w.send_text({'id': 'probe-a', 'name': 'probe-a', 'x': 1, 'y': 2,
                         'hp': 90, 'max_hp': 100, 'state': 'play'})
            http_json('/mud/seen', {'id': 'probe-b', 'name': 'probe-b', 'x': 50, 'y': 60,
                                    'hp': 70, 'max_hp': 100, 'state': 'play'})
            d = recv_broadcast(w)
            ids = [o['id'] for o in d['others']]
            assert_('probe-b' in ids, f'broadcast missing probe-b: {d}')
            assert_('probe-a' not in ids, f'broadcast must exclude self: {d}')
            row = next(o for o in d['others'] if o['id'] == 'probe-b')
            assert_(row['x'] == 50 and row['hp'] == 70, f'broadcast row malformed: {row}')
            w.close()
        check('2. broadcast: HTTP-posted lantern pushed to ws peer, self excluded', t2)

        def t3():
            w = WS(PORT)
            ws_upgraded(w)
            w.send_text({'id': 'probe-ghost', 'name': 'ghost', 'x': 0, 'y': 0,
                         'hp': 1, 'max_hp': 10, 'state': 'play'})
            time.sleep(0.3)
            ids = [p['id'] for p in http_json('/mud/state')['players']]
            assert_('probe-ghost' in ids, f'ghost should be registered, players: {ids}')
            w.send_close()
            time.sleep(0.2)
            w.close()
            deadline = time.time() + 3
            while time.time() < deadline:
                ids = [p['id'] for p in http_json('/mud/state')['players']]
                if 'probe-ghost' not in ids:
                    return
                time.sleep(0.1)
            raise AssertionError(f'ghost lantern survived socket close: {ids}')
        check('3. socket close drops the lantern immediately (no 6s ghost)', t3)

        def t4():
            http_json('/mud/seen', {'id': 'http-l', 'name': 'http-l', 'x': 5, 'y': 6,
                                    'hp': 10, 'max_hp': 10, 'state': 'play'})
            o = http_json('/mud/others?id=other')
            assert_(any(p['id'] == 'http-l' for p in o['others']), f'http others broken: {o}')
            st = http_json('/mud/state')
            assert_(st['ok'] and any(p['id'] == 'http-l' for p in st['players']), f'http state broken: {st}')
        check('4. v1 HTTP path (seen/others/state) still works after the spike', t4)

        def t5():
            try:
                r = urllib.request.urlopen(f'http://127.0.0.1:{PORT}/mud/ws', timeout=5)
                status, body = r.status, json.loads(r.read().decode())
            except urllib.error.HTTPError as e:
                status, body = e.code, json.loads(e.read().decode())
            assert_(status == 400 and 'upgrade' in body.get('error', ''),
                    f'plain GET /mud/ws should 400 with upgrade error, got {status} {body}')
        check('5. non-upgrade GET /mud/ws refused cleanly (400, not silent 404)', t5)

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    fails = [r for r in results if not r[1]]
    for name, ok, err in results:
        print(('PASS' if ok else 'FAIL'), '-', name, ('' if ok else f'  -> {err}'))
    print(f'{len(results) - len(fails)}/{len(results)} PASS')
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
