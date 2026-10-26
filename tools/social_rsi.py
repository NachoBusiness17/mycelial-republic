#!/usr/bin/env python3
"""social_rsi.py - Recursive Social Improvement loop, v0 (2026-10-04).

The operator recipe (watch/inbox/X_INTEL_PAPERS_20261004.md section 6, his
words: "I do this manually, but it would actually be awesome to do it
autonomously"): (1) aggregate sessions, (2) search failure patterns,
(3) collect examples + solutions and synthesize a skill, (4) use it.
This tool is the deterministic front half of that loop:

  step 1+2  PATTERN ROLL-UP - scan queue/lanes/*/trail.jsonl CYCLE_FAIL
            rows, group by normalized failure detail (the same keying
            mag/lane_runner.py normalize_detail uses for CLUSTER_REPORT;
            a simple tokenizer + first-120-chars bucket stands in if that
            import is unreachable), joined against logs/failure_kb.jsonl
            known sigs.
  step 2b   EVIDENCE PAIRS - per top pattern, a CYCLE_FAIL followed later
            in the same lane by a green CYCLE or a trail FIX row (event
            containing "FIX") = before/after solution evidence; plus
            matching receipts grepped from watch/inbox (cap 3 per pattern).
  step 3    SYNTHESIS PACKET - per top-N pattern, a packet under
            watch/inbox/social_rsi/ carrying the pattern, the evidence,
            the receipts, and a SYNTHESIS ASK block for a seat to draft a
            skill card in the estate's winning shape (the five card rules
            measured in watch/inbox/IMAGE_BLASTER_GO_20261003.md, template
            .agents/skills/image-blast/SKILL.md).

WIRED-ORGAN LAW (B2 verkle_vs_embedding verdict, no new store): this tool
is a QUERY + PACKET surface over ledgers that already exist (lane trails,
logs/failure_kb.jsonl, watch/inbox receipts). It creates no database, no
index file, no cache; its only writes are the packets themselves.

PROMOTE-GATE LAW (skill census; ractor50 verdict "waves are the fuzzer,
cards are the commits"): drafting the card is a separate seated step and
the commit stays human - mag.cmd promote --apply. The packet footer says
so; this tool never promotes anything.

TEXT LAW: plain hyphens only, zero em/en dashes in every byte it writes
or prints (quoted trail details are scrubbed on the way out).

Exit codes: 0 ok (including zero patterns found); 2 usage error or the
queue/lanes root is missing entirely.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent

TRAIL_GLOB = ("queue", "lanes", "*", "trail.jsonl")
FKB_PATH = ("logs", "failure_kb.jsonl")
PACKET_DIR = ("watch", "inbox", "social_rsi")
RECEIPT_DIR = "watch/inbox"

# Receipt-scan bounds: watch/inbox is 6.3G of markdown on the live tree;
# the scan reads top-level *.md first (sorted), then subdirectories
# (sorted), until these caps. Deterministic on every rerun of same tree.
RECEIPT_FILE_CAP_BYTES = 1_000_000        # skip any single file larger
RECEIPT_TOTAL_CAP_BYTES = 48_000_000      # stop the scan past this many
RECEIPTS_PER_PATTERN = 3
PAIRS_PER_PATTERN = 3
FKB_SIGS_SHOWN = 3

_EMDASH_CHARS = ("\u2014", "\u2013", "\u2012", "\u2015")


def no_emdash(text: str) -> str:
    """Text law: every dash this tool emits is a plain hyphen. Trail
    details carry em-dashes on the live tree (e.g. TESUJI_DROP rows);
    quoted text is scrubbed through here on the way out."""
    out = str(text)
    for ch in _EMDASH_CHARS:
        out = out.replace(ch, " - ")
    return out


# ---------------------------------------------------------------- ts

def parse_ts(raw) -> datetime | None:
    """Trail rows carry 2026-09-04T15:34:55Z; failure_kb rows carry
    2026-08-05T15:13:08.357243+00:00. Both arms of fromisoformat after
    the Z fold; naive stamps are pinned to UTC."""
    if raw is None:
        return None
    try:
        dt = datetime.fromisoformat(str(raw).strip().replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


# ------------------------------------------------- normalization key

def _load_normalize_detail():
    """Reuse the CLUSTER_REPORT keying from mag/lane_runner.py when the
    import is reachable (same bucketing as the per-lane reports, so the
    cross-lane roll-up speaks the same class language). Fallback arm per
    build spec: a simple tokenizer + first-120-chars bucket."""
    try:
        root = str(HERE.parent)
        if root not in sys.path:
            sys.path.insert(0, root)
        from mag.lane_runner import normalize_detail  # type: ignore
        return normalize_detail, "mag.lane_runner.normalize_detail"
    except Exception:
        def simple_tokenizer(detail: str) -> str:
            s = str(detail or "").lower()[:120]
            s = re.sub(r"[^a-z0-9]+", " ", s).strip()
            return " ".join(s.split()[:6]) or "unclassified"
        return simple_tokenizer, "simple-tokenizer-fallback"


# ------------------------------------------------------- data loading

@dataclass
class TrailRow:
    lane: str
    ts: datetime
    event: str
    detail: str
    raw_ts: str


def load_trails(root: Path) -> tuple[dict[str, list[TrailRow]], dict]:
    """Read every queue/lanes/*/trail.jsonl. Returns per-lane row lists
    (all events, ts-sorted stable by file order) + a scan summary that
    names malformed lines by count, never silently dropping them."""
    lanes: dict[str, list[TrailRow]] = {}
    summary = {"trails": 0, "rows": 0, "malformed": 0, "no_ts": 0}
    pattern = root.joinpath(*TRAIL_GLOB[:2])
    if not pattern.is_dir():
        return lanes, summary
    for trail in sorted(root.glob("/".join(TRAIL_GLOB))):
        lane = trail.parent.name
        rows: list[TrailRow] = []
        with trail.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    summary["malformed"] += 1
                    continue
                if not isinstance(row, dict):
                    summary["malformed"] += 1
                    continue
                ts = parse_ts(row.get("ts"))
                if ts is None:
                    summary["no_ts"] += 1
                    continue
                rows.append(TrailRow(
                    lane=lane, ts=ts, event=str(row.get("event") or ""),
                    detail=str(row.get("detail") or ""), raw_ts=str(row.get("ts") or "")))
        summary["trails"] += 1
        summary["rows"] += len(rows)
        lanes[lane] = rows
    return lanes, summary


def load_fkb_window(root: Path, cutoff: datetime) -> list[dict]:
    """Windowed rows of logs/failure_kb.jsonl (authoritative event log
    per mag/failure_kb.py). Malformed lines are skipped and named by the
    caller-visible count in the roll-up summary."""
    out: list[dict] = []
    path = root.joinpath(*FKB_PATH)
    if not path.is_file():
        return out
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if not isinstance(row, dict):
                continue
            ts = parse_ts(row.get("ts"))
            if ts is None or ts < cutoff:
                continue
            row["_ts"] = ts
            out.append(row)
    return out


# --------------------------------------------------------- roll-up

@dataclass
class Pattern:
    key: str
    count: int = 0
    lanes: Counter = field(default_factory=Counter)
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    example_detail: str = ""
    fkb_count: int = 0
    fkb_sigs: list = field(default_factory=list)
    fkb_scanned: int = 0

    def lanes_display(self, cap: int = 4) -> str:
        items = [f"{lane}({n})" for lane, n in sorted(self.lanes.items(),
                                                      key=lambda kv: (-kv[1], kv[0]))]
        if len(items) > cap:
            return ", ".join(items[:cap]) + f" (+{len(items) - cap} more)"
        return ", ".join(items)


def rollup(lanes: dict[str, list[TrailRow]], cutoff: datetime,
           normalize, fkb_rows: list[dict]) -> list[Pattern]:
    """Group windowed CYCLE_FAIL rows by normalized detail; attach the
    failure_kb known-sig join (exact key match on the normalized detail
    or >= 2 shared distinctive tokens against sig+detail+error+kind)."""
    patterns: dict[str, Pattern] = {}
    all_time_fails = 0
    for lane in sorted(lanes):
        for row in lanes[lane]:
            if row.event != "CYCLE_FAIL":
                continue
            all_time_fails += 1
            if row.ts < cutoff:
                continue
            key = normalize(row.detail)
            pat = patterns.setdefault(key, Pattern(key=key))
            pat.count += 1
            pat.lanes[lane] += 1
            if pat.first_seen is None or row.ts < pat.first_seen:
                pat.first_seen = row.ts
            if pat.last_seen is None or row.ts > pat.last_seen:
                pat.last_seen = row.ts
            if not pat.example_detail:
                pat.example_detail = row.detail
    ranked = sorted(patterns.values(), key=lambda p: (-p.count, p.key))
    if ranked:
        _join_fkb(ranked, fkb_rows, normalize)
    return ranked


def _needles(key: str, cap: int = 3) -> list[str]:
    """Distinctive tokens for receipt/fkb grep: the longest tokens of
    the normalized key (len >= 4), longest first, capped."""
    tokens = sorted({t for t in key.split() if len(t) >= 4},
                    key=lambda t: (-len(t), t))
    return tokens[:cap]


def _needle_hits(needles: list[str], blob: str) -> int:
    low = blob.lower()
    return sum(1 for n in needles if n in low)


def _join_fkb(patterns: list[Pattern], fkb_rows: list[dict], normalize) -> None:
    by_key: dict[str, list[dict]] = defaultdict(list)
    for row in fkb_rows:
        by_key[normalize(row.get("detail") or "")].append(row)
    for pat in patterns:
        pat.fkb_scanned = len(fkb_rows)
        exact = by_key.get(pat.key, [])
        if exact:
            pat.fkb_count = len(exact)
            pat.fkb_sigs = sorted({str(r.get("sig")) for r in exact
                                   if r.get("sig")})[:FKB_SIGS_SHOWN]
            continue
        needles = _needles(pat.key)
        if len(needles) < 2:
            continue
        sig_hits = Counter()
        for row in fkb_rows:
            blob = " ".join(str(row.get(k) or "") for k in
                            ("sig", "detail", "error", "kind", "tool"))
            if _needle_hits(needles, blob) >= 2:
                sig = str(row.get("sig") or "unknown")
                sig_hits[sig] += 1
        if sig_hits:
            pat.fkb_count = sum(sig_hits.values())
            pat.fkb_sigs = sorted(sig_hits)[:FKB_SIGS_SHOWN]


# ---------------------------------------------------- evidence pairs

@dataclass
class EvidencePair:
    lane: str
    fail_ts: datetime
    fail_raw_ts: str
    recovery_ts: datetime
    recovery_event: str
    recovery_detail: str

    @property
    def gap_s(self) -> float:
        return (self.recovery_ts - self.fail_ts).total_seconds()


def is_fix_event(event: str) -> bool:
    """Trail FIX row: any event whose name carries FIX (the live tree's
    fix-family rows are event-prefixed, e.g. LEASE_LAW_FIX_APPLIED)."""
    return "FIX" in event.upper()


def evidence_pairs(pat: Pattern, lanes: dict[str, list[TrailRow]],
                   normalize, cap: int = PAIRS_PER_PATTERN) -> list[EvidencePair]:
    """BEFORE/AFTER evidence per lane: the lane's LAST windowed fail of
    this pattern, then the FIRST later row in that lane which is a green
    CYCLE or a FIX-family event. Lanes with no later recovery row are not
    evidence. Ranked most-recent fail first, lane asc tiebreak."""
    pairs: list[EvidencePair] = []
    for lane in sorted(pat.lanes):
        rows = lanes.get(lane, [])
        fails = [r for r in rows if r.event == "CYCLE_FAIL"
                 and normalize(r.detail) == pat.key]
        if not fails:
            continue
        last_fail = max(fails, key=lambda r: r.ts)
        for row in rows:
            if row.ts <= last_fail.ts:
                continue
            if row.event == "CYCLE" or is_fix_event(row.event):
                pairs.append(EvidencePair(
                    lane=lane, fail_ts=last_fail.ts, fail_raw_ts=last_fail.raw_ts,
                    recovery_ts=row.ts, recovery_event=row.event,
                    recovery_detail=row.detail))
                break
    pairs.sort(key=lambda p: (-p.fail_ts.timestamp(), p.lane))
    return pairs[:cap]


# -------------------------------------------------------- receipts

def find_receipts(root: Path, pat: Pattern,
                  cap: int = RECEIPTS_PER_PATTERN) -> tuple[list[tuple[Path, list[str]]], int]:
    """Grep watch/inbox markdown for the pattern's needles. Top-level
    *.md first (sorted), then subdirectories (sorted), under the byte
    caps named in the constants; a file matches at 2+ needle hits (1 if
    the key yields a single needle). Ranked by hits desc, path asc."""
    needles = _needles(pat.key)
    if not needles:
        return [], 0
    need = min(2, len(needles))
    inbox = root / RECEIPT_DIR
    if not inbox.is_dir():
        return [], 0
    files = sorted(inbox.glob("*.md"))
    subdirs = sorted(d for d in inbox.iterdir() if d.is_dir())
    for sub in subdirs:
        files.extend(sorted(sub.rglob("*.md")))
    matches: list[tuple[int, Path, list[str]]] = []
    budget = RECEIPT_TOTAL_CAP_BYTES
    for path in files:
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > RECEIPT_FILE_CAP_BYTES:
            continue
        if budget <= 0:
            break
        budget -= size
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hit = [n for n in needles if n in text.lower()]
        if len(hit) >= need:
            matches.append((len(hit), path, hit))
    matches.sort(key=lambda m: (-m[0], str(m[1])))
    # repo-relative with forward slashes: the estate's citation shape
    cited = [(p.relative_to(root).as_posix(), hit) for _, p, hit in matches[:cap]]
    return cited, len(files)


# ---------------------------------------------------------- packets

def slugify(key: str, cap: int = 40) -> str:
    parts = re.findall(r"[a-z0-9]+", key.lower())
    slug = "-".join(parts)[:cap].strip("-")
    return slug or "pattern"


def packet_path(root: Path, pat: Pattern, day: str) -> Path:
    return root.joinpath(*PACKET_DIR) / f"packet_{slugify(pat.key)}_{day}.md"


def render_packet(pat: Pattern, pairs: list[EvidencePair],
                  receipts: list[tuple[Path, list[str]]], day: str,
                  days: int, normalizer_name: str) -> str:
    """The synthesis packet: pattern (instrument-named), evidence pairs,
    matching receipts, the SYNTHESIS ASK, and the promote-gate footer."""
    L: list[str] = []
    L.append(f"# SOCIAL RSI PACKET - {no_emdash(pat.key)}")
    L.append("")
    L.append(f"Filed {day} by tools/social_rsi.py v0 (pattern rank by windowed")
    L.append(f"count; day window {days}d).")
    L.append("")
    L.append("## Pattern (instrument-named)")
    L.append("")
    L.append(f"- class (normalized detail key): `{no_emdash(pat.key)}`")
    L.append(f"- count: {pat.count} CYCLE_FAIL rows in the {days}d window")
    L.append(f"- instrument: `queue/lanes/*/trail.jsonl` CYCLE_FAIL event rows,")
    L.append(f"  keyed by {normalizer_name} (the mag/lane_runner.py")
    L.append("  CLUSTER_REPORT keying, so this cross-lane roll-up speaks the")
    L.append("  same class language as the per-lane reports)")
    L.append(f"- first-seen (window): {pat.first_seen.isoformat() if pat.first_seen else 'n/a'}")
    L.append(f"- last-seen (window): {pat.last_seen.isoformat() if pat.last_seen else 'n/a'}")
    L.append(f"- lanes affected: {pat.lanes_display(cap=99)}")
    L.append("- example detail (verbatim from the newest matching row class):")
    L.append(f"  `{no_emdash(pat.example_detail[:200])}`")
    L.append(f"- failure_kb join: {pat.fkb_count} matching rows in the windowed")
    L.append(f"  `logs/failure_kb.jsonl` ({pat.fkb_scanned} rows scanned)")
    if pat.fkb_sigs:
        L.append(f"  known sigs: {', '.join(no_emdash(s) for s in pat.fkb_sigs)}")
    else:
        L.append("  no matching signature - the KB covers seat/session failures;")
        L.append("  a lane-cycle pattern absent from it is new evidence, not noise")
    L.append("")
    L.append("## Evidence pairs (before/after)")
    L.append("")
    if pairs:
        for p in pairs:
            L.append(f"- lane `{p.lane}`: CYCLE_FAIL at {p.fail_raw_ts} ->")
            L.append(f"  {p.recovery_event} at {p.recovery_ts.isoformat()}")
            L.append(f"  (gap {int(p.gap_s)}s); recovery detail: {no_emdash(p.recovery_detail[:160])}")
    else:
        L.append("- none in this window: no lane shows this pattern failing and")
        L.append("  then greening or FIX-ing later in the window. The synthesis")
        L.append("  ask below works from the receipts and the failure shape alone.")
    L.append("")
    L.append("## Matching receipts (watch/inbox grep, cap 3)")
    L.append("")
    if receipts:
        for path, hit in receipts:
            L.append(f"- `{path}` (matched: {', '.join(hit)})")
    else:
        L.append("- none: no watch/inbox markdown matched this pattern's needles.")
        L.append("  The first packet for this class becomes the founding receipt.")
    L.append("")
    L.append("## SYNTHESIS ASK (seated step: a seat or free lane, not this tool)")
    L.append("")
    L.append("Draft ONE skill card for `.agents/skills/<verb-slug>/SKILL.md` that")
    L.append("prevents or repairs this pattern, in the estate's winning shape per")
    L.append("`watch/inbox/IMAGE_BLASTER_GO_20261003.md` (the five card-editing")
    L.append("rules its lane measured) with `.agents/skills/image-blast/SKILL.md`")
    L.append("as the template:")
    L.append("")
    L.append("1. argument-hint frontmatter - a real argument surface, not prose")
    L.append("2. exactly one verb per card")
    L.append("3. at least one runnable command with a verified (not phantom) path")
    L.append("4. gates written into the card text where the action happens")
    L.append("5. a `Final response:` line naming what the seat reports back")
    L.append("")
    L.append("Synthesize from the evidence pairs above (what failed, what")
    L.append("greened after), the receipts above, and the failure_kb signature")
    L.append("if one matched. The card must name this pattern's class key")
    L.append(f"(`{no_emdash(pat.key)}`) in its description so the falsifier can")
    L.append("measure it: a session with the card active should fail less on")
    L.append("this class than without (the arena/gwap instrument, per")
    L.append("watch/inbox/X_INTEL_PAPERS_20261004.md section 6's falsifier).")
    L.append("")
    L.append("## Promote gate (the commit stays human)")
    L.append("")
    L.append("This packet is the deliverable. Drafting the card is a separate")
    L.append("seated step BY DESIGN: the human promote gate (`mag.cmd promote")
    L.append("--apply`) stays the commit - autonomously drafted, humanly")
    L.append("promoted. The skill census law holds (the ractor50 verdict: waves")
    L.append("are the fuzzer, cards are the commits).")
    return "\n".join(L) + "\n"


# ------------------------------------------------------------- CLI

def build_table(patterns: list[Pattern], days: int, now: datetime,
                trail_summary: dict, normalizer_name: str) -> str:
    L: list[str] = []
    L.append("social_rsi PATTERN ROLL-UP v0")
    L.append(f"instrument: queue/lanes/*/trail.jsonl CYCLE_FAIL rows + "
             f"logs/failure_kb.jsonl known sigs")
    L.append(f"keying: {normalizer_name}")
    L.append(f"window: {days}d ending {now.isoformat(timespec='seconds')}")
    L.append(f"scanned: {trail_summary['trails']} trails, "
             f"{trail_summary['rows']} rows, "
             f"{trail_summary['malformed']} malformed lines named, "
             f"{trail_summary['no_ts']} rows without usable ts")
    if not patterns:
        L.append("no CYCLE_FAIL rows in the window: nothing to roll up")
        return "\n".join(L)
    header = f"{'rank':<5} {'count':>5}  {'class':<44} {'first':<10} {'last':<10} {'lanes':<28} {'fkb':>4}"
    L.append(header)
    L.append("-" * len(header))
    for i, pat in enumerate(patterns, 1):
        first = pat.first_seen.date().isoformat() if pat.first_seen else "-"
        last = pat.last_seen.date().isoformat() if pat.last_seen else "-"
        key = no_emdash(pat.key)[:44]
        L.append(f"{i:<5} {pat.count:>5}  {key:<44} {first:<10} {last:<10} "
                 f"{no_emdash(pat.lanes_display()):<28} {pat.fkb_count:>4}")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="social_rsi.py",
        description="Recursive Social Improvement v0: failure-pattern roll-up "
                    "over lane trails + failure_kb, evidence pairs, synthesis "
                    "packets. Query + packet surface only (no new store).")
    parser.add_argument("--check", action="store_true",
                        help="print the pattern roll-up table to stdout (writes nothing)")
    parser.add_argument("--packets", action="store_true",
                        help="write synthesis packets to watch/inbox/social_rsi/ "
                             "(implies the roll-up table)")
    parser.add_argument("--top", type=int, default=5,
                        help="top-N patterns to packet (default 5)")
    parser.add_argument("--days", type=int, default=14,
                        help="lookback window in days (default 14)")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                        help="repo root (default: this tool's repo; tests point it at tmp trees)")
    args = parser.parse_args(argv)

    if not args.check and not args.packets:
        parser.print_usage(sys.stderr)
        print("error: pass --check (stdout only) or --packets (write packets)",
              file=sys.stderr)
        return 2
    root = args.root.resolve()
    if not root.joinpath(*TRAIL_GLOB[:2]).is_dir():
        print(f"error: {root / 'queue' / 'lanes'} not found - not a mag root?",
              file=sys.stderr)
        return 2

    normalize, normalizer_name = _load_normalize_detail()
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=max(0, args.days))
    lanes, trail_summary = load_trails(root)
    fkb_rows = load_fkb_window(root, cutoff)
    patterns = rollup(lanes, cutoff, normalize, fkb_rows)

    print(build_table(patterns, args.days, now, trail_summary, normalizer_name))
    print(f"failure_kb window rows scanned: {len(fkb_rows)}")

    if not args.packets:
        return 0

    day = now.date().isoformat()
    out_dir = root.joinpath(*PACKET_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for pat in patterns[:max(0, args.top)]:
        pairs = evidence_pairs(pat, lanes, normalize)
        receipts, _scanned = find_receipts(root, pat)
        text = render_packet(pat, pairs, receipts, day, args.days, normalizer_name)
        for ch in _EMDASH_CHARS:
            assert ch not in text, f"em-dash leaked into packet for {pat.key!r}"
        path = packet_path(root, pat, day)
        path.write_text(text, encoding="utf-8")
        written.append(path)
        print(f"packet written: {path}")
        for p in pairs:
            print(f"  pair: {p.lane} fail {p.fail_raw_ts} -> "
                  f"{p.recovery_event} (+{int(p.gap_s)}s)")
        for rpath, hit in receipts:
            print(f"  receipt: {rpath} (matched: {', '.join(hit)})")
    if not written:
        print("no patterns in window: zero packets written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
