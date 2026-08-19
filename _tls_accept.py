from pathlib import Path
p = Path("dashboard/server.py")
t = p.read_text(encoding="utf-8")
old = '''def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, *, tls: bool = False) -> None:
    """Serve the desk. tls=True wraps the socket so a phone mic is a secure context."""
    import ssl
    from config import ROOT, print_bind_banner

    STATIC.mkdir(parents=True, exist_ok=True)
    if host in ("0.0.0.0", "::") or host.startswith("192."):
        tls = True
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
new = '''class _TLSServer(ThreadingHTTPServer):
    """Wrap each accept, not the listen socket. Android RST on listen-wrap."""

    def __init__(self, addr, handler, ctx):
        super().__init__(addr, handler)
        self._tls_ctx = ctx

    def get_request(self):
        import ssl as _ssl
        sock, addr = self.socket.accept()
        try:
            return self._tls_ctx.wrap_socket(sock, server_side=True), addr
        except _ssl.SSLError:
            try:
                sock.close()
            except Exception:
                pass
            raise


def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, *, tls: bool = False) -> None:
    """Serve the desk. tls=True so a phone mic is a secure context."""
    import ssl
    from config import ROOT, print_bind_banner

    STATIC.mkdir(parents=True, exist_ok=True)
    if host in ("0.0.0.0", "::") or str(host).startswith("192."):
        tls = True
    scheme = "http"
    ctx = None
    if tls:
        crt = ROOT / "memory" / "tls" / "lan.crt"
        key = ROOT / "memory" / "tls" / "lan.key"
        if not crt.is_file() or not key.is_file():
            raise SystemExit("tls requested but memory/tls/lan.crt missing")
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.load_cert_chain(str(crt), str(key))
        httpd = _TLSServer((host, port), Handler, ctx)
        scheme = "https"
    else:
        httpd = ThreadingHTTPServer((host, port), Handler)
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
    raise SystemExit("run block missing")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("tls accept wrap")
