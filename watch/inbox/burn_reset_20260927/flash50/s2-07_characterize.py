"""s2-07 instrument v3: characterize the top-10 files by byte count.

For each: size, link count, file index, head/tail bytes, line count (jsonl),
first/last line (truncated), tar member list (tars), header hex (binary).
Full sha256 for the two same-size ESTATE_INDEX.jsonl copies.
"""
import os
import sys
import hashlib
import tarfile
import datetime

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

TOP10 = [
    r"attic\20260923_mimosa_rotation\hook-state_stale_baselines.tar",
    r"dashboard\data\ractor_board.jsonl.runaway-evidence-20260903",
    r"watch\inbox\ESSENTIALS_PACK_20260926.tar.gz.enc",
    r"watch\ESTATE_INDEX\ESTATE_INDEX.jsonl",
    r"dashboard\data\ESTATE_INDEX.jsonl",
    r"memory\ingest\registry.jsonl",
    r"logs\kpi.jsonl",
    r"dashboard\data\ractor_board.jsonl",
    r"memory\runs\ghost\trail.jsonl",
    r"memory\runs\file_dogfood\manifest.jsonl",
]


def printable(b):
    return "".join(chr(c) if 32 <= c < 127 else "." for c in b)


def head_tail(path, nbytes=400):
    out = []
    with open(path, "rb") as f:
        out.append(("head", f.read(nbytes)))
        f.seek(-min(nbytes, os.path.getsize(path)), os.SEEK_END)
        out.append(("tail", f.read(nbytes)))
    return out


def first_last_line(path):
    res = []
    with open(path, "rb") as f:
        first = f.readline(2000)
        f.seek(0, os.SEEK_END)
        size = f.tell()
        back = min(size, 65536)
        f.seek(size - back)
        chunk = f.read()
    lines = chunk.splitlines()
    last = lines[-1] if lines else b""
    res.append((first[:300]))
    res.append((last[-300:]))
    return res


def count_lines(path):
    n = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 24)
            if not chunk:
                break
            n += chunk.count(b"\n")
    return n


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 24)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


for rel in TOP10:
    p = os.path.join(ROOT, rel)
    print("=" * 100)
    print("FILE:", rel)
    try:
        st = os.stat(p)
    except OSError as e:
        print("  STAT ERROR:", e)
        continue
    print(f"  bytes={st.st_size} mtime={datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds')} nlink={st.st_nlink} fileindex={st.st_ino}")
    if rel.endswith(".tar"):
        try:
            with tarfile.open(p, "r|") as tf:
                shown = 0
                for m in tf:
                    if shown < 20:
                        print(f"  tar-member: {m.name} size={m.size}")
                        shown += 1
                    else:
                        break
                print("  (member listing capped at 20; not counting the rest)")
        except Exception as e:
            print("  TAR ERROR:", repr(e))
    elif rel.endswith(".enc"):
        with open(p, "rb") as f:
            hdr = f.read(32)
        print("  first-32-bytes-hex:", hdr.hex())
        print("  first-32-bytes-prn:", printable(hdr))
        print("  (encrypted container: content not readable without key; no line count)")
    elif rel.endswith(".jsonl") or rel.endswith(".log"):
        for tag, b in head_tail(p):
            print(f"  {tag}: {printable(b)}")
        print("  first-line:", printable(first_last_line(p)[0]))
        print("  last-line :", printable(first_last_line(p)[1]))
        print("  counting lines ...")
        n = count_lines(p)
        print(f"  line_count={n}")

print("=" * 100)
print("SHA256 of the two same-size ESTATE_INDEX.jsonl copies:")
a = os.path.join(ROOT, r"watch\ESTATE_INDEX\ESTATE_INDEX.jsonl")
b = os.path.join(ROOT, r"dashboard\data\ESTATE_INDEX.jsonl")
ha = sha256_file(a)
print("  watch\\ESTATE_INDEX\\ESTATE_INDEX.jsonl", ha)
hb = sha256_file(b)
print("  dashboard\\data\\ESTATE_INDEX.jsonl      ", hb)
print("  identical:", ha == hb)
print("  sum_top10_bytes:", sum(os.stat(os.path.join(ROOT, r)).st_size for r in TOP10))
