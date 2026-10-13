from pathlib import Path
p = Path("/app/mag/game_view.py")
t = p.read_text(encoding="utf-8")
bad = '        status=str(camp.get("status") or ""def handle_table_view(body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:'
# types may be dict[str, str]
import re
t2, n = re.subn(
    r'status=str\(camp\.get\("status"\) or ""def handle_table_view',
    'status=str(camp.get("status") or ""),\n    )\n\n\ndef handle_table_view',
    t,
    count=1,
)
if n != 1:
    raise SystemExit(f"replace count {n}")
p.write_text(t2, encoding="utf-8")
print("syntax fixed")
