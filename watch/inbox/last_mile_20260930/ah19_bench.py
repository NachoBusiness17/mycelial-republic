"""ah19_bench.py — AH19 (audit finding #10) wall-time bench: 100 v2 appends vs 100 v1 amends.

Run:  .venv/Scripts/python.exe watch/inbox/last_mile_20260930/ah19_bench.py

Design (AH19_AMEND_PERF.md): seed a fresh chain with 500 distinct sessions,
then re-save ONE far-from-tail session (the live disease shape: a hot session
amended over a long chain) 100 times under each chain mode. Everything is
redirected into a temp dir — the live chain is never touched.

Bytes-written accounting is honest to the write model: a v1 amend rewrites the
whole file (bytes_written += new file size); a v2 append writes one line
(bytes_written += size delta). Verify (the pre-append integrity gate + the
post-append self-verify) runs inside both timings — same cost shape per save.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from mag import verkle_knot as vk  # noqa: E402

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 500
SAVES = int(sys.argv[2]) if len(sys.argv) > 2 else 100


def dossier(session_id: str, salt: str, tension: float = 0.25) -> dict:
    return {
        "session_id": session_id,
        "time": {
            "created_at": {"iso_minute": "2026-09-30T00:00:00Z", "unix_minute": 5000000,
                            "date": "2026-09-30"},
            "updated_at": {"iso_minute": "2026-09-30T00:01:00Z", "unix_minute": 5000001},
        },
        "scalar_knot": {"tension_index": tension, "duration_minutes": 1},
        "content_commit": {"hex": hashlib.sha256(f"{session_id}:{salt}".encode()).hexdigest()},
    }


def redirect(tmp: Path) -> None:
    vk.CHAIN = tmp / "verkle_chain.jsonl"
    vk.TIP = tmp / "verkle_tip.json"
    vk.KNOTS = tmp / "knots"
    vk.EVOLUTION = tmp / "topic_evolution.json"
    vk.LATEST = tmp / "latest.knot.json"
    vk.LOCK = tmp / ".verkle.lock"
    vk.KNOTS.mkdir(parents=True, exist_ok=True)


def chain_size() -> int:
    return vk.CHAIN.stat().st_size if vk.CHAIN.is_file() else 0


def n_rows() -> int:
    if not vk.CHAIN.is_file():
        return 0
    return sum(1 for l in vk.CHAIN.read_text(encoding="utf-8").splitlines() if l.strip())


def run(mode: str, tmp: Path) -> dict:
    redirect(tmp)
    vk.chain_mode = (lambda: mode)  # noqa: E731 — bench-local mode pin
    t0 = time.perf_counter()
    for i in range(SEED):
        r = vk.append_verkle_knot(dossier(f"sess-seed-{i}", str(i)))
        assert r.get("ok"), r
    seed_s = time.perf_counter() - t0

    hot = "sess-seed-3"  # far from tail
    size_before = chain_size()
    bytes_written = 0
    t1 = time.perf_counter()
    amended = 0
    appended = 0
    skipped = 0
    for i in range(SAVES):
        r = vk.append_verkle_knot(dossier(hot, f"re{i}", tension=0.1 + i / 100))
        assert r.get("ok"), r
        amended += int(bool(r.get("amended")))
        appended += int(not r.get("amended") and not r.get("skipped"))
        skipped += int(bool(r.get("skipped")))
        now = chain_size()
        if mode == "v1":
            bytes_written += now  # amend rewrote the WHOLE file
        else:
            bytes_written += now - size_before  # append wrote one line
            size_before = now
    save_s = time.perf_counter() - t1

    ok, why = vk._verify_chain_consistent()
    return {
        "mode": mode, "seed_rows": SEED, "saves": SAVES,
        "seed_seconds": round(seed_s, 3),
        "saves_seconds": round(save_s, 3),
        "ms_per_save": round(save_s * 1000 / SAVES, 2),
        "bytes_written_during_saves": bytes_written,
        "mb_written_during_saves": round(bytes_written / 1e6, 2),
        "write_amplification_x": round(bytes_written / (chain_size() / 1e0), 1) if mode == "v1" else None,
        "final_rows": n_rows(),
        "amended": amended, "appended": appended, "skipped": skipped,
        "verify_ok": ok, "verify_why": why,
        "final_chain_bytes": chain_size(),
    }


def main() -> int:
    results = []
    with tempfile.TemporaryDirectory(prefix="ah19_bench_") as td:
        results.append(run("v1", Path(td) / "v1"))
    with tempfile.TemporaryDirectory(prefix="ah19_bench_") as td:
        results.append(run("v2", Path(td) / "v2"))

    v1, v2 = results
    speedup = round(v1["saves_seconds"] / v2["saves_seconds"], 1) if v2["saves_seconds"] else float("inf")
    print(json.dumps({"v1": v1, "v2": v2, "speedup_v1_over_v2": speedup}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
