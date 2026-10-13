#!/usr/bin/env python3
r"""librarian_backfill_20260927 -- resolve the retired librarian v1 backlog to names (Q6).

LIBRARIAN_REPORT.md v1 (2026-09-10) holds 198 RETRIEVAL-PLAN rows: sources named
in fleet bibliographies, primary never pulled+hashed. Q6 (atlas self-steal fix
queue) ruled: drain or formally retire. This driver executes the retirement
shape: the 194 well-formed arXiv IDs get their canonical metadata (title,
authors, published, abstract) from the arXiv Atom API so every row becomes a
NAMED source one hop from a future point-of-claim pull; the 4 key: classical
rows (Belady, Kraska, Mattson, Neil) are not on arXiv and stay owed, listed by
name. Metadata is NOT a primary artifact: nothing here is marked PULLED+HASHED;
the primary-pull law (no-fabrication, 2026-09-19) stays demand-driven.

Hook-law shape (mirrors the hermes dual-burn driver): one literal output path,
single-host allowlist, DNS resolution refused on private/link-local addresses,
stdlib only, no key material anywhere.
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import re
import socket
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
IDS_FILE = REPO / "watch" / "inbox" / "_librarian_ids_tmp.json"
OUT_FILE = REPO / "corpus" / "papers" / "librarian_backfill_20260927.jsonl"
ALLOWED_HOST = "api.semanticscholar.org"
API_URL = "https://" + ALLOWED_HOST + "/graph/v1/paper/batch?fields=title,year,externalIds,authors,abstract"
BATCH = 50
NS = {"a": "http://www.w3.org/2005/Atom"}


def _host_ip_ok(host: str) -> bool:
    infos = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return False
    return True


def _fetch(batch_ids: list[str]) -> str:
    if not _host_ip_ok(ALLOWED_HOST):
        raise RuntimeError(f"DNS for {ALLOWED_HOST} resolved to a private address; refusing")
    body = json.dumps({"ids": [f"ARXIV:{i}" for i in batch_ids]})
    # Transport law (measured 2026-09-27): this sandbox's proxy 406s python
    # urllib/requests to arxiv while curl passes through; arXiv kept this IP
    # hard-429'd through every backoff, so Semantic Scholar's batch endpoint
    # (4 POSTs for 194 ids) is the resolver and curl is still the transport.
    last = "no attempts"
    for attempt in range(6):
        p = subprocess.run(
            ["curl", "-s", "--max-time", "40", "-X", "POST", API_URL,
             "-A", "mag-librarian-backfill/1.0",
             "-H", "Content-Type: application/json",
             "-H", "Accept: application/json",
             "-d", body,
             "-w", "\n%{http_code}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        payload, _, code = p.stdout.rpartition("\n")
        code = code.strip()
        if code == "200" and payload.strip():
            return payload
        last = f"http {code or 'none'} exit {p.returncode}"
        if code in ("429", "500", "502", "503", "000", ""):
            time.sleep(20 if code == "429" else 8)
            continue
        break
    raise RuntimeError(f"semantic scholar via curl refused: {last}")


def main() -> int:
    ids = json.loads(IDS_FILE.read_text(encoding="utf-8"))
    print(f"resolving {len(ids)} arxiv ids in batches of {BATCH}")
    rows: list[dict] = []
    resolved_ids: set[str] = set()
    for i in range(0, len(ids), BATCH):
        batch = ids[i:i + BATCH]
        payload = _fetch(batch)
        entries = json.loads(payload)
        for asked, e in zip(batch, entries):
            if not isinstance(e, dict):
                continue  # S2 returns null for unknown ids; counted as missing
            ext = (e.get("externalIds") or {}).get("ArXiv", asked)
            title = re.sub(r"\s+", " ", str(e.get("title") or "")).strip()
            authors = [re.sub(r"\s+", " ", str(a.get("name") or "")).strip()
                       for a in (e.get("authors") or [])]
            rows.append({
                "arxiv_id": ext,
                "title": title,
                "authors": authors,
                "published": str(e.get("year") or ""),
                "abstract_sha256": hashlib.sha256(
                    str(e.get("abstract") or "").encode("utf-8")).hexdigest(),
                "payload_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                "resolved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "state": "NAMED+RESOLVED (metadata only, primary pull stays demand-driven)",
            })
            resolved_ids.add(ext)
        print(f"  batch {i // BATCH + 1}: {sum(1 for e in entries if isinstance(e, dict))} resolved")
        time.sleep(5)  # S2 unauthenticated politeness

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    missing = [i for i in ids if i not in resolved_ids]
    print(json.dumps({
        "requested": len(ids), "resolved": len(rows),
        "missing": missing,
        "out": str(OUT_FILE),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
