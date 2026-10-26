#!/usr/bin/env python3
"""B2-96 board landing: retire claims, landing note, self-feeds (2026-09-26).

Targeted string surgery on QUEUE.md with an mtime guard (the B2-373 pattern):
the board is hot, so the script re-reads and retries when the mtime moves.
Self-feed numbers are computed at run time as board-highest+1 so concurrent
lanes cannot be collided (B2-167 renumber law); the landing note carries the
numbers actually used.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"
CLAIM_TS = "2026-09-26T18:33:30Z"
ROW_TAIL = "pointer scan-2026-09-26T04-10-04.918Z-41fc75fa84c4 findings.json."


def self_feeds(n1: int, n2: int, n3: int) -> str:
    return (
        f"- [ ] B2-{n1} Fix the live runner-driven scripts/ ssrf/path set: "
        f"(self-fed by B2-96) the triage left 17 occurrences in 4 files as must-fix "
        f"because real drivers execute them, so pin the input surfaces: "
        f"scripts/desk_baseline_probe.py _http_get_json/_http_get_text take caller URLs "
        f"(flagged :42/:53/:218/:231) and are fired by configs/coding_session_loop.yaml:23, "
        f"mag/coding_session_loop.py:241 and mag/governor_autorun.py:374, so pin the "
        f"probe URL allowlist to config constants with a fixture test; "
        f"scripts/hunger_ledger.py writes LEDGER at :120/:147 and is the canonical "
        f"fallback of mag/lane_runner.py:545, so pin the ledger path derivation; "
        f"scripts/wave_driver.py writes args.board/task/res paths (:195/:417/:521/:613/:745-755) "
        f"and scripts/m12_pairing.py writes base/steers/inbox (:391/:398/:405/:438), so pin "
        f"each write target to repo-root-derived constants; falsifier: a test that passes a "
        f"repo-external path or URL to any of the four entry points still lands a write or "
        f"a request after the fix; pointers watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md "
        f"Evidence section, configs/violation_baseline.json (the 20 accepted claims name the "
        f"un-accepted live set).\n"
        f"- [ ] B2-{n2} File the wave_driver scheduling truth: (self-fed by B2-96) the "
        f"2026-09-12 execution wave staged a night cron for the driver (21:15 tick + 06:45 "
        f"M12 close per queue/handoff/zcode/CONVO.md) but the 2026-09-26 schtasks full census "
        f"(332 tasks) holds zero wave_driver/m12_pairing entries, so the LOOK/JUDGE/ACT/RECORD "
        f"heartbeat organ (HEARTBEAT_TTL_S = 900, driver presumed dead past TTL) currently runs "
        f"only under tests/test_wave_driver.py + tests/wave_driver_test.py and manual launch, "
        f"while estate prose still implies a night loop; either re-stage the driver tick with a "
        f"receipt naming the task name and cadence, or register the driver as test-driven-only "
        f"in the organ docs and correct the CONVO-era prose pointers; falsifier: any doc or card "
        f"claiming the night driver runs while a fresh schtasks census has no entry survives the "
        f"pass; pointers scripts/wave_driver.py:66-84, watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md.\n"
        f"- [ ] B2-{n3} Pin the hunger_ledger cage/canonical divergence: (self-fed by B2-96) "
        f"mag/lane_runner.py:543-545 runs watch/cage_bin/hunger_ledger.py first and falls back "
        f"to scripts/hunger_ledger.py on rc 2, but the two copies DIFFER on bytes (sha256 "
        f"e0c0ce77 vs c4a00b72 at triage time) and nothing pins which behavior is canonical, so "
        f"a cage copy that drifts or disappears silently changes which ledger write path runs; "
        f"add a drift pin (fixture comparing the two on a fixture WATCH dir, or a receipt "
        f"declaring scripts/ fallback-only and the divergence intentional); falsifier: mutate "
        f"one copy's LEDGER write shape and no test goes red; pointers mag/lane_runner.py "
        f"cycle_economist, scripts/hunger_ledger.py:40/:120/:147, "
        f"watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md.\n"
    )


LANDING = (
    " Landed 2026-09-26 (row arrived pre-checked [x] from birth with no receipt, the "
    "B2-238 disease shape; this landing earns the check): sealed scan holds exactly 43 "
    "ssrf/path occurrences in 21 files under scripts/ (29 path-traversal + 14 ssrf), "
    "brief counts confirmed per file (wave_driver 7, fetch_training_pdfs 4, m12_pairing 4, "
    "desk_baseline_probe 4), all 43 flagged lines read in bytes; classification by real "
    "drivers: schtasks full census 332 tasks and configs/lanes.yaml hold ZERO stem hits "
    "for all 21 files, so liveness comes from mag code and config gates, not the scheduler; "
    "LIVE must-fix 17 occurrences / 4 files (desk_baseline_probe via coding_session_loop "
    "yaml gate + mag import + governor_autorun, hunger_ledger via lane_runner canonical "
    "fallback, wave_driver test-driven tick organ with the staged 2026-09-12 cron absent "
    "today, m12_pairing via the driver's guarded import); ACCEPTED 26 occurrences / 17 "
    "files as 20 claims in configs/violation_baseline.json register 900 to 920 via "
    "watch/inbox/burn_wave_20260926/B2_96_baseline_update.py (B2-11 fingerprint scheme, "
    "per-file acceptance evidence in notes, script asserts 43/26/20 so the live set cannot "
    "leak in; ack_reaper and k17_pilot accepted naming their test-only execution), configs "
    "re-sealed by name, CONFIG-SEAL verify PASS 49/49; INDEX items registered, em-dash 0; "
    "receipt watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md; self-fed "
    "B2-{n1}, B2-{n2}, B2-{n3} UNCHECKED."
)


def land_once(raw: str) -> str | None:
    for old, new in [
        (f"- CLAIM B2-96 configs/violation_baseline.json {CLAIM_TS}",
         f"- CLAIMED B2-96 configs/violation_baseline.json {CLAIM_TS}"),
        (f"- CLAIM B2-96 watch/inbox/burn_wave_20260926/QUEUE.md {CLAIM_TS}",
         f"- CLAIMED B2-96 watch/inbox/burn_wave_20260926/QUEUE.md {CLAIM_TS}"),
    ]:
        if old in raw:
            raw = raw.replace(old, new, 1)
    if ROW_TAIL + "\n" in raw and "B2-96 scripts/ mimosa ssrf/path triage" in raw:
        highest = 0
        for m in re.finditer(r"B2-(\d+)", raw):
            highest = max(highest, int(m.group(1)))
        n1, n2, n3 = highest + 1, highest + 2, highest + 3
        row_new = ROW_TAIL + LANDING.format(n1=n1, n2=n2, n3=n3) + "\n"
        raw = raw.replace(ROW_TAIL + "\n", row_new, 1)
        raw = raw.rstrip("\n") + "\n" + self_feeds(n1, n2, n3)
        return raw
    return None


def main() -> int:
    for attempt in range(12):
        raw = BOARD.read_text(encoding="utf-8")
        if "- CLAIM B2-96 configs/violation_baseline.json" not in raw:
            print("claims already retired; nothing to do")
            return 0
        landed = land_once(raw)
        if landed is None:
            print("anchors missing; aborting without write")
            return 1
        time.sleep(0.4)
        if BOARD.read_text(encoding="utf-8") == raw:
            BOARD.write_text(landed, encoding="utf-8")
            print(f"B2-96 board landing ok on attempt {attempt + 1}")
            return 0
    print("board stayed hot for 12 attempts; rerun me")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
