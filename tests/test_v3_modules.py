"""v3 research modules — loops, resonance, spider, conductor, grove."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_loops_registry():
    from mag.loops_registry import build_registry

    reg = build_registry()
    assert reg.get("schema") == "mag_loops_registry.v1"
    assert reg["summary"]["total"] >= 5
    ids = {r["id"] for r in reg["loops"]}
    assert "resonance" in ids and "spider" in ids
    assert "switchboard" in ids


def test_resonance_top_cards():
    from mag.resonance import score_echoes, tick

    cards = score_echoes("autorun improve mag", limit=3)
    assert isinstance(cards, list)
    res = tick("test goal", dry=True)
    assert res.get("ok") is True
    assert res.get("written") is False


def test_resonance_l0e_format():
    from mag.resonance import format_l0e

    text = format_l0e([{"kind": "remedy", "title": "test", "excerpt": "x", "path": "a/b", "score": 1.0}])
    assert "L0e Resonance" in text


def test_spider_tick_dry():
    from mag.spider import tick

    res = tick(dry=True, inject=False)
    assert res.get("ok") is True
    assert "signals" in res


def test_spider_detects_fkb_repeat():
    """Regression: spider was blind to FKB patterns because it called
    recurring_patterns(limit=5) which raises TypeError (no such kwarg),
    silently swallowed by the except block. Now it must surface fkb_repeat
    signals when the FKB index has recurring signatures."""
    from mag.spider import (
        FKB_REPEAT_THRESHOLD,
        FKB_SEVERE_KINDS,
        FKB_SEVERE_REPEAT_THRESHOLD,
        _check_fkb_repeat,
    )

    sigs = _check_fkb_repeat()
    # Live FKB index census 2026-09-28: 15 signatures; the spider must see the
    # recurring ones (Q-008: the old thresholds emitted only 5 of 15).
    assert isinstance(sigs, list)
    fkb = [s for s in sigs if s.get("kind") == "fkb_repeat"]
    assert len(fkb) >= 1, "spider should surface FKB repeat signals"
    # Each signal must carry a real signature (not None) and a count that
    # meets its kind's floor (Q-008: ordinary >=2, severe kinds >=1).
    for s in fkb:
        assert s.get("signature"), "fkb_repeat signal must carry a signature"
        floor = (
            FKB_SEVERE_REPEAT_THRESHOLD
            if s.get("fkb_kind") in FKB_SEVERE_KINDS
            else FKB_REPEAT_THRESHOLD
        )
        assert int(s.get("count") or 0) >= floor


def test_spider_fkb_no_rank_slice_and_severe_kinds():
    """Q-008 regression (2026-09-28): against the real 2026-09-27 index the
    spider emitted only 5 of 15 signatures via two mechanisms: the [:5] rank
    slice hid recurring sigs ranked 6+ (run_shell:c73866f2f1b5 x11 with a
    remedy attached was invisible under 4 guard_registry rows plus the 804x
    amd_window_guard), and the flat count>=3 bar hid the severe kinds
    (collapse x2, fake_success x1). Contract now: no rank cut, ordinary kinds
    at count>=2, collapse/fake_success at count>=1 with severity=error, and
    count-1 ordinary sigs stay hidden (FKB log-only law)."""
    import mag.failure_kb as fkb_mod
    from mag import spider

    synthetic: dict = {"schema": "failure_kb.signatures.v1", "signatures": {}}
    sigs_def = synthetic["signatures"]
    for i, c in zip(range(4), (800, 50, 41, 32)):
        s = f"guard_registry:{i:012x}"
        sigs_def[s] = {"sig": s, "tool": "guard_registry", "kind": "guard_registry", "count": c}
    sigs_def["run_shell:00000000c738"] = {"sig": "run_shell:00000000c738", "tool": "run_shell", "kind": "tool_fail", "count": 11}
    sigs_def["run_shell:00000000b471"] = {"sig": "run_shell:00000000b471", "tool": "run_shell", "kind": "http_tool_fail", "count": 1}
    sigs_def["run_shell:0000000069ef"] = {"sig": "run_shell:0000000069ef", "tool": "run_shell", "kind": "tool_fail", "count": 2}
    sigs_def["write_file:00000000f86c"] = {"sig": "write_file:00000000f86c", "tool": "write_file", "kind": "collapse", "count": 1}
    sigs_def["write_file:00000000e49e"] = {"sig": "write_file:00000000e49e", "tool": "write_file", "kind": "fake_success", "count": 2}

    orig = fkb_mod._load_index
    fkb_mod._load_index = lambda: synthetic
    try:
        out = spider._check_fkb_repeat()
    finally:
        fkb_mod._load_index = orig

    by_sig = {s.get("signature"): s for s in out if s.get("kind") == "fkb_repeat"}
    # The x11 tool_fail surfaces even though 4 guard sigs outrank it (the old
    # [:5] slice silently dropped exactly this shape in the real index).
    assert "run_shell:00000000c738" in by_sig
    # Severe kinds surface on first occurrence, flagged error.
    assert by_sig["write_file:00000000f86c"]["count"] == 1
    assert by_sig["write_file:00000000f86c"]["severity"] == "error"
    assert by_sig["write_file:00000000e49e"]["count"] == 2
    assert by_sig["write_file:00000000e49e"]["severity"] == "error"
    # Ordinary x2 meets the new floor of 2.
    assert "run_shell:0000000069ef" in by_sig
    # Count-1 ordinary sig stays hidden: the spider detects recurrence, and
    # the FKB's own policy keeps count-1 sigs log-only.
    assert "run_shell:00000000b471" not in by_sig
    # No rank cut: every threshold-passing sig is present (8 of 9).
    assert len(by_sig) == 8


def test_conductor_phase_detect():
    from mag.conductor import conduct, detect_phase

    assert detect_phase("[priority] plan only architecture") == "plan"
    assert detect_phase("[build] implement pytest") == "build"
    assert detect_phase("audit only ponytail diff") == "audit"
    res = conduct("mag autorun smoke test", dry=True)
    assert res.get("schema") == "conductor.v1"
    assert res.get("route")


def test_grove_build_dry():
    from mag.grove import build

    res = build(dry=True)
    assert res.get("ok") is True
    assert res.get("dry") is True


def test_context_pack_has_resonance_layer(monkeypatch):
    from mag.context_pack import build_context_pack

    pack = build_context_pack()
    layers = pack.get("layers") or []
    assert "L0e_resonance" in layers
    assert "resonance_cards" in pack
