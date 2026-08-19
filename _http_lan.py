from pathlib import Path
p = Path("dashboard/server.py")
t = p.read_text(encoding="utf-8")
t = t.replace(
    '''    if host in ("0.0.0.0", "::") or str(host).startswith("192."):
        tls = True
''',
    "    # tls only when asked. LAN HTTP must load on a phone; HTTPS via tunnel.\n",
    1,
)
p.write_text(t, encoding="utf-8")
print("no auto tls")
Path("_run_http.py").write_text(
    "from dashboard.server import run\nrun(host='0.0.0.0', port=8765, tls=False)\n",
    encoding="utf-8",
)
print("wrote _run_http.py")
