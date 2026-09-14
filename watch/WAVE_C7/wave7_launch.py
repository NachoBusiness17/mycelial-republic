#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""WAVE 7 (cycle 3) — the wide launch.  Driver/tender: Mag seat, 2026-09-11.

Width = 7 (the band maximum: never zero, never eight). Each slot is a NEW task that FOLLOWS UP
ON THE OLD (a cycle-1 or cycle-2 lane), carries the cycle-1/2 genetics (LEDGER ROW FIRST-CLASS,
ABSORB FIRST, MEASURE DON'T ASSUME, SEEDED+DENOMINATED, TRI-STATE+FALSIFIERS, ASSERT-THEN-WRITE,
NO SILENT PASS, CYCLE GENETICS), and the cycle-3 amendment:

    MICKY-17 CLAUSE — the worker writes "NEXT: <one line>" and then LAUNCHES ITS OWN MICKEY 17
    (one reprint, depth 1, via watch/WAVE_C7/spawn_reprint.sh) on that bounded task before folding.

Usage:
    python watch/WAVE_C7/wave7_launch.py            # write prompts + manifest, launch nothing
    python watch/WAVE_C7/wave7_launch.py --launch    # write then launch all 7, staggered
    python watch/WAVE_C7/wave7_launch.py --launch --slots 1,2,3
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
STAGE = os.path.join(ROOT, "watch", "WAVE_C7")
LEDGER = os.path.join(ROOT, "watch", "WAVE_LEDGER.jsonl")
DATE = "20260911"
MODEL = "glm-4.7[1m]"
STAGGER_S = 25
DATE_METHOD = "launched 2026-09-11 by the tender (Mag seat); ts = ISO Z UTC stamped at spawn"

COMMON = """You are WAVE WORKER slot {slot}, cycle 3 (WAVE 7 wide, tender-launched 2026-09-11) in the
local_sovereign_agent fleet wave. Repo = cwd = C:/Users/foste/Documents/projects/local_sovereign_agent.
Date now: {ts} (ISO Z UTC). Dating method: {date_method}; file mtimes are local.

Read first — they bind you: watch/NIGHT_FOLD_20260911.md (rotation at bounded width, no silent pass,
name your dating method) and watch/WAVE_CYCLE_GENETICS_20260911.md (the genetics you inherit).

LANE (WAVE_QUEUE follow-up on the old) — source card: {source}
{lane}

BOUNDS: read-only EXCEPT (1) your one output card watch/inbox/{card}, (2) one appended line in
watch/WAVE_LEDGER.jsonl, (3) {extra_write}. No chain writes (the verkle chain is read-only; orphans
reconcile by completion index, nothing is rebuilt). No credentials echoed — names only, never values.
No network posting; fetching only where this lane says so. $0 — free lane only, no paid API calls.
{bounds_extra}

PROTOCOL (genetics, in force since cycle 2 and binding on you):
A. ABSORB FIRST, CROSS-LINK IN 5 LINES: read the source card named above before working; your card's
   first 5 lines list the absorbed siblings (path + one-line take). If the source card already
   discharged this lane, say so in one line and pivot to the highest-value item on its remains/next
   list — do not re-do finished work.
B. LEDGER ROW IS FIRST-CLASS, NOT "LAST TASK": file the card AND append the ledger row in the same
   turn. Fields {{ts ISO Z, lane, worker, did, found, remains, prev, hash}}; prev = the hash field of
   the file's current last line, read immediately before the append (retry once if it moved); hash =
   first 16 hex of sha256(prev+"|"+ts+"|"+lane+"|"+worker). Single >> redirect; never rewrite rows.
   Your worker string is "w7s{slot}"; your lane string is "{lane_short}".
C. MEASURE, DON'T ASSUME: enumerate witnesses beyond the named ones (unindexed backups, sibling
   dirs); one schema-peek row before any field-level parse of an unfamiliar .jsonl (a line starting
   with something other than ts silently defeats prefix filters); name the dating method on every count.
D. SEEDED + DENOMINATED: samples are seeded and reproducible; a sample verdict carries its denominator
   and the line "widen before promoting to law".
E. TRI-STATE + FALSIFIERS: Supported / Disputed / Unproven with evidence; a FALSIFIERS section in the
   card.
F. ASSERT-THEN-WRITE (estate folds): sum-assert before write, .bak beside the file, JSON round-trip
   after, constant filename kept.
G. NO SILENT PASS: every failure, dead end or swallowed error is named in the card.
H. CYCLE GENETICS line at card end: what worked / what to change, one paragraph.
Card under ~150 lines. Dense, evidence-cited, plain English.

MICKY-17 CLAUSE (cycle-3 amendment; the wave's fold ritual — mandatory):
1. Your card's last content section before the genetics line is "NEXT: <one line>" — the single
   bounded task you judge should follow yours. Your lane's highest-confidence heir, not a wishlist.
2. Then LAUNCH YOUR MICKEY 17 before folding, with exactly one command:
       bash watch/WAVE_C7/spawn_reprint.sh {slot} "<that one line>"
   It appends a durable queue row to watch/WAVE_C7/reprint_queue.jsonl and starts ONE reprint worker
   (WAVE_DEPTH=1) on that bounded task after a stagger, logging to watch/WAVE_C7/reprint_{slot}_out.log.
   Run it ONCE. The reprint does the bounded task, files its own card, and does NOT spawn again.
3. Then FOLD (stop). If the reprint cannot start, name it in the card under NO SILENT PASS and still
   write NEXT: — the queue row is the durable half and the tender drains it.
4. Make the last line of your reply:  NEXT: <the same one line>
"""

SLOTS = [
    dict(
        slot=1,
        lane_short="loop_futility_audit",
        source="watch/inbox/ORCHESTRATOR_SEEDS_20260911.md, watch/inbox/HOLLOW_MASS_BODIES_20260911.md, "
               "memory/runs/ghost/autonomous_fixes/",
        lane="LOOP-FUTILITY AUDIT (cycle 1 slots 3+4 converge on this pointer). The janitor chased one FKB "
             "signal for 19 days while its escalation lane sat keyless. Diff the files the autonomous janitor "
             "actually wrote under memory/runs/ghost/autonomous_fixes/ against the FKB signal counts it "
             "claimed to chase: did 19 days of diagnosis close anything, or did the signal only grow "
             "(the x20 -> x138 trace)? Price the absent DEEPSEEK_OVERMIND_API_KEY as the era's cheapest "
             "unblock — its NAME only, never a value, and say whether the absence is the loop's cause or "
             "just its alibi.",
        card="LOOP_FUTILITY_AUDIT_20260911.md",
        extra_write="one summary line appended to watch/WAVE_C7/driver_notes.md",
        bounds_extra="Read-only lane: do not edit, move or delete anything under memory/runs/ghost/.",
    ),
    dict(
        slot=2,
        lane_short="step0_partition_recount",
        source="watch/inbox/RETROKNOTTER_PREP_20260911.md",
        lane="STEP-0 PARTITION RECOUNT AS A STANDALONE COUNTED ARTIFACT. Cycle 1 slot 1 showed the mission's "
             "two class counts use different censuses (2,960 silence files vs 13,693 never-referenced orphans) "
             "and acting on either alone would double-fold hundreds of knots. Ship the prerequisite the card "
             "asked for as its own file: the counted fold-eligibility partition, per class, under the "
             "three-gate eligibility rule, with the counting method and the census of each class named. "
             "Read-only toward the chain — count, do not fold.",
        card="STEP0_PARTITION_RECOUNT_20260911.md",
        extra_write="the standalone counted artifact watch/STEP0_PARTITION_20260911.json (a NEW file; "
                    "JSON round-trip validated after write)",
        bounds_extra="You own exactly one new artifact file plus your card. Nothing else on disk changes.",
    ),
    dict(
        slot=3,
        lane_short="nav_debt_reconcile",
        source="watch/inbox/NAV_REVERIFY_20260911.md (cycle 2 slot 9) and any NAV_WIRING law card it cites",
        lane="NAV DEBT RECONCILE (cycle 1's convergent 'nav fix lane', fed by cycle 2). NAV_REVERIFY already "
             "cleared the wiring check; do NOT re-verify what passed. Discharge the DEBTS that card named "
             "instead: the duplicate-target debt in the nav surface (the same ~10 targets appended twice, the "
             "63 -> 93 tail growth), the unreceipted dedupe pass on the birth-index file, and the receipt-count "
             "label off-by-one. For each debt: verdict (open / already-discharged-elsewhere / not-a-debt), "
             "evidence, and the exact write surface any fix would touch. Verify-file-exists-before-wiring per "
             "the NAV_WIRING law it cites.",
        card="NAV_DEBT_RECONCILE_20260911.md",
        extra_write="the receipt watch/NAV_DEBT_RECEIPT_20260911.json (a NEW file) recording each verdict",
        bounds_extra="At most ONE mutating edit in this lane, and only if it is a clean duplicate-target or "
                     "label fix in the file the source card names as debtor: .bak beside it, re-parse after, "
                     "exact before/after named in the card. If the edit is not clean, do not make it — write "
                     "the spec instead.",
    ),
    dict(
        slot=4,
        lane_short="salon_tier_b_mine",
        source="watch/inbox/SALON_REINGEST_T1A_20260911.md (cycle 2 slot 7) and the salon cards it names",
        lane="SALON TIER-B MINE (cycle-2 follow-up). Take the stratum the salon re-ingest left behind — its "
             "remains list is your lane verbatim. Drive every bibliographic ID the card could not prove to a "
             "verdict from artifacts ALREADY ON DISK: proven / unprovable-with-on-disk-artifacts / "
             "needs-network. $0 and no network: if proof requires a fetch, that is the verdict, not a task. "
             "Same for the ractor salon sessions the card flags as unmined: mine what is on disk, name what is not.",
        card="SALON_TIER_B_MINE_20260911.md",
        extra_write="the per-ID verdict table watch/SALON_TIER_B_VERDICTS_20260911.json (a NEW file)",
        bounds_extra="Read-only toward the salon cards and the corpus: you add two new files, nothing else.",
    ),
    dict(
        slot=5,
        lane_short="wow_txt_promotion",
        source="watch/inbox/WOW_TXT_MINED_20260911.md (cycle 2 slot 10)",
        lane="WOW.TXT PROMOTION + DISK CENSUS (cycle-2 follow-up). Work the promotion queue that card left: "
             "for each queued item, promote it, or say in one line why it should not be promoted, with the "
             "receipt path. Then take the disk census the same card flagged (the logs/ footprint, the "
             "unswept memory/runs/ strata) as a counted table: path, bytes, file count, last mtime, "
             "swept-or-not, and the one command that would sweep it. Count, do not sweep: deletion is not "
             "this lane's authority.",
        card="WOW_TXT_PROMOTION_20260911.md",
        extra_write="the promotion receipt watch/WOW_TXT_PROMOTION_RECEIPT_20260911.json (a NEW file)",
        bounds_extra="No deletions anywhere in this lane — the census is the deliverable, the sweep command "
                     "is the pointer.",
    ),
    dict(
        slot=6,
        lane_short="boot_audit_apply2",
        source="watch/inbox/BOOT_AUDIT_APPLIED_20260911.md (cycle 2 slot 8), AGENTS.md, CURRENT.md",
        lane="BOOT AUDIT, SECOND PASS (cycle-2 follow-up). The first pass applied most audit rows and "
             "deferred two. Discharge the deferred rows THIS cycle where the write surface is a doc the "
             "audit already owns: the CURRENT.md route line and the spine stamp (plus the launch-law "
             "cross-reference if the card lists it). Apply with .bak + re-read-after-write; anything that "
             "needs operator GO gets a one-line receipt saying exactly what GO would authorise instead of "
             "a half-applied edit.",
        card="BOOT_AUDIT_APPLY2_20260911.md",
        extra_write=".bak backups beside any doc you edit (no other new files)",
        bounds_extra="Edits limited to the doc rows the source card deferred: CURRENT.md and the spine "
                     "stamp surface it names — not AGENTS.md wholesale, not the chain.",
    ),
    dict(
        slot=7,
        lane_short="x_link_research_mine",
        source="watch/inbox/X_LINK_HARVEST_20260911.md (filed by the tender) with "
               "watch/X_HARVEST_DOCTRINE_20260905.md as the fallback law",
        lane="RESEARCH MINE — THE WINDOW'S DEPOSIT (the operator dropped a link into this window; this lane "
             "turns it into corpus). Source is the harvested link card if it exists; otherwise harvest per "
             "the doctrine first (the operator's link is PhysRevX status 2098109032472941015). Then mine: "
             "what is the paper's actual claim, which of our existing lanes does it touch, and what is the "
             "one bounded test or steal it enables here? Cite everything (URL or on-disk path per claim). "
             "Do not paste the abstract as the card — extract the claim, the mechanism, and the falsifier.",
        card="X_LINK_RESEARCH_MINE_20260911.md",
        extra_write="the extraction watch/X_LINK_EXTRACT_20260911.md if that file does not already exist "
                    "(the tender's harvest card is the preferred source; do not overwrite it)",
        bounds_extra="One fetch for the link at most, $0, no posting. If the network is dead, mine what is "
                     "already on disk and name the blocked fetch under NO SILENT PASS.",
    ),
]


def ts_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ledger_row(lane, worker, did, found, remains):
    """Append one row using the genetics recipe: prev = hash field of the current last line."""
    prev = ""
    try:
        with open(LEDGER, "r", encoding="utf-8") as fh:
            lines = [ln for ln in fh.read().splitlines() if ln.strip()]
        if lines:
            try:
                prev = json.loads(lines[-1]).get("hash", "")
            except Exception:
                prev = hashlib.sha256(lines[-1].encode("utf-8")).hexdigest()[:16]
    except FileNotFoundError:
        prev = "GENESIS"
    ts = ts_now()
    h = hashlib.sha256(("%s|%s|%s|%s" % (prev, ts, lane, worker)).encode("utf-8")).hexdigest()[:16]
    row = {"ts": ts, "lane": lane, "worker": worker, "did": did, "found": found,
           "remains": remains, "prev": prev, "hash": h}
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main():
    argv = sys.argv[1:]
    do_launch = "--launch" in argv
    slots = [s["slot"] for s in SLOTS]
    if "--slots" in argv:
        want = argv[argv.index("--slots") + 1]
        slots = [int(x) for x in want.split(",") if x.strip()]

    os.makedirs(STAGE, exist_ok=True)
    ts = ts_now()
    manifest = {"cycle": 3, "wave": "WAVE 7 wide", "width": 7, "model": MODEL,
                "tender": "mag-seat", "ts": ts, "date_method": DATE_METHOD, "slots": []}

    for s in SLOTS:
        if s["slot"] not in slots:
            continue
        prompt = COMMON.format(slot=s["slot"], ts=ts, date_method=DATE_METHOD,
                               source=s["source"], lane=s["lane"], card=s["card"],
                               extra_write=s["extra_write"], bounds_extra=s["bounds_extra"],
                               lane_short=s["lane_short"])
        ppath = os.path.join(STAGE, "slot%d_prompt.md" % s["slot"])
        with open(ppath, "w", encoding="utf-8") as fh:
            fh.write(prompt)
        lpath = os.path.join(STAGE, "slot%d_out.log" % s["slot"])
        entry = dict(slot=s["slot"], lane_short=s["lane_short"], card=s["card"],
                     prompt=ppath.replace(os.sep, "/"), log=lpath.replace(os.sep, "/"),
                     prompt_bytes=len(prompt.encode("utf-8")))
        if do_launch:
            # detached + staggered so the fleet never stacks past bounded width
            shell = ("sleep %d; cd '%s' || exit 1; timeout 3600 claude -p \"$(cat '%s')\" "
                     "--model '%s' --dangerously-skip-permissions >> '%s' 2>&1; "
                     "echo \"EXIT:$? $(date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ)\" >> '%s'"
                     % (26 * len(manifest["slots"]), ROOT, ppath, MODEL, lpath, lpath))
            proc = subprocess.Popen(["bash", "-c", shell],
                                    cwd=ROOT, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL, start_new_session=True)
            entry["pid"] = proc.pid
        manifest["slots"].append(entry)

    # launch canary: proves detached children survive their parent shell
    if do_launch:
        canary = ("sleep 90; date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ > '%s'; echo canary_ok >> '%s'"
                  % (os.path.join(STAGE, "canary_alive.txt").replace(os.sep, "/"),
                     os.path.join(STAGE, "canary_alive.txt").replace(os.sep, "/")))
        manifest["canary_pid"] = subprocess.Popen(
            ["bash", "-c", canary], cwd=ROOT, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, start_new_session=True).pid

    mpath = os.path.join(STAGE, "launch_manifest.json")
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    if do_launch:
        row = ledger_row("wave7_launch", "tender-mag",
                         "launched WAVE 7 wide: %d slots, staggered, cycle-3 genetics + MICKY-17 clause"
                         % len(manifest["slots"]),
                         "manifest %s; reprints queue at watch/WAVE_C7/reprint_queue.jsonl" % mpath.replace(os.sep, "/"),
                         "7 cards + 7 ledger rows + up to 7 depth-1 reprint cards; tender verifies then writes the cycle-3 handoff")
        print("ledger row:", json.dumps(row))
    print("manifest:", mpath.replace(os.sep, "/"))
    print(json.dumps(manifest, indent=2)[:2000])


if __name__ == "__main__":
    main()
