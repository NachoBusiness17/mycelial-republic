"""Run ghost_memlance.select() and write the result to disk (reliable despite flaky terminal)."""
import sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from mag import ghost_memlance  # noqa: E402

out = ghost_memlance.select(
    "Saelis the Mirror Sea invariant, D&D tabletop DM game party frontier seats, "
    "desktop Electron seat CDP direct-DOM steal, clipboard-paste not keystroke typing, "
    "DeepSeek swarm standing wave, emerging game state observers",
    k=8,
)
dst = ROOT / "memory" / "runs" / "memlance_select.json"
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print("wrote", dst.relative_to(ROOT))
