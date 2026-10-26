#!/usr/bin/env python
"""oral_law_mine - THE RESET BURN (2026-09-30). Operator order: use all the compute, burn down
the remaining authorized budget so he can reset.

Runs the N5 schema (designed by night-burn gopher N5, $0.14) over the founding record:
samples threads from corpus/oral_history/seat_pools/session_index.jsonl, pastes each thread's
user+assistant turns to glm-5.3-prime (the proven seat), extracts {thread -> decisions ->
laws-or-debts} rows, appends ORAL_LAW_INDEX.jsonl. BUDGET-CAPPED at $15 of the remaining
authorized spend; checkpointed per thread; SSRF-guarded (pinned host) per Mimosa."""
from __future__ import annotations

import json
import os
import pathlib
import random
import time
import urllib.error
import urllib.parse
import urllib.request

HERMES_DIR = r"C:\Users\foste\AppData\Local\hermes"
ALLOWED_HOST = "inference-api.nousresearch.com"
BASE = "https://" + ALLOWED_HOST + "/v1/chat/completions"
REPO = pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
POOLS = REPO / "corpus" / "oral_history" / "seat_pools"
OUT = REPO / "watch" / "inbox" / "operator_model" / "ORAL_LAW_INDEX.jsonl"
BUDGET = 15.0
MODEL = "z-ai/glm-5.3-prime"

ASK = """You are extracting the founding law of an AI research estate from its earliest session records.
Below is ONE session thread (user + assistant turns, lightly truncated). Extract:
1. thread_name (given), 2. decisions: the concrete choices made (max 3, one line each),
3. laws_or_debts: any rule/principle/documented-owe that was born or repeated here
   (format: LAW: <text> or DEBT: <text>, max 3), 4. confidence: high|med|low based on evidence in the text.
If the thread contains no law-worthy material, return {\"skip\": true, \"why\": \"<one line>\"}.
FALSIFIER: only extract what is LITERALLY in the text; never infer philosophy. Output ONE JSON object, no prose.
Laws: no em-dashes.

THREAD_NAME: {name}
<THREAD>
{body}
</THREAD>"""


def load_env():
    for line in open(os.path.join(HERMES_DIR, ".env"), encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


def call(prompt, key):
    p = urllib.parse.urlparse(BASE)
    assert p.scheme == "https" and p.hostname == ALLOWED_HOST
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 6000, "temperature": 0.2,
                       "reasoning": {"max_tokens": 2500}}).encode()
    req = urllib.request.Request(BASE, data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)


GROK_SKIP_PREFIXES = ("<system-reminder>", "<user_info>")  # env boilerplate grok injects as fake user turns


def _grok_text(content):
    # grok content is either a plain string (assistant, system) or a list of {"type":"text","text":...} parts (user)
    if isinstance(content, str):
        return content
    parts = []
    for c in content or []:
        if isinstance(c, dict) and c.get("text"):
            parts.append(str(c["text"]))
    return "\n".join(parts)


def grok_thread_body(sid, limit=9000):
    # grok pool layout: grok_sessions/<url-encoded-cwd>/<session-uuid>/chat_history.jsonl
    # (852 session dirs, 2026-09-30 survey; event types: system(str)/user(list)/reasoning/backend_tool_call/
    #  assistant(str)/tool_result(str); user turns tagged <system-reminder>|<user_info> are env boilerplate,
    #  real queries arrive wrapped in <user_query>...</user_query>).
    hits = list((POOLS / "grok_sessions").glob(f"*/{sid}/chat_history.jsonl"))
    if not hits:
        return None
    turns = []
    for ln in hits[0].read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(ln)
        except Exception:
            continue
        t = e.get("type")
        if t not in ("user", "assistant"):  # skips system, reasoning, backend_tool_call, tool_result
            continue
        txt = _grok_text(e.get("content")).strip()
        if t == "user":
            if txt.startswith(GROK_SKIP_PREFIXES):
                continue
            if txt.startswith("<user_query>"):
                txt = txt[len("<user_query>"):].strip()
            if txt.endswith("</user_query>"):
                txt = txt[: -len("</user_query>")].strip()
        if txt and len(txt) > 5:
            turns.append(f"{t.upper()}: {txt[:1200]}")
        if len(turns) >= 14:
            break
    body = "\n".join(turns)[:limit]
    return body or None


def thread_body(idx_row, limit=9000):
    sid = idx_row["id"]
    hits = list((POOLS / "codex_sessions").glob(f"*/*/*/rollout-*-{sid}.jsonl"))
    if not hits:
        return grok_thread_body(sid, limit=limit)  # not codex: try the grok pool before giving up
    turns = []
    for ln in hits[0].read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(ln)
        except Exception:
            continue
        if e.get("type") != "response_item":
            continue
        p = e.get("payload", {})
        if p.get("type") != "message" or p.get("role") not in ("user", "assistant"):
            continue
        parts = []
        for c in p.get("content") or []:
            if isinstance(c, dict) and c.get("text"):
                parts.append(str(c["text"]))
        txt = "\n".join(parts).strip()
        if txt and len(txt) > 5 and not txt.startswith("<app-context>"):
            turns.append(f"{p['role'].upper()}: {txt[:1200]}")
        if len(turns) >= 14:
            break
    body = "\n".join(turns)[:limit]
    return body or None


def main():
    load_env()
    keys = [k for k in (os.environ.get("NOUS_SDD_API_KEY"), os.environ.get("HERMES_API_KEY_1")) if k]
    key = keys[0]
    rows = [json.loads(l) for l in (POOLS / "session_index.jsonl").read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    random.Random(20260930).shuffle(rows)  # deterministic sample
    done_ids = set()
    if OUT.exists():
        for l in OUT.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                done_ids.add(json.loads(l).get("thread_id"))
            except Exception:
                pass
    spent = 0.0
    n_ok = n_skip = n_err = 0
    with open(OUT, "a", encoding="utf-8") as out:
        for row in rows:
            if spent >= BUDGET:
                print(f"BUDGET CAP reached: ${spent:.4f}")
                break
            if row["id"] in done_ids:
                continue
            body = thread_body(row)
            if not body:
                continue
            try:
                prompt = ASK.replace("{name}", row["thread_name"]).replace("{body}", body)  # .format() choked on the template's literal JSON braces (KeyError '"skip"', fire-3 root cause)
                resp = call(prompt, key)
                usage = resp.get("usage", {})
                c = float(usage.get("cost") or 0)
                spent += c
                txt = (resp["choices"][0]["message"].get("content") or "").strip()
                i, j = txt.find("{"), txt.rfind("}")
                if i < 0 or j <= i:
                    n_err += 1
                    continue
                data = json.loads(txt[i:j + 1])
                rec = {"thread_id": row["id"], "thread_name": row["thread_name"], "ts": row.get("updated_at"),
                       "extracted": data, "model": MODEL, "cost_usd": round(c, 4)}
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                out.flush()
                done_ids.add(row["id"])
                if data.get("skip"):
                    n_skip += 1
                else:
                    n_ok += 1
                print(f"{row['thread_name'][:40]:40s} ${c:.4f} cum ${spent:.4f} ok={n_ok} skip={n_skip}")
            except urllib.error.HTTPError as e:
                print(f"HTTP {e.code} on {row['thread_name'][:40]} - backing off 30s")
                time.sleep(30)
                n_err += 1
                if n_err > 8:
                    break
            except Exception as e:
                n_err += 1
                print(f"err: {e}")
    print(f"ORAL LAW MINE DONE: extracted={n_ok} skipped={n_skip} errors={n_err} spent=${spent:.4f} -> {OUT}")


if __name__ == "__main__":
    main()
