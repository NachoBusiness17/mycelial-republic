import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mag.governor_autorun import autorun_loop
from tools.instance_guard import guard_or_exit

# dogfood-48h move 4: singleton guard, exit 3 on a live twin (the descent
# twins double-drained $2.25 before this class had a guard anywhere).
guard_or_exit("autorun_loop")
autorun_loop(5.0)
