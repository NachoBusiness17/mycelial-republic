#!/usr/bin/env python3
"""tools/attention_dam.py - the attention dam (Mickey17 W3, 2026-09-30).

Telemetry finding: memory/attention.md floods with a `### Session record
ready` block every ~90s (mag/biography.py `_ping_attention` prepends one per
biographer cycle), so real alerts ([priority][probe-alarm] DOWN lines, census
COLLECT-DRIFT patrol verdicts, gate-canary DEAD/BLIND canaries) sink under
hundreds of session-record lines and the operator stops reading the file.

The dam (this tool):
  1. CLASSIFIES attention.md blocks: signal (probe-alarm, patrol, gate,
     DOWN, DRIFT, any [priority] alert, any non-session heading, the
     preserved-alert sentinel) vs noise (the closed class of session-record/
     biography boilerplate blocks). Noise is the ONLY archivable class --
     anything unrecognized stays in attention.md (signal-by-default).
  2. ONE PASS moves noise blocks verbatim to the dated archive
     (memory/attention_archive_20260930.md by default) -- move, not delete --
     and leaves a pointer note in the attention.md header naming the archive.
  3. `--stats` reports the signal:noise ratio read-only; a dam pass prints
     the same stats before and after.
  4. Idempotent: a pass that finds zero noise blocks writes nothing, so
     back-to-back runs leave both files byte-identical and never stack
     duplicate pointer notes.

Region contract respected: mag/act.py `evict_for_prepend` splits attention.md
at ATTENTION_ALERT_SENTINEL and bottom-appenders (census patrol, improve)
write below it; the dam never removes the sentinel and never reorders the
surviving blocks, so the flood/evict machinery keeps working unchanged.

Run: .venv/Scripts/python.exe tools/attention_dam.py           # dam pass
     .venv/Scripts/python.exe tools/attention_dam.py --stats   # read-only
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ATTENTION = ROOT / "memory" / "attention.md"
DEFAULT_ARCHIVE = ROOT / "memory" / "attention_archive_20260930.md"

# Same sentinel mag/act.py owns; duplicated here only to recognize and keep it.
SENTINEL = "<!-- attention:alerts-preserved-below -->"

# The one noise class: biography session-record boilerplate.
SESSION_HEADING_RE = re.compile(r"^### Session record ready \((first|amended)\)\s*$")

# Signal markers. A block carrying ANY of these is kept no matter what.
# (case matters: DOWN/DRIFT are shouted on purpose; probe-alarm/patrol/gate
# classes are matched case-insensitively as tags/words.)
SIGNAL_RES = tuple(
    re.compile(p)
    for p in (
        r"\[priority\]",  # any priority-tagged alert line (covers probe-alarm/gate-canary)
        r"probe-alarm",
        r"patrol",
        r"gate-canary",
        r"\[gate",
        r"\bDOWN\b",
        r"\bDRIFT\b",
        re.escape(SENTINEL),
    )
)

# Markdown thematic-break separators are the block boundaries (same shape
# mag/act.py ATTENTION_BLOCK_SEP uses for its whole-block eviction).
SEP_RE = re.compile(r"(?m)^---\s*$")

# The dam's own header furniture, stripped before parsing so reruns never
# stack duplicate pointers.
TITLE_RE = re.compile(r"(?m)^# Mag attention\s*$")
POINTER_RE = re.compile(r"(?m)^<!-- attention-dam: .*$\n?")


@dataclass
class DamStats:
    """Line/block census of one attention.md state."""

    total_lines: int = 0
    signal_lines: int = 0
    noise_lines: int = 0
    signal_blocks: int = 0
    noise_blocks: int = 0

    @property
    def ratio(self) -> str:
        if self.noise_lines == 0:
            return f"{self.signal_lines}:0"
        if self.signal_lines == 0:
            return f"0:{self.noise_lines}"
        g = _gcd(self.signal_lines, self.noise_lines)
        return f"{self.signal_lines // g}:{self.noise_lines // g}"

    def as_dict(self) -> dict[str, object]:
        return {
            "total_lines": self.total_lines,
            "signal_lines": self.signal_lines,
            "noise_lines": self.noise_lines,
            "signal_blocks": self.signal_blocks,
            "noise_blocks": self.noise_blocks,
            "signal_noise_ratio": self.ratio,
        }


@dataclass
class Classification:
    """Split of attention.md into kept-signal blocks and noise blocks."""

    signal_blocks: list[str] = field(default_factory=list)
    noise_blocks: list[str] = field(default_factory=list)


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a or 1


def is_noise_block(block: str) -> bool:
    """True only for known session-record boilerplate with no signal inside.

    Conservative by construction: an unrecognized block, or a session block
    carrying any signal marker (an alert line appended inside it), is kept.
    """
    lines = block.splitlines()
    has_session_heading = any(SESSION_HEADING_RE.match(ln) for ln in lines)
    if not has_session_heading:
        return False
    body = "\n".join(
        ln for ln in lines if not SESSION_HEADING_RE.match(ln)
    )
    return not any(rx.search(body) for rx in SIGNAL_RES)


def classify(text: str) -> Classification:
    """Classify attention.md content into signal (keep) and noise blocks."""
    body = TITLE_RE.sub("", text)
    body = POINTER_RE.sub("", body)
    # Noise is the closed class: is_noise_block demands a session-record
    # heading AND a body with no signal marker, so any block with a
    # non-session heading (patrol blocks, future alert shapes) or any
    # unrecognized content is kept as signal by default.
    pieces: list[str] = []
    for piece in SEP_RE.split(body):
        # The sentinel is a harness-owned boundary (mag/act.py): bottom-
        # appenders glue alert lines straight after the last record body
        # with no --- between, so split there instead of letting the last
        # session block ride inside the preserved-alert piece.
        idx = piece.find(SENTINEL)
        if idx > 0:
            pieces.append(piece[:idx])
            pieces.append(piece[idx:])
        else:
            pieces.append(piece)
    out = Classification()
    for piece in pieces:
        if not piece.strip():
            continue  # pure whitespace between separators carries nothing
        if is_noise_block(piece):
            out.noise_blocks.append(piece)
        else:
            out.signal_blocks.append(piece)
    return out


def stats_of(text: str) -> DamStats:
    """Line/block census of one attention.md state (signal vs noise)."""
    cls = classify(text)
    st = DamStats()
    st.total_lines = len(text.rstrip("\n").splitlines())
    for b in cls.signal_blocks:
        st.signal_lines += len(b.strip("\n").splitlines())
    for b in cls.noise_blocks:
        st.noise_lines += len(b.strip("\n").splitlines())
    st.signal_blocks = len(cls.signal_blocks)
    st.noise_blocks = len(cls.noise_blocks)
    return st


def _render(signal_blocks: list[str], pointer: str) -> str:
    parts = ["# Mag attention\n", pointer, "\n"]
    parts.append("\n---\n\n".join(b.strip("\n") for b in signal_blocks))
    return "".join(parts).rstrip("\n") + "\n"


def dam_pass(
    attention_path: Path, archive_path: Path, *, dry_run: bool = False
) -> dict[str, object]:
    """One dam pass: move noise blocks to the archive, keep signal.

    Returns a report dict with before/after stats. Idempotent: zero noise
    blocks (with the pointer already in place) writes nothing at all.
    """
    if not attention_path.is_file():
        raise FileNotFoundError(f"attention file not found: {attention_path}")
    text = attention_path.read_text(encoding="utf-8")
    before = stats_of(text)
    cls = classify(text)
    already_dammed = bool(POINTER_RE.search(text))

    if not cls.noise_blocks:
        after = before
        archived_lines = 0
        if not dry_run and not already_dammed and text.strip():
            # Clean file, first dam visit: leave the pointer so the archive
            # contract is visible even when there was nothing to move.
            attention_path.write_text(
                _render(cls.signal_blocks, _pointer(0, 0, archive_path)),
                encoding="utf-8",
            )
            after = stats_of(attention_path.read_text(encoding="utf-8"))
        return {
            "before": before.as_dict(),
            "after": after.as_dict(),
            "archived_blocks": 0,
            "archived_lines": 0,
            "dry_run": dry_run,
            "wrote": False,
        }

    archived_lines = sum(len(b.strip("\n").splitlines()) for b in cls.noise_blocks)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pointer = _pointer(len(cls.noise_blocks), archived_lines, archive_path)

    if not dry_run:
        # Archive: move, not delete. Blocks land verbatim, original order.
        if archive_path.is_file():
            with archive_path.open("a", encoding="utf-8") as fh:
                fh.write(f"\n\n<!-- dam run {stamp}: +{len(cls.noise_blocks)} blocks -->\n\n")
                for b in cls.noise_blocks:
                    fh.write(b.strip("\n") + "\n\n---\n\n")
        else:
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            with archive_path.open("w", encoding="utf-8") as fh:
                fh.write(
                    "# attention archive 2026-09-30\n\n"
                    "Session-record noise moved from memory/attention.md by\n"
                    "tools/attention_dam.py (the dam). Move, not delete: every\n"
                    "block below is byte-preserved. Signal (probe-alarm, patrol,\n"
                    "gate, DOWN, DRIFT, [priority] alerts) stayed in attention.md.\n\n"
                )
                fh.write(f"<!-- dam run {stamp}: {len(cls.noise_blocks)} blocks -->\n\n")
                for b in cls.noise_blocks:
                    fh.write(b.strip("\n") + "\n\n---\n\n")
        attention_path.write_text(_render(cls.signal_blocks, pointer), encoding="utf-8")
        after = stats_of(attention_path.read_text(encoding="utf-8"))
    else:
        after = stats_of(_render(cls.signal_blocks, pointer))

    return {
        "before": before.as_dict(),
        "after": after.as_dict(),
        "archived_blocks": len(cls.noise_blocks),
        "archived_lines": archived_lines,
        "dry_run": dry_run,
        "wrote": not dry_run,
    }


def _pointer(blocks: int, lines: int, archive_path: Path) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    what = (
        f"archived {blocks} session-record noise blocks ({lines} lines)"
        if blocks
        else "no noise blocks present"
    )
    return (
        f"<!-- attention-dam: {stamp} dam pass {what} to "
        f"{archive_path.name}; signal kept; noise moved, not deleted -->\n"
    )


def _fmt(label: str, st: dict[str, object]) -> str:
    return (
        f"{label}: total={st['total_lines']} lines | "
        f"signal={st['signal_lines']} lines/{st['signal_blocks']} blocks | "
        f"noise={st['noise_lines']} lines/{st['noise_blocks']} blocks | "
        f"ratio signal:noise = {st['signal_noise_ratio']}"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="the attention dam (see module docstring)")
    ap.add_argument("--attention", type=Path, default=DEFAULT_ATTENTION)
    ap.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    ap.add_argument("--stats", action="store_true", help="read-only report, no writes")
    ap.add_argument("--dry-run", action="store_true", help="report the pass, write nothing")
    args = ap.parse_args(argv)

    if args.stats:
        if not args.attention.is_file():
            print(f"attention file not found: {args.attention}", file=sys.stderr)
            return 2
        st = stats_of(args.attention.read_text(encoding="utf-8"))
        print(_fmt("stats", st.as_dict()))
        return 0

    report = dam_pass(args.attention, args.archive, dry_run=args.dry_run)
    print(_fmt("before", report["before"]))
    print(_fmt("after ", report["after"]))
    verb = "would archive" if args.dry_run else "archived"
    print(
        f"dam: {verb} {report['archived_blocks']} noise blocks "
        f"({report['archived_lines']} lines) -> {args.archive}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
