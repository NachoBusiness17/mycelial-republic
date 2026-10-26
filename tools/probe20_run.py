"""probe20_run -- series runner for the steering drift pairs (2026-09-26).

Lands the pass-c receipt (watch/inbox/BURN_steering-theory_20260925_c.md):
drift.py holds no registry; a pair is a caller-side series + drift_check
call. This runner is that caller. stdlib only.

Per invocation (real mode): append one cycle row to
memory/runs/probe20/<lane>_<pair>_series.jsonl, then once >= min_points rows
exist call drift_check (tools/drift.py) on the tails and print the verdict.

Noise floor (pass-c finding, one-flip VACUOUS escape): drift.py's VACUOUS
gate is any(delta != 0), so a single 0.05 task flip on the quantized
referent escapes the kill. The runner overrides any non-VACUOUS verdict to
INSUFFICIENT when max |delta referent| across the window < 0.1; a truly
flat referent still kills as VACUOUS (the native kill, not an escape).

Pair A (pass-b fields): metric = mean verdict-token logprob margin over the
probe at cycle t; referent = correct/20. The margin/correct values are
supplied by the caller's probe execution (e.g. OLLAMA_LOGPROBS_PROBE lane
read); this runner is the series + verdict organ, not the model client.

--demo: three synthetic scenarios, in memory only, no files written.
--seed: write watch/inbox/PROBE20_steering_v1.jsonl (20 labeled tasks + pair
registry rows + hash over the task lines), verified on every load or refuse.

--live: the built client (BURN_steering-theory_20260926_b.md item (b)-(d),
landed 2026-09-26). Runs the 20 loaded probe tasks against a local
llama-server /completion endpoint (default http://127.0.0.1:8081/completion,
overridable via env LLAMA_SERVER_URL or --llama-url), each POST carrying
n_probs and a GBNF grammar forcing exactly TRUE or FALSE. Per-task margin =
logprob(TRUE) - logprob(FALSE); cycle margin = mean of the 20 margins;
correct = argmax token equals the labeled answer. Connection failure prints
LIVE-UNREACHABLE and exits 3 without writing a series row. A reachable
server that rejects the request or returns no usable probability block is
instrument-missing: LIVE-BAD-RESPONSE, exit 4, no fallback margin, no
synthetic rows (pre-registered falsifier, BURN _b). Pair A only; the
computed values flow through the unchanged append + evaluate path.
"""

import argparse
import hashlib
import json
import os
import socket
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBE_PATH = os.path.join(REPO, "watch", "inbox", "PROBE20_steering_v1.jsonl")
SERIES_DIR = os.path.join(REPO, "memory", "runs", "probe20")
PROBE_N = 20
NOISE_FLOOR = 0.1
MIN_POINTS = 5

# --live client constants (BURN_steering-theory_20260926_b.md (b)-(c)).
# Port 8081 dedicated compute port (Port 8080 reserved for GSTD Node Dashboard).
DEFAULT_LLAMA_URL = "http://127.0.0.1:8081/completion"
ENV_LLAMA_URL = "LLAMA_SERVER_URL"
LIVE_TIMEOUT = 300  # seconds; first request may load the model
N_PROBS = 20  # confirmed against the served binary 2026-09-27 (gemma:2b blob, llama-server Vulkan build): request param `n_probs` unchanged, but the response fields WERE renamed across llama.cpp versions -- completion_probabilities[0].top_logprobs[].token (was probs[].tok_str); client reads the served shape, no fallback branch (no-fallback-creep law, BURN_reset_20260927 probe20_live)
VERDICT_GRAMMAR = 'root ::= "TRUE" | "FALSE"'
LIVE_PROMPT = "Statement: %s\nAnswer TRUE or FALSE with one word.\nAnswer:"

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import drift as _drift
    HAVE_DRIFT = True
except ImportError:  # pragma: no cover
    HAVE_DRIFT = False
    # inline fallback, source: tools/drift.py::drift_check (repo, read 2026-09-26)
    def _drift_check(metric, referent, window=0, label=""):
        def deltas(s):
            return [s[i + 1] - s[i] for i in range(len(s) - 1)]

        def pearson(xs, ys):
            n = len(xs)
            if n < 2 or n != len(ys):
                return None
            mx, my = sum(xs) / n, sum(ys) / n
            cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            vx = sum((x - mx) ** 2 for x in xs)
            vy = sum((y - my) ** 2 for y in ys)
            if vx == 0 or vy == 0:
                return None
            return cov / ((vx ** 0.5) * (vy ** 0.5))

        metric = [float(x) for x in metric]
        referent = [float(x) for x in referent]
        dm, dr = deltas(metric), deltas(referent)
        if window and window >= 1:
            dm, dr = dm[-int(window):], dr[-int(window):]
        if len(dm) < 3:
            return {"ok": True, "verdict": "INSUFFICIENT", "deltas": len(dm)}
        corr = pearson(dm, dr)
        if not any(d != 0 for d in dr):
            return {"ok": True, "verdict": "VACUOUS", "corr_dm_dr": None,
                    "note": "referent never moved during the window"}
        if corr is None:
            return {"ok": True, "verdict": "DEGENERATE", "corr_dm_dr": None}
        if corr >= 0.5:
            verdict = "ALIGNED"
        elif corr <= -0.5:
            verdict = "INVERTED"
        else:
            verdict = "DRIFTING"
        return {"ok": True, "verdict": verdict,
                "corr_dm_dr": round(corr, 4) if corr is not None else None}


def drift_check(metric, referent, window=0, label=""):
    if HAVE_DRIFT:
        return _drift.drift_check(metric, referent, window=window, label=label)
    return _drift_check(metric, referent, window=window, label=label)


# tasks live in tools/probe20_tasks.py since 2026-09-27 (ratchet split, pure
# data move); sibling import in script mode, package import otherwise
try:
    from probe20_tasks import TASKS  # type: ignore
except ImportError:  # pragma: no cover
    from tools.probe20_tasks import TASKS  # type: ignore



def version_hash():
    canon = "\n".join(json.dumps(t, sort_keys=True) for t in TASKS)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


PAIRS = {
    "A": {"label": "lane=gemma4:A-conf-margin-vs-correctness",
          "row_schema": ["cycle", "margin", "correct"],
          "expect_corr": [0.3, 0.8]},
    "B": {"label": "lane=gemma4:B-escalate-rate-vs-overturn-rate",
          "row_schema": ["cycle", "escalated", "total", "overturns"],
          "derived": {"metric": "escalated/total", "referent": "overturns/escalated"},
          "den_min": {"metric": 20, "referent": 5},
          "expect_corr": [0.0, 0.6]},
}


def seed_lines():
    meta = {"type": "meta", "version": "v1", "created": "2026-09-26",
            "probe_n": PROBE_N, "min_points": MIN_POINTS,
            "noise_floor": NOISE_FLOOR, "version_hash": version_hash(),
            "pairs": [dict(pair=k, **v) for k, v in sorted(PAIRS.items())],
            "source": "BURN_steering-theory_20260925_b.md fields + _c registry draft"}
    lines = [json.dumps(meta, sort_keys=True)]
    lines += [json.dumps(dict(type="task", **t), sort_keys=True) for t in TASKS]
    return lines


def write_seed(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(seed_lines()) + "\n")
    return path


def load_probe(path):
    if not os.path.exists(path):
        print("MISSING PROBE: %s" % path)
        print("missing-file path: run `python tools/probe20_run.py --seed` to "
              "write the v1 seed (20 tasks + pair registry + version hash), "
              "or supply --probe pointing at an existing battery.")
        sys.exit(2)
    meta, tasks = None, []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("type") == "meta":
                meta = row
            elif row.get("type") == "task":
                tasks.append(row)
    if meta is None or not tasks:
        print("BAD PROBE: %s has no meta or no tasks" % path)
        sys.exit(2)
    recomputed = version_hash()
    if meta.get("version_hash") != recomputed:
        print("PROBE VERSION MISMATCH: recorded %s, recomputed %s. "
              "Never mix probe versions in one series." % (meta.get("version_hash"), recomputed))
        sys.exit(2)
    return meta, tasks


def series_path(lane, pair):
    return os.path.join(SERIES_DIR, "%s_%s_series.jsonl" % (lane, pair))


def derive(pair, row):
    if pair == "A":
        return float(row["margin"]), row["correct"] / float(PROBE_N)
    total = float(row["total"])
    esc = float(row["escalated"])
    return esc / total, (float(row["overturns"]) / esc) if esc else 0.0


def evaluate(pair, rows, window):
    metric = [derive(pair, r)[0] for r in rows]
    referent = [derive(pair, r)[1] for r in rows]
    raw = drift_check(metric, referent, window=window, label=PAIRS[pair]["label"])
    ref_win = referent[-int(window):] if window and window >= 1 else referent
    # net referent movement across the window, with an epsilon guard: binary
    # float subtraction makes 0.6 - 0.5 read as 0.09999999999999998, which
    # would floor a genuine 0.1 delta (defect caught in demo1, 2026-09-26).
    net_dr = abs(ref_win[-1] - ref_win[0]) if len(ref_win) >= 2 else 0.0
    enforced = dict(raw)
    if raw.get("verdict") == "VACUOUS":
        enforced["note"] = raw.get("note", "") + " [runner: flat referent, native kill stands]"
    elif net_dr + 1e-9 < NOISE_FLOOR:
        enforced["verdict"] = "INSUFFICIENT"
        enforced["corr_dm_dr"] = None
        enforced["runner_override"] = ("noise floor: net |delta referent| %.3f < %.2f across window; "
                                       "one-flip VACUOUS escape blocked (BURN _c)" % (net_dr, NOISE_FLOOR))
    return {"raw": raw, "enforced": enforced, "n_rows": len(rows), "net_referent_delta": round(net_dr, 4)}


def run_demo():
    scenarios = [
        ("demo1-aligned", [1.0, 1.5, 1.8, 2.3, 2.6, 2.9], [10, 12, 13, 15, 16, 17]),
        ("demo2-one-flip-escape", [1.0, 1.4, 1.1, 1.6, 1.3], [14, 14, 15, 15, 15]),
        ("demo3-true-vacuous", [1.0, 1.4, 1.1, 1.6, 1.3], [14, 14, 14, 14, 14]),
    ]
    print("probe20_run --demo (pair A schema, in memory only, no files written, "
          "drift import from tools/drift.py: %s)" % HAVE_DRIFT)
    for name, margins, correct in scenarios:
        rows = [{"cycle": i, "margin": m, "correct": c}
                for i, (m, c) in enumerate(zip(margins, correct))]
        out = evaluate("A", rows, window=0)
        out["scenario"] = name
        print(json.dumps(out, sort_keys=True))


def resolve_llama_url(flag_url):
    url = flag_url or os.environ.get(ENV_LLAMA_URL) or DEFAULT_LLAMA_URL
    url = url.rstrip("/")
    return url if url.endswith("/completion") else url + "/completion"


def live_probe_task(url, task):
    """One POST per task; returns (margin, argmax_matches).

    margin = logprob(TRUE) - logprob(FALSE) under the TRUE|FALSE grammar.
    Exits 3 on connection failure (LIVE-UNREACHABLE) and 4 on a reachable
    server that rejects the request or returns no usable probability block
    (LIVE-BAD-RESPONSE); neither writes a series row (rows are written only
    after this returns, BURN _b falsifier: instrument-missing aborts, no
    fallback margin).
    """
    payload = {"prompt": LIVE_PROMPT % task["text"], "n_predict": 1,
               "n_probs": N_PROBS, "grammar": VERDICT_GRAMMAR}
    req = urllib.request.Request(
        url, method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=LIVE_TIMEOUT) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("LIVE-BAD-RESPONSE: %s rejected the probe request -> HTTP %d: %s"
              % (url, e.code, e.reason))
        sys.exit(4)
    except urllib.error.URLError as e:
        print("LIVE-UNREACHABLE: %s (%s)" % (url, e.reason))
        sys.exit(3)
    except (socket.timeout, TimeoutError, OSError) as e:
        print("LIVE-UNREACHABLE: %s (%s)" % (url, e))
        sys.exit(3)

    positions = resp.get("completion_probabilities") or []
    cands = positions[0].get("top_logprobs") if positions else None
    if not cands:
        print("LIVE-BAD-RESPONSE: response carries no completion_probabilities[0].top_logprobs "
              "block; served-binary shape confirmed 2026-09-27, unexpected response (BURN _b)")
        sys.exit(4)

    def norm(tok):
        return (tok or "").strip().upper()

    argmax = norm(cands[0].get("token"))
    logprobs = {}
    for cand in cands:
        tok = norm(cand.get("token"))
        if tok in ("TRUE", "FALSE") and tok not in logprobs and "logprob" in cand:
            logprobs[tok] = float(cand["logprob"])
    if "TRUE" not in logprobs or "FALSE" not in logprobs:
        print("LIVE-BAD-RESPONSE: no TRUE and FALSE entries in the probability block; "
              "grammar or tokenization mismatch, no fallback margin (BURN _b)")
        sys.exit(4)
    return logprobs["TRUE"] - logprobs["FALSE"], 1 if argmax == task["answer"] else 0


def run_live(url_flag, tasks):
    url = resolve_llama_url(url_flag)
    print("LIVE: %d tasks -> %s (n_probs=%d, grammar %s)"
          % (len(tasks), url, N_PROBS, VERDICT_GRAMMAR))
    margins, correct = [], 0
    for task in tasks:
        margin, hit = live_probe_task(url, task)
        margins.append(margin)
        correct += hit
        print("  %s: margin %+.4f argmax-match=%d (answer %s)"
              % (task["id"], margin, hit, task["answer"]))
    mean_margin = sum(margins) / float(len(margins))
    print("LIVE CYCLE: mean margin %.4f correct %d/%d" % (mean_margin, correct, len(tasks)))
    return mean_margin, correct


def main():
    ap = argparse.ArgumentParser(description="probe20 steering pair series runner")
    ap.add_argument("--demo", action="store_true", help="synthetic series, dry mode, writes nothing")
    ap.add_argument("--live", action="store_true",
                    help="run the loaded probe against a local llama-server /completion "
                         "(env LLAMA_SERVER_URL or --llama-url) and compute pair A "
                         "margin/correct from the logprobs")
    ap.add_argument("--llama-url", default=None,
                    help="llama-server base or /completion URL; overrides env %s (default %s)"
                         % (ENV_LLAMA_URL, DEFAULT_LLAMA_URL))
    ap.add_argument("--seed", action="store_true", help="write the v1 seed probe file if absent")
    ap.add_argument("--probe", default=PROBE_PATH)
    ap.add_argument("--pair", choices=sorted(PAIRS), default="A")
    ap.add_argument("--lane", default="gemma4")
    ap.add_argument("--cycle", type=int, default=None)
    ap.add_argument("--window", type=int, default=0)
    ap.add_argument("--margin", type=float, default=None, help="pair A metric value")
    ap.add_argument("--correct", type=int, default=None, help="pair A referent count /20")
    ap.add_argument("--escalated", type=int, default=None, help="pair B")
    ap.add_argument("--total", type=int, default=None, help="pair B denominator")
    ap.add_argument("--overturns", type=int, default=None, help="pair B")
    args = ap.parse_args()

    if args.demo:
        run_demo()
        return
    if args.seed:
        if os.path.exists(args.probe):
            print("SEED REFUSED: %s already exists; probe versions are append-only, never overwrite" % args.probe)
            sys.exit(2)
        write_seed(args.probe)
        print("seeded %s (version_hash %s)" % (args.probe, version_hash()))
        return
    meta, tasks = load_probe(args.probe)
    path = series_path(args.lane, args.pair)
    os.makedirs(SERIES_DIR, exist_ok=True)
    rows = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if l.strip()]
    last_cycle = rows[-1]["cycle"] if rows else -1
    cycle = args.cycle if args.cycle is not None else last_cycle + 1
    if cycle <= last_cycle:
        print("REJECT: cycle %d <= last cycle %d; series is append-only, oldest first" % (cycle, last_cycle))
        sys.exit(2)

    if args.live:
        if args.pair != "A":
            print("--live computes pair A fields only (margin, correct); use --pair A")
            sys.exit(2)
        if args.margin is not None or args.correct is not None:
            print("--live computes --margin and --correct from the server; do not pass them by hand")
            sys.exit(2)

    if args.pair == "A":
        if args.live:
            args.margin, args.correct = run_live(args.llama_url, tasks)
        if args.margin is None or args.correct is None:
            print("pair A needs --margin and --correct (values from the caller's probe execution)")
            sys.exit(2)
        row = {"cycle": cycle, "ts": __import__("datetime").datetime.utcnow().isoformat() + "Z",
               "lane": args.lane, "probe_version_hash": meta["version_hash"],
               "margin": args.margin, "correct": args.correct}
    else:
        if None in (args.escalated, args.total, args.overturns):
            print("pair B needs --escalated, --total, --overturns")
            sys.exit(2)
        den = PAIRS["B"]["den_min"]
        if args.total < den["metric"] or args.escalated < den["referent"]:
            print("POINT NOT FILED: denominator law (total >= %d, escalated >= %d); "
                  "got total=%d escalated=%d (BURN _b)" % (den["metric"], den["referent"], args.total, args.escalated))
            sys.exit(1)
        row = {"cycle": cycle, "ts": __import__("datetime").datetime.utcnow().isoformat() + "Z",
               "lane": args.lane, "probe_version_hash": meta["version_hash"],
               "escalated": args.escalated, "total": args.total, "overturns": args.overturns}

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
    rows.append(row)
    print("appended cycle %d to %s (%d rows)" % (cycle, os.path.relpath(path, REPO), len(rows)))
    if len(rows) >= MIN_POINTS:
        out = evaluate(args.pair, rows, window=args.window)
        print(json.dumps(out, sort_keys=True))
    else:
        print("INSUFFICIENT (runner): %d/%d rows; no verdict until >= %d" % (len(rows), MIN_POINTS, MIN_POINTS))


if __name__ == "__main__":
    main()
