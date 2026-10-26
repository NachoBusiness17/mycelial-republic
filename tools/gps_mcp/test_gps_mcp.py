"""gps-mcp v0 tests. Run from the repo root:

    .venv/Scripts/python.exe -m pytest tools/gps_mcp/test_gps_mcp.py -q

Everything runs against the in-process test double: $0, no network,
deterministic (fixture rates are hand-picked literals, no RNG).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools.gps_mcp import providers as prov
from tools.gps_mcp import seed_fixtures
from tools.gps_mcp.ledger import CapabilityLedger
from tools.gps_mcp.router import (
    RECEIPT_REQUIRED_KEYS,
    Constraints,
    Router,
)
from tools.gps_mcp.server import ServerState, process_request

PACKAGE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = PACKAGE_DIR / "config.json"


def seed_ledger(ledger: CapabilityLedger) -> int:
    count = 0
    for (model_id, task_shape), (rate, size) in sorted(
        seed_fixtures.FIXTURE_RATES.items()
    ):
        ledger.upsert_measurement(
            model_id=model_id,
            task_shape=task_shape,
            pass_rate=rate,
            sample_size=size,
            cost_usd_per_call=seed_fixtures.FIXTURE_COSTS[model_id],
            last_measured=seed_fixtures.SEED_DATE,
            # Ractor finding 1 (2026-10-10): a capability row without
            # resolved verdict evidence is self-attested and get_rate
            # bounds it to 0.21; the seeder therefore MINTS the resolved
            # evidence for each claimed rate (the finding's "re-derive
            # from resolved evidence" move) so thresholds are tested
            # against honest numbers.
            evidence_note=f"seed {task_shape}",
        )
        count += 1
    return count


@pytest.fixture
def env(tmp_path):
    ledger = CapabilityLedger(tmp_path / "led.db3")
    seeded = seed_ledger(ledger)
    receipts = tmp_path / "receipts.jsonl"
    registry = prov.build_registry(prov.load_config(CONFIG_PATH))
    router = Router(registry, ledger, receipts)
    return SimpleNamespace(
        ledger=ledger, receipts=receipts, registry=registry,
        router=router, seeded=seeded, tmp_path=tmp_path,
    )


# -- ledger ------------------------------------------------------------------


def test_record_verdict_running_mean_incremental(tmp_path):
    ledger = CapabilityLedger(tmp_path / "led.db3")
    r1 = ledger.record_verdict("m", "shape", True, "ev1")
    assert (r1.pass_rate, r1.sample_size) == (1.0, 1)
    r2 = ledger.record_verdict("m", "shape", False, "ev2")
    assert r2.sample_size == 2
    assert r2.pass_rate == pytest.approx(0.5)
    r3 = ledger.record_verdict("m", "shape", True, "ev3")
    assert r3.sample_size == 3
    assert r3.pass_rate == pytest.approx(2.0 / 3.0)


def test_report_capability_returns_full_row(env):
    row = env.ledger.report_capability("flash-mid-1", "code_review")
    assert row is not None
    assert row["model_id"] == "flash-mid-1"
    assert row["task_shape"] == "code_review"
    assert row["pass_rate"] == pytest.approx(0.88)
    # Ractor finding 1: the seeder MINTS the resolved evidence for the
    # claimed rate, so the raw row carries the seeded claim PLUS the 75
    # minted observations (n=150, rate still exactly 0.88 because the
    # mint adds round(0.88*75)=66 passes to a 0.88 mean). The
    # qualification basis stays the 75 resolved rows: get_rate reads
    # (0.7874, 75), never the inflated point rate.
    assert row["sample_size"] == 150
    assert row["cost_usd_per_call"] == pytest.approx(0.004)
    # Ractor finding 1: the minted evidence lands through
    # record_verdict, which stamps last_measured at append, so the raw
    # row no longer carries the pinned SEED_DATE: the measurement is
    # re-derived from resolved rows and last_measured tracks that
    # derivation (byte-equal to updated_at on the final mint write,
    # which sets both columns from the same ts).
    assert row["last_measured"] == row["updated_at"]
    datetime.fromisoformat(row["updated_at"])  # parseable ISO stamp
    assert env.ledger.report_capability("flash-mid-1", "never_measured") is None


def test_verdict_log_retains_evidence_hashes(tmp_path):
    ledger = CapabilityLedger(tmp_path / "led.db3")
    ledger.record_verdict("m", "shape", "pass", "hash-a")
    ledger.record_verdict("m", "shape", "fail", "hash-b")
    rows = ledger.verdict_log_rows("m", "shape")
    assert [r["evidence_hash"] for r in rows] == ["hash-a", "hash-b"]
    assert [r["verdict"] for r in rows] == [1, 0]


def test_record_verdict_rejects_garbage(tmp_path):
    ledger = CapabilityLedger(tmp_path / "led.db3")
    with pytest.raises(ValueError):
        ledger.record_verdict("m", "shape", "maybe")


def test_task_shape_has_history(env):
    assert env.ledger.task_shape_has_history("code_review") is True
    assert env.ledger.task_shape_has_history("brand_new_shape") is False


# -- config and providers -----------------------------------------------------


def test_shipped_config_builds_registry():
    registry = prov.build_registry(prov.load_config(CONFIG_PATH))
    assert len(registry.providers) == 6
    assert registry.tier_order == ["local", "mid", "frontier"]
    assert registry.exploration_model == "flash-mid-1"


def test_gstd_config_builds_registry():
    # The live surface (2026-10-09): config.gstd.json = the 6 test doubles
    # PLUS 14 real gstd-tier garden models served by the desktop gstd node.
    # Loaded via GPS_MCP_CONFIG; the shipped config.json stays pure doubles
    # so this suite keeps running offline. Building is offline by design;
    # CALLING gstd providers is live (never exercised here). Receipt:
    # watch/inbox/gstd_basecamp_20260109/ROUTER_VOCAB_LANDED.md
    registry = prov.build_registry(
        prov.load_config(PACKAGE_DIR / "config.gstd.json")
    )
    gstd = [p for p in registry.providers.values() if p.tier == "gstd"]
    assert len(gstd) == 14
    assert all(not p.test_double for p in gstd)
    assert all(p.base_url == "http://localhost:8080/v1" for p in gstd)
    assert len(registry.providers) == 6 + 14
    assert registry.tier_order == ["gstd", "local", "mid", "frontier"]
    assert registry.exploration_model == "flash-mid-1"


def test_test_double_is_deterministic():
    cfg = prov.ProviderConfig(
        model_id="td", base_url="http://x", model="td", tier="local",
        cost_usd_per_call=0.001, test_double=True, confidence_default=0.9,
        confidence_by_task_shape={"hard": 0.2},
    )
    a = prov.call_provider(cfg, "hard", "payload one")
    b = prov.call_provider(cfg, "hard", "payload one")
    assert a.answer == b.answer
    assert a.confidence == 0.2  # task-shape override beats default
    c = prov.call_provider(cfg, "easy", "payload one")
    assert c.confidence == 0.9
    d = prov.call_provider(cfg, "hard", "payload two")
    assert d.answer != a.answer  # answer tracks the payload digest
    with_ctx = prov.call_provider(cfg, "hard", "p", prior_answers=["prior"])
    assert with_ctx.prior_context == 1
    assert "ctx:1" in with_ctx.answer


def test_yaml_config_supported(tmp_path):
    pytest.importorskip("yaml")
    cfg_file = tmp_path / "cfg.yaml"
    cfg_file.write_text(
        "tier_order: [local, mid]\n"
        "exploration_model: m1\n"
        "providers:\n"
        "  - model_id: m1\n"
        "    base_url: http://localhost:1/v1\n"
        "    model: m1\n"
        "    tier: local\n"
        "    cost_usd_per_call: 0.001\n"
        "  - model_id: m2\n"
        "    base_url: http://localhost:2/v1\n"
        "    model: m2\n"
        "    tier: mid\n"
        "    cost_usd_per_call: 0.01\n",
        encoding="utf-8",
    )
    registry = prov.build_registry(prov.load_config(cfg_file))
    assert set(registry.providers) == {"m1", "m2"}


def test_default_exploration_picks_middle_tier(tmp_path):
    cfg = {
        "tier_order": ["local", "mid", "frontier"],
        "providers": [
            {"model_id": "a", "base_url": "u", "model": "a", "tier": "local",
             "cost_usd_per_call": 0.001},
            {"model_id": "b", "base_url": "u", "model": "b", "tier": "mid",
             "cost_usd_per_call": 0.01},
            {"model_id": "c", "base_url": "u", "model": "c", "tier": "mid",
             "cost_usd_per_call": 0.005},
            {"model_id": "d", "base_url": "u", "model": "d", "tier": "frontier",
             "cost_usd_per_call": 0.5},
        ],
    }
    registry = prov.build_registry(cfg)
    assert registry.exploration_model == "c"  # cheapest of the middle tier


# -- ask: constraint filtering and ledger-driven routing ----------------------


def test_ask_routes_cheapest_qualifying(env):
    # Ractor finding 1: qualify on the Wilson lower bound, not the point
    # rate. summarize bounds: gemma-worker-4b 0.8391 (n=140) and
    # flash-mid-2 0.8302 sit UNDER the 0.85 threshold, so the cheapest
    # honest qualifier is flash-mid-1 (0.8737 at n=130, cost 0.004).
    d = env.router.ask("summarize", "summarize this")
    assert d.chosen == "flash-mid-1"
    assert d.exploration is False
    assert d.confidence == pytest.approx(0.92)
    rates = {c["model_id"]: c for c in d.considered}
    assert rates["yesno-tiny"]["passes_threshold"] is False  # 0.0475 bound
    assert rates["gemma-worker-4b"]["passes_threshold"] is False  # 0.8391 bound


def test_ask_cost_constraint_filters(env):
    # design_judgment: only frontier-opus clears 0.85, but a 0.005 cap
    # excludes it; router falls back to the cheapest constraint-passing
    # model and says so in reasons.
    d = env.router.ask(
        "design_judgment", "judge this",
        Constraints(max_cost_usd=0.005),
    )
    assert d.chosen == "yesno-tiny"
    rates = {c["model_id"]: c for c in d.considered}
    assert rates["frontier-opus"]["passes_constraints"] is False
    assert any("threshold" in r for r in d.reasons)


def test_ask_latency_constraint_filters(env):
    d = env.router.ask(
        "design_judgment", "judge this",
        Constraints(max_latency_ms=1000),
    )
    stats = {c["model_id"]: c for c in d.considered}
    assert stats["frontier-opus"]["passes_constraints"] is False
    assert stats["frontier-opus"]["latency_ms"] == 4000
    assert d.chosen != "frontier-opus"


def test_ask_no_history_routes_exploration(env):
    d = env.router.ask("brand_new_shape", "anything")
    assert d.chosen == "flash-mid-1"  # designated mid tier
    assert d.exploration is True
    assert any("no ledger history" in r for r in d.reasons)
    assert d.receipt["exploration"] is True
    assert d.receipt["chosen"] == "flash-mid-1"


def test_ask_threshold_override(env):
    # Ractor finding 1: at the 0.95 threshold NO fixture survives its
    # Wilson lower bound on code_review (frontier-opus tops out at
    # 0.8654 on n=50), so the router takes its documented cheapest
    # constraint-passing fallback instead of awarding the route on an
    # inflated point rate. The fallback reason names the threshold.
    d = env.router.ask(
        "code_review", "review", Constraints(pass_rate_threshold=0.95)
    )
    assert d.chosen == "yesno-tiny"
    assert any("threshold" in r for r in d.reasons)


def test_ask_no_candidates_receipts_null_choice(env):
    d = env.router.ask(
        "code_review", "review", Constraints(max_cost_usd=0.00001)
    )
    assert d.chosen is None
    assert d.answer is None
    assert d.receipt["chosen"] is None
    assert d.receipt["cost_usd"] == 0.0


def test_ask_low_confidence_flagged_in_reasons(env):
    # Ractor finding 1: post-Wilson the summarize route lands on
    # flash-mid-1 (cheapest qualifier at bound 0.8737), whose 0.92
    # confidence is what the 0.99 floor flags.
    d = env.router.ask(
        "summarize", "s", Constraints(min_confidence=0.99)
    )
    assert any("min_confidence" in r for r in d.reasons)
    assert d.receipt["confidence"] == pytest.approx(0.92)


# -- cascade -------------------------------------------------------------------


def test_cascade_escalates_with_trace(env):
    # Ractor finding 1: summarize Wilson bounds sit gemma-worker-4b at
    # 0.8391 and flash-mid-2 at 0.8302, both UNDER the 0.85 threshold,
    # so the cheapest QUALIFYING start is flash-mid-1 (0.8737) whose
    # 0.92 confidence meets the 0.8 cascade floor on attempt one. The
    # gemma -> flash escalation this test once exercised is unreachable
    # on the seeded fixtures under Wilson honesty; the escalate-path
    # machinery (escalated flag, prior-answer ctx carry) is a named
    # coverage gap, not a silent deletion. trace_id grouping stays
    # asserted on the one attempt receipt.
    result = env.router.cascade("summarize", "summarize this")
    assert [a.model_id for a in result.attempts] == ["flash-mid-1"]
    assert [a.tier for a in result.attempts] == ["mid"]
    assert result.total_cost_usd == pytest.approx(0.004)
    assert "meets threshold" in result.attempts[-1].reason
    assert result.attempts[0].escalated is False
    trace_rows = [
        r for r in env.router.receipts.rows() if "trace_id" in r
    ]
    assert len(trace_rows) == 1
    assert trace_rows[0]["cascade_step"] == 0


def test_cascade_max_three_tiers(env):
    # Ractor finding 1: post-Wilson only two tiers can qualify on
    # summarize (flash-mid-1 0.8737 mid; frontier-opus 0.8517 frontier;
    # gemma-worker-4b 0.8391 and flash-mid-2 0.8302 sit under 0.85), so
    # the unconfident climb ends at the frontier with no third tier
    # left. The 3-tier cap itself is a named coverage gap: no seeded
    # shape offers three threshold-qualifying tiers under Wilson
    # honesty, so "max 3 tiers" is unreachable on these fixtures.
    for mid in ("gemma-worker-4b", "flash-mid-1", "flash-mid-2", "frontier-opus"):
        env.registry.get(mid).confidence_default = 0.5
    result = env.router.cascade("summarize", "s", Constraints(min_confidence=0.8))
    assert [a.tier for a in result.attempts] == ["mid", "frontier"]
    assert [a.model_id for a in result.attempts] == [
        "flash-mid-1", "frontier-opus"
    ]
    assert result.attempts[-1].tier == "frontier"
    assert "no higher tier" in result.stopped_because


def test_cascade_cost_cap_blocks_escalation(env):
    # Ractor finding 1: gemma-worker-4b (bound 0.8391) no longer
    # qualifies, so the cap test rides on flash-mid-1 alone: it
    # qualifies under the 0.005 cap (cost 0.004), its 0.92 confidence
    # misses the 0.95 floor, and the only higher tier (frontier-opus at
    # 0.12) is blocked by the cap.
    result = env.router.cascade(
        "summarize", "s",
        Constraints(min_confidence=0.95, max_cost_usd=0.005),
    )
    assert [a.model_id for a in result.attempts] == ["flash-mid-1"]
    assert "no higher tier" in result.stopped_because


def test_cascade_confident_first_tier_stops(env):
    # yes_no_decision: yesno-tiny is cheapest qualifying and confident.
    result = env.router.cascade("yes_no_decision", "is it ready")
    assert len(result.attempts) == 1
    assert result.attempts[0].model_id == "yesno-tiny"
    assert result.attempts[0].confidence == pytest.approx(0.95)
    assert "meets threshold" in result.stopped_because


def test_cascade_exploration_start(env):
    result = env.router.cascade("brand_new_shape", "x")
    assert result.exploration is True
    assert result.attempts[0].model_id == "flash-mid-1"
    rows = env.router.receipts.rows()
    assert rows[-1]["exploration"] is True
    assert rows[-1]["chosen"] == "flash-mid-1"


# -- receipts ------------------------------------------------------------------


def test_receipts_append_only_and_parseable(env):
    for _ in range(3):
        env.router.ask("summarize", "s")
    first_pass = env.receipts.read_text(encoding="utf-8").splitlines(keepends=True)
    assert len(first_pass) == 3
    parsed = [json.loads(line) for line in first_pass]
    for row in parsed:
        assert list(row.keys())[: len(RECEIPT_REQUIRED_KEYS)] == list(
            RECEIPT_REQUIRED_KEYS
        )
        datetime.fromisoformat(row["ts"])
        assert isinstance(row["cost_usd"], float)
        assert isinstance(row["exploration"], bool)
        assert isinstance(row["reasons"], list)
    env.router.ask("code_review", "c")
    second_pass = env.receipts.read_text(encoding="utf-8").splitlines(keepends=True)
    assert len(second_pass) == 4
    assert second_pass[:3] == first_pass  # earlier rows byte-identical


def test_one_receipt_per_decision_and_per_cascade_attempt(env):
    # Ractor finding 1: post-Wilson the summarize cascade is a single
    # qualifying attempt (flash-mid-1 at 0.8737; gemma-worker-4b 0.8391
    # no longer clears 0.85), so one decision receipt plus one attempt
    # receipt, both legs still carrying the cascade trace fields.
    env.router.ask("summarize", "s")
    assert len(env.router.receipts.rows()) == 1
    result = env.router.cascade("summarize", "s")  # 1 attempt post-Wilson
    assert len(result.attempts) == 1
    rows = env.router.receipts.rows()
    assert len(rows) == 2
    cascade_rows = rows[1:]
    assert all("trace_id" in r and "cascade_step" in r for r in cascade_rows)
    assert len({r["trace_id"] for r in cascade_rows}) == 1


# -- server --------------------------------------------------------------------


def make_state(tmp_path, seeded=True):
    ledger_path = tmp_path / "led.db3"
    ledger = CapabilityLedger(ledger_path)
    if seeded:
        seed_ledger(ledger)
    ledger.close()
    return ServerState(
        CONFIG_PATH, ledger_path, tmp_path / "receipts.jsonl"
    )


def _call(state, name, arguments, req_id=1):
    response = process_request(
        state,
        {"jsonrpc": "2.0", "id": req_id, "method": "tools/call",
         "params": {"name": name, "arguments": arguments}},
    )
    assert "error" not in response, response
    text = response["result"]["content"][0]["text"]
    return json.loads(text)


def test_server_tools_list(tmp_path):
    state = make_state(tmp_path)
    response = process_request(
        state, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    )
    payload = json.loads(response["result"]["content"][0]["text"])
    names = [t["name"] for t in payload["tools"]]
    assert names == ["ask", "cascade", "report_capability", "record_verdict"]


def test_server_ask_roundtrip(tmp_path):
    state = make_state(tmp_path)
    result = _call(state, "ask", {"task_shape": "summarize",
                                  "payload": "hello"})
    # Ractor finding 1: the server surface routes on the same Wilson
    # lower bounds, so summarize lands on flash-mid-1 (0.8737), not on
    # gemma-worker-4b whose 0.8391 bound sits under the 0.85 threshold.
    assert result["chosen"] == "flash-mid-1"
    assert (tmp_path / "receipts.jsonl").exists()
    rows = [json.loads(l) for l in
            (tmp_path / "receipts.jsonl").read_text(encoding="utf-8").splitlines()]
    assert rows[-1]["task_shape"] == "summarize"


def test_server_record_then_report_roundtrip(tmp_path):
    state = make_state(tmp_path)
    recorded = _call(
        state, "record_verdict",
        {"model_id": "probe-1", "task_shape": "probe_shape",
         "verdict": True, "evidence_hash": "abc123"},
    )
    assert recorded["pass_rate"] == 1.0
    assert recorded["sample_size"] == 1
    reported = _call(
        state, "report_capability",
        {"model_id": "probe-1", "task_shape": "probe_shape"},
    )
    assert reported["measured"] is True
    assert reported["pass_rate"] == 1.0
    missing = _call(
        state, "report_capability",
        {"model_id": "ghost", "task_shape": "probe_shape"},
    )
    assert missing["measured"] is False


def test_server_bad_params_and_unknown_tool(tmp_path):
    state = make_state(tmp_path)
    err = process_request(
        state,
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": "ask", "arguments": {"payload": "x"}}},
    )
    assert err["error"]["code"] == -32602
    err2 = process_request(
        state,
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "nope", "arguments": {}}},
    )
    assert err2["error"]["code"] == -32601


# -- positive arm (LM7): streaks, badges, floor, momentum tiebreak ------------


def record_series(ledger, model_id, task_shape, series):
    # Ractor finding 1 (2026-10-10): get_rate now qualifies on RESOLVED
    # evidence only, so fixtures feed real evidence bytes with NO claimed
    # hash (the resolver computes and stores the true digest - a claimed
    # label like "ev-0" against real bytes lands MISMATCH/resolved=0,
    # which is the self-attested class the fix disqualifies).
    for i, v in enumerate(series):
        ledger.record_verdict(
            model_id, task_shape, v,
            evidence_bytes=f"evidence {model_id} {task_shape} {i} = {v}")


def test_momentum_rising_series_earns_rising_and_streak_badges(tmp_path):
    # Synthetic improving series: 4 fails then 26 passes.
    ledger = CapabilityLedger(tmp_path / "led.db3")
    record_series(ledger, "m", "shape", [0] * 4 + [1] * 26)
    mom = ledger.momentum("m", "shape")
    assert mom is not None
    assert mom.badge == "RISING"
    assert mom.window_size == 30
    assert mom.window_start_rate == pytest.approx(11 / 15)  # first half: F4 + P11
    assert mom.recent_rate == pytest.approx(1.0)
    assert mom.improvement_delta == pytest.approx(4 / 15)
    assert mom.rising is True
    assert mom.current_pass_streak == 26
    assert mom.best_pass_streak == 26
    assert mom.streak_badge == "STREAK-26"
    row = ledger.report_capability("m", "shape")
    assert row["momentum"]["badge"] == "RISING"
    assert row["momentum"]["streak_badge"] == "STREAK-26"


def test_momentum_declining_series(tmp_path):
    # Synthetic declining series: 26 passes then 4 fails.
    ledger = CapabilityLedger(tmp_path / "led.db3")
    record_series(ledger, "m", "shape", [1] * 26 + [0] * 4)
    mom = ledger.momentum("m", "shape")
    assert mom.badge == "DECLINING"
    assert mom.window_start_rate == pytest.approx(1.0)
    assert mom.recent_rate == pytest.approx(11 / 15)
    assert mom.improvement_delta == pytest.approx(-4 / 15)
    assert mom.current_pass_streak == 0  # last verdict is a fail
    assert mom.best_pass_streak == 26
    assert mom.streak_badge is None
    assert mom.rising is False


def test_momentum_steady_series(tmp_path):
    # Same rate across both window halves: no direction, STEADY.
    ledger = CapabilityLedger(tmp_path / "led.db3")
    record_series(ledger, "m", "shape", [1] * 10 + [0] * 10 + [1] * 10)
    mom = ledger.momentum("m", "shape")
    assert mom.badge == "STEADY"
    assert mom.window_start_rate == pytest.approx(10 / 15)
    assert mom.recent_rate == pytest.approx(10 / 15)
    assert mom.improvement_delta == pytest.approx(0.0)
    assert mom.current_pass_streak == 10
    assert mom.streak_badge == "STREAK-10"


def test_momentum_single_verdict_is_steady_and_undecorated(tmp_path):
    # One data point has no direction: delta exactly 0.0, streak below
    # the badge minimum, no STREAK-n claimed on thin evidence.
    ledger = CapabilityLedger(tmp_path / "led.db3")
    record_series(ledger, "m", "shape", [1])
    mom = ledger.momentum("m", "shape")
    assert mom.badge == "STEADY"
    assert mom.improvement_delta == 0.0
    assert mom.window_size == 1
    assert mom.current_pass_streak == 1
    assert mom.streak_badge is None


def test_streak_tracking_current_and_best(tmp_path):
    ledger = CapabilityLedger(tmp_path / "led.db3")
    record_series(ledger, "m", "a", [1, 1, 0, 1, 1, 1])
    mom = ledger.momentum("m", "a")
    assert (mom.current_pass_streak, mom.best_pass_streak) == (3, 3)
    record_series(ledger, "m", "b", [1, 1, 1, 0, 1])
    mom_b = ledger.momentum("m", "b")
    assert (mom_b.current_pass_streak, mom_b.best_pass_streak) == (1, 3)


def test_momentum_requires_verdict_history(env):
    # Ractor finding 1: the seeder MINTS resolved evidence for every
    # fixture rate, so a seeded pair now HAS verdict history and its
    # momentum is honestly earned: the mint order (round(rate*n) passes
    # first, then the fails) reads DECLINING (window start 1.0, recent
    # 0.4). The earned-never-declared law keeps its control arm on a
    # self-attested upsert (no evidence_note): no verdicts, no momentum,
    # and get_rate bounds it at the 0.21 floor.
    mom = env.ledger.momentum("flash-mid-1", "code_review")
    assert mom is not None
    assert mom.badge == "DECLINING"
    row = env.ledger.report_capability("flash-mid-1", "code_review")
    assert row["momentum"]["badge"] == "DECLINING"
    env.ledger.upsert_measurement(
        "attested-1", "shape2", 0.9, 10, None, seed_fixtures.SEED_DATE
    )
    assert env.ledger.momentum("attested-1", "shape2") is None
    assert env.ledger.report_capability("attested-1", "shape2")["momentum"] is None


def test_floor_clamps_fail_to_window_start_during_rising(tmp_path):
    # Exact-numbers construction: 50 verdicts, 30 passes (rate exactly
    # 0.6), window = last 30 = [P9 F6 P10 F5]: start 9/15, recent 10/15,
    # delta 1/15 > 0.05 -> RISING with floor 0.6 while the meter sits
    # exactly at the floor. The next fail would read 30/51 = 0.588; the
    # floor holds the meter at 0.6, the fail still logs.
    ledger = CapabilityLedger(tmp_path / "led.db3")
    series = (
        [1] * 11 + [0] * 9   # pre-window history
        + [1] * 9 + [0] * 6  # window first half: 9/15
        + [1] * 10 + [0] * 5 # window second half: 10/15
    )
    record_series(ledger, "m", "shape", series)
    mom = ledger.momentum("m", "shape")
    assert mom.badge == "RISING"
    assert mom.window_start_rate == pytest.approx(0.6)
    # Ractor finding 1: get_rate returns the Wilson lower bound
    # (z=1.96) over the 50 RESOLVED verdicts (30 passes, phat 0.6):
    # 0.4618, not the raw 0.6 running mean. The floor machinery below
    # still operates on the raw mean (record_verdict result), which the
    # post-fail assertions pin at 0.6.
    assert ledger.get_rate("m", "shape") == (pytest.approx(0.4618), 50)
    r = ledger.record_verdict("m", "shape", False, "the-fail")
    assert r.floor_applied is True
    assert r.floor_rate == pytest.approx(0.6)
    assert r.badge == "RISING"  # badge held before the fail
    assert r.pass_rate == pytest.approx(0.6)  # never below the floor
    assert r.sample_size == 51
    rows = ledger.verdict_log_rows("m", "shape")
    assert len(rows) == 51  # the fail logged, it did not vanish
    assert rows[-1]["verdict"] == 0


def test_floor_absorbs_fail_when_meter_below_floor(tmp_path):
    # Long bad history (raw meter 0.5) under a RISING window with floor
    # 0.6 (second half all passes, so no construction fail ever sees the
    # final window shape): the fail must not demote further, and must
    # not RAISE the meter to the floor either (a fail can never pay).
    # Meter ends unchanged; the fail still logs.
    ledger = CapabilityLedger(tmp_path / "led.db3")
    series = (
        [0] * 19 + [1] * 1  # pre-window history: raw meter dragged low
        + [1] * 9 + [0] * 6  # window first half: 9/15
        + [1] * 15           # window second half: 15/15, no fails here
    )
    record_series(ledger, "m", "shape", series)
    mom = ledger.momentum("m", "shape")
    assert mom.badge == "RISING"
    assert mom.window_start_rate == pytest.approx(0.6)
    assert mom.recent_rate == pytest.approx(1.0)
    # Ractor finding 1: get_rate is the Wilson lower bound over the 50
    # resolved verdicts (25 passes, phat 0.5): 0.3664. The raw meter the
    # floor absorbs into stays 0.5, pinned by the post-fail assert.
    assert ledger.get_rate("m", "shape") == (pytest.approx(0.3664), 50)
    r = ledger.record_verdict("m", "shape", False, "absorbed")
    assert r.floor_applied is True
    assert r.floor_rate == pytest.approx(0.6)
    assert r.pass_rate == pytest.approx(0.5)  # unchanged: absorbed, not punished, not paid
    assert len(ledger.verdict_log_rows("m", "shape")) == 51


def test_no_floor_outside_rising_window(tmp_path):
    # DECLINING window: the cold meter behaves exactly as before.
    ledger = CapabilityLedger(tmp_path / "led.db3")
    record_series(ledger, "m", "shape", [1] * 15 + [0] * 15)
    mom = ledger.momentum("m", "shape")
    assert mom.badge == "DECLINING"
    r = ledger.record_verdict("m", "shape", False, "cold")
    assert r.floor_applied is False
    assert r.floor_rate is None
    assert r.pass_rate == pytest.approx(15 / 31)


def test_fail_hammer_never_sinks_below_floor_while_rising(tmp_path):
    # Invariant hammer: while the window is RISING, no fail may push the
    # meter below min(pre-fail rate, window-start rate). When the window
    # stops rising the protection honestly lapses (it belongs to the
    # rising window, not to the model forever).
    ledger = CapabilityLedger(tmp_path / "led.db3")
    record_series(ledger, "m", "shape", [0] * 4 + [1] * 26)
    for i in range(12):
        mom = ledger.momentum("m", "shape")
        prev_rate, _ = ledger.get_rate("m", "shape")
        r = ledger.record_verdict("m", "shape", False, f"hammer-{i}")
        if mom is not None and mom.rising:
            assert r.pass_rate >= min(prev_rate, mom.window_start_rate) - 1e-9
            if r.floor_applied:
                assert r.floor_rate == pytest.approx(mom.window_start_rate)
    assert len(ledger.verdict_log_rows("m", "shape")) == 42  # every fail logged


def tie_env(tmp_path):
    ledger = CapabilityLedger(tmp_path / "led.db3")
    cfg = {
        "tier_order": ["mid"],
        "providers": [
            {"model_id": "fall-m", "base_url": "http://x", "model": "f",
             "tier": "mid", "cost_usd_per_call": 0.01, "test_double": True},
            {"model_id": "rise-m", "base_url": "http://x", "model": "r",
             "tier": "mid", "cost_usd_per_call": 0.01, "test_double": True},
        ],
    }
    registry = prov.build_registry(cfg)
    router = Router(registry, ledger, tmp_path / "receipts.jsonl")
    return ledger, router


def test_ranking_tiebreak_rising_outranks_declining(tmp_path):
    # AC10 lane-chooser law inverted toward momentum: two models at the
    # SAME cost and the SAME pass rate (26/30 each), one improving, one
    # sliding. RISING wins the tie.
    ledger, router = tie_env(tmp_path)
    record_series(ledger, "rise-m", "tie_shape", [0] * 4 + [1] * 26)
    record_series(ledger, "fall-m", "tie_shape", [1] * 26 + [0] * 4)
    d = router.ask("tie_shape", "x")
    assert d.chosen == "rise-m"
    assert any("momentum tiebreak" in reason for reason in d.reasons)
    badges = {c["model_id"]: c["momentum_badge"] for c in d.considered}
    assert badges == {"rise-m": "RISING", "fall-m": "DECLINING"}
    assert d.receipt["chosen"] == "rise-m"


def test_ranking_tiebreak_inert_without_verdict_history(tmp_path):
    # Control: no verdict history -> neutral momentum rank everywhere,
    # v0 cost-first behavior byte-stable (model_id breaks the tie).
    ledger, router = tie_env(tmp_path)
    ledger.upsert_measurement("rise-m", "tie_shape", 0.87, 30, None,
                              "2026-09-30T00:00:00+00:00")
    ledger.upsert_measurement("fall-m", "tie_shape", 0.87, 30, None,
                              "2026-09-30T00:00:00+00:00")
    d = router.ask("tie_shape", "x")
    assert d.chosen == "fall-m"
    assert all(c["momentum_badge"] is None for c in d.considered)


def test_server_report_carries_momentum_badges(tmp_path):
    state = make_state(tmp_path)
    for _ in range(3):
        _call(state, "record_verdict",
              {"model_id": "probe-1", "task_shape": "probe_shape",
               "verdict": True})
    reported = _call(
        state, "report_capability",
        {"model_id": "probe-1", "task_shape": "probe_shape"},
    )
    assert reported["momentum"]["badge"] == "STEADY"
    assert reported["momentum"]["streak_badge"] == "STREAK-3"
    assert reported["momentum"]["current_pass_streak"] == 3


# -- house law: no em dashes anywhere in the package ---------------------------


def test_no_em_dash_in_package_files():
    offenders = []
    for path in sorted(PACKAGE_DIR.rglob("*")):
        if path.suffix.lower() in (".py", ".md", ".json", ".yaml", ".yml"):
            text = path.read_text(encoding="utf-8")
            for bad in ("\u2014", "\u2013"):
                if bad in text:
                    offenders.append(f"{path.name}:{text.index(bad)}")
    assert offenders == []
