"""Project-wide pytest setup."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def pytest_configure(config):
    """Keep concurrent Windows test runs out of each other's temp directory."""
    if not config.option.basetemp:
        config.option.basetemp = str(ROOT / "agents" / f"pytest-tmp-{os.getpid()}")
    # Ensure the basetemp dir EXISTS. pytest's make_numbered_dir() calls
    # os.scandir() on the base dir; if it's missing (fresh run), every tmp_path
    # fixture dies in setup with FileNotFoundError. This was the root cause of
    # 56 suite failures in the 2026-08-09 full-blast audit.
    Path(config.option.basetemp).mkdir(parents=True, exist_ok=True)
