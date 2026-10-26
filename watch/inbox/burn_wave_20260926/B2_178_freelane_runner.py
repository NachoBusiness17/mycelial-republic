# B2-178 free-lane tandem burn runner (2026-09-26).
# Burns ESTATE work through the alive free lanes measured by B2-04:
# groq (openai/gpt-oss-120b), openrouter key1+key2 (stealth/space-bunny-alpha),
# nous-hermes (stealth/space-bunny-alpha), together (DeepSeek-V4-Flash-0731),
# cohere (command-r-plus-08-2024), zai Pro+Lite (glm-4.7-flash, 1305 spaced retry).
# Estate tasks (real inputs, metadata only):
#   links_title_norm  - watch/inbox/LINKS.jsonl titles (public material)
#   links_dedupe      - candidate pairs from LINKS.jsonl (public material)
#   caption_enrich    - CAPTION_LEDGER_20260926.jsonl STRUCTURE ONLY (caption
#                       text never leaves the machine; synthetic-safe by design)
#   corpus_class      - corpus/ file metadata only (subdir + ext + size bucket;
#                       filenames and contents never leave the machine)
# Counters per lane: requests, statuses, bytes sent/received, usage-reported
# tokens (the falsifier). Hourly receipts FREELANE_BURN_H<H>.md, close totals
# at 23:30 local + LEDGER.jsonl row. Laws: no fabrication, no em-dash, this
# script runs only under .venv/Scripts/python.exe.
import hashlib
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = HERE
LINKS_PATH = os.path.join(REPO, "watch", "inbox", "LINKS.jsonl")
CAPTION_PATH = os.path.join(REPO, "watch", "inbox", "CAPTION_LEDGER_20260926.jsonl")
CORPUS_DIR = os.path.join(REPO, "corpus")
LEDGER_PATH = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")
QUEUE_PATH = os.path.join(HERE, "QUEUE.md")
COUNTERS_PATH = os.path.join(OUT, "B2_178_counters.json")
EVENTS_PATH = os.path.join(OUT, "B2_178_events.jsonl")
STATUS_PATH = os.path.join(OUT, "B2_178_status.json")
MANIFEST_PATH = os.path.join(OUT, "B2_178_queue_manifest.json")
CLOSE_PATH = os.path.join(OUT, "FREELANE_BURN_CLOSE_20260926.md")
SMOKE = "--smoke" in sys.argv
DEADLINE_ARG = "23:30"
for i, a in enumerate(sys.argv):
    if a == "--deadline" and i + 1 < len(sys.argv):
        DEADLINE_ARG = sys.argv[i + 1]

TASKS = ["links_title_norm", "links_dedupe", "caption_enrich", "corpus_class"]
OUT_FILES = {
    "links_title_norm": os.path.join(OUT, "B2_178_out_links_titles.jsonl"),
    "links_dedupe": os.path.join(OUT, "B2_178_out_links_dedupe.jsonl"),
    "caption_enrich": os.path.join(OUT, "B2_178_out_caption_enrich.jsonl"),
    "corpus_class": os.path.join(OUT, "B2_178_out_corpus_class.jsonl"),
}
CORPUS_PER_SUBDIR = 100000 if not SMOKE else 3  # full metadata census; runner parks at deadline
DEDUPE_PAIR_CAP = 400

if SMOKE:
    # smoke artifacts never touch the real run's falsifier files
    COUNTERS_PATH = COUNTERS_PATH.replace(".json", "_SMOKE.json")
    EVENTS_PATH = EVENTS_PATH.replace(".jsonl", "_SMOKE.jsonl")
    STATUS_PATH = STATUS_PATH.replace(".json", "_SMOKE.json")
    MANIFEST_PATH = MANIFEST_PATH.replace(".json", "_SMOKE.json")
    CLOSE_PATH = CLOSE_PATH.replace(".md", "_SMOKE.md")
    OUT_FILES = {t: p.replace(".jsonl", "_SMOKE.jsonl") for t, p in OUT_FILES.items()}
    def _smoke_hourly(path):
        return path.replace(".md", "_SMOKE.md")
else:
    def _smoke_hourly(path):
        return path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 MagBurn/1.0")
OR_HEADERS = {"HTTP-Referer": "http://127.0.0.1:8765", "X-Title": "Mag Resource Harness"}

LANE_DEFS = [
    dict(name="groq", base="https://api.groq.com/openai/v1", env="GROQ_API_KEY",
         model="openai/gpt-oss-120b", interval=8.0, max_tokens=400,
         extra={"reasoning_effort": "low"}, tpd_guard=185000),
    dict(name="openrouter-k1", base="https://openrouter.ai/api/v1", env="OPENROUTER_API_KEY",
         model="stealth/space-bunny-alpha", interval=3.5, max_tokens=1000,
         headers=OR_HEADERS, rpm_shape="20 RPM per operator brief"),
    dict(name="openrouter-k2", base="https://openrouter.ai/api/v1", env="OPENROUTER_API_KEY_2",
         model="stealth/space-bunny-alpha", interval=3.5, max_tokens=1000,
         headers=OR_HEADERS, rpm_shape="20 RPM per operator brief"),
    dict(name="nous-hermes", base="https://inference-api.nousresearch.com/v1",
         env="HERMES_API_KEY_1", model="stealth/space-bunny-alpha",
         interval=10.0, max_tokens=300),
    dict(name="together", base="https://api.together.xyz/v1", env="TOGETHER_API_KEY",
         model="deepseek-ai/DeepSeek-V4-Flash-0731", interval=10.0, max_tokens=300),
    dict(name="cohere", base="https://api.cohere.com/compatibility/v1",
         env="COHERE_API_KEY_FREE", model="command-r-plus-08-2024",
         interval=10.0, max_tokens=300),
    dict(name="zai-pro", base="https://api.z.ai/api/coding/paas/v4", env="ZAI_API_KEY_Pro",
         model="glm-4.7-flash", interval=10.0, max_tokens=1200, zai=True),
    dict(name="zai-lite", base="https://api.z.ai/api/coding/paas/v4", env="ZAI_API_KEY_Lite",
         model="glm-4.7-flash", interval=10.0, max_tokens=1200, zai=True),
]


def load_env():
    env = {}
    path = os.path.join(REPO, ".env")
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*=\s*(.*)$", line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bucket(n, edges):
    for i, e in enumerate(edges):
        if n < e:
            return i
    return len(edges)


# ---------- queue builders (real estate bytes) ----------

def build_links_rows():
    rows = []
    with open(LINKS_PATH, encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                rows.append(json.loads(ln))
            except Exception:
                continue
    return rows


def build_queues():
    q = {t: [] for t in TASKS}
    manifest = {"built_ts": now_iso(), "sources": {}, "counts": {}}
    rows = build_links_rows()
    manifest["sources"]["LINKS.jsonl"] = {
        "sha256": sha256_file(LINKS_PATH), "rows": len(rows)}

    titled = [r for r in rows if (r.get("title") or "").strip()]
    for i, r in enumerate(titled):
        url = r.get("url") or r.get("canonical") or ""
        dom = domain_of(url)
        q["links_title_norm"].append({
            "id": "lt-%04d" % i, "seq": r.get("seq"), "title": r.get("title"), "domain": dom})

    # dedupe candidates: same canonical first, then title token jaccard
    def toks(s):
        return set(re.findall(r"[a-z0-9]+", (s or "").lower()))
    by_canon = {}
    for r in rows:
        c = (r.get("canonical") or "").strip()
        if c:
            by_canon.setdefault(c, []).append(r)
    cand = []
    seen_pairs = set()
    for c, grp in sorted(by_canon.items()):
        for i in range(len(grp)):
            for j in range(i + 1, len(grp)):
                cand.append((1.0, grp[i], grp[j]))
    keyed = [(r, toks(r.get("title")), idx) for idx, r in enumerate(titled)]
    for a in range(len(keyed)):
        ta = keyed[a][1]
        if len(ta) < 3:
            continue
        for b in range(a + 1, len(keyed)):
            tb = keyed[b][1]
            if len(tb) < 3:
                continue
            inter = len(ta & tb)
            if not inter:
                continue
            jac = inter / float(len(ta | tb))
            if jac >= 0.45:
                ra, rb = keyed[a][0], keyed[b][0]
                pk = (ra.get("seq"), rb.get("seq"))
                if pk not in seen_pairs:
                    seen_pairs.add(pk)
                    cand.append((jac, ra, rb))
    cand.sort(key=lambda x: -x[0])
    for i, (score, ra, rb) in enumerate(cand[:DEDUPE_PAIR_CAP]):
        q["links_dedupe"].append({
            "id": "dd-%04d" % i, "a_seq": ra.get("seq"), "b_seq": rb.get("seq"),
            "a_title": ra.get("title"), "a_domain": domain_of(ra.get("url") or ra.get("canonical") or ""),
            "b_title": rb.get("title"), "b_domain": domain_of(rb.get("url") or rb.get("canonical") or ""),
            "score": round(score, 3), "same_canonical":
                (ra.get("canonical") or "") == (rb.get("canonical") or "") and bool(ra.get("canonical"))})

    # caption ledger: STRUCTURE ONLY, caption text stays local by construction
    n_cap = 0
    with open(CAPTION_PATH, encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                r = json.loads(ln)
            except Exception:
                continue
            n_cap += 1
            blen = r.get("caption_len") or 0
            cap = r.get("caption") or ""
            q["caption_enrich"].append({
                "id": "ce-%04d" % n_cap, "cite": r.get("cite"), "msg_id": r.get("msg_id"),
                "kind": r.get("kind"), "media_type": r.get("media_type"),
                "ext": r.get("file_ext"), "status": r.get("status"),
                "bytes_bucket": bucket(r.get("bytes") or 0, [1024, 102400, 1048576, 10485760]),
                "cap_len_bucket": bucket(blen, [1, 81, 241, 1001]),
                "cap_has_url": 1 if ("http" in cap) else 0,
                "via_group": 1 if (r.get("caption_via") or "") not in ("", "self") else 0})
    manifest["sources"]["CAPTION_LEDGER_20260926.jsonl"] = {
        "sha256": sha256_file(CAPTION_PATH), "rows": n_cap}

    # corpus metadata census: subdir + ext + size bucket only
    # fix receipt (B2-178): the first real-launch build crashed in
    # ntpath.relpath with "path is on mount \\. nul" because corpus/ holds a
    # reparse point resolving to the NUL device namespace; every path call in
    # this walk is now guarded and such entries are skipped and counted.
    per_dir = {}
    skipped_device = 0
    idx = 0
    for root, dirs, files in os.walk(CORPUS_DIR):
        dirs[:] = [d for d in dirs if d != ".git"]
        try:
            rel_root = os.path.relpath(root, CORPUS_DIR)
        except (ValueError, OSError):
            dirs[:] = []
            continue
        sub = rel_root.split(os.sep)[0] if rel_root != "." else "(root)"
        if per_dir.get(sub, 0) >= CORPUS_PER_SUBDIR:
            dirs[:] = []
            continue
        for fn in files:
            if per_dir.get(sub, 0) >= CORPUS_PER_SUBDIR:
                break
            full = os.path.join(root, fn)
            try:
                sz = os.path.getsize(full)
                path_rel = os.path.relpath(full, REPO)
            except (ValueError, OSError):
                skipped_device += 1
                continue
            per_dir[sub] = per_dir.get(sub, 0) + 1
            idx += 1
            q["corpus_class"].append({
                "id": "cc-%05d" % idx, "subdir": sub,
                "ext": os.path.splitext(fn)[1].lower() or "(none)",
                "size_bucket": bucket(sz, [1024, 65536, 1048576, 33554432]),
                "path": path_rel})
    manifest["sources"]["corpus/"] = {"files_seen": idx, "per_subdir_capped": CORPUS_PER_SUBDIR,
                                      "subdirs": sorted(per_dir.keys()),
                                      "skipped_device_paths": skipped_device}
    for t in TASKS:
        manifest["counts"][t] = len(q[t])
    if SMOKE:
        for t in TASKS:
            q[t] = q[t][:3]
        manifest["counts"] = {t: len(q[t]) for t in TASKS}
    manifest["total_items"] = sum(manifest["counts"].values())
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    return q, manifest


def domain_of(url):
    m = re.match(r"^https?://([^/]+)", url or "")
    return m.group(1) if m else ""


# ---------- prompts (privacy-scrubbed by construction) ----------

def prompt_for(task, it):
    if task == "links_title_norm":
        return ("Normalize a link-library title. Reply ONLY compact JSON: "
                '{"site": "<domain or empty>", "work": "<cleaned work name, max 100 chars>", '
                '"type": "paper|tool|repo|article|post|video|dataset|other"}. '
                "Title: %s (domain: %s)" % (it["title"], it["domain"]))
    if task == "links_dedupe":
        return ("Two link-library entries. Same underlying resource? Reply ONLY compact JSON: "
                '{"same": true or false, "reason": "max 15 words"}. '
                "A: %s (%s) B: %s (%s)" % (it["a_title"], it["a_domain"], it["b_title"], it["b_domain"]))
    if task == "caption_enrich":
        return ("Classify a media-ledger row by structure only, no text content available. "
                'Reply ONLY compact JSON: {"class": "photo-doc|photo-scene|video-clip|link-preview|doc|other", '
                '"archive_worthy": true or false, "reason": "max 10 words"}. '
                "Row: kind=%s media_type=%s ext=%s status=%s bytes_bucket=%s cap_len_bucket=%s "
                "cap_has_url=%s via_group=%s" % (
                    it["kind"], it["media_type"], it["ext"], it["status"],
                    it["bytes_bucket"], it["cap_len_bucket"], it["cap_has_url"], it["via_group"]))
    if task == "corpus_class":
        return ("Classify a file by metadata only. Reply ONLY compact JSON: "
                '{"class": "code|prose|data|config|vcs-internal|media|archive|other", '
                '"keep": true or false, "reason": "max 10 words"}. '
                "subdir=%s ext=%s size_bucket=%s" % (it["subdir"], it["ext"], it["size_bucket"]))
    raise ValueError(task)


# ---------- shared state ----------

class State:
    def __init__(self):
        self.lock = threading.Lock()
        self.lanes = {}
        self.queues = {}
        self.task_lock = threading.Lock()
        self.rr = 0
        self.done_by_task = {t: 0 for t in TASKS}
        self.out_files = {}
        self.events_fh = None
        self.started = time.time()

    def open_out(self):
        self.events_fh = open(EVENTS_PATH, "a", encoding="utf-8")
        for t, p in OUT_FILES.items():
            self.out_files[t] = open(p, "a", encoding="utf-8")

    def claim(self):
        with self.task_lock:
            for _ in TASKS:
                t = TASKS[self.rr % len(TASKS)]
                self.rr += 1
                if self.queues[t]:
                    return t, self.queues[t].pop(0)
            return None, None

    def record(self, lane, task, item_id, resp, bytes_sent, usage, note=""):
        st = resp["status"]
        with self.lock:
            L = self.lanes[lane]
            L["requests"] += 1
            L["bytes_sent"] += bytes_sent
            L["bytes_recv"] += len(resp["body"])
            key = "s%d" % st if st else "err"
            L["status"][key] = L["status"].get(key, 0) + 1
            L["latency_s"] += resp["latency_s"]
            if usage:
                L["tokens_prompt"] += usage.get("prompt_tokens") or 0
                L["tokens_completion"] += usage.get("completion_tokens") or 0
                L["tokens_total"] += usage.get("total_tokens") or 0
            else:
                L["no_usage"] += 1
            ev = {"ts": now_iso(), "lane": lane, "task": task, "item": item_id,
                  "status": st, "latency_s": resp["latency_s"],
                  "bytes_sent": bytes_sent, "bytes_recv": len(resp["body"]),
                  "usage": usage, "note": note}
            self.events_fh.write(json.dumps(ev) + "\n")
            self.events_fh.flush()

    def land(self, task, obj):
        with self.lock:
            self.out_files[task].write(json.dumps(obj) + "\n")
            self.out_files[task].flush()
            self.done_by_task[task] += 1

    def snapshot(self):
        with self.lock:
            return {
                "ts": now_iso(), "uptime_s": round(time.time() - self.started, 1),
                "remaining": {t: len(self.queues[t]) for t in TASKS},
                "done_by_task": dict(self.done_by_task),
                "lanes": json.loads(json.dumps(self.lanes)),
            }


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()) + time.strftime("%Z")


# ---------- http ----------

def http_post(url, key, payload, extra_headers=None, timeout=90):
    headers = {"User-Agent": UA, "Authorization": "Bearer " + key,
               "Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "latency_s": round(time.time() - t0, 2),
                    "body": resp.read().decode("utf-8", errors="replace")}
    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return {"status": e.code, "latency_s": round(time.time() - t0, 2), "body": raw}
    except Exception as e:
        return {"status": 0, "latency_s": round(time.time() - t0, 2),
                "body": type(e).__name__ + ": " + str(e)[:200]}


def extract_content(body):
    try:
        return json.loads(body)["choices"][0]["message"].get("content") or ""
    except Exception:
        return ""


def extract_usage(body):
    try:
        u = json.loads(body).get("usage") or {}
        return {k: u.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens")}
    except Exception:
        return {}


# ---------- lane worker ----------

def lane_worker(state, env, deadline, lane_def):
    name = lane_def["name"]
    key = env.get(lane_def["env"], "")
    st = state.lanes[name]
    if not key:
        st["disabled"] = "no key in .env"
        return
    url = lane_def["base"] + "/chat/completions"
    next_slot = time.time()
    consec_err = 0
    while time.time() < deadline:
        if st.get("disabled"):
            return
        if lane_def.get("tpd_guard") and st["tokens_total"] >= lane_def["tpd_guard"]:
            st["disabled"] = "tpd guard %d reached" % lane_def["tpd_guard"]
            return
        task, item = state.claim()
        if item is None:
            st["parked"] = "queues drained"
            return
        prompt = prompt_for(task, item)
        payload = {"model": lane_def["model"],
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": lane_def["max_tokens"], "temperature": 0}
        if lane_def.get("extra"):
            payload.update(lane_def["extra"])
        bytes_sent = len(json.dumps(payload).encode("utf-8"))
        wait = next_slot - time.time()
        if wait > 0:
            time.sleep(wait)
        next_slot = time.time() + lane_def["interval"]
        attempts = 0
        while True:
            attempts += 1
            resp = http_post(url, key, payload, lane_def.get("headers"))
            usage = extract_usage(resp["body"]) if resp["status"] == 200 else {}
            note = ""
            if resp["status"] == 429 and lane_def.get("zai") and "1305" in resp["body"]:
                note = "zai 1305, spaced retry 15s"
                state.record(name, task, item["id"], resp, bytes_sent, usage, note)
                consec_err += 1
                if attempts <= 3:
                    time.sleep(15)
                    continue
            break
        state.record(name, task, item["id"], resp, bytes_sent, usage, note)
        c = extract_content(resp["body"]) if resp["status"] == 200 else ""
        if resp["status"] == 200 and c.strip():
            consec_err = 0
            state.land(task, {"item": item["id"], "lane": name, "raw": c.strip()[:800]})
        elif resp["status"] == 200:
            consec_err += 1
            # empty content (reasoning-model token sink, B2-04 lore): one retry
            # via requeue, land only when the retry is spent, never both
            if item.get("_attempts", 0) < 1:
                item["_attempts"] = 1
                with state.task_lock:
                    state.queues[task].append(item)
            else:
                state.land(task, {"item": item["id"], "lane": name, "raw": "",
                                  "note": "empty content after retry"})
        else:
            consec_err += 1
            if attempts < 2 and resp["status"] in (429, 500, 502, 503, 0):
                item["_attempts"] = attempts + (item.get("_attempts", 0))
                with state.task_lock:
                    state.queues[task].append(item)
            else:
                state.land(task, {"item": item["id"], "lane": name, "raw": "",
                                  "note": "status %s" % resp["status"]})
            if resp["status"] in (401, 402, 403, 404, 410):
                st["disabled"] = "status %s on %s" % (resp["status"], item["id"])
                return
            if consec_err >= 8:
                st["parked"] = "8 consecutive errors, cooling 10 min"
                time.sleep(600)
                consec_err = 0
                st["parked"] = ""


# ---------- receipts ----------

def fmt_int(n):
    return "{:,}".format(n)


def lane_table(state, snap0, title):
    lines = ["| lane | calls | 200 | err | bytes_sent | bytes_recv | tok_prompt | tok_completion | tok_total | state |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for name, L in state.lanes.items():
        if snap0:
            P = snap0["lanes"][name]
        else:
            P = {k: 0 for k in ("requests", "bytes_sent", "bytes_recv", "tokens_prompt",
                                "tokens_completion", "tokens_total")}
            P["status"] = {}
        calls = L["requests"] - P["requests"]
        ok = L["status"].get("s200", 0) - P["status"].get("s200", 0)
        errs = calls - ok
        flag = "disabled: %s" % L["disabled"] if L.get("disabled") else (L.get("parked") or "running")
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            name, fmt_int(calls), fmt_int(max(ok, 0) if snap0 else ok), fmt_int(errs),
            fmt_int(L["bytes_sent"] - P["bytes_sent"]), fmt_int(L["bytes_recv"] - P["bytes_recv"]),
            fmt_int(L["tokens_prompt"] - P["tokens_prompt"]),
            fmt_int(L["tokens_completion"] - P["tokens_completion"]),
            fmt_int(L["tokens_total"] - P["tokens_total"]), flag))
    return "\n".join(lines)


def sample_outputs(task, n=3):
    p = OUT_FILES[task]
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        lines = f.readlines()
    return [l.strip()[:220] for l in lines[-n:]]


def write_hourly(state, hour_bucket, snap0, status_note):
    snap = state.snapshot()
    path = _smoke_hourly(os.path.join(OUT, "FREELANE_BURN_H%s.md" % hour_bucket))
    with open(path, "w", encoding="utf-8") as f:
        f.write("# FREELANE BURN H%s (B2-178, %s)\n\n" % (hour_bucket, now_iso()))
        f.write("%s\n\n" % status_note)
        f.write("## Per-lane counters (window | falsifier: usage-reported tokens)\n\n")
        f.write(lane_table(state, snap0, "window") + "\n\n")
        f.write("## Queue state\n\n")
        for t in TASKS:
            done = snap["done_by_task"][t] - (snap0["done_by_task"][t] if snap0 else 0)
            f.write("- %s: %s done this window, %s remaining (manifest %s)\n" % (
                t, fmt_int(done), fmt_int(snap["remaining"][t]),
                fmt_int(MANIFEST_COUNTS.get(t, snap["remaining"][t] + snap["done_by_task"][t]))))
        f.write("\n## Output samples (last per task, trimmed)\n\n")
        for t in TASKS:
            for s in sample_outputs(t):
                f.write("- %s: %s\n" % (t, s.replace("\n", " ")))
        f.write("\nPrivacy: caption rows and corpus files send structure metadata only; "
                "caption text, filenames and file contents never leave this machine.\n")
    return snap


# ---------- main ----------

MANIFEST_COUNTS = {}


def main():
    global MANIFEST_COUNTS
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    env = load_env()
    queues, manifest = build_queues()
    MANIFEST_COUNTS = dict(manifest["counts"])
    print("manifest:", manifest["counts"], "total", manifest["total_items"])

    lt = time.localtime()
    hh, mm = DEADLINE_ARG.split(":")
    deadline = time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday, int(hh), int(mm), 0,
                            lt.tm_wday, lt.tm_yday, -1))
    if SMOKE:
        deadline = time.time() + 150
    if time.time() >= deadline:
        print("deadline already passed, nothing to run")
        return

    state = State()
    state.queues = queues
    for d in LANE_DEFS:
        state.lanes[d["name"]] = {
            "requests": 0, "status": {}, "bytes_sent": 0, "bytes_recv": 0,
            "tokens_prompt": 0, "tokens_completion": 0, "tokens_total": 0,
            "no_usage": 0, "latency_s": 0.0, "disabled": "", "parked": ""}
    state.open_out()
    with open(COUNTERS_PATH, "w", encoding="utf-8") as f:
        json.dump(state.snapshot(), f, indent=1)

    threads = []
    for d in LANE_DEFS:
        th = threading.Thread(target=lane_worker, args=(state, env, deadline, d), daemon=True)
        th.start()
        threads.append(th)

    last_hour = time.localtime().tm_hour
    snap0 = write_hourly(state, "%02d" % last_hour, None,
                         "Launch window partial hour (cumulative since start).")
    while time.time() < deadline:
        time.sleep(20 if SMOKE else 30)
        with open(STATUS_PATH, "w", encoding="utf-8") as f:
            json.dump(state.snapshot(), f, indent=1)
        with open(COUNTERS_PATH, "w", encoding="utf-8") as f:
            json.dump(state.snapshot(), f, indent=1)
        h = time.localtime().tm_hour
        if h != last_hour and not SMOKE:
            snap0 = write_hourly(
                state, "%02d" % h, snap0,
                "Hour bucket H%02d: window counters cover this hour bucket only (delta since the previous hourly snapshot)." % h)
            last_hour = h

    for _ in threads:
        _.join(timeout=120)  # let in-flight calls (90s http timeout) land before close

    # close totals
    snap = state.snapshot()
    with open(CLOSE_PATH, "w", encoding="utf-8") as f:
        f.write("# FREELANE BURN CLOSE (B2-178, %s)\n\n" % now_iso())
        f.write("Ran %s to %s local deadline 23:30. All counters below are per-lane totals.\n\n" % (
            time.strftime("%H:%M", time.localtime(state.started)), time.strftime("%H:%M")))
        f.write("## Per-lane totals (falsifier: usage-reported token counters)\n\n")
        f.write(lane_table(state, None, "totals") + "\n\n")
        f.write("## Totals\n\n")
        tp = sum(L["tokens_prompt"] for L in state.lanes.values())
        tc = sum(L["tokens_completion"] for L in state.lanes.values())
        tt = sum(L["tokens_total"] for L in state.lanes.values())
        bs = sum(L["bytes_sent"] for L in state.lanes.values())
        br = sum(L["bytes_recv"] for L in state.lanes.values())
        calls = sum(L["requests"] for L in state.lanes.values())
        f.write("- calls %s, bytes_sent %s, bytes_recv %s, tokens prompt %s completion %s total %s\n\n" % (
            fmt_int(calls), fmt_int(bs), fmt_int(br), fmt_int(tp), fmt_int(tc), fmt_int(tt)))
        f.write("## Work landed\n\n")
        for t in TASKS:
            f.write("- %s: %s items answered -> %s\n" % (t, fmt_int(snap["done_by_task"][t]), OUT_FILES[t]))
        f.write("\n## Remaining queue at close\n\n")
        for t in TASKS:
            f.write("- %s: %s items not yet burned (resume pointer: manifest %s, rerun runner)\n" % (
                t, fmt_int(snap["remaining"][t]), MANIFEST_PATH))
        f.write("\nPrivacy law held: no caption text, no filenames, no file contents left the machine; "
                "LINKS titles/domains (public) only.\n")
    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(state.snapshot(), f, indent=1)

    if not SMOKE:
        row = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "slug": "B2-178-freelane-close",
            "verdict": "CLOSED",
            "landing": CLOSE_PATH,
            "one_line": ("B2-178 free-lane tandem burn close: %s calls across 8 lanes "
                         "(groq, openrouter k1/k2, nous, together, cohere, zai pro/lite), "
                         "bytes_sent %s bytes_recv %s tokens reported prompt %s completion %s total %s; "
                         "estate items answered: %s; per-lane token counters are the falsifier; "
                         "privacy: caption text, filenames, file contents never left the machine") % (
                fmt_int(calls), fmt_int(bs), fmt_int(br), fmt_int(tp), fmt_int(tc), fmt_int(tt),
                json.dumps(snap["done_by_task"])),
            "lane": "B2-178",
        }
        with open(LEDGER_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
    print("CLOSE WRITTEN", CLOSE_PATH)


if __name__ == "__main__":
    main()
