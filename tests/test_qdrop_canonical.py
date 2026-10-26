"""Q-drop canonical numbering guard tests (B2-404, 2026-09-26).

Ground truth (B2-93 receipt + B2-14 correction, both byte-anchored):
canonical drop #874 = Snowden HK post (id 580331, local drop_no 1088); the
Think Bridge post (id 967331, local drop_no 1406) = canonical drop #1104 and
is the 874th Q-authored row. qdrops.jsonl's drop_no FIELD is the local
renumbering (B2-67: local 200 = q_num 174), never the canonical number.
"""
from __future__ import annotations

import importlib.util
import io
import inspect
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
TOOL = HERE / "watch" / "inbox" / "qdrop_export" / "qdrop_canonical.py"


def _mod():
    spec = importlib.util.spec_from_file_location("qdrop_canonical", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["qdrop_canonical"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def qdrops():
    return _mod().load_qdrops()


def test_local_field_is_not_canonical_snowden(qdrops):
    m = _mod()
    info = m.canonical_drop_no(qdrops, id="580331", ts="2018-03-07")
    assert info["local_drop_no"] == 1088        # the qdrops.jsonl drop_no field
    assert info["canonical_drop_no"] == 874     # receipt-anchored (B2-14/B2-93)
    assert info["canonical_anchored"] is True


def test_think_bridge_is_canonical_1104_not_874(qdrops):
    m = _mod()
    info = m.canonical_drop_no(qdrops, id="967331", ts="2018-04-09")
    assert info["local_drop_no"] == 1406
    assert info["canonical_drop_no"] == 1104
    assert info["canonical_anchored"] is True


def test_unanchored_row_refuses_a_canonical_number(qdrops):
    m = _mod()
    row = next(r for r in qdrops if str(r.get("id")) == "580366")  # local 1089
    info = m.canonical_drop_no(qdrops, id="580366", ts="2018-03-07")
    assert info["canonical_drop_no"] is None
    assert info["canonical_anchored"] is False
    assert "NOT confirmed canonical" in info["warning"]
    label = m.drop_label(info["local_drop_no"], None, info["id"], str(row["ts"]))
    assert "canonical number unanchored" in label


def test_resolver_refuses_position_and_unmatched_lookups(qdrops):
    m = _mod()
    with pytest.raises(ValueError):
        m.canonical_drop_no(qdrops, id="580331")                    # ts missing
    with pytest.raises(ValueError):
        m.canonical_drop_no(qdrops, id="580331", ts="2018-03-07T99:00:00Z")  # ts mismatch
    with pytest.raises(ValueError):
        m.canonical_drop_no(qdrops, id="000000", ts="2018-03-07")   # unknown id
    with pytest.raises(ValueError):
        m.canonical_drop_no(qdrops, id=None, ts="2018-03-07")       # position ignored


def test_line_6423_counter_shape_now_carries_the_guard_warning(qdrops):
    """The falsifier, killed: rerunning the line-6423 shape (874th Q-authored
    row) must NOT yield a bare 'Q drop #874'; it returns the resolved
    canonical number (#1104) and a mandatory warning naming the trap."""
    m = _mod()
    info = m.q_authored_ordinal_guard(qdrops, 874)
    assert info["id"] == "967331"                     # the Think Bridge post
    assert info["canonical_drop_no"] == 1104          # anchored canonical
    assert info["conflated"] is True                  # 874th ordinal != local 1406
    assert "NOT canonical drop #874" in info["guard_warning"]
    assert "line-6423" in info["guard_warning"]


def test_drop_label_takes_fields_never_a_position():
    m = _mod()
    label = m.drop_label(1088, 874, "580331", "2018-03-07T20:56:26+00:00")
    assert label == "canonical drop #874 (id 580331, ts 2018-03-07T20:56:26+00:00)"
    sig = inspect.signature(m.drop_label)
    assert list(sig.parameters) == ["local_drop_no", "canonical_drop_no", "id", "ts"]


def test_cli_guard_demo_exits_2_on_conflation(qdrops):
    m = _mod()
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = m.main(["--guard", "874"])
    assert rc == 2
    assert "GUARD" in buf.getvalue()
