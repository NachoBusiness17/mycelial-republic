"""dispatch_landing_join - the PROVEN-vs-landing cross-join (Q33 frontier, 2026-10-01).

Q33 (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md): seat_dispatch rows
carry done/failed + detail, but nothing greps whether a "done" dispatch has a
LANDED RECEIPT that names it. This tool is that join - a fabrication smell
detector: done with no receipt on the shared inbox is CLAIMED-DONE-NO-RECEIPT
and the tool exits 1 (fail-loud).

Inputs (read-only):
  * ledger - mag/seat_dispatch.py stores nothing itself; it registers/finalizes
    through mag.orchestrator, one JSON per task under
    memory/runs/orchestrator/tasks/. A dispatch row = record whose `seat` is a
    seat_dispatch seat (mirrored below from HEADLESS + MAILBOX; keep in sync -
    not imported so the tool stays standalone). Shape: task_id, tag, status,
    source, seat, goal, detail, created_at, ended_at, exit_code.
  * receipts - watch/inbox tree: contents of every text file, plus INDEX.json
    items and index_events.jsonl rows (path/purpose scanned as evidence; a hit
    cites the file they name, or the index row when the artifact is absent).

MATCH RULE (explicit; false OPEN beats false PROVEN):
  Tier 1 exact id: the task_id (e.g. "ext-017eb4afbe") appears verbatim
  (case-insensitive) in receipt evidence. BULK-DUMP GUARD: one artifact naming
  >= --bulk-limit (default 8) DISTINCT ids is a ledger enumeration (live:
  burn_reset_20260927/flash50/_f26_raw.json names all 317), not provenance -
  excluded and reported. queue/handoff/<seat>/OUTBOX/<id>.md is NOT evidence:
  seat_dispatch writes it itself, so it would prove the dispatcher by itself.
  Tier 2 name tokens: distinctive tokens (>= 5 chars, letter-first,
  stopword-stripped, case-folded, and RARE in the goal corpus: in < 30% of
  goals) of the receipt FILE NAME, >= 3 shared with the goal AND >= 60% of
  name tokens contained - strict, receipt names are short so this rarely
  fires. Every PROVEN row cites path + tier.

Classes: PROVEN-LANDED (done + receipt), CLAIMED-DONE-NO-RECEIPT (done alone,
exit 1), FAILED (terminal non-done; a receipt is noted, never upgrades),
OPEN (running/queued). Exit codes: 0 clean, 1 fabrication rows, 2 usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_LEDGER = ROOT / "memory" / "runs" / "orchestrator" / "tasks"
DEFAULT_RECEIPTS = ROOT / "watch" / "inbox"

# Mirror of mag/seat_dispatch.py HEADLESS + MAILBOX (read-only source of truth).
SEAT_DISPATCH_SEATS = frozenset(
    ("openclaw", "openclaw-heavy", "openclaw-worker", "claude-zai",
     "opencode", "zcode-cli", "zcode", "autoclaw"))

# Mirror of mag.orchestrator.TERMINAL.
TERMINAL = frozenset({"done", "failed", "timeout", "stalled", "killed", "died"})

# Text artifacts scanned for Tier 1 ids (receipt tree is prose + json + code).
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".txt", ".csv", ".log", ".yaml",
                 ".yml", ".html", ".js", ".mjs", ".py", ".ps1", ".sh", ".ini",
                 ".cfg"}
MAX_SCAN_BYTES = 4_000_000  # per file; bigger artifacts are skipped, not guessed

# Tier 2 boilerplate: prompt-scaffolding words in almost every goal that prove
# nothing about WHICH goal a receipt belongs to.
STOPWORDS = frozenset(
    "about after again answer before below between both check clause code could "
    "every example file files first found from give have here into just lines "
    "list little might must notes only other output over plain please point "
    "read report reporting repo same shall share should single small source "
    "start still such take text that their there these thing think this those "
    "through under until want what where which while words would write your "
    "yours yourself understand following message session".split())

TOKEN_RE = re.compile(r"[a-z][a-z0-9]{4,}")


def tokens(text: str) -> set[str]:
    """Distinctive name tokens: >= 5 chars, letter-first, stopword-stripped."""
    return {t for t in TOKEN_RE.findall((text or "").lower()) if t not in STOPWORDS}


def load_dispatch_rows(ledger_dir: Path, seats: frozenset[str]) -> tuple[list[dict], int]:
    """All seat-dispatch rows from the ledger dir. Returns (rows, malformed)."""
    rows: list[dict] = []
    malformed = 0
    for p in sorted(ledger_dir.glob("*.json")):
        try:
            row = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            row = None
        if not isinstance(row, dict):
            malformed += 1
            continue
        if row.get("seat") not in seats:
            continue
        if not str(row.get("task_id") or "").strip():
            malformed += 1
            continue
        rows.append(row)
    return rows, malformed


def resolve_inbox_path(raw: str, inbox_root: Path) -> str:
    """Normalize an INDEX/events `file` field to a path relative to the inbox root.

    Seen in the wild: "/board/inbox/X.md" (docker mount), "sub/X.json"
    (relative), "C:/Users/.../watch/inbox/X.md" (absolute host path).
    """
    s = (raw or "").replace("\\", "/").strip()
    for prefix in ("/board/inbox/", "board/inbox/"):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    if "watch/inbox/" in s:
        s = s.split("watch/inbox/", 1)[1]
    if ":" in s.split("/", 1)[0]:  # drive-letter absolute
        s = s.split(":", 1)[1].lstrip("/")
    return s


def _ids_in(text_lower: str, ids: list[str]) -> list[str]:
    return [tid for tid in ids if tid.lower() in text_lower]


def build_evidence(receipts_root: Path, ids: list[str], *,
                   bulk_limit: int) -> tuple[dict[str, list[str]], list[dict]]:
    """Scan the receipt tree + indexes. Returns (evidence, excluded_dumps).

    evidence maps task_id -> [receipt citation, ...] where a citation is a
    path relative to receipts_root (or "INDEX.json -> <item path>" /
    "index_events.jsonl -> <file>" when the named artifact is absent).
    excluded_dumps lists artifacts that name >= bulk_limit distinct ids.
    """
    evidence: dict[str, list[str]] = {}
    dumps: list[dict] = []

    def add_hits(hit_ids: list[str], citation: str) -> None:
        for tid in hit_ids:
            evidence.setdefault(tid, [])
            if citation not in evidence[tid]:
                evidence[tid].append(citation)

    def add_text(raw_text: str, citation: str) -> None:
        hit = _ids_in(raw_text.lower(), ids)
        if len(hit) >= bulk_limit:
            dumps.append({"citation": citation, "distinct_ids": len(hit)})
            return
        add_hits(hit, citation)

    # 1. receipt tree file contents
    for p in sorted(receipts_root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if p.name in ("INDEX.json", "index_events.jsonl"):
            continue  # handled below as index evidence
        try:
            if p.stat().st_size > MAX_SCAN_BYTES:
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        add_text(text, p.relative_to(receipts_root).as_posix())

    # 2. INDEX.json items + 3. index_events.jsonl rows (path + purpose text)
    def _index_rows() -> list[tuple[str, str]]:
        rows_out: list[tuple[str, str]] = []
        index_path = receipts_root / "INDEX.json"
        if index_path.is_file():
            try:
                items = json.loads(index_path.read_text(encoding="utf-8")).get("items") or []
            except (OSError, ValueError, AttributeError):
                items = []
            for item in items:
                if isinstance(item, dict):
                    rows_out.append((str(item.get("path") or ""),
                                     str(item.get("purpose") or "")))
        events_path = receipts_root / "index_events.jsonl"
        if events_path.is_file():
            try:
                lines = events_path.read_text(encoding="utf-8",
                                              errors="replace").splitlines()
            except OSError:
                lines = []
            for line in lines:
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if isinstance(ev, dict):
                    rows_out.append((str(ev.get("file") or ""),
                                     str(ev.get("purpose") or "")))
        return rows_out

    for raw_path, purpose in _index_rows():
        hit = _ids_in(f"{raw_path} {purpose}".lower(), ids)
        if not hit:
            continue
        named = resolve_inbox_path(raw_path, receipts_root)
        if named and (receipts_root / named).is_file():
            citation = named
        elif raw_path:
            citation = f"index-row -> {raw_path}"
        else:
            citation = "index-row (no path)"
        if len(hit) >= bulk_limit:
            dumps.append({"citation": citation, "distinct_ids": len(hit)})
            continue
        add_hits(hit, citation)

    return evidence, dumps


def _distinctive_tokens(rows: list[dict]) -> frozenset[str]:
    """Tokens rare in the goal corpus. A token in >= 30% of goals (and >= 3)
    is prompt boilerplate - live example: the archaeologist goals all say
    "patterns the fleet could steal" about hermes-agent files, so hermes/
    agent/steal name-match a HERMES_AGENT_STEAL receipt against 12 unrelated
    dispatches. Boilerplate tokens cannot prove identity."""
    df: dict[str, int] = {}
    n = 0
    for row in rows:
        n += 1
        for t in tokens(str(row.get("goal") or "")):
            df[t] = df.get(t, 0) + 1
    cut = max(3, (n * 3 + 9) // 10)  # ceil(0.3 * n), floor 3
    return frozenset(t for t, c in df.items() if c < cut)


def tier2_match(goal: str, receipt_rel: str, distinctive: frozenset[str]) -> bool:
    """Strict name-token containment: >= 3 shared corpus-rare distinctive
    tokens AND >= 60% of the receipt-name tokens present in the goal.
    False on any doubt - false OPEN beats false PROVEN."""
    name_toks = tokens(Path(receipt_rel).stem)
    if len(name_toks) < 3:
        return False
    shared = name_toks & tokens(goal) & distinctive
    return len(shared) >= 3 and len(shared) / len(name_toks) >= 0.6


def classify(rows: list[dict], evidence: dict[str, list[str]],
             receipt_names: list[str]) -> list[dict]:
    """Join each dispatch row to receipt evidence -> classed result rows."""
    distinctive = _distinctive_tokens(rows)
    out: list[dict] = []
    for row in rows:
        tid = str(row.get("task_id") or "")
        status = str(row.get("status") or "")
        rec: dict = {
            "task_id": tid, "seat": row.get("seat"), "tag": row.get("tag"),
            "status": status, "created_at": row.get("created_at"),
            "goal": str(row.get("goal") or "")[:120],
        }
        cites = list(evidence.get(tid, []))
        if status == "done":
            if cites:
                rec["class"] = "PROVEN-LANDED"
                rec["tier"] = "tier1-exact-id"
                rec["receipts"] = cites
            else:
                t2 = [n for n in receipt_names
                      if tier2_match(str(row.get("goal") or ""), n, distinctive)]
                if t2:
                    rec["class"] = "PROVEN-LANDED"
                    rec["tier"] = "tier2-name-tokens"
                    rec["receipts"] = sorted(t2)[:3]
                else:
                    rec["class"] = "CLAIMED-DONE-NO-RECEIPT"
        elif status in TERMINAL:
            rec["class"] = "FAILED"
            if cites:
                rec["receipts"] = cites  # noted, does not change the class
        else:
            rec["class"] = "OPEN"
        out.append(rec)
    return out


def build_report(results: list[dict], *, ledger_dir: Path, receipts_root: Path,
                 bulk_limit: int, malformed: int, dumps: list[dict],
                 as_json: bool, verbose: bool) -> dict:
    counts: dict[str, int] = {c: 0 for c in
                              ("PROVEN-LANDED", "CLAIMED-DONE-NO-RECEIPT",
                               "FAILED", "OPEN")}
    for rec in results:
        counts[rec["class"]] += 1
    fabrication = [r for r in results if r["class"] == "CLAIMED-DONE-NO-RECEIPT"]
    proven = [r for r in results if r["class"] == "PROVEN-LANDED"]
    report = {
        "tool": "dispatch_landing_join",
        "ledger": str(ledger_dir),
        "receipts": str(receipts_root),
        "dispatch_rows": len(results),
        "malformed_rows": malformed,
        "match_rule": (
            "tier1 exact task_id in receipt evidence text (bulk-dump guard: "
            f">= {bulk_limit} distinct ids in one artifact = excluded dump); "
            "tier2 receipt-name distinctive tokens (corpus-rare: in < 30% of "
            "goals) >= 3 shared AND >= 60% contained in the goal; "
            "PROVEN cites path+tier"
        ),
        "counts": counts,
        "bulk_dumps_excluded": dumps,
        "claimed_done_no_receipt": fabrication,
        "proven_landed": proven,
        "exit": 1 if fabrication else 0,
    }
    if as_json:
        return report

    def line(s: str = "") -> None:
        print(s)

    line("dispatch_landing_join - PROVEN-vs-landing cross-join (Q33)")
    line(f"  ledger   : {ledger_dir}")
    line(f"  receipts : {receipts_root}")
    line(f"  rows     : {len(results)} seat-dispatch rows"
         f" ({malformed} malformed skipped)")
    line(f"  match    : {report['match_rule']}")
    for d in dumps:
        line(f"  bulk dump excluded: {d['citation']} ({d['distinct_ids']} ids)")
    line("  counts   : " + "  ".join(f"{k}={v}" for k, v in counts.items()))
    note = "  (findings, not failures to hide)" if fabrication else ""
    line(f"  exit     : {report['exit']}{note}")
    if fabrication:
        line("")
        line(f"CLAIMED-DONE-NO-RECEIPT ({len(fabrication)}):")
        for r in fabrication:
            line(f"  {r['task_id']}  seat={r['seat']}  tag={r['tag']}  "
                 f"created={r['created_at']}")
            line(f"    goal: {r['goal']}")
    if proven:
        line("")
        line(f"PROVEN-LANDED ({len(proven)}):")
        for r in proven:
            line(f"  {r['task_id']}  seat={r['seat']}  tier={r['tier']}  "
                 f"receipt={r['receipts'][0]}")
    if verbose:
        for cls in ("FAILED", "OPEN"):
            rows = [r for r in results if r["class"] == cls]
            if rows:
                line("")
                line(f"{cls} ({len(rows)}):")
                for r in rows:
                    line(f"  {r['task_id']}  seat={r['seat']}  "
                         f"status={r['status']}  goal: {r['goal'][:70]}")
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="dispatch_landing_join",
        description="cross-join seat_dispatch rows against landed watch/inbox "
                    "receipts; exit 1 on done-with-no-receipt (fabrication smell)")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER),
                    help="dispatch ledger dir (default: memory/runs/orchestrator/tasks)")
    ap.add_argument("--receipts", default=str(DEFAULT_RECEIPTS),
                    help="receipt tree root (default: watch/inbox)")
    ap.add_argument("--bulk-limit", type=int, default=8,
                    help="artifact naming >= N distinct ids = bulk dump, "
                         "not provenance (default 8)")
    ap.add_argument("--seats", default="",
                    help="comma-separated seat override (default: the "
                         "mag/seat_dispatch.py seat set)")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--verbose", action="store_true",
                    help="also list FAILED and OPEN rows")
    a = ap.parse_args(argv)

    ledger_dir = Path(a.ledger)
    receipts_root = Path(a.receipts)
    if not ledger_dir.is_dir():
        print(f"usage error: ledger dir not found: {ledger_dir}", file=sys.stderr)
        return 2
    if not receipts_root.is_dir():
        print(f"usage error: receipts root not found: {receipts_root}", file=sys.stderr)
        return 2
    if a.bulk_limit < 1:
        print("usage error: --bulk-limit must be >= 1", file=sys.stderr)
        return 2
    seats = (frozenset(s.strip() for s in a.seats.split(",") if s.strip())
             if a.seats else SEAT_DISPATCH_SEATS)
    if not seats:
        print("usage error: --seats produced an empty seat set", file=sys.stderr)
        return 2

    rows, malformed = load_dispatch_rows(ledger_dir, seats)
    ids = [str(r["task_id"]) for r in rows]
    evidence, dumps = build_evidence(receipts_root, ids, bulk_limit=a.bulk_limit)
    receipt_names = [p.relative_to(receipts_root).as_posix()
                     for p in receipts_root.rglob("*")
                     if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES]
    results = classify(rows, evidence, receipt_names)
    report = build_report(
        results, ledger_dir=ledger_dir, receipts_root=receipts_root,
        bulk_limit=a.bulk_limit, malformed=malformed, dumps=dumps,
        as_json=a.json, verbose=a.verbose,
    )
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return report["exit"]


if __name__ == "__main__":
    raise SystemExit(main())
