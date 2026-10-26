"""Phase 2 judge checks (pure python): ollama digest probe + freeze-mechanism already-covered scan + grok void-clause lines. No subprocess."""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")


def sec(t):
    print("\n" + "=" * 10 + " " + t + " " + "=" * 10)


sec("Q ollama /api/tags gemma digest probe (read-only GET loopback)")
try:
    with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=10) as resp:
        data = json.loads(resp.read())
    found = False
    for m in data.get("models", []):
        if "gemma" in m.get("name", "").lower():
            found = True
            print("name:", m.get("name"), "| digest:", m.get("digest"),
                  "| modified:", m.get("modified_at"))
    if not found:
        print("no gemma models listed")
except Exception as e:
    print("PROBE FAILED:", type(e).__name__, str(e)[:200])

sec("R already-covered scan for freeze-mechanism surface (interference + gitignore/unversioned/unpinned/digest/pin)")
bases = [ROOT / "watch", ROOT / "queue"]
pat_arm = re.compile(r"interference", re.I)
pat_mech = re.compile(r"gitignore|unversioned|unpinned|unhashed|mutable tag|model digest|pin the (model|serving)", re.I)
hits_any = False
for base in bases:
    if not base.exists():
        continue
    for f in base.rglob("*.md"):
        if not f.is_file():
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        if not any(pat_arm.search(l) for l in lines):
            continue
        for i, l in enumerate(lines):
            if pat_mech.search(l):
                hits_any = True
                print(f"{f.relative_to(ROOT)}:{i + 1}: {l.strip()[:180]}")
if not hits_any:
    print("NO md file mentioning interference also mentions the freeze-mechanism surface")

sec("S grok pass void-clause lines")
gp = ROOT / "watch/inbox/INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md"
for i, l in enumerate(gp.read_text(encoding="utf-8").splitlines()):
    if "voids the arm" in l or "freeze before launch" in l:
        print(f":{i + 1} {l.strip()[:180]}")

print("\nDONE PHASE 2")
