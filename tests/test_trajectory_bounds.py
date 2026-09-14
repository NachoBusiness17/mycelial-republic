from __future__ import annotations

import hashlib
import json


def test_build_bounds_counts_physical_lines_and_bounded_records(tmp_path):
    from mag.trajectory_bounds import build_bounds

    first = {"event": "compact", "metadata": {
        "schema": "trajectory_span.v1",
        "lineRange": [1, 1],
        "byteRange": [0, 10],
        "bodySha256": "0" * 64,
    }}
    second = {"event": "legacy"}
    tape = tmp_path / "tape.jsonl"
    raw = (json.dumps(first) + "\n" + json.dumps(second) + "\n").encode()
    tape.write_bytes(raw)

    result = build_bounds(tape)

    assert result["lines"] == 2
    assert result["bounded"] == 1
    assert result["legacyUnbounded"] == 1
    assert result["prefixAnchored"] is False
    assert result["tapeSha"] == "sha256:" + hashlib.sha256(raw).hexdigest()
