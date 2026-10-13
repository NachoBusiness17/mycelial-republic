"""B2-133: the providers.yaml dormant flag gates every mag/ hardcoded lane list.

CAUSE: B2-36 declared cerebras dormant (card-gated 30-day trial, chat 402 no-credit)
in configs/providers.yaml, but seven mag/ modules kept routing or pricing it from
hardcoded lists. EVIDENCE: watch/inbox/burn_wave_20260926/
B2_36_cerebras_reclassify_20260926.md (the flag, `dormant: true` on the cerebras
block) and mag/doctor.py:607 (dormant is a declared state, never probed).

The law under test: (1) mag.dormant reads the flag from bytes, including the
host-match form raw-URL lane lists need, and never invents dormancy from an
unreadable config; (2) no mag/ lane list or pricing set carries a provider that is
dormant RIGHT NOW (tracks the flag, so operator GO auto-disarms this test by
shrinking the dormant set, never by rotting).
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from mag import dormant  # noqa: E402


def test_dormant_helper_reads_flag_from_bytes(tmp_path):
    cfg = tmp_path / "providers.yaml"
    cfg.write_text(
        "providers:\n"
        "  lane_a:\n"
        "    dormant: true\n"
        "    base_url: https://api.lane-a.test/v1\n"
        "  lane_b:\n"
        "    base_url: https://api.lane-b.test/v1\n",
        encoding="utf-8")
    assert dormant.dormant_ids(cfg) == {"lane_a"}
    assert dormant.dormant_hosts(cfg) == {"api.lane-a.test"}
    assert dormant.is_dormant(provider_id="lane_a", path=cfg)
    assert dormant.is_dormant(base_url="https://api.lane-a.test/v1", path=cfg)
    assert not dormant.is_dormant(provider_id="lane_b", path=cfg)
    assert not dormant.is_dormant(base_url="https://api.lane-b.test/v1", path=cfg)
    # an unreadable config never invents dormancy (empty set, fail-open honest)
    assert dormant.dormant_ids(tmp_path / "missing.yaml") == set()
    assert dormant.dormant_hosts(tmp_path / "missing.yaml") == set()


def test_no_mag_lane_list_carries_a_currently_dormant_provider():
    """Wiring proof: while cerebras is dormant (B2-36), no mag/ list routes or
    prices it; the same holds for every other flagged provider (saelis, gemini,
    mistral, nvidia today). Post-GO the flag flips and this stays green."""
    live = dormant.dormant_ids()
    assert "cerebras" in live, (
        "B2-133 premise gone: providers.yaml no longer flags cerebras dormant "
        "(operator GO landed?); this wiring test then has no bite and may be retired")
    from mag import cost_truth, free_tier, fuel_feed  # noqa: E402
    from mag import lane_salon, quorum_window, research_fanout, rotation_harness  # noqa: E402

    assert not {l[1] for l in fuel_feed.FREE_LANES} & live
    assert not {l[0] for l in fuel_feed.FAST_LANES} & live
    assert not {l[0] for l in fuel_feed.STRONG_LANES} & live
    assert not {l[0] for l in rotation_harness.LANES} & live
    assert not {w[1] for w in lane_salon.WITNESSES} & live
    assert not {l[0] for l in quorum_window.FREE_LANES} & live
    assert not {s["id"] for s in free_tier.FREE_SURFACES} & live
    assert not cost_truth._PROVIDER_FREE_OR_CREDIT & live
    # research_fanout lanes are lane-local ids behind raw base urls: host match
    hosts = dormant.dormant_hosts()
    from urllib.parse import urlsplit
    for lane in research_fanout.LANES:
        assert urlsplit(lane.get("base", "")).hostname not in hosts, lane["id"]


def test_dormant_provider_historical_rows_never_reprice_to_spend():
    """B2-522 decision pin (2026-09-26 review, receipt
    watch/inbox/burn_wave_20260926/B2_522_cost_truth_20260926.md): the historical
    cerebras/nvidia usage rows (165 + 100 in logs/provider_usage.jsonl) were
    provider credits, never spend, so the dormant gate's re-pricing of them to
    the unpriced unknown is accepted and any future fix that yields a nonzero
    calculated_usd for these provider/model ids is the falsified direction.
    Whichever way the flag points, dollars stay 0.0; while dormant the state is
    the first-class unpriced unknown, after GO it is free_or_quota again."""
    from mag import cost_truth, dormant  # noqa: E402

    live = dormant.dormant_ids()
    ids = (
        ("cerebras", "gpt-oss-120b"),
        ("cerebras", "llama-3.3-70b"),
        ("nvidia", "deepseek-ai/deepseek-v4-flash-0731"),
        ("nvidia", "meta/llama-3.3-70b-instruct"),
        # z_ai3 joined the dormant set 2026-10-03 (operator: Lite lane given to
        # adam; receipt watch/inbox/LITE_LANE_PULL_20261003.md). Unlike
        # cerebras/nvidia it CARRIES a real glm-5.3-flash rate, so this pin
        # guards the seam fix: dormancy must intercept the rate path too.
        ("z_ai3", "glm-5.3-flash"),
    )
    for provider, model in ids:
        priced = cost_truth.price_tokens(
            provider, model, cache_hit_tokens=100, cache_miss_tokens=1000, completion_tokens=100
        )
        assert priced["calculated_usd"] == 0.0, (provider, model, priced)
        if provider in live:
            assert priced["state"] == "unpriced", (provider, model, priced["state"])
        else:
            assert priced["state"] == "free_or_quota", (provider, model, priced["state"])

    # Byte anchor over the live receipt stream: while a provider is dormant,
    # every logged row for it is historical credit traffic and must contribute
    # zero calculated dollars. Post-GO the dormant set shrinks and this scan
    # fades out instead of rotting.
    rows, _ = cost_truth._read_usage()
    for row in rows:
        provider = str(row.get("provider") or row.get("provider_id") or "").lower()
        if provider not in live:
            continue
        parts = cost_truth._row_tokens(row)
        priced = cost_truth.price_tokens(
            provider,
            str(row.get("model") or ""),
            cache_hit_tokens=int(parts["cache_hit_tokens"]),
            cache_miss_tokens=int(parts["cache_miss_tokens"]),
            completion_tokens=int(parts["completion_tokens"]),
            at=cost_truth._parse_ts(row.get("ts")),
        )
        assert priced["calculated_usd"] == 0.0, (provider, row.get("model"), priced)
