# B2-52 lane script: append one LEDGER.jsonl row (json.dumps, never heredoc) + self-feed QUEUE briefs.
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[3]
ledger = root / "memory" / "burns" / "LEDGER.jsonl"
queue = root / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-52-off-machine-bridge-card",
    "verdict": "landed: HARD FINDING proven from host bytes on all three axes (fsutil reparsepoint query empty + GetFileAttributesW 0x10 on the repo path = no junction; no Drive File Stream in Program Files, no GoogleDrive folder in the profile = no client; git remote local = C:\\Users\\foste\\Documents\\projects\\Mag-backup.git same volume C:, bare mtime Sep 16 18:17 = same-disk backup); operator-GO card written from protocol Host setup :22-29 verbatim (Drive install fostertron@gmail.com mirror, fleet stop, same-volume move, mklink /J :27, upload wait, byte-identical verify via git rev-parse HEAD both paths + doctor + :8765) plus the :15-20 one-machine-live contract; card only, no installs, no moves",
    "landing": "watch/inbox/burn_wave_20260926/B2_52_bridge_card_20260926.md",
    "one_line": "the 09-19 sync protocol was never executed here (proven byte-level) and the exact 7-step operator-GO card now exists so the full-fidelity Drive layer can be stood up on one GO",
}

before = ledger.read_text(encoding="utf-8").rstrip("\n")
ledger.write_text(before + "\n" + json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
print("ledger rows now:", len(before.splitlines()) + 1)

briefs = """- [ ] B2-125 Execute the B2-52 bridge GO card on operator GO: run the 7 steps (Drive install fostertron@gmail.com, fleet stop, same-volume move, mklink /J per protocol :27, upload wait, git rev-parse HEAD identical both paths + doctor + :8765) and file the post-execution receipt; pointer watch/inbox/burn_wave_20260926/B2_52_bridge_card_20260926.md.
- [ ] B2-126 Laptop bootstrap receipt: when the bridge or the travel kit first lands on the laptop, file the protocol :31-35 receipt (archive old backup folder by rename, git worktree prune, ensure_venv.ps1 rebuild, mag.cmd doctor) plus the first one-machine-live switch log; pointer watch/inbox/TWO_MACHINE_SYNC_20260919.md.
- [ ] B2-127 Doctor same-volume-remote check: a git remote whose path sits on the same volume as the repo should be named same-disk (not a backup) in mag/doctor.py output, so the Sep-16-stale Mag-backup.git stops reading as off-machine protection; pointer watch/inbox/burn_wave_20260926/B2_52_bridge_card_20260926.md evidence section.
"""
with queue.open("a", encoding="utf-8") as f:
    f.write(briefs)
print("queue briefs appended: B2-125, B2-126, B2-127")
