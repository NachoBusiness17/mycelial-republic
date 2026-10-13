"""Backend-tier field on the gguf_cartography census row (build wave B9, 2026-10-05).

Port from the day-4 mine card (quantization-and-compression steal): one field
in the census output recording backend tier (GGUF vs non-GGUF) next to each
model's quant level, so the AQLM method-tier rule (any non-GGUF backend swap
reopens the method question) is machine-checkable at census time instead of
memory-resident.
"""
import json
import struct

from mag.gguf_cartography import scan


def _kv_str(key: str, val: str) -> bytes:
    return (struct.pack("<Q", len(key)) + key.encode("utf-8")
            + struct.pack("<I", 8)
            + struct.pack("<Q", len(val)) + val.encode("utf-8"))


def _kv_u32(key: str, val: int) -> bytes:
    return (struct.pack("<Q", len(key)) + key.encode("utf-8")
            + struct.pack("<I", 4) + struct.pack("<I", val))


def _write_gguf(path) -> None:
    """Minimal GGUF v3: 3 metadata kvs, one F16 tensor of 8 elements."""
    name = "blk.0.attn_weight"
    data = struct.pack("<8e", 1.0, -0.5, 0.25, 0.125, 2.0, 4.0, 8.0, 16.0)
    buf = b"GGUF" + struct.pack("<I", 3)
    buf += struct.pack("<Q", 1)      # tensor_count
    buf += struct.pack("<Q", 3)      # metadata_kv_count
    buf += _kv_str("general.architecture", "llama")
    buf += _kv_str("general.name", "b9-backend-tier-fixture")
    buf += _kv_u32("general.file_type", 15)  # 15 = Q4_K_M in FILE_TYPES
    buf += struct.pack("<Q", len(name)) + name.encode("utf-8")
    buf += struct.pack("<I", 1)      # n_dims
    buf += struct.pack("<Q", 8)      # dims = [8]
    buf += struct.pack("<I", 1)      # dtype 1 = F16
    buf += struct.pack("<Q", 0)      # offset 0, relative to data section
    buf += b"\x00" * ((-len(buf)) % 32)  # default alignment 32
    path.write_bytes(buf + data)


def test_backend_tier_field_lands_on_census_row(tmp_path):
    gguf = tmp_path / "tiny.gguf"
    out = tmp_path / "census.json"
    _write_gguf(gguf)

    doc = scan(gguf, sample_mb=1.0, out=out)

    assert doc["backend_tier"] == "GGUF"
    # the tier rides next to the quant level, not buried elsewhere
    assert doc["quant_file_type"] == "Q4_K_M"
    # and it persists into the written census JSON, where a checker reads it
    reread = json.loads(out.read_text(encoding="utf-8"))
    assert reread["backend_tier"] == "GGUF"
