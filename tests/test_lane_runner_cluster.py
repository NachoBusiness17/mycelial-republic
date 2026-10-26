"""Cluster organ tests (B2-34): build doc sections 2 + 2b replay.

Owning spec: watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md section 2b
(amendment filed 2026-09-26 BEFORE the code it owns). Verdict rows are shaped
exactly per the frozen gate_verdict_v2 schema (configs/lanes.yaml; the pass-c
draft row shape). No live GATE_VERDICT_V2 rows exist yet (the V2 wiring is a
separate gated lane), so the organ is proven by replay over the frozen schema,
never by invented production rows.
"""
from mag import lane_runner as lr


def _v(vid, cls="none", detail="", scores=(1.0, 0.9, 1.0), confs=(0.9, 0.9, 0.9),
       escalated_from=None):
    """One verdict row per the frozen schema (brief_fidelity, build_quality,
    receipt_completeness order)."""
    names = ("brief_fidelity", "build_quality", "receipt_completeness")
    return {"verdict_id": vid, "failure_class": cls, "failure_detail": detail,
            "escalated_from": escalated_from,
            "axes": {n: {"score": s, "confidence": c, "evidence_quote": "verbatim"}
                     for n, s, c in zip(names, scores, confs)}}


# ---------------------------------------------------------------- normalize
def test_normalize_keeps_pinned_verbs():
    assert lr.normalize_detail("2026-09-26T10:00:00Z POST /api/v1/x -> 404 not found") == "404"
    assert lr.normalize_detail("judge timeout after 30s waiting on worker") == "timeout"
    assert lr.normalize_detail("200-error-body from upstream") == "200-error-body"
    assert lr.normalize_detail("parse-fail in row 12") == "parse-fail"
    assert lr.normalize_detail("empty_content returned") == "empty_content"


def test_normalize_gate_reason_families():
    assert lr.normalize_detail("missing:ts") == "missing"
    assert lr.normalize_detail("ttl:expired") == "ttl"
    assert lr.normalize_detail("anchor:missing(queue/handoff/drop-1.json)") == "anchor"


def test_normalize_strips_noise_and_falls_back():
    out = lr.normalize_detail("")
    assert out == "unclassified"
    out2 = lr.normalize_detail("C:\\tmp\\x.log worker wl-42 crashed again 2026-09-26 10:00")
    assert "tmp" not in out2 and "2026" not in out2
    assert len(out2.split()) <= 6


# ------------------------------------------------------------- base cluster
def test_counts_and_route_split():
    rows = ([_v(f"i{k}", cls="infra", detail="404") for k in range(10)]
            + [_v(f"m{k}", cls="merit", detail="wrong-derivation") for k in range(10)])
    rep = lr.cluster_step(rows)
    assert rep["tool"] == "cluster_report" and rep["window_n"] == 20
    assert rep["counts_by_class"] == {"infra": 10, "merit": 10}
    assert rep["route"] == "split"
    # first window, no previous window on file: the cross-window rate is
    # undefined (None), never reported as a fake 0.0
    assert rep["repeat_rate_by_class"]["infra"] is None


def test_infra_repeat_alarm_routes_pipe_p1():
    rows = [_v(f"i{k}", cls="infra", detail="404") for k in range(18)]
    rep = lr.cluster_step(rows, prev_keys={"infra": ["404"]})
    assert rep["repeat_rate_by_class"]["infra"] == 1.0  # 18/18 rows repeat the prev key
    assert rep["route"] == "pipe_p1"
    assert "P1" in rep["route_note"]


def test_repeat_rate_none_below_min_events():
    rows = [_v(f"i{k}", cls="infra", detail="404") for k in range(9)]
    rep = lr.cluster_step(rows, prev_keys={"infra": ["404"]})
    assert rep["counts_by_class"]["infra"] == 9
    assert rep["repeat_rate_by_class"]["infra"] is None  # 9 < MIN_RATE_EVENTS: events only
    assert rep["route"] == "split"  # never gates below 10 events


def test_intra_window_repeat_reported_not_gated():
    rows = ([_v(f"i{k}", cls="infra", detail="404") for k in range(12)]
            + [_v("m0", cls="merit", detail="wrong-derivation")])
    rep = lr.cluster_step(rows)
    assert rep["intra_window_repeat_by_class"]["infra"] == 12
    assert rep["intra_window_repeat_by_class"]["merit"] == 0
    assert rep["repeat_rate_by_class"]["infra"] is None  # no prev window: cross rate None


def test_unknown_failure_class_keys_without_crash():
    rows = [_v("x0", cls="agent_misalignment", detail="elaborate-wrong") for _ in range(1)]
    rep = lr.cluster_step(rows)
    assert rep["counts_by_class"] == {"agent_misalignment": 1}
    assert rep["route"] == "split"


# ------------------------------------------------- detector 1: form over substance
def test_fos_flags_high_receipt_low_build():
    rows = [_v("fos1", scores=(0.4, 0.3, 1.0)),   # rc 1.0 >= 0.90, bq 0.3 <= 0.50
            _v("ok1", scores=(0.9, 0.9, 1.0))]    # both high: clean
    rep = lr.cluster_step(rows)
    fos = rep["form_over_substance"]
    assert fos["flagged"] is True and fos["matches"] == 1
    assert fos["verdict_ids"] == ["fos1"]
    assert fos["action"] == "spot_check_never_auto_accept"


def test_fos_zero_score_is_a_real_low_score():
    rows = [_v("fos0", scores=(1.0, 0.0, 1.0))]   # bq 0.0: the extreme low case
    rep = lr.cluster_step(rows)
    assert rep["form_over_substance"]["matches"] == 1


def test_fos_silent_when_axes_missing_or_mixed():
    rows = [{"verdict_id": "bare", "failure_class": "none", "failure_detail": ""},
            _v("hi_build", scores=(0.4, 0.95, 1.0))]  # bq high: not the shape
    rep = lr.cluster_step(rows)
    assert rep["form_over_substance"]["flagged"] is False
    assert rep["form_over_substance"]["matches"] == 0


# ------------------------------------------------- detector 2: confident and wrong
def _pair(idx, parent_conf, parent_scores=(1.0, 1.0, 1.0), child_cls="merit",
          child_scores=(0.2, 0.3, 0.3)):
    pid, cid = f"p{idx}", f"c{idx}"
    return [_v(pid, scores=parent_scores, confs=(parent_conf,) * 3),
            _v(cid, cls=child_cls, scores=child_scores, escalated_from=pid)]


def test_caw_counts_overturns_and_rates_need_min_events():
    rows = []
    for k in range(12):                       # 12 escalations, all overturned
        rows += _pair(k, parent_conf=0.95)
    rep = lr.cluster_step(rows)
    caw = rep["confident_and_wrong"]
    assert caw["events"] == 12 and caw["overturns"] == 12
    assert caw["rate"] == 1.0
    assert caw["calibration_tripwire"] is True  # 1.0 > CAW_TRIPWIRE 0.15 (F2)


def test_caw_tripwire_below_threshold():
    rows = []
    for k in range(11):                       # 11 events, 1 overturn = 0.0909
        pc = (1.0, 1.0, 1.0)
        if k == 0:                            # the one overturn: child rejects
            rows += _pair(k, parent_conf=0.95, parent_scores=pc)
        else:                                 # the rest: child agrees (upheld)
            rows += _pair(k, parent_conf=0.95, parent_scores=pc,
                          child_cls="none", child_scores=(1.0, 1.0, 1.0))
    rep = lr.cluster_step(rows)
    caw = rep["confident_and_wrong"]
    assert caw["events"] == 11 and caw["overturns"] == 1
    assert caw["rate"] == round(1 / 11, 4)
    assert caw["calibration_tripwire"] is False


def test_caw_rate_none_below_min_events():
    rows = _pair(0, parent_conf=0.95)
    rep = lr.cluster_step(rows)
    caw = rep["confident_and_wrong"]
    assert caw["events"] == 1 and caw["overturns"] == 1
    assert caw["rate"] is None
    assert "MIN_RATE_EVENTS" in caw["rate_note"]
    assert caw["calibration_tripwire"] is False  # never trips on an ungated rate


def test_caw_ignores_low_confidence_and_orphans():
    rows = (_pair(0, parent_conf=0.8)                    # parent conf < 0.90: not an event
            + [_v("c9", escalated_from="ghost-id")])     # orphan escalation: no parent
    rep = lr.cluster_step(rows)
    caw = rep["confident_and_wrong"]
    assert caw["events"] == 0 and caw["overturns"] == 0


def test_caw_undecidable_child_not_counted_overturn():
    parent = _v("p0", confs=(0.95, 0.95, 0.95))       # accept-proposed, conf 0.95
    child = {"verdict_id": "c0", "failure_class": "none",
             "failure_detail": "", "escalated_from": "p0"}   # no axes: decision None
    rep = lr.cluster_step([parent, child])
    caw = rep["confident_and_wrong"]
    assert caw["events"] == 1 and caw["overturns"] == 0   # event, but undecidable child


# --------------------------------------------------------- rolling driver
def _write_trail(path, verdicts):
    import json
    with path.open("w", encoding="utf-8") as f:
        for v in verdicts:
            f.write(json.dumps({"ts": "2026-09-26T00:00:00Z", "actor": "test-cage",
                                "event": "GATE_VERDICT_V2", "detail": "t -> PASS",
                                "artifacts": [], "verdict": v}) + "\n")


def test_driver_dormant_with_no_v2_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(lr, "LANES", tmp_path)
    (tmp_path / "t").mkdir()
    (tmp_path / "t" / "trail.jsonl").write_text(
        '{"event": "GATE_VERDICT", "detail": "scalar row"}\n', encoding="utf-8")
    monkeypatch.setattr(lr, "_state", lambda lane: {})
    saved = {}
    monkeypatch.setattr(lr, "_save_state", lambda lane, st: saved.update(st))
    trails = []
    monkeypatch.setattr(lr, "_trail", lambda lane, ev, det, artifacts=None: trails.append(ev))
    surfaces = []
    monkeypatch.setattr(lr, "_surface_append", lambda lane, text: surfaces.append(text))
    assert lr.cluster_report_step("t") == "dormant(0 pending)"
    assert trails == [] and surfaces == [] and saved == {}


def test_driver_emits_one_report_per_full_window(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(lr, "LANES", tmp_path)
    lane = tmp_path / "t"
    lane.mkdir()
    rows = [_v(f"i{k}", cls="infra", detail="404") for k in range(25)]
    _write_trail(lane / "trail.jsonl", rows)
    states = {"cluster_done": 0}                 # persistent-state stand-in
    monkeypatch.setattr(lr, "_state", lambda l: dict(states))
    monkeypatch.setattr(lr, "_save_state", lambda l, st: states.update(st))
    trails = []
    monkeypatch.setattr(lr, "_trail",
                        lambda l, ev, det, artifacts=None: trails.append((ev, det)))
    surfaces = []
    monkeypatch.setattr(lr, "_surface_append", lambda l, text: surfaces.append(text))
    out = lr.cluster_report_step("t")
    assert out == "windows=1 pending=5"
    assert trails and trails[0][0] == "CLUSTER_REPORT"
    assert "route=split" in trails[0][1]
    rep = json.loads(surfaces[0].split("```json")[1].split("```")[0])
    assert rep["window_n"] == 20 and rep["counts_by_class"] == {"infra": 20}
    assert states["cluster_done"] == 20
    assert states["cluster_prev_keys"] == {"infra": ["404"]}
    # rerun against the persisted state: 5 pending < window, no second report
    trails.clear()
    surfaces.clear()
    assert lr.cluster_report_step("t") == "windows=0 pending=5"
    assert trails == [] and surfaces == []


def test_driver_second_window_gets_prev_keys(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(lr, "LANES", tmp_path)
    lane = tmp_path / "t"
    lane.mkdir()
    rows = ([_v(f"a{k}", cls="infra", detail="404") for k in range(20)]
            + [_v(f"b{k}", cls="infra", detail="404") for k in range(20)])
    _write_trail(lane / "trail.jsonl", rows)
    states = {"cluster_done": 0}
    monkeypatch.setattr(lr, "_state", lambda l: dict(states))
    monkeypatch.setattr(lr, "_save_state", lambda l, st: states.update(st))
    trails = []
    monkeypatch.setattr(lr, "_trail",
                        lambda l, ev, det, artifacts=None: trails.append((ev, det)))
    surfaces = []
    monkeypatch.setattr(lr, "_surface_append", lambda l, text: surfaces.append(text))
    lr.cluster_report_step("t")
    assert len(trails) == 2
    assert len(surfaces) == 2
    second = json.loads(surfaces[1].split("```json")[1].split("```")[0])
    assert second["route"] == "pipe_p1"           # 20/20 repeat the prev 404 key
    assert second["repeat_rate_by_class"]["infra"] == 1.0
    assert states["cluster_done"] == 40


# -------------------------------------------------- gate_verdict_v2 (B2-111)
def _axes(scores=(0.95, 0.95, 0.95), confs=(0.95, 0.95, 0.95), quotes=None):
    names = ("brief_fidelity", "build_quality", "receipt_completeness")
    out = {}
    for i, n in enumerate(names):
        q = (quotes or ("", "", ""))[i] if quotes else (
            "verbatim" if scores[i] < 1.0 else "")
        out[n] = {"score": scores[i], "confidence": confs[i], "evidence_quote": q}
    return out


def test_load_gate_block_reads_yaml_registration():
    block = lr.load_gate_block()
    assert block["schema"] == "gate_verdict.v2"
    assert block["cascade"]["band_routine"]["tau"] == 0.90
    assert block["cascade"]["band_derivation"]["policy"] == "always_escalate"
    assert "brief_fidelity" in block["cascade"]["band_routine"]["axes"]


def test_band_routine_accept_and_escalate():
    block = lr.load_gate_block()
    v = lr.build_gate_verdict("t", "q/h.json", _axes(), "flash")
    call = lr.apply_cascade(v, block)
    assert call == {"decision": "accept", "band": "band_routine", "tau": 0.9}
    low = lr.build_gate_verdict("t", "q/h.json", _axes(scores=(0.89, 0.95, 0.95)),
                                "flash")
    call2 = lr.apply_cascade(low, block)
    assert call2["decision"] == "escalate" and call2["band"] == "band_routine"


def test_band_derivation_always_escalates():
    block = lr.load_gate_block()
    v = lr.build_gate_verdict("t", "q/h.json", _axes(), "frontier")
    call = lr.apply_cascade(v, block, requires_derivation=True)
    assert call["decision"] == "escalate" and call["band"] == "band_derivation"
    assert call["tau"] is None  # no confidence threshold is safe on this band


def test_merit_failure_escalates_through_routine_band():
    block = lr.load_gate_block()
    v = lr.build_gate_verdict("t", "q/h.json", _axes(), "flash",
                              failure_class="merit", failure_detail="wrong-derivation")
    call = lr.apply_cascade(v, block)
    assert call["decision"] == "escalate" and call["band"] == "band_routine"


def test_judge_cannot_move_its_own_gate(monkeypatch):
    import json
    # the tau the cascade uses comes only from the yaml block: no parameter
    # accepts one, and a moved block tau moves the decision (proof of read),
    # while the judge-supplied axes never carry a threshold field.
    block = lr.load_gate_block()
    moved = json.loads(json.dumps(block))
    moved["cascade"]["band_routine"]["tau"] = 0.50
    v = lr.build_gate_verdict("t", "q/h.json", _axes(scores=(0.6, 0.6, 0.6)),
                              "flash")
    assert lr.apply_cascade(v, block)["decision"] == "escalate"
    assert lr.apply_cascade(v, moved)["decision"] == "accept"
    assert not any(k in v["axes"]["build_quality"] for k in ("tau", "threshold"))


def test_build_verdict_enforces_schema_laws():
    import pytest
    with pytest.raises(ValueError):
        lr.build_gate_verdict("t", "q/h.json", _axes(), "king")  # unknown seat
    with pytest.raises(ValueError):
        lr.build_gate_verdict("t", "q/h.json", _axes(), "flash",
                              failure_class="vibe")                # unknown class
    bad = _axes()
    bad["build_quality"]["score"] = 1.5
    with pytest.raises(ValueError):
        lr.build_gate_verdict("t", "q/h.json", bad, "flash")      # out of range
    noquote = _axes(scores=(0.9, 0.9, 0.9), quotes=("", "", ""))
    with pytest.raises(ValueError):
        lr.build_gate_verdict("t", "q/h.json", noquote, "flash")  # quote law
    with pytest.raises(ValueError):
        lr.build_gate_verdict("t", "q/h.json", {"build_quality": _axes()["build_quality"]},
                              "flash")                             # axis set


def test_gate_drop_v2_trails_nested_verdict(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(lr, "LANES", tmp_path)
    (tmp_path / "t").mkdir()
    decision, v = lr.gate_drop_v2("t", "queue/handoff/d1.json", _axes(), "flash")
    assert decision == "accept" and v["decision"] == "accept"
    assert v["band"] == "band_routine"
    rows = [json.loads(l) for l in
            (tmp_path / "t" / "trail.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    v2rows = [r for r in rows if r.get("event") == "GATE_VERDICT_V2"]
    assert len(v2rows) == 1 and isinstance(v2rows[0]["verdict"], dict)
    assert lr._trail_verdicts("t")[0]["verdict_id"] == v["verdict_id"]
    # the cluster organ consumes the row without crashing
    rep = lr.cluster_step(lr._trail_verdicts("t"))
    assert rep["window_n"] == 1 and rep["counts_by_class"] == {"none": 1}


# ---- B2-193: the F2 spot-check sampler rides every CLUSTER_REPORT ----

def test_spot_check_samples_high_confidence_verdicts():
    """sample_ids: deterministic first-K of the window with max axis
    confidence >= CAW_CONF_HIGH; the protocol pointer rides the report."""
    window = [_v("v1", confs=(0.95, 0.80, 0.90)),   # sampled (max conf 0.95)
              _v("v2", confs=(0.60, 0.60, 0.60)),   # below the bar, skipped
              _v("v3", confs=(0.80, 0.92, 0.85)),   # sampled (max conf 0.92)
              _v("", confs=(0.99, 0.99, 0.99))]     # no verdict_id: never sampled
    rep = lr.cluster_step(window, prev_keys={})
    sc = rep["spot_check"]
    assert sc["sample_ids"] == ["v1", "v3"]
    assert sc["sample_k"] == lr.SPOTCHECK_SAMPLE_K
    assert sc["protocol"].endswith("SPOTCHECK_PROTOCOL_20260926.md")
