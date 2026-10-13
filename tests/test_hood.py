"""Looking-eye hood — trajectory + RIBs from existing ledgers."""
from mag.hood import snapshot


def test_hood_snapshot_shape():
    s = snapshot()
    assert s["ok"] is True
    assert s["schema"] == "hood.v1"
    assert "models" in s and "ribs" in s and "traj" in s and "chan" in s
    assert isinstance(s["ribs"].get("n_domains"), int)
    assert isinstance(s["models"].get("path"), list)
    assert s["ribs"]["n_domains"] >= 1
