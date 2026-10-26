"""Tests for spore_seed module - demonstrates cryptographic anchoring and continuity.

B2-303 (2026-09-26): this module was the standing "1 error" in every full-suite
receipt (B2_34/B2_51/B2_64/B2_303). Cause, named per the fix-comment law:
test_generate_and_validate_spore_seed requested the `mocker` fixture
(pytest-mock) which is not installed in this venv, so the test errored at
setup on every run. The parameter was also unused; removed, not stubbed.
Second defect fixed in the same breath: test_seed_persistence reassigned the
imported name SPORE_SEED_FILE locally (no effect on mag.spore_seed), so every
suite run appended a test record to the PRODUCTION memory/spore_seeds/
testseat.jsonl (10 pollution rows on file at fix time). It now monkeypatches
mag.spore_seed.SPORE_SEED_FILE, the name _seed_file actually reads.
"""

import json

from mag import spore_seed


def test_generate_and_validate_spore_seed(tmp_path, monkeypatch):
    """Test that a generated spore seed validates correctly.

    B2-303: validate_spore_seed also needs the exact generate timestamp (the
    seed material is seat:timestamp:root), and generate_spore_seed appends to
    the spore log, so the log path is redirected to tmp_path (generate used to
    append to the PRODUCTION testseat.jsonl on every suite run).
    """
    monkeypatch.setattr(spore_seed, "SPORE_SEED_FILE", tmp_path / "{seat_id}.jsonl")

    seat_id = "testseat"
    root_hash = "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f9"
    timestamp = "2026-09-26T00:00:00+00:00"
    seed = spore_seed.generate_spore_seed(seat_id, root_hash, timestamp)

    assert spore_seed.validate_spore_seed(seed, seat_id, root_hash, timestamp) is True


def test_seed_persistence(tmp_path, monkeypatch):
    """Test that seeds are persisted to the append-only log (in tmp, never production)."""
    monkeypatch.setattr(
        spore_seed, "SPORE_SEED_FILE",
        tmp_path / "{seat_id}.jsonl",
    )

    record = {
        "timestamp": "2026-09-13T10:00:00Z",
        "seed": "abc123",
        "seat_id": "testseat",
        "root_hash": "def456",
        "knot_hash": "ghi789",
        "signature": "sig",
    }

    spore_seed._append_seed_record(record)
    seed_file = tmp_path / "testseat.jsonl"
    assert seed_file.exists()

    with open(seed_file, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1

    loaded = json.loads(lines[0])
    assert loaded == record


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
