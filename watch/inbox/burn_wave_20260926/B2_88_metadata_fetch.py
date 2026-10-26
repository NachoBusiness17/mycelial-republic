#!/usr/bin/env python
"""B2-88 (2026-09-26): refetch the 314 metadata-only mrpool photos.

Class: CAPTION_LEDGER_20260926.jsonl rows status=metadata-only, file_ext=.jpg
(314 rows, all media_type=MessageMediaWebPage in mrpool_export/ledger_full.jsonl,
msg 176 at ledger_full line 3662 is the shape). The export never downloaded
these files to disk, no sha256 exists for the class, so nothing is verified
against a prior hash: every recovered file is recorded with the sha256 of the
bytes actually fetched from the public t.me/s/MrPool_Q web preview, its real
byte count, and whether that count matches the export's file_size metadata
(known placeholder-heavy: 262 of 314 rows share file_size 33881).

Phases (separate CLI arms so a network failure never loses prior work):
  crawl   page the public web preview newest -> oldest, collect per-message
          image candidates, checkpoint to B2_88_crawl_map.json every 25 pages
  fetch   download candidates for the 314 targets into
          mrpool_export/media_recovered_20260926/, sha256 each file,
          write media_recovered_register_20260926.jsonl (recovered) and
          metadata_unreachable_20260926.jsonl (exactly which stayed unreachable)
  report  print the counts from the two output files

No fabrication: a target is recovered only if real bytes came back over HTTP
and landed on disk; a target with no bubble, no image candidate, or a failed
download is recorded unreachable with the reason. Nothing is synthesized.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_88_metadata_fetch.py crawl|fetch|report
"""
import hashlib
import json
import re
import sys
import time
import urllib.request
import gzip
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BURN = ROOT / "watch" / "inbox" / "burn_wave_20260926"
EXPORT = ROOT / "watch" / "inbox" / "mrpool_export"
CAPTION_LEDGER = ROOT / "watch" / "inbox" / "CAPTION_LEDGER_20260926.jsonl"
CRAWL_MAP = BURN / "B2_88_crawl_map.json"
RECOVER_DIR = EXPORT / "media_recovered_20260926"
RECOVER_REG = EXPORT / "media_recovered_register_20260926.jsonl"
UNREACH = EXPORT / "metadata_unreachable_20260926.jsonl"
CHANNEL_URL = "https://t.me/s/MrPool_Q"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) B2-88-metadata-fetch/1.0"
PACE = 0.25
CHECKPOINT_EVERY = 25


def targets():
    out = []
    for line in open(CAPTION_LEDGER, encoding="utf-8"):
        r = json.loads(line)
        if r["status"] == "metadata-only" and r["file_ext"] == ".jpg":
            out.append(r)
    return out


def http_get(url, binary=False, tries=4):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            raw = urllib.request.urlopen(req, timeout=40).read()
            if raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            return raw if binary else raw.decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001 - network path, log and retry
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after {tries} tries: {url}: {last}")


def parse_bubbles(html):
    """Return {int post_id: {"photo": [urls], "thumb": [urls]}} for one page."""
    found = {}
    parts = re.split(r'(?=<div class="tgme_widget_message_wrap)', html)
    for b in parts:
        m = re.search(r'data-post="MrPool_Q/(\d+)"', b)
        if not m:
            continue
        pid = int(m.group(1))
        entry = {"photo": [], "thumb": []}
        # real photo bubbles
        entry["photo"] += re.findall(
            r'class="tgme_widget_message_photo[^"]*"[^>]*src="([^"]+)"', b)
        # link preview thumbnails (the MessageMediaWebPage visual)
        entry["thumb"] += re.findall(
            r'link_preview_\w*image"[^>]*background-image:url\(\'([^\'"]+)\'', b)
        entry["thumb"] += re.findall(
            r'tgme_widget_message_link_preview[^>]*style="[^"]*url\(\'([^\'"]+)\'', b)
        # any remaining cdn image inside the bubble body (fallback)
        extra = [u for u in re.findall(r'src="(https://cdn\d+\.telesco\.pe/[^"]+)"', b)]
        for u in extra:
            if u not in entry["photo"] and u not in entry["thumb"]:
                entry["thumb"].append(u)
        if entry["photo"] or entry["thumb"]:
            found[pid] = entry
    return found


def cmd_crawl():
    min_target = min(r["msg_id"] for r in targets())
    cmap = {}
    seen_pages = 0
    url = CHANNEL_URL
    lowest = None
    while url:
        html = http_get(url)
        seen_pages += 1
        page = parse_bubbles(html)
        cmap.update(page)
        ids = sorted(page)
        lowest = min(ids) if ids else None
        if lowest is None or lowest <= min_target:
            break
        url = f"{CHANNEL_URL}?before={lowest}"
        time.sleep(PACE)
        if seen_pages % CHECKPOINT_EVERY == 0:
            CRAWL_MAP.write_text(json.dumps(cmap), encoding="utf-8")
            print(f"checkpoint pages={seen_pages} ids={len(cmap)} lowest={lowest}", flush=True)
    CRAWL_MAP.write_text(json.dumps(cmap), encoding="utf-8")
    hit = sum(1 for r in targets() if r["msg_id"] in cmap)
    print(f"CRAWL DONE pages={seen_pages} bubbles_with_images={len(cmap)} "
          f"targets_hit={hit}/314 lowest_id_seen={lowest} min_target={min_target}")


def cmd_fetch():
    cmap = json.loads(CRAWL_MAP.read_text(encoding="utf-8"))
    cmap = {int(k): v for k, v in cmap.items()}
    RECOVER_DIR.mkdir(parents=True, exist_ok=True)
    rows, unreach = [], []
    for r in sorted(targets(), key=lambda x: x["msg_id"]):
        cite = r["cite"]
        mid = r["msg_id"]
        entry = cmap.get(mid)
        if entry is None:
            unreach.append({"cite": cite, "msg_id": mid,
                            "reason": "no bubble with image candidates in t.me/s preview (deleted or not publicly rendered)"})
            continue
        candidates = [("photo", u) for u in entry["photo"]] + [("thumb", u) for u in entry["thumb"]]
        got = None
        errors = []
        for kind, u in candidates:
            try:
                raw = http_get(u, binary=True)
            except Exception as e:  # noqa: BLE001
                errors.append(f"{kind}: {e}")
                continue
            if len(raw) < 64:
                errors.append(f"{kind}: {len(raw)} bytes only")
                continue
            magic = "jpeg" if raw[:3] == b"\xff\xd8\xff" else ("png" if raw[:8] == b"\x89PNG\r\n\x1a\n" else "unknown")
            if magic == "unknown":
                errors.append(f"{kind}: not a jpeg/png payload ({raw[:16].hex()})")
                continue
            got = {"kind": kind, "url": u, "raw": raw, "magic": magic}
            break
        if got is None:
            unreach.append({"cite": cite, "msg_id": mid,
                            "reason": "image candidates failed to download or were not image bytes: " + "; ".join(errors[:3])})
            continue
        raw = got["raw"]
        sha = hashlib.sha256(raw).hexdigest()
        ext = ".jpg" if got["magic"] == "jpeg" else ".png"
        path = RECOVER_DIR / f"msg_{mid}{ext}"
        path.write_bytes(raw)
        rows.append({
            "cite": cite,
            "msg_id": mid,
            "file": f"media_recovered_20260926/msg_{mid}{ext}",
            "sha256": sha,
            "bytes": len(raw),
            "ledger_file_size": r["bytes"],
            "size_matches_export_metadata": len(raw) == r["bytes"],
            "provenance": f"t.me/s/MrPool_Q web preview {got['kind']} image, fetched 2026-09-26",
            "source_url": got["url"],
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
    with open(RECOVER_REG, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    with open(UNREACH, "w", encoding="utf-8") as f:
        for row in unreach:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"FETCH DONE recovered={len(rows)} unreachable={len(unreach)}")


def cmd_report():
    rows = [json.loads(l) for l in open(RECOVER_REG, encoding="utf-8")]
    un = [json.loads(l) for l in open(UNREACH, encoding="utf-8")]
    match = sum(1 for x in rows if x["size_matches_export_metadata"])
    total = len(rows) + len(un)
    print(f"recovered={len(rows)} unreachable={len(un)} total={total} "
          f"size_match_export_meta={match}/{len(rows)}")
    print("reasons:", {})
    import collections
    print(collections.Counter(x["reason"].split(":")[0] for x in un))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "crawl":
        cmd_crawl()
    elif cmd == "fetch":
        cmd_fetch()
    elif cmd == "report":
        cmd_report()
    else:
        print("usage: B2_88_metadata_fetch.py crawl|fetch|report")
        sys.exit(2)
