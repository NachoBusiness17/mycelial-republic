"""B2-85 board landing per the shared-file claim law (QUEUE.md header).
Sequence inside one pass to shrink the collision window:
  1. append the CLAIM B2-85 line at the top of Open (claim BEFORE reading bytes to edit)
  2. re-read the board bytes (the claim law's re-read trigger)
  3. verify anchors are unique, then land: B2-85 row landing note + receipt pointer,
     CLAIM retirement in place, 3 self-fed briefs UNCHECKED.
Idempotent-ish: refuses to run if the landing marker is already present.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

QUEUE = Path(__file__).with_name("QUEUE.md")
RECEIPT = "watch/inbox/burn_wave_20260926/B2_85_powershell_fix_20260926.md"
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

text = QUEUE.read_text(encoding="utf-8")
if "B2_85_powershell_fix_20260926.md" in text:
    print("B2-85 landing already present on board; aborting (no double-land)")
    sys.exit(2)

# --- step 1: claim line, before reading further bytes for editing ---
claim_line = f"- CLAIM B2-85 watch/inbox/burn_wave_20260926/QUEUE.md {now} (B2-85 board landing: own-row landing note + receipt pointer, 3 self-fed briefs)"
anchor = "## Open\n"
if text.count(anchor) != 1:
    print("Open anchor not unique; aborting")
    sys.exit(2)
text = text.replace(anchor, anchor + claim_line + "\n", 1)
QUEUE.write_text(text, encoding="utf-8")

# --- step 2: re-read bytes (claim law re-read trigger) ---
text = QUEUE.read_text(encoding="utf-8")

# --- step 3: verify anchors, then land ---
row_marker = "- [x] B2-85 Bare-powershell PATH fix propagation:"
if text.count(row_marker) != 1:
    print("B2-85 row not unique on re-read; aborting without landing")
    sys.exit(2)

row_line = row_marker + " run_shell:e566037def80 \"[Errno 2] ... powershell\" 11,818 FKB events since 2026-09-19 (228 today, logs/failure_kb.jsonl); fix pattern exists at mag/process_reaper.py:82-90 (shutil.which + System32 fallback with receipt comment) but 8 modules still call bare [powershell]: gpu_ghost.py:84, legacy_audit.py:181, icon_drop.py:131, offerings.py:152, platform_kill.py:65, loop_breaker.py:99, saelis_room.py:57, power.py:165; propagate + re-run the calling flows."
if text.count(row_line) != 1:
    print("B2-85 row full-text anchor not unique (concurrent edit?); aborting")
    sys.exit(2)

landing_note = (" Landed 2026-09-26 (row sat pre-checked [x] with no receipt before this landing, the B2-238 disease; this landing earns it): "
                "all 10 bare-powershell sites fixed, including the root writer tools/shell.py:42 (the run_shell tool whose FileNotFoundError string IS the sig) "
                "plus power.py:203 found by sweep; byte recount 7,964 events since 2026-09-19 and 238 today at census (the brief's 11,818/228 are stale); "
                "flow probe watch/inbox/burn_wave_20260926/B2_85_flow_probe_results.json all_ok 10/10 incl. forced psutil-ImportError branches "
                "(10/2/2 rows, zero Errno 2) and a live amd-cim GPU read; targeted pytest 11 passed; ratchet check --changed NEW=0; "
                "straggler sites source_trace.py:160, box_burn_watch.py:31, lattice_check.py:47+66 self-fed B2-352; "
                f"receipt {RECEIPT}.")
text = text.replace(row_line, row_line + landing_note, 1)

if text.count(claim_line) != 1:
    print("own claim line not unique on re-read; aborting")
    sys.exit(2)
retired = claim_line.replace("- CLAIM B2-85", "- CLAIMED B2-85", 1) + f" -> {RECEIPT}"
text = text.replace(claim_line, retired, 1)

feeds = [
    ("- [ ] B2-352 Finish the B2-85 sweep on the stragglers: (self-fed by B2-85) four bare powershell call sites outside the briefed 8 still carry the same [Errno 2] disease (mag/source_trace.py:160 CIM fallback, tools/box_burn_watch.py:31, scripts/lattice_check.py:47 and :66); apply the process_reaper resolution pattern (shutil.which + powershell.exe + System32 fallback + receipt comment naming the sig) and re-run each calling flow; falsifier: grep '\\[\"powershell\"' over mag/ tools/ scripts/ returns zero live-code hits; pointers watch/inbox/burn_wave_20260926/B2_85_powershell_fix_20260926.md, mag/process_reaper.py:82-90."),
    ("- [ ] B2-353 Pin the tools/shell.py powershell resolution: (self-fed by B2-85) the run_shell root fix (shutil.which + System32 fallback) has no test, so a refactor back to the bare literal silently re-opens the 7,964-row failure class; add tests/test_shell_powershell_resolution.py pinning that run_shell executes an allowlisted command when shutil.which returns None (System32 path taken, no FileNotFoundError mentioning powershell); falsifier: revert tools/shell.py to the bare [\"powershell\"] literal and the new test must fail; pointers tools/shell.py:40-56, watch/inbox/burn_wave_20260926/B2_85_powershell_fix_20260926.md."),
    ("- [ ] B2-354 icon_drop honesty beyond the no-powershell skip: (self-fed by B2-85) drop_shortcut passes check=False and writes status dropped without checking returncode or that the .lnk exists, so a failed WScript.Shell Save still lands a dropped ledger row (B2-85 landed only the skipped_no_powershell arm); verify the .lnk exists after the run and record a failed status naming the error when it does not; falsifier: a drop_shortcut whose powershell exits nonzero must not record dropped; pointers mag/icon_drop.py drop_shortcut, watch/inbox/burn_wave_20260926/B2_85_powershell_fix_20260926.md."),
]
feed_block = "\n".join(feeds)
# insert the self-fed briefs directly after the (now extended) B2-85 row line
idx = text.find(landing_note)
if idx == -1:
    print("landing note not found after replace; aborting")
    sys.exit(2)
line_end = text.find("\n", idx)
text = text[:line_end] + "\n" + feed_block + text[line_end:]

QUEUE.write_text(text, encoding="utf-8")
print("LANDED: claim retired, B2-85 row note + pointer, self-feeds B2-352/353/354 unchecked")
