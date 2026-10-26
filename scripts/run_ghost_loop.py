import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mag.ghost import cycle

while True:
    try:
        cycle()
    except Exception:
        pass
