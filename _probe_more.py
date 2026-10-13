import socket, ssl, time, urllib.request

def raw(host, port, payload, timeout=4):
    t0 = time.time()
    s = socket.create_connection((host, port), timeout=timeout)
    s.settimeout(timeout)
    s.sendall(payload)
    try:
        data = s.recv(200)
    except Exception as e:
        data = f"recv {type(e).__name__}: {e}".encode()
    s.close()
    return time.time()-t0, data

def http(url, timeout=5):
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            b = r.read(200)
            return time.time()-t0, r.status, b[:120]
    except Exception as e:
        return time.time()-t0, type(e).__name__, str(e)[:160]

print("HTTP /", http("http://127.0.0.1:8765/"))
print("HTTP /table", http("http://127.0.0.1:8765/table"))
print("HTTP /api/v1/table/view", http("http://127.0.0.1:8765/api/v1/table/view"))
print("HTTP /api/v1/game", http("http://127.0.0.1:8765/api/v1/game"))

req = b"GET / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n"
sec, data = raw("127.0.0.1", 8765, req)
print("RAW /", round(sec,3), data[:160])

# TLS try
t0 = time.time()
try:
    ctx = ssl._create_unverified_context()
    with socket.create_connection(("127.0.0.1", 8765), timeout=4) as sock:
        with ctx.wrap_socket(sock, server_hostname="127.0.0.1") as ssock:
            ssock.sendall(b"GET /api/v1/table/view HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n")
            data = ssock.recv(200)
            print("TLS view", round(time.time()-t0,3), data[:160])
except Exception as e:
    print("TLS view", round(time.time()-t0,3), type(e).__name__, e)
