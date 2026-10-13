"""The single-writer Verkle lock must recover a marker whose owner died."""
from __future__ import annotations

from datetime import datetime, timezone


def test_dead_owner_lock_is_reclaimed(tmp_path, monkeypatch) -> None:
    from mag import verkle_knot as vk

    lock = tmp_path / ".verkle.lock"
    lock.write_text(
        f"99999999 {datetime.now(timezone.utc).isoformat()}", encoding="utf-8")
    monkeypatch.setattr(vk, "LOCK", lock)
    monkeypatch.setattr(vk, "_LOCK_POLL_SECONDS", 0.01)
    with vk.verkle_lock(timeout=0.25):
        assert lock.is_file()
    assert not lock.exists()
