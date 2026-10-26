"""full_scan — the estate-wide semantic catalog churn (2026-09-23, "go wide").

v2: per-lane worker threads pull from a shared queue (serial per lane = no
rate-limit storms). One brief-chore per text record: a plain-English one-liner
saying what the record is. Output: state/fuel/record_briefs.jsonl — the semantic
layer of the Librarian's catalog. Scope law: project folders only.
"""
from __future__ import annotations

import json
import os
import queue
import sys
import threading
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from models.env_load import load_dotenv
load_dotenv()
from mag import lite_guard  # noqa: E402

BRIEFS = ROOT / "state" / "fuel" / "record_briefs.jsonl"
LEDGER = ROOT / "state" / "fuel" / "full_scan_ledger.jsonl"
REPORT = ROOT / "watch" / "inbox" / "FULL_SCAN_REPORT_20260923.md"

WALKS = [
    ROOT / "watch",
    ROOT / "docs" / "ref",
    ROOT / "handoff",
    ROOT / "corpus" / "canon",
    ROOT / "corpus" / "game_estate",
    ROOT / "corpus" / "tartaria_lives",
    ROOT / "corpus" / "telegram",
]
LANE_DEFS = [
    ("nous-qwen38flash", "https://inference-api.nousresearch.com/v1/chat/completions", "qwen/qwen3.8-flash", ["HERMES_API_KEY_1", "HERMES_API_KEY_2"], 1),
    ("deepseek-chat", "https://api.deepseek.com/chat/completions", "deepseek-chat", ["DEEPSEEK_API_KEY"], 1),
    ("openrouter-a1", "https://openrouter.ai/api/v1/chat/completions", "openrouter/auto", ["OPENROUTER_API_KEY"], 1),
    ("openrouter-a2", "https://openrouter.ai/api/v1/chat/completions", "openrouter/auto", ["OPENROUTER_API_KEY_2"], 1),
    ("nvidia-glm53", "https://integrate.api.nvidia.com/v1/chat/completions", "z-ai/glm-5.3-flash", ["NVIDIABuild"], 1),
    ("groq-oss120", "https://api.groq.com/openai/v1/chat/completions", "openai/gpt-oss-120b", ["GROQ_API_KEY"], 1),
    ("groq2-oss120", "https://api.groq.com/openai/v1/chat/completions", "openai/gpt-oss-120b", ["GROQ_API_KEY_2"], 1),
    ("nvidia-dsv41", "https://integrate.api.nvidia.com/v1/chat/completions", "deepseek-ai/deepseek-v4.1-flash", ["NVIDIABuild"], 1),
    ("zai-key2-glm47", "https://api.z.ai/api/paas/v4/chat/completions", "glm-4.7-flash", ["ZAI_API_KEY_2"], 1),
]

stats = {"ok": 0, "fail": 0, "skipped": 0}
stats_lock = threading.Lock()


def key_for(names):
    for n in names:
        k = (os.environ.get(n, "") or "").strip()
        if k:
            return k
    return ""


class Lane:
    def __init__(self, name, url, model, keynames, conc):
        self.name = name
        self.url = url
        self.model = model
        self.key = key_for(keynames)
        self.alive = bool(self.key)
        self.conc = conc


LANES = [Lane(n, u, m, ks, c) for n, u, m, ks, c in LANE_DEFS if key_for(ks)]


def call(lane, prompt):
    if not lite_guard._safe_https_url(lane.url):
        return "[ssrf-blocked]"
    payload = {"model": lane.model,
               "messages": [{"role": "user", "content": prompt}],
               "max_tokens": 500, "temperature": 0}
    req = urllib.request.Request(lane.url, data=json.dumps(payload).encode(), headers={
        "Authorization": "Bearer " + lane.key, "Content-Type": "application/json"})
    try:
        with lite_guard._OPENER.open(req, timeout=180) as r:
            d = json.loads(r.read().decode())
        msg = (d.get("choices") or [{}])[0].get("message", {}) or {}
        content = (msg.get("content") or "").strip()
        if not content:
            payload["thinking"] = {"type": "disabled"}
            payload["max_tokens"] = 500
            req2 = urllib.request.Request(lane.url, data=json.dumps(payload).encode(), headers={
                "Authorization": "Bearer " + lane.key, "Content-Type": "application/json"})
            with lite_guard._OPENER.open(req2, timeout=180) as r2:
                d2 = json.loads(r2.read().decode())
            msg2 = (d2.get("choices") or [{}])[0].get("message", {}) or {}
            content = (msg2.get("content") or "").strip() or (msg2.get("reasoning_content") or "").strip()[:300]
        return content
    except urllib.error.HTTPError as e:
        if e.code == 429:
            time.sleep(30)
        return "[429]"
    except Exception as e:
        return "[fail:" + type(e).__name__ + ": " + str(e)[:100] + "]"


def brief_one(path: Path, lane: Lane) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except Exception as e:
        return {"path": str(path), "brief": "[unreadable: " + type(e).__name__ + "]"}
    prompt = ("Read this estate record. Output ONE line in plain English — "
              "what this record is, max 25 words, no preamble:\n\n" + text)
    brief = call(lane, prompt)
    return {"path": str(path), "brief": brief, "lane": lane.name,
            "ts": datetime.now(timezone.utc).isoformat()}


def collect_records():
    records = []
    seen = set()
    if BRIEFS.is_file():
        for line in BRIEFS.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                seen.add(json.loads(line).get("path"))
            except Exception:
                continue
    for base in WALKS:
        if not base.is_dir():
            continue
        for dp, _dn, fns in os.walk(base):
            for fn in fns:
                if not fn.lower().endswith((".md", ".txt")):
                    continue
                fp = Path(dp) / fn
                if str(fp) in seen:
                    continue
                try:
                    if fp.stat().st_size > 2_000_000:
                        continue
                except OSError:
                    continue
                records.append(fp)
    return records


def main(budget_minutes: int = 240) -> dict:
    records = collect_records()
    q: queue.Queue = queue.Queue()
    attempts: dict = {}
    attempts_lock = threading.Lock()
    MAX_ATTEMPTS = 3
    for fp in records:
        q.put((fp, 1))
    print("full_scan v2: %d records, %d lanes, budget %d min" % (len(records), len(LANES), budget_minutes), flush=True)
    deadline = time.time() + budget_minutes * 60

    def lane_worker(lane: Lane):
        last_call = 0.0
        while time.time() < deadline:
            try:
                fp, attempt = q.get_nowait()
            except queue.Empty:
                return
            # per-lane pacing: >=5.0s between calls enforces INVARIANT-20261017-03
            wait = 5.0 - (time.time() - last_call)
            if wait > 0:
                time.sleep(wait)
            last_call = time.time()
            row = brief_one(fp, lane)
            good = not row["brief"].startswith("[")
            if good:
                with stats_lock:
                    stats["ok"] = stats.get("ok", 0) + 1
                # only successful briefs enter the semantic catalog
                append_jsonl(BRIEFS, row)
                append_ledger({"ts": now_iso(), "lane": lane.name,
                               "path": row["path"], "brief": row["brief"][:80], "ok": True})
            elif attempt < MAX_ATTEMPTS:
                with attempts_lock:
                    attempts[row["path"]] = attempts.get(row["path"], 1) + 1
                q.put((fp, attempt + 1))
            else:
                with stats_lock:
                    stats["fail"] = stats.get("fail", 0) + 1
                append_ledger({"ts": now_iso(), "lane": lane.name,
                               "path": row["path"], "brief": row["brief"][:80], "ok": False})

    threads = [threading.Thread(target=lane_worker, args=(l,), daemon=True) for l in LANES]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=max(1, deadline - time.time()))

    return {"records": len(records), "ok": stats.get("ok", 0), "fail": stats.get("fail", 0),
            "remaining": q.qsize()}


def append_ledger(obj):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")


def append_jsonl(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    mins = int(sys.argv[sys.argv.index("--budget-minutes") + 1]) if "--budget-minutes" in sys.argv else 240
    result = main(mins)
    print(json.dumps(result, indent=1))
    md = ["# FULL SCAN — semantic catalog churn",
          "",
          "run %s — records: %d — ok: %d — fail: %d — remaining in queue: %d" % (
              now_iso(), result["records"], result["ok"], result["fail"], result["remaining"]),
          "",
          "briefs: state/fuel/record_briefs.jsonl · ledger: state/fuel/full_scan_ledger.jsonl"]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "watch" / "inbox" / "FULL_SCAN_REPORT_20260923.md").write_text("\n".join(md), encoding="utf-8")
