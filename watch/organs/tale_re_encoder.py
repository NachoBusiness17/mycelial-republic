#!/usr/bin/env python3
"""TALE-RE-ENCODER v0 -- the fleet's typed tape retold as a monomyth.

Organ: watch/INTAKE_HEROS_JOURNEY_20260903.md (built 2026-09-03).
Reads typed rows (ts/kind/detail) from watch/room.jsonl, maps one UTC day's
spine onto Campbell stages deterministically, writes a story brief markdown.

Campbell mapping (monomyth as query protocol):
  CALL      = first typed row of the window   (what summoned the fleet)
  THRESHOLD = kinds containing gate/falsifier/audit (the guarded crossing)
  ALLIES    = distinct actors/chairs/seats named in details (who walked in)
  DRAGON    = rows whose detail says died/disputed/falsified/reject
  ELIXIR    = receipts and closures (wire.closed, falsifier.run verdicts,
              *.fold, receipt kinds)
  RETURN    = last typed row of the window    (what the day left on the tape)

Typed rows matching no stage land in "The Road Between" appendix: the
coverage law applies to tales too -- a recorded act must not vanish.

Legacy rows (seat/event/text schema, pre-typed-tape) are counted for
honesty but not mapped: they are mostly bootstrap chatter, and mapping
them would make the CALL a heartbeat, not a summons.

Stdlib only. Zero network. Fails loud: missing tape, empty window, or a
window with zero typed rows exits nonzero with the reason on stderr.
Malformed tape lines are skipped with a loud stderr warning and reported
in the counts (the tape is a shared append log; one wrapped line must
not kill the organ), but a fully unparseable tape is a hard failure.
"""

import argparse
import json
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TAPE = REPO_ROOT / "watch" / "room.jsonl"
DEFAULT_OUT_DIR = REPO_ROOT / "watch" / "tales"

EXCERPT_WORDS = 12

# ---------------------------------------------------------------------------
# Actor lexicon: the fleet names its actors (seats, chairs, the operator).
# Seats match case-insensitively on word boundaries; chairs are the ractor
# panel names and match case-sensitively as they are styled in the tape.
# Extending the roster is a one-line edit here, nothing else.
# ---------------------------------------------------------------------------
SEAT_NAMES = [
    "operator", "sancho", "quixote", "zcode", "copilot", "claw", "codex",
    "driver", "forge", "watcher", "maze-keeper", "grok", "deepseek", "qwen",
]
CHAIR_NAMES = ["JUNG", "BERNAYS", "ELLUL"]

SEAT_RE = re.compile(
    r"\b(" + "|".join(re.escape(n) for n in SEAT_NAMES) + r")\b", re.IGNORECASE
)
CHAIR_RE = re.compile(r"\b(" + "|".join(CHAIR_NAMES) + r")\b")

DRAGON_RE = re.compile(r"\b(died|disputed|falsified|reject\w*)\b", re.IGNORECASE)

THRESHOLD_TOKENS = ("gate", "falsifier", "audit")
ELIXIR_EXACT = {"wire.closed"}
ELIXIR_SUFFIX = ".fold"
ELIXIR_TOKENS = ("receipt", "falsifier.run")


class TapeFail(SystemExit):
    """Fail-loud exit with a TALE ENCODER FAIL banner."""


def fail(msg: str) -> None:
    print(f"TALE ENCODER FAIL: {msg}", file=sys.stderr)
    raise SystemExit(2)


def excerpt(detail: str, limit: int = EXCERPT_WORDS) -> str:
    words = detail.split()
    text = " ".join(words[:limit])
    return text + (" ..." if len(words) > limit else "")


def read_tape(tape_path: Path):
    """Parse the JSONL tape. Returns (rows, stats_dict). Rows preserve file
    order. Unparseable lines are skipped loudly and counted."""
    if not tape_path.is_file():
        fail(f"tape not found: {tape_path}")
    rows = []
    bad_lines = 0
    replaced_chars = 0
    with tape_path.open("r", encoding="utf-8", errors="replace") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                bad_lines += 1
                print(
                    f"TALE ENCODER WARN: skipped malformed tape line {lineno}",
                    file=sys.stderr,
                )
                continue
            if not isinstance(row, dict):
                bad_lines += 1
                print(
                    f"TALE ENCODER WARN: skipped non-object tape line {lineno}",
                    file=sys.stderr,
                )
                continue
            if "\ufffd" in json.dumps(row, ensure_ascii=False):
                replaced_chars += 1
            rows.append(row)
    stats = {"bad_lines": bad_lines, "encoding_repairs": replaced_chars}
    return rows, stats


def window_rows(rows, date_str: str):
    """Rows whose ts starts with the ISO date. Missing-ts rows are skipped
    and counted; a window with zero rows fails loud."""
    inside, no_ts = [], 0
    for row in rows:
        ts = row.get("ts")
        if not isinstance(ts, str) or not ts:
            no_ts += 1
            continue
        if ts.startswith(date_str):
            inside.append(row)
    if not inside:
        fail(f"no tape rows at all for {date_str} in {len(rows)} parsed rows")
    return inside, no_ts


def typed_rows(window):
    """The story spine: rows carrying kind/detail. Legacy rows (seat/event)
    are counted but not mapped -- see module docstring."""
    typed, legacy = [], 0
    for row in window:
        if isinstance(row.get("kind"), str) and row["kind"]:
            typed.append(row)
        else:
            legacy += 1
    if not typed:
        fail(
            f"window has {len(window)} rows but zero typed (kind/detail) rows; "
            "the monomyth needs a typed spine"
        )
    return typed, legacy


def find_allies(rows):
    """Distinct actors named in details, with first-seen row citation.
    Deterministic scan against the roster; case-insensitive dedupe."""
    seen = OrderedDict()  # canonical -> dict(name, row)
    for row in rows:
        detail = str(row.get("detail", ""))
        for match in CHAIR_RE.finditer(detail):
            key = match.group(1).upper()
            seen.setdefault(key, {"name": match.group(1), "row": row})
        for match in SEAT_RE.finditer(detail):
            key = match.group(1).lower()
            seen.setdefault(key, {"name": match.group(1), "row": row})
    return seen


def map_stages(rows):
    """Deterministic Campbell mapping over the typed spine (file order).
    Returns dict stage -> list of citation dicts; a row may serve two
    stages (the threshold crossing can yield the first elixir)."""
    stages = {
        "CALL": [],
        "THRESHOLD": [],
        "ALLIES": [],
        "DRAGON": [],
        "ELIXIR": [],
        "RETURN": [],
    }
    stages["CALL"].append(cite(rows[0], "first typed row of the window"))
    stages["RETURN"].append(cite(rows[-1], "last typed row of the window"))

    for row in rows:
        kind = str(row.get("kind", ""))
        detail = str(row.get("detail", ""))
        if any(tok in kind for tok in THRESHOLD_TOKENS):
            stages["THRESHOLD"].append(cite(row, "gate/falsifier/audit kind"))
        if DRAGON_RE.search(detail):
            stages["DRAGON"].append(cite(row, "falsified/dead/disputed thing"))
        is_elixir = (
            kind in ELIXIR_EXACT
            or kind.endswith(ELIXIR_SUFFIX)
            or any(tok in kind for tok in ELIXIR_TOKENS)
        )
        if is_elixir:
            stages["ELIXIR"].append(cite(row, "receipt or closure"))

    allies = find_allies(rows)
    stages["ALLIES"] = [
        {
            "ts": info["row"].get("ts", "?"),
            "kind": str(info["row"].get("kind", "?")),
            "excerpt": excerpt(str(info["row"].get("detail", ""))),
            "why": f"actor named in detail: {info['name']}",
            "actor": info["name"],
        }
        for info in allies.values()
    ]
    return stages


def cite(row, why: str) -> dict:
    return {
        "ts": row.get("ts", "?"),
        "kind": str(row.get("kind", "?")),
        "excerpt": excerpt(str(row.get("detail", ""))),
        "why": why,
    }


def render_tale(date_str: str, stages, counts) -> str:
    """Story brief: Campbell stages as headers, one line per mapped row
    citing ts + kind + 12-word excerpt."""
    lines = []
    lines.append(f"# TALE -- {date_str}")
    lines.append("")
    lines.append(
        f"*The fleet's typed tape for {date_str}, retold through the monomyth "
        f"by tale_re_encoder v0. Typed spine: {counts['typed']} rows; "
        f"legacy rows present, unmapped: {counts['legacy']}; "
        f"malformed tape lines skipped: {counts['bad_lines']}.*"
    )
    lines.append("")

    stage_meta = [
        ("CALL", "I. The Call -- what summoned the fleet"),
        ("THRESHOLD", "II. The Threshold -- the guarded crossing"),
        ("ALLIES", "III. The Allies -- who walked in"),
        ("DRAGON", "IV. The Dragon -- what was falsified, disputed, slain"),
        ("ELIXIR", "V. The Elixir -- receipts carried back"),
        ("RETURN", "VI. The Return -- what the day left on the tape"),
    ]
    for key, header in stage_meta:
        lines.append(f"## {header}")
        lines.append("")
        entries = stages[key]
        if not entries:
            lines.append("_No rows mapped to this stage today._")
            lines.append("")
            continue
        if key == "ALLIES":
            names = ", ".join(e["actor"] for e in entries)
            lines.append(f"Named on the tape ({len(entries)} distinct): {names}.")
            lines.append("")
            for e in entries:
                lines.append(
                    f"- **{e['actor']}** -- first named `{e['ts']}` "
                    f'`{e["kind"]}`: "{e["excerpt"]}"'
                )
        else:
            for e in entries:
                lines.append(
                    f"- `{e['ts']}` `{e['kind']}` -- {e['why']}: "
                    f'"{e["excerpt"]}"'
                )
        lines.append("")

    road = stages.get("ROAD", [])
    if road:
        lines.append(
            "## The Road Between -- typed rows mapping to no Campbell stage"
        )
        lines.append("")
        lines.append(
            "_(organ appendix, not a Campbell stage: the coverage law keeps "
            "recorded acts in the story)_"
        )
        lines.append("")
        for e in road:
            lines.append(f"- `{e['ts']}` `{e['kind']}` -- \"{e['excerpt']}\"")
        lines.append("")

    lines.append("---")
    lines.append(
        "*Encoded by watch/organs/tale_re_encoder v0 -- stdlib only, zero "
        "network. Stages are lenses, not buckets: a row may serve two.*"
    )
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Retell one day of the typed room tape as a Campbell monomyth."
    )
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="UTC date to encode, YYYY-MM-DD (default: today UTC)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="output markdown path (default: watch/tales/TALE_<date>.md)",
    )
    parser.add_argument(
        "--tape",
        default=str(DEFAULT_TAPE),
        help="tape JSONL path (default: watch/room.jsonl)",
    )
    args = parser.parse_args(argv)

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        fail(f"--date must be YYYY-MM-DD, got: {args.date!r}")

    rows, tape_stats = read_tape(Path(args.tape))
    window, no_ts = window_rows(rows, args.date)
    spine, legacy = typed_rows(window)

    stages = map_stages(spine)

    # Road Between: typed spine rows that landed in no Campbell stage.
    placed = set()
    for key in ("CALL", "THRESHOLD", "DRAGON", "ELIXIR", "RETURN"):
        for e in stages[key]:
            placed.add((e["ts"], e["kind"], e["excerpt"]))
    road = []
    for row in spine:
        c = cite(row, "typed row")
        if (c["ts"], c["kind"], c["excerpt"]) not in placed:
            road.append(c)
    stages["ROAD"] = road

    counts = {
        "parsed": len(rows),
        "window": len(window),
        "typed": len(spine),
        "legacy": legacy,
        "no_ts": no_ts,
        "bad_lines": tape_stats["bad_lines"],
        "stages_populated": sum(
            1 for key in ("CALL", "THRESHOLD", "ALLIES", "DRAGON", "ELIXIR", "RETURN")
            if stages[key]
        ),
    }

    out_path = (
        Path(args.out)
        if args.out
        else DEFAULT_OUT_DIR / f"TALE_{args.date}.md"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_tale(args.date, stages, counts), encoding="utf-8")

    print(f"TALE: {out_path}")
    print(
        f"rows: {counts['parsed']} parsed | {counts['window']} in window "
        f"{args.date} | {counts['typed']} typed (spine) | {counts['legacy']} "
        f"legacy (unmapped) | {counts['bad_lines']} malformed skipped"
    )
    print(
        "stages: "
        + " ".join(
            f"{k}={len(stages[k])}"
            for k in ("CALL", "THRESHOLD", "ALLIES", "DRAGON", "ELIXIR", "RETURN", "ROAD")
        )
        + f" | populated: {counts['stages_populated']}/6"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
