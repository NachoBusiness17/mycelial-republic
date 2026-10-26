"""B2-145 close: append LEDGER.jsonl row (json.dumps, never heredoc) and
self-feed 2 briefs to QUEUE.md under '## Open'. Then re-verify the queue tail
to prove the lines landed intact (concurrent-lane collision check)."""
import json
from datetime import datetime, timezone

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-145-phantom-paths",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_145_phantom_paths_20260926.md",
    "one_line": (
        "absolute-path phantom sweep closed: INDEX.json carried 5 items registered under the absolute "
        "host root C:/Users/foste/... that never matches a bare inbox path (RIDE_FAMILY_VERDICTS_20260922.md, "
        "DIRECTIVE_WATCHERS_20260926.md, RECAP_7D_20260926.md, ESSENTIALS_RESTORE.md, burn_wave_20260926/QUEUE.md); "
        "mints were d05-rides-r2 (event 1376), md-record-seal autoseal (2542/2786/2788) and drift-patrol-cron "
        "minting QUEUE.md twice (2784 plus 3053 in a /board/inbox/C:/ double-prefix form); all 5 invalidated "
        "(seqs 1789823567015749380-384) and re-registered bare as RECEIPT/DIRECTIVE/BRIEF/DOCTRINE/BOARD; "
        "fold clean of C:/ paths; 4 remaining verify mismatches are pre-existing stale-sha rows owned by B2-41"
    ),
}

briefs = [
    "- [ ] B2-150 Living-file hash law: QUEUE.md and LINKS.jsonl go sha-stale on every concurrent append "
    "(QUEUE.md registered by B2-145 was stale within minutes of lane appends; LINKS.jsonl sits in today's "
    "verify failures for the same reason), so hash-verify cries wolf on the two busiest boards; decide the "
    "design: a living=true item field the verify skips with a count, exclusion by class, or a close-pass "
    "refresh; never paper it with repeated re-registers; pointers scripts/index_fold_host.mjs verify "
    "(lines 271-305) + watch/inbox/burn_wave_20260926/B2_145_phantom_paths_20260926.md.",
    "- [ ] B2-151 Sharpen B2-149 with the composed-prefix case: drift-patrol-cron minted "
    "/board/inbox/C:/Users/.../watch/inbox/burn_wave_20260926/QUEUE.md (index_events.jsonl:3053), so the "
    "normInboxFile fix must strip the board|app/inbox prefix AND the absolute host root in one pass, and "
    "tests/test_index_fold_host.py needs that composed shape plus a fold warning when a post-normalize "
    "path still fails the inbox-relative check; pointer watch/inbox/burn_wave_20260926/B2_145_phantom_paths_20260926.md "
    "evidence section.",
]


def main():
    with open(ROOT + r"\memory\burns\LEDGER.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    qpath = ROOT + r"\watch\inbox\burn_wave_20260926\QUEUE.md"
    with open(qpath, encoding="utf-8") as f:
        q = f.read()
    marker = "## Open\n"
    i = q.rindex(marker) + len(marker)
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
