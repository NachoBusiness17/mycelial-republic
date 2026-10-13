import hashlib
import json

from mag.trajectory_rib import compile_tape


def _bounded_row(text="keep this anchor"):
    body = {"ts": "2026-09-02T00:00:00Z", "session": "agent:test", "event": "compact", "text": text}
    body_bytes = (json.dumps(body, separators=(",", ":")) + "\n").encode()
    raw_len = 0
    final = dict(body)
    final["metadata"] = {
        "schema": "trajectory_span.v1",
        "spanId": "span-1",
        "lineRange": [1, 1],
        "byteRange": [0, 0],
        "bodySha256": hashlib.sha256(body_bytes).hexdigest(),
    }
    # The writer measures the serialized row after inserting a placeholder
    # range, then writes that measured end byte into the row.  Iterate because
    # changing the number of digits can itself change the serialized length.
    end = 0
    for _ in range(4):
        final["metadata"]["byteRange"] = [raw_len, end]
        end = len((json.dumps(final, separators=(",", ":")) + "\n").encode())
    final["metadata"]["byteRange"] = [raw_len, end]
    return final


def test_compile_accepts_verified_span_and_rejects_legacy(tmp_path):
    tape = tmp_path / "traj.jsonl"
    tape.write_bytes((
        json.dumps(_bounded_row(), separators=(",", ":")) + "\n"
        + json.dumps({"event": "old"}, separators=(",", ":")) + "\n"
    ).encode())
    output = tmp_path / "compiled.jsonl"

    report = compile_tape(tape, output)

    assert report["compiled"] == 1
    assert report["rejected_unbounded"] == 1
    row = json.loads(output.read_text().splitlines()[0])
    assert row["source"]["bounded"] is True
    assert row["acceptance"]["status"] == "unproven"


def test_compile_redacts_secret(tmp_path):
    tape = tmp_path / "traj.jsonl"
    row = _bounded_row("token=sk-abcdefghijklmnopqrstuvwxyz"); row["metadata"]["bodySha256"] = "0" * 64
    # Use a normal unbounded row for this safety-only test; it must stay excluded.
    tape.write_bytes((json.dumps(row) + "\n").encode())
    output = tmp_path / "compiled.jsonl"
    report = compile_tape(tape, output, include_legacy=True)
    assert report["compiled"] == 1
    assert "sk-abcdefghijklmnopqrstuvwxyz" not in output.read_text()
    assert "[REDACTED]" in output.read_text()
