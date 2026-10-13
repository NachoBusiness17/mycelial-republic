"""Tests for tools/regen_front_door.py (Mickey17 W3, return 12).

Covers the two landing laws named in the wave ask:
  - template render determinism: two runs over an unchanged tree are
    byte-identical (including on the live repo);
  - era parse fixture: the zeitgeist era line parses, variants parse, and a
    dead line fails closed.
Plus the em-dash fail-closed law, --at stamp pinning, gates final-row-wins,
and placeholder integrity.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import tools.regen_front_door as rfd

REPO = Path(__file__).resolve().parents[1]

TEMPLATE_FIXTURE = """# Fake repo front door

Header prose line.

<!--REGEN:ERA-->
<!--REGEN:GATES-->
<!--REGEN:AGENT_STATE-->
<!--REGEN:LAYOUT-->

## Stable section

Stable body.
"""

ZEITGEIST_FIXTURE = (
    "# Zeitgeist \u2014 era 003: THE POUR (iterated 2026-09-05)\n\nbody\n"
)

GATES_FIXTURE = "\n".join(
    [
        '{"schema": "mag_release_gate.v1", "ts": "2026-08-06T12:00:00+00:00", "version": "v2", "gate_id": "run_a", "ok": false, "note": "awaiting merge"}',
        '{"schema": "mag_release_gate.v1", "ts": "2026-08-06T13:00:00+00:00", "version": "v2", "gate_id": "run_a", "ok": true, "note": "merged"}',
        '{"schema": "mag_release_gate.v1", "ts": "2026-09-26T13:35:47+00:00", "version": "v5", "gate_id": "regime_law", "ok": true, "note": "landed"}',
        "",
    ]
)

LATEST_FIXTURE = """# Agent state LOAD - ghost-self

**schema:** `mag_agent_state.v1`
**commitment:** `fixture-window-20260929T000000Z`
**ts:** 2026-09-29T00:00:00+00:00
**agent_tip_root:** `deadbeefdeadbeef\u2026` \u00b7 n=42

## One line (do not reinvent)

ghost-self: sensing 3 surfaces \u00b7 graph 10n/2e

## Anti-reinvention (hard)

- redesign the graph
- prompt the operator for secrets

## Next moves (ordered)

1. first move
2. second move

## Stack snapshot
"""


def make_repo(tmp_path: Path) -> Path:
    (tmp_path / "docs" / "templates").mkdir(parents=True)
    (tmp_path / "docs" / "archive").mkdir(parents=True)
    (tmp_path / "memory" / "improve" / "releases").mkdir(parents=True)
    (tmp_path / "memory" / "agent_state").mkdir(parents=True)
    (tmp_path / "docs" / "templates" / "FRONT_DOOR_TEMPLATE.md").write_text(
        TEMPLATE_FIXTURE, encoding="utf-8"
    )
    (tmp_path / "docs" / "archive" / "ZEITGEIST.md").write_text(
        ZEITGEIST_FIXTURE, encoding="utf-8"
    )
    (tmp_path / "memory" / "improve" / "releases" / "gates.jsonl").write_text(
        GATES_FIXTURE, encoding="utf-8"
    )
    (tmp_path / "memory" / "agent_state" / "LATEST.md").write_text(
        LATEST_FIXTURE, encoding="utf-8"
    )
    (tmp_path / "AGENTS.md").write_text("x", encoding="utf-8")
    (tmp_path / "scratch.txt").write_text("x", encoding="utf-8")
    (tmp_path / "mag").mkdir()
    return tmp_path


# ---------------------------------------------------------- determinism law


def test_two_runs_byte_identical(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    first, _ = rfd.build(repo)
    second, _ = rfd.build(repo)
    assert first == second


def test_real_repo_two_runs_byte_identical() -> None:
    first, _ = rfd.build(REPO)
    second, _ = rfd.build(REPO)
    assert first == second


# ------------------------------------------------------------ era parse law


def test_era_parse_canonical() -> None:
    era = rfd.parse_era("# Zeitgeist \u2014 era 003: THE POUR (iterated 2026-09-05)\n")
    assert (era.number, era.name, era.iterated) == ("003", "THE POUR", "2026-09-05")


def test_era_parse_variant() -> None:
    era = rfd.parse_era(
        "prose line\n# Zeitgeist \u2014 era 004: THE FLOOD (iterated 2026-10-01)\n"
    )
    assert (era.number, era.name, era.iterated) == ("004", "THE FLOOD", "2026-10-01")


def test_era_parse_fails_closed() -> None:
    with pytest.raises(rfd.RegenError, match="era line unreadable"):
        rfd.parse_era("# Zeitgeist (no era clause here)\n")


# -------------------------------------------------------------- em-dash law


def test_render_has_no_emdash_despite_emdash_sources(tmp_path: Path) -> None:
    # Both the zeitgeist era line and the tip root carry U+2014/U+2026 in the
    # source; neither may leak into the render.
    out, _ = rfd.build(make_repo(tmp_path))
    assert "\u2014" not in out
    assert "Era:** 003 - THE POUR" in out


def test_emdash_in_template_fails_closed(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    template = repo / "docs" / "templates" / "FRONT_DOOR_TEMPLATE.md"
    template.write_text(TEMPLATE_FIXTURE + "\nhand-written \u2014 slip\n", encoding="utf-8")
    with pytest.raises(rfd.RegenError, match="em-dash in render"):
        rfd.build(repo)


# ------------------------------------------------------------- stamps / --at


def test_pinned_at_appears_in_all_four_sections(tmp_path: Path) -> None:
    out, stamps = rfd.build(make_repo(tmp_path), "2026-09-29T00:00:00Z")
    assert out.count("*generated_at: 2026-09-29T00:00:00Z") == 4
    assert set(stamps.values()) == {"2026-09-29T00:00:00Z"}


def test_truth_keyed_stamps_render_iso(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    _, stamps = rfd.build(repo)
    assert len(stamps) == 4
    assert all(len(stamp) == 20 and stamp.endswith("Z") for stamp in stamps.values())


# ---------------------------------------------------------------- gates law


def test_gates_final_row_wins_and_open_gates_surface(tmp_path: Path) -> None:
    gates = rfd.parse_gates(GATES_FIXTURE)
    assert gates.final[("v2", "run_a")].ok is True  # later row flipped it green
    out, _ = rfd.build(make_repo(tmp_path))
    assert "| v2 | 1/1 | none | 2026-08-06 |" in out
    assert "regime_law" in out


def test_gates_open_gate_listed_after_later_fail(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    gates_path = repo / "memory" / "improve" / "releases" / "gates.jsonl"
    gates_path.write_text(
        GATES_FIXTURE.rstrip("\n")
        + "\n"
        + '{"schema": "mag_release_gate.v1", "ts": "2026-09-28T00:00:00+00:00", "version": "v5", "gate_id": "regime_law", "ok": false, "note": "regressed"}',
        encoding="utf-8",
    )
    out, _ = rfd.build(repo)
    assert "| v5 | 0/1 | regime_law | 2026-09-28 |" in out


def test_gates_malformed_row_fails_closed() -> None:
    with pytest.raises(rfd.RegenError, match="malformed"):
        rfd.parse_gates("{not json}\n")


# --------------------------------------------------------- template assembly


def test_missing_placeholder_fails_closed(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    template = repo / "docs" / "templates" / "FRONT_DOOR_TEMPLATE.md"
    template.write_text(TEMPLATE_FIXTURE.replace("<!--REGEN:LAYOUT-->\n", ""), encoding="utf-8")
    with pytest.raises(rfd.RegenError, match="missing placeholders"):
        rfd.build(repo)


def test_agent_state_tip_fields_render(tmp_path: Path) -> None:
    out, _ = rfd.build(make_repo(tmp_path))
    assert "fixture-window-20260929T000000Z" in out
    assert "ghost-self: sensing 3 surfaces" in out
    assert "n=42" in out
    assert "redesign the graph \u00b7 prompt the operator for secrets" in out
    assert "1. first move" in out
