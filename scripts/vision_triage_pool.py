#!/usr/bin/env python3
"""vision_triage_pool.py — Mr Pool image triage, batches 7+ (resumes the inline
runs lost to the 2026-09-19 ZCode update at 1,017 unique / 2,011).

Rebuilds the lost inline driver as a persisted script. Fixes three defects the
inline runs had: (1) idempotent — msg_ids already in vision_triage.jsonl are
skipped, so a rerun never double-counts (the old runs wrote 23 duplicate rows);
(2) model provenance recorded per batch (old reading files named no lane);
(3) transport deaths (429/timeout) land in `errors`, never in `triaged` —
per the 2026-09-19 law: instruments that cannot distinguish reached-the-gate
from died-in-transit file no verdict.

Lanes:
  local  ollama qwen2.5vl:3b  (sovereign, unlimited, weaker)
  groq   meta-llama/llama-4-scout-17b-16e-instruct (free tier, stronger, paced)

SSRF posture (same as mag/verb.py + scripts/endpoint_news.py): fixed URLs,
scheme+host pinned, resolved-IP boundary check (loopback-pinned for the local
lane, global-only for the remote lane), redirects refused.

Usage:
  python scripts/vision_triage_pool.py --calibrate 3          # compare lanes
  python scripts/vision_triage_pool.py --run --lane local     # batches 7-10
"""
from __future__ import annotations

import argparse
import base64
import ipaddress
import json
import re
import socket
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MRP = ROOT / "watch" / "inbox" / "mrpool_export"
TRIAGE = MRP / "vision_triage.jsonl"
MEDIA = MRP / "media_full"

PROMPT = (
    "Archive triage of this image. Answer in EXACTLY this format:\n"
    "TYPE: photo|screenshot|meme|art|document|other\n"
    "SUBJECT: one line, what is depicted\n"
    "TEXT: all visible text verbatim, or NONE\n"
    "SYMBOLS: comma list of any of eye, pyramid, water, bridge, numbers, "
    "clock, door, skull, key, trump — or none"
)
SYMBOL_VOCAB = ["eye", "pyramid", "water", "bridge", "numbers", "clock",
                "door", "skull", "key", "trump"]

LOCAL_MODEL = "qwen2.5vl:3b"
LOCAL_URL = "http://127.0.0.1:11434/api/generate"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def env_key(name: str) -> str:
    env = ROOT / ".env"
    if env.exists():
        for ln in env.read_text(encoding="utf-8", errors="replace").splitlines():
            ln = ln.strip()
            if ln.startswith(name + "="):
                return ln.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def guarded_post(url: str, boundary: str, data: bytes, headers: dict,
                 timeout: int) -> dict:
    """Hardened POST: pin scheme+host, verify resolved IPs against the boundary,
    refuse redirects. boundary is 'loopback' (local ollama pin) or 'global'."""
    p = urllib.parse.urlparse(url)
    port = p.port or (443 if p.scheme == "https" else 80)
    if boundary == "loopback":
        if p.scheme != "http" or p.hostname != "127.0.0.1" or port != 11434:
            raise ValueError("local endpoint not allowed")
        check = lambda ip: ipaddress.ip_address(ip).is_loopback
    else:
        if p.scheme != "https" or p.hostname != "api.groq.com":
            raise ValueError("host not allowed")
        check = lambda ip: ipaddress.ip_address(ip).is_global
    for _f, _s, _pr, _c, sa in socket.getaddrinfo(p.hostname, port):
        if not check(sa[0]):
            raise ValueError("resolved address outside allowed boundary")
    req = urllib.request.Request(url, data=data, headers=headers)
    opener = urllib.request.build_opener(_NoRedirect)
    with opener.open(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def ask_local(img: Path) -> str:
    body = {"model": LOCAL_MODEL, "prompt": PROMPT, "images": [b64(img)],
            "stream": False, "options": {"temperature": 0.1, "num_predict": 300}}
    d = guarded_post(LOCAL_URL, "loopback", json.dumps(body).encode("utf-8"),
                     {"Content-Type": "application/json"}, timeout=180)
    return d.get("response", "")


def ask_groq(img: Path, key: str) -> str:
    body = {
        "model": GROQ_MODEL, "temperature": 0.1, "max_tokens": 400,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url",
             "image_url": {"url": f"data:image/jpeg;base64,{b64(img)}"}},
        ]}],
    }
    d = guarded_post(GROQ_URL, "global", json.dumps(body).encode("utf-8"),
                     {"Authorization": f"Bearer {key}",
                      "Content-Type": "application/json",
                      "User-Agent": "mag-vision-triage/1.0"}, timeout=120)
    return (d["choices"][0]["message"].get("content") or "").strip()


def parse_symbols(reading: str) -> set:
    """Vocab match on the SYMBOLS line. Negation clauses ("no eyes, pyramids",
    "none") are consumed up to the next semicolon so a negated mention never
    counts — the recorded rows use that style and a naive match would inflate
    the census."""
    low = reading.lower()
    if "symbols:" not in low:
        return set()
    tail = low.split("symbols:")[-1][:200]
    cleaned = re.sub(r"\b(no|none|not|without)\b[^;]*", " ", tail)
    return {s for s in SYMBOL_VOCAB if s in cleaned}


def done_ids() -> set:
    ids = set()
    if TRIAGE.exists():
        for ln in TRIAGE.open(encoding="utf-8"):
            if ln.strip():
                try:
                    ids.add(json.loads(ln)["msg_id"])
                except json.JSONDecodeError:
                    continue
    return ids


def batch_paths(n_per: int = 200) -> list:
    remaining = sorted((p for p in MEDIA.glob("msg_*.jpg")
                        if int(p.stem.split("_")[1]) not in done_ids()),
                       key=lambda p: -int(p.stem.split("_")[1]))
    return [remaining[i:i + n_per] for i in range(0, len(remaining), n_per)]


def run_batch(idx: int, paths: list, lane: str, key: str, pause: float) -> dict:
    model = LOCAL_MODEL if lane == "local" else GROQ_MODEL
    rows, errors = [], []
    syms: dict[str, int] = {}
    for i, img in enumerate(paths):
        mid = int(img.stem.split("_")[1])
        try:
            reading = ask_local(img) if lane == "local" else ask_groq(img, key)
            if not reading.strip():
                raise RuntimeError("empty content")
            rows.append({"msg_id": mid, "file": f"media_full/{img.name}",
                         "reading": reading.strip()})
            for s in parse_symbols(reading.strip()):
                syms[s] = syms.get(s, 0) + 1
        except Exception as e:
            errors.append({"msg_id": mid, "error": f"{type(e).__name__}: {e}"[:160]})
        if pause and (i + 1) % 10 == 0:
            time.sleep(pause)
        if (i + 1) % 25 == 0:
            print(f"  batch{idx}: {i+1}/{len(paths)} ok={len(rows)} err={len(errors)}", flush=True)
    out = {"batch": idx, "model": model, "lane": lane,
           "triaged": len(rows), "errors": len(errors),
           "symbols": syms,
           "coverage": None,
           "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
    with (MRP / f"VISION_READING_B{idx}.json").open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with TRIAGE.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if errors:
        with (MRP / "vision_errors.jsonl").open("a", encoding="utf-8") as f:
            for e in errors:
                f.write(json.dumps({**e, "batch": idx, "lane": lane},
                                   ensure_ascii=False) + "\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", type=int, default=0)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--lane", choices=["local", "groq"], default="local")
    ap.add_argument("--batches", type=int, default=99, help="max batches this fire")
    ap.add_argument("--pause", type=float, default=1.0, help="seconds each 10 imgs (groq pacing)")
    a = ap.parse_args()
    key = env_key("GROQ_API_KEY")

    if a.calibrate:
        ids = sorted(done_ids())[: a.calibrate]
        for mid in ids:
            img = MEDIA / f"msg_{mid}.jpg"
            known = ""
            for ln in TRIAGE.open(encoding="utf-8"):
                if ln.strip() and json.loads(ln).get("msg_id") == mid:
                    known = json.loads(ln)["reading"]
                    break
            print(f"=== msg_{mid} RECORDED ===\n{known[:300]}\n")
            for lane in ("local", "groq"):
                try:
                    ans = ask_local(img) if lane == "local" else ask_groq(img, key)
                    print(f"--- {lane} ---\n{ans[:300]}\n")
                except Exception as e:
                    print(f"--- {lane} ERROR: {e}\n")
        return 0

    if a.run:
        batches = batch_paths()
        print(f"remaining images: {sum(len(b) for b in batches)} in {len(batches)} batches")
        nums = []
        for p in MRP.glob("VISION_READING_B*.json"):
            m = re.match(r"VISION_READING_B(\d+)\.json", p.stem + ".json")
            if m:
                nums.append(int(m.group(1)))
        base = max(nums or [6])
        fired = 0
        for off, paths in enumerate(batches[: a.batches]):
            idx = base + 1 + off
            print(f"batch {idx}: {len(paths)} images on {a.lane}", flush=True)
            out = run_batch(idx, paths, a.lane, key, a.pause)
            total = len(done_ids())
            out["coverage"] = f"{total}/2011"
            print(f"batch {idx} done: triaged={out['triaged']} errors={out['errors']} coverage={out['coverage']}", flush=True)
            fired += 1
        print(f"FIRED {fired} batches")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
