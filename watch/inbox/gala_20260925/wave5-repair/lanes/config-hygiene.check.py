"""config-hygiene lane finish-line checks (gala wave5-repair, 2026-09-29).

Instrument: exercises the two fail-loud loaders against corrupt/missing
fixtures in a temp dir (never under configs/, so the seal is untouched),
then proves the live configs still load (regression guard).

Run: .venv/Scripts/python.exe watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.check.py
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))

fails = []


def check(name, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"       {detail}")
    if not ok:
        fails.append(name)


import models.providers as P  # noqa: E402

tmp = Path(tempfile.mkdtemp(prefix="config_hygiene_"))
print(f"scratch dir: {tmp}")
print()

# CHECK 1: corrupt providers.yaml (yaml scanner error) fails loud naming the file
corrupt = tmp / "providers.yaml"
corrupt.write_text("providers:\n  - broken: [unclosed\n  bad indent: :\n", encoding="utf-8")
P._PROVIDERS_PATH = corrupt
P._CFG = None
try:
    P.load_providers()
    check("corrupt providers.yaml fails loud (parse error)", False,
          "load_providers returned without raising")
except P.ProviderConfigError as e:
    check("corrupt providers.yaml fails loud (parse error)", str(corrupt) in str(e),
          f"ProviderConfigError: {e}")
except Exception as e:  # noqa: BLE001
    check("corrupt providers.yaml fails loud (parse error)", False,
          f"wrong exception type {type(e).__name__}: {e}")

# CHECK 2: providers.yaml that parses to a non-mapping fails loud
scalar = tmp / "providers_scalar.yaml"
scalar.write_text("just a string not a mapping\n", encoding="utf-8")
P._PROVIDERS_PATH = scalar
P._CFG = None
try:
    P.load_providers()
    check("non-mapping providers.yaml fails loud (shape error)", False,
          "load_providers returned without raising")
except P.ProviderConfigError as e:
    check("non-mapping providers.yaml fails loud (shape error)", str(scalar) in str(e),
          f"ProviderConfigError: {e}")

# CHECK 3: missing providers.yaml fails loud naming the file
missing = tmp / "nope" / "providers.yaml"
P._PROVIDERS_PATH = missing
P._CFG = None
try:
    P.load_providers()
    check("missing providers.yaml fails loud", False, "returned without raising")
except P.ProviderConfigError as e:
    check("missing providers.yaml fails loud", str(missing) in str(e),
          f"ProviderConfigError: {e}")

# CHECK 4: live roster still loads (regression guard)
P._PROVIDERS_PATH = None
P._CFG = None
ids = P.list_provider_ids()
check("live configs/providers.yaml still loads", len(ids) > 0,
      f"{len(ids)} providers loaded, first 8: {', '.join(sorted(ids)[:8])}")

import mag.improve as imp  # noqa: E402

real_cfg_path = imp.CFG_PATH

# CHECK 5: missing improve.yaml fails loud naming the path
imp.CFG_PATH = tmp / "improve.yaml"
assert not imp.CFG_PATH.is_file()
try:
    imp.load_config()
    check("missing improve.yaml fails loud", False, "returned without raising")
except FileNotFoundError as e:
    check("missing improve.yaml fails loud", str(imp.CFG_PATH) in str(e),
          f"FileNotFoundError: {e}")

# CHECK 6: real improve.yaml still loads (regression guard)
imp.CFG_PATH = real_cfg_path
cfg = imp.load_config()
srcs = cfg.get("sources") or {}
check("real configs/improve.yaml still loads", bool(cfg.get("enabled")),
      f"enabled={cfg.get('enabled')} sources={len(srcs)} "
      f"budget_keys={sorted((cfg.get('budgets') or {}).keys())[:5]}")

print()
print(f"RESULT: {6 - len(fails)}/6 checks passed" + ("" if not fails else f"; FAILED: {fails}"))
sys.exit(1 if fails else 0)
