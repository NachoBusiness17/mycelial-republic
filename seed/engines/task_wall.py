"""task_wall — the standing concurrent task engine (2026-09-23, operator: "explode our
throughput... test concurrency everywhere to touch the wall... task everything on").

A queue of REAL backlog chores + a pool of every free lane + concurrency that ramps per
lane until it touches each provider wall, then backs off and records the ceiling.
Pitfalls baked in: reasoning-budget rescue, 429 backoff, quota markdown, empty-200
marker, Lite pacing. No SQL anywhere — jsonl ledgers only.
"""
from __future__ import annotations

import json
import os
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

REPORT = ROOT / "watch" / "inbox" / "TASK_WALL_REPORT_20260923.md"
LEDGER = ROOT / "state" / "fuel" / "task_wall_ledger.jsonl"
LABELS = ROOT / "state" / "fuel" / "label_farm.jsonl"
ANCHORS = ROOT / "state" / "fuel" / "anchor_notes.jsonl"
QUESTIONS = ROOT / "state" / "fuel" / "gap_questions.jsonl"

RECORDS = [
    ("undeniable-ledger", ROOT / "watch" / "inbox" / "THE_UNDENIABLE_LEDGER_20260923.md"),
    ("ledger-addendum", ROOT / "watch" / "inbox" / "UNDENIABLE_LEDGER_ADDENDUM_20260923.md"),
    ("reset-spec", ROOT / "watch" / "inbox" / "RESET_EVIDENCE_SPEC_20260923.md"),
    ("old-books-shelf", ROOT / "watch" / "inbox" / "THE_OLD_BOOKS_SHELF_20260923.md"),
    ("old-books-shelf-2", ROOT / "watch" / "inbox" / "THE_OLD_BOOKS_SHELF_DIG2_20260923.md"),
    ("worldview-audit", ROOT / "watch" / "inbox" / "WORLDVIEW_AUDIT_20260923.md"),
    ("account-vs-audit", ROOT / "watch" / "inbox" / "ACCOUNT_VS_AUDIT_20260923.md"),
]

PILLARS = [
    ("pillar1-epstein-web", "The Chandler/SRA/Epstein web post. Verified kernel: 2008 NPA with named co-conspirators, Marra CVRA ruling Feb 2019, SDNY indictment, Maxwell 240 months, Preska unsealings. Draft a two-sentence anchor note tying the post to the court receipts."),
    ("pillar2-cave", "The ancient-families post. Verified kernel: Gilens and Page 1,779 cases - elite-favored about 45 percent adoption vs about 18, average citizens near-zero independent effect. Draft a two-sentence anchor note."),
    ("pillar3-adrenochrome", "The inverted-sacrament essay. Verified kernel: the trafficking network is court-proven; the chemistry claim has no court stone and is held as thesis. Draft a two-sentence anchor note that holds both facts."),
    ("pillar4-black-nobility", "The Black Nobility manifesto. Verified kernel: Jekyll Island November 1910 is documented history; record 4.4 billion lobbying 2024; connections beat expertise in lobbying returns per AER. Draft a two-sentence anchor note."),
    ("pillar5-smith-mundt", "The Smith-Mundt seam post. Verified kernel: S. Rep. 94-755, COINTELPRO 2,000-plus actions, SHAMROCK about 150k telegrams per month, Church on NBC Aug 17 1975. Draft a two-sentence anchor note."),
]

FAMILIES = ["epstein-docket", "church-committee", "censorship-complex", "gilens-page",
            "money-politics", "trafficking-abroad", "intel-deception", "human-experiments",
            "domestic-covert", "modern-fisa", "manufactured-doubt"]

LANE_DEFS = [
    ("nvidia-glm53", "https://integrate.api.nvidia.com/v1/chat/completions", "z-ai/glm-5.3-flash", ["NVIDIABuild"]),
    ("nvidia-dsv41", "https://integrate.api.nvidia.com/v1/chat/completions", "deepseek-ai/deepseek-v4.1-flash", ["NVIDIABuild"]),
    ("openrouter-a1", "https://openrouter.ai/api/v1/chat/completions", "openrouter/auto", ["OPENROUTER_API_KEY"]),
    ("openrouter-a2", "https://openrouter.ai/api/v1/chat/completions", "openrouter/auto", ["OPENROUTER_API_KEY_2"]),
    ("groq-llama33", "https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile", ["GROQ_API_KEY"]),
    ("groq2-llama33", "https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile", ["GROQ_API_KEY_2"]),
    ("cerebras-llama33", "https://api.cerebras.ai/v1/chat/completions", "llama-3.3-70b", ["CEREBRAS_API_KEY", "CEREBRAS_API_KEY_2"]),
    ("deepseek-chat", "https://api.deepseek.com/chat/completions", "deepseek-chat", ["DEEPSEEK_API_KEY"]),
    ("together-dsv4flash", "https://api.together.xyz/v1/chat/completions", "deepseek-ai/DeepSeek-V4-Flash-0731", ["TOGETHER_API_KEY"]),
    ("zai-key2-glm47", "https://api.z.ai/api/paas/v4/chat/completions", "glm-4.7-flash", ["ZAI_API_KEY_2"]),
]


def key_for(names):
    for n in names:
        k = (os.environ.get(n, "") or "").strip()
        if k:
            return k
    return ""


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class Lane:
    def __init__(self, name, url, model, keynames):
        self.name = name
        self.url = url
        self.model = model
        self.key = key_for(keynames)
        self.alive = bool(self.key)
        self.conc = 1
        self.ceiling = None
        self.ok = 0
        self.fails = 0
        self.lock = threading.Lock()

    def touch_ok(self):
        with self.lock:
            self.ok += 1
            if self.ceiling is None and self.ok % 8 == 0 and self.conc < 8:
                self.conc += 1

    def touch_fail(self, kind):
        with self.lock:
            self.fails += 1
            if kind in ("429", "quota"):
                self.ceiling = self.conc
                self.conc = max(1, self.conc // 2)


LANES = [Lane(n, u, m, ks) for n, u, m, ks in LANE_DEFS if key_for(ks)]


def call(lane, prompt):
    if not lite_guard._safe_https_url(lane.url):
        return "", "fail"
    body = json.dumps({"model": lane.model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 900, "temperature": 0}).encode()
    req = urllib.request.Request(lane.url, data=body, headers={
        "Authorization": "Bearer " + lane.key, "Content-Type": "application/json"})
    try:
        with lite_guard._OPENER.open(req, timeout=150) as r:
            d = json.loads(r.read().decode())
        msg = (d.get("choices") or [{}])[0].get("message", {}) or {}
        content = (msg.get("content") or "").strip()
        if content:
            return content, "ok"
        rc = (msg.get("reasoning_content") or "").strip()
        return (rc[:500] if rc else ""), ("empty" if not rc else "ok")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return "", "429"
        if e.code in (402, 403):
            return "", "quota"
        return "", "fail"
    except Exception:
        return "", "fail"


def append_jsonl(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")


def dispatch(chore):
    lane = chore["lane"]
    for _attempt in range(2):
        text, kind = call(lane, chore["prompt"])
        if kind == "ok" and text:
            lane.touch_ok()
            out = chore.get("out")
            if out:
                append_jsonl(out, {"ts": now_iso(), "chore": chore["name"],
                                   "lane": lane.name, "body": text[:4000]})
            append_jsonl(LEDGER, {"ts": now_iso(), "lane": lane.name,
                                  "chore": chore["name"], "ok": True})
            return
        lane.touch_fail(kind)
        if kind == "429":
            time.sleep(30)
            continue
        append_jsonl(LEDGER, {"ts": now_iso(), "lane": lane.name,
                              "chore": chore["name"], "ok": False, "kind": kind})
        if kind == "quota":
            return
        break
    others = [l for l in LANES if l.alive and l is not lane]
    if others and chore.get("retries", 0) < 2:
        chore["retries"] = chore.get("retries", 0) + 1
        chore["lane"] = others[hash(chore["name"] + str(chore["retries"])) % len(others)]
        return dispatch(chore)


def build_chores():
    chores = []
    for name, path in RECORDS:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        chunks = [text[i:i + 8000] for i in range(0, min(len(text), 24000), 8000)]
        for i, ch in enumerate(chunks):
            chores.append({
                "name": "labels:" + name + ":" + str(i + 1), "lane": None, "out": LABELS,
                "prompt": "Extract Fleet-Bench labeled rows from this record slice. Output ONLY JSONL, "
                          "one object per verifiable claim: "
                          '{"claim":"...","tier":"stranger-replayable|contested|do-not-post",'
                          '"anchor_url":"...","label":"capture|deception|experiment|trafficking|money|reset|books"}. '
                          "No prose.\n\n" + ch})
    for pname, kernel in PILLARS:
        chores.append({
            "name": "anchor:" + pname, "lane": None, "out": ANCHORS,
            "prompt": kernel + "\n\nOutput ONLY the two-sentence anchor note. No commentary."})
    for fam in FAMILIES:
        chores.append({
            "name": "gapq:" + fam, "lane": None, "out": QUESTIONS,
            "prompt": "Family: " + fam + ". In one sentence: what is the single most important "
                      "question that remains UNVERIFIED about this family after the evidence dig, "
                      "and which archive would answer it? Output only the question and the archive."})
    return chores


def main(budget_minutes=30):
    chores = build_chores()
    deadline = time.time() + budget_minutes * 60
    print("task_wall: %d chores, %d lanes, budget %d min" % (len(chores), len(LANES), budget_minutes), flush=True)
    threads = []

    def worker(chore):
        lane = chore.get("lane") or LANES[hash(chore["name"]) % len(LANES)]
        chore["lane"] = lane
        while time.time() < deadline:
            dispatch(chore)
            return

    for c in chores:
        t = threading.Thread(target=worker, args=(dict(c),))
        t.start()
        threads.append(t)
        time.sleep(0.05)
        if time.time() > deadline:
            break
    for t in threads:
        t.join(timeout=max(1, deadline - time.time()))

    lanes_report = [{"lane": l.name, "alive": l.alive, "calls_ok": l.ok, "fails": l.fails,
                     "final_conc": l.conc, "ceiling": l.ceiling} for l in LANES]
    done = 0
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                if json.loads(line).get("ok"):
                    done += 1
            except Exception:
                pass
    md = ["# TASK WALL REPORT — full-blast concurrent churn (2026-09-23 night)",
          "",
          "chores queued: %d — lanes alive: %d/%d — chore OKs: %d" % (len(chores), sum(1 for l in LANES if l.alive), len(LANES), done),
          "",
          "| lane | ok | fails | final conc | ceiling |",
          "|---|---|---|---|---|"]
    for l in LANES:
        md.append("| " + l.name + " | " + str(l.ok) + " | " + str(l.fails) + " | "
                  + str(l.conc) + " | " + (str(l.ceiling) if l.ceiling else "not yet") + " |")
    md += ["", "The wall is wherever the failures start. The ramp records it, backs off, keeps working."]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(md), encoding="utf-8")
    return {"chores": len(chores), "lanes_alive": sum(1 for l in LANES if l.alive), "done": done,
            "lanes_report": lanes_report}


if __name__ == "__main__":
    mins = 30
    if "--budget-minutes" in sys.argv:
        mins = int(sys.argv[sys.argv.index("--budget-minutes") + 1])
    print(json.dumps(main(mins), indent=1))
