#!/usr/bin/env python3
"""vision_nightly.py — THE 50 W9 T44: unattended nightly driver for the Mr Pool
vision triage backlog (engine: scripts/vision_triage_pool.py).

Fires nightly (Windows Task Scheduler, see scripts/register_vision_nightly.ps1).
Idempotent by construction: vision_triage_pool skips msg_ids already in
vision_triage.jsonl, so a complete corpus is an honest no-op, new media or
future error rows are drained automatically, and transport deaths (429/timeout)
land in vision_errors.jsonl, never in triaged rows.

Modes:
  --dry-run   no inference. Env checks + coverage snapshot + the plan the run
              WOULD fire. Appends a receipt row. The wiring proof.
  --smoke     one real local-lane inference on an already-recorded image via
              the pool's guarded POST path. Read-only (no triage rows written).
              The live proof that the exact inference path works.
  --run       the nightly fire: delegates to vision_triage_pool --run --lane
              local --batches N (default 1, paced). Env not ready = clean skip
              receipt, exit 0 (unattended cron must not error-spam).

Receipts: watch/inbox/mrpool_export/vision_nightly_receipts.jsonl
Log:      logs/vision_nightly.log

Usage: .venv\\Scripts\\python.exe scripts\\vision_nightly.py --dry-run|--smoke|--run
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

MRP = ROOT / "watch" / "inbox" / "mrpool_export"
RECEIPTS = MRP / "vision_nightly_receipts.jsonl"
LOG = ROOT / "logs" / "vision_nightly.log"
TRIAGE = MRP / "vision_triage.jsonl"

LOCAL_TAGS_URL = "http://127.0.0.1:11434/api/tags"
VISION_MODEL = "qwen2.5vl:3b"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def log(msg: str) -> None:
    """Append one timestamped line to the nightly log (and stdout)."""
    line = f"[{datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}] {msg}"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def receipt(row: dict) -> None:
    """Append one JSONL receipt row (json.dumps, never heredoc)."""
    row = {"ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
           "mode": MODE[0], **row}
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    with RECEIPTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


MODE = ["unknown"]


def ollama_ready() -> tuple[bool, str]:
    """Loopback-pinned GET of /api/tags (same SSRF posture as the pool script:
    scheme+host pinned, resolved-IP boundary check, redirects refused)."""
    p = urllib.parse.urlparse(LOCAL_TAGS_URL)
    if p.scheme != "http" or p.hostname != "127.0.0.1" or (p.port or 80) != 11434:
        return False, "tags url not loopback-pinned"
    for _f, _s, _pr, _c, sa in socket.getaddrinfo(p.hostname, p.port or 80):
        if not ipaddress.ip_address(sa[0]).is_loopback:
            return False, "resolved address outside loopback boundary"
    req = urllib.request.Request(LOCAL_TAGS_URL)
    try:
        opener = urllib.request.build_opener(_NoRedirect)
        with opener.open(req, timeout=10) as r:
            tags = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
    names = [m.get("name", "") for m in tags.get("models", [])]
    if VISION_MODEL not in names:
        return False, f"{VISION_MODEL} not served (have: {', '.join(names[:6])}...)"
    return True, "ok"


def coverage() -> dict:
    """Decidable health: media_full vs triage. Also ledger size for context
    (full universe re-derivation is a separate filed debt, not this job)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import vision_triage_pool as pool
    done = pool.done_ids()
    media = {int(p.stem.split("_")[1]) for p in pool.MEDIA.glob("msg_*.jpg")}
    ledger = set()
    lf = MRP / "ledger_full.jsonl"
    if lf.exists():
        for ln in lf.open(encoding="utf-8"):
            if ln.strip():
                try:
                    mid = json.loads(ln).get("msg_id")
                    if mid is not None:
                        ledger.add(int(mid))
                except (json.JSONDecodeError, ValueError, TypeError):
                    continue
    remaining = sorted(media - done)
    return {
        "media_full": len(media),
        "triaged_unique": len(done),
        "remaining": len(remaining),
        "coverage_pct": round(100.0 * len(done & media) / len(media), 1) if media else None,
        "ledger_ids_total": len(ledger),
        "next_batch_would_fire": len(remaining) > 0,
    }


def pick_smoke_image() -> Path | None:
    """Smallest already-recorded image: fastest honest probe of the real path."""
    if not TRIAGE.exists():
        return None
    ids = set()
    for ln in TRIAGE.open(encoding="utf-8"):
        if ln.strip():
            try:
                ids.add(int(json.loads(ln)["msg_id"]))
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    cands = sorted(((p.stat().st_size, p) for p in (MRP / "media_full").glob("msg_*.jpg")
                    if int(p.stem.split("_")[1]) in ids))
    return cands[0][1] if cands else None


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--smoke", action="store_true")
    g.add_argument("--run", action="store_true")
    ap.add_argument("--batches", type=int, default=1,
                    help="max batches per nightly fire (default 1 = up to 200 images)")
    a = ap.parse_args()
    MODE[0] = "dry_run" if a.dry_run else ("smoke" if a.smoke else "run")

    log(f"START mode={MODE[0]}")
    ready, why = ollama_ready()
    cov = coverage()
    log(f"ollama={'ready' if ready else 'DOWN'} ({why}); coverage={cov['triaged_unique']}/{cov['media_full']} remaining={cov['remaining']}")

    if a.dry_run:
        receipt({"ok": ready, "ollama": why, **cov,
                 "would": "vision_triage_pool --run --lane local "
                          f"--batches {a.batches} (schedule: MagVisionNightly daily 02:30)"})
        log(f"DRY-RUN plan: fire={cov['next_batch_would_fire']} batches={a.batches} lane=local")
        log("END ok=1 (dry-run, no inference fired)")
        return 0 if ready else 2

    if a.smoke:
        if not ready:
            receipt({"ok": False, "skipped": f"ollama not ready: {why}", **cov})
            log("END skip (env not ready)")
            return 0
        import vision_triage_pool as pool
        img = pick_smoke_image()
        if img is None:
            receipt({"ok": False, "skipped": "no recorded image to smoke against", **cov})
            log("END skip (no image)")
            return 0
        t0 = time.time()
        try:
            reading = pool.ask_local(img).strip()
            ok = bool(reading)
            head = reading[:80].replace("\n", " / ")
        except Exception as e:
            ok, head = False, f"{type(e).__name__}: {e}"[:160]
        dt = round(time.time() - t0, 1)
        receipt({"ok": ok, "img": img.name, "sec": dt, "reading_head": head,
                 "lane": "local", "model": pool.LOCAL_MODEL, **cov})
        log(f"SMOKE {'OK' if ok else 'FAIL'} {img.name} {dt}s head={head!r}")
        log(f"END ok={int(ok)} (smoke, read-only: no triage rows written)")
        return 0 if ok else 3

    # --run: the nightly fire.
    if not ready:
        receipt({"ok": False, "skipped": f"ollama not ready: {why}", **cov})
        log("END skip (env not ready, clean receipt filed)")
        return 0
    if not cov["next_batch_would_fire"]:
        receipt({"ok": True, "fired": 0, "note": "corpus complete, idempotent no-op", **cov})
        log("END no-op (0 remaining, corpus complete)")
        return 0
    cmd = [str(ROOT / ".venv" / "Scripts" / "python.exe"),
           str(ROOT / "scripts" / "vision_triage_pool.py"),
           "--run", "--lane", "local", "--batches", str(a.batches), "--pause", "1.0"]
    log(f"FIRE {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=4 * 60 * 60)
    for ln in (r.stdout or "").splitlines()[-20:]:
        log(f"  pool| {ln}")
    if r.returncode != 0:
        log(f"  pool stderr tail: {(r.stderr or '')[-400:]!r}")
    cov_after = coverage()
    triaged_this_fire = cov_after["triaged_unique"] - cov["triaged_unique"]
    receipt({"ok": r.returncode == 0, "fired": 1, "batches": a.batches,
             "exit": r.returncode, "triaged_this_fire": triaged_this_fire,
             **cov_after})
    log(f"END exit={r.returncode} triaged_this_fire={triaged_this_fire}")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
