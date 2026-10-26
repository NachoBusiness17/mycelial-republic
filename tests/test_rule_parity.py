"""tests for tools/rule_parity.py — the V5 parity harness (2026-09-30).

Laws pinned here:
  - generation is byte-deterministic per seed (the canonical JSON both
    sides consume is reproducible);
  - the Python side is FAITHFUL to the authoritative server path: for the
    mountain family its per-tick graph hashes equal MountainWorld's
    (server/world.py) on the same frames — so a divergence the comparator
    reports is engine-real, not harness artifact;
  - the comparator finds the FIRST divergent tick with both hashes, and
    stays silent (parity=True) on identical rows;
  - end-to-end: the harness runs both engines when the Godot binary
    exists. It asserts the report's parity verdict MATCHES the rows (the
    honest-orbit law: the instrument is trusted because it is checked
    against itself, not because parity is assumed).

The harness's parity VERDICT on random boards is deliberately NOT pinned
by a test: the verdict is the measurement, and the measurement is allowed
to say "diverged" (receipt watch/inbox/last_mile_20260930/V5_PARITY.md).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.rule_parity import (  # noqa: E402
    GODOT_EXE, HYDRO_SHAPES, QUICK_FRAME_BUDGET, PROFILES, HarnessWorld,
    canonical_state_text, compare, generate, resolve_params, run_python,
    state_hash, total_frames,
)

server_world = pytest.importorskip("server.world")


# ------------------------------------------------------- ci profile law ----

def test_profiles_quick_small_full_receipt_compatible():
    """D2 contract: quick = 20 sequences (the pre-push payload), full = the
    nightly depth profile (seed 20260930, n=100, ticks=120). Profile PARAMS
    are the V5 receipt's; the R8 mix amendment (2026-09-30) added the
    stress_domain family to the same-seed corpus — the V5 byte-compat claim
    retired by receipt R8_INT_DOMAIN.md, frame totals unchanged."""
    assert PROFILES["quick"]["n"] == 20
    assert PROFILES["full"] == {"seed": 20260930, "n": 100, "ticks": 120}


def test_resolve_params_flags_beat_profile():
    assert resolve_params("quick", None, None, None) == dict(PROFILES["quick"])
    got = resolve_params("quick", seed=7, n=5, ticks=9)
    assert got == {"seed": 7, "n": 5, "ticks": 9}


def test_quick_corpus_covers_every_family_within_frame_budget():
    """The mix law: a 20-sequence quick run must still exercise EVERY family
    (the LW5 gated-siblings seam is where the v0 divergence lived - twenty
    mountain copies would be a gate that cannot see today's bug), and stay
    inside the frame budget that backs the <60s pre-push cost. R8: the
    stress_domain family is part of 'every family' — the pre-push gate must
    cross the int64 ceiling every run. Q11 (2026-10-01): the receipt family
    (the legality ladder) is part of 'every family' too. Q02 (2026-10-01):
    the hydrology family (graded head) joins that law."""
    doc = generate(PROFILES["quick"]["seed"], PROFILES["quick"]["n"],
                   PROFILES["quick"]["ticks"])
    fams = {s["family"] for s in doc["sequences"]}
    assert fams == {"mountain", "gated_siblings", "economy",
                    "fracture_loop", "stress_domain", "receipt",
                    "hydrology", "random"}
    assert len(doc["sequences"]) == 20
    frames = total_frames(doc)
    assert frames <= QUICK_FRAME_BUDGET, frames


def test_full_corpus_is_receipt_shaped():
    """R8 mix amendment: stress_domain 8 carved from random; Q11 mix
    amendment (2026-10-01): receipt 8 carved from random (18 -> 10); Q02
    mix amendment (2026-10-01): hydrology 6 carved from economy
    (24 -> 22) and random (10 -> 6) — the LW5 gated-siblings seam keeps
    its full share — and the 14,040 frame total is the V5 receipt shape
    (every non-fracture family shares the profile tick count)."""
    doc = generate(PROFILES["full"]["seed"], PROFILES["full"]["n"],
                   PROFILES["full"]["ticks"])
    fams: dict[str, int] = {}
    for s in doc["sequences"]:
        fams[s["family"]] = fams.get(s["family"], 0) + 1
    assert fams == {"mountain": 20, "gated_siblings": 24, "economy": 22,
                    "fracture_loop": 6, "stress_domain": 8, "receipt": 8,
                    "hydrology": 6, "random": 6}
    assert total_frames(doc) == 14040      # the V5 receipt's 14,040 tick frames


def test_small_n_generation_still_spreads_families():
    """n<20 used to be all-mountain (the v0 mix cap); the D2 mix law scales
    the mountain share down instead so even tiny corpora hit the seam."""
    doc = generate(seed=99, n=12, ticks=10)
    fams = {s["family"] for s in doc["sequences"]}
    assert "gated_siblings" in fams and "mountain" in fams


# --------------------------------------------------------------- gen law ----

def test_generate_is_deterministic_per_seed():
    a = generate(seed=99, n=12, ticks=15)
    b = generate(seed=99, n=12, ticks=15)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_generate_seeds_differ():
    a = generate(seed=1, n=12, ticks=10)
    b = generate(seed=2, n=12, ticks=10)
    assert json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True)


def test_generate_family_mix_and_shape():
    doc = generate(seed=5, n=100, ticks=120)
    fams: dict[str, int] = {}
    for s in doc["sequences"]:
        fams[s["family"]] = fams.get(s["family"], 0) + 1
        assert len(s["frames"]) == s["ticks"]
        names = {n["name"] for n in s["nodes"]}
        for p in s["pipes"]:
            assert p["src"] in names and p["dst"] in names
    assert set(doc["verbs"]) == set(server_world.VERBS)
    assert doc["max_say"] == server_world.MAX_SAY   # Q11: no forked bound
    assert fams["mountain"] == 20          # the shipping board is always covered
    assert fams["gated_siblings"] >= 10    # the LW5 seam family
    assert fams["fracture_loop"] >= 1      # AC2 burst window exercised
    assert fams["stress_domain"] >= 1      # R8: the int64 ceiling crossed
    assert fams["receipt"] >= 2            # Q11: the legality ladder exercised
    assert fams["hydrology"] >= 1          # Q02: the graded-head law exercised
    assert sum(fams.values()) == 100


# ------------------------------------------------------------ python law ----

def test_run_python_rows_complete():
    doc = generate(seed=3, n=6, ticks=8)
    rows = run_python(doc)
    assert len(rows) == sum(len(s["frames"]) for s in doc["sequences"])
    for r in rows:
        assert len(r["hash"]) == 64 and r["tick"] >= 1


def test_receipt_family_covers_every_reject_class():
    """Q11: the offline mirror must reject exactly what the server rejects
    at receipt. The receipt family walks the full ladder, so its verdicts
    must include every typed reject the server can emit on the action path
    plus the acks that prove the envelopes SPEND correctly (whisper spends
    the tick window; rejects spend nothing but the nonce)."""
    doc = generate(seed=20260930, n=100, ticks=12)
    receipt = [s for s in doc["sequences"] if s["family"] == "receipt"]
    assert len(receipt) >= 2
    rows = run_python({"verbs": doc["verbs"], "max_say": doc["max_say"],
                       "sequences": receipt})
    verdicts = [v for r in rows for v in r["verdicts"]]
    codes = {v[len("reject:"):] for v in verdicts if v.startswith("reject:")}
    assert codes >= {"UNKNOWN_SID", "UNKNOWN_VERB", "UNKNOWN_TARGET",
                     "DRY_POOL", "BAD_TEXT", "STALE_NONCE", "RATE_CAP",
                     "BAD_MAC"}, codes
    # the spend laws: whisper acks (direct, still spends the window — the
    # RATE_CAP above proves it), plain acks exist, and tamper goes dark
    # (the mac_* variants' post-tamper frames emit NO verdict at all)
    assert "ack" in verdicts
    dark_seqs = [s for s in receipt if s.get("arm_at_tick", -1) > 0]
    assert dark_seqs, "the corpus must include an armed (BAD_MAC) sequence"
    for s in dark_seqs:
        seq_rows = sorted((r for r in rows if r["seq"] == s["id"]),
                          key=lambda r: r["tick"])
        armed = next(r for r in seq_rows
                     if r["tick"] >= s["arm_at_tick"])
        assert armed["verdicts"] == ["reject:BAD_MAC"]
        later = [r for r in seq_rows if r["tick"] > armed["tick"]]
        assert all(r["verdicts"] == [] for r in later), \
            "tamper disconnects: later frames never arrive"


def test_python_side_is_faithful_to_the_authoritative_server():
    """The harness's Python side must BE the server law: same frames through
    the server's own receipt ladder (protocol_table.ReceiptGate around
    server/world.py MountainWorld — server/server.py _admit_action's exact
    ordering, replayed here 1:1) produce the same per-tick graph hashes. A
    reported engine divergence can then only be mag/water_graph.py vs
    water_graph.gd — never the shim. Q11 (2026-10-01): the oracle grew the
    ReceiptGate with the shim — the offline mirror now rejects exactly what
    the server rejects at receipt (RATE_CAP/STALE_NONCE included)."""
    from server.protocol_table import NO_NONCE, ReceiptGate
    doc = generate(seed=11, n=20, ticks=40)
    mountain_seqs = [s for s in doc["sequences"] if s["family"] == "mountain"]
    assert mountain_seqs, "seed 11 mix must include the mountain family"
    seq = mountain_seqs[0]
    world = server_world.MountainWorld()
    for sid in seq["sids"]:
        world.register_session(sid, f"user_{sid}")
    gate = ReceiptGate()
    harness_rows = [r for r in run_python({"verbs": doc["verbs"],
                                           "max_say": doc["max_say"],
                                           "sequences": [seq]})
                    if r["seq"] == seq["id"]]
    for t, frame in enumerate(seq["frames"], start=1):
        for act in frame:
            # server/server.py _admit_action :489-521, verbatim ordering:
            # nonce law (burns at receipt) -> world validation -> rate cap
            # (spent only by an ack) -> stage -> commit.
            nonce = act["n"] if "n" in act else NO_NONCE
            why = gate.admit_nonce(act["sid"], nonce)
            if why is None:
                ok, why = world.validate(act["sid"], act["verb"], act["target"])
                if ok:
                    why = None
            if why is None:
                applies_at = world.graph.tick_count + 1
                why = gate.admit_cap(act["sid"], applies_at)
            if why is None:
                reply = world.stage(act["sid"], act["verb"], act["target"])
                if reply["op"] == "ack":
                    gate.commit(act["sid"], applies_at)
        world.tick()
        assert state_hash(world.graph) == harness_rows[t - 1]["hash"], \
            f"shim diverged from the server ladder at tick {t}"


def test_canonical_state_text_is_pinned():
    """Golden canonical form — any drift in field order/content breaks both
    engines' agreement contract (the .gd twin formats the same lines)."""
    from mag.water_graph import WaterGraph
    g = WaterGraph()
    g.add_node("b", elev=2, kind="xor", sill=0, volume=3, )
    g.add_node("a", elev=5, kind="plain", volume=1)
    g.add_pipe("p2", "a", "b", cap=2, siphon=True, crest=3)
    g.add_pipe("p1", "b", "a", cap=1, open_=False, stress=7)
    g.tick_count = 9
    text = canonical_state_text(g.tick_count, g.nodes, g.pipes)
    assert text == (
        "t=9\n"
        "N|a|5|plain|0|1|0\n"
        "N|b|2|xor|0|3|0\n"
        "P|p1|b|a|1|0|2|0|0|7|0\n"
        "P|p2|a|b|2|1|3|0|1|0|0")


# ----------------------------------------------- hydrology family (Q02) ----

def _hydro(doc):
    return [s for s in doc["sequences"] if s["family"] == "hydrology"]


def test_hydrology_family_mix_shape_and_domain():
    """Q02 (2026-10-01): the graded-head family rides every corpus, rotates
    all four divergence shapes (the receipt-variant pattern), stamps
    conductance + cross_sections, and stays inside the small-volume domain —
    the int64 ceiling is the stress family's subject; the gradient law is
    this one's."""
    doc = generate(PROFILES["full"]["seed"], PROFILES["full"]["n"],
                   PROFILES["full"]["ticks"])
    hs = _hydro(doc)
    assert len(hs) == 6
    assert {s["shape"] for s in hs} == set(HYDRO_SHAPES)
    for s in hs:
        assert s["conductance"] in (2, 4, 8, 16)
        assert any("cross_section" in n for n in s["nodes"])
        for n in s["nodes"]:
            assert n.get("cross_section", 1000) >= 1
            assert n["volume"] <= 1000, "hydrology stays small-volume"
    quick = generate(PROFILES["quick"]["seed"], PROFILES["quick"]["n"],
                     PROFILES["quick"]["ticks"])
    assert _hydro(quick), "quick must touch the graded law too"


def test_hydrology_rows_are_graded_not_boolean():
    """The routing law: hydrology sequences must run through the GRADED
    oracle (mag.hydrology.HydrologyGraph), never silently fall to the
    boolean engine — a fallthrough would freeze the WRONG law as the
    twin's target. Replay every hydrology sequence through a boolean
    HarnessWorld (same frames, cross_section unread) and require the hash
    streams to diverge on at least one tick per sequence: each shape's
    board is engineered to part ways with the boolean verdict."""
    doc = generate(PROFILES["full"]["seed"], PROFILES["full"]["n"],
                   PROFILES["full"]["ticks"])
    hs = _hydro(doc)
    assert len(hs) >= 4
    graded = {(r["seq"], r["tick"]): r["hash"]
              for r in run_python(doc) if r["family"] == "hydrology"}
    bool_doc = {"schema": doc["schema"], "verbs": doc["verbs"],
                "max_say": doc["max_say"],
                "sequences": [{**s, "family": "boolean_probe"} for s in hs]}
    bool_rows = run_python(bool_doc)
    by_seq: dict[str, set[int]] = {s["id"]: set() for s in hs}
    for r in bool_rows:
        if graded[(r["seq"], r["tick"])] != r["hash"]:
            by_seq[r["seq"]].add(r["tick"])
    for s in hs:
        assert by_seq[s["id"]], \
            f"{s['id']} ({s['shape']}) never diverged from the boolean law"


def test_graded_law_diverges_from_boolean_both_directions():
    """THE Q02 GAP, PINNED THROUGH THE HARNESS: before the hydrology family,
    no parity input could distinguish the graded-head law from the boolean
    verdict law in EITHER direction. Crafted boards, zero actions, one tick:
      backwater — boolean pours (elev drop), graded refuses (dst head
                  higher): the drowned inlet.
      head_hill — boolean refuses (uphill in elevation), graded pours
                  (src head higher despite the lower elevation).
    """
    verbs = ("say", "whisper", "join", "boil", "valve", "tag")

    def one_tick(board):
        out = {}
        for graded in (False, True):
            seq = {"id": "b", "family": "hydrology", "ticks": 1,
                   "sids": ["s1"], "nodes": board,
                   "pipes": [{"name": "p", "src": board[0]["name"],
                              "dst": board[1]["name"], "cap": 5,
                              "siphon": False, "crest": 2, "open": True}],
                   "frames": [[]]}
            w = HarnessWorld(seq, verbs, graded=graded)
            out[graded] = w.tick_frame([], tick_no=1)
        return out

    backwater = one_tick([
        {"name": "hi", "elev": 6, "kind": "plain", "sill": 0, "volume": 40,
         "cross_section": 4000},     # depth 10  -> head 1546
        {"name": "lo", "elev": 2, "kind": "plain", "sill": 0, "volume": 300,
         "cross_section": 200},      # depth 1500 -> head 2012
    ])
    assert backwater[False]["hash"] != backwater[True]["hash"]
    assert backwater[True]["state"]["nodes"]["hi"]["volume"] == 40   # frozen
    assert backwater[False]["state"]["nodes"]["hi"]["volume"] == 35  # poured 5

    head_hill = one_tick([
        {"name": "lo", "elev": 2, "kind": "plain", "sill": 0, "volume": 400,
         "cross_section": 200},      # depth 2000 -> head 2512
        {"name": "hi", "elev": 5, "kind": "plain", "sill": 0, "volume": 0,
         "cross_section": 4000},     # head 1280
    ])
    assert head_hill[False]["hash"] != head_hill[True]["hash"]
    assert head_hill[True]["state"]["nodes"]["hi"]["volume"] > 0    # uphill pour
    assert head_hill[False]["state"]["nodes"]["hi"]["volume"] == 0  # boolean: no


def test_cross_section_variance_changes_graded_flux():
    """Same elevations, same src volume — ONLY the dst geometry differs,
    and the graded law yields three different fluxes (11 free pour into an
    empty wide basin, 8 throttled into a half-full equal-shape pool, 0
    stalled by a narrow pre-filled one) while the boolean law pours all
    three identically: geometry is invisible to the verdict engine."""
    verbs = ("say", "whisper", "join", "boil", "valve", "tag")
    src = {"name": "s", "elev": 4, "kind": "plain", "sill": 0,
           "volume": 100, "cross_section": 1000}      # head 1124
    dsts = [
        {"name": "d", "elev": 3, "kind": "plain", "sill": 0, "volume": 0,
         "cross_section": 4000},    # head 768  -> dHead 356 -> flow 11
        {"name": "d", "elev": 3, "kind": "plain", "sill": 0, "volume": 96,
         "cross_section": 1000},    # head 864  -> dHead 260 -> flow 8
        {"name": "d", "elev": 3, "kind": "plain", "sill": 0, "volume": 40,
         "cross_section": 100},     # head 1168 -> dHead -44 -> flow 0
    ]
    graded_flux, boolean_flux = [], []
    for dst in dsts:
        seq = {"id": "b", "family": "hydrology", "ticks": 1, "sids": ["s1"],
               "nodes": [src, dst],
               "pipes": [{"name": "p", "src": "s", "dst": "d", "cap": 100,
                          "siphon": False, "crest": 2, "open": True}],
               "frames": [[]]}
        row_g = HarnessWorld(seq, verbs, graded=True).tick_frame([], tick_no=1)
        row_b = HarnessWorld(seq, verbs, graded=False).tick_frame([], tick_no=1)
        graded_flux.append(row_g["state"]["nodes"]["d"]["volume"] - dst["volume"])
        boolean_flux.append(row_b["state"]["nodes"]["d"]["volume"] - dst["volume"])
    assert graded_flux == [11, 8, 0], graded_flux
    assert boolean_flux == [100, 100, 100], boolean_flux


def test_hydrology_python_side_is_the_hydrology_module():
    """The freeze's source of truth: HarnessWorld(graded=True) per-tick
    hashes must equal a DIRECT mag.hydrology.HydrologyGraph replay of the
    same board with no actions (pure physics, ladder out of the way) — the
    same faithfulness law the mountain family pins against the server. A
    re-typed shim here would freeze a fork, not the oracle."""
    from mag.hydrology import HydrologyGraph
    doc = generate(PROFILES["full"]["seed"], PROFILES["full"]["n"],
                   PROFILES["full"]["ticks"])
    seq = next(s for s in _hydro(doc) if s["shape"] == "cascade")
    quiet = {**seq, "frames": [[] for _ in seq["frames"]]}
    rows = run_python({"schema": doc["schema"], "verbs": doc["verbs"],
                       "max_say": doc["max_say"], "sequences": [quiet]})
    g = HydrologyGraph(conductance=seq["conductance"])
    for n in quiet["nodes"]:
        g.add_node(n["name"], elev=n["elev"], kind=n["kind"],
                   sill=n.get("sill", 0), volume=n.get("volume", 0),
                   cross_section=n.get("cross_section", 1000))
    for p in quiet["pipes"]:
        g.add_pipe(p["name"], p["src"], p["dst"], cap=p.get("cap", 1),
                   siphon=bool(p.get("siphon", False)),
                   crest=int(p.get("crest", 2)),
                   open_=bool(p.get("open", True)))
    for t in range(1, len(quiet["frames"]) + 1):
        g.tick()
        assert state_hash(g) == rows[t - 1]["hash"], f"tick {t}"


def test_hydrology_oracle_rows_are_byte_reproducible():
    """The frozen-oracle contract: two independent oracle runs over the
    same hydrology sequences must be byte-identical (cmd_all asserts this
    at freeze time; this pins the property at the source)."""
    doc = generate(seed=77, n=20, ticks=30)
    hs = _hydro(doc)
    assert hs
    sub = {"schema": doc["schema"], "verbs": doc["verbs"],
           "max_say": doc["max_say"], "sequences": hs}
    first = json.dumps(run_python(sub), sort_keys=True)
    second = json.dumps(run_python(sub), sort_keys=True)
    assert first == second


# ---------------------------------------------------------- compare law ----

def _row(seq, tick, hash_, verdicts):
    return {"seq": seq, "family": "x", "tick": tick, "hash": hash_,
            "verdicts": verdicts,
            "state": {"tick": tick, "nodes": {}, "pipes": {}}}


def test_compare_parity_on_identical_rows():
    rows = [_row("s", 1, "a" * 64, ["ack"]), _row("s", 2, "b" * 64, [])]
    report = compare(rows, [dict(r) for r in rows])
    assert report["parity"] is True
    assert report["first_divergence"] is None


def test_compare_finds_first_divergent_tick_with_both_hashes():
    py = [_row("s", 1, "a" * 64, []), _row("s", 2, "b" * 64, []),
          _row("s", 3, "c" * 64, [])]
    gd = [_row("s", 1, "a" * 64, []), _row("s", 2, "d" * 64, []),
          _row("s", 3, "e" * 64, [])]
    report = compare(py, gd)
    assert report["parity"] is False
    fd = report["first_divergence"]
    assert fd["tick"] == 2 and fd["kind"] == "state_hash"
    assert fd["hash_py"] == "b" * 64 and fd["hash_gd"] == "d" * 64


def test_compare_catches_verdict_divergence_with_same_hash():
    py = [_row("s", 1, "a" * 64, ["ack"])]
    gd = [_row("s", 1, "a" * 64, ["reject:DRY_POOL"])]
    fd = compare(py, gd)["first_divergence"]
    assert fd["kind"] == "verdicts"
    assert fd["verdicts_py"] == ["ack"] and fd["verdicts_gd"] == ["reject:DRY_POOL"]


def test_compare_catches_missing_godot_rows():
    py = [_row("s", 1, "a" * 64, []), _row("s", 2, "b" * 64, [])]
    gd = [_row("s", 1, "a" * 64, [])]
    report = compare(py, gd)
    assert report["parity"] is False
    assert report["first_divergence"]["kind"] == "missing_on_godot_side"
    assert report["first_divergence"]["tick"] == 2


# ------------------------------------------------------- end-to-end law ----

@pytest.mark.skipif(not GODOT_EXE.exists(), reason="godot binary not present")
def test_end_to_end_report_verdict_matches_rows(tmp_path: Path):
    """Run BOTH engines on a small seeded corpus. The asserted law: the
    comparator's verdict agrees with a direct row-by-row hash equality
    check — the instrument checks itself. (Whether parity HOLDS is the
    measurement, pinned in the receipt, not in this test.)"""
    from tools.rule_parity import run_godot
    doc = generate(seed=42, n=6, ticks=12)
    inp = tmp_path / "in.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    py_rows = run_python(doc)
    gd_path = tmp_path / "gd.jsonl"
    run_godot(inp, gd_path)
    gd_rows = [json.loads(x) for x in
               gd_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(gd_rows) == len(py_rows)
    report = compare(py_rows, gd_rows)
    direct = all(p["hash"] == g["hash"] and p["verdicts"] == g["verdicts"]
                 for p, g in zip(py_rows, gd_rows))
    assert report["parity"] == direct
    if not direct:
        fd = report["first_divergence"]
        assert fd["tick"] >= 1 and fd["hash_py"] != fd["hash_gd"]
