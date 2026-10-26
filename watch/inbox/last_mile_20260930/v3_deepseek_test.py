#!/usr/bin/env python
"""v3_deepseek_test - LAST MILE V3 (2026-09-30). Owner file: V3_DEEPSEEK_TEST.md (same dir).

Tests deepseek/deepseek-v4.1-flash on Nous as a bulk workhorse against two real estate jobs:
  A) oral-law extraction: the EXACT miner ask (oral_law_mine_20260930.ASK) re-run on 5 threads
     already mined by z-ai/glm-5.3-prime (rows in watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl),
     scored vs glm's recorded rows.
  B) water-graph legality verification: a spec exercising check-valve / xor / sill-hold /
     starvation / siphon-prime / steam-condense laws; ground truth computed locally by
     mag/water_graph.py (deterministic, free oracle), DeepSeek verdicts scored against it.
BUDGET CAP $0.50 (mission). SSRF-guarded pinned host, same pattern as the miner.
"""
from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
HERMES_DIR = r"C:\Users\foste\AppData\Local\hermes"
ALLOWED_HOST = "inference-api.nousresearch.com"
BASE = "https://" + ALLOWED_HOST + "/v1/chat/completions"
MODEL = "deepseek/deepseek-v4.1-flash"
BUDGET = 0.50
LANE = REPO / "watch" / "inbox" / "last_mile_20260930"
RESULTS = LANE / "v3_deepseek_results.json"

# catalog pricing per-token (bytes from /v1/models, 2026-09-30)
PROMPT_PER_TOK = 0.0000000198
COMPLETION_PER_TOK = 0.0000003960

_spec = importlib.util.spec_from_file_location(
    "oral_law_mine", REPO / "watch" / "inbox" / "mates_leave_protocol" / "oral_law_mine_20260930.py")
miner = importlib.util.module_from_spec(_spec)
sys.modules["oral_law_mine"] = miner
_spec.loader.exec_module(miner)  # safe: module only defines functions + constants

ASK = miner.ASK
thread_body = miner.thread_body


def load_env():
    for line in open(os.path.join(HERMES_DIR, ".env"), encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


def call(prompt, key, max_tokens=6000):
    p = urllib.parse.urlparse(BASE)
    assert p.scheme == "https" and p.hostname == ALLOWED_HOST
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
               "max_tokens": max_tokens, "temperature": 0.2}
    for attempt, extra in ((0, {"reasoning": {"max_tokens": 2500}}), (1, {})):
        body = dict(payload)
        if extra:
            body.update(extra)
        req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
                                     headers={"Authorization": "Bearer " + key,
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=400) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 400 and attempt == 0:
                continue  # deepseek may reject the reasoning param: retry plain
            raise


def parse_json_obj(txt):
    txt = re.sub(r"```(?:json)?", "", txt)  # strip markdown fences
    i, j = txt.find("{"), txt.rfind("}")
    if i < 0 or j <= i:
        return None
    try:
        return json.loads(txt[i:j + 1])
    except Exception:
        return None


def literal_score(line, body_lower_words):
    """fraction of content words (len>3) of an extracted line present in the thread body"""
    text = re.sub(r"^(LAW|DEBT):\s*", "", line)
    words = [w for w in re.findall(r"[a-zA-Z0-9_.\\/]+", text.lower()) if len(w) > 3]
    if not words:
        return 1.0
    return sum(1 for w in words if w in body_lower_words) / len(words)


def main():
    load_env()
    key = os.environ.get("NOUS_SDD_API_KEY") or os.environ.get("HERMES_API_KEY_1")
    spent = 0.0
    results = {"task_a": [], "task_b": {}, "model": MODEL}

    # ---------------------------------------------------------------- task A
    idx_rows = [json.loads(l) for l in (REPO / "watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl")
                .read_text(encoding="utf-8").splitlines() if l.strip()]
    pick = [0, 14, 22]  # retry the timed-out rows; 4 and 9 already banked in v3_deepseek_results.json
    for i in pick:
        row = idx_rows[i]
        if spent >= BUDGET:
            break
        body = thread_body({"id": row["thread_id"]})
        if not body:
            results["task_a"].append({"i": i, "error": "body unresolved"})
            continue
        prompt = ASK.replace("{name}", row["thread_name"]).replace("{body}", body)
        resp = None
        err = None
        for attempt in range(2):
            try:
                resp = call(prompt, key)
                break
            except Exception as e:
                err = str(e)
                print(f"A[{i}] attempt {attempt + 1} failed: {err[:90]}")
        if resp is None:
            results["task_a"].append({"i": i, "thread": row["thread_name"], "error": err})
            continue
        usage = resp.get("usage", {})
        c = float(usage.get("cost") or 0) or (
            int(usage.get("prompt_tokens", 0)) * PROMPT_PER_TOK
            + int(usage.get("completion_tokens", 0)) * COMPLETION_PER_TOK)
        spent += c
        txt = (resp["choices"][0]["message"].get("content") or "").strip()
        data = parse_json_obj(txt)
        body_words = set(re.findall(r"[a-zA-Z0-9_.\\/]+", body.lower()))
        rec = {"i": i, "thread": row["thread_name"], "cost_usd": round(c, 5),
               "glm_cost_usd": row["cost_usd"],
               "prompt_tokens": usage.get("prompt_tokens"),
               "completion_tokens": usage.get("completion_tokens"),
               "json_ok": data is None}
        if data is None:
            rec["json_ok"] = False
            rec["raw"] = txt[:300]
        else:
            rec["json_ok"] = True
            ex = data
            rec["skip"] = bool(ex.get("skip"))
            rec["glm_skip"] = bool(row["extracted"].get("skip"))
            lines = (ex.get("decisions") or []) + (ex.get("laws_or_debts") or [])
            rec["n_lines"] = len(lines)
            rec["em_dash"] = any("\u2014" in l for l in lines)
            rec["literal_min"] = round(min([literal_score(l, body_words) for l in lines] or [1.0]), 2)
            rec["literal_mean"] = round(sum(literal_score(l, body_words) for l in lines) / max(1, len(lines)), 2)
            rec["ds_extract"] = ex
            rec["glm_extract"] = row["extracted"]
        results["task_a"].append(rec)
        print(f"A[{i}] {row['thread_name'][:35]:35s} ${c:.5f} cum ${spent:.4f} json_ok={rec['json_ok']}")

    if spent < BUDGET:
        spent = run_task_b(results, key, spent)
    finish(results, spent)


def build_task_b():
    """returns (ask_text, spec_dict). Ground truth is computed by the caller via mag.water_graph."""
    spec = {
        "schema": "water_graph.v1",
        "nodes": {
            "R1": {"elev": 10, "kind": "plain", "volume": 12, "steam": 0},
            "R2": {"elev": 9, "kind": "plain", "volume": 6, "steam": 0},
            "U": {"elev": 5, "kind": "plain", "volume": 8, "steam": 0},
            "R3": {"elev": 7, "kind": "plain", "volume": 2, "steam": 0},
            "X": {"elev": 3, "kind": "xor", "volume": 0, "steam": 0},
            "S": {"elev": 4, "kind": "sill", "sill": 2, "volume": 0, "steam": 0},
            "T": {"elev": 1, "kind": "plain", "volume": 0, "steam": 0},
            "W": {"elev": 0, "kind": "waste", "volume": 0, "steam": 0},
            "C": {"elev": 20, "kind": "cold", "volume": 0, "steam": 0},
        },
        "pipes": {
            "p1": {"src": "R1", "dst": "X", "cap": 2},
            "p2": {"src": "R2", "dst": "X", "cap": 2},
            "x_out": {"src": "X", "dst": "T", "cap": 3},
            "sip": {"src": "U", "dst": "T", "cap": 2, "siphon": True, "crest": 4},
            "p3": {"src": "R3", "dst": "S", "cap": 2},
            "s_out": {"src": "S", "dst": "W", "cap": 5},
            "p_uphill": {"src": "U", "dst": "R1", "cap": 9},
        },
    }
    # ground truth: run the real engine
    sys.path.insert(0, str(REPO))
    from mag.water_graph import from_spec
    g = from_spec(spec)
    g.boil("R1", 3)
    gt_events = []
    gt_events += g.tick()
    gt_events += g.tick()
    g.close("p2")
    gt_events += g.tick()
    gt_events += g.tick()
    gt_final = {n: g.volume(n) for n in g.nodes}
    gt = {"events": gt_events, "final": gt_final}

    ask_b = """You are the legality verifier (propagator) for the estate's water-graph engine.
Physics laws of the engine (EXACT semantics, integer volumes, deterministic):
1. Check valve: a normal pipe flows only if src elevation > dst elevation; NEVER uphill, no backflow.
2. Siphon pipe: primes only when src volume >= crest AND src elev > dst elev; once primed flows min(cap, src volume) each tick; breaks when intake runs dry.
3. XOR junction: delivers only when EXACTLY ONE inlet delivered this tick; on two inlets it does NOT deliver, the inflow is HELD pooled in the junction.
4. SILL junction: gate needs >= sill inlets delivering this tick; below gate the inflow is HELD pooled; if a later tick brings NO new inflow while pooled volume exists, the pooled water is spilled to waste with a STARVED event naming node, amount, gate.
5. Gated junction outflow pipes run only on ticks where the gate passed.
6. Steam: boil lifts volume to steam; each tick ALL steam condenses at the HIGHEST cold node (ignores pipes); if no cold node exists it returns to origin.
7. Waste swallows anything routed to it.

SPEC (water_graph.v1):
%s

OPERATIONS: boil(R1, 3); tick(); tick(); close pipe p2; tick(); tick().

ANSWER as ONE JSON object, no prose:
{"tick_events": {"1": ["short event lines"], "2": [...], "3": [...], "4": [...]},
 "final_volumes": {"R1": n, "R2": n, "U": n, "R3": n, "X": n, "S": n, "T": n, "W": n, "C": n},
 "legality": {
   "p_uphill_ever_flows": true/false,
   "x_delivers_on_both_inlet_tick": true/false,
   "s_junction_pool_spilled_with_starved_event": true/false,
   "sip_primed_at_crest": true/false,
   "steam_condenses_at_C": true/false,
   "x_out_flows_only_when_gate_passed": true/false,
   "held_below_gate_water_survives_to_later_tick": true/false
 },
 "violations_found": ["any law the SPEC itself violates, else empty list"]}
Numbers must be integers. No em-dashes.""" % json.dumps(spec)
    return ask_b, gt, gt_events, gt_final


def run_task_b(results, key, spent, max_tokens=12000):
    ask_b, gt, gt_events, gt_final = build_task_b()
    try:
        resp = call(ask_b, key, max_tokens=max_tokens)
        usage = resp.get("usage", {})
        c = float(usage.get("cost") or 0) or (
            int(usage.get("prompt_tokens", 0)) * PROMPT_PER_TOK
            + int(usage.get("completion_tokens", 0)) * COMPLETION_PER_TOK)
        spent += c
        txt = (resp["choices"][0]["message"].get("content") or "").strip()
        data = parse_json_obj(txt)
        results["task_b"] = {"cost_usd": round(c, 5),
                             "prompt_tokens": usage.get("prompt_tokens"),
                             "completion_tokens": usage.get("completion_tokens"),
                             "json_ok": data is not None, "ds": data,
                             "raw": txt[:4000], "ground_truth": gt,
                             "max_tokens": max_tokens}
        print(f"B water-graph ${c:.5f} cum ${spent:.4f} json_ok={data is not None}")
    except Exception as e:
        results["task_b"] = {"error": str(e), "ground_truth": gt}
    return spent


def finish(results, spent):
    results["spent_usd"] = round(spent, 5)
    if RESULTS.exists():  # merge banked rows from earlier attempts of this same test
        try:
            old = json.loads(RESULTS.read_text(encoding="utf-8"))
            have = {r.get("i") for r in results["task_a"]}
            for r in old.get("task_a", []):
                if r.get("i") not in have:
                    results["task_a"].insert(0, r)
            results["spent_usd"] = round(results["spent_usd"] + float(old.get("spent_usd", 0)), 5)
        except Exception:
            pass
    results["task_a"].sort(key=lambda r: r.get("i") if r.get("i") is not None else 99)
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"TOTAL SPENT ${spent:.5f} -> {RESULTS}")
    gt_events = results.get("task_b", {}).get("ground_truth", {}).get("events", [])
    for e in gt_events:
        print("  ", e)
    print("GROUND TRUTH final:", results.get("task_b", {}).get("ground_truth", {}).get("final"))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "b":  # B-only rerun (A rows stay banked via finish-merge)
        load_env()
        key = os.environ.get("NOUS_SDD_API_KEY") or os.environ.get("HERMES_API_KEY_1")
        results = {"task_a": [], "model": MODEL}
        spent = run_task_b(results, key, 0.0)
        finish(results, spent)
    else:
        main()
