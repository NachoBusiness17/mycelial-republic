from pathlib import Path

# --- rest.py: cheap tileset attach ---
p = Path("/app/dashboard/rest.py")
t = p.read_text(encoding="utf-8")
start = t.find("        out = handle_table_view(body, _p)")
if start < 0:
    raise SystemExit("rest.py handle_table_view call not found")
end = t.find("        return 200, out", start)
if end < 0:
    raise SystemExit("rest.py return not found")
end = end + len("        return 200, out")
# only replace the first h_table_view body
new = """        out = handle_table_view(body, _p)
        # Meta only. Never convert/copy DF art on the request path.
        try:
            from mag.df_tileset import tileset_meta
            out["tileset"] = tileset_meta()
        except Exception as te:
            out["tileset"] = {"ok": False, "error": str(te)[:120]}
        return 200, out"""
t = t[:start] + new + t[end:]
p.write_text(t, encoding="utf-8")
print("rest.py ok")

# --- server.py: request timeout + daemon threads ---
p = Path("/app/dashboard/server.py")
t = p.read_text(encoding="utf-8")
old = """class Handler(BaseHTTPRequestHandler):
    server_version = \"MagDashboard/1.0\"
"""
new = """class Handler(BaseHTTPRequestHandler):
    server_version = \"MagDashboard/1.0\"
    timeout = 20
"""
if old not in t:
    raise SystemExit("Handler class not found")
t = t.replace(old, new, 1)
old = """    else:
        httpd = ThreadingHTTPServer((host, port), Handler)
    print_bind_banner(host=host, port=port)
"""
new = """    else:
        httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.daemon_threads = True
    print_bind_banner(host=host, port=port)
"""
if old not in t:
    raise SystemExit("httpd bind block not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("server.py ok")

# --- table.html: abort hung view ---
p = Path("/app/dashboard/static/table.html")
t = p.read_text(encoding="utf-8")
old = """        const r = await fetch(url);
        const j = await r.json();
"""
new = """        const ctrl = new AbortController();
        const to = setTimeout(() => ctrl.abort(), 6000);
        const r = await fetch(url, { signal: ctrl.signal });
        clearTimeout(to);
        const j = await r.json();
"""
if old not in t:
    raise SystemExit("table.html fetch not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("table.html ok")
