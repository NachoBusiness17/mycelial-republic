import sys
from pathlib import Path
sys.path.insert(0, r"c:\Users\foste\Documents\projects\local_sovereign_agent")
from mag import offerings as o
s = o.status()
print("RESULT n_bodies=" + str(s["n_bodies"]) + " vision_installed=" + str(s["bodies"].get("vision", {}).get("installed")))
from mag.work_register import record
kn = record("module", "vision-seat-deepseek",
            path="mag/vision.py",
            note="Agents can SEE: deepseek-v4-flash-vision-exp wired as mag/vision.py + the agent vision tool + offerings body. Base64-inline, browser UA, user-message images. Verified: aerial_tramway.png -> Cablecar (207/65 tokens).",
            claim={"statement": "the fleet has a working vision capability", "status": "Supported",
                   "basis": ["Evidence"], "evidence": ["vision test returned Cablecar", "tool + offerings registered"]})
print("fold verkle=" + str(kn["row"]["verkle"]))
