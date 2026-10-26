"""F4 flash-vs-max census - systematic quality across work-shapes (2026-09-30).

Mission (operator, beyond the duel): the LW9/W8 duels answered "who wins one
ask"; this census answers "which family wins which WORK-SHAPE". 25 mini
tasks (5 shapes x 5 tasks), each fired at BOTH contenders:

  flash = deepseek/deepseek-v4.1-flash  (WORK lane, thinking-OFF mandatory,
         W8 router law: thinking-on burns the whole budget on schema/plan)
  max   = qwen/qwen3.8-max-prime        (driving-ladder workhorse+judgment)

Shapes (the work this estate actually runs):
  code-writing  write a small function
  analysis      read a real repo file and summarize it
  extraction    pull strict structured data from prose
  judgment      pick the better of two options with reasoning
  creative      generate exactly 5 alternative approaches

Judging: THIRD family google/gemini-3.8-flash, BLIND (contenders shown as
A and B only, identities never in the judge prompt), slot order shuffled
per task by a seeded coin (recorded in the row; slot tally reported so
position bias stays visible). Judge prompt + parser are reused verbatim
from tools/duel_harness.py (v1.1 blind shape) so verdicts parse under the
battle-tested contract.

Budget: $0.50 ABSOLUTE including preflight probes. Spend is metered from
usage.cost (API truth), price-table fallback otherwise. Idempotent on
banked task ids; contender answers cached in f4_contenders.jsonl so a
killed run resumes without re-paying. No writes to logs/duel/duels.jsonl
(that ledger is not this lane's file ownership): rows land in
f4_census_rows.jsonl, same shape as duel rows plus census fields.

Laws honored: width 1 (sequential), no em-dashes in anything written,
no model rotation on retry (same model, same key set), trust bytes not
projections (every number in the receipt comes from these rows).

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/f4_flash_census.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/f4_flash_census.py --preflight
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/f4_flash_census.py [--limit N]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402

FLASH = "deepseek/deepseek-v4.1-flash"
MAXM = "qwen/qwen3.8-max-prime"
JUDGE = "google/gemini-3.8-flash"

# Published fallback only; fire() prefers usage.cost from the API.
# ds rates: V3 catalog bytes 2026-09-30. qwen: Nous list. gemini: d6
# operator-published blended rate (3.38, 3.38).
dh.PRICE[FLASH] = (0.0198, 0.396)
dh.PRICE[JUDGE] = (3.38, 3.38)

BUDGET_CAP = 0.50            # ABSOLUTE for THIS mission, preflight included
SOFT_STOP = 0.47             # stop starting a new task past this spend
PROJECTED_PER_TASK = 0.025   # charged before each task fires
CONTENDER_TOKENS = 800       # mini tasks: bound the answer, bound the cost
JUDGE_TOKENS = 600
REASONING_QWEN = {"max_tokens": 800}   # mini asks; deep reasoning unneeded
REASONING_DS_OFF = {"enabled": False}  # W8 router law for ds long-form

ROWS_PATH = HERE / "f4_census_rows.jsonl"
CACHE_PATH = HERE / "f4_contenders.jsonl"
CORR_PATH = HERE / "f4_corr_id.txt"
GEMINI_REASONING_PATH = HERE / "f4_gemini_reasoning.json"

WORDS_RE = re.compile(r"\S+")
FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def series_corr_id() -> str:
    """Stable per-series join id (AH14 shape); minted once, kept on disk."""
    if CORR_PATH.is_file():
        return CORR_PATH.read_text(encoding="utf-8").strip()
    cid = uuid.uuid4().hex[:8]
    CORR_PATH.write_text(cid + "\n", encoding="utf-8")
    return cid


# ---------------------------------------------------------------------------
# transport: streaming SSE for qwen/gemini (V1 multifamily gateway law:
# long non-streaming sockets die on read timeouts), plain POST for ds
# (W8 proved non-streaming fine once thinking is off).
# ---------------------------------------------------------------------------

def call_plain(model: str, prompt: str, key: str, max_tokens: int,
               reasoning: dict) -> dict:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "reasoning": reasoning,
    }).encode()
    req = urllib.request.Request(
        dh.BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def call_stream(model: str, prompt: str, key: str, max_tokens: int,
                reasoning: dict) -> dict:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "reasoning": reasoning,
        "stream": True,
        "stream_options": {"include_usage": True},
    }).encode()
    req = urllib.request.Request(
        dh.BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    parts: list[str] = []
    usage: dict = {}
    with urllib.request.urlopen(req, timeout=600) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            choices = chunk.get("choices") or [{}]
            delta = choices[0].get("delta") or {}
            if delta.get("content"):
                parts.append(delta["content"])
            if chunk.get("usage"):
                usage = chunk["usage"]
    return {"choices": [{"message": {"content": "".join(parts)}}], "usage": usage}


def gemini_reasoning() -> dict:
    """Judge reasoning shape: thinking-off unless preflight banked a
    fallback (the gateway 400s on 'enabled' for some families; W8 saw
    this exact rejection on qwen3.7-flash)."""
    if GEMINI_REASONING_PATH.is_file():
        try:
            return json.loads(GEMINI_REASONING_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"enabled": False}


def call(model: str, prompt: str, key: str, max_tokens: int,
         reasoning: dict | None = None) -> dict:
    if model == FLASH:
        return call_plain(model, prompt, key, max_tokens, reasoning or REASONING_DS_OFF)
    return call_stream(model, prompt, key, max_tokens,
                       reasoning if reasoning is not None else REASONING_QWEN)


def fire(model: str, prompt: str, keys: list[str], tag: str,
         max_tokens: int, reasoning: dict | None = None) -> tuple[str, float]:
    """One call, single retry (same model, next key). No rotation ever."""
    last_err: Exception | None = None
    for attempt in (1, 2):
        key = keys[hash((tag, attempt)) % len(keys)]
        try:
            t0 = time.time()
            resp = call(model, prompt, key, max_tokens, reasoning)
            usage = resp.get("usage", {}) or {}
            cost = dh.cost_of(model, usage)
            content = (resp["choices"][0]["message"].get("content") or "")
            if not content.strip():
                raise ValueError("empty content")
            print(f"fire {tag} model={model} cost=${cost:.4f} "
                  f"secs={time.time() - t0:.1f} chars={len(content)}", flush=True)
            return content, cost
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError,
                OSError, KeyError, TimeoutError) as e:
            last_err = e
            print(f"retry {tag} after {type(e).__name__}: {e}", flush=True)
    raise RuntimeError(f"{tag}: both attempts failed: {last_err}")


# ---------------------------------------------------------------------------
# tasks: 5 shapes x 5 mini tasks. analysis asks embed real repo bytes.
# ---------------------------------------------------------------------------

LAWS = ("Laws: no em-dashes in your output. Be concise: under 220 words "
        "unless the code genuinely needs more. No preamble, no praise.")

RUBRICS = {
    "code-writing": ["correctness", "edge-case handling", "clarity"],
    "analysis": ["accuracy", "coverage", "concision"],
    "extraction": ["schema fidelity", "completeness", "accuracy"],
    "judgment": ["decision clarity", "justification quality", "tradeoff awareness"],
    "creative": ["distinctiveness", "feasibility", "grounding"],
}


def read(rel: str, limit: int) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")[:limit]


def build_tasks() -> list[dict]:
    t: list[dict] = []

    def add(tid: str, shape: str, ask: str):
        t.append({"id": tid, "shape": shape, "ask": ask, "rubric": RUBRICS[shape]})

    # ---------------------------------------------------------- code-writing
    add("f4-code-slug", "code-writing",
        "Write a Python function slug(title: str, date: str) -> str that returns "
        "a keystone slug: date as YYYY-MM-DD prefix, then the title lowercased, "
        "spaces to hyphens, punctuation stripped, collapsed hyphens. Show 3 "
        "assert examples including one with punctuation. " + LAWS)
    add("f4-code-median", "code-writing",
        "Write a Python function rolling_median(nums: list[float], k: int) -> "
        "list[float] returning the median of each sliding window of size k. "
        "State how you handle even k and k larger than len(nums). Include 2 "
        "assert examples. " + LAWS)
    add("f4-code-duration", "code-writing",
        "Write a Python function parse_duration(s: str) -> int that parses "
        "strings like '2d 4h 30m', '90s', '1h' into total minutes as int "
        "(seconds floor-divided into minutes), units allowed in any order, "
        "repeated units allowed, and raises ValueError on garbage. 3 assert "
        "examples including one ValueError case. " + LAWS)
    add("f4-code-brackets", "code-writing",
        "Write a Python function is_balanced(s: str) -> bool checking balanced "
        "brackets for () [] {} with correct nesting, ignoring other "
        "characters. 3 assert examples. " + LAWS)
    add("f4-code-intervals", "code-writing",
        "Write a Python function merge_intervals(pairs: list[tuple[int, int]]) "
        "-> list[tuple[int, int]] merging overlapping or touching [start, end] "
        "intervals, input not necessarily sorted, empty input returns empty. "
        "2 assert examples. " + LAWS)

    # -------------------------------------------------------------- analysis
    an_laws = ("Summarize in under 180 words: what this artifact does, its "
               "core rule or mechanism, its output/exit contract, and one "
               "real limitation you can see in the bytes. Laws: no em-dashes. "
               "No preamble.")
    for tid, rel, lim in [
        ("f4-an-freshness", r"tools\freshness_check.py", 2400),
        ("f4-an-warmboot", r"mag\hermes_warm_boot.py", 2200),
        ("f4-an-animal", r"tools\animal_profiles.py", 2200),
        ("f4-an-contract", r"watch\inbox\SHARED_SURFACE_CONTRACT.json", 2200),
        ("f4-an-drift", r"tools\census_drift_patrol.py", 2200),
    ]:
        add(tid, "analysis",
            "<SOURCE>\n" + read(rel, lim) + "\n</SOURCE>\n\n" + an_laws)

    # ------------------------------------------------------------- extraction
    ex_laws = ("Return ONLY strict JSON, no prose outside the JSON, no "
               "markdown fences. Laws: no em-dashes inside the JSON.")
    add("f4-ex-dispatch", "extraction",
        "Extract every event as JSON: {\"events\": [{\"time\": \"HH:MM\", "
        "\"actor\": str, \"action\": str, \"cost_usd\": float_or_null}]}. "
        "Prose: 'At 09:02 the janitor ran a sweep costing $0.0041. At 09:17 "
        "the orchestrator dispatched a duel, no cost recorded. At 09:31 the "
        "biographer answered a query for $0.0008. At 09:45 the janitor "
        "refused an unkeyed write, cost none.' " + ex_laws)
    add("f4-ex-spend", "extraction",
        "Extract the spend table as JSON: {\"total_usd\": float, \"items\": "
        "[{\"name\": str, \"usd\": float}]}. Prose: 'Window spend: contender "
        "fires $0.0548, judge calls $0.2308, key probes $0.0183, plus a "
        "worst-case estimate of $0.0250 for two unmetered timeouts. Total "
        "was $0.3289.' " + ex_laws)
    add("f4-ex-outage", "extraction",
        "Extract the incident as JSON: {\"cause\": str, \"window_minutes\": "
        "int, \"steps\": [str]}. Prose: 'The router died at 10:04 and came "
        "back at 10:19, fifteen minutes dark. Cause: an expired sign-in. "
        "Recovery steps were: detect the provider error, resolve the "
        "credentials with the user, resume the stopped run from its journal.' "
        + ex_laws)
    add("f4-ex-eval", "extraction",
        "Extract the eval tally as JSON: {\"rows\": [{\"model\": str, "
        "\"wins\": int, \"losses\": int, \"ties\": int, \"mean_cost_usd\": "
        "float}]}. Prose: 'glm-prime went 6 wins 0 losses 0 ties at a mean "
        "$0.03 per answer. ds-v4.1-flash matched 6-0-0 at $0.0043 mean. "
        "grok-4.3 fell to 0-6-0 at $0.0048 mean. qwen3.7-flash also 0-6-0 "
        "at $0.0005 mean.' " + ex_laws)
    add("f4-ex-workorder", "extraction",
        "Extract the work order as JSON: {\"tasks\": [{\"id\": str, "
        "\"owner\": str, \"due\": \"YYYY-MM-DD\", \"done\": bool}]}. Prose: "
        "'Task T-101, owner ZCode, due 2026-10-01, is done. Task T-102, "
        "owner Hermes, due 2026-10-02, is not done. Task T-103 is unowned, "
        "due 2026-10-05, not done. Task T-104, owner ZCode again, was "
        "finished early, due 2026-09-30, done.' " + ex_laws)

    # --------------------------------------------------------------- judgment
    jd_laws = ("Pick ONE option and justify it. Name what you would lose by "
               "not picking the other. Laws: no em-dashes, under 160 words, "
               "no preamble.")
    add("f4-jd-code", "judgment",
        "Which snippet is better for counting metered retries, and why?\n"
        "OPTION 1:\nattempts = 0\nwhile True:\n    attempts += 1\n    "
        "try:\n        return call()\n    except HTTPError:\n        "
        "if attempts >= 2: raise\n\n"
        "OPTION 2:\nfor attempt in (1, 2):\n    try:\n        return "
        "call()\n    except HTTPError:\n        last = attempt\nelse:\n    "
        "raise RuntimeError('retries exhausted')\n" + jd_laws)
    add("f4-jd-layout", "judgment",
        "A multi-agent estate needs one durable cross-session write surface. "
        "OPTION 1: a single flat inbox directory with a JSON index file "
        "every session appends to. OPTION 2: per-day subdirectories each "
        "with their own index, plus a top-level pointer file. Which is "
        "better for concurrent writers, and why? " + jd_laws)
    add("f4-jd-errors", "judgment",
        "A metered LLM loop must stay under a hard $0.50 cap per run. "
        "OPTION 1: exponential backoff retry (up to 5 attempts) on any HTTP "
        "error, then continue the loop. OPTION 2: fail fast on the first "
        "error, bank what was done, exit nonzero. Which is better, and "
        "why? " + jd_laws)
    add("f4-jd-name", "judgment",
        "Naming a config field that bounds API retries for a duel harness "
        "where contenders must NEVER rotate models. OPTION 1: name it "
        "'max_attempts'. OPTION 2: name it 'retry_budget'. Which better "
        "prevents a future maintainer from breaking the no-rotation law, "
        "and why? " + jd_laws)
    add("f4-jd-tests", "judgment",
        "For a pre-push gate on a 2000-test repo, you can afford one: "
        "OPTION 1: 50 fast unit tests covering the gate's parser and exit "
        "codes (seconds). OPTION 2: 1 end-to-end integration test that "
        "pushes against a fake remote (minutes). Which gives the gate more "
        "protection per second of CI time, and why? " + jd_laws)

    # ---------------------------------------------------------------- creative
    cr_laws = ("Give EXACTLY 5 alternative approaches, numbered 1-5, one "
               "line each, each technically distinct (not rewordings). "
               "Laws: no em-dashes, no preamble.")
    add("f4-cr-drift", "creative",
        "Problem: a test-count headline in a doc drifts from the real "
        "pytest collect count, and nobody notices for weeks. Generate 5 "
        "alternative approaches to catch the drift automatically. " + cr_laws)
    add("f4-cr-fence", "creative",
        "Problem: LLM agent seats keep writing durable files outside the "
        "one shared inbox directory. Generate 5 alternative approaches to "
        "fence them in. " + cr_laws)
    add("f4-cr-budget", "creative",
        "Problem: metered API calls must stay under a hard per-run dollar "
        "cap but costs are only known after each response. Generate 5 "
        "alternative approaches to enforce the cap. " + cr_laws)
    add("f4-cr-warmboot", "creative",
        "Problem: a warm-boot cache file goes stale between sessions and no "
        "daemon may run. Generate 5 alternative approaches to keep it "
        "fresh. " + cr_laws)
    add("f4-cr-packer", "creative",
        "Problem: a context pack for agent seats burns too many prompt "
        "tokens. Generate 5 alternative approaches to shrink it without "
        "losing load-bearing facts. " + cr_laws)

    return t


# ---------------------------------------------------------------------------
# caches, spend truth, rows
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if path.is_file():
        with path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return rows


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def cached_answers() -> dict[tuple[str, str], dict]:
    return {(r["task_id"], r["model"]): r for r in load_jsonl(CACHE_PATH)}


def spent_so_far() -> float:
    s = 0.0
    for r in load_jsonl(CACHE_PATH):
        s += float(r.get("cost", 0.0))
    for r in load_jsonl(ROWS_PATH):
        s += float(r.get("judge_cost", 0.0) or 0.0)
    return s


def metrics(text: str) -> dict:
    return {"chars": len(text),
            "words": len(WORDS_RE.findall(text)),
            "headers": dh.count_headers(text)}


def json_valid(text: str) -> bool:
    body = text.strip()
    m = FENCE_RE.search(body)
    if m:
        body = m.group(1).strip()
    try:
        json.loads(body)
        return True
    except json.JSONDecodeError:
        return False


def get_answer(task: dict, model: str, keys: list[str],
               cache: dict, spent: float) -> tuple[dict, float]:
    """Fire or load one contender answer. Returns (record, new_spend)."""
    ck = (task["id"], model)
    if ck in cache:
        rec = dict(cache[ck])
        rec["cached"] = True
        return rec, spent
    try:
        content, cost = fire(model, task["ask"], keys, f"{task['id']}:{model.split('/')[-1]}",
                             CONTENDER_TOKENS)
        rec = {"task_id": task["id"], "shape": task["shape"], "model": model,
               "content": content, "cost": round(cost, 6), "error": None,
               **metrics(content)}
        if task["shape"] == "extraction":
            rec["json_valid"] = json_valid(content)
    except Exception as e:  # noqa: BLE001
        rec = {"task_id": task["id"], "shape": task["shape"], "model": model,
               "content": "", "cost": 0.0, "error": f"{type(e).__name__}: {e}",
               "chars": 0, "words": 0, "headers": 0}
        if task["shape"] == "extraction":
            rec["json_valid"] = False
        append_jsonl(CACHE_PATH, rec)
        cache[ck] = rec
        return rec, spent
    append_jsonl(CACHE_PATH, rec)
    cache[ck] = rec
    return rec, spent + cost


def judge_pair(task: dict, flash_rec: dict, max_rec: dict, keys: list[str],
               swap: bool) -> tuple[dict, float]:
    """Blind third-family judgment. slot A carries max text when swap."""
    logical_a, logical_b = flash_rec["content"], max_rec["content"]
    slot_a, slot_b = (logical_b, logical_a) if swap else (logical_a, logical_b)
    jp = dh.judge_prompt(task["ask"], slot_a, slot_b, task["rubric"])
    # gemini judge: thinking disabled by default (validated by --preflight);
    # preflight persists the fallback shape if the gateway 400s on it
    j_reason = gemini_reasoning()
    j_text, j_cost = fire(JUDGE, jp, keys, f"{task['id']}:JUDGE", JUDGE_TOKENS,
                          reasoning=j_reason)
    v = dh.parse_judge(j_text)
    winner_slot = v["winner"]
    if swap and winner_slot in ("A", "B"):
        winner_logical = "B" if winner_slot == "A" else "A"
    else:
        winner_logical = winner_slot
    winner = {"A": "flash", "B": "max", "TIE": "TIE",
              "UNPARSED": "UNPARSED"}[winner_logical]
    crit = v["criteria"]
    if swap:
        crit = [dict(c, a=c["b"], b=c["a"]) for c in crit]
    # criteria remapped: a=flash, b=max
    return {"winner": winner, "criteria": crit, "rationale": v["rationale"],
            "parsed": v["parsed"]}, j_cost


def run(tasks: list[dict], limit: int) -> int:
    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2
    corr = series_corr_id()
    banked = {r["task_id"] for r in load_jsonl(ROWS_PATH)}
    cache = cached_answers()
    todo = [t for t in tasks if t["id"] not in banked]
    if limit:
        todo = todo[:limit]
    spent = spent_so_far()
    print(f"corr_id={corr} banked={len(banked)} todo={len(todo)} "
          f"resumed_spent=${spent:.4f}", flush=True)

    for task in todo:
        if spent + PROJECTED_PER_TASK > SOFT_STOP:
            print(f"BUDGET HOLD: spent ${spent:.4f} + projected "
                  f"${PROJECTED_PER_TASK} past soft stop ${SOFT_STOP:.2f}; "
                  f"halting before {task['id']}", flush=True)
            break
        rng = random.Random(corr + task["id"])
        swap = rng.random() < 0.5
        flash_rec, spent = get_answer(task, FLASH, keys, cache, spent)
        max_rec, spent = get_answer(task, MAXM, keys, cache, spent)
        row = {"task_id": task["id"], "shape": task["shape"], "corr_id": corr,
               "ts": datetime.now(timezone.utc).isoformat(),
               "flash_model": FLASH, "max_model": MAXM, "judge": JUDGE,
               "swap": swap,
               "slot_of_flash": "B" if swap else "A",
               "flash": {k: flash_rec[k] for k in
                         ("content", "cost", "error", "chars", "words",
                          "headers", "json_valid") if k in flash_rec},
               "max": {k: max_rec[k] for k in
                       ("content", "cost", "error", "chars", "words",
                        "headers", "json_valid") if k in max_rec}}
        if flash_rec["error"] or max_rec["error"]:
            row["winner"] = "ERROR"
            row["criteria"], row["rationale"] = [], ""
            row["judge_cost"] = 0.0
            print(f"TASK {task['id']} contender error, no judge fired",
                  flush=True)
        else:
            try:
                verdict, j_cost = judge_pair(task, flash_rec, max_rec, keys, swap)
                spent += j_cost
                row.update(verdict)
                row["judge_cost"] = round(j_cost, 6)
            except Exception as e:  # noqa: BLE001
                row["winner"] = "JUDGE_ERROR"
                row["criteria"], row["rationale"] = [], ""
                row["judge_error"] = f"{type(e).__name__}: {e}"
                row["judge_cost"] = 0.0
                print(f"JUDGE FAILED {task['id']}: {e}", flush=True)
        append_jsonl(ROWS_PATH, row)
        print(f"ROW {task['id']} shape={task['shape']} winner={row['winner']} "
              f"spent=${spent:.4f}", flush=True)
        if spent >= BUDGET_CAP:
            print(f"BUDGET BLOWN at ${spent:.4f} after {task['id']}; halting",
                  flush=True)
            break
    print(f"SERIES DONE spent=${spent:.4f} cap=${BUDGET_CAP:.2f}", flush=True)
    return 0


def preflight(keys: list[str]) -> float:
    """Three tiny probes: ds thinking-off shape, qwen stream shape, gemini
    reasoning-disabled judge shape (fallback reasoning-capped). Returns spend."""
    spent = 0.0
    probe = ("Reply with the single word OK and nothing else.")
    for model, reasoning, label in [
        (FLASH, REASONING_DS_OFF, "ds-thinkoff"),
        (MAXM, REASONING_QWEN, "qwen-stream"),
        (JUDGE, {"enabled": False}, "gemini-judge"),
    ]:
        try:
            content, cost = fire(model, probe, keys, f"preflight-{label}",
                                 400, reasoning=reasoning)
            spent += cost
            print(f"probe {label}: OK cost=${cost:.5f} "
                  f"reply={content.strip()[:20]!r}", flush=True)
        except Exception as e:  # noqa: BLE001
            if model == JUDGE:
                print(f"probe gemini-judge failed ({e}); retrying with "
                      "reasoning cap 800", flush=True)
                try:
                    content, cost = fire(model, probe, keys,
                                         "preflight-gemini-cap", 400,
                                         reasoning={"max_tokens": 800})
                    spent += cost
                    GEMINI_REASONING_PATH.write_text(
                        json.dumps({"max_tokens": 800}), encoding="utf-8")
                    print(f"probe gemini-cap: OK cost=${cost:.5f} "
                          f"(fallback banked to {GEMINI_REASONING_PATH.name})",
                          flush=True)
                except Exception as e2:  # noqa: BLE001
                    print(f"probe gemini-cap FAILED: {e2}", flush=True)
            else:
                print(f"probe {label} FAILED: {e}", flush=True)
    return spent


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="F4 flash-vs-max work-shape census")
    p.add_argument("--dry", action="store_true", help="print the plan, no calls")
    p.add_argument("--preflight", action="store_true",
                   help="run the 3 cheap probes only")
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args(argv)
    tasks = build_tasks()
    if args.dry:
        print(json.dumps({
            "series": "f4-flash-census", "budget_cap": BUDGET_CAP,
            "flash": FLASH, "max": MAXM, "judge": JUDGE,
            "tasks": [{"id": t["id"], "shape": t["shape"],
                       "ask_chars": len(t["ask"])} for t in tasks],
            "banked": [r["task_id"] for r in load_jsonl(ROWS_PATH)],
            "spent_so_far": round(spent_so_far(), 4),
        }, indent=2))
        return 0
    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2
    if args.preflight:
        spent = preflight(keys)
        print(f"preflight spend ${spent:.5f}")
        return 0
    return run(tasks, args.limit)


if __name__ == "__main__":
    sys.exit(main())
