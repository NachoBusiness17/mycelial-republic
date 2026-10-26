#!/usr/bin/env python3
"""qwen2.5:7b Q4_K_M vs q8_0 A/B runner - amended four-pinned-choices instrument.

Spec: watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md (P6, commit 6685db6bc).
Arms per spec lines 51-56:
  A: qwen2.5:7b (Q4_K_M, on-box digest 845dbda0ea48)
  B: qwen2.5:7b-instruct-q8_0 (library pull)
Legs implemented (spec lines 63-90):
  1 FIVE-PROMPT RULE: 10 tasks x 5 phrasings = 50 runs per arm.
  2 DEPLOYMENT VERDICT: full-pipeline success pooled over ALL tasks and prompts.
  3 MATCHED-TASK DELTAS DIAGNOSTIC: per-prompt clean-intersection deltas, sign flips.
  4 STRICT-PARSE CHANNEL separate; Qwen-flat prior stated in the receipt.
  5 PER-TASK SPREAD reported with the pooled verdict.
  6 EXPORT-CAST RIDER: sha256 of the exact GGUF blobs + toolchain pin.
  7 THINKING CHANNEL logged rider only.
Kept from 10-03: serving-cache state pinned per arm (ollama ps logged per run),
token counts compared only on EOS-terminated responses or equal caps (cap 512 both arms).
$0 compute. stdlib only. ASCII only.

Usage:
  python run_ab.py info      # manifest digests + blob sha256 (cached)
  python run_ab.py armA      # 50 runs, resume-safe jsonl
  python run_ab.py armB
  python run_ab.py summarize # verdicts + falsifiers, writes SUMMARY.json
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OLLAMA = "http://127.0.0.1:11434"
ARMS = {"A": "qwen2.5:7b", "B": "qwen2.5:7b-instruct-q8_0"}
NUM_CTX = 8192          # estate envelope, configs/lanes.yaml:30,63
NUM_PREDICT = 512       # identical caps both arms (10-03 stopping rule: cap >= 512)
TEMP = 0.0
MODELS_DIR = os.path.join(os.path.expanduser("~"), ".ollama", "models")

# ---------------------------------------------------------------- tasks ----
# 10 deterministic tool-failure-recovery tasks. Fixed key per task. The response
# schema is stated in every phrasing (a real pipeline hands the model a schema);
# the measured axes are recovery correctness and format compliance, not schema
# guessing. 5 phrasings per task vary wording only, data identical.

TASKS = [
    {
        "id": "T01_json_repair",
        "data": {
            "broken": '{"name": web_fetch,, "url": "https://example.com/feed", "timeout": 30,}',
            "note": "the name value lost its closing quote and there is a trailing comma",
        },
        "schema": '{"name": "<tool name>", "url": "<url>", "timeout": <number>}',
        "expect": {"name": "web_fetch", "url": "https://example.com/feed", "timeout": 30},
        "phrasings": [
            "You are a pipeline janitor agent. A tool call you sent failed JSON validation. The broken call was: {broken} ({note}). Repair it into valid JSON keeping every field and value unchanged. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation failed validation. Broken serialization: {broken} ({note}). Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure. The serialized call {broken} is malformed ({note}). Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher rejected your call as invalid JSON: {broken} ({note}). Decide the repair and respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: malformed tool call {broken} ({note}). Return just the JSON decision object with the repaired call in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T02_retry_backoff",
        "data": {"status": "HTTP 429", "header": "Retry-After: 12",
                 "rule": "house rule: honor the server's Retry-After value, then retry once"},
        "schema": '{"action": "<retry|abort>", "wait_seconds": <number>}',
        "expect": {"action": "retry", "wait_seconds": 12},
        "phrasings": [
            "You are a pipeline janitor agent. The fetch tool returned {status} with header {header}. {rule}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation got {status}, header {header}. {rule}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure: {status}, {header}. {rule}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher reports {status} with {header}. {rule}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: {status}, {header}. {rule}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T03_path_404",
        "data": {"err": "ENOENT: no such file or directory, open 'data/2026/10/07.csv'",
                 "note": "the daily rollup ran overnight and today's file is dated 2026-10-08, same directory and same naming pattern"},
        "schema": '{"action": "<retry|abort>", "path": "<correct file path>"}',
        "expect": {"action": "retry", "path": "data/2026/10/08.csv"},
        "phrasings": [
            "You are a pipeline janitor agent. read_file failed: {err}. Context: {note}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation failed: {err}. Context: {note}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure: {err}. Context: {note}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher reports a read error: {err}. Context: {note}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: {err}. Context: {note}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T04_schema_field",
        "data": {"err": "unknown field 'when' in tool write_log",
                 "note": "the tool schema requires the field 'timestamp' instead"},
        "schema": '{"action": "<retry|abort>", "field": "<correct field name>"}',
        "expect": {"action": "retry", "field": "timestamp"},
        "phrasings": [
            "You are a pipeline janitor agent. The call was rejected: {err}. {note}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation was rejected: {err}. {note}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure: {err}. {note}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher rejected the call: {err}. {note}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: {err}. {note}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T05_timeout_escalate",
        "data": {"fact": "read_file timed out after 60 seconds. This same call has already been retried once.",
                 "rule": "house rule: retry at most once per call, then escalate to the operator"},
        "schema": '{"action": "<retry|escalate>"}',
        "expect": {"action": "escalate"},
        "phrasings": [
            "You are a pipeline janitor agent. {fact} {rule}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation: {fact} {rule}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure. {fact} {rule}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher reports: {fact} {rule}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident. {fact} {rule}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T06_budget_pick",
        "data": {"rule": "the budget allows exactly one more tool call this turn",
                 "a": "Candidate A: db_query, latency 400 ms, value 3",
                 "b": "Candidate B: cache_get, latency 200 ms, value 5",
                 "crit": "pick the candidate with the higher value per millisecond"},
        "schema": '{"action": "keep", "keep": "<A|B>"}',
        "expect": {"action": "keep", "keep": "B"},
        "phrasings": [
            "You are a pipeline janitor agent. {rule}. {a}. {b}. {crit}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A scheduling decision in your automation: {rule}. {a}. {b}. {crit}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Budget decision. {rule}. {a}. {b}. {crit}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Resource gate: {rule}. {a}. {b}. {crit}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: {rule}. {a}. {b}. {crit}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T07_wrong_tool",
        "data": {"goal": "summarize the local file notes.md",
                 "tools": "web_search(url), read_file(path), send_email(to, subject, body)",
                 "note": "pick the one tool that serves this goal"},
        "schema": '{"tool": "<tool name>"}',
        "expect": {"tool": "read_file"},
        "phrasings": [
            "You are a pipeline janitor agent. Goal: {goal}. Available tools: {tools}. {note}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool selection in your automation. Goal: {goal}. Tools: {tools}. {note}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from the wrong-tool pick. Goal: {goal}. Tools: {tools}. {note}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher asks for a selection. Goal: {goal}. Tools: {tools}. {note}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: wrong tool was chosen. Goal: {goal}. Tools: {tools}. {note}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T08_missing_param",
        "data": {"err": "missing required param 'to' in tool send_email",
                 "note": "the memo says: send the digest to Dana at dana@example.com"},
        "schema": '{"action": "<retry|abort>", "to": "<recipient email>"}',
        "expect": {"action": "retry", "to": "dana@example.com"},
        "phrasings": [
            "You are a pipeline janitor agent. send_email failed: {err}. {note}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation failed: {err}. {note}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure: {err}. {note}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher rejected the call: {err}. {note}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: {err}. {note}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T09_truncated_resume",
        "data": {"fact": "fetch_page returned only the first 500 bytes of a 2000-byte document before the connection dropped",
                 "rule": "policy: resume from the byte offset right after the bytes that arrived"},
        "schema": '{"action": "<resume|abort>", "from_offset": <number>}',
        "expect": {"action": "resume", "from_offset": 500},
        "phrasings": [
            "You are a pipeline janitor agent. {fact}. {rule}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation: {fact}. {rule}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure. {fact}. {rule}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher reports: {fact}. {rule}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident. {fact}. {rule}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
    {
        "id": "T10_perm_fallback",
        "data": {"err": "permission denied writing /etc/hosts",
                 "rule": "policy: fall back to the workspace override path /workspace/hosts.override"},
        "schema": '{"action": "<fallback|abort>", "path": "<fallback path>"}',
        "expect": {"action": "fallback", "path": "/workspace/hosts.override"},
        "phrasings": [
            "You are a pipeline janitor agent. Write failed: {err}. {rule}. Respond with ONLY this JSON object and nothing else: {schema}",
            "A tool call in your automation failed: {err}. {rule}. Output only a JSON object, no markdown, no explanation, in exactly this shape: {schema}",
            "Recover from this tool failure: {err}. {rule}. Reply with exactly one JSON object and nothing else, matching: {schema}",
            "Tool dispatcher reports: {err}. {rule}. Respond with a single JSON object only, no code fences, shaped exactly: {schema}",
            "Queue incident: {err}. {rule}. Return just the JSON decision object in this form and no other text: {schema}",
        ],
    },
]


def build_runs():
    runs = []
    for t_i, task in enumerate(TASKS):
        for p_i, phrasing in enumerate(task["phrasings"]):
            text = phrasing
            for k, v in task["data"].items():
                text = text.replace("{" + k + "}", v)
            text = text.replace("{schema}", task["schema"])
            leftover = re.findall(r"\{[a-z_]+\}", text)
            assert not leftover, "unfilled placeholder(s): %s" % leftover
            seed = 1000 + t_i * 10 + p_i          # paired seed: same for both arms
            runs.append({"task": task["id"], "prompt_idx": p_i, "seed": seed,
                         "prompt": text, "expect": task["expect"]})
    return runs


def ollama_ps():
    try:
        with urllib.request.urlopen(OLLAMA + "/api/ps", timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:  # logged, never fatal
        return [{"error": str(e)}]


def generate(model, prompt, seed):
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": TEMP, "seed": seed,
                    "num_ctx": NUM_CTX, "num_predict": NUM_PREDICT},
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=1800) as r:
        out = json.loads(r.read().decode("utf-8"))
    out["_wall_s"] = round(time.time() - t0, 3)
    return out


def first_json_object(text):
    """First balanced {...} that json-parses, or None."""
    for m in re.finditer(r"\{", text):
        depth = 0
        start = m.start()
        for i in range(start, len(text)):
            c = text[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    cand = text[start:i + 1]
                    try:
                        return json.loads(cand)
                    except Exception:
                        break
        continue
    return None


def grade(text, expect):
    obj = first_json_object(text)
    pipeline = False
    if obj is not None:
        pipeline = all(obj.get(k) == v for k, v in expect.items())
    s = text.strip()
    strict = False
    try:
        sobj = json.loads(s)
        strict = isinstance(sobj, dict) and all(sobj.get(k) == v for k, v in expect.items())
    except Exception:
        strict = False
    return {"pipeline_pass": pipeline, "strict_pass": strict}


def cmd_info():
    lines = []
    for arm, tag in ARMS.items():
        ns = tag.split(":")[0]
        t = tag.split(":", 1)[1]
        mpath = os.path.join(MODELS_DIR, "manifests", "registry.ollama.ai",
                             "library", ns, t)
        with open(mpath, "r", encoding="utf-8") as f:
            man = json.load(f)
        biggest = max(man["layers"], key=lambda L: L["size"])
        blob = os.path.join(MODELS_DIR, "blobs", biggest["digest"].replace(":", "-"))
        h = hashlib.sha256()
        with open(blob, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        lines.append({"arm": arm, "tag": tag, "manifest_schema": man.get("schemaVersion"),
                      "weight_layer_digest": biggest["digest"],
                      "weight_blob_bytes": biggest["size"],
                      "blob_sha256_recomputed": h.hexdigest(),
                      "sha_matches_content_address": h.hexdigest() == biggest["digest"].split(":")[1]})
    out = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "ollama_note": "version recorded separately in receipt (ollama --version)",
           "blobs": lines}
    with open(os.path.join(HERE, "BLOBS.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


def cmd_arm(arm):
    model = ARMS[arm]
    out_path = os.path.join(HERE, "results_arm%s.jsonl" % arm)
    done = set()
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                    done.add((row["task"], row["prompt_idx"]))
                except Exception:
                    pass
    runs = build_runs()
    with open(out_path, "a", encoding="utf-8") as f:
        for run in runs:
            if (run["task"], run["prompt_idx"]) in done:
                continue
            ps_before = ollama_ps()
            resp = generate(model, run["prompt"], run["seed"])
            text = resp.get("response", "")
            g = grade(text, run["expect"])
            row = {
                "arm": arm, "model": model, "task": run["task"],
                "prompt_idx": run["prompt_idx"], "seed": run["seed"],
                "pipeline_pass": g["pipeline_pass"], "strict_pass": g["strict_pass"],
                "done_reason": resp.get("done_reason"),
                "total_duration_ns": resp.get("total_duration"),
                "eval_count": resp.get("eval_count"),
                "prompt_eval_count": resp.get("prompt_eval_count"),
                "eval_duration_ns": resp.get("eval_duration"),
                # eval_count in ollama /api/generate is the RESPONSE token count
                # (prompt tokens are prompt_eval_count); keep both raw, no subtraction.
                "out_tokens": resp.get("eval_count"),
                "wall_s": resp.get("_wall_s"),
                "empty_content": len(text.strip()) == 0,
                "think_tags": text.count("<think>"),
                "response_chars": len(text),
                "response_text": text[:2000],
                "ps_before": ps_before,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            f.write(json.dumps(row) + "\n")
            f.flush()
            print("%s %s p%d strict=%s pipe=%s reason=%s out_tok=%s wall=%ss" % (
                arm, run["task"], run["prompt_idx"], g["strict_pass"],
                g["pipeline_pass"], row["done_reason"], row["out_tokens"], row["wall_s"]), flush=True)
    print("ARM %s COMPLETE" % arm)


def pct(n, d):
    return round(100.0 * n / d, 1) if d else None


def cmd_summarize():
    rows = []
    for arm in ("A", "B"):
        p = os.path.join(HERE, "results_arm%s.jsonl" % arm)
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                rows.append(json.loads(line))
    summ = {"n_runs": len(rows), "arms": {}, "per_task": {}, "per_prompt_delta": [],
            "channels": {}}
    for arm in ("A", "B"):
        ar = [r for r in rows if r["arm"] == arm]
        n = len(ar)
        pipe = sum(1 for r in ar if r["pipeline_pass"])
        strict = sum(1 for r in ar if r["strict_pass"])
        eos = [r for r in ar if r["done_reason"] == "stop"]
        speeds = [(r["eval_duration_ns"] / 1e9, r["eval_count"]) for r in ar
                  if r["eval_count"] and r["eval_duration_ns"]]
        sps = [c / d for d, c in speeds if d > 0]
        capped = sum(1 for r in ar if r["done_reason"] != "stop")
        summ["arms"][arm] = {
            "model": ar[0]["model"], "n": n,
            "pipeline_pass": pipe, "pipeline_pct": pct(pipe, n),
            "strict_pass": strict, "strict_pct": pct(strict, n),
            "eos_terminated": len(eos), "cap_or_other_finish": capped,
            "tok_s_median": sorted(sps)[len(sps) // 2] if sps else None,
            # eval_count is authoritative (response tokens); early armA rows carry a
            # bogus negative out_tokens from a pre-fix subtraction, never summed here.
            "out_tokens_total": sum(r["eval_count"] or 0 for r in ar),
            "empty_content": sum(1 for r in ar if r["empty_content"]),
            "think_tags": sum(1 for r in ar if r["think_tags"]),
        }
        for r in ar:
            tk = summ["per_task"].setdefault(r["task"], {"A": [0, 0], "B": [0, 0]})
            tk[arm][0] += 1 if r["pipeline_pass"] else 0
            tk[arm][1] += 1
    # per-task spread of pipeline success per arm (percentage points)
    spread = {}
    for arm in ("A", "B"):
        vals = [100.0 * v[arm][0] / v[arm][1] for v in summ["per_task"].values()]
        spread[arm] = {"min": round(min(vals), 1), "max": round(max(vals), 1),
                       "spread_pp": round(max(vals) - min(vals), 1)}
    summ["per_task_pct"] = {t: {"A": round(100.0 * v["A"][0] / v["A"][1], 1),
                                "B": round(100.0 * v["B"][0] / v["B"][1], 1)}
                            for t, v in summ["per_task"].items()}
    summ["per_task_spread"] = spread
    # matched-task deltas per prompt: clean-intersection = pairs where BOTH arms
    # produced a parseable JSON object (strict-parse success); delta = passA - passB.
    # Deployment verdict above is pooled over ALL pairs; these are diagnostic only
    # (spec leg 3), reported with their sign flips across prompts.
    deltas = []
    for p_i in range(5):
        pairs = []
        for t in summ["per_task"]:
            ra = [r for r in rows if r["arm"] == "A" and r["task"] == t and r["prompt_idx"] == p_i]
            rb = [r for r in rows if r["arm"] == "B" and r["task"] == t and r["prompt_idx"] == p_i]
            if ra and rb:
                pairs.append((ra[0], rb[0]))
        clean = [(a, b) for a, b in pairs if a["strict_pass"] and b["strict_pass"]]
        if clean:
            d = sum(1 for a, b in clean if a["pipeline_pass"]) - \
                sum(1 for a, b in clean if b["pipeline_pass"])
            deltas.append({"prompt_idx": p_i, "n_clean_pairs": len(clean),
                           "delta_A_minus_B_points": d, "sign": "+" if d > 0 else ("-" if d < 0 else "0")})
        else:
            deltas.append({"prompt_idx": p_i, "n_clean_pairs": 0, "delta_A_minus_B_points": None,
                           "sign": "no-clean-pairs"})
    summ["per_prompt_delta"] = deltas
    summ["matched_task_screening_check"] = {
        "note": "deployment verdict is pooled full-pipeline over ALL pairs; deltas are diagnostic only (spec leg 3)"}
    with open(os.path.join(HERE, "SUMMARY.json"), "w", encoding="utf-8") as f:
        json.dump(summ, f, indent=2)
    print(json.dumps(summ, indent=2))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "info":
        cmd_info()
    elif cmd in ("armA", "armB"):
        cmd_arm(cmd[-1])
    elif cmd == "summarize":
        cmd_summarize()
    else:
        print("usage: run_ab.py info|armA|armB|summarize")
        sys.exit(2)
