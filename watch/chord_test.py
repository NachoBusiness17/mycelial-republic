#!/usr/bin/env python3
"""CHORD TEST — does the salon fold beat a random member post?
Per the planning salon's own spec: random-member pairing (never "best post"),
forced-choice binary rubric (3 items), tie = loss for the fold, randomized A/B
presentation, null-variant canary (identical text both sides, expect ~50%),
cross-check on a second judge family. Blind: the judge never knows which side
is which. Spec: pass >= 75% pair-win rate (binomial p<0.05 at N=20).
Judge: anthropic haiku (its own family appears only as an S3 post engine);
cross-check: deepseek. Keys from .env, never echoed.
"""
import concurrent.futures, json, os, random, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALONS_DIR = os.path.join(ROOT, "memory", "runs", "salons")
OUT = os.path.join(ROOT, "memory", "runs", "chord_test")
FRESH = ["hyperspectral_salon_20260903c", "planning_chord_test_20260903",
         "planning_gate_v3_20260903", "planning_tab_train_20260903",
         "planning_rake_20260903"]
SEED = 20260903
PAIRS_PER_SALON = 4
CANARY_N = 4
CROSSCHECK_N = 4

ENV = {}
for _line in open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="ignore"):
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        ENV[_k.strip()] = _v.strip()


def judge_anthropic(text_a, text_b, question):
    prompt = ("You are a blind evaluator comparing two anonymous responses (A and B) "
              "to the same research question. Neither is privileged. Judge only what "
              "is written.\n\nQUESTION (context): " + question +
              "\n\nRESPONSE A:\n" + text_a[:6000] +
              "\n\nRESPONSE B:\n" + text_b[:6000] +
              "\n\nAnswer three forced-choice questions, choosing A or B for each:\n"
              "1. Which response gives a more concrete, actionable next step?\n"
              "2. Which response more explicitly states its own evidential limits "
              "(what is unproven or blocked)?\n"
              "3. Which response avoids unsupported claims about sources?\n\n"
              "Reply EXACTLY in this format and nothing else:\n1:<A|B> 2:<A|B> 3:<A|B>")
    body = {"model": "claude-haiku-4-5-20251001", "max_tokens": 40,
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"x-api-key": ENV.get("ANTHROPIC_API_KEY", ""),
                 "anthropic-version": "2023-06-01",
                 "anthropic-workspace-id": ENV.get("ANTHROPIC_WORKSPACE_ID", ""),
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        j = json.loads(resp.read().decode("utf-8"))
    txt = "\n".join(b.get("text", "") for b in j.get("content", [])
                    if b.get("type") == "text")
    m = re.findall(r"[123]:\s*([AB])", txt)
    return m if len(m) == 3 else None


def judge_deepseek(text_a, text_b, question):
    prompt = ("You are a blind evaluator comparing two anonymous responses (A and B) "
              "to the same research question. Neither is privileged. Judge only what "
              "is written.\n\nQUESTION (context): " + question +
              "\n\nRESPONSE A:\n" + text_a[:6000] +
              "\n\nRESPONSE B:\n" + text_b[:6000] +
              "\n\nAnswer three forced-choice questions, choosing A or B for each:\n"
              "1. Which response gives a more concrete, actionable next step?\n"
              "2. Which response more explicitly states its own evidential limits?\n"
              "3. Which response avoids unsupported claims about sources?\n\n"
              "Reply EXACTLY: 1:<A|B> 2:<A|B> 3:<A|B> and nothing else.")
    body = {"model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}], "max_tokens": 40}
    req = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Authorization": "Bearer " + ENV.get("DEEPSEEK_API_KEY", ""),
                 "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (MAG chord test)"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        j = json.loads(resp.read().decode("utf-8"))
    txt = ((j.get("choices") or [{}])[0].get("message") or {}).get("content", "")
    m = re.findall(r"[123]:\s*([AB])", txt)
    return m if len(m) == 3 else None


def load_salons():
    out = []
    for name in FRESH:
        sdir = os.path.join(SALONS_DIR, name)
        apath = os.path.join(sdir, "SALON_ARTIFACT.md")
        if not os.path.exists(apath):
            print("skip (no artifact):", name)
            continue
        src = open(apath, encoding="utf-8").read()
        if "## VERDICT (judge fold)" not in src:
            print("skip (no verdict):", name)
            continue
        verdict = src.split("## VERDICT (judge fold)")[1].split("## BLIND POSTS")[0].strip()
        qline = ""
        for line in src.splitlines():
            if line.startswith("question: "):
                qline = line[len("question: "):]
                break
        posts = {}
        for fn in os.listdir(sdir):
            if fn.startswith("post_S") and fn.endswith(".md"):
                posts[fn[5:-3]] = open(os.path.join(sdir, fn), encoding="utf-8").read()
        if verdict and posts:
            out.append({"name": name, "question": qline, "verdict": verdict, "posts": posts})
    return out


def main():
    salons = load_salons()
    rng = random.Random(SEED)
    pairs = []
    for s in salons:
        picks = rng.sample(sorted(s["posts"].keys()), min(PAIRS_PER_SALON, len(s["posts"])))
        for shape in picks:
            fold_first = rng.random() < 0.5
            pairs.append({"salon": s["name"], "shape": shape, "question": s["question"],
                          "fold": s["verdict"], "post": s["posts"][shape],
                          "fold_first": fold_first, "kind": "pair"})
    for i in range(CANARY_N):  # null variant: identical text both sides
        s = salons[i % len(salons)]
        pairs.append({"salon": s["name"], "shape": "canary", "question": s["question"],
                      "fold": s["verdict"], "post": s["verdict"],
                      "fold_first": rng.random() < 0.5, "kind": "canary"})
    print("pairs:", sum(1 for p in pairs if p["kind"] == "pair"),
          "canary:", sum(1 for p in pairs if p["kind"] == "canary"), flush=True)

    os.makedirs(OUT, exist_ok=True)
    log = open(os.path.join(OUT, "pairs.jsonl"), "w", encoding="utf-8")

    def run_pair(p, judge_fn, judge_name):
        a, b = (p["fold"], p["post"]) if p["fold_first"] else (p["post"], p["fold"])
        try:
            marks = judge_fn(a, b, p["question"])
        except Exception as exc:
            return dict(p, judge=judge_name, error=type(exc).__name__ + ": " + str(exc)[:120])
        if not marks:
            return dict(p, judge=judge_name, error="unparseable")
        wins = sum(1 for m in marks if (m == "A") == p["fold_first"])
        return dict(p, judge=judge_name, marks=marks, fold_item_wins=wins,
                    fold_pair_win=1 if wins >= 2 else 0)

    real = [p for p in pairs if p["kind"] == "pair"]
    canary = [p for p in pairs if p["kind"] == "canary"]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(run_pair, p, judge_anthropic, "haiku"): p for p in pairs}
        for fut in concurrent.futures.as_completed(futs):
            r = fut.result()
            results.append(r)
            log.write(json.dumps(r, default=str) + "\n")
            log.flush()
            tag = r.get("error") or ("win" if r.get("fold_pair_win") else "loss")
            print("[" + r["kind"] + "] " + r["salon"][:28] + "/" + r["shape"]
                  + " -> " + str(tag), flush=True)

    cross = [run_pair(p, judge_deepseek, "deepseek") for p in
             [dict(p, fold_first=not p["fold_first"]) for p in
              sorted(real, key=lambda x: x["salon"] + x["shape"])[:CROSSCHECK_N]]]
    for r in cross:
        log.write(json.dumps(r, default=str) + "\n")
    log.close()

    r_real = [r for r in results if r["kind"] == "pair" and "error" not in r]
    r_can = [r for r in results if r["kind"] == "canary" and "error" not in r]
    wins = sum(r["fold_pair_win"] for r in r_real)
    n = len(r_real)
    cw = sum(r["fold_pair_win"] for r in r_can)
    xw = sum(r.get("fold_pair_win", 0) for r in cross if "error" not in r)
    report = ["=== CHORD TEST RESULT ===",
              "pairs judged: %d/%d  fold wins: %d (%.0f%%)" % (n, len(real), wins, 100.0 * wins / max(n, 1)),
              "PASS BAR: >=15/20 (75%%)   KILL BAR: <=13",
              "canary (null variant, expect ~50%%): %d/%d fold-wins %s"
              % (cw, len(r_can), "(SANITY OK)" if 1 <= cw <= 3 else "(SANITY FAIL - judge bias!)"),
              "cross-check deepseek on %d pairs: %d fold-wins" % (len(cross), xw),
              "VERDICT: " + ("PASS - fold beats member posts" if wins >= 15 else
                             ("KILL - fold does not beat member posts" if wins <= 13 else
                              "INCONCLUSIVE - between bars, gather more salons"))]
    out = "\n".join(report)
    print(out)
    open(os.path.join(OUT, "RESULT.md"), "w", encoding="utf-8").write(out + "\n")


if __name__ == "__main__":
    main()
