#!/usr/bin/env python3
"""STATELESS VISOR: cross-session, cross-job observability board.

Operator order 2026-09-26: "be context aware of every other active session and
background jobs... a stateless visor where they all communicate."

Design: the visor owns nothing and remembers nothing. Every invocation recomputes
the whole board from bytes on disk (the hypervisor-board pattern: the board is a
read-only view over shared surfaces; the surfaces ARE the communication).

Surfaces scanned:
  - ~/.zcode/cli/agents/<sess>/*.txt   background agent transcripts (mtime = liveness)
  - ~/.zcode/cli/exec/<sess>/*.log     background exec logs (mtime = liveness)
  - .zcode/workflow-drafts/*.dwf.ts    workflow scripts (mtime = recent amend/launch)
  - memory/workflows/REGISTRY.jsonl    gate submissions
  - memory/burns/LEDGER.jsonl          burn receipts
  - watch/inbox/EVENTS.jsonl           fleet events
  - logs/hermes_dual_20260926.jsonl    hermes burn progress
  - queue/queue_index.jsonl            queue roam state
  - billboard surfaces                 writer liveness (Q3, GAP 3 of
                                        ATLAS_SELF_STEAL_20260927: per surface
                                        last-write age + writer identity, so a
                                        starving lane or a dead feed shows up
                                        as a class instead of hiding in one
                                        trail row)

Read-only: never writes, never signals, never gates. Exit 0 always (a board).
"""
import glob
import json
import os
import re
import sys
import time

HOME = os.path.expanduser("~")
ZCLI = os.path.join(HOME, ".zcode", "cli")
ACTIVE_WINDOW_SEC = 60 * 20  # 20 minutes = live
LIVE_WRITE_SEC = 24 * 3600  # billboard: written within 24h = live writer
STALE_WRITE_SEC = 7 * 86400  # billboard: 24h..7d = stale, > 7d = dead

# Writer-liveness table (Q3, GAP 3 of ATLAS_SELF_STEAL_20260927). Hardcoded on
# purpose: the table IS the org chart of billboards. Liveness is always the
# surface mtime; the writer string is the identity claim. Third field marks the
# one surface whose deliberate shutdown is a FROZEN banner, not an age fact.
BILLBOARD_SURFACES = [
    ("dashboard/static/deck.html", "scripts/build_deck.py", False),
    ("dashboard/static/DAY_WORK_DIGEST.md", "lane_runner day_work lane", False),
    ("dashboard/static/trails/day_work.jsonl", "lane mirror", False),
    ("memory/briefs/latest.md",
     "mag/brief_local.py + mag/session_state_brief.py (sealed by banner)", True),
    ("state/CURRENT.md", "agent_cli live seat state mirror", False),
    ("memory/attention.md", "act/biography/chronicle attention writers", False),
    ("memory/bonds_active.md", "mag/bonds.py", False),
    ("dashboard/static/drift_board.html", "tools/drift_dashboard.py", False),
    ("watch/inbox/INDEX.json", "mag/shared_surface.py", False),
    ("queue/queue_index.jsonl",
     "unattributed (no repo writer found 2026-09-27)", False),
]


def age_str(mtime):
    a = time.time() - mtime
    if a < 90:
        return str(int(a)) + "s"
    if a < 5400:
        return str(int(a // 60)) + "m"
    if a < 172800:
        return str(int(a // 3600)) + "h"
    return str(int(a // 86400)) + "d"


def last_line(path, maxlen=110):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = [l.rstrip() for l in f if l.strip()]
        if not lines:
            return "(empty)"
        return lines[-1][:maxlen]
    except OSError as e:
        return "(unreadable: " + str(e)[:60] + ")"


def scan_zcli(label, pattern):
    rows = []
    now = time.time()
    for path in glob.glob(pattern):
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            continue
        rows.append((mtime, path))
    rows.sort(reverse=True)
    live = [r for r in rows if now - r[0] < ACTIVE_WINDOW_SEC]
    print("")
    print("== " + label + ": " + str(len(rows)) + " total, " + str(len(live)) + " live (mtime < 20m)")
    for mtime, path in rows[:8]:
        flag = "LIVE " if now - mtime < ACTIVE_WINDOW_SEC else "     "
        rel = path.replace(HOME, "~")
        print("  " + flag + age_str(mtime).rjust(5) + "  " + os.path.basename(path)[:60] + "  | " + last_line(path))
    if len(rows) > 8:
        print("  ... and " + str(len(rows) - 8) + " older")


def tail_jsonl(label, path, count=3):
    rows = []
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(line)
    except OSError:
        print("")
        print("== " + label + ": MISSING (" + path + ")")
        return
    print("")
    print("== " + label + ": " + str(len(rows)) + " rows")
    for line in rows[-count:]:
        try:
            r = json.loads(line)
            brief = {k: (str(v)[:90]) for k, v in list(r.items())[:4]}
            print("  " + json.dumps(brief, ensure_ascii=False))
        except json.JSONDecodeError:
            print("  " + line[:110])


def frozen_banner_present(path):
    """True when the surface opens with a FROZEN banner (deliberate shutdown).

    Same contract the sealed writers enforce (mag/brief_local.py and
    mag/session_state_brief.py, P0-1 warm-face law 2026-09-26): first 240
    chars, BOM stripped, startswith '# FROZEN'. Mirrored here byte-for-byte
    so the visor's FROZEN verdict can never disagree with the seal check;
    verified against the frozen brief 2026-09-27.
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(240)
    except OSError:
        return False
    return head.lstrip("\ufeff").startswith("# FROZEN")


def classify_billboard(path, is_freezable):
    """(class, mtime) for one billboard surface. MISSING beats everything,
    FROZEN beats age math (a sealed writer with a fresh banner touch is still
    deliberately shut, not live), then LIVE/STALE/DEAD by age thresholds."""
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return "MISSING", None
    if is_freezable and frozen_banner_present(path):
        return "FROZEN", mtime
    age = time.time() - mtime
    if age < LIVE_WRITE_SEC:
        return "LIVE", mtime
    if age < STALE_WRITE_SEC:
        return "STALE", mtime
    return "DEAD", mtime


def digest_stalled_lanes(path):
    """Lane names the digest itself flags as stalled, or None if unreadable.

    Two shapes honored: an inline bold marker naming its lane (on-disk shape
    2026-09-27: '... **elder STALLED-TRAIL** (324B = open row only ...)') and
    a 'STALLED' heading section whose bullets name one lane each. Returns []
    when the digest is readable but flags nothing (not the same as None).
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return None
    names = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            in_section = "stalled" in stripped.lower()
            continue
        if in_section:
            body = stripped.lstrip("-* ").strip()
            if body:
                token = body.split()[0].rstrip(":,;")
                if token.lower() != "stalled" and token not in names:
                    names.append(token)
            continue
        for m in re.finditer(r"\*\*([A-Za-z0-9_.-]+)\s+STALLED", line):
            if m.group(1) not in names:
                names.append(m.group(1))
    return names


def scan_billboards():
    counts = {}
    print("")
    print("== billboard writer liveness: " + str(len(BILLBOARD_SURFACES))
          + " surfaces (LIVE < 24h / STALE < 7d / DEAD > 7d / FROZEN = banner)")
    for path, writer, is_freezable in BILLBOARD_SURFACES:
        cls, mtime = classify_billboard(path, is_freezable)
        counts[cls] = counts.get(cls, 0) + 1
        age = age_str(mtime) if mtime is not None else "-"
        row = "  " + cls.ljust(7) + age.rjust(6) + "  " + path
        row += "  | writer: " + writer
        if re.fullmatch(r"[A-Za-z0-9_./\\-]+\.py", writer) and not os.path.exists(writer):
            row += "  (writer script MISSING)"
        print(row)
    print("  tally: " + " / ".join(k + " " + str(v) for k, v in sorted(counts.items())))
    stalled = digest_stalled_lanes(os.path.join("dashboard", "static", "DAY_WORK_DIGEST.md"))
    if stalled is None:
        print("  stalled lanes (digest self-report): digest unreadable")
    elif not stalled:
        print("  stalled lanes (digest self-report): none flagged")
    else:
        print("  stalled lanes (digest self-report): " + ", ".join(stalled))


def main():
    print("STATELESS VISOR " + time.strftime("%Y-%m-%d %H:%M:%S"))
    sess_agents = os.path.join(ZCLI, "agents", "sess_*", "*.txt")
    sess_exec = os.path.join(ZCLI, "exec", "sess_*", "*.log")
    scan_zcli("background agents (all sessions)", sess_agents)
    scan_zcli("background exec logs (all sessions)", sess_exec)

    drafts = sorted(glob.glob(".zcode/workflow-drafts/*.dwf.ts"), key=os.path.getmtime, reverse=True)
    print("")
    print("== workflow drafts: " + str(len(drafts)) + " (most recent = most recent launch/amend)")
    for path in drafts[:6]:
        print("  " + age_str(os.path.getmtime(path)).rjust(5) + "  " + os.path.basename(path)[:70])

    tail_jsonl("workflow gate registry", os.path.join("memory", "workflows", "REGISTRY.jsonl"), 3)
    tail_jsonl("burn ledger", os.path.join("memory", "burns", "LEDGER.jsonl"), 4)
    tail_jsonl("fleet events", os.path.join("watch", "inbox", "EVENTS.jsonl"), 3)
    tail_jsonl("hermes dual burn", os.path.join("logs", "hermes_dual_20260926", "output.jsonl"), 3)

    # Dirac loops (2026-09-27): the operational graph's open holonomies —
    # read-only rank line; a growing open_gaps count is unbanked tesuji.
    try:
        import sys as _sys

        _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if _root not in _sys.path:
            _sys.path.insert(0, _root)
        from tools.dirac_loop_shim import dirac_rank  # type: ignore

        r = dirac_rank()
        print("== dirac loops: beta1=" + str(r.get("betti1"))
              + " vertices=" + str(r.get("n_vertices"))
              + " edges=" + str(r.get("n_edges")))
    except Exception as e:
        print("== dirac loops: unavailable (" + str(e)[:60] + ")")

    qi = os.path.join("queue", "queue_index.jsonl")
    if os.path.exists(qi):
        roamed = 0
        total = 0
        bad = 0
        with open(qi, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                total += 1
                try:
                    if json.loads(line).get("roamed"):
                        roamed += 1
                except json.JSONDecodeError:
                    # count the unparseable row, never silently skip it
                    # (ratchet except-pass fix 2026-09-27)
                    bad += 1
        print("")
        print("== queue index: " + str(roamed) + "/" + str(total) + " roamed"
              + (", " + str(bad) + " unparseable" if bad else ""))

    scan_billboards()
    print("")
    print("(stateless: this board is recomputed from bytes every run; the visor owns nothing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
