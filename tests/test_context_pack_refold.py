"""ReFold reversible pack sheds (port-order lane P5, 2026-10-07).

Pins the steal: every shed rung files a reversible stub (section name + source
organ + content sha256 + chars) into the offload row instead of silent-drop
telemetry; the stage-3 fold leaves a marker line naming the restore door;
restore re-renders the section from the stub's named source, sha-verified;
the ledger reader skips torn non-UTF8 rows with a note and flags stale-code
budget rows; renders stay byte-identical between fold advances.
Receipt: watch/inbox/port_wave_20261007/p5_refold.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FOLD_RE = re.compile(
    r"^\[SHED this fold: (\d+) sections \| restore: python -m mag\.context_pack sheds\]$"
)


def _fold_markers(text: str) -> list[int]:
    return [int(m.group(1)) for ln in text.splitlines() if (m := FOLD_RE.match(ln))]


def _row_stubs(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        for st in r.get("stubs") or []:
            out.append(st)
    return out


def _shed_sources() -> dict:
    from mag.context_pack import SHED_SOURCES

    return SHED_SOURCES


@pytest.fixture(scope="module")
def route_pack() -> dict:
    from mag.context_pack import build_context_pack

    return build_context_pack(mode="route", fast=True)


def _forced_shed_render(monkeypatch, tmp_path, pack, mode="route", max_chars=5200):
    from mag import context_pack as cp

    monkeypatch.setattr(cp, "PACK_OFFLOAD_FILE", tmp_path / "PACK_OFFLOAD.jsonl")
    text = cp.format_context_pack_text(pack, mode=mode, max_chars=max_chars)
    rows = []
    f = tmp_path / "PACK_OFFLOAD.jsonl"
    if f.is_file():
        rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return text, rows


def test_shed_rows_carry_reversible_stubs(monkeypatch, tmp_path, route_pack):
    """Every shed files a stub row: section + source organ + sha256 + chars.
    The ledger is a restore index, not write-only telemetry."""
    text, rows = _forced_shed_render(monkeypatch, tmp_path, route_pack)
    stubs = _row_stubs(rows)
    assert stubs, "forced overflow filed no stubs: the drop is still irreversible"
    for st in stubs:
        assert st["section"] in _shed_sources(), f"stub {st['section']!r} not in SHED_SOURCES"
        assert st["source"], "stub carries no source organ path"
        assert re.fullmatch(r"[0-9a-f]{64}", st["sha256"]), "stub sha256 malformed"
        assert isinstance(st["chars"], int) and st["chars"] >= 0
    assert all(r.get("schema") == "pack_offload.v1" for r in rows), (
        "schema string drifted: stubs ride as an additive field under v1")
    assert _fold_markers(text), "stage-3 fold left no marker line in the render"
    assert _fold_markers(text)[-1] == len([r for r in rows if r.get("stage") == 3]), (
        "fold marker count does not match the stage-3 sheds filed")


def test_shed_then_restore_round_trips_byte_identical(monkeypatch, tmp_path, route_pack):
    """The ReFold core law: restore re-renders the shed section and the bytes
    match the stub's recorded sha256 + char count exactly."""
    from mag.context_pack import restore_shed_section

    _text, rows = _forced_shed_render(monkeypatch, tmp_path, route_pack)
    stubs = _row_stubs(rows)
    assert stubs, "no stubs filed; nothing to restore"
    for st in stubs:
        res = restore_shed_section(st["section"], mode="route", pack=route_pack,
                                   sha=st["sha256"])
        assert res["ok"], f"restore refused for {st['section']}: {res.get('reason')}"
        assert res["sha256"] == st["sha256"], f"restored sha mismatch for {st['section']}"
        assert res["chars"] == st["chars"], f"restored char count mismatch for {st['section']}"


def test_restore_sha_gate_refuses_drifted_organ(monkeypatch, tmp_path, route_pack):
    """A wrong sha must refuse the restore, never silently pass."""
    from mag.context_pack import restore_shed_section

    _text, rows = _forced_shed_render(monkeypatch, tmp_path, route_pack)
    stubs = _row_stubs(rows)
    assert stubs
    st = stubs[0]
    bad = "0" * 64 if st["sha256"] != "0" * 64 else "1" * 64
    res = restore_shed_section(st["section"], mode="route", pack=route_pack, sha=bad)
    assert not res["ok"], "restore accepted a sha that matches nothing"
    assert "mismatch" in (res.get("reason") or "")


def test_render_byte_identical_between_fold_advances(monkeypatch, tmp_path, route_pack):
    """No per-render jitter: consecutive renders under the same organ state are
    byte-identical, shed rungs and fold markers included."""
    from mag import context_pack as cp

    monkeypatch.setattr(cp, "PACK_OFFLOAD_FILE", tmp_path / "PACK_OFFLOAD.jsonl")
    t1 = cp.format_context_pack_text(route_pack, mode="route", max_chars=5200)
    t2 = cp.format_context_pack_text(route_pack, mode="route", max_chars=5200)
    assert t1 == t2, "render jitter: consecutive renders diverged"
    assert _fold_markers(t1), "forced overflow never folded on this pack"


def test_unsheded_render_carries_no_fold_marker(route_pack):
    """No fold, no marker: a render with ample budget carries zero SHED lines."""
    from mag.context_pack import format_context_pack_text

    text = format_context_pack_text(route_pack, mode="route", max_chars=40000)
    assert "[SHED " not in text, "fold marker leaked into a render that never overflowed"


def test_ledger_reader_skips_torn_non_utf8_row(tmp_path):
    """A torn partial write (the live 80 a6 + CR row) is skipped with a note,
    never a crash, and good rows around it still parse."""
    from mag.context_pack import read_pack_offload

    good = json.dumps({
        "ts": "2026-10-07T21:11:41Z", "schema": "pack_offload.v2", "mode": "route",
        "max_chars": 5800, "total_chars": 6000, "shed_sections": ["L0e resonance"],
        "stage": 3, "stubs": [], "root_short": "",
    })
    stale = json.dumps({
        "ts": "2026-10-07T23:05:24Z", "schema": "pack_offload.v1", "mode": "full",
        "max_chars": 7200, "total_chars": 9471, "shed_sections": ["L0d zeitgeist"],
        "stage": 3, "root_short": "",
    })
    f = tmp_path / "PACK_OFFLOAD.jsonl"
    raw = (good + "\n").encode("utf-8") + b"\x80\xa6\"}\r\n" + (stale + "\n").encode("utf-8")
    f.write_bytes(raw)
    led = read_pack_offload(path=f)
    assert led["raw_lines"] == 3
    assert len(led["rows"]) == 2, "good rows around the torn row must still parse"
    assert led["torn_rows"] == 1
    assert led["torn_notes"] and "non-UTF8" in led["torn_notes"][0]


def test_reader_flags_stale_code_rows_against_current_budget(tmp_path):
    """A row emitted under a dead constant (the full/7200 family) is flagged
    stale_code against the current MODE_CONFIG budget."""
    from mag.context_pack import MODE_CONFIG, read_pack_offload

    row = {
        "ts": "2026-10-07T23:05:24Z", "schema": "pack_offload.v1", "mode": "full",
        "max_chars": 7200, "total_chars": 9471, "shed_sections": ["L0d zeitgeist"],
        "stage": 3, "root_short": "",
    }
    f = tmp_path / "PACK_OFFLOAD.jsonl"
    f.write_text(json.dumps(row) + "\n", encoding="utf-8")
    led = read_pack_offload(path=f)
    assert led["rows"], "row lost"
    flagged = led["rows"][0].get("stale_code")
    assert flagged, "stale-code row not flagged"
    assert flagged["emitted_max_chars"] == 7200
    assert flagged["current_max_chars"] == MODE_CONFIG["full"]["max_chars"]


def test_list_shed_stubs_collects_v2_stubs(monkeypatch, tmp_path):
    """list_shed_stubs reads v2 rows back out of the ledger as a restore index."""
    from mag import context_pack as cp

    monkeypatch.setattr(cp, "PACK_OFFLOAD_FILE", tmp_path / "PACK_OFFLOAD.jsonl")
    cp.format_context_pack_text(
        cp.build_context_pack(mode="route", fast=True), mode="route", max_chars=5200)
    led = cp.list_shed_stubs(tail=100)
    assert led["stubs"], "no stubs listed from a shedding render's ledger"
    st = led["stubs"][0]
    for key in ("section", "source", "sha256", "chars", "ts", "mode"):
        assert key in st, f"stub index missing {key}"


def test_recipe_mirrors_live_section_build(route_pack):
    """The recipe rebuild of an UNSHED section must equal the live render bytes:
    this is what makes restore byte-identical, so it is pinned directly."""
    from mag.context_pack import _shed_recipe_render, format_context_pack_text

    # Ample budget: nothing sheds, so every section's live bytes are present.
    full_render = format_context_pack_text(route_pack, mode="route", max_chars=40000)
    for name in ("L1 bonds", "L0 coordination", "L1b/L1c skills + ijl + mirror/clue"):
        rebuilt = "\n".join(_shed_recipe_render(name, route_pack, "route"))
        assert rebuilt and rebuilt in full_render, (
            f"recipe for {name} diverged from the live build")


def test_restore_cli_exit_codes(monkeypatch, tmp_path, route_pack, capsys):
    """The restore CLI reports OK on a verified restore and exit 1 on drift."""
    from mag import context_pack as cp

    _text, rows = _forced_shed_render(monkeypatch, tmp_path, route_pack)
    stubs = _row_stubs(rows)
    assert stubs
    st = stubs[0]
    # Pin the CLI's fresh-pack rebuild to the module fixture so the sha
    # verdict tests the gate, not organ drift between two builds.
    monkeypatch.setattr(cp, "build_context_pack", lambda **kw: dict(route_pack))
    assert cp._main(["restore", "--section", st["section"], "--mode", "route",
                     "--sha", st["sha256"]]) == 0
    bad = "f" * 64
    assert cp._main(["restore", "--section", st["section"], "--mode", "route",
                     "--sha", bad]) == 1
    assert cp._main(["restore", "--section", "no such section", "--mode", "route"]) == 1
    out = capsys.readouterr().out
    assert "sha verified" in out


def test_sheds_cli_lists_ledger(monkeypatch, tmp_path, capsys):
    """The sheds CLI reads the ledger and reports torn rows without crashing."""
    from mag import context_pack as cp

    f = tmp_path / "PACK_OFFLOAD.jsonl"
    good = json.dumps({
        "ts": "2026-10-07T23:05:24Z", "schema": "pack_offload.v2", "mode": "plan",
        "max_chars": 11000, "total_chars": 12000, "shed_sections": ["L0d zeitgeist"],
        "stage": 3,
        "stubs": [{"section": "L0d zeitgeist", "source": "docs/archive/ZEITGEIST.md",
                   "sha256": "a" * 64, "chars": 800}],
        "root_short": "",
    })
    f.write_bytes((good + "\n").encode("utf-8") + b"\x80\xa6\r\n")
    monkeypatch.setattr(cp, "PACK_OFFLOAD_FILE", f)
    assert cp._main(["sheds", "--tail", "10"]) == 0
    out = capsys.readouterr().out
    assert "torn=1" in out
    assert "L0d zeitgeist" in out


def test_stage1_heat_shed_files_stub(monkeypatch, tmp_path, route_pack):
    """Stage 1 (heat drop) files a reversible stub too, not a silent drop."""
    from mag import context_pack as cp

    pack = dict(route_pack)
    pack["live_tail"] = "x" * 4000
    _text, rows = _forced_shed_render(monkeypatch, tmp_path, pack,
                                      mode="plan", max_chars=9000)
    heat_stubs = [s for s in _row_stubs(rows)
                  if s["section"] == "L4 Heat (live_tail, attention)"]
    assert heat_stubs, "stage 1 heat drop filed no stub"
    st = heat_stubs[0]
    res = cp.restore_shed_section("L4 Heat (live_tail, attention)", mode="plan",
                                  pack=pack, sha=st["sha256"])
    assert res["ok"] and res["chars"] == st["chars"]
