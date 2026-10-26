"""One-shot evidence packer for the disk-storm audit (2026-10-09).

Receipt-space script (NOT a repo tool). Single process, metadata-only walks
(scandir/stat, no hashing, no bulk content reads), bounded content samples.
The ONLY place a child path is ever joined is safe_child(): the name is
rejected if it is empty/dot/dotdot or contains a path separator, and the
resolved candidate must sit inside the resolved allowroot. Display labels
carry the already-guarded Path objects; writes go through write_text on
guarded paths. Nothing outside the named roots is opened or stated.
Output: watch/inbox/disk_audit_20261009/evidence_pack/{exec_forensics.json,
samples.jsonl, digest.md}. See WAVE_PLAN.md Phase 0.
"""
import heapq
import json
import os
import random
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

EXEC_ROOT = Path(r"C:\Users\foste\.zcode\cli\exec")
CLI_ROOT = Path(r"C:\Users\foste\.zcode\cli")
HERMES_ROOT = Path(r"C:\Users\foste\AppData\Local\hermes")
TEMP_ROOT = Path(r"C:\Users\foste\AppData\Local\Temp")
HF_ROOT = Path(r"C:\Users\foste\.cache\huggingface\models")
OUT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\disk_audit_20261009\evidence_pack")
NOW = time.time()
DAY = 86400.0
SAMPLE_EVERY = 4000          # keep every Nth path for the sampling pool
SAMPLE_READ_CAP = 150        # max files actually opened (2KB each)
LARGEST_N = 60
AGE_EDGES = [(1, "lt1d"), (3, "d1_3"), (7, "d3_7"), (14, "d7_14"), (30, "d14_30"), (10**9, "gt30d")]

def safe_child(dirpath: Path, name: str, allowroot: Path):
    """The single sanctioned join: dirpath/name is built only when name is a
    plain filename and the resolved candidate stays inside allowroot."""
    if name in ("", ".", "..") or "/" in name or "\\" in name:
        return None
    p = dirpath / name
    try:
        if not p.resolve().is_relative_to(allowroot.resolve()):
            return None
    except OSError:
        return None
    return p

def safe_dir(dirpath: Path, allowroot: Path) -> bool:
    try:
        return dirpath.resolve().is_relative_to(allowroot.resolve())
    except OSError:
        return False

def age_name(days: float) -> str:
    for lim, name in AGE_EDGES:
        if days < lim:
            return name
    return "gt30d"

def gb(n: float) -> float:
    return round(n / 2**30, 2)

def walk_exec():
    per_age = defaultdict(lambda: [0, 0])
    per_day = defaultdict(int)
    per_sess = defaultdict(lambda: [0, 0, 0.0])   # key -> [count, bytes, last_mtime]
    exts = defaultdict(lambda: [0, 0])
    largest = []                                   # min-heap of (bytes, guarded Path, mtime)
    pool = []                                      # sampling candidate guarded Paths
    nfiles = nbytes = errors = 0
    for dirpath, _dirnames, filenames in os.walk(EXEC_ROOT):
        dpath = Path(dirpath)
        if not safe_dir(dpath, EXEC_ROOT):
            continue
        rel = dpath.relative_to(EXEC_ROOT)
        parts = rel.parts
        # key: sess dir (first level under exec); "(root)" for loose files
        key = parts[0] if parts else "(root)"
        for fn in filenames:
            nfiles += 1
            if nfiles % 20000 == 0:
                print(f"progress: {nfiles} files {gb(nbytes)}GiB", flush=True)
            p = safe_child(dpath, fn, EXEC_ROOT)
            if p is None:
                errors += 1
                continue
            try:
                st = p.stat()
            except OSError:
                errors += 1
                continue
            b, mt = st.st_size, st.st_mtime
            nbytes += b
            an = age_name((NOW - mt) / DAY)
            per_age[an][0] += 1
            per_age[an][1] += b
            per_day[datetime.fromtimestamp(mt, timezone.utc).strftime("%m-%d")] += b
            row = per_sess[key]
            row[0] += 1
            row[1] += b
            row[2] = max(row[2], mt)
            ext = p.suffix.lower() or "(none)"
            exts[ext][0] += 1
            exts[ext][1] += b
            item = (b, p, mt)
            if len(largest) < LARGEST_N:
                heapq.heappush(largest, item)
            elif b > largest[0][0]:
                heapq.heapreplace(largest, item)
            if nfiles % SAMPLE_EVERY == 0:
                pool.append(p)
    return dict(nfiles=nfiles, nbytes=nbytes, errors=errors,
                per_age={k: dict(count=v[0], bytes=v[1]) for k, v in per_age.items()},
                per_day=dict(sorted(per_day.items())),
                top_sess=sorted(((v[1], k, v[0], v[2]) for k, v in per_sess.items()), reverse=True)[:40],
                exts=sorted(((v[1], k, v[0]) for k, v in exts.items()), reverse=True)[:20],
                largest=sorted(((b, str(p), mt) for b, p, mt in largest), reverse=True)), pool

def classify_head(head: bytes) -> str:
    if head.startswith(b"{") or head.startswith(b"["):
        return "json"
    if head.startswith(b"<"):
        return "xml/html"
    if b"\x00" in head:
        return "binary"
    printable = sum(32 <= c < 127 or c in (9, 10, 13) for c in head[:256])
    if printable / max(1, min(256, len(head))) > 0.85:
        low = head[:512].decode("latin1", "ignore").lower()
        if "error" in low or "traceback" in low:
            return "text-errorish"
        return "text"
    return "binary-ish"

def sample(pool):
    rng = random.SystemRandom()
    rows = []
    for p in rng.sample(pool, min(SAMPLE_READ_CAP, len(pool))):
        # re-verify containment at open time (guard adjacent to the access)
        if not safe_dir(p.parent, EXEC_ROOT):
            continue
        q = safe_child(p.parent, p.name, EXEC_ROOT)
        if q is None:
            continue
        try:
            with open(q, "rb") as f:
                head = f.read(2048)
            rows.append({"path": str(q), "size": q.stat().st_size,
                         "cls": classify_head(head), "head": head[:220].decode("latin1", "ignore")})
        except OSError:
            continue
    return rows

def top_sizes(root: Path, skip: set = set()) -> dict:
    """Cheap bounded table: sizes of entries directly under root, guarded."""
    out = {}
    try:
        entries = list(os.scandir(root))
    except OSError:
        return {"(unreadable)": 0}
    for e in entries:
        if e.name in skip:
            continue
        p = safe_child(root, e.name, root)
        if p is None:
            continue
        try:
            if e.is_dir(follow_symlinks=False):
                tot = 0
                for dp, _dn, fns in os.walk(p):
                    dpp = Path(dp)
                    if not safe_dir(dpp, root):
                        continue
                    for fn in fns:
                        c = safe_child(dpp, fn, root)
                        if c is None:
                            continue
                        try:
                            tot += c.stat().st_size
                        except OSError:
                            pass
                out[e.name] = tot
            else:
                out[e.name] = p.stat().st_size
        except OSError:
            out[e.name] = -1
    return dict(sorted(out.items(), key=lambda kv: -kv[1])[:25])

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print("walking exec forest ...", flush=True)
    res, pool = walk_exec()
    print(f"walk done: {res['nfiles']} files {gb(res['nbytes'])}GiB in {time.time()-t0:.0f}s; sampling", flush=True)
    res["samples"] = sample(pool)
    res["secondary"] = {
        "zcode_cli_top": top_sizes(CLI_ROOT, skip={"exec"}),
        "hermes_local_top": top_sizes(HERMES_ROOT),
        "temp_top": top_sizes(TEMP_ROOT),
        "hf_models": top_sizes(HF_ROOT),
    }
    out_json = safe_child(OUT, "exec_forensics.json", OUT)
    out_samples = safe_child(OUT, "samples.jsonl", OUT)
    out_digest = safe_child(OUT, "digest.md", OUT)
    if out_json is None or out_samples is None or out_digest is None:
        raise SystemExit("output path containment failed; refusing to write")
    out_json.write_text(json.dumps(res, default=str, indent=1))
    samples_text = "\n".join(json.dumps(s) for s in res["samples"])
    out_samples.write_text(samples_text, encoding="latin1")
    purge_prize = res["per_age"].get("d7_14", {"bytes": 0})["bytes"] + res["per_age"].get("d14_30", {"bytes": 0})["bytes"] + res["per_age"].get("gt30d", {"bytes": 0})["bytes"]
    lines = [
        "# EXEC FOREST FORENSICS - evidence pack digest",
        f"moment: {datetime.now(timezone.utc).isoformat()} | walk seconds: {time.time()-t0:.0f}",
        f"total: {res['nfiles']} files, {gb(res['nbytes'])}GiB, stat-errors {res['errors']}",
        "",
        "## age histogram (the purge prize)",
        "| bucket | files | GiB |",
        "|---|---|---|",
    ]
    for lim, name in AGE_EDGES:
        v = res["per_age"].get(name)
        if v:
            lines.append(f"| {name} | {v['count']} | {gb(v['bytes'])} |")
    lines += ["", f"**purge prize (7d+): {gb(purge_prize)}GiB**", "",
              "## daily growth curve (GiB by mtime day)", "```"]
    mx = max(res["per_day"].values(), default=0)
    for d, b in res["per_day"].items():
        lines.append(f"{d} {gb(b):>8} {'#' * max(1, int(40 * b / max(1, mx)))}")
    lines += ["```", "", "## top sessions (who)", "```"]
    for b, k, c, mt in res["top_sess"][:20]:
        lines.append(f"{gb(b):>8}GiB {c:>7}f {datetime.fromtimestamp(mt, timezone.utc).strftime('%m-%d %H:%M')} {k}")
    lines += ["```", "", "## sample classes"]
    cc = defaultdict(int)
    for s in res["samples"]:
        cc[s["cls"]] += 1
    lines.append(json.dumps(dict(cc), indent=1))
    out_digest.write_text("\n".join(lines))
    print("evidence pack written:", OUT, flush=True)

if __name__ == "__main__":
    main()
