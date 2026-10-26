"""w4_rerun_harness_20260925.py - GAUNTLET W4 RERUN (owed per GAUNTLET_W4_VERDICT_20260925.md)

Rerun conditions from the verdict doc (all three fixed here):
  (a) model id bug fixed: model="deepseek-chat" (the 09-01 run passed the env-var
      NAME "DEEPSEEK_API_KEY" where the model id belongs -> 40/60 invalid_request_error rows).
  (b) >=50 varied tails per arm (10 instruction types x 5 wording variants = 50 per arm).
  (c) cacheFloorOk: null on non-200 rows (writer bug fix; original wrote true).

Mechanic preserved from GAUNTLET_W4_READY_20260901.md:
  WARM = call same frozen prefix 2x (ctrl warmup), then steered call.
  COLD = fresh prefix variant per trial (byte-diff -> miss), no warmup, COLD_REPS=37.
  Prefix = "NIGHT_SHIFT_CACHE_PROBE_20260901_V1. " + "cache-me-now-2026..." * WARM_REPS
  (~4.8K tok per preregistration; reps calibrated 09-25, see note at WARM_REPS).
  Per trial: obey, cachedTok (warm floor 4800 per READY doc, stricter than the 95% bar),
  ms, cost$ (in .14/out .28/cache-hit .03 per M).

Predicates fixed by the READY doc table (T01..T10), applied identically to both arms.

Budget: brief allows pennies, <=~250 calls. This run: 50*3 (warm) + 50 (cold) = 200 calls.
Hard abort if cumulative estimated spend exceeds SPEND_CAP_USD.

Receipts -> watch/gauntlet_w4_rerun_receipts.jsonl (append-only, json.dumps per row).
Summary  -> watch/gauntlet_w4_rerun_summary.json.
Run: watch$ ../.venv/Scripts/python.exe w4_rerun_harness_20260925.py [--dry]
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WATCH = REPO / "watch"
ENV = REPO / ".env"
RECEIPTS = WATCH / "gauntlet_w4_rerun_receipts.jsonl"
SUMMARY = WATCH / "gauntlet_w4_rerun_summary.json"

MODEL = "deepseek-chat"  # (a) the fix. Never pass the env-var name here.
API_URL = "https://api.deepseek.com/v1/chat/completions"
TEMP = 0.2
MAX_TOKENS = 300
PRICE_IN = 0.14 / 1e6
PRICE_OUT = 0.28 / 1e6
PRICE_CACHE = 0.03 / 1e6
SPEND_CAP_USD = 0.50
WARM_REPS = 630  # calibrated 09-25 by probe: doc's 380 reps tokenizes to ~3045 tok on the
# current tokenizer (promptTok 3085, cached 2944=46 blocks); 630 reps measures promptTok
# 5086, cached 4864 (76 blocks) - the preregistered ~4.8K prefix, matching the 09-01
# run's own measured cachedTok=4864. Preregistered SIZE (~4.8K, floor 4800) is honored;
# the doc's rep count was an implementation estimate, not the fixed quantity.
COLD_REPS = 37
VARIANTS = 5  # wording variants per instruction type -> 50 tails per arm
WARM_FLOOR_TOK = 4800  # preregistered READY-doc floor; 95% of 4872 = 4628, so this is stricter

PREFIX_WARM = "NIGHT_SHIFT_CACHE_PROBE_20260901_V1. " + "cache-me-now-2026..." * WARM_REPS


def cold_prefix(i: int) -> str:
    return (f"NIGHT_SHIFT_COLD_{i}_PROBE_20260925_V1. "
            + f"cache-me-cold-{i}-2026..." * COLD_REPS)


SYSTEM = "You are a precise instruction-following assistant. Obey the user's constraint exactly."
WARMUP_TAIL = "Reply with the single word READY."


def get_key(path: Path, name: str) -> str:
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise KeyError(name)


# --- the 10 preregistered steering instruction types (READY doc table) -------------
# each: (trial id, expect label, 5 instruction wordings, predicate)
ACCENTS_FR = re.compile("[àâäçéèêëîïôöùûüÿœæ]", re.IGNORECASE)
ACCENTS_ES = re.compile("[áéíóúñü¿¡]", re.IGNORECASE)

TYPES = [
    ("T01_wordcount3", "exactly 3 words",
     ["Reply in exactly 3 words.",
      "Your entire reply must be exactly 3 words long.",
      "Answer using exactly 3 words, no more, no fewer.",
      "Give a reply of exactly 3 words.",
      "Respond with 3 words and nothing else."],
     lambda o: len(o.split()) == 3),
    ("T02_fixedkeyword", "sentence with ELDRITCHCOG",
     ["Write one sentence that contains the word ELDRITCHCOG.",
      "Compose a sentence including ELDRITCHCOG somewhere in it.",
      "Reply with a single sentence containing the token ELDRITCHCOG.",
      "Produce one sentence in which ELDRITCHCOG appears.",
      "Say one sentence and make sure ELDRITCHCOG is in it."],
     lambda o: bool(re.search(r"ELDRITCHCOG", o))),
    ("T03_jsonshape", 'exact JSON {"flag":1,"ok":true}',
     ['Reply with exactly this JSON and nothing else: {"flag":1,"ok":true}',
      'Output only the JSON object {"flag":1,"ok":true}.',
      'Your complete response must be the JSON {"flag":1,"ok":true}.',
      'Return the exact JSON object {"flag":1,"ok":true} with no other text.',
      'Send back precisely {"flag":1,"ok":true} as your whole answer.'],
     lambda o: _json_eq(o, {"flag": 1, "ok": True})),
    ("T04_langFR", "French sentence (accented)",
     ["Answer with one sentence in French.",
      "Reply in French with a single sentence.",
      "Write your response in French, one sentence only.",
      "Give the answer as one French sentence.",
      "Respond entirely in French using one sentence."],
     lambda o: bool(ACCENTS_FR.search(o))),
    ("T05_wordcount_keyword", "5 words, first=ZORB",
     ["Reply in exactly 5 words and make the first word ZORB.",
      "Use exactly 5 words, and the very first must be ZORB.",
      "Answer with a 5-word reply that starts with the word ZORB.",
      "Give exactly five words in response, beginning with ZORB.",
      "Respond in precisely 5 words where word one is ZORB."],
     lambda o: (lambda w: len(w) == 5 and w[0].upper() == "ZORB")(o.split())),
    ("T06_json_nested", 'exact JSON {"n":3,"items":[1,2,3]}',
     ['Reply with exactly this JSON and nothing else: {"n":3,"items":[1,2,3]}',
      'Output only the JSON object {"n":3,"items":[1,2,3]}.',
      'Your complete response must be the JSON {"n":3,"items":[1,2,3]}.',
      'Return the exact JSON {"n":3,"items":[1,2,3]} with no other text.',
      'Send back precisely {"n":3,"items":[1,2,3]} as your whole answer.'],
     lambda o: _json_eq(o, {"n": 3, "items": [1, 2, 3]})),
    ("T07_langES_keyword", "Spanish with ARCOIRIS",
     ["Escribe una frase en espanol que contenga la palabra ARCOIRIS.",
      "Write one sentence in Spanish that includes the word ARCOIRIS.",
      "Reply in Spanish with a single sentence containing ARCOIRIS.",
      "Answer in Spanish, one sentence, and use the word ARCOIRIS in it.",
      "Compose a Spanish sentence featuring the word ARCOIRIS."],
     lambda o: ("ARCOIRIS" in o) and bool(ACCENTS_ES.search(o))),
    ("T08_negkeyword", "READY (no Q naturally)",
     ["Reply with exactly the word READY and nothing else.",
      "Your entire response must be the single word READY.",
      "Answer using only the word READY.",
      "Send back one word only: READY.",
      "Respond with just READY, no other characters."],
     lambda o: o.strip() == "READY"),
    ("T09_json_array", 'exact JSON ["alpha","beta","gamma"]',
     ['Reply with exactly this JSON array and nothing else: ["alpha","beta","gamma"]',
      'Output only the JSON array ["alpha","beta","gamma"].',
      'Your complete response must be the array ["alpha","beta","gamma"].',
      'Return the exact JSON array ["alpha","beta","gamma"] with no other text.',
      'Send back precisely ["alpha","beta","gamma"] as your whole answer.'],
     lambda o: _json_eq(o, ["alpha", "beta", "gamma"])),
    ("T10_langDE_keyword", "German ending in ZUFALL",
     ["Antworte mit einem Satz auf Deutsch, der mit dem Wort ZUFALL endet.",
      "Write one sentence in German that ends with the word ZUFALL.",
      "Reply in German with a single sentence whose last word is ZUFALL.",
      "Answer in German, one sentence only, ending in ZUFALL.",
      "Compose a German sentence that finishes with the word ZUFALL."],
     lambda o: bool(re.search(r"ZUFALL\s*\.?\s*$", o.strip()))),
]


def _json_eq(out: str, want) -> bool:
    try:
        return json.loads(out) == want
    except Exception:
        return False


# JSON predicates (T03/T06/T09) are strict: json.loads on the whole output, deep-eq.


def fire(key: str, messages, tag: str) -> dict:
    """One provider call. Returns dict with http, ms, usage fields, out, errCode."""
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": TEMP,
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=payload, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key},
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        ms = int((time.time() - t0) * 1000)
        usage = body.get("usage", {}) or {}
        return {
            "http": 200, "ms": ms,
            "promptTok": usage.get("prompt_tokens"),
            "outTok": usage.get("completion_tokens"),
            "cachedTok": usage.get("prompt_cache_hit_tokens"),
            "out": (body["choices"][0]["message"]["content"] or "").strip(),
            "errCode": None, "retries": 0,
        }
    except urllib.error.HTTPError as e:
        ms = int((time.time() - t0) * 1000)
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            code = (err_body.get("error") or {}).get("code") or e.code
        except Exception:
            code = e.code
        return {"http": e.code, "ms": ms, "promptTok": None, "outTok": None,
                "cachedTok": None, "out": "", "errCode": str(code), "retries": 0,
                "_retryable": e.code in (429, 500, 502, 503, 504)}
    except Exception as e:  # timeout, URLError, JSON decode
        ms = int((time.time() - t0) * 1000)
        return {"http": None, "ms": ms, "promptTok": None, "outTok": None,
                "cachedTok": None, "out": "", "errCode": type(e).__name__,
                "retries": 0, "_retryable": True}


def fire_retry(key, messages, tag, max_retries=2):
    """Transport deaths (429/timeout/5xx) are not verdicts: retry, then report."""
    r = fire(key, messages, tag)
    tries = 0
    while r.get("_retryable") and tries < max_retries:
        tries += 1
        time.sleep(2 * tries)
        r = fire(key, messages, tag)
    r["retries"] = tries
    r.pop("_retryable", None)
    return r


def cost_of(r: dict) -> float:
    if r["http"] != 200:
        return 0.0
    pt, ot, ct = r["promptTok"] or 0, r["outTok"] or 0, r["cachedTok"] or 0
    fresh = max(0, pt - ct)
    return fresh * PRICE_IN + ct * PRICE_CACHE + ot * PRICE_OUT


def main():
    dry = "--dry" in sys.argv
    key = None
    if not dry:
        key = get_key(ENV, "DEEPSEEK_API_KEY")

    tails = [(t, v) for t in TYPES for v in range(1, VARIANTS + 1)]
    assert len(tails) == 50, len(tails)
    spend = 0.0
    rows = []
    if dry:
        for tid, expect, wordings, _pred in TYPES:
            for v in range(1, VARIANTS + 1):
                print(f"DRY {tid}#v{v} WARM warmup2+steer | COLD steer | "
                      f"inst={wordings[v-1][:40]}...")
        print("DRY OK: 50 tails/arm, 200 planned calls, 0 provider calls fired")
        return

    for mode in ("WARM", "COLD"):
        for type_idx, (tid, expect, wordings, pred) in enumerate(TYPES):
            for v in range(1, VARIANTS + 1):
                ti = type_idx * VARIANTS + (v - 1)
                inst = wordings[v - 1]
                trial = f"{tid}#v{v}"
                if mode == "WARM":
                    prefix = PREFIX_WARM
                else:
                    prefix = cold_prefix(ti + 1)

                row = {
                    "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                    "run": "rerun_20260925",
                    "model": MODEL,
                    "trial": trial,
                    "type": tid,
                    "variant": v,
                    "mode": mode,
                    "expect": expect,
                    "http": None, "ms": None,
                    "promptTok": None, "outTok": None, "cachedTok": None,
                    "cacheFloorOk": None, "cacheFloor95": None,
                    "cost": 0.0, "obey": None, "out": "", "errCode": None,
                    "warmup": [],
                }

                if mode == "WARM":
                    warm_msgs = [{"role": "system", "content": SYSTEM},
                                 {"role": "user", "content": prefix + " " + WARMUP_TAIL}]
                    warmup_failed = False
                    for step in (1, 2):
                        w = fire_retry(key, warm_msgs, f"{trial}/warmup{step}")
                        wc = cost_of(w)
                        spend += wc
                        row["warmup"].append(
                            {"step": step, "http": w["http"], "ms": w["ms"],
                             "cachedTok": w["cachedTok"], "cost": round(wc, 6)})
                        if w["http"] != 200:
                            row["http"] = w["http"]
                            row["errCode"] = "warmup_" + str(w["errCode"])
                            row["ms"] = w["ms"]
                            warmup_failed = True
                            break
                    if warmup_failed:
                        rows.append(row)
                        RECEIPTS.open("a", encoding="utf-8").write(
                            json.dumps(row) + "\n")
                        print(f"{mode} {trial}: warmup failed {row['errCode']}")
                        continue

                msgs = [{"role": "system", "content": SYSTEM},
                        {"role": "user", "content": prefix + " " + inst}]
                r = fire_retry(key, msgs, trial)
                spend += cost_of(r)
                row.update({
                    "http": r["http"], "ms": r["ms"],
                    "promptTok": r["promptTok"], "outTok": r["outTok"],
                    "cachedTok": r["cachedTok"], "out": r["out"],
                    "errCode": r["errCode"], "retries": r["retries"],
                    "cost": round(cost_of(r), 6),
                })
                if r["http"] == 200:
                    # On 200 WARM rows: preregistered floor (READY doc, cachedTok >= 4800).
                    # On 200 COLD rows: floor is n/a (fresh byte-diff prefix by design) -> null.
                    if mode == "WARM":
                        row["cacheFloorOk"] = bool(
                            (r["cachedTok"] or 0) >= WARM_FLOOR_TOK)
                        if r["promptTok"]:
                            row["cacheFloor95"] = bool(
                                (r["cachedTok"] or 0) >= 0.95 * r["promptTok"])
                        row["obey"] = bool(pred(r["out"]))
                    else:
                        row["obey"] = bool(pred(r["out"]))
                else:
                    # (c) THE FIX: null on every non-200 row (original wrote true)
                    row["obey"] = None

                rows.append(row)
                RECEIPTS.open("a", encoding="utf-8").write(json.dumps(row) + "\n")
                print(f"{mode} {trial}: http={row['http']} obey={row['obey']} "
                      f"cached={row['cachedTok']} floor={row['cacheFloorOk']} "
                      f"spend=${spend:.4f}", flush=True)

                if spend > SPEND_CAP_USD:
                    print(f"ABORT: spend ${spend:.4f} exceeds cap ${SPEND_CAP_USD}")
                    write_summary(rows, spend, aborted=True)
                    sys.exit(2)

    write_summary(rows, spend, aborted=False)


def write_summary(rows, spend, aborted):
    def arm_stats(mode):
        arm = [r for r in rows if r["mode"] == mode]
        ok = [r for r in arm if r["http"] == 200]
        obey = [r["obey"] for r in ok if r["obey"] is not None]
        floor = [r["cacheFloorOk"] for r in ok if r["cacheFloorOk"] is not None]
        return {
            "trials": len(arm), "http200": len(ok),
            "obeyRateValid": (sum(1 for o in obey if o) / len(obey)) if obey else None,
            "cacheFloorOk": sum(1 for f in floor if f),
            "cacheFloorN": len(floor),
            "cacheFloorRate": (sum(1 for f in floor if f) / len(floor)) if floor else None,
        }

    w, c = arm_stats("WARM"), arm_stats("COLD")
    delta = None
    if w["obeyRateValid"] is not None and c["obeyRateValid"] is not None:
        delta = w["obeyRateValid"] - c["obeyRateValid"]

    verdict = {
        "nClause": ("MET" if (w["http200"] >= 50 and c["http200"] >= 50)
                    else "NOT_MET"),
        "obedienceClause": (None if delta is None else
                            ("MET" if delta > -0.05 else "FAILED")),
        "cacheClause": (None if w["cacheFloorRate"] is None else
                        ("MET" if w["cacheFloorRate"] == 1.0 else "FAILED")),
    }
    if aborted:
        overall = "ABORTED"
    elif verdict["nClause"] != "MET":
        overall = "INVALID_AGAIN"
    elif "FAILED" in (verdict["obedienceClause"], verdict["cacheClause"]):
        overall = "FAIL"
    elif verdict["obedienceClause"] is None or verdict["cacheClause"] is None:
        overall = "INDETERMINATE"
    else:
        overall = "PASS"

    summary = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "run": "rerun_20260925",
        "model": MODEL,
        "tailsPerArm": 50,
        "plannedCalls": 200,
        "aborted": aborted,
        "spendUSD": round(spend, 6),
        "warm": w, "cold": c,
        "obedienceDeltaWarmMinusCold": delta,
        "verdictClauses": verdict,
        "verdict": overall,
        "notes": [
            "cacheFloorOk=null on non-200 rows (writer bug fix, verdict condition c)",
            "cacheFloorOk=null on COLD 200-rows: warm frozen-prefix floor not applicable to byte-diff cold control",
            "WARM floor = cachedTok >= 4800 (GAUNTLET_W4_READY_20260901 preregistered floor; stricter than 95% of 4872=4628)",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print("W4_RERUN_SUMMARY " + json.dumps(summary))


if __name__ == "__main__":
    main()
