from pathlib import Path
t = Path("main.py").read_text(encoding="utf-8")
old = "        run_dashboard(host=host, port=args.port)\n"
new = "        run_dashboard(host=host, port=args.port, tls=bool(getattr(args, \"lan\", False)))\n"
if old not in t:
    raise SystemExit("run_dashboard call missing")
Path("main.py").write_text(t.replace(old, new, 1), encoding="utf-8")
print("lan implies tls")
