# B2-469 close (2026-09-26): retire board claims, earn the pre-checked row,
# self-feed 3 briefs UNCHECKED (band re-read on fresh bytes, renumber past any
# foreign band), append the LEDGER row via json.dumps, and register the two new
# artifacts in watch/inbox/index_events.jsonl. Appends and anchored replaces
# only, never a whole-file rewrite from a snapshot.
import hashlib
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
QUEUE = HERE / "QUEUE.md"
LEDGER = REPO / "memory" / "burns" / "LEDGER.jsonl"
EVENTS = REPO / "watch" / "inbox" / "index_events.jsonl"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_469_dated_meters_20260926.md"
METERS_LEDGER = "watch/inbox/DATED_METERS.jsonl"
CLAIM_TS = "2026-09-26T19:20:17Z"


def guard(text: str) -> str:
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in appended text")
    return text


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def close_board() -> list[int]:
    q = QUEUE.read_text(encoding="utf-8", errors="replace")

    # 1. retire both claim lines (CLAIM -> CLAIMED + receipt pointer)
    for prefix in (
        "- CLAIM B2-469 scripts/census_patrol_daily.ps1 " + CLAIM_TS,
        "- CLAIM B2-469 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS,
    ):
        hit = [ln for ln in q.splitlines() if ln.startswith(prefix)]
        if len(hit) != 1:
            raise SystemExit(f"own CLAIM line not found or doubled on fresh bytes: {prefix[:60]}")
        retired = hit[0].replace("- CLAIM ", "- CLAIMED ", 1) + " -> " + RECEIPT
        q = q.replace(hit[0], guard(retired), 1)

    # 2. earn the pre-checked B2-469 row (append the landing note on the row line)
    row_prefix = "- [x] B2-469 Wire dated meters"
    hit = [ln for ln in q.splitlines() if ln.startswith(row_prefix)]
    if len(hit) != 1:
        raise SystemExit(f"expected exactly one B2-469 row, found {len(hit)}")
    landing = guard(
        " Landed 2026-09-26 (row sat pre-checked [x] with no receipt, the B2-238 "
        "disease; this landing earns the check): new organ tools/meter_patrol.py "
        "(314 lines, under the 400-line bar) appends one dated row per "
        "institutional-cluster meter class (rubric items 1-4, boundaries frozen "
        "from the pre-registered cards, both card hashes byte-identical to the "
        "B2-166 pins) to watch/inbox/DATED_METERS.jsonl, state RECEIPT with "
        "candidate pointers or explicit NOBS, schema dated_meter_v1, boundary-true "
        "matching (case-sensitive EBS/MOEX, word-bounded phrases, website/ebs "
        "substring disease regression-tested), idempotent per day, gap days named "
        "and never backfilled (no fabrication), corrupt ledger fails closed exit 2; "
        "rides the existing MagCensusPatrolDaily cron body as a second step "
        "(scripts/census_patrol_daily.ps1, own alert path to memory/attention.md, "
        "worst-code-wins exit, PS parse clean); first live run 19:30:22Z landed 4 "
        "rows dated 2026-09-26 (sha256 80a6195f44c82378b43753cb2e8ac37ae13ec5e5b91"
        "3a56e3b59853845d70dc9, all RECEIPT candidates 14/7/2/8, candidates "
        "explicitly never HIT verdicts); census tripwire untouched (sha FFE096BE "
        "pinned as zero-touch proof, the organ is a sibling module not an edit); "
        "54 passed targeted (6 new tests + 48 census patrol), ratchet NEW=0, "
        "em-dash 0; falsifier operationalized: a post-2026-09-26 scoring citing "
        "\"no receipt\" for items 1-4 without naming the DATED_METERS state for "
        "the window dates voids itself; wire-pull arm filed forward as B2-495"
        f"; receipt {RECEIPT}; self-fed B2-495 B2-496 B2-497 UNCHECKED."
    )
    q = q.replace(hit[0], hit[0] + landing, 1)

    # 3. self-feed 3 briefs UNCHECKED at the board tail; re-read the band on
    # fresh bytes and renumber past any foreign band per the B2-167 law.
    briefs = [
        guard(
            "Wire-pull arm for the meter organ: tools/meter_patrol.py witnesses "
            "only the archive (its NOBS rows say so on their face), so a NOBS "
            "streak still ends with a human pulling wires by hand; add a curl-based "
            "daily pull per meter class (candidate public feeds: NWS/IPAWS active "
            "alerts for national_alert_nonweather, MOEX news page for moex_xrp_halt, "
            "a G20 news sweep for blackout and circuit breaker), land dated "
            "snapshots under watch/inbox/wires/<date>/, and have meter_patrol cite "
            "external snapshot bytes in RECEIPT rows so a candidate pointer can be "
            "an outside wire rather than board chatter; curl -I first per AGENTS.md "
            "(SSO 302 possible), synthetic or public URLs only, never private "
            "material; falsifier: a RECEIPT row whose pointer set contains only "
            "burn_wave/board files on a day an external feed was reachable and "
            "unfetched; pointers tools/meter_patrol.py METERS + "
            "watch/inbox/DATED_METERS.jsonl + watch/inbox/burn_wave_20260926/"
            "B2_469_dated_meters_20260926.md Falsifier 1."
        ),
        guard(
            "Scoring-reader pin for the meter ledger: the OCT 3 check (B2-468) and "
            "any future window scoring do not read watch/inbox/DATED_METERS.jsonl "
            "today, so the B2-469 falsifier (a scoring citing bare \"no receipt\" "
            "for items 1-4 while NOBS rows or GAP alerts cover the window voids "
            "itself) is enforced only by discipline; add a pre-scoring step that "
            "loads the meter rows for the window dates and blocks a MISS verdict "
            "for any class whose dates hold NOBS rows or uncovered gap alerts, "
            "filing the meter-state table into the scoring receipt; falsifier: a "
            "post-pin scoring receipt containing \"no receipt\" for a class whose "
            "window dates have rows on file; pointers watch/inbox/DATED_METERS.jsonl "
            "+ watch/inbox/WINDOW_2122_SCORING_RUBRIC_20260920.md + queue B2-468 row."
        ),
        guard(
            "Prophecy-cluster meter class: dated_meter_v1 covers only the "
            "institutional cluster (rubric items 1-4); item 5 (dated "
            "register-principal pre-claims) and the Pool-channel silence telemetry "
            "that made B2-166 PROVISIONAL have no daily row, so channel-silence "
            "windows stay judgeable-by-archive-silence; extend meter_patrol with a "
            "prophecy class keyed to mrpool_export delta files (B2-467's re-pull "
            "cadence emits dated delta jsonl), emitting RECEIPT rows when a fresh "
            "harvest landed and NOBS rows when the snapshot is stale, so item 5 "
            "scoring reads a dated witness row too; falsifier: a future item-5 "
            "scoring that finds neither a meter row nor a fresh harvest date; "
            "pointers watch/inbox/WATER_WATCHLIST_20260921.json prophecy_cluster + "
            "tools/meter_patrol.py + watch/inbox/burn_wave_20260926/"
            "B2_166_rubric_scoring_20260926.md Verdict (the Pool arm hole)."
        ),
    ]
    fresh = QUEUE.read_text(encoding="utf-8", errors="replace")
    nums = [int(m) for m in re.findall(r"B2-(\d+)", fresh)]
    top = max(nums)
    tail = ""
    for i, brief in enumerate(briefs):
        tail += "\n- [ ] B2-%d %s" % (top + 1 + i, brief)
    if not fresh.endswith("\n"):
        tail = "\n" + tail
    with QUEUE.open("a", encoding="utf-8", newline="") as f:
        f.write(tail + "\n")
    print(f"board closed: claims retired, B2-469 row earned, self-fed "
          f"B2-{top + 1}..B2-{top + 3} UNCHECKED (fresh-bytes top was B2-{top})")

    # 4. LEDGER row (json.dumps, never heredoc)
    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "slug": "B2-469-dated-meters",
        "verdict": "LANDED",
        "lane": "B2-469",
        "landing": RECEIPT,
        "one_line": guard(
            "B2-469 dated meters landed: new $0 organ tools/meter_patrol.py (314 "
            "lines, schema dated_meter_v1, under the 400-line bar) appends one "
            "dated row per institutional-cluster meter class to watch/inbox/"
            "DATED_METERS.jsonl daily, RECEIPT candidate pointers or explicit NOBS "
            "(LAW-13 name-the-absence), boundaries frozen byte-identical to the "
            "pre-registered cards B2-166 scored against (rubric A76590AC.., "
            "watchlist 156CEF8F..), boundary-true matching bars the website/ebs "
            "substring disease structurally, idempotent per (date, class), gap "
            "days named never backfilled, corrupt ledger exit 2 fail-closed; cron "
            "body scripts/census_patrol_daily.ps1 gained the meter step after the "
            "census deep check with its own GAP/cannot-verify alert path to "
            "memory/attention.md and worst-code-wins exit, PS parse clean; first "
            "live run 19:30:22Z exit 0 landed 4 rows dated 2026-09-26 sha "
            "80a6195f.. (RECEIPT 14/7/2/8, candidates never HIT verdicts); census "
            "tripwire zero-touch (FFE096BE.. pinned, sibling module instead of an "
            "edit, the B2-244/B2-245 co-edit disease avoided); 54 passed targeted "
            "(6 new meter tests + 48 census patrol), self-test 7 check groups, "
            "ratchet NEW=0, em-dash 0, claim law honored (claims 19:20:17Z "
            "appended before claimed-byte reads, retired at close, band "
            "B2-495..497 claimed on fresh-bytes census B2-494); falsifier "
            "operationalized: post-2026-09-26 scoring citing bare \"no receipt\" "
            "for items 1-4 without the DATED_METERS state voids itself; wire-pull "
            "arm owed filed as B2-495; self-fed B2-495 B2-496 B2-497 UNCHECKED"
        ),
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("LEDGER row appended")

    # 5. index_events.jsonl registrations (append-only)
    now = time.gmtime()
    seq = int(time.time() * 1e6)
    entries = [
        (METERS_LEDGER, "artifact", "B2-469 landing: dated witness meters for the "
         "institutional cluster, one row per meter class per day, RECEIPT "
         "candidates or explicit NOBS, schema dated_meter_v1; first 4 rows dated "
         "2026-09-26; living ledger, grows daily by cron design", True),
        (RECEIPT, "receipt", "B2-469 receipt: meter organ + cron step + tests + "
         "first live run, falsifier operationalized against bare archive-silence "
         "scoring", False),
    ]
    with EVENTS.open("a", encoding="utf-8") as f:
        for rel, cls, purpose, living in entries:
            path = REPO / rel
            payload = {
                "seq": str(seq),
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", now),
                "op": "register",
                "file": rel,
                "sha256": sha256(path),
                "class": cls,
                "purpose": purpose,
                "writer": "zcode-b2-469-dated-meters",
            }
            if living:
                payload["living"] = True
                payload["seal"] = "open"
            f.write(guard(json.dumps(payload, ensure_ascii=False)) + "\n")
            seq += 1
    print("index_events rows appended (meters ledger living, receipt static)")
    return [top + 1, top + 2, top + 3]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    close_board()
