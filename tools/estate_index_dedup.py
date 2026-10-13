"""Estate-index mirror dedup: verify byte-for-byte duplication, then swap a pointer in.

W3 Mickey17 lane (2026-09-29). Telemetry finding: dashboard/data/ESTATE_INDEX.jsonl
(~1.95 GB) appears duplicated byte-for-byte at watch/ESTATE_INDEX/ESTATE_INDEX.jsonl
(~1.95 GB mirror = ~3.9 GB on disk for one index). This tool is the honest verifier
and the one sanctioned replacer:

  --check (default): sample-hash BOTH files at head/mid/tail (default 4 MiB windows)
      + size equality. Never mutates anything.
        exit 0 = duplicate confirmed (samples+sizes equal) OR already deduped (pointer)
        exit 1 = DIVERGENT (sizes differ or any sampled region hashes differently)
        exit 2 = error (file missing/unreadable)
  --apply: only after a full re-verification — sizes, all three sample regions, AND a
      full streaming sha256 of BOTH files must agree. The full shas are BANKED to
      <mirror>.dedup_shas.json BEFORE the mirror is touched, then the mirror file is
      replaced (write-temp + atomic os.replace on the same volume) by a one-line
      pointer: "superseded by <primary>, deduped <date>, sha head/tail recorded".
      Any divergence at any gate => abort, touch nothing, exit 1.

Fix carries the receipt: the 2026-09-29 dedup ran --check first (head/mid/tail sample
shas + size matched), then --apply banked full sha256 of both copies before the
pointer swap; receipt watch/inbox/W3R_EID_DEDUP.md.

Usage:
  python tools/estate_index_dedup.py --check
  python tools/estate_index_dedup.py --apply [--dedup-date 2026-09-30]
  python tools/estate_index_dedup.py --check --primary P --mirror M   (arbitrary pair)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIMARY = ROOT / "dashboard" / "data" / "ESTATE_INDEX.jsonl"
DEFAULT_MIRROR = ROOT / "watch" / "ESTATE_INDEX" / "ESTATE_INDEX.jsonl"
DEFAULT_DEDUP_DATE = "2026-09-30"  # operator-prescribed pointer line (W3 mission text)
POINTER_MARK = "superseded by "
READ_CHUNK = 8 * 1024 * 1024
SAMPLE_BYTES = 4 * 1024 * 1024
POINTER_MAX_BYTES = 4096


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sample_shas(path: Path, sample: int = SAMPLE_BYTES) -> dict:
    """sha256 of the head/mid/tail sample windows + file size (cheap, no full read)."""
    size = path.stat().st_size
    out: dict[str, object] = {"size": size}
    with path.open("rb") as f:
        for region in ("head", "mid", "tail"):
            if region == "head":
                f.seek(0)
            elif region == "mid":
                f.seek(max(0, (size - sample) // 2))
            else:
                f.seek(max(0, size - sample))
            out[region] = hashlib.sha256(f.read(sample)).hexdigest()
    return out


def full_sha256(path: Path) -> str:
    """Streaming full-file sha256 (8 MiB chunks; sized for the ~1.95 GB index)."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(READ_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def is_pointer_file(path: Path) -> bool:
    """A dedup pointer is tiny and its first line announces the supersession."""
    if not path.is_file() or path.stat().st_size > POINTER_MAX_BYTES:
        return False
    with path.open("rb") as f:
        first = f.readline()
    return first.decode("utf-8", "replace").startswith(POINTER_MARK)


def check_pair(primary: Path, mirror: Path, sample: int = SAMPLE_BYTES) -> dict:
    """Compare primary vs mirror WITHOUT mutating anything. Returns a verdict dict."""
    verdict: dict[str, object] = {
        "primary": str(primary), "mirror": str(mirror), "sample_bytes": sample,
    }
    for name, p in (("primary", primary), ("mirror", mirror)):
        if not p.exists():
            verdict["state"] = f"missing-{name}"
            return verdict
    p_stat, m_stat = primary.stat(), mirror.stat()
    verdict["primary_size"], verdict["mirror_size"] = p_stat.st_size, m_stat.st_size
    if is_pointer_file(mirror):
        verdict["state"] = "deduped"
        verdict["pointer_line"] = mirror.read_text(encoding="utf-8").strip()
        return verdict
    ps, ms = sample_shas(primary, sample), sample_shas(mirror, sample)
    verdict["regions"] = {
        r: {"primary": ps[r], "mirror": ms[r], "match": ps[r] == ms[r]}
        for r in ("head", "mid", "tail")
    }
    sizes_equal = p_stat.st_size == m_stat.st_size
    regions_match = all(v["match"] for v in verdict["regions"].values())
    verdict["sizes_equal"] = sizes_equal
    if sizes_equal and regions_match:
        verdict["state"] = "dup"
    else:
        verdict["state"] = "divergent"
    return verdict


def apply_pointer(primary: Path, mirror: Path, dedup_date: str,
                  sample: int = SAMPLE_BYTES) -> dict:
    """Full verify -> bank shas -> swap pointer. Any divergence aborts untouched."""
    report: dict[str, object] = {"action": "apply", "primary": str(primary),
                                 "mirror": str(mirror), "dedup_date": dedup_date}
    for name, p in (("primary", primary), ("mirror", mirror)):
        if not p.exists():
            report.update(state=f"missing-{name}", touched=False)
            return report
    if is_pointer_file(mirror):
        report.update(state="already-deduped", touched=False)
        return report

    # Gate 1+2: sizes and all three sample regions must agree (cheap re-check).
    chk = check_pair(primary, mirror, sample)
    if chk["state"] != "dup":
        report.update(state="divergent", check=chk, touched=False,
                      note="sizes/samples disagree; nothing written")
        return report

    # Gate 3: full streaming sha256 of BOTH files (the byte-for-byte claim).
    p_sha, m_sha = full_sha256(primary), full_sha256(mirror)
    ps, ms = sample_shas(primary, sample), sample_shas(mirror, sample)
    report.update(primary_sha256=p_sha, mirror_sha256=m_sha,
                  size_bytes=chk["primary_size"])
    if p_sha != m_sha:
        report.update(state="divergent", touched=False,
                      note="full sha256 differs despite matching samples; nothing written")
        return report

    # Bank BEFORE touching the mirror: full + sample shas, sizes, mtimes, verdict.
    bank = mirror.with_name(mirror.name + ".dedup_shas.json")
    bank_data = {
        "deduped": dedup_date, "applied_utc": _utc_now(),
        "primary": str(primary), "mirror": str(mirror),
        "primary_sha256": p_sha, "mirror_sha256": m_sha,
        "size_bytes": chk["primary_size"], "sample_bytes": sample,
        "sample_shas": {"head": ps["head"], "mid": ps["mid"], "tail": ps["tail"]},
        "primary_mtime_utc": datetime.fromtimestamp(
            primary.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mirror_mtime_utc": datetime.fromtimestamp(
            mirror.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": ("byte-identical: sizes equal, head/mid/tail sample shas equal, "
                    "full sha256 equal"),
    }
    bank.write_text(json.dumps(bank_data, indent=1), encoding="utf-8")

    # Pointer swap: write a temp sibling, then atomic os.replace over the mirror.
    # WinError 5 fix (W3 2026-09-29): the first live run's os.replace was denied —
    # MoveFileEx(REPLACE_EXISTING) returns ACCESS_DENIED while ANY handle on the
    # target lacks FILE_SHARE_DELETE (fleet watchers/readers hold transient handles
    # on this mirror; shas were already banked so nothing was at risk). Cause-fixed
    # with a bounded retry; only if replacement stays denied do we remove the
    # target and rename the temp in (same end state, one no-file window), and a
    # denial of BOTH surfaces as a named error — never a silent skip.
    # Pointer names the primary repo-relative when it lives under ROOT (the
    # operator-prescribed W3 line reads "superseded by dashboard/data/
    # ESTATE_INDEX.jsonl, ..."); arbitrary outside-ROOT pairs print absolute.
    try:
        ptr_target = primary.relative_to(ROOT).as_posix()
    except ValueError:
        ptr_target = primary.as_posix()
    pointer_line = (f"{POINTER_MARK}{ptr_target}, deduped {dedup_date}, "
                    f"sha head/tail recorded\n")
    fd, tmp = tempfile.mkstemp(dir=str(mirror.parent), prefix=".eid_ptr_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(pointer_line)
        replaced = False
        for attempt in range(5):
            try:
                os.replace(tmp, mirror)
                replaced = True
                break
            except PermissionError:
                if attempt == 4:
                    try:
                        os.unlink(mirror)
                        os.replace(tmp, mirror)
                        replaced = True
                    except OSError as exc:
                        raise PermissionError(
                            f"cannot swap pointer over {mirror} after 5 attempts "
                            f"({exc}); shas are banked at {bank} — retry --apply "
                            f"after the holding process releases the file") from exc
                time.sleep(1.0)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    report.update(state="deduped", touched=True, bank=str(bank),
                  pointer_line=pointer_line.strip(),
                  reclaimed_bytes=chk["mirror_size"] - len(pointer_line.encode("utf-8")))
    return report


def _print_result(res: dict) -> int:
    state = res.get("state")
    if res.get("action") == "apply":
        if state == "deduped":
            print(f"APPLY OK: mirror replaced by pointer; reclaimed "
                  f"{res['reclaimed_bytes']:,} bytes")
            print(f"  pointer: {res['pointer_line']}")
            print(f"  bank:    {res['bank']}")
            print(f"  primary sha256 {res['primary_sha256']}")
            print(f"  mirror  sha256 {res['mirror_sha256']} (equal: "
                  f"{res['primary_sha256'] == res['mirror_sha256']})")
            return 0
        if state == "already-deduped":
            print("APPLY SKIP: mirror is already a pointer; nothing to do")
            return 0
        print(f"APPLY ABORT ({state}): mirror untouched")
        if "note" in res:
            print(f"  {res['note']}")
        return 1 if state == "divergent" else 2
    # check mode
    if state == "deduped":
        print(f"CHECK: already deduped — mirror is a pointer")
        print(f"  {res.get('pointer_line')}")
        return 0
    if state == "dup":
        print(f"CHECK: DUPLICATE CONFIRMED — sizes equal "
              f"({res['primary_size']:,} bytes), head/mid/tail sample shas all match")
        for r, v in res["regions"].items():
            print(f"  {r:<4} {v['primary'][:16]}... match={v['match']}")
        print("  dedup eligible: run --apply (banks full sha256s, then swaps pointer)")
        return 0
    if state == "divergent":
        print(f"CHECK: DIVERGENT — sizes_equal={res.get('sizes_equal')}")
        for r, v in res.get("regions", {}).items():
            print(f"  {r:<4} primary={v['primary'][:16]}... mirror={v['mirror'][:16]}..."
                  f" match={v['match']}")
        print("  mirror is NOT a byte copy; do not dedup")
        return 1
    print(f"CHECK ERROR: {state}")
    return 2


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", default=True,
                      help="verify only (default; never mutates)")
    mode.add_argument("--apply", action="store_true",
                      help="full verify, bank shas, replace mirror with pointer")
    ap.add_argument("--primary", type=Path, default=DEFAULT_PRIMARY)
    ap.add_argument("--mirror", type=Path, default=DEFAULT_MIRROR)
    ap.add_argument("--sample-mb", type=float, default=4.0,
                    help="sample window size in MiB for head/mid/tail (default 4)")
    ap.add_argument("--dedup-date", default=DEFAULT_DEDUP_DATE,
                    help="date stamped into the pointer line")
    ap.add_argument("--json", action="store_true", help="print result as JSON")
    args = ap.parse_args(argv)
    sample = int(args.sample_mb * 1024 * 1024)

    # Relative paths resolve under the repo root so CLI calls work from anywhere.
    primary = args.primary if args.primary.is_absolute() else ROOT / args.primary
    mirror = args.mirror if args.mirror.is_absolute() else ROOT / args.mirror

    if args.apply:
        res = apply_pointer(primary, mirror, args.dedup_date, sample)
    else:
        res = check_pair(primary, mirror, sample)
        res["action"] = "check"
    if args.json:
        print(json.dumps(res, indent=1))
    return _print_result(res)


if __name__ == "__main__":
    sys.exit(main())
