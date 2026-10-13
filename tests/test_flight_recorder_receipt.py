"""Cache-receipt producer wiring tests (ouroboros R2 row 6, 2026-10-05).

Row 6 of watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/SYNTHESIS.md:
the cache-receipt KPI had zero producers (grep -rln cache_receipt over mag/
and tools/ returned only the reader, tools/cache_kpi.py), so the receipted
split read 0.0 against a 96.6 percent nominal hit rate. These tests pin the
producer contract now wired into record_call: a call that reuses a cached
prefix and reports cache telemetry gets cache_receipt {ok, verified_tokens,
reason} stamped onto its telemetry row through the strict-prefix gate in
mag/context_checkpoint.py, and the stamped rows feed tools/cache_kpi.py's
receipted split (the first nonzero recv reading).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mag import flight_recorder as fr  # noqa: E402
from mag.context_checkpoint import freeze_receipt  # noqa: E402
from tools.cache_kpi import compute, read_rows  # noqa: E402

# 264 bytes = 66 tokens at the estate chars-per-token convention (len // 4),
# small enough to stay under the fixture's 100 claimed cached tokens so the
# KPI clamp never engages and the assertions stay exact.
PREFIX = "frozen prefix block. " * 12
GEN = "gen-r2"


def _fake_chat(**_kw):
    """Deepseek-shaped vendor body: a nominal cache hit with the hit/miss split."""
    return {"usage": {"prompt_tokens": 200, "completion_tokens": 10,
                      "prompt_cache_hit_tokens": 100,
                      "prompt_cache_miss_tokens": 100}}


def _last_row(log_path):
    return json.loads(Path(log_path).read_text(encoding="utf-8").strip().splitlines()[-1])


def test_verified_reuse_stamps_ok_receipt(tmp_path):
    log = tmp_path / "fr.jsonl"
    receipt = freeze_receipt(PREFIX, GEN)
    status, result = fr.record_call(_fake_chat, "api", "deepseek-v4", "probe",
                                    log_path=log, cached_prefix=PREFIX,
                                    prefix_receipt=receipt, config_generation=GEN)
    assert status == "ok" and "usage" in result
    row = _last_row(log)
    assert row["cached_tok"] == 100
    assert row["cache_receipt"]["ok"] is True
    assert row["cache_receipt"]["verified_tokens"] == len(PREFIX.encode()) // 4
    assert row["cache_receipt"]["reason"] == "ok"


def test_mismatched_generation_stamps_measured_rejection(tmp_path):
    """Same bytes, wrong producer generation: the gate REFUSES and the row says so."""
    log = tmp_path / "fr.jsonl"
    receipt = freeze_receipt(PREFIX, GEN)
    fr.record_call(_fake_chat, "api", "deepseek-v4", "probe", log_path=log,
                   cached_prefix=PREFIX, prefix_receipt=receipt,
                   config_generation="gen-other")
    row = _last_row(log)
    assert row["cache_receipt"]["ok"] is False
    assert row["cache_receipt"]["verified_tokens"] == 0
    assert row["cache_receipt"]["reason"] == "config-generation-mismatch"


def test_tampered_prefix_stamps_partial_verify_rejection(tmp_path):
    log = tmp_path / "fr.jsonl"
    receipt = freeze_receipt(PREFIX, GEN)
    fr.record_call(_fake_chat, "api", "deepseek-v4", "probe", log_path=log,
                   cached_prefix=PREFIX[:100] + "X" + PREFIX[101:],
                   prefix_receipt=receipt, config_generation=GEN)
    row = _last_row(log)
    assert row["cache_receipt"]["ok"] is False
    assert row["cache_receipt"]["reason"] == "prefix-divergence"


def test_no_receipt_inputs_leaves_row_nominal(tmp_path):
    """Pre-law behaviour preserved: no receipt inputs, no stamp, cache_kpi reads
    the row nominally only."""
    log = tmp_path / "fr.jsonl"
    fr.record_call(_fake_chat, "api", "deepseek-v4", "probe", log_path=log)
    row = _last_row(log)
    assert row.get("cache_receipt") is None
    assert row["cached_tok"] == 100


def test_no_cache_telemetry_never_stamps(tmp_path):
    """The decision point is the reuse claim: no vendor cache telemetry, no verdict,
    even with receipt inputs supplied."""
    log = tmp_path / "fr.jsonl"
    receipt = freeze_receipt(PREFIX, GEN)
    fr.record_call(lambda **_kw: {"usage": {"prompt_tokens": 50, "completion_tokens": 5}},
                   "api", "deepseek-v4", "probe", log_path=log,
                   cached_prefix=PREFIX, prefix_receipt=receipt,
                   config_generation=GEN)
    row = _last_row(log)
    assert row.get("cached_tok") is None
    assert row.get("cache_receipt") is None


def test_upstream_usage_receipt_passes_through(tmp_path):
    """A producer that already gated upstream may carry usage.cache_receipt; the
    recorder stamps it verbatim."""
    log = tmp_path / "fr.jsonl"
    upstream = {"ok": True, "verified_tokens": 77, "reason": "ok"}
    fr.record_call(lambda **_kw: {"usage": {"prompt_tokens": 200,
                                            "cache_hit_tokens": 90,
                                            "cache_miss_tokens": 110,
                                            "cache_receipt": dict(upstream)}},
                   "api", "deepseek-v4", "probe", log_path=log)
    row = _last_row(log)
    assert row["cache_receipt"] == upstream


def test_failopen_gate_error_never_breaks_the_call(tmp_path, capsys, monkeypatch):
    """Recorder law: a telemetry error prints loudly and never breaks the call."""
    import mag.context_checkpoint as cc

    def boom(*_a, **_k):
        raise RuntimeError("gate exploded")

    monkeypatch.setattr(cc, "gate_skip_recompute", boom)
    log = tmp_path / "fr.jsonl"
    receipt = freeze_receipt(PREFIX, GEN)
    status, result = fr.record_call(_fake_chat, "api", "deepseek-v4", "probe",
                                    log_path=log, cached_prefix=PREFIX,
                                    prefix_receipt=receipt, config_generation=GEN)
    assert status == "ok" and "usage" in result          # call unaffected
    row = _last_row(log)
    assert row.get("cache_receipt") is None              # row left nominal
    assert "RECEIPT STAMP FAILED" in capsys.readouterr().err


def test_stamped_rows_feed_cache_kpi_receipted_split(tmp_path):
    """The synthetic-row KPI proof: rows emitted by record_call, read back through
    tools/cache_kpi.compute, produce a nonzero receipted reading (the number the
    2026-10-05 synthesis found at 0.0 with zero producers)."""
    log = tmp_path / "fr.jsonl"
    receipt = freeze_receipt(PREFIX, GEN)
    # row 1: verified reuse (66 verified tokens under a 100 nominal claim)
    fr.record_call(_fake_chat, "api", "deepseek-v4", "probe", log_path=log,
                   cached_prefix=PREFIX, prefix_receipt=receipt,
                   config_generation=GEN)
    # row 2: same vendor shape, no receipt inputs -> nominal only
    fr.record_call(_fake_chat, "api", "deepseek-v4", "probe", log_path=log)
    rows = read_rows(str(log))
    assert len(rows) == 2
    g = compute(rows)["deepseek"]
    verified = len(PREFIX.encode()) // 4                 # 66, under the 100 claim
    assert g["receipt_rows"] == 1
    assert g["receipt_ok_rows"] == 1
    assert g["receipt_tok"] == verified
    assert g["unreceipted_tok"] == 200 - verified        # 100+100 claimed, 66 proven
    assert g["tok_hit_rate"] == 0.5                      # nominal: 200 hit / 400 denom
    assert 0 < g["tok_hit_receipted_rate"] < g["tok_hit_rate"]  # usable share is real and lower
    assert g["tok_hit_receipted_rate"] == round(verified / 400, 4)
