"""Regenerate the front door (docs/FRAMEWORK_LOAD.md) from live truth.

Why (Mickey17 W3, return 12, watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md):
two rival self-stories - FRAMEWORK_LOAD.md + compass narrated the August
estate while DNA.md pointed at the live ghost-self chain, so a cold seat
loaded an estate that no longer exists; plus v5 gates sat ok:true on disk
while the version registry still said planned, and the front door carried
dangling links. Never-trust-a-hand-written-count applied to the estate's own
self-description: the front door becomes a REGENERATED CLONE, re-rendered
from bytes at each wave close.

Truth sources (all read-only):
  - docs/templates/FRONT_DOOR_TEMPLATE.md   stable prose + REGEN placeholders
  - docs/archive/ZEITGEIST.md               era line (first matching heading)
  - memory/improve/releases/gates.jsonl     version + gate rows
  - memory/agent_state/LATEST.md            agent-state tip
  - repo root scandir                       top-level layout (ls semantics)

Determinism law: no wall clock, no dict iteration order, no locale. Every
auto section carries generated_at keyed to the NEWEST mtime of its own truth
sources, so two runs over an unchanged tree are byte-identical; --at pins
all stamps (receipts). Em-dash law: U+2014 anywhere in the render is a hard
exit 2 naming the output line - parsed truth is never silently laundered.

Usage (repo venv, never bare python):
    .venv/Scripts/python.exe tools/regen_front_door.py            # write the door
    .venv/Scripts/python.exe tools/regen_front_door.py --stdout   # print, no write
    .venv/Scripts/python.exe tools/regen_front_door.py --check    # 0 fresh / 1 stale / 2 error
    .venv/Scripts/python.exe tools/regen_front_door.py --at 2026-09-29T00:00:00Z
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

EMDASH = "\u2014"
DOOR_REL = Path("docs") / "FRAMEWORK_LOAD.md"
TEMPLATE_REL = Path("docs") / "templates" / "FRONT_DOOR_TEMPLATE.md"
ZEITGEIST_REL = Path("docs") / "archive" / "ZEITGEIST.md"
GATES_REL = Path("memory") / "improve" / "releases" / "gates.jsonl"
AGENT_STATE_REL = Path("memory") / "agent_state" / "LATEST.md"

# Curated key files for the layout section (existence-filtered, sorted).
KEY_ROOT_FILES = (
    "AGENTS.md",
    "CONSTITUTION.md",
    "LOAD.md",
    "README.md",
    "main.py",
    "mag.cmd",
    "pytest.ini",
    "requirements.txt",
)

PLACEHOLDER_RE = re.compile(r"^\s*<!--REGEN:(\w+)-->\s*$")
PINNED_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
# The zeitgeist era line (em-dash lives in the SOURCE; it never enters output).
ERA_RE = re.compile(
    r"^#\s+Zeitgeist\s+\u2014\s+era\s+(\d+)\s*:\s*(.+?)\s*"
    r"\(iterated\s+(\d{4}-\d{2}-\d{2})\)"
)

STAMP_NOTE_TRUTH = "truth-keyed: newest source mtime; rerun byte-identical until truth moves"
STAMP_NOTE_PINNED = "pinned via --at"


class RegenError(Exception):
    """Fail-closed regen error (maps to exit 2)."""


# ---------------------------------------------------------------- read truth


def _read(repo: Path, rel: Path) -> str:
    path = repo / rel
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        raise RegenError(f"missing truth source: {rel}") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise RegenError(f"unreadable truth source {rel}: {exc}") from None


def _mtime_z(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _stamp(paths: list[Path], pinned: str | None, note: str) -> str:
    if pinned:
        return f"*generated_at: {pinned} ({STAMP_NOTE_PINNED}; {note})*"
    newest = max(_mtime_z(p) for p in paths)
    return f"*generated_at: {newest} ({STAMP_NOTE_TRUTH}; {note})*"


# ------------------------------------------------------------------- parsers


@dataclass
class Era:
    number: str
    name: str
    iterated: str


@dataclass
class GateRow:
    version: str
    gate_id: str
    ok: bool
    ts: str


@dataclass
class Gates:
    versions: list[str] = field(default_factory=list)  # first-appearance order
    final: dict[tuple[str, str], GateRow] = field(default_factory=dict)
    last: GateRow | None = None


@dataclass
class AgentTip:
    commitment: str
    ts: str
    tip_root: str
    tip_n: str | None
    one_line: str
    anti: list[str] = field(default_factory=list)
    next_moves: list[str] = field(default_factory=list)


def parse_era(text: str) -> Era:
    """Parse the era line from the zeitgeist doc (searches the first 5 lines)."""
    for line in text.splitlines()[:5]:
        match = ERA_RE.match(line.strip())
        if match:
            return Era(match.group(1), match.group(2).strip(), match.group(3))
    head = next((ln for ln in text.splitlines() if ln.strip()), "")
    raise RegenError(f"zeitgeist era line unreadable near: {head[:100]!r} ({ZEITGEIST_REL})")


def parse_gates(text: str) -> Gates:
    """Parse gates.jsonl. The file is append-only truth, so the LAST row for a
    (version, gate_id) pair is the final state of that gate."""
    gates = Gates()
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            row = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise RegenError(f"gates.jsonl line {lineno} malformed: {exc}") from None
        missing = [k for k in ("version", "gate_id", "ok", "ts") if k not in row]
        if missing:
            raise RegenError(
                f"gates.jsonl line {lineno} missing keys {missing} ({GATES_REL})"
            )
        gate = GateRow(str(row["version"]), str(row["gate_id"]), bool(row["ok"]), str(row["ts"]))
        if gate.version not in gates.versions:
            gates.versions.append(gate.version)
        gates.final[(gate.version, gate.gate_id)] = gate
        gates.last = gate
    if gates.last is None:
        raise RegenError(f"gates.jsonl has no rows ({GATES_REL})")
    return gates


def _require_heading_block(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip().startswith(heading))
    except StopIteration:
        return []
    block: list[str] = []
    for ln in lines[start + 1 :]:
        if ln.strip().startswith("## "):
            break
        block.append(ln)
    return block


def parse_agent_state(text: str) -> AgentTip:
    def field_line(label: str) -> str | None:
        match = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$", text, re.M)
        return match.group(1) if match else None

    commitment = field_line("commitment")
    if not commitment:
        raise RegenError(f"agent-state commitment line missing ({AGENT_STATE_REL})")
    commitment = commitment.strip().strip("`")

    ts_raw = (field_line("ts") or "").strip()
    tip_raw = field_line("agent_tip_root") or ""
    tip_match = re.match(r"`([^`]+)`(?:\s*\u00b7\s*n=(\d+))?", tip_raw)
    if not tip_match:
        raise RegenError(f"agent-state tip root line unreadable ({AGENT_STATE_REL})")

    one_block = _require_heading_block(text, "## One line")
    one_line = next((ln.strip() for ln in one_block if ln.strip()), "")
    if not one_line:
        raise RegenError(f"agent-state one-line section missing ({AGENT_STATE_REL})")

    anti = [ln.strip()[2:].strip() for ln in _require_heading_block(text, "## Anti-reinvention") if ln.strip().startswith("- ")]
    moves = [re.sub(r"^\d+\.\s*", "", ln.strip()) for ln in _require_heading_block(text, "## Next moves") if re.match(r"^\d+\.", ln.strip())]

    return AgentTip(
        commitment=commitment,
        ts=ts_raw,
        tip_root=tip_match.group(1),
        tip_n=tip_match.group(2),
        one_line=one_line,
        anti=anti,
        next_moves=moves,
    )


# ----------------------------------------------------------------- renderers


def render_era(era: Era, repo: Path, pinned: str | None) -> str:
    stamp = _stamp([repo / ZEITGEIST_REL], pinned, f"source: {ZEITGEIST_REL.as_posix()}")
    return (
        "## Current era (auto)\n"
        "\n"
        f"- **Era:** {era.number} - {era.name}\n"
        f"- **Iterated:** {era.iterated}\n"
        f"- **Source:** `{ZEITGEIST_REL.as_posix()}` (parsed from the era line)\n"
        "\n"
        f"{stamp}\n"
    )


def render_gates(gates: Gates, repo: Path, pinned: str | None) -> str:
    stamp = _stamp([repo / GATES_REL], pinned, f"source: {GATES_REL.as_posix()}")
    last = gates.last
    assert last is not None  # parse_gates guarantees it
    lines = [
        "## Version + gates (auto)",
        "",
        f"Latest gate row: `{last.version} / {last.gate_id} / {'ok' if last.ok else 'FAIL'}` "
        f"stamped {last.ts[:10]}.",
        "",
        "| Version | Gates ok | Open gates | Last gate stamp |",
        "|---|---|---|---|",
    ]
    for version in gates.versions:
        rows = [r for (v, _), r in gates.final.items() if v == version]
        ok_count = sum(1 for r in rows if r.ok)
        open_ids = sorted(r.gate_id for r in rows if not r.ok)
        lines.append(
            f"| {version} | {ok_count}/{len(rows)} | "
            f"{', '.join(open_ids) if open_ids else 'none'} | "
            f"{max(r.ts for r in rows)[:10]} |"
        )
    lines += [
        "",
        "Gate truth here is the jsonl bytes; the final row per gate wins. When a",
        "registry or roadmap label disagrees with this table, the bytes win (W3",
        "return 12 named the inverse-trap: all-pass gates under a still-planned",
        "label).",
        "",
        stamp,
    ]
    return "\n".join(lines) + "\n"


def render_agent_state(tip: AgentTip, repo: Path, pinned: str | None) -> str:
    stamp = _stamp([repo / AGENT_STATE_REL], pinned, f"source: {AGENT_STATE_REL.as_posix()}")
    n_part = f" n={tip.tip_n}" if tip.tip_n else ""
    lines = [
        "## Agent-state tip (auto)",
        "",
        f"- **One line:** {tip.one_line}",
        f"- **Commitment:** `{tip.commitment}`",
        f"- **Tip:** `{tip.tip_root}`{n_part}",
        f"- **Stamped:** {tip.ts}",
        f"- **Source:** `{AGENT_STATE_REL.as_posix()}` (agent tip, not session tip; "
        "LOAD before redesign)",
    ]
    if tip.anti:
        lines += ["", "**Anti-reinvention (hard):** " + " · ".join(tip.anti)]
    if tip.next_moves:
        lines += ["", "**Next moves (ordered):**"]
        lines += [f"{i}. {move}" for i, move in enumerate(tip.next_moves, 1)]
    lines += ["", stamp]
    return "\n".join(lines) + "\n"


def render_layout(repo: Path, pinned: str | None) -> str:
    dirs: list[str] = []
    file_count = 0
    with os.scandir(repo) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.name.startswith("."):
                dirs.append(entry.name)
            elif entry.is_file():
                file_count += 1
    dirs.sort(key=lambda name: (name.lower(), name))
    keys = sorted(f for f in KEY_ROOT_FILES if (repo / f).is_file())
    stamp = _stamp([repo], pinned, "source: repo root mtime")
    wrapped = textwrap.fill(", ".join(dirs), width=88) or "(none)"
    return (
        "## Top-level layout (auto)\n"
        "\n"
        f"{len(dirs)} directories at root (complete list, ls semantics: dot-entries hidden):\n"
        "\n"
        "```text\n"
        f"{wrapped}\n"
        "```\n"
        "\n"
        f"Key files: {', '.join(keys) if keys else '(none found)'} "
        f"(plus {file_count} root files, scratch-heavy by design and elided here).\n"
        "\n"
        f"{stamp}\n"
    )


# -------------------------------------------------------------------- build


def build(repo: Path, pinned: str | None = None) -> tuple[str, dict[str, str]]:
    """Render the door. Returns (markdown, section -> generated_at stamp value)."""
    template = _read(repo, TEMPLATE_REL)
    era = parse_era(_read(repo, ZEITGEIST_REL))
    gates = parse_gates(_read(repo, GATES_REL))
    tip = parse_agent_state(_read(repo, AGENT_STATE_REL))

    rendered = {
        "ERA": render_era(era, repo, pinned),
        "GATES": render_gates(gates, repo, pinned),
        "AGENT_STATE": render_agent_state(tip, repo, pinned),
        "LAYOUT": render_layout(repo, pinned),
    }
    stamps = {
        key: re.search(r"\*generated_at: (\S+) ", body).group(1)  # type: ignore[union-attr]
        for key, body in rendered.items()
    }

    out_lines: list[str] = []
    for line in template.splitlines():
        match = PLACEHOLDER_RE.match(line)
        if match:
            key = match.group(1)
            if key not in rendered:
                raise RegenError(f"template uses unknown placeholder <!--REGEN:{key}-->")
            out_lines.append(rendered.pop(key))
        else:
            out_lines.append(line)
    if rendered:
        raise RegenError(f"template is missing placeholders: {sorted(rendered)}")

    out = "\n".join(out_lines).rstrip("\n") + "\n"

    if EMDASH in out:
        for lineno, ln in enumerate(out.splitlines(), 1):
            if EMDASH in ln:
                raise RegenError(
                    f"em-dash in render at output line {lineno}: {ln.strip()[:100]}"
                )

    return out, stamps


def default_repo() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate docs/FRAMEWORK_LOAD.md from live truth (deterministic, em-dash 0)."
    )
    parser.add_argument("--repo", default=str(default_repo()), help="repo root (default: this repo)")
    parser.add_argument("--stdout", action="store_true", help="print the render instead of writing")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare only: exit 0 fresh, 1 stale, 2 error",
    )
    parser.add_argument(
        "--at",
        default=None,
        help="pin all generated_at stamps, e.g. 2026-09-29T00:00:00Z (default: truth-keyed mtimes)",
    )
    args = parser.parse_args(argv)

    if args.at and not PINNED_AT_RE.match(args.at):
        print(f"regen_front_door: --at must match YYYY-MM-DDTHH:MM:SSZ, got {args.at!r}", file=sys.stderr)
        return 2

    repo = Path(args.repo).resolve()
    try:
        out, stamps = build(repo, args.at)
    except RegenError as exc:
        print(f"regen_front_door: FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2

    if args.stdout:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.write(out)
        return 0

    door = repo / DOOR_REL
    existing = door.read_bytes() if door.exists() else None
    fresh = existing == out.encode("utf-8")
    if args.check:
        print(f"{DOOR_REL.as_posix()}: {'fresh' if fresh else 'stale'}")
        return 0 if fresh else 1

    if fresh:
        print(f"regen_front_door: {DOOR_REL.as_posix()} already fresh ({len(out)} bytes)")
    else:
        door.parent.mkdir(parents=True, exist_ok=True)
        door.write_bytes(out.encode("utf-8"))
        print(f"regen_front_door: wrote {DOOR_REL.as_posix()} ({len(out)} bytes, LF)")
    for key in ("ERA", "GATES", "AGENT_STATE", "LAYOUT"):
        print(f"  {key.lower()} generated_at={stamps[key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
