# B2-53 queue repair script (2026-09-26).
# Incident: B2-53 first appended self-feeds as B2-125/126/127 against a stale
# census (highest was actually B2-132), then removed them with a prefix filter
# that also caught six pre-existing lines from concurrent lanes. Four are
# restored verbatim from the owning lanes' own scripts. Two could not be
# recovered from any on-disk source and are filed as owed in the note below.
# Laws: .venv python, no heredoc at call time, no em-dashes.
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "QUEUE.md"

restored = [
    # verbatim from watch/inbox/burn_wave_20260926/B2_52_ledger_queue.py:22-24
    "- [ ] B2-125 Execute the B2-52 bridge GO card on operator GO: run the 7 steps (Drive install fostertron@gmail.com, fleet stop, same-volume move, mklink /J per protocol :27, upload wait, git rev-parse HEAD identical both paths + doctor + :8765) and file the post-execution receipt; pointer watch/inbox/burn_wave_20260926/B2_52_bridge_card_20260926.md.",
    "- [ ] B2-126 Laptop bootstrap receipt: when the bridge or the travel kit first lands on the laptop, file the protocol :31-35 receipt (archive old backup folder by rename, git worktree prune, ensure_venv.ps1 rebuild, mag.cmd doctor) plus the first one-machine-live switch log; pointer watch/inbox/TWO_MACHINE_SYNC_20260919.md.",
    "- [ ] B2-127 Doctor same-volume-remote check: a git remote whose path sits on the same volume as the repo should be named same-disk (not a backup) in mag/doctor.py output, so the Sep-16-stale Mag-backup.git stops reading as off-machine protection; pointer watch/inbox/burn_wave_20260926/B2_52_bridge_card_20260926.md evidence section.",
    # verbatim from watch/inbox/burn_wave_20260926/B2_37_ledger_queue.py:43-47
    "- [ ] B2-127 PROVIDER_HEALTH nous cell erratum: the scoreboard row at watch/inbox/PROVIDER_HEALTH_20260926.md:17 says \"no rate headers exposed\" but B2_04_probe_results.json:608-623 records the full nous x-ratelimit set (50 req/min, 500k tok/min, 2100/h, 6M/h); fix the one cell to cite the measured headers and keep the 0 x 429 sub-claim.",
]

new_briefs = [
    "- [ ] B2-133 Ask 3 source repair before any Grok refire: FlashREINFORCE/GPO/RPG/BPO live only as memory/corpus/LINKS.jsonl:32 (LINKS-283, one row); watch/inbox/LINKS.jsonl has zero rows for those names or arxiv ids and the packet fallback memory/live_from_grok.md is a 17-line telemetry stub; mirror the row into watch/inbox/LINKS.jsonl or amend watch/inbox/GROK_LANE_PACKET_20260925.md:25 so the seat never fires with no on-disk source (fabrication pressure).",
    "- [ ] B2-134 Arm C 200-leg close-out fold: close receipt froze ARM C budget-200 at RUNNING 1/30 (n=1, no claims) ~04:45Z 09-26 with leg completion listed open; when the leg lands, fold the final solve count into BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md and correct the >=15/30 secondary reading against the trained-judge 30/30 interference reference; pointers watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md:13-14,54-55 + watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md:24-28.",
    "- [ ] B2-135 Grok Ask 4 scope freeze: the packet \"about 20 files\" line now faces 52 BURN_*/SEED_SALON_* files in watch/inbox (37 dated 20260925, 14 dated 20260926, none 09-24), so an unfired audit burns the seat window on post-packet filings; bind the audit to the 20260925 set and park the 14 new files as a second-wave ask; pointers watch/inbox/GROK_LANE_PACKET_20260925.md:32 + watch/inbox census 2026-09-26.",
]

note = """## Restoration note (B2-53, 2026-09-26)

While renumbering its own self-feeds (first appended as B2-125/126/127 against a
stale census, highest was actually B2-132, refiled below as B2-133/134/135), the
B2-53 lane removed its three lines with a startswith filter that also caught six
pre-existing lines from concurrent lanes claiming B2-125/126/127. Four are
restored above verbatim from the owning lanes' own scripts
(B2_52_ledger_queue.py:22-24 and B2_37_ledger_queue.py:43-47). Two further
deleted lines (prefixes B2-125/126/127, owning lane unidentified; no on-disk
quote exists in any burn_wave script, receipt, or memory/burns/LEDGER.jsonl row)
could NOT be recovered and are filed as owed: the owning lane must re-append its
brief. Treat B2-125/126/127 as contested numbers per B2-107 until then.
"""

text = QUEUE.read_text(encoding="utf-8")
if text and not text.endswith("\n"):
    text += "\n"
text += "\n".join(restored) + "\n" + "\n".join(new_briefs) + "\n" + note
QUEUE.write_text(text, encoding="utf-8", newline="")
print("restored:", len(restored), "new:", len(new_briefs), "note appended")
