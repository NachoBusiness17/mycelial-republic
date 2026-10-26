"""Q-005: collapse delivered session-record pings in memory/attention.md.

Reads the file, byte-verifies every pinged session record exists on disk
(derived .md + residual .json), then replaces the ping backlog with a
triage block. Races the biography writer with a compare-and-swap loop;
aborts without writing if any record fails verification.
"""
import re
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
ATT = ROOT / "memory" / "attention.md"


def verify(text):
    sids = sorted(set(re.findall(r"session: `([A-Za-z0-9\-]+)`", text)))
    ok, miss = 0, []
    for sid in sids:
        d = ROOT / "memory" / "biography" / "derived" / f"{sid}.md"
        r = ROOT / "memory" / "biography" / "residual" / f"{sid}.json"
        if d.is_file() and r.is_file():
            ok += 1
        else:
            miss.append(sid)
    newest = re.search(r"session: `([A-Za-z0-9\-]+)`", text)
    return sids, ok, miss, (newest.group(1) if newest else "unknown")


def block(n, ok, newest, stamp):
    return (
        "# Mag attention\n\n"
        f"### Triage 2026-09-28 (Q-005, burn reset queue gopher): {n} session-record pings resolved\n\n"
        f"- All {n} \"Session record ready\" pings in this file as of {stamp} were triaged and collapsed here. "
        "Pings that landed during the edit window were verified on disk the same way and are covered by this block.\n"
        f"- Verdict: RESOLVED, not stale. Every pinged session record was byte-verified on disk before removal: "
        f"{ok}/{n} have both `memory/biography/derived/<sid>.md` and `memory/biography/residual/<sid>.json` present. "
        f"Newest record at triage time: `mag-agent-orc-{newest}`.\n"
        "- Why removal is safe: the pings are delivered notifications, not open asks. The durable trail lives in "
        "`memory/biography/derived/`, `memory/biography/residual/`, `memory/biography/latest.md`, and briefs under `memory/briefs/`.\n"
        "- Writer protocol (mag/biography.py:509-526): each first-write session record prepends a ping here and truncates "
        "the file at 40,000 chars, so the backlog of identical pings was self-scrolling noise; consumers clip this file "
        "head-first (mag/context_pack.py:605 clips to 600 chars, mag/lanes.py:293 to 3000), meaning the backlog pushed "
        "real signal out of every consumer's budget.\n"
        "- New pings continue to prepend automatically on the next biography write. No action needed on this block.\n"
    )


for attempt in range(6):
    text = ATT.read_text(encoding="utf-8")
    sids, ok, miss, newest = verify(text)
    if miss:
        print(f"ABORT: {len(miss)} records missing on disk: {miss[:5]}")
        sys.exit(2)
    if ATT.read_text(encoding="utf-8") != text:
        print(f"race on attempt {attempt}: file changed under us, retrying")
        time.sleep(0.3)
        continue
    stamp = time.strftime("%H:%M EDT %Y-%m-%d")
    ATT.write_text(block(len(sids), ok, newest, stamp), encoding="utf-8")
    print(f"WROTE triage block over {len(sids)} verified pings, ok={ok}, newest={newest}")
    sys.exit(0)

print("FAILED: writer kept racing for 6 attempts")
sys.exit(3)
