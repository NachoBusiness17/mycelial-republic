"""Tests for spore_seed module — demonstrates cryptographic anchoring and continuity."""

import json
import tempfile
from pathlib import Path


def test_generate_and_validate_spore_seed(mocker):
    """Test that a generated spore seed validates correctly."""
    # Mock verkle chain to return a known root
    from mag.spore_seed import generate_spore_seed, validate_spore_seed
    
    # Generate a seed with a known root
    seat_id = "testseat"
    root_hash = "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f9"
    seed = generate_spore_seed(seat_id, root_hash)
    
    # Validate the seed
    assert validate_spore_seed(seed, seat_id, root_hash) is True


def test_seed_persistence(tmp_path):
    """Test that seeds are persisted to the append-only log."""
    # Temporarily redirect seed file path
    from mag.spore_seed import _append_seed_record
    from mag.constants import SPORE_SEED_FILE
    
    # Create a test seed record
    record = {
        "timestamp": "2026-09-13T10:00:00Z",
        "seed": "abc123",
        "seat_id": "testseat",
        "root_hash": "def456",
        "knot_hash": "ghi789",
        "signature": "sig"
    }
    
    # Temporarily override the file path
    old_format = SPORE_SEED_FILE
    SPORE_SEED_FILE = Path(tmp_path) / "{seat_id}.jsonl"
    
    try:
        _append_seed_record(record)
        seed_file = SPORE_SEED_FILE.format(seat_id="testseat")
        assert seed_file.exists()
        
        with open(seed_file, "r") as f:
            lines = f.readlines()
        assert len(lines) == 1
        
        loaded = json.loads(lines[0])
        assert loaded == record
    finally:
        SPORE_SEED_FILE = old_format

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
