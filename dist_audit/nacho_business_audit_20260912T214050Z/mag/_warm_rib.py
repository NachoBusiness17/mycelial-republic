import sys
from pathlib import Path
sys.path.insert(0, r"c:\Users\foste\Documents\projects\local_sovereign_agent")
ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")

# 1) dump the FROZEN_RIB to a file for the zcode CLI seat + operator
from mag.rib_cache import FROZEN_RIB
dest = ROOT / "queue" / "handoff" / "zcode" / "RIB.md"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(FROZEN_RIB + "\n", encoding="utf-8")
print("RIB written -> " + str(dest.relative_to(ROOT)))
print("chars=" + str(len(FROZEN_RIB)) + " tokens_est=" + str(len(FROZEN_RIB) // 4))

# 2) warm the cache: one rib_chat call with the frozen prefix, confirm cached_tokens
from mag.rib_cache import rib_chat
w = rib_chat("Cache-warm handshake for the zcode CLI session. Reply with exactly: warm")
print("warm_call ok=" + str(w.get("ok")) + " cached=" + str(w.get("cached_tokens")) +
      "/" + str(w.get("prompt_tokens")) + " text=" + str(w.get("text"))[:40])
