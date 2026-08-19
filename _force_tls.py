from pathlib import Path

# 0.0.0.0 implies tls
p = Path("dashboard/server.py")
t = p.read_text(encoding="utf-8")
old = '''    STATIC.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), Handler)
    scheme = "http"
    if tls:
'''
new = '''    STATIC.mkdir(parents=True, exist_ok=True)
    if host in ("0.0.0.0", "::") or host.startswith("192."):
        tls = True
    httpd = ThreadingHTTPServer((host, port), Handler)
    scheme = "http"
    if tls:
'''
if old not in t:
    raise SystemExit("run wrap site missing")
p.write_text(t.replace(old, new, 1), encoding="utf-8")

m = Path("main.py")
mt = m.read_text(encoding="utf-8")
old2 = "        run_dashboard(host=host, port=port)\n        return 0\n"
new2 = "        run_dashboard(host=host, port=port, tls=True)\n        return 0\n"
if old2 in mt:
    m.write_text(mt.replace(old2, new2, 1), encoding="utf-8")
    print("second call tls")
else:
    print("second call not patched", old2 in mt)

# wave: bounce to https if not secure
w = Path("dashboard/static/wave.html")
html = w.read_text(encoding="utf-8")
if "isSecureContext" not in html:
    needle = "    const ptt = document.getElementById(\"ptt\");"
    insert = '''    if (!window.isSecureContext && location.protocol === "http:" && location.hostname !== "localhost" && location.hostname !== "127.0.0.1") {
      location.replace("https://" + location.host + location.pathname + location.search);
    }
    const ptt = document.getElementById("ptt");'''
    if needle not in html:
        raise SystemExit("ptt const missing")
    html = html.replace(needle, insert, 1)
    w.write_text(html, encoding="utf-8")
    print("wave https bounce")
else:
    print("wave already has isSecureContext")
print("ok")
