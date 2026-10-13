"""One-command envelope harvest for Task-agent fire data (B2-424).

Turns the B2-97 ready-to-fire card's prose harvest steps into one command:
per-agent metadata.json fields (status, createdAt, totalDurationMs,
totalTokens, totalToolUseCount) are clustered into waves by creation-time
gaps, summarized per wave (the B2-25 table shape), and the 1302/429 grep
counts are computed over the agent output files. Output is JSON.

Validation arm (--validate-b2-25): the first wave of the reference session
(sess_fd5ec147, lanes created 2026-09-26T11:24:57Z, all 10 completed) must
reproduce the B2-25 envelope re-measure numbers exactly: 37,386,533 tokens,
1229.9 s max duration, 109.4M tok/h. Anything else exits 1.

Usage:
  python tools/envelope_harvest.py --agents-dir <dir> --width-label width15
  python tools/envelope_harvest.py --agents-dir <dir> --validate-b2-25
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WAVE_GAP_MS = 300_000  # a creation gap over 5 minutes starts a new wave


def parse_ts(s: str) -> float:
    from datetime import datetime, timezone
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000.0


def load_agents(agents_dir: Path) -> list[dict]:
    out = []
    for mf in sorted(agents_dir.glob("agent_*/metadata.json")):
        try:
            d = json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            continue
        d["_dir"] = str(mf.parent)
        out.append(d)
    return out


def cluster_waves(agents: list[dict]) -> list[list[dict]]:
    def key(a):
        return parse_ts(a["createdAt"])

    agents = sorted(agents, key=key)
    waves: list[list[dict]] = []
    for a in agents:
        if not waves or key(a) - key(waves[-1][-1]) > WAVE_GAP_MS:
            waves.append([a])
        else:
            waves[-1].append(a)
    return waves


def summarize(wave: list[dict], label: str, idx: int) -> dict:
    done = [a for a in wave if a.get("status") == "completed"]
    toks = [int(a.get("totalTokens") or 0) for a in wave]
    durs = [round((int(a.get("totalDurationMs") or 0)) / 1000.0, 1) for a in wave]
    tools = [int(a.get("totalToolUseCount") or 0) for a in wave]
    created = [parse_ts(a["createdAt"]) for a in wave]
    completed = [parse_ts(a["completedAt"]) for a in done if a.get("completedAt")]
    start, end = min(created), (max(completed) if completed else max(created))
    window_h = (end - start) / 3_600_000.0
    total = sum(toks)
    tok_h = total / window_h if window_h > 0 else 0.0
    max_tok = max(toks) if toks else 0
    max_dur = max(durs) if durs else 0.0
    max_tok_lane = next((a.get("description", "")[:24] for a in wave
                         if int(a.get("totalTokens") or 0) == max_tok), "")
    return {
        "wave": idx,
        "label": label,
        "width": len(wave),
        "completed": len(done),
        "open": len(wave) - len(done),
        "tokens_total": total,
        "tokens_mean": round(total / len(wave)) if wave else 0,
        "tokens_max": max_tok,
        "tokens_max_lane": max_tok_lane,
        "dur_s_mean": round(sum(durs) / len(durs), 1) if durs else 0.0,
        "dur_s_max": max_dur,
        "tools_mean": round(sum(tools) / len(tools), 1) if tools else 0.0,
        "window_start": min(a["createdAt"] for a in wave),
        "window_end": max((a.get("completedAt") or a["createdAt"]) for a in wave),
        "window_h": round(window_h, 5),
        "tok_per_h": round(tok_h / 1e6, 1),
        "partial": len(done) != len(wave),
        "per_lane": [
            {"lane": a.get("description", "")[:24], "dur_s": d, "tokens": t, "tools": tl}
            for a, d, t, tl in sorted(zip(wave, durs, toks, tools),
                                      key=lambda x: -x[2])
        ],
    }


def grep_counts(agents_dir: Path) -> dict:
    counts = {"1302": {"files": 0, "hits": 0}, "429": {"files": 0, "hits": 0}}
    for mf in agents_dir.glob("agent_*/*"):
        if mf.name not in ("output.txt", "task.output"):
            continue
        try:
            txt = mf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for sig in counts:
            n = txt.count(sig)
            if n:
                counts[sig]["files"] += 1
                counts[sig]["hits"] += n
    return counts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--agents-dir", type=Path, required=True)
    ap.add_argument("--width-label", default="unlabeled")
    ap.add_argument("--output", type=Path, default=None, help="write JSON here (default stdout)")
    ap.add_argument("--limit", type=int, default=0, help="only the first N waves (0 = all)")
    ap.add_argument("--validate-b2-25", action="store_true")
    args = ap.parse_args(argv)

    agents = load_agents(args.agents_dir)
    if not agents:
        print(json.dumps({"ok": False, "error": "no metadata.json found"}))
        return 1
    waves = cluster_waves(agents)
    if args.limit:
        waves = waves[: args.limit]
    out = {
        "ok": True,
        "agents_dir": str(args.agents_dir),
        "width_label": args.width_label,
        "metadata_files": len(agents),
        "waves": [summarize(w, args.width_label, i + 1) for i, w in enumerate(waves)],
        "grep_1302_429": grep_counts(args.agents_dir),
    }
    if args.validate_b2_25:
        w1 = out["waves"][0]
        checks = {
            "tokens_total_37386533": w1["tokens_total"] == 37_386_533,
            "dur_max_1229_9": abs(w1["dur_s_max"] - 1229.9) < 0.05,
            "tok_h_109_4M": abs(w1["tok_per_h"] - 109.4) < 0.05,
            "width_10": w1["width"] == 10 and w1["completed"] == 10,
        }
        out["validation"] = {"target": "B2-25 wave 1", "checks": checks,
                             "pass": all(checks.values())}
    js = json.dumps(out, indent=1)
    if args.output:
        args.output.write_text(js + "\n", encoding="utf-8")
    else:
        print(js)
    if args.validate_b2_25 and not out["validation"]["pass"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
