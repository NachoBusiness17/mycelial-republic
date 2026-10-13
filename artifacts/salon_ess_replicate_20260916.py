#!/usr/bin/env python3
"""salon_ess_replicate_20260916.py — pre-registered Salon ESS replicate (falsifier §4.1 follow-up).

Run with the repo venv python (never bare python):
  ./.venv/Scripts/python.exe artifacts/salon_ess_replicate_20260916.py gen [START END]
  ./.venv/Scripts/python.exe artifacts/salon_ess_replicate_20260916.py shuffle
  ./.venv/Scripts/python.exe artifacts/salon_ess_replicate_20260916.py analyze G01,G02,...,G36

Stages:
  gen      36 Ollama calls (gemma:2b), temperatures [0.3, 0.8, 1.3] x 12 runs each,
           per-call temperature. Resumable: completed call indices are skipped.
           Appends one log line per landed replicate to the receipt.
  shuffle  writes the blind presentation file (T01..T36) with fixed seed 20260916.
  analyze  grades arrive on argv in T01..T36 order (they must already be committed
           to the receipt); joins them with the deterministic shuffle mapping,
           computes Jaccard decorrelation, per-temperature table, ESS proxy,
           Spearman rho + permutation p, mechanical verdict; writes the
           T-id -> (temp, run, grade) mapping file LAST, per pre-registration.

Stdlib only. Network: http://localhost:11434 only. Cost: $0.
"""
import json
import random
import re
import sys
import time
import urllib.request
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ART = REPO / "artifacts"
RECEIPT = REPO / "watch" / "inbox" / "physical_computing" / "receipts" / "SALON_ESS_REPLICATE_20260916.md"
GEN_JSON = ART / "salon_ess_gen_20260916.json"
PRESENT = ART / "salon_ess_shuffled_20260916.txt"
MAPPING = ART / "salon_ess_mapping_20260916.json"

MODEL = "gemma:2b"
TEMPS = [0.3, 0.8, 1.3]
N_PER_TEMP = 12
TOTAL = len(TEMPS) * N_PER_TEMP
NUM_PREDICT = 300
SHUFFLE_SEED = 20260916
PERM_SEED = 20260916
N_PERM = 100_000
QUESTION = ("A town must cut its budget by 10%. Argue for the single change that best "
            "balances harm and fairness. Answer in 150 words or fewer.")
URL = "http://localhost:11434/api/generate"


def log(msg: str) -> None:
    line = f"- {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    with open(RECEIPT, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def shuffle_order():
    order = list(range(TOTAL))
    random.Random(SHUFFLE_SEED).shuffle(order)
    return order


def tid(k: int) -> str:
    return f"T{k + 1:02d}"


def word_set(text: str):
    return frozenset(re.findall(r"[a-z']+", text.lower()))


def jaccard(a, b) -> float:
    if not a and not b:
        return 1.0
    union = len(a | b)
    return len(a & b) / union if union else 1.0


def cmd_gen(start: int, end: int) -> None:
    data = {"question": QUESTION, "model": MODEL, "num_predict": NUM_PREDICT, "calls": []}
    if GEN_JSON.exists():
        data = json.loads(GEN_JSON.read_text(encoding="utf-8"))
    have = {c["i"] for c in data["calls"]}
    win_t0 = time.time()
    for i in range(start, end):
        if i in have:
            print(f"skip {i} (already done)", flush=True)
            continue
        temp = TEMPS[i // N_PER_TEMP]
        run = i % N_PER_TEMP + 1
        payload = {"model": MODEL, "prompt": QUESTION, "stream": False,
                   "options": {"temperature": temp, "num_predict": NUM_PREDICT}}
        req = urllib.request.Request(
            URL, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        err, text = None, ""
        for attempt in (1, 2):
            t1 = time.time()
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    body = json.loads(r.read().decode("utf-8"))
                text = (body.get("response") or "").strip()
                err = None
                break
            except Exception as e:  # noqa: BLE001 - local lab script
                err = e
                log(f"gen[{i:02d}] attempt {attempt} failed: {e!r}; retrying")
                time.sleep(2)
        if err is not None:
            log(f"gen[{i:02d}] FAILED after retry — aborting stage: {err!r}")
            raise SystemExit(2)
        elapsed = round(time.time() - t1, 1)
        rec = {"i": i, "temp": temp, "run": run, "elapsed_s": elapsed,
               "words": len(text.split()), "text": text}
        data["calls"].append(rec)
        ART.mkdir(parents=True, exist_ok=True)
        GEN_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        log(f"gen[{i:02d}] temp={temp} run={run:02d} words={rec['words']} elapsed={elapsed}s")
    log(f"gen window [{start}:{end}] done; total calls on disk={len(data['calls'])}/{TOTAL}; "
        f"window wall={round(time.time() - win_t0, 1)}s")


def cmd_shuffle() -> None:
    data = json.loads(GEN_JSON.read_text(encoding="utf-8"))
    calls = sorted(data["calls"], key=lambda c: c["i"])
    assert len(calls) == TOTAL, f"expected {TOTAL} calls, have {len(calls)}"
    assert all(c["text"].strip() for c in calls), "empty text found"
    order = shuffle_order()
    blocks = []
    for k, gi in enumerate(order):
        t = calls[gi]["text"].strip()
        blocks.append(f"=== {tid(k)} === (words: {len(t.split())})\n{t}\n")
    header = ("BLIND PRESENTATION — salon ESS replicate 2026-09-16\n"
              f"shuffle seed: {SHUFFLE_SEED} | 36 texts, grade each 0-10\n"
              "rubric: one change 0-3, harm 0-2, fairness 0-2, concrete 0-2, "
              "length 1 if <=170 words else 0\n\n")
    PRESENT.write_text(header + "\n".join(blocks), encoding="utf-8")
    log(f"shuffle done: seed={SHUFFLE_SEED}; blind presentation -> {PRESENT.name} "
        "(grader sees T-ids only; generation JSON stays closed until grades are committed)")


def ranks(v):
    idx = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[idx[j + 1]] == v[idx[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[idx[k]] = avg
        i = j + 1
    return r


def cmd_analyze(grades_arg: str) -> None:
    grades_t = [float(x) for x in grades_arg.split(",")]
    assert len(grades_t) == TOTAL, f"need {TOTAL} grades, got {len(grades_t)}"
    data = json.loads(GEN_JSON.read_text(encoding="utf-8"))
    calls = sorted(data["calls"], key=lambda c: c["i"])
    assert len(calls) == TOTAL
    order = shuffle_order()  # presentation position k -> generation index
    grade_gi = [0.0] * TOTAL
    for k, gi in enumerate(order):
        grade_gi[gi] = grades_t[k]

    sets = [word_set(c["text"]) for c in calls]

    # per-text decorrelation vs all other 35 (pooled)
    dec = []
    for i in range(TOTAL):
        vals = [1.0 - jaccard(sets[i], sets[j]) for j in range(TOTAL) if j != i]
        dec.append(sum(vals) / len(vals))

    # per-temperature table (within-temp pairs only)
    rows = []
    for ti, temp in enumerate(TEMPS):
        idxs = list(range(ti * N_PER_TEMP, (ti + 1) * N_PER_TEMP))
        pairs = list(combinations(idxs, 2))
        mdec = sum(1.0 - jaccard(sets[a], sets[b]) for a, b in pairs) / len(pairs)
        msim = 1.0 - mdec
        mgrade = sum(grade_gi[i] for i in idxs) / len(idxs)
        ess = 1.0 / (1.0 + msim)
        rows.append((temp, mdec, mgrade, ess))

    # Spearman rho across all 36
    rd, rg = ranks(dec), ranks(grade_gi)
    n = TOTAL
    md, mg = sum(rd) / n, sum(rg) / n
    dc = [x - md for x in rd]
    gc = [x - mg for x in rg]
    dot_obs = sum(a * b for a, b in zip(dc, gc))
    va = sum(a * a for a in dc)
    vb = sum(b * b for b in gc)
    rho = dot_obs / (va * vb) ** 0.5 if va > 0 and vb > 0 else float("nan")

    # exact-threshold permutation test: two-sided, seed fixed, (b+1)/(N+1)
    rng = random.Random(PERM_SEED)
    count = 0
    perm = list(range(n))
    for _ in range(N_PERM):
        rng.shuffle(perm)
        d = sum(dc[i] * gc[perm[i]] for i in range(n))
        if abs(d) >= abs(dot_obs) - 1e-9:
            count += 1
    p = (count + 1) / (N_PERM + 1)

    if rho < -0.3:
        verdict = "SUPPORTED"
    elif rho > 0.3:
        verdict = "REFUTED"
    else:
        verdict = "NULL/INSUFFICIENT"

    total_wall = round(sum(c["elapsed_s"] for c in calls), 1)
    log("ANALYSIS (pre-registered stats; grades as committed above):")
    for temp, mdec, mgrade, ess in rows:
        log(f"  temp={temp}: n=12  mean_pairwise_decorrelation={mdec:.4f}  "
            f"mean_grade={mgrade:.2f}  ESS_proxy={ess:.4f}")
    log(f"  Spearman(decorrelation, grade) n=36: rho={rho:.4f}  "
        f"perm_p(two-sided, {N_PERM} draws, seed {PERM_SEED})={p:.6f}")
    log(f"  MECHANICAL VERDICT (thresholds: SUPPORTED rho<-0.3 / REFUTED rho>+0.3): {verdict}")
    log(f"  gen compute time (sum of call wall times): {total_wall}s")

    # mapping file written LAST, only after grades were committed to the receipt
    mapping = [{"tid": tid(k), "gen_index": gi, "temp": calls[gi]["temp"],
                "run": calls[gi]["run"], "grade": grades_t[k],
                "words": calls[gi]["words"], "decorr": round(dec[gi], 4)}
               for k, gi in enumerate(order)]
    MAPPING.write_text(json.dumps({"shuffle_seed": SHUFFLE_SEED, "perm_seed": PERM_SEED,
                                   "model": MODEL, "rho": rho, "p": p,
                                   "verdict": verdict, "mapping": mapping},
                                  indent=1), encoding="utf-8")
    log(f"mapping file written post-grade (as pre-registered) -> {MAPPING.name}")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    stage = sys.argv[1]
    if stage == "gen":
        s = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        e = int(sys.argv[3]) if len(sys.argv) > 3 else TOTAL
        cmd_gen(s, e)
    elif stage == "shuffle":
        cmd_shuffle()
    elif stage == "analyze":
        cmd_analyze(sys.argv[2])
    else:
        raise SystemExit(f"unknown stage: {stage}")


if __name__ == "__main__":
    main()
