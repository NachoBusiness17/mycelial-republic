from __future__ import annotations

from mag.vast_cost import _period


def test_period_splits_child_amount_usd_without_recounting_parent():
    result = _period(
        [
            {
                "source": "instance-7",
                "type": "instance",
                "start": 1_000,
                "end": 2_000,
                "amount_usd": 10.0,
                "items": [
                    {"type": "gpu", "amount_usd": 4.0, "description": "4 hours GPU"},
                    {"type": "storage", "amount_usd": 3.0, "description": "disk"},
                    {"type": "bandwidth", "amount_usd": 3.0, "description": "egress"},
                ],
            }
        ],
        start=1_000,
        end=2_000,
    )
    assert result["actual_charges_usd"] == 10.0
    assert result["gpu_charges_usd"] == 4.0
    assert result["storage_charges_usd"] == 3.0
    assert result["bandwidth_charges_usd"] == 3.0
    assert result["gpu_hours"] == 4.0
    assert result["by_instance"] == [{"source": "instance-7", "amount_usd": 10.0}]

