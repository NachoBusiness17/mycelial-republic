import json
import sys
from pathlib import Path

# Ensure project root is on sys.path so `mag` package imports work when run from tools/
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from mag import gpipes

if __name__ == '__main__':
    res = gpipes.fan_out(["Draft a creative brief", "Invent 3 alternative hooks"], provider="deepseek", timeout=300, tags=["test", "test"])
    print(json.dumps(res, indent=2, default=str))
