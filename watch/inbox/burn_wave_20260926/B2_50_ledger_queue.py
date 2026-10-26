"""B2-50 close: append LEDGER.jsonl row (json.dumps, never heredoc) and
self-feed 2 briefs to QUEUE.md under '## Open'. Then re-verify the queue tail
to prove the lines landed intact (concurrent-lane collision check)."""
import json
from datetime import datetime, timezone

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-50-missing-triage",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_50_missing_triage_20260926.md",
    "one_line": (
        "missing-triage sweep closed: INDEX vs index_events fold-exact diff found 3 files with "
        "broken triage; FRONTDOOR_MISSING_JOINS_20260901.md and RESOLUTION_J1_CAGE_TO_MAG_ROUTE_20260901.md "
        "sat UNPROVEN since 9/01 (seq 25/26, classify-before-use never done) and were refiled STEAL and "
        "RECEIPT with shas unchanged since 9/01; LAW13_EXPERIMENT_ON_ABSENCE_20260926.md was registered 12:55Z "
        "under an absolute C:/Users path that OUTSIDE_RE never strips so it never folded into INDEX, "
        "invalidated and re-registered bare as DOCTRINE (matches LAW-13 in memory/law/registry.json); "
        "fold now 972 active, 0 UNPROVEN, 0 missing; adjacent findings (5 phantom absolute-path items, "
        "5 unregistered on-disk files) self-fed as B2-142/143"
    ),
}

briefs = [
    "- [ ] B2-142 Absolute-path phantom items: INDEX.json still holds 5 items registered under full "
    "C:/Users paths that never match bare inbox paths (RIDE_FAMILY_VERDICTS_20260922.md, "
    "DIRECTIVE_WATCHERS_20260926.md, RECAP_7D_20260926.md, ESSENTIALS_RESTORE.md, "
    "burn_wave_20260926/QUEUE.md); per B2_50_missing_triage_20260926.md pattern, invalidate each "
    "absolute row and re-register the bare path from watch/inbox cwd, then rebuild+verify.",
    "- [ ] B2-143 Unregistered inbox files: 5 on-disk files have no active registration (EVENTS.jsonl "
    "35KB free-resource-scout alert stream, ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc, "
    "BURN_doctrine-owed-chase_20260926_b.md, BURN_free-resource-landscape_20260926_e.md, "
    "BURN_judge-lane-spec_20260926_e.md); read each, register with class+purpose or file owed; "
    "INDEX.md and SHARED_SURFACE_CONTRACT.json stay retired per patrol law 20260922 (events 1381/1379).",
]


def main():
    with open(ROOT + r"\memory\burns\LEDGER.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    qpath = ROOT + r"\watch\inbox\burn_wave_20260926\QUEUE.md"
    with open(qpath, encoding="utf-8") as f:
        q = f.read()
    marker = "## Open\n"
    i = q.index(marker) + len(marker)
    q2 = q[:i] + "\n".join(briefs) + "\n" + q[i:]
    with open(qpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(q2)

    with open(qpath, encoding="utf-8") as f:
        check = f.read()
    for b in briefs:
        head = b.split(" ", 2)[1]
        assert b in check, f"MISSING after write: {head}"
    print("ledger row appended; queue briefs landed:")
    for b in briefs:
        print(" ", b.split(" ", 2)[1])


if __name__ == "__main__":
    main()
