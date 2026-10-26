#!/usr/bin/env python3
"""consensus_harness - GB perimeter assertion A2 (2026-10-10).

"Nodes must confirm the ability of different models to generate a consensus
answer." This harness dispatches a closed-form task bank to K heterogeneous
models via an OpenAI-compatible Ollama host, computes modal-answer consensus,
runs the dead-salmon control (per-model cyclic answer shift breaks task
alignment; consensus must fall), and banks per-model ledger rows in a
GPS-importable shape so the network's learning is the accumulating ledger.
A1 (payout assertion) is stubbed: payout_delta stays null until the staging
endpoint exists, and the summary says so plainly.

Coldest vertex law: stdlib only, no docker, CPU-class. The Windows 10 laptop
runs this file unchanged against a remote OLLAMA_HOST on the LAN or tailnet.

Network law (SSRF guard, Mimosa 2026-10-10): a closed-perimeter tool must not
be able to reach the public internet or cloud metadata. The host allowlist is
loopback + RFC1918 LAN + Tailscale CGNAT only; redirects are refused.

Usage:
  python tools/consensus_harness.py --models gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct
  python tools/consensus_harness.py --host http://192.168.1.20:11434 --classify 6
Exit 0 = run banked (rates are data, not pass/fail); 2 = cannot run.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import ipaddress
import json
import re
import socket
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ESTATE = Path(__file__).resolve().parent.parent
LINKS = ESTATE / "memory" / "corpus" / "LINKS.jsonl"
OUT_ROOT = ESTATE / "watch" / "inbox" / "gstd_perimeter_build_20261010" / "runs"

VOCAB = [
    "memory", "routing", "security", "game", "economics", "rendering",
    "verification", "workflow", "network", "storage", "audio", "law",
    "census", "ractor", "verkle", "test", "burn", "lane", "rib", "gate",
    "agent", "model", "disk", "token", "mesh", "receipt",
]


def strip_reasoning(s: str) -> str:
    """Reasoning models emit <think>...</think>; the answer is what remains."""
    return re.sub(r"<think>.*?</think>", "", s or "", flags=re.S).strip()


def norm(s: str) -> str:
    s = strip_reasoning(s).strip().lower()
    s = re.sub(r"[^a-z0-9.:/_-]+", " ", s)
    return re.sub(r"\s+", " ", s).strip(" .")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None


def check_host(host: str) -> str:
    """Closed-perimeter allowlist: scheme http(s), no userinfo, and every
    resolved address must be loopback, RFC1918, or Tailscale CGNAT 100.64/10.
    Public internet, link-local (cloud metadata), and anything else refuse."""
    m = re.match(r"^(https?)://([^/@:]+|\[[^]]+\])(?::(\d+))?/?$", host)
    if not m:
        raise ValueError("host must be http(s)://host[:port], no path or userinfo")
    scheme, hostname = m.group(1), m.group(2).strip("[]")
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as e:
        raise ValueError("cannot resolve host: " + hostname) from e
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        ok = (ip.is_loopback
              or ip in ipaddress.ip_network("10.0.0.0/8")
              or ip in ipaddress.ip_network("172.16.0.0/12")
              or ip in ipaddress.ip_network("192.168.0.0/16")
              or ip in ipaddress.ip_network("100.64.0.0/10"))
        if not ok:
            raise ValueError(
                "host resolves outside the closed perimeter (" + str(ip) + "); "
                "this tool reaches loopback/LAN/tailnet only")
    return host.rstrip("/")


_OPENER = urllib.request.build_opener(_NoRedirect)


def load_tasks(n_classify: int, n_extract: int) -> list[dict]:
    """Closed-form tasks from real estate bytes; ground truth computed here.

    Bank richness law (the 2026-10-10 first live run's lesson: 3 tasks all
    truth=json saturate the null to 1.0 and the verdict is honestly
    NOISE-CLASS): extract tasks are drawn so their truths VARY (dates from
    row timestamps, extensions sampled distinctly, numbers from titles), and
    the run warns DEGENERATE-TASKBANK when distinct truths stay under 4."""
    tasks: list[dict] = []
    rows = []
    if LINKS.exists():
        for line in LINKS.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    for r in rows[-n_classify:]:
        title = str(r.get("title") or r.get("src") or "")[:120]
        if not title:
            continue
        words = re.findall(r"[a-zA-Z]{4,}", title.lower())
        truth = next((v for v in VOCAB if v in words), None)
        if truth is None:
            continue
        tasks.append({
            "shape": "classify", "prompt": (
                "Classify this work item title into exactly one category from this "
                "list: " + ", ".join(VOCAB) + ". Reply with ONLY the single category "
                "word, nothing else.\n\nTitle: " + title),
            "truth": truth, "source_title": title,
        })
    # date extraction: varied truths by construction (row timestamps)
    dated = [r for r in rows if re.search(r"\d{4}-\d{2}-\d{2}", str(r.get("ts") or ""))]
    for r in dated[-n_extract // 2:]:
        ts = re.search(r"\d{4}-\d{2}-\d{2}", str(r.get("ts"))).group(0)
        line_text = "Work record filed " + str(r.get("ts")) + " by " + str(
            r.get("author") or "a lane")[:60] + " titled " + str(r.get("title") or "")[:60]
        tasks.append({
            "shape": "extract-date", "prompt": (
                "Read this line and reply with ONLY the filing date in YYYY-MM-DD "
                "form, nothing else.\n\nLine: " + line_text),
            "truth": ts, "source_title": line_text[:80],
        })
    # extension extraction: sample DISTINCT extensions only
    srcs = [str(r.get("src") or "") for r in rows if r.get("src")]
    seen_ext: set[str] = set()
    chosen: list[str] = []
    for s in reversed(srcs):
        ext = Path(s).suffix.lstrip(".") or "none"
        if ext not in seen_ext:
            seen_ext.add(ext)
            chosen.append(s)
        if len(chosen) >= max(2, n_extract - n_extract // 2):
            break
    for s in chosen:
        ext = Path(s).suffix.lstrip(".") or "none"
        tasks.append({
            "shape": "extract-ext", "prompt": (
                "Read this file path and reply with ONLY its file extension (the "
                "part after the last dot, no dot, one word). If there is no dot, "
                "reply none.\n\nPath: " + s),
            "truth": ext, "source_title": s,
        })
    if not tasks:
        # Fleet-portability fallback (2026-10-10, the independent-builds order):
        # a phone or any bare box has no estate LINKS; the harness still runs,
        # on built-in fixtures with varied truths (the bank-richness law holds).
        fixtures = [
            ("classify", "Weekly memory vault repair and recall audit", "memory"),
            ("classify", "Router lane pricing and token budget review", "routing"),
            ("classify", "Threat model and gate hardening pass", "security"),
            ("extract-date",
             "Work record filed 2026-03-14T09:00:00Z by a lane titled census",
             "2026-03-14"),
            ("extract-date",
             "Work record filed 2026-07-02T18:30:00Z by a lane titled verkle",
             "2026-07-02"),
            ("extract-ext", "C:/logs/report.json", "json"),
            ("extract-ext", "/var/log/out.md", "md"),
            ("extract-ext", "results_page.py", "py"),
        ]
        shapes = {
            "classify": "Classify this work item title into exactly one category "
                        "from this list: " + ", ".join(VOCAB)
                        + ". Reply with ONLY the single category word, nothing "
                          "else.\n\nTitle: ",
            "extract-date": "Read this line and reply with ONLY the filing date "
                            "in YYYY-MM-DD form, nothing else.\n\nLine: ",
            "extract-ext": "Read this file path and reply with ONLY its file "
                           "extension (the part after the last dot, no dot, one "
                           "word). If there is no dot, reply none.\n\nPath: ",
        }
        for shape, text, truth in fixtures:
            tasks.append({"shape": shape, "prompt": shapes[shape] + text,
                          "truth": truth, "source_title": text[:60]})
    return tasks


def ask_model(host: str, model: str, prompt: str, timeout: int) -> str:
    body = json.dumps({
        "model": model, "stream": False, "temperature": 0, "num_predict": 48,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        host + "/api/chat", data=body, headers={"Content-Type": "application/json"})
    with _OPENER.open(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    return (data.get("message") or {}).get("content") or ""


def modal_consensus(answers: list[str]) -> tuple[str | None, int]:
    """(consensus_answer, votes) when a strict majority exists, else (None, max)."""
    c = Counter(answers)
    top, votes = c.most_common(1)[0]
    need = len(answers) // 2 + 1
    return (top, votes) if votes >= need else (None, votes)


def dead_salmon(matrix: list[list[str]]) -> float:
    """Bootstrap null for consensus (the label-shuffle class, honest at any n).

    Simulates B matrices where each model's answer at each task is drawn i.i.d.
    from THAT MODEL's empirical answer distribution - task alignment destroyed,
    distributions preserved - and returns the mean consensus rate under the
    null. Seeded (13), so it is replayable. The live rate beats this null by
    more than 0.15 = structure; near it = noise-class.

    Why not a per-model permutation of the row: with short rows or duplicate
    answers the permutation space collapses (seeds collide, identical rows are
    shift-invariant - both found by test fixtures 2026-10-10), and a majority
    of identical answers honestly stays a majority under any shuffle. The
    bootstrap null handles every case, including the constant-answer model
    whose null is rightly 1.0: a model that always says the same thing carries
    no alignment to break."""
    import random as _random
    if not matrix:
        return 0.0
    n = len(matrix[0])
    dists = []
    for row in matrix:
        c = Counter(row)
        total = sum(c.values()) or 1
        dists.append((list(c.keys()), [v / total for v in c.values()]))
    rng = _random.Random(13)
    sims = 200
    total_rate = 0.0
    for _ in range(sims):
        col_hits = 0
        for _j in range(n):
            col = [rng.choices(keys, weights)[0] for keys, weights in dists]
            ans, _ = modal_consensus(col)
            col_hits += int(ans is not None)
        total_rate += col_hits / n if n else 0.0
    return total_rate / sims


def run(args: argparse.Namespace) -> int:
    try:
        host = check_host(args.host)
    except ValueError as e:
        print("host refused: " + str(e), file=sys.stderr)
        return 2
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    if len(models) < 2:
        print("need >=2 models for consensus", file=sys.stderr)
        return 2
    # --questions (2026-10-15, row 44 linked-logs evidence): a JSONL bank of
    # {"prompt", "truth", "shape"} rows overrides the LINKS-derived bank so a
    # fixed question set is replayable; everything downstream (norm, modal
    # consensus, dead-salmon, ledger, summary) is unchanged.
    if args.questions:
        tasks = []
        for line in Path(args.questions).read_text(
                encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    else:
        tasks = load_tasks(args.classify, args.extract)
    if not tasks:
        print("no tasks built (LINKS.jsonl unreadable)", file=sys.stderr)
        return 2
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = OUT_ROOT / ts
    run_dir.mkdir(parents=True, exist_ok=True)
    run_id = "consensus-" + ts

    matrix: list[list[str]] = []
    per_model = {m: {"ask": 0, "agree": 0, "correct": 0} for m in models}
    rows: list[dict] = []
    for m in models:
        col: list[str] = []
        for t in tasks:
            try:
                raw = ask_model(host, m, t["prompt"], args.timeout)
            except Exception as e:  # noqa: BLE001 - a down model is data, not death
                raw = ""
                rows.append({"event": "model_error", "model": m, "err": str(e)[:120]})
            col.append(norm(raw))
            per_model[m]["ask"] += 1
        matrix.append(col)

    cons_hits = 0
    truth_hits = 0
    for j, t in enumerate(tasks):
        col = [matrix[i][j] for i in range(len(models))]
        ans, votes = modal_consensus(col)
        got_cons = ans is not None
        cons_hits += int(got_cons)
        correct = got_cons and ans == norm(t["truth"])
        truth_hits += int(correct)
        for i, m in enumerate(models):
            if col[i] and ans is not None and col[i] == ans:
                per_model[m]["agree"] += 1
            if col[i] == norm(t["truth"]):
                per_model[m]["correct"] += 1
        rows.append({
            "event": "task", "shape": t["shape"], "source": t["source_title"][:80],
            "truth": t["truth"], "answers": col, "consensus": ans,
            "votes": votes, "consensus_reached": got_cons, "consensus_correct": correct,
            "payout_delta": None,
            "payout_note": "A1 stub: staging endpoint pending; no assertion run",
        })
    rate = cons_hits / len(tasks)
    control = dead_salmon(matrix)
    distinct_truths = len({norm(t["truth"]) for t in tasks})
    degenerate = distinct_truths < 4
    by_shape: dict[str, list[int]] = {}
    for j, t in enumerate(tasks):
        ans, _ = modal_consensus([matrix[i][j] for i in range(len(models))])
        corr = ans is not None and ans == norm(t["truth"])
        by_shape.setdefault(t["shape"], [0, 0, 0])
        by_shape[t["shape"]][0] += int(ans is not None)
        by_shape[t["shape"]][1] += int(corr)
        by_shape[t["shape"]][2] += 1
    with (run_dir / "consensus_ledger.jsonl").open("w", encoding="utf-8") as fh:
        for m in models:
            p = per_model[m]
            fh.write(json.dumps({
                "run_id": run_id, "ts": ts, "model": m,
                "shape": "all", "asked": p["ask"],
                "agree_with_consensus": p["agree"], "correct": p["correct"],
            }) + "\n")
    (run_dir / "receipt.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    summary = {
        "run_id": run_id, "models": models, "tasks": len(tasks),
        "distinct_truths": distinct_truths,
        "consensus_rate": round(rate, 4),
        "consensus_correct_rate": round(truth_hits / len(tasks), 4),
        "dead_salmon_control_rate": round(control, 4),
        "by_shape": {k: {"consensus": v[0], "correct": v[1], "n": v[2]}
                     for k, v in by_shape.items()},
        "verdict": ("DEGENERATE-TASKBANK (distinct truths under 4; consensus "
                    "untestable)" if degenerate else
                    "STRUCTURE" if rate > control + 0.15 else
                    "WEAK" if rate > control else "NOISE-CLASS"),
        "a1_payout": "stub - staging endpoint pending GB",
        "coldest_vertex": "stdlib-only, CPU-class, LAN/tailnet host allowlist",
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="http://localhost:11434")
    ap.add_argument("--models", default="gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct")
    ap.add_argument("--classify", type=int, default=12)
    ap.add_argument("--extract", type=int, default=10)
    ap.add_argument("--questions", default=None)
    ap.add_argument("--timeout", type=int, default=180)
    return run(ap.parse_args())


if __name__ == "__main__":
    sys.exit(main())
