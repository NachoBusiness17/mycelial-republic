"""verify_seal — check every file in MANIFEST.sha256 against its hash. Exit 0 = intact."""
import hashlib, sys
from pathlib import Path

root = Path(__file__).resolve().parent
bad = missing = 0
rows = [r for r in (root / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines() if r.strip()]
for row in rows:
    want, _, rel = row.partition("  ")
    f = root / rel
    if not f.is_file():
        print(f"MISSING  {rel}"); missing += 1; continue
    got = hashlib.sha256(f.read_bytes()).hexdigest()
    if got != want:
        print(f"DRIFT    {rel}"); bad += 1
print(f"{len(rows) - bad - missing}/{len(rows)} verified, {bad} drifted, {missing} missing")
sys.exit(0 if (bad == 0 and missing == 0) else 1)
