import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

# pythonw trap: sys.stdout/stderr are None under the headless interpreter,
# and stealth_driver's loop prints would raise AttributeError and kill the
# process silently. Route them to a rolling log instead.
LOG = ROOT / "logs" / "stealth_driver_stdout.log"
LOG.parent.mkdir(parents=True, exist_ok=True)
if sys.stdout is None:
    sys.stdout = open(LOG, "a", encoding="utf-8", buffering=1)
if sys.stderr is None:
    sys.stderr = sys.stdout or open(LOG, "a", encoding="utf-8", buffering=1)

from stealth_driver import main  # noqa: E402
from tools.instance_guard import guard_or_exit  # noqa: E402

# dogfood-48h move 4: singleton guard, exit 3 on a live twin (two stealth
# driver pids rode together 09-29, the boot-lane double-launch disease).
guard_or_exit("stealth_driver")

sys.exit(main())
