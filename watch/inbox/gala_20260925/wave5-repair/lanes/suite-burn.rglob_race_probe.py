"""suite-burn wave5 mechanism probe: the f-15 FileNotFoundError pair.

Proves (1) the OLD walker expression (ROOT.rglob) raises FileNotFoundError when a
path under ROOT vanishes mid-walk (the exact interference class: a concurrent
pytest run's tmp rmtree under in-repo agents/pytest-tmp-<pid>), and (2) the NEW
_iter_py (os.walk + pruned skip/reparse dirs + onerror) survives the same churn.

Run: .venv/Scripts/python.exe suite-burn.rglob_race_probe.py
"""
from __future__ import annotations

import shutil
import sys
import threading
import time
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))

CHURN = ROOT / "agents" / "pytest-tmp-raceprobe"
stop = threading.Event()


def churner() -> None:
    """Mirror the interference: create a subtree, delete it, repeat."""
    n = 0
    while not stop.is_set():
        d = CHURN / f"gen{n % 7}" / "test_x0" / "memory_training"
        try:
            d.mkdir(parents=True, exist_ok=True)
            (d / "weights.json").write_text("{}", encoding="utf-8")
            time.sleep(0.0005)
            shutil.rmtree(CHURN / f"gen{n % 7}", ignore_errors=False)
        except Exception:
            pass
        n += 1


def old_walk() -> None:
    files = [p for p in ROOT.rglob("*.py")]  # the pre-fix expression
    print(f"old rglob pass: {len(files)} files, no error")


def new_walk() -> None:
    from mag.ponytail_audit import _iter_py
    files = _iter_py()
    print(f"new _iter_py pass: {len(files)} files, no error")


def race(fn, label, max_s=45.0) -> None:
    t = threading.Thread(target=churner, daemon=True)
    t.start()
    t0 = time.time()
    tries = 0
    hit = None
    while time.time() - t0 < max_s:
        tries += 1
        try:
            fn()
        except OSError as e:
            hit = f"{type(e).__name__}: {e}"
            break
    stop.set()
    t.join(timeout=2)
    print(f"{label}: tries={tries} raced_hit={hit!r}")


if __name__ == "__main__":
    shutil.rmtree(CHURN, ignore_errors=True)
    race(old_walk, "OLD rglob under churn")
    race(new_walk, "NEW _iter_py under churn")
    shutil.rmtree(CHURN, ignore_errors=True)
    print("probe done")
