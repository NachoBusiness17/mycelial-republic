from pathlib import Path
t = Path("dashboard/server.py").read_text(encoding="utf-8")
old = '''def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    from config import print_bind_banner

    STATIC.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), Handler)
    print_bind_banner(host=host, port=port)
    print(f"  biography: {BIO}")
    print(f"  ingest:    {INGEST}")
    print("Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nstopped")
    finally:
        httpd.server_close()
'''
new = '''def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, *, tls: bool = False) -> None:
    """Serve the desk. tls=True wraps the socket so a phone mic is a secure context."""
    import ssl
    from config import ROOT, print_bind_banner

    STATIC.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), Handler)
    scheme = "http"
    if tls:
        crt = ROOT / "memory" / "tls" / "lan.crt"
        key = ROOT / "memory" / "tls" / "lan.key"
        if not crt.is_file() or not key.is_file():
            raise SystemExit("tls requested but memory/tls/lan.crt missing")
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(str(crt), str(key))
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        scheme = "https"
    print_bind_banner(host=host, port=port)
    print(f"  scheme:    {scheme}")
    print(f"  biography: {BIO}")
    print(f"  ingest:    {INGEST}")
    print("Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nstopped")
    finally:
        httpd.server_close()
'''
if old not in t:
    raise SystemExit("run() block missing")
Path("dashboard/server.py").write_text(t.replace(old, new, 1), encoding="utf-8")
print("dashboard tls wrap")
