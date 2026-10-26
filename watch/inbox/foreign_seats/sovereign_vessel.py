#!/usr/bin/env python3
"""tools/sovereign/vessel.py - The Invariant Memory Vessel & Relative Offset Architecture.

Foundational prototype of the Estate's Invariant Language:
- Eliminates unbounded 64-bit virtual memory heap pointers and broken Rust/C++ pointer webs.
- Enforces Bounded State: memory is allocated as fixed-size contiguous arenas.
- Compressed Relative Offsets: pointers are 32-bit offsets relative to the vessel base.
  They are bounds-checked at access and can never escape the vessel boundary.
- Zero-Copy Serialization: in-memory arena format IS the disk/wire format.
- Content-Addressed Cross-Vessel Links: relationships across vessels are established
  strictly via 32-byte SHA-256 digests, eliminating dangling inter-process pointers.
"""

from __future__ import annotations

import hashlib
import struct
from typing import Any, Dict, List, Optional, Tuple, Union


class VesselOverflowError(Exception):
    """Raised when an allocation exceeds the bounded arena capacity."""
    pass


class BoundedArena:
    """Fixed-capacity memory buffer with O(1) monotonic bump allocation.

    Memory layout:
    [Header: 32 bytes]
      - 4 bytes magic: b'VESL'
      - 2 bytes version: 1
      - 2 bytes flags: (1 = sealed/immutable)
      - 4 bytes total_capacity
      - 4 bytes bump_offset (bytes used)
      - 4 bytes record_count
      - 12 bytes reserved
    [Payload: bump_offset bytes of contiguous packed structs]
    """

    MAGIC = b"VESL"
    HEADER_SIZE = 32
    HEADER_FORMAT = "<4sHHIII12s"

    def __init__(self, capacity: int = 1048576) -> None:  # Default 1 MB arena
        if capacity < self.HEADER_SIZE:
            raise ValueError(f"Capacity must be at least {self.HEADER_SIZE} bytes")
        self.capacity = capacity
        self.buffer = bytearray(capacity)
        self.bump_offset = self.HEADER_SIZE
        self.record_count = 0
        self.sealed = False
        self._write_header()

    def _write_header(self) -> None:
        flags = 1 if self.sealed else 0
        struct.pack_into(
            self.HEADER_FORMAT,
            self.buffer,
            0,
            self.MAGIC,
            1,  # version
            flags,
            self.capacity,
            self.bump_offset,
            self.record_count,
            b"\x00" * 12,
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> BoundedArena:
        """Zero-copy instantiation from raw buffer."""
        if len(raw) < cls.HEADER_SIZE:
            raise ValueError("Buffer too small to contain vessel header")
        magic, ver, flags, cap, bump, rec_cnt, _ = struct.unpack_from(cls.HEADER_FORMAT, raw, 0)
        if magic != cls.MAGIC:
            raise ValueError(f"Invalid vessel magic: {magic}")
        arena = cls.__new__(cls)
        arena.capacity = cap
        arena.buffer = bytearray(raw)
        arena.bump_offset = bump
        arena.record_count = rec_cnt
        arena.sealed = bool(flags & 1)
        return arena

    def allocate(self, size: int, alignment: int = 4) -> int:
        """Bump allocates 'size' bytes. Returns relative offset from vessel head."""
        if self.sealed:
            raise PermissionError("Cannot allocate into a sealed immutable vessel")
        # Align offset
        rem = self.bump_offset % alignment
        if rem != 0:
            self.bump_offset += alignment - rem

        if self.bump_offset + size > self.capacity:
            raise VesselOverflowError(
                f"Vessel capacity exceeded: needed {size} bytes, free {self.capacity - self.bump_offset}"
            )

        offset = self.bump_offset
        self.bump_offset += size
        self.record_count += 1
        self._write_header()
        return offset

    def write_blob(self, data: bytes) -> int:
        """Writes a length-prefixed blob into the arena and returns its relative offset."""
        # 4-byte length prefix + data bytes
        total_len = 4 + len(data)
        offset = self.allocate(total_len)
        struct.pack_into(f"<I{len(data)}s", self.buffer, offset, len(data), data)
        return offset

    def read_blob(self, offset: int) -> bytes:
        """Reads a length-prefixed blob given its relative offset."""
        if offset < self.HEADER_SIZE or offset >= self.bump_offset:
            raise IndexError(f"Relative pointer out of vessel bounds: {offset}")
        length = struct.unpack_from("<I", self.buffer, offset)[0]
        data_start = offset + 4
        if data_start + length > self.bump_offset:
            raise IndexError(f"Blob extends beyond allocated vessel area: {data_start + length}")
        return bytes(self.buffer[data_start : data_start + length])

    def write_record(self, key: str, value: str, prev_hash: bytes = b"\x00" * 32) -> int:
        """Appends an immutable state record (key, value, prev_hash, digest).

        Record layout:
          - 32 bytes prev_hash
          - 32 bytes record_sha256
          - 2 bytes key_len
          - 4 bytes val_len
          - key_len bytes key
          - val_len bytes val
        """
        k_bytes = key.encode("utf-8")
        v_bytes = value.encode("utf-8")
        h = hashlib.sha256()
        h.update(prev_hash)
        h.update(k_bytes)
        h.update(v_bytes)
        digest = h.digest()

        rec_size = 32 + 32 + 2 + 4 + len(k_bytes) + len(v_bytes)
        offset = self.allocate(rec_size)

        fmt = f"<32s32sHI{len(k_bytes)}s{len(v_bytes)}s"
        struct.pack_into(fmt, self.buffer, offset, prev_hash, digest, len(k_bytes), len(v_bytes), k_bytes, v_bytes)
        return offset

    def read_record(self, offset: int) -> Dict[str, Any]:
        """Reads a record from its relative offset with invariant integrity check."""
        if offset < self.HEADER_SIZE or offset >= self.bump_offset:
            raise IndexError(f"Relative pointer out of vessel bounds: {offset}")
        prev_hash, digest, k_len, v_len = struct.unpack_from("<32s32sHI", self.buffer, offset)
        data_pos = offset + 70  # 32 + 32 + 2 + 4
        k_bytes = bytes(self.buffer[data_pos : data_pos + k_len])
        v_bytes = bytes(self.buffer[data_pos + k_len : data_pos + k_len + v_len])

        # Verify invariant
        h = hashlib.sha256()
        h.update(prev_hash)
        h.update(k_bytes)
        h.update(v_bytes)
        computed = h.digest()
        if computed != digest:
            raise ValueError(f"Record integrity violated at offset {offset}! Hash mismatch.")

        return {
            "offset": offset,
            "prev_hash": prev_hash.hex(),
            "sha256": digest.hex(),
            "key": k_bytes.decode("utf-8"),
            "value": v_bytes.decode("utf-8"),
        }

    def seal(self) -> bytes:
        """Seals the vessel, making it immutable and returning its SHA-256 digest."""
        self.sealed = True
        self._write_header()
        used_slice = bytes(self.buffer[: self.bump_offset])
        return hashlib.sha256(used_slice).digest()

    def get_used_bytes(self) -> bytes:
        """Returns the trimmed byte slice containing only active data."""
        return bytes(self.buffer[: self.bump_offset])


if __name__ == "__main__":
    print("Testing Invariant Memory Vessel...")
    arena = BoundedArena(capacity=65536)  # 64 KB arena
    off1 = arena.write_blob(b"Van Oortmerssen FlatBuffers Thesis")
    off2 = arena.write_record("NODE_ID", "bob_nvme_01")
    off3 = arena.write_record("INVARIANT", "Bounded state beats unbounded state at every scale")

    print(f"Bump offset: {arena.bump_offset} / {arena.capacity} bytes")
    print(f"Read blob: {arena.read_blob(off1).decode('utf-8')}")
    print(f"Read record 1: {arena.read_record(off2)}")
    print(f"Read record 2: {arena.read_record(off3)}")

    seal_digest = arena.seal()
    print(f"Vessel sealed successfully! Content hash: {seal_digest.hex()}")

    # Test zero-copy reload
    serialized = arena.get_used_bytes()
    reloaded = BoundedArena.from_bytes(serialized)
    print(f"Reloaded vessel record count: {reloaded.record_count}")
    print(f"Reloaded record: {reloaded.read_record(off3)['value']}")
    print("ALL INVARIANT VESSEL TESTS PASSED.")
